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
- inspect Git history and diffs;
- delegate well-scoped sub-tasks to sub-agents (see `multi-agent-policy.md`);
- install development dependencies declared in `package.json`.

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
- introducing a new externally managed service with significant cost/security/operational implications;
- major dependency upgrades that cross breaking-change boundaries;
- adding new authentication/authorization providers;
- changing database schemas in production environments.

## Escalation procedure

When approval is required:

1. Prepare everything possible without executing the irreversible step.
2. Provide the exact action, risk, expected effect, and verification plan.
3. Clearly state what will happen if the action is approved.
4. Clearly state what will happen if the action is rejected (alternative plan).
5. Wait for explicit approval before proceeding.

## Sub-agent checkpoint inheritance

Sub-agents inherit the checkpoint requirements of their parent task's risk level. A sub-agent performing work that would require approval at the task level must escalate to the orchestrating agent, which escalates to the human.
