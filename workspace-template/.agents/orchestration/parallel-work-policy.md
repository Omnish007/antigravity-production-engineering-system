# Parallel Work Policy

<MISSION>
Allow concurrency across tasks and agents without creating conflicting, incompatible, or unmergeable work.
</MISSION>

<NON_NEGOTIABLES>
- Parallel subagents must operate in isolated git worktrees or branches to prevent file collision and race conditions whenever modifying code.
- Canonical state writes (`tasks/TASK-xxx.json`, `events/TASK-xxx.jsonl`, `blockers/BLK-xxx.json`) are scoped per-task to eliminate write collisions; aggregate state files (`tasks.json`, `events.jsonl`, `blockers.json`) are derived and synchronized centrally.
- Never assume a clean Git merge means the integrated result is semantically correct.
</NON_NEGOTIABLES>

<DECISION_RULES>
## Safe to parallelize

Parallel execution is reasonable when tasks:
- have no overlapping output files;
- touch independent modules;
- have stable contracts at their boundary;
- do not require mutually exclusive dependency/version changes;
- do not mutate the same database migration/schema artifacts.

Read-only review, analysis, and test planning can often run in parallel with implementation when their inputs are stable.

## Isolate when

Use worktrees or equivalent native isolation when:
- two tasks touch the same files;
- two tasks modify the same module heavily;
- dependency changes may conflict;
- schema/migration work can conflict;
- environment configuration differs;
- the host agent's concurrent-edit behavior cannot guarantee clean reconciliation.
</DECISION_RULES>

<ACTION_SPACE_CONSTRAINTS>
## Before parallel start

1. Decompose work into tasks.
2. Declare expected output paths.
3. Identify dependencies.
4. Decide shared workspace versus isolated worktree.
5. Ensure each task has its own acceptance criteria.
6. Use canonical per-task state files (`tasks/TASK-xxx.json`, `governance/TASK-xxx.json`, `events/TASK-xxx.jsonl`, `blockers/BLK-xxx.json`) to eliminate state file contention across parallel workers.
</ACTION_SPACE_CONSTRAINTS>

<EXECUTION_POLICY>
## Reconciliation

After parallel completion:
- compare changed-file sets;
- check textual conflicts;
- check semantic conflicts in shared configs/contracts;
- run the integrated test/build suite;
- reconcile project memory once, centrally, after the combined state is known.

Never assume a clean Git merge means the result is semantically correct.

## Communication between parallel agents

When multiple agents work concurrently:
- use state files as the coordination mechanism, not shared mutable variables;
- the orchestrating agent is responsible for merging results and resolving conflicts;
- each agent should complete its work to a committable state before handoff;
- document what was done and what remains in the task record.
</EXECUTION_POLICY>

<FAILURE_RECOVERY>
## Failure isolation

If one parallel task fails:
- it should not block other independent tasks;
- record the failure in `retries.json` and `events.jsonl`;
- preserve successful work from other parallel tasks;
- re-evaluate dependencies before continuing dependent tasks.
</FAILURE_RECOVERY>
