"""R-shared-physics-audit — static analysis of function-convention contamination.

Pre-registered hypotheses in STUDY.md. This script does the mechanical work:

  Step 1: catalogue shared-library functions in water-prop/src/waterprop/
  Step 2: catalogue round-local convention-bearing functions in water-prop/rounds/*/run.py
  Step 3: build the call graph (every flagged-function call site, with argument expressions)
  Step 4: per-call-site convention-correctness heuristic verdict
  Step 5: tier rounds A/B/C against design-axes/INDEX.md status
  Step 6: emit contamination_matrix.csv + per-hypothesis JSON used by results/H1..H6.md

Run from the repository root:
    PYTHONPATH=water-prop/src python water-prop/rounds/R_shared_physics_audit/run.py

The script is intentionally read-only: it does not modify any other round's files.
The library hardening patch is a separate deliverable applied directly to water-prop/src/.
"""

from __future__ import annotations

import ast
import csv
import dataclasses
import json
import re
from pathlib import Path

ROUND_DIR = Path(__file__).resolve().parent
REPO_ROOT = ROUND_DIR.parent.parent.parent
WATERPROP_SRC = REPO_ROOT / "water-prop" / "src" / "waterprop"
ROUNDS_ROOT = REPO_ROOT / "water-prop" / "rounds"
DESIGN_AXES = REPO_ROOT / "design-axes"
MATRIX_DOC = REPO_ROOT / "water-prop" / "docs" / "ARCHITECTURE-DECISION-MATRIX.md"
RESULTS = ROUND_DIR / "results"
RESULTS.mkdir(exist_ok=True)

# Seed list of function names that have been independently surfaced as convention-bearing
# (PROTOCOL methodology lesson 6 + SCOPE.md). Not exhaustive — the audit also flags any
# additional function whose signature matches the (mass, dv, power, isp) convention pattern.
SEED_FUNCTIONS = {
    "constant_thrust_burn",
    "edelbaum_spiral",
    "edelbaum_spiral_dv_km_s",
    "spiral_burn",
    "burn_from_wet",
    "burn_from_dry_end",
    "impulsive_burn",
}

# Argument-name regex hints used by the convention-correctness heuristic. Variables whose
# names match a "dry" or "final" pattern are evidence the caller is passing post-burn mass;
# variables whose names match a "wet" or "initial" or "+ chunk" pattern are evidence of
# pre-burn mass. The heuristic is purposefully conservative: anything not matching is
# tagged ambiguous.
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


@dataclasses.dataclass
class LibraryFunction:
    module: str
    name: str
    line: int
    signature: list[str]
    docstring_first_line: str
    convention_class: str  # "mass_convention" | "unit_convention" | "none"


@dataclasses.dataclass
class RoundLocalDef:
    round_name: str
    file: str
    line: int
    name: str
    signature: list[str]
    formula_variant: str  # "wet_at_start" | "dry_at_end" | "other"
    propellant_formula: str  # the m_prop expression as source text
    docstring_first_line: str


@dataclasses.dataclass
class CallSite:
    round_name: str
    file: str
    line: int
    callee: str
    args_text: list[str]
    first_positional: str | None
    convention_verdict: str  # "correct" | "incorrect" | "ambiguous" | "n/a"
    notes: str


# ---------------------------------------------------------------------------
# Step 1: catalogue shared-library functions
# ---------------------------------------------------------------------------


def _arg_names(args: ast.arguments) -> list[str]:
    parts = []
    for a in args.args:
        parts.append(a.arg if a.annotation is None else f"{a.arg}: {ast.unparse(a.annotation)}")
    return parts


def _classify_convention(name: str, sig: list[str], doc: str) -> str:
    sig_text = " ".join(sig)
    body = (doc or "").lower()
    if re.search(r"\bm_initial|m_final|m_dry|m_wet|mass.+kg|mass.+_t\b", sig_text, re.IGNORECASE):
        return "mass_convention"
    if "delta_v" in sig_text.lower() or "dv_" in sig_text.lower() or "isp" in sig_text.lower():
        return "unit_convention"
    if "mass" in body and ("initial" in body or "final" in body or "wet" in body or "dry" in body):
        return "mass_convention"
    return "none"


