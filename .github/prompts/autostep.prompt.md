---
mode: agent
agent: Coordinator
description: "Run a build step end-to-end through Quick → Plan-Review → Reviewer plan gate → Architect → Reviewer loops → Quick, stopping only at human gates."
---

Start or continue coordinated execution for step ${input:stepId}.

Use the repository workflow exactly as written: Quick setup if needed, Plan-Review planning, automatic Reviewer plan review until the plan is cleared, Architect implementation, Reviewer fix loop until cleared, then Quick finalization.

Use this for well-scoped steps that should stay mostly autonomous until a real human gate appears.

By using `/autostep`, I am explicitly waiving the separate manual Human Pre-Flight pause for this run. The substitute trust check is an automatic Reviewer plan gate before implementation.

Preserve the existing `docs/build/` artifacts and human gates. If the Plan-Review ↔ Reviewer plan loop stalls on repeated technical disagreement, stop and surface the dispute instead of spinning. Stop before GitHub UI actions and tell me the exact next thing I need to do.