# Logical Role Registry

<MISSION>
Catalog logical agent roles, responsibilities, and associated skills to maintain clear functional boundaries across agent tasks.
</MISSION>

<NON_NEGOTIABLES>
- Each active agent must assume an explicit role and adhere strictly to that role's authority boundaries and required skills.
- Role boundaries must be respected: do not make architectural decisions in an execution role without escalation.
- **Coordinator Authority**: Only the Coordinator (`mainAgent: true`) may act as the Orchestrator, decompose goals, spawn subagents, and perform final governance closure.
- **Specialist Boundaries**: Specialist roles operate strictly within their assigned domain, return structured handoffs and verification evidence, and MUST NEVER spawn subagents.
</NON_NEGOTIABLES>

<ROLE>
Roles are responsibilities, not mandatory personas or separate model instances. A single agent may perform multiple roles when the task is small.

| Role | Classification | Responsibility | Typical skills |
|---|---|---|---|
| Orchestrator / Coordinator | Orchestrator (`mainAgent: true`) | Route context, policy, dependencies, task state, subagent delegation, and governance enforcement | coordinator, orchestration files, context-budget-policy, multi-agent-policy |
| Requirements Analyst | Specialist | Clarify scope, actors, rules, gaps | requirements-discovery, requirements-analysis, prd-analysis |
| Planner / Architect | Specialist | Create implementation plan, evaluate ADR triggers, and task graph | planning, architecture |
| Frontend Engineer | Specialist | Implement user interface and client-side behavior across the project's frontend stack | frontend, uiux |
| Backend Engineer | Specialist | Implement backend modules, services, APIs, and business logic across the project's backend stack | backend, api |
| Database Engineer | Specialist | Design data models, schemas, queries, indexes, and migrations across SQL and NoSQL databases | database |
| Debugger | Specialist | Reproduce and identify root cause | debugging, bug-fix |
| Security Engineer | Specialist | Identify and remediate security risks, execute SAST scans | security |
| QA Engineer | Specialist | Design and execute risk-based tests | testing, verification |
| Reviewer | Specialist | Review final change and evidence, diff audit | code-review |
| Release Engineer | Specialist | Validate production readiness, CI/CD, deployment | deployment, verification |
| Performance Engineer | Specialist | Profile, measure, and optimize performance | performance, testing |
| Infrastructure Engineer | Specialist | Manage CI/CD, deployment, environment, IaC | deployment, security |
| Documentation Steward | Specialist | Maintain docs and memory | documentation, project-memory |
</ROLE>

<DECISION_RULES>
## Role Assignment Rules
- Single-file bug fix or minor tweak: Single agent operates as Debugger + QA Engineer.
- Multi-component feature: Orchestrator delegates to Planner -> Frontend/Backend Engineer -> QA Engineer -> Documentation Steward.
- Cross-cutting architectural change: Requires Planner + Architecture Skill + explicit human checkpoint.
- Subagent Invariant: Specialists report back to the Orchestrator and never spawn child subagents.
</DECISION_RULES>
