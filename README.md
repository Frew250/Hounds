# Hounds of Cuchulain

Workspace for **The Hounds of Cuchulain** — a Celtic folk band based in Victoria, British Columbia. _"Celtic Folk, Loud & Alive."_

This repo holds the band's website alongside the tooling used to build and maintain it.

## What's in here

| Path | Purpose |
|------|---------|
| [`projects/site/`](projects/site/) | The band's public website (the main deliverable) |
| [`projects/briefs/`](projects/briefs/) | Project briefs and specs |
| [`brand_context/`](brand_context/) | Brand voice and positioning reference |
| [`context/`](context/) | Working notes, memory, and learnings |
| [`cron/`](cron/) | Scheduled job definitions |
| [`scripts/`](scripts/) | Workspace automation and setup scripts |
| [`_template/`](_template/) | Project scaffolding template |

## The website

A vanilla static site — no framework, no build step. Deployable to any static host.

| File | Purpose |
|------|---------|
| [`index.html`](projects/site/index.html) | Main page (hero, about, shows, shop, media, contact) |
| [`shows.html`](projects/site/shows.html) | Full shows listing |
| [`epk.html`](projects/site/epk.html) | Electronic Press Kit (for promoters & media) |
| [`media.html`](projects/site/media.html) | Media / gallery page |
| [`shows-data.js`](projects/site/shows-data.js) | Show dates — **edit here to add gigs** |
| [`script.js`](projects/site/script.js) / [`chat.js`](projects/site/chat.js) | Site JavaScript |
| [`styles.css`](projects/site/styles.css) | All styles |
| [`assets/`](projects/site/assets/) | Images, logos, gallery media |

**Tech:** HTML / CSS / JS · Fonts: Cinzel (headings) + Inter (body) via Google Fonts.

### Run it locally

No build needed — open the file directly, or serve the folder:

```bash
cd projects/site
python -m http.server 8000
# then visit http://localhost:8000
```

## Band details

- **Genre:** Celtic folk / Celtic punk-influenced
- **Home base:** Victoria, BC (Vancouver Island & touring)
- **Typical set:** 60–90 minutes, flexible — festivals, theatres, pubs, special events
- **Contact:** info@houndsofcuchulain.com

## Notes

- Secrets live in `.env`, which is git-ignored — never commit credentials.
- See [`projects/briefs/hounds-site/brief.md`](projects/briefs/hounds-site/brief.md) for the full project brief and open items.
