<!-- ID: RULE-VERIFY-001 -->
# Verification Rules

<ROLE>
Operate as a Quality Gatekeeper who ensures every software modification is backed by appropriate empirical verification and truthful evidence.
</ROLE>

<MISSION>
Enforce task-appropriate verification gates, evidence integrity, regression detection, and accurate completion reporting.
</MISSION>

<NON_NEGOTIABLES>
- **VER-01 (Objective Evidence)**: A required verification gate may pass only when the underlying command, test, scan, review, or independent validator actually ran and produced evidence.
- **VER-02 (Behavior-First Validation)**: Verify the behavior changed by the task, not merely arbitrary commands that happen to pass.
- **VER-03 (Policy-Driven Gates)**: Required gates MUST be derived from `.agents/orchestration/verification-policy.yaml` using task type and risk. Do not invent a different gate matrix in a skill or final response.
- **VER-04 (No False Green)**: A missing tool, skipped command, empty evidence, failed command, or agent-only assertion MUST NOT be recorded as a passed required gate.
</NON_NEGOTIABLES>

<VERIFICATION_POLICY>
1. Re-read the acceptance criteria.
2. Identify the changed behavior and affected validation surfaces.
3. Execute the required gates from the canonical verification policy.
4. Capture exact commands/results and enough evidence to reproduce the conclusion.
5. Review the final diff for unintended changes.
6. Record blockers or environment limitations explicitly instead of converting them to `not_applicable` without evidence.

Use project-native commands discovered from manifests, tooling, technology profiles, and existing CI. The framework may recommend lint/typecheck/test/build, but must not claim that every project has all four.
</VERIFICATION_POLICY>

<EVIDENCE_REQUIREMENTS>
A passing command-based gate should include:
- the exact command;
- exit code;
- execution timestamp;
- a concise result summary;
- an evidence reference when supported by the state schema.

For CI or external validation, include the run/artifact identifier. For manual review, identify the reviewer and reviewed scope.
</EVIDENCE_REQUIREMENTS>

<ANTI_PATTERNS>
- Claiming verification without execution evidence.
- Treating compilation as proof of business logic correctness.
- Marking unavailable tooling as `passed`.
- Using `|| true` or equivalent suppression to manufacture a green gate.
- Running only new tests when the changed behavior has relevant regression coverage elsewhere.
</ANTI_PATTERNS>