def catalogue_library() -> list[LibraryFunction]:
    out: list[LibraryFunction] = []
    for py in sorted(WATERPROP_SRC.rglob("*.py")):
        if py.name == "__init__.py":
            continue
        module = py.relative_to(WATERPROP_SRC).with_suffix("").as_posix().replace("/", ".")
        tree = ast.parse(py.read_text(), filename=str(py))
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                doc = ast.get_docstring(node) or ""
                sig = _arg_names(node.args)
                out.append(
                    LibraryFunction(
                        module=module,
                        name=node.name,
                        line=node.lineno,
                        signature=sig,
                        docstring_first_line=doc.split("\n", 1)[0].strip(),
                        convention_class=_classify_convention(node.name, sig, doc),
                    )
                )
    return out


# ---------------------------------------------------------------------------
# Step 2: catalogue round-local definitions of seed-list-named functions
# ---------------------------------------------------------------------------


def _formula_variant(node: ast.FunctionDef, source_lines: list[str]) -> tuple[str, str]:
    """Inspect a constant_thrust_burn-shaped function and decide whether its m_prop
    formula treats m_initial_t as wet-at-start or dry-at-end mass.

    Returns (variant_label, formula_source_text).
    """
    formula_src = ""
    for sub in ast.walk(node):
        if isinstance(sub, ast.Assign):
            targets_text = ", ".join(ast.unparse(t) for t in sub.targets)
            if "m_prop" in targets_text:
                formula_src = ast.unparse(sub.value).strip()
                break
    if not formula_src:
        return ("other", "")
    # Heuristic regex on the unparsed expression. Match integer and float literals.
    # wet_at_start: m_initial * (1 - 1/MR)  or  m_initial * (1 - exp(-...))
    # dry_at_end : m_initial * (MR - 1)
    src = formula_src
    if re.search(r"1(?:\.0+)?\s*-\s*1(?:\.0+)?\s*/", src):
        return ("wet_at_start", formula_src)
    if re.search(r"(?:mass_ratio|MR|\)\s*)\s*-\s*1(?:\.0+)?\b", src):
        return ("dry_at_end", formula_src)
    if "exp(-" in src and re.search(r"1(?:\.0+)?\s*-\s*", src):
        return ("wet_at_start", formula_src)
    if "exp(" in src and re.search(r"-\s*1(?:\.0+)?\b", src) and "1 -" not in src:
        return ("dry_at_end", formula_src)
    return ("other", formula_src)


def catalogue_round_local_defs() -> list[RoundLocalDef]:
    out: list[RoundLocalDef] = []
    for run_py in sorted(ROUNDS_ROOT.glob("*/run.py")):
        round_name = run_py.parent.name
        try:
            source = run_py.read_text()
            tree = ast.parse(source, filename=str(run_py))
        except SyntaxError:
            continue
        source_lines = source.splitlines()
        for node in ast.walk(tree):
            if not isinstance(node, ast.FunctionDef):
                continue
            if node.name not in SEED_FUNCTIONS:
                continue
            sig = _arg_names(node.args)
            doc = ast.get_docstring(node) or ""
            variant, formula = _formula_variant(node, source_lines)
            out.append(
                RoundLocalDef(
                    round_name=round_name,
                    file=str(run_py.relative_to(REPO_ROOT)),
                    line=node.lineno,
                    name=node.name,
                    signature=sig,
                    formula_variant=variant,
                    propellant_formula=formula,
                    docstring_first_line=doc.split("\n", 1)[0].strip(),
                )
            )
    return out


# ---------------------------------------------------------------------------
# Step 3: build the call graph
# ---------------------------------------------------------------------------


