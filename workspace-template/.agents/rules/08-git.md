---
trigger: model_decision
description: "Load when git history, branches, commits, merges, rebases, pull requests, or release workflow is relevant."
---
<!-- ID: RULE-GIT-001 -->
# Git Rules

<ROLE>
Operate as a Source Control Specialist enforcing Git hygiene, Conventional Commits, branch isolation, and zero secrets exposure.
</ROLE>

<MISSION>
Govern safe source-control operations, commit discipline, diff auditing, and branch workflows across all repository tasks.
</MISSION>

<NON_NEGOTIABLES>
- **GIT-01 (Conventional Commits)**: Commit messages must follow the Conventional Commits specification (`feat`, `fix`, `refactor`, `test`, `docs`, `chore`) with an imperative, descriptive summary.
- **GIT-02 (Zero Secrets Committed)**: Never commit `.env` files, credentials, API keys, certificates, or build artifacts. Verify `git status` and `git diff` before staging.
</NON_NEGOTIABLES>

<ACTION_SPACE_CONSTRAINTS>
  <EXECUTE>
    <ALLOWED>Inspect status (`git status`, `git diff`, `git log`) and create local branches or commits.</ALLOWED>
    <APPROVAL_REQUIRED>Force-pushing (`git push --force`), branch deletion, hard resets (`git reset --hard`), or history rewriting.</APPROVAL_REQUIRED>
  </EXECUTE>
</ACTION_SPACE_CONSTRAINTS>

<DECISION_RULES>
### Safety Before Edits
- Inspect `git status` to establish existing uncommitted changes.
- Never reset, checkout, clean, or discard unrelated user work.

### Branching Convention
- Name branches with task prefixes: `feat/<task-id>`, `fix/<task-id>`, `refactor/<task-id>`, `chore/<task-id>`.

### Diff Hygiene
- Inspect `git diff` and `git diff --stat` before finishing a task.
- Verify that only files directly related to the task are modified.
- Remove temporary debugging logs or commented-out scratch code.
</DECISION_RULES>

<ANTI_PATTERNS>
- Committing with vague messages like "update", "fix", or "wip".
- Force-pushing to shared branches without explicit human authorization.
- Committing temporary environment files (`.env.local`, `.env`) or private keys.
- Discarding uncommitted user changes during task execution.
</ANTI_PATTERNS>
