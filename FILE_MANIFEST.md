# File Manifest

Every file listed below is included in this package. Each has one primary responsibility. Update this manifest when the structure changes.

## Package-level

| Path | Purpose |
|---|---|
| `.gitignore` | Defines .gitignore specification and implementation. |
| `CHANGELOG.md` | Documents release history, migrations, and freeze specifications across all versions. |
| `COMPATIBILITY.md` | Defines COMPATIBILITY.md specification and implementation. |
| `FILE_MANIFEST.md` | Gives a one-line purpose for every packaged file. |
| `README.md` | Explains the architecture, installation, source-of-truth hierarchy, and completion contract. |
| `RESEARCH_BASIS.md` | Documents researched official sources, release lines, and architectural baselines. |
| `VALIDATION.md` | Documents comprehensive validation matrix, test results, and adversarial security assessments. |
| `VERSION.md` | Freezes the system specification at version 4.0.0. |
| `global/GEMINI.md` | Defines cross-project agent behavior and durable engineering principles. |
| `workspace-template/.agents/CONTROL_PLANE_MANIFEST.json` | Authoritative SHA-256 integrity manifest for protected control-plane files. |
| `workspace-template/.agents/agents/architect.md` | Defines architect.md specification and implementation. |
| `workspace-template/.agents/agents/code-reviewer.md` | Defines code-reviewer.md specification and implementation. |
| `workspace-template/.agents/agents/database-specialist.md` | Defines database-specialist.md specification and implementation. |
| `workspace-template/.agents/agents/implementer.md` | Defines implementer.md specification and implementation. |
| `workspace-template/.agents/agents/release-engineer.md` | Defines release-engineer.md specification and implementation. |
| `workspace-template/.agents/agents/researcher.md` | Defines researcher.md specification and implementation. |
| `workspace-template/.agents/agents/security-reviewer.md` | Defines security-reviewer.md specification and implementation. |
| `workspace-template/.agents/agents/test-engineer.md` | Defines test-engineer.md specification and implementation. |
| `workspace-template/.agents/hooks.json` | Defines hooks.json specification and implementation. |
| `workspace-template/.agents/validation/core/__init__.py` | Python package initializer for core governance and verification engine. |
| `workspace-template/.agents/validation/core/governance_core.py` | Authoritative governance evaluation engine enforcing task-scoped stop conditions and completion invariants. |
| `workspace-template/.agents/validation/core/verification_policy.py` | Executable verification policy engine implementing canonical gate registry and taxonomy. |
| `workspace-template/.agents/validation/core/workspace_resolver.py` | Deterministic workspace and governance root resolver enforcing explicit sentinels. |
| `workspace-template/.agents/validation/fixtures/invalid/contradictory-classification.json` | Defines contradictory-classification.json specification and implementation. |
| `workspace-template/.agents/validation/fixtures/invalid/fake-quality-gate.json` | Defines fake-quality-gate.json specification and implementation. |
| `workspace-template/.agents/validation/fixtures/invalid/fake-security-evidence.json` | Defines fake-security-evidence.json specification and implementation. |
| `workspace-template/.agents/validation/fixtures/invalid/missing-adr.json` | Defines missing-adr.json specification and implementation. |
| `workspace-template/.agents/validation/fixtures/invalid/missing-start-event.json` | Defines missing-start-event.json specification and implementation. |
| `workspace-template/.agents/validation/fixtures/invalid/missing-test.json` | Defines missing-test.json specification and implementation. |
| `workspace-template/.agents/validation/fixtures/invalid/ungrounded-approval.json` | Defines ungrounded-approval.json specification and implementation. |
| `workspace-template/.agents/validation/fixtures/invalid/unresolved-blocker.json` | Defines unresolved-blocker.json specification and implementation. |
| `workspace-template/.agents/validation/fixtures/valid/high-risk-task.json` | Defines high-risk-task.json specification and implementation. |
| `workspace-template/.agents/validation/fixtures/valid/migration-task.json` | Defines migration-task.json specification and implementation. |
| `workspace-template/.agents/validation/fixtures/valid/minimal-fast-task.json` | Defines minimal-fast-task.json specification and implementation. |
| `workspace-template/.agents/validation/fixtures/valid/standard-feature-task.json` | Defines standard-feature-task.json specification and implementation. |
| `workspace-template/.agents/validation/tests/test-lifecycle-simulation.py` | Defines test-lifecycle-simulation.py specification and implementation. |
| `workspace-template/.agents/validation/tests/test-validators.py` | Defines test-validators.py specification and implementation. |
| `workspace-template/.gitignore` | Defines .gitignore specification and implementation. |

