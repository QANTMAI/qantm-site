#!/usr/bin/env python3
"""Generate the Qantm AI static site: 5 pages + 404, shared head/nav/footer.

Content is transcribed from the live qantm.ai rendered pages (2026-07-08) —
nothing invented. URLs match the live SPA exactly (/services, /about,
/case-studies, /contact as extensionless .html files GitHub Pages serves at
the bare path). Run:  python3 build.py
"""

import json

SITE = "https://qantm.ai"

ORG_JSONLD = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "Qantm AI",
    "alternateName": "QANTM AI",
    "url": SITE,
    "logo": f"{SITE}/favicon.png",
    "description": "AI strategy, governance, and implementation consulting — AI iQ™ readiness assessments, governance & ethics alignment, executive education, and GenAI/ML implementation.",
    "email": "info@qantm.ai",
    "contactPoint": {"@type": "ContactPoint", "email": "info@qantm.ai", "contactType": "sales", "availableLanguage": "English"},
    "founder": {"@type": "Person", "name": "Seth Dobrin", "honorificPrefix": "Dr.", "jobTitle": "CEO & AI Strategist"},
    "employee": [
        {"@type": "Person", "name": "Seth Dobrin", "honorificPrefix": "Dr.", "jobTitle": "CEO & AI Strategist"},
        {"@type": "Person", "name": "Tabitha Rudd", "jobTitle": "COO"},
    ],
    "brand": {"@type": "Brand", "name": "0penRX", "url": "https://0penrx.org"},
    "knowsAbout": ["AI Governance", "AI Strategy", "Machine Learning", "AI Implementation", "AI Ethics", "AI Risk Assessment"],
    "serviceArea": {"@type": "Place", "name": "Worldwide"},
    "sameAs": [
        "https://www.linkedin.com/company/qantm-ai/",
        "https://bsky.app/profile/qantmai.bsky.social",
        "https://siliconsandstudio.substack.com/",
        "https://github.com/QANTMAI",
    ],
}

EMAIL = "mailto:info@qantm.ai"

NAV = [("Home", "/"), ("Services", "/services"), ("Case Studies", "/case-studies"), ("Media", "/media"), ("About", "/about"), ("Contact", "/contact")]


def jsonld(extra=None):
    graph = [ORG_JSONLD] + (extra or [])
    body = json.dumps(graph if len(graph) > 1 else graph[0], ensure_ascii=False, separators=(",", ":"))
    return body.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")


def page(path, title, desc, h1, body, extra_ld=None, noindex=False):
    canonical = f"{SITE}{path if path != '/' else '/'}"
    CUR = ' aria-current="page"'
    nav_parts = []
    for label, href in NAV:
        rel = "./" if href == "/" else "." + href
        cur = CUR if href == path else ""
        cls = ' class="contact-btn"' if href == "/contact" else ""
        nav_parts.append(f'<a href="{rel}"{cls}{cur}>{label}</a>')
    nav = "".join(nav_parts)
    robots = '<meta name="robots" content="noindex, nofollow">' if noindex else '<meta name="robots" content="index, follow, max-snippet:-1">'  # noqa: E501
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/favicon.png">
<meta name="twitter:card" content="summary">
<link rel="icon" type="image/x-icon" href="./favicon.ico">
<link rel="icon" type="image/png" sizes="32x32" href="./favicon-32x32.png">
<link rel="apple-touch-icon" href="./favicon.png">
<link rel="stylesheet" href="./assets/styles.css">
<script type="application/ld+json">{jsonld(extra_ld)}</script>
</head>
<body>
<header>
  <div class="hdr">
    <a class="logo" href="./"><img src="./assets/img/logo.png" alt="Qantm AI — Next Level AI Solutions" width="112" height="50"></a>
    <nav class="main" aria-label="Main">{nav}</nav>
  </div>
