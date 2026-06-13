# Template Maintenance Plan — DELETE THIS FILE

> This file is a maintainer note for `_template/`. It should not ship in a
> customized project. Delete it once the template has been copied into a real
> repo.

This file tracks what the template is expected to contain and how it should be
kept in sync with the live workflow.

---

## What This Template Is

A sanitized Copilot-agent workflow framework for VS Code:

- multi-agent planning, implementation, review, and finalization
- build artifact structure under `docs/build/`
- slash prompts for the common workflow actions
- reusable hook and script infrastructure
- skill skeletons that the target repo fills in with its own patterns

The template should mirror the live workflow structure, but with domain,
organization, and tech-stack specifics replaced by placeholders or generic
guidance.

---

## Current Shipped Surface

The template should currently include these workflow surfaces.

### Agents

- `Architect`
- `Plan-Review`
- `Reviewer`
- `Quick`
- `Design`
- `Critic`
- `Dreamer`
- `Coordinator`
- `component-checklists.md` as a support file for planning/review prompts

### Prompts

- `bootstrap`
- `autostep`
- `checkpoint`
- `design`
- `finish`
- `newstep`
- `park`
- `plan`
- `post-merge`
- `pr-comments`
- `resume`
- `review`
- `untangle`

### Scripts

- `verify_step.py`
- `build_progress.py`
- `workflow_audit.py`
- `scripts/hooks/*`

### Core Docs

- `README.md`
- `CUSTOMIZE.md`
- `CLAUDE.md`
- `.github/copilot-instructions.md`
- `.github/IMPLEMENTATION_PLAYBOOK.md`
- `.github/instructions/*`

Avoid hard-coded counts in these files where possible. Prefer naming the actual
surface area instead of saying "7 agents" or "11 prompts" so the template does
not go stale every time the workflow grows.

---

## Sync Policy

When the live workflow changes, propagate the sanitized version into `_template/`
by source area.

### Must sync quickly

- `.github/agents/`
- `.github/prompts/`
- `.github/instructions/`
- `.github/copilot-instructions.md`
- `.github/IMPLEMENTATION_PLAYBOOK.md`
- generic scripts under `scripts/`
- user-facing template docs (`README.md`, `CUSTOMIZE.md`, this file)

### Sync when relevant to portability

- `.github/hooks/`
- `scripts/hooks/`
- skill skeleton wording in `.github/skills/`

### Intentionally not mirrored

- application code under `app/` or `frontend/`
- canonical architecture docs under `docs/`
- deployment workflows under `.github/workflows/`
- app-specific seed/delete scripts
- deprecated live-only agents or experiments

---

## Sanitization Rules

When copying from the live repo into `_template/`:

1. Replace project/domain specifics with placeholders or generic wording.
2. Keep workflow mechanics intact unless they depend on app-specific behavior.
3. Preserve file paths that are part of the workflow contract (`docs/build/`,
   `.github/prompts/`, `.github/agents/`, `scripts/`).
4. Remove organization-specific names, schema names, storage prefixes, and
   business-domain examples unless they are converted into placeholders.
5. Prefer generic examples over app-specific examples when a concept needs one.

---

## Maintenance Checklist

When refreshing `_template/` from the live workflow:

1. Inventory the live agents, prompts, hooks, instructions, and scripts.
2. Add any missing template files before editing the docs that reference them.
3. Update the top-level docs so they describe the actual shipped template.
4. Search `_template/` for stale names, counts, or references to removed files.
5. Verify that every template prompt or doc only references files that exist in
   `_template/`.
6. Verify that live workflow files were not edited during the refresh.

---

## Placeholder Convention

The template uses `{{PLACEHOLDER}}` syntax for project-specific values. See
`CUSTOMIZE.md` for the full placeholder list and fill-in guidance.
