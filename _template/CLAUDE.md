# CLAUDE.md — AI Assistant Session Instructions

Read this file first. Then read `PROJECT_CONTEXT.md` for full detail.

---

## What This Project Is

{{PROJECT_DESCRIPTION}}

<!-- Fill in: 2-3 sentences expanding on the description. What does it do, who uses it, what's the tech stack at a high level? -->

---

## Source of Truth Policy

`PROJECT_CONTEXT.md` and `CLAUDE.md` are the source of truth for **what the application does** — its functionality, business rules, data model, and requirements. They were written before the codebase existed and without the benefit of a live development environment.

They are **not** the source of truth for implementation conventions, framework patterns, or tooling details (e.g., table naming conventions, ORM syntax, migration patterns, UI component patterns). When the docs prescribe an implementation detail that conflicts with the correct or idiomatic way to use a tool or framework, **update the docs to match reality** — do not force the code to follow an incorrect convention from the docs.

**Stated constraints vs. gaps.** Canonical docs are authoritative for what they explicitly state. When a doc is _silent_ on something the implementation needs (e.g., a validation rule the author didn't enumerate, an edge case not contemplated), that is a gap — not a prohibition. Gaps are filled through the Living Architecture Protocol in `copilot-instructions.md`: propose the addition, classify it, and either update the doc (technical refinement) or surface to the user (workflow-affecting change).

When a stated constraint needs to change — because it produces worse output, conflicts with how a framework actually works, or because implementation reveals a better approach — that is also handled through the Living Architecture Protocol. Authoritative does not mean frozen. The docs improve through every build step. The only hard rule is: changes that affect what end users see require the user's decision.

---

## Starting a Session

1. Read `PROJECT_CONTEXT.md` for project overview, architecture, and critical rules
2. Read this file for session rules and coding standards
3. Read the relevant `docs/` file for your current task area
<!-- Fill in your docs list, e.g.:
   - `docs/DATA_MODEL.md` — models, schemas, migrations, database work
   - `docs/API_DESIGN.md` — routers, endpoints, request/response
   - `docs/FRONTEND.md` — React components, layouts, pages
   - `docs/TEST_PLAN.md` — writing or running tests
-->
4. Ask what we are working on today
5. Create a feature branch before writing any code (see Git Workflow below)
6. If resuming from a previous session, check which branch we were on and what state the code is in before touching anything

---

## Git Workflow

### Before Starting Any Work

```bash
git pull                              # on the current build-track branch
git checkout -b feat/1234-descriptive-name
```

During active build phases, the build-track branch is `{{BUILD_TRACK_BRANCH}}` — not `main`. Create step branches off the build-track branch.

Use lowercase, hyphens, no spaces in branch names, and include the ticket/task number when available:

- `feat/1234-descriptive-name`
- `fix/1234-bug-description`

### During Work

Commit frequently with meaningful messages:

- Format: `"Add [thing]"`, `"Fix [issue]"`, `"Update [component] to [do what]"`
- Good: `"Add User and Organization SQLAlchemy models"`
- Bad: `"updates"`, `"WIP"`, `"stuff"`

**Never commit:**

- `.env`, secrets, connection strings, API keys, or passwords — if about to write something that looks like a credential, stop and confirm first
- `__pycache__/`, `.venv/`, `node_modules/`, `*.db`, or any file in `.gitignore`
- If creating a new file type that should be ignored, add it to `.gitignore` before committing

### When Work Is Complete

```bash
# Push the step branch
git push origin feat/1234-descriptive-name

# Open a PR (or confirm existing one has the new commits)
gh pr create --base {{BUILD_TRACK_BRANCH}} --title "Step X: description" --body "..."
```

During active build phases, step branches merge into the build-track branch via PR after review. **Merging is done manually by the human via the GitHub UI** after all reviews clear. Only merge directly to `main` once the build-track branch itself is ready to land.

### If Something Goes Wrong

- Do not use `git push --force` unless explicitly asked and consequences are understood
- If a merge has conflicts, show the conflicts and explain what each side is before resolving
- Prefer `git revert` (creates a new commit that undoes changes) over `git reset` (rewrites history)
- Never `git mv` or delete a `??` (untracked) file without first committing, stashing, or copying it

---

## Critical Architecture Rules

<!-- Replace this section entirely with YOUR project's numbered architecture rules.
     These are the hard invariants that every agent must respect.
     Examples of the kinds of rules to include:

1. Database schema rules (e.g., "all tables use the X schema")
2. Soft-delete policy
3. Pagination rules
4. Concurrency handling
5. Audit/logging requirements
6. Content versioning rules
7. Processing order invariants
8. Frontend type-safety rules
9. Auth model
10. Error handling standards
-->

{{CRITICAL_ARCH_RULES}}

---

## Code Standards

### Backend

<!-- Replace with YOUR backend standards. Keep the structure. -->

{{CODE_STANDARDS_BACKEND}}

### Error Handling

- Every API endpoint should have try/except with meaningful error messages
- Return proper HTTP status codes: 400 for bad input, 404 for not found, 409 for concurrency conflict, 500 for server errors
- Never expose raw stack traces in the API response — log them, return a clean message

### Testing

- Write tests alongside code, not as an afterthought
- Test files go in `tests/` mirroring the app structure
- Use synthetic data in all tests
- Maintain coverage above 80%. Do not edit code to pass tests — perfect functionality is the goal.

### Frontend

<!-- Replace with YOUR frontend standards. Keep the structure. -->

{{CODE_STANDARDS_FRONTEND}}

---

## Session Practices

### Build Priorities

- `docs/ARCH_BUILD_STEPS.md` is the **authoritative source** for phase order, step decomposition, and per-step context loading.
- `.github/IMPLEMENTATION_PLAYBOOK.md` is a non-authoritative operator's guide — conflicts are resolved in favor of `ARCH_BUILD_STEPS.md`.

### During a Session

- Before creating a new file, check if it already exists — don't overwrite previous work
- Before editing a file, read it first to understand current state
- When making changes that affect multiple files, list all the files that need to change before starting
- If a task is large (more than ~5 files), break it into steps and confirm the plan before writing code

### Explaining Things

- Use plain language when explaining technical concepts or tradeoffs
- Do not assume knowledge of technical acronyms unless defined in PROJECT_CONTEXT.md
- When there is a choice to make, present the options with pros/cons and let the user decide
- When something could go wrong or has a risk, say so proactively

### What Never Goes in the Repo

- Actual production data or PII
- Real names, addresses, or deal-specific terms
- Passwords, secrets, connection strings, API keys, tokens
- Large binary files (unless small and necessary)
- Personal notes, meeting minutes, or internal communications

---

## Technology Stack (quick reference)

<!-- Replace with YOUR tech stack table -->

| Layer | Technology |
|-------|------------|
| API | {{TECH_STACK_BACKEND}} |
| ORM | {{TECH_STACK_ORM}} |
| Migrations | {{TECH_STACK_MIGRATIONS}} |
| Database | {{TECH_STACK_DB}} |
| Frontend | {{TECH_STACK_FRONTEND}} |
| Auth | {{TECH_STACK_AUTH}} |
| Hosting | {{TECH_STACK_HOSTING}} |

---

## Environment Setup

<!-- Replace with YOUR environment setup -->

### Local `.env` file (never committed)

```env
{{ENVIRONMENT_SETUP}}
```

### Running locally

```bash
# API
# {{your backend run command}}

# Frontend (separate terminal)
# {{your frontend run command}}
```

### Database migrations

```bash
# {{your migration commands}}
```

---

## Project Structure (quick reference)

<!-- Replace with YOUR project structure -->

```
{{PROJECT_STRUCTURE}}
```

---

## Key Concepts (quick reference)

<!-- Replace with YOUR domain concepts -->

{{DOMAIN_CONCEPTS}}

---

## Full Context

Everything else — full data model, all API endpoints, engine detail, frontend architecture, test plan — is in **`PROJECT_CONTEXT.md`**.
