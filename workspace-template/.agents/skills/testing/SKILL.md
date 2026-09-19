---
name: testing
description: Run impact-aware unit, integration, API, and E2E testing and select the smallest test set that provides sufficient behavioral confidence.
---

# Testing Skill

## Test selection

Determine:

- what files/modules changed;
- which consumers depend on them;
- whether API contracts changed;
- whether data state changes;
- whether auth/security boundaries changed;
- which critical user journeys are affected.

## Default tool choices

Use the repository's configured tools. A modern default may be:

- Vitest for TypeScript unit/integration tests;
- React Testing Library for React behavior;
- Supertest for Express HTTP integration;
- Playwright for browser E2E.

## Test levels

### Unit

Use for pure functions, domain rules, mappers, validators, and isolated service behavior.

### Integration

Use for service/repository interactions, database invariants, and cross-module behavior.

### API

Verify request/response contracts, authentication, authorization, validation, error semantics, idempotency, and persistence effects.

### E2E

Verify the smallest set of high-value user journeys across the real browser boundary.

## Test design

- Prefer deterministic fixtures/factories.
- Avoid shared mutable state.
- Mock external systems at a stable boundary when a real dependency is not the subject under test.
- Use realistic integration tests where the integration itself is the risk.
- Test failure and boundary conditions, not only the happy path.

For Playwright, prefer user-facing locators and web-first assertions.

## Completion

Report exact commands run and the resulting pass/fail state. Do not claim "all tests passed" when only a focused subset was executed.
