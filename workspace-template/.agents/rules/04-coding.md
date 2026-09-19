# Coding Rules

Recommended activation: **Glob** for `**/*.{ts,tsx,js,jsx}` and other application source patterns.

## TypeScript

- Prefer strict TypeScript configuration.
- Avoid `any`; use precise types, generics, discriminated unions, `unknown`, or validated runtime types as appropriate.
- Model nullable and optional values explicitly.
- Prefer immutable values and pure functions when practical.
- Narrow `unknown` at boundaries before use.
- Keep public functions and module APIs strongly typed.

## Functions and modules

- Keep functions small enough to reason about, but do not split code mechanically.
- Separate pure transformation from I/O and side effects.
- Give business operations explicit names rather than generic names such as `handleData`.
- Avoid deep parameter lists; use typed option objects for evolving inputs.
- Avoid cyclic imports and hidden initialization dependencies.

## Async behavior

- Propagate failures deliberately.
- Add timeouts to outbound requests where the library/runtime permits it.
- Support cancellation for long-running browser/server operations when appropriate.
- Avoid fire-and-forget promises unless ownership and failure handling are explicit.

## Comments

Comments should explain **why**, invariants, security constraints, trade-offs, or non-obvious behavior. Do not write comments that merely restate the code.

## Data handling

- Validate untrusted data before trusting it.
- Normalize only when normalization is part of the contract.
- Never log passwords, session identifiers, access tokens, refresh tokens, API keys, or raw sensitive payloads.

## Structured logging

- Use structured log formats (JSON or key-value) rather than unstructured string messages.
- Include correlation/request IDs in every log entry for cross-service tracing.
- Use consistent log levels: `error` for failures requiring attention, `warn` for degraded states, `info` for significant business events, `debug` for development diagnostics.
- Never log secrets, tokens, passwords, or raw personal data.
- Include sufficient context (user ID, resource ID, action) to diagnose issues without reproducing them.

## Resilience patterns

- **Circuit breaker**: For external dependencies, implement circuit breaker logic to prevent cascade failures. Open the circuit after repeated failures; periodically test recovery before fully closing.
- **Graceful degradation**: When a non-critical dependency fails, degrade functionality rather than failing the entire request. Communicate the degraded state to the user.
- **Timeouts**: Set explicit timeouts for all outbound calls. Never wait indefinitely.
- **Bulkhead**: Isolate resource pools for independent subsystems to prevent resource exhaustion in one area from affecting others.

## Feature flags

When introducing significant new behavior:

- wrap the feature behind a flag for gradual rollout when appropriate;
- ensure the old code path remains functional when the flag is off;
- clean up feature flags after rollout is complete and stable;
- do not leave dead feature flag branches indefinitely.

## Anti-patterns

Do not:

- add duplicate abstractions;
- suppress type errors without a documented reason;
- catch and ignore exceptions;
- hardcode environment-specific URLs or secrets;
- put database calls directly into presentational components;
- create generic abstractions before a concrete repeated need exists;
- introduce circular dependencies between modules;
- use mutable global state for request-scoped data.
