"""Verification Policy Engine — Executable verification rules and canonical gate registry.

Implements:
- P0-23: 16 canonical task types + alias mapping (review modeled as gate/activity).
- P0-24: Executable verification policy deriving required gates from task type, risk, and changed files.
- P0-25: NOT_APPLICABLE requires evidence and non-empty justification.
- P0-26: not_configured can NEVER satisfy a required gate.
- P0-27: Canonical gate kinds (test, lint, typecheck, build, security, diff-review, memory-sync, adr).
         No keyword-based substring matching!
"""

from dataclasses import dataclass, field
from enum import Enum
import re
from typing import Any, Dict, List, Optional, Set, Tuple


class GateKind(str, Enum):
    TEST = "test"
    LINT = "lint"
    TYPECHECK = "typecheck"
    BUILD = "build"
    SECURITY = "security"
    DIFF_REVIEW = "diff-review"
    MEMORY_SYNC = "memory-sync"
    ADR = "adr"


# Canonical 16 task types (P0-23)
CANONICAL_TASK_TYPES = {
    "simple",
    "bug",
    "feature",
    "complex-feature",
    "refactor",
    "architecture",
    "security",
    "database",
    "migration",
    "performance",
    "testing",
    "deployment",
    "documentation",
    "requirements",
    "investigation",
    "infrastructure",
}

# Aliases mapped to canonical types
TASK_TYPE_ALIASES = {
    "bugfix": "bug",
    "test": "testing",
    "docs": "documentation",
    "infra": "infrastructure",
}

# Canonical Gate Registry (P0-27)
CANONICAL_GATE_REGISTRY: Dict[str, Dict[str, Any]] = {
    "lint": {
        "id": "GATE-LINT",
        "kind": GateKind.LINT,
        "name": "lint",
        "description": "Static code analysis and style checks",
    },
    "format": {
        "id": "GATE-FORMAT",
        "kind": GateKind.LINT,
        "name": "format",
        "description": "Code formatting verification",
    },
    "docLint": {
        "id": "GATE-DOCLINT",
        "kind": GateKind.LINT,
        "name": "docLint",
        "description": "Documentation linter verification",
    },
    "typecheck": {
        "id": "GATE-TYPECHECK",
        "kind": GateKind.TYPECHECK,
        "name": "typecheck",
        "description": "Static type checking verification",
    },
    "test": {
        "id": "GATE-TEST",
        "kind": GateKind.TEST,
        "name": "test",
        "description": "Automated behavioral and regression test execution",
    },
    "migrationTest": {
        "id": "GATE-MIGRATION-TEST",
        "kind": GateKind.TEST,
        "name": "migrationTest",
        "description": "Database schema migration test",
    },
    "benchmark": {
        "id": "GATE-BENCHMARK",
        "kind": GateKind.TEST,
        "name": "benchmark",
        "description": "Performance benchmark execution",
    },
    "smokeTest": {
        "id": "GATE-SMOKE",
        "kind": GateKind.TEST,
        "name": "smokeTest",
        "description": "Smoke and health check testing",
    },
    "dryRun": {
        "id": "GATE-DRYRUN",
        "kind": GateKind.TEST,
        "name": "dryRun",
        "description": "Infrastructure deployment plan dry-run",
    },
    "build": {
        "id": "GATE-BUILD",
        "kind": GateKind.BUILD,
        "name": "build",
        "description": "Compilation and deployable package build verification",
    },
    "security": {
        "id": "GATE-SECURITY",
        "kind": GateKind.SECURITY,
        "name": "security",
        "description": "Security scanning, SAST, or dependency vulnerability checks",
    },
    "diffReview": {
        "id": "GATE-DIFF-REVIEW",
        "kind": GateKind.DIFF_REVIEW,
        "name": "diffReview",
        "description": "Automated or peer diff review for blast radius and correctness",
    },
    "rollbackPlan": {
        "id": "GATE-ROLLBACK",
        "kind": GateKind.DIFF_REVIEW,
        "name": "rollbackPlan",
        "description": "Reversibility and rollback plan review",
    },
    "governanceValidation": {
        "id": "GATE-GOV-VALIDATION",
        "kind": GateKind.DIFF_REVIEW,
        "name": "governanceValidation",
        "description": "Governance schema and artifact consistency validation",
    },
    "memorySync": {
        "id": "GATE-MEM-SYNC",
        "kind": GateKind.MEMORY_SYNC,
        "name": "memorySync",
        "description": "Durable knowledge and project memory synchronization",
    },
    "adrReview": {
        "id": "GATE-ADR",
        "kind": GateKind.ADR,
        "name": "adrReview",
        "description": "Architecture Decision Record compliance and registration",
    },
}

