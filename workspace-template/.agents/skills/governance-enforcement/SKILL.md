---
name: governance-enforcement
id: SKILL-GOV-001
description: Resolve, record, validate, and enforce task-scoped governance requirements, quality gates, and completion criteria.
---

# Governance Enforcement Skill

<ROLE>
Operate as a Principal Governance Enforcement Engineer ensuring that every task satisfies its mandatory rules, skills, technology profiles, quality gates, and evidence requirements before completion.
</ROLE>

<MISSION>
Resolve task-scoped governance requirements during planning, record them in machine-readable state, validate evidence during verification, and enforce completion gates so that no task is marked complete without compliance proof.
</MISSION>

<WHEN_TO_USE>
- When initializing governance for a newly classified task.
- When resolving mandatory rules, skills, and technology profiles for a task plan.
- Before executing code modifications to verify action-space constraints.
- During task verification to validate quality gates and evidence.
- Before transitioning the current task record `.agents/state/tasks/TASK-ID.json` to `COMPLETED`.
</WHEN_TO_USE>

<WHEN_NOT_TO_USE>
- During initial repository bootstrap (`project-init` handles bootstrap).
- For passive code reading or directory inspection that makes no changes.
</WHEN_NOT_TO_USE>

<PRECONDITIONS>
### Prerequisites
- The current governed task must be registered in `.agents/state/tasks/TASK-ID.json`.
- Task classification must be established (`type` and `risk`) in the canonical task record.
- Repository stack must be detected in `.agents/state/stack.json`.

### Pre-flight Checklist
- [ ] Task ID exists and is unique
- [ ] Active stack profiles identified from `stack.json`
- [ ] Canonical policy ownership matrix reviewed (`policy-ownership.md`)
- [ ] Governance state record initialized in `.agents/state/governance/TASK-ID.json`
</PRECONDITIONS>

<INPUT_CONTRACT>
- `taskId`: Stable task identifier (e.g., `TASK-001`).
- `classification`: Task type and risk level.
- `stack`: Detected stack state from `stack.json`.
- `acceptanceCriteria`: Specific testable criteria for the task.
</INPUT_CONTRACT>

<SOURCE_OF_TRUTH>
- Governance policy: `.agents/orchestration/governance-enforcement-policy.md`
- Policy ownership: `.agents/orchestration/policy-ownership.md`
- Task state machine: `.agents/orchestration/task-lifecycle.md`
- Governance state: `.agents/state/governance/TASK-ID.json`
</SOURCE_OF_TRUTH>

<CONTEXT_POLICY>
Load only the minimum sufficient context required for governance resolution:
- Always load: `governance-enforcement-policy.md`, `context-router.md`, `policy-ownership.md`.
- Load mapped domain rules and profiles according to the task domain.
- Exclude unrelated domain skills during governance evaluation.
</CONTEXT_POLICY>

<ACTION_SPACE_CONSTRAINTS>
  <READ>
    <ALLOWED>Inspect repository state, source files, test outputs, and diffs.</ALLOWED>
  </READ>
  <WRITE>
    <ALLOWED>Update canonical governance records (`.agents/state/governance/<task-id>.json`) and canonical task records (`.agents/state/tasks/<task-id>.json`), and synchronize aggregates via `aggregate-state.py`.</ALLOWED>
  </WRITE>
  <EXECUTE>
    <ALLOWED>Run `validate-governance.py` and canonical verification commands.</ALLOWED>
  </EXECUTE>
</ACTION_SPACE_CONSTRAINTS>

<TOOL_POLICY>
Use capability-oriented tool interactions. Inspect repository state files, run validation commands, and record state updates directly.
</TOOL_POLICY>

<NON_NEGOTIABLES>
- Canonical per-task governance records are authoritative.
- Quality gates cannot be passed with empty, missing, or trivial evidence.
- Every task must have an associated governance record before completion.
- Fail closed on missing, malformed, or invalid governance data.
</NON_NEGOTIABLES>

