# Go live: Replit → GitHub Pages for qantm.ai

The master checklist for pointing **qantm.ai** at this GitHub Pages build and
retiring the Replit site. Self-contained — follow it top to bottom. `DNS_CUTOVER.md`
has extra DNS detail if you want it.

**One golden rule:** at the DNS step you change **only the apex `A` record** (and
add `AAAA` + adjust `www`). **Do not touch `MX` or `TXT`** — those run your Google
Workspace email and your domain verifications. A-record changes don't affect email.

---

## Status — what's already done (verified 2026-07-11)

- ✅ Build is content-complete: Home, Services, Case Studies, About, Contact,
  Media all serve **200** on `https://qantmai.github.io/qantm-site/`, plus
  `sitemap.xml`, `robots.txt`, `404.html`.
- ✅ Sitemap/canonicals already use `https://qantm.ai/` — no URL changes needed.
- ✅ CI guards every change (build + provenance gate + drift check).
- ✅ IndexNow key `7cc8f59755982601c9f65dd2ff11a719.txt` is deployed.
- ⏳ **Not done (your call):** the DNS flip, and decommissioning Replit.

## Your current DNS (the rollback + do-not-touch reference)

| Record | Current value | At cutover |
|---|---|---|
| `A` @ (apex) | `34.111.179.208` ← rollback target | **replace** with GitHub IPs (below) |
| `CNAME` www | → `qantm.ai` | point to `qantmai.github.io` |
| `MX` | Google Workspace (`aspmx.l.google.com`, …) | **leave untouched** |
| `TXT` SPF | `v=spf1 include:dc-aa8e722993._spfm.qantm.ai ~all` | **leave untouched** |
| `TXT` | `google-site-verification: …` | **leave untouched** (keeps Search Console) |
| `TXT` | `replit-verify=…` | leave for now; remove in Phase 5 |

DNS is managed at **GoDaddy** (`ns05/ns06.domaincontrol.com`).

---

## Phase 0 — Pre-flight (5 min, do the day before)

- [ ] Open `https://qantmai.github.io/qantm-site/` and click through all six pages
      + the mobile menu. Confirm it's the site you want live.
- [ ] Confirm there's **no other public Replit page** that isn't in this build
      (this build has the six routes above; if Replit has more, tell me first).
- [ ] Confirm you can log in to **GoDaddy** (DNS) and **Google Search Console**.

## Phase 1 — Lower the TTL (the day before)

In **GoDaddy → My Products → qantm.ai → DNS**, edit the apex `A` record and the
`www` record and set **TTL = 600 seconds** (10 min). Save. Wait for the old TTL
to lapse. This shrinks the cutover window from hours to minutes.

## Phase 2 — The cutover (10 min of work + propagation)

### 2a. Repoint DNS at GoDaddy

**Delete** the apex `A` record `34.111.179.208`, then **add these** (Name = `@`):

```
A     @   185.199.108.153
A     @   185.199.109.153
A     @   185.199.110.153
A     @   185.199.111.153
AAAA  @   2606:50c0:8000::153
AAAA  @   2606:50c0:8001::153
AAAA  @   2606:50c0:8002::153
AAAA  @   2606:50c0:8003::153
```

**Edit `www`** → CNAME to `qantmai.github.io`.

> These four IPs are GitHub's published Pages addresses — confirm them against
> GitHub's current docs ("Managing a custom domain → apex domain") before saving.
> **Leave every `MX` and `TXT` record exactly as-is.**

### 2b. Tell GitHub about the domain

Once `dig +short qantm.ai` starts returning the `185.199.x` addresses, run:

```bash
gh api -X PUT repos/QANTMAI/qantm-site/pages -f cname=qantm.ai
```

(or: repo → Settings → Pages → Custom domain → `qantm.ai` → Save). This writes a
`CNAME` file to the repo and starts HTTPS certificate provisioning (minutes → up
to an hour). HTTP works immediately.

> Don't do 2b before 2a — setting the domain first makes the github.io URL
> redirect to qantm.ai while qantm.ai still points at Replit, i.e. the new build
> goes dark. That's why the repo has no `CNAME` file today.

## Phase 3 — Verify (once the cert is issued)

```bash
dig +short qantm.ai                      # → 185.199.108–111.153
curl -sI https://qantm.ai | head -1      # → HTTP/2 200
curl -s  https://qantm.ai/ | grep -c 'Qantm AI'
curl -sI https://www.qantm.ai | head -1  # → 200 / redirect to apex
```

- [ ] Visit qantm.ai + all six pages; confirm the **padlock** (valid HTTPS).
- [ ] In repo → Settings → Pages, tick **Enforce HTTPS** (available once the cert
      is ready).
- [ ] Send yourself a test email and reply to one — confirms MX untouched.

## Phase 4 — SEO / post-launch (same day)

- [ ] **Google Search Console** → your `qantm.ai` domain property (already
      DNS-verified, so it survives the cutover) → **Sitemaps** → submit
      `https://qantm.ai/sitemap.xml`. Then URL-inspect the homepage → *Request
      indexing*.
- [ ] **IndexNow** — ping the six URLs (key is already live):
```bash
KEY=7cc8f59755982601c9f65dd2ff11a719
for u in "" services case-studies about contact media; do
  curl -s "https://api.indexnow.org/indexnow?url=https://qantm.ai/$u&key=$KEY&keyLocation=https://qantm.ai/$KEY.txt" -o /dev/null -w "%{http_code} https://qantm.ai/$u\n"
done
```
- [ ] Spot-check that inbound links / bookmarks to the old site still resolve
      (URLs are identical, so they should).

## Phase 5 — Decommission Replit (after 24–48 h stable)

Only once qantm.ai has served cleanly from GitHub for a day or two:

- [ ] In the Replit project, **remove the qantm.ai custom-domain binding** so
      Replit stops claiming the domain.
- [ ] **Stop / archive** the Replit deployment. Keep the Repl itself as a backup
      for a few weeks — don't delete it yet.
- [ ] In GoDaddy, delete the now-obsolete `TXT` `replit-verify=…` record. (Leave
      SPF and google-site-verification.)

## Rollback (if anything looks wrong at any point)

```bash
# GoDaddy: delete the 4 A + 4 AAAA GitHub records, re-add:
A  @  34.111.179.208
# GitHub: release the custom domain so github.io keeps working:
gh api -X PUT repos/QANTMAI/qantm-site/pages -f cname=""
```
DNS reverts within the 600 s TTL you set in Phase 1. Nothing is lost — the build
stays live at the github.io URL throughout.
