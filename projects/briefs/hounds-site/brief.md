---
project: hounds-site
status: active
level: 2
created: 2026-05-15
---

# Hounds of Cuchulain — Band Website

## Goal
Build and maintain the public website for The Hounds of Cuchulain Celtic folk band. Craig is the developer (and band member). The site is the band's primary digital presence for fans, promoters, and media.

## Site structure
- `projects/site/index.html` — main page (hero, about, shows, shop, media, contact)
- `projects/site/shows.html` — full shows listing
- `projects/site/epk.html` — Electronic Press Kit (for promoters/media)
- `projects/site/shows-data.js` — show dates data (update here for new gigs)
- `projects/site/script.js` — site JS
- `projects/site/styles.css` — all styles
- `projects/site/assets/` — images, logos, SVGs
- `projects/site/livingstone/` — sub-section (TBD)

## Band details
- **Full name:** The Hounds of Cuchulain
- **Genre:** Celtic folk / Celtic punk-influenced
- **Home base:** Victoria, British Columbia (Vancouver Island & touring)
- **Tagline:** "Celtic Folk, Loud & Alive"
- **Typical set:** 60–90 minutes, flexible
- **Ideal for:** Festivals, theatres, pubs, special events
- **Contact:** hounds.of.cuchulain@gmail.com

## Tech stack
- Vanilla HTML/CSS/JS (no framework)
- Fonts: Cinzel (headings) + Inter (body) via Google Fonts
- No build step — static files, deployable anywhere

## Deliverables
- Functional multi-page static site
- Shows data system (JS-driven, easy to update)
- EPK page for promoters
- Content for all sections (about, bio, shows, shop, media)

## Acceptance criteria
- All pages render correctly across mobile and desktop
- Shows data loads dynamically from `shows-data.js`
- EPK has downloadable PDF link wired up
- Contact form functional (or clearly deferred)
- No broken image paths or dead links

## Constraints
- Static hosting (no backend)
- Craig manages both development and content

## Open items
- `livingstone/` subfolder — purpose TBD
- Shop links (Bandcamp, merch) — placeholders currently
- EPK PDF — not yet created
- Contact form — needs a service (Formspree, Netlify Forms, etc.)
- Media section — video/audio embeds not yet in place
