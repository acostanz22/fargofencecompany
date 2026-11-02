# -*- coding: utf-8 -*-
"""Generate the Fargo Fence Company static site."""
import html as htmllib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Real pixel sizes of every file in images/ so <img> width/height match the file.
IMG_SIZES = {
    "images/aluminum.jpg": (800, 533),
    "images/design-50.png": (800, 533),
    "images/design-51.png": (800, 533),
    "images/design-52.png": (800, 533),
    "images/design-55.png": (800, 533),
    "images/design-56.png": (800, 533),
    "images/design-57.png": (800, 533),
    "images/design-58.png": (800, 533),
    "images/hero-bg.jpg": (1792, 1024),
    "images/vinyl-gate.jpg": (628, 420),
    "images/vinyl-privacy.jpg": (800, 533),
    "images/vinyl-semi.jpg": (800, 533),
}

# Genuine customer reviews only. Leave empty until real, attributable reviews are supplied;
# the reviews section is omitted entirely while this list is empty. Each entry: (quote, name, source).
REVIEWS = []


def img(src, alt, loading="lazy", extra=""):
    w, h = IMG_SIZES[src]
    load = f' loading="{loading}" decoding="async"' if loading else ""
    return f'<img src="{src}" alt="{alt}" width="{w}" height="{h}"{load}{extra}>'


def esc(text):
    return htmllib.escape(text, quote=True)
SITE = "https://www.fargofencecompany.net"
NAME = "Fargo Fence Company"
PHONE = "(701) 394-8468"
TEL = "+17013948468"
TALLY = (
    "https://tally.so/embed/xX6B0y?alignLeft=1&hideTitle=1"
    "&transparentBackground=1&dynamicHeight=1&source=Fargo+Fence+Company"
)
PHONE_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'
MENU_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 6h16M4 12h16M4 18h16"/></svg>'
TALLY_JS = '<script>var d=document,w="https://tally.so/widgets/embed.js",v=function(){"undefined"!=typeof Tally?Tally.loadEmbeds():d.querySelectorAll("iframe[data-tally-src]:not([src])").forEach((function(e){e.src=e.dataset.tallySrc}))};if("undefined"!=typeof Tally)v();else if(d.querySelector(\'script[src="\'+w+\'"]\')==null){var s=d.createElement("script");s.src=w,s.onload=v,s.onerror=v,d.body.appendChild(s);}</script>'

SERVICES = []
LOCATIONS = []


def canonical(path):
    if path in ("", "index.html"):
        return SITE + "/"
    return SITE + "/" + path


def call_btn(cls="btn btn-ghost"):
    return f'<a class="{cls}" href="tel:{TEL}">{PHONE_SVG}{PHONE}</a>'


OFFICE_HOURS = "Monday–Sunday: 7 am – 7 pm"
PHONE_ICON = (
    '<svg class="phone-icon" width="18" height="18" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
    '<path fill="currentColor" d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1.1-.3 1.2.4 2.5.6 3.8.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.6.6 3.8.1.4 0 .8-.3 1.1L6.6 10.8z"/>'
    "</svg>"
)


def phone_link(extra_class=""):
    cls = "phone-link" + (f" {extra_class}" if extra_class else "")
    return f'<a class="{cls}" href="tel:{TEL}">{PHONE_ICON}<strong>{PHONE}</strong></a>'


def quote_href(current):
    return "#quote"


def crumbs(items):
    parts = ['<a href="index.html">Home</a>']
    for href, label in items[:-1]:
        parts.append(f'<a href="{href}">{label}</a>')
    parts.append(items[-1][1])
    return f'<p class="crumbs">{" / ".join(parts)}</p>'


def faq_html(items):
    blocks = []
    for q, a in items:
        blocks.append(f'<div class="faq-item"><h3>{q}</h3><p>{a}</p></div>')
    return '<div class="faq-grid">' + "".join(blocks) + "</div>"


def steps_html(steps):
    lis = []
    for i, (title, text) in enumerate(steps, 1):
        lis.append(f'<li><span class="num">{i}</span><span><strong>{title}</strong> {text}</span></li>')
    return '<ol class="steps">' + "".join(lis) + "</ol>"


def factors_html(items):
    blocks = []
    for title, text in items:
        blocks.append(f'<article class="factor"><h3>{title}</h3><p>{text}</p></article>')
    return '<div class="factor-grid">' + "".join(blocks) + "</div>"


