---
name: backend
id: SKILL-BACKEND-001
description: Implement production-grade backend modules across any runtime and framework with explicit layered boundaries, schema validation, authorization, error handling, resilience, and observability.
---

# Backend Development Skill

<MISSION>
Implement production-grade backend modules across any runtime and framework with explicit layered boundaries, schema validation, authorization, error handling, resilience, and observability.
</MISSION>

<WHEN_TO_USE>
Activate this skill when executing tasks requiring backend capabilities, workflows, or architectural guidance.
</WHEN_TO_USE>

<PRECONDITIONS>
### Prerequisites
- Active task in .agents/state/tasks.json must be IN_PROGRESS.
    - TASK_STARTED event must be recorded in .agents/state/events.jsonl.
    - Must consult `.agents/state/stack.json` and load the matching profile from `.agents/technology/profiles/backend/` and language profile from `.agents/technology/profiles/language/`.
    - Must be loaded as part of the Atomic Backend Bundle alongside `.agents/skills/api/SKILL.md`, `.agents/skills/security/SKILL.md`, and `.agents/rules/07-security.md`.

### Pre-flight Checklist
- [ ] Active backend and language profiles loaded from `.agents/technology/profiles/`
- [ ] 4-Layer directory structure verified (routes, controllers, services, repositories, dtos)
- [ ] Architectural constraints loaded: no DB queries in routes/controllers, no HTTP objects in services
- [ ] Worker concurrency bounded
- [ ] Graceful shutdown and signal traps verified
- [ ] Idempotency key checked before execution
- [ ] Error handling and retry backoff configured
</PRECONDITIONS>

<NON_NEGOTIABLES>
- Strict adherence to RULE-ARCH-LAYER-001 (15-layered-architecture.md). Any inline DB query in routes or controllers is an automatic task failure.
- Decouple long-running background workers from HTTP request cycles.
- Enforce graceful shutdown on SIGTERM and SIGINT with connection draining.
- All external operations must have explicit timeouts and cancellation tokens.
- Mutating jobs must enforce idempotency keys to prevent duplicate processing.
- If meeting the Canonical ADR Trigger (Type 1 Reversibility OR any two of: D1 Blast Radius, D3 Trade-offs, D4 Non-Functional Impact), an ADR MUST be authored in `docs/decisions/` and `.agents/skills/architecture/SKILL.md` must be read before implementation.
</NON_NEGOTIABLES>

<PROCEDURE>
## Architecture and structure

Organize backend capabilities around distinct domain boundaries and explicit layers:

```text
feature/
  handler/controller   -> Transport adapter (HTTP, gRPC, event handler)
  service/use-case     -> Business rules, domain orchestration, transactions
  repository/adapter   -> Data persistence and external service client
  schema/dto           -> Input/output validation contracts and types
  routes/endpoints     -> Route registration and middleware binding
  tests/               -> Unit, integration, and contract tests
```

Adapt directory naming and file extensions to match the active language and framework conventions.

## Request processing pipeline

Enforce the canonical processing pipeline:

```text
request -> security middleware -> validation -> authorization -> controller/handler -> service/use-case -> repository -> response
```

Keep controllers and handlers thin:
- Extract and validate parameters, headers, and request bodies.
- Delegate business rules to domain services or use-case interactors.
- Map domain results and exceptions to transport-appropriate responses.

## Framework adaptation

- **Node.js (Express, Fastify, NestJS)**: Use native async error propagation; avoid unhandled promise rejections; configure central error middleware; enforce TypeScript types across boundaries.
- **Python (FastAPI, Django, Litestar)**: Leverage Pydantic or dataclasses for request/response serialization; use dependency injection for database sessions and auth; manage async event loops cleanly.
- **Go (net/http, Gin, Echo, Chi)**: Use standard `context.Context` for cancellation and timeouts; return explicit errors up the call stack; keep interfaces on the consumer side.
- **Rust (Axum, Actix)**: Leverage type-safe extractors; model errors with custom enums implementing `IntoResponse`; manage state with thread-safe wrappers (`Arc`).
- **Java / Kotlin (Spring Boot, Quarkus)**: Use controller-service-repository pattern; leverage Bean Validation (`@Valid`); handle exceptions with central `@ControllerAdvice`.
- **C# (.NET / ASP.NET Core)**: Use Minimal APIs or Controllers; enforce FluentValidation; leverage built-in dependency injection; use MediatR or direct service injection.

## Validation

- Validate all incoming data (path parameters, query strings, headers, payloads) against explicit schemas before execution.
- Reject unknown or unauthorized fields to prevent mass-assignment vulnerabilities.
- Return structured, machine-readable validation errors indicating the exact path and failure reason.

## Authorization

- Perform authorization server-side on every request.
- Authorize both the action and the specific resource instance (object-level and property-level).
- Never trust client-supplied tenant, role, or user identifiers. Derive actor identity from verified authentication tokens or sessions.

## Operational resilience

### Structured logging & tracing
- Format logs as structured JSON with standard fields: `timestamp`, `level`, `requestId` (correlation ID), `userId`, `action`, `durationMs`, and `error`.
- Propagate correlation IDs across downstream HTTP calls, database queries, and message queues.

### Circuit breakers
- Wrap external dependencies with circuit breakers to prevent cascading failures.
- Configure failure thresholds, timeout limits, and half-open test recovery states.
- Provide graceful degradation or cached fallbacks when circuits are open.

### Rate limiting & concurrency
- Protect public, authentication, and expensive endpoints with rate limiters (token bucket, sliding window).
- Return HTTP 429 with `Retry-After` headers when limits are exceeded.
- Implement concurrency limits (bulkheads) on resource-intensive operations to preserve service stability.

### Background jobs and queues
- Offload non-blocking or long-running work to asynchronous queues.
- Ensure job handlers are idempotent (safe to retry upon failure).
- Implement dead-letter queues (DLQ) with monitoring for permanently failed jobs.
- Set strict execution timeouts on queue consumers.

### Graceful shutdown
- Listen for termination signals (`SIGTERM`, `SIGINT`).
- Stop accepting new requests immediately.
- Allow in-flight requests to complete within a bounded grace period (e.g., 10-30s).
- Cleanly close database connections, queue listeners, and external sockets before process exit.
</PROCEDURE>

<VERIFICATION_POLICY>
## Verification

Every backend change requires verification covering:
- Happy-path execution and expected response payloads;
- Input validation failure handling (HTTP 400 / unprocessable entity);
- Authentication (HTTP 401) and authorization (HTTP 403) enforcement;
- Resource not found (HTTP 404) and conflict states (HTTP 409);
- Error propagation and boundary masking (no leaked stack traces);
- Database persistence side effects and transactional rollback;
- Architecture Verification: Must execute `.agents/validation/check-architecture.py` before declaring completion. Zero violations allowed.

### Exit Criteria
Backend service builds cleanly and passes concurrency/stress tests.
</VERIFICATION_POLICY>

<DELIVERABLES>
- Implemented and verified backend services, models, and endpoints.
- Passing backend test suite with verification evidence logged in task artifacts.
</DELIVERABLES>
