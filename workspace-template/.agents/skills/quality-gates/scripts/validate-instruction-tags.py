#!/usr/bin/env python3
"""
validate-instruction-tags.py

Validates literal instruction wrappers across the Antigravity Production Engineering System:
1. All XML tags belong to the approved canonical vocabulary.
2. Opening and closing tags are properly balanced and nested.
3. YAML frontmatter in SKILL.md is not wrapped in XML.
4. No XML tags exist in JSON, JSONL, or schema files.
5. Rules do not exceed 12,000 characters.
6. No instruction demands XML output as a pre-tool protocol.
"""

import os
import sys
import re
import json

APPROVED_TAGS = {
    # Core identity & priorities
    "ROLE",
    "MISSION",
    "INSTRUCTION_HIERARCHY",
    "PRIORITIES",
    
    # Constraints & safety
    "NON_NEGOTIABLES",
    "SAFETY_CONSTRAINTS",
    "ACTION_SPACE_CONSTRAINTS",
    "PROHIBITED_ACTIONS",
    
    # Action classes & sub-permissions
    "READ",
    "WRITE",
    "EXECUTE",
    "DELETE",
    "NETWORK",
    "CREDENTIAL",
    "PRODUCTION",
    "EXTERNAL_SIDE_EFFECT",
    "ALLOWED",
    "CONDITIONAL",
    "APPROVAL_REQUIRED",
    "PROHIBITED",
    
    # Tools & execution
    "TOOL_POLICY",
    "GENERAL",
    "INSPECTION",
    "DESTRUCTIVE_OPERATIONS",
    "UNTRUSTED_CONTENT",
    "SECRETS",
    "FAILURE",
    "EXECUTION_POLICY",
    "PRECONDITIONS",
    "DECISION_RULES",
    "ESCALATION_POLICY",
    
    # Context & memory
    "CONTEXT_POLICY",
    "SOURCE_OF_TRUTH",
    "MEMORY_POLICY",
    "STATE_POLICY",
    "READ_POLICY",
    "WRITE_POLICY",
    
    # Verification & output
    "VERIFICATION_POLICY",
    "EVIDENCE_REQUIREMENTS",
    "OUTPUT_CONTRACT",
    "FAILURE_RECOVERY",
    "VERSION_POLICY",
    "TRUTHFULNESS_POLICY",
    
    # Conditional & skill-specific
    "WHEN_TO_USE",
    "WHEN_NOT_TO_USE",
    "EXCEPTIONS",
    "ANTI_PATTERNS",
    "INPUT_CONTRACT",
    "PROCEDURE",
    "DELIVERABLES",
    "MEMORY_SYNC",
    "FRAMEWORK_CONSTRAINTS",
    
    # Container wrappers
    "AGENT_OPERATING_CONTRACT",
    "EXECUTION_CONTRACT",
}

# Regex to find tags: <TAG> or </TAG> or <TAG attr="val">
TAG_PATTERN = re.compile(r'<\s*(/?)\s*([A-Za-z0-9_-]+)(?:\s+[^>]*)?>')

def check_json_file(file_path):
    errors = []
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Check if raw XML tags appear in JSON keys or values (detect ANY XML tag)
    matches = TAG_PATTERN.findall(content)
    for slash, tag in matches:
        errors.append(f"Forbidden XML markup <{slash}{tag}> found in machine-readable file: {file_path}")
    return errors