<PROCEDURE>
## 1. Governance Resolution (Pre-Implementation)
1. Read the task only from `.agents/state/tasks/<task-id>.json`.
2. Determine applicable stable Rule IDs from `.agents/orchestration/context-router.md`.
3. Determine applicable stable Skill IDs from the domain mapping.
4. Match required technology profiles from `.agents/state/stack.json`.
5. Check for relevant existing ADRs in `docs/decisions/`.
6. Determine applicable quality gates (lint, typecheck, test, build, security).
7. Determine if human approval is required based on risk and action space.
8. Write the governance record to canonical file `.agents/state/governance/<task-id>.json` with `governanceStatus: "ready"` (and sync aggregate via `aggregate-state.py`).

## 2. In-Flight Governance Monitoring
1. When implementation begins, update `governanceStatus` to `"in_progress"` in `.agents/state/governance/<task-id>.json`.
2. Ensure edits remain strictly within the resolved action-space constraints.
3. If new dependencies or architectural choices emerge, update the governance record.

## 3. Governance Validation (Pre-Completion)
1. When implementation completes, update `governanceStatus` to `"verification_required"`.
2. Execute all required quality gates and record results + evidence in `qualityGates`.
3. Confirm that all acceptance criteria have verifiable execution evidence.
4. Verify that durable memory sync is complete (or explicitly not required).
5. Run automated validation: `python3 .agents/skills/quality-gates/scripts/validate-governance.py .agents/state/governance/<task-id>.json .agents/state/tasks/<task-id>.json` (or run against `.agents/state`).
6. IF validation returns `PASS`: update `governanceStatus` to `"complete"` in `.agents/state/governance/<task-id>.json`.
7. IF validation returns `FAIL` or `BLOCKED`: do not allow task completion.
</PROCEDURE>

<DECISION_RULES>
- IF any required quality gate is missing or failed:
    Task cannot transition to `complete`. Set `governanceStatus: "failed"`.
- IF human approval is required but not recorded as satisfied:
    Task cannot proceed. Set `governanceStatus: "blocked"`.
- IF a required check cannot run due to missing local tools:
    Record gate status as `blocked` or `not_applicable` with documented evidence; never record `passed`.
- IF an ADR conflict is detected:
    Follow ADR conflict procedure: state conflict, evaluate trade-offs, author superseding ADR before completing.
</DECISION_RULES>

<FAILURE_RECOVERY>
When governance fails:
1. Isolate the specific missing gate or failing check from validator output.
2. If evidence is missing: re-run the check and capture command output.
3. If test/gate failed: diagnose root cause, repair code, and re-run.
4. If approval missing: request human approval via checkpoint protocol.
5. Re-run `validate-governance.py` until clean `PASS`.
</FAILURE_RECOVERY>

<VERIFICATION_POLICY>
The completion gate evaluates every applicable governance invariant and verification gate defined by the canonical policy. A task is verified only when `validate-governance.py` exits with code 0 and all required evidence is present.
</VERIFICATION_POLICY>

<EVIDENCE_REQUIREMENTS>
Every quality gate must record:
- Gate ID (e.g. `GATE-TYPECHECK`, `GATE-LINT`, `GATE-TEST`, `GATE-BUILD`, `GATE-SECURITY`)
- Gate name (e.g. `typecheck`, `lint`, `test`, `build`, `security`)
- Required status (`true` | `false`)
- Execution status (`passed`, `failed`, `blocked`, `not_applicable`, `not_configured`, `unknown`)
- Executed command (if applicable) and exit code (`exitCode: 0` for passed commands)
- Objective evidence string (command snippet, test counts, or tool output)
- Explicit reason string (mandatory whenever status is `not_applicable` or `not_configured`)
- ISO 8601 timestamp
</EVIDENCE_REQUIREMENTS>

<STATE_POLICY>
All governed work must be maintained in canonical per-task `.agents/state/governance/TASK-ID.json` conforming to `governance.schema.json`. Aggregate `governance.json` is a derived view and must not be used to bypass task-scoped governance.
</STATE_POLICY>

<OUTPUT_CONTRACT>
Governance evaluation produces:
1. Task ID and classification.
2. Resolved Rule IDs and Skill IDs.
3. Quality gates executed with status and evidence.
4. Memory sync confirmation.
5. Governance verdict: `PASS`, `BLOCKED`, or `FAILED`.
</OUTPUT_CONTRACT>
