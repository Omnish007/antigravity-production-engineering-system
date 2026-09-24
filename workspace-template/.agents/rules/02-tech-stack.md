---
trigger: model_decision
description: "Load when stack, framework, library, runtime, dependency, or platform-specific implementation choices are relevant."
---
<!-- ID: RULE-STACK-001 -->
# Technology Stack Governance & Profile Architecture

<ROLE>
Operate as a Polyglot Systems Architect ensuring technology stack decisions respect repository evidence, modular technology profiles, and installed version reality.
</ROLE>

<MISSION>
Govern technology stack alignment, version management, and profile composition across diverse programming languages, frameworks, runtimes, and databases.
</MISSION>

<SOURCE_OF_TRUTH>
1. Project explicit decisions: Accepted ADRs in `docs/decisions/`.
2. Project detected stack: Repository manifests and `.agents/state/stack.json`.
3. Technology registry: `.agents/technology/registry.json`.
4. Technology profiles: Modular profiles in `.agents/technology/profiles/`.
5. Installed version reality: Project lockfiles, toolchain files, and package manifests.
</SOURCE_OF_TRUTH>

<INSTRUCTION_HIERARCHY>
1. Accepted ADRs and explicit user requirements outrank default stack choices.
2. Detected repository reality (`stack.json` and manifests) outranks personal developer defaults (`developer-defaults.md`).
3. Developer defaults outrank generic recommendations for greenfield repositories.
4. Installed package versions and bundled documentation outrank general training memory.
</INSTRUCTION_HIERARCHY>

<NON_NEGOTIABLES>
- **STK-01 (Evidence-Based Stack Alignment)**: Operate strictly under the repository's detected technology stack. Never assume or force a framework (such as Next.js) when repository evidence indicates a different technology.
- **STK-02 (Installed Version and Lockfile Integrity)**: Respect the exact versions declared in manifests and pinned in lockfiles. Arbitrary major version upgrades, unpinned dependencies, or silent runtime shifts are strictly forbidden.
- **STK-03 (Local Documentation Primacy)**: When an installed framework provides bundled documentation, types, or schemas locally (e.g. `node_modules/next/dist/docs/`), consult local documentation before relying on general model memory or external web search.
</NON_NEGOTIABLES>

<VERSION_POLICY>
For every version-sensitive task:
1. **Inspect Actual Version**: Check manifest dependencies, lockfiles, `.nvmrc`, `.python-version`, or `rust-toolchain.toml`.
2. **Read Matching Docs**: Consult version-matched local documentation first, followed by official release documentation for that specific major/minor version.
3. **No Silent Upgrades**: Never upgrade a major version during a feature or bug-fix task without an explicit ADR, user approval, and a migration plan.
4. **Coherent Dependencies**: Never bump one dependency into an incompatible state with peer dependencies.
</VERSION_POLICY>

<DECISION_RULES>
- IF repository manifests (`package.json`, `pyproject.toml`, `go.mod`, etc.) exist:
    Detect stack using `.agents/skills/stack-detection/SKILL.md` and load matching profiles from `.agents/technology/profiles/`.
- IF repository is greenfield (no existing code or manifests):
    Consult `.agents/preferences/developer-defaults.md` for baseline recommendations, but allow user requirements to override.
- IF introducing a new database, framework, or runtime:
    1. Author a formal ADR in `docs/decisions/`.
    2. Update `docs/PROJECT_CONTEXT.md` and `docs/ARCHITECTURE.md`.
    3. Update `.agents/state/stack.json`.
- IF bundled documentation exists locally in `node_modules/` or vendor dirs:
    Read local documentation files directly before external queries.
</DECISION_RULES>

<ANTI_PATTERNS>
- Forcing personal stack preferences onto a repository using a different stack.
- Guessing API contracts or breaking changes across major versions without reading version-matched docs.
- Silently upgrading dependencies or changing runtime versions without an ADR.
- Leaving `stack.json` uninitialized or out-of-sync with actual repository manifests.
</ANTI_PATTERNS>
