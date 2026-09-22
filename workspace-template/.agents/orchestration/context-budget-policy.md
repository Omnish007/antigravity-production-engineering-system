# Context Budget Policy

<MISSION>
Manage the agent's context window as a finite, high-value resource, preventing context rot, optimizing signal density, and mitigating lost-in-the-middle degradation.
</MISSION>

<NON_NEGOTIABLES>
- **BUDGET-01 (Mandatory Skill Activation)**: Activated required Skills must be loaded when applicable; unrelated Skills should not be loaded. Antigravity uses progressive disclosure to expose metadata first and load relevant Skill content when needed.
- **BUDGET-02 (Prohibition of Bulk Loading)**: Bulk-loading entire directories (`docs/`, `.agents/`, `src/`) or massive lockfiles into context is strictly forbidden.
</NON_NEGOTIABLES>

<CONTEXT_POLICY>
### Hierarchical Loading Order
Load context in this priority order to maximize cache efficiency and prevent displacement of critical constraints:
1. Safety and platform constraints.
2. Core rules (`00-core.md`, `13-agent-safety.md`).
3. Active technology profiles (`.agents/technology/profiles/*`) & stack state (`stack.json`).
4. Mandatory domain skills for active task (`.agents/skills/<skill>/SKILL.md`) — loaded when performing domain tasks.
5. Task-specific rules (`03-architecture.md`, `07-security.md`, `09-testing.md`).
6. Project memory indexes (`docs/INDEX.md`, `docs/CURRENT_STATE.md`).
7. Relevant architecture/conventions/ADRs (only when required).
8. Task-specific source files (strictly affected scope).
9. Volatile task data (errors, logs, test outputs).

### Lost-in-the-Middle Mitigation
Arrange loaded content strategically:
- Safety rules and critical invariants appear first.
- Reference documentation and conventions occupy the middle.
- Specific task instructions, acceptance criteria, and verification commands appear last, adjacent to the working area.
</CONTEXT_POLICY>

<DECISION_RULES>
- IF reading project memory:
    Follow an index-first strategy: read `docs/INDEX.md` and `docs/CURRENT_STATE.md` before opening full documents.
- IF inspecting a large file (>500 lines):
    Inspect file structure or outline first; load specific sections on demand.
- IF context window reaches heavy saturation (>50% capacity):
    Decompose remaining work into focused sub-tasks with clean context rather than continuing with degraded reasoning.
</DECISION_RULES>

<ANTI_PATTERNS>
- Loading lockfiles (`package-lock.json`, `yarn.lock`) unless diagnosing dependency conflicts.
- Loading minified bundles, build outputs, or compiled artifacts.
- Loading full test fixture datasets or large binary media.
- Omitting required domain skill files during execution of governed tasks.
</ANTI_PATTERNS>
