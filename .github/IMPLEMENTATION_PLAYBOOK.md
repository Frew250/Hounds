# IMPLEMENTATION PLAYBOOK

> **This is an operator's guide, not a source of truth.**
> Step sequencing → `docs/ARCH_BUILD_STEPS.md`. Rules, routing, workflow → `.github/copilot-instructions.md`.
> Architecture → canonical docs listed in `CLAUDE.md`. This playbook teaches patterns and captures
> lessons. It does not restate rules, routing tables, or step sequences from those files.

---

## Rules

All rules, quality gates, and workflow phases are defined in `.github/copilot-instructions.md`. This playbook does not restate them.

**One exception worth repeating:** This playbook is a living document. After every completed step, check whether it needs updates — new patterns, prompting improvements, workflow discoveries, or lessons learned. The finalize phase in `copilot-instructions.md` includes this as a mandatory checkpoint.

---

## Quick-Reference Prompts

These are also available as slash prompts in `.github/prompts/` — type `/plan`, `/newstep`, `/autostep`, `/design`, `/finish`, `/checkpoint`, `/park`, `/resume`, `/review`, `/pr-comments`, `/post-merge`, or `/untangle` in VS Code chat.

**`/newstep`** — Start a new step (git safety, branch creation, evolved prompt lookup)
**`/autostep`** — Run a well-scoped step end-to-end through the worker agents in one coordinated session
**`/design`** — Start a Design session before a major phase transition
**`/plan`** — Start planning (fallback if no evolved prompt exists)
**`/finish`** — Finalize a completed step
**`/checkpoint`** — Complete a sub-plan within a multi-phase step
**`/park`** — Stepping away (safety push)
**`/resume`** — Resuming
**`/review`** — Code review
**`/untangle`** — Forgot to finalize before starting new work
**`/pr-comments`** — Triage Copilot code review findings
**`/post-merge`** — Clean up after a merged step PR and return to the build-track branch

---

## Starting a New Step

1. Check `docs/ARCH_BUILD_STEPS.md` for the step description and its Load directives.
2. **Check for a Design Session marker.** If the step is preceded by a design session block, invoke **Design** before planning.
3. Check the previous step's implementation log for evolved prompts. If the prior step wrote a "next step prompt," use it.
4. If no evolved prompt exists, have Plan-Review generate one from the step description.
5. Create the step branch: `git checkout -b feat/phaseX-stepYZ-description`
6. Invoke the correct planning agent per the routing table.

---

## Agent Cheat Sheet

| Agent           | Use for                                                                               |
| --------------- | ------------------------------------------------------------------------------------- |
| **Coordinator** | Optional orchestration-only agent for end-to-end runs. Preserves worker roles and human gates. |
| **Design**      | Architecture design sessions at phase boundaries. 5-phase flow with Dreamer subagent. |
| **Plan-Review** | All planning. Creates plan, runs Critic adversarially, iterates until ready.          |
| **Architect**   | Sole implementation agent. Full spectrum from CRUD to core logic.                     |
| **Reviewer**    | Plan and code review. Human-invoked. Writes findings, never edits app code.           |
| **Quick**       | Mechanical tasks: git, test runs, file operations, finalization.                      |
| **Critic**      | Subagent-only adversarial reviewer for Plan-Review. Do not invoke directly.           |
| **Dreamer**     | Subagent-only divergent explorer for Design. Do not invoke directly.                  |

**When in doubt:** prefer Plan-Review over improvising.

---

## Execution Modes

### Interactive (default for important work)

Use the workspace custom agents and handoff buttons. Full loop: Plan → Review Plan → Human Pre-Flight → Implement → Review Code → Fix Loop → Finalize → PR Review & Merge.

**Use for:** Critical path steps, core logic, migrations, novel patterns.

### Coordinated (optional for well-scoped work)

Use **Coordinator** via `/autostep` when the step is well-scoped and expected to need little human input between phases.

**Use for:** Steps where you want one-session orchestration but still want the normal artifacts, review gates, and stop conditions.

### Cloud Agent (background for routine work)

1. Create a GitHub issue with the step title and paste the Plan-Review prompt.
2. Assign the issue to `@copilot`.
3. Check out the branch locally. Run Reviewer for a humanize pass.

**Use for:** CRUD models, schemas, routers, pattern-based UI, straightforward tests.

### Parallel Execution

Kick off 2–3 cloud agent issues, then do a critical-path step interactively.

---

## Copilot Code Review on PRs

**How to request:** Push branch → open PR → click "Request review" → select "Copilot" in the GitHub UI.

**Fix options:**

- **One-click fix:** Each comment has an "Implement suggestion" button.
- **Batch fix:** Comment `@copilot Please address all review findings in this PR.`
- **In-editor fix:** Tell Architect to read and address the review comments.
- **Selective fix:** List comments first, then fix selectively.

**After fixes:** Push to the step branch, re-request review, merge when clean.

---

## Git Safety

- **Pull only when working tree is clean.** If dirty: commit or stash first, then pull.
- **WIP commit + push = remote safety net.** Survives laptop loss.
- **git stash = local only.** Use WIP commits for overnight safety.
- Prefer `git revert` over `git reset`.
- Never `git push --force` unless explicitly asked.

---

## Quality Stack

For interactive steps you get multiple AI perspectives plus your judgment:

1. **High-reasoning plan** (Plan-Review + Critic)
2. **Adversarial critique** (Critic — different model)
3. **Optional plan review** (Reviewer — fresh eyes)
4. **Implementation** (Architect with self-review)
5. **Independent code review** (Reviewer — different model)
6. **Copilot code review** on the PR
7. **Your human read** of the final diff

---

## Prompting Conventions

- Every plan includes Round 1 implementation and review prompts.
- After each pass, the implementer writes evolved prompts into the implementation log.
- Launch subsequent work from evolved prompts, not static templates.
- Multi-pass review (3–5 rounds) is the norm for critical-path work.
- 2–3 rounds is typical for routine pattern-following work.

---

## Fix-Loop Template

1. Read the latest fixes file and the implementation log's "Updated Prompts" section.
2. Apply each finding. For any you disagree with, explain why rather than silently skipping.
3. Update the implementation log with what was changed and deferred.
4. Write updated prompts for the next round if significant rework occurred.
5. Run relevant tests.
6. If finalization is in scope, run `python scripts/workflow_audit.py` in addition to `python scripts/verify_step.py`.

---

## Lessons Learned

<!-- Add lessons as you complete steps. Examples:

**From Step X (description):**
- Cross-reference-heavy tasks lose precision under context compaction. Write critical schemas to session memory before editing.
- Post-edit verification: re-read the section, count items, verify structural changes.
- Read the canonical source doc before writing behavioral contracts.
- Every fix needs its own verification — the reviewer caught a wrong value introduced while fixing a different issue.
-->
