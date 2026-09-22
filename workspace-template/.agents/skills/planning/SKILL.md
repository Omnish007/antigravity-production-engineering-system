---
name: planning
id: SKILL-PLAN-001
description: Create an implementation-ready plan with dependencies, architecture impact, task sequencing, risks, and verification strategy.
---

# Planning Skill

<MISSION>
Create an implementation-ready plan with dependencies, architecture impact, task sequencing, risks, and verification strategy.
</MISSION>

<WHEN_TO_USE>
Activate this skill when executing tasks requiring planning capabilities, workflows, or architectural guidance.
</WHEN_TO_USE>

<PRECONDITIONS>
### Prerequisites
- Active task in .agents/state/tasks.json must be IN_PROGRESS.
    - TASK_STARTED event must be recorded in .agents/state/events.jsonl.

### Pre-flight Checklist
- [ ] Approved requirements or user request available
- [ ] Project context (docs/PROJECT_CONTEXT.md), architecture (docs/ARCHITECTURE.md), and conventions (docs/CONVENTIONS.md) available
- [ ] Active stack snapshot (.agents/state/stack.json) and relevant technology profiles identified
- [ ] Context router (.agents/orchestration/context-router.md) available for rule and skill mapping
- [ ] Current tasks state (.agents/state/tasks.json) inspected for active DAG state
</PRECONDITIONS>

<NON_NEGOTIABLES>
- Decompose user goals into an atomic Directed Acyclic Graph (DAG) in tasks.json.
- Every task must have explicit dependencies, acceptance criteria, and expected outputs.
- Never create tasks that mix multiple unrelated architectural boundaries.
- If the plan involves decisions meeting the Canonical ADR Trigger (Type 1 OR any 2 of D1, D3, D4), an ADR creation task MUST be sequenced BEFORE implementation tasks.
- The implementation plan MUST include a `## Governed System Compliance` section documenting:
  1. `.agents/orchestration/context-router.md` loaded into context.
  2. Active stack snapshot from `.agents/state/stack.json` and loaded technology profiles (`.agents/technology/profiles/`).
  3. All mapped Mandatory Rules (`.agents/rules/*.md`) inspected and loaded into context.
  4. All mapped Atomic Skill Bundles (`.agents/skills/*/SKILL.md`) inspected and loaded into context.
  5. Canonical ADR Significance evaluation (D1-D4).
</NON_NEGOTIABLES>

<PROCEDURE>
## Inputs

Use approved requirements, acceptance criteria, project context, architecture, conventions, and relevant ADRs.

## Procedure

1. Map requirements to system boundaries.
2. Identify affected modules/files.
3. Identify data-model/API/UI changes.
4. Identify migrations and backward compatibility needs.
5. Identify security and observability implications.
6. Determine dependencies and safe parallelism.
7. Decompose into small, assignable tasks.
8. Order tasks by dependency, risk, and feedback value.
9. Define verification for each task and integrated verification for the feature.
10. Identify decisions that need an ADR before implementation.

## Task quality

Each task should include:

- stable ID;
- objective;
- scope;
- dependencies;
- expected files/modules;
- acceptance criteria;
- test strategy;
- verification command(s) where known;
- owner/role;
- risk notes.

## Avoid

- tasks that merely say "implement feature";
- arbitrary hour estimates presented as facts;
- decompositions that split tightly coupled changes unnaturally;
- parallel tasks that touch the same files without isolation.

## Output

Produce a task graph and a concise execution order. Store the plan in the project's chosen planning document and mirror tracked execution state into `.agents/state/tasks.json`.
</PROCEDURE>

<VERIFICATION_POLICY>
### Exit Criteria
Structured tasks.json DAG approved and emitted to events.jsonl.
</VERIFICATION_POLICY>

<DELIVERABLES>
- Detailed implementation plan artifact with risk assessment and dependency ordering.
- Executable task graph recorded in .agents/state/tasks.json.
</DELIVERABLES>