def _imports_waterprop(tree: ast.Module) -> bool:
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(a.name.startswith("waterprop") for a in node.names):
                return True
        if isinstance(node, ast.ImportFrom):
            if (node.module or "").startswith("waterprop"):
                return True
    return False


def _local_assignment_for(name: str, scope_node: ast.AST) -> str | None:
    """Walk a function body to find the most recent assignment expression for `name`."""
    last = None
    for sub in ast.walk(scope_node):
        if isinstance(sub, ast.Assign):
            for tgt in sub.targets:
                if isinstance(tgt, ast.Name) and tgt.id == name:
                    last = ast.unparse(sub.value).strip()
        if isinstance(sub, ast.AnnAssign) and isinstance(sub.target, ast.Name) and sub.target.id == name:
            if sub.value is not None:
                last = ast.unparse(sub.value).strip()
    return last


# Manual carve-outs for intentional bug reproductions and known false positives.
# Each entry: (file_suffix, line, reason). These call sites are marked correct-intentional
# in the verdict rather than incorrect, because reading the surrounding code shows the
# call is deliberately demonstrating the bug pattern (unit-sanity-check inside the rerun
# round) or the heuristic mis-classified a wet-mass variable whose name accidentally
# matches a dry-hint regex. Findings documented in READING.md.
INTENTIONAL_OR_FALSE_POSITIVE = {
    ("R_electric_outbound_rerun/run.py", 195): "unit_sanity_check intentionally calls burn_from_wet(m_final) to demonstrate the bugged pattern",
    ("R_electric_outbound_rerun/run.py", 225): "round_trip reproduces the bugged call under use_bugged_outbound=True flag (documented at line 213-220)",
    ("R_electric_outbound_rerun/run.py", 234): "round_trip reproduces the bugged call under use_bugged_outbound=True flag (documented at line 213-220)",
    ("R_redundancy_budget_cost/run.py", 222): "m_after_kick is wet-at-start-of-electric-burn (m_initial_inbound / math.exp(...) is Tsiolkovsky-after-kick); the variable name 'after_kick' trips the dry-hint regex but the semantic is wet-at-start-of-next-burn",
}


def _convention_verdict(callee: str, first_arg_text: str, local_def_lookup: dict[str, RoundLocalDef], context_scope: ast.AST | None, round_name: str) -> tuple[str, str]:
    """Heuristic convention-correctness for a call site.

    Returns (verdict, notes).
    """
    # If we know the local-redefinition's formula variant, decide based on
    # whether the first positional argument's name (or assigned expression)
    # matches that variant's expected convention.
    key = (round_name, callee)
    rdef = local_def_lookup.get(key)
    notes_parts = []
    if rdef is None:
        # Calling a shared-library function or a function defined elsewhere.
        # Library functions classified as mass_convention expect wet-at-start (verified manually).
        if callee in {"power_optimal_isp", "energy_balance_residual"}:
            # Expected convention: wet-at-start.
            expects = "wet_at_start"
        else:
            return ("n/a", "callee not in flagged set or convention not classified")
    else:
        expects = rdef.formula_variant
        notes_parts.append(f"local def at {rdef.file}:{rdef.line} variant={expects}")

    # Decide what the call site is passing.
    arg_text = first_arg_text or ""
    # First, look for compound expressions (e.g. m_tug + chunk_t) — these are
    # typically wet-mass-at-start assemblies.
    if "+" in arg_text and re.search(r"chunk|prop|wet", arg_text, re.IGNORECASE):
        observed = "wet_at_start"
        notes_parts.append("arg is a sum suggesting wet-mass assembly")
    elif WET_HINTS.search(arg_text):
        observed = "wet_at_start"
        notes_parts.append(f"arg name matches wet-hints: {arg_text!r}")
    elif DRY_HINTS.search(arg_text):
        observed = "dry_at_end"
        notes_parts.append(f"arg name matches dry-hints: {arg_text!r}")
    elif context_scope is not None and re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", arg_text):
        # Trace back the local assignment.
        assigned = _local_assignment_for(arg_text, context_scope)
        if assigned is None:
            return ("ambiguous", "; ".join(notes_parts + [f"arg {arg_text!r} not assigned in scope"]))
        if WET_HINTS.search(assigned) or ("+" in assigned and re.search(r"chunk|prop|wet", assigned, re.IGNORECASE)):
            observed = "wet_at_start"
            notes_parts.append(f"arg {arg_text!r} assigned from {assigned!r}")
        elif DRY_HINTS.search(assigned):
            observed = "dry_at_end"
            notes_parts.append(f"arg {arg_text!r} assigned from {assigned!r} (dry-hint)")
        else:
            return ("ambiguous", "; ".join(notes_parts + [f"arg {arg_text!r} assignment {assigned!r} ambiguous"]))
    else:
        return ("ambiguous", "; ".join(notes_parts + [f"arg text {arg_text!r} not classifiable"]))

    if expects == observed:
        return ("correct", "; ".join(notes_parts + [f"expects={expects} observed={observed}"]))
    if expects in {"wet_at_start", "dry_at_end"} and observed in {"wet_at_start", "dry_at_end"}:
        return ("incorrect", "; ".join(notes_parts + [f"expects={expects} observed={observed} — CONVENTION MISMATCH"]))
    return ("ambiguous", "; ".join(notes_parts + [f"expects={expects} observed={observed}"]))


