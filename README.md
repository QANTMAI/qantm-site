# qantm.ai — static site

The live **qantm.ai** site, served by **GitHub Pages** (`QANTMAI/qantm-site`) —
it replaced the former Replit-hosted Vite/Express SPA. Six pages, same URLs, no
build step at serve time (`build.py` regenerates the pages), full SEO baked in:
per-page titles/descriptions/canonicals/h1 (Bing-rule compliant), Organization
JSON-LD (founder, contact point, 0penRX brand), llms.txt, robots.txt,
sitemap.xml, real 404.

- `INVENTORY.md` — the full pre-build inventory of qantm.ai, regenesis.qantm.ai,
  and 0penrx.org (what existed, what was preserved, what was deliberately dropped).
- `build.py` — regenerates the six HTML files; edit content there, not in the HTML.
- Live: https://qantm.ai
- **Status — live on GitHub Pages since 2026-07-11.** Apex `qantm.ai` A records →
  185.199.108–111.153, `www` CNAME → `qantmai.github.io`, HTTPS enforced, `CNAME`
  file = `qantm.ai`. DNS is fully cut over; the site no longer depends on Replit.
  Final Replit-dashboard cleanup (owner-only): `docs/GO_LIVE.md` Phase 5.
