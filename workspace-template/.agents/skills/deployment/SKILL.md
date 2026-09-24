---
name: deployment
id: SKILL-DEPLOY-001
description: Prepare, execute, and verify zero-downtime production releases using modern cloud-native deployment patterns, immutable artifacts, health checks, and automated rollback triggers.
---

# Deployment Skill

<MISSION>
Prepare, execute, and verify zero-downtime production releases using modern cloud-native deployment patterns, immutable artifacts, health checks, and automated rollback triggers.
</MISSION>

<WHEN_TO_USE>
Activate this skill when executing tasks requiring deployment capabilities, workflows, or architectural guidance.
</WHEN_TO_USE>

<PRECONDITIONS>
### Prerequisites
- The current governed task record `.agents/state/tasks/TASK-ID.json` must be `IN_PROGRESS`.
    - A `TASK_STARTED` event must be recorded in `.agents/state/events/TASK-ID.jsonl`.

### Pre-flight Checklist
- [ ] Build succeeds in production mode
    - [ ] Health endpoints respond within 2 seconds
    - [ ] Environment variables validated on startup
    - [ ] Rollback procedure documented
</PRECONDITIONS>

<NON_NEGOTIABLES>
- Expose dedicated health probes (/health/live, /health/ready).
    - Never deploy without passing all quality gates (lint, typecheck, test, build).
    - All configuration must come from environment variables (15-Factor App).
</NON_NEGOTIABLES>

<PROCEDURE>
## 15-Factor release discipline

Enforce the strict separation of lifecycle stages:
```text
Build (Compile & Package) -> Release (Artifact + Environment Config) -> Run (Process Execution)
```

- **Immutable artifacts**: Build artifacts once (e.g., container images, compiled binaries) tagged with the exact Git commit SHA. Never re-build between staging and production; promote the identical artifact.
- **Never deploy `:latest`**: Always deploy explicit, immutable version tags or content digests (`sha256:...`).
- **Config in environment**: Store configuration in the deployment environment, never baked into images or checked into source control.
- **Stateless processes**: Design processes to be stateless and disposable; share state only via attached backing services (databases, distributed caches).

## Pre-deployment readiness checklist

Verify before executing any deployment:
- [ ] **Artifact verified**: Automated quality gates (format, lint, typecheck, tests, build) passed in CI.
- [ ] **Secrets & config confirmed**: Required environment variables and secret vault references exist in the target environment.
- [ ] **Database migrations staged**: Schema changes are backwards-compatible (Expand phase) and tested against staging data volumes.
- [ ] **Rollback plan documented**: Exact commands, procedures, and conditions for rolling back are prepared and tested.
- [ ] **Monitoring & alerting active**: Dashboards for error rates, latency, and resource saturation are open and monitoring.

## Zero-downtime deployment strategies

Choose the appropriate strategy based on criticality and infrastructure capabilities:

### 1. Rolling update
- Gradually replaces instances of the previous version with instances of the new version.
- **Configuration**:
  - `maxSurge`: Maximum number of extra instances created above desired count (e.g., 25%).
  - `maxUnavailable`: Maximum number of instances unavailable during rollout (e.g., 0% for zero-downtime).
- **Best for**: Low-to-medium risk updates, stateless web and API services.

### 2. Blue / Green deployment
- Deploys the new version (Green) alongside the running version (Blue) in an identical environment.
- Validates the Green environment fully using smoke tests and internal traffic.
- Atomically shifts live traffic at the router or load balancer from Blue to Green.
- **Rollback**: Instant traffic reversion to Blue if errors are detected.
- **Best for**: High-risk releases, major framework upgrades, or services requiring instant rollback capability.

### 3. Canary deployment
- Routes a small percentage of production traffic (e.g., 2% -> 10% -> 50% -> 100%) to the new version.
- Compares Service Level Indicators (SLIs: HTTP 5xx error rate, p99 latency) between canary and baseline pods.
- **Automated rollback**: Automatically aborts rollout and shifts traffic back if canary error rates exceed thresholds.
- **Best for**: Mission-critical services, complex algorithm updates, or performance-sensitive paths.

### 4. Feature flags (Dark launching)
- Deploys new code with the execution path wrapped behind a runtime feature flag.
- Decouples deployment (shipping code) from release (enabling user visibility).
- Allows gradual percentage rollouts, user targeting, and instant feature disabling without redeployment.

## Runtime health & container lifecycle

Ensure containers and processes integrate cleanly with orchestrators:

- **Startup probe**: Allows slow-starting applications (cache initialization, warm-up) time to initialize before liveness probes start.
- **Liveness probe**: Periodically verifies the application process is healthy and not deadlocked. Restarts container on failure.
- **Readiness probe**: Verifies the application is ready to accept user traffic (database connections alive, dependencies reachable). Removes container from load balancer on failure.
- **Graceful shutdown (`SIGTERM`)**:
  1. Receive `SIGTERM` signal.
  2. Orchestrator stops sending new traffic to the instance.
  3. Complete in-flight HTTP requests within a grace period (e.g., 15-30 seconds).
  4. Flush pending log buffers and distributed traces.
  5. Close database connections and queue consumer channels.
  6. Exit cleanly with status code `0`.

## Post-deployment smoke verification

Immediately after deployment traffic shift:
1. **Health endpoint check**: Verify `/health/live` and `/health/ready` return HTTP 200.
2. **Critical path smoke tests**: Execute automated smoke tests exercising authentication, primary read path, and primary write path.
3. **Telemetry inspection**:
   - Verify log streams show no spike in `ERROR` or unhandled exceptions;
   - Verify p95/p99 latency remains within the established Service Level Objective (SLO);
   - Verify database connection pool metrics are healthy.

## Rollback trigger criteria

Trigger an immediate rollback if within 15 minutes of release:
- HTTP 5xx error rate increases by more than 0.5% above baseline;
- p95 latency exceeds SLO threshold by more than 50%;
- Unhandled critical exceptions appear in structured logs;
- Data corruption or integrity violation is detected.
</PROCEDURE>

<VERIFICATION_POLICY>
### Exit Criteria
Production build and deployment verification smoke test pass with exit code 0.
</VERIFICATION_POLICY>

<DELIVERABLES>
- Deployment configuration, environment manifests, CI/CD pipeline definitions.
- Post-deployment health check verification evidence.
</DELIVERABLES>
