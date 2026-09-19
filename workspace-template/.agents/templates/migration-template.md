# Migration Plan

## Metadata

- Migration ID:
- Name:
- Status: Planning | Ready | In progress | Validating | Complete | Rolled back
- Risk level: Low | Medium | High | Critical
- Owner:
- Estimated duration:
- Scheduled date:
- Related ADR:

## Scope

### What is changing

### What is not changing

### Affected systems/services

### Affected data

- Collections/tables affected:
- Estimated document/row count:
- Embedded document changes:
- Reference/relationship changes:

## Pre-migration checklist

- [ ] Backup/snapshot taken and verified
- [ ] Rollback procedure documented and tested
- [ ] Stakeholders notified
- [ ] Maintenance window scheduled (if needed)
- [ ] Monitoring/alerting configured for migration metrics
- [ ] Dependencies identified and coordinated
- [ ] Feature flags in place for gradual rollout (if applicable)
- [ ] Migration script tested against representative data volume
- [ ] Idempotency verified (safe to re-run if interrupted)

## Backward compatibility

- Is the migration backward-compatible?
- If not, what is the coordination plan for dependent systems?
- Can the old and new versions coexist during migration?
- Can the application read/write both old and new formats during transition?

## Migration strategy

### Expand/migrate/contract (preferred for zero-downtime)

```text
Phase 1 (Expand): Deploy new schema/structure alongside old. Application writes both formats.
Phase 2 (Migrate): Backfill existing data to new format. Verify completeness.
Phase 3 (Contract): Remove old format support. Clean up dual-write code.
```

### Big-bang (when coexistence is not possible)

```text
1. Schedule maintenance window
2. Take backups
3. Execute migration
4. Validate
5. Resume service
```

## Rollback strategy

- Is rollback possible?
- What is the rollback procedure?
- What is the maximum rollback window?
- What data would be lost on rollback?
- Has rollback been tested?
- Is forward-fix preferable to rollback for this migration?

## Data validation plan

| Validation check | Method | Expected result |
|---|---|---|
| Document/record count | Aggregation/query comparison | Old count ≤ New count (≤ accounts for concurrent writes) |
| Data integrity | Sampling + field-level comparison | No corruption or data loss |
| Reference integrity | Application-level reference check | No orphaned references or broken links |
| Embedded document structure | Schema validation or spot checks | All documents match expected shape |
| Index coverage | `explain()` on critical queries | Queries use expected indexes |
| Duplicate detection | Aggregation on unique fields | No unintended duplicates created |
| Application behavior | Smoke test of critical paths | All reads/writes function correctly |
| Performance | Benchmark critical queries pre/post | No degradation beyond threshold |

## Concurrent write safety

- How are concurrent writes handled during migration?
- Is the migration idempotent (safe to re-run)?
- Are there race conditions between the migration and live traffic?
- Is a read/write lock or pause needed?

## Cutover procedure

Step-by-step execution plan:

1.
2.
3.

## Post-migration verification

- [ ] Data validation checks pass
- [ ] Application smoke tests pass
- [ ] Performance benchmarks acceptable
- [ ] No error rate increase
- [ ] Monitoring confirms healthy state
- [ ] Index usage verified with `explain()`
- [ ] Rollback artifacts cleaned up (after confidence period)
- [ ] Dual-write code removed (after confidence period)

## Communication plan

| Audience | Message | Timing |
|---|---|---|
| Engineering team | Migration scheduled | Before |
| Stakeholders | Migration complete | After |
| Users (if visible) | Planned maintenance | Before |

## Risks

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| | | | |

## Evidence

Record actual migration execution details here after completion:

- Start time:
- End time:
- Duration:
- Documents/records processed:
- Issues encountered:
- Rollback needed: yes/no
- Validation results:
- Memory/ADR updates made:
