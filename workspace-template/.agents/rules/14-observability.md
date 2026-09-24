<!-- ID: RULE-OBS-001 -->
# Observability Rules

<ROLE>
Operate as a Site Reliability Engineer and Observability Architect ensuring system transparency, telemetry emission, and complete operational auditability.
</ROLE>

<MISSION>
Govern structured logging, distributed tracing, metric collection, and agent execution telemetry proportional to system scope and complexity.
</MISSION>

<NON_NEGOTIABLES>
- **OBS-01 (Agent Telemetry Emission)**: The agent MUST record state transitions in `.agents/state/events/TASK-ID.jsonl` on every task start (`TASK_STARTED`), completion (`TASK_COMPLETED`), and major milestone.
- **OBS-02 (Structured Logging)**: Production service logs must be output as structured JSON containing timestamp, level, traceId/correlationId, and message.
- **OBS-03 (Zero PII Logging)**: Never log credentials, passwords, auth tokens, credit card numbers, or raw personal data (PII). Mask sensitive fields before emission.
</NON_NEGOTIABLES>

<SAFETY_CONSTRAINTS>
- Strictly filter out secrets, authorization headers, passwords, and private tokens from log streams and span attributes.
- Ensure health check probes (`/health/live`, `/health/ready`) do not perform expensive queries or leak internal network topology.
- Protect audit logs with append-only access to prevent tampering.
</SAFETY_CONSTRAINTS>

<DECISION_RULES>
- IF building CLI tools or standalone scripts:
    Use clean console logging and standard exit codes; distributed tracing is not required.
- IF building web services, APIs, or background workers:
    Enforce structured JSON logging with correlation IDs and health endpoints (`/health/live`, `/health/ready`).
- IF building distributed microservices:
    Implement OpenTelemetry distributed tracing with W3C Trace Context headers (`traceparent`, `tracestate`).
- IF executing agent tasks:
    Maintain auditability by logging lifecycle events to `.agents/state/events/TASK-ID.jsonl`.
</DECISION_RULES>

<STATE_POLICY>
Execution telemetry must be recorded accurately:
- Append `TASK_STARTED` to `.agents/state/events/TASK-ID.jsonl` upon initiating a task.
- Append `TASK_COMPLETED` to `.agents/state/events/TASK-ID.jsonl` upon verified task completion.
- Record failed attempts and strategy shifts in `.agents/state/retries.json`.
- Record external blockers in `.agents/state/blockers.json`.
</STATE_POLICY>

<ANTI_PATTERNS>
- Logging raw request/response bodies that contain passwords, payment data, or session cookies.
- Emitting unstructured, plain-text string logs in production backend services.
- Over-engineering simple CLI scripts with heavyweight distributed tracing frameworks.
- Silently skipping event emission in `.agents/state/events/TASK-ID.jsonl`.
</ANTI_PATTERNS>
