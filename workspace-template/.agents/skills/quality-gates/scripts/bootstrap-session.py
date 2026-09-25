#!/usr/bin/env python3
"""Bootstrap one Antigravity conversation before the model invocation.

The hook turns the system's lifecycle from a prose convention into a runtime
checkpoint: discover workspace -> read bootstrap context -> classify intent ->
create/attach execution state -> publish a deterministic context plan.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


SCRIPT_DIR = Path(__file__).resolve().parent
CONTROL_ROOT = SCRIPT_DIR.parents[2]
STATE_ROOT = CONTROL_ROOT / "state"
RUNTIME_DIR = STATE_ROOT / "runtime"
SESSIONS_DIR = RUNTIME_DIR / "sessions"
CONTEXT_PLANS_DIR = RUNTIME_DIR / "context-plans"
SESSION_FILE = RUNTIME_DIR / "session.json"  # last-active convenience view; lifecycle logic uses per-conversation sessions
CONTEXT_PLAN_FILE = RUNTIME_DIR / "context-plan.md"  # last-active convenience view
TASKS_DIR = STATE_ROOT / "tasks"

# Capability policy for PreInvocation injection.
#
# The public hook contract documents `toolCall` injection, but some live
# runtimes have rejected the same shape with `unknown injected step type: <nil>`.
# Therefore `auto` MUST fail closed to deferred messages unless the host sends
# an explicit capability signal or the operator has explicitly verified native
# injection. Never infer support from model name or product version alone.
PREINVOCATION_MODE_ENV = "ANTIGRAVITY_PREINVOCATION_MODE"
PREINVOCATION_CAPABILITIES_ENV = "ANTIGRAVITY_CAPABILITIES_FILE"
PREINVOCATION_TOOLCALL_OPTIN_ENV = "ANTIGRAVITY_ENABLE_PREINVOCATION_TOOLCALLS"
SUPPORTED_INJECTION_STEPS = {"toolCall", "userMessage", "ephemeralMessage"}

INQUIRY_PATTERNS = [
    r"\bwhat is\b", r"\bwhat are\b", r"\bwhy\b", r"\bhow does\b",
    r"\bhow do i\b", r"\bhow can i\b", r"\bexplain\b", r"\bmeaning\b",
    r"\bcompare\b", r"\bresearch\b", r"\banaly[sz]e\b", r"\binspect\b",
    r"\breview\b", r"\bcheck\b", r"\bfind out\b", r"\btell me\b",
    r"\bshow me\b", r"\bunderstand\b", r"\bwhy is\b",
]
MUTATION_PATTERNS = [
    r"\bfix\b", r"\bchange\b", r"\bmodify\b", r"\bupdate\b", r"\bedit\b",
    r"\badd\b", r"\bremove\b", r"\bdelete\b", r"\bcreate\b", r"\bbuild\b",
    r"\bimplement\b", r"\brefactor\b", r"\bimprove\b", r"\boptimi[sz]e\b",
    r"\bmigrate\b", r"\bupgrade\b", r"\breplace\b", r"\brename\b",
    r"\bmake\s+(?:this|it|the|project|website|site|app|code|page|file)\b.*(?:better|work|change|update|more|less|faster)",
    r"\bwrite\b", r"\bdeploy\b", r"\bconfigure\b",
]

CORE_READS = [
    "AGENTS.md",
    ".agents/orchestration/policy-registry.yaml",
    ".agents/orchestration/agent-operating-contract.md",
    ".agents/orchestration/task-lifecycle.md",
    ".agents/orchestration/task-classifier.md",
    ".agents/orchestration/lane-policy.yaml",
    ".agents/orchestration/context-router.md",
    ".agents/orchestration/verification-policy.yaml",
    ".agents/orchestration/verification-schema.json",
    ".agents/rules/rule-activation.yaml",
    "docs/INDEX.md",
    "docs/PROJECT_CONTEXT.md",
    "docs/CURRENT_STATE.md",
    "docs/ARCHITECTURE.md",
    ".agents/state/stack.json",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def safe_conversation_id(conversation_id: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]", "_", conversation_id or "unknown")
    return cleaned[:180] or "unknown"


def session_path(conversation_id: str) -> Path:
    return SESSIONS_DIR / f"{safe_conversation_id(conversation_id)}.json"


def context_plan_path(conversation_id: str) -> Path:
    return CONTEXT_PLANS_DIR / f"{safe_conversation_id(conversation_id)}.md"


def write_json(path: Path, value: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def _normalize_capability_types(value: Any) -> Optional[set[str]]:
    """Normalize host-advertised injected-step capability names."""
    if isinstance(value, (list, tuple, set)):
        return {str(item) for item in value if isinstance(item, (str, int, float))}
    return None


def _extract_toolcall_capability(payload: Dict[str, Any]) -> Optional[bool]:
    """Read only explicit host capability metadata; return None when unknown.

    Future Antigravity runtimes may expose capability metadata on hook stdin.
    This adapter accepts a few stable, namespaced shapes without guessing from
    unrelated fields such as modelName. Positive support must be explicit.
    """
    direct = _normalize_capability_types(payload.get("supportedInjectedStepTypes"))
    if direct is not None:
        if "toolCall" in direct:
            return True
        if direct and direct.isdisjoint({"toolCall"}):
            return False

    caps = payload.get("capabilities")
    if isinstance(caps, dict):
        pre = caps.get("preInvocation") or caps.get("PreInvocation")
        if isinstance(pre, dict):
            value = pre.get("toolCallInjection")
            if value is None:
                value = pre.get("toolCall")
            if isinstance(value, bool):
                return value
            types = _normalize_capability_types(pre.get("supportedInjectedStepTypes"))
            if types is not None:
                if "toolCall" in types:
                    return True
                if types and types.isdisjoint({"toolCall"}):
                    return False

    return None


def _read_capability_file(workspace: Path) -> Optional[bool]:
    """Read an operator-verified runtime capability file, if present."""
    raw_path = os.getenv(PREINVOCATION_CAPABILITIES_ENV, "").strip()
    path = Path(raw_path).expanduser() if raw_path else (
        workspace / ".agents" / "state" / "runtime" / "host-capabilities.json"
    )
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None

    pre = data.get("preInvocation") if isinstance(data, dict) else None
    if not isinstance(pre, dict):
        return None
    value = pre.get("toolCallInjection")
    if isinstance(value, bool):
        return value
    status = str(pre.get("toolCallSupport", "")).strip().lower()
    if status in {"verified", "supported", "enabled"}:
        return True
    if status in {"unsupported", "disabled", "blocked"}:
        return False
    return None


def resolve_preinvocation_injection_mode(payload: Dict[str, Any], workspace: Path) -> Dict[str, str]:
    """Resolve native vs deferred injection with fail-closed capability gating.

    Precedence:
    1. explicit mode env (`native`/`deferred`)
    2. explicit host capability metadata in hook stdin
    3. verified operator capability file
    4. legacy explicit opt-in env (`...ENABLE_PREINVOCATION_TOOLCALLS=1`)
    5. safe default: deferred
    """
    requested = os.getenv(PREINVOCATION_MODE_ENV, "auto").strip().lower()
    if requested in {"deferred", "safe", "off", "disabled"}:
        return {"mode": "deferred-read", "reason": "explicit-mode", "support": "disabled"}
    if requested in {"native", "toolcall", "enabled"}:
        return {"mode": "native-toolCall", "reason": "explicit-mode", "support": "verified-by-operator"}
    if requested not in {"", "auto"}:
        return {"mode": "deferred-read", "reason": "invalid-mode-fails-closed", "support": "unknown"}

    host_signal = _extract_toolcall_capability(payload)
    if host_signal is True:
        return {"mode": "native-toolCall", "reason": "host-capability-signal", "support": "advertised"}
    if host_signal is False:
        return {"mode": "deferred-read", "reason": "host-capability-signal", "support": "unsupported"}

    file_signal = _read_capability_file(workspace)
    if file_signal is True:
        return {"mode": "native-toolCall", "reason": "verified-capability-file", "support": "verified"}
    if file_signal is False:
        return {"mode": "deferred-read", "reason": "verified-capability-file", "support": "unsupported"}

    legacy_optin = os.getenv(PREINVOCATION_TOOLCALL_OPTIN_ENV, "0").strip().lower()
    if legacy_optin in {"1", "true", "yes", "on"}:
        return {"mode": "native-toolCall", "reason": "legacy-explicit-opt-in", "support": "verified-by-operator"}

    return {"mode": "deferred-read", "reason": "unknown-fails-closed", "support": "unknown"}


def workspace_from_payload(payload: Dict[str, Any]) -> Path:
    candidates = payload.get("workspacePaths", [])
    if isinstance(candidates, str):
        candidates = [candidates]
    for raw in candidates:
        try:
            p = Path(raw).resolve()
        except Exception:
            continue
        for candidate in [p, *p.parents]:
            if (candidate / ".agents").is_dir() and (candidate / "AGENTS.md").is_file():
                return candidate
    if (CONTROL_ROOT.parent / "AGENTS.md").is_file():
        return CONTROL_ROOT.parent
    return Path.cwd().resolve()


def read_latest_user_prompt(transcript_path: Optional[str]) -> Tuple[str, int]:
    if not transcript_path:
        return "", 0
    path = Path(transcript_path)
    if not path.is_file():
        return "", 0

    latest = ""
    user_count = 0

    def consume(item: Any) -> None:
        nonlocal latest, user_count
        if not isinstance(item, dict):
            return
        role = item.get("role") or item.get("message", {}).get("role")
        if role != "user":
            return
        content = item.get("content") or item.get("message", {}).get("content") or ""
        if isinstance(content, list):
            parts: List[str] = []
            for part in content:
                if isinstance(part, dict) and isinstance(part.get("text"), str):
                    parts.append(part["text"])
                elif isinstance(part, str):
                    parts.append(part)
            content = "\n".join(parts)
        if isinstance(content, str):
            user_count += 1
            latest = content.strip()

    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
        # Official hook metadata points to transcript.jsonl, but accepting a JSON
        # array/object here makes the adapter robust to exported/test transcripts.
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, list):
                for item in parsed:
                    consume(item)
                return latest, user_count
            if isinstance(parsed, dict):
                messages = parsed.get("messages") or parsed.get("entries") or parsed.get("transcript")
                if isinstance(messages, list):
                    for item in messages:
                        consume(item)
                    return latest, user_count
                consume(parsed)
                return latest, user_count
        except Exception:
            pass

        for line in raw.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                consume(json.loads(line))
            except Exception:
                continue
    except Exception:
        return "", 0
    return latest, user_count


def classify(prompt: str) -> str:
    normalized = prompt.lower()
    mutation = any(re.search(p, normalized) for p in MUTATION_PATTERNS)
    inquiry = any(re.search(p, normalized) for p in INQUIRY_PATTERNS)
    if mutation:
        return "governed"
    if inquiry:
        return "inquiry"
    # Unknown intent fails safe into an inquiry/read-only session. A mutation
    # still cannot pass the pre-tool gate without an active task in execution.
    return "inquiry"


def candidate_task_type(prompt: str) -> str:
    """Return a non-authoritative task-type hint used only for routing/bootstrap.

    The model remains authoritative for final classification. This deterministic
    hint exists so the pre-invocation hook can preload the most likely skill set
    before the first model turn.
    """
    p = prompt.lower()
    patterns = [
        (r"\b(?:bug|bugfix|fix|regression|error|exception|broken|not working)\b", "bug"),
        (r"\b(?:security|vulnerability|cve|auth|authorization|secret|credential)\b", "security"),
        (r"\b(?:migration|migrate|schema change|data migration)\b", "migration"),
        (r"\b(?:database|mongodb|postgres|mysql|sql|index|query)\b", "database"),
        (r"\b(?:architecture|architectural|system design|design decision|adr)\b", "architecture"),
        (r"\b(?:performance|slow|latency|optimi[sz]e|core web vitals|benchmark)\b", "performance"),
        (r"\b(?:deploy|deployment|release|ci/cd|infrastructure|terraform|docker)\b", "deployment"),
        (r"\b(?:test|testing|coverage|e2e|unit test|integration test)\b", "testing"),
        (r"\b(?:requirement|requirements|prd|acceptance criteria|user story)\b", "requirements"),
        (r"\b(?:document|documentation|docs|memory|current state|adr index)\b", "documentation"),
        (r"\b(?:refactor|restructure|cleanup|reorganize)\b", "refactor"),
        (r"\b(?:implement|build|create|add|feature|new page|new endpoint|new component)\b", "feature"),
    ]
    for pattern, task_type in patterns:
        if re.search(pattern, p):
            return task_type
    return "investigation"


def candidate_risk_level(prompt: str, task_type: str) -> str:
    """Return a conservative routing hint; final risk remains policy-resolved."""
    p = prompt.lower()
    if task_type in {"security", "migration", "deployment", "database", "architecture"}:
        return "high"
    if re.search(r"\b(?:production|prod|live|customer data|payment|credential|secret|breaking change|force push|delete|drop|destroy)\b", p):
        return "high"
    if task_type in {"bug", "complex-feature", "performance", "refactor"}:
        return "medium"
    return "low"


def candidate_technology_profiles(workspace: Path) -> List[str]:
    """Resolve active technology profiles from detected stack state when available."""
    stack_path = workspace / ".agents" / "state" / "stack.json"
    if not stack_path.is_file():
        return []
    try:
        stack = json.loads(stack_path.read_text(encoding="utf-8"))
    except Exception:
        return []

    candidates: List[str] = []
    active = stack.get("activeProfiles") or []
    if isinstance(active, list):
        candidates.extend(str(x) for x in active if isinstance(x, str))
    for key in ("languages",):
        values = stack.get(key) or []
        if isinstance(values, list):
            candidates.extend(str(x) for x in values if isinstance(x, str))
    for key in ("frontend", "backend", "database"):
        value = stack.get(key)
        if isinstance(value, str) and value:
            candidates.append(value)
    deployment = stack.get("deployment") or {}
    if isinstance(deployment, dict) and deployment.get("target"):
        candidates.append(str(deployment["target"]))

    profile_root = workspace / ".agents" / "technology" / "profiles"
    resolved: List[str] = []
    for candidate in candidates:
        normalized = candidate.replace(":", "/").strip().lower()
        direct = profile_root / f"{normalized}.md"
        if direct.is_file():
            resolved.append(str(direct.relative_to(workspace)))
            continue
        for path in profile_root.rglob("*.md"):
            if path.name.lower() == f"{normalized}.md" or path.stem.lower() == normalized:
                resolved.append(str(path.relative_to(workspace)))
                break
    return list(dict.fromkeys(resolved))[:8]


def next_task_id() -> str:
    # Timestamp-based IDs avoid collisions when two conversations bootstrap the
    # same workspace concurrently. The schema permits any 3+ digit TASK number.
    candidate = int(datetime.now(timezone.utc).timestamp() * 1000)
    TASKS_DIR.mkdir(parents=True, exist_ok=True)
    while (TASKS_DIR / f"TASK-{candidate}.json").exists():
        candidate += 1
    return f"TASK-{candidate}"


def ensure_provisional_task(prompt: str, conversation_id: str, workspace: Path, task_type: str, risk_level: str) -> str:
    """Create/reuse a provisional task and matching governance record before mutation is allowed."""
    current_session = session_path(conversation_id)
    if current_session.is_file():
        try:
            current = json.loads(current_session.read_text(encoding="utf-8"))
            existing = current.get("activeTaskId")
            if existing:
                task_path = TASKS_DIR / f"{existing}.json"
                if task_path.is_file():
                    record = json.loads(task_path.read_text(encoding="utf-8"))
                    active_states = {
                        "DRAFT", "CLASSIFIED", "CONTEXT_READY", "PLANNED", "READY",
                        "IN_PROGRESS", "TESTING", "VERIFYING", "REVIEWING",
                        "MEMORY_SYNC", "STATE_SYNC", "GOVERNANCE_CHECK"
                    }
                    if record.get("status") in active_states:
                        ensure_provisional_governance(workspace, existing, task_type, risk_level)
                        return existing
        except Exception:
            pass

    task_id = next_task_id()
    acceptance = (prompt.strip().replace("\n", " ")[:300] or "Complete the requested engineering work and verify the result.")
    record = {
        "id": task_id,
        "type": task_type,
        "status": "DRAFT",
        "priority": "P2",
        "riskLevel": risk_level,
        "title": "Provisional task for current user request",
        "description": acceptance,
        "acceptanceCriteria": [acceptance],
        "scope": {"include": [], "exclude": ["unrelated changes"]},
        "dependencies": [],
        "createdAt": utc_now(),
        "updatedAt": utc_now(),
        "bootstrapProvisional": True,
        "conversationId": conversation_id or None,
        "candidateClassification": {"type": task_type, "risk": risk_level},
        "notes": "Created by PreInvocation bootstrap. The model must inspect/classify/load and either finalize or cancel this provisional task before completion.",
    }
    task_path = TASKS_DIR / f"{task_id}.json"
    task_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    ensure_provisional_governance(workspace, task_id, task_type, risk_level)
    return task_id


def ensure_provisional_governance(workspace: Path, task_id: str, task_type: str, risk_level: str) -> None:
    """Materialize the governance shell immediately so every active task has canonical governance state."""
    gov_dir = workspace / ".agents" / "state" / "governance"
    gov_dir.mkdir(parents=True, exist_ok=True)
    path = gov_dir / f"{task_id}.json"
    if path.exists():
        return
    record = {
        "taskId": task_id,
        "classification": {"type": task_type, "risk": risk_level},
        "requiredRules": [],
        "requiredSkills": [],
        "requiredTechnologyProfiles": [],
        "relevantAdrs": [],
        "qualityGates": [],
        "securityChecks": [],
        "memorySyncRequired": False,
        "memorySyncCompleted": False,
        "approvalRequirements": {"required": False, "satisfied": False, "approver": None, "approvalSource": None, "approvalId": None, "approvedAt": None, "approvalEvidence": None, "notes": "Provisional governance shell; final requirements are resolved during classification."},
        "evidenceRequirements": [],
        "governanceStatus": "pending",
        "completedAt": None,
        "notes": "Created automatically during PreInvocation bootstrap. Final rule/skill/profile/gate resolution is authoritative after repository inspection.",
    }
    path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")


def candidate_rules(prompt: str) -> List[str]:
    p = prompt.lower()
    rules = [".agents/rules/00-core.md", ".agents/rules/10-verification.md", ".agents/rules/11-project-memory.md", ".agents/rules/13-agent-safety.md"]
    if re.search(r"frontend|react|next\.js|ui|ux|css|component|tailwind|browser", p):
        rules += [".agents/rules/04-coding.md", ".agents/rules/05-naming.md", ".agents/rules/06-uiux.md", ".agents/rules/02-tech-stack.md", ".agents/rules/15-layered-architecture.md"]
    if re.search(r"api|backend|server|node|express|database|mongo|postgres|sql", p):
        rules += [".agents/rules/02-tech-stack.md", ".agents/rules/03-architecture.md", ".agents/rules/07-security.md", ".agents/rules/15-layered-architecture.md"]
    if re.search(r"security|auth|jwt|oauth|credential|secret|permission|vulnerabil", p):
        rules += [".agents/rules/07-security.md", ".agents/rules/13-agent-safety.md"]
    if re.search(r"test|bug|regression|failure|error|debug", p):
        rules += [".agents/rules/09-testing.md", ".agents/rules/14-observability.md"]
    if re.search(r"requirement|acceptance|prd|user stor", p):
        rules += [".agents/rules/12-requirements.md"]
    if re.search(r"git|commit|branch|merge|rebase|pull request|pr ", p):
        rules += [".agents/rules/08-git.md"]
    if re.search(r"architecture|design|module|boundary|dependency|adr", p):
        rules += [".agents/rules/03-architecture.md", ".agents/rules/15-layered-architecture.md"]
    if re.search(r"logging|telemetry|metrics|tracing|observability", p):
        rules += [".agents/rules/14-observability.md"]
    if re.search(r"document|memory|state|docs", p):
        rules += [".agents/rules/11-project-memory.md"]
    # preserve order, remove duplicates
    return list(dict.fromkeys(rules))


def candidate_skills(prompt: str) -> List[str]:
    p = prompt.lower()
    # These are the minimum lifecycle skills for every governed task.  The old
    # system was effective because planning, verification, and recovery were
    # treated as part of the execution contract rather than optional add-ons.
    # Keep them in the preload set so the 24-file bootstrap cap cannot evict
    # verification merely because a prompt also matches several domain skills.
    skills = [
        ".agents/skills/planning/SKILL.md",
        ".agents/skills/verification/SKILL.md",
        ".agents/skills/testing/SKILL.md",
        ".agents/skills/quality-gates/SKILL.md",
        ".agents/skills/governance-enforcement/SKILL.md",
    ]
    mappings = [
        (r"\bfix|bug|regression|debug", ".agents/skills/bug-fix/SKILL.md"),
        (r"\bfeature|implement|build|create", ".agents/skills/feature-development/SKILL.md"),
        (r"frontend|react|next\.js|ui|ux", ".agents/skills/frontend/SKILL.md"),
        (r"backend|node|express|server", ".agents/skills/backend/SKILL.md"),
        (r"api|endpoint", ".agents/skills/api/SKILL.md"),
        (r"database|mongodb|postgres|migration", ".agents/skills/database/SKILL.md"),
        (r"security|auth|vulnerabil", ".agents/skills/security/SKILL.md"),
        (r"test|verify|validation", ".agents/skills/testing/SKILL.md"),
        (r"architecture|design", ".agents/skills/architecture/SKILL.md"),
        (r"documentation|docs|memory", ".agents/skills/documentation/SKILL.md"),
        (r"deploy|release|infrastructure", ".agents/skills/deployment/SKILL.md"),
        (r"requirement|prd|acceptance", ".agents/skills/requirements-discovery/SKILL.md"),
        (r"feature|implement|build|create|architecture|database|migration", ".agents/skills/planning/SKILL.md"),
        (r"review|audit|inspect|code quality", ".agents/skills/code-review/SKILL.md"),
        (r"verify|validation|completion|quality gate|test|bug|feature", ".agents/skills/verification/SKILL.md"),
        (r"debug|error|failure|regression|not working", ".agents/skills/debugging/SKILL.md"),
    ]
    for pattern, skill in mappings:
        if re.search(pattern, p):
            skills.append(skill)
    return list(dict.fromkeys(skills))


def write_context_plan(workspace: Path, prompt: str, mode: str, task_id: Optional[str], conversation_id: str, task_type: str, risk_level: str) -> Path:
    plan = [
        "# Runtime Context Plan",
        "",
        f"Generated: `{utc_now()}`",
        f"Mode: **{mode}**",
        f"Active task: **{task_id or 'none'}**",
        f"Candidate task type (non-authoritative): **{task_type}**",
        f"Candidate risk (non-authoritative): **{risk_level}**",
        "",
        "## Mandatory bootstrap reads",
    ]
    plan.extend(f"- `{p}`" for p in CORE_READS if (workspace / p).exists())
    plan += ["", "## Candidate rules for this request"]
    plan.extend(f"- `{p}`" for p in candidate_rules(prompt) if (workspace / p).exists())
    plan += ["", "## Candidate skills for this request"]
    plan.extend(f"- `{p}`" for p in candidate_skills(prompt) if (workspace / p).exists())
    plan += ["", "## Active technology profiles detected at bootstrap"]
    plan.extend(f"- `{p}`" for p in candidate_technology_profiles(workspace) if (workspace / p).exists())
    plan += [
        "",
        "## Runtime contract",
        "- Read the actual files above; do not claim a rule/skill/policy was loaded from this plan alone.",
        "- Before application mutation, the active task must be classified and moved out of `DRAFT` into the lifecycle state required by policy.",
        "- Required context must be resolved from the repository and authoritative project documents before editing.",
        "- After implementation, run the applicable verification gates and synchronize canonical task/memory state before completion.",
    ]
    plan_path = context_plan_path(conversation_id)
    plan_path.parent.mkdir(parents=True, exist_ok=True)
    content = "\n".join(plan) + "\n"
    plan_path.write_text(content, encoding="utf-8")
    CONTEXT_PLAN_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONTEXT_PLAN_FILE.write_text(content, encoding="utf-8")
    return plan_path


def main() -> int:
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except Exception:
        payload = {}

    workspace = workspace_from_payload(payload)
    conversation_id = str(payload.get("conversationId") or "unknown")
    prompt, user_message_count = read_latest_user_prompt(payload.get("transcriptPath"))
    prompt_hash = hashlib.sha256(prompt.encode("utf-8")).hexdigest() if prompt else None

    previous: Dict[str, Any] = {}
    conversation_session = session_path(conversation_id)
    if conversation_session.is_file():
        try:
            previous = json.loads(conversation_session.read_text(encoding="utf-8"))
        except Exception:
            previous = {}

    same_user_turn = (
        previous.get("conversationId") == conversation_id
        and previous.get("userMessageCount") == user_message_count
        and previous.get("promptHash") == prompt_hash
        and user_message_count > 0
    )

    if same_user_turn:
        previous["lastInvocationAt"] = utc_now()
        previous["invocationNum"] = payload.get("invocationNum")
        previous["invocationCount"] = int(previous.get("invocationCount", 1)) + 1
        write_json(conversation_session, previous)
        write_json(SESSION_FILE, previous)
        print(json.dumps({
            "injectSteps": [{
                "ephemeralMessage": f"Runtime bootstrap already completed for this user turn (invocation={payload.get('invocationNum', 'unknown')}); continue the existing lifecycle session without re-injecting duplicate context reads."
            }]
        }))
        return 0

    mode = classify(prompt)
    task_type = candidate_task_type(prompt)
    risk_level = candidate_risk_level(prompt, task_type)
    active_task = ensure_provisional_task(prompt, conversation_id, workspace, task_type, risk_level) if mode == "governed" else None
    plan_path = write_context_plan(workspace, prompt, mode, active_task, conversation_id, task_type, risk_level)

    injection_capability = resolve_preinvocation_injection_mode(payload, workspace)

    session = {
        "version": 1,
        "status": "bootstrapped",
        "mode": mode,
        "conversationId": conversation_id,
        "promptHash": prompt_hash,
        "promptPreview": prompt[:500] if prompt else None,
        "userMessageCount": user_message_count,
        "activeTaskId": active_task,
        "candidateTaskType": task_type,
        "candidateRisk": risk_level,
        "contextPlan": str(plan_path),
        "bootstrappedAt": utc_now(),
        "lastInvocationAt": utc_now(),
        "invocationNum": payload.get("invocationNum"),
        "invocationCount": 1,
        "preInvocationInjection": injection_capability,
    }
    write_json(conversation_session, session)
    write_json(SESSION_FILE, session)

    steps: List[Dict[str, Any]] = []
    injected_paths: List[str] = []

    # Priority order follows the context-budget policy: safety/core invariants →
    # task-specific rules and skills → active technology → project memory.  This
    # prevents a long list of generic docs from crowding out a skill/rule that is
    # directly relevant to the user request.
    task_rules = candidate_rules(prompt)
    task_skills = candidate_skills(prompt)
    technology_profiles = candidate_technology_profiles(workspace)

    # Promote the safety/verification rules that are directly implicated by the
    # prompt ahead of the general rule set. This preserves the fixed preload
    # budget while guaranteeing that a high-signal rule cannot be evicted by a
    # long list of lower-priority project-memory documents.
    critical_rules: List[str] = []
    normalized_prompt = prompt.lower()
    if re.search(r"\b(?:security|auth|jwt|oauth|credential|secret|permission|vulnerabil)", normalized_prompt):
        critical_rules.append(".agents/rules/07-security.md")
    if re.search(r"\b(?:test|testing|coverage|regression|failure|error|debug|bug)", normalized_prompt):
        critical_rules.extend([".agents/rules/09-testing.md", ".agents/rules/14-observability.md"])
    critical_rules = list(dict.fromkeys(critical_rules))
    remaining_rules = [rule for rule in task_rules if rule not in critical_rules]

    priority_core = [
        "AGENTS.md",
        str(plan_path.relative_to(workspace)),
        ".agents/state/stack.json",
        ".agents/orchestration/policy-registry.yaml",
        ".agents/orchestration/task-lifecycle.md",
        ".agents/orchestration/task-classifier.md",
        ".agents/orchestration/context-router.md",
        ".agents/rules/00-core.md",
        ".agents/rules/13-agent-safety.md",
        ".agents/rules/10-verification.md",
    ]
    priority_project = [
        "docs/INDEX.md", "docs/PROJECT_CONTEXT.md", "docs/CURRENT_STATE.md",
        "docs/CONVENTIONS.md", "docs/decisions/INDEX.md", "docs/requirements/INDEX.md",
    ]
    candidate_paths = [
        *priority_core,
        *critical_rules,
        *task_skills,
        *remaining_rules,
        *technology_profiles,
        *priority_project,
    ]
    if active_task:
        candidate_paths += [
            str((TASKS_DIR / f"{active_task}.json").relative_to(workspace)),
            str((workspace / ".agents" / "state" / "governance" / f"{active_task}.json").relative_to(workspace)),
        ]

    # Resolve a bounded, deterministic preload plan. Keep the plan in runtime state
    # regardless of host capabilities. Native tool-call injection is capability-gated
    # and fails closed to deferred messages when support is unknown.
    for path in list(dict.fromkeys(candidate_paths))[:24]:
        if (workspace / path).is_file():
            injected_paths.append(path)
            if injection_capability["mode"] == "native-toolCall":
                steps.append({
                    "toolCall": {
                        "name": "view_file",
                        "args": {"AbsolutePath": str(workspace / path)},
                    }
                })

    relative_context = "\n".join(f"- {path}" for path in injected_paths)
    injection_mode = injection_capability["mode"]
    guidance = (
        "Runtime bootstrap complete. Before mutation or final verification, inspect the context plan "
        "and listed files with normal read tools; do not assume they were automatically opened. "
        f"Bootstrap mode={injection_mode}; capability={injection_capability['support']}; "
        f"reason={injection_capability['reason']}; context plan={plan_path}; "
        f"activeTask={active_task or 'none'}.\n\n"
        f"Required bootstrap context ({len(injected_paths)} files):\n{relative_context}"
    )
    steps.append({"ephemeralMessage": guidance})
    print(json.dumps({"injectSteps": steps}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
