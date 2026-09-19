---
name: git
description: Operate Git safely with minimal history disruption, coherent commits, diff review, and controlled branching/merging.
---

# Git Skill

## Procedure

1. Inspect status and understand existing changes.
2. Confirm or choose branch strategy (feature branch, worktree, trunk-based).
3. Keep changes scoped to one logical concern per commit.
4. Review the full diff before committing.
5. Run verification appropriate to the change.
6. Commit coherent changes with descriptive messages.
7. Push or prepare for review as the workflow requires.

## Branch strategy

- Use feature branches for non-trivial work.
- Name branches descriptively: `feature/<name>`, `fix/<name>`, `refactor/<name>`.
- Keep branches short-lived; merge and delete when complete.
- Use worktrees for parallel work on the same repository when needed (see `worktree-policy.md`).

## Commits

- Use Conventional Commits when adopted by the repository (e.g., `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`).
- Keep commits logically reversible and atomic.
- Do not mix unrelated refactors with behavior changes in one commit.
- Write commit messages that explain the "why" when the "what" is not obvious from the diff.
- Include issue/ticket references when the project uses them.

## Diff hygiene

- Review every diff before committing.
- Verify no unintended files were staged (lockfile changes, IDE configs, generated files).
- Verify no secrets, credentials, or sensitive data appear in the diff.
- Verify no debug logging, commented-out code, or TODO hacks remain.
- Keep the diff minimal; only include changes related to the task.

## Merge/reconcile

Before merging parallel work:

- inspect both diffs;
- resolve file conflicts;
- inspect semantic conflicts (two changes that don't conflict textually but conflict logically);
- run integrated verification after the merge;
- verify the merge result builds, passes tests, and type-checks.

## Stashing and staging

- Use `git stash` to temporarily shelve work when switching tasks.
- Use `git add -p` for granular staging when a working tree contains multiple logical changes.
- Prefer small, focused commits over large monolithic ones.

## Safety

- Never use force-push, destructive reset, bulk cleanup, or branch deletion without explicit authorization for that operation.
- Before any destructive git operation, verify the current branch and state.
- Do not rebase shared/published branches without coordination.
- Prefer `--no-ff` merges when preserving branch history is valuable.

## Recovery

- If a commit is made in error, prefer `git revert` over `git reset --hard` for shared branches.
- If working tree changes are lost, check `git stash list` and `git reflog`.
- Document any non-trivial recovery actions in the task record.
