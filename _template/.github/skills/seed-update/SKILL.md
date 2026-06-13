# Skill: Seed Update

After data model changes, keep synthetic seed/delete scripts in sync.

## When to use

When new models or columns are added that need synthetic test data.

## Checklist

### 1. Identify new entities

- [ ] List all new models added in this step
- [ ] List any models with new columns that affect seeding

### 2. Update seed script

<!-- Replace with your actual seed script path -->

File: `scripts/seed_synthetic.py` (or equivalent)

- [ ] Add creation logic for new entities
- [ ] Respect creation order (parent records before children with FKs)
- [ ] Use synthetic/fake data only — no real data
- [ ] New records connect to existing seed data via foreign keys

### 3. Update delete script

File: `scripts/delete_synthetic.py` (or equivalent)

- [ ] Add deletion logic for new entities
- [ ] Respect deletion order (reverse of creation — children before parents)
- [ ] Use soft-delete if that's the project convention

### 4. Full-cycle test

```bash
# Run seed script:
# {{your seed command}}

# Verify data exists:
# {{your verification command or API call}}

# Run delete script:
# {{your delete command}}

# Verify data is gone/deactivated:
# {{your verification command}}
```

### 5. Run endpoint tests

- [ ] Run full test suite to confirm seed data doesn't break existing tests

## Lessons Learned

<!-- Add seed-related mistakes you've encountered. Example:
- Step X: Forgot to add FK reference, got integrity error.
  Fix: Always create parent records first.
-->
