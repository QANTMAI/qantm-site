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
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "5900 Balcones Dr Ste 100",
        "addressLocality": "Austin",
        "addressRegion": "TX",
        "postalCode": "78731",
        "addressCountry": "US",
    },
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

CALENDLY = "https://calendly.com/dr-seth-qantm"

NAV = [("Home", "/"), ("Services", "/services"), ("Case Studies", "/case-studies"), ("About", "/about"), ("Contact", "/contact")]


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
        nav_parts.append(f'<a href="{rel}"{cur}>{label}</a>')
    nav = "".join(nav_parts)
    robots = '<meta name="robots" content="noindex, nofollow">' if noindex else '<meta name="robots" content="index, follow, max-snippet:-1">'
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
    <a class="logo" href="./"><img src="./favicon-32x32.png" alt="" width="30" height="30">Qantm AI</a>
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
    <p class="copy">&copy; 2026 Qantm AI, LLC. All rights reserved. &middot; 5900 Balcones Dr Ste 100, Austin, TX 78731 &middot; <a href="mailto:info@qantm.ai">info@qantm.ai</a> &middot; <a href="https://0penrx.org">0penRX — free prescription price transparency</a></p>
  </div>
</footer>
</body>
</html>
"""


OFFERINGS = [
    ("AI iQ™ Governance & Ethics Alignment", "Ensuring your AI initiatives align with the highest ethical standards"),
    ("AI iQ™ Readiness Assessment", "Discover how ready your organization is to leap into the AI revolution"),
    ("AI iQ™ Strategy Development", "Crafting a winning strategy tailored to your unique aspirations"),
    ("AI iQ™ Executive Education", "Empowering your leadership with AI landscape navigation skills"),
    ("AI iQ™ GenAI Capability Tuning", "Fine-tuning your generative AI capabilities for maximum impact"),
    ("AI iQ™ GenAI/ML Implementation", "Achieving excellence in AI and machine learning operations"),
]

home_body = f"""
<div class="hero">
  <p style="max-width:60ch;font-size:1.15rem;color:hsl(var(--muted-foreground))">Leading the way in artificial intelligence, with a leadership team bringing decades of success in AI strategy, governance, and development.</p>
  <div class="cta-row">
    <a class="btn pri" href="{CALENDLY}" rel="noopener">Get Started Today</a>
    <a class="btn" href="./services">Our Services</a>
  </div>
</div>
<section id="offerings">
  <h2>Our Tailored Offerings</h2>
  <div class="grid">
{"".join(f'    <div class="card"><h3>{t}</h3><p>{d}</p></div>' for t, d in OFFERINGS)}
  </div>
</section>
<section id="ethics">
  <h2>Ethical AI Governance</h2>
  <p class="lede">At Qantm AI, we put ethical practices front and center in every engagement. Our comprehensive governance frameworks and robust data privacy safeguards ensure transparency and fairness&mdash;because in this fast-paced world, integrity is always in vogue!</p>
</section>
<section id="cta">
  <h2>Join the AI Revolution!</h2>
  <p class="lede">Contact Qantm AI today to discover how our tailor-made solutions can elevate your organization into the bright future of technology.</p>
  <div class="cta-row"><a class="btn pri" href="./contact">Contact Us</a><a class="btn" href="{CALENDLY}" rel="noopener">Book a call</a></div>
</section>
"""

services_body = f"""
<p class="lede" style="margin-top:2.2rem">Transform your business with our expert AI consulting services.</p>
<div class="grid">
  <div class="card"><h3>AI Strategy Consulting</h3><p>Develop a comprehensive AI roadmap aligned with your business objectives.</p>
    <ul><li>AI readiness assessment</li><li>Technology stack evaluation</li><li>Implementation roadmap</li><li>ROI analysis</li></ul></div>
  <div class="card"><h3>Implementation Support</h3><p>Expert guidance in selecting and deploying AI solutions.</p>
    <ul><li>Vendor selection</li><li>Integration planning</li><li>Technical architecture</li><li>Change management</li></ul></div>
  <div class="card"><h3>AI Training &amp; Education</h3><p>Empower your team with AI knowledge and practical skills.</p>
    <ul><li>Executive workshops</li><li>Technical training</li><li>Best practices</li><li>Hands-on exercises</li></ul></div>
</div>
<section>
  <h2>Why Choose Us?</h2>
  <p class="lede">We combine deep AI expertise with practical business experience to deliver real results.</p>
  <div class="grid">
    <div class="card"><h3>Expert Knowledge</h3><p>Access to leading AI experts and latest technologies.</p></div>
    <div class="card"><h3>Proven Results</h3><p>Track record of successful AI implementations.</p></div>
    <div class="card"><h3>Trusted Partner</h3><p>Long-term support and guidance throughout your AI journey.</p></div>
  </div>
  <div class="cta-row"><a class="btn pri" href="{CALENDLY}" rel="noopener">Get Started</a></div>
</section>
"""

case_body = f"""
<p class="lede" style="margin-top:2.2rem">Discover how our AI solutions have transformed businesses across diverse industries. Explore real-world success stories and learn how Qantm AI delivers measurable results.</p>
<div class="prose">
  <p>We publish case studies with our clients&rsquo; permission. To hear how engagements like yours have gone &mdash; readiness assessments, governance programs, GenAI implementations &mdash; the fastest route is a conversation.</p>
