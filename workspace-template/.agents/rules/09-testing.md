<!-- ID: RULE-TEST-001 -->
# Testing Rules

<MISSION>
Govern risk-based, polyglot test design, execution, and deterministic evidence collection across all project layers.
</MISSION>

<NON_NEGOTIABLES>
- **TST-01 (Proportionate Verification Mandate)**: Every behavior change requires proportionate, reproducible verification. Automated tests are the default where practical and valuable; where automated tests are impractical or disproportionate, explicit contract checks, type validation, or reproducible verification commands must provide equivalent empirical proof. Non-behavioral changes (copy, docs, styling tokens) must verify against existing test suites with exit code 0.
- **TST-02 (TDD Reproduction for Bugs)**: For any bug fix, the agent MUST write a reproducing test first to prove the bug exists, then implement the fix, then verify the test passes.
- **TST-03 (Deterministic Tests)**: Tests must be deterministic, isolated, and hermetic. Never rely on sleep timeouts; use event listeners, condition polling, or fake timers.
</NON_NEGOTIABLES>

<DECISION_RULES>
- IF fixing a reported defect:
    Write a failing test case that reproduces the defect before modifying production code.
- IF introducing or altering business logic:
    Add unit tests for happy paths, edge cases, and explicit error states.
- IF creating or modifying an API endpoint:
    Add integration tests verifying input validation (400), authentication (401), authorization (403), and success envelopes.
- IF modifying database schemas or queries:
    Add integration tests verifying transactions, constraints, and index query execution plans.
- IF updating user-facing UI workflows:
    Run automated accessibility checks (axe-core) and component/E2E interaction tests.
</DECISION_RULES>

<EXECUTION_POLICY>
1. **Scope Assessment**: Identify affected modules, interfaces, and potential blast radius.
2. **Reproduction (if bug)**: Implement test that fails with the reported behavior.
3. **Implementation**: Write the minimal code that satisfies the test.
4. **Graduated Verification**:
   - Step 1: Run focused tests for changed files.
   - Step 2: Run related integration/contract tests.
   - Step 3: Run full test suite for cross-cutting or architectural changes.
   - Step 4: Run format, lint, typecheck, and build checks.
5. **Evidence Collection**: Capture test runner output and exit code.
</EXECUTION_POLICY>

<VERIFICATION_POLICY>
A test execution is considered valid only when:
- The test runner terminates with exit code 0.
- All newly added and existing tests pass.
- No test is disabled, skipped, or commented out to bypass failures.
- No tests rely on arbitrary sleep timeouts.
</VERIFICATION_POLICY>

<EVIDENCE_REQUIREMENTS>
- Plain statements such as "tests passed" are invalid without empirical proof.
- Record command invocations, total test counts, and terminal exit codes.
- Identify any skipped, quarantined, or blocked tests explicitly with rationale.
</EVIDENCE_REQUIREMENTS>

<EXCEPTIONS>
- Pure documentation edits (`.md` files) do not require new automated tests, but must not break existing test runs.
- Static assets (images, icons, pure CSS variables) do not require dedicated unit tests, but require build verification.
</EXCEPTIONS>
