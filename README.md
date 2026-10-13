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

## Posting a vacancy

Vacancies live in `jobs.json`.

1. Copy one of the job blocks, fill in the details, and set `"published": true`.
2. Set `"closing"` to the last day to apply (`YYYY-MM-DD`). The job disappears after that day. Leave it empty for no closing date.
3. Run `python build.py`, then commit and push.

To preview unpublished jobs locally, run `python build.py --drafts`, but rebuild with plain `python build.py` before pushing.

Applications: set `"apply_form_url"` to an application form link (for example a Tally form with a file-upload field for CVs, and a hidden field called `job`). If it's empty, the Apply button opens an email to the company instead.

## Hosting

Deployed on Vercel. `vercel.json` tells Vercel to serve the `site/` folder with no build step.

## Photos

The photos in `site/img/` come from [Pexels](https://www.pexels.com) and are used under the
[Pexels License](https://www.pexels.com/license/) (free for commercial use, no attribution required):

| File | Pexels photo |
| --- | --- |
| hero.jpg | https://www.pexels.com/photo/8488034/ |
| facility.jpg | https://www.pexels.com/photo/34557960/ |
| janitorial.jpg | https://www.pexels.com/photo/6196684/ |
| post-construction.jpg | https://www.pexels.com/photo/6197122/ |
| real-estate.jpg | https://www.pexels.com/photo/8470845/ |
| team.jpg | https://www.pexels.com/photo/30688593/ |
| moving-in.jpg | https://www.pexels.com/photo/4971211/ |
| keys.jpg | https://www.pexels.com/photo/7937959/ |
| about-house.jpg | https://www.pexels.com/photo/38040969/ |
| engineer.jpg | https://www.pexels.com/photo/33915172/ |
