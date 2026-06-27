# Project Setup & Customization

This file fills in everything a new (or existing) project needs so the AI agents working in it have proper context. It is designed to be run **against a project that may already have files in it** — brand assets, configs, half-finished code. It fills gaps; it does not bulldoze what's already there.

> **Run mode:** Use `/bootstrap` for an interactive pass, or work through the sections below manually. Either way, follow the **Golden Rule** first.

---

## Golden Rule — detect before you write

Before replacing ANY placeholder or creating ANY file, check what already exists. This file is run on live projects.

1. **Scan the folder first.** Note existing brand files, `README`, `package.json`, `.env`, logo/asset folders, design files, any existing `CLAUDE.md` or `.github/` content.
2. **Never overwrite an existing file without asking.** If a target file already exists (e.g. `CLAUDE.md`, brand guide, `.env`), treat its current contents as the source of truth and only fill *missing* fields.
3. **Pull values from what's already there.** If `package.json` already names the project, or a brand file already states the colour palette / fonts / tone, read those instead of asking. Only prompt for genuinely missing values.
4. **Flag conflicts, don't resolve them silently.** If the folder says React but this file is being filled in as Vue, stop and ask.
5. **Leave a `## Gaps still open` list** at the bottom of the generated `CLAUDE.md` for anything that couldn't be auto-filled.

---

## Section 1 — Core Project Identity

Fill these in. Auto-detect from `package.json` / existing README / brand files where possible.

| Placeholder | Description | Example |
|---|---|---|
| `{{PROJECT_NAME}}` | Display name | Brentwood Bakes |
| `{{PROJECT_SLUG}}` | Lowercase hyphenated slug | brentwood-bakes |
| `{{PROJECT_DESCRIPTION}}` | One-sentence summary | A landing site + online order form for a local bakery |
| `{{PROJECT_TYPE}}` | What kind of build this is | `marketing-site` / `web-app` / `vibe-coded-prototype` / `e-commerce` |
| `{{PRIMARY_GOAL}}` | What "done" looks like for v1 | Visitors can browse menu and place a pickup order |

---

## Section 2 — Brand & Design (check for existing files first!)

**Look for these before asking:** `brand.md`, `brand-guide.*`, a `/brand` or `/assets` folder, logo files, a Figma export, an existing stylesheet with CSS variables, or colours already defined in the code.

| Placeholder | Description | Where to find it / Example |
|---|---|---|
| `{{BRAND_COLORS}}` | Primary / secondary / accent hex values | Pull from existing CSS vars, logo, or brand file |
| `{{BRAND_FONTS}}` | Heading + body typefaces | Check existing `@font-face`, Google Fonts links, brand guide |
| `{{BRAND_TONE}}` | Voice in copy | e.g. warm and casual / clean and corporate |
| `{{LOGO_LOCATION}}` | Path to logo asset(s) | e.g. `/assets/logo.svg` (note if light/dark variants exist) |
| `{{FAVICON_STATUS}}` | Present or needs creating | exists / missing |
| `{{DESIGN_REFERENCE}}` | Any reference site or mockup | URL or file path, if provided |

> If **no brand files exist**, note that under `## Gaps still open` and propose sensible defaults rather than inventing a brand silently.

---

## Section 3 — Tech Stack

Auto-detect from `package.json`, lockfiles, config files (`vite.config`, `next.config`, `tailwind.config`, etc.) before asking. Omit any row that doesn't apply — small sites won't need most of these.

| Placeholder | Description | Example |
|---|---|---|
| `{{STACK_FRONTEND}}` | Framework + language | React + TypeScript + Vite / plain HTML+CSS+JS / Next.js |
| `{{STACK_STYLING}}` | Styling approach | Tailwind / CSS modules / plain CSS |
| `{{STACK_BACKEND}}` | Backend, if any | None (static) / Express + Node / Next API routes / Supabase |
| `{{STACK_DB}}` | Database, if any | None / Supabase / SQLite / Firebase |
| `{{STACK_HOSTING}}` | Where it deploys | Vercel / Netlify / Cloudflare Pages / GitHub Pages |
| `{{STACK_AUTH}}` | Auth, if any | None / Supabase Auth / Clerk |
| `{{STACK_OTHER}}` | Notable libs/APIs | Stripe, a CMS, an email service, etc. |

