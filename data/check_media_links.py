#!/usr/bin/env python3
"""Link + structure gate for data/media-catalog.json.

The Media page (Dr. Seth Dobrin's press, talks, podcasts, and profiles) is
generated from data/media-catalog.json. Unlike case-studies.json — which cites a
small allowlist of trusted vendor/government sources — these links point across
the open web: event pages, publishers, podcast platforms, personal profiles.
Those rot over time (an event ends and its speaker page 404s), so this gate keeps
the page honest:

  * structural (offline, CI-safe): valid JSON; every group has a name and a
    non-empty items list; every item has a title, a detail, and an http(s) url;
    no placeholder text.
  * live (--live): every url still resolves. A responding server — even a
    401/403/405/406/429/5xx — proves the endpoint exists; publishers and podcast
    platforms (Apple Podcasts 5xx, Wiley/SAGE/Medium 403, LinkedIn 999) routinely
    bot-block automated clients that way, while the page is perfectly live in a
    browser. Only an explicit 404/410 ("Not Found"/"Gone"), or a host that
    answers nothing at all AND fails a TLS handshake, is a dead link. This is the
    deliberate difference from verify_case_studies.py, whose curated trusted-host
    set makes a 5xx genuinely suspicious; here it is just bot-mitigation.

  python3 data/check_media_links.py           # structural gate (offline)
  python3 data/check_media_links.py --live      # also verify every url resolves

Exit 0 = clean; exit 1 = at least one violation (prints every failure).
"""

from __future__ import annotations

import json
import os
import re
import socket
import ssl
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "media-catalog.json")

PLACEHOLDER_PAT = re.compile(
    r"example\.com|lorem ipsum|\btbd\b|\bxxx+\b|placeholder|coming soon|todo\b",
    re.I,
)

# Codes that prove the endpoint exists (server answered) — never "dead". 4xx
# other than 404/410 and every 5xx are bot-mitigation or transient server state,
# not a missing resource. Only 404 (Not Found) and 410 (Gone) mean the link is
# dead.
DEAD_STATUSES = {404, 410}

_HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36"),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def _iter_items(groups):
    """Yield (group_name, item) for every item, in file order."""
    for g in groups:
        for it in g.get("items", []):
            yield g.get("name", "?"), it


def _check_structure(groups, errors):
    for gi, g in enumerate(groups):
        gname = g.get("name")
        if not gname or not str(gname).strip():
            errors.append(f"group[{gi}]: missing/empty 'name'")
        items = g.get("items")
        if not isinstance(items, list) or not items:
            errors.append(f"group {gname!r}: 'items' must be a non-empty list")
            continue
        for ii, it in enumerate(items):
            tag = f"[{gname} #{ii}]"
            for f in ("title", "detail", "url"):
                v = it.get(f)
                if not v or not str(v).strip():
                    errors.append(f"{tag}: missing/empty {f!r}")
            blob = json.dumps(it, ensure_ascii=False)
            m = PLACEHOLDER_PAT.search(blob)
            if m:
                errors.append(f"{tag}: placeholder text {m.group(0)!r} present")
            url = str(it.get("url", ""))
            if url:
                scheme = urlparse(url).scheme
                if scheme not in ("http", "https"):
                    errors.append(f"{tag}: url scheme {scheme!r} is not http(s) ({url})")


def _status_for(url: str, timeout: int) -> int:
    req = urllib.request.Request(url, method="GET", headers=_HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status


def _tls_reachable(url: str) -> bool:
    """Transport-layer fallback: some hosts tarpit unknown HTTP clients into a
    timeout yet are plainly live. A completed TLS handshake proves the domain
    resolves and answers; a dead domain fails here. A gone *page* still surfaces
    as a 404/410 at the HTTP layer above."""
    p = urlparse(url)
    host, port = p.hostname, (p.port or (443 if p.scheme == "https" else 80))
    try:
        with socket.create_connection((host, port), timeout=15) as sock:
            if p.scheme != "https":
                return True
            with ssl.create_default_context().wrap_socket(sock, server_hostname=host):
                return True
    except Exception:  # noqa: BLE001
        return False


def _liveness(url: str):
    """Return None if the link is live/answering, else a short reason string."""
    for attempt, timeout in enumerate((25, 45)):
        try:
            st = _status_for(url, timeout)
        except urllib.error.HTTPError as ex:
            st = ex.code  # the server answered → the endpoint exists
        except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError) as ex:
            if attempt == 0:
                continue  # one longer retry for a slow/tarpitting host
            return None if _tls_reachable(url) else f"no response — {ex}"
        return f"HTTP {st}" if st in DEAD_STATUSES else None
    return None


def _check_live(groups, errors):
    records = list(_iter_items(groups))

    def worker(rec):
        gname, it = rec
        return gname, it, _liveness(str(it.get("url", "")))

    with ThreadPoolExecutor(max_workers=10) as pool:
        for gname, it, reason in pool.map(worker, records):
            if reason:
                errors.append(f"[{gname}] {it.get('title')!r}: {reason} ({it.get('url')})")


def main() -> int:
    live = "--live" in sys.argv
    with open(DATA, encoding="utf-8") as fh:
        groups = json.load(fh)
    if not isinstance(groups, list) or not groups:
        print("media-catalog.json must be a non-empty JSON array of groups", file=sys.stderr)
        return 1

    errors: list[str] = []
    _check_structure(groups, errors)
    if live and not errors:
        # Only spend the network budget once the structure is sound.
        _check_live(groups, errors)

    n_items = sum(1 for _ in _iter_items(groups))
    if errors:
        print(f"FAIL — {len(errors)} violation(s) across {len(groups)} groups / {n_items} items:\n")
        for msg in errors:
            print("  ✗", msg)
        return 1
    print(f"OK — {len(groups)} groups / {n_items} media items verified"
          f"{' + all links resolve' if live else ''}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
