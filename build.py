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
         '<link rel="stylesheet" href="styles.css">\n'
         '<link rel="icon" type="image/png" sizes="32x32" href="img/favicon-32.png">\n'
         '<link rel="apple-touch-icon" href="img/apple-touch-icon.png">')

PHONE = "0802 303 2178"
PHONE_INTL = "+2348023032178"
WHATSAPP = "0802 303 2178"
WA_LINK = "https://wa.me/2348023032178"
EMAIL = "Quantumleapm@yahoo.com"
ADDRESS = "Suite 23, Double Crown Plaza, Ogombo Road, off Lekki-Epe Expressway, Ajah, Lagos"
IG = "https://www.instagram.com/quantum.leap.management/"
FB = "https://www.facebook.com/quantumleapmgtservices/"
MAP = "https://www.google.com/maps/search/?api=1&query=Double+Crown+Plaza+Ogombo+Road+Ajah+Lagos"

BROCHURE = "downloads/Quantum-Leap-Brochure-2026.pdf"
_b = Path(__file__).parent / "site" / BROCHURE
BROCHURE_SIZE = f"PDF, {_b.stat().st_size / 1_048_576:.1f} MB" if _b.exists() else "PDF"


# Properties come from projects.json (shown on Home, About and the Projects page)
def load_projects():
    import json as _json
    data = _json.loads((Path(__file__).parent / "projects.json").read_text(encoding="utf-8"))
    return [p for p in data.get("projects", []) if p.get("published")]


def properties_list():
    return "".join(f'<li><b>{p["name"]}</b><span>{p["location"]}</span></li>' for p in load_projects())


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
        "download": '<path d="M12 3v12M7 10l5 5 5-5M4 19h16"/>',
    }
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths[name]}</svg>')


LOGO = '<img class="logo-mark" src="img/logo.png" width="40" height="40" alt="">'

