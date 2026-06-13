# Client: Hounds of Cuchulain

Instructions for how to work in this repo. Claude reads this every session.

## About this project

The Hounds of Cuchulain are a Celtic folk band in Victoria, BC — *"Celtic Folk, Loud & Alive."*
The main thing in this repo is the band's **website**, a plain static site (HTML / CSS / JavaScript,
no framework, no build step). It lives in [`projects/site/`](projects/site/).

## How to work with me

- **Talk in plain language.** Assume I'm not a developer. Skip the jargon, and if a technical word
  is unavoidable, explain what it means in everyday terms. Tell me what a change means for the
  *website*, not just the code.
- **Just do the small stuff.** For small, obvious edits (fixing text, swapping an image, adding a
  show, tweaking styling) go ahead and make the change, then tell me what you did. For anything big,
  risky, or that changes how the site looks/works in a major way, explain the plan first and wait
  for my OK.
- **Handle git for me.** After you make changes, commit them yourself with a clear message. I don't
  want to think about git. Never commit secrets or anything in `.gitignore` (especially `.env`).
- **Flag risks.** If something could break the site or is hard to undo, say so before doing it.

## What I mostly do here

1. **Editing the website** — text, images, styling, page content.
2. **Adding shows / gigs** — keeping the gig list up to date.
3. **Deploying / publishing** — getting updates live.

## Where things are

| I want to... | Edit this |
|--------------|-----------|
| Add or change a gig/show date | [`projects/site/shows-data.js`](projects/site/shows-data.js) |
| Change the main page | [`projects/site/index.html`](projects/site/index.html) |
| Change the full shows page | [`projects/site/shows.html`](projects/site/shows.html) |
| Change the press kit (EPK) | [`projects/site/epk.html`](projects/site/epk.html) |
| Change the media/gallery page | [`projects/site/media.html`](projects/site/media.html) |
| Change colours, fonts, spacing | [`projects/site/styles.css`](projects/site/styles.css) |
| Add/replace images | [`projects/site/assets/`](projects/site/assets/) |

## Seeing the site locally

No build step — the site is just files. To preview it:

```bash
cd projects/site
python -m http.server 8000
# then open http://localhost:8000 in a browser
```

## Notes

- Band contact: info@houndsofcuchulain.com
- Full brief and open items: [`projects/briefs/hounds-site/brief.md`](projects/briefs/hounds-site/brief.md)
- Secrets live in `.env` (git-ignored) — never commit them.
