# Skill: New Model

Scaffold a new database model following this project's exact patterns.

## When to use

When adding a new database entity.

## How to fill this in

1. Build your first model manually.
2. Once it's working and migrated, paste it below as the reference pattern.
3. Include your migration workflow commands.

---

## Reference Model Pattern

<!-- Paste a COMPLETE working model file here. Include:
     - Import style
     - Base class
     - Table args (schema, constraints)
     - Column patterns (PK, timestamps, soft-delete flag)
     - Relationship patterns
-->

```python
# PASTE YOUR MODEL PATTERN HERE
```

## Model Registration

<!-- Where do new models get registered? Example:
     app/models/__init__.py — add import line -->

```python
# PASTE YOUR REGISTRATION PATTERN HERE
```

## Migration Workflow

```bash
# Generate migration after model changes:
# {{your generate command, e.g.: alembic revision --autogenerate -m "Add EntityName"}}

# Apply migration:
# {{your apply command, e.g.: alembic upgrade head}}

# Test up/down cycle:
# {{your up-down-up test commands}}
```

## Migration Checklist

- [ ] `include_object` filter (if applicable) scopes to your schema only
- [ ] New columns have correct types, nullable, defaults
- [ ] Foreign keys reference correct tables with correct column names
- [ ] Index names don't exceed database length limits
- [ ] Down migration drops what up migration creates
- [ ] Up → Down → Up cycle works without errors
