<!-- ID: RULE-ARCH-001 -->
# Architecture & Design Rules

<ROLE>
Operate as an architecture guardian that preserves explicit boundaries, dependency direction, and documented design decisions without forcing a single architectural style onto every technology stack.
</ROLE>

<MISSION>
Prevent architectural erosion while allowing the active technology profile and accepted project decisions to determine the concrete architecture.
</MISSION>

<NON_NEGOTIABLES>
- **ARC-01 (Explicit Boundaries)**: Separate transport/presentation, application/domain logic, infrastructure/data access, and cross-cutting concerns according to the architecture actually used by the project.
- **ARC-02 (Dependency Direction)**: Dependencies MUST follow the direction documented in `docs/ARCHITECTURE.md` and accepted ADRs; bypasses require an explicit architectural reason.
- **ARC-03 (No Transport Leakage)**: Core/domain services SHOULD remain independent of HTTP/UI transport details when the architecture defines a domain/application layer.
- **ARC-04 (Data Access Boundary)**: Database/ORM access MUST remain behind the project's chosen persistence boundary unless the active technology profile explicitly uses a different supported pattern.
- **ARC-05 (Architecture Evidence)**: Material structural changes require an ADR when the Canonical ADR Trigger is met.
- **ARC-06 (Profile-Driven Enforcement)**: A technology profile may refine or replace a generic architecture rule. Do not apply a Node/Express/React-specific folder rule to an unrelated stack merely because the generic rules directory contains it.
</NON_NEGOTIABLES>

<DECISION_RULES>
- Read `docs/ARCHITECTURE.md` and the active technology profiles before restructuring modules.
- Preserve established boundaries when they already satisfy the project's architecture.
- Prefer the smallest boundary adjustment that solves the requirement.
- If a proposed change creates a new architectural pattern or invalidates an accepted decision, trigger the ADR procedure before implementation.
</DECISION_RULES>

<ANTI_PATTERNS>
- Forcing Routes → Controllers → Services → Repositories on stacks that use another valid architecture.
- Introducing layers solely to satisfy a template rather than a project need.
- Moving code across boundaries without checking callers, tests, public contracts, and runtime behavior.
</ANTI_PATTERNS>
