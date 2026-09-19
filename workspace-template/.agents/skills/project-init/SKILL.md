---
name: project-init
description: Initialize a repository with the agent system, project memory, baseline conventions, and safe execution state.
---

# Project Initialization Skill

## Outcome

Produce a repository that a fresh AI chat can understand and continue safely.

## Procedure

1. Inspect the repository before changing anything.
2. Identify whether the project is greenfield, existing, monorepo, single app, or multi-app.
3. Inspect `package.json`, lockfile, source tree, build scripts, test scripts, deployment config, and environment examples.
4. Install only missing project dependencies required by the explicit project requirements; never rewrite package versions merely for uniformity.
5. Establish or merge `.agents/` without destroying existing project rules.
6. Establish `docs/` and populate project-specific context from verified repository facts.
7. Decide and document the actual architecture.
8. Identify durable technical decisions already present in the codebase and record them as ADRs where rationale is important and recoverable.
9. Populate `docs/CURRENT_STATE.md` from actual code/repo state.
10. Populate `.agents/state/project.json` and create initial task state only for real tracked work.
11. Run baseline formatter/lint/typecheck/test/build commands that already exist in the repository.
12. Record limitations and unresolved decisions.

## Greenfield projects

For a new Next.js application, prefer the current official project generator and verify the generated package versions. Use the App Router by default unless a requirement says otherwise.

For a full-stack repository, keep web and API boundaries explicit. Do not add a shared package until a real cross-boundary need exists.

## Existing projects

Do not impose the template's directory structure mechanically. Preserve the repository's architecture when it is sound. Use the system to document and improve it, not to perform a cosmetic rewrite.

## Completion

Initialization is complete only when a brand-new agent can locate:

- what the project is;
- how it is structured;
- what conventions it follows;
- what important decisions exist;
- what is currently incomplete;
- how to verify changes.
