---
name: requirements-analysis
description: Analyze structured or unstructured requirements for completeness, contradictions, risks, boundaries, dependencies, and implementation implications.
---

# Requirements Analysis Skill

## Analysis model

For each requirement, identify:

- actor;
- trigger;
- preconditions;
- system behavior;
- postconditions;
- data touched;
- authorization;
- failure behavior;
- observability needs;
- acceptance criteria.

## Gap analysis

Check for:

- contradictory requirements;
- missing actor permissions;
- missing empty/error/loading behavior;
- unbounded inputs or data growth;
- concurrency/race conditions;
- idempotency requirements;
- retry semantics;
- timezone/date handling;
- localization/currency assumptions;
- privacy and deletion implications;
- migration/backward compatibility;
- external dependency failure;
- abuse/rate-limit scenarios.

## Requirement maturity

Classify items as:

- ready to build;
- buildable with a recorded assumption;
- needs research;
- needs user/product decision.

## Output

Produce a traceable mapping:

```text
Requirement -> acceptance criteria -> affected module(s) -> API/data impact -> test strategy
```

Do not design the implementation in detail until the product behavior is sufficiently unambiguous.
