#!/usr/bin/env python3
"""
validate-agents.py

Automated validator for Antigravity custom agent metadata in .agents/agents/*.md (P1-20, P1-21, P1-22):
- Validates YAML frontmatter across all agent definitions using PyYAML.
- Dynamically loads known tools from antigravity-tool-registry.json.
- Validates skill bindings against available skills in .agents/skills/.
- Required fields: name, description, tools, mainAgent, subagent.
- Enforces:
  1. Unique agent names across all definitions.
  2. Tools must belong to the versioned Antigravity tool registry.
  3. Exactly one main agent / coordinator (mainAgent: true).
  4. Least privilege / read-only constraints:
     - researcher, code-reviewer, and security-reviewer cannot have file write tools.
     - researcher cannot have command execution tools (run_command).
  5. Frontmatter syntax and boolean types.
- Returns exit code 0 on PASS, 1 on FAIL.
"""

import json
import os
from pathlib import Path
import re
import sys
from typing import Any, Dict, List, Optional, Set, Tuple

import yaml

# Core paths resolver
_script_dir = Path(__file__).resolve().parent
_core_dir = _script_dir.parent.parent.parent / "validation" / "core"
if _core_dir.is_dir() and str(_core_dir) not in sys.path:
    sys.path.insert(0, str(_core_dir))

try:
    from workspace_resolver import resolve_workspace
except ImportError:
    try:
        from .workspace_resolver import resolve_workspace
    except ImportError:
        resolve_workspace = None

FALLBACK_TOOLS: Set[str] = {
    "run_command", "write_to_file", "replace_file_content", "multi_replace_file_content",
    "view_file", "list_dir", "grep_search", "find_by_name", "read_url_content",
    "search_web", "ask_question", "schedule", "manage_task", "call_mcp_tool",
    "list_resources", "read_resource", "generate_image", "invoke_subagent",
    "define_subagent", "manage_subagents", "send_message",
}

READ_ONLY_AGENTS: Set[str] = {
    "researcher",
    "code-reviewer",
    "security-reviewer",
}

FILE_MUTATION_TOOLS: Set[str] = {
    "write_to_file",
    "replace_file_content",
    "multi_replace_file_content",
}


def load_tool_registry(agents_dir: Path) -> Set[str]:
    """Load tools dynamically from antigravity-tool-registry.json (P1-21)."""
    candidates = [
        agents_dir.parent / "orchestration" / "antigravity-tool-registry.json",
        agents_dir.parent / "antigravity-tool-registry.json",
        Path(".agents/orchestration/antigravity-tool-registry.json"),
        Path("workspace-template/.agents/orchestration/antigravity-tool-registry.json"),
    ]
    for cand in candidates:
        if cand.is_file():
            try:
                with open(cand, "r", encoding="utf-8") as f:
                    reg = json.load(f)
                    tools = set(reg.get("tools", {}).keys())
                    if tools:
                        return tools
            except Exception:
                pass
    raise RuntimeError("Antigravity tool registry not found; refusing to validate agents against an implicit tool allowlist.")


def parse_frontmatter(file_content: str, filepath: str) -> Tuple[Dict[str, Any], List[str]]:
    """Parse YAML frontmatter using real YAML parser (P1-20)."""
    errors: List[str] = []
    if not file_content.startswith("---"):
        return {}, [f"{filepath}: Missing starting '---' YAML frontmatter delimiter."]

    parts = file_content.split("---", 2)
    if len(parts) < 3:
        return {}, [f"{filepath}: Unclosed '---' YAML frontmatter delimiter."]

    yaml_block = parts[1]
    try:
        data = yaml.safe_load(yaml_block)
        if not isinstance(data, dict):
            return {}, [f"{filepath}: Frontmatter did not parse into a dictionary."]
        return data, []
    except yaml.YAMLError as ye:
        return {}, [f"{filepath}: YAML frontmatter parse error: {ye}"]