def business_node():
    offers = []
    for s in SERVICES:
        offers.append({
            "@type": "Offer",
            "itemOffered": {
                "@type": "Service",
                "@id": f"{SITE}/{s['slug']}#service",
                "name": s["schema_name"],
                "url": f"{SITE}/{s['slug']}",
                "provider": {"@id": f"{SITE}/#business"},
            },
        })
    return {
        "@type": ["LocalBusiness", "HomeAndConstructionBusiness"],
        "@id": f"{SITE}/#business",
        "name": NAME,
        "url": f"{SITE}/",
        "telephone": "+1-701-394-8468",
        "image": f"{SITE}/images/vinyl-privacy.jpg",
        "logo": f"{SITE}/logo.svg",
        "description": "Fence installation and repair for homes, farms, and commercial lots in Fargo, North Dakota and nearby Cass County and Clay County. Service-area business with no public storefront.",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Fargo",
            "addressRegion": "ND",
            "addressCountry": "US",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": 46.8772, "longitude": -96.7898},
        "areaServed": [
            {
                "@type": "GeoCircle",
                "name": "About 25 miles around Fargo, North Dakota",
                "geoMidpoint": {"@type": "GeoCoordinates", "latitude": 46.8772, "longitude": -96.7898},
                "geoRadius": 40234,
            },
            {"@type": "City", "name": "Fargo, ND"},
            {"@type": "City", "name": "West Fargo, ND"},
            {"@type": "City", "name": "Moorhead, MN"},
            {"@type": "City", "name": "Horace, ND"},
            {"@type": "City", "name": "Dilworth, MN"},
            {"@type": "City", "name": "Casselton, ND"},
            {"@type": "City", "name": "Mapleton, ND"},
            {"@type": "City", "name": "Harwood, ND"},
            {"@type": "AdministrativeArea", "name": "Cass County, ND"},
        ],
        "knowsAbout": [
            "Aluminum fence installation",
            "Vinyl fence installation",
            "Wood fence installation",
            "Metal fence installation",
            "Farm fencing",
            "Picket fencing",
            "Privacy fencing",
            "Chain-link fence installation",
            "Gate installation and repair",
            "Commercial fencing",
            "Fence repair",
            "Frost heave in Red River Valley clay",
            "Fargo residential fence height limits",
            "West Fargo fence rules",
        ],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Fence installation and repair",
            "itemListElement": offers,
        },
        "potentialAction": {
            "@type": "CommunicateAction",
            "name": "Request a fence estimate",
            "target": f"{SITE}/contact.html",
        },
    }


def graph(*nodes):
    website = {
        "@type": "WebSite",
        "@id": f"{SITE}/#website",
        "url": f"{SITE}/",
        "name": NAME,
        "publisher": {"@id": f"{SITE}/#business"},
        "inLanguage": "en-US",
    }
    payload = {"@context": "https://schema.org", "@graph": [business_node(), website, *nodes]}
    return json.dumps(payload, ensure_ascii=False)


def faq_node(page_id, items):
    return {
        "@type": "FAQPage",
        "@id": page_id,
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in items
        ],
    }


def head(path, title, description, image, schema, robots="index, follow"):
    url = canonical(path)
    title = esc(title)
    description = esc(description)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="robots" content="{robots}">
  <link rel="canonical" href="{url}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{url}">
  <meta property="og:site_name" content="{NAME}">
  <meta property="og:image" content="{SITE}/{image}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;600&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">
  <script type="application/ld+json">{schema}</script>
</head>
'''


def header(current):
    def a(href, label):
        cur = ' aria-current="page"' if href == current else ""
        return f'<a href="{href}"{cur}>{label}</a>'

    service_links = a("services.html", "All services") + "".join(
        a(s["slug"], s["nav"]) for s in SERVICES
    )
    area_links = a("service-areas.html", "All service areas") + "".join(
        a(loc["slug"], loc["nav"]) for loc in LOCATIONS
    )
    return f'''<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="topbar">
    <div class="container topbar-inner">
      <span>Free on-site estimates</span>
      <a href="tel:{TEL}">{PHONE}</a>
    </div>
  </div>
  <div class="container header-inner">
    <a class="logo-link" href="index.html" aria-label="Fargo Fence Company home"><img src="logo.svg" alt="Fargo Fence Company" width="280" height="56"></a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Open menu">{MENU_SVG}</button>
    <nav class="nav" id="site-nav" aria-label="Primary">
      {a("index.html", "Home")}
      <details>
        <summary>Services</summary>
        <div class="nav-panel">{service_links}</div>
      </details>
      <details>
        <summary>Service area</summary>
        <div class="nav-panel">{area_links}</div>
      </details>
      {a("faq.html", "FAQ")}
      {a("about.html", "About")}
      {a("contact.html", "Contact")}
    </nav>
    <div class="header-actions">
      {call_btn()}
      <a class="btn btn-primary" href="{quote_href(current)}">Get a free quote</a>
    </div>
  </div>
</header>
'''


OFFICE_HOURS_DAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
OFFICE_HOURS_TIME = "7 am – 7 pm"


def office_hours_block():
    rows = "".join(f"<div><span>{day}</span><span>{OFFICE_HOURS_TIME}</span></div>" for day in OFFICE_HOURS_DAYS)
    return f'<div class="hours-list">{rows}</div>'


def footer(current):
    service_li = "".join(f'<li><a href="{s["slug"]}">{s["nav"]}</a></li>' for s in SERVICES)
    qhref = quote_href(current)
    return f'''<footer class="site-footer">
  <div class="footer-accent"></div>
  <div class="container footer-grid">
    <div>
      <h2>Company</h2>
      <img src="logo.svg" alt="" width="280" height="56">
      <p style="margin-top:0.9rem">Fence installation and repair for homes, farms, and commercial lots in Fargo, ND and nearby Cass County and Clay County.</p>
      <a class="footer-phone" href="tel:{TEL}">{PHONE}</a>
      <ul style="margin-top:0.8rem">
        <li><a href="about.html">About</a></li>
        <li><a href="contact.html">Contact</a></li>
      </ul>
    </div>
    <div>
      <h2>Services</h2>
      <ul>{service_li}</ul>
    </div>
    <div>
      <h2>Quick links</h2>
      <ul>
        <li><a href="index.html">Home</a></li>
        <li><a href="services.html">Services</a></li>
        <li><a href="faq.html">FAQ</a></li>
        <li><a href="service-areas.html">Service areas</a></li>
        <li><a href="privacy.html">Privacy</a></li>
        <li><a href="sitemap.xml">Sitemap</a></li>
      </ul>
    </div>
    <div>
      <h2>Office Hours</h2>
      {office_hours_block()}
    </div>
  </div>
  <div class="container footer-base">
    <p>© 2026 Fargo Fence Company.</p>
    <p><a href="sitemap.xml">XML sitemap</a> · <a href="robots.txt">robots.txt</a></p>
  </div>