</header>
<main class="wrap">
<h1{' class="sr"' if not h1[1] else ''}>{h1[0]}</h1>
{body}
</main>
<footer>
  <div class="wrap">
    <div class="cols">
      <nav aria-label="Footer">
        <a href="./">Home</a><a href="./services">Services</a><a href="./case-studies">Case Studies</a><a href="./about">About</a><a href="./contact">Contact</a>
      </nav>
      <nav aria-label="Elsewhere">
        <a href="https://www.linkedin.com/company/qantm-ai/" rel="noopener">LinkedIn</a>
        <a href="https://siliconsandstudio.substack.com/" rel="noopener">Substack</a>
        <a href="https://github.com/QANTMAI" rel="noopener">GitHub</a>
        <a href="https://0penrx.org" rel="noopener">0penRX</a>
      </nav>
    </div>
    <p class="copy">&copy; 2026 Qantm AI, LLC. All rights reserved. &middot; <a href="mailto:info@qantm.ai">info@qantm.ai</a> &middot; <a href="https://0penrx.org">0penRX — free prescription price transparency</a></p>
  </div>
</footer>
</body>
</html>
"""


# lucide icons (MIT) — path data captured verbatim from the live qantm.ai cards.
ICONS = {
    "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/>',
    "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "cog": '<path d="M12 20a8 8 0 1 0 0-16 8 8 0 0 0 0 16Z"/><path d="M12 14a2 2 0 1 0 0-4 2 2 0 0 0 0 4Z"/><path d="M12 2v2"/><path d="M12 22v-2"/><path d="m17 20.66-1-1.73"/><path d="M11 10.27 7 3.34"/><path d="m20.66 17-1.73-1"/><path d="m3.34 7 1.73 1"/><path d="M14 12h8"/><path d="M2 12h2"/><path d="m20.66 7-1.73 1"/><path d="m3.34 17 1.73-1"/><path d="m17 3.34-1 1.73"/><path d="m11 13.73-4 6.93"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "brain": '<path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"/><path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z"/><path d="M15 13a4.5 4.5 0 0 1-3-4 4.5 4.5 0 0 1-3 4"/><path d="M17.599 6.5a3 3 0 0 0 .399-1.375"/><path d="M6.003 5.125A3 3 0 0 0 6.401 6.5"/><path d="M3.477 10.896a4 4 0 0 1 .585-.396"/><path d="M19.938 10.5a4 4 0 0 1 .585.396"/><path d="M6 18a4 4 0 0 1-1.967-.516"/><path d="M19.967 17.484A4 4 0 0 1 18 18"/>',
    "sparkles": '<path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z"/><path d="M20 3v4"/><path d="M22 5h-4"/><path d="M4 17v2"/><path d="M5 18H3"/>',
    "code": '<polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>',
    "lightbulb": '<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/>',
    "chart": '<line x1="12" x2="12" y1="20" y2="10"/><line x1="18" x2="18" y1="20" y2="4"/><line x1="6" x2="6" y1="20" y2="16"/>',
}


def _icon(name):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


def _tile(color, icon, title, body):
    ic = _icon(icon) if icon else ""
    return f'<div class="tile tile--{color}">{ic}<h3>{title}</h3>{body}</div>'


def _team(color, img, name, role, desc):
    return (f'<div class="team-card tile--{color}">'
            f'<img src="./assets/img/{img}.png" alt="{name}" width="118" height="118" loading="lazy">'
            f'<h3>{name}</h3><p class="role">{role}</p><p>{desc}</p></div>')


# (title, description, brand colour, icon) — colours/icons read from the live site.
OFFERINGS = [
    ("AI iQ™ Governance & Ethics Alignment", "Ensuring your AI initiatives align with the highest ethical standards", "red", "shield"),
    ("AI iQ™ Readiness Assessment", "Discover how ready your organization is to leap into the AI revolution", "navy", "target"),
    ("AI iQ™ Strategy Development", "Crafting a winning strategy tailored to your unique aspirations", "gold", "cog"),
    ("AI iQ™ Executive Education", "Empowering your leadership with AI landscape navigation skills", "pink", "users"),
    ("AI iQ™ GenAI Capability Tuning", "Fine-tuning your generative AI capabilities for maximum impact", "cyan", "brain"),
    ("AI iQ™ GenAI/ML Implementation", "Achieving excellence in AI and machine learning operations", "purple", "sparkles"),
]

home_body = f"""
<div class="hero">
  <p>Leading the way in artificial intelligence, with a leadership team bringing decades of success in AI strategy, governance, and development.</p>
  <div class="cta-row">
    <a class="btn pri" href="{EMAIL}">Get Started Today</a>
    <a class="btn blue" href="{EMAIL}">Contact Us</a>
  </div>
