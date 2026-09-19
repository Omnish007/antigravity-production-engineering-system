---
name: refactoring
description: Perform behavior-preserving code transformations with characterization testing, incremental migration, scope control, and full regression safety.
---

# Refactoring Skill

## Core principle

Refactoring changes internal structure without changing external behavior. Every refactoring step must be verifiable as behavior-preserving.

## Procedure

1. **Identify the goal**: What structural improvement is needed and why.
2. **Characterize existing behavior**: Ensure adequate test coverage of current behavior before changing structure.
3. **Plan incremental steps**: Break the refactoring into small, independently verifiable transformations.
4. **Execute one step at a time**: Make one structural change, verify tests still pass, then proceed.
5. **Verify continuously**: Run relevant tests after every meaningful change.
6. **Review the result**: Confirm the structural goal was achieved without behavior regression.
7. **Clean up**: Remove dead code, update imports, fix documentation.

## Characterization testing

Before refactoring code with insufficient test coverage:

- Write characterization tests that capture current behavior, including edge cases and error paths.
- These tests define "correct" as "what the code currently does," not "what we wish it did."
- Run characterization tests after each refactoring step to verify behavior preservation.
- Bug fixes discovered during refactoring should be separated into distinct commits/tasks.

## Strategies

### Extract/inline

Use for reorganizing responsibilities between functions, classes, or modules. Maintain the same public API surface while improving internal organization.

### Strangler fig

For large-scale refactoring or migration:

```text
1. Create the new structure alongside the old.
2. Route new functionality to the new structure.
3. Incrementally migrate existing functionality.
4. Remove the old structure when fully migrated.
5. Verify at each stage.
```

### Contract preservation

When refactoring code with external consumers (APIs, shared modules):

- maintain backward compatibility throughout the migration;
- use deprecation annotations when replacing public interfaces;
- provide the new API alongside the old during transition;
- document the migration path for consumers;
- create a superseding ADR when the refactoring changes architecture.

## Scope control

- Refactor only what the task requires. Do not improve adjacent code opportunistically.
- Do not mix behavior changes with structural changes in the same commit.
- If the refactoring reveals bugs, log them separately and fix them in distinct tasks unless they are trivially small.
- If the refactoring reveals a better architecture, propose it as a separate task rather than expanding scope.

## Verification

Before and after every refactoring:

- run the full test suite relevant to the changed modules;
- compare test results before and after;
- verify no previously passing tests now fail;
- for API refactoring, verify contract compatibility;
- for data model refactoring, verify migration safety;
- review the final diff to confirm only structural changes were made.

## Memory sync

After meaningful refactoring:

- update `docs/ARCHITECTURE.md` if module boundaries or dependency direction changed;
- update `docs/CONVENTIONS.md` if new patterns were established;
- create an ADR if the refactoring represents a deliberate architectural choice;
- update `docs/CURRENT_STATE.md` with the refactoring status.
