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

## Hosting

Deployed on Vercel. `vercel.json` tells Vercel to serve the `site/` folder with no build step.
