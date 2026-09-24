# Error Recovery and Escalation Policy

<MISSION>
Provide deterministic recovery cycles and structured escalation paths when commands, tests, builds, or tasks fail, preventing thrashing, masked errors, and unrecorded retries.
</MISSION>

<NON_NEGOTIABLES>
- On any command or test failure (Exit Code != 0), your immediate next tool call must record the retry in `.agents/state/retries.json`.
- Modifying code or re-running commands without recording the failure in `retries.json` is strictly forbidden.
- Never retry the exact same failing command without changing code, environment, or strategy (no doom loops).
- Never mask failures by deleting tests, widening catch blocks, or arbitrarily increasing timeouts.
</NON_NEGOTIABLES>

<FAILURE_RECOVERY>
## Recovery cycle

```text
DETECT -> LOG RETRY -> DIAGNOSE -> ISOLATE -> REPAIR -> VERIFY
```

### 1. Detect & Immediate Trap
Recognize failure signals:
- non-zero exit codes from commands;
- type-check, lint, or test failures;
- runtime exceptions or unexpected behavior;
- build failures.

**MANDATORY IMMEDIATE ACTION**: Before touching code, write to `.agents/state/retries.json`:
- `taskId`, `failureClass`, `errorMessage`, `approach`, `attempt`, `escalationLevel`.

### 2. Diagnose
Before attempting a fix:
- read the full error message and stack trace;
- identify the failure class (client, domain, infrastructure, unexpected, agent);
- determine whether the failure is in the agent's work or pre-existing;
- check if the error matches a known pattern in project memory;
- form an explicit hypothesis about root cause.

### 3. Isolate
Contain the failure:
- do not attempt broad changes to fix a localized error;
- revert uncommitted speculative changes that made the situation worse;
- ensure successful work completed before the failure is preserved;
- identify the minimum scope of the fix.

### 4. Repair
Apply a targeted fix:
- address root cause, not symptoms;
- make the smallest coherent change;
- re-run the failed verification;
- if the first fix attempt fails, change approach rather than repeating the same action.

### 5. Verify & Closeout
After recovery passes:
- update the retry record in `.agents/state/retries.json` with `outcome: "success"`;
- log `RETRY_RESOLVED` event in `.agents/state/events/TASK-ID.jsonl`.
</FAILURE_RECOVERY>

<ESCALATION_POLICY>
## Graduated escalation

```text
Level 1: Retry with the same approach (max 2 attempts)
Level 2: Change approach or strategy (max 2 alternative approaches)
Level 3: Research the problem using documentation/web
Level 4: Reduce scope to a simpler version of the goal
Level 5: Record blocker and request human input
```

Progress through levels sequentially. Do not skip to human escalation without attempting self-recovery, but do not exhaust all levels for trivially obvious blockers.

## Iteration caps

| Phase | Max attempts before escalation |
|---|---|
| Same command/approach retry | 2 |
| Alternative approach attempts | 2 |
| Research cycles | 2 |
| Total recovery attempts per failure | 6 |

When the cap is reached, record the failure in `.agents/state/blockers.json` and request guidance.
</ESCALATION_POLICY>

<ACTION_SPACE_CONSTRAINTS>
## Stateful checkpointing

Before risky operations:
- note the current state of affected files;
- ensure work completed so far is coherent and preservable;
- if using Git, consider committing successful incremental work;
- document what has been verified and what remains.

After recovery:
- verify that the checkpoint state is still valid;
- re-run relevant verification from the last known-good state.
</ACTION_SPACE_CONSTRAINTS>

<ANTI_PATTERNS>
## Anti-patterns

Do not:
- retry the exact same failing command without changing anything (doom loop);
- add broad exception handling to mask failures;
- increase timeouts arbitrarily as a "fix";
- disable type checking, linting, or tests to make errors disappear;
- delete or modify test expectations to match incorrect behavior;
- make unrelated changes hoping something will unstick the situation;
- continue accumulating changes on top of a broken state.
</ANTI_PATTERNS>

<OUTPUT_CONTRACT>
## Failure evidence

When recording a failure, capture:
- the exact error message and exit code;
- the command or action that failed;
- the hypothesis about root cause;
- what was tried and what happened;
- the current state of the work;
- recommended next steps.

## Integration
- Retry policy configuration: `.agents/state/retries.json`
- Blocker recording: `.agents/state/blockers.json`
- Event logging: `.agents/state/events/TASK-ID.jsonl`
- Human approval gates: `.agents/orchestration/checkpoint-policy.md`
</OUTPUT_CONTRACT>
