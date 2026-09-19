# File Manifest

Every file listed below is included in this package. Each has one primary responsibility. Update this manifest when the structure changes.

## Package-level

| Path | Purpose |
|---|---|
| `README.md` | Explains the architecture, installation, source-of-truth hierarchy, and completion contract. |
| `FILE_MANIFEST.md` | Gives a one-line purpose for every packaged file. |
| `global/GEMINI.md` | Defines cross-project agent behavior and durable engineering principles. |

## Workspace bridge

| Path | Purpose |
|---|---|
| `workspace-template/AGENTS.md` | Gives general-purpose agents a compact entry point into the same memory, architecture, rules, and version-matched Next.js documentation contract. |
| `workspace-template/.nvmrc` | Declares the project's Node.js version for local tooling and CI. Update to match your project's required version. |

## Rules

| Path | Purpose |
|---|---|
| `.agents/rules/00-core.md` | Defines non-negotiable engineering and agent behavior that applies to meaningful work. |
| `.agents/rules/01-project-context.md` | Requires reconstruction of project intent and current context before implementation. |
| `.agents/rules/02-tech-stack.md` | Establishes the default stack and version-management policy. |
| `.agents/rules/03-architecture.md` | Defines structural architecture, module boundaries, dependency direction, and evolution rules. |
| `.agents/rules/04-coding.md` | Defines maintainable TypeScript/JavaScript coding conventions. |
| `.agents/rules/05-naming.md` | Defines consistent names for code, APIs, files, data, and Git artifacts. |
| `.agents/rules/06-uiux.md` | Defines accessible, responsive, cohesive interface requirements for React/Tailwind/shadcn. |
| `.agents/rules/07-security.md` | Defines mandatory secure-development constraints for web, API, auth, data, and dependencies. |
| `.agents/rules/08-git.md` | Defines safe source-control handling, diff hygiene, and commit discipline. |
| `.agents/rules/09-testing.md` | Defines risk-based test requirements and evidence expectations. |
| `.agents/rules/10-verification.md` | Defines the completion gate and required objective evidence. |
| `.agents/rules/11-project-memory.md` | Defines how durable knowledge is read, classified, and synchronized. |
| `.agents/rules/12-requirements.md` | Defines requirements interpretation, ambiguity handling, assumptions, and acceptance criteria discipline. |
| `.agents/rules/13-agent-safety.md` | Defines AI-agent-specific safety: prompt injection defense, excessive agency prevention, output sanitization, and OWASP LLM alignment. |
| `.agents/rules/14-observability.md` | Defines agent execution tracing, context budget awareness, error classification, and drift detection. |

## Skills

| Path | Purpose |
|---|---|
| `.agents/skills/project-init/SKILL.md` | Initializes a new repository with correct structure, context, conventions, and state. |
| `.agents/skills/requirements-discovery/SKILL.md` | Turns vague product ideas into explicit, testable requirements. |
| `.agents/skills/requirements-analysis/SKILL.md` | Analyzes requirements for scope, actors, workflows, constraints, risks, and gaps. |
| `.agents/skills/prd-analysis/SKILL.md` | Converts an existing PRD into an implementation-ready product/engineering specification. |
| `.agents/skills/acceptance-criteria/SKILL.md` | Converts behavior into objective, testable acceptance conditions. |
| `.agents/skills/planning/SKILL.md` | Converts approved requirements into an architecture-aware execution plan and task graph. |
| `.agents/skills/feature-development/SKILL.md` | Executes a feature end-to-end from context loading through implementation and memory sync. |
| `.agents/skills/frontend/SKILL.md` | Implements Next.js/React frontend behavior using the project architecture. |
| `.agents/skills/uiux/SKILL.md` | Builds polished, responsive, accessible interfaces with Tailwind and shadcn/ui. |
| `.agents/skills/backend/SKILL.md` | Implements Express backend modules, middleware, services, and operational behavior. |
| `.agents/skills/api/SKILL.md` | Designs and implements predictable, validated, versioned HTTP API contracts. |
| `.agents/skills/database/SKILL.md` | Designs MongoDB/Mongoose schemas, indexes, queries, and data-access patterns. |
| `.agents/skills/bug-fix/SKILL.md` | Handles defect resolution from reproduction through regression proof. |
| `.agents/skills/debugging/SKILL.md` | Performs root-cause investigation with evidence-driven hypotheses. |
| `.agents/skills/testing/SKILL.md` | Selects and executes risk-appropriate unit, integration, API, and E2E tests. |
| `.agents/skills/verification/SKILL.md` | Produces objective verification evidence and acceptance-criteria status. |
| `.agents/skills/code-review/SKILL.md` | Reviews changes for correctness, security, architecture, maintainability, and regression risk. |
| `.agents/skills/security/SKILL.md` | Performs secure design and implementation review against OWASP/NIST-aligned controls. |
| `.agents/skills/git/SKILL.md` | Performs safe branching, commit, diff, merge, and repository operations. |
| `.agents/skills/documentation/SKILL.md` | Maintains technical docs, API docs, ADRs, and project knowledge. |
| `.agents/skills/deployment/SKILL.md` | Prepares and verifies production release, configuration, health, rollback, and smoke-check concerns. |
| `.agents/skills/project-memory/SKILL.md` | Performs the durable memory synchronization step after meaningful work. |
| `.agents/skills/quality-gates/SKILL.md` | Evaluates agent output quality through self-assessment, trajectory analysis, regression detection, and CI/CD gating. |
| `.agents/skills/refactoring/SKILL.md` | Performs behavior-preserving code transformations with characterization testing and scope control. |
| `.agents/skills/performance/SKILL.md` | Measures, analyzes, and optimizes performance across frontend, backend, and database layers. |

