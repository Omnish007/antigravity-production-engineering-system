# Worktree Policy

<MISSION>
Define safe repository isolation for parallel or high-risk work without reimplementing the host IDE's native worktree mechanism.
</MISSION>

<NON_NEGOTIABLES>
- Temporary worktrees must be cleaned up and pruned upon task completion or termination.
- Never delete a worktree merely because the task is marked complete; first reconcile its output and evidence.
- State files (`.agents/state/`) are shared across worktrees because they represent project-level state; never create divergent state file versions across worktrees.
</NON_NEGOTIABLES>

<ACTION_SPACE_CONSTRAINTS>
## Antigravity Native Task Groups & Worktree Support

When Antigravity or the host runtime provides native Task Groups or workspace branching, use them for parallel subagent execution. Native task groups coordinate subagents while worktrees provide file-system isolation.

## Naming

Use a task-oriented convention such as:
```text
.worktrees/<task-id>
feat/<task-id>
fix/<task-id>
```
The exact convention should follow repository policy.

## Safety invariants

Before cleanup:
- verify there are no uncommitted or untracked changes that belong to unresolved work;
- verify the branch is reconciled/merged or explicitly preserved;
- verify no task state depends on the worktree still existing.
</ACTION_SPACE_CONSTRAINTS>

<DECISION_RULES>
## When to use worktrees

Prefer worktrees (over working in the same branch) when:
- two tasks modify overlapping files;
- the work requires different dependency versions;
- schema/migration changes could conflict;
- the change is high-risk and you want easy rollback via branch deletion.

For simpler parallel work with no file overlap, shared-workspace concurrency (see `parallel-work-policy.md`) is sufficient.

## Conflict policy

A conflict includes both textual merge conflicts and semantic conflicts such as:
- incompatible API contracts;
- contradictory config changes;
- duplicate migrations;
- incompatible package upgrades;
- two implementations of the same domain rule.

Escalate unresolved conflicts rather than choosing arbitrarily.
</DECISION_RULES>

<EXECUTION_POLICY>
## Lifecycle

```text
CREATE -> ATTACH -> EXECUTE -> VERIFY -> RECONCILE -> CLEANUP
```

## State File Handling & Merge Conflict Elimination

State files (`.agents/state/`) represent project-level state. To eliminate merge conflicts across parallel worktrees and concurrent subagents:
- **Canonical Per-Task Isolation**: Subagents in separate worktrees write exclusively to canonical per-task files:
  * `.agents/state/tasks/TASK-xxx.json`
  * `.agents/state/governance/TASK-xxx.json`
  * `.agents/state/events/TASK-xxx.jsonl`
  * `.agents/state/blockers/BLK-xxx.json`
  Because each task has a dedicated file path, git merges between worktree branches and main will never experience state collisions.
- **Derived Aggregates**: Monolithic files (`tasks.json`, `governance.json`, `events.jsonl`, `blockers.json`) are derived aggregates. They are generated centrally by the Coordinator in the primary worktree via `aggregate-state.py` or `reconcile-state.py` after worktree reconciliation. Subagents in worktrees must NEVER directly mutate aggregate state files.
</EXECUTION_POLICY>

<FAILURE_RECOVERY>
## Emergency recovery

If a worktree becomes corrupted or the work must be abandoned:
- verify no valuable uncommitted changes remain;
- if changes exist, stash or commit them to a recovery branch;
- remove the worktree with `git worktree remove`;
- record the abandoned work in the task record;
- update `events.jsonl` with the worktree abandonment event.
</FAILURE_RECOVERY>
