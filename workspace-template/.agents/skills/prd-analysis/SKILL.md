---
name: prd-analysis
description: Analyze an existing PRD and transform it into an implementation-ready specification with risks, gaps, dependencies, and acceptance criteria.
---

# PRD Analysis Skill

## Phase 1 — Extract intent

Identify:

- product objective;
- target users;
- problem statement;
- success measures;
- scope;
- out-of-scope items;
- user journeys;
- functional requirements;
- non-functional requirements;
- constraints;
- dependencies;
- integrations.

## Phase 2 — Challenge the document

Look for:

- contradictions;
- ambiguous terminology;
- missing permissions;
- missing failure behavior;
- implicit business rules;
- unbounded inputs/storage;
- unclear lifecycle/retention;
- missing auditability;
- missing observability;
- untestable success criteria;
- unsupported performance claims;
- security assumptions that exist only in the UI.

## Phase 3 — Translate to engineering impact

Map requirements to:

- frontend surfaces;
- API endpoints;
- data models;
- authorization boundaries;
- background work;
- external integrations;
- tests;
- migrations;
- operational controls.

## Phase 4 — Produce implementation inputs

Create:

- requirement traceability table;
- acceptance criteria;
- architecture-impact summary;
- data-impact summary;
- API-impact summary;
- risks and open decisions;
- dependency list;
- phased implementation plan.

## Output integrity

Do not silently "fix" the product specification. Mark inferred behavior as assumptions. High-impact business questions remain open until explicitly resolved.
