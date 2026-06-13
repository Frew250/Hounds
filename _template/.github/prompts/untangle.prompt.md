---
mode: agent
description: "Untangle a missed finalization — commit the completed step cleanly, then park any new work."
---

@Quick

I started new work before finalizing the previous step. Help me untangle this:

1. Show me `git diff --stat` and `git log --oneline -5` so we can see what's committed vs uncommitted.
2. Identify which files belong to the completed step vs the new work.
3. Stage and commit ONLY the completed step's files with a proper commit message.
4. Run `python scripts/verify_step.py` for the completed step to confirm it passes.
5. Then stage everything else as a WIP commit.
6. Push both commits.

Show me the plan before executing — I want to confirm the file split is right.
