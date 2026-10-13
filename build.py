"""Builds the Quantum Leap website into site/.

Header, footer and page shells live here once; each page only defines its own body.
Run:  python build.py            (vacancies come from jobs.json)
      python build.py --drafts   (also shows unpublished jobs, for previewing only; don't push this build)
Outputs site/index.html, about.html, services.html, careers.html, contact.html (full pages for any web host)
and _preview-home.html next to this script (the home page body, used only for the Claude preview; not part of the website).
"""
import html
import json
import sys
from datetime import date
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).parent
OUT = ROOT / "site"
SHOW_DRAFTS = "--drafts" in sys.argv

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800'
         '&family=Figtree:ital,wght@0,400;0,500;0,600;1,500&family=IBM+Plex+Mono:wght@400;500&display=swap">\n'
         '<link rel="stylesheet" href="styles.css">')

PHONE = "0802 303 2178"
PHONE_INTL = "+2348023032178"
WHATSAPP = "0802 303 2178"
WA_LINK = "https://wa.me/2348023032178"
EMAIL = "Quantumleapm@yahoo.com"
ADDRESS = "Suite 26, Mobolaji Shopping Plaza, Ikota Bridge, Ikota, Lagos"
IG = "https://www.instagram.com/quantum.leap.management/"
FB = "https://www.facebook.com/quantumleapmgtservices/"
MAP = "https://www.google.com/maps/search/?api=1&query=Mobolaji+Shopping+Plaza+Ikota+Lagos"


def icon(name, size=22):
    paths = {
        "building": '<path d="M3 21h18M5 21V7l7-4 7 4v14M9 21v-6h6v6M9 10h.01M15 10h.01"/>',
        "broom": '<path d="M7 3h10l-1 6H8L7 3zM6 9h12l-1 12H7L6 9zM10 13v4M14 13v4"/>',
        "crane": '<path d="M2 20h20M4 20V10l5-3v13M9 20V5l7 3v12M16 20v-8l4 2v6"/>',
        "home": '<path d="M3 11l9-7 9 7M5 10v10h14V10M10 20v-5h4v5"/>',
        "people": '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6M16 4.5a3 3 0 0 1 0 6M21 20c0-2.6-1.6-4.8-4-5.6"/>',
        "process": '<path d="M4 6h10M4 12h16M4 18h10"/><circle cx="18" cy="6" r="2"/><circle cx="18" cy="18" r="2"/>',
        "chip": '<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/>',
        "medal": '<circle cx="12" cy="14" r="6"/><path d="M8.5 9.2L6 2h4l2 5 2-5h4l-2.5 7.2"/>',
        "wrench": '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.6 2.6-2.4-.6-.6-2.4 2.6-2.6z"/>',
        "bolt": '<path d="M13 2L4 14h7l-1 8 9-12h-7l1-8z"/>',
        "shield": '<path d="M12 3l8 3v6c0 4.5-3.4 8.3-8 9-4.6-.7-8-4.5-8-9V6l8-3z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
        "phone": '<path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2z"/>',
        "chat": '<path d="M21 12a8.5 8.5 0 0 1-12.6 7.4L3 21l1.6-5.2A8.5 8.5 0 1 1 21 12z"/>',
        "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
        "pin": '<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
        "ig": '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".8" fill="currentColor"/>',
        "fb": '<path d="M14 8h3V4h-3a4 4 0 0 0-4 4v3H7v4h3v6h4v-6h3l1-4h-4V8z"/>',
        "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    }
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths[name]}</svg>')


LOGO = ('<svg width="38" height="38" viewBox="0 0 40 40" aria-hidden="true"><defs><linearGradient id="ring{n}" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#1aa3b5"/><stop offset="1" stop-color="#4d5ff0"/></linearGradient></defs>'
        '<circle cx="20" cy="20" r="16.5" fill="none" stroke="url(#ring{n})" stroke-width="4"/>'
        '<path d="M20 9v17" stroke="url(#ring{n})" stroke-width="3.2" stroke-linecap="round"/>'
        '<circle cx="20" cy="30" r="3" fill="url(#ring{n})"/></svg>')