NAV = [("index.html", "Home", "home"), ("about.html", "About us", "about"),
       ("services.html", "Services", "services"), ("projects.html", "Projects", "projects"),
       ("careers.html", "Careers", "careers"),
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
  <a class="brand" href="index.html" aria-label="Quantum Leap Management Services, home">{LOGO}<span><b>Quantum Leap</b><small>Management Services Ltd</small></span></a>
  <button class="menu-btn" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="mainnav">{icon("menu")}</button>
  <nav class="main" id="mainnav" aria-label="Main">{links}<a class="btn btn-primary" href="contact.html#audit">Book a free audit</a></nav>
  <a class="btn btn-primary cta" href="contact.html#audit">Book a free audit</a>
</div></header>'''


FOOTER = f'''<footer class="site">
  <div class="wrap cols">
    <div class="about-f">
      <a class="brand" href="index.html">{LOGO}<span><b>Quantum Leap</b><small>Management Services Ltd</small></span></a>
      <p>Trusted facility managers since 2012. Supporting your critical infrastructure needs.</p>
      <div class="social"><a href="{IG}" target="_blank" rel="noopener" aria-label="Instagram">{icon("ig", 18)}</a><a href="{FB}" target="_blank" rel="noopener" aria-label="Facebook">{icon("fb", 18)}</a></div>
    </div>
    <div><h3>Company</h3><ul><li><a href="index.html">Home</a></li><li><a href="about.html">About us</a></li><li><a href="services.html">Services</a></li><li><a href="projects.html">Projects</a></li><li><a href="careers.html">Careers</a></li><li><a href="contact.html">Contact</a></li><li><a href="{BROCHURE}" download>Download our brochure ({BROCHURE_SIZE})</a></li></ul></div>
    <div><h3>Services</h3><ul><li><a href="facility-management.html">Facility management</a></li><li><a href="janitorial-services.html">Janitorial services</a></li><li><a href="post-construction-cleaning.html">Post-construction cleaning</a></li><li><a href="real-estate-services.html">Real estate services</a></li><li><a href="services.html#audit">Free facility audit</a></li></ul></div>
    <div><h3>Get in touch</h3><ul><li>{ADDRESS}</li><li>Phone and WhatsApp: {PHONE}</li><li>{EMAIL}</li></ul></div>
  </div>
  <div class="bottom"><div class="wrap"><span>© <span id="year">2026</span> Quantum Leap Management Services Ltd. All rights reserved.</span><span>Ajah, Lagos, Nigeria</span></div></div>
</footer>
<script src="site.js"></script>'''


def cta_band():
    return f'''<section class="cta-band"><div class="wrap">
  <div><h2>Ready to give your property the care it deserves?</h2><p>Book a free facility audit, or send us a message and we'll get back to you.</p></div>
  <div class="ctas"><a class="btn btn-light" href="contact.html#audit">Book a free audit</a><a class="btn btn-outline-light" href="{WA_LINK}" target="_blank" rel="noopener">Chat on WhatsApp</a></div>
</div></section>'''


# Six reasons from the company profile ("Why Choose Us")
WHY_US = f'''<div class="why six">
    <div class="reason"><span class="ic">{icon("bolt")}</span><h3>Operational efficiency</h3><p>Our service plans are designed to make your property run more efficiently.</p></div>
    <div class="reason"><span class="ic">{icon("process")}</span><h3>Tailored solutions</h3><p>Every client gets a service plan built around their property's needs.</p></div>
    <div class="reason"><span class="ic">{icon("people")}</span><h3>Experienced team</h3><p>Skilled professionals committed to quality service.</p></div>
    <div class="reason"><span class="ic">{icon("phone")}</span><h3>Prompt response</h3><p>Fast response to maintenance requests and emergencies.</p></div>
    <div class="reason"><span class="ic">{icon("shield")}</span><h3>Quality assurance</h3><p>Routine inspections and facility audits keep standards consistently high.</p></div>
    <div class="reason"><span class="ic">{icon("chat")}</span><h3>Transparent communication</h3><p>Regular reports and clear, honest communication with every client.</p></div>
  </div>'''

# Six steps from the company profile ("Our Process")
PROCESS = '''<div class="steps six">
    <div class="step"><h3>Facility inspection and needs assessment</h3><p>We visit your property to understand how it runs and what it needs.</p></div>
    <div class="step"><h3>Facility audit report</h3><p>You receive a written report of what we found and what needs attention.</p></div>
    <div class="step"><h3>Customised service proposal</h3><p>We propose a service plan and scope designed for your property.</p></div>
    <div class="step"><h3>Service implementation</h3><p>Our team and trusted vendors start work as agreed.</p></div>
    <div class="step"><h3>Routine monitoring and reporting</h3><p>Regular inspections and reports keep you informed.</p></div>
    <div class="step"><h3>Continuous improvement and support</h3><p>We review performance and adjust the plan as your needs change.</p></div>
  </div>'''


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
    <a class="svc-card" href="facility-management.html"><img src="img/facility.jpg" alt="Residential high-rise in Lagos" loading="lazy"><div class="body"><h3>Facility management</h3><p>Keeping buildings running efficiently, safely and cost-effectively over the long run.</p><span class="more arrow">Learn more </span></div></a>
    <a class="svc-card" href="janitorial-services.html"><img src="img/janitorial.jpg" alt="Cleaning crew mopping, wiping and washing windows in a modern kitchen" loading="lazy"><div class="body"><h3>Janitorial services</h3><p>Clean, hygienic and presentable spaces for daily use, with light and deep cleaning plans.</p><span class="more arrow">Learn more </span></div></a>
    <a class="svc-card" href="post-construction-cleaning.html"><img src="img/post-construction.jpg" alt="Cleaner in overalls washing the windows of a newly finished home" loading="lazy"><div class="body"><h3>Post-construction cleaning</h3><p>Preparing newly built or renovated properties for handover, occupation or sale.</p><span class="more arrow">Learn more </span></div></a>
    <a class="svc-card" href="real-estate-services.html"><img src="img/real-estate.jpg" alt="Real estate agent holding house keys and a SOLD sign" loading="lazy"><div class="body"><h3>Real estate services</h3><p>Property sourcing, leasing and basic property management for owners and clients.</p><span class="more arrow">Learn more </span></div></a>
  </div>
</div></section>

<section class="block alt"><div class="wrap split">
  <div class="media"><img src="img/team.jpg" alt="Team meeting in an office in Lagos" loading="lazy"></div>
  <div class="copy">
    <p class="eyebrow">About Quantum Leap</p>
    <h2>Helping clients manage, maintain, improve and transform their properties</h2>
    <p>We are an integrated facility management, real estate and property solutions company. We protect property value, improve how buildings run, and make them better places for the people who use them.</p>
    <p>Our strength is offering several related services under one trusted brand, so you work with a single partner instead of multiple vendors.</p>
    <ul class="ticks"><li>One partner instead of multiple vendors</li><li>A service plan tailored to your property</li><li>Regular reports and clear communication</li></ul>
    <a class="btn btn-primary arrow" href="about.html">More about us </a>
  </div>
</div></section>

<section class="block"><div class="wrap">
  <div class="sec-head">
    <div><p class="eyebrow">Why choose us</p><h2>Why property owners trust Quantum Leap</h2></div>
    <p>Trust and facility management go hand in hand. This is what you get when you work with us.</p>
  </div>
  {WHY_US}
</div></section>

<section class="block alt"><div class="wrap split">
  <div class="media"><img src="img/double-crown-plaza.jpg" alt="Double Crown Plaza on Ogombo Road, Ajah" loading="lazy"></div>
  <div class="copy">
    <p class="eyebrow">Our experience</p>
    <h2>Properties we've managed</h2>
    <p>We have worked with estates and commercial properties across Lekki, Ajah and Eti-Osa, including:</p>
    <ul class="props">{properties_list()}</ul>
    <a class="btn btn-primary arrow" href="projects.html">See our projects </a>
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
  <p class="lede">An integrated facility management, real estate and property solutions company helping businesses, developers, institutions and property owners keep their properties running smoothly.</p>
</div></section>

<section class="block"><div class="wrap split">
  <div class="copy">
    <p class="eyebrow">Who we are</p>
    <h2>One trusted partner for the care of your property</h2>
    <p>Quantum Leap Management Services Ltd provides a full range of facility management services that protect property value, improve operational efficiency, and make buildings better for the people who use them, through proactive maintenance and excellent service.</p>
    <p>Our strength is offering several related services under one trusted brand, so clients work with a single partner instead of multiple vendors. From light building cleaning to strategic property management, we leave your environment clean, safe and productive.</p>
    <p>Whether it's a residential estate, commercial building, school, healthcare facility or corporate office, we tailor our solutions to each client's needs.</p>
    <div class="facts">
      <div class="fact"><b>2012</b><span>Year we started</span></div>
      <div class="fact"><b>4</b><span>Core services under one roof</span></div>
      <div class="fact"><b>Ajah</b><span>Office on Ogombo Road, Lagos</span></div>
    </div>
  </div>
  <div class="media"><img src="img/about-house.jpg" alt="Newly built house in Abuja" loading="lazy"></div>
</div></section>

<section class="block alt"><div class="wrap">
  <div class="sec-head">
    <div><p class="eyebrow">What drives us</p><h2>Our vision, mission and philosophy</h2></div>
    <p>Supporting your critical infrastructure needs.</p>
  </div>
  <div class="why three">
    <div class="reason"><span class="ic">{icon("medal")}</span><h3>Our vision</h3><p>To redefine property care by making proactive, high-quality asset preservation the standard for every property owner.</p></div>
    <div class="reason"><span class="ic">{icon("process")}</span><h3>Our mission</h3><p>To deliver seamless facility management that safeguards your assets, drives operational efficiency, and frees you to focus on what you do best.</p></div>
    <div class="reason"><span class="ic">{icon("shield")}</span><h3>Our philosophy</h3><p>Exceptional service equals property value. We don't just maintain your building; we actively safeguard your investment so its market value is retained and enhanced over time.</p></div>
  </div>
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

<section class="block"><div class="wrap split flip">
  <div class="media"><img src="img/engineer.jpg" alt="Engineer in a hard hat at an electrical substation in Nigeria" loading="lazy"></div>
  <div class="copy">
    <p class="eyebrow">Our service delivery team</p>
    <h2>A flexible team that scales with your property</h2>
    <p>We combine management oversight, facility operations, technical support and trained service staff, and deploy the right people for the size, complexity and needs of each property.</p>
    <dl class="team-units">
      <div><dt>Management and client relations</dt><dd>Strategic oversight, client communication and performance management.</dd></div>
      <div><dt>Facility operations</dt><dd>Day-to-day facility supervision, inspections and service coordination.</dd></div>
      <div><dt>Technical support</dt><dd>Building systems, preventive maintenance and corrective maintenance coordination.</dd></div>
      <div><dt>Soft services team</dt><dd>Cleaning, landscaping, waste management and other property services.</dd></div>
    </dl>
  </div>
</div></section>

<section class="block tight"><div class="wrap">
  <div class="brochure-band">
    <span class="ic">{icon("download", 26)}</span>
    <div><h2>Download our company brochure</h2><p>Our services, vision and mission, and the properties we've managed, in one document you can save or share.</p></div>
    <a class="btn btn-primary" href="{BROCHURE}" download>Download brochure <span class="btn-note">{BROCHURE_SIZE}</span></a>
  </div>
</div></section>

<section class="block alt" id="experience" style="scroll-margin-top:90px"><div class="wrap split">
  <div class="copy">
    <p class="eyebrow">Our experience</p>
    <h2>Properties we've managed</h2>
    <p>Over the past few years we have worked with these estates and properties:</p>
    <ul class="props">{properties_list()}</ul>
    <a class="btn btn-primary arrow" href="projects.html">See our projects </a>
  </div>
  <div class="media"><img src="img/double-crown-plaza.jpg" alt="Double Crown Plaza on Ogombo Road, Ajah" loading="lazy"></div>
</div></section>

<section class="block"><div class="wrap">
  <div class="sec-head">
    <div><p class="eyebrow">Who we work with</p><h2>Clients and properties we serve</h2></div>
    <p>We work with businesses, developers, institutions and property owners.</p>
  </div>
  <div class="chips"><span>Residential estates</span><span>Commercial buildings</span><span>Corporate offices</span><span>Plazas and shopping centres</span><span>Educational institutions</span><span>Healthcare facilities</span><span>Mixed-use developments</span><span>Private homes</span></div>
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
      <p>We make sure buildings and facilities run efficiently, safely and cost-effectively over the long run. Our facility management covers everything involved in keeping a property well maintained, on terms agreed with the property owner.</p>
      <ul class="ticks"><li>Day-to-day facility operations coordination</li><li>Preventive and corrective maintenance oversight</li><li>Asset management and maintenance scheduling</li><li>Vendor and artisan coordination (cleaners, security, electrical, plumbing, HVAC and more)</li><li>Routine facility inspections and reporting</li><li>Energy management</li><li>Security and access control</li><li>A clean and well-kept environment</li><li>Client reporting and performance tracking</li></ul>
      <div class="ctas" style="margin-top:4px"><a class="btn btn-primary" href="contact.html#facility">Request facility management</a><a class="btn btn-ghost arrow" href="facility-management.html">Full details </a></div>
    </div>
  </article>
  <article class="svc-detail" id="janitorial">
    <div class="media"><img src="img/janitorial.jpg" alt="Cleaning crew mopping, wiping and washing windows in a modern kitchen" loading="lazy"></div>
    <div class="copy">
      <span class="num">Service 02</span>
      <h2>Janitorial services</h2>
      <p>We keep spaces clean, hygienic and presentable for daily use. We offer both light and deep cleaning plans, depending on what your property needs.</p>
      <ul class="ticks"><li>Daily, weekly and periodic cleaning</li><li>Office cleaning</li><li>Residential and estate cleaning</li><li>Restroom and common-area sanitation</li><li>Waste management and disposal coordination</li><li>Cleaning staff supervision and quality checks</li></ul>
      <div class="ctas" style="margin-top:4px"><a class="btn btn-primary" href="contact.html#janitorial">Request janitorial services</a><a class="btn btn-ghost arrow" href="janitorial-services.html">Full details </a></div>
    </div>
  </article>
  <article class="svc-detail" id="post-construction">
    <div class="media"><img src="img/post-construction.jpg" alt="Cleaner in overalls washing the windows of a newly finished home" loading="lazy"></div>
    <div class="copy">
      <span class="num">Service 03</span>
      <h2>Post-construction cleaning</h2>
      <p>We prepare newly built or renovated properties for handover, occupation or sale, clearing the dust and debris that construction leaves behind.</p>
      <ul class="ticks"><li>Removal of construction debris and dust</li><li>Deep cleaning of floors, walls, fittings and surfaces</li><li>Window, glass and façade cleaning</li><li>Final detailing and finishing cleans</li><li>Handover-ready cleaning for inspections and client use</li></ul>
      <div class="ctas" style="margin-top:4px"><a class="btn btn-primary" href="contact.html#post-construction">Request post-construction cleaning</a><a class="btn btn-ghost arrow" href="post-construction-cleaning.html">Full details </a></div>
    </div>
  </article>
  <article class="svc-detail" id="real-estate">
    <div class="media"><img src="img/real-estate.jpg" alt="Real estate agent holding house keys and a SOLD sign" loading="lazy"></div>
    <div class="copy">
      <span class="num">Service 04</span>
      <h2>Real estate services</h2>
      <p>We support property owners and clients with property sourcing, leasing and basic property management.</p>
      <ul class="ticks"><li>Property sourcing and listing</li><li>Property inspections and evaluations</li><li>Leasing and tenant coordination</li><li>Support for sales and lettings</li><li>Property handover and documentation support</li></ul>
      <div class="ctas" style="margin-top:4px"><a class="btn btn-primary" href="contact.html#real-estate">Request real estate services</a><a class="btn btn-ghost arrow" href="real-estate-services.html">Full details </a></div>
    </div>
  </article>
</div></section>

<section class="block alt" id="process" style="scroll-margin-top:90px"><div class="wrap">
  <div class="sec-head">
    <div><p class="eyebrow">How we work</p><h2>Our process</h2></div>
    <p>Every engagement follows the same six steps, from the first inspection to ongoing support.</p>
  </div>
  {PROCESS}
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
    <dl class="c-card"><span class="ic">{icon("download")}</span><dt>Company brochure</dt><dd><a class="small-btn" href="{BROCHURE}" download>Download brochure</a></dd><dd class="note">{BROCHURE_SIZE}</dd></dl>
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
    <div class="step"><h3>Send your application</h3><p>Click "Apply for this role" and send your CV along with your details.</p></div>
    <div class="step"><h3>We review it</h3><p>Our team checks your experience against what the role needs.</p></div>
    <div class="step"><h3>Interview</h3><p>Shortlisted applicants are invited to an interview at our office in Ajah or by phone.</p></div>
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


# ---------------------------------------------------------------- one page per service
# "included" lists come from the company profile; the rest is written for the website.

SERVICE_PAGES = [
    {
        "file": "facility-management.html", "anchor": "facility", "contact": "facility",
        "name": "Facility management", "img": "facility.jpg", "alt": "Residential high-rise in Lagos",
        "title": "Facility Management in Lagos | Quantum Leap Management Services",
        "desc": "Facility management for estates, offices and commercial buildings in Lagos: maintenance, vendor coordination, inspections, security and reporting. Book a free facility audit.",
        "headline": "Facility management that keeps your property running",
        "lede": "We make sure buildings and facilities run efficiently, safely and cost-effectively over the long run.",
        "intro": [
            "Our facility management covers everything involved in keeping a property well maintained, on terms agreed with the property owner.",
            "Instead of juggling separate cleaners, security, electricians, plumbers and HVAC technicians, you deal with one team. We plan the maintenance, coordinate the vendors, inspect the work and report back to you regularly.",
        ],
        "included": [
            "Day-to-day facility operations coordination",
            "Preventive and corrective maintenance oversight",
            "Asset management and maintenance scheduling",
            "Vendor and artisan coordination (cleaners, security, electrical, plumbing, HVAC and more)",
            "Routine facility inspections and reporting",
            "Energy management",
            "Security and access control",
            "A clean and well-kept environment",
            "Client reporting and performance tracking",
        ],
        "for": ["Residential estates", "Commercial buildings", "Corporate offices", "Plazas and shopping centres",
                "Educational institutions", "Healthcare facilities", "Mixed-use developments"],
        "faq": [
            ("What does a facility manager actually do?",
             "We run the day-to-day upkeep of your property for you: scheduling maintenance, coordinating artisans and vendors, inspecting the property and reporting to you, so problems are caught early and handled properly."),
            ("Can you take over from our current vendors?",
             "Yes. We can coordinate the cleaners, security, electricians, plumbers and other vendors you already use, or bring in our own, so you have one point of contact."),
            ("How will I know what's happening at my property?",
             "We carry out routine inspections and send you regular reports on the work done and any issues that need your decision."),
            ("How do we get started?",
             "Book a free facility audit. We inspect your property, give you a report of what we find, and then propose a service plan for your property."),
        ],
    },
    {
        "file": "janitorial-services.html", "anchor": "janitorial", "contact": "janitorial",
        "name": "Janitorial services", "img": "janitorial.jpg", "alt": "Cleaning crew mopping, wiping and washing windows in a modern kitchen",
        "title": "Janitorial and Cleaning Services in Lagos | Quantum Leap Management Services",
        "desc": "Office, residential and estate cleaning in Lagos. Daily, weekly and periodic cleaning, restroom and common-area sanitation, and supervised cleaning staff.",
        "headline": "Clean, hygienic spaces, every day",
        "lede": "We keep offices, homes and estates clean, hygienic and presentable for daily use.",
        "intro": [
            "We offer both light and deep cleaning plans, depending on what your property needs, on a daily, weekly or periodic schedule.",
            "Our cleaning staff are supervised, and their work is checked regularly, so the standard stays high long after the first visit.",
        ],
        "included": [
            "Daily, weekly and periodic cleaning",
            "Office cleaning",
            "Residential and estate cleaning",
            "Restroom and common-area sanitation",
            "Waste management and disposal coordination",
            "Cleaning staff supervision and quality checks",
        ],
        "for": ["Offices", "Residential estates", "Apartment blocks and common areas", "Plazas and shopping centres",
                "Schools", "Healthcare facilities", "Private homes"],
        "faq": [
            ("Do you offer both light and deep cleaning?",
             "Yes. We have light cleaning plans for routine upkeep and deep cleaning plans for a thorough clean, depending on your property's needs."),
            ("How often can you clean?",
             "We clean daily, weekly or periodically. We'll recommend a schedule based on how your space is used."),
            ("Who supervises the cleaners?",
             "Our team supervises the cleaning staff and carries out regular quality checks."),
            ("Can you handle waste disposal too?",
             "Yes. We coordinate waste management and disposal as part of the service."),
        ],
    },
    {
        "file": "post-construction-cleaning.html", "anchor": "post-construction", "contact": "post-construction",
        "name": "Post-construction cleaning", "img": "post-construction.jpg", "alt": "Cleaner in overalls washing the windows of a newly finished home",
        "title": "Post-Construction Cleaning in Lagos | Quantum Leap Management Services",
        "desc": "Post-construction and after-renovation cleaning in Lagos. Debris and dust removal, deep cleaning, window and facade cleaning, and handover-ready finishing.",
        "headline": "Handover-ready after building or renovation",
        "lede": "We prepare newly built or renovated properties for handover, occupation or sale.",
        "intro": [
            "Building work leaves dust, debris, paint and cement on every surface. We clear it all and finish the property to a standard that's ready for inspection, for new occupants or for buyers.",
            "We work with developers, contractors, landlords and homeowners, from single homes to full developments.",
        ],
        "included": [
            "Removal of construction debris and dust",
            "Deep cleaning of floors, walls, fittings and surfaces",
            "Window, glass and façade cleaning",
            "Final detailing and finishing cleans",
            "Handover-ready cleaning for inspections and client use",
        ],
        "for": ["Property developers", "Building contractors", "Homeowners after renovation",
                "Landlords preparing for new tenants", "Properties being prepared for sale"],
        "faq": [
            ("When should I book a post-construction clean?",
             "Once the building or renovation work is finished and before the handover, inspection or move-in date. Booking early helps us plan around your deadline."),
            ("What does a post-construction clean include?",
             "Removing construction debris and dust, deep cleaning floors, walls, fittings and surfaces, cleaning windows, glass and the façade, and a final detailing clean."),
            ("Do you clean for inspections and handovers?",
             "Yes. We finish properties to a handover-ready standard for inspections and client use."),
            ("I've just bought a newly built home. Can you help?",
             "Yes. A post-construction clean before you move in removes the dust and debris builders leave behind."),
        ],
    },
    {
        "file": "real-estate-services.html", "anchor": "real-estate", "contact": "real-estate",
        "name": "Real estate services", "img": "real-estate.jpg", "alt": "Real estate agent holding house keys and a SOLD sign",
        "title": "Real Estate Services in Lagos | Quantum Leap Management Services",
        "desc": "Property sourcing and listing, inspections, leasing and tenant coordination, sales and lettings support, and handover documentation in Lagos.",
        "headline": "Support for buying, letting and managing property",
        "lede": "We support property owners and clients with property sourcing, leasing and basic property management.",
        "intro": [
            "Whether you're looking for a property, letting one out or handing one over, we help with the practical work: finding and listing properties, inspecting them, coordinating tenants and handling the paperwork at handover.",
            "Because we also manage and maintain properties, we know what to look for beyond the finishes.",
        ],
        "included": [
            "Property sourcing and listing",
            "Property inspections and evaluations",
            "Leasing and tenant coordination",
            "Support for sales and lettings",
            "Property handover and documentation support",
        ],
        "for": ["Property owners and landlords", "Buyers looking for a property", "Tenants looking to rent",
                "Developers selling or letting units", "Estate associations"],
        "faq": [
            ("Can you help me find a property?",
             "Yes. We source properties that match what you're looking for and arrange inspections."),
            ("Can you inspect a property before I buy or rent it?",
             "Yes. We carry out property inspections and evaluations so you know its condition before you commit."),
            ("Do you manage tenants for landlords?",
             "We handle leasing and tenant coordination, and can combine this with our facility management for the property itself."),
            ("Do you help with handover paperwork?",
             "Yes. We support property handovers and the documentation that goes with them."),
        ],
    },
]


def service_page(s):
    intro = "".join(f"<p>{p}</p>" for p in s["intro"])
    inc = "".join(f"<li>{i}</li>" for i in s["included"])
    who = "".join(f"<span>{w}</span>" for w in s["for"])
    faq = "".join(f'<details class="faq-item"><summary>{q}</summary><p>{a}</p></details>' for q, a in s["faq"])
    others = "".join(
        f'<a class="svc-card" href="{o["file"]}"><img src="img/{o["img"]}" alt="{o["alt"]}" loading="lazy">'
        f'<div class="body"><h3>{o["name"]}</h3><p>{o["lede"]}</p><span class="more arrow">Learn more </span></div></a>'
        for o in SERVICE_PAGES if o is not s)
    return f'''<main>
<section class="page-hero"><div class="wrap">
  <p class="crumbs"><a href="index.html">Home</a> / <a href="services.html">Services</a> / {s["name"]}</p>
  <p class="eyebrow">{s["name"]}</p>
  <h1>{s["headline"]}</h1>
  <p class="lede">{s["lede"]}</p>
  <div class="ctas"><a class="btn btn-light" href="contact.html#{s["contact"]}">Request this service</a><a class="btn btn-outline-light" href="{WA_LINK}" target="_blank" rel="noopener">Chat on WhatsApp</a></div>
</div></section>

<section class="block"><div class="wrap split">
  <div class="copy">
    <p class="eyebrow">Overview</p>
    <h2>{s["lede"]}</h2>
    {intro}
  </div>
  <div class="media"><img src="img/{s["img"]}" alt="{s["alt"]}"></div>
</div></section>

<section class="block alt"><div class="wrap">
  <div class="sec-head">
    <div><p class="eyebrow">What's included</p><h2>Our {s["name"].lower()} service covers</h2></div>
    <p>Choose the full service or the parts you need. We'll agree the scope with you before we start.</p>
  </div>
  <ul class="ticks included">{inc}</ul>
</div></section>

<section class="block"><div class="wrap">
  <div class="sec-head">
    <div><p class="eyebrow">Who it's for</p><h2>Properties and clients we serve</h2></div>
    <p>Whatever the size of your property, we tailor the service plan to it.</p>
  </div>
  <div class="chips">{who}</div>
</div></section>

<section class="block alt"><div class="wrap">
  <div class="sec-head">
    <div><p class="eyebrow">How we work</p><h2>Our process</h2></div>
    <p>From the first inspection to ongoing support, every engagement follows the same six steps.</p>
  </div>
  {PROCESS}
</div></section>

<section class="block"><div class="wrap faq-wrap">
  <div><p class="eyebrow">Questions</p><h2>Frequently asked questions</h2><p class="muted" style="margin-top:12px">Can't find your answer? Call or WhatsApp us on {PHONE}.</p></div>
  <div class="faq">{faq}</div>
</div></section>

<section class="block tight"><div class="wrap">
  <div class="sec-head"><div><p class="eyebrow">More from Quantum Leap</p><h2>Our other services</h2></div><p>Combine services and work with one partner instead of several vendors.</p></div>
  <div class="svc-grid three">{others}</div>
</div></section>
</main>
{cta_band()}'''


# ---------------------------------------------------------------- projects (from projects.json)

def project_card(p):
    q = quote(f'{p["name"]}, {p["location"]}')
    if p.get("image"):
        media = f'<img src="img/{esc(p["image"])}" alt="{esc(p["name"])}, {esc(p["location"])}" loading="lazy">'
    else:
        media = f'<div class="proj-placeholder" aria-hidden="true">{icon("building", 40)}<span>{esc(p["name"])}</span></div>'
    tags = "".join(f"<span>{esc(s)}</span>" for s in p.get("services", []))
    return f'''<article class="project">
  <div class="proj-media">{media}</div>
  <div class="proj-body">
    {f'<p class="eyebrow">{esc(p["type"])}</p>' if p.get("type") else ""}
    <h3>{esc(p["name"])}</h3>
    <p class="proj-loc">{icon("pin", 18)}<span>{esc(p["location"])}</span></p>
    {f'<p>{esc(p["summary"])}</p>' if p.get("summary") else ""}
    {f'<div class="chips">{tags}</div>' if tags else ""}
    <a class="small-btn" href="https://www.google.com/maps/search/?api=1&amp;query={q}" target="_blank" rel="noopener">View on map</a>
  </div>
</article>'''


def projects_page():
    cards = "".join(project_card(p) for p in load_projects())
    return f'''<main>
<section class="page-hero"><div class="wrap">
  <p class="crumbs"><a href="index.html">Home</a> / Projects</p>
  <p class="eyebrow">Our projects</p>
  <h1>Properties we've managed</h1>
  <p class="lede">Over the past few years we have looked after estates and commercial properties across Lekki, Ajah and Eti-Osa in Lagos.</p>
</div></section>

<section class="block"><div class="wrap">
  <div class="projects">{cards}</div>
</div></section>

<section class="block alt"><div class="wrap">
  <div class="sec-head">
    <div><p class="eyebrow">What we do for every property</p><h2>One partner for the whole property</h2></div>
    <p>We bring several related services under one trusted brand, so property owners and estate associations work with one team instead of many vendors.</p>
  </div>
  <div class="svc-grid">
    {"".join(f'<a class="svc-card" href="{s["file"]}"><img src="img/{s["img"]}" alt="{s["alt"]}" loading="lazy"><div class="body"><h3>{s["name"]}</h3><p>{s["lede"]}</p><span class="more arrow">Learn more </span></div></a>' for s in SERVICE_PAGES)}
  </div>
</div></section>

<section class="block tight" style="padding-top:88px"><div class="wrap">
  <div class="audit-band">
    <div>
      <p class="eyebrow" style="color:#cfe9ee">Your property could be next</p>
      <h2 style="margin-top:10px">Start with a free facility audit</h2>
      <p>We inspect your property, give you a report of what we find, and propose a service plan built around it.</p>
      <div class="ctas"><a class="btn btn-light" href="contact.html#audit">Book your free audit</a></div>
    </div>
    <ul><li>Building condition assessment</li><li>Maintenance and repair review</li><li>Cleaning and hygiene assessment</li></ul>
  </div>
</div></section>
</main>
{cta_band()}'''


PAGES = {
    "index.html": ("Quantum Leap Management Services | Facility Management in Lagos", "home", HOME,
                   "Facility management, janitorial services, post-construction cleaning and real estate services for estates, offices and homes in Lagos. Book a free facility audit."),
    "about.html": ("About Us | Quantum Leap Management Services", "about", ABOUT,
                   "Quantum Leap Management Services is an integrated facility management, real estate and property solutions company based in Ajah, Lagos. Our vision, mission, team and experience."),
    "services.html": ("Our Services | Quantum Leap Management Services", "services", SERVICES,
                      "Facility management, janitorial services, post-construction cleaning and real estate services in Lagos, from one trusted partner. See what each service includes."),
    **{s["file"]: (s["title"], "services", service_page(s), s["desc"]) for s in SERVICE_PAGES},
    "projects.html": ("Projects | Quantum Leap Management Services", "projects", projects_page(),
                      "Estates and commercial properties managed by Quantum Leap Management Services in Lekki, Ajah and Eti-Osa, Lagos."),
    "careers.html": ("Careers | Quantum Leap Management Services", "careers", careers_page(SHOW_DRAFTS),
                     "Job vacancies at Quantum Leap Management Services in Lagos. See open roles in facility management and operations, and apply online."),
    "contact.html": ("Contact Us | Quantum Leap Management Services", "contact", CONTACT,
                     "Contact Quantum Leap Management Services: call or WhatsApp 0802 303 2178, email Quantumleapm@yahoo.com, or visit Suite 23, Double Crown Plaza, Ogombo Road, Ajah, Lagos."),
}

DESC = "Quantum Leap Management Services Ltd: facility management, janitorial services, post-construction cleaning and real estate services in Lagos, Nigeria. Since 2012."

# ---------------------------------------------------------------- search engines and link previews

# Change this when the site moves to its own domain (e.g. "https://quantumleapmgt.com.ng").
SITE_URL = "https://quantum-leap-website.vercel.app"
# Paste the code from Google Search Console's "HTML tag" verification method here (just the content="..." value).
GOOGLE_SITE_VERIFICATION = ""
OG_IMAGE = f"{SITE_URL}/img/og-image.jpg"


def page_url(fname):
    return f"{SITE_URL}/{'' if fname == 'index.html' else fname[:-5]}"


BUSINESS_ID = f"{SITE_URL}/#business"
BUSINESS = {
    "@type": "ProfessionalService",
    "@id": BUSINESS_ID,
    "name": "Quantum Leap Management Services Ltd",
    "alternateName": "Quantum Leap Management Services",
    "description": "Integrated facility management, real estate and property solutions company in Lagos, Nigeria.",
    "slogan": "Supporting your critical infrastructure needs.",
    "url": SITE_URL + "/",
    "logo": f"{SITE_URL}/img/logo.png",
    "image": [OG_IMAGE, f"{SITE_URL}/img/double-crown-plaza.jpg"],
    "telephone": PHONE_INTL,
    "email": EMAIL,
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "Suite 23, Double Crown Plaza, Ogombo Road, off Lekki-Epe Expressway",
        "addressLocality": "Ajah",
        "addressRegion": "Lagos",
        "addressCountry": "NG",
    },
    "areaServed": [{"@type": "City", "name": "Lagos"}],
    "sameAs": [IG, FB],
    "hasOfferCatalog": {
        "@type": "OfferCatalog",
        "name": "Services",
        "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": page_url(s["file"])}}
            for s in SERVICE_PAGES
        ],
    },
}

CRUMB_NAMES = {"about.html": "About us", "services.html": "Services", "projects.html": "Projects",
               "careers.html": "Careers", "contact.html": "Contact"}
SERVICE_BY_FILE = {s["file"]: s for s in SERVICE_PAGES}


def structured_data(fname, title, desc):
    graph = []
    if fname in ("index.html", "contact.html", "about.html"):
        graph.append(BUSINESS)
    else:
        graph.append({"@type": "ProfessionalService", "@id": BUSINESS_ID, "name": BUSINESS["name"], "url": SITE_URL + "/"})
    if fname != "index.html":
        crumbs = [("Home", page_url("index.html"))]
        if fname in SERVICE_BY_FILE:
            crumbs += [("Services", page_url("services.html")), (SERVICE_BY_FILE[fname]["name"], page_url(fname))]
        else:
            crumbs.append((CRUMB_NAMES.get(fname, title), page_url(fname)))
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]})
    if fname in SERVICE_BY_FILE:
        s = SERVICE_BY_FILE[fname]
        graph.append({"@type": "Service", "name": s["name"], "serviceType": s["name"], "description": desc,
                      "url": page_url(fname), "provider": {"@id": BUSINESS_ID},
                      "areaServed": {"@type": "City", "name": "Lagos"}})
        graph.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in s["faq"]]})
    data = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
    return f'<script type="application/ld+json">\n{data.replace("</", "<\\/")}\n</script>'


def seo_head(fname, title, desc):
    url, t, d = page_url(fname), html.escape(title), html.escape(desc)
    verify = (f'<meta name="google-site-verification" content="{html.escape(GOOGLE_SITE_VERIFICATION)}">\n'
              if GOOGLE_SITE_VERIFICATION else "")
    return (f'<link rel="canonical" href="{url}">\n{verify}'
            f'<meta name="theme-color" content="#12164f">\n'
            f'<meta property="og:type" content="website">\n'
            f'<meta property="og:site_name" content="Quantum Leap Management Services">\n'
            f'<meta property="og:locale" content="en_NG">\n'
            f'<meta property="og:title" content="{t}">\n'
            f'<meta property="og:description" content="{d}">\n'
            f'<meta property="og:url" content="{url}">\n'
            f'<meta property="og:image" content="{OG_IMAGE}">\n'
            f'<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
            f'<meta property="og:image:alt" content="Quantum Leap Management Services: facility management and cleaning in Lagos">\n'
            f'<meta name="twitter:card" content="summary_large_image">\n'
            f'<meta name="twitter:title" content="{t}">\n'
            f'<meta name="twitter:description" content="{d}">\n'
            f'<meta name="twitter:image" content="{OG_IMAGE}">\n'
            f'{structured_data(fname, title, desc)}\n')


for fname, (title, key, body, *rest) in PAGES.items():
    desc = rest[0] if rest else DESC
    inner = f"{header(key)}\n{body}\n{FOOTER}\n"
    full = (f'<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            f'<title>{title}</title>\n<meta name="description" content="{html.escape(desc)}">\n'
            f'{seo_head(fname, title, desc)}{FONTS}\n</head>\n<body>\n{inner}</body>\n</html>\n')
    (OUT / fname).write_text(full, encoding="utf-8")
    if key == "home":
        (Path(__file__).parent / "_preview-home.html").write_text(f"<title>{title}</title>\n{FONTS}\n{inner}", encoding="utf-8")

# Sitemap and robots.txt so search engines find every page (clean URLs, as Vercel serves them)
urls = "".join(
    f"  <url><loc>{page_url(f)}</loc><lastmod>{date.today().isoformat()}</lastmod></url>\n"
    for f in PAGES)
(OUT / "sitemap.xml").write_text(
    f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n',
    encoding="utf-8")
(OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")

print("Built:", ", ".join(PAGES))
