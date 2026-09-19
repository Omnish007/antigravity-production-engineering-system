# Testing Rules

Recommended activation: **Model Decision** for changes that can affect behavior.

## Test philosophy

Tests are executable specifications and risk controls, not a coverage contest. Select tests according to behavioral risk, dependency impact, and criticality.

## Minimum expectations

- New business logic: unit tests for important branches and failure modes.
- API changes: request validation, authorization, success, common failure, and data-state tests.
- Database changes: schema/validation tests and representative query/index verification.
- Critical user journeys: E2E coverage where practical.
- Bug fixes: regression test for the original failure whenever feasible.
- Security-sensitive changes: security-focused positive and negative tests.

## Test tools

The default toolchain may use:

- Vitest for unit/integration-level JavaScript/TypeScript tests when compatible with the repository;
- React Testing Library for user-oriented React behavior;
- Supertest or equivalent for Express HTTP integration tests;
- Playwright for browser E2E.

The installed repository configuration is authoritative. Do not replace an established runner merely for stylistic preference.

## Test design

Prefer behavior-focused assertions over implementation-detail assertions. Use deterministic fixtures and factories. Keep tests isolated, repeatable, and independent.

For Playwright, prefer user-facing locators and web-first assertions rather than fragile CSS selectors or manual visibility checks.

## Graduated verification

1. Focused tests for changed behavior.
2. Related integration/API tests.
3. Broader suite for cross-cutting, auth, dependency, or architecture changes.
4. E2E for critical workflows or UI behavior.
5. Build/type/lint checks as configured by the repo.

## Coverage

Use repository-configured thresholds where they exist. When no threshold exists, do not invent a single universal percentage; evaluate whether meaningful branches, failure modes, security properties, and critical workflows are covered.
