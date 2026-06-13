---
mode: agent
agent: Quick
description: "Set up a new build step: git safety, branch, evolved prompt lookup"
---

The user is starting step ${input:stepId}. Do these things in order:

### 1. Git Safety

- Run `git status --porcelain`.
- If the working tree is dirty:
  - Show the user the dirty files.
  - Ask: "Do you want me to (a) WIP-commit and push these first, (b) stash them, or (c) abort so you can sort it out?"
  - Do NOT proceed to step 2 until the tree is clean.
- `git checkout {{BUILD_TRACK_BRANCH}} && git pull`

### 2. Create Step Branch

- Look up step ${input:stepId} in `docs/ARCH_BUILD_STEPS.md` to get the step title and phase.
- **Check for a Design Session marker** immediately before this step. If one exists, tell the user:
  "This step is preceded by a Design Session marker. Run `/design` before `/plan`."
- `git checkout -b feat/phaseX-stepYZ-description` (use the actual phase and step from ARCH_BUILD_STEPS.md)

### 3. Find Evolved Prompt

- Scan `docs/build/` for the most recently completed step folder (the one just before ${input:stepId}).
- Find the latest `implementation*.md` file.
- Search for any heading containing "Plan-Review", "Planner", "Next Step", "Updated Prompts", or "Step ${input:stepId}".
- If found, extract the full prompt text and print it clearly under **"Evolved prompt from prior step:"**.
- If NOT found, say: "No evolved prompt found in the previous step's implementation log."

### 4. Print Plan-Review Prompt

Whether or not an evolved prompt was found, also print a generic fallback:

```
@Plan-Review Plan step ${input:stepId}. Read #file:docs/ARCH_BUILD_STEPS.md for the step description and Load directives. Write to docs/build/phaseX/stepYZ-description/plan.md
```

Tell the user: "If an evolved prompt was found above, use that. Otherwise use the generic fallback."
