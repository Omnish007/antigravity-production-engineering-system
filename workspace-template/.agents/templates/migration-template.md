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

## Pre-migration checklist

- [ ] Backup/snapshot taken and verified
- [ ] Rollback procedure documented and tested
- [ ] Stakeholders notified
- [ ] Maintenance window scheduled (if needed)
- [ ] Monitoring/alerting configured for migration metrics
- [ ] Dependencies identified and coordinated
- [ ] Feature flags in place for gradual rollout (if applicable)

## Backward compatibility

- Is the migration backward-compatible?
- If not, what is the coordination plan for dependent systems?
- Can the old and new versions coexist during migration?

## Migration strategy

### Expand/migrate/contract (preferred for zero-downtime)

```text
Phase 1 (Expand): Deploy new structure alongside old
Phase 2 (Migrate): Move data/traffic to new structure
Phase 3 (Contract): Remove old structure
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

## Data validation plan

| Validation check | Method | Expected result |
|---|---|---|
| Record count matches | Query comparison | Old count == New count |
| Data integrity | Checksum/sampling | No corruption |
| Referential integrity | Foreign key / reference check | No orphans |
| Application behavior | Smoke test | All critical paths work |
| Performance | Benchmark comparison | No degradation |

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
- [ ] Rollback artifacts cleaned up (after confidence period)

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
- Issues encountered:
- Rollback needed: yes/no
- Validation results:
- Memory/ADR updates made:
