---
mode: agent
description: "Fetch Copilot code review comments on the current PR, assess each, and fix after user approval."
---

@Architect Review and address Copilot code review comments on the current branch's PR.

## Phase 1 — Fetch and assess

Run these commands to collect all review comments:

```
$pr = gh pr view --json number --jq .number
$repo = gh repo view --json nameWithOwner --jq .nameWithOwner
gh api "repos/$repo/pulls/$pr/comments" | ConvertFrom-Json | ForEach-Object { [PSCustomObject]@{File=$_.path; Line=$_.line; Body=$_.body} } | Format-Table -Wrap
gh api "repos/$repo/pulls/$pr/reviews" | ConvertFrom-Json | Where-Object { $_.body -ne '' } | ForEach-Object { [PSCustomObject]@{State=$_.state; Body=$_.body} } | Format-Table -Wrap
```

For each inline comment:

1. Read the file and surrounding context.
2. Assess: **valid** (real issue), **won't-fix** (disagree/out of scope), or **deferred** (valid but belongs elsewhere).
3. If valid, describe the proposed fix.

## Phase 2 — Ask for dispositions

Present a numbered table of comments with columns: #, File, Line, Status, Assessment, Proposed Fix.

Use `vscode_askQuestions` to confirm dispositions. **Stop and wait for answers.**

## Phase 3 — Implement fixes

Fix all confirmed-valid comments. Read file first, make edit, verify. Run tests. Commit.

## Phase 4 — Review-fix loop

Run a review-fix loop using @Reviewer as subagent until cleared.