## Workspace bridge

| Path | Purpose |
|---|---|
| `workspace-template/AGENTS.md` | Gives general-purpose agents a compact entry point into project memory, architecture, polyglot commands, and documentation contract. |

## Developer Preferences

| Path | Purpose |
|---|---|
| `workspace-template/.agents/preferences/developer-defaults.md` | Documents personal developer defaults with explicit precedence: Project Reality > Personal Preference. |

## Technology Catalog & Profiles

| Path | Purpose |
|---|---|
| `workspace-template/.agents/technology/README.md` | Architectural extension guide for adding and managing technology profiles. |
| `workspace-template/.agents/technology/profiles/backend/django.md` | Django production architecture, ORM query optimization, and settings modularity. |
| `workspace-template/.agents/technology/profiles/backend/express.md` | Express 5+ middleware architecture, route modularization, and error handling. |
| `workspace-template/.agents/technology/profiles/backend/fastapi.md` | FastAPI modern Python ASGI framework, Pydantic v2 validation, and async endpoints. |
| `workspace-template/.agents/technology/profiles/backend/fastify.md` | Fastify high-performance backend, schema-based serialization, and plugin architecture. |
| `workspace-template/.agents/technology/profiles/backend/go.md` | Go backend architecture, stdlib `net/http` / Gin, context propagation, and error handling. |
| `workspace-template/.agents/technology/profiles/backend/nestjs.md` | NestJS enterprise TypeScript backend, modular architecture, and dependency injection. |
| `workspace-template/.agents/technology/profiles/backend/node.md` | Node.js 22/24 LTS (26 Current), ESM, worker threads, async I/O, and diagnostic tooling. |
| `workspace-template/.agents/technology/profiles/backend/spring-boot.md` | Spring Boot 3/4 (Java 17-26), modular service architecture, JPA, and Virtual Threads. |
| `workspace-template/.agents/technology/profiles/database/dynamodb.md` | DynamoDB single-table design, partition/sort keys, GSIs, and bounded item sizes. |
| `workspace-template/.agents/technology/profiles/database/mongodb.md` | MongoDB document data modeling, indexing, aggregation pipeline, and replica set transactions. |
| `workspace-template/.agents/technology/profiles/database/mysql.md` | MySQL 8+ InnoDB architecture, indexing, isolation levels, and zero-downtime migrations. |
| `workspace-template/.agents/technology/profiles/database/postgresql.md` | PostgreSQL relational modeling, indexing (B-Tree, GIN, GiST), transactions, and migrations. |
| `workspace-template/.agents/technology/profiles/database/redis.md` | Redis in-memory cache, data structures, eviction policies, distributed locks, and pub/sub. |
| `workspace-template/.agents/technology/profiles/database/sqlite.md` | SQLite embedded database, WAL mode, single-writer concurrency, and pragmas. |
| `workspace-template/.agents/technology/profiles/deployment/aws.md` | AWS cloud deployment (ECS, Lambda, S3, CloudFront), IAM least-privilege, and CDK/Terraform. |
| `workspace-template/.agents/technology/profiles/deployment/docker.md` | Multi-stage Docker builds, non-root users, layer caching, and compose environments. |
| `workspace-template/.agents/technology/profiles/deployment/k8s.md` | Kubernetes manifests, Deployments, Services, Ingress, probes, and resource limits. |
| `workspace-template/.agents/technology/profiles/deployment/vercel.md` | Vercel Edge/Serverless deployment, routing, environment variables, and caching. |
| `workspace-template/.agents/technology/profiles/frontend/angular.md` | Angular 21/22+ Standalone Components, Signals, and Control Flow syntax. |
| `workspace-template/.agents/technology/profiles/frontend/nextjs.md` | Next.js 16+ App Router, Server/Client components, Server Actions, and Turbopack. |
| `workspace-template/.agents/technology/profiles/frontend/nuxt.md` | Nuxt 4+ full-stack Vue, auto-imports, SSR/SSG, and Nitro server engine. |
| `workspace-template/.agents/technology/profiles/frontend/react.md` | Modern React 19+, Hooks, Suspense, Actions, and Server Components. |
| `workspace-template/.agents/technology/profiles/frontend/sveltekit.md` | SvelteKit, Svelte 5 Runes, server routes, and progressive enhancement. |
| `workspace-template/.agents/technology/profiles/frontend/vue.md` | Vue 3 Composition API, `<script setup>`, Pinia, and Vite. |
| `workspace-template/.agents/technology/profiles/language/go.md` | Go idioms, interfaces, goroutines, channels, and error handling. |
| `workspace-template/.agents/technology/profiles/language/java.md` | Modern Java 21+, records, pattern matching, Sealed classes, and Virtual Threads. |
| `workspace-template/.agents/technology/profiles/language/javascript.md` | Modern ECMAScript (ES2024+), modules, async/await, and runtime safety. |
| `workspace-template/.agents/technology/profiles/language/python.md` | Python 3.12+ modern typing, async idioms, error modeling, and packaging. |
| `workspace-template/.agents/technology/profiles/language/rust.md` | Rust ownership, memory safety, lifetimes, traits, and error handling. |
| `workspace-template/.agents/technology/profiles/language/typescript.md` | TypeScript strict typing, generics, utility types, and compiler configuration. |
| `workspace-template/.agents/technology/registry.json` | Machine-readable registry cataloging all supported technologies, profiles, and versions. |