</footer>
<nav class="callbar" aria-label="Call or request a quote">
  <a class="btn btn-ink" href="tel:{TEL}">{PHONE_SVG}Call</a>
  <a class="btn btn-primary" href="{qhref}">Free quote</a>
</nav>
<script src="main.js"></script>
{TALLY_JS}
</body>
</html>
'''


def wrap(path, title, description, image, schema, body, robots="index, follow"):
    return head(path, title, description, image, schema, robots) + header(path) + body + footer(path)


def cta_band(heading="Get an estimate for this fence"):
    return f'''<section class="cta-band">
  <div class="container cta-inner">
    <div>
      <h2>{heading}</h2>
      <p>Call {PHONE} or send the town, the fence type, and roughly how much line you need.</p>
    </div>
    <div class="cta-actions">
      <a class="btn btn-light btn-lg" href="#quote">Get a free quote</a>
      {call_btn("btn btn-outline-light btn-lg")}
    </div>
  </div>
</section>'''


def tally_card():
    return f'''<div class="quote-card" id="quote">
      <h2>Get a free quote</h2>
      <p class="quote-note">Tell us the town, the fence type, and roughly how much line you need.</p>
      <iframe data-tally-src="{TALLY}" loading="lazy" width="100%" height="552" frameborder="0" marginheight="0" marginwidth="0" title="Get a free quote"></iframe>
    </div>'''


INTROS = {}


def intro_p(key):
    return f'<p class="lede intro">{INTROS[key]}</p>'


def hero_actions():
    return f'<div class="hero-actions">{call_btn("btn btn-primary btn-lg")}<a class="btn btn-ghost btn-lg" href="#quote">Get a free quote</a></div>'


def page_hero(key, crumb_items, h1, eyebrow=""):
    """Slim interior header: breadcrumb, H1, 5-6 sentence intro, and the quote form."""
    eb = f'<p class="eyebrow">{eyebrow}</p>' if eyebrow else ""
    return f'''<section class="page-hero">
  <div class="container hero-grid">
    <div class="hero-copy">
      {crumbs(crumb_items)}
      {eb}
      <h1>{h1}</h1>
      {intro_p(key)}
      {hero_actions()}
    </div>
    {tally_card()}
  </div>