NAV = [("index.html", "Home", "home"), ("about.html", "About us", "about"),
       ("services.html", "Services", "services"), ("careers.html", "Careers", "careers"),
       ("contact.html", "Contact", "contact")]


def header(active):
    links = "".join(
        f'<a href="{href}"{" aria-current=\"page\"" if key == active else ""}>{label}</a>' for href, label, key in NAV)
    return f'''<div class="strip"><div class="wrap">
  <span>Call or WhatsApp: <b>{PHONE}</b></span>
  <span class="hide-sm">{EMAIL}</span>
  <span class="socials-mini"><a href="{IG}" target="_blank" rel="noopener">Instagram</a><a href="{FB}" target="_blank" rel="noopener">Facebook</a></span>
</div></div>
<header class="site"><div class="wrap">
  <a class="brand" href="index.html" aria-label="Quantum Leap Management Services, home">{LOGO.format(n=1)}<span><b>Quantum Leap</b><small>Management Services Ltd</small></span></a>
  <button class="menu-btn" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="mainnav">{icon("menu")}</button>
  <nav class="main" id="mainnav" aria-label="Main">{links}<a class="btn btn-primary" href="contact.html#audit">Book a free audit</a></nav>
  <a class="btn btn-primary cta" href="contact.html#audit">Book a free audit</a>
</div></header>'''


FOOTER = f'''<footer class="site">
  <div class="wrap cols">
    <div class="about-f">
      <a class="brand" href="index.html">{LOGO.format(n=2)}<span><b>Quantum Leap</b><small>Management Services Ltd</small></span></a>
      <p>Trusted facility managers since 2012. Supporting your critical infrastructure needs.</p>
      <div class="social"><a href="{IG}" target="_blank" rel="noopener" aria-label="Instagram">{icon("ig", 18)}</a><a href="{FB}" target="_blank" rel="noopener" aria-label="Facebook">{icon("fb", 18)}</a></div>
    </div>
    <div><h3>Company</h3><ul><li><a href="index.html">Home</a></li><li><a href="about.html">About us</a></li><li><a href="services.html">Services</a></li><li><a href="careers.html">Careers</a></li><li><a href="contact.html">Contact</a></li></ul></div>
    <div><h3>Services</h3><ul><li><a href="services.html#facility">Facility management</a></li><li><a href="services.html#janitorial">Janitorial services</a></li><li><a href="services.html#post-construction">Post-construction cleaning</a></li><li><a href="services.html#real-estate">Real estate services</a></li><li><a href="services.html#audit">Free facility audit</a></li></ul></div>
    <div><h3>Get in touch</h3><ul><li>{ADDRESS}</li><li>Phone and WhatsApp: {PHONE}</li><li>{EMAIL}</li></ul></div>
  </div>
  <div class="bottom"><div class="wrap"><span>© <span id="year">2026</span> Quantum Leap Management Services Ltd. All rights reserved.</span><span>Ikota, Lagos, Nigeria</span></div></div>
</footer>
<script src="site.js"></script>'''


def cta_band():
    return f'''<section class="cta-band"><div class="wrap">
  <div><h2>Ready to give your property the care it deserves?</h2><p>Book a free facility audit, or send us a message and we'll get back to you.</p></div>
  <div class="ctas"><a class="btn btn-light" href="contact.html#audit">Book a free audit</a><a class="btn btn-outline-light" href="{WA_LINK}" target="_blank" rel="noopener">Chat on WhatsApp</a></div>
</div></section>'''


# ---------------------------------------------------------------- pages

