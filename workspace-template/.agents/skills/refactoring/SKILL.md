---
name: refactoring
id: SKILL-REFACTOR-001
description: Perform behavior-preserving code transformations with characterization testing, incremental maneuvers, Martin Fowler's refactoring patterns, and full regression safety.
---

# Refactoring Skill

<MISSION>
Perform behavior-preserving code transformations with characterization testing, incremental maneuvers, Martin Fowler's refactoring patterns, and full regression safety.
</MISSION>

<WHEN_TO_USE>
Activate this skill when executing tasks requiring refactoring capabilities, workflows, or architectural guidance.
</WHEN_TO_USE>

<PRECONDITIONS>
### Prerequisites
- Active task in .agents/state/tasks.json must be IN_PROGRESS.
    - TASK_STARTED event must be recorded in .agents/state/events.jsonl.

### Pre-flight Checklist
- [ ] Tests pass before change
    - [ ] Structural refactor applied
    - [ ] Tests pass after change
    - [ ] No behavior altered
</PRECONDITIONS>

<NON_NEGOTIABLES>
- Automated tests must pass BEFORE and AFTER refactoring.
    - Zero change in observable external behavior.
    - Refactoring must be surgical and focused on a single structural improvement.
</NON_NEGOTIABLES>

<PROCEDURE>
## Core principle (Martin Fowler's Refactoring)

> **Refactoring is a disciplined technique for restructuring an existing body of code, altering its internal structure without changing its external behavior.**

Key principles:
- **Two hats**: When programming, switch between two distinct activities: adding functionality (no refactoring) and refactoring (no new features). Never mix both in the same commit.
- **Micro-steps**: Refactor through tiny, behavior-preserving transformations backed by automated tests.
- **Leave it cleaner (The Boy Scout Rule)**: Leave the code in a slightly better state than you found it.

## The Refactoring lifecycle

```text
Assess Coverage -> Characterize Behavior -> Plan Maneuvers -> Execute Micro-Steps -> Verify -> Clean Up
```

### 1. Characterization testing
Before refactoring code with inadequate or uncertain test coverage:
- Write **characterization tests** to capture the actual current behavior, including edge cases, boundary values, and error paths.
- Define "correct" as "what the system currently does in production," not "what we think it should do."
- Ensure tests run fast and deterministically.

### 2. Standard refactoring catalog

Apply established refactoring maneuvers:

#### Composing functions
- **Extract Function**: Break long functions (>25 lines) into smaller, well-named functions that express intent.
- **Replace Temp with Query**: Replace temporary variables storing calculations with dedicated pure functions.
- **Introduce Explaining Variable**: Break down complex expressions into named intermediate variables.

#### Simplifying conditionals
- **Replace Nested Conditionals with Guard Clauses**: Use early returns to eliminate deep indentation and improve readability.
- **Decompose Conditional**: Extract complex boolean conditions into clearly named helper predicates.
- **Replace Conditional with Polymorphism / Strategy**: Replace `switch` or `if/else` chains dispatching on type codes with polymorphic classes or strategy objects.

#### Organizing data & parameters
- **Introduce Parameter Object**: Replace parameter lists with 4+ arguments with a typed configuration or DTO object.
- **Preserve Whole Object**: Pass the entire domain object instead of extracting multiple individual properties.
- **Separate Query from Modifier (CQS)**: Ensure functions either return a value (query) or modify state (command), never both.

#### Moving features between objects
- **Move Function / Field**: Move responsibilities to the class or module that holds the data it operates on (improving cohesion).
- **Hide Delegate (Law of Demeter)**: Provide direct helper methods on immediate collaborators rather than reaching through objects (`a.getB().getC().doSomething()`).

## Large-scale architectural refactoring

For major structural transitions across services, databases, or frameworks:

### 1. Strangler Fig pattern
- Build the new service or module alongside the legacy system.
- Route new functionality directly to the new implementation.
- Incrementally migrate existing endpoints or capabilities one by one.
- Decommission the legacy system only after 100% traffic migration and parity verification.

### 2. Branch by Abstraction
- Introduce an abstraction (interface/port) in front of the code to be replaced.
- Point existing callers to the abstraction.
- Create the new implementation behind the abstraction.
- Switch the implementation via configuration or dependency injection.
- Remove the old implementation and inline the abstraction if no longer needed.

### 3. The Mikado Method
For complex refactorings with cascading dependencies:
1. Set the ultimate refactoring goal.
2. Attempt the change directly and observe what breaks (compiler errors, failing tests).
3. Revert the change (`git reset`).
4. Record the prerequisite sub-goals on a dependency graph (Mikado graph).
5. Solve leaf prerequisites first, committing each step cleanly, until the primary goal succeeds.
</PROCEDURE>

<VERIFICATION_POLICY>
## Verification & regression prevention

After every micro-step:
- Run the focused test suite for the modified module.
- Confirm all tests pass with zero regression.
- Review `git diff` to ensure only structural changes were made—no accidental feature changes or bug fixes mixed in.

## Memory synchronization

After completing meaningful refactoring:
- Update `docs/ARCHITECTURE.md` if module boundaries, interfaces, or dependency direction changed.
- Update `docs/CONVENTIONS.md` if new design patterns or coding conventions were adopted.
- Record an ADR in `docs/decisions/` if the refactoring represented an architectural pivot.

### Exit Criteria
Refactored code verified with 100% test pass rate and clean diff.
</VERIFICATION_POLICY>

<DELIVERABLES>
- Refactored code with improved structure and maintainability.
- Preserved behavior verified by passing tests before and after the refactor.
</DELIVERABLES>