</section>'''


def sections(blocks):
    """Wrap each block in a section with alternating backgrounds (plain, alt, plain, ...)."""
    out = []
    for i, inner in enumerate(blocks):
        alt = " section-alt" if i % 2 else ""
        out.append(f'<section class="section{alt}">\n{inner}\n</section>')
    return "\n".join(out)


def webpage_node(path, name, desc, about=None):
    url = canonical(path)
    node = {
        "@type": "WebPage",
        "@id": url + "#webpage",
        "url": url,
        "name": name,
        "description": desc,
        "isPartOf": {"@id": f"{SITE}/#website"},
        "publisher": {"@id": f"{SITE}/#business"},
        "inLanguage": "en-US",
    }
    if about:
        node["about"] = {"@id": about}
    return node


def breadcrumb_node(path, trail):
    url = canonical(path)
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"}]
    for i, (name, p) in enumerate(trail, 2):
        items.append({"@type": "ListItem", "position": i, "name": name, "item": canonical(p)})
    return {"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": items}


def towns_block(title="Towns we serve"):
    towns = "".join(f'<li><a href="{loc["slug"]}">{loc["nav"]}</a></li>' for loc in LOCATIONS)
    return f'''<div class="container">
    <h2>{title}</h2>
    <ul class="chips light-chips">{towns}</ul>
    <p class="towns-links"><a href="service-areas.html">Service areas</a> · <a href="services.html">All services</a> · <a href="#quote">Request an estimate</a></p>
  </div>'''


def service_card(slug, image, alt, title, text, more="View service"):
    return f'''<a class="service-card" href="{slug}">
        <span class="media">{img(image, alt)}</span>
        <span class="body"><h3>{title}</h3><p>{text}</p><span class="more">{more}</span></span>
      </a>'''


def reviews_block():
    """Only renders when genuine reviews exist in REVIEWS; otherwise the section is omitted."""
    if not REVIEWS:
        return ""
    cards = "".join(
        f'<figure class="review"><blockquote>{q}</blockquote><figcaption>{n}, {src}</figcaption></figure>'
        for q, n, src in REVIEWS
    )
    return f'''<div class="container">
    <div class="section-head"><p class="kicker">Reviews</p><h2>What customers say</h2></div>
    <div class="review-grid">{cards}</div>
  </div>'''


def service_gallery(s):
    """Primary service image plus one other service image."""
    order = [slug for slug, _ in s["related"]] + [o["slug"] for o in SERVICES]
    by_slug = {o["slug"]: o for o in SERVICES}
    shots = [s]
    for slug in order:
        o = by_slug.get(slug)
        if o and o["slug"] != s["slug"] and o["image"] != s["image"]:
            shots.append(o)
            break
    figs = "".join(f'<figure class="service-shot">{img(o["image"], o["alt"])}</figure>' for o in shots)
    return f'<div class="service-gallery">{figs}</div>'


def service_related(s):
    links = list(s["related"])
    seen = {slug for slug, _ in links} | {s["slug"]}
    for o in SERVICES:
        if len(links) >= 4:
            break
        if o["slug"] not in seen:
            links.append((o["slug"], o["nav"]))
            seen.add(o["slug"])
    return "".join(f'<li><a href="{slug}">{label}</a></li>' for slug, label in links[:4])


def service_page(s):
    schema = graph(
        webpage_node(s["slug"], s["h1"], s["description"], about=f"{SITE}/{s['slug']}#service"),
        {
            "@type": "Service",
            "@id": f"{SITE}/{s['slug']}#service",
            "name": s["schema_name"],
            "serviceType": s["nav"],
            "description": s["description"],
            "url": f"{SITE}/{s['slug']}",
            "provider": {"@id": f"{SITE}/#business"},
            "areaServed": {"@type": "AdministrativeArea", "name": "Cass County, ND"},
        },
        breadcrumb_node(s["slug"], [("Services", "services.html"), (s["nav"], s["slug"])]),
        faq_node(f"{SITE}/{s['slug']}#faq", s["faqs"]),
    )
    detail = f'''<div class="container service-layout">
    <div class="service-main">
      {service_gallery(s)}
      <div class="prose service-copy">
        <h2>When this fence is the right job</h2>
        <p>{s["when"]}</p>
        <h2>How the work goes</h2>
        {steps_html(s["steps"])}
        <p>{s["after"]}</p>
      </div>
    </div>
    <aside class="service-aside" aria-label="Estimate and related services">
      <div class="side-card">
        <p class="side-kicker">Talk through the line</p>
        <p>Call or send the town, the fence type, and a rough length. We will tell you if the job is a repair, a replacement, or a different material than you started with.</p>
        <p class="side-phone">{phone_link("phone-link-lg")}</p>
        <p class="side-hours">{OFFICE_HOURS}</p>
        <p><a class="btn btn-primary" href="#quote">Get a free quote</a></p>
      </div>
      <div class="side-card side-card-muted">
        <p class="side-kicker">Related</p>
        <ul class="side-links">{service_related(s)}</ul>
      </div>
    </aside>
  </div>'''
    factors = f'''<div class="container">
    <div class="section-head">
      <h2>What changes the estimate</h2>
      <p>We price the line on the lot. These are the pieces that move the number. We do not publish a per-foot menu.</p>
    </div>
    {factors_html(s["factors"])}
  </div>'''
    faqs = f'''<div class="container">
    <h2>Questions about {s["faq_label"]}</h2>
    <div class="block-gap">{faq_html(s["faqs"])}</div>
  </div>'''
    body = f'''<main id="main">
{page_hero(s["slug"], [("services.html", "Services"), (s["slug"], s["nav"])], s["h1"], eyebrow=s["nav"])}
{sections([detail, factors, faqs, towns_block()])}
{cta_band("Get an estimate for this fence")}
</main>
'''
    return wrap(s["slug"], s["title"], s["description"], s["image"], schema, body)


def location_page(loc):
    related = " · ".join(f'<a href="{slug}">{label}</a>' for slug, label in loc["related"])
    services = " · ".join(f'<a href="{slug}">{label}</a>' for slug, label in loc["services"])
    schema = graph(
        webpage_node(loc["slug"], loc["h1"], loc["description"], about=f"{SITE}/{loc['slug']}#place"),
        {
            "@type": "City",
            "@id": f"{SITE}/{loc['slug']}#place",
            "name": loc["place"],
            "containedInPlace": {"@type": "State", "name": loc["state"]},
        },
        breadcrumb_node(loc["slug"], [("Service areas", "service-areas.html"), (loc["nav"], loc["slug"])]),
        faq_node(f"{SITE}/{loc['slug']}#faq", loc["faqs"]),
    )
    paras = "".join(f"<p>{p}</p>" for p in loc["paras"])
    when = f'''<div class="container split">
    <div class="split-media">{img(loc["image"], loc["alt"])}</div>
    <div class="prose">
      <h2>What changes the fence here</h2>
      <p>{loc["when"]}</p>
    </div>
  </div>'''
    rules = f'''<div class="container prose narrow-prose">
    <h2>Ground, rules, and the line</h2>
    {paras}
    <p class="block-gap">Fences that fit this work: {services}</p>
  </div>'''
    faqs = f'''<div class="container">
    <h2>Questions about fencing in {loc["nav"]}</h2>
    <div class="block-gap">{faq_html(loc["faqs"])}</div>
    <p class="block-gap">Nearby: {related}</p>
  </div>'''
    body = f'''<main id="main">
{page_hero(loc["slug"], [("service-areas.html", "Service areas"), (loc["slug"], loc["nav"])], loc["h1"], eyebrow=loc["place"])}
{sections([when, rules, faqs])}
{cta_band("Request an estimate in " + loc["nav"])}
</main>
'''
    return wrap(loc["slug"], loc["title"], loc["description"], loc["image"], schema, body)


def load_content():
    global SERVICES, LOCATIONS, INTROS
    from content import SERVICES as S, LOCATIONS as L, INTROS as I
    SERVICES = S
    LOCATIONS = L
    INTROS = I


HOME_FAQS = [
    (
        "How much does a fence cost in Fargo, ND?",
        "The price follows the line we measure: length, height, material, gates, and whether an old fence comes out. Digging deep post holes in wet lake clay, a long carry from the driveway, and a gate that has to clear a mower all move the number. We do not publish a per-foot menu. The estimate comes from the property.",
    ),
    (
        "Can you set fence posts in Red River Valley clay so they do not heave?",
        "Yes. Fargo sits on lake-plain clay that holds water, and winter frost goes several feet down. A post set at a depth that works in a southern city will jack out of this ground. We set posts in concrete deep enough for the lot and crown the mix so meltwater does not sit against the post. If a hole is still full of water, we say so before we pour it.",
    ),
    (
        "Do you offer wood, vinyl, aluminum, chain link, metal, and farm fencing?",
        "Yes. Wood and vinyl cover privacy and picket work. Aluminum and heavier ornamental metal cover open lines. Chain link covers yards, dogs, and commercial perimeters. Farm fencing covers rail, wire, and pipe for animals on larger parcels. Repair and gates are part of the same call.",
    ),
    (
        "Do I need a permit to put up a fence in Fargo?",
        "The city’s inspections FAQ says a permit is not required unless the fence is more than 6½ feet. The residential fence handout says a permit is required when a fence exceeds 8½ feet. Those two pages do not match, so confirm with Inspections before you build over 6½ feet. Height limits still apply either way: 3 feet solid in a front yard, 4 feet if the fence is at least 75 percent open, and 6½ feet on the side and rear. Horace requires a fence permit. West Fargo uses a different height chart.",
    ),
    (
        "Can you repair a fence that leaned over the winter, or does the whole line have to come out?",
        "If the posts are still sound, we repair the section that failed and leave the rest. If the posts have heaved or rotted at the ground, new boards on those posts will lean again, and that stretch should be reset. Spring thaw is when this shows up. We will tell you which one you have after we see the line.",
    ),
]

FAQ_PAGE = HOME_FAQS + [
    (
        "Are West Fargo fence rules the same as Fargo’s?",
        "No. West Fargo limits a solid front-yard fence to 2 feet 6 inches. An open fence you can see through at least 50 percent may be 4 feet. Side and rear fences may be 6 feet, and the posts have to face your side of the property. Do not order a Fargo-height front fence for a West Fargo lot.",
    ),
    (
        "Does a Moorhead fence follow North Dakota rules?",
        "No. Moorhead is in Minnesota. The city says residential fences may go to the property line and that a permit is not required unless the fence is over 7 feet. Call 811 before digging. On that side of the river the locate is Gopher State One Call. The clay and the frost are the same problem as in Fargo.",
    ),
    (
        "Will vinyl survive a North Dakota winter?",
        "A vinyl fence built for cold will, if the posts do not heave and crack the rails. The plastic gets less forgiving below zero, so a hard impact can break a rail that would have flexed in summer. It does not need stain. If you want wood you can paint to the house, that is a different fence and a different upkeep plan.",
    ),
    (
        "Can you add privacy slats to chain link in the front yard?",
        "On the side and rear, usually yes, if the posts can take the extra wind. In a Fargo front yard, slats can drop the fence out of the 75 percent open category and pull the height limit from 4 feet back to 3 feet. If the goal is a solid screen, a privacy fence behind the front of the house is the cleaner layout.",
    ),
    (
        "What should I have ready when I ask for an estimate?",
        "The city, the address, what the fence has to do, and a rough length. Photos of the old fence help on a repair. If an association has a fence rule, send it. We still look at the ground before the price is final, because clay, access, and gates do not show up in a snapshot.",
    ),
]


HOME_TITLE = "Fence Company Fargo ND | Vinyl Fence, Wood Fence, Aluminum Fence & More"
HOME_H1 = "Fence Company Fargo ND"


def home_page():
    cards = "".join(service_card(s["slug"], s["image"], s["alt"], s["nav"], s["card"]) for s in SERVICES)
    chips = "".join(f'<li><a href="{loc["slug"]}">{loc["nav"]}</a></li>' for loc in LOCATIONS)
    gallery = [
        ("images/design-50.png", "Horizontal wood privacy fence beside a patio"),
        ("images/vinyl-privacy.jpg", "White vinyl privacy fence and gate along a lawn"),
        ("images/vinyl-semi.jpg", "White vinyl picket fence meeting a privacy panel at a corner"),
        ("images/design-55.png", "Black chain-link fence with privacy slats in part of the run"),
        ("images/aluminum.jpg", "Black aluminum fence with a walk gate along a lawn"),
        ("images/design-52.png", "Wood crossbuck rail fence along a lawn and trees"),
    ]
    figs = "".join(f"<figure>{img(src, alt)}</figure>" for src, alt in gallery)
    desc = "Fargo Fence Company installs and repairs wood, vinyl, aluminum, chain-link, metal, and farm fencing in Fargo and nearby Cass County. Call (701) 394-8468."
    schema = graph(
        webpage_node("index.html", HOME_H1, desc, about=f"{SITE}/#business"),
        faq_node(f"{SITE}/#faq", HOME_FAQS),
    )
    why_items = [
        ("Quoted from the property", "Every estimate comes from the lot, not from a catalog price. Length, height, gates, access, and the ground are all measured before a number is given."),
        ("Posts set for clay and frost", "Fargo sits on lake-plain clay that holds water, and frost heave is the usual way a fence fails. Posts go in concrete deep enough for this ground, crowned so meltwater sheds off them."),
        ("Every common fence material", "Wood, vinyl, aluminum, ornamental metal, chain link, and farm fencing, plus gates and repair, all from one call."),
        ("City rules checked first", "Fargo, West Fargo, Horace, and Moorhead each write their own height and permit rules. We build to the city the lot is in, and to an association rule when it is stricter."),
        ("Straight repair advice", "If the posts are sound, we fix the failed section. If they have heaved, we say so, even when that means a smaller job."),
        ("Free on-site estimates", f"Office hours are 7 am to 7 pm, Monday through Sunday. Call {PHONE} or send the form and we schedule a visit to the property."),
    ]
    why = f'''<div class="container">
    <div class="section-head">
      <p class="kicker">Why choose us</p>
      <h2>Why Choose Fargo Fence Company</h2>
      <p>A fence in the Red River Valley has to survive frost, wet clay, and prairie wind. These are the things we do on every job.</p>
    </div>
    {factors_html(why_items)}
  </div>'''
    services = f'''<div class="container">
    <div class="section-head">
      <p class="kicker">Materials and work</p>
      <h2>Fence services in Fargo</h2>
      <p>Start with the job. A front-yard picket, a backyard screen, a dog run, and a pasture line are not the same fence.</p>
    </div>
    <div class="card-grid services">{cards}</div>
    <div class="split-2 block-gap-lg">
      <div class="panel">
        <h3>Houses</h3>
        <p>Backyard privacy, pet runs, and property-line replacements. In Fargo a solid front-yard fence stops at 3 feet, and an open fence may go to 4 feet. The taller wood or vinyl line belongs on the side and rear. West Fargo’s front-yard numbers are shorter. We use the city the lot is in.</p>
        <a class="more" href="privacy-fence.html">Privacy fencing</a>
      </div>
      <div class="panel">
        <h3>Lots and acreage</h3>
        <p>A storage yard needs heavier chain link and a vehicle gate. A pasture toward Casselton or Harwood needs rail or wire sized for the animals, not a backyard panel. Tell us how the ground is used and we will spec the line for that use.</p>
        <a class="more" href="farm-fence.html">Farm fencing</a>
      </div>
    </div>
  </div>'''
    gallery_block = f'''<div class="container">
    <div class="section-head">
      <p class="kicker">Gallery</p>
      <h2>Fences we install</h2>
      <p>Privacy, vinyl, chain link, aluminum, and rail from the crew that walks the line in Fargo and Cass County.</p>
    </div>
    <div class="gallery">{figs}</div>
    <p class="block-gap"><a class="more-link" href="services.html">See all fence services</a></p>
  </div>'''
    process = f'''<div class="container split-2">
    <div>
      <h2>How a fence job is quoted</h2>
      <ol class="steps">
        <li><span class="num">1</span><span><strong>Name the job.</strong> Screen a yard, contain animals, mark a frontage, or secure a lot. That choice picks the material faster than a photo.</span></li>
        <li><span class="num">2</span><span><strong>Walk the ground.</strong> This valley is flat, but the clay holds water and frost heave is the usual failure. Ditches, corners, and a long carry from the truck change the labor.</span></li>
        <li><span class="num">3</span><span><strong>Count the openings.</strong> A fence with the wrong gate is a daily problem. Walk gates and drive gates are priced as their own pieces.</span></li>
        <li><span class="num">4</span><span><strong>Repair or replace.</strong> Sound posts can take new panels. Posts that heaved over the winter cannot. We say which one you have.</span></li>
      </ol>
    </div>
    <div class="panel">
      <h2>Repairs and gates</h2>
      <p>Leaning posts, split rails, and gates that no longer latch are a large share of the calls after the ground thaws. If the rest of the line is sound, we repair the failed section.</p>
      <p>Gates are hung on posts sized for the opening. A walk gate and a drive gate are different builds, and an opener is not a patch for a post that moved.</p>
      <a class="more" href="fence-repair.html">Fence repair</a>
    </div>
  </div>'''
    areas = f'''<div class="container">
    <h2>Service area</h2>
    <p class="area-note">We work in Fargo and nearby communities, roughly a 25-mile drive, including the Minnesota side of the river. Each city writes its own fence rules. The clay does not change at the city limit.</p>
    <ul class="chips light-chips">{chips}</ul>
    <p class="towns-links"><a href="service-areas.html">All service areas</a></p>
  </div>'''
    faqs = f'''<div class="container">
    <h2>Questions before you call</h2>
    <div class="block-gap">{faq_html(HOME_FAQS)}</div>
    <p class="block-gap"><a class="more-link" href="faq.html">More fence questions</a></p>
  </div>'''
    blocks = [why, services, gallery_block]
    reviews = reviews_block()
    if reviews:
        blocks.append(reviews)
    blocks += [process, areas, faqs]
    body = f'''<main id="main">
