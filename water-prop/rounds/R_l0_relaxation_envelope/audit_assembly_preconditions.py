"""Assembly-precondition audit (rhea-5 work order, dispatched 2026-05-26).

Question (Saturn orchestrator, latest+25): 180 of 1744 paths in the
saturn_water_v1 closed-loop closure sweep die at P0b_assembly, split 90/90
between "passthrough cannot run with pending-assembly flag" and "depot-relay
requires existing_leo_depot". Is the multi-launch -> assembly option wiring a
walker pairing bug that silently kills viable mission designs, or honest
precondition rejections produced by exhaustive enumeration?

Decision rule (pre-registered in the work order):
  BUG      -> some multi-launch path prefix that reaches P0b has NO sibling
              branch that continues through autonomous_assembly, i.e. real
              mission designs are lost at P0b.
  NO BUG   -> every multi-launch prefix that reaches P0b continues through
              autonomous_assembly and dies (or survives) downstream; the 180
              records are bookkeeping stubs of the open enumeration, not
              lost designs.

Run from project root:
  python3 water-prop/rounds/R_l0_relaxation_envelope/audit_assembly_preconditions.py

Writes results/audit_assembly_preconditions.json (small; results/ is not
committed per project rules — the memo carries the numbers).
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path


def _ensure_import_path():
    here = Path(__file__).resolve()
    sims_dir = here.parents[2] / "sims"
    if str(sims_dir) not in sys.path:
        sys.path.insert(0, str(sims_dir))
    sweeps_dir = sims_dir / "mission_graph" / "missions" / "sweeps"
    if str(sweeps_dir) not in sys.path:
        sys.path.insert(0, str(sweeps_dir))


_ensure_import_path()

from saturn_water_v1_closure_sweep import base_params, run_closed_loop  # noqa: E402


MULTI_LAUNCH_IDS = ("multi_falcon_2_launch", "multi_falcon_4_launch", "multi_falcon_6_launch")
SINGLE_LAUNCH_IDS = ("falcon_heavy_expended", "starship")


def _option_id(node_label: str) -> str:
    # node_label format: "{phase_id}.{option_id}.{params_hash}" (framework/labels.py)
    return node_label.split(".")[1]


def main():
    print("Running saturn_water_v1 closed-loop sweep (150 cells)...")
    cells = run_closed_loop()

    bp = base_params()
    print(f"  base params carry existing_leo_depot: {('existing_leo_depot' in bp)!s}")

    total_results = 0
    fail_by_phase = Counter()
    fail_reasons_p0b = Counter()
    leaf_count = 0

    # Verdict bookkeeping
    p0b_fail_prefixes = set()          # (cell_id, P0 option id) that produced a P0b stub
    p0b_fail_count_by_prefix = Counter()
    continuations = defaultdict(list)  # (cell_id, P0 option id) -> results that passed P0b
    single_launch_p0b_fails = 0

    for cell in cells:
        if cell.skipped_reason is not None:
            continue
        for r in cell.results:
            total_results += 1
            if r.is_feasible:
                leaf_count += 1
            else:
                fail_by_phase[r.infeasible_at] += 1

            p0_opt = _option_id(r.node_labels[0]) if r.node_labels else "?"
            key = (cell.cell_id, p0_opt)

            if r.infeasible_at == "P0b_assembly":
                fail_reasons_p0b[r.infeasible_reason] += 1
                if p0_opt in MULTI_LAUNCH_IDS:
                    p0b_fail_prefixes.add(key)
                    p0b_fail_count_by_prefix[key] += 1
                elif p0_opt in SINGLE_LAUNCH_IDS:
                    single_launch_p0b_fails += 1
            elif len(r.node_labels) >= 2 and _option_id(r.node_labels[1]) == "autonomous_assembly":
                # Passed P0b via autonomous assembly; record where it ended up.
                continuations[key].append(r)

    print(f"\ntotal enumerated results: {total_results}")
    print(f"feasible leaves: {leaf_count}")
    print("failures by phase:")
    for phase, n in fail_by_phase.most_common():
        print(f"  {phase:>22s}: {n}")
    print("P0b failure reasons:")
    for reason, n in fail_reasons_p0b.most_common():
        print(f"  [{n}] {reason}")

    # Core check: every multi-launch prefix with a P0b stub must have a
    # continuing autonomous_assembly sibling.
    orphaned = sorted(k for k in p0b_fail_prefixes if not continuations.get(k))
    print(f"\nmulti-launch prefixes that reached P0b: {len(p0b_fail_prefixes)}")
    print(f"  P0b stub records they generated: {sum(p0b_fail_count_by_prefix.values())}")
    print(f"  stubs per prefix (should be exactly 2 = passthrough + depot_relay): "
          f"{sorted(set(p0b_fail_count_by_prefix.values()))}")
    print(f"  prefixes WITHOUT an autonomous_assembly continuation (bug if > 0): {len(orphaned)}")
    if orphaned:
        for k in orphaned[:10]:
            print(f"    ORPHANED: cell {k[0]}, P0 option {k[1]}")
    print(f"single-launch P0b stub failures (expect 0 if no single launch survives P0): "
          f"{single_launch_p0b_fails}")

    # Where do the autonomous continuations end?
    downstream = Counter()
    downstream_reasons = Counter()
    for results in continuations.values():
        for r in results:
            if r.is_feasible:
                downstream["LEAF (all phases done, judged by closure predicates)"] += 1
            else:
                downstream[r.infeasible_at] += 1
                downstream_reasons[(r.infeasible_at, r.infeasible_reason)] += 1
    print("\nwhere autonomous-assembly continuations terminate:")
    for where, n in downstream.most_common():
        print(f"  {where:>55s}: {n}")
    print("top downstream failure reasons:")
    for (phase, reason), n in downstream_reasons.most_common(8):
        print(f"  [{n}] {phase}: {reason}")

    verdict = "NO_BUG_HONEST_ENUMERATION" if not orphaned and single_launch_p0b_fails == 0 else (
        "NO_BUG_BUT_SINGLE_LAUNCH_STUBS" if not orphaned else "BUG_ORPHANED_PREFIXES"
    )
    print(f"\nVERDICT: {verdict}")

    out = Path(__file__).parent / "results"
    out.mkdir(exist_ok=True)
    (out / "audit_assembly_preconditions.json").write_text(json.dumps({
        "total_enumerated_results": total_results,
        "feasible_leaves": leaf_count,
        "failures_by_phase": dict(fail_by_phase),
        "p0b_failure_reasons": {k: v for k, v in fail_reasons_p0b.items()},
        "multi_launch_prefixes_at_p0b": len(p0b_fail_prefixes),
        "p0b_stub_records": sum(p0b_fail_count_by_prefix.values()),
        "orphaned_prefixes": [list(k) for k in orphaned],
        "single_launch_p0b_fails": single_launch_p0b_fails,
        "autonomous_continuation_terminations": dict(downstream),
        "verdict": verdict,
    }, indent=2))
    print(f"wrote {out / 'audit_assembly_preconditions.json'}")


if __name__ == "__main__":
    main()
