# CLAUDE.md — The Hounds of Cuchulain

Session entry point for any AI working in this repo. Read this first, then `AGENTS.md`
(how the owner likes to work) and `docs/PROJECT_CONTEXT.md` (the detailed site spec).
When docs disagree with the live files in `projects/site/`, the live files win.

@AGENTS.md

## What this is

The public website for **The Hounds of Cuchulain**, a Celtic folk band in Victoria, BC
— *"Celtic Folk, Loud & Alive."* A plain **static site** (no framework, no build step)
serving three audiences: fans, promoters/bookers, and press. The site lives in
[`projects/site/`](projects/site/). Project type: marketing site (static).

## Brand quick-reference

- **Tagline:** Celtic Folk, Loud & Alive
- **Voice:** bold, warm, irreverent — "a session and a show." Full guide:
  [`brand_context/voice-profile.md`](brand_context/voice-profile.md).
- **Colours** (`projects/site/styles.css` `:root`): dark base `#141414` / `#1a1a1a`,
  green accent `#4ba46a` (strong `#9be7b4`), text `#fafafa`, muted `#c2cad8`.
- **Fonts:** Cinzel + local "Livingstone" for display/headings; Inter for body
  (Google Fonts + `projects/site/livingstone/`).
- **Logo:** `projects/site/assets/hounds-logo.png` (+ `hounds_logo_transparent.png`).
  **Favicon:** present (`assets/favicon-32.png` / `favicon-180.png`).

## Tech stack

| Layer | Choice |
|---|---|
| Frontend | Plain HTML5 + CSS3 + vanilla JS (no framework, no bundler) |
| Styling | Single `styles.css`, CSS custom properties |
| Backend / DB / Auth | None — fully static |
| Hosting | Hostinger (auto-deploys the `live` branch into `public_html`) |
| Shop | External — `shop.houndsofcuchulain.com` (Wix) |
| Embeds | YouTube + Spotify (media page) |

## Preview locally

No build step — just serve the folder:

```bash
cd projects/site
python -m http.server 8000   # then open http://localhost:8000
```

## Critical rules (full list in `docs/PROJECT_CONTEXT.md`)

1. **No build step** — everything must work by opening the files or serving the folder.
2. **Show data lives only in** `projects/site/shows-data.js` — never hard-code gigs into HTML.
3. **All styling in** `styles.css` — reuse the CSS variables above; avoid inline styles.
4. **Shared JS must fail quietly** — guard DOM lookups so a script doesn't throw on a page
   that lacks the element it expects.
5. **Everything shipped is public** — no secrets, keys, or private endpoints in client code.
6. **Content is the owner's call** — show dates, prices, bios, quotes, links: confirm, never invent.
7. **Docs track reality** — when a doc and the live site disagree on an implementation detail,
   fix the doc to match the site.

## Where things are

See the "Where things are" table in `AGENTS.md`. All site files are under `projects/site/`.

## Deploy / publishing

- **Flow:** edit on `dev` → merge to `main` → push. A GitHub Action
  (`.github/workflows/publish-live.yml`) copies `projects/site/` to the root of the `live`
  branch; **Hostinger auto-deploys `live`**. So pushing **site changes** to `main` goes live
  automatically (the Action only runs when `projects/site/**` changes, so docs-only commits don't deploy).
- **Live URL:** https://houndsofcuchulain.com (Hostinger)
- **Repo:** github.com/Frew250/Hounds — default branch `main`
- Full details + manual fallback: [`memory/deploy-setup.md`](memory/deploy-setup.md).

## Working with Codex (run on every non-trivial change)

This project deliberately uses **two models**: **Claude** builds and designs; **Codex**
(via the Codex plugin) independently reviews. They have different blind spots — using both
on purpose produces materially better work than either alone.

**The loop:** Claude builds a complete first pass → hands the real code/design + context to
Codex for a sharp, severity-ranked critique (not a yes/no) → Claude reconciles each point
(fix it, or reject it with a one-line reason; surface genuine disagreements to the owner) →
re-run a short pass if the change was substantial → only then is it done.

**Invoke Codex for:** anything handling user input, forms, external APIs, or security; any
change over ~150 lines or touching multiple files; before deploying a meaningful feature; a
bug still unsolved after two attempts; and a critique pass on any new page/component or
user-facing copy (visual hierarchy, spacing, responsive behaviour, accessibility, polish).
**Skip it** for trivial edits (a copy tweak, a colour change). Treat "Codex found nothing"
on a real change as a cue to prompt harder, not as success. Full protocol: `CUSTOMIZE.md`
Section 5.

## Project decisions (don't re-litigate)

- **Contact:** show the email `hounds.of.cuchulain@gmail.com` directly. **No contact form** — by design.
- **Band members:** do **not** name the lineup (it changes). Keep bios, credits, and copy general.

## Open items

- **Album "The Unsung"** — confirm details to work into the bio / EPK.
- **EPK "Download Full EPK (PDF)"** — button is "coming soon"; the PDF doesn't exist yet.
- **`.env`** — a git-ignored leftover from the old scaffold; the static site needs no env vars.