<section class="hero">
  <div class="hero-media">{img("images/hero-bg.jpg", "White vinyl privacy fence along a landscaped backyard", loading=None, extra=' fetchpriority="high"')}</div>
  <div class="hero-shade"></div>
  <div class="container hero-grid">
    <div class="hero-copy">
      <p class="eyebrow">Fargo, North Dakota</p>
      <h1>{HOME_H1}</h1>
      {intro_p("home")}
      {hero_actions()}
    </div>
    {tally_card()}
  </div>
</section>
{sections(blocks)}
{cta_band("Ready to walk the line?")}
</main>
'''
    return wrap("index.html", HOME_TITLE, desc, "images/vinyl-privacy.jpg", schema, body)


def faq_page():
    desc = "Fence cost, permits, frost heave, and repairs in Fargo, West Fargo, and Moorhead. Straight answers from Fargo Fence Company."
    schema = graph(
        webpage_node("faq.html", "Fence FAQ for Fargo, ND", desc),
        faq_node(f"{SITE}/faq.html#faq", FAQ_PAGE),
        breadcrumb_node("faq.html", [("FAQ", "faq.html")]),
    )
    faqs = f'''<div class="container">
    {faq_html(FAQ_PAGE)}
    <p class="block-gap"><a href="#quote">Request an estimate</a> or call <a href="tel:{TEL}">{PHONE}</a>.</p>
  </div>'''
    body = f'''<main id="main">
{page_hero("faq", [("faq.html", "FAQ")], "Fence questions in Fargo")}
{sections([faqs, towns_block("Where we answer these questions")])}
{cta_band("Still have a fence question?")}
</main>
'''
    return wrap("faq.html", "Fence FAQ for Fargo, ND | Fargo Fence Company", desc, "images/vinyl-privacy.jpg", schema, body)


def about_page():
    desc = "Fargo Fence Company installs and repairs fences for homes, farms, and commercial lots around Fargo, ND. Estimates are made on the property."
    schema = graph(
        webpage_node("about.html", "About Fargo Fence Company", desc, about=f"{SITE}/#business"),
        breadcrumb_node("about.html", [("About", "about.html")]),
    )
    prose = f'''<div class="container prose narrow-prose">
    <h2>What we do</h2>
    <p>The work is wood, vinyl, aluminum, ornamental metal, chain link, farm fencing, gates, and repair. A front-yard picket and a pasture line are different products. We ask what the fence has to do before we name a material.</p>
    <p>This is a service-area business. There is no public storefront and no published street address. Estimates are scheduled at the property. Call {PHONE} or use the form.</p>
    <h2>How an estimate works</h2>
    <p>Tell us the city, the fence type, and a rough length. We look at access, gates, the old fence if there is one, and the ground. Fargo clay holds water, and shallow posts heave. That digging is part of the price, which is why a per-foot number from another climate does not transfer.</p>
    <p>City rules do not transfer either. Fargo, West Fargo, Horace, and Moorhead each write their own height and permit lines. If an association has a fence sheet, bring it. We build to the stricter rule.</p>
    <p><a href="service-areas.html">See the service area</a> or <a href="services.html">browse the services</a>.</p>
  </div>'''
    body = f'''<main id="main">
{page_hero("about", [("about.html", "About")], "About Fargo Fence Company")}
{sections([prose, towns_block("Where we work")])}
{cta_band("Talk through the line")}
</main>
'''
    return wrap("about.html", "About Fargo Fence Company", desc, "images/vinyl-privacy.jpg", schema, body)


def contact_page():
    desc = "Request a fence estimate from Fargo Fence Company. Call (701) 394-8468. Service-area business, no public storefront."
    schema = graph(
        webpage_node("contact.html", "Contact Fargo Fence Company", desc),
        breadcrumb_node("contact.html", [("Contact", "contact.html")]),
    )
    info = f'''<div class="container contact-layout">
    <div class="prose">
      <h2>What helps us price it</h2>
      <p>The town matters because Fargo, West Fargo, Horace, and Moorhead do not share a height chart. A photo of the old fence helps on a repair. An association rule helps on a newer plat.</p>
      <p>We are a service-area business. There is no showroom. The map is the area we drive, not a storefront pin.</p>
      <p><a class="footer-phone-dark" href="tel:{TEL}">{PHONE}</a></p>
      <div class="hours-card"><h3>Office hours</h3>{office_hours_block()}</div>
    </div>
    <div class="map-frame">
      <iframe title="Map of the Fargo area we serve" src="https://www.openstreetmap.org/export/embed.html?bbox=-97.25%2C46.72%2C-96.55%2C47.02&amp;layer=mapnik" loading="lazy"></iframe>
      <p class="map-caption">About a 25-mile drive around Fargo, including West Fargo, Horace, Moorhead, and nearby Cass County. No public storefront.</p>
    </div>
  </div>'''
    body = f'''<main id="main">
{page_hero("contact", [("contact.html", "Contact")], "Request a fence estimate")}
{sections([info, towns_block("Towns we drive to")])}
</main>
'''
    return wrap("contact.html", "Contact Fargo Fence Company | Free Fence Estimate", desc, "images/vinyl-privacy.jpg", schema, body)


def services_page():
    desc = "Wood, vinyl, aluminum, metal, chain-link, picket, privacy, farm, commercial fencing, gates, and repair in Fargo, ND."
    cards = "".join(service_card(s["slug"], s["image"], s["alt"], s["nav"], s["card"]) for s in SERVICES)
    schema = graph(
        webpage_node("services.html", "Fence services in Fargo, ND", desc),
        breadcrumb_node("services.html", [("Services", "services.html")]),
    )
    grid = f'''<div class="container">
    <div class="card-grid services">{cards}</div>
  </div>'''
    body = f'''<main id="main">
{page_hero("services", [("services.html", "Services")], "Fence services in Fargo")}
{sections([grid, towns_block()])}
{cta_band("Which fence fits your yard?")}
</main>
'''
    return wrap("services.html", "Fence Services in Fargo, ND | Fargo Fence Company", desc, "images/vinyl-privacy.jpg", schema, body)


def areas_page():
    desc = "Fence installation around Fargo, West Fargo, Moorhead, Horace, Dilworth, Casselton, Mapleton, Harwood, and Cass County."
    cards = "".join(
        service_card(loc["slug"], loc["image"], loc["alt"], loc["nav"], loc["lede"], more="View area")
        for loc in LOCATIONS
    )
    schema = graph(
        webpage_node("service-areas.html", "Fence service areas around Fargo, ND", desc),
        breadcrumb_node("service-areas.html", [("Service areas", "service-areas.html")]),
    )
    grid = f'''<div class="container">
    <div class="card-grid services">{cards}</div>
  </div>'''
    note = f'''<div class="container prose narrow-prose">
    <h2>Fargo and towns not listed</h2>
    <p>Fargo itself is covered from the <a href="index.html">home page</a>. If your town is inside the drive and it is not listed, call {PHONE} and ask. We would rather say no than stretch a city rule onto the wrong parcel.</p>
  </div>'''
    body = f'''<main id="main">
{page_hero("areas", [("service-areas.html", "Service areas")], "Service areas around Fargo")}
{sections([grid, note])}
{cta_band("Request an estimate in your town")}
</main>
'''
    return wrap("service-areas.html", "Fence Service Areas around Fargo, ND", desc, "images/vinyl-privacy.jpg", schema, body)


def privacy_page():
    desc = "How Fargo Fence Company uses the estimate form. We use your details to reply to the request."
    schema = graph(
        webpage_node("privacy.html", "Privacy policy", desc),
        breadcrumb_node("privacy.html", [("Privacy", "privacy.html")]),
    )
    prose = f'''<div class="container prose narrow-prose">
    <p>The quote form is embedded from Tally. Submissions include the information you type, plus a hidden source field set to “Fargo Fence Company” so we can see which site the request came from. We use that information to respond to the estimate. We do not sell it.</p>
    <p>Phone calls to {PHONE} are answered as normal business calls. This site does not run a customer account or a payment page. Do not send card numbers or other payment details through the form.</p>
    <p>To ask about a submission, call {PHONE}.</p>
  </div>'''
    body = f'''<main id="main">
{page_hero("privacy", [("privacy.html", "Privacy")], "Privacy")}
{sections([prose])}
</main>
'''
    return wrap("privacy.html", "Privacy Policy | Fargo Fence Company", desc, "images/vinyl-privacy.jpg", schema, body)


def not_found_page():
    desc = "That page is not on the Fargo Fence Company site."
    schema = graph(webpage_node("404.html", "Page not found", desc))
    nxt = f'''<div class="container prose narrow-prose">
    <h2>Where to go next</h2>
    <p><a href="index.html">Home</a> · <a href="services.html">Fence services</a> · <a href="service-areas.html">Service areas</a> · <a href="faq.html">FAQ</a> · <a href="contact.html">Contact</a></p>
  </div>'''
    body = f'''<main id="main">
{page_hero("notfound", [("404.html", "Page not found")], "Page not found")}
{sections([nxt])}
</main>
'''
    return wrap("404.html", "Page not found | Fargo Fence Company", desc, "images/vinyl-privacy.jpg", schema, body, robots="noindex, follow")


def write_sitemap(paths):
    urls = []
    for path in paths:
        loc = canonical(path)
        urls.append(f"  <url><loc>{loc}</loc></url>")
    xml = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
''' + "\n".join(urls) + "\n</urlset>\n"
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")


