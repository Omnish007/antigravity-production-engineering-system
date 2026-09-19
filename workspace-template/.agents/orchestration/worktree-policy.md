# Worktree Policy

## Purpose

Define safe repository isolation for parallel or high-risk work without reimplementing the host IDE's native worktree mechanism.

## Use native support

When Antigravity or the host agent provides native worktree support, use it instead of maintaining a competing worktree manager.

## Naming

Use a task-oriented convention such as:

```text
.worktrees/<task-id>
feat/<task-id>
fix/<task-id>
```

The exact convention should follow repository policy.

## Lifecycle

```text
CREATE -> ATTACH -> EXECUTE -> VERIFY -> RECONCILE -> CLEANUP
```

## When to use worktrees

Prefer worktrees (over working in the same branch) when:

- two tasks modify overlapping files;
- the work requires different dependency versions;
- schema/migration changes could conflict;
- the change is high-risk and you want easy rollback via branch deletion.

For simpler parallel work with no file overlap, shared-workspace concurrency (see `parallel-work-policy.md`) is sufficient.

## State file handling

State files (`.agents/state/`) are shared across worktrees because they represent project-level state, not branch-level state:

- coordinate state file writes to avoid conflicts;
- update state files from the main worktree after reconciliation;
- do not create divergent state file versions across worktrees.

## Safety invariants

Before cleanup:

- verify there are no uncommitted or untracked changes that belong to unresolved work;
- verify the branch is reconciled/merged or explicitly preserved;
- verify no task state depends on the worktree still existing.

Never delete a worktree merely because the task is marked complete; first reconcile its output and evidence.

## Conflict policy

A conflict includes both textual merge conflicts and semantic conflicts such as:

- incompatible API contracts;
- contradictory config changes;
- duplicate migrations;
- incompatible package upgrades;
- two implementations of the same domain rule.

Escalate unresolved conflicts rather than choosing arbitrarily.

## Emergency recovery

If a worktree becomes corrupted or the work must be abandoned:

- verify no valuable uncommitted changes remain;
- if changes exist, stash or commit them to a recovery branch;
- remove the worktree with `git worktree remove`;
- record the abandoned work in the task record;
- update `events.jsonl` with the worktree abandonment event.
