#!/usr/bin/env python3
"""Automated Static Architecture Linter (RULE-ARCH-LAYER-001).

Validates architecture boundaries. By default, it checks only explicitly selected/conventional boundaries; --strict enables the legacy four-layer policy for projects that have adopted it:
1. Route Violations: Forbids direct ORM/database imports and query calls in routes/endpoints/API handlers.
2. Controller Violations: Forbids direct ORM/DB model imports and query calls in controllers.
3. Service Violations: Forbids HTTP transport coupling (Request, Response, status codes) in domain services.
4. Frontend Violations: Forbids direct fetch() / axios calls inside UI components and views.

Usage:
    python3 check-architecture.py [--root PATH] [--strict] [--json] [--verbose]
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
import os
from pathlib import Path
import re
import sys
from typing import List, Optional, Pattern

# ANSI Color codes
COLOR_RESET = "\033[0m"
COLOR_RED = "\033[31m"
COLOR_GREEN = "\033[32m"
COLOR_YELLOW = "\033[33m"
COLOR_CYAN = "\033[36m"
COLOR_BOLD = "\033[1m"

DEFAULT_IGNORE_DIRS = {
    "node_modules",
    ".git",
    "dist",
    "build",
    ".next",
    ".nuxt",
    ".svelte-kit",
    "coverage",
    "venv",
    ".venv",
    "__pycache__",
    ".agents",
    "docs",
    ".turbo",
    ".output",
}

VALID_EXTENSIONS = {
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".mjs",
    ".cjs",
    ".py",
    ".go",
    ".java",
    ".vue",
    ".svelte",
}


@dataclass
class ArchitectureViolation:
    rule_id: str
    category: str
    file_path: str
    line_number: int
    line_content: str
    message: str
    remediation: str
    severity: str = "ERROR"  # ERROR or WARNING


class ArchitectureChecker:
    def __init__(
        self,
        root_dir: Path,
        ignore_dirs: Optional[set[str]] = None,
        verbose: bool = False,
    ):
        self.root_dir = root_dir.resolve()
        self.ignore_dirs = ignore_dirs or DEFAULT_IGNORE_DIRS
        self.verbose = verbose
        self.violations: List[ArchitectureViolation] = []

        # Route regex patterns
        self.re_orm_imports_js = re.compile(
            r"""(?:import\s+.*\s+from\s+['"](?:mongoose|@prisma/client|typeorm|sequelize|pg|mysql2|sqlite3|knex)['"]|"""
            r"""require\(\s*['"](?:mongoose|@prisma/client|typeorm|sequelize|pg|mysql2|sqlite3|knex)['"]\s*\))""",
            re.IGNORECASE,
        )
        self.re_orm_imports_py = re.compile(
            r"""(?:from\s+(?:sqlalchemy|motor|tortoise|peewee|django\.db\.models)\b|"""
            r"""import\s+(?:sqlalchemy|motor|tortoise|peewee)\b)""",
            re.IGNORECASE,
        )
        self.re_db_method_calls = re.compile(
            r"""(?:\b(?:prisma\.[a-zA-Z0-9_]+|UserModel|db|pool|session|entityManager)\s*\.)?"""
            r"""\b(?:find|findOne|findMany|findById|create|insert|update|updateOne|updateMany|"""
            r"""delete|deleteOne|deleteMany|query|aggregate|save)\s*\(""",
        )
        self.re_db_python_calls = re.compile(
            r"""\b(?:session|db)\.(?:execute|query|add|commit|rollback)\s*\(|"""
            r"""\b(?:objects|select)\.(?:filter|all|create|get|values|exclude)\s*\(""",
        )

        # Service transport coupling regex patterns
        self.re_service_http_ts = re.compile(
            r"""\b(?:Request|Response|NextFunction|FastifyRequest|FastifyReply)\b|"""
            r"""\b(?:res|reply)\.(?:status|send|json|setHeader)\s*\(|"""
            r"""\bstatus\s*\(\s*(?:200|201|400|401|403|404|409|422|500)\s*\)"""
        )
        self.re_service_http_py = re.compile(
            r"""\b(?:from\s+fastapi\s+import.*(?:Request|Response|HTTPException)|"""
            r"""\b(?:Request|Response)\b\s*[:=]|"""
            r"""\bstatus\.HTTP_\d{3}_)"""
        )
        self.re_service_http_go = re.compile(
            r"""\b(?:http\.ResponseWriter|\*http\.Request|http\.Status[A-Za-z]+)\b"""
        )
        self.re_service_http_java = re.compile(
            r"""\b(?:HttpServletRequest|HttpServletResponse|ResponseEntity|HttpStatus)\b"""
        )

        # Frontend direct network calls regex patterns
        self.re_frontend_fetch = re.compile(r"""\bfetch\s*\(\s*['"`/]""")
        self.re_frontend_axios = re.compile(
            r"""\baxios\.(?:get|post|put|delete|patch|request)\s*\(|\baxios\s*\("""
        )

    def scan(self) -> List[ArchitectureViolation]:
        self.violations.clear()
        for root, dirs, files in os.walk(self.root_dir):
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs and not d.startswith(".")]

            for file in files:
                ext = Path(file).suffix.lower()
                if ext not in VALID_EXTENSIONS:
                    continue

                full_path = Path(root) / file
                rel_path = full_path.relative_to(self.root_dir)
                rel_str = str(rel_path).replace("\\", "/")

                if self._is_test_file(file):
                    continue

                self._check_file(full_path, rel_str)

        return self.violations

    def _is_test_file(self, filename: str) -> bool:
        low = filename.lower()
        return (
            low.endswith(".test.ts")
            or low.endswith(".test.js")
            or low.endswith(".spec.ts")
            or low.endswith(".spec.js")
            or low.endswith("_test.go")
            or low.startswith("test_")
            or low.endswith("_test.py")
        )

    def _check_file(self, full_path: Path, rel_str: str) -> None:
        try:
            with open(full_path, "r", encoding="utf-8", errors="replace") as f:
                lines = f.readlines()
        except Exception as e:
            if self.verbose:
                print(f"Error reading {rel_str}: {e}", file=sys.stderr)
            return

        is_route = self._is_route_file(rel_str)
        is_controller = self._is_controller_file(rel_str)
        is_service = self._is_service_file(rel_str)
        is_frontend = self._is_frontend_file(rel_str)

        for line_no, raw_line in enumerate(lines, start=1):
            line = raw_line.strip()
            if not line or line.startswith("//") or line.startswith("#") or line.startswith("/*"):
                continue

            if "arch-ignore" in line or "no-arch-check" in line:
                continue

            if is_route:
                self._check_route_line(rel_str, line_no, line)
            elif is_controller:
                self._check_controller_line(rel_str, line_no, line)
            elif is_service:
                self._check_service_line(rel_str, line_no, line)
            elif is_frontend:
                self._check_frontend_line(rel_str, line_no, line)

    def _is_route_file(self, rel_str: str) -> bool:
        parts = rel_str.lower().split("/")
        filename = parts[-1]
        if self._is_service_file(rel_str) or self._is_controller_file(rel_str) or "repository" in filename or "repositories" in parts or "model" in filename or "models" in parts:
            return False
        route_dirs = {"routes", "endpoints"}
        in_route_dir = any(p in route_dirs for p in parts[:-1]) or (parts[-2] == "api" if len(parts) >= 2 else False) or "app/api" in rel_str
        has_route_name = "route" in filename or "router" in filename or "endpoint" in filename
        return in_route_dir or has_route_name

    def _is_controller_file(self, rel_str: str) -> bool:
        parts = rel_str.lower().split("/")
        filename = parts[-1]
        ctrl_dirs = {"controllers", "handlers"}
        in_ctrl_dir = any(p in ctrl_dirs for p in parts[:-1])
        has_ctrl_name = "controller" in filename or "handler" in filename
        return in_ctrl_dir or has_ctrl_name

    def _is_service_file(self, rel_str: str) -> bool:
        parts = rel_str.lower().split("/")
        filename = parts[-1]
        srv_dirs = {"services", "use-cases", "usecases"}
        in_srv_dir = any(p in srv_dirs for p in parts[:-1])
        has_srv_name = "service" in filename or "usecase" in filename or "use-case" in filename
        return in_srv_dir or has_srv_name

    def _is_frontend_file(self, rel_str: str) -> bool:
        parts = rel_str.lower().split("/")
        filename = parts[-1]
        # Skip server API routes in Next.js / Nuxt
        if "app/api" in rel_str or "server/api" in rel_str or "pages/api" in rel_str:
            return False
        fe_dirs = {"components", "views", "pages", "widgets", "ui"}
        in_fe_dir = any(p in fe_dirs for p in parts[:-1])
        ext = Path(filename).suffix.lower()
        return in_fe_dir and ext in {".tsx", ".jsx", ".vue", ".svelte"}

    def _check_route_line(self, rel_str: str, line_no: int, line: str) -> None:
        # Check ORM imports
        if self.re_orm_imports_js.search(line) or self.re_orm_imports_py.search(line):
            self.violations.append(
                ArchitectureViolation(
                    rule_id="ARCH-ROUTE-ORM-IMPORT",
                    category="Route Layer Violation",
                    file_path=rel_str,
                    line_number=line_no,
                    line_content=line,
                    message="Direct database or ORM/ODM import inside route/endpoint file.",
                    remediation="Remove database driver/ORM import from route. Delegate handling to a Controller or Service.",
                )
            )

        # Check direct DB calls
        if self.re_db_method_calls.search(line) or self.re_db_python_calls.search(line):
            # Exclude HTTP routing method calls on routers
            if not re.search(r"""\b(?:router|app|[a-zA-Z0-9_]*router)\.(?:use|get|post|put|patch|delete|all|options|head)\s*\(""", line, re.IGNORECASE):
                self.violations.append(
                    ArchitectureViolation(
                        rule_id="ARCH-ROUTE-DB-QUERY",
                        category="Route Layer Violation",
                        file_path=rel_str,
                        line_number=line_no,
                        line_content=line,
                        message="Direct database query or ORM method call inside route/endpoint handler.",
                        remediation="Move database queries into a dedicated Repository. Call the Repository from a Service.",
                    )
                )

    def _check_controller_line(self, rel_str: str, line_no: int, line: str) -> None:
        # Check ORM imports
        if self.re_orm_imports_js.search(line) or self.re_orm_imports_py.search(line):
            self.violations.append(
                ArchitectureViolation(
                    rule_id="ARCH-CTRL-ORM-IMPORT",
                    category="Controller Layer Violation",
                    file_path=rel_str,
                    line_number=line_no,
                    line_content=line,
                    message="Direct database or ORM/ODM import inside controller file.",
                    remediation="Controllers must only invoke domain services. Persistence belongs in repositories.",
                )
            )

        # Check direct DB queries in controllers
        if self.re_db_method_calls.search(line) or self.re_db_python_calls.search(line):
            self.violations.append(
                ArchitectureViolation(
                    rule_id="ARCH-CTRL-DB-QUERY",
                    category="Controller Layer Violation",
                    file_path=rel_str,
                    line_number=line_no,
                    line_content=line,
                    message="Direct database query inside controller.",
                    remediation="Controllers must remain thin adapters. Delegate queries to domain services and repositories.",
                )
            )

    def _check_service_line(self, rel_str: str, line_no: int, line: str) -> None:
        if (
            self.re_service_http_ts.search(line)
            or self.re_service_http_py.search(line)
            or self.re_service_http_go.search(line)
            or self.re_service_http_java.search(line)
        ):
            self.violations.append(
                ArchitectureViolation(
                    rule_id="ARCH-SRV-HTTP-LEAK",
                    category="Service Layer Violation",
                    file_path=rel_str,
                    line_number=line_no,
                    line_content=line,
                    message="HTTP transport object or status code referenced inside domain service.",
                    remediation="Domain services must be transport-agnostic. Move HTTP request/response handling to the controller.",
                )
            )

    def _check_frontend_line(self, rel_str: str, line_no: int, line: str) -> None:
        if self.re_frontend_fetch.search(line):
            self.violations.append(
                ArchitectureViolation(
                    rule_id="ARCH-FE-DIRECT-FETCH",
                    category="Frontend Layer Violation",
                    file_path=rel_str,
                    line_number=line_no,
                    line_content=line,
                    message="Direct fetch() call inside UI component file.",
                    remediation="Extract network request into a dedicated API service (e.g. `services/api/`) and consume via custom hooks.",
                    severity="WARNING",
                )
            )
        elif self.re_frontend_axios.search(line):
            self.violations.append(
                ArchitectureViolation(
                    rule_id="ARCH-FE-DIRECT-AXIOS",
                    category="Frontend Layer Violation",
                    file_path=rel_str,
                    line_number=line_no,
                    line_content=line,
                    message="Direct axios call inside UI component file.",
                    remediation="Move Axios requests into a centralized API service and custom hook.",
                    severity="WARNING",
                )
            )