HOME = f'''<main>
<section class="hero"><div class="wrap">
  <div>
    <div class="since"><span>Since 2012</span><p class="eyebrow">Facility management · Lagos</p></div>
    <h1>Trusted <span>facility managers</span> for Lagos properties</h1>
    <p class="tagline">Supporting your critical infrastructure needs.</p>
    <p class="lede">Your property is one of your biggest investments. We take care of the maintenance, cleaning and day-to-day running, so it stays safe, clean and valuable, and you have one less thing to worry about.</p>
    <div class="ctas"><a class="btn btn-primary" href="contact.html#audit">Book a free facility audit</a><a class="btn btn-ghost" href="services.html">Explore our services</a></div>
  </div>
  <div class="hero-media">
    <img class="main-img" src="img/hero.jpg" alt="Engineer in a hard hat and safety vest filling in an inspection checklist" width="1100" height="1056">
    <div class="badge"><span class="stamp">Free</span><b>Facility audit</b><span>We assess your property and show you what needs attention.</span></div>
  </div>
</div></section>

<section class="block"><div class="wrap">
  <div class="sec-head">
    <div><p class="eyebrow">What we do</p><h2>A one-stop shop for all your property needs</h2></div>
    <p>From routine maintenance to a deep clean after construction, one team takes care of it all. Choose a single service or combine them.</p>
  </div>
  <div class="svc-grid">
    <a class="svc-card" href="services.html#facility"><img src="img/facility.jpg" alt="Residential high-rise in Lagos" loading="lazy"><div class="body"><h3>Facility management</h3><p>Planned and reactive maintenance that keeps your building working.</p><span class="more arrow">Learn more </span></div></a>
    <a class="svc-card" href="services.html#janitorial"><img src="img/janitorial.jpg" alt="Cleaning crew in red overalls at work in a modern apartment" loading="lazy"><div class="body"><h3>Janitorial services</h3><p>Reliable daily, weekly or one-off cleaning by supervised crews.</p><span class="more arrow">Learn more </span></div></a>
    <a class="svc-card" href="services.html#post-construction"><img src="img/post-construction.jpg" alt="Cleaner in overalls washing the windows of a newly finished home" loading="lazy"><div class="body"><h3>Post-construction cleaning</h3><p>Dust, debris and stains cleared so your property is ready to use.</p><span class="more arrow">Learn more </span></div></a>
    <a class="svc-card" href="services.html#real-estate"><img src="img/real-estate.jpg" alt="Real estate agent holding house keys and a SOLD sign" loading="lazy"><div class="body"><h3>Real estate services</h3><p>Property management and guidance for owners and buyers.</p><span class="more arrow">Learn more </span></div></a>
  </div>
</div></section>

<section class="block alt"><div class="wrap split">
  <div class="media"><img src="img/team.jpg" alt="Team meeting in an office in Lagos" loading="lazy"></div>
  <div class="copy">
    <p class="eyebrow">About Quantum Leap</p>
    <h2>Helping clients manage, maintain, improve and transform their properties</h2>
    <p>We are an integrated facility management, real estate and property solutions company. We work across residential, commercial and mixed-use developments in Lagos, and we have been doing it since 2012.</p>
    <ul class="ticks"><li>A team of professional facility managers</li><li>One point of contact for every service</li><li>Quality service and care for every property</li></ul>
    <a class="btn btn-primary arrow" href="about.html">More about us </a>
  </div>
</div></section>

<section class="block"><div class="wrap">
  <div class="sec-head">
    <div><p class="eyebrow">Why choose us</p><h2>Four reasons to trust us with your property</h2></div>
    <p>Trust and facility management go hand in hand. This is what you get when you work with Quantum Leap.</p>
  </div>
  <div class="why">
    <div class="reason"><span class="ic">{icon("medal")}</span><h3>Expertise and experience</h3><p>Professional facility managers serving Lagos properties since 2012.</p></div>
    <div class="reason"><span class="ic">{icon("wrench")}</span><h3>Maintenance and repairs</h3><p>We fix what's broken and keep up the routine work that stops it breaking again.</p></div>
    <div class="reason"><span class="ic">{icon("bolt")}</span><h3>Fast and reliable support</h3><p>Call or WhatsApp us and a real person picks it up and follows it through.</p></div>
    <div class="reason"><span class="ic">{icon("shield")}</span><h3>Smart maintenance and care</h3><p>Planned upkeep that protects your property's value over time.</p></div>
  </div>
</div></section>

<section class="block tight"><div class="wrap">
  <div class="audit-band">
    <div>
      <p class="eyebrow" style="color:#cfe9ee">Is your property performing at its best?</p>
      <h2 style="margin-top:10px">Book a free facility audit</h2>
      <p>Our experts inspect your property and help you find problems before they affect your property, tenants, employees or visitors.</p>
      <div class="ctas"><a class="btn btn-light" href="contact.html#audit">Book your audit</a></div>
    </div>
    <ul><li>Building condition assessment</li><li>Maintenance and repair review</li><li>Cleaning and hygiene assessment</li></ul>
  </div>
</div></section>

<section class="block alt"><div class="wrap split flip">
  <div class="media"><img src="img/moving-in.jpg" alt="Couple carrying boxes into their new home" loading="lazy"></div>
  <div class="copy">
    <p class="eyebrow">Just bought a home in Lagos?</p>
    <h2>Before you unpack, get the house ready</h2>
    <p>Buying a home in Lagos is a big deal. A well-maintained home is more comfortable and holds its value better over time. We inspect, clean and fix the small things before you move in.</p>
    <a class="btn btn-primary arrow" href="services.html#new-home">See our move-in checklist </a>
  </div>
</div></section>
</main>
{cta_band()}'''

