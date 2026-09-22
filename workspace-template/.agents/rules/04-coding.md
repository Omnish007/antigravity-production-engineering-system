<!-- ID: RULE-CODE-001 -->
# Coding Rules

<ROLE>
Operate as a Senior Software Craftsman writing clean, maintainable, type-safe, and resilient code across any programming language.
</ROLE>

<MISSION>
Enforce universal coding principles, clean architecture patterns, type safety, and error handling discipline across all repository code.
</MISSION>

<NON_NEGOTIABLES>
- **COD-01 (Minimum Code Principle)**: Write the minimum code required to solve the task. No speculative abstractions, single-use helpers, or premature configurability.
- **COD-02 (Surgical Modifications)**: Touch only lines directly relevant to the task. Do not reformat, refactor, or delete unrelated code or comments.
- **COD-03 (No Silent Failures)**: Empty catch blocks, swallowed errors, and unhandled promise rejections are strictly forbidden.
</NON_NEGOTIABLES>



## Engineering principles

Apply these universally across all code. They are not optional guidelines; they define what production-quality code looks like.

### SOLID

- **Single Responsibility**: Every module, class, and function should have one reason to change. If a function does two unrelated things, split it.
- **Open/Closed**: Design modules to be extendable without modifying existing code. Use interfaces, abstract classes, strategy patterns, and plugin architectures.
- **Liskov Substitution**: Subtypes must be substitutable for their base types without altering correctness. Overridden methods must honor the base contract.
- **Interface Segregation**: Prefer small, focused interfaces over large, general-purpose ones. Consumers should not depend on methods they do not use.
- **Dependency Inversion**: High-level modules should depend on abstractions, not concrete implementations. Inject dependencies rather than hardcoding them.

### DRY (Don't Repeat Yourself)

- Extract shared logic into well-named, well-tested utilities when the same concept appears in three or more places.
- DRY applies to knowledge, not just code. If a business rule is expressed in multiple places, centralize it.
- Do not over-DRY: two pieces of code that look similar but represent different concepts should remain separate. Premature abstraction is worse than duplication.

### KISS (Keep It Simple, Stupid)

- Choose the simplest solution that correctly solves the problem.
- Avoid clever code; prefer readable code that any team member can understand and modify.
- Reduce cognitive load: shorter functions, fewer branches, clearer names, less indirection.
- If a pattern, abstraction, or tool adds complexity without a clear benefit, do not use it.

### YAGNI (You Aren't Gonna Need It)

- Do not build features, abstractions, or infrastructure for speculative future requirements.
- Implement what is needed now, and design so that future extension is possible but not pre-built.
- If a requirement is uncertain, defer the implementation until it is validated.

### Separation of concerns

- Keep presentation, business logic, data access, and infrastructure in distinct layers.
- Each layer should be independently testable.
- Cross-layer calls should flow in one direction (presentation → business → data); never allow data access to call presentation directly.
- Configuration, logging, and error handling are cross-cutting concerns; centralize them rather than scattering them through business logic.

### Composition over inheritance

- Prefer composition (assembling behavior from small, focused pieces) over deep inheritance hierarchies.
- Use inheritance only when there is a genuine "is-a" relationship and the Liskov Substitution Principle holds.
- Favor mixins, higher-order functions, hooks, or dependency injection for shared behavior.

### Law of Demeter (principle of least knowledge)

- A module should only talk to its immediate collaborators, not reach through objects to access deeply nested properties.
- Avoid chains like `user.getAddress().getCity().getName()`. Instead, expose the needed information directly or use a dedicated method.

## Object-oriented design

Use OOP where it genuinely improves clarity and maintainability:

- Use classes for stateful services, domain entities, and complex lifecycles.
- Use interfaces/abstract classes to define contracts between layers.
- Keep class responsibilities focused; a class with more than ~200 lines likely needs decomposition.
- Make fields private by default; expose only what consumers actually need.
- Prefer factory methods or builder patterns over complex constructors.
- Use the strategy pattern for interchangeable algorithms, the observer pattern for event-driven communication, and the repository pattern for data access.
- Do not force OOP on simple utilities, transformations, or configuration; plain functions and modules are often clearer.

## Code readability

- Code is read far more often than it is written. Optimize for the reader.
- Use consistent formatting (enforced by the project's formatter).
- Keep functions under ~30 lines when practical; split longer functions into named sub-steps.
- Keep files under ~300 lines when practical; split when a file covers multiple concepts.
- Use early returns to reduce nesting depth.
- Avoid magic numbers and strings; use named constants.
- Group related code together; separate unrelated code with blank lines or into separate files.
- Write self-documenting code through descriptive naming, then add comments only for the "why."

## Type safety and static analysis

- **Static typing**: Enable strict compiler/checker settings (TypeScript strict mode, Mypy strict, Go vet, Rust compiler warnings, Java/C# compiler checks).
- **Avoid untyped escape hatches**: Avoid `any`, `Object`, `interface{}` (Go), or dynamic reflection unless interfacing with unvalidated dynamic boundaries.
- **Boundary validation**: Validate unparsed external data (JSON, YAML, query params) into strongly-typed domain structures before passing to internal layers.
- **Model optionality explicitly**: Use explicit option/nullable types (`Option<T>`, `T | null`, `Optional[T]`, pointers) rather than assuming values exist.
- **Immutability**: Prefer immutable data structures and pure functions where practical to reduce state-dependent bugs.
- **Resource management**: Always release resources deterministically using language idioms (RAII in Rust/C++, `defer` in Go, context managers `with` in Python, `try-with-resources` in Java, `using` in C#).

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

<ANTI_PATTERNS>
- Adding duplicate or speculative abstractions.
- Suppressing type errors without a documented reason.
- Catching and ignoring exceptions (empty catch blocks).
- Hardcoding environment-specific URLs or secrets.
- Putting database calls directly into presentational components.
- Introducing circular dependencies between modules.
- Using mutable global state for request-scoped data.
- Using magic numbers or unnamed string literals.
- Creating God objects or God functions that do everything.
- Violating the dependency direction defined in `ARCHITECTURE.md`.
- Mixing business logic with infrastructure concerns (HTTP, database drivers, file I/O).
</ANTI_PATTERNS>

## Maintainability checklist

Before considering code complete, verify:

- Can a new developer understand this code without asking the author?
- Can this code be tested in isolation (unit testable)?
- Can this code be modified without unintended side effects (low coupling)?
- Is the public API of each module minimal and well-typed?
- Are error cases handled explicitly, not silently swallowed?
- Is the code consistent with existing project conventions?
- Would this code survive a code review by a senior engineer?
