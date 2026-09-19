# Requirements Rules

Recommended activation: **Always On**

## Requirement classification

Separate every statement into one of these categories:

- explicit requirement;
- acceptance criterion;
- business rule;
- non-functional requirement;
- constraint;
- assumption;
- implementation choice;
- open question.

Do not silently turn an implementation preference into a product requirement.

## Ambiguity

Before implementation, identify ambiguities that can materially change behavior, data, security, cost, UX, or architecture.

Resolve them by:

1. reading the PRD/requirements;
2. reading accepted ADRs and conventions;
3. examining existing behavior;
4. researching the technical fact if it is researchable;
5. asking the user only when the remaining uncertainty is a real product/business/high-impact choice.

## Completeness

For meaningful requirements, consider:

- actors and permissions;
- primary and alternate flows;
- success and failure behavior;
- empty/loading states;
- validation rules;
- edge/boundary cases;
- concurrency/idempotency;
- security/privacy;
- observability/audit needs;
- performance/scalability expectations;
- data retention/deletion;
- API and integration contracts;
- migration/backward compatibility.

## Acceptance criteria

Acceptance criteria must be observable and testable. Prefer Given/When/Then or similarly explicit statements. Avoid vague phrases such as "works well", "fast", "secure", or "user-friendly" without measurable or observable meaning.

## Scope

Do not expand scope merely because a related improvement is interesting. Log out-of-scope improvements separately and only implement them when requested or intentionally scheduled.