TRIVIAL_STRINGS = {
    "trust me", "done", "passed", "pass", "ok", "okay", "works", "working",
    "true", "yes", "verified", "tested", "good", "looks good", "dummy",
    "placeholder", "todo", "fixme", "n/a", "na", "none", "null", "test",
    "see output", "all good"
}


def normalize_task_type(task_type: str) -> str:
    """Normalize task type using canonical taxonomy and alias map (P0-23)."""
    t = task_type.strip().lower()
    return TASK_TYPE_ALIASES.get(t, t)


def is_canonical_task_type(task_type: str) -> bool:
    """Check if task type is one of the 16 canonical types."""
    return task_type in CANONICAL_TASK_TYPES


def is_substantive_evidence(evidence: Any) -> bool:
    """Evaluate whether evidence is substantive (P0-01, P0-25)."""
    if isinstance(evidence, dict):
        ev_type = evidence.get("type")
        return bool(
            ev_type and (
                evidence.get("artifact") or
                evidence.get("command") or
                evidence.get("runId") or
                evidence.get("evidenceRef") or
                evidence.get("summary")
            )
        )
    if not evidence or not isinstance(evidence, str):
        return False
    trimmed = evidence.strip()
    if len(trimmed) < 6:
        return False
    lower = trimmed.lower()
    if lower in TRIVIAL_STRINGS:
        return False
    if any(re.search(p, lower) for p in [r"\btrust me\b", r"\bworks for me\b", r"\bplaceholder\b", r"\bdummy\b"]):
        return False
    return True


@dataclass
class GateEvaluationResult:
    gate_name: str
    status: str
    passed: bool
    kind: GateKind
    error: Optional[str] = None