ABOUT = f'''<main>
<section class="page-hero"><div class="wrap">
  <p class="crumbs"><a href="index.html">Home</a> / About us</p>
  <p class="eyebrow">About us</p>
  <h1>Trusted facility managers since 2012</h1>
  <p class="lede">We are a team of management service professionals who support the critical infrastructure needs of property owners across Lagos.</p>
</div></section>

<section class="block"><div class="wrap split">
  <div class="copy">
    <p class="eyebrow">Who we are</p>
    <h2>An integrated facility management, real estate and property solutions company</h2>
    <p>Quantum Leap Management Services Ltd helps clients manage, maintain, improve and transform their properties across residential, commercial and mixed-use developments.</p>
    <p>We offer property management solutions as a one-stop shop for all your property needs. We provide quality services and care that help every property reach its full potential.</p>
    <div class="facts">
      <div class="fact"><b>2012</b><span>Year we started</span></div>
      <div class="fact"><b>4</b><span>Core services under one roof</span></div>
      <div class="fact"><b>Lagos</b><span>Office in Ikota</span></div>
    </div>
  </div>
  <div class="media"><img src="img/about-house.jpg" alt="Newly built house in Abuja" loading="lazy"></div>
</div></section>

<section class="block alt"><div class="wrap split flip">
  <div class="copy">
    <p class="eyebrow">Our goal</p>
    <p class="quote-block">"Our goal is to support your critical infrastructure needs."</p>
    <p>A property loses value quietly. Blocked drains, hidden maintenance issues, poor cleaning and safety risks all add up. We find and fix these early, so owners and tenants can get on with their lives and work.</p>
  </div>
  <div class="media"><img src="img/engineer.jpg" alt="Engineer in a hard hat at an electrical substation in Nigeria" loading="lazy"></div>
</div></section>

<section class="block band"><div class="wrap">
  <div class="sec-head">
    <div><p class="eyebrow">Our approach</p><h2>We stand on the four pillars of facility management</h2></div>
    <p>A building only runs well when all four work together. We plan every contract around them.</p>
  </div>
  <div class="pillars">
    <div class="pillar"><span class="ic">{icon("people")}</span><h3>People</h3><p>Trained, supervised staff who know your property and the people who use it.</p></div>
    <div class="pillar"><span class="ic">{icon("process")}</span><h3>Process</h3><p>Clear schedules, checklists and reporting, so nothing depends on memory.</p></div>
    <div class="pillar"><span class="ic">{icon("building")}</span><h3>Building</h3><p>The structure, systems and equipment, kept in good working order.</p></div>
    <div class="pillar"><span class="ic">{icon("chip")}</span><h3>Technology</h3><p>Smart tools to track maintenance, log issues and respond faster.</p></div>
  </div>
</div></section>

<section class="block"><div class="wrap">
  <div class="sec-head">
    <div><p class="eyebrow">Who we work with</p><h2>Properties we look after</h2></div>
    <p>Whatever the size of your property, a well-run facility starts with the right partner.</p>
  </div>
  <div class="chips"><span>Residential estates</span><span>Private homes</span><span>Offices</span><span>Plazas and shopping centres</span><span>Schools</span><span>Hospitals</span><span>Commercial property</span><span>Mixed-use developments</span></div>
</div></section>
</main>
{cta_band()}'''

