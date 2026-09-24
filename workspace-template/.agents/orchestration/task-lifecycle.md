# Task Lifecycle

## Purpose

Define the canonical persisted state machine for governed tasks. Inquiry mode is outside this state machine because it does not mutate repository state.

## Canonical States

```text
DRAFT
  ↓
CLASSIFIED
  ↓
CONTEXT_READY
  ↓
PLANNED
  ↓
READY
  ↓
IN_PROGRESS
  ↓
TESTING
  ↓
VERIFYING
  ↓
REVIEWING
  ↓
MEMORY_SYNC
  ↓
STATE_SYNC
  ↓
GOVERNANCE_CHECK
  ↓
COMPLETED
```

Exception/terminal states: `FAILED`, `BLOCKED`, `CANCELLED`.
Optional wait state: `PENDING` when a required approval or dependency prevents execution.

## State Authority

Per-task files are canonical:

- `.agents/state/tasks/TASK-ID.json`
- `.agents/state/governance/TASK-ID.json`
- `.agents/state/events/TASK-ID.jsonl`

Aggregate files such as `tasks.json`, `governance.json`, and `events.jsonl` are derived views. Regenerate them through the aggregation tooling; do not treat them as independent authority.

## Transition Invariants

- Do not skip required states for the active lane.
- Do not mutate application code while a task is `DRAFT`, `BLOCKED`, `CANCELLED`, or `COMPLETED`.
- Only one task may be `IN_PROGRESS` per agent session unless the parallel-work policy explicitly provisions isolated worktrees and ownership.
- `TASK_STARTED` must occur before implementation mutations.
- A completed task must have a corresponding governance record and passing required verification gates.
- A gate failure moves the task to `FAILED` or keeps it before completion while recovery is performed; it must not be hidden.
- Approval requirements must be satisfied before entering an execution state that requires them.

## Activity Mapping

| Activity | Persisted state / condition |
|---|---|
| Understand / Receive | `DRAFT` |
| Classify | `CLASSIFIED` |
| Load context | `CONTEXT_READY` |
| Plan | `PLANNED` |
| Resolve dependencies/approval | `READY` or `PENDING` |
| Start implementation | `IN_PROGRESS` + `TASK_STARTED` |
| Test | `TESTING` |
| Security checks | Verification activity during `TESTING` when required |
| Verify | `VERIFYING` |
| Review diff | `REVIEWING` |
| Sync durable docs | `MEMORY_SYNC` |
| Sync machine state | `STATE_SYNC` |
| Governance validation | `GOVERNANCE_CHECK` |
| Complete | `COMPLETED` + `TASK_COMPLETED` |

## Required State Evidence

Each transition must be attributable to a concrete action or validator result. The state file must not claim a transition solely because the model intended to perform it.

## Recovery

On failure:

1. record the failed attempt in retry state;
2. preserve successful changes;
3. classify the failure;
4. choose a justified recovery strategy;
5. re-enter the appropriate state rather than rewriting history.

Interrupted tasks should be recovered using `recover-task.py` rather than manually guessing the last valid state.
