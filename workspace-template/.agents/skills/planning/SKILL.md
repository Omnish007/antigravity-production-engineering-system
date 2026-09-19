---
name: planning
description: Create an implementation-ready plan with dependencies, architecture impact, task sequencing, risks, and verification strategy.
---

# Planning Skill

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
