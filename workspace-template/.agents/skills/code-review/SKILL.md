---
name: code-review
id: SKILL-REVIEW-001
description: Conduct rigorous, constructive code reviews based on Google Engineering Practices to maintain codebase health, correctness, security, simplicity, and test quality.
---

# Code Review Skill

<MISSION>
Conduct rigorous, constructive code reviews based on Google Engineering Practices to maintain codebase health, correctness, security, simplicity, and test quality.
</MISSION>

<WHEN_TO_USE>
Activate this skill when executing tasks requiring code-review capabilities, workflows, or architectural guidance.
</WHEN_TO_USE>

<PRECONDITIONS>
### Prerequisites
- Active task in .agents/state/tasks.json must be IN_PROGRESS.
    - TASK_STARTED event must be recorded in .agents/state/events.jsonl.

### Pre-flight Checklist
- [ ] Diff inspected for scope adherence
    - [ ] Security and trust boundaries verified
    - [ ] Quality gates evaluated
    - [ ] Feedback documented with actionable recommendations
</PRECONDITIONS>

<NON_NEGOTIABLES>
- Review diff against 00-core.md, 04-coding.md, and 07-security.md.
    - Verify zero secrets, credentials, or PII are exposed in the diff.
    - Verify no dead code, orphaned imports, or speculative abstractions were added.
</NON_NEGOTIABLES>

<PROCEDURE>
## Core philosophy (Google Engineering Practices)

The primary purpose of code review is to **maintain and improve the overall health of the codebase over time**. 

Key principles:
- **Code health over perfection**: A change should be approved if it improves the overall codebase health, even if it is not completely perfect.
- **Mentorship & shared ownership**: Reviews are educational exchanges that align the team on architecture, conventions, and quality.
- **Explain the "why"**: Always explain the rationale behind review comments and propose concrete alternatives.
- **Surgical scope**: Distinguish between issues introduced by the current change versus pre-existing technical debt. Do not block a PR on unrelated pre-existing debt.

## Review evaluation dimensions

Review every change across seven essential dimensions:

### 1. Design & Architecture
- Does this change fit the overall system architecture (`docs/ARCHITECTURE.md`)?
- Does it respect domain boundaries and the allowed dependency direction?
- Is the new capability placed in the right module or layer?
- Does it introduce premature abstractions or unnecessary microservices?

### 2. Functionality & Correctness
- Does the code completely satisfy the stated acceptance criteria and PRD?
- Does it handle boundary conditions (null/empty, zero, maximum limits, special characters)?
- Are race conditions, concurrency hazards, or deadlocks possible?
- Is error handling explicit, safe, and actionable?

### 3. Complexity (KISS & YAGNI)
- Could the code be simpler? Could another engineer understand and modify it easily?
- Does it contain speculative functionality or over-engineered flexibility?
- Are functions and classes focused on a single responsibility?
- Does it avoid deep nesting, magic values, and unnecessary indirection?

### 4. Tests & Verification
- Are there automated tests accompanying the change?
- Do the tests cover meaningful failure modes, edge cases, and security boundaries?
- Are the tests readable, isolated, deterministic, and free of flakiness?
- Do tests assert behavior rather than internal implementation trivia?

### 5. Naming & Documentation
- Do variable, function, class, and file names clearly communicate domain intent?
- Do comments explain **why** something was done (invariants, trade-offs), rather than restating what the code does?
- Are relevant docs (`docs/ARCHITECTURE.md`, `docs/CONVENTIONS.md`, ADRs) updated to reflect durable changes?

### 6. Security & Privacy
- Are all external inputs validated server-side against strict schemas?
- Are authorization checks enforced on the specific resource and action?
- Are parameterized queries used to prevent injection?
- Are secrets kept out of code, and is sensitive data (PII) masked from logs?

### 7. Performance & Resource Hygiene
- Are there obvious algorithmic bottlenecks ($O(n^2)$ on unbounded sets)?
- Does the change introduce N+1 query patterns or unindexed database lookups?
- Are database connections, file handles, and network sockets deterministically released?

## Finding severity classification

Label every finding with an explicit severity level:

| Severity | Definition | Merge Impact |
|---|---|---|
| **BLOCKER / CRITICAL** | Security vulnerability, data loss risk, severe functional defect, or broken public API contract. | Must be resolved before merge. |
| **HIGH** | Significant bug, architectural violation, missing critical test, or concurrency hazard. | Must be resolved before merge. |
| **MEDIUM** | Code smell, suboptimal performance, missing edge-case test, or convention deviation. | Should be addressed or tracked as follow-up. |
| **NIT / LOW** | Minor readability improvement, typo, or stylistic suggestion. | Optional; author may choose to address or defer. |

## Review comment structure

Format constructive findings using the standard pattern:
```markdown
**[SEVERITY] `<Concise Issue Title>`**
- **Location**: `path/to/file:line`
- **Issue**: Clear explanation of the problem and why it matters.
- **Suggestion**: Concrete code snippet or recommended alternative approach.
```

## Final approval standard

Before approving a change, verify:
- [ ] All critical and high findings have been resolved;
- [ ] Automated tests pass and provide sufficient behavioral evidence;
- [ ] The diff is surgical with no unrelated changes or debug artifacts;
- [ ] Project memory and documentation are updated.
</PROCEDURE>

<VERIFICATION_POLICY>
### Exit Criteria
Formal review report with pass/fail evaluation on all quality gates.
</VERIFICATION_POLICY>

<DELIVERABLES>
- Structured code review report with severity levels, identified defects, and concrete remediations.
</DELIVERABLES>