class VerificationPolicyEngine:
    """Executable verification policy determining and checking required quality gates."""

    def __init__(self, policy_yaml_data: Optional[Dict[str, Any]] = None):
        self.policy_data = policy_yaml_data or {}

    def get_required_gates(self, task_type: str, risk_level: str) -> List[str]:
        """Derive the required gate identifiers based on task type and risk level (P0-24)."""
        canon_type = normalize_task_type(task_type)
        risk = risk_level.strip().lower()

        required_set: Set[str] = set()

        # 1. Base gates by risk level
        if risk == "low":
            required_set.update(["lint"])
        elif risk == "medium":
            required_set.update(["lint", "typecheck", "test", "build"])
        elif risk == "high":
            required_set.update(["lint", "typecheck", "test", "build", "security", "memorySync"])
        elif risk == "critical":
            required_set.update([
                "lint", "typecheck", "test", "build", "security",
                "memorySync", "adrReview", "diffReview"
            ])
        else:
            # Default to medium if unknown risk
            required_set.update(["lint", "typecheck", "test", "build"])

        # 2. Type-specific mandatory overrides
        if canon_type == "simple":
            # Simple tasks only mandate lint
            required_set = {"lint"}
        elif canon_type in {"documentation", "requirements", "investigation"}:
            # Doc/req/investigation only mandate docLint or lint, not binary build
            required_set = {"lint"}
        elif canon_type == "security":
            required_set.update(["security", "test", "diffReview"])
        elif canon_type == "migration":
            required_set.update(["migrationTest", "rollbackPlan", "adrReview", "test"])
        elif canon_type == "architecture":
            required_set.update(["adrReview", "diffReview"])
        elif canon_type == "performance":
            required_set.update(["benchmark", "test"])
        elif canon_type == "testing":
            required_set.update(["test"])
        elif canon_type == "deployment":
            required_set.update(["build", "security", "smokeTest"])

        return sorted(list(required_set))

    def evaluate_gates(
        self,
        task_type: str,
        risk_level: str,
        recorded_gates: List[Dict[str, Any]],
    ) -> Tuple[bool, List[GateEvaluationResult], Optional[str]]:
        """Evaluate recorded gates against required policy gates.

        Returns:
            (all_passed, results, failure_reason)
        """
        required_gates = self.get_required_gates(task_type, risk_level)
        recorded_map: Dict[str, Dict[str, Any]] = {}
        for g in recorded_gates:
            if isinstance(g, dict) and g.get("name"):
                recorded_map[g["name"]] = g

        results: List[GateEvaluationResult] = []

        # Check all required gates
        for req in required_gates:
            reg_entry = CANONICAL_GATE_REGISTRY.get(req, {
                "id": f"GATE-{req.upper()}",
                "kind": GateKind.TEST if "test" in req.lower() else GateKind.LINT,
                "name": req,
            })
            kind = reg_entry["kind"]

            if req not in recorded_map:
                res = GateEvaluationResult(
                    gate_name=req,
                    status="missing",
                    passed=False,
                    kind=kind,
                    error=f"Mandatory verification gate '{req}' is missing from governance record.",
                )
                results.append(res)
                return False, results, res.error

            g_rec = recorded_map[req]
            status = g_rec.get("status", "unknown")

            # P0-26: not_configured can NEVER satisfy a required gate
            if status == "not_configured":
                res = GateEvaluationResult(
                    gate_name=req,
                    status=status,
                    passed=False,
                    kind=kind,
                    error=f"Mandatory verification gate '{req}' cannot pass with status 'not_configured'.",
                )
                results.append(res)
                return False, results, res.error

            # P0-25: NOT_APPLICABLE requires evidence
            if status == "not_applicable":
                reason = g_rec.get("reason") or ""
                app_evidence = g_rec.get("applicabilityEvidence") or g_rec.get("evidenceRef") or g_rec.get("evidence")
                if not reason.strip():
                    res = GateEvaluationResult(
                        gate_name=req,
                        status=status,
                        passed=False,
                        kind=kind,
                        error=f"Gate '{req}' marked 'not_applicable' without explanatory reason.",
                    )
                    results.append(res)
                    return False, results, res.error
                if not is_substantive_evidence(app_evidence):
                    res = GateEvaluationResult(
                        gate_name=req,
                        status=status,
                        passed=False,
                        kind=kind,
                        error=f"Gate '{req}' marked 'not_applicable' lacks required substantive applicabilityEvidence.",
                    )
                    results.append(res)
                    return False, results, res.error
                res = GateEvaluationResult(
                    gate_name=req,
                    status=status,
                    passed=True,
                    kind=kind,
                )
                results.append(res)
                continue

            if status in {"failed", "blocked", "pending", "unknown"}:
                res = GateEvaluationResult(
                    gate_name=req,
                    status=status,
                    passed=False,
                    kind=kind,
                    error=f"Mandatory verification gate '{req}' is non-passing (status='{status}').",
                )
                results.append(res)
                return False, results, res.error

            if status == "passed":
                ev = g_rec.get("evidenceRef") or g_rec.get("evidence")
                if not is_substantive_evidence(ev):
                    res = GateEvaluationResult(
                        gate_name=req,
                        status=status,
                        passed=False,
                        kind=kind,
                        error=f"Gate '{req}' marked 'passed' lacks substantive verification evidence.",
                    )
                    results.append(res)
                    return False, results, res.error
                res = GateEvaluationResult(
                    gate_name=req,
                    status=status,
                    passed=True,
                    kind=kind,
                )
                results.append(res)

        # Ensure at least one gate actually passed (prevent all-N/A pass on medium/high/critical)
        risk = risk_level.strip().lower()
        if risk in {"medium", "high", "critical"}:
            has_passed = any(r.passed and r.status == "passed" for r in results)
            if not has_passed:
                return False, results, f"Task risk is '{risk}' but zero required verification gates passed (all gates were N/A or unexecuted)."

        return True, results, None
