---
name: deployment
description: Prepare and verify production releases with configuration, build, health, rollback, migration, security, and smoke-test discipline.
---

# Deployment Skill

## Pre-deployment

Verify:

- application build succeeds;
- required environment variables are documented and present in the deployment system;
- secrets are not embedded in artifacts;
- database migration/backfill plan is safe;
- health/readiness checks exist where required;
- observability and logs are adequate;
- dependencies have no known release-blocking issue;
- rollback/forward-fix path is understood.

## Runtime

Configure:

- HTTPS/TLS at the appropriate boundary;
- secure headers;
- restricted CORS;
- resource limits;
- graceful shutdown;
- health checks;
- timeouts for dependencies.

## Deployment strategies

Choose the appropriate deployment strategy based on risk and infrastructure:

- **Rolling update**: Default for low-risk changes. Gradually replace instances.
- **Blue/green**: Maintain two identical environments; switch traffic atomically. Use for high-risk changes requiring instant rollback.
- **Canary**: Route a percentage of traffic to the new version; monitor before full rollout. Use for changes where gradual confidence building is needed.
- **Feature flags**: Deploy code changes behind flags for runtime activation. Use for decoupling deployment from release.

Document the chosen strategy in the deployment plan and rollback procedure.

## Feature flag rollout

When using feature flags for deployment:

- start with internal/staff users;
- expand to a small percentage;
- monitor error rates, latency, and business metrics;
- expand to full traffic;
- clean up the flag after stable rollout.

## Infrastructure as code

When infrastructure configuration exists:

- validate configuration changes before applying;
- use version-controlled infrastructure definitions;
- test infrastructure changes in staging before production;
- document infrastructure dependencies and resource limits.

## Container security

When using containerized deployments:

- scan container images for known vulnerabilities;
- use minimal base images;
- do not run containers as root;
- do not embed secrets in images;
- pin image versions rather than using `:latest`.

## Service level objectives

Where SLOs are defined:

- monitor SLIs (latency, error rate, availability) aligned with SLOs;
- set alerting thresholds below the SLO to allow response time;
- document SLOs, error budgets, and escalation procedures;
- review SLO compliance as part of deployment verification.

## Migration safety

Prefer backwards-compatible expand/migrate/contract sequences for changes that cannot be deployed atomically.

Never perform destructive production data changes without explicit approval and a verified backup/restore or rollback strategy.

## Release

For production actions requiring approval, prepare commands/checklists but pause before executing the irreversible step.

## Smoke verification

After release, verify the smallest set of critical paths: health, authentication where applicable, critical API route, critical page, database connectivity, and error logging.