def write_robots():
    (ROOT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\nSitemap: https://www.fargofencecompany.net/sitemap.xml\n",
        encoding="utf-8",
    )


def sentence_count(text):
    return len([x for x in re.split(r"(?<=[.!?])\s+", text.strip()) if x])


def audit_intros(pages):
    """Every page intro must be 5-6 sentences and start with the business name."""
    bad = []
    for name, page in pages.items():
        m = re.search(r'<p class="lede intro">(.*?)</p>', page, re.S)
        if not m:
            bad.append((name, "no intro"))
            continue
        text = re.sub(r"<[^>]+>", "", m.group(1))
        n = sentence_count(text)
        if not text.startswith(NAME) or not 5 <= n <= 6:
            bad.append((name, n, text[:40]))
        if name == "index.html":
            h1 = re.search(r"<h1>(.*?)</h1>", page).group(1)
            assert h1 == "Fence Company Fargo ND", h1
            assert f"<title>{esc(HOME_TITLE)}</title>" in page
    if bad:
        print("INTRO PROBLEMS")
        for b in bad:
            print(b)
        raise SystemExit(1)
    print("Intros OK: 5-6 sentences, start with", NAME)


def main():
    load_content()
    pages = {
        "index.html": home_page(),
        "services.html": services_page(),
        "service-areas.html": areas_page(),
        "faq.html": faq_page(),
        "about.html": about_page(),
        "contact.html": contact_page(),
        "privacy.html": privacy_page(),
        "404.html": not_found_page(),
    }
    for s in SERVICES:
        pages[s["slug"]] = service_page(s)
    for loc in LOCATIONS:
        pages[loc["slug"]] = location_page(loc)
    for name, html in pages.items():
        (ROOT / name).write_text(html, encoding="utf-8")
    sitemap_paths = [p for p in pages if p != "404.html"]
    write_sitemap(sitemap_paths)
    write_robots()
    # internal link check
    missing = []
    for name, html in pages.items():
        for href in __import__("re").findall(r'href="([^"]+)"', html):
            if href.startswith(("http", "tel:", "mailto:", "#", "sitemap", "robots")):
                continue
            target = href.split("#")[0]
            if target and target not in pages and not target.startswith("images/") and not target.endswith((".svg", ".css", ".js", ".xml", ".txt", ".jpg", ".png")):
                missing.append((name, href))
    print(f"Wrote {len(pages)} pages")
    if missing:
        print("MISSING LINKS")
        for item in missing:
            print(item)
        raise SystemExit(1)
    audit_intros(pages)
    lengths = [len(s["card"]) for s in SERVICES]
    print("Card lengths", min(lengths), max(lengths))


if __name__ == "__main__":
    main()
