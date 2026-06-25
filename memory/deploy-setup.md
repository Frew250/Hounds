---
name: deploy-setup
description: How the Hounds site is hosted and published (Hostinger + auto-published `live` branch)
metadata:
  type: project
---

The live site **houndsofcuchulain.com** is hosted on **Hostinger**, which **auto-deploys the `live` branch** into `public_html` (auto-deployment is ON).

Structure: the site files live in **`projects/site/`** on `main`/`dev` (tooling like `AGENTS.md` and `.claude/` must stay at the repo root). On the **`live`** branch the site files sit at the **root** (flattened) so Hostinger serves them straight into `public_html`.

**Publishing is automated** — do NOT hand-sync `live` anymore. A GitHub Action (`.github/workflows/publish-live.yml`, using `peaceiris/actions-gh-pages@v4` with `force_orphan`) copies `projects/site/` to the `live` branch root on every push to `main`. Hostinger then auto-deploys. So the flow is simply: **edit → commit/merge to `main` → push** → Action publishes to `live` → Hostinger deploys. Watch runs at github.com/Frew250/Hounds/actions.

If the Action ever fails, the manual fallback is to sync `live` by hand: `git worktree add <dir> live`, then `git rm -rqf . && git archive origin/main:projects/site | tar -x && git add -A && git commit && git push origin live`.

The old GitHub Pages workflow was removed (redundant after moving to Hostinger). The **shop** is separate: `shop.houndsofcuchulain.com` (Wix); products live at `shop.houndsofcuchulain.com/category/all-products`.
