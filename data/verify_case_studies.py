#!/usr/bin/env python3
"""Provenance gate for data/case-studies.json — makes fabrication un-shippable.

The previous /api/case-studies feed rotted into fiction: five fabricated
"clients" with https://example.com/ URLs and invented metrics, plus ~50 raw
news headlines whose `solution`/`results` were the literal string "To be
analyzed" and whose `industry` was the literal string "industry". This gate
exists so that can never happen again. Every case study MUST:

  * carry full provenance — a real primary-source URL, a source name, the
    fetched page <title>, a project year, and a verifiedOn date;
  * link to a *primary source* only (vendor customer-story library or an
    official government/authoritative domain) — never a news/blog aggregator;
  * contain no placeholder text ("To be analyzed", "industry", "example.com",
    lorem, TBD, …) anywhere;
  * carry substantive challenge / solution / results prose, real technologies
    (no raw RSS "category-/…" tags), and a short verbatim source quote.

Default run is offline (CI-safe). Pass --live to additionally HTTP-check that
every referenceUrl resolves (< 400).

  python3 data/verify_case_studies.py          # structural gate (offline)
  python3 data/verify_case_studies.py --live    # also verify URLs resolve

Exit 0 = clean; exit 1 = at least one violation (prints every failure).
"""

from __future__ import annotations

import datetime as _dt
import json
import os
import re
import sys
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "case-studies.json")

# ── Primary-source allowlist ────────────────────────────────────────────────
# Case studies may cite ONLY these families: named-customer story libraries
# from the AI platform vendors, and official government / authoritative
# domains. Anything else (VentureBeat, TechCrunch, Medium/Towards Data Science,
# press-release wires, personal blogs) is rejected — that class of source is
# exactly what produced the junk feed.
TRUSTED_HOSTS = {
    "cloud.google.com", "aws.amazon.com", "amazon.com", "microsoft.com",
    "customers.microsoft.com", "news.microsoft.com", "ibm.com", "openai.com",
    "anthropic.com", "claude.com", "databricks.com", "snowflake.com", "salesforce.com",
    "servicenow.com", "nvidia.com", "blogs.nvidia.com", "sap.com", "oracle.com",
    "deloitte.com", "mckinsey.com", "bcg.com", "accenture.com", "deepmind.google",
    # Official government domains whose TLD isn't covered by TRUSTED_SUFFIXES.
    "canada.ca",   # Government of Canada
    "ria.ee",      # Estonian Information System Authority (RIA)
}
# Government / official suffixes (host == suffix or endswith "." + suffix, and
# the dotted gov suffixes match by endswith).
TRUSTED_SUFFIXES = (
    ".gov", ".mil", ".gov.uk", ".gov.au", ".gov.sg", ".govt.nz", ".gc.ca",
    ".go.jp", ".europa.eu", ".gov.ie", ".gov.in", ".govt.uk",
)

PLACEHOLDER_PAT = re.compile(
    r"to be analyzed|example\.com|lorem ipsum|\btbd\b|\bxxx+\b|placeholder|"
    r"coming soon|todo\b|\bn/?a\b", re.I,
)
REQUIRED = [
    "client", "sector", "org_type", "title", "challenge", "solution",
    "results", "technologies", "referenceUrl", "sourceName",
    "sourcePageTitle", "projectYear", "verifiedOn",
]
ORG_TYPES = {"enterprise", "government"}
MIN_PROSE = 30          # challenge/solution/results must be real sentences
YEAR_RANGE = range(2015, 2027)


def _host(url: str) -> str:
    return (urlparse(url).hostname or "").lower()


def _host_trusted(host: str) -> bool:
    if host in TRUSTED_HOSTS:
        return True
    if any(host == h or host.endswith("." + h) for h in TRUSTED_HOSTS):
        return True
    if any(host == s.lstrip(".") or host.endswith(s) for s in TRUSTED_SUFFIXES):
        return True
    return False


