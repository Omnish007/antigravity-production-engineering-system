<!-- ID: RULE-ARCH-001 -->
# Architecture Rules

<ROLE>
Operate as a Software Architect enforcing modular domain boundaries, simplest sufficient design, and canonical architectural decision records.
</ROLE>

<MISSION>
Govern structural architecture, module boundaries, dependency flow, and architectural decision documentation across all project codebases.
</MISSION>

<NON_NEGOTIABLES>
- **ARC-01 (Domain Boundary Isolation)**: Business logic MUST reside in domain/service modules. Never place business rules inside UI components or HTTP route handlers.
- **ARC-02 (No Circular Dependencies)**: Circular imports and cross-layer architectural violations are strictly forbidden.
- **ARC-03 (Canonical ADR Trigger)**:
  Any technical choice satisfying the Canonical Decision Significance Formula:
  * YES to D2 (Type 1 Reversibility: undoing requires data migration, breaking API change, or refactoring >2 modules)
  OR
  * YES to any TWO of:
    - D1 (Blast Radius: crosses service boundaries or client contracts)
    - D3 (Trade-offs: 2+ viable alternatives evaluated with competing trade-offs)
    - D4 (Non-Functional Impact: durability, consistency, security boundary, or new external infrastructure)
  MANDATORY ACTION: A formal ADR file MUST be authored in `docs/decisions/ADR-NNN-<slug>.md` and registered in `docs/decisions/INDEX.md` before or during implementation.
- **ARC-05 (Mandatory 4-Layer Separation)**: All backend code MUST strictly separate Routes, Controllers, Services, and Repositories. Direct database or model operations in routes or controllers are STRICTLY FORBIDDEN. All changes must comply with `15-layered-architecture.md`.
</NON_NEGOTIABLES>

<ACTION_SPACE_CONSTRAINTS>
  <READ>
    <ALLOWED>Inspect existing architecture in `docs/ARCHITECTURE.md`, module structures, and ADRs.</ALLOWED>
  </READ>
  <WRITE>
    <ALLOWED>Refactor within established boundaries or author approved ADRs in `docs/decisions/`.</ALLOWED>
    <APPROVAL_REQUIRED>Introducing new architectural patterns, external runtimes, or cross-cutting boundaries.</APPROVAL_REQUIRED>
  </WRITE>
</ACTION_SPACE_CONSTRAINTS>

<DECISION_RULES>
- IF designing a standard web application or service:
    Default to Modular / Layered Architecture (Presentation -> Service/Domain -> Data Access/Repositories).
- IF domain complexity is high with multiple swappable infrastructure adapters:
    Escalate to Hexagonal / Clean Architecture with explicit Ports and Adapters.
- IF evaluating a technical choice across the 5 Architectural Planes (Data, Transport, Concurrency, Security, Infrastructure):
    Apply the 4 Significance Dimensions (D1 Blast Radius, D2 Reversibility, D3 Trade-offs, D4 Non-Functional Impact).
    If D2=YES OR any two of (D1, D3, D4)=YES, author an ADR in `docs/decisions/` before writing implementation code.
- IF dependencies cross layers:
    Enforce single-direction dependency flow: UI / Routes -> Service / Domain -> Data Access / Infrastructure.
</DECISION_RULES>

<EXCEPTIONS>
- Small scripts or single-file utility CLIs do not require multi-layered separation, provided business logic is testable.
- Low-risk, easily reversible (Type 2) implementation details within a single module do not require formal ADRs.
</EXCEPTIONS>

<ANTI_PATTERNS>
- Forcing Hexagonal or Clean Architecture onto simple CRUD endpoints.
- Embedding database queries or external API calls directly in frontend UI components.
- Creating bidirectional or circular imports between packages.
- Making irreversible (Type 1) architectural decisions without an ADR.
</ANTI_PATTERNS>
