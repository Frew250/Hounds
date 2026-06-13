# Template Customization Reference

Every `{{PLACEHOLDER}}` in this template needs to be replaced with your project's values. Use `/bootstrap` for an interactive fill-in, or search and replace manually.

## Core Placeholders

| Placeholder | Description | Example (from original project) |
|---|---|---|
| `{{PROJECT_NAME}}` | Display name | e.g., Acme Invoice Manager |
| `{{PROJECT_SLUG}}` | Lowercase hyphenated slug | e.g., acme-invoice-manager |
| `{{PROJECT_DESCRIPTION}}` | One-sentence summary | e.g., Automated invoice processing for accounts payable |
| `{{BUILD_TRACK_BRANCH}}` | Long-running integration branch name | `feat/application-buildout` |

## Tech Stack

| Placeholder | Description | Example |
|---|---|---|
| `{{TECH_STACK_BACKEND}}` | Backend framework + language | e.g., FastAPI + Python 3.12, or Express + Node 20 |
| `{{TECH_STACK_FRONTEND}}` | Frontend framework | e.g., React 18 + TypeScript + Vite |
| `{{TECH_STACK_DB}}` | Database | e.g., PostgreSQL 16 |
| `{{TECH_STACK_ORM}}` | ORM / data access | e.g., SQLAlchemy 2.0, Prisma, Drizzle |
| `{{TECH_STACK_MIGRATIONS}}` | Migration tool | e.g., Alembic, Prisma Migrate, Knex |
| `{{TECH_STACK_HOSTING}}` | Deployment target | e.g., AWS ECS, Cloud Run, Vercel |
| `{{TECH_STACK_AUTH}}` | Auth mechanism | e.g., JWT + OAuth 2.0, NextAuth, Clerk |
| `{{TECH_STACK_EDITOR}}` | Rich text editor (if applicable) | e.g., Lexical, TipTap, ProseMirror (omit if N/A) |

## Database

| Placeholder | Description | Example |
|---|---|---|
| `{{SCHEMA_NAME}}` | SQL schema namespace (if applicable) | e.g., `app`, `public`, or none |
| `{{BLOB_PREFIX}}` | Storage prefix (if applicable) | e.g., `myapp-`, or none |

## Content Sections (fill with your own)

These are larger blocks that replace entire sections. Write them for YOUR project.

| Placeholder | Where Used | What to Write |
|---|---|---|
| `{{CRITICAL_ARCH_RULES}}` | `CLAUDE.md` | Numbered list of your project's hard architecture rules (e.g., "all tables use X schema", "never hard-delete", "all list endpoints are paginated") |
| `{{CODE_REVIEW_RULES}}` | `copilot-instructions.md` | First ~4000 chars: database rules, API rules, engine rules, frontend rules, general rules. This is what Copilot PR code review reads. |
| `{{DOMAIN_CONCEPTS}}` | `CLAUDE.md` | Key terms table: Term → Definition. Domain-specific vocabulary for the agents. |
| `{{FILE_LOCATIONS}}` | `copilot-instructions.md`, `CLAUDE.md` | Table mapping categories to paths (Models → app/models/, Tests → tests/, etc.) |
| `{{PROJECT_STRUCTURE}}` | `CLAUDE.md` | ASCII tree of your project's folder structure with descriptions |
| `{{MANDATORY_ROUTING}}` | `copilot-instructions.md` | Table of work types that require specific agent scrutiny |
| `{{ENVIRONMENT_SETUP}}` | `CLAUDE.md` | Local .env variables, run commands, database setup |
| `{{CODE_STANDARDS_BACKEND}}` | `CLAUDE.md` | Python/backend specific standards |
| `{{CODE_STANDARDS_FRONTEND}}` | `CLAUDE.md` | TypeScript/React specific standards |
| `{{COMPONENT_CHECKLISTS}}` | `component-checklists.md` | Planning requirements, edge cases, and research prompts for your critical components |

## Model Preferences

These appear in agent YAML frontmatter. Adjust to your available models:

| Role | Default | Purpose |
|---|---|---|
| High-reasoning primary | Claude Opus 4.6 | Planning, implementation, design |
| Cross-model diversity | GPT-5.4 | Review, critique, dreaming (different model = different blindspots) |
| Fast mechanical | Grok code fast 1 | Git ops, file moves, test runs |

## After Customization

1. Delete `CUSTOMIZE.md` and `PLAN.md` from the template folder (they're scaffolding)
2. Move the `.github/` contents to your project's `.github/`
3. Move `CLAUDE.md` to your project root
4. Move `scripts/` to your project root
5. Create your `docs/ARCH_BUILD_STEPS.md` with your phased build plan
6. Create your architecture docs
7. Run `/newstep` to start your first build step, or `/autostep` for a coordinated run on a well-scoped step
8. If you use Design sessions, keep `examples/` in place so staged source material stays part of the workflow
