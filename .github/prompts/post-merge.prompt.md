---
mode: agent
description: "After merging a step PR in the GitHub UI — switch to build-track, pull, and clean up the step branch."
---

@Quick Post-merge cleanup:

1. Detect the current branch name (this is the step branch that was just merged).
2. `git checkout dev`
3. `git pull origin dev`
4. Delete the step branch locally: `git branch -D <step-branch>`
5. Delete the step branch on the remote (if it still exists): `git push origin --delete <step-branch>`
6. `git remote prune origin`
7. Confirm: clean working tree, on build-track branch, step branch gone locally and remotely.
