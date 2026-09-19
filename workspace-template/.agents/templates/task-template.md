# Task Record

```yaml
id: TASK-000
name: <short-name>
type: feature  # feature | bugfix | refactor | performance | review | deployment | infrastructure | migration | documentation
status: PENDING  # PENDING | READY | IN_PROGRESS | VERIFYING | COMPLETED | FAILED | BLOCKED | CANCELLED
riskLevel: medium  # low | medium | high | critical
priority: P1  # P0 (urgent) | P1 (high) | P2 (normal) | P3 (low)
owner: <logical-role>
dependencies: []
expectedOutputs: []
acceptanceCriteria: []
verification: []
risks: []
createdAt: <ISO 8601>
updatedAt: <ISO 8601>
completedAt: null
notes: []
```

## Context

Brief description of the task purpose and any background information needed.

## Scope

### In scope

### Out of scope

## Approach

Outline of the planned implementation approach.

## Definition of done

- acceptance criteria verified with evidence;
- required checks executed (format, lint, type-check, test, build);
- diff reviewed for unintended changes;
- security impact assessed for high/critical risk tasks;
- performance impact assessed where relevant;
- blockers recorded if any;
- memory synchronized if durable knowledge changed;
- state files updated (tasks.json, events.jsonl).

## Evidence

Link to verification report, test output, or other evidence when task is complete.

## Related artifacts

- Requirements:
- ADRs:
- Feature spec:
- Verification report:
