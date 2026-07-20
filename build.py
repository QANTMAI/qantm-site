#!/usr/bin/env python3
"""Generate the Qantm AI static site: 5 pages + 404, shared head/nav/footer.

Content is transcribed from the live qantm.ai rendered pages (2026-07-08) —
nothing invented. URLs match the live SPA exactly (/services, /about,
/case-studies, /contact as extensionless .html files GitHub Pages serves at
the bare path). Run:  python3 build.py
"""

import hashlib
import json

SITE = "https://qantm.ai"

# Content-hash the stylesheet so browsers fetch the new CSS immediately after a
# deploy instead of serving a stale cached copy.
ASSET_V = hashlib.md5(open("assets/styles.css", "rb").read()).hexdigest()[:8]

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
    "founder": {"@type": "Person", "name": "Seth Dobrin", "honorificPrefix": "Dr.", "jobTitle": "Founder & CEO", "description": "Founder & CEO of Qantm AI; author of AI iQ for a Human-Focused Future (Routledge, 2024).", "sameAs": ["https://www.linkedin.com/company/qantm-ai/"]},
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

BOOK_JSONLD = {
    "@context": "https://schema.org",
    "@type": "Book",
    "name": "AI iQ for a Human-Focused Future",
    "author": {"@type": "Person", "name": "Seth Dobrin", "honorificPrefix": "Dr."},
    "publisher": {"@type": "Organization", "name": "Routledge / CRC Press"},
    "datePublished": "2024",
    "isbn": "9781032603896",
    "url": "https://www.routledge.com/AI-IQ-for-a-Human-focused-Future-Strategy-Talent-and-Culture/Dobrin/p/book/9781032603896",
}

EMAIL = "mailto:info@qantm.ai"

NAV = [("Home", "/"), ("Services", "/services"), ("Case Studies", "/case-studies"), ("Media", "/media"), ("About", "/about"), ("Contact", "/contact")]


def jsonld(extra=None):
    graph = [ORG_JSONLD, BOOK_JSONLD] + (extra or [])
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
<meta property="og:image" content="{SITE}/assets/img/og-card.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Qantm AI — Next Level AI Solutions">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{SITE}/assets/img/og-card.png">
<link rel="icon" type="image/x-icon" href="./favicon.ico">
<link rel="icon" type="image/png" sizes="32x32" href="./favicon-32x32.png">
<link rel="apple-touch-icon" href="./favicon.png">
<link rel="stylesheet" href="./assets/styles.css?v={ASSET_V}">
<script type="application/ld+json">{jsonld(extra_ld)}</script>
</head>
<body>
<header>
  <div class="hdr">
    <a class="logo" href="./"><img src="./assets/img/logo.png" alt="Qantm AI — Next Level AI Solutions" width="112" height="50"></a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="mainnav" aria-label="Open menu"><span></span><span></span><span></span></button>
    <nav class="main" id="mainnav" aria-label="Main">{nav}</nav>
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
        <a href="./">Home</a><a href="./services">Services</a><a href="./case-studies">Case Studies</a><a href="./media">Media</a><a href="./about">About</a><a href="./contact">Contact</a>
      </nav>
      <nav aria-label="Elsewhere">
        <a href="https://www.linkedin.com/company/qantm-ai/" rel="noopener">LinkedIn</a>
        <a href="https://siliconsandstudio.substack.com/" rel="noopener">Substack</a>
        <a href="https://github.com/QANTMAI" rel="noopener">GitHub</a>
        <a href="https://0penrx.org" rel="noopener">0penRX</a>
      </nav>
    </div>
    <p class="copy">&copy; 2026 Qantm AI, LLC. All rights reserved.</p>
  </div>
