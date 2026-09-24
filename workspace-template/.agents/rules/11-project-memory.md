<!-- ID: RULE-MEM-001 -->
# Project Memory Rules

<MISSION>
Ensure durable repository memory is systematically consulted before work and synchronized after work, preserving decisions, conventions, and architectural state across independent AI sessions.
</MISSION>

<SOURCE_OF_TRUTH>
1. Project Knowledge Index: `docs/INDEX.md`
2. Durable Decisions: `docs/decisions/` and `docs/decisions/INDEX.md`
3. System Architecture: `docs/ARCHITECTURE.md`
4. Project Conventions: `docs/CONVENTIONS.md`
5. Active Status & Risks: `docs/CURRENT_STATE.md`
</SOURCE_OF_TRUTH>

<CONTEXT_POLICY>
Before beginning meaningful implementation, load memory in this sequence:
1. `docs/INDEX.md` (navigation map).
2. `docs/PROJECT_CONTEXT.md` (project goals and constraints).
3. `docs/CURRENT_STATE.md` (active status, blockers, and recent changes).
4. `docs/ARCHITECTURE.md` and `docs/CONVENTIONS.md` (when structural or implementation patterns apply).
5. Only specific relevant ADRs from `docs/decisions/`.
</CONTEXT_POLICY>

<MEMORY_POLICY>
Repository memory is durable; chat history is transient:
- Before work: Consult existing decisions so previous trade-offs are honored.
- After work: Evaluate what changed permanently and synchronize the appropriate documents:
  * Store reusable patterns in `docs/CONVENTIONS.md`.
  * Store boundary or structural changes in `docs/ARCHITECTURE.md`.
  * Store durable choices meeting the Canonical ADR Trigger as numbered ADRs in `docs/decisions/`.
  * Store phase and milestone progress in `docs/CURRENT_STATE.md`.
- Never store temporary debugging scratchpad notes or trivial styling adjustments in durable memory.
- Never overwrite historical ADRs; mark old ADRs as `superseded` and author a new ADR.
</MEMORY_POLICY>

<ACTION_SPACE_CONSTRAINTS>
  <READ>
    <ALLOWED>Read any project memory file under `docs/` and `.agents/state/`.</ALLOWED>
  </READ>
  <WRITE>
    <ALLOWED>Update `docs/CURRENT_STATE.md`, `docs/CONVENTIONS.md`, `docs/ARCHITECTURE.md`, and author new ADRs in `docs/decisions/`.</ALLOWED>
    <PROHIBITED>Silently modifying or deleting accepted historical ADRs without superseding them.</PROHIBITED>
  </WRITE>
</ACTION_SPACE_CONSTRAINTS>

<EXECUTION_POLICY>
At the conclusion of every meaningful task, execute the memory synchronization loop:
1. **Assess Impact**: Ask what changed permanently (architecture, conventions, status, requirements).
2. **Author Decisions**: If an architectural choice was made, write an ADR and update `docs/decisions/INDEX.md`.
3. **Update Documentation**: Synchronize affected documents in `docs/`.
4. **Update Execution State**: Ensure the canonical task record `.agents/state/tasks/TASK-ID.json` reflects the task status; regenerate derived aggregates after state changes.
5. **Verify Accuracy**: Confirm that documentation matches the actual code in the repository.
</EXECUTION_POLICY>

<VERIFICATION_POLICY>
A task cannot be marked complete if:
- Architectural changes were committed without updating `docs/ARCHITECTURE.md` or creating an ADR.
- `docs/CURRENT_STATE.md` does not reflect the current phase or known blockers.
- Discovered project conventions remain only in chat history.
</VERIFICATION_POLICY>
