# Quantum Leap Management Services website

Website for Quantum Leap Management Services Ltd, a facility and property management company in Ikota, Lagos.

## Folders

- `site/` is the website: Home (`index.html`), About, Services, Contact, styles, script and photos.
- `build.py` generates the four pages in `site/`. The header, footer and contact details are defined once at the top.
- `ig-source/` holds the original Instagram graphics the photos were cropped from.

## Changing the content

1. Edit the text or contact details in `build.py`.
2. Run `python build.py` to regenerate the pages in `site/`.
3. Commit and push. Vercel redeploys automatically.

## Updating projects

The Projects page (and the property lists on Home and About) come from `projects.json`.
Add a photo to `site/img/`, put its file name in `"image"`, and fill in `"type"`, `"summary"` and `"services"` as you get the details.
Run `python build.py`, then commit and push.

## Posting a vacancy

Vacancies live in `jobs.json`.

1. Copy one of the job blocks, fill in the details, and set `"published": true`.
2. Set `"closing"` to the last day to apply (`YYYY-MM-DD`). The job disappears after that day. Leave it empty for no closing date.
3. Run `python build.py`, then commit and push.

To preview unpublished jobs locally, run `python build.py --drafts`, but rebuild with plain `python build.py` before pushing.

Applications: set `"apply_form_url"` to an application form link (for example a Tally form with a file-upload field for CVs, and a hidden field called `job`). If it's empty, the Apply button opens an email to the company instead.

## Search engines and link previews

Every page includes a canonical URL, link-preview tags (`site/img/og-image.jpg`) and structured business data for Google.
Two settings at the bottom of `build.py`:

- `SITE_URL`: currently the Cloudflare address; change it if the site moves to its own domain, then rebuild (this also updates `sitemap.xml`).
- `GOOGLE_SITE_VERIFICATION`: paste the code from Google Search Console's "HTML tag" option, then rebuild and push.

## Hosting

Hosted on Cloudflare (Workers static assets) at https://www.quantumleapmgt.workers.dev, connected to this GitHub repository: every push to `main` redeploys.
`wrangler.jsonc` tells Cloudflare to serve only the `site/` folder. `vercel.json` permanently redirects the old Vercel address (quantum-leap-website.vercel.app) to the Cloudflare site.
