---
mode: agent
description: "Finalize a completed step — run tests, verify, commit, push, and open/update a PR for review."
---

@Quick Finalize the current step:

1. Run the relevant test suite.
2. Run `python scripts/verify_step.py` for this step. If it fails, stop immediately.
3. Check `git diff --stat`.
4. Verify canonical doc updates from the plan's `## Canonical Doc Updates` section were applied. Verify the implementation log's `## Deferred Items` section names concrete owning steps.
5. Check whether `.github/IMPLEMENTATION_PLAYBOOK.md` needs updates based on what was learned.
6. Update `README.md` to reflect the new step status if applicable.
7. Archive mid-step working files (fixes-*.md, plan review files, subagent-outputs/, etc.) into the step's `archive/` subfolder. Only `plan.md` and `implementation*.md` stay at the top level.
8. Commit with a meaningful message, push, and open a PR to the build-track branch (or push to the existing one).
9. Remind the user to request Copilot code review on the PR via the GitHub UI.
