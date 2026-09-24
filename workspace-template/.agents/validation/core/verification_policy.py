"""Executable verification policy engine backed by verification-policy.yaml."""

from dataclasses import dataclass
from enum import Enum
import json
from pathlib import Path
import re
from typing import Any, Dict, List, Optional, Set, Tuple

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - environment error
    yaml = None


class GateKind(str, Enum):
    TEST = "test"
    LINT = "lint"
    TYPECHECK = "typecheck"
    BUILD = "build"
    SECURITY = "security"
    DIFF_REVIEW = "diff-review"
    MEMORY_SYNC = "memory-sync"
    ADR = "adr"


CANONICAL_TASK_TYPES: Set[str] = {
    "simple", "bug", "feature", "complex-feature", "refactor", "architecture",
    "security", "database", "migration", "performance", "testing", "deployment",
    "documentation", "requirements", "investigation", "infrastructure",
}
TASK_TYPE_ALIASES = {
    "bugfix": "bug", "test": "testing", "docs": "documentation", "infra": "infrastructure",
}
TRIVIAL_STRINGS = {
    "trust me", "done", "passed", "pass", "ok", "okay", "works", "working", "true", "yes",
    "verified", "tested", "good", "looks good", "dummy", "placeholder", "todo", "fixme",
    "n/a", "na", "none", "null", "test", "see output", "all good",
}


def _default_policy_path() -> Path:
    return Path(__file__).resolve().parents[2] / "orchestration" / "verification-policy.yaml"


def load_canonical_policy(path: Optional[Path] = None) -> Dict[str, Any]:
    policy_path = path or _default_policy_path()
    if yaml is None:
        raise RuntimeError("PyYAML is required to evaluate the canonical verification policy.")
    try:
        data = yaml.safe_load(policy_path.read_text(encoding="utf-8")) or {}
    except Exception as exc:
        raise RuntimeError(f"Unable to load canonical verification policy: {policy_path}: {exc}") from exc
    if not isinstance(data.get("policy"), dict):
        raise RuntimeError(f"Canonical verification policy is malformed: {policy_path}")
    return data["policy"]


def normalize_task_type(task_type: str) -> str:
    t = (task_type or "").strip().lower()
    return TASK_TYPE_ALIASES.get(t, t)


def is_canonical_task_type(task_type: str) -> bool:
    return task_type in CANONICAL_TASK_TYPES


def is_substantive_evidence(evidence: Any) -> bool:
    if isinstance(evidence, dict):
        ev = evidence
        if "evidenceRef" in ev and isinstance(ev["evidenceRef"], dict):
            return is_substantive_evidence(ev["evidenceRef"])
        ev_type = ev.get("type")
        if ev_type not in {"ci-artifact", "local-command", "artifact-review", "manual-checkpoint"}:
            return False
        if ev_type == "local-command":
            return bool(ev.get("command") and isinstance(ev.get("exitCode"), int) and ev.get("capturedAt"))
        if ev_type == "ci-artifact":
            return bool((ev.get("artifact") or ev.get("runId")) and ev.get("capturedAt"))
        if ev_type == "artifact-review":
            return bool(ev.get("artifact") and ev.get("capturedAt"))
        if ev_type == "manual-checkpoint":
            return bool(ev.get("summary") and ev.get("capturedAt"))
        return False
    if not isinstance(evidence, str) or len(evidence.strip()) < 6:
        return False
    trimmed = evidence.strip().lower()
    return trimmed not in TRIVIAL_STRINGS and not any(
        re.search(p, trimmed) for p in [r"\btrust me\b", r"\bworks for me\b", r"\bplaceholder\b", r"\bdummy\b"]
    )


@dataclass
class GateEvaluationResult:
    gate_name: str
    status: str
    passed: bool
    kind: GateKind
    error: Optional[str] = None


class VerificationPolicyEngine:
    def __init__(self, policy_yaml_data: Optional[Dict[str, Any]] = None, policy_path: Optional[Path] = None):
        self.policy_data = policy_yaml_data or load_canonical_policy(policy_path)
        self.gate_registry = self.policy_data.get("gateRegistry", {})
        self.risk_levels = self.policy_data.get("riskLevels", {})
        self.task_types = self.policy_data.get("taskTypes", {})

    def get_required_gates(self, task_type: str, risk_level: str) -> List[str]:
        canon_type = normalize_task_type(task_type)
        if not is_canonical_task_type(canon_type) or canon_type not in self.task_types:
            raise ValueError(f"Unsupported canonical task type: {task_type!r}")
        risk = (risk_level or "").strip().lower()
        if risk not in self.risk_levels:
            raise ValueError(f"Unsupported risk level: {risk_level!r}")
        required: Set[str] = set(self.risk_levels[risk].get("requiredGates", []))
        required.update(self.task_types[canon_type].get("mandatoryGates", []))
        return sorted(required)

    def evaluate_gates(self, task_type: str, risk_level: str, recorded_gates: List[Dict[str, Any]]) -> Tuple[bool, List[GateEvaluationResult], Optional[str]]:
        required_gates = self.get_required_gates(task_type, risk_level)
        recorded_map = {g.get("name"): g for g in recorded_gates if isinstance(g, dict) and g.get("name")}
        results: List[GateEvaluationResult] = []

        for req in required_gates:
            reg = self.gate_registry.get(req)
            if not isinstance(reg, dict):
                return False, results, f"Mandatory gate '{req}' is not present in the canonical gate registry."
            try:
                kind = GateKind(reg.get("kind"))
            except Exception:
                return False, results, f"Mandatory gate '{req}' has invalid kind '{reg.get('kind')}'."
            g_rec = recorded_map.get(req)
            if not g_rec:
                err = f"Mandatory verification gate '{req}' is missing from governance record."
                return False, results + [GateEvaluationResult(req, "missing", False, kind, err)], err
            status = g_rec.get("status", "unknown")
            if status == "not_configured":
                err = f"Mandatory verification gate '{req}' cannot pass with status 'not_configured'."
                return False, results + [GateEvaluationResult(req, status, False, kind, err)], err
            if status == "not_applicable":
                reason = str(g_rec.get("reason") or "").strip()
                ev = g_rec.get("evidenceRef") or g_rec.get("applicabilityEvidence") or g_rec.get("evidence")
                if not reason or not is_substantive_evidence(ev):
                    err = f"Gate '{req}' marked 'not_applicable' lacks substantive applicability evidence and justification."
                    return False, results + [GateEvaluationResult(req, status, False, kind, err)], err
                results.append(GateEvaluationResult(req, status, True, kind))
                continue
            if status != "passed":
                err = f"Mandatory verification gate '{req}' is non-passing (status='{status}')."
                return False, results + [GateEvaluationResult(req, status, False, kind, err)], err
            ev = g_rec.get("evidenceRef") or g_rec.get("evidence")
            if not is_substantive_evidence(ev):
                err = f"Gate '{req}' is marked 'passed' but has no valid runtime/independent evidence reference."
                return False, results + [GateEvaluationResult(req, status, False, kind, err)], err
            if isinstance(ev, dict) and ev.get("type") == "local-command" and ev.get("exitCode") != 0:
                err = f"Gate '{req}' is marked 'passed' with a non-zero command exit code."
                return False, results + [GateEvaluationResult(req, status, False, kind, err)], err
            results.append(GateEvaluationResult(req, status, True, kind))

        return True, results, None
