# Instruction Tag Standard

This document defines the canonical literal wrapper language used across the Antigravity Production Engineering System.

## 1. Purpose and Philosophy

Modern Large Language Models (LLMs) such as Gemini, Claude, and GPT-4 process instructions more reliably when different semantic components—identity, priorities, constraints, action space, tool policy, execution procedures, context policy, decision rules, verification, and output contracts—are cleanly delimited.

As recommended by Google's Gemini prompting and tool-use guidance:
- Clear delimiters (such as XML-style tags) help models distinguish instructions, constraints, context, and output formats.
- Delimiters provide **semantic structure**, not emotional emphasis.
- Delimiters are **internal instruction-file markers**, NOT native Antigravity runtime control primitives or live tool-call protocols.

## 2. Inviolable Invariants

1. **Static Instruction Structure Only**: Tags are used exclusively inside instruction-oriented Markdown files.
2. **Never a Tool-Call Protocol**: An agent must NEVER be instructed to emit XML wrappers (such as `<UPDATE>` or `<ACTION_SPACE_CONSTRAINTS>`) before or after calling a tool. Function calling proceeds directly via native tool invocation.
3. **Native Skill Frontmatter**: In Antigravity Skill files (`SKILL.md`), YAML frontmatter (`--- name: ... description: ... ---`) must remain native and unencumbered at the top of the file. XML tags belong only in the Markdown body.
4. **Machine-Readable Cleanliness**: All `*.json`, `*.jsonl`, and `*.schema.json` files must remain pure machine-readable data with ZERO XML wrappers.
5. **Human-Readable Memory**: Ordinary ADRs (`docs/decisions/*.md`) and project memory files (`docs/*.md`) remain human-readable Markdown without artificial XML tagging. Only the rules and skills governing their creation and maintenance use wrappers.

---

## 3. Approved Canonical Tag Vocabulary

Only tags in this canonical vocabulary are permitted. Synonyms, improvised tags, or emotional-emphasis tags are strictly forbidden.

### A. Core Identity & Priorities

| Tag | Responsibility | Example Content |
|---|---|---|
| `<ROLE>` | Defines who/what the agent operates as. | Agent persona and operating environment. |
| `<MISSION>` | Defines the primary objective and responsibility of the file. | Clear purpose statement. |
| `<INSTRUCTION_HIERARCHY>` | Defines conflict resolution precedence between rules, user instructions, and ADRs. | Explicit override order. |
| `<PRIORITIES>` | Defines trade-off ordering when goals conflict. | Ranked priority list (e.g. 1. Safety, 2. Correctness). |

### B. Constraints & Safety

| Tag | Responsibility | Example Content |
|---|---|---|
| `<NON_NEGOTIABLES>` | Genuinely mandatory, non-negotiable rules and invariants. | Hard invariants and boundary rules. |
| `<SAFETY_CONSTRAINTS>` | Security and threat-mitigation boundaries. | Secret exposure, injection defense, privilege escalation. |
| `<ACTION_SPACE_CONSTRAINTS>` | Conceptual action permissions across action classes. | Categorized into `<READ>`, `<WRITE>`, `<EXECUTE>`, `<DELETE>`, `<NETWORK>`, `<CREDENTIAL>`, `<PRODUCTION>`, `<EXTERNAL_SIDE_EFFECT>`. |
| `<PROHIBITED_ACTIONS>` | Concise list of strictly disallowed behaviors. | Targeted list of forbidden actions. |

### C. Tools & Execution

| Tag | Responsibility | Example Content |
|---|---|---|
| `<TOOL_POLICY>` | Safe, disciplined tool usage principles. | Categorized into `<GENERAL>`, `<INSPECTION>`, `<DESTRUCTIVE_OPERATIONS>`, `<UNTRUSTED_CONTENT>`, `<SECRETS>`, `<FAILURE>`. |
| `<EXECUTION_POLICY>` | Ordered execution procedure or lifecycle sequence. | Numbered execution phases. |
| `<PRECONDITIONS>` | Conditions that must be satisfied before execution starts. | Required state, files, or stack readiness. |
| `<DECISION_RULES>` | Conditional logic and deterministic decision tables. | `IF ... THEN ... ELSE ...` rules. |
| `<ESCALATION_POLICY>` | Conditions requiring the agent to pause and ask the human. | Irreversible choices, ambiguous requirements. |

