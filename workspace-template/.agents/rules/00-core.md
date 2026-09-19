# Core Engineering Rules

Recommended activation: **Always On**

## Purpose

Define non-negotiable engineering behavior for all meaningful changes.

## Before editing

- Inspect the repository tree relevant to the task.
- Read `docs/INDEX.md`, `docs/PROJECT_CONTEXT.md`, and `docs/CURRENT_STATE.md`.
- Read architecture and conventions when the task touches structure or established behavior.
- Check the working tree before modifying files when Git is present.
- Identify exact acceptance criteria and affected boundaries.

## Implementation principles

- Prefer simple, explicit, maintainable designs.
- Preserve domain boundaries and dependency direction.
- Reuse existing abstractions when they are correct; do not create duplicate helpers.
- Keep business logic out of UI markup and transport handlers when it belongs in domain/service code.
- Keep validation close to trust boundaries and enforce it server-side.
- Keep side effects explicit and isolated.
- Fail safely and return actionable errors without leaking secrets or internals.
- Design for cancellation, timeouts, retries, and idempotency when external operations are involved.
- Avoid hidden global state.
- Avoid premature optimization; measure before introducing complexity for performance.

## Dependency discipline

Before adding a dependency, determine:

- whether the repository already has an equivalent capability;
- whether the package supports the installed Node/Next/React versions;
- maintenance/health signals;
- security implications;
- bundle/runtime cost;
- whether the dependency creates architectural lock-in.

Record material new dependencies in project conventions or an ADR when appropriate.

## Error handling

Errors must be:

- represented with types/classes or stable error codes where useful;
- mapped to user-safe messages at the boundary;
- logged with sufficient diagnostic metadata but without secrets or sensitive payloads;
- distinguishable between client, domain, infrastructure, and unexpected failure classes.

Never use `catch {}` to silently discard a meaningful failure.

## Completion

Do not mark work complete until verification and memory synchronization have been considered. A clean build is evidence of build correctness, not proof that product behavior is correct.