## Rules

| Path | Purpose |
|---|---|
| `workspace-template/.agents/rules/00-core.md` | Defines non-negotiable engineering and agent behavior that applies to meaningful work. |
| `workspace-template/.agents/rules/01-project-context.md` | Requires reconstruction of project intent and current context before implementation. |
| `workspace-template/.agents/rules/02-tech-stack.md` | Defines the universal stack-agnostic technology architecture, profile catalog, and version-management policy. |
| `workspace-template/.agents/rules/03-architecture.md` | Defines structural architecture, module boundaries, dependency direction, and evolution rules. |
| `workspace-template/.agents/rules/04-coding.md` | Defines maintainable, type-safe coding conventions across languages and paradigms. |
| `workspace-template/.agents/rules/05-naming.md` | Defines consistent names across languages, APIs, databases, and Git artifacts. |
| `workspace-template/.agents/rules/06-uiux.md` | Defines accessible, responsive, token-driven interface requirements across frontend technologies. |
| `workspace-template/.agents/rules/07-security.md` | Defines mandatory secure-development constraints for web, API, auth, data, and dependencies. |
| `workspace-template/.agents/rules/08-git.md` | Defines safe source-control handling, diff hygiene, and commit discipline. |
| `workspace-template/.agents/rules/09-testing.md` | Defines risk-based polyglot test requirements and evidence expectations. |
| `workspace-template/.agents/rules/10-verification.md` | Defines the completion gate and required objective evidence. |
| `workspace-template/.agents/rules/11-project-memory.md` | Defines how durable knowledge is read, classified, and synchronized. |
| `workspace-template/.agents/rules/12-requirements.md` | Defines requirements interpretation, ambiguity handling, assumptions, and acceptance criteria discipline. |
| `workspace-template/.agents/rules/13-agent-safety.md` | Defines AI-agent-specific safety: prompt injection defense, excessive agency prevention, output sanitization, and OWASP LLM alignment. |
| `workspace-template/.agents/rules/14-observability.md` | Defines agent execution tracing, context budget awareness, error classification, and drift detection. |
| `workspace-template/.agents/rules/RULE_ACTIVATION.md` | Authoritative catalog of all project rules, activation criteria, and precedence levels. |
| `workspace-template/.agents/rules/rule-activation.yaml` | Declarative matrix defining rule activation triggers, stable IDs, and domain mappings. |

