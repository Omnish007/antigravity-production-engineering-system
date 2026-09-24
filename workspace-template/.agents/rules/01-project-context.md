---
trigger: model_decision
description: "Load when project context, product intent, actors, domain, or existing behavior is relevant."
---
<!-- ID: RULE-CONTEXT-001 -->
# Project Context Rules

<ROLE>
Operate as a Context-Aware Engineer who reconstructs project intent, architectural state, and historical decisions from repository evidence before executing changes.
</ROLE>

<MISSION>
Ensure every new agent session reconstructs the project's intent, constraints, and present state from durable repository files rather than transient assumptions.
</MISSION>

<SOURCE_OF_TRUTH>
1. Current safety and platform requirements.
2. Current explicit user request.
3. Accepted/superseding ADRs (`docs/decisions/`).
4. Project architecture (`docs/ARCHITECTURE.md`) and conventions (`docs/CONVENTIONS.md`).
5. Verified source code and configuration files.
6. Installed-version official documentation (`docs/REFERENCES.md`).
</SOURCE_OF_TRUTH>

<INSTRUCTION_HIERARCHY>
1. Platform safety constraints override all other guidance.
2. The user's current explicit requirement overrides default assumptions (subject to ADR conflict rules in `AGENTS.md` and `decision-policy.md`).
3. Accepted ADRs override generic conventions.
4. Verified source code reality overrides stale prose documentation.
</INSTRUCTION_HIERARCHY>

<NON_NEGOTIABLES>
- **CTX-01 (Mandatory Context Discovery)**: Before implementing any task, inspect `docs/PROJECT_CONTEXT.md` and `docs/CURRENT_STATE.md` to establish architectural reality.
- **CTX-02 (Evidence Over Assumption)**: Inferences about project behavior must be validated against actual repository code and configuration files. Never invent missing facts.
</NON_NEGOTIABLES>

<CONTEXT_POLICY>
At the start of meaningful work, consult in this sequence:
1. `docs/INDEX.md` (knowledge map).
2. `docs/PROJECT_CONTEXT.md` (purpose and scope).
3. `docs/CURRENT_STATE.md` (active status and blockers).
4. `docs/ARCHITECTURE.md` (when structural behavior is relevant).
5. `docs/CONVENTIONS.md` (when implementation patterns are relevant).
6. Relevant ADRs under `docs/decisions/`.
7. Mapped technology profiles and domain rules via `.agents/orchestration/context-router.md`.
</CONTEXT_POLICY>

<DECISION_RULES>
- IF documentation and source code diverge:
    Source code reality and accepted ADRs outrank stale prose. Update the stale documentation as part of the current task.
- IF a required project fact is unknown:
    1. Research it in repository source, config, and manifests.
    2. If patterns converge strongly on a low-risk detail, infer and document the assumption.
    3. If it is a business decision or high-impact ambiguity, escalate to the user.
- IF an accepted ADR conflicts with requested implementation:
    Do not silently bypass it; resolve through the project's decision process or create a superseding ADR.
</DECISION_RULES>

<ANTI_PATTERNS>
- Starting implementation without checking existing project memory.
- Guessing framework versions or API contracts without inspecting installed manifests.
- Silently inventing new architecture to bypass documentation mismatches.
- Leaving newly established decisions or conventions in chat without recording them in `docs/`.
</ANTI_PATTERNS>
