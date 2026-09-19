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
- Performance-sensitive changes: baseline measurement and post-change comparison.
- Accessibility-impacting UI: automated accessibility checks (axe-core, Pa11y, or equivalent).

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

## Additional test strategies

### Contract testing

When services communicate across boundaries (frontend-backend, microservice-microservice), consider contract tests that verify the agreed-upon request/response schemas remain compatible independently of full integration tests.

### Snapshot testing

Use snapshot tests for UI components when visual regression detection is valuable. Review snapshot changes deliberately; do not update snapshots blindly.

### Performance testing

For performance-sensitive work, establish baseline metrics and compare after changes. Use representative data volumes and realistic concurrency. See `.agents/skills/performance/SKILL.md`.

### Accessibility testing

Integrate automated accessibility scanning (axe-core, Pa11y) into the test pipeline for UI work. Automated tools catch a subset of issues; supplement with manual keyboard and screen-reader testing for critical workflows.

### Mutation testing

When test confidence matters (critical business logic, security controls), consider mutation testing to verify that tests detect meaningful code changes. Use judiciously; mutation testing is expensive and most valuable for high-risk modules.

## Graduated verification

1. Focused tests for changed behavior.
2. Related integration/API tests.
3. Broader suite for cross-cutting, auth, dependency, or architecture changes.
4. E2E for critical workflows or UI behavior.
5. Build/type/lint checks as configured by the repo.

## Coverage

Use repository-configured thresholds where they exist. When no threshold exists, do not invent a single universal percentage; evaluate whether meaningful branches, failure modes, security properties, and critical workflows are covered.