### D. Context & Memory

| Tag | Responsibility | Example Content |
|---|---|---|
| `<CONTEXT_POLICY>` | Minimum sufficient context loading order. | Hierarchical loading priority. |
| `<SOURCE_OF_TRUTH>` | Mapping of facts to their authoritative sources. | Where decisions, architecture, and versions live. |
| `<MEMORY_POLICY>` | Rules governing reading and updating durable repository memory. | Memory durability vs transient chat. |
| `<STATE_POLICY>` | Rules governing machine-readable execution state. | Separation of state from narrative prose. |
| `<READ_POLICY>` | Guidelines for inspecting files and memory. | Targeted inspection principles. |
| `<WRITE_POLICY>` | Guidelines for modifying files and state. | Atomic, surgical update rules. |

### E. Verification & Output

| Tag | Responsibility | Example Content |
|---|---|---|
| `<VERIFICATION_POLICY>` | Mandatory checks and gates required before completion. | Test, build, typecheck, and lint gates. |
| `<EVIDENCE_REQUIREMENTS>` | Standards for empirical proof vs unsubstantiated claims. | Required command outputs and exit codes. |
| `<OUTPUT_CONTRACT>` | Expected completion artifacts and report format. | What to report upon task completion. |
| `<FAILURE_RECOVERY>` | Structured recovery and escalation ladder upon error. | Detect-diagnose-isolate-repair-learn cycle. |
| `<VERSION_POLICY>` | Version-sensitive dependency and documentation rules. | Installed version > local docs > official docs. |
| `<TRUTHFULNESS_POLICY>` | Anti-hallucination, factual grounding, and honesty rules. | Grounding claims in empirical evidence. |

### F. Conditional & Skill-Specific

| Tag | Responsibility | Example Content |
|---|---|---|
| `<WHEN_TO_USE>` | Trigger conditions activating a skill or policy. | Specific scenarios warranting use. |
| `<WHEN_NOT_TO_USE>` | Explicit exclusion conditions preventing misapplication. | Scenarios where the skill must not be used. |
| `<EXCEPTIONS>` | Legitimate, documented deviations from normal rules. | Explicit edge-case handling. |
| `<ANTI_PATTERNS>` | Known harmful approaches and anti-patterns to avoid. | Specific bad practices. |
| `<INPUT_CONTRACT>` | Required input artifacts, parameters, or state. | Prerequisite inputs for skills. |
| `<PROCEDURE>` | Detailed step-by-step procedural instructions for a skill. | Sequential action steps. |
| `<DELIVERABLES>` | Concrete work products produced by a skill. | Expected output files or state records. |
| `<MEMORY_SYNC>` | Skill-specific memory update requirements. | Exactly which memory docs to update. |
| `<FRAMEWORK_CONSTRAINTS>` | Framework-specific invariants where applicable. | Idiosyncratic framework rules. |

---

## 4. Allowed Tag Nesting

Tag nesting is permitted only when representing genuine semantic parent-child relationships:

### Action Space Hierarchy
```xml
<ACTION_SPACE_CONSTRAINTS>
  <READ>
    <ALLOWED>...</ALLOWED>
  </READ>
  <WRITE>
    <ALLOWED>...</ALLOWED>
    <CONDITIONAL>...</CONDITIONAL>
  </WRITE>
  <EXECUTE>
    <ALLOWED>...</ALLOWED>
    <CONDITIONAL>...</CONDITIONAL>
  </EXECUTE>
  <DELETE>
    <APPROVAL_REQUIRED>...</APPROVAL_REQUIRED>
  </DELETE>
  <NETWORK>
    <CONDITIONAL>...</CONDITIONAL>
  </NETWORK>
  <CREDENTIAL>
    <PROHIBITED>...</PROHIBITED>
  </CREDENTIAL>
  <PRODUCTION>
    <APPROVAL_REQUIRED>...</APPROVAL_REQUIRED>
  </PRODUCTION>
  <EXTERNAL_SIDE_EFFECT>
    <APPROVAL_REQUIRED>...</APPROVAL_REQUIRED>
  </EXTERNAL_SIDE_EFFECT>
</ACTION_SPACE_CONSTRAINTS>
```