def build_call_graph(local_defs: list[RoundLocalDef]) -> list[CallSite]:
    local_def_lookup = {(d.round_name, d.name): d for d in local_defs}
    out: list[CallSite] = []
    for run_py in sorted(ROUNDS_ROOT.glob("*/run.py")):
        round_name = run_py.parent.name
        try:
            source = run_py.read_text()
            tree = ast.parse(source, filename=str(run_py))
        except SyntaxError:
            continue
        # Build map of function-scope nodes for local-assignment trace.
        scope_for = {}
        for fn in ast.walk(tree):
            if isinstance(fn, ast.FunctionDef):
                for sub in ast.walk(fn):
                    scope_for[id(sub)] = fn

        for call in ast.walk(tree):
            if not isinstance(call, ast.Call):
                continue
            if isinstance(call.func, ast.Name):
                callee = call.func.id
            elif isinstance(call.func, ast.Attribute):
                callee = call.func.attr
            else:
                continue
            if callee not in SEED_FUNCTIONS and callee not in {
                "power_optimal_isp", "energy_balance_residual",
            }:
                continue
            args_text = [ast.unparse(a) for a in call.args]
            first_pos = args_text[0] if args_text else None
            scope = scope_for.get(id(call))
            verdict, notes = _convention_verdict(callee, first_pos or "", local_def_lookup, scope, round_name)
            # Apply manual carve-outs (intentional bugged-call reproductions, false positives).
            file_rel = str(run_py.relative_to(REPO_ROOT))
            short = file_rel.split("water-prop/rounds/")[-1]
            carve = INTENTIONAL_OR_FALSE_POSITIVE.get((short, call.lineno))
            if carve and verdict == "incorrect":
                verdict = "intentional"
                notes = f"manual-carveout: {carve}"
            out.append(
                CallSite(
                    round_name=round_name,
                    file=file_rel,
                    line=call.lineno,
                    callee=callee,
                    args_text=args_text,
                    first_positional=first_pos,
                    convention_verdict=verdict,
                    notes=notes,
                )
            )
    return out


# ---------------------------------------------------------------------------
# Step 5: tier rounds against design-axes status
# ---------------------------------------------------------------------------


