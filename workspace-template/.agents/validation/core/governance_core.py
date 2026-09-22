"""Governance Core — Single Authoritative Completion & Governance Evaluator.

Implements:
- P0-01: Shared authoritative completion evaluator across Stop Hook, Validators, and CI.
- P0-02: Task-scoped Stop evaluation (strictly scoped, never falls back to all tasks if filter missing).
- P0-03: Strict fullyIdle requirement (must be present, boolean, and True).
- P0-04 / P0-06: Evaluates canonical state (tasks/, governance/, events/, blockers/) first.
- P0-08 / P0-09: Validates event schema, sequence monotonicity, and TASK_STARTED < TASK_COMPLETED.
- P0-22: Grounded external approval verification for High-Assurance tasks.
- P0-24 / P0-25 / P0-26 / P0-27: Machine-enforced verification policy & canonical gate registry.
- P0-28 / P0-29: ADR registration verification against docs/decisions/INDEX.md.
- P0-35 / P0-36 / P0-37: Scoped blocker validation (global vs task-scoped, resolved semantics).
"""

from dataclasses import dataclass
import json
import os
from pathlib import Path
import re
from typing import Any, Dict, List, Optional, Set, Tuple

try:
    from .workspace_resolver import resolve_workspace, WorkspaceInfo
    from .verification_policy import (
        VerificationPolicyEngine,
        normalize_task_type,
        is_canonical_task_type,
        is_substantive_evidence,
    )
except (ImportError, ValueError):
    from workspace_resolver import resolve_workspace, WorkspaceInfo
    from verification_policy import (
        VerificationPolicyEngine,
        normalize_task_type,
        is_canonical_task_type,
        is_substantive_evidence,
    )

NON_TERMINAL_STATES = {
    "DRAFT",
    "CLASSIFIED",
    "CONTEXT_READY",
    "PLANNED",
    "PENDING",
    "READY",
    "IN_PROGRESS",
    "TESTING",
    "VERIFYING",
    "REVIEWING",
    "MEMORY_SYNC",
    "STATE_SYNC",
    "GOVERNANCE_CHECK",
}

TERMINAL_STATES = {
    "COMPLETED",
    "FAILED",
    "CANCELLED",
}

EVENT_ID_PATTERN = re.compile(r"^EVT-[0-9]{4,}$")
BLOCKER_ID_PATTERN = re.compile(r"^(?:BLK|BLOCKER)-[0-9]{3,}$")
TASK_ID_PATTERN = re.compile(r"^TASK-[0-9]{3,}$")


@dataclass
class CompletionResult:
    allowed: bool
    decision: str  # "allow" or "continue"
    reason: Optional[str] = None
    task_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        res: Dict[str, Any] = {
            "allowed": self.allowed,
            "decision": self.decision,
        }
        if self.reason:
            res["reason"] = self.reason
        if self.task_id:
            res["taskId"] = self.task_id
        return res


def _check_adr_registration(workspace_root: Path, adr_id: str) -> Tuple[bool, str]:
    """Verify that ADR is registered in docs/decisions/INDEX.md (P0-29)."""
    index_file = workspace_root / "docs" / "decisions" / "INDEX.md"
    if not index_file.is_file():
        # Check without docs/ prefix if not found
        index_file = workspace_root / "decisions" / "INDEX.md"
        if not index_file.is_file():
            return False, f"ADR registry '{index_file}' does not exist."
    try:
        with open(index_file, "r", encoding="utf-8") as f:
            content = f.read()
        if adr_id in content:
            return True, ""
        return False, f"ADR '{adr_id}' is not registered in '{index_file}'."
    except Exception as e:
        return False, f"Failed to read ADR index '{index_file}': {e}"


