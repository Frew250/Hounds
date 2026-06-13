# ARCH_BUILD_STEPS.md — Hounds of Cuchulain Website

**Authoritative source for phase order, step decomposition, and per-step context
loading.** Plan-Review plans from this file; the IMPLEMENTATION_PLAYBOOK is a
non-authoritative operator's guide and conflicts resolve in favour of this doc.

The website already exists and is functional. These steps cover the **remaining
gaps** from the brief plus forward maintenance. Steps are small by design — this
is a static site, so most are single-pass.

Context loading: unless noted, load `docs/PROJECT_CONTEXT.md` and the named
file(s) only. Do not read the whole `projects/site/` tree per step.

---

## Phase 1 — Close the functional gaps

The brief lists four "open items" that make the site feel unfinished. This phase
closes them.

### Step 1a — Contact form
- **Goal:** Make the contact section actually send. Static site = needs a
  third-party form service (Formspree, Netlify Forms, or Web3Forms).
- **Decision required (user):** which service, and which inbox it lands in.
- **Files:** `index.html` (contact section), `script.js`, `styles.css`.
- **Done when:** a test submission arrives at the band's inbox; success/error
  states are shown to the user; no secrets in client JS.

### Step 1b — EPK PDF
- **Goal:** Wire up the "download EPK" link on `epk.html` to a real PDF.
- **Depends on:** the PDF existing (user supplies, or we generate from the EPK
  page content).
- **Files:** `epk.html`, `assets/`.
- **Done when:** the link points to a real file and downloads correctly.

### Step 1c — Shop / Bandcamp links
- **Goal:** Replace placeholder shop and Bandcamp links with real destinations.
- **Decision required (user):** real URLs (Bandcamp, merch store).
- **Files:** `index.html`, possibly `shows.html`/`epk.html` footers.
- **Done when:** every shop/music link resolves to a real page; placeholders are
  removed or clearly labelled "coming soon".

---

## Phase 2 — Media section

> **Design session recommended before planning Phase 2.** How video/audio are
> embedded affects layout, performance, and the gallery's structure. Invoke
> **Design** to decide the approach (native embeds vs. YouTube/Bandcamp players
> vs. lightbox gallery) before Plan-Review plans the steps.

### Step 2a — Gallery
- **Goal:** Surface `assets/Gallery Assets/` properly on `media.html` (grid +
  lightbox, lazy-loaded, responsive).
- **Files:** `media.html`, `styles.css`, `script.js`.
- **Watch:** the gallery assets are heavy — lazy-load and use the `.webp`
  variants where they exist.

### Step 2b — Video / audio embeds
- **Goal:** Embed performance video and audio (the brief notes these aren't in
  place yet).
- **Decision required (user):** which platform(s) — YouTube, Bandcamp, Spotify.
- **Files:** `media.html` (and/or `index.html` media section), `styles.css`.

---

## Phase 3 — Livingstone section

> **Purpose TBD — Design session required.** `projects/site/livingstone/`
> contains a custom font and text but its role on the site is undefined. Do not
> plan implementation until the user defines what this section is for.

### Step 3a — Define and build the Livingstone section
- **Blocked on:** a user decision about what this section is.
- **Files:** new page or `index.html` section; `livingstone/`, `styles.css`.

---

## Phase 4 — Polish & launch readiness

### Step 4a — Responsive QA
- **Goal:** Verify every page renders correctly on mobile and desktop; fix
  breakpoints. **Files:** all pages, `styles.css`.

### Step 4b — Link & asset audit
- **Goal:** No broken image paths or dead links anywhere (an acceptance
  criterion). Consider adapting the `run-tests` skill into a simple link checker.
- **Files:** all pages.

### Step 4c — Accessibility & SEO pass
- **Goal:** Alt text on all images, semantic landmarks, page titles/meta
  descriptions, Open Graph tags for link previews. **Files:** all pages.

---

## Notes

- Each step still produces `plan.md` + `implementation.md` under
  `docs/build/phaseX/stepYZ-description/` and gets a Reviewer pass.
- Steps marked "Decision required (user)" are workflow-affecting — surface the
  question and wait, per the escalation policy.
- This plan can be amended as priorities shift; keep it the single source of
  truth for what's next.
