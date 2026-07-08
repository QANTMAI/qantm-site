# qantm.ai — static site

Static replacement for the Replit-hosted Vite/Express SPA. Five pages, same
URLs, no build step at serve time (`build.py` regenerates the pages), full SEO
baked in: per-page titles/descriptions/canonicals/h1 (Bing-rule compliant),
Organization JSON-LD (founder, address, contact, 0penRX brand), llms.txt,
robots.txt, sitemap.xml, real 404.

- `INVENTORY.md` — the full pre-build inventory of qantm.ai, regenesis.qantm.ai,
  and 0penrx.org (what existed, what was preserved, what was deliberately dropped).
- `build.py` — regenerates the six HTML files; edit content there, not in the HTML.
- Preview: https://qantmai.github.io/qantm-site/
- **Cutover:** add a `CNAME` file containing `qantm.ai`, set Pages custom domain,
  then at the DNS host point `qantm.ai` A records to GitHub Pages
  (185.199.108.153 / 109.153 / 110.153 / 111.153) and `www` CNAME to
  `qantmai.github.io`. The Replit deployment stays live until DNS flips.