> **Static site or simple vibe-coded app?** It's fine for most of this section to be "None." Don't force backend/DB/auth onto a project that doesn't have them.

---

## Section 4 — Project Conventions (for the agents)

These give the AI working in the repo its guardrails. Keep them short and real — for a small project, 3–5 rules beat 30.

| Placeholder | Where Used | What to Write |
|---|---|---|
| `{{ARCH_RULES}}` | `CLAUDE.md` | A short numbered list of hard rules. E.g. "all components functional", "no inline styles — use the design tokens", "keep secrets in `.env`, never commit them" |
| `{{FILE_LOCATIONS}}` | `CLAUDE.md` | Table mapping things to paths (components → `/src/components`, assets → `/assets`, pages → `/src/pages`) |
| `{{PROJECT_STRUCTURE}}` | `CLAUDE.md` | A quick ASCII tree of the folders that exist |
| `{{ENV_SETUP}}` | `CLAUDE.md` | `.env` variables needed, install command, run command, deploy command |
| `{{DOMAIN_TERMS}}` | `CLAUDE.md` | Any project-specific vocabulary the agent should know (omit if none) |
| `{{KNOWN_GOTCHAS}}` | `CLAUDE.md` | Anything weird/fragile in the project an agent should not break |

---

## Section 5 — Claude + Codex Collaboration Protocol

This project runs **two models working together**: **Claude** as the primary builder/designer, and **Codex** (via the Codex plugin) as an independent second model. They have different blind spots — using both, deliberately, produces materially better code and design than either alone. The goal of this section is to make sure Codex is **actually used to its fullest**, not left on the shelf.

**Operating mode: autonomous.** Claude invokes Codex directly, mid-task, without stopping to ask permission each time. Claude decides when a step meets a trigger below and runs the loop on its own, then reports what Codex found and how it was reconciled.

### The roles

| Model | Owns | Strength to lean on |
|---|---|---|
| **Claude** | Planning, building, design, copy, final integration | Architecture, UX/visual judgment, synthesis, taste |
| **Codex** | Independent review of Claude's output | Catching logic bugs, edge cases, security/correctness issues, and design weaknesses Claude is too close to see |

Codex is a **peer reviewer, not a rubber stamp.** Its job is to find problems. Treat "Codex found nothing" on a non-trivial change as a signal to prompt it harder, not as automatic success.

### The build loop (run this on every non-trivial change)

1. **Claude builds** the feature / component / fix to a complete, working first pass.
2. **Claude hands it to Codex** for an independent review (see triggers + prompts below). Claude gives Codex the actual code/design plus the relevant context, and asks for specific critique — not a yes/no.
3. **Codex critiques.** Claude collects the findings.
4. **Claude reconciles.** For each point: fix it, or consciously reject it with a one-line reason. Claude does not blindly accept Codex's changes — it applies judgment. Genuine disagreements get surfaced to Craig.
5. **Re-run if the change was substantial** — a second short pass once fixes are in.
6. **Only then** is the change considered done / ready to commit.

### When Claude must invoke Codex (triggers)

**Code:**
- Before any deploy / before committing a meaningful feature
- Any logic that handles money, auth, user input, data writes, or external API calls
- Anything security-sensitive (secrets handling, form submissions, file uploads)
- A bug Claude has attempted twice without resolving → hand to Codex for a fresh model's diagnosis
- Any file over ~150 lines, or a change touching multiple files

**Design / UX:**
- After a first visual pass on a page or key component
- Layout, responsive behaviour, accessibility (contrast, focus states, semantic markup), and visual hierarchy
- Copy and microcopy on anything user-facing

For small/trivial edits (a copy tweak, a colour change), the loop is overkill — Claude uses judgment and skips it.

### How Claude should prompt Codex (make it count)

Vague prompts waste the second model. Claude gives Codex a sharp brief:
- **Code review:** *"Review this [component] for correctness, edge cases, security, and maintainability. Assume it ships to production. List concrete problems ranked by severity, with the fix for each."*
- **Design critique:** *"Critique this UI for visual hierarchy, spacing, responsive behaviour, accessibility, and whether it looks polished or templated. Be specific and harsh."*
- **Stuck debugging:** *"Here's the bug, what I've tried, and the relevant code. Give me hypotheses I haven't considered."*

> **The standard:** every meaningful piece of work passes through both models before it's called done. Claude builds, Codex challenges, Claude reconciles. That loop — run consistently — is what delivers the highest-quality output this setup is capable of.

