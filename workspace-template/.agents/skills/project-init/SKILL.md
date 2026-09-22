---
name: project-init
id: SKILL-INIT-001
description: Inspect and initialize any repository with the agent system, persistent project memory, detected tech stack conventions, and verified execution state.
---

# Project Initialization Skill

<MISSION>
Inspect and initialize any repository with the agent system, persistent project memory, detected tech stack conventions, and verified execution state.
</MISSION>

<WHEN_TO_USE>
Activate this skill when executing tasks requiring project-init capabilities, workflows, or architectural guidance.
</WHEN_TO_USE>

<PRECONDITIONS>
### Prerequisites
- Repository root is accessible.
- No prior active task or event log is required for initial bootstrap.
- If execution state already exists, preserve and merge it safely.

### Pre-flight Checklist
- [ ] Repository root inspected
- [ ] Tech stack detected and recorded in `.agents/state/stack.json`
- [ ] State files (`.agents/state/`) initialized
- [ ] `SYSTEM_INITIALIZED` execution event logged to `events.jsonl`
</PRECONDITIONS>

<NON_NEGOTIABLES>
- Execute stack detection from repository evidence; never make unverified assumptions about frameworks or runtimes.
- Initialize `.agents/state/project.json` and `tasks.json` with valid starter schemas.
- Record the `SYSTEM_INITIALIZED` execution event in `.agents/state/events.jsonl`.
- Maintain a clean boundary between repository bootstrap (this skill) and subsequent per-task execution.
</NON_NEGOTIABLES>

<PROCEDURE>
## Outcome

Produce a fully documented repository that any fresh AI chat or new engineer can immediately understand, plan, implement, and verify safely.

## Procedure

1. **Inspect before modifying**: Inspect the repository structure, configuration files, and recent commit history before making any changes.
2. **Detect project type & architecture**: Determine whether the project is greenfield or existing, single-service, monorepo, client-server, or microservices.
3. **Detect technology stack**:
   - **Node.js / TypeScript**: Look for `package.json`, lockfiles (`pnpm-lock.yaml`, `package-lock.json`, `bun.lockb`), `tsconfig.json`.
   - **Python**: Look for `pyproject.toml`, `requirements.txt`, `Pipfile`, `setup.py`, `.python-version`.
   - **Go**: Look for `go.mod`, `go.sum`.
   - **Rust**: Look for `Cargo.toml`, `Cargo.lock`, `rust-toolchain.toml`.
   - **JVM / Java / Kotlin**: Look for `pom.xml`, `build.gradle`, `build.gradle.kts`.
   - **C# / .NET**: Look for `*.csproj`, `*.sln`, `global.json`.
   - **Containers / Cloud**: Look for `Dockerfile`, `docker-compose.yml`, Kubernetes manifests, Terraform/OpenTofu files.
4. **Establish or merge `.agents/`**: Copy or update `.agents/` rules, skills, orchestration, and templates without destroying existing custom rules.
5. **Establish project memory (`docs/`)**:
   - Populate `docs/PROJECT_CONTEXT.md` with actual project identity, goals, users, and the detected technology baseline.
   - Document the real architectural boundaries in `docs/ARCHITECTURE.md`.
   - Record established conventions in `docs/CONVENTIONS.md`.
   - Record known existing technical decisions as ADRs in `docs/decisions/`.
   - Initialize `docs/CURRENT_STATE.md` with current milestone, active tasks, and known blockers.
6. **Initialize execution state**: Populate `.agents/state/project.json` and initialize task state for tracked work.
7. **Verify baseline commands**: Execute the repository's existing format, lint, typecheck, test, and build commands to establish the baseline health.
8. **Document open questions**: Record any ambiguities or missing project facts in `docs/CURRENT_STATE.md`.

## Greenfield projects

- When creating a new project from scratch, use the official, community-standard generator for the chosen ecosystem:
  - TypeScript/Web: Official framework generator (e.g., `create-next-app`, `create-vite`)
  - Python: `uv init`, `poetry new`, or framework-specific scaffolding (`django-admin startproject`)
  - Go: `go mod init <module-path>`
  - Rust: `cargo new <crate-name> --bin` (or `--lib`)
  - Java: Spring Initializr (`start.spring.io`), Quarkus CLI
  - .NET: `dotnet new webapi` / `dotnet new sln`
- Keep initial boundaries simple and explicit. Avoid adding speculative abstractions or premature microservices.

## Existing projects

- Never rebuild or restructure an application just to fit a template. Preserve the existing working architecture.
- Document what actually exists rather than an idealized design.
- Capture established project patterns in `docs/CONVENTIONS.md` so future agent actions match existing style.

## Completion standard

Initialization is complete only when:
- Project context, architecture, conventions, and current state are documented from verified repository facts;
- The technology stack, build commands, and test runners are verified and documented in `AGENTS.md` and `docs/PROJECT_CONTEXT.md`;
- Baseline verification commands execute successfully or known failures are documented as active issues.
</PROCEDURE>

<VERIFICATION_POLICY>
### Exit Criteria
Repository initialized with verified state files and declared stack profile.
</VERIFICATION_POLICY>

<DELIVERABLES>
- Initialized repository structure, base configurations, and toolchain setup.
- Validated initial build, lint, and test runs.
</DELIVERABLES>
