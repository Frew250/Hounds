---
mode: agent
description: "Hand off to Reviewer. Use this as a fallback — the implementation log should contain a better, step-specific reviewer prompt."
---

This is a fallback prompt. Before using it, check: did the implementer write a reviewer prompt in the implementation log's Updated Prompts section? If yes, use that instead.

If no specific reviewer prompt exists, use this:

@Reviewer Read the latest implementation log and all changed source files for the current step. Check the plan for deviation. Write findings to the step folder as the next numbered fixes file (e.g., fixes-1.md or fixes-{subplan}-1.md).