### Tool Policy Hierarchy
```xml
<TOOL_POLICY>
  <GENERAL>...</GENERAL>
  <INSPECTION>...</INSPECTION>
  <DESTRUCTIVE_OPERATIONS>...</DESTRUCTIVE_OPERATIONS>
  <UNTRUSTED_CONTENT>...</UNTRUSTED_CONTENT>
  <SECRETS>...</SECRETS>
  <FAILURE>...</FAILURE>
</TOOL_POLICY>
```

Arbitrary or emotional nesting (e.g. `<IMPORTANT><CRITICAL><MUST>...</MUST></CRITICAL></IMPORTANT>`) is strictly prohibited.

---

## 5. File Applicability Matrix

| File Category | Recommended Tags | Forbidden Tags |
|---|---|---|
| **Global Control Plane** (`GEMINI.md`) | `<ROLE>`, `<MISSION>`, `<INSTRUCTION_HIERARCHY>`, `<PRIORITIES>`, `<NON_NEGOTIABLES>`, `<SAFETY_CONSTRAINTS>`, `<ACTION_SPACE_CONSTRAINTS>`, `<TOOL_POLICY>`, `<CONTEXT_POLICY>`, `<VERSION_POLICY>`, `<TRUTHFULNESS_POLICY>`, `<OUTPUT_CONTRACT>` | Skill-specific tags (`<PROCEDURE>`, `<DELIVERABLES>`) |
| **Workspace Bridge** (`AGENTS.md`) | `<MISSION>`, `<SOURCE_OF_TRUTH>`, `<INSTRUCTION_HIERARCHY>`, `<EXECUTION_POLICY>`, `<CONTEXT_POLICY>`, `<VERIFICATION_POLICY>`, `<MEMORY_POLICY>`, `<OUTPUT_CONTRACT>` | Volatile state or granular implementation details |
| **Core Rules** (`.agents/rules/*.md`) | `<ROLE>`, `<MISSION>`, `<NON_NEGOTIABLES>`, `<SAFETY_CONSTRAINTS>`, `<ACTION_SPACE_CONSTRAINTS>`, `<DECISION_RULES>`, `<EXCEPTIONS>`, `<ANTI_PATTERNS>`, `<VERIFICATION_POLICY>` | Runtime data or transient execution state |
| **Orchestration Policies** (`.agents/orchestration/*.md`) | `<MISSION>`, `<INSTRUCTION_HIERARCHY>`, `<CONTEXT_POLICY>`, `<ACTION_SPACE_CONSTRAINTS>`, `<TOOL_POLICY>`, `<EXECUTION_POLICY>`, `<DECISION_RULES>`, `<ESCALATION_POLICY>`, `<STATE_POLICY>`, `<VERIFICATION_POLICY>` | Ordinary code snippets or style preferences |
| **Skills** (`.agents/skills/*/SKILL.md`) | `<MISSION>`, `<WHEN_TO_USE>`, `<WHEN_NOT_TO_USE>`, `<PRECONDITIONS>`, `<INPUT_CONTRACT>`, `<SOURCE_OF_TRUTH>`, `<ACTION_SPACE_CONSTRAINTS>`, `<TOOL_POLICY>`, `<PROCEDURE>`, `<DECISION_RULES>`, `<FAILURE_RECOVERY>`, `<VERIFICATION_POLICY>`, `<EVIDENCE_REQUIREMENTS>`, `<DELIVERABLES>`, `<MEMORY_SYNC>` | YAML frontmatter wrapping |
| **State Files** (`*.json`, `*.jsonl`, `*.schema.json`) | **NONE** — Must remain pure JSON/JSONL | Any XML tag |
| **Project Memory & ADRs** (`docs/*.md`) | **NONE** — Must remain human-readable Markdown | Any XML tag |
