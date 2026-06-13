# Copilot Agent Workflow Template

A reusable multi-agent workflow framework for VS Code Copilot. Provides the complete planning–implementation–review loop, build artifact tracking, quality gates, and workflow automation that you'd otherwise spend weeks building from scratch.

## What's Included

| Folder | Contents |
|--------|----------|
| `.github/agents/` | Workflow agents plus support files such as `component-checklists.md` |
| `.github/instructions/` | Language-specific coding conventions (Python, TypeScript, planning) |
| `.github/prompts/` | Workflow slash commands, plus `/bootstrap` for initial customization |
| `.github/hooks/` | Hook configurations for session start, formatting, safety |
| `.github/skills/` | 7 scaffolding skills (endpoint, model, component, hook, migration, tests, seed) |
| `scripts/` | Build verification, workflow audit, and progress dashboard |
| `scripts/hooks/` | Python hook scripts (formatting, safety, context injection) |
| `docs/build/` | Where build artifacts live (plans, implementation logs, reviews) |
| `examples/` | Where domain examples are staged for design sessions |
| `memories/` | Copilot memory structure (session + repo scoped) |

## Quick Start

### 1. Copy the template

Copy the contents of this template folder into the root of your new project.

### 2. Read CUSTOMIZE.md

Open `CUSTOMIZE.md` — it lists every `{{PLACEHOLDER}}` in the template with descriptions and examples.

### 3. Run the bootstrap prompt

In VS Code with Copilot, use `/bootstrap` — it's an interactive interview that will fill in the placeholders for you based on your project.

### 4. Fill in your project docs

Create your architecture docs in `docs/`:

- `docs/DATA_MODEL.md` — your data model specification
- `docs/API_DESIGN.md` — your API endpoints
- `docs/ASSEMBLY_ENGINE.md` or equivalent — your core engine/processing docs
- `docs/FRONTEND.md` — your frontend architecture
- `docs/TEST_PLAN.md` — your testing strategy
- `docs/ARCH_BUILD_STEPS.md` — your phased build plan (steps with dependencies)

These docs are what the agents read when planning and implementing. The workflow framework doesn't work without them — the agents need architecture docs to plan from.

### 5. Fill in your skills

Each skill in `.github/skills/` is a skeleton with instructions to paste in a real example from your codebase. Once you have one working endpoint/model/component, paste it into the skill file as the pattern to follow.

### 6. Start building

```
/newstep 1a
```

For a well-scoped step that you want to run end-to-end in one session, use:

```
/autostep 1a
```

## The Agent Loop

```
Design (optional, at phase boundaries)
  ↓
Plan-Review → Critic (adversarial loop)
  ↓
Architect (implementation + self-review)
  ↓
Reviewer (independent code review)
  ↓
Architect (fix loop)
  ↓
Quick (finalize, commit, PR)
```

Optional coordinated mode:

```
Coordinator
  ↓
Quick → Plan-Review → Reviewer plan gate → Architect → Reviewer → Quick
```

Every step produces:
- `docs/build/phaseX/stepYZ-description/plan.md`
- `docs/build/phaseX/stepYZ-description/implementation.md`
- `docs/build/phaseX/stepYZ-description/archive/fixes-*.md`

## Agent Roles

| Agent | Model | Purpose |
|-------|-------|---------|
| **Coordinator** | High-reasoning | Optional orchestration-only agent for end-to-end runs. Preserves human gates and worker responsibilities. |
| **Plan-Review** | High-reasoning | All planning. Runs Critic adversarial loop automatically. |
| **Architect** | High-reasoning | All implementation. Self-reviews before handoff. |
| **Reviewer** | Different model | Independent code review. Never edits app code. |
| **Quick** | Fast model | Mechanical tasks: git, tests, file ops, finalization. |
| **Design** | High-reasoning | Architecture discovery sessions at phase boundaries. |
| **Critic** | Different model | Subagent for Plan-Review. Adversarial plan review. |
| **Dreamer** | Different model | Subagent for Design. Divergent exploration. |

Cross-model diversity is intentional — different models catch different things.

## Prerequisites

- VS Code with GitHub Copilot Chat
- Python 3.12+ (for hooks and scripts)
- Node.js (if using frontend prompts/hooks)
- Git

## Customizing Further

After the initial setup, the workflow evolves with your project:

- **Skills** get filled in as you build real patterns
- **Component checklists** grow as you discover edge cases
- **The playbook** updates with lessons learned per step
- **Architecture docs** update through the Living Architecture Protocol
- **Build steps** can be amended as the plan evolves
- **Workflow audit reports** help catch process drift as the repo grows

The framework is designed to improve with every step completed.
