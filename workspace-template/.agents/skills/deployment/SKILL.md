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

## Migration safety

Prefer backwards-compatible expand/migrate/contract sequences for changes that cannot be deployed atomically.

Never perform destructive production data changes without explicit approval and a verified backup/restore or rollback strategy.

## Release

For production actions requiring approval, prepare commands/checklists but pause before executing the irreversible step.

## Smoke verification

After release, verify the smallest set of critical paths: health, authentication where applicable, critical API route, critical page, database connectivity, and error logging.
