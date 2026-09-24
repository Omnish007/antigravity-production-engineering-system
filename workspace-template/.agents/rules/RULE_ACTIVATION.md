---
title: Rule Activation Contract
---

# Rule Activation Contract

The runtime activation contract is **platform-native YAML frontmatter on each rule file** plus the repository-level routing table in `rule-activation.yaml`. The routing table is a documentation/audit index; it is not a substitute for the platform trigger metadata.

## Supported runtime triggers

- `always_on`: loaded for every model invocation.
- `model_decision`: the runtime selects the rule from the task/context.
- `glob`: selected when the target files match the rule's `globs`.
- `manual`: loaded only when explicitly requested.

Every modular rule under `.agents/rules/*.md` must contain valid frontmatter with a supported `trigger`. `model_decision` rules must provide a useful `description`; `glob` rules must provide `globs`.

## Layering

`AGENTS.md` remains the repository bootstrap contract and is always authoritative. `always_on` rules provide universal constraints. The context router, task classifier, technology profiles, skills, and project documents narrow the runtime context for the current request.

## Reliability rule

Do not claim a rule, policy, or skill was loaded merely because it is listed in a registry. The agent must read the actual file or receive runtime evidence that the file was loaded.
