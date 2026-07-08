# QANTM AI web-property inventory — 2026-07-08

Compiled before building this static replacement. Every fact below was verified
live (curl, DNS, real-browser rendering, JS-bundle analysis) on 2026-07-08.

## 1. qantm.ai (this site's predecessor)

- **Hosting:** Replit deployment — Vite React SPA served by Express
  (`x-powered-by: Express`, `via: 1.1 google`, GCLB IP 34.111.179.208).
  Sets a `visitId` cookie (server-side visit tracking).
- **Routes (React router):** `/`, `/services`, `/case-studies`, `/about`, `/contact` — exactly five.
- **Server APIs found in the bundle:**
  - `/api/case-studies` — WORKS: returns 54 items, but it is an **AI-news feed**
    (VentureBeat/MIT-TR-style headlines, categories "industry"/"research") mixed
    with 3 authored-looking case studies (Healthcare / Agriculture / Cybersecurity).
    Raw capture preserved at `docs/case-studies-api-capture.json`. NOT republished
    here — the three "case studies" need confirmation they are real engagements
    before they appear on a public page.
  - `/api/contact` — contact-form POST target (form dropped in this rebuild; replaced
    with mailto + Calendly, both already published channels).
  - `/api/chat` — a chat feature (not rebuilt; note if wanted, it needs a backend).
  - `/api/consultations/store` — consultation storage (Calendly link covers booking).
  - `/api/footer-content` — DEAD: returns the SPA HTML (footer text is baked in the bundle).
- **External integrations:** Calendly (`calendly.com/dr-seth-qantm` + widget.js),
  LinkedIn, Bluesky, Substack (Silicon Sands Studio).
- **Broken link on the live site:** the bundle references `https://risk.qantm.ai/auth` —
  DNS resolves (34.117.189.25) but nothing answers (connection fails). Any UI
  element pointing there is a dead CTA.
- **SEO state (why this rebuild exists):** 1 of 5 pages indexed (Google & Bing);
  every route shipped the same `<head>` canonicalized to `/`; body was an empty
  `<div id="root">` (no content for non-JS crawlers); unknown URLs returned
  200 + homepage (soft-404); `/llms.txt` returned homepage HTML; `summary_large_image`
  card with no `og:image`; GSC verified with ~294 crawl requests / 90 days —
  crawled but refused indexing, consistent with the canonical bug.
- **Assets preserved:** favicon.ico / favicon.png (219KB logo) / favicon-32x32 / favicon-16x16
  (downloaded from the live site into this repo).

## 2. regenesis.qantm.ai (browser-verified 2026-07-08)

- **"ReGenesis Discovery Engine"** — a full public SaaS property, same Replit ingress
  (34.111.179.208). The landing page is a REVENUE marketing surface: "Find. Score.
  Report. Decide. 13 engines, one platform" — property discovery/scoring with
  published membership plans (Explorer $0 · Analyst $199/mo · Investor Pro $299/mo ·
  Enterprise $799/mo, team seats +$99).
- **/admin-dashboard is auth-gated** (verified in-browser without signing in):
  "ADMIN ACCESS REQUIRED — sign in with your Google account." UI-level gate confirmed;
  API-level enforcement not probed from prod (the repo's
  SECURITY_KERNEL_IMPLEMENTATION.md is the right place to audit that — code-level).
- **SEO state:** the same SPA pattern as old qantm.ai — a ~1.5KB HTML shell, one shared
  head, no crawlable content. As a paid product's storefront it deserves the same
  treatment qantm.ai got: index + fully mark up the landing page, `noindex` the
  app/auth/admin routes. Recommend folding that into its migration.
- **GitHub migration exists:** `QANTMAI/REgenesis` (private) is a Python platform repo
  (Alembic, Dockerfile, GCP_DEPLOYMENT_GUIDE.md, MIGRATION_INVENTORY.md,
  PRE_MIGRATION_AUDIT.md, REPLIT_DEPLOYMENT_INSTRUCTIONS.md) — its Replit→GCP
  migration is its own documented track. **Out of scope for this repo.**

## 3. 0penrx.org

- GitHub Pages (`QANTMAI/0penRX` → qantmai.github.io, apex A records 185.199.108–111.153).
- Fully SEO'd this week: crawl-mesh internal links, truth-branched query titles,
  visible FAQs with schema parity, IndexNow (96 URLs accepted), GSC verified via
  file + meta tag, Bing rules (titles ≤70 / descriptions 25–160 / h1) pass on all
  97 pages. Cross-links: every 0penRX footer → qantm.ai; this site's footer +
  Organization JSON-LD (`brand`) → 0penrx.org.

## 4. DNS map (2026-07-08)

| Host | Points to | Serves |
|---|---|---|
| qantm.ai | A 34.111.179.208 (Replit/GCLB) | Vite/Express SPA (to be replaced by this repo) |
| www.qantm.ai | CNAME → qantm.ai | same |
| regenesis.qantm.ai | A 34.111.179.208 | ReGenesis Discovery Engine SPA |
| risk.qantm.ai | A 34.117.189.25 | **nothing answers** (dead deployment?) |
| 0penrx.org | A 185.199.108–111.153 (GitHub Pages) | 0penRX |
| www.0penrx.org | CNAME → qantmai.github.io | 0penRX |

## 5. Decisions taken in this rebuild (flag to change)

1. **Contact form → mailto + Calendly** (both already-published channels). A static
   site has no `/api/contact`; if a form is wanted, add Formspree later.
2. **Case-studies page ships without case studies** — honest intro + booking CTA —
   until the 3 authored items are confirmed real (see §1). No invented content.
3. **Chat feature not rebuilt** (needs a server; usage unknown).
4. **Team page keeps all four listed members** verbatim from the live site,
   including the two canine officers — published brand voice, easy to trim.
5. **URLs preserved exactly** (`/services`, `/about`, `/case-studies`, `/contact`)
   as extensionless files GitHub Pages serves at the bare path — zero redirects
   at cutover.
