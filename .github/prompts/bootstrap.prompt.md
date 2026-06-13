---
mode: agent
description: "Bootstrap a new project from this workflow template — interactive interview that fills in all placeholders."
---

@Plan-Review

I'm setting up this workflow template for a new project. Interview me to fill in all the `{{PLACEHOLDER}}` values, then generate the filled-in files.

## Step 1: Project basics

Ask me:
1. What is the project name? (display name)
2. What is the project slug? (lowercase-hyphenated, e.g., "my-project")
3. Describe the project in one sentence.
4. What is the build-track branch name? (e.g., "feat/application-buildout" or "develop")

## Step 2: Tech stack

Ask me:
1. Backend framework + language (e.g., "FastAPI, Python 3.12+, Pydantic v2")
2. Frontend framework (e.g., "React 18, TypeScript, Vite, Tailwind CSS")
3. ORM / data access (e.g., "SQLAlchemy 2.0 async")
4. Database (e.g., "PostgreSQL 16")
5. Migration tool (e.g., "Alembic")
6. Auth mechanism (e.g., "JWT with OAuth2")
7. Hosting/deployment target (e.g., "AWS ECS + S3")

## Step 3: Database conventions

Ask me:
1. Do you use a named SQL schema? If so, what? (e.g., "app", "public", or none)
2. Do you use a storage prefix? (e.g., "myapp-", or none)

## Step 4: Architecture rules

Ask me to list my project's critical architecture rules — the hard invariants every agent must respect. Give me examples from the placeholder to help me understand the format.

## Step 5: Domain concepts

Ask me to list 5-15 key domain terms with one-line definitions.

## Step 6: File structure

Ask me about my project's file structure, or offer to auto-detect it from the workspace.

## Step 7: Generate

Once I've answered everything:
1. Search for all `{{PLACEHOLDER}}` occurrences across all template files
2. Replace them with my answers
3. Generate the filled-in `CLAUDE.md` and `copilot-instructions.md` with my content
4. Report what was filled in and what still needs manual attention
