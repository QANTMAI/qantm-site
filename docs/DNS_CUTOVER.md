# DNS cutover — point qantm.ai at this GitHub Pages build

Everything on the GitHub side is prepared. This is the runbook for the final
flip. **Nothing here is done automatically** — the DNS change happens in your
GoDaddy account, and it's the moment qantm.ai leaves its current host, so it's
yours to trigger.

> **Verify the two IP lists below against GitHub's current docs before you run
> this** — search "GitHub Pages Managing a custom domain → apex domain". GitHub's
> Pages IPs are stable but this doc should never be the source of truth for them.

## Ground truth (checked 2026-07-11)

| Thing | Value |
|---|---|
| DNS host for qantm.ai | **GoDaddy** (`ns05.domaincontrol.com`, `ns06.domaincontrol.com`) |
| Current apex `A` record | `34.111.179.208` ← save this, it's the rollback target |
| Current `www` | CNAME → `qantm.ai` |
| Pages repo | `QANTMAI/qantm-site` (project site) |
| Pages status | built, HTTPS enforced, **no custom domain set** (`cname: null`) |

## What the flip does

qantm.ai currently resolves to `34.111.179.208`. After the flip it resolves to
GitHub Pages, which serves the content of this repo at the domain root
(`qantm.ai/`, not `/qantm-site/`).

Apex domains can't be a CNAME, so the apex uses **A/AAAA records** to GitHub's
Pages IPs; `www` uses a CNAME to the Pages host.

## Step 1 — (a day ahead) lower the TTL

In GoDaddy DNS for qantm.ai, set the TTL on the apex `A` record and the `www`
record to **600 seconds**. Wait for the old TTL to expire. This keeps the
cutover window to minutes instead of hours.

## Step 2 — repoint DNS at GoDaddy

Replace the apex records. In **GoDaddy → Domains → qantm.ai → DNS**:

**Delete** the apex `A` record pointing to `34.111.179.208`, then **add** four
`A` records (Name `@`) and four `AAAA` records:

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

**Set `www`** to a CNAME → `qantmai.github.io` (Name `www`, Value
`qantmai.github.io`).

## Step 3 — tell GitHub Pages about the domain

Do this right after DNS starts propagating (`dig +short qantm.ai` returns the
185.199.x addresses). Two equivalent options:

**Option A — one command (recommended):**
```bash
gh api -X PUT repos/QANTMAI/qantm-site/pages -f cname=qantm.ai -F https_enforced=true
```

**Option B — the UI:** repo → Settings → Pages → Custom domain → enter
`qantm.ai` → Save.

Either way GitHub writes a `CNAME` file (containing `qantm.ai`) to the repo. It
then starts provisioning a Let's Encrypt certificate — this can take a few
minutes up to an hour. HTTP works immediately; **"Enforce HTTPS" becomes
available once the cert is issued** — tick it then.

> Do **not** create the `CNAME` file or set the custom domain before the DNS is
> pointed at GitHub. Doing so makes `qantmai.github.io/qantm-site` redirect to
> qantm.ai while qantm.ai still points at the old host — i.e. the new build
> becomes unreachable. That's why this repo intentionally has **no `CNAME` file
> today**.

## Step 4 — verify

```bash
dig +short qantm.ai                 # → 185.199.108-111.153
curl -sI https://qantm.ai | head -1 # → HTTP/2 200
curl -s  https://qantm.ai/ | grep -c 'Qantm AI'   # content served
curl -sI https://www.qantm.ai | head -1           # www → redirects/serves
```

Also click through Home / Services / Case Studies / Media / About / Contact and
confirm the padlock (valid HTTPS).

## Rollback

If anything is wrong, restore the old apex record in GoDaddy:

```
A  @  34.111.179.208     (delete the four GitHub A records + AAAA records)
```

…and clear the custom domain so github.io keeps working:

```bash
gh api -X PUT repos/QANTMAI/qantm-site/pages -f cname=""
```

DNS reverts within the TTL you set in Step 1.

## After a successful cutover

- Update `robots.txt` / `sitemap.xml` if any absolute URLs need to be canonical
  to `https://qantm.ai` (they already are — `SITE = "https://qantm.ai"` in
  build.py).
- Submit the sitemap in Google Search Console for `qantm.ai`.
- Decommission the old Replit deployment once qantm.ai is confirmed stable.
