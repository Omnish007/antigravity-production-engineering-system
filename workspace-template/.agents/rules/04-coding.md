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

## Anti-patterns

Do not:

- add duplicate abstractions;
- suppress type errors without a documented reason;
- catch and ignore exceptions;
- hardcode environment-specific URLs or secrets;
- put database calls directly into presentational components;
- create generic abstractions before a concrete repeated need exists.