## Skills

| Path | Purpose |
|---|---|
| `workspace-template/.agents/skills/acceptance-criteria/SKILL.md` | Converts behavior into objective, testable acceptance conditions. |
| `workspace-template/.agents/skills/api/SKILL.md` | Designs and implements predictable, versioned APIs across REST, GraphQL, gRPC, and event-driven protocols. |
| `workspace-template/.agents/skills/architecture/SKILL.md` | Designs decoupled, modular system architectures, evaluates pattern trade-offs, and authors ADRs. |
| `workspace-template/.agents/skills/backend/SKILL.md` | Implements production-grade backend modules across any runtime with explicit boundaries and resilience. |
| `workspace-template/.agents/skills/bug-fix/SKILL.md` | Handles defect resolution from reproduction through regression proof. |
| `workspace-template/.agents/skills/code-review/SKILL.md` | Reviews changes for correctness, security, architecture, maintainability, and regression risk. |
| `workspace-template/.agents/skills/database/SKILL.md` | Designs, models, and safely migrates Relational (SQL) and Document/NoSQL databases with zero downtime. |
| `workspace-template/.agents/skills/debugging/SKILL.md` | Performs root-cause investigation with evidence-driven hypotheses. |
| `workspace-template/.agents/skills/deployment/SKILL.md` | Prepares and verifies production release, configuration, health, rollback, and smoke-check concerns. |
| `workspace-template/.agents/skills/documentation/SKILL.md` | Maintains technical docs, API docs, ADRs, and project knowledge. |
| `workspace-template/.agents/skills/feature-development/SKILL.md` | Executes a feature end-to-end from context loading through implementation and memory sync. |
| `workspace-template/.agents/skills/frontend/SKILL.md` | Implements modern, accessible, high-performance frontend interfaces across any framework. |
| `workspace-template/.agents/skills/git/SKILL.md` | Performs safe branching, commit, diff, merge, and repository operations. |
| `workspace-template/.agents/skills/governance-enforcement/SKILL.md` | Defines SKILL.md specification and implementation. |
| `workspace-template/.agents/skills/performance/SKILL.md` | Measures, analyzes, and optimizes performance across frontend, backend, database, and caching tiers. |
| `workspace-template/.agents/skills/planning/SKILL.md` | Converts approved requirements into an architecture-aware execution plan and task graph. |
| `workspace-template/.agents/skills/prd-analysis/SKILL.md` | Converts an existing PRD into an implementation-ready product/engineering specification. |
| `workspace-template/.agents/skills/project-init/SKILL.md` | Inspects and initializes any repository with correct structure, detected tech stack, context, and state. |
| `workspace-template/.agents/skills/project-memory/SKILL.md` | Performs the durable memory synchronization step after meaningful work. |
| `workspace-template/.agents/skills/quality-gates/SKILL.md` | Evaluates agent output quality through self-assessment, trajectory analysis, regression detection, and CI/CD gating. |
| `workspace-template/.agents/skills/refactoring/SKILL.md` | Performs behavior-preserving code transformations with characterization testing and scope control. |
| `workspace-template/.agents/skills/requirements-analysis/SKILL.md` | Analyzes requirements for scope, actors, workflows, constraints, risks, and gaps. |
| `workspace-template/.agents/skills/requirements-discovery/SKILL.md` | Turns vague product ideas into explicit, testable requirements. |
| `workspace-template/.agents/skills/security/SKILL.md` | Performs secure design and implementation review against OWASP/NIST-aligned controls. |
| `workspace-template/.agents/skills/stack-detection/SKILL.md` | Detects project technologies from manifest files and records active stack state to `stack.json`. |
| `workspace-template/.agents/skills/testing/SKILL.md` | Plans, designs, and executes impact-aware unit, integration, API, and E2E tests across any ecosystem. |
| `workspace-template/.agents/skills/uiux/SKILL.md` | Builds polished, responsive, accessible interfaces using established design tokens and primitives. |
| `workspace-template/.agents/skills/verification/SKILL.md` | Produces objective verification evidence and acceptance-criteria status. |

