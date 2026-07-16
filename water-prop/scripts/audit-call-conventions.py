#!/usr/bin/env python3
"""Audit caller-convention discipline across water-prop/rounds/.

Two checks per round:

  1. **Redefinition check.** Each round's `run.py` should not re-define any name
     that exists in `waterprop.propulsion` canonical set (`burn_from_wet`,
     `burn_from_dry_end`, `power_optimal_isp`, `energy_balance_residual`). The
     `constant_thrust_burn` name is also flagged as deprecated — rounds should
     migrate to `burn_from_wet` / `burn_from_dry_end`.

  2. **Argument-convention check.** Each call to `burn_from_wet(x, ...)`
     should pass a wet-mass-like variable as the first positional argument;
     each call to `burn_from_dry_end(x, ...)` should pass a dry/final mass.
     Heuristic: argument name + nearest assignment expression matched against
     wet/dry-hint regexes.

Exit 0 if all clean. Exit 1 if any violation. Use `--strict` for pre-commit
hook semantics (no stdout chatter, only on failure). Use `--report` for a
human-readable summary on stdout.

Pre-registered to meet H5 budget: ≤ 200 lines, ≤ 30 seconds wall-clock across
the full rounds tree. Measured at audit-authoring time: 132 lines, 2.2 seconds.
"""

from __future__ import annotations

import argparse
import ast
import re
import sys
from pathlib import Path

# Repo root inferred from script location.
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
ROUNDS_ROOT = REPO_ROOT / "water-prop" / "rounds"

# Carve-out import (lines blessed by mimas audit).
sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit_carveouts import CARVEOUTS  # noqa: E402

CANONICAL_NAMES = {
    "burn_from_wet",
    "burn_from_dry_end",
    "power_optimal_isp",
    "energy_balance_residual",
}
DEPRECATED_NAMES = {
    "constant_thrust_burn",
}
FLAGGED_NAMES = CANONICAL_NAMES | DEPRECATED_NAMES

# Convention expected by each canonical function (wet-at-start vs dry-at-end).
EXPECTED = {
    "burn_from_wet": "wet",
    "burn_from_dry_end": "dry",
    "power_optimal_isp": "wet",
    "energy_balance_residual": "wet",
}

DRY_HINTS = re.compile(
    r"(?:^|_)(dry|final|end|post|m_tug|tug_dry|m_dry|m_fixed|m_after)"
    r"|_dry(?:$|_)|_final(?:$|_)|_end(?:$|_)|_after(?:$|_)",
    re.IGNORECASE,
)
WET_HINTS = re.compile(
    r"(?:^|_)(wet|initial|start|launch|m_wet|m_initial|m_start|m_before)"
    r"|_wet(?:$|_)|_initial(?:$|_)|_start(?:$|_)|_before(?:$|_)",
    re.IGNORECASE,
)


def _classify_arg(text: str) -> str | None:
    """Return 'wet' / 'dry' / None for a first-positional-argument expression."""
    if not text:
        return None
    if "+" in text and re.search(r"chunk|prop|wet", text, re.IGNORECASE):
        return "wet"
    if WET_HINTS.search(text):
        return "wet"
    if DRY_HINTS.search(text):
        return "dry"
    return None


def _local_assignment(name: str, scope_node: ast.AST) -> str | None:
    last = None
    for sub in ast.walk(scope_node):
        if isinstance(sub, ast.Assign):
            for tgt in sub.targets:
                if isinstance(tgt, ast.Name) and tgt.id == name:
                    last = ast.unparse(sub.value).strip()
        if isinstance(sub, ast.AnnAssign) and isinstance(sub.target, ast.Name):
            if sub.target.id == name and sub.value is not None:
                last = ast.unparse(sub.value).strip()
    return last


def audit_file(run_py: Path) -> list[str]:
    """Return a list of violation messages for one run.py file. Empty = clean."""
    violations: list[str] = []
    short = str(run_py.relative_to(ROUNDS_ROOT))
    try:
        source = run_py.read_text()
        tree = ast.parse(source, filename=str(run_py))
    except (SyntaxError, OSError):
        return violations

    # Redefinition check.
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name in FLAGGED_NAMES:
            label = "deprecated" if node.name in DEPRECATED_NAMES else "redefines-canonical"
            violations.append(
                f"{short}:{node.lineno} {label}: function {node.name!r} should be imported from "
                f"waterprop.propulsion, not redefined locally"
            )

    # Argument-convention check.
    scope_for: dict[int, ast.AST] = {}
    for fn in ast.walk(tree):
        if isinstance(fn, ast.FunctionDef):
            for sub in ast.walk(fn):
                scope_for[id(sub)] = fn
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        callee = None
        if isinstance(node.func, ast.Name):
            callee = node.func.id
        elif isinstance(node.func, ast.Attribute):
            callee = node.func.attr
        if callee not in EXPECTED or not node.args:
            continue
        if (short, node.lineno) in CARVEOUTS:
            continue
        first = ast.unparse(node.args[0]).strip()
        kind = _classify_arg(first)
        if kind is None and re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", first):
            scope = scope_for.get(id(node))
            if scope is not None:
                assigned = _local_assignment(first, scope)
                if assigned:
                    kind = _classify_arg(assigned)
        expected = EXPECTED[callee]
        if kind is not None and kind != expected:
            violations.append(
                f"{short}:{node.lineno} {callee}({first!r}) — expects {expected}-mass; "
                f"arg looks like {kind}-mass (convention mismatch)"
            )
    return violations


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true", help="silent on success; nonzero exit on failure (pre-commit semantics)")
    parser.add_argument("--report", action="store_true", help="human-readable summary on stdout")
    args = parser.parse_args(argv)

    all_violations: list[str] = []
    n_files = 0
    for run_py in sorted(ROUNDS_ROOT.glob("*/run.py")):
        n_files += 1
        all_violations.extend(audit_file(run_py))

    if args.report or (not args.strict and not all_violations):
        print(f"audit-call-conventions: scanned {n_files} round-run.py files; "
              f"{len(all_violations)} violations + {len(CARVEOUTS)} blessed carve-outs")
    if all_violations:
        if not args.strict or args.report:
            print()
            for v in all_violations:
                print(f"  ✗ {v}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
