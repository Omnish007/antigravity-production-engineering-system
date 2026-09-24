"""Workspace Resolver — Authoritative workspace and governance root resolution.

Provides deterministic resolution of project root, governance root (.agents),
and state root (.agents/state) with explicit sentinel validation (P0-30),
no template-specific path assumptions (P0-31), and a single source of truth (P0-32).
"""

from dataclasses import dataclass
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Optional, List, Dict, Any


@dataclass
class WorkspaceInfo:
    project_root: Path
    governance_root: Path
    state_root: Path
    is_governed: bool
    sentinel: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


def _find_sentinel_in_dir(dir_path: Path) -> Optional[tuple[Path, Dict[str, Any]]]:
    """Check if dir_path contains a valid .agents/state/project.json sentinel."""
    candidate = dir_path / ".agents" / "state" / "project.json"
    if candidate.is_file():
        try:
            with open(candidate, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict) and data.get("governanceMode") == "managed":
                return candidate, data
        except Exception:
            return candidate, {"governanceMode": "corrupt"}
    return None


def resolve_workspace(
    start_path: Optional[str or Path] = None,
    payload: Optional[Dict[str, Any]] = None,
    require_governed: bool = False,
) -> WorkspaceInfo:
    """Resolve project root, governance root (.agents), and state root deterministically.

    Order of evaluation:
    1. Explicit payload['workspacePaths'] if supplied (first valid path).
    2. Explicit start_path if supplied.
    3. Traversal upward from current working directory (Path.cwd()).
    4. Traversal upward from script directory (os.path.abspath(__file__)).
    5. Git top-level directory if inside a git repository.
    """
    candidates: List[Path] = []

    # 1. Runtime payload workspace paths
    if payload and isinstance(payload, dict):
        ws_paths = payload.get("workspacePaths") or []
        if isinstance(ws_paths, list):
            for wp in ws_paths:
                if wp and isinstance(wp, str):
                    candidates.append(Path(wp).resolve())

    # 2. Explicit start path
    if start_path:
        candidates.append(Path(start_path).resolve())

    # 3. Current working directory
    try:
        candidates.append(Path.cwd().resolve())
    except Exception:
        pass

    # 4. Search upward from candidates for sentinel
    resolved_root: Optional[Path] = None
    sentinel_data: Optional[Dict[str, Any]] = None

    for base in candidates:
        curr = base if base.is_dir() else base.parent
        # Walk upward
        for p in [curr, *curr.parents]:
            res = _find_sentinel_in_dir(p)
            if res:
                resolved_root = p
                sentinel_data = res[1]
                break
        if resolved_root:
            break

    # 5. Git root fallback check if sentinel wasn't found in normal walk
    if not resolved_root:
        for base in candidates:
            try:
                res = subprocess.run(
                    ["git", "rev-parse", "--show-toplevel"],
                    cwd=str(base if base.is_dir() else base.parent),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=2,
                )
                if res.returncode == 0:
                    git_root = Path(res.stdout.strip()).resolve()
                    s_res = _find_sentinel_in_dir(git_root)
                    if s_res:
                        resolved_root = git_root
                        sentinel_data = s_res[1]
                        break
            except Exception:
                pass

    # 6. Do not infer governance solely from the presence of a `.agents` directory.
    # A workspace is governed only when the managed project sentinel is valid.

    # 7. Ultimate fallback: CWD
    if not resolved_root:
        resolved_root = Path.cwd().resolve()

    governance_dir = resolved_root / ".agents"
    state_dir = governance_dir / "state"
    is_governed = False

    if sentinel_data and sentinel_data.get("governanceMode") == "managed":
        is_governed = True
    elif governance_dir.is_dir() and (state_dir / "project.json").is_file():
        # Read to verify
        try:
            with open(state_dir / "project.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            if data.get("governanceMode") == "managed":
                is_governed = True
                sentinel_data = data
        except Exception:
            pass

    if require_governed and not is_governed:
        return WorkspaceInfo(
            project_root=resolved_root,
            governance_root=governance_dir,
            state_root=state_dir,
            is_governed=False,
            error=f"Workspace at '{resolved_root}' is not a valid governed project (missing managed sentinel project.json).",
        )

    return WorkspaceInfo(
        project_root=resolved_root,
        governance_root=governance_dir,
        state_root=state_dir,
        is_governed=is_governed,
        sentinel=sentinel_data,
    )


if __name__ == "__main__":
    info = resolve_workspace()
    print(f"Project Root: {info.project_root}")
    print(f"Governance Root: {info.governance_root}")
    print(f"State Root: {info.state_root}")
    print(f"Governed: {info.is_governed}")
    if info.sentinel:
        print(f"Sentinel: {info.sentinel.get('projectId', 'unknown')}")
