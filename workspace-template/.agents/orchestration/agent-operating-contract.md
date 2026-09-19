# Agent Operating Contract

## Purpose

Define the canonical execution sequence for any meaningful task. This is the master dependency chain that all other orchestration policies, rules, and skills feed into. Every task follows this contract unless a rule explicitly defines a deviation.

## Execution sequence

```text
1. RECEIVE    → Parse the task request.
2. CLASSIFY   → Determine task type, risk level, required skills.
3. LOAD       → Route minimum sufficient context per budget policy.
4. PLAN       → Design the approach; get approval for high/critical risk.
5. IMPLEMENT  → Execute the plan using activated skills.
6. TEST       → Run appropriate verification for the risk level.
7. VERIFY     → Produce evidence against acceptance criteria.
8. REVIEW     → Self-review diff, quality gates, and trajectory.
9. SYNC       → Update project memory if durable knowledge changed.
10. UPDATE    → Update state files (tasks, events, blockers).
11. COMPLETE  → Report results and evidence.
```

## Phase details

### 1. RECEIVE

- Read the task request carefully.
- Identify explicit and implicit requirements.
- Note acceptance criteria if provided.

### 2. CLASSIFY

Reference: `.agents/orchestration/task-classifier.md`

- Determine task type (feature, bugfix, refactor, performance, review, deployment, infrastructure, migration, documentation).
- Assess risk level (low, medium, high, critical).
- Risk determines the depth of subsequent phases.

### 3. LOAD

References: `.agents/orchestration/context-router.md`, `.agents/orchestration/context-budget-policy.md`

- Load context groups for the classified task type.
- Follow hierarchical loading order: safety → core rules → task rules → project memory → source files.
- Apply minimum-sufficient-context principle; do not bulk-load.
- Verify version-sensitive documentation when framework behavior matters.

### 4. PLAN

References: `.agents/orchestration/decision-policy.md`, `.agents/orchestration/checkpoint-policy.md`

- For **low risk**: plan mentally, act directly.
- For **medium risk**: outline the approach, then act.
- For **high risk**: produce an explicit plan, review against architecture and ADRs.
- For **critical risk**: produce a detailed plan, request human approval before proceeding.

### 5. IMPLEMENT

References: activated skills, `.agents/rules/04-coding.md`, `.agents/rules/05-naming.md`

- Follow the plan step by step.
- Apply coding conventions, naming standards, and architecture rules.
- Verify incrementally; do not defer all checks to the end.
- If errors occur, follow `.agents/orchestration/error-recovery-policy.md`.

### 6. TEST

Reference: `.agents/rules/09-testing.md`, `.agents/skills/testing/SKILL.md`

- Run verification appropriate to the change and risk level.
- For low risk: focused tests on changed behavior.
- For medium risk: focused + integration tests.
- For high risk: focused + integration + security/accessibility where relevant.
- For critical risk: full test suite + deployment verification.

### 7. VERIFY

References: `.agents/rules/10-verification.md`, `.agents/skills/verification/SKILL.md`

- Map each acceptance criterion to evidence.
- Run format, lint, type-check, build.
- Record command outputs and exit codes.
- Produce a verification report using `.agents/templates/verification-template.md`.

### 8. REVIEW

References: `.agents/skills/quality-gates/SKILL.md`, `.agents/skills/code-review/SKILL.md`

- Review the final diff for unintended changes.
- Evaluate quality gates: scope discipline, security, performance, accessibility.
- Evaluate trajectory: was the approach efficient? Any doom loops or scope creep?
- For critical risk: request human code review.

### 9. SYNC

References: `.agents/rules/11-project-memory.md`, `.agents/orchestration/memory-sync-policy.md`, `.agents/skills/project-memory/SKILL.md`

- Determine if durable knowledge changed.
- Update the appropriate canonical document(s).
- Do not update memory speculatively; update only when actual execution changed a documented fact.

### 10. UPDATE

References: `.agents/state/tasks.json`, `.agents/state/events.jsonl`

- Update task status if using tracked tasks.
- Log significant events.
- Record blockers if any remain.
- Update retry records if recovery occurred.

### 11. COMPLETE

- Summarize what was done, what was verified, what remains (if anything).
- Report trajectory: path taken, recovery actions, decisions made.
- Reference evidence produced.

## Risk determines depth

| Phase | Low | Medium | High | Critical |
|---|---|---|---|---|
| Plan | implicit | outlined | explicit | detailed + approval |
| Test | focused | focused + integration | broad | full suite |
| Review | self-review | self-review | self-review + gates | human review |
| Sync | if needed | if needed | always evaluate | always update |

## Error handling

At any phase, if an error occurs:

1. Follow `.agents/orchestration/error-recovery-policy.md`.
2. Do not skip phases to recover; return to the earliest affected phase.
3. If recovery fails after exhausting the escalation ladder, record a blocker and request human input.

## Multi-agent coordination

When work is delegated to sub-agents:

1. Each sub-agent follows this same contract for its assigned sub-task.
2. The orchestrating agent is responsible for phases 2, 3, 8 (integration review), 9, 10, and 11 at the overall task level.
3. Follow `.agents/orchestration/multi-agent-policy.md` for handoff and conflict prevention.

## Policy index

This contract depends on the following policies. Read them when their phase is reached:

| Policy | Used in phases |
|---|---|
| `task-classifier.md` | 2 (CLASSIFY) |
| `context-router.md` | 3 (LOAD) |
| `context-budget-policy.md` | 3 (LOAD) |
| `decision-policy.md` | 4 (PLAN) |
| `checkpoint-policy.md` | 4 (PLAN), 8 (REVIEW) |
| `error-recovery-policy.md` | 5 (IMPLEMENT), any error |
| `memory-sync-policy.md` | 9 (SYNC) |
| `multi-agent-policy.md` | all, when sub-agents are involved |
| `task-lifecycle.md` | 10 (UPDATE) |
| `parallel-work-policy.md` | 5 (IMPLEMENT), when concurrent work exists |
| `worktree-policy.md` | 5 (IMPLEMENT), when worktree isolation is used |