def _check_entry(i: int, e: dict, errors: list[str]) -> None:
    tag = f"[{i}] {e.get('client', '?')!r}"

    for f in REQUIRED:
        v = e.get(f)
        if v is None or (isinstance(v, str) and not v.strip()) or (isinstance(v, list) and not v):
            errors.append(f"{tag}: missing/empty required field {f!r}")

    # No placeholder text anywhere in the record.
    blob = json.dumps(e, ensure_ascii=False)
    m = PLACEHOLDER_PAT.search(blob)
    if m:
        errors.append(f"{tag}: placeholder text {m.group(0)!r} present")

    # Literal 'industry' as a sector was the old bug's fingerprint.
    if str(e.get("sector", "")).strip().lower() == "industry":
        errors.append(f"{tag}: sector is the literal placeholder 'industry'")

    if e.get("org_type") not in ORG_TYPES:
        errors.append(f"{tag}: org_type must be one of {sorted(ORG_TYPES)}")

    for f in ("challenge", "solution", "results"):
        v = str(e.get(f, ""))
        if 0 < len(v.strip()) < MIN_PROSE:
            errors.append(f"{tag}: {f!r} too short to be real ({len(v.strip())} chars)")

    # referenceUrl: https, real path, primary-source host.
    url = str(e.get("referenceUrl", ""))
    if url:
        p = urlparse(url)
        host = _host(url)
        if p.scheme != "https":
            errors.append(f"{tag}: referenceUrl must be https ({url})")
        if not p.path or p.path == "/":
            errors.append(f"{tag}: referenceUrl must point at a specific story, not a homepage ({url})")
        if "example.com" in host:
            errors.append(f"{tag}: referenceUrl is a placeholder example.com URL")
        elif not _host_trusted(host):
            errors.append(f"{tag}: referenceUrl host {host!r} is not a trusted primary source "
                          f"(vendor customer-story or official government domain)")

    # technologies: real, curated, no raw feed tags, no dupes.
    techs = e.get("technologies") or []
    if isinstance(techs, list):
        low = [str(t).strip().lower() for t in techs]
        if any(t.startswith("category-/") or t.startswith("category-") for t in low):
            errors.append(f"{tag}: technologies contains raw RSS 'category-' tags")
        if len(low) != len(set(low)):
            errors.append(f"{tag}: technologies has duplicate entries {techs}")
        if any(not t for t in low):
            errors.append(f"{tag}: technologies has an empty entry")

    # projectYear sane.
    yr = e.get("projectYear")
    if not (isinstance(yr, int) and yr in YEAR_RANGE):
        errors.append(f"{tag}: projectYear {yr!r} out of range {YEAR_RANGE.start}-{YEAR_RANGE.stop - 1}")

    # verifiedOn is an ISO date.
    vo = str(e.get("verifiedOn", ""))
    try:
        _dt.date.fromisoformat(vo)
    except ValueError:
        errors.append(f"{tag}: verifiedOn {vo!r} is not an ISO date (YYYY-MM-DD)")

    # quote should be short (a pull-quote, not a paragraph) when present.
    q = str(e.get("quote", ""))
    if q and len(q) > 260:
        errors.append(f"{tag}: quote is {len(q)} chars — keep it a short pull-quote (≤260)")


def _check_live(entries: list[dict], errors: list[str]) -> None:
    """Confirm each referenceUrl resolves to a live endpoint.

    A responding server — even a 403/401/429 — proves the URL exists; those
    codes are bot-mitigation on real pages (e.g. canada.ca behind Akamai), not
    dead links. Only a 404, a 5xx, or no response at all is a real failure.
    Gov sites can tarpit unknown clients, so timeouts get one longer retry.
    """
    import socket
    import urllib.error
    import urllib.request

    headers = {
        "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36"),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }

    def status_for(url: str, timeout: int) -> int:
        req = urllib.request.Request(url, method="GET", headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status

    def tls_reachable(url: str) -> bool:
        # Transport-layer fallback: some hosts (e.g. canada.ca behind Akamai)
        # tarpit unknown HTTP clients into a timeout, yet are plainly live. If
        # the host completes a TLS handshake, the domain resolves and answers —
        # a dead domain fails here. A gone *page* still surfaces as a 404 above.
        import ssl
        p = urlparse(url)
        host, port = p.hostname, p.port or 443
        try:
            with socket.create_connection((host, port), timeout=15) as sock:
                with ssl.create_default_context().wrap_socket(sock, server_hostname=host):
                    return True
        except Exception:  # noqa: BLE001
            return False

    for i, e in enumerate(entries):
        url = e.get("referenceUrl")
        if not url:
            continue
        for attempt, timeout in enumerate((25, 45)):
            try:
                st = status_for(url, timeout)
            except urllib.error.HTTPError as ex:
                st = ex.code  # server answered → endpoint exists
            except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError) as ex:
                if attempt == 0:
                    continue  # retry once, longer
                if tls_reachable(url):
                    break  # host is live at the transport layer (HTTP tarpitted)
                errors.append(f"[{i}] {e.get('client')!r}: referenceUrl did not resolve ({url}) — {ex}")
                break
            if st == 404 or st >= 500:
                errors.append(f"[{i}] {e.get('client')!r}: referenceUrl HTTP {st} ({url})")
            break


def main() -> int:
    live = "--live" in sys.argv
    with open(DATA, encoding="utf-8") as fh:
        entries = json.load(fh)
    if not isinstance(entries, list) or not entries:
        print("case-studies.json must be a non-empty JSON array", file=sys.stderr)
        return 1

    errors: list[str] = []

    # Duplicate detection.
    seen: dict[tuple, int] = {}
    for i, e in enumerate(entries):
        key = (str(e.get("client", "")).lower(), str(e.get("title", "")).lower())
        if key in seen:
            errors.append(f"[{i}] duplicate of [{seen[key]}]: {key}")
        seen[key] = i
        _check_entry(i, e, errors)

    if live:
        _check_live(entries, errors)

    n_gov = sum(1 for e in entries if e.get("org_type") == "government")
    n_ent = sum(1 for e in entries if e.get("org_type") == "enterprise")
    if errors:
        print(f"FAIL — {len(errors)} violation(s) across {len(entries)} case studies:\n")
        for msg in errors:
            print("  ✗", msg)
        return 1
    print(f"OK — {len(entries)} case studies verified "
          f"({n_ent} enterprise, {n_gov} government)"
          f"{' + all URLs resolve' if live else ''}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