## Orchestration

| Path | Purpose |
|---|---|
| `workspace-template/.agents/agents/coordinator.md` | Central engineering coordinator responsible for task decomposition, context routing, subagent delegation, result synthesis, and final governance enforcement. |
| `workspace-template/.agents/orchestration/agent-operating-contract.md` | Defines the canonical 14-phase task execution sequence and maps all policies to their phases. |
| `workspace-template/.agents/orchestration/antigravity-tool-registry.json` | Authoritative versioned registry of Antigravity platform tools, access modes, and risk levels. |
| `workspace-template/.agents/orchestration/checkpoint-policy.md` | Defines autonomous versus approval-required actions. |
| `workspace-template/.agents/orchestration/context-budget-policy.md` | Defines context window management, hierarchical loading, and token optimization strategy. |
| `workspace-template/.agents/orchestration/context-router.md` | Routes the minimum sufficient context and active technology profiles for a task. |
| `workspace-template/.agents/orchestration/decision-policy.md` | Defines act/infer/research/ask boundaries and canonical ADR trigger formula. |
| `workspace-template/.agents/orchestration/error-recovery-policy.md` | Defines graduated failure recovery with detect-diagnose-isolate-repair-learn cycle. |
| `workspace-template/.agents/orchestration/governance-enforcement-policy.md` | Defines governance-enforcement-policy.md specification and implementation. |
| `workspace-template/.agents/orchestration/instruction-tag-standard.md` | Defines the canonical XML-style instruction tag standard, hierarchy, approved vocabulary, and tag rules. |
| `workspace-template/.agents/orchestration/lane-policy.yaml` | Authoritative machine-readable execution lane policy governing Fast, Standard, and High-Assurance ceremonies. |
| `workspace-template/.agents/orchestration/memory-sync-policy.md` | Defines when and how durable project memory must be updated. |
| `workspace-template/.agents/orchestration/multi-agent-policy.md` | Defines sub-agent delegation, handoff protocol, and multi-agent coordination patterns. |
| `workspace-template/.agents/orchestration/parallel-work-policy.md` | Defines safe parallel execution and conflict conditions. |
| `workspace-template/.agents/orchestration/policy-ownership.md` | Single authoritative index mapping every engineering policy domain to its canonical owner. |
| `workspace-template/.agents/orchestration/policy-registry.yaml` | Authoritative machine-readable registry of policy domains, canonical owners, and schemas. |
| `workspace-template/.agents/orchestration/role-registry.md` | Defines logical roles and their normal skill/context responsibilities. |
| `workspace-template/.agents/orchestration/task-classifier.md` | Classifies work so only relevant capabilities and context are activated. |
| `workspace-template/.agents/orchestration/task-lifecycle.md` | Defines the canonical stateful lifecycle from intake to completion. |
| `workspace-template/.agents/orchestration/verification-policy.yaml` | Declarative matrix defining mandatory verification gates and evidence requirements per task risk and type. |
| `workspace-template/.agents/orchestration/verification-schema.json` | Machine-readable contract for task verification evidence. |
| `workspace-template/.agents/orchestration/worktree-policy.md` | Defines safe worktree isolation and reconciliation behavior when worktrees are used. |
| `workspace-template/.agents/skills/quality-gates/scripts/aggregate-state.py` | Defines aggregate-state.py specification and implementation. |
| `workspace-template/.agents/skills/quality-gates/scripts/completion_gate.py` | Authoritative stop condition and completion gate evaluator for governed tasks. |
| `workspace-template/.agents/skills/quality-gates/scripts/generate-manifest.py` | Automated manifest generator and parity checker to prevent manifest drift. |
| `workspace-template/.agents/skills/quality-gates/scripts/hook-post-tool.py` | Defines hook-post-tool.py specification and implementation. |
| `workspace-template/.agents/skills/quality-gates/scripts/hook-pre-tool.py` | Defines hook-pre-tool.py specification and implementation. |
| `workspace-template/.agents/skills/quality-gates/scripts/hook-stop.py` | Defines hook-stop.py specification and implementation. |
| `workspace-template/.agents/skills/quality-gates/scripts/lint-documentation.py` | Lints documentation for tag closures, broken relative links, and heading hierarchy. |
| `workspace-template/.agents/skills/quality-gates/scripts/lint-policy-consistency.py` | Lints documentation and policies for semantic consistency and prevents obsolete concepts. |
| `workspace-template/.agents/skills/quality-gates/scripts/lint-state-instructions.py` | Lints agent instructions to ensure writes target canonical per-task state. |
| `workspace-template/.agents/skills/quality-gates/scripts/reconcile-state.py` | Reconciles and detects drift between canonical per-task state and derived aggregates. |
| `workspace-template/.agents/skills/quality-gates/scripts/recover-task.py` | Diagnoses and remediates interrupted tasks using git working tree and event history. |
| `workspace-template/.agents/skills/quality-gates/scripts/validate-agents.py` | Validates agent definitions, frontmatter, tool validity, and least-privilege role boundaries. |
| `workspace-template/.agents/skills/quality-gates/scripts/validate-control-plane.py` | Verifies control-plane integrity, CODEOWNERS coverage, and cryptographic hashes. |
| `workspace-template/.agents/skills/quality-gates/scripts/validate-governance.py` | Defines validate-governance.py specification and implementation. |
| `workspace-template/.agents/skills/quality-gates/scripts/validate-instruction-tags.py` | Automated validator verifying instruction tag vocabulary, balancing, frontmatter integrity, and rule character limits. |
| `workspace-template/.agents/skills/quality-gates/scripts/validate-policy-registry.py` | Validates policy registry integrity, canonical owners, and supporting artifacts. |
| `workspace-template/.agents/skills/quality-gates/scripts/validate-skills.py` | Validates Antigravity Skills mechanically using PyYAML, checking required sections and naming. |
| `workspace-template/.agents/skills/quality-gates/scripts/validate-task-dag.py` | Automated semantic DAG validator verifying task graph integrity, acyclicity, and status progression. |
| `workspace-template/.agents/skills/quality-gates/scripts/validate-technology-profiles.py` | Validates technology profile frontmatter, required metadata, and document structure. |