</footer>
<script>(function(){{var b=document.querySelector('.nav-toggle'),n=document.getElementById('mainnav');if(b&&n){{b.addEventListener('click',function(){{var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false');b.setAttribute('aria-label',o?'Close menu':'Open menu');}});}}}})();</script>
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
    "book-open": '<path d="M12 7v14"/><path d="M3 18a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h5a4 4 0 0 1 4 4 4 4 0 0 1 4-4h5a1 1 0 0 1 1 1v13a1 1 0 0 1-1 1h-6a3 3 0 0 0-3 3 3 3 0 0 0-3-3z"/>',
    "mic": '<path d="M12 19v3"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><rect x="9" y="2" width="6" height="13" rx="3"/>',
    "video": '<path d="m16 13 5.223 3.482a.5.5 0 0 0 .777-.416V7.87a.5.5 0 0 0-.752-.432L16 10.5"/><rect x="2" y="6" width="14" height="12" rx="2"/>',
    "tv": '<path d="m17 2-5 5-5-5"/><rect width="20" height="15" x="2" y="7" rx="2"/>',
    "newspaper": '<path d="M15 18h-5"/><path d="M18 14h-8"/><path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 1-4 0v-9a2 2 0 0 1 2-2h2"/><rect width="8" height="4" x="10" y="6" rx="1"/>',
    "presentation": '<path d="M2 3h20"/><path d="M21 3v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V3"/><path d="m7 21 5-5 5 5"/>',
    "square-pen": '<path d="M12 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.375 2.625a1 1 0 0 1 3 3l-9.013 9.014a2 2 0 0 1-.853.505l-2.873.84a.5.5 0 0 1-.62-.62l.84-2.873a2 2 0 0 1 .506-.852z"/>',
    "graduation-cap": '<path d="M21.42 10.922a1 1 0 0 0-.019-1.838L12.83 5.18a2 2 0 0 0-1.66 0L2.6 9.08a1 1 0 0 0 0 1.832l8.57 3.908a2 2 0 0 0 1.66 0z"/><path d="M22 10v6"/><path d="M6 12.5V16a6 3 0 0 0 12 0v-3.5"/>',
    "arrow-up-right": '<path d="M7 7h10v10"/><path d="M7 17 17 7"/>',
    "landmark": '<path d="M10 18v-7"/><path d="M11.119 2.205a2 2 0 0 1 1.762 0l7.84 3.846A.5.5 0 0 1 20.5 7h-17a.5.5 0 0 1-.22-.949z"/><path d="M14 18v-7"/><path d="M18 18v-7"/><path d="M3 22h18"/><path d="M6 18v-7"/>',
    "radio-tower": '<path d="M4.9 16.1C1 12.2 1 5.8 4.9 1.9"/><path d="M7.8 4.7a6.14 6.14 0 0 0-.8 7.5"/><circle cx="12" cy="9" r="2"/><path d="M16.2 4.8c2 2 2.26 5.11.8 7.47"/><path d="M19.1 1.9a9.96 9.96 0 0 1 0 14.1"/><path d="M9.5 18h5"/><path d="m8 22 4-11 4 11"/>',
    "flask-conical": '<path d="M14 2v6a2 2 0 0 0 .245.96l5.51 10.08A2 2 0 0 1 18 22H6a2 2 0 0 1-1.755-2.96l5.51-10.08A2 2 0 0 0 10 8V2"/><path d="M6.453 15h11.094"/><path d="M8.5 2h7"/>',
    "banknote": '<rect width="20" height="12" x="2" y="6" rx="2"/><circle cx="12" cy="12" r="2"/><path d="M6 12h.01M18 12h.01"/>',
    "globe": '<circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/>',
}


def _icon(name):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


def _tile(color, icon, title, body):
    ic = _icon(icon) if icon else ""
    return f'<div class="tile tile--{color}">{ic}<h3>{title}</h3>{body}</div>'


def _team(color, img, name, role, desc):
    return (f'<div class="team-card tile--{color}">'
            f'<img src="./assets/img/{img}.jpg" alt="{name}" width="118" height="118" loading="lazy">'
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
  <p>Most AI initiatives stall between the demo and the boardroom. Qantm AI closes that gap with the AI iQ&trade; approach &mdash; readiness assessments, governance guardrails, and hands-on implementation for enterprises and governments moving from pilots to production.</p>
</div>
<section id="offerings">
  <h2>Our Tailored Offerings</h2>
  <div class="tiles">
{"".join('    ' + _tile(c, i, t, f'<p>{d}</p>') + chr(10) for t, d, c, i in OFFERINGS)}  </div>
</section>
<section id="our-work">
  <h2>Our Work</h2>
  <p class="lede">Most of our engagements are confidential &mdash; our clients ask us not to publish their names, and we honor that. What we can share is the breadth of organizations that trust Qantm AI to move from AI ambition to production:</p>
  <div class="tiles">
    {_tile("navy", "landmark", "Government", "<p>National and public-sector bodies in the Middle East.</p>")}
    {_tile("cyan", "radio-tower", "Telecommunications", "<p>Telecom carriers and network operators.</p>")}
    {_tile("purple", "flask-conical", "Biotech &amp; Life Sciences", "<p>Biotech and life-sciences organizations.</p>")}
    {_tile("gold", "code", "Software &amp; Technology", "<p>Software and technology companies.</p>")}
    {_tile("red", "banknote", "Banking &amp; Financial Services", "<p>Banks and financial institutions.</p>")}
    {_tile("pink", "globe", "Global Nonprofits &amp; NGOs", "<p>Mission-driven nonprofits and NGOs worldwide.</p>")}
  </div>
</section>
<section id="ethics">
  <h2>Ethical AI Governance</h2>
  <p class="lede">At Qantm AI, we put ethical practices front and center in every engagement. Our comprehensive governance frameworks and robust data privacy safeguards keep AI transparent and accountable&mdash;because integrity isn&rsquo;t a trend, it&rsquo;s the foundation of AI you can defend to your board, your regulators, and your customers.</p>
</section>
<section id="cta">
  <h2>Move from AI pilots to production</h2>
  <p class="lede">Talk to Qantm AI about a readiness assessment, a governance framework, or hands-on implementation &mdash; and turn stalled initiatives into governed, in-production results.</p>
  <img class="cta-image" src="./assets/img/join-ai-revolution.jpg" alt="Qantm AI — from AI pilots to production" width="500" height="300" loading="lazy">
  <div class="cta-row"><a class="btn pri" href="./contact">Contact us</a></div>
</section>
"""

services_body = f"""
<p class="lede" style="margin-top:2.2rem">Transform your organization with the AI iQ&trade; approach &mdash; a clear path from readiness and strategy to governed, in-production AI.</p>
<section id="offerings">
  <h2>Our AI iQ&trade; Offerings</h2>
  <div class="tiles">
{"".join('    ' + _tile(c, i, t, f'<p>{d}</p>') + chr(10) for t, d, c, i in OFFERINGS)}  </div>
</section>
<section>
  <h2>Why Choose Us?</h2>
  <p class="lede">We combine deep AI expertise with practical business experience to deliver real results.</p>
  <div class="tiles">
    {_tile("pink", "lightbulb", "Expert Knowledge", "<p>Access to leading AI experts and latest technologies.</p>")}
    {_tile("gold", "chart", "Proven Results", "<p>Track record of successful AI implementations.</p>")}
    {_tile("red", "shield", "Trusted Partner", "<p>Long-term support and guidance throughout your AI journey.</p>")}
  </div>
  <div class="cta-row"><a class="btn pri" href="./contact">Book a call</a></div>
</section>
"""

about_body = f"""
<p class="lede" style="margin-top:2.2rem">We're a team of AI experts and business strategists helping organizations navigate the future of technology.</p>
<section>
  <div class="split">
    <img src="./assets/img/ipad-playbook.jpg" alt="Qantm AI Playbook on iPad" width="1000" height="526" loading="lazy">
    <div class="prose">
      <h2 style="text-align:left">Our Mission</h2>
      <p>At Qantm AI, we believe in democratizing artificial intelligence for businesses of all sizes. Our mission is to bridge the gap between cutting-edge AI technology and practical business applications, ensuring our clients stay ahead in an increasingly digital world.</p>
    </div>
  </div>
</section>
<section>
  <h2>Our Values</h2>
  <div class="tiles tiles-4">
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
  <p class="lede" style="margin-top:2.2rem">Book a call or drop us a line &mdash; whichever is easier. We&rsquo;d love to hear from you.</p>

  <div class="card booking-card">
    <div>
      <h3 style="margin:0 0 .35rem">Book a 30-minute AI readiness call</h3>
      <p style="margin:0">Pick a time that works &mdash; it goes straight into our calendar.</p>
    </div>
    <a class="btn blue" href="https://calendar.app.google/fyVQVA7XUn4NtttM9" target="_blank" rel="noopener">Book a call &rarr;</a>
  </div>

  <div class="kv" style="margin-top:2.2rem">
    <div class="card"><strong>Email</strong><a href="mailto:info@qantm.ai">info@qantm.ai</a></div>
    <div class="card"><strong>Business hours</strong>Monday&ndash;Friday<br>9:00 AM&ndash;5:00 PM CST</div>
  </div>
  <p class="lede" style="margin-top:1.6rem">Prefer email? Reach us at <a href="mailto:info@qantm.ai">info@qantm.ai</a> &mdash; we typically respond within 24&ndash;48 business hours.</p>
  """

nf_body = """
<p class="lede" style="margin-top:2.2rem">That page doesn't exist. Try the navigation above, or head <a href="./">home</a>.</p>
"""

import json as _json
import html as _html


def _media_body():
    """Render the Media page as a portfolio: a stats band, a featured book, a
    decade-of-speaking timeline, media cards, and a publications list.

    The 23 source categories in data/media-catalog.json are regrouped into eight
    sections; nothing is invented \u2014 every card is a real {title, detail, url}
    entry, and the timeline years are parsed from the category names.
    """
    import re as _re
    cats = _json.load(open("data/media-catalog.json", encoding="utf-8"))

    def esc(s):
        return _html.escape(str(s))

    def sec_of(name):
        if name == "Book":
            return "book"
        if name.startswith("Podcasts"):
            return "podcasts"
        if name.startswith("YouTube"):
            return "video"
        if name.startswith("TV"):
            return "tv"
        if name.startswith("Silicon Sands"):
            return "newsletter"
        if name.startswith("Speaking"):
            return "speaking"
        if name.startswith("Academic"):
            return "research"
        if name.startswith("Articles"):
            return "articles"
        return "elsewhere"

    by = {}
    for c in cats:
        by.setdefault(sec_of(c["name"]), []).append(c)

    def items_of(key):
        return [it for c in by.get(key, []) for it in c["items"]]

    def count(key):
        return len(items_of(key))

    # (key, label, icon, accent) \u2014 order defines the page and the section nav.
    SECTIONS = [s for s in [
        ("book", "The Book", "book-open", "navy"),
        ("speaking", "Speaking & Conferences", "presentation", "pink"),
        ("video", "Video & Keynotes", "video", "red"),
        ("podcasts", "Podcasts", "mic", "purple"),
        ("tv", "TV, Broadcast & Press", "tv", "gold"),
        ("newsletter", "Silicon Sands Newsletter", "newspaper", "cyan"),
        ("articles", "Articles & Op-Eds", "square-pen", "red"),
        ("research", "Research & Publications", "graduation-cap", "navy"),
        ("elsewhere", "Profiles & Elsewhere", "arrow-up-right", "purple"),
    ] if s[0] in by]

    def head(key, label, icon, accent):
        n = count(key)
        badge = f'<span class="msec-count">{n}</span>' if (n and key != "book") else ""
        return (f'<div class="msec-head"><span class="msec-icon tile--{accent}">{_icon(icon)}</span>'
                f'<h2>{esc(label)}</h2>{badge}</div>')

    out = [
        '<p class="lede" style="margin-top:2rem">Dr. Seth Dobrin \u2014 author, keynote speaker, and a '
        'widely-cited voice in enterprise and responsible AI. A decade of talks, interviews, '
        'broadcasts, and peer-reviewed research, gathered in one place.</p>'
    ]

    # Stats band (real counts).
    stats = [
        (count("speaking"), "Talks &amp; keynotes"),
        (count("video") + count("podcasts"), "Podcasts &amp; videos"),
        (count("research"), "Publications"),
        (count("tv"), "TV &amp; press"),
    ]
    out.append('<div class="mstats">' + "".join(
        f'<div class="mstat"><span class="mstat-n">{n}</span><span class="mstat-l">{l}</span></div>'
        for n, l in stats if n) + '</div>')

    # Section nav.
    out.append('<nav class="media-nav" aria-label="Jump to a section">' + "".join(
        f'<a href="#sec-{k}">{esc(lbl)}</a>' for k, lbl, _i, _a in SECTIONS) + '</nav>')

    for key, label, icon, accent in SECTIONS:
        if key == "book":
            b = items_of("book")
            title = b[0]["title"] if b else "AI iQ for a Human-Focused Future"
            btns = "".join(
                f'<a class="btn pri" href="{esc(it["url"])}" target="_blank" rel="noopener">'
                f'{esc(it["detail"].split(chr(8212))[0].strip())}</a>' for it in b)
            out.append(
                f'<section id="sec-book" class="msec">{head(key, label, icon, accent)}'
                f'<div class="book-feature">'
                f'<div class="book-cover tile--{accent}"><span class="book-cover-tag">Book &middot; 2024</span>'
                f'<span class="book-cover-title">{esc(title)}</span>'
                f'<span class="book-cover-by">Dr. Seth Dobrin</span></div>'
                f'<div class="book-meta"><h3 class="book-title">{esc(title)}</h3>'
                f'<p class="book-sub">By Dr. Seth Dobrin &middot; Routledge / CRC Press &middot; 2024</p>'
                f'<p class="book-get">Get the book:</p>'
                f'<div class="cta-row" style="justify-content:flex-start">{btns}</div>'
                f'</div></div></section>')
        elif key == "speaking":
            years = []
            for c in by["speaking"]:
                m = _re.search(r"(\d{4})", c["name"])
                years.append((int(m.group(1)) if m else 0, c["items"]))
            years.sort(key=lambda x: -x[0])
            tl = [f'<section id="sec-speaking" class="msec">{head(key, label, icon, accent)}'
                  f'<p class="msec-sub">{count("speaking")} engagements across 2017\u20132026.</p>'
                  '<div class="timeline">']
            for yr, its in years:
                rows = "".join(
                    f'<a class="tl-item" href="{esc(it["url"])}" target="_blank" rel="noopener">'
                    f'<span class="tl-date">{esc(it["detail"])}</span>'
                    f'<span class="tl-title">{esc(it["title"])}</span></a>' for it in its)
                tl.append(f'<div class="tl-year"><div class="tl-marker">{yr}</div>'
                          f'<div class="tl-items">{rows}</div></div>')
            tl.append('</div></section>')
            out.append("".join(tl))
        elif key == "research":
            rows = "".join(
                f'<li><a href="{esc(it["url"])}" target="_blank" rel="noopener">{esc(it["title"])}</a>'
                f'<span class="pub-year">{esc(it["detail"])}</span></li>' for it in items_of("research"))
            out.append(f'<section id="sec-research" class="msec">{head(key, label, icon, accent)}'
                       f'<ul class="pub-list">{rows}</ul></section>')
        elif key == "elsewhere":
            chips = "".join(
                f'<a class="mchip" href="{esc(it["url"])}" target="_blank" rel="noopener">{esc(it["title"])}</a>'
                for it in items_of("elsewhere"))
            out.append(f'<section id="sec-elsewhere" class="msec">{head(key, label, icon, accent)}'
                       f'<div class="mchips">{chips}</div></section>')
        else:
            cards = "".join(
                f'<a class="mcard" href="{esc(it["url"])}" target="_blank" rel="noopener">'
                f'<span class="mcard-date">{esc(it["detail"])}</span>'
                f'<span class="mcard-title">{esc(it["title"])}</span>'
                f'<span class="mcard-go">{_icon("arrow-up-right")}</span></a>' for it in items_of(key))
            out.append(f'<section id="sec-{key}" class="msec">{head(key, label, icon, accent)}'
                       f'<div class="mcards">{cards}</div></section>')

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
        f'<div class="cta-row"><a class="btn pri" href="./contact">Talk to Qantm AI about your AI initiative</a></div>'
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
        ("Turn AI ambition into governed, in-production results.", True), home_body,
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