# From design-axes/INDEX.md at last_revised 2026-05-19 (latest+13).
AXIS_STATUS = {
    "01": "open",       "02": "open",       "03": "closed",
    "04": "closed",     "05": "open",       "06": "closed",
    "07": "closed",     "08": "open",       "09": "open",
    "10": "open",       "11": "falsified",  "12": "falsified",
    "13": "open",       "14": "open",       "15": "closed",
    "16": "open",       "17": "open",       "18": "closed",
    "19": "falsified",  "20": "open",
}


def find_supported_axes(round_name: str) -> list[tuple[str, str]]:
    """Grep design-axes/*.md + matrix HISTORY for the round name.

    Returns a list of (axis_number, status) tuples for axes that reference the round.
    """
    out: list[tuple[str, str]] = []
    candidates = []
    if DESIGN_AXES.exists():
        candidates.extend(sorted(DESIGN_AXES.glob("*.md")))
    if MATRIX_DOC.exists():
        candidates.append(MATRIX_DOC)
    # Round names vary in formatting (R_x vs R-x); search for both.
    needles = {round_name, round_name.replace("_", "-")}
    seen_axes = set()
    for path in candidates:
        text = path.read_text()
        if any(n in text for n in needles):
            m = re.match(r"(\d{2})-", path.name)
            if m:
                axis = m.group(1)
                if axis in seen_axes:
                    continue
                seen_axes.add(axis)
                out.append((axis, AXIS_STATUS.get(axis, "unknown")))
            else:
                # Matrix doc — record as 'matrix' but no axis number.
                out.append(("matrix", "see-history"))
    return out


# Manual tier overrides for rounds with incorrect call sites.
# Mimas hand-tiered against the latest+13 axis state (design-axes/INDEX.md last_revised
# 2026-05-19) plus the project-owner directive retiring 500 kilowatt-electric. Each entry
# names the supported axis/cell, the live status, and the resulting tier. Documented in
# READING.md "Tier-A re-run dispatch" and "Tier-B/C audit-trail cleanup".
MANUAL_TIER_OVERRIDES = {
    "R_electric_outbound": (
        "B",
        "anchors axis 02 (surviving cell, open) and axis 13 (outbound launch architecture, open) BUT has already been "
        "SUPERSEDED by R_electric_outbound_rerun (rhea, integrated 2026-05-15 evening). The corrected outbound burn "
        "time + the titan-inbound delta-velocity correction together retracted the bugged headline. No live re-run "
        "needed — the load-bearing fix is already in main.",
    ),
    "R_megawatt_architecture_viability": (
        "B",
        "anchors axis 02 (surviving cell, open) and axis 05 (reactor power floor, open-but-amended). The round's "
        "headline cell is megawatt-class architecture closure. Per project-owner directive 2026-05-19 latest+13 retiring "
        "500 kilowatt-electric (locked memory feedback_no_large_fission.md), the megawatt cell this round supports is "
        "now dead by directive. Re-running the round would correct burn time but not rescue a live verdict — closure "
        "cell at latest+13 is the titan-3 40-80 tonne / 30 kilowatt-electric cell, which this round does not touch.",
    ),
    "R_redundancy_budget_cost": (
        "B",
        "anchors axis 15 (per-mission reliability, CLOSED) — the round's per-vehicle redundancy-overlay cost "
        "($565M-$710M) is its load-bearing finding, not the outbound burn time. The bugged call site at line 226 is "
        "inside the inbound_chunkfed=False branch (all-electric outbound, no chunk), which contributes to round-trip "
        "time but not to the cost finding. Cost is invariant under burn-time correction. Re-running would clean up the "
        "round-trip number for an axis that is closed; the headline reliability/cost finding stands.",
    ),
}