def check_markdown_file(file_path, is_skill=False, is_rule=False, is_agent=False):
    errors = []
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Rule character limit
    if is_rule:
        char_count = len(content)
        if char_count >= 12000:
            errors.append(f"Rule exceeds 12,000 character limit: {file_path} ({char_count} chars)")

    # Skill frontmatter check
    if is_skill:
        if not content.startswith('---\n'):
            errors.append(f"Skill file does not start with YAML frontmatter: {file_path}")
        else:
            end_fm = content.find('\n---\n', 4)
            if end_fm == -1:
                errors.append(f"Unclosed YAML frontmatter in skill: {file_path}")
            else:
                frontmatter = content[:end_fm+5]
                if TAG_PATTERN.search(frontmatter):
                    errors.append(f"XML tags found inside YAML frontmatter in skill: {file_path}")

    # Custom Agent frontmatter check
    if is_agent:
        if not content.startswith('---\n'):
            errors.append(f"Agent file does not start with YAML frontmatter: {file_path}")
        else:
            end_fm = content.find('\n---\n', 4)
            if end_fm == -1:
                errors.append(f"Unclosed YAML frontmatter in agent: {file_path}")
            else:
                frontmatter = content[:end_fm+5]
                if TAG_PATTERN.search(frontmatter):
                    errors.append(f"XML tags found inside YAML frontmatter in agent: {file_path}")
                if 'name:' not in frontmatter:
                    errors.append(f"Agent frontmatter missing 'name:' field: {file_path}")
                if 'description:' not in frontmatter:
                    errors.append(f"Agent frontmatter missing 'description:' field: {file_path}")
                if 'tools:' not in frontmatter:
                    errors.append(f"Agent frontmatter missing 'tools:' field: {file_path}")

    # Check for forbidden pre-tool output instructions
    if re.search(r'before\s+(?:every|each)\s+tool\s+call\s*:\s*<', content, re.IGNORECASE) or \
       re.search(r'emit\s+<[A-Z_]+>\s+before\s+tool', content, re.IGNORECASE):
        errors.append(f"File requires XML output as a pre-tool protocol: {file_path}")

    # Parse and validate tags in the markdown body
    # Strip HTML comments (e.g. <!-- ... -->) before checking tags
    content_no_comments = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)

    # Ignore code blocks (both ``` and `)
    lines = content_no_comments.splitlines()
    in_code_block = False
    clean_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            continue
        if not in_code_block:
            # remove inline code spans
            no_inline_code = re.sub(r'`[^`]+`', '', line)
            clean_lines.append(no_inline_code)

    body_to_check = '\n'.join(clean_lines)
    matches = list(TAG_PATTERN.finditer(body_to_check))
    
    tag_stack = []
    for m in matches:
        is_closing = (m.group(1) == '/')
        tag_name = m.group(2)

        # Ignore standard HTML tags like <br>, <img>, <div>, <details>, etc.
        if tag_name.lower() in {"br", "hr", "img", "div", "span", "p", "a", "details", "summary", "ul", "ol", "li", "table", "tr", "td", "th", "tbody", "thead"}:
            continue

        # Tag must be uppercase and in APPROVED_TAGS
        if tag_name not in APPROVED_TAGS:
            errors.append(f"Unapproved or invalid tag <{tag_name}> in {file_path}")
            continue

        if not is_closing:
            # Opening tag
            tag_stack.append((tag_name, m.start()))
        else:
            # Closing tag
            if not tag_stack:
                errors.append(f"Unmatched closing tag </{tag_name}> in {file_path}")
            else:
                last_tag, _ = tag_stack.pop()
                if last_tag != tag_name:
                    errors.append(f"Mismatched tags: expected </{last_tag}>, found </{tag_name}> in {file_path}")

    if tag_stack:
        for unclosed, _ in tag_stack:
            errors.append(f"Unclosed tag <{unclosed}> in {file_path}")

    return errors

def main():
    root_dir = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    all_errors = []
    files_checked = 0

    for dirpath, dirnames, filenames in os.walk(root_dir):
        if '.git' in dirpath:
            continue
        for f in filenames:
            full_path = os.path.join(dirpath, f)
            rel_path = os.path.relpath(full_path, root_dir)

            if f.endswith('.json') or f.endswith('.jsonl') or f.endswith('.schema.json'):
                files_checked += 1
                all_errors.extend(check_json_file(full_path))
            elif f.endswith('.md'):
                files_checked += 1
                is_skill = (f == 'SKILL.md' and '/skills/' in full_path)
                is_rule = ('/.agents/rules/' in full_path)
                is_agent = ('/.agents/agents/' in full_path)
                all_errors.extend(check_markdown_file(full_path, is_skill=is_skill, is_rule=is_rule, is_agent=is_agent))

    print(f"Instruction Tag Validator: checked {files_checked} files.")
    if all_errors:
        print(f"FAILED with {len(all_errors)} errors:")
        for err in all_errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print("SUCCESS: All instruction tags are approved, balanced, properly nested, and cleanly separated!")
        sys.exit(0)

if __name__ == '__main__':
    main()
