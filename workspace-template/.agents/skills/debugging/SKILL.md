---
name: debugging
id: SKILL-DEBUG-001
description: Perform rigorous, evidence-driven root-cause investigation across frontend, backend, database, and distributed systems using the scientific method.
---

# Debugging Skill

<MISSION>
Perform rigorous, evidence-driven root-cause investigation across frontend, backend, database, and distributed systems using the scientific method.
</MISSION>

<WHEN_TO_USE>
Activate this skill when executing tasks requiring debugging capabilities, workflows, or architectural guidance.
</WHEN_TO_USE>

<PRECONDITIONS>
### Prerequisites
- Active task in .agents/state/tasks.json must be IN_PROGRESS.
    - TASK_STARTED event must be recorded in .agents/state/events.jsonl.

### Pre-flight Checklist
- [ ] Failure logged to retries.json
    - [ ] Error message and stack trace diagnosed
    - [ ] Root cause isolated from symptoms
    - [ ] Targeted fix applied and verified
</PRECONDITIONS>

<NON_NEGOTIABLES>
- ON FAILURE: Immediately append record to .agents/state/retries.json before editing code.
    - Form explicit hypothesis from error trace before modifying files.
    - Change approach if the same fix fails twice (anti-doom loop).
</NON_NEGOTIABLES>

<PROCEDURE>
## The Scientific Debugging Method

Root-cause investigation must be systematic and evidence-driven. Never guess or apply speculative fixes. Follow the cycle:

```text
Observe -> Minimal Reproduction -> Isolate Boundary -> Formulate Hypotheses -> Discriminating Test -> Root Cause -> Verify
```

### 1. Observe and construct Minimal Reproducible Example (MRE)
- Capture the exact failure symptom: error message, stack trace, HTTP status, anomalous output, or unexpected state.
- Identify the trigger preconditions: input payload, environment variables, authentication context, database seed state, network conditions.
- Construct the smallest possible test case or script that reliably triggers the failure.

### 2. Isolate the failure boundary
Divide the execution path systematically to isolate the failure layer:
- **Client / UI**: State transition, component render, event handler, browser API failure.
- **Network / Transport**: Request payload serialization, HTTP headers, CORS, TLS, timeout, proxy routing.
- **API / Gateway**: Route matching, authentication token validation, schema deserialization.
- **Application / Domain**: Business logic invariant violation, state machine error, null/nil pointer dereference.
- **Persistence / Database**: Constraint violation, transaction isolation anomaly, deadlocks, missing index scan.
- **External Dependency**: Third-party API rate limit, socket exhaustion, protocol mismatch.

Use **binary search (bisection)** across the call stack, data pipeline, or Git commit history (`git bisect`) to rapidly narrow down when and where the fault was introduced.

### 3. Formulate falsifiable hypotheses

For non-trivial bugs, maintain an explicit **Hypothesis Matrix**:

| # | Hypothesis (Suspected Root Cause) | Supporting Evidence | Refuting Evidence | Discriminating Experiment | Outcome |
|---|---|---|---|---|---|
| 1 | Race condition on concurrent token refresh | Intermittent 401s under load | Passes in sequential tests | Run 10 parallel refresh requests | Confirmed |
| 2 | Clock skew between services | Token expired prematurely | Token lifetime is 1 hour | Inspect server vs client UTC clocks | Refuted |

### 4. Conduct discriminating experiments
- Change only **one variable at a time**.
- Design experiments that can definitively prove or disprove the hypothesis.
- If an experiment fails to reproduce or refute the issue, revert changes before testing the next hypothesis.

### 5. Root-cause identification (The 5 Whys)
Do not stop at the immediate symptom. Ask "Why?" until the systemic root cause is exposed:
1. *Why did the request fail?* -> The database query timed out.
2. *Why did the query time out?* -> It executed a full table scan on 2 million rows.
3. *Why did it perform a full table scan?* -> The compound index did not match the query predicate order (ESR rule violated).
4. *Why was the index ordered incorrectly?* -> The schema migration was created without profiling the actual query shape.
5. *Why was it not profiled?* -> Missing query execution plan validation in CI.

## Specialized diagnostic toolchains

- **Memory & Leaks**: Heap profiling, allocation flamegraphs, garbage collection pause logs.
- **Concurrency & Deadlocks**: Thread dumps, goroutine stack dumps, race detectors (`go test -race`, ThreadSanitizer).
- **Network & APIs**: cURL with timing breakdowns (`curl -w "@curl-format.txt"`), packet inspection, HTTP request/response diffing.
- **Database & Queries**: `EXPLAIN ANALYZE`, lock contention queries, slow query logs, transaction isolation inspection.

## Debugging anti-patterns

Do not:
- **Shotgun debug**: Change multiple lines across multiple files hoping the bug disappears.
- **Paper over the symptom**: Catch exceptions and return default values without understanding why the exception was thrown.
- **Mask timing issues with sleeps**: Add arbitrary delays (`sleep(500)`) instead of proper synchronization (promises, locks, channels, conditions).
- **Disable security or validation**: Turn off auth, CSP, or schema validation to "make the test pass."
- **Assume without verifying**: Trust comments, assumptions, or stale documentation over what the runtime is actually doing.

## Investigation output

Document the investigation findings:
- **Symptoms**: Exact error messages, logs, and reproduction steps.
- **Root Cause**: The underlying flaw that produced the failure.
- **Minimal Fix**: The smallest coherent change that resolves the root cause.
- **Regression Prevention**: The automated test added to guarantee this bug cannot recur.
</PROCEDURE>

<VERIFICATION_POLICY>
### Exit Criteria
Failing test/command succeeds with exit code 0 and retry record marked resolved.
</VERIFICATION_POLICY>

<DELIVERABLES>
- Diagnostic hypothesis, reproduction script or test case, and isolated root cause analysis.
</DELIVERABLES>