## State

| Path | Purpose |
|---|---|
| `workspace-template/.agents/state/agents.json` | Stores active logical roles/tasks and ownership state. |
| `workspace-template/.agents/state/agents.schema.json` | JSON Schema defining agent roles, tasks, and state. |
| `workspace-template/.agents/state/blocker-record.schema.json` | Strict canonical schema for blocker records. |
| `workspace-template/.agents/state/blockers.json` | Stores unresolved blockers and their disposition. |
| `workspace-template/.agents/state/blockers.schema.json` | JSON Schema defining blocker severity, resolution, and tracking. |
| `workspace-template/.agents/state/blockers/.gitkeep` | Defines .gitkeep specification and implementation. |
| `workspace-template/.agents/state/event.schema.json` | Strict canonical schema for task lifecycle and recovery events. |
| `workspace-template/.agents/state/events.jsonl` | Stores append-only execution events for traceability. Starts empty; events are recorded during actual execution. |
| `workspace-template/.agents/state/events.schema.json` | JSON Schema defining the structure and allowed values for events in `events.jsonl`. |
| `workspace-template/.agents/state/events/.gitkeep` | Defines .gitkeep specification and implementation. |
| `workspace-template/.agents/state/governance-record.schema.json` | Strict canonical schema for per-task governance records. |
| `workspace-template/.agents/state/governance.json` | Defines governance.json specification and implementation. |
| `workspace-template/.agents/state/governance.schema.json` | Defines governance.schema.json specification and implementation. |
| `workspace-template/.agents/state/governance/.gitkeep` | Defines .gitkeep specification and implementation. |
| `workspace-template/.agents/state/project.json` | Stores project lifecycle and current phase metadata. |
| `workspace-template/.agents/state/project.schema.json` | JSON Schema defining valid project metadata and lifecycle phase structure. |
| `workspace-template/.agents/state/retries.json` | Stores failed attempts, reasons, and retry policy state. |
| `workspace-template/.agents/state/retries.schema.json` | JSON Schema defining retry logging and escalation ladder state. |
| `workspace-template/.agents/state/stack.json` | Stores detected and declared technology stack state. |
| `workspace-template/.agents/state/stack.schema.json` | JSON Schema defining technology stack structure, categories, and version metadata. |
| `workspace-template/.agents/state/task-record.schema.json` | Strict canonical schema for per-task state records. |
| `workspace-template/.agents/state/tasks.json` | Stores tasks, dependencies, status, and outputs. |
| `workspace-template/.agents/state/tasks.schema.json` | JSON Schema defining the task DAG structure, statuses, and properties. |
| `workspace-template/.agents/state/tasks/.gitkeep` | Defines .gitkeep specification and implementation. |

