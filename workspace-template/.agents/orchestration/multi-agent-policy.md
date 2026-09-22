# Multi-Agent Orchestration Policy

<MISSION>
Define safe patterns for delegating work across multiple agent sessions, sub-agents, or parallel agent instances while maintaining consistency, avoiding conflicts, and preserving project memory integrity.
</MISSION>

<NON_NEGOTIABLES>
- Multiple agents working in parallel MUST NOT edit the same files simultaneously. Ownership must be tracked in `.agents/state/agents.json`.
- Only the Coordinator (`mainAgent: true`) may invoke or spawn subagents via `invoke_subagent`. Specialist subagents must NEVER spawn subagents.
- No sub-agent may bypass the checkpoint policy independently.
- No sub-agent may make architectural decisions without orchestrator awareness.
- All sub-agent work must be verified before integration.
- Sub-agents must not create ADRs independently; escalate decisions to the orchestrator.
- Memory synchronization must happen centrally after parallel phases complete.
- Canonical state files (`tasks/TASK-xxx.json`, `governance/TASK-xxx.json`, `events/TASK-xxx.jsonl`) are managed per-task to prevent multi-agent write collisions.
</NON_NEGOTIABLES>

<WHEN_TO_USE>
## When to use multi-agent patterns

Multi-agent decomposition is appropriate when:
- a task naturally separates into independent, parallelizable units;
- context requirements exceed what a single session can hold effectively;
- specialized reasoning is needed for distinct sub-problems (e.g., security review vs. performance optimization);
- long-running work benefits from fresh context for each phase.

Do not use multi-agent patterns merely because a task is large. A single agent with a clear plan is often more effective than poorly coordinated parallel work.
</WHEN_TO_USE>

<EXECUTION_POLICY>
## Delegation patterns

### Discovery → Plan → Execute

```text
Phase 1 (Discovery Agent):
  - Research codebase
  - Identify affected files and boundaries
  - Produce Implementation Plan artifact

Phase 2 (Planning Agent):
  - Review implementation plan
  - Validate against architecture and constraints
  - Decompose into executable task graph
  - Identify safe parallelism

Phase 3 (Execution Agents):
  - Each agent executes a focused task unit
  - Isolated context per task
  - Produces verification evidence

Phase 4 (Integration Agent):
  - Reconcile parallel outputs
  - Run integrated verification
  - Synchronize project memory
```

### Orchestrator-Worker

```text
Orchestrator:
  - Decomposes high-level goal into sub-tasks
  - Assigns sub-tasks to worker agents
  - Monitors progress and handles dependencies
  - Synthesizes final result and verification

Workers:
  - Execute focused, well-defined sub-tasks
  - Return structured results and evidence
  - Do not make architectural decisions independently
  - Escalate blockers to orchestrator
```

## Context handoff protocol

When transferring work between agent sessions:
1. **State summary**: What was accomplished, what remains, what was verified.
2. **Key decisions**: Any decisions made during the session with rationale.
3. **Blockers**: Any issues that prevented completion.
4. **File inventory**: Files created, modified, or that need attention.
5. **Verification status**: What has been tested and what has not.
6. **Memory sync status**: Whether project memory has been updated.

Store the handoff in a structured artifact. Do not rely on the receiving agent having access to the sending agent's conversation history.
</EXECUTION_POLICY>

<ACTION_SPACE_CONSTRAINTS>
## Conflict prevention

When multiple agents work in the same repository:
- use `parallel-work-policy.md` to identify safe parallelism;
- assign non-overlapping file sets to each agent;
- use `worktree-policy.md` when file overlap is unavoidable;
- coordinate shared configuration and dependency changes centrally;
- never assume a clean merge means semantic correctness.

## Sub-agent guidelines

When spawning sub-agents:
- Only the Coordinator (`mainAgent: true`) invokes subagents.
- Specialist subagents must NEVER invoke subagents or spawn child agents.
- provide explicit task scope, acceptance criteria, and constraints;
- specify which project rules and skills apply;
- define the expected output format;
- set iteration and time limits;
- require verification evidence in the sub-agent's response.
</ACTION_SPACE_CONSTRAINTS>

<MEMORY_POLICY>
## Memory synchronization

When multiple agents contribute to a task:
- designate one agent or phase as the memory synchronization owner;
- do not allow parallel, uncoordinated updates to the same project memory file;
- reconcile memory updates after parallel work completes;
- use `.agents/state/agents.json` to track active roles and ownership.
</MEMORY_POLICY>

<SAFETY_CONSTRAINTS>
## Safety invariants

- Only the Coordinator (`mainAgent: true`) may spawn subagents. Specialists are strictly forbidden from spawning child subagents.
- No sub-agent may bypass the checkpoint policy independently.
- No sub-agent may make architectural decisions without orchestrator awareness.
- All sub-agent work must be verified before integration.
- Sub-agents should not create ADRs independently; escalate decisions to the orchestrator.
- Memory synchronization must happen centrally after parallel phases complete.
</SAFETY_CONSTRAINTS>
