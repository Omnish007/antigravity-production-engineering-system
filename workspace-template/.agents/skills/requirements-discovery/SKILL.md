---
name: requirements-discovery
id: SKILL-REQ-DISC-001
description: Turn an incomplete idea into explicit, testable, implementation-ready requirements without inventing business decisions.
---

# Requirements Discovery Skill

<MISSION>
Turn an incomplete idea into explicit, testable, implementation-ready requirements without inventing business decisions.
</MISSION>

<WHEN_TO_USE>
Activate this skill when executing tasks requiring requirements-discovery capabilities, workflows, or architectural guidance.
</WHEN_TO_USE>

<PRECONDITIONS>
### Prerequisites
- Active task in .agents/state/tasks.json must be IN_PROGRESS.
    - TASK_STARTED event must be recorded in .agents/state/events.jsonl.

### Pre-flight Checklist
- [ ] Stakeholder personas identified
    - [ ] Non-functional requirements discovered
    - [ ] Scope boundaries established
</PRECONDITIONS>

<NON_NEGOTIABLES>
- Identify user personas, system actors, and trust boundaries.
    - Uncover implicit requirements (reliability, rate limiting, error handling, auditability).
    - Structure discovered requirements into clear functional categories.
</NON_NEGOTIABLES>

<PROCEDURE>
## Use when

The user has an idea, rough request, conversation notes, or an incomplete feature description rather than a sufficiently detailed specification.

## Procedure

1. Restate the objective in one sentence.
2. Identify actors/personas and permissions.
3. Identify the primary user journey.
4. Identify alternate, failure, empty, and recovery flows.
5. Extract domain entities and state transitions.
6. Identify functional requirements.
7. Identify non-functional requirements: security, privacy, accessibility, performance, reliability, observability, compliance, and data lifecycle.
8. Identify external integrations and trust boundaries.
9. Identify constraints that are explicit versus assumed.
10. Convert vague goals into observable acceptance criteria.
11. List genuine open decisions separately from technical implementation choices.
12. Generate a scope boundary: in-scope, out-of-scope, future consideration.

## Question strategy

Ask questions only when the answer materially changes product behavior or risk. Prefer a small number of high-value questions over exhaustive interrogation.

When a technical answer can be derived from repository evidence or official documentation, research it instead of asking the user.

## Output

Produce a structured requirements document or update the appropriate file under `docs/requirements/` if that directory exists in the project.

## Guardrail

Never manufacture product rules such as refund policy, role permissions, retention periods, pricing behavior, or legal/compliance requirements. Mark them as decisions the product owner must make when they cannot be inferred.
</PROCEDURE>

<VERIFICATION_POLICY>
### Exit Criteria
Discovered requirements documented in docs/PROJECT_CONTEXT.md.
</VERIFICATION_POLICY>

<DELIVERABLES>
- Clarifying stakeholder questions, discovered constraints, user personas, and initial requirements draft.
</DELIVERABLES>
