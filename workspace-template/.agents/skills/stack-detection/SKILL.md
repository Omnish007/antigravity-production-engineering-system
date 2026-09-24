---
name: stack-detection
id: SKILL-STACK-001
description: Detect the actual technology stack from repository evidence and produce a validated stack snapshot (stack.json) used by orchestration and contextual routing.
---

# Stack Detection Skill

<MISSION>
Inspect executable repository evidence (manifests, lockfiles, configuration, source files) to accurately detect the project's technology stack, validate compatibility, and produce a machine-readable `.agents/state/stack.json` snapshot.
</MISSION>

<WHEN_TO_USE>
- During initial project intake or project bootstrap (`project-init`).
- When entering an existing repository for the first time.
- When new dependencies, configuration files, or frameworks are introduced.
- When context routing requires determining the active language, frontend, backend, database, or deployment profiles.
</WHEN_TO_USE>

<WHEN_NOT_TO_USE>
- During routine code edits when the stack has already been detected, validated, and recorded in `.agents/state/stack.json`.
</WHEN_NOT_TO_USE>

<PRECONDITIONS>
- Access to repository root and configuration/manifest files.
- For formal lifecycle execution, the current task record `.agents/state/tasks/TASK-ID.json` must exist.
</PRECONDITIONS>

<NON_NEGOTIABLES>
- Base detection strictly on executable repository evidence, never on unverified assumptions or personal developer preferences.
- Produce output strictly conforming to `.agents/state/stack.schema.json`.
</NON_NEGOTIABLES>

<PROCEDURE>
```text
1. Inspect Manifests & Config
         ↓
2. Detect Languages & Runtimes
         ↓
3. Detect Frameworks & Databases
         ↓
4. Detect Tooling, Testing & CI
         ↓
5. Evaluate Compatibility
         ↓
6. Write .agents/state/stack.json
         ↓
7. Route Technology Profiles
```

### Step 1: Inspect Manifests & Configuration
Inspect the repository root and configuration files in order of priority:
- **Node.js / JS / TS**: `package.json`, `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `tsconfig.json`, `next.config.*`, `nuxt.config.*`, `vite.config.*`, `angular.json`, `svelte.config.*`.
- **Python**: `pyproject.toml`, `requirements.txt`, `poetry.lock`, `Pipfile`, `setup.py`, `manage.py`.
- **Go**: `go.mod`, `go.sum`.
- **Rust**: `Cargo.toml`, `Cargo.lock`.
- **JVM**: `pom.xml`, `build.gradle`, `build.gradle.kts`.
- **Containers & Deploy**: `Dockerfile`, `docker-compose.yml`, `vercel.json`, `k8s/`.

### Step 2: Extract Versions & Evidence Across All Dependency Scopes
For each detected technology:
1. Deeply inspect manifests across all dependency scopes: `dependencies`, `devDependencies`, `peerDependencies`, and `optionalDependencies` in `package.json`, as well as standard, optional, and test groups in `pyproject.toml`, `Cargo.toml`, and `pom.xml`. Tooling, linters, test runners, and type checkers frequently reside in `devDependencies`.
2. Extract the declared or pinned version from the manifest/lockfile across whichever scope it is declared in.
3. Record the exact detection source (e.g. `package.json:dependencies.next`, `package.json:devDependencies.typescript`).
4. Assign confidence:
   - `HIGH`: Pinned dependency in lockfile/manifest + active configuration file present.
   - `MEDIUM`: Dependency listed in manifest, but no configuration or source imports observed yet.
   - `LOW`: Inferred from indirect clues or sample fixtures.

### Step 3: Check Compatibility
Verify that detected combinations are compatible:
- Validate framework and runtime compatibility dynamically against official engine/runtime constraints (e.g. `engines.node` in `package.json`, `python_requires` in `pyproject.toml`, or the framework's official runtime compatibility matrix).
- React version vs. framework compatibility (e.g. Next.js 15/16 with React 19).
- ORM/driver version vs. database server compatibility.

### Step 4: Write Stack Snapshot
Serialize the findings into `.agents/state/stack.json` matching `.agents/state/stack.schema.json`.

### Step 5: Route Profiles
Using `.agents/technology/registry.json`, map detected technologies to their respective profiles in `.agents/technology/profiles/` and provide them to `.agents/orchestration/context-router.md`.
</PROCEDURE>

<VERIFICATION_POLICY>
- Verify that `.agents/state/stack.json` validates against `.agents/state/stack.schema.json`.
- Verify that all detected frameworks map to existing profiles in `.agents/technology/profiles/`.
</VERIFICATION_POLICY>

<DELIVERABLES>
- Validated `.agents/state/stack.json` adhering to `stack.schema.json`.
- List of active Technology Profiles for context routing.
</DELIVERABLES>
