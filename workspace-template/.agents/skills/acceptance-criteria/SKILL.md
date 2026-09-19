---
name: acceptance-criteria
description: Convert requirements into objective, testable acceptance conditions that can be traced to implementation and verification evidence.
---

# Acceptance Criteria Skill

## Quality rules

Each criterion should be:

- observable;
- specific;
- independently testable where practical;
- tied to a user/system outcome;
- unambiguous;
- realistic for the stated scope.

## Preferred structure

Use Given/When/Then for behavioral flows:

```text
Given <precondition>
When <action>
Then <observable result>
And <additional invariant>
```

For non-behavioral constraints, use measurable statements, such as response status, data invariant, accessibility property, or build/test condition.

## Coverage prompts

For every meaningful feature consider:

- happy path;
- validation failure;
- unauthorized/forbidden;
- not found;
- conflict/duplicate;
- rate limit/resource constraint;
- empty state;
- retry/recovery;
- concurrency/idempotency;
- persistence invariant;
- accessibility;
- performance requirement when explicitly required.

## Traceability

Assign stable criterion IDs when the feature is complex, for example `AC-01`, `AC-02`. Map each criterion to implementation tasks and verification evidence.
