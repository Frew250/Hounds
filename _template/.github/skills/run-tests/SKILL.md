# Skill: Run Tests

Run the project test suite and diagnose failures.

## When to use

When running backend tests, frontend tests, or both.

## Backend Tests

```bash
# Run all backend tests:
# {{your test command, e.g.: python -m pytest tests/ -v}}

# Run a specific test file:
# {{e.g.: python -m pytest tests/test_routers.py -v}}

# Run with coverage:
# {{e.g.: python -m pytest tests/ --cov=app --cov-report=term-missing}}
```

## Frontend Tests

```bash
# Run all frontend tests:
# {{your test command, e.g.: cd frontend && npx vitest run}}

# Run a specific test file:
# {{e.g.: cd frontend && npx vitest run src/components/MyComponent.test.tsx}}
```

## Common Failure Patterns

<!-- Fill in as you discover them. Examples:

### Import error in test
**Cause:** New model/router not registered in __init__.py
**Fix:** Add the import to the registration file

### Database schema error
**Cause:** Migration not applied, or schema name mismatch in test environment
**Fix:** Run migrations, check test database configuration

### Type error in test
**Cause:** Schema change not reflected in test fixtures
**Fix:** Update test data to match new schema
-->

## Test Environment Notes

<!-- Document your test environment setup:
     - Test database configuration (SQLite in-memory, separate test DB, etc.)
     - Environment variables needed for tests
     - Fixtures and conftest.py patterns
-->
