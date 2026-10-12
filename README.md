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
