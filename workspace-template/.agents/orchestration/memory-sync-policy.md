# Memory Synchronization Policy

<MISSION>
Turn important outcomes from an AI session into durable repository knowledge without creating documentation noise.
</MISSION>

<NON_NEGOTIABLES>
- Project memory in `docs/` MUST be updated immediately after verification passes and before declaring the task complete.
- Never record transient debugging steps, trivial refactors, or details obvious from source code without decision rationale.
- Reconcile memory centrally when completing multi-agent or parallel work.
</NON_NEGOTIABLES>

<MEMORY_POLICY>
## Synchronization trigger

Run this review after:
- feature implementation;
- bug fix;
- refactor that changes reusable patterns;
- API/database/auth change;
- architecture/planning milestone;
- deployment/release preparation;
- any task where the team explicitly made a lasting technical decision.

## Classification

| Finding | Destination |
|---|---|
| Product purpose/scope/user context changed | `docs/PROJECT_CONTEXT.md` |
| Runtime/module/data-flow structure changed | `docs/ARCHITECTURE.md` |
| Reusable practice adopted | `docs/CONVENTIONS.md` |
| Deliberate trade-off/long-lived choice | new or updated ADR |
| Completed/in-progress/blocked work changed | `docs/CURRENT_STATE.md` |
| Task execution metadata changed | `.agents/state/*.json` / `events.jsonl` |
</MEMORY_POLICY>

<DECISION_RULES>
## Decision test

Create an ADR when at least one is true:
- reasonable engineers could choose multiple approaches;
- the choice affects architecture or public contracts;
- the choice creates meaningful constraints or lock-in;
- reversing later would be costly;
- security/reliability/cost consequences are material;
- future agents need the rationale, not merely the final code.

## Convention test

Update `CONVENTIONS.md` when the team now expects future code to follow the same rule in multiple places.
</DECISION_RULES>

<ANTI_PATTERNS>
## No-noise rule

Do not record:
- trivial refactors;
- one-file implementation details with no future relevance;
- transient debugging steps;
- information that is already obvious from source and has no decision context.
</ANTI_PATTERNS>

<EXECUTION_POLICY>
## ADR update procedure

1. Choose the next sequential ADR number.
2. Fill the template completely.
3. Mark prior decisions as `Superseded` if this decision replaces them.
4. Update `docs/decisions/INDEX.md`.
5. Update architecture/conventions if the decision has operational consequences.
6. Mention the ADR in the task completion summary.
</EXECUTION_POLICY>

<VERIFICATION_POLICY>
## Final check

Before closing the task, ask:
> Could a brand-new AI chat understand every important lasting decision made during this task by reading the repository, without reading this conversation?

If not, synchronize the missing durable knowledge.
</VERIFICATION_POLICY>
