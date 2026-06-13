# Skill: New Hook

Scaffold a new data-fetching hook file following this project's exact patterns.

## When to use

When adding API integration for a new entity.

## How to fill this in

1. Build your first hook file manually.
2. Once it's working, paste it below as the reference pattern.

---

## Reference Hook Pattern

<!-- Paste a COMPLETE working hook file here. Include:
     - Query hooks (list, detail)
     - Mutation hooks (create, update, delete/deactivate)
     - Query key conventions
     - Invalidation strategy
     - Type imports
-->

```tsx
// PASTE YOUR HOOK PATTERN HERE
```

## API Client Pattern

<!-- Paste your API client's request functions if they follow a pattern -->

```tsx
// PASTE YOUR API CLIENT PATTERN HERE
```

## Conventions

<!-- Document when you have them:
     - Query key naming (e.g., kebab-case string-first arrays)
     - Pagination support pattern
     - Error handling in mutations
     - Optimistic updates (if used)
-->

## Checklist (for the agent)

- [ ] Create hook file in the correct directory
- [ ] Import types from types directory
- [ ] Follow query key naming conventions
- [ ] List query with pagination support (if top-level)
- [ ] Detail query with `enabled` guard on ID
- [ ] Create mutation with success invalidation
- [ ] Update mutation with success invalidation
- [ ] Deactivate/delete mutation (if applicable)
