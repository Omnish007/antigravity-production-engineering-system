# Naming Rules

Recommended activation: **Glob**.

## General

Names should communicate domain intent, not implementation trivia. Prefer complete, searchable names over clever abbreviations.

## TypeScript / React

- Components: `PascalCase`.
- Hooks: `useSomething`.
- Functions/variables: `camelCase`.
- Types/interfaces: domain-specific `PascalCase`.
- Boolean values: use names such as `isOpen`, `hasAccess`, `canEdit`, `shouldRetry`.
- Constants: use `UPPER_SNAKE_CASE` only for true module-level constants where that improves clarity; otherwise normal `camelCase` is acceptable.

## Files

Prefer names that match the exported responsibility, for example:

```text
user.service.ts
user.controller.ts
user.schema.ts
use-user.tsx
user-card.tsx
```

Keep the repository's established file naming convention once chosen. Do not rename broad areas for stylistic preference.

## APIs

Use nouns for resources and explicit action names only when the operation is not naturally represented by a resource action. Use consistent casing and path conventions throughout the project.

## MongoDB

Use stable, domain-oriented collection/model names and consistent field names. Keep timestamps predictable (`createdAt`, `updatedAt`) unless the project has a justified alternative.

## Git

Use consistent branch prefixes and concise Conventional Commit-compatible messages when the repository adopts Conventional Commits.

## Naming review

Before adding a name, search for existing analogous names. Prefer consistency with adjacent code over inventing a theoretically cleaner convention.