</div>
<section id="offerings">
  <h2>Our Tailored Offerings</h2>
  <div class="tiles">
{"".join('    ' + _tile(c, i, t, f'<p>{d}</p>') + chr(10) for t, d, c, i in OFFERINGS)}  </div>
</section>
<section id="ethics">
  <h2>Ethical AI Governance</h2>
  <p class="lede">At Qantm AI, we put ethical practices front and center in every engagement. Our comprehensive governance frameworks and robust data privacy safeguards ensure transparency and fairness&mdash;because in this fast-paced world, integrity is always in vogue!</p>
</section>
<section id="cta">
  <h2>Join the AI Revolution!</h2>
  <p class="lede">Contact Qantm AI today to discover how our tailor-made solutions can elevate your organization into the bright future of technology.</p>
  <img class="cta-image" src="./assets/img/join-ai-revolution.png" alt="Join the AI Revolution with Qantm AI" width="500" height="300" loading="lazy">
  <div class="cta-row"><a class="btn pri" href="{EMAIL}">Contact Us</a></div>
</section>
"""

services_body = f"""
<p class="lede" style="margin-top:2.2rem">Transform your business with our expert AI consulting services.</p>
<div class="tiles">
  {_tile("navy", "brain", "AI Strategy Consulting", "<p>Develop a comprehensive AI roadmap aligned with your business objectives.</p><ul><li>AI readiness assessment</li><li>Technology stack evaluation</li><li>Implementation roadmap</li><li>ROI analysis</li></ul>")}
  {_tile("cyan", "code", "Implementation Support", "<p>Expert guidance in selecting and deploying AI solutions.</p><ul><li>Vendor selection</li><li>Integration planning</li><li>Technical architecture</li><li>Change management</li></ul>")}
  {_tile("purple", "users", "AI Training &amp; Education", "<p>Empower your team with AI knowledge and practical skills.</p><ul><li>Executive workshops</li><li>Technical training</li><li>Best practices</li><li>Hands-on exercises</li></ul>")}
</div>
<section>
  <h2>Why Choose Us?</h2>
  <p class="lede">We combine deep AI expertise with practical business experience to deliver real results.</p>
  <div class="tiles">
    {_tile("pink", "lightbulb", "Expert Knowledge", "<p>Access to leading AI experts and latest technologies.</p>")}
    {_tile("gold", "chart", "Proven Results", "<p>Track record of successful AI implementations.</p>")}
    {_tile("red", "shield", "Trusted Partner", "<p>Long-term support and guidance throughout your AI journey.</p>")}
  </div>
  <div class="cta-row"><a class="btn pri" href="{EMAIL}">Get Started</a></div>
</section>
"""

about_body = f"""
<p class="lede" style="margin-top:2.2rem">We're a team of AI experts and business strategists helping organizations navigate the future of technology.</p>
<section>
  <div class="split">
    <img src="./assets/img/ipad-playbook.png" alt="Qantm AI Playbook on iPad" width="1000" height="526" loading="lazy">
    <div class="prose">
      <h2 style="text-align:left">Our Mission</h2>
      <p>At Qantm AI, we believe in democratizing artificial intelligence for businesses of all sizes. Our mission is to bridge the gap between cutting-edge AI technology and practical business applications, ensuring our clients stay ahead in an increasingly digital world.</p>
    </div>
  </div>
</section>
<section>
  <h2>Our Values</h2>
  <div class="tiles">
    {_tile("navy", None, "Innovation", "<p>Constantly pushing boundaries and exploring new possibilities in AI.</p>")}
    {_tile("purple", None, "Excellence", "<p>Delivering high-quality solutions that drive real business value.</p>")}
    {_tile("cyan", None, "Partnership", "<p>Building long-term relationships based on trust and mutual success.</p>")}
    {_tile("red", None, "Responsibility", "<p>Ensuring ethical AI development and sustainable practices.</p>")}
  </div>