def format_report_text(violations: List[ArchitectureViolation], root_dir: Path) -> str:
    if not violations:
        return f"{COLOR_BOLD}{COLOR_GREEN}✓ Architecture Integrity Check Passed:{COLOR_RESET} Zero layer boundary violations found."

    lines = [
        f"{COLOR_BOLD}{COLOR_RED}✗ Architecture Integrity Check Failed:{COLOR_RESET} Found {len(violations)} layer violation(s).\n"
    ]

    for v in violations:
        color = COLOR_RED if v.severity == "ERROR" else COLOR_YELLOW
        lines.append(f"{COLOR_BOLD}{color}[{v.rule_id}] {v.category} ({v.severity}){COLOR_RESET}")
        lines.append(f"  {COLOR_CYAN}File:{COLOR_RESET} {v.file_path}:{v.line_number}")
        lines.append(f"  {COLOR_CYAN}Code:{COLOR_RESET} {v.line_content}")
        lines.append(f"  {COLOR_CYAN}Issue:{COLOR_RESET} {v.message}")
        lines.append(f"  {COLOR_CYAN}Fix:{COLOR_RESET} {v.remediation}\n")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Automated Static Architecture Linter (RULE-ARCH-LAYER-001)"
    )
    parser.add_argument(
        "--root",
        type=str,
        default=None,
        help="Root directory of the project to scan. If omitted, auto-detect the workspace root.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        default=False,
        help="Treat architecture warnings as errors; use when the project explicitly adopts strict boundary enforcement.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print verbose diagnostic information",
    )

    args = parser.parse_args()

    if args.root:
        root_path = Path(args.root).resolve()
    else:
        cwd = Path.cwd().resolve()
        package_workspace = Path(__file__).resolve().parents[2]
        candidates = [cwd, cwd / "workspace-template", package_workspace]
        root_path = next((candidate for candidate in candidates if (candidate / ".agents").is_dir()), cwd)

    if not root_path.exists():
        print(f"Error: Path {root_path} does not exist.", file=sys.stderr)
        return 2

    checker = ArchitectureChecker(root_dir=root_path, verbose=args.verbose)
    violations = checker.scan()

    errors = [v for v in violations if v.severity == "ERROR"]
    warnings = [v for v in violations if v.severity == "WARNING"]

    if args.json:
        result = {
            "root": str(root_path),
            "passed": len(violations) == 0 or (not args.strict and len(errors) == 0),
            "total_violations": len(violations),
            "errors": len(errors),
            "warnings": len(warnings),
            "violations": [asdict(v) for v in violations],
        }
        print(json.dumps(result, indent=2))
    else:
        print(format_report_text(violations, root_path))

    if len(errors) > 0 or (args.strict and len(warnings) > 0):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