SERVICES = f'''<main>
<section class="page-hero"><div class="wrap">
  <p class="crumbs"><a href="index.html">Home</a> / Services</p>
  <p class="eyebrow">Our services</p>
  <h1>Everything your property needs, under one roof</h1>
  <p class="lede">Choose one service or combine them. Every job comes with a clear scope, trained staff and one contact who answers your calls.</p>
</div></section>

<section class="block"><div class="wrap">
  <article class="svc-detail" id="facility">
    <div class="media"><img src="img/facility.jpg" alt="Residential high-rise in Lagos" loading="lazy"></div>
    <div class="copy">
      <span class="num">Service 01</span>
      <h2>Facility management</h2>
      <p>We keep your building, its systems and its common areas working properly, with planned maintenance and fast repairs when something goes wrong.</p>
      <ul class="ticks"><li>Routine maintenance and repairs</li><li>Plumbing and drainage</li><li>Electrical and generator checks</li><li>Safety inspections</li><li>Supervision of vendors and artisans</li></ul>
      <a class="btn btn-primary" href="contact.html#facility">Request facility management</a>
    </div>
  </article>
  <article class="svc-detail" id="janitorial">
    <div class="media"><img src="img/janitorial.jpg" alt="Cleaning crew in red overalls at work in a modern apartment" loading="lazy"></div>
    <div class="copy">
      <span class="num">Service 02</span>
      <h2>Janitorial services</h2>
      <p>Supervised cleaning crews on a daily, weekly or one-off schedule, for homes, offices and shared spaces.</p>
      <ul class="ticks"><li>Office and common-area cleaning</li><li>Washrooms and kitchens</li><li>Floor and window care</li><li>Waste disposal</li><li>Fumigation</li></ul>
      <a class="btn btn-primary" href="contact.html#janitorial">Request janitorial services</a>
    </div>
  </article>
  <article class="svc-detail" id="post-construction">
    <div class="media"><img src="img/post-construction.jpg" alt="Cleaner in overalls washing the windows of a newly finished home" loading="lazy"></div>
    <div class="copy">
      <span class="num">Service 03</span>
      <h2>Post-construction cleaning</h2>
      <p>Building or renovation leaves dust, paint, cement and debris everywhere. We clear it all, so you can move in or hand over the property.</p>
      <ul class="ticks"><li>Debris and rubble removal</li><li>Paint and cement stain removal</li><li>Tiles, glass and fittings cleaned</li><li>A move-in ready finish</li></ul>
      <a class="btn btn-primary" href="contact.html#post-construction">Request post-construction cleaning</a>
    </div>
  </article>
  <article class="svc-detail" id="real-estate">
    <div class="media"><img src="img/real-estate.jpg" alt="Real estate agent holding house keys and a SOLD sign" loading="lazy"></div>
    <div class="copy">
      <span class="num">Service 04</span>
      <h2>Real estate services</h2>
      <p>Property management and practical advice for landlords, owners and first-time buyers in Lagos.</p>
      <ul class="ticks"><li>Property management</li><li>Tenant and estate liaison</li><li>Pre-purchase inspections</li><li>Guidance for home buyers</li></ul>
      <a class="btn btn-primary" href="contact.html#real-estate">Request real estate services</a>
    </div>
  </article>
</div></section>

<section class="block tight" id="audit" style="scroll-margin-top:90px"><div class="wrap">
  <div class="audit-band">
    <div>
      <p class="eyebrow" style="color:#cfe9ee">Free facility audit</p>
      <h2 style="margin-top:10px">Is your property performing at its best?</h2>
      <p>Our experts inspect your property and give you practical recommendations. Find problems before they affect your property, tenants, employees or visitors. Limited slots each month.</p>
      <div class="ctas"><a class="btn btn-light" href="contact.html#audit">Book your free audit</a></div>
    </div>
    <ul><li>Building condition assessment</li><li>Maintenance and repair review</li><li>Cleaning and hygiene assessment</li></ul>
  </div>
</div></section>

<section class="block alt" id="new-home" style="scroll-margin-top:90px"><div class="wrap">
  <div class="split">
    <div class="copy">
      <p class="eyebrow">For new homeowners</p>
      <h2>What to do after buying a house in Lagos</h2>
      <p>Buying a home is a big deal. Before you unpack, there are a few steps you shouldn't skip. A well-maintained home is more comfortable and holds its value better over time.</p>
      <a class="btn btn-primary" href="contact.html#post-construction">Get a move-in quote</a>
    </div>
    <div class="media"><img src="img/keys.jpg" alt="Couple holding the keys to their new home" loading="lazy"></div>
  </div>
  <div class="steps" style="margin-top:48px">
    <div class="step"><h3>Inspect beyond the finishes</h3><p>We check plumbing, wiring, drainage and the roof, not only the paint and tiles.</p></div>
    <div class="step"><h3>Deep clean before move-in</h3><p>A post-construction or deep clean removes dust and debris from every room.</p></div>
    <div class="step"><h3>Fix the small things early</h3><p>Leaks, faulty sockets and blocked drains cost less to fix now than later.</p></div>
    <div class="step"><h3>Plan for long-term costs</h3><p>Set up a maintenance plan so your home keeps its value.</p></div>
  </div>
</div></section>
</main>
{cta_band()}'''

