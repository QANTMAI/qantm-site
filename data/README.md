# Case-studies dataset

`case-studies.json` powers the **/case-studies** page: a curated, source-verified
briefing of how leading enterprises and governments deploy AI, and the results
they report. It replaces the old `/api/case-studies` feed, which had rotted into
fabricated "clients" (fictional companies with `example.com` URLs and invented
metrics) plus raw AI-news headlines whose `solution`/`results` were the literal
string *"To be analyzed"*.

## The rule: primary source or it doesn't ship

Every entry is a **real, named** enterprise or government AI deployment drawn
from a **primary source** — a vendor customer-story library (Google Cloud, AWS,
Microsoft, Snowflake, Databricks, Anthropic, …) or an official government page
(`*.gov`, `*.gov.uk`, `europa.eu`, …). No news aggregators, no blogs, no
press-release wires — that class of source is exactly what produced the junk.

Qantm AI **curates and independently verifies** these; it does **not** claim to
have delivered them. Each card links to its original source.

## Schema (per entry)

| field | meaning |
|---|---|
| `client` | the real named organization or agency |
| `sector` | canonical sector bucket (drives the filter chips) |
| `org_type` | `enterprise` or `government` |
| `country` | where the deployment happened (may be `""`) |
| `title` | concise case-study title |
| `challenge` / `solution` / `results` | faithful summaries from the source |
| `metric` | the single headline outcome, as stated (may be `""`) |
| `quote` | a short verbatim pull-quote from the source page |
| `technologies` | curated real tech (no raw RSS tags) |
| `vendor` | the AI platform/partner named (may be `""`) |
| `referenceUrl` | the real, reachable story/source URL |
| `sourceName` | the publisher (e.g. "AWS Customer Stories") |
| `sourcePageTitle` | the fetched page's `<title>` — proof it was read |
| `projectYear` | year of the deployment/publication |
| `verifiedOn` | ISO date the entry was last checked |

## The gate — makes fabrication un-shippable

`python3 data/verify_case_studies.py` runs on every build (and should run in CI).
It fails if **any** entry has a placeholder URL/text, a non-primary-source host,
a missing provenance field, a literal `industry` sector, raw `category-/` tech
tags, an out-of-range year, or a duplicate. Add `--live` to also confirm every
`referenceUrl` resolves (`< 400`).

## Refreshing (keeping it "the latest")

Freshness is by **re-verification against primary sources**, never by scraping
news. To refresh:

1. Gather new verified entries from the primary-source families above — each
   entry's `referenceUrl` must be **fetched and confirmed** to contain the named
   client and the stated outcome (capture the page `<title>` as `sourcePageTitle`
   and a verbatim `quote`).
2. Update `verifiedOn` on any entry you re-confirm; drop anything whose source
   has gone dead or changed.
3. `python3 data/verify_case_studies.py --live` — must print **OK**.
4. `python3 build.py` — regenerates `case-studies.html` (the gate also runs here).

Because the page is generated statically, the case studies are visible to search
engines and never depend on a runtime fetch that can fail.
