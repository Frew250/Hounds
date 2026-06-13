# Copilot Workspace Instructions

<!-- CODE REVIEW RULES — first 4,000 chars are read by Copilot PR code review.
     Everything after the "--- END CODE REVIEW RULES ---" marker is for Copilot
     Chat and agents only. Keep this block under 4,000 characters. -->

## Code Review Rules

When performing a code review, enforce these architecture rules:

<!-- Replace this entire section with YOUR project's code review rules.
     Keep it under 4,000 characters. Organize by area:

### Database & Models
- Schema rules, soft-delete policy, FK conventions, PK conventions, timestamps

### API Endpoints
- Pagination, concurrency checks, audit logging, HTTP status codes, error handling

### Engine / Core Logic
- Processing order, resolution precedence, output format rules

### Frontend
- Type safety, API client rules, state management, loading states

### General
- No secrets, logging requirements, naming conventions
-->

This is a **static website** — vanilla HTML5, CSS3, and JavaScript with no
build step, no backend, no database, and no framework. Review with that in mind.

### HTML
- Pages are standalone HTML files in `projects/site/`. Keep markup semantic and accessible (landmarks, alt text on images, descriptive link text).
- No inline `<script>`/`<style>` blocks for anything non-trivial — JS lives in `.js` files, CSS in `styles.css`.
- Every `<img>`/`<a href>` must point to a real asset or page. Broken paths and dead links are review-blocking.

### CSS
- All styles live in `projects/site/styles.css`. No inline `style="..."` attributes except where genuinely dynamic.
- Must render correctly on mobile and desktop — check responsive breakpoints.
- Use the established fonts (Cinzel for headings, Inter for body) and existing colour values; don't introduce one-off styles.

