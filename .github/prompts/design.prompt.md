---
mode: agent
agent: Design
description: "Start a Design session — 5-phase discovery flow with Dreamer subagent for divergent exploration."
---

@Design

Start a Design session for ${input:topic}.

Check `docs/ARCH_BUILD_STEPS.md` for the relevant Design Session marker and its listed focus areas. Read the canonical docs listed in the marker's Load directives.

Check `examples/_index.md` for staged examples. Read the manifest first, then selectively read files relevant to this session.

Run the full 5-phase flow: Ground + Mini-Dream → Interview → Full Dream → React → Synthesis + Critic.

Write the session summary to `docs/build/design-sessions/${input:topic}/summary.md`.