CONTACT = f'''<main>
<section class="page-hero"><div class="wrap">
  <p class="crumbs"><a href="index.html">Home</a> / Contact</p>
  <p class="eyebrow">Contact us</p>
  <h1>Let's talk about your property</h1>
  <p class="lede">Call, send a WhatsApp message, email or visit our office. To book a free facility audit, fill in the form and send it to us on WhatsApp in one tap.</p>
</div></section>

<section class="block" id="audit" style="scroll-margin-top:90px"><div class="wrap contact-grid">
  <div class="contact-cards">
    <dl class="c-card"><span class="ic">{icon("phone")}</span><dt>Phone</dt><dd><span class="val">{PHONE}</span><button class="small-btn" type="button" data-copy="{PHONE_INTL}">Copy</button></dd></dl>
    <dl class="c-card"><span class="ic">{icon("chat")}</span><dt>WhatsApp</dt><dd><span class="val">{WHATSAPP}</span><a class="small-btn" href="{WA_LINK}" target="_blank" rel="noopener">Open chat</a></dd></dl>
    <dl class="c-card"><span class="ic">{icon("mail")}</span><dt>Email</dt><dd><span class="val">{EMAIL}</span><button class="small-btn" type="button" data-copy="{EMAIL}">Copy</button></dd></dl>
    <dl class="c-card"><span class="ic">{icon("pin")}</span><dt>Office</dt><dd><span class="val">{ADDRESS}</span></dd><dd><a class="small-btn" href="{MAP}" target="_blank" rel="noopener">View on Google Maps</a></dd></dl>
    <dl class="c-card"><span class="ic">{icon("ig")}</span><dt>Social media</dt><dd><a class="small-btn" href="{IG}" target="_blank" rel="noopener">Instagram</a><a class="small-btn" href="{FB}" target="_blank" rel="noopener">Facebook</a></dd></dl>
  </div>

  <form class="request" id="requestForm" novalidate>
    <h2>Book a free audit or request a quote</h2>
    <p>We'll reply on WhatsApp or by phone.</p>
    <div class="field"><label for="q-name">Your name</label><input id="q-name" name="name" autocomplete="name" placeholder="Adaeze Okafor"></div>
    <div class="field"><label for="q-phone">Phone or WhatsApp</label><input id="q-phone" name="phone" type="tel" autocomplete="tel" placeholder="0803 000 0000"></div>
    <div class="field"><label for="q-type">Property type</label>
      <select id="q-type" name="type"><option>Residential estate</option><option>Private home</option><option>Office</option><option>Plaza or shopping centre</option><option>School</option><option>Hospital</option><option>Other commercial property</option></select></div>
    <div class="field"><label for="q-area">Location</label><input id="q-area" name="area" placeholder="e.g. Ajah, Lekki Phase 1"></div>
    <div class="field full"><span class="label">What do you need?</span>
      <div class="checks">
        <label><input type="checkbox" id="s-audit" name="svc" value="Free facility audit">Free facility audit</label>
        <label><input type="checkbox" id="s-fm" name="svc" value="Facility management">Facility management</label>
        <label><input type="checkbox" id="s-jan" name="svc" value="Janitorial services">Janitorial services</label>
        <label><input type="checkbox" id="s-pcc" name="svc" value="Post-construction cleaning">Post-construction cleaning</label>
        <label><input type="checkbox" id="s-re" name="svc" value="Real estate services">Real estate services</label>
      </div></div>
    <div class="field full"><label for="q-notes">Tell us about the property</label><textarea id="q-notes" name="notes" placeholder="e.g. 4-bedroom duplex, renovation just finished, need a clean before move-in next week"></textarea></div>
    <p class="err full" id="q-err" hidden></p>
    <div class="field full"><button class="btn btn-primary" type="submit">Prepare my request</button></div>
  </form>
</div></section>
</main>'''

# ---------------------------------------------------------------- careers (from jobs.json)

def esc(s):
    return html.escape(str(s or ""), quote=True)


def apply_link(job, form_url):
    if job.get("apply_url"):
        return job["apply_url"], ' target="_blank" rel="noopener"'
    if form_url:
        sep = "&" if "?" in form_url else "?"
        return f"{form_url}{sep}job={quote(job['title'])}", ' target="_blank" rel="noopener"'
    subject = quote(f"Application: {job['title']}")
    body = quote(f"Hello Quantum Leap,\n\nI would like to apply for the {job['title']} role. "
                 "My CV is attached.\n\nName:\nPhone:\nLocation:\n")
    return f"mailto:{EMAIL}?subject={subject}&body={body}", ""


def job_card(job, form_url, draft=False):
    closing = job.get("closing") or ""
    meta = [job.get("type"), job.get("level"), job.get("location"), job.get("salary")]
    chips = "".join(f"<span>{esc(m)}</span>" for m in meta if m)
    if closing:
        d = date.fromisoformat(closing)
        chips += f'<span>Apply by {d.day} {d.strftime("%B %Y")}</span>'
    resp = "".join(f"<li>{esc(r)}</li>" for r in job.get("responsibilities", []))
    reqs = "".join(f"<li>{esc(r)}</li>" for r in job.get("requirements", []))
    href, target = apply_link(job, form_url)
    via = "Opens the application form" if (job.get("apply_url") or form_url) else f"Opens an email to {EMAIL}. Attach your CV before sending."
    flag = '<span class="draft-flag">Draft: not shown on the live site</span>' if draft else ""
    return f'''<article class="job" data-closes="{esc(closing)}">
  <details>
    <summary>
      <div class="job-head"><h3>{esc(job["title"])}</h3>{flag}<div class="chips">{chips}</div><p>{esc(job.get("summary"))}</p></div>
      <span class="job-toggle" aria-hidden="true"></span>
    </summary>
    <div class="job-body">
      <div class="job-cols">
        <div><h4>What you'll do</h4><ul class="ticks">{resp}</ul></div>
        <div><h4>What we're looking for</h4><ul class="ticks">{reqs}</ul></div>
      </div>
      <div class="job-apply"><a class="btn btn-primary" href="{esc(href)}"{target}>Apply for this role</a><span class="muted">{esc(via)}</span></div>
    </div>
  </details>
</article>'''