def validate_agents(agents_dir: str) -> Tuple[List[str], int]:
    errors: List[str] = []
    agents_path = Path(agents_dir).resolve()
    if not agents_path.is_dir():
        return [f"Agents directory '{agents_dir}' not found."], 0

    agent_files = sorted([f for f in agents_path.iterdir() if f.name.endswith(".md")])
    if not agent_files:
        return [f"No agent definitions found in '{agents_dir}'."], 0

    known_tools = load_tool_registry(agents_path)
    skills_dir = agents_path.parent / "skills"
    known_skills = set()
    if skills_dir.is_dir():
        known_skills = {d.name for d in skills_dir.iterdir() if d.is_dir()}

    seen_names: Set[str] = set()
    coordinator_count = 0

    for fpath in agent_files:
        fname = fpath.name
        try:
            content = fpath.read_text(encoding="utf-8")
        except Exception as e:
            errors.append(f"Failed to read agent file '{fname}': {e}")
            continue

        meta, parse_errs = parse_frontmatter(content, fname)
        if parse_errs:
            errors.extend(parse_errs)
            continue

        # Required fields check
        for req in ["name", "description", "tools", "mainAgent", "subagent"]:
            if req not in meta:
                errors.append(f"{fname}: Missing required frontmatter field '{req}'.")

        name = meta.get("name")
        if name:
            if not isinstance(name, str) or not re.match(r"^[a-z0-9-]+$", name):
                errors.append(f"{fname}: Invalid agent name '{name}' (must be lowercase alphanumeric + hyphens).")
            elif name in seen_names:
                errors.append(f"{fname}: Duplicate agent name '{name}' already defined.")
            seen_names.add(name)

        desc = meta.get("description")
        if desc and (not isinstance(desc, str) or len(desc.strip()) < 10):
            errors.append(f"{fname}: Description must be a descriptive string (>= 10 chars).")

        tools = meta.get("tools")
        if not isinstance(tools, list):
            errors.append(f"{fname}: 'tools' must be a list of tool names.")
        else:
            for t in tools:
                if t not in known_tools:
                    errors.append(f"{fname}: Unknown tool '{t}' not in Antigravity tool registry.")

            # Least privilege validation
            if name in READ_ONLY_AGENTS:
                for mt in FILE_MUTATION_TOOLS:
                    if mt in tools:
                        errors.append(f"{fname}: Read-only agent '{name}' is forbidden from having file mutation tool '{mt}'.")

            if name == "researcher":
                if "run_command" in tools:
                    errors.append(f"{fname}: Read-only researcher agent is forbidden from having 'run_command'.")

        # Validate skill bindings if present (P1-22)
        agent_skills = meta.get("skills")
        if agent_skills is not None:
            if not isinstance(agent_skills, list):
                errors.append(f"{fname}: 'skills' must be a list of skill identifiers.")
            elif known_skills:
                for sk in agent_skills:
                    if sk not in known_skills:
                        errors.append(f"{fname}: Bound skill '{sk}' does not exist in .agents/skills/.")

        main_agent = meta.get("mainAgent")
        if not isinstance(main_agent, bool):
            errors.append(f"{fname}: 'mainAgent' must be a boolean.")
        elif main_agent is True:
            coordinator_count += 1
            if name != "coordinator":
                errors.append(f"{fname}: Only 'coordinator' should have 'mainAgent: true' (got '{name}').")

        sub_agent = meta.get("subagent")
        if not isinstance(sub_agent, bool):
            errors.append(f"{fname}: 'subagent' must be a boolean.")

    # Exactly one coordinator required
    if coordinator_count != 1:
        errors.append(f"Expected exactly 1 mainAgent (coordinator), found {coordinator_count}.")

    return errors, len(agent_files)


def main():
    agents_dir = None
    if len(sys.argv) > 1:
        agents_dir = sys.argv[1]
    else:
        # Resolve the governed workspace even when this validator is launched
        # from the package root, CI checkout root, or the workspace itself.
        # This prevents path-dependent validation where the same validator
        # passes only because the caller happened to `cd` into workspace-template.
        resolved = resolve_workspace() if resolve_workspace is not None else None
        candidates = []
        if resolved is not None:
            candidates.append(resolved.project_root / ".agents" / "agents")
        candidates.extend([
            Path.cwd() / ".agents" / "agents",
            Path.cwd() / "workspace-template" / ".agents" / "agents",
            _script_dir.parent.parent.parent.parent / ".agents" / "agents",
        ])
        for c in candidates:
            c = Path(c).resolve()
            if c.is_dir():
                agents_dir = str(c)
                break

    if not agents_dir:
        print("Error: Could not locate .agents/agents directory.", file=sys.stderr)
        sys.exit(1)

    errors, count = validate_agents(agents_dir)
    print(f"Agent Metadata Validator: Checked {count} agent definition(s) in {agents_dir}")

    if errors:
        print(f"FAILED with {len(errors)} error(s):", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)
    else:
        print(f"SUCCESS: All {count} agents strictly adhere to metadata, role, and least-privilege constraints.")
        sys.exit(0)


if __name__ == "__main__":
    main()
