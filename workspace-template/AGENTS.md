# Project Agent Entry Point & Repository Governance Contract

<MISSION>
Provide the universal bootstrap contract and entry point for AI agents interacting with this repository, establishing the multi-stack architecture, execution lifecycle, source of truth, governance enforcement, and memory synchronization rules.
</MISSION>

<SOURCE_OF_TRUTH>
1. Project requirements: `docs/requirements/PRD.md` and explicit user instructions.
2. Architecture and decisions: `docs/ARCHITECTURE.md` and accepted ADRs in `docs/decisions/`.
3. Project state: `docs/CURRENT_STATE.md`, `.agents/state/tasks.json`, and `.agents/state/governance.json`.
4. Technology stack: `.agents/state/stack.json` and active profiles in `.agents/technology/profiles/`.
5. Canonical rules: `.agents/rules/` (`RULE-CORE-001` through `RULE-OBS-001`).
6. Skills catalog: `.agents/skills/` (`SKILL-AC-001` through `SKILL-VERIFY-001`).
7. Governance enforcement: `.agents/orchestration/governance-enforcement-policy.md`.
8. Conventions: `docs/CONVENTIONS.md` and repository manifest files.
</SOURCE_OF_TRUTH>

<INSTRUCTION_HIERARCHY>
1. Platform safety constraints and security invariants.
2. Explicit, current user instructions (subject to the ADR Conflict Rule below).
3. Accepted ADRs (`docs/decisions/`) and project memory (`docs/`).
4. Universal rules (`.agents/rules/`) and active technology profiles (`.agents/technology/profiles/`).
5. Developer defaults (`.agents/preferences/developer-defaults.md`) — overridden whenever project reality differs.

**ADR Conflict Rule**: Current user requests may propose a change to an accepted project decision, but the agent must not silently bypass that decision. When a request intentionally contradicts or modifies an accepted ADR:
1. Identify and state the conflict explicitly to the user.
2. Evaluate the proposed change and its trade-offs.
3. If confirmed or requested, author a superseding ADR (`docs/decisions/ADR-NNN-<slug>.md`) before implementation.
4. Implement under the new decision.
</INSTRUCTION_HIERARCHY>

## System Architecture Separation
1. **Portable Contract** (cross-tool interoperability): `AGENTS.md`, `docs/CONVENTIONS.md`, `docs/ARCHITECTURE.md`, `docs/decisions/`.
2. **Antigravity Control Plane** (native runtime + governance):
   - Execution Authority: Antigravity Native Runtime (Planning Mode, Task Groups, Artifacts, Permissions, Terminal Sandbox).
   - Governance Metadata Layer: `.agents/rules/`, `.agents/skills/`, `.agents/agents/`, `.agents/technology/`, `.agents/state/`.

<EXECUTION_POLICY>
The system executes tasks through three adaptive lanes to maximize developer velocity while preserving rigorous safety:

### Lane A — Fast (Native Fast Mode)
- **Scope**: Typo fixes, variable/symbol renames, formatting, tiny local refactors, documentation corrections, obvious 1-file fixes.
- **Flow**: `CLASSIFY -> TARGETED CONTEXT -> IMPLEMENT -> VERIFY -> COMPLETE`
- **Overhead**: Zero bureaucratic ceremony. No mandatory ADR, no multi-file preflight reading. Focus on surgical change and fast verification (e.g., format/typecheck).

### Lane B — Standard (Native Planning / Task Groups)
- **Scope**: New features, standard bug fixes, API updates, UI components, non-critical database refactoring.
- **Flow**: `CLASSIFY -> CONTEXT -> PLAN -> IMPLEMENT -> TEST -> VERIFY -> REVIEW -> COMPLETE`
- **Runtime**: Uses Antigravity's native Implementation Plan and Task Group mechanisms as execution authority. Automated test execution and diff review required.

### Lane C — High Assurance (Full Governance Machine)
- **Scope**: Authentication, authorization, security changes, database migrations, infrastructure/deployment, financial/payment logic, data retention, destructive operations, or major architecture changes.
- **Flow**: `CLASSIFY -> CONTEXT -> PLAN -> ADR -> GOVERNANCE -> IMPLEMENT -> TEST -> SECURITY -> VERIFY -> DIFF REVIEW -> HUMAN APPROVAL -> MEMORY SYNC -> GOVERNANCE CHECK -> COMPLETE`
- **Rigor**: Full Grouped Completion Invariants (Groups A–J), mandatory ADR evaluation, 7-point security check evidence, and externally grounded human approval.
</EXECUTION_POLICY>

<CONTEXT_POLICY>
Context loading is lane-aware and progressive to prevent context window exhaustion:
- **Lane A**: Load only the user prompt, target file, and relevant minimal coding rule (`00-core.md` / `04-coding.md`).
- **Lane B**: Load `AGENTS.md`, active project context (`docs/CURRENT_STATE.md`), domain rules, and relevant skill from `.agents/skills/`.
- **Lane C**: Load full baseline context, active technology profiles (`.agents/technology/profiles/`), security rules (`RULE-SEC-001`), and governance enforcement policy.
- Never flood context with unrelated directories, vendor lockfiles, or speculative documentation.
</CONTEXT_POLICY>

<VERIFICATION_POLICY>
A task is complete only when:
- All acceptance criteria are satisfied with objective evidence.
- Canonical verification commands exit with code 0:
  * TypeScript/Node: `npm run typecheck`, `npm run lint`, `npm test`, `npm run build`
  * Python: `ruff check`, `mypy`, `pytest`
  * Go: `go vet ./...`, `go test ./...`, `go build ./...`
  * Rust: `cargo fmt --check`, `cargo clippy`, `cargo test`, `cargo build`
- No errors are masked or suppressed.
- Governance validator (`validate-governance.py`) returns `PASS` and `governanceStatus` is `complete`.
</VERIFICATION_POLICY>

<MEMORY_POLICY>
Repository memory is durable; conversation history is transient:
- Before work: Reconstruct context from `docs/` and `.agents/state/`.
- After work: Record durable decisions in `docs/decisions/` and status in `docs/CURRENT_STATE.md`.
- Never leave important decisions or architectural changes stranded in chat.
- Never overwrite historical ADRs; supersede them deliberately with new numbered ADRs.
</MEMORY_POLICY>

<OUTPUT_CONTRACT>
Upon completion, provide:
1. Concise executive summary of changes.
2. Complete file change list with specific actions taken.
3. Objective verification evidence (commands, exit codes, test results).
4. Synchronized project memory documents.
5. Governance status and validation outcome.
6. Any remaining blockers or deferred risks.
</OUTPUT_CONTRACT>