## Orchestration

| Path | Purpose |
|---|---|
| `.agents/orchestration/task-classifier.md` | Classifies work so only relevant capabilities and context are activated. |
| `.agents/orchestration/context-router.md` | Routes the minimum sufficient context for a task. |
| `.agents/orchestration/decision-policy.md` | Defines act/infer/research/ask boundaries. |
| `.agents/orchestration/checkpoint-policy.md` | Defines autonomous versus approval-required actions. |
| `.agents/orchestration/task-lifecycle.md` | Defines the canonical stateful lifecycle from intake to completion. |
| `.agents/orchestration/memory-sync-policy.md` | Defines when and how durable project memory must be updated. |
| `.agents/orchestration/parallel-work-policy.md` | Defines safe parallel execution and conflict conditions. |
| `.agents/orchestration/worktree-policy.md` | Defines safe worktree isolation and reconciliation behavior when worktrees are used. |
| `.agents/orchestration/role-registry.md` | Defines logical roles and their normal skill/context responsibilities. |
| `.agents/orchestration/verification-schema.json` | Machine-readable contract for task verification evidence. |
| `.agents/orchestration/context-budget-policy.md` | Defines context window management, hierarchical loading, and token optimization strategy. |
| `.agents/orchestration/error-recovery-policy.md` | Defines graduated failure recovery with detect-diagnose-isolate-repair-learn cycle. |
| `.agents/orchestration/multi-agent-policy.md` | Defines sub-agent delegation, handoff protocol, and multi-agent coordination patterns. |
| `.agents/orchestration/agent-operating-contract.md` | Defines the canonical 11-phase task execution sequence and maps all policies to their phases. |

## State

| Path | Purpose |
|---|---|
| `.agents/state/project.json` | Stores project lifecycle and current phase metadata. |
| `.agents/state/tasks.json` | Stores tasks, dependencies, status, and outputs. |
| `.agents/state/blockers.json` | Stores unresolved blockers and their disposition. |
| `.agents/state/retries.json` | Stores failed attempts, reasons, and retry policy state. |
| `.agents/state/events.jsonl` | Stores append-only execution events for traceability. Starts empty; events are recorded during actual execution. |
| `.agents/state/events.schema.json` | JSON Schema defining the structure and allowed values for events in `events.jsonl`. |
| `.agents/state/agents.json` | Stores active logical roles/tasks and ownership state. |

## Templates

| Path | Purpose |
|---|---|
| `.agents/templates/prd-template.md` | Produces a complete product requirements document. |
| `.agents/templates/requirements-template.md` | Captures raw-to-structured requirements before a formal PRD exists. |
| `.agents/templates/feature-template.md` | Specifies a feature, acceptance criteria, dependencies, risks, and implementation boundaries. |
| `.agents/templates/bug-template.md` | Captures reproducible defect information and expected behavior. |
| `.agents/templates/api-template.md` | Documents an HTTP API endpoint contract and operational requirements. |
| `.agents/templates/component-template.md` | Specifies a reusable UI component and its state/accessibility contract. |
| `.agents/templates/test-template.md` | Defines tests using behavior-focused scenarios and evidence. |
| `.agents/templates/review-template.md` | Standardizes code review findings and verification status. |
| `.agents/templates/adr-template.md` | Standardizes durable architectural and technical decision records. |
| `.agents/templates/task-template.md` | Standardizes executable task records for the task graph. |
| `.agents/templates/verification-template.md` | Standardizes human-readable verification reports and evidence capture. |
| `.agents/templates/incident-template.md` | Standardizes production incident reports with timeline, root cause, and prevention. |
| `.agents/templates/migration-template.md` | Standardizes data/schema/API migration planning with rollback and validation. |

## CI/CD

| Path | Purpose |
|---|---|
| `.github/workflows/ai-validation.yml` | GitHub Actions workflow for automated validation of AI-generated changes (format, lint, type-check, test, build, security). |

## Requirements

| Path | Purpose |
|---|---|
| `docs/requirements/INDEX.md` | Defines the canonical location and relationships for product requirements artifacts. |
| `docs/requirements/PRD.md` | Starter PRD document for the project's validated product requirements. |
| `docs/requirements/ACCEPTANCE_CRITERIA.md` | Optional cross-feature acceptance criteria register with verification status. |

## Project memory

| Path | Purpose |
|---|---|
| `docs/INDEX.md` | Entry point and navigation map for all project knowledge. |
| `docs/PROJECT_CONTEXT.md` | Records product purpose, users, scope, constraints, and high-level project facts. |
| `docs/ARCHITECTURE.md` | Records the actual chosen system architecture and structural boundaries. |
| `docs/CONVENTIONS.md` | Records established project-specific practices that should be applied consistently. |
| `docs/CURRENT_STATE.md` | Records what is completed, in progress, blocked, next, and known to be risky. |
| `docs/REFERENCES.md` | Lists external source material used by this project when version-sensitive guidance matters. |
| `docs/decisions/INDEX.md` | Indexes accepted, superseded, and proposed ADRs without replacing the individual ADR files. |

## Naming conventions (not packaged files)

These are naming patterns for files created during project execution:

| Pattern | When created |
|---|---|
| `docs/decisions/ADR-<NNN>-<decision-name>.md` | When a durable architectural or technical decision is made. Use the ADR template. |
