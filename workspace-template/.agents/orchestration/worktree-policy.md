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
