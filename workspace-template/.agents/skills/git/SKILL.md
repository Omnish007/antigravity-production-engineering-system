---
name: git
description: Operate Git safely with minimal history disruption, coherent commits, diff review, and controlled branching/merging.
---

# Git Skill

## Procedure

1. Inspect status.
2. Understand existing changes.
3. Choose or confirm branch/worktree strategy.
4. Keep changes scoped.
5. Review diff.
6. Run verification.
7. Commit coherent changes when requested or repository workflow expects it.

## Commits

Use Conventional Commits when adopted by the repository. Keep commits logically reversible and avoid mixing unrelated refactors with behavior changes.

## Merge/reconcile

Before merging parallel work:

- inspect both diffs;
- resolve file conflicts;
- inspect semantic conflicts;
- run integrated verification.

## Safety

Never use force-push, destructive reset, bulk cleanup, or branch deletion without explicit authorization for that operation.
