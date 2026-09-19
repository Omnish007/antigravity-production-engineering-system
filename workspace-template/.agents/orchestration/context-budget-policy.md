# Context Budget Policy

## Purpose

Manage the agent's context window as a finite, high-value resource. Prevent context rot, optimize signal density, and ensure the most critical information is always available for reasoning.

## Hierarchical loading order

Load context in this priority order. Place invariant, high-priority material first to maximize cache efficiency and ensure it is never displaced:

```text
1. Safety and platform constraints
2. Core rules (00-core, 13-agent-safety)
3. Task-specific rules (activated by classifier)
4. Project memory indexes (docs/INDEX.md, docs/CURRENT_STATE.md)
5. Relevant architecture/conventions/ADRs (only if task requires)
6. Task-specific source files (only affected files)
7. Volatile task data (errors, logs, test output)
```

## Progressive disclosure

Follow an index-first strategy:

1. Read `docs/INDEX.md` to understand the knowledge map.
2. Read `docs/CURRENT_STATE.md` for present context.
3. Open `docs/ARCHITECTURE.md`, `docs/CONVENTIONS.md`, or specific ADRs only when the task touches those domains.
4. Load source files only when implementation requires them.
5. Never bulk-load the entire `docs/` or `.agents/` directory.

## Signal density

Maximize the information value per token:

- prefer summaries and indexes over full documents when exploring;
- load only the relevant sections of large files;
- avoid loading files that are clearly irrelevant to the current task;
- when a file exceeds reasonable size, read the structure/interface first and specific sections on demand;
- do not load test fixtures, generated files, or lockfiles unless specifically investigating them.

## Lost-in-the-middle mitigation

Models process information at the beginning and end of context more reliably than the middle. Arrange loaded content so that:

- safety rules and critical constraints appear first;
- the specific task instructions and acceptance criteria appear near the working area;
- reference material occupies the middle;
- commands to execute and verification checklists appear last.

## Context saturation

When a session becomes heavily loaded:

- evaluate whether remaining work can be completed effectively;
- consider decomposing into focused sub-tasks with clean context;
- if handover is needed, produce a structured state summary covering: what was done, what remains, key decisions made, and blockers found;
- prefer starting a fresh session over continuing with degraded reasoning.

## File size awareness

Apply judgment to large files:

- lockfiles (`package-lock.json`, `yarn.lock`): do not load unless investigating a specific dependency;
- generated code, bundles, and build artifacts: do not load;
- large data files: read only the schema/first records;
- images, binaries, and media: inspect metadata only when relevant.

## Context router integration

The `context-router.md` defines which context groups to load per task type. This policy governs **how** that loading should be performed for efficiency. Both policies work together.