def evaluate_governance_completion(
    workspace_root: Optional[str or Path] = None,
    payload: Optional[Dict[str, Any]] = None,
    task_id_filter: Optional[str] = None,
    state_dir_override: Optional[str or Path] = None,
) -> CompletionResult:
    """Authoritative evaluation of task completion and Stop hook invariants."""
    payload = payload or {}

    # P0-03: Require fullyIdle == True
    fully_idle = payload.get("fullyIdle")
    if fully_idle is None:
        return CompletionResult(
            allowed=False,
            decision="continue",
            reason="[GOVERNANCE GUARD] Cannot stop: Required runtime signal 'fullyIdle' is missing. Wait for Antigravity runtime to report worker status.",
        )
    if not isinstance(fully_idle, bool):
        return CompletionResult(
            allowed=False,
            decision="continue",
            reason=f"[GOVERNANCE GUARD] Cannot stop: Runtime signal 'fullyIdle' must be boolean, got {type(fully_idle).__name__}.",
        )
    if fully_idle is False:
        return CompletionResult(
            allowed=False,
            decision="continue",
            reason="[GOVERNANCE GUARD] Cannot stop: Background tasks or subagents are still actively running (fullyIdle=false). Wait for all async workers to complete.",
        )

    # Resolve workspace deterministically
    ws_info = resolve_workspace(
        start_path=workspace_root,
        payload=payload,
    )

    # If workspace is not governed, allow stop
    if not ws_info.is_governed:
        return CompletionResult(allowed=True, decision="allow")

    state_dir = Path(state_dir_override) if state_dir_override else ws_info.state_root
    if not state_dir.is_dir():
        return CompletionResult(
            allowed=False,
            decision="continue",
            reason="[GOVERNANCE GUARD] Cannot stop: Governed workspace detected but state directory '.agents/state/' is missing or unreadable. State must not be bypassed.",
        )

    # 1. Load canonical blockers & validate semantics (P0-35, P0-36, P0-37)
    global_active_blockers: List[Dict[str, Any]] = []
    task_active_blockers: Dict[str, List[Dict[str, Any]]] = {}

    def _process_blocker(b: Dict[str, Any], src_name: str) -> Optional[str]:
        if not isinstance(b, dict):
            return f"Corrupt blocker record in '{src_name}': expected object."
        b_id = b.get("id", "UNKNOWN")
        status = b.get("status", "active")
        scope = b.get("scope", "global" if not b.get("taskId") else "task")
        t_id = b.get("taskId")

        # Semantic validation
        if status == "resolved":
            if not b.get("resolvedAt") or not b.get("resolution"):
                return f"Blocker '{b_id}' is marked resolved but missing required resolvedAt or resolution."
        elif status == "active":
            if scope in {"global", "project"} or not t_id or t_id == "__global__":
                global_active_blockers.append(b)
            else:
                task_active_blockers.setdefault(t_id, []).append(b)
        return None

    blockers_dir = state_dir / "blockers"
    if blockers_dir.is_dir():
        for fname in sorted(os.listdir(blockers_dir)):
            if fname.endswith(".json"):
                fpath = blockers_dir / fname
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        b_rec = json.load(f)
                except Exception as e:
                    return CompletionResult(
                        allowed=False,
                        decision="continue",
                        reason=f"[GOVERNANCE GUARD] Cannot stop: Failed to parse blocker file '{fname}': {e}. Fix state corruption before stopping.",
                    )
                items = b_rec if isinstance(b_rec, list) else (b_rec.get("active", []) if isinstance(b_rec, dict) and "active" in b_rec else [b_rec])
                for b in items:
                    err = _process_blocker(b, fname)
                    if err:
                        return CompletionResult(allowed=False, decision="continue", reason=f"[GOVERNANCE GUARD] {err}")

    # Read aggregate blockers.json
    agg_blockers_file = state_dir / "blockers.json"
    if agg_blockers_file.is_file():
        try:
            with open(agg_blockers_file, "r", encoding="utf-8") as f:
                b_agg = json.load(f)
        except Exception as e:
            return CompletionResult(
                allowed=False,
                decision="continue",
                reason=f"[GOVERNANCE GUARD] Cannot stop: Failed to parse aggregate blockers file '{agg_blockers_file.name}': {e}. Fix state corruption before stopping.",
            )
        if isinstance(b_agg, dict):
            for b in b_agg.get("active", []):
                err = _process_blocker(b, "blockers.json")
                if err:
                    return CompletionResult(allowed=False, decision="continue", reason=f"[GOVERNANCE GUARD] {err}")

    # Check global active blockers
    if global_active_blockers:
        b = global_active_blockers[0]
        b_id = b.get("id", "UNKNOWN")
        desc = b.get("what") or b.get("description") or "Global active blocker"
        return CompletionResult(
            allowed=False,
            decision="continue",
            reason=f"[GOVERNANCE GUARD] Cannot stop: Unresolved global blocker '{b_id}': {desc}. Please resolve before stopping.",
        )

    # 2. Load Tasks (P0-04, P0-06)
    tasks: Dict[str, Dict[str, Any]] = {}

    # Aggregate first (if present)
    agg_tasks_file = state_dir / "tasks.json"
    if agg_tasks_file.is_file():
        try:
            with open(agg_tasks_file, "r", encoding="utf-8") as f:
                t_agg = json.load(f)
            if isinstance(t_agg, dict):
                for t in t_agg.get("tasks", []):
                    if isinstance(t, dict) and t.get("id"):
                        tasks[t["id"]] = t
        except Exception as e:
            return CompletionResult(
                allowed=False,
                decision="continue",
                reason=f"[GOVERNANCE GUARD] Cannot stop: Failed to parse tasks file '{agg_tasks_file.name}': {e}. Fix state corruption before stopping.",
            )

    # Canonical per-task files overwrite aggregate
    tasks_dir = state_dir / "tasks"
    if tasks_dir.is_dir():
        for fname in sorted(os.listdir(tasks_dir)):
            if fname.endswith(".json"):
                fpath = tasks_dir / fname
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        t = json.load(f)
                    if isinstance(t, dict) and t.get("id"):
                        tasks[t["id"]] = t
                except Exception as e:
                    return CompletionResult(
                        allowed=False,
                        decision="continue",
                        reason=f"[GOVERNANCE GUARD] Cannot stop: Failed to parse per-task file '{fname}': {e}. Fix state corruption before stopping.",
                    )

    # 3. Load Governance Records
    gov_records: Dict[str, Dict[str, Any]] = {}
    agg_gov_file = state_dir / "governance.json"
    if agg_gov_file.is_file():
        try:
            with open(agg_gov_file, "r", encoding="utf-8") as f:
                g_agg = json.load(f)
            if isinstance(g_agg, dict):
                for r in g_agg.get("records", []):
                    if isinstance(r, dict) and r.get("taskId"):
                        gov_records[r["taskId"]] = r
        except Exception as e:
            return CompletionResult(
                allowed=False,
                decision="continue",
                reason=f"[GOVERNANCE GUARD] Cannot stop: Failed to parse governance file '{agg_gov_file.name}': {e}. Fix state corruption before stopping.",
            )

    gov_dir = state_dir / "governance"
    if gov_dir.is_dir():
        for fname in sorted(os.listdir(gov_dir)):
            if fname.endswith(".json"):
                fpath = gov_dir / fname
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        r = json.load(f)
                    if isinstance(r, dict) and r.get("taskId"):
                        gov_records[r["taskId"]] = r
                except Exception as e:
                    return CompletionResult(
                        allowed=False,
                        decision="continue",
                        reason=f"[GOVERNANCE GUARD] Cannot stop: Failed to parse per-task governance file '{fname}': {e}. Fix state corruption before stopping.",
                    )

    # 4. Load Events per task
    events_by_task: Dict[str, List[Dict[str, Any]]] = {}
    events_dir = state_dir / "events"
    if events_dir.is_dir():
        for fname in sorted(os.listdir(events_dir)):
            if fname.endswith(".jsonl") or fname.endswith(".json"):
                fpath = events_dir / fname
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        for line in f:
                            l = line.strip()
                            if l:
                                ev = json.loads(l)
                                if isinstance(ev, dict):
                                    t_id = ev.get("taskId") or "__global__"
                                    events_by_task.setdefault(t_id, []).append(ev)
                except Exception as e:
                    return CompletionResult(
                        allowed=False,
                        decision="continue",
                        reason=f"[GOVERNANCE GUARD] Cannot stop: Failed to parse events file '{fname}': {e}. Fix state corruption before stopping.",
                    )

    agg_events_file = state_dir / "events.jsonl"
    if agg_events_file.is_file():
        try:
            with open(agg_events_file, "r", encoding="utf-8") as f:
                for line in f:
                    l = line.strip()
                    if l:
                        ev = json.loads(l)
                        if isinstance(ev, dict):
                            t_id = ev.get("taskId") or "__global__"
                            if ev not in events_by_task.get(t_id, []):
                                events_by_task.setdefault(t_id, []).append(ev)
        except Exception as e:
            return CompletionResult(
                allowed=False,
                decision="continue",
                reason=f"[GOVERNANCE GUARD] Cannot stop: Failed to parse aggregate events file '{agg_events_file.name}': {e}. Fix state corruption before stopping.",
            )

    # 5. P0-02: Task-scoped Stop evaluation
    # Determine the target task(s) to evaluate
    effective_task_id = task_id_filter or payload.get("taskId") or payload.get("activeTaskId")

    if effective_task_id:
        if effective_task_id not in tasks:
            # P0-02 Rule: task ID supplied but missing -> CONTINUE with ERROR, NEVER evaluate all tasks!
            return CompletionResult(
                allowed=False,
                decision="continue",
                reason=f"[GOVERNANCE GUARD] Cannot stop: Scoped task '{effective_task_id}' was not found in canonical or aggregate state. Fix task configuration before stopping.",
                task_id=effective_task_id,
            )
        target_tasks = [tasks[effective_task_id]]
    else:
        # No task ID supplied: check if tasks exist
        if not tasks:
            # Governed workspace with no tasks defined
            return CompletionResult(allowed=True, decision="allow")

        # If exactly 1 task exists in state, evaluate that task
        if len(tasks) == 1:
            target_tasks = list(tasks.values())
        else:
            # If multiple tasks exist, check if there are in-progress tasks
            in_progress = [t for t in tasks.values() if t.get("status") in NON_TERMINAL_STATES]
            if in_progress:
                t = in_progress[0]
                return CompletionResult(
                    allowed=False,
                    decision="continue",
                    reason=f"[GOVERNANCE GUARD] Cannot stop: Task '{t.get('id')}' is currently in state '{t.get('status')}'. Complete active work before stopping.",
                    task_id=t.get("id"),
                )
            target_tasks = list(tasks.values())

    policy_engine = VerificationPolicyEngine()

    for t in target_tasks:
        t_id = t.get("id", "UNKNOWN")
        t_status = t.get("status")

        # 1. Non-terminal states must NOT stop
        if t_status in NON_TERMINAL_STATES:
            return CompletionResult(
                allowed=False,
                decision="continue",
                reason=(
                    f"[GOVERNANCE GUARD] Cannot stop: Task '{t_id}' is currently in state '{t_status}'. "
                    f"Please complete implementation, verify all quality gates, and finalize governance before stopping."
                ),
                task_id=t_id,
            )

        # 2. Unknown status check (P1-09)
        if t_status not in TERMINAL_STATES and t_status not in NON_TERMINAL_STATES:
            return CompletionResult(
                allowed=False,
                decision="continue",
                reason=f"[GOVERNANCE GUARD] Cannot stop: Task '{t_id}' has unknown status '{t_status}'. Status must be a recognized lifecycle state.",
                task_id=t_id,
            )

        # 3. If COMPLETED, enforce full authoritative completion gate
        if t_status == "COMPLETED":
            # A. Task-scoped active blocker check (P0-37)
            if task_active_blockers.get(t_id):
                b = task_active_blockers[t_id][0]
                b_id = b.get("id", "UNKNOWN")
                desc = b.get("what") or b.get("description") or "Active blocker"
                return CompletionResult(
                    allowed=False,
                    decision="continue",
                    reason=f"[GOVERNANCE GUARD] Cannot stop: Task '{t_id}' has unresolved active blocker '{b_id}': {desc}.",
                    task_id=t_id,
                )

            # B. Governance record must exist
            g_rec = gov_records.get(t_id)
            if not g_rec:
                return CompletionResult(
                    allowed=False,
                    decision="continue",
                    reason=f"[GOVERNANCE GUARD] Cannot stop: Task '{t_id}' is marked COMPLETED but has no governance record.",
                    task_id=t_id,
                )

            # C. Governance status must be complete
            g_status = g_rec.get("governanceStatus")
            if g_status != "complete":
                return CompletionResult(
                    allowed=False,
                    decision="continue",
                    reason=f"[GOVERNANCE GUARD] Cannot stop: Task '{t_id}' is COMPLETED but its governance status is '{g_status}' (must be 'complete').",
                    task_id=t_id,
                )

            # D. Executable verification policy evaluation (P0-24, P0-25, P0-26, P0-27)
            task_type = t.get("type") or (g_rec.get("classification") or {}).get("type", "feature")
            risk_level = t.get("riskLevel") or (g_rec.get("classification") or {}).get("risk", "medium")
            recorded_gates = g_rec.get("qualityGates", [])

            passed, eval_results, fail_reason = policy_engine.evaluate_gates(
                task_type=task_type,
                risk_level=risk_level,
                recorded_gates=recorded_gates,
            )
            if not passed:
                return CompletionResult(
                    allowed=False,
                    decision="continue",
                    reason=f"[GOVERNANCE GUARD] Cannot stop: Task '{t_id}' failed quality gate evaluation: {fail_reason}",
                    task_id=t_id,
                )

            # E. Event stream validation (P0-08, P0-09)
            t_events = events_by_task.get(t_id, [])
            if not t_events:
                return CompletionResult(
                    allowed=False,
                    decision="continue",
                    reason=f"[GOVERNANCE GUARD] Cannot stop: Task '{t_id}' has no recorded execution events.",
                    task_id=t_id,
                )

            start_ev: Optional[Dict[str, Any]] = None
            complete_ev: Optional[Dict[str, Any]] = None
            seen_seqs: Set[int] = set()
            prev_seq = 0

            for ev in t_events:
                if not isinstance(ev, dict):
                    continue
                ev_name = ev.get("event")
                seq = ev.get("sequence")
                ev_id = ev.get("eventId")

                # Sequence validation if sequence is present
                if seq is not None and isinstance(seq, int):
                    if seq <= prev_seq and seq in seen_seqs:
                        return CompletionResult(
                            allowed=False,
                            decision="continue",
                            reason=f"[GOVERNANCE GUARD] Cannot stop: Task '{t_id}' has non-monotonic event sequence ({seq} after {prev_seq}).",
                            task_id=t_id,
                        )
                    seen_seqs.add(seq)
                    prev_seq = seq

                if ev_name == "TASK_STARTED":
                    start_ev = ev
                elif ev_name == "TASK_COMPLETED":
                    complete_ev = ev

            if not start_ev:
                return CompletionResult(
                    allowed=False,
                    decision="continue",
                    reason=f"[GOVERNANCE GUARD] Cannot stop: Task '{t_id}' execution event stream is missing mandatory 'TASK_STARTED'.",
                    task_id=t_id,
                )
            if not complete_ev:
                return CompletionResult(
                    allowed=False,
                    decision="continue",
                    reason=f"[GOVERNANCE GUARD] Cannot stop: Task '{t_id}' execution event stream is missing mandatory 'TASK_COMPLETED'.",
                    task_id=t_id,
                )

            # Check sequence ordering if both have sequence
            start_seq = start_ev.get("sequence")
            complete_seq = complete_ev.get("sequence")
            if start_seq is not None and complete_seq is not None:
                if start_seq >= complete_seq:
                    return CompletionResult(
                        allowed=False,
                        decision="continue",
                        reason=f"[GOVERNANCE GUARD] Cannot stop: Task '{t_id}' TASK_STARTED sequence ({start_seq}) >= TASK_COMPLETED sequence ({complete_seq}).",
                        task_id=t_id,
                    )

            # F. Approval requirements check (P0-22)
            approvals = g_rec.get("approvalRequirements", {})
            if isinstance(approvals, dict) and approvals.get("required") is True:
                if not approvals.get("satisfied"):
                    return CompletionResult(
                        allowed=False,
                        decision="continue",
                        reason=f"[GOVERNANCE GUARD] Cannot stop: Task '{t_id}' requires approval but approvalRequirements.satisfied is False.",
                        task_id=t_id,
                    )
                if not approvals.get("approvalSource") and not approvals.get("approvalId") and not approvals.get("approver"):
                    return CompletionResult(
                        allowed=False,
                        decision="continue",
                        reason=f"[GOVERNANCE GUARD] Cannot stop: Task '{t_id}' approval is satisfied but lacks authoritative external approval reference (approvalSource/approvalId/approver).",
                        task_id=t_id,
                    )

            # G. ADR registration check (P0-28, P0-29)
            adrs = g_rec.get("relevantAdrs", [])
            if adrs and isinstance(adrs, list):
                for adr_ref in adrs:
                    if isinstance(adr_ref, str) and adr_ref.startswith("ADR-"):
                        ok, adr_err = _check_adr_registration(ws_info.project_root, adr_ref)
                        if not ok:
                            return CompletionResult(
                                allowed=False,
                                decision="continue",
                                reason=f"[GOVERNANCE GUARD] Cannot stop: Task '{t_id}' references unverified ADR: {adr_err}",
                                task_id=t_id,
                            )

    return CompletionResult(allowed=True, decision="allow")