</div>
<div class="cta-row"><a class="btn pri" href="{CALENDLY}" rel="noopener">Book a call with Dr. Dobrin</a><a class="btn" href="./contact">Contact us</a></div>
"""

about_body = """
<p class="lede" style="margin-top:2.2rem">We're a team of AI experts and business strategists helping organizations navigate the future of technology.</p>
<section>
  <h2>Our Mission</h2>
  <p class="lede">At Qantm AI, we believe in democratizing artificial intelligence for businesses of all sizes. Our mission is to bridge the gap between cutting-edge AI technology and practical business applications, ensuring our clients stay ahead in an increasingly digital world.</p>
</section>
<section>
  <h2>Our Values</h2>
  <div class="grid">
    <div class="card"><h3>Innovation</h3><p>Constantly pushing boundaries and exploring new possibilities in AI.</p></div>
    <div class="card"><h3>Excellence</h3><p>Delivering high-quality solutions that drive real business value.</p></div>
    <div class="card"><h3>Partnership</h3><p>Building long-term relationships based on trust and mutual success.</p></div>
    <div class="card"><h3>Responsibility</h3><p>Ensuring ethical AI development and sustainable practices.</p></div>
  </div>
</section>
<section>
  <h2>Our Team</h2>
  <div class="grid">
    <div class="card"><h3>Dr. Seth Dobrin</h3><p><strong>CEO &amp; AI Strategist</strong><br>15+ years of experience in AI and business transformation.</p></div>
    <div class="card"><h3>Tabitha Rudd</h3><p><strong>COO</strong><br>Business operations, marketing, sales operations &amp; partnership relations.</p></div>
    <div class="card"><h3>Gigi Frenchie</h3><p><strong>CSO</strong><br>Cookie breach &amp; toy phishing expert, specializing in robust package delivery safety protocols &amp; team crisis management.</p></div>
    <div class="card"><h3>Dot LeBot</h3><p><strong>MDL</strong><br>Development, implementation, and management helper.</p></div>
  </div>
</section>
"""

contact_body = f"""
<p class="lede" style="margin-top:2.2rem">Have a question or want to work together? We'd love to hear from you.</p>
<div class="kv">
  <div class="card"><strong>Email</strong><a href="mailto:info@qantm.ai">info@qantm.ai</a></div>
  <div class="card"><strong>Book a call</strong><a href="{CALENDLY}" rel="noopener">calendly.com/dr-seth-qantm</a></div>
  <div class="card"><strong>Address</strong>5900 Balcones Dr Ste 100<br>Austin, TX 78731, United States</div>
  <div class="card"><strong>Business hours</strong>Monday&ndash;Friday<br>9:00 AM&ndash;5:00 PM CST</div>
</div>
<p class="lede" style="margin-top:1.6rem">We typically respond to inquiries within 24&ndash;48 business hours. For urgent matters, please include &ldquo;URGENT&rdquo; in your subject line.</p>
"""

nf_body = """
<p class="lede" style="margin-top:2.2rem">That page doesn't exist. Try the navigation above, or head <a href="./">home</a>.</p>
"""

pages = {
    "index.html": ("/", "Qantm AI — AI Strategy, Governance & Implementation Consulting",
        "AI consulting led by Dr. Seth Dobrin: AI iQ™ readiness assessments, governance and ethics alignment, executive education, and GenAI/ML implementation.",
        ("The Future of Business, Delivered Today!", True), home_body,
        [{"@context": "https://schema.org", "@type": "WebSite", "name": "Qantm AI", "url": SITE}]),
    "services.html": ("/services", "AI Advisory Services — Strategy, Implementation, Training | Qantm AI",
        "AI strategy consulting, implementation support (vendor selection, architecture, change management), and AI training for executives and technical teams.",
        ("Comprehensive AI Advisory Services", True), services_body, None),
    "case-studies.html": ("/case-studies", "AI Case Studies — Real-World Implementations | Qantm AI",
        "How Qantm AI's strategy, governance, and implementation work has delivered measurable results for businesses across industries.",
        ("Case Studies", True), case_body, None),
    "about.html": ("/about", "About Qantm AI — Dr. Seth Dobrin & Team | Austin, TX",
        "Qantm AI democratizes AI for businesses of all sizes. Led by Dr. Seth Dobrin (CEO & AI Strategist, 15+ years) and Tabitha Rudd (COO). Based in Austin, TX.",
        ("Leading the AI Revolution in Business", True), about_body,
        [{"@context": "https://schema.org", "@type": "AboutPage", "name": "About Qantm AI", "url": f"{SITE}/about"}]),
    "contact.html": ("/contact", "Contact Qantm AI — AI Consulting in Austin, TX",
        "Talk to Qantm AI about AI strategy, governance, or implementation. info@qantm.ai · 5900 Balcones Dr Ste 100, Austin, TX 78731 · Mon–Fri 9–5 CST.",
        ("Get In Touch", True), contact_body,
        [{"@context": "https://schema.org", "@type": "ContactPage", "name": "Contact Qantm AI", "url": f"{SITE}/contact"}]),
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

# sitemap
urls = "\n".join(
    f"  <url><loc>{SITE}{p}</loc><lastmod>2026-07-08</lastmod></url>"
    for p in ["/", "/services", "/case-studies", "/about", "/contact"])
open("sitemap.xml", "w").write(
    f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')
print("wrote sitemap.xml")
