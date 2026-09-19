# Observability Rules

Recommended activation: **Always On**

## Purpose

Ensure agent work is traceable, measurable, and auditable. Observable agent behavior enables diagnosis of reasoning failures, performance optimization, and continuous improvement.

## Execution tracing

For non-trivial tasks, maintain a traceable record of:

- task classification and skill activation decisions;
- files read and their relevance to the task;
- key decisions made and the evidence supporting them;
- commands executed, their exit codes, and diagnostic excerpts;
- files created or modified;
- errors encountered and recovery actions taken;
- memory synchronization performed.

Use `.agents/state/events.jsonl` for machine-readable event capture. Each event should include a timestamp, event type, task ID, and sufficient context to reconstruct the action later.

## Application observability

When implementing or modifying application code, ensure adequate operational observability:

- structured logging with consistent field schemas;
- correlation/request IDs propagated across service boundaries;
- error classification by type (client, domain, infrastructure, unexpected);
- health and readiness endpoints where the deployment model requires them;
- performance-relevant metrics at critical paths;
- audit logging for security-sensitive operations.

Avoid logging secrets, authentication tokens, raw personal data, or unbounded payloads. Log enough to investigate failures without creating privacy or security liabilities.

## Context budget awareness

Track context consumption during complex tasks:

- be aware of how many files and how much content has been loaded into the current session;
- prefer indexes and summaries before loading full documents;
- when context grows large, evaluate whether a sub-task or new session would be more effective;
- place the most critical instructions and constraints at the beginning of loaded context.

Reference `.agents/orchestration/context-budget-policy.md` for detailed loading strategy.

## Error classification

When recording errors, classify them:

| Class | Examples |
|---|---|
| `client` | invalid input, missing required field, unauthorized request |
| `domain` | business rule violation, state conflict, insufficient permissions |
| `infrastructure` | database timeout, network failure, service unavailable |
| `unexpected` | unhandled exception, null reference, type mismatch |
| `agent` | reasoning error, tool misuse, context overflow, doom loop |

This classification supports both application error handling and agent self-diagnosis.

## Performance awareness

When agent work involves performance-sensitive changes:

- capture baseline measurements before optimization;
- record the specific metrics improved;
- document trade-offs made for performance gains;
- reference `.agents/skills/performance/SKILL.md` for detailed guidance.

## Drift detection

Monitor for signs that agent behavior has drifted from intended patterns:

- task scope expanding beyond the original request without explicit authorization;
- repeated failures without approach changes;
- actions that contradict established project rules or ADRs;
- generation of artifacts not required by the task;
- circular reasoning or redundant operations.

When drift is detected, pause, reassess the task plan, and realign with project rules before continuing.