## Templates

| Path | Purpose |
|---|---|
| `workspace-template/.agents/templates/adr-template.md` | Standardizes durable architectural and technical decision records. |
| `workspace-template/.agents/templates/api-template.md` | Documents an HTTP API endpoint contract and operational requirements. |
| `workspace-template/.agents/templates/bug-template.md` | Captures reproducible defect information and expected behavior. |
| `workspace-template/.agents/templates/component-template.md` | Specifies a reusable UI component and its state/accessibility contract. |
| `workspace-template/.agents/templates/feature-template.md` | Specifies a feature, acceptance criteria, dependencies, risks, and implementation boundaries. |
| `workspace-template/.agents/templates/incident-template.md` | Standardizes production incident reports with timeline, root cause, and prevention. |
| `workspace-template/.agents/templates/migration-template.md` | Standardizes data/schema/API migration planning with rollback and validation. |
| `workspace-template/.agents/templates/prd-template.md` | Produces a complete product requirements document. |
| `workspace-template/.agents/templates/requirements-template.md` | Captures raw-to-structured requirements before a formal PRD exists. |
| `workspace-template/.agents/templates/review-template.md` | Standardizes code review findings and verification status. |
| `workspace-template/.agents/templates/task-template.md` | Standardizes executable task records for the task graph. |
| `workspace-template/.agents/templates/test-template.md` | Defines tests using behavior-focused scenarios and evidence. |
| `workspace-template/.agents/templates/verification-template.md` | Standardizes human-readable verification reports and evidence capture. |

## CI/CD

| Path | Purpose |
|---|---|
| `workspace-template/.github/CODEOWNERS` | Defines CODEOWNERS specification and implementation. |
| `workspace-template/.github/workflows/ai-validation.yml` | Polyglot GitHub Actions workflow for automated validation of AI-generated changes across Node, Python, Go, Rust, and Java. |

## Requirements

| Path | Purpose |
|---|---|
| `workspace-template/docs/requirements/ACCEPTANCE_CRITERIA.md` | Optional cross-feature acceptance criteria register with verification status. |
| `workspace-template/docs/requirements/INDEX.md` | Defines the canonical location and relationships for product requirements artifacts. |
| `workspace-template/docs/requirements/PRD.md` | Starter PRD document for the project's validated product requirements. |

## Project Memory

| Path | Purpose |
|---|---|
| `workspace-template/docs/ARCHITECTURE.md` | Records the actual chosen system architecture and structural boundaries. |
| `workspace-template/docs/CONVENTIONS.md` | Records established project-specific practices that should be applied consistently. |
| `workspace-template/docs/CURRENT_STATE.md` | Records what is completed, in progress, blocked, next, and known to be risky. |
| `workspace-template/docs/INDEX.md` | Entry point and navigation map for all project knowledge. |
| `workspace-template/docs/PROJECT_CONTEXT.md` | Records product purpose, users, scope, constraints, and high-level project facts. |
| `workspace-template/docs/REFERENCES.md` | Lists external source material used by this project when version-sensitive guidance matters. |
| `workspace-template/docs/decisions/ADR-001-initial-architecture.md` | Defines ADR-001-initial-architecture.md specification and implementation. |
| `workspace-template/docs/decisions/INDEX.md` | Indexes accepted, superseded, and proposed ADRs without replacing the individual ADR files. |
