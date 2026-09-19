# Human Checkpoint Policy

## Objective

Maximize safe autonomy while preventing irreversible or high-impact actions without approval.

## Autonomous actions

The agent may normally:

- read repository files;
- edit/create source and documentation;
- run local formatter/linter/type-check/test/build commands;
- create or update ADRs and project-memory documents;
- create `.env.example` files;
- create branches/worktrees when repository policy permits;
- run local, non-destructive development commands;
- generate seed/test data in isolated development environments;
- inspect Git history and diffs.

## Approval required before

### Critical

- production deployment;
- destructive database operations;
- deleting or overwriting valuable user data;
- modifying real production credentials/secrets;
- destructive filesystem operations;
- rotating keys with live-user impact;
- enabling public access to a previously private service.

### High

- breaking public API changes;
- payment/financial workflow changes with live consequences;
- irreversible external actions such as sending real emails/messages;
- force-push or destructive history rewriting;
- broad data migrations without a verified rollback/backup path.

### Medium/high judgment

- material architecture changes not covered by project decisions;
- introducing a new externally managed service with significant cost/security/operational implications.

## Safe alternative

When approval is required, prepare everything possible without executing the irreversible step. Provide the exact action, risk, expected effect, and verification plan.
