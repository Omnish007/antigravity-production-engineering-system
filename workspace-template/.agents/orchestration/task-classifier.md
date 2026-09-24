# Task Classifier

## Purpose

Classify every request before governed mutation so the agent can load the minimum sufficient context and the correct governance rigor. The canonical task taxonomy is shared with `verification-policy.yaml` and the task-state schema.

## Classification Contract

For governed work, record:

1. **Mode:** `inquiry` or `governed`.
2. **Task type:** exactly one canonical type.
3. **Risk:** `low`, `medium`, `high`, or `critical`.
4. **Reversibility:** `HIGH`, `MEDIUM`, or `LOW`.
5. **Target sensitivity:** `PUBLIC`, `INTERNAL`, `SENSITIVE`, or `SECRET`.
6. **External side effects:** boolean plus a concrete description.
7. **Confidence:** `high`, `medium`, or `low`.

Low-confidence classification that could change safety, data integrity, production behavior, or architecture must escalate before risky mutation.

## Canonical Task Types

`simple`, `bug`, `feature`, `complex-feature`, `refactor`, `architecture`, `security`, `database`, `migration`, `performance`, `testing`, `deployment`, `documentation`, `requirements`, `investigation`, `infrastructure`.

Aliases are normalized before state persistence:

- `bugfix` → `bug`
- `test` → `testing`
- `docs` → `documentation`
- `infra` → `infrastructure`

`review` is a verification activity (`diff-review`), not a task type. Do not persist `review` as a canonical task type.

## Risk Floors

- **Low:** highly reversible documentation, localized cosmetics, or isolated non-sensitive changes.
- **Medium:** normal feature work, non-critical bugs, internal refactoring, normal testing/database work.
- **High:** cross-layer changes, API compatibility changes, security-sensitive logic, sensitive-data handling, or significant operational side effects.
- **Critical:** destructive or difficult-to-reverse production/data operations, major security boundary changes, or equivalent material risk.

Any task involving authentication, authorization, credentials, production data, financial logic, destructive migration, external side effects, or public API compatibility must be at least **high**, and may be **critical** based on reversibility and impact.

## Lane Assignment

- **Inquiry mode:** read-only; no governed mutation.
- **Lane A:** `simple`, `documentation`, or `requirements` with low risk, HIGH reversibility, bounded scope, and no external side effects.
- **Lane B:** standard work with low/medium risk and no high-assurance trigger.
- **Lane C:** any high/critical risk, LOW reversibility, external side effect, production impact, or security/database/deployment/infrastructure/architecture trigger.

The machine-readable lane rules in `lane-policy.yaml` are authoritative when this document and another description differ.

## Pre-mutation Decision Procedure

1. Identify the requested outcome and explicit constraints.
2. Determine inquiry vs governed work.
3. Inspect repository evidence before assuming architecture or tooling.
4. Normalize the task type.
5. Assign risk using impact and reversibility, not only task labels.
6. Resolve target sensitivity and external side effects.
7. Assign the minimum lane that satisfies all policy floors.
8. Resolve required rules, skills, technology profiles, and quality gates.
9. If material uncertainty remains, escalate rather than silently inventing a requirement.