def tier_round(round_name: str, has_incorrect_call: bool, supported_axes: list[tuple[str, str]]) -> str:
    if not has_incorrect_call:
        return "—"
    if round_name in MANUAL_TIER_OVERRIDES:
        return MANUAL_TIER_OVERRIDES[round_name][0]
    statuses = {status for ax, status in supported_axes if ax != "matrix"}
    if not statuses:
        return "C"  # not referenced by any design axis (matrix reference alone insufficient)
    if "open" in statuses:
        return "A"
    if statuses <= {"closed", "falsified", "see-history"}:
        return "B"
    return "C"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> dict:
    library = catalogue_library()
    local_defs = catalogue_round_local_defs()
    call_sites = build_call_graph(local_defs)

    # Group call sites by round + decide round-level verdict.
    rounds_with_calls: dict[str, list[CallSite]] = {}
    for cs in call_sites:
        rounds_with_calls.setdefault(cs.round_name, []).append(cs)

    contamination_rows = []
    for round_name in sorted(rounds_with_calls.keys()):
        sites = rounds_with_calls[round_name]
        verdicts = [s.convention_verdict for s in sites]
        has_incorrect = "incorrect" in verdicts
        has_ambiguous = "ambiguous" in verdicts
        supported = find_supported_axes(round_name)
        tier = tier_round(round_name, has_incorrect, supported)
        rationale = MANUAL_TIER_OVERRIDES.get(round_name, ("", ""))[1]
        contamination_rows.append({
            "round": round_name,
            "n_call_sites": len(sites),
            "callees": "|".join(sorted({s.callee for s in sites})),
            "verdicts": "|".join(sorted(set(verdicts))),
            "has_incorrect": has_incorrect,
            "has_ambiguous": has_ambiguous,
            "supported_axes": "|".join(f"{ax}({st})" for ax, st in supported) or "none",
            "tier": tier,
            "tier_rationale": rationale,
        })

    # Emit JSON artifacts.
    (RESULTS / "library_functions.json").write_text(
        json.dumps([dataclasses.asdict(x) for x in library], indent=2)
    )
    (RESULTS / "round_local_defs.json").write_text(
        json.dumps([dataclasses.asdict(x) for x in local_defs], indent=2)
    )
    (RESULTS / "call_sites.json").write_text(
        json.dumps([dataclasses.asdict(x) for x in call_sites], indent=2)
    )

    # Emit contamination_matrix.csv.
    csv_path = ROUND_DIR / "contamination_matrix.csv"
    with csv_path.open("w", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "round", "n_call_sites", "callees", "verdicts",
                "has_incorrect", "has_ambiguous", "supported_axes", "tier", "tier_rationale",
            ],
        )
        writer.writeheader()
        writer.writerows(contamination_rows)

    # Summary statistics for hypothesis adjudication.
    n_rounds_with_calls = len(rounds_with_calls)
    n_with_incorrect = sum(1 for r in contamination_rows if r["has_incorrect"])
    n_with_ambiguous = sum(1 for r in contamination_rows if r["has_ambiguous"])
    n_tier_a = sum(1 for r in contamination_rows if r["tier"] == "A")
    n_tier_b = sum(1 for r in contamination_rows if r["tier"] == "B")
    n_tier_c = sum(1 for r in contamination_rows if r["tier"] == "C")
    total_rounds = sum(1 for _ in ROUNDS_ROOT.glob("*/run.py"))

    summary = {
        "total_round_directories": total_rounds,
        "rounds_that_call_flagged_functions": n_rounds_with_calls,
        "rounds_with_incorrect_call_site": n_with_incorrect,
        "rounds_with_ambiguous_call_site": n_with_ambiguous,
        "tier_a_count": n_tier_a,
        "tier_b_count": n_tier_b,
        "tier_c_count": n_tier_c,
        "library_functions_catalogued": len(library),
        "round_local_definitions_found": len(local_defs),
        "total_call_sites": len(call_sites),
        "seed_function_redefinitions": {
            name: sum(1 for d in local_defs if d.name == name) for name in sorted(SEED_FUNCTIONS)
        },
        "formula_variants": {
            v: sum(1 for d in local_defs if d.formula_variant == v)
            for v in {"wet_at_start", "dry_at_end", "other"}
        },
    }
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == "__main__":
    main()
