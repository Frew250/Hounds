# PROJECT_CONTEXT.md — Hounds of Cuchulain Website

The source-of-truth context for the website. Read this before planning or
implementing any change. For how Claude should work in this repo, see
`AGENTS.md` at the repo root.

---

## What This Project Is

The public website for **The Hounds of Cuchulain**, a Celtic folk band based in
Victoria, British Columbia (Vancouver Island & touring). The site is the band's
primary digital presence for three audiences: **fans**, **promoters/bookers**,
and **media/press**.

Tagline: _"Celtic Folk, Loud & Alive."_

Craig (the developer) is also a band member and manages both the code and the
content.

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Markup | HTML5 (multi-page, hand-authored) |
| Styling | CSS3 — single stylesheet, no preprocessor |
| Behaviour | Vanilla JavaScript — no framework, no bundler |
| Fonts | Display/headings: local "Livingstone" with Cinzel fallback; body: Inter (Cinzel + Inter via Google Fonts, Livingstone in `projects/site/livingstone/`) |
| Build step | **None** — static files, open directly or serve the folder |
| Backend / DB / Auth | **None** — fully static |
| Hosting | Static host (GitHub Pages, Netlify, or similar) |

There is no package manager, no compile step, and no server. A change is "live"
the moment the static files are deployed.

---

## Site Structure

```
projects/site/
  index.html        # Main page: hero, about, shows, shop, media, contact
  shows.html        # Full shows listing
  epk.html          # Electronic Press Kit (for promoters & media)
  media.html        # Media / gallery page
  shows-data.js     # Show dates — SINGLE SOURCE OF TRUTH for gigs
  script.js         # Site behaviour
  chat.js           # Chat widget behaviour
  styles.css        # All styles
  assets/           # Images, logos, gallery media
    Gallery Assets/ # Photo/video gallery source
  livingstone/      # Sub-section (Livingstone font + text) — purpose TBD
```

---

## Critical Architecture Rules

1. **No build step.** Everything must work by opening the HTML files directly or
   serving the folder statically. Do not introduce a bundler, transpiler, or
   npm dependency without an explicit decision.
2. **Show data lives only in `shows-data.js`.** Never hard-code gig dates,
   venues, or times into the HTML. Pages render shows dynamically from this file.
3. **All styling in `styles.css`.** No inline `style=""` except where genuinely
   dynamic. Reuse existing fonts and colour values.
4. **JS fails quietly.** A script shared across pages must not throw when an
   element it expects is absent on a given page. Guard DOM lookups.
5. **No secrets in client code.** Everything shipped is public. No API keys,
   tokens, or private endpoints in the HTML/JS.
6. **Content is the user's call.** Show dates, prices, bios, quotes, and links
   are content — confirm with the user; never invent them.
7. **Docs track reality.** If this document and the live site disagree, the live
   site wins for implementation details — update this doc to match.

---

## Key Concepts

| Term | Definition |
|------|------------|
| **EPK** | Electronic Press Kit — the `epk.html` page promoters and media use to book or write about the band (bio, photos, tech needs, contact). |
| **Shows / gigs** | Live performance dates. Stored in `shows-data.js`, rendered on `index.html` and `shows.html`. |
| **Hero** | The top banner section of `index.html`. |
| **Gallery** | The photo/video collection under `assets/Gallery Assets/`, surfaced on `media.html`. |
| **Livingstone** | A custom font (and text) in `projects/site/livingstone/`; its role on the site is not yet defined. |

---

## Band Details (reference for content work)

- **Full name:** The Hounds of Cuchulain
- **Genre:** Celtic folk / Celtic punk-influenced
- **Home base:** Victoria, BC (Vancouver Island & touring)
- **Typical set:** 60–90 minutes, flexible
- **Ideal for:** Festivals, theatres, pubs, special events
- **Contact:** hounds.of.cuchulain@gmail.com

---

## Acceptance Criteria (from the brief)

- All pages render correctly across mobile and desktop.
- Shows load dynamically from `shows-data.js`.
- EPK has a working downloadable PDF link.
- Contact form is functional (or clearly deferred to a named service).
- No broken image paths or dead links.

---

## Source

This document is derived from `projects/briefs/hounds-site/brief.md`. When the
brief and the live site disagree, the live site wins for implementation details;
update this doc to match reality.
