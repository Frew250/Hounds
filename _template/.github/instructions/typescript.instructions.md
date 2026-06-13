---
applyTo: "**/*.{ts,tsx}"
---

# TypeScript & React Conventions

## General

<!-- Adjust versions and preferences to match your project -->

- TypeScript strict mode. Explicit return types on all exported functions and components.
- Use `interface` for object shapes, `type` for unions and intersections.
- No `any` types.

## Components

- Functional components only. No class components.
- Props interfaces defined in the component file unless shared.
- Handle `isLoading`, `isError`, `error` states in UI. No silent failures.

## Styling

<!-- Adapt to your styling approach (Tailwind, CSS Modules, styled-components, etc.) -->

- Use utility classes exclusively (if Tailwind).
- All colors, fonts, and spacing reference the design system — no hardcoded hex values.

## Data Fetching

<!-- Adapt to your data fetching approach (TanStack Query, SWR, RTK Query, etc.) -->

- Custom hooks for all server state.
- Always handle loading, error, and empty states in the UI.
- Mutations should invalidate related queries on success.

## State Management

- Server state: query library (not local state, not context).
- UI state: React `useState` or `useReducer`.
- Global UI state: React Context.

## Pages

- One page per route.
- All routes defined in a central router file.

## UX Requirements

- Every destructive action has a confirmation dialog.
- Every list has a designed empty state.
- Every form with unsaved changes has a navigation guard.
- Loading: skeleton loaders for page loads, spinner for buttons.

## Project-Specific Conventions (Observed)

<!-- Fill this section in as you build patterns. Examples:

### Theme Tokens
- Custom color groups: ...
- Font families: ...

### Router Pattern
- Manual routing via createBrowserRouter
- Layout shells: ...
- Access control: ...

### API Client Pattern
- All API calls through a shared client
- Shared request<T> wrapper

### Query Hook Pattern
- Hook files per entity domain
- Query key style: string-first arrays in kebab-case
-->