def careers_page(show_drafts=False):
    data = json.loads((ROOT / "jobs.json").read_text(encoding="utf-8"))
    form_url = data.get("apply_form_url", "").strip()
    today = date.today().isoformat()
    cards = []
    for job in data.get("jobs", []):
        if job.get("closing") and job["closing"] < today:
            continue
        if job.get("published"):
            cards.append(job_card(job, form_url))
        elif show_drafts:
            cards.append(job_card(job, form_url, draft=True))
    general_subject = quote("General application")
    empty = f'''<div class="no-jobs"{" hidden" if cards else ""}>
    <h3>No open positions right now</h3>
    <p>We're not hiring for a specific role at the moment, but we're always glad to hear from good people. Send us your CV and we'll keep it on file.</p>
  </div>'''
    return f'''<main>
<section class="page-hero"><div class="wrap">
  <p class="crumbs"><a href="index.html">Home</a> / Careers</p>
  <p class="eyebrow">Careers</p>
  <h1>Build your career with Quantum Leap</h1>
  <p class="lede">We look after homes, estates, offices and commercial properties across Lagos. If you take pride in good work, we'd like to hear from you.</p>
</div></section>

<section class="block" id="openings" style="scroll-margin-top:90px"><div class="wrap">
  <div class="sec-head">
    <div><p class="eyebrow">Open positions</p><h2>Current vacancies</h2></div>
    <p>Click a role to see the full details. Applications close at the end of the date shown.</p>
  </div>
  <div class="jobs">
  {"".join(cards)}
  {empty}
  </div>
</div></section>

<section class="block alt"><div class="wrap">
  <div class="sec-head">
    <div><p class="eyebrow">How to apply</p><h2>What happens after you apply</h2></div>
    <p>We read every application. If your experience matches the role, we'll contact you by phone or email.</p>
  </div>
  <div class="steps">
    <div class="step"><h3>Send your application</h3><p>Click "Apply for this role" and send your CV along with your name and phone number.</p></div>
    <div class="step"><h3>We review it</h3><p>Our team checks your experience against what the role needs.</p></div>
    <div class="step"><h3>Interview</h3><p>Shortlisted applicants are invited to an interview at our office in Ikota or by phone.</p></div>
    <div class="step"><h3>Offer</h3><p>Successful applicants receive an offer and start with an introduction to our sites and team.</p></div>
  </div>
</div></section>

<section class="block"><div class="wrap split">
  <div class="copy">
    <p class="eyebrow">Don't see the right role?</p>
    <h2>Send us your CV anyway</h2>
    <p>We regularly need cleaners, supervisors, technicians and facility officers. Email your CV with the subject "General application" and tell us the kind of work you're looking for.</p>
    <div class="ctas" style="margin-top:6px"><a class="btn btn-primary" href="mailto:{EMAIL}?subject={general_subject}">Email your CV</a></div>
    <p class="muted" style="font-size:.9rem">Or send it to <b>{EMAIL}</b></p>
  </div>
  <div class="media"><img src="img/janitorial.jpg" alt="Cleaning crew in red overalls at work in a modern apartment" loading="lazy"></div>
</div></section>

<section class="block tight"><div class="wrap">
  <p class="privacy-note">We use the details and CV you send only to assess your application and contact you about roles at Quantum Leap. We don't share them with anyone else. To have your details deleted, email {EMAIL}.</p>
</div></section>
</main>'''


PAGES = {
    "index.html": ("Quantum Leap Management Services", "home", HOME),
    "about.html": ("About Us | Quantum Leap Management Services", "about", ABOUT),
    "services.html": ("Services | Quantum Leap Management Services", "services", SERVICES),
    "careers.html": ("Careers | Quantum Leap Management Services", "careers", careers_page(SHOW_DRAFTS)),
    "contact.html": ("Contact | Quantum Leap Management Services", "contact", CONTACT),
}

DESC = "Quantum Leap Management Services Ltd: facility management, janitorial services, post-construction cleaning and real estate services in Lagos, Nigeria. Since 2012."

for fname, (title, key, body) in PAGES.items():
    inner = f"{header(key)}\n{body}\n{FOOTER}\n"
    full = (f'<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            f'<title>{title}</title>\n<meta name="description" content="{DESC}">\n{FONTS}\n</head>\n<body>\n{inner}</body>\n</html>\n')
    (OUT / fname).write_text(full, encoding="utf-8")
    if key == "home":
        (Path(__file__).parent / "_preview-home.html").write_text(f"<title>{title}</title>\n{FONTS}\n{inner}", encoding="utf-8")

print("Built:", ", ".join(PAGES))