### JavaScript
- Vanilla JS only — no framework, no bundler, no npm dependencies added without discussion.
- Show data is the single source of truth in `projects/site/shows-data.js`. Never hard-code gig dates into HTML.
- Keep DOM queries defensive (an element may be absent on pages that don't include it). Fail quietly; never throw on a normal page load.

### Content & Data
- Band-facing copy, dates, and links are content — confirm changes with the user; don't invent show dates, prices, or quotes.
- Placeholder links (shop, Bandcamp, EPK PDF) must be clearly marked, not silently broken.

### General
- Never commit secrets or `.env`. No API keys in client-side JS (it's all public).
- No large new binaries without reason — the gallery assets are already heavy.
- Match the existing code's style and indentation in each file.

<!-- --- END CODE REVIEW RULES --- -->

---

## Session Startup

1. `git pull` on the current build-track branch (currently `dev`).
2. Create or switch to a step branch off that build-track branch: `git checkout -b feat/phaseX-stepYZ-description`
3. Read ONLY the docs relevant to the current task.
4. Use the workspace custom agents and their handoff buttons by default.

---

## Default Operating Mode

This workspace is designed around a custom-agent workflow, not a single general-purpose chat thread.

**Use handoffs instead of retyping context whenever possible.**
The intended loop is fully viable in VS Code because custom agents can hand off to other custom agents, and custom agents can invoke scoped custom subagents.

That means the workflow is:

- **Plan-Review** handles all planning, with Critic as its adversarial subagent.
- **Critic** runs as its subagent for adversarial plan review.
- **Reviewer** can hand work back to **Architect** for fixes.

An optional **Coordinator** agent can orchestrate the same worker flow end-to-end in one session while preserving the same artifacts and human stop points.

For all important tasks, default to the best available model in high reasoning mode.
Important tasks include planning, architecture decisions, critical-path implementation,
novel logic, migrations with production risk, and any review pass that decides correctness.

---

## Agent Selection

| Agent           | Default model    | Use for                                                                                                                                                                  |
| --------------- | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Coordinator** | High-reasoning   | Optional top-level workflow orchestrator. Runs Quick, Plan-Review, Reviewer plan review, Architect, Reviewer, and Quick in one session while preserving human gates.   |
| **Design**      | High-reasoning   | Architecture design sessions. Orchestrates 5-phase discovery flow with Dreamer subagent for divergent exploration. Produces updated canon docs with provenance tags.     |
| **Plan-Review** | High-reasoning   | All planning. Writes the plan, runs Critic for adversarial review, then hands off to Architect.                                                                          |
| **Architect**   | High-reasoning   | Sole implementation agent. Handles the full spectrum from CRUD scaffolding to core logic.                                                                                |
| **Reviewer**    | Cross-model      | Plan and code review. Human-invoked (with optional context). Writes findings to `docs/build/` and never edits application code.                                          |
| **Quick**       | Fast model       | Mechanical work: git, test runs, file operations, cleanup, import hygiene, and final wrap-up.                                                                            |
| **Dreamer**     | Cross-model      | Subagent-only divergent explorer. Used by Design for Mini-Dream and Full Dream phases. Do not invoke directly.                                                           |
| **Critic**      | Cross-model      | Subagent-only adversarial reviewer. Used by Plan-Review for plans AND by Design for feasibility checks. Do not invoke directly.                                          |

### Mandatory routing

All implementation routes through **Plan-Review** (planning) → **Architect** (implementation).

| Work type | Required scrutiny |
|---|---|
| New page or major layout change | Plan-Review (plan the structure + responsive behaviour) → Architect |
| Shows data / schedule changes (`shows-data.js`) | Plan-Review confirms the data shape with the user → Architect |
| Content/copy changes (about, bio, EPK) | Confirm wording with the user before publishing → Architect |
| Styling system changes (`styles.css` variables, fonts, breakpoints) | Plan-Review (site-wide impact) → Architect |
| Third-party integrations (contact form, embeds, shop links) | Plan-Review (privacy, which service) → user decision → Architect |

All other work (small copy tweaks, single-asset swaps, link fixes, docs) also routes through Architect. Prefer **Plan-Review** over improvising.

---

## Workflow

### Design Sessions (before major phase transitions)

`docs/ARCH_BUILD_STEPS.md` marks natural stopping points where the user should invoke **Design** before Plan-Review can plan the next group of steps effectively. Design sessions produce updated canonical docs, not implementation plans.

Design runs a 5-phase session: Ground + Mini-Dream (automatic) → Interview (human) → Full Dream (automatic, different model) → React (human, decision table) → Synthesis + Critic (automatic). The Dreamer subagent runs on a different model for cognitive diversity.

**Enforcement gate:** Plan-Review refuses to plan any step preceded by a Design Session marker unless a `docs/build/design-sessions/<topic>/summary.md` file exists or the user explicitly waives the session.

**Examples folder:** Users stage real project files in `examples/` (gitignored) with a manifest at `examples/_index.md`. Design reads the manifest to select session-relevant files.

### Coordinated End-to-End Mode (optional)

An optional **Coordinator** agent can orchestrate the existing workflow in one session: Quick → Plan-Review → Reviewer plan gate → Architect → Reviewer fix loop → Quick.

- Use it when a step is already well-scoped and expected to need little human input.
- It preserves the same `docs/build/` artifacts, review gates, and worker responsibilities as the manual workflow.
- Starting Coordinator is an explicit opt-in waiver of the manual Human Pre-Flight pause for that run.
- It must still stop at human gates: dirty tree decisions, Design-session requirements, workflow-affecting questions, major replanning, or GitHub UI actions.

### Question Escalation Policy

- **Technical refinements** default to Plan-Review + Critic. Prefer the best extensible technical path for the application instead of escalating routine engineering choices.
- **Workflow-affecting or missing-feature questions** go to the user.
- **Ask as late as safely possible.** If research and most of the plan can continue before a user decision is needed, do that work first and batch the remaining questions.
- **Use plain language.** Explain why the choice matters, include a recommended default, and say whether work can continue while waiting.

### Technical Decision Guardrails

- Reuse an existing repository pattern when it already solves the same problem cleanly.
- Prefer framework-native and maintained-library solutions before inventing custom helpers or abstraction layers.
- Use domain-driven names and boundaries for load-bearing concepts.
- Keep the design as simple as the requirement allows.
- If a limit or rule is arbitrary and not load-bearing, prefer changing the constraint over building complexity around it.

### Phase 1: Plan

1. Use **Plan-Review** for all planning. It runs the Critic adversarial loop automatically.
2. Use `#file:` references to load only the relevant docs and code.
3. Write the plan to `docs/build/phaseX/stepYZ-description/plan.md`.
4. Verify the plan file exists and is readable.

### Phase 2: Review The Plan

5. Plan-Review runs the Critic loop automatically and keeps findings and dispositions in the plan file.
6. Optionally, invoke **Reviewer** for an independent human-directed plan review after the Critic loop completes.
7. Do not implement while critical plan issues remain unresolved.

### Phase 3: Human Pre-Flight

8. Open the plan file yourself and read it before implementation.
9. Check:

- Does it touch files with local uncommitted work?
- Do the assumptions match the current codebase?
- Is it about to delete or replace something unexpectedly?

### Phase 4: Implement

10. Use **Architect** for all implementation.
11. Implement from the plan file and the latest review or fixes file only.
12. Write the implementation log to `docs/build/phaseX/stepYZ-description/implementation.md` (single-pass steps) or `implementation-{subplan}.md` (multi-phase steps).
13. Run targeted tests as you go, then the relevant broader test suite.

### Phase 5: Review The Code

14. Hand off to **Reviewer**. The user may add context (concerns, focus areas).
15. Reviewer reads the implementation log plus changed source files and writes `fixes-1.md` (or `fixes-{subplan}-1.md`) in the step folder.
16. Reviewer includes a **Humanize** section — stripping AI-generated verbosity, redundant comments, and robotic patterns.

### Phase 6: Fix Loop

17. Hand off back to Architect.
18. Implement from the latest fixes file only.
19. Rerun relevant tests.
20. If fixes are significant, send back to **Reviewer** for another pass (creates `fixes-2.md`, etc.).
21. Stop only when Reviewer reports no critical issues.

### Phase 7: Finalize

22. Use **Quick** for final mechanical wrap-up: run full tests, run `python scripts/verify_step.py phaseX stepYZ-description`, run `python scripts/workflow_audit.py`, check `git diff --stat`, and update any step docs that are stale.
23. If `verify_step.py` fails, stop finalization and surface the failing checks clearly.
24. Check whether `IMPLEMENTATION_PLAYBOOK.md` needs updates based on what was learned during this step.
25. Verify canonical doc updates from the plan's `## Canonical Doc Updates` section were applied. Verify the implementation log's `## Deferred Items` section names concrete owning steps.
26. Quick archives mid-step working files into the step's `archive/` subfolder.
27. Quick commits, pushes, and opens a PR from the step branch to `dev`. **Quick does not merge the PR.**

### Phase 8: PR Review and Merge (human-driven)

28. Copilot code review runs on the PR. Wait for it to complete.
29. Use `/pr-comments` to fetch and address Copilot's PR comments.
30. After fixes clear, run `python scripts/verify_step.py phaseX stepYZ-description` one final time.
31. When all reviews are clean, **you (human) merge the PR** via the GitHub UI.
32. After merge, delete the step branch. Use `/newstep` to start the next step.

---

## Review Cadence

Copilot code review intensity is tiered by step risk, not applied uniformly to every PR.

| Tier | When | Mechanism |
|---|---|---|
| **Per-step** | Critical-path steps: core logic, auth, schema migrations, load-bearing interfaces | Request Copilot code review on the individual step PR |
| **Batch-deferred** | Patterned CRUD groups following an established pattern | Merge per-step PRs without Copilot review; batch review at group boundary |
| **Phase boundary** | End of a major phase or build-track merge to `main` | Full-diff review PR |

---

## Build Artifacts

Every completed build step must maintain these files in its own folder under `docs/build/`:

```text
docs/build/phaseX/stepYZ-description/
  plan.md
  implementation.md
  archive/                # created at finalization by Quick
    plan-fixes-1.md       # optional: Reviewer plan review findings
    fixes-1.md            # numbered review rounds
    fixes-2.md
    subagent-outputs/     # raw subagent findings
```

Rules:

- The plan file is the source of truth for what should be built.
- The implementation file records what was actually done and what was validated.
- Each review pass gets its own numbered fixes file.
- The implementer always reads only the latest fixes file.

### Multi-Phase Steps

When a step is too large for one implementation pass (more than ~5 meaningful files), split it into sub-plans:

```text
docs/build/phaseX/stepYZ-description/
  plan.md                          # single source of truth
  implementation-{subplan}.md      # one per sub-plan
  archive/
    fixes-{subplan}-N.md           # review per sub-plan
    subagent-outputs/
```

Sub-plan rules:

- Reviewer is mandatory after each sub-plan.
- When starting sub-plan N+1, read the latest fixes from sub-plan N for scope changes.
- The plan file remains the single shared source of truth.
- **Prompt handoff quality:** Implementation logs must contain copy-paste-ready prompts for both the reviewer (three-layer structure) and the next sub-plan implementer.

### Subagent Output Persistence

When subagents are invoked for review or verification, they **must write their raw findings to a file** before returning their summary:

```text
docs/build/phaseX/stepYZ-description/subagent-outputs/
  {subagent-name}-{date}.md
```

---

## Operating Tips

### Use `#file:` references

Always prefer `#file:path/to/file` over pasted snippets.

### Scope attention tightly

Do not say "read the whole doc." Say exactly which section matters.

### Break up large work

If a step spans more than about five meaningful files, use checkpoints.

### When an agent is stuck

Stop it and ask for the exact error first.

### Use `/compact`

When the session gets long:

```text
/compact Keep: current step, plan file path, implementation status, open blockers. Forget: earlier exploration and abandoned attempts.
```

---

## Compaction Resilience

Context compaction can silently discard cross-reference details mid-implementation. The following rules are mandatory:

### Session Memory for Critical Cross-References

Before starting any implementation that references schemas, field lists, precedence orders, or behavioral contracts from other docs, write the critical values to session memory (`/memories/session/cross-refs.md`). Session memory survives compaction.

### Post-Edit Verification Checklist

After editing any section with enumerated requirements:

1. **Read the edited section back in full** — do not rely on memory.
2. **Compare bullet-by-bullet against the plan instruction** — count items.
3. **For enumerated additions**, count the installed items and confirm the range is complete.

### Canonical Doc Read-Before-Write Rule

When writing behavioral contracts, schemas, or processing rules into target files, read the canonical source doc first — not the plan's summary.

---

## Canonical Heading Reference

Build artifact files use specific Markdown headings that workflow scripts parse programmatically. **Agents MUST use exactly these headings.**

### Plan files (`plan.md`)

| Heading | Purpose |
|---|---|
| `## Canonical Doc Updates` | Lists doc changes this step must make |

### Implementation logs (`implementation*.md`)

| Heading | Purpose |
|---|---|
| `## Deferred Items` | Work pushed to a future step |
| `## Updated Prompts` | Reviewer and next-sub-plan prompts |
| `## Self-review results` | Pass 1/2/3 summary from Architect self-review |
| `## Deviations from plan` | Where implementation diverged |
| `## What was built` | File-by-file summary |

### Fixes files (`fixes*.md`)

| Heading | Purpose |
|---|---|
| `## Verdict` | Cleared / Not cleared |

---

## Quality Gates

- **`docs/ARCH_BUILD_STEPS.md` is the authoritative source for phase order, step decomposition, and per-step context loading.**
- **Every step gets a plan, implementation log, and review file.** No exceptions.
- **Every step gets review.** Reviewer is mandatory.
- **Critical path work does not skip Architect.**
- **Plan-Review is the single planning agent for all build steps.**
- **Use the best available model in high reasoning mode for every important task.**

---

## Living Architecture Protocol

Canonical architecture docs were written before the codebase existed. As each build step runs, it will discover gaps, omissions, and occasionally conflicts. This protocol governs how those discoveries feed back into the docs.

### Change classification

| Category | Scope | Who decides | Protocol |
|---|---|---|---|
| **Workflow-affecting** | Changes what end users see, business rules, output format | User | Plan-Review surfaces as interactive question. Implementation proceeds only after user decision. |
| **Technical refinement** | Code organization, validation, API surface, developer ergonomics | Plan-Review + Critic | Plan-Review proposes. Critic evaluates. Escalates to user only if disagreement. |

**When in doubt, classify as workflow-affecting.**

### Doc update mechanism

Plans include a `## Canonical Doc Updates` section listing what's missing, wrong, or incomplete in canonical docs, with proposed changes, classification, and timing.

### Deferred items

Implementation logs include a `## Deferred Items` section listing what was deferred and where it should land.

---

## File Locations

| Category | Path |
|---|---|
| Website source (all pages) | `projects/site/` |
| Main page | `projects/site/index.html` |
| Shows listing / EPK / media pages | `projects/site/shows.html`, `epk.html`, `media.html` |
| Show data (single source of truth) | `projects/site/shows-data.js` |
| Site JavaScript | `projects/site/script.js`, `projects/site/chat.js` |
| Styles | `projects/site/styles.css` |
| Images, logos, gallery media, fonts | `projects/site/assets/`, `projects/site/livingstone/` |
| Project brief | `projects/briefs/hounds-site/brief.md` |
| Build artifacts (plans, logs, reviews) | `docs/build/` |
| Build plan (authoritative step order) | `docs/ARCH_BUILD_STEPS.md` |
| Full project context | `docs/PROJECT_CONTEXT.md` |
| Brand voice reference | `brand_context/` |

---

## Code Standards

<!-- Brief version — the full version is in CLAUDE.md -->

- Type hints / explicit types on all signatures
- All new code gets tests
- Never commit secrets or `.env`
- Do not treat a step as complete while build artifacts are missing or stale

---

## End Of Step

When a step is done, report:

1. Which step was completed
2. Which files changed
3. Which tests were run and whether they passed
4. Whether there are any remaining blockers or follow-up items
5. The exact next recommended prompt for the next session
