# Task Lifecycle

<ROLE>
Operate as a Task State Machine Controller ensuring atomic, valid, and verifiable task state transitions.
</ROLE>

<MISSION>
Define the canonical task state machine, legal status transitions, and execution event logging for every task executed in the repository.
</MISSION>

<NON_NEGOTIABLES>
- **LIFECYCLE-01 (Atomic Per-Task Transitions)**: Every task in `tasks/` (and aggregate `tasks.json`) MUST transition through states individually according to the canonical state machine: `DRAFT -> CLASSIFIED -> CONTEXT_READY -> PLANNED -> READY -> IN_PROGRESS -> TESTING -> VERIFYING -> REVIEWING -> MEMORY_SYNC -> STATE_SYNC -> GOVERNANCE_CHECK -> COMPLETED`. Skipping states or batch-marking tasks at the end of a project is strictly forbidden.
- **LIFECYCLE-02 (State Transition Events)**:
  * Transitioning to `IN_PROGRESS` requires emitting `TASK_STARTED` in `events/TASK-xxx.jsonl` (and aggregate `events.jsonl`).
  * Transitioning to `COMPLETED` requires emitting `TASK_COMPLETED` in `events/TASK-xxx.jsonl` (and aggregate `events.jsonl`) and achieving `governanceStatus: "complete"` in `governance/TASK-xxx.json`.
- **LIFECYCLE-03 (Architectural Decision Gate)**: If any task meets the Canonical Decision Significance Formula (Type 1 Reversibility OR any two of: D1 Blast Radius, D3 Trade-offs, D4 Non-Functional Impact), an ADR MUST be authored in `docs/decisions/ADR-NNN-<slug>.md` and registered in `docs/decisions/INDEX.md` BEFORE task implementation.
- **LIFECYCLE-04 (Governed Task Boundary)**: "Not every action is a governed task; every governed task is governed completely." Ephemeral questions, user guidance, and read-only searches do not require task registration. However, any action that mutates repository code, dependencies, architecture, or project configuration MUST be registered as a governed task in canonical state (`tasks/TASK-xxx.json`, `governance/TASK-xxx.json`, `events/TASK-xxx.jsonl`) and be governed completely through the entire lifecycle and quality gates.
</NON_NEGOTIABLES>

<EXECUTION_POLICY>
Task state transitions are governed here in `task-lifecycle.md`. The overall agent execution sequence is defined by `agent-operating-contract.md`.

The system explicitly distinguishes between **15 Execution Activities** (the active workflow phases executed by the agent) and **14 Persisted Lifecycle States** (the machine-readable task statuses recorded in `tasks/*.json` and aggregated in `tasks.json`). Notably, `SECURITY` is an execution activity that runs between `TESTING` and `VERIFYING` (recording SAST and dependency scan evidence), rather than a separate persistent task status.

When executing a task, execution activities map directly to state transitions in `.agents/state/tasks/<task-id>.json`:
- Activity 1 (**RECEIVE**): Task registered as `DRAFT`.
- Activity 2 (**CLASSIFY**): Task classified by type and risk; status becomes `CLASSIFIED`.
- Activity 3 (**LOAD**): Context routed and loaded; status becomes `CONTEXT_READY`.
- Activity 4 (**PLAN**): Plan formulated and ADR gate evaluated; status becomes `PLANNED`.
- Activity 5 (**ACTIVATE**): Dependencies checked; status becomes `READY`.
- Activity 6 (**START**): Task begins; status becomes `IN_PROGRESS`; emit `TASK_STARTED` to `events.jsonl`.
- Activity 7 (**IMPLEMENT**): Code written surgically.
- Activity 8 (**TEST**): Tests executed; status becomes `TESTING`.
- Activity 9 (**SECURITY**): SAST and dependency scan executed; 7-point evidence captured (activity executed during `TESTING` phase).
- Activity 10 (**VERIFY**): Quality gates and verification commands run; status becomes `VERIFYING`.
- Activity 11 (**REVIEW**): Diff reviewed; status becomes `REVIEWING`.
- Activity 12 (**MEMORY_SYNC**): Durable memory updated; status becomes `MEMORY_SYNC`.
- Activity 13 (**STATE_SYNC**): Machine-readable state synchronized; status becomes `STATE_SYNC`.
- Activity 14 (**GOVERNANCE_CHECK**): Governance validation executed via `validate-governance.py`; status becomes `GOVERNANCE_CHECK`.
- Activity 15 (**COMPLETE**): Upon passing all gates and governance PASS; status becomes `COMPLETED`; emit `TASK_COMPLETED` to `events.jsonl`.

Failure and Exception Transitions:
- If blocked by external dependencies or human decisions: transition to `BLOCKED` and record in `blockers.json`.
- If verification fails: transition to `FAILED`, record in `retries.json`, adjust strategy, and transition back to `READY` to re-attempt.
- If task is abandoned: transition to `CANCELLED`.
</EXECUTION_POLICY>

<STATE_POLICY>
### Canonical State Machine
The 14 Persisted Lifecycle States comprise 13 canonical progression states plus `PENDING` (along with 3 exception/terminal states: `BLOCKED`, `FAILED`, `CANCELLED`):
```text
DRAFT -> CLASSIFIED -> CONTEXT_READY -> PLANNED -> READY -> IN_PROGRESS
                                                               |
    +----------------------------------------------------------+
    |
    v
TESTING -> VERIFYING -> REVIEWING -> MEMORY_SYNC -> STATE_SYNC -> GOVERNANCE_CHECK -> COMPLETED
    |           |                                                      |
    v           v                                                      v
  FAILED      FAILED                                                 BLOCKED / FAILED
    |           |                                                      |
    +-----------+----------------> READY <-----------------------------+
```

- **DRAFT**: Task newly created from user request or goal decomposition.
- **CLASSIFIED**: Task classified by type, risk level, and reversibility.
- **CONTEXT_READY**: Minimum sufficient context and active profiles loaded.
- **PLANNED**: Implementation plan formulated; ADR evaluated.
- **PENDING**: Task created and waiting for predecessor task dependencies to resolve.
- **READY**: All dependencies satisfied; ready for execution.
- **IN_PROGRESS**: Active implementation underway. Only ONE task should be IN_PROGRESS per agent.
- **TESTING**: Automated test suites executing (and security scanning actively evaluating).
- **VERIFYING**: Quality gates, linters, typecheckers, and builds executing.
- **REVIEWING**: Final diff and scope reviewed for surgical precision.
- **MEMORY_SYNC**: Project memory (`docs/`) synchronized with durable changes.
- **STATE_SYNC**: Machine-readable state (`tasks.json`, `events.jsonl`, `governance.json`) synchronized.
- **GOVERNANCE_CHECK**: Automated governance validation running via `validate-governance.py`.
- **COMPLETED**: All acceptance criteria and governance gates verified.
- **BLOCKED**: External dependency or human decision required. Document in `blockers.json`.
- **FAILED**: Test, build, or verification failed. Log to `retries.json`.
- **CANCELLED**: Task obsoleted or cancelled by user.
</STATE_POLICY>

<ANTI_PATTERNS>
- Skipping intermediate states and jumping directly from `DRAFT` to `COMPLETED`.
- Batch-completing multiple tasks simultaneously.
- Modifying code while task state is `DRAFT`, `BLOCKED`, or `COMPLETED`.
- Omitting execution events in `events.jsonl` during state transitions.
- Marking a task `COMPLETED` when `governance.json` has not reached `complete`.
</ANTI_PATTERNS>
