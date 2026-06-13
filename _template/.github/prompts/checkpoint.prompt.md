---
mode: agent
description: "Checkpoint a completed sub-plan within a multi-phase step — verify, commit, and push."
---

@Quick Checkpoint the current sub-plan. Run `python scripts/verify_step.py` with the sub-plan ID for this step, commit with a meaningful message, and push. Do not archive, open a PR, or request review — those happen at `/finish` when the full step is done.
