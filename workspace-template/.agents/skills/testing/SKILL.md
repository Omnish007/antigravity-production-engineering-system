---
name: testing
id: SKILL-TEST-001
description: Plan, design, and execute impact-aware unit, integration, API, contract, and E2E tests across any language and framework.
---

# Testing Skill

<MISSION>
Plan, design, and execute impact-aware unit, integration, API, contract, and E2E tests across any language and framework.
</MISSION>

<WHEN_TO_USE>
Activate this skill when executing tasks requiring testing capabilities, workflows, or architectural guidance.
</WHEN_TO_USE>

<PRECONDITIONS>
### Prerequisites
- The current governed task record `.agents/state/tasks/TASK-ID.json` must be `IN_PROGRESS`.
- A `TASK_STARTED` event must be recorded in `.agents/state/events/TASK-ID.jsonl`.

### Pre-flight Checklist
- [ ] Test surface and affected code paths identified
- [ ] Test tooling and test runner detected from repository evidence
- [ ] Existing test conventions and strategy understood
</PRECONDITIONS>

<NON_NEGOTIABLES>
- Every behavior change requires proportionate verification: automated tests are required for domain logic, APIs, and data integrity; manual or visual verification is acceptable for pure documentation, visual styling, or configuration changes where automated testing is impractical.
- Tests must be deterministic, hermetic, and independent (zero arbitrary sleep calls; use explicit polling or event listeners).
- All applicable tests must pass with exit code 0 before task completion.
</NON_NEGOTIABLES>

<PROCEDURE>
## Test selection and impact analysis

Before running tests, determine the exact scope of affected behavior:

- Which files and modules were modified?
- Which downstream components or services depend on them?
- Did API request/response contracts change?
- Did database schemas, queries, or data state change?
- Were authentication or authorization boundaries touched?
- Which critical user journeys or business workflows are impacted?

## Ecosystem test toolchains

Always use the test runner and assertion libraries configured in the repository:

| Ecosystem | Unit & Integration | HTTP / API Integration | Browser / E2E |
|---|---|---|---|
| **TypeScript / JS** | Vitest, Jest | Supertest, node-mocks-http | Playwright, Cypress |
| **Python** | `pytest`, `unittest` | `httpx`, FastAPI `TestClient` | Playwright Python |
| **Go** | `go test`, `testify` | `httptest` | Playwright Go |
| **Rust** | `cargo test`, `tokio::test` | `reqwest`, `wiremock` | Playwright |
| **Java / Kotlin** | JUnit 5, AssertJ, Mockito | MockMvc, TestRestTemplate, Testcontainers | Playwright Java, Selenium |
| **C# / .NET** | xUnit, NUnit, FluentAssertions | WebApplicationFactory, WireMock.Net | Playwright .NET |

## Test levels and responsibilities

### Unit tests
- Test individual functions, pure domain logic, value objects, calculations, and data mappers in isolation.
- Keep unit tests fast, in-memory, and free of external network or database calls.

### Integration tests
- Verify interactions between collaborators: service to repository, database transactions, cache operations, and message queue publishing.
- Use lightweight local instances or containerized dependencies (e.g., Testcontainers) rather than mocking database drivers.

### API & Contract tests
- Verify request validation, HTTP status codes, response schemas, authentication, authorization, and error envelopes.
- Verify contract compatibility between services (e.g., consumer-driven contracts or OpenAPI validation).

### End-to-End (E2E) tests
- Exercise critical user journeys across real system boundaries.
- Use user-facing locators (roles, text, accessible names) and web-first assertions; avoid brittle implementation selectors (CSS paths, auto-generated class names).

## Test design best practices

- **Deterministic test data**: Use explicit fixtures, object factories, or builders. Avoid random test data unless property-based or fuzz testing.
- **Test isolation**: Every test must run independently. Clean up created data (transactions rolled back, test databases wiped) after runs.
- **Mock at stable boundaries**: Mock third-party external services (payment gateways, external SMS/email APIs) at stable interface boundaries; avoid mocking internal domain logic.
- **Test negative & boundary conditions**: Test invalid inputs, unauthorized actors, timeouts, empty collections, and race conditions, not just the happy path.

## Completion

Report the exact test commands executed, number of passed/failed tests, and diagnostic output for any failures. Never claim "all tests passed" without running the test suite and producing concrete evidence.
</PROCEDURE>

<VERIFICATION_POLICY>
### Exit Criteria
Test suite passes with 100% exit code 0 and coverage for changed code.
</VERIFICATION_POLICY>

<DELIVERABLES>
- Comprehensive test suites (unit, integration, E2E) with high coverage of critical paths and edge cases.
- Verification test reports and coverage evidence.
</DELIVERABLES>
