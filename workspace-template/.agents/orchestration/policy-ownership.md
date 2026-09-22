# Policy Ownership Matrix

<MISSION>
Establish the single authoritative source of truth for every engineering governance, orchestration, and operational policy in the repository, eliminating competing authorities and policy drift.
</MISSION>

<NON_NEGOTIABLES>
- **OWN-01 (Single Policy Authority)**: Every policy domain MUST have exactly one canonical owner file. In case of divergence or ambiguity across documents, the canonical owner identified in this matrix is strictly authoritative.
- **OWN-02 (Zero Duplicate Authority)**: Secondary documents must cross-reference the canonical owner rather than redefining the policy rules.
- **OWN-03 (Explicit Artifact Roles)**: Every document, schema, and tool belongs to one of four unambiguous roles:
  1. **Canonical Owner**: The single, authoritative file that governs a policy domain. In any dispute or contradiction, the canonical owner strictly overrides all other documents.
  2. **Supporting Artifact**: A companion document, skill, template, or guide that elaborates, applies, or operationalizes the canonical policy without establishing competing authority.
  3. **Derived / Generated Artifact**: An artifact produced by tooling, scripts, or runtime execution (e.g., `FILE_MANIFEST.md`, `events.jsonl`, test reports).
  4. **Machine-Readable Schema**: A formal JSON Schema (Draft 2020-12) defining structural and syntactic constraints for machine-readable state, subordinate to the canonical policy's semantic rules.
</NON_NEGOTIABLES>

<DECISION_RULES>
## Canonical Policy Ownership Table

| Policy Domain | Canonical Owner File | Supporting Artifacts | Scope & Authority |
|---|---|---|---|
| **Agent Execution Lifecycle** | `agent-operating-contract.md` | `task-lifecycle.md`, `AGENTS.md` | Sole authority for the 15-stage High-Assurance Lifecycle sequence (`RECEIVE` through `COMPLETE`), phase boundaries, and operational modes. |
| **Task State Machine** | `task-lifecycle.md` | `tasks.schema.json`, `tasks.json`, `events.jsonl`, `validate-task-dag.py` | Sole authority for task state definitions (`DRAFT` through `COMPLETED`), legal transitions, and execution event logging. |
| **Architectural Decisions & ADR Triggers** | `decision-policy.md` | `docs/decisions/INDEX.md`, ADR templates | Sole authority for the Canonical Significance Formula (ADR trigger), autonomous vs escalation boundaries, and ADR conflict resolution. |
| **Context Loading & Routing** | `context-router.md` | `context-budget-policy.md` | Sole authority for mapping task types and risk levels to four-tier context bundles (`REQUIRED`, `RECOMMENDED`, `OPTIONAL`, `EXCLUDED`). |
| **Context Budget & Window Optimization** | `context-budget-policy.md` | `context-router.md` | Sole authority for context window limits, token optimization strategies, and eviction priorities. |
| **Durable Memory Synchronization** | `memory-sync-policy.md` | `docs/INDEX.md`, `docs/CURRENT_STATE.md`, `docs/CONVENTIONS.md` | Sole authority for when, where, and how durable project memory (`docs/`) must be updated following code changes. |
| **Verification Gates & Evidence** | `10-verification.md` | `verification-schema.json`, `SKILL-VERIFY-001`, `quality-gates/` | Sole authority for objective completion criteria, required exit codes, and verification evidence standards. |
| **Failure Recovery & Retries** | `error-recovery-policy.md` | `retries.json`, `retries.schema.json` | Sole authority for graduated failure recovery, retry logging (`retries.json`), and anti-doom-loop escalation ladders. |
| **Action Permissions & Checkpoints** | `checkpoint-policy.md` | `13-agent-safety.md` | Sole authority for autonomous vs approval-required actions, blast radius thresholds, and human checkpoint protocols. |
| **Agent Safety Guardrails** | `13-agent-safety.md` | `00-core.md`, `07-security.md` | Sole authority for prompt injection defenses, credential sanitization, untrusted content handling, and sandbox constraints. |
| **Technology Stack Detection** | `stack-detection/SKILL.md` | `stack.json`, `stack.schema.json` | Sole authority for detecting languages, frameworks, runtimes, and databases from repository evidence into `stack.json`. |
| **Technology Profiles & Metadata** | `technology/registry.json` | `technology/README.md`, `technology/profiles/*` | Sole authority for registered technology IDs, version policies, and the 8-section profile standard. |
| **Instruction Tag Standard** | `instruction-tag-standard.md` | `validate-instruction-tags.py` | Sole authority for approved XML tag vocabulary, hierarchy, syntax rules, and validator enforcement. |
| **Parallel Work & Concurrency** | `parallel-work-policy.md` | `worktree-policy.md` | Sole authority for concurrent task execution, conflict domains, and resource locking. |
| **Worktree Isolation** | `worktree-policy.md` | `parallel-work-policy.md` | Sole authority for git worktree creation, directory isolation, lifecycle cleanup, and branch merging. |
| **Multi-Agent Delegation** | `multi-agent-policy.md` | `agents.json`, `agents.schema.json` | Sole authority for sub-agent spawning, context passing, task partitioning, and handoff protocols. |
| **Governance Enforcement** | `governance-enforcement-policy.md` | `governance.schema.json`, `governance.json`, `validate-governance.py`, `SKILL-GOV-001` | Sole authority for task-scoped governance resolution, Grouped Completion Invariants (Groups A–J), and compliance validation. |
| **Developer Preferences** | `developer-defaults.md` | None | Sole authority for personal developer defaults, governed by `Project Reality > Personal Preference`. |
</DECISION_RULES>
