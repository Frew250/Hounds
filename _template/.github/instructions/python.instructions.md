---
applyTo: "**/*.py"
---

# Python Conventions

## General

<!-- Adjust the Python version and syntax preferences to match your project -->

- Python 3.12+. Use modern syntax (type unions with `|`, `match` where appropriate).
- Type hints on ALL function signatures — parameters and return types.
- Docstrings only when behavior isn't obvious from name and signature.
- Never add comments that restate what the code does. Comments explain WHY, not WHAT.

## ORM Models

<!-- Adapt to your ORM (SQLAlchemy, Django ORM, Tortoise, etc.) -->

- One model per file.
- All tables use the dedicated SQL schema in `__table_args__` (if using schema namespacing).
- Never hard-delete records. Use soft deletes (e.g., `is_active = False`).
- Primary resource PUT endpoints check `updated_at` for optimistic concurrency → return 409 Conflict if stale.
- All models include `created_at` and `updated_at` timestamp columns.

## API Schemas

<!-- Adapt to your schema library (Pydantic, Marshmallow, etc.) -->

- Request schemas: only fields the client sends. No `id`, `created_at`, `updated_at`.
- Response schemas: include `id`, timestamps, and any computed/derived fields.
- Use validation constraints where appropriate.

## API Routers

<!-- Adapt to your framework (FastAPI, Flask, Django, etc.) -->

- Use dependency injection for database sessions.
- Top-level list endpoints are paginated. Nested resources return plain arrays.
- Return appropriate HTTP status codes: 201 create, 200 update/get, 404 not found, 409 concurrency conflict.

## Error Handling

- Let unexpected errors propagate to the global error handler. Do not wrap every database call in try/except.
- Only catch specific, expected exceptions.
- Error messages must be specific and helpful.

## Testing

- Test file mirrors the module it tests.
- Test names describe the scenario.
- Cover happy path AND at least one error/edge case per function.

## Project-Specific Conventions (Observed)

<!-- Fill this section in as you build patterns. Examples:

### Import Ordering
- stdlib → third-party → local imports. One blank line between groups.

### Model Baseline
- Primary keys: UUIDs via `default=uuid.uuid4`
- Foreign keys: schema-qualified `ForeignKey("{{SCHEMA_NAME}}.table_name.id")`

### DB Dependency
- Endpoints use `session: AsyncSession = Depends(get_session)`

### Pagination
- page/page_size query params with PaginatedResponse[T] wrapper
-->