---

## Section 6 — Generate the Files

Once the placeholders above are filled, produce these — **but only create ones that don't already exist**, and merge into any that do:

1. **`CLAUDE.md`** at project root — the main context file. Assemble it from Sections 1–4. This is the single most important output. **Include a "Working with Codex" block** in it (condensed from Section 5) so every future session in this project knows to run the Claude-builds → Codex-reviews → Claude-reconciles loop on non-trivial work. Without this, the protocol is forgotten once setup is done.
2. **`.env.example`** — if the project has any secrets/keys, list the variable *names* (never real values).
3. **`README.md`** — if missing: project name, description, install/run/deploy commands. If it exists, leave it.
4. **`.gitignore`** — ensure `.env`, `node_modules`, build output, and OS junk are ignored. Append, don't replace.

---

## Section 7 — Establish the Repo

The deploy workflow is **push to Git → host deploys from Git**. This section gets the project onto a remote and connected to the host. Auto-detect state first: check for an existing `.git` folder, a `git remote -v`, and whether a host is already linked.

### 7a — Pre-flight (do this before the first commit)

- [ ] `.gitignore` is in place and **`.env` / secrets are listed** — confirm nothing sensitive will be committed. Run `git status` and eyeball it before the first `git add`.
- [ ] No large/build artifacts staged (`node_modules`, `dist`, `build`).

| Placeholder | Description | Example |
|---|---|---|
| `{{GIT_HOST}}` | Where the repo lives | GitHub |
| `{{REPO_VISIBILITY}}` | Public or private | private |
| `{{REPO_NAME}}` | Repo name (usually the slug) | brentwood-bakes |
| `{{DEFAULT_BRANCH}}` | Main branch name | `main` |
| `{{DEPLOY_HOST}}` | Who deploys from Git | Vercel / Netlify / Cloudflare Pages / GitHub Pages |
| `{{DEPLOY_BRANCH}}` | Branch the host deploys from | `main` (production) |
| `{{BUILD_COMMAND}}` | Build step the host runs | `npm run build` / none (static) |
| `{{OUTPUT_DIR}}` | Folder the host serves | `dist` / `build` / `.` |

### 7b — Initialise & push (only if not already a repo)

```bash
git init
git add -A
git status                       # final check — no secrets, no node_modules
git commit -m "Initial commit"
git branch -M {{DEFAULT_BRANCH}}
# create the remote (GitHub CLI):
gh repo create {{REPO_NAME}} --{{REPO_VISIBILITY}} --source=. --remote=origin --push
# or, if the remote already exists:
git remote add origin <repo-url>
git push -u origin {{DEFAULT_BRANCH}}
```

> If the folder is **already a repo**, skip init. Just confirm the remote (`git remote -v`), commit any pending work, and push.

### 7c — Connect the host

- [ ] Link the repo in the host's dashboard (Vercel/Netlify/etc.), or note it's already connected.
- [ ] Set **build command** = `{{BUILD_COMMAND}}` and **output dir** = `{{OUTPUT_DIR}}`.
- [ ] Add any `.env` variables into the host's environment settings (they aren't in Git).
- [ ] Confirm the host auto-deploys on push to `{{DEPLOY_BRANCH}}`.
- [ ] Push a trivial commit and verify the deploy goes green.

> Record the live URL and the host project name in `CLAUDE.md` under environment/deploy so the agent knows where this ships to.

---

## Section 8 — Final Checklist

- [ ] Scanned the folder; nothing existing was overwritten
- [ ] All applicable placeholders filled; N/A rows removed
- [ ] Brand values pulled from existing files where present
- [ ] `CLAUDE.md` created/updated at root
- [ ] `CLAUDE.md` includes the "Working with Codex" loop so future sessions use both models
- [ ] `.env` / secrets handled safely (names only, real values gitignored)
- [ ] Repo initialised (or confirmed existing), remote set, first push done
- [ ] Host connected; build command + output dir set; env vars added on host
- [ ] Test deploy verified green; live URL recorded in `CLAUDE.md`
- [ ] `## Gaps still open` section lists anything that couldn't be auto-filled
- [ ] This `CUSTOMIZE.md` can be deleted, or kept to re-run on the next gap

---

### `## Gaps still open`
*(The agent fills this in when running against an existing project — list every value it couldn't auto-detect and needs you to confirm.)*
