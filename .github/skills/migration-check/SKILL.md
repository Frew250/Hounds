# Skill: Migration Check

After model changes, verify the database migration is correct.

## When to use

After adding or modifying ORM models.

## Checklist

### 1. Pre-generation

- [ ] Verify the migration scope filter (e.g., `include_object` in Alembic) is in place
- [ ] This prevents the migration tool from detecting tables outside your schema

### 2. Generate

```bash
# {{your migration generate command}}
# Example: alembic revision --autogenerate -m "Add FieldName to TableName"
```

### 3. Review the generated migration

- [ ] Only expected tables/columns appear in the upgrade
- [ ] No unexpected DROP TABLE or DROP COLUMN
- [ ] Column types are correct for your database dialect
- [ ] Foreign key references are correct and schema-qualified (if using schema namespacing)
- [ ] Index names don't exceed your database's length limits

### 4. Test the up/down cycle

```bash
# {{your up command}}
# {{your down command}}
# {{your up command again}}
```

- [ ] Up succeeds
- [ ] Down succeeds without errors
- [ ] Second up succeeds (proves down was complete)

### 5. Dialect-specific checks

<!-- If you support multiple database dialects (e.g., SQLite for dev, PostgreSQL for prod),
     note any differences here. Example:

SQLite limitations:
- No ALTER TABLE ... DROP COLUMN (before SQLite 3.35)
- No schema namespacing
- `batch_alter_table` may be needed for column changes

PostgreSQL/SQL Server differences:
- Schema-qualified table names
- Different date/time types
-->

## Lessons Learned

<!-- Add migration mistakes you've encountered and their fixes.
     This section grows as you build. Example:

- Step X: Migration tried to drop external tables.
  Fix: Added include_object filter to env.py
-->
