---
mode: agent
description: "Start planning the next build step. Use this as a fallback — check for an evolved prompt from the previous step first."
---

This is a fallback prompt. Before using it, check: did the previous step's implementation log write a "next step prompt" in its Updated Prompts section? If yes, use that instead — it will be more specific.

If no evolved prompt exists, use this:

@Plan-Review Read #file:docs/ARCH_BUILD_STEPS.md and identify the next unstarted step. Read the Load directives for that step to know which docs to consume. Check the previous step's implementation log for any context or warnings carried forward. Plan the step and write to the appropriate docs/build/phaseX/stepYZ-description/plan.md folder.

The plan will include a Round 1 implementation prompt and a Round 1 reviewer prompt. Those evolve with each pass — the implementer writes updated prompts into the implementation log after each round.