</section>
<section>
  <h2>Our Team</h2>
  <div class="team-grid">
    {_team("pink", "team-seth", "Dr. Seth Dobrin", "CEO &amp; AI Strategist", "Formerly IBM's first-ever Global Chief AI Officer &mdash; 15+ years transforming business through AI.")}
    {_team("gold", "team-rudd", "Tabitha Rudd", "COO", "Business operations, marketing, sales operations &amp; partnership relations.")}
    {_team("cyan", "team-gigi", "Gigi Frenchie", "CSO", "Cookie breach &amp; toy phishing expert, specializing in robust package delivery safety protocols &amp; team crisis management.")}
    {_team("red", "team-dot", "Dot LeBot", "MDL", "Development, implementation, and management helper.")}
  </div>
</section>
"""

contact_body = f"""
<p class="lede" style="margin-top:2.2rem">Have a question or want to work together? We'd love to hear from you.</p>
<div class="kv">
  <div class="card"><strong>Email</strong><a href="mailto:info@qantm.ai">info@qantm.ai</a></div>
  <div class="card"><strong>Business hours</strong>Monday&ndash;Friday<br>9:00 AM&ndash;5:00 PM CST</div>
</div>
<p class="lede" style="margin-top:1.6rem">We typically respond to inquiries within 24&ndash;48 business hours. For urgent matters, please include &ldquo;URGENT&rdquo; in your subject line.</p>
"""

nf_body = """
<p class="lede" style="margin-top:2.2rem">That page doesn't exist. Try the navigation above, or head <a href="./">home</a>.</p>
"""

import json as _json
import html as _html


def _media_body():
    cats = _json.load(open("data/media-catalog.json", encoding="utf-8"))
    out = ['<p class="lede" style="margin-top:2.2rem">Dr. Seth Dobrin\u2019s books, interviews, keynotes, broadcast appearances, peer-reviewed publications, and speaking engagements \u2014 a complete, sourced catalog.</p>']
    for c in cats:
        out.append(f'<section><h2>{_html.escape(c["name"])}</h2><ul class="media-list">')
        for it in c["items"]:
            t = _html.escape(it["title"]); d = _html.escape(it["detail"]); u = _html.escape(it["url"], quote=True)
            out.append(f'<li><a href="{u}" target="_blank" rel="noopener">{t}</a> <span class="media-detail">{d}</span></li>')
        out.append("</ul></section>")
    return "\n".join(out)


MEDIA_BODY = _media_body()


def _case_studies():
    """Render the Case Studies page from the verified data/case-studies.json.

    These are REAL, primary-source AI deployments across enterprises and
    governments — each card links to the vendor customer-story or official
    government source it was drawn from. Qantm AI curates and verifies this
    briefing; it does not claim to have delivered these engagements. The
    provenance gate (data/verify_case_studies.py) guarantees every entry has a
    real source and no placeholder data.
    """
    import subprocess
    import sys as _sys
    gate = subprocess.run([_sys.executable, "data/verify_case_studies.py"])
    if gate.returncode != 0:
        raise SystemExit("case-studies provenance gate FAILED — refusing to build stale/fake data")
    items = _json.load(open("data/case-studies.json", encoding="utf-8"))
    # Newest first, then by client name.
    items = sorted(items, key=lambda e: (-int(e.get("projectYear", 0)), str(e.get("client", "")).lower()))

    # Sector chips (single filter dimension), most common first.
    from collections import Counter
    counts = Counter(e["sector"] for e in items)
    sectors = [s for s, _ in counts.most_common()]

    def esc(s):
        return _html.escape(str(s))

    n = len(items)
    n_gov = sum(1 for e in items if e.get("org_type") == "government")
    n_ent = n - n_gov
    lede = (
        '<p class="lede" style="margin-top:2.2rem">How the world’s largest enterprises and '
        'governments are putting AI to work — and the results they report. A curated, '
        f'continuously verified briefing of {n} real deployments ({n_ent} enterprise, {n_gov} '
        'government). Every case links to its primary source.</p>'
    )

    chips = [f'<button class="cs-chip is-on" data-filter="all" aria-pressed="true">All <span>{n}</span></button>']
    for s in sectors:
        chips.append(f'<button class="cs-chip" data-filter="{esc(s)}" aria-pressed="false">'
                     f'{esc(s)} <span>{counts[s]}</span></button>')
    filter_bar = f'<div class="cs-filters" role="group" aria-label="Filter by sector" hidden>{"".join(chips)}</div>'

    cards = []
    for e in items:
        gov = e.get("org_type") == "government"
        badge = ('<span class="cs-badge cs-gov">Government</span>' if gov
                 else '<span class="cs-badge cs-ent">Enterprise</span>')
        year = f' <span class="cs-year">&middot; {esc(e["projectYear"])}</span>'
        country = f'<span class="cs-country">{esc(e["country"])}</span>' if e.get("country") else ""
        metric = f'<p class="cs-metric">{esc(e["metric"])}</p>' if e.get("metric") else ""
        quote = f'<blockquote class="cs-quote">{esc(e["quote"])}</blockquote>' if e.get("quote") else ""
        techs = "".join(f'<li>{esc(t)}</li>' for t in (e.get("technologies") or []))
        techs = f'<ul class="cs-tech" aria-label="Technologies">{techs}</ul>' if techs else ""
        vendor = f' &middot; {esc(e["vendor"])}' if e.get("vendor") else ""
        url = _html.escape(str(e["referenceUrl"]), quote=True)
        cards.append(
            f'<article class="cs-card" data-sector="{esc(e["sector"])}">'
            f'<div class="cs-top">{badge}<span class="cs-sector">{esc(e["sector"])}</span>{country}</div>'
            f'<h3 class="cs-client">{esc(e["client"])}{year}</h3>'
            f'<p class="cs-name">{esc(e["title"])}</p>'
            f'{metric}'
            f'<dl class="cs-dl">'
            f'<dt>Challenge</dt><dd>{esc(e["challenge"])}</dd>'
            f'<dt>Solution</dt><dd>{esc(e["solution"])}</dd>'
            f'<dt>Results</dt><dd>{esc(e["results"])}</dd>'
            f'</dl>'
            f'{quote}'
            f'{techs}'
            f'<p class="cs-src">Source: <a href="{url}" target="_blank" rel="noopener nofollow">'
            f'{esc(e["sourceName"])}{vendor} ↗</a></p>'
            f'</article>'
        )

    script = (
        '<script>(function(){var f=document.querySelector(".cs-filters");if(!f)return;'
        'f.hidden=false;var cards=[].slice.call(document.querySelectorAll(".cs-card"));'
        'f.addEventListener("click",function(ev){var b=ev.target.closest(".cs-chip");if(!b)return;'
        'var q=b.getAttribute("data-filter");'
        '[].forEach.call(f.querySelectorAll(".cs-chip"),function(c){var on=c===b;'
        'c.classList.toggle("is-on",on);c.setAttribute("aria-pressed",on?"true":"false");});'
        'cards.forEach(function(c){c.hidden=(q!=="all"&&c.getAttribute("data-sector")!==q);});});})();</script>'
    )
    disclosure = (
        '<p class="cs-note">Qantm AI curates and independently verifies these case studies from '
        'primary sources; we do not claim to have delivered these specific engagements. '
        'Every entry links to its original source and is re-checked on each site build.</p>'
        f'<div class="cta-row"><a class="btn pri" href="{EMAIL}">Talk to Qantm AI about your AI initiative</a></div>'
    )
    body = f'{lede}{filter_bar}<div class="cs-grid">{"".join(cards)}</div>{disclosure}{script}'

    # SEO: an ItemList of the case studies, each a CreativeWork citing its source.
    item_list = {
        "@context": "https://schema.org", "@type": "ItemList",
        "name": "Enterprise & Government AI Case Studies",
        "numberOfItems": n,
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "item": {
                "@type": "CreativeWork", "name": e["title"], "url": e["referenceUrl"],
                "about": {"@type": "Organization", "name": e["client"]},
                "isBasedOn": e["referenceUrl"], "publisher": {"@type": "Organization", "name": e["sourceName"]}}}
            for i, e in enumerate(items)
        ],
    }
    collection = {"@context": "https://schema.org", "@type": "CollectionPage",
                  "name": "AI Case Studies — Enterprise & Government", "url": f"{SITE}/case-studies"}
    return body, [collection, item_list], n, n_ent, n_gov


CASE_BODY, CASE_LD, CS_N, CS_ENT, CS_GOV = _case_studies()


pages = {
    "index.html": ("/", "Qantm AI — AI Strategy, Governance & Implementation Consulting",
        "AI consulting led by Dr. Seth Dobrin: AI iQ™ readiness assessments, governance and ethics alignment, executive education, and GenAI/ML implementation.",
        ("The Future of Business, Delivered Today!", True), home_body,
        [{"@context": "https://schema.org", "@type": "WebSite", "name": "Qantm AI", "url": SITE}]),
    "services.html": ("/services", "AI Advisory Services — Strategy, Implementation, Training | Qantm AI",
        "AI strategy consulting, implementation support (vendor selection, architecture, change management), and AI training for executives and technical teams.",
        ("Comprehensive AI Advisory Services", True), services_body, None),
    "case-studies.html": ("/case-studies", "AI Case Studies — How Enterprises & Governments Use AI | Qantm AI",
        "A curated, source-verified briefing of how leading enterprises and governments deploy AI — real-world case studies and the measurable results they report.",
        ("Case Studies", True), CASE_BODY, CASE_LD),
    "about.html": ("/about", "About Qantm AI — Dr. Seth Dobrin & Team | Austin, TX",
        "Qantm AI democratizes AI for businesses of all sizes. Led by Dr. Seth Dobrin (CEO & AI Strategist, 15+ years) and Tabitha Rudd (COO). Based in Austin, TX.",
        ("Leading the AI Revolution in Business", True), about_body,
        [{"@context": "https://schema.org", "@type": "AboutPage", "name": "About Qantm AI", "url": f"{SITE}/about"}]),
    "contact.html": ("/contact", "Contact Qantm AI — AI Consulting in Austin, TX",
        "Talk to Qantm AI about AI strategy, governance, or implementation. Email info@qantm.ai · Monday–Friday, 9:00 AM–5:00 PM CST.",
        ("Get In Touch", True), contact_body,
        [{"@context": "https://schema.org", "@type": "ContactPage", "name": "Contact Qantm AI", "url": f"{SITE}/contact"}]),
    "media.html": ("/media", "Media, Publications & Speaking \u2014 Dr. Seth Dobrin | Qantm AI",
        "Dr. Seth Dobrin\u2019s media catalog: the AI iQ book, 60+ podcasts and keynotes, TV appearances, peer-reviewed publications, and speaking engagements.",
        ("Media, Publications & Speaking", True), MEDIA_BODY,
        [{"@context": "https://schema.org", "@type": "CollectionPage", "name": "Qantm AI Media & Publications", "url": f"{SITE}/media"}]),
    "404.html": ("/404", "Page not found — Qantm AI",
        "That page doesn't exist on qantm.ai. Browse AI strategy, governance, and implementation consulting from Qantm AI in Austin, TX.",
        ("Page not found", True), nf_body, None, True),
}

for fname, spec in pages.items():
    path, title, desc, h1, body = spec[0], spec[1], spec[2], spec[3], spec[4]
    extra = spec[5] if len(spec) > 5 else None
    noindex = spec[6] if len(spec) > 6 else False
    assert len(title) <= 70, f"{fname} title {len(title)}"
    assert 25 <= len(desc) <= 160, f"{fname} desc {len(desc)}"
    open(fname, "w").write(page(path, title, desc, h1, body, extra, noindex))
    print(f"wrote {fname}  (title {len(title)}, desc {len(desc)})")

# sitemap — all pages rebuilt with the live-matched design on 2026-07-11
urls = "\n".join(
    f'  <url><loc>{SITE}{p}</loc><lastmod>2026-07-11</lastmod></url>'
    for p in ["/", "/services", "/case-studies", "/media", "/about", "/contact"])
open("sitemap.xml", "w").write(
    f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')
print("wrote sitemap.xml")
