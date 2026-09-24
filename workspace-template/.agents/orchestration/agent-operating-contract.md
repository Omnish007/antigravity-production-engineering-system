# Agent Operating Contract

## Purpose

Define the canonical execution lifecycle for governed engineering work. The policy registry identifies this file as the lifecycle owner; detailed task states remain owned by `task-lifecycle.md` and risk/lanes by `lane-policy.yaml`.

## Priorities

1. Safety and security boundaries
2. User-request correctness and acceptance criteria
3. Empirical verification evidence
4. Existing project decisions and architecture
5. Surgical scope discipline
6. Durable memory and state consistency

## Operating Modes

### Inquiry mode

Read-only explanation, inspection, or research that does not mutate repository state. Do not create a governed task solely for an inquiry.

### Lane A

Low-risk, highly reversible repository mutations. Use the minimum ceremony defined by `lane-policy.yaml`, but still register and validate the task.

### Lane B

Standard engineering changes. Use the normal plan → implement → test → verify → review lifecycle.

### Lane C

High-risk, high-impact, difficult-to-reverse, production, security, database, infrastructure, or externally side-effecting work. Full governance and approval requirements apply.

## Non-negotiable Execution Rules

- Resolve the task type and risk before mutation.
- Read the governing skill and applicable rules before planning or modifying files.
- Inspect existing implementation and tests before editing.
- Keep the active task scope explicit.
- Use the least powerful semantic capability that can safely complete the phase.
- Unknown/unmapped tool capabilities do not receive implicit trust.
- Record failed verification before changing strategy.
- Never claim a gate passed without runtime-observed or independently derived evidence.
- Never bypass a required approval or safety boundary.
- Keep canonical per-task state authoritative; aggregate state is derived.

## Context Loading

Load progressively:

1. `AGENTS.md` and platform safety constraints.
2. Project navigation/context: `docs/INDEX.md`, `PROJECT_CONTEXT.md`, `CURRENT_STATE.md`.
3. Applicable rules from `.agents/rules/`.
4. Relevant ADRs and conventions.
5. Relevant technology profiles.
6. Primary domain skill and supporting skills.
7. Affected source/test files.

Do not flood context with unrelated files.

## Execution Lifecycle

The lifecycle is:

**UNDERSTAND → INSPECT → CLASSIFY → LOAD → PLAN → CHECKPOINT (when required) → IMPLEMENT → TEST → VERIFY → REVIEW → MEMORY_SYNC → STATE_SYNC → GOVERNANCE_CHECK → COMPLETE**

The task state machine in `task-lifecycle.md` determines which persisted state corresponds to each activity. `SECURITY` is a verification activity, not a separate persisted state.

## Failure Handling

When a command or gate fails:

1. Preserve the failure evidence.
2. Diagnose whether the failure is code, environment, requirement, governance, or tool related.
3. Record the failed attempt in retry state before changing strategy.
4. Retry only when there is a justified next step.
5. After repeated failure without progress, change strategy or escalate rather than looping.

## Completion

Completion is allowed only when the applicable governance and verification gates pass. The final report must identify actual commands and results, scope, durable documentation changes, and unresolved items.
