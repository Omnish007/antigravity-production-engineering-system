# Git Rules

Recommended activation: **Always On**

## Safety

Before substantial edits:

- inspect `git status`;
- understand existing local changes;
- do not reset, checkout, clean, or revert unrelated user work;
- inspect recent history when it helps explain an existing convention or change.

## Branching

Follow the repository's established branch strategy. For new branches, use a consistent prefix such as:

```text
feat/<short-task-id>
fix/<short-task-id>
refactor/<short-task-id>
chore/<short-task-id>
```

## Commits

Keep commits logically coherent. When Conventional Commits are adopted, use:

```text
<type>(optional-scope): imperative summary
```

Examples: `feat(auth): add refresh-token rotation`, `fix(api): reject expired reset tokens`.

Do not create meaningless commits such as `changes`, `update`, or `final fix`.

## Diff hygiene

Before completion:

- inspect `git diff` and `git diff --stat`;
- verify only intended files changed;
- remove accidental debug output;
- ensure generated files are treated according to repository policy;
- ensure no secrets or environment credentials were added.

## History rewriting

Force-push, branch deletion, history rewriting, or destructive cleanup requires explicit approval unless the user has clearly authorized the exact operation.

## Parallel work

Use `.agents/orchestration/parallel-work-policy.md` and `.agents/orchestration/worktree-policy.md`. Never merge work blindly; reconcile semantic conflicts as well as text conflicts.
