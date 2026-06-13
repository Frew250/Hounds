---
applyTo: "docs/build/**"
---

# Planning Conventions

These conventions apply when working on build artifacts (plans, implementation logs, fixes files) in `docs/build/`. They supplement the multi-phase rules in `copilot-instructions.md`.

---

## Prompt skeletons for multi-phase steps

When a plan has sub-plans (more than ~5 meaningful files), every sub-plan MUST include copy-paste-ready handoff prompts. The user should never have to assemble a prompt from scratch.

### Implementation prompt skeleton

```markdown
### Read first (in this order)

1. #file:docs/build/phaseX/stepYZ-description/plan.md — sections [X] only
2. #file:path/to/canonical-doc.md — section [Y] only
3. #file:path/to/prior-sub-plan-fixes.md — for context on scope changes

### Important context

- [Current codebase state relevant to this sub-plan]
- [What the prior sub-plan changed that affects this one]
- [Assumptions the implementer should verify before starting]

### Execution

1. [Step-by-step: which file, what change, what pattern to follow]
2. [If a pattern exists, name the example file explicitly]
3. [If creating a new file, name the existing file to use as template]

### Required output

1. Implementation log: what was built, deviations, test results
2. Updated Prompts section containing:
   (a) A reviewer prompt for THIS pass (three-layer)
   (b) A next-sub-plan implementer prompt (if applicable)
3. If the latest fixes file contains a `## Suggested Prompt Improvements` section,
   incorporate each suggestion into the refreshed `## Updated Prompts` section or
   explicitly reject it with reasoning in the implementation log.

### Success condition

[Concrete and verifiable. Not "it works" — say "all 12 tests pass"
or "POST /api/resource returns 201 with valid input and 409 on stale updated_at."]

### In-scope files

[Exact list. The implementer should only touch these unless they document a deviation.]
```

### Reviewer prompt skeleton (three-layer)

```markdown
### Layer 1: Mandatory baseline (implementer cannot weaken or omit these)

- Holistic file-by-file review: does each modified file match the plan's instructions for that file?
- Deviation check: does the implementation log accurately describe what changed?
- Cross-file consistency: do types, imports, schemas, and interfaces align across all modified files?

### Layer 2: Implementer-guided focus (strictly additive)

- [Specific areas for extra scrutiny]
- [Judgment calls that need validation]

### Layer 3: Adversarial framing (always present)

- Verify independently. Do not trust the implementer's self-assessment.
- Look for what the implementer may have missed or rationalized.
- Check that test coverage validates requirements, not just that tests pass.
```

### Fix prompt skeleton (Reviewer writes this)

```markdown
### Read first

1. This fixes file
2. [Specific source files that need changes]

### Execution

1. Address each finding below.
2. Critically evaluate each fix against governing docs before implementing.
3. If you believe a fix is incorrect, say so and explain why.
4. Do not blindly apply — implementation judgment is still required.

### Required output

1. Updated implementation log with a "Round N Fixes" section
2. A re-review prompt (three-layer) for this fix pass
```

---

## Prompt reconciliation after revisions

Whenever a plan changes after self-review, Critic, or Reviewer feedback, update the plan narrative and prompt blocks in the same edit pass.

1. Reconcile `Files to Create`, `Files to Modify`, `Order of Operations`, `Test Scenarios`, `Canonical Doc Updates`, `Deferred Items`, `Implementation Prompt`, `Reviewer Prompt`, and `Success condition` together.
2. A prompt is incomplete if it omits a doc or file the plan now requires.
3. Prefer named scenarios over brittle counts unless the count is part of the requirement.
4. Do not claim that a session-memory file, artifact, or handoff output already exists unless it has been verified.

---

## Code quality gates

When planning steps that produce application code, the plan MUST address these concerns explicitly.

### Backend / service work

- **Migration strategy:** Any new or modified persistence contract should state whether a migration is required and whether up/down or storage-level proof is needed.
- **Schema alignment:** Every new schema should match the underlying model or serialized contract — names, types, and optionality.
- **Registration:** New routes, modules, or registries should list the files where they must be wired in.
- **Test plan:** Name the test file and the behavioral scenarios to prove, including failure paths.
- **Error handling:** Specific messages and correct HTTP status codes. No vague fallback errors.
- **Storage semantics:** If behavior depends on persistence semantics, plan the exact contract up front and require at least one storage-level or migration-level proof.

### Frontend / UI work

- **Type alignment:** Frontend types should match the backend or serialized contract.
- **Hook and API conventions:** Name the integration files and the established pattern to follow.
- **Route registration:** New pages or routes should list where they are registered.
- **No hidden transport logic:** If the repo uses a central API client, the plan should say so.

### Core logic / engine work

- **Processing order:** If the component has a fixed pipeline or precedence order, the plan must state it explicitly.
- **Output contract:** Name the exact output shape and its downstream consumers.
- **Behavioral proof scenarios:** For output-contract work, `## Test Scenarios` must specify representative input/output proofs and edge cases, not just helper-level assertions.
- **Self-review trigger flags:** Storage-sensitive or output-sensitive steps should include `## Self-Review Trigger Flags` naming any mandatory adversarial review conditions.

### Cross-file consistency (the biggest risk in multi-file steps)

When a step creates entities spanning multiple files (Model → Schema → Router → TS Type → Hook → Component), the plan must:

1. Name every file in the chain, plus sibling write paths or reused consumers.
2. Specify the field or contract list once and reference it from each file.
3. State any create-vs-update parity or caller expectations that must move together.
4. Include a verification step to compare the contract across all affected files.

---

## Compaction resilience in plans

1. **Name the canonical doc and section** for each cross-reference
2. **Include a session-memory step** in execution instructions
3. **Keep sub-plans below 5 files × 3 canonical docs**
4. **Include post-edit verification** for enumerated instructions
5. **Verify artifact truthfulness after revisions** — counts, paths, and claimed outputs drift easily

---

## Common AI failure modes to guard against

- **Tests that test the implementation, not the requirements.** Describe behavior to verify.
- **Prompt drift.** If the plan changes, reconcile the prompt blocks and success condition in the same pass.
- **Unverified artifact claims.** Avoid claiming a session-memory file, count, or artifact exists unless verified.
- **Schema drift.** List fields once with types.
- **Contract propagation misses.** Name the sibling routes, consumers, docs, and tests that must move with the contract.
- **Import errors.** Name import paths explicitly.
- **Storage-semantics guesswork.** If persistence behavior matters, state the contract explicitly instead of assuming the implementation will infer it.
- **Over-engineering.** Say "do not add" where it applies.
- **Over-commenting.** Say "no comments that restate what the code does."
- **Pattern-matching without reading.** Say "read [file] first, then follow the same structure."
