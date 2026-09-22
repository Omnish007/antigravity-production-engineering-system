# Decision Policy

<MISSION>
Provide predictable boundaries for autonomous agent action, inference, research, and human escalation.
</MISSION>

<INSTRUCTION_HIERARCHY>
1. Platform safety and security constraints.
2. Explicit, current user requirements.
3. Accepted ADRs (`docs/decisions/`).
4. Established project conventions (`docs/CONVENTIONS.md`).
5. Existing code patterns.
6. Installed-version official documentation.
7. General software engineering practice.
</INSTRUCTION_HIERARCHY>

<NON_NEGOTIABLES>
- **DEC-01 (Decision Hierarchy Enforcement)**: Conflicts must be resolved using the strict hierarchy: Safety > User Requirement > ADRs > Conventions > Existing Code > General Practice.
- **DEC-02 (Mandatory ADR for Architectural Choices)**:
  Any technical choice satisfying the Canonical Significance Formula:
  * YES to D2 (Type 1 Reversibility)
  OR
  * YES to any TWO of:
    - D1: Blast Radius (affects more than one module, service boundary, or client contract)
    - D3: Evaluated Trade-offs (between 2+ viable alternatives across the 5 architectural planes: Data, Transport, Concurrency, Security, Infrastructure)
    - D4: Non-Functional Impact (durability, consistency, security trust boundaries, or new external runtimes)
  MANDATORY ACTION:
    1. Must read `.agents/skills/architecture/SKILL.md`.
    2. Must write an ADR file to `docs/decisions/ADR-NNN-<slug>.md` documenting the decision and options considered.
    3. Must update `docs/decisions/INDEX.md`.
  VIOLATION: Implementing any architectural decision meeting the trigger without an ADR is an INVALID ACTION.
</NON_NEGOTIABLES>

<DECISION_RULES>
### 1. Act Autonomously
Act without asking when the decision is established by:
- An accepted ADR.
- Established project conventions.
- Explicit user requirements.
- Existing configuration files.
- Installed-version official documentation.
- A reversible, low-risk (Type 2) implementation choice.

### 2. Infer and Record
Infer when multiple signals converge strongly and the choice is low-risk and reversible:
- Record the assumption in task evidence and, when durable, in `docs/CONVENTIONS.md`.
- Never invent business rules just because implementation would be simpler.

### 3. Research First
Research before acting when:
- Documentation is version-sensitive or dependencies are recently upgraded.
- Multiple supported technical approaches exist with uncertain trade-offs.
- Performance or security consequences require empirical evidence.
</DECISION_RULES>

<ESCALATION_POLICY>
Stop and ask the user when uncertainty involves decisions the repository cannot resolve safely:
- Ambiguous business behavior with divergent product outcomes.
- Irreversible or high-impact architecture choices (Type 1).
- Production credential changes or secrets rotation.
- Destructive data operations or schema truncation.
- External side effects that cannot be undone.
- Public API breaking changes.
- Financial, legal, or compliance decisions.
</ESCALATION_POLICY>

<EXCEPTIONS>
- If current work conflicts with an accepted ADR, do NOT silently bypass the ADR. Ask the user if they intend to supersede the decision; if yes, author a new superseding ADR.
</EXCEPTIONS>
