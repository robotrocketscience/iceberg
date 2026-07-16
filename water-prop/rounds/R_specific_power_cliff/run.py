"""R-specific-power-cliff — round 10.

Finer-grained sweep to locate the Architecture-E L0-05-closure cliff between
5 and 10 W/kg specific power. Same physics as R9 (which replicated R6).

Pre-registration in STUDY.md (H-10-a..h).
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

# Reuse R9's physics by importing it
sys.path.insert(0, str(Path(__file__).parent.parent / "R_arch_E_specific_power_flown_anchored"))
from run import (  # type: ignore
    REACTOR_POWERS_KWE,
    CHUNK_MASSES_T,
    ISP_VALUES_S,
    round_trip_E,
    closure_counts,
    best_cell,
)


SPECIFIC_POWERS = [2.4, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]


def build_model(specific_power_w_per_kg: float) -> dict:
    return {
        "kind": "bundled",
        "m_fixed_t": 5.0,
        "specific_power_total_w_per_kg": specific_power_w_per_kg,
    }


def run_sweep_for(sp: float) -> list[dict]:
    model = build_model(sp)
    rows = []
    for r in REACTOR_POWERS_KWE:
        for c in CHUNK_MASSES_T:
            for isp in ISP_VALUES_S:
                cell = round_trip_E(model, r, c, isp)
                cell.update({
                    "specific_power_w_per_kg": sp,
                    "reactor_kwe": r,
                    "chunk_t": c,
                    "isp_s": isp,
                })
                rows.append(cell)
    return rows


def main():
    out: dict = {
        "round": "R-specific-power-cliff",
        "author": "enceladus-r5",
        "date": "2026-05-15",
        "pre_registration": "STUDY.md (H-10-a..h)",
        "specific_power_levels_w_per_kg": SPECIFIC_POWERS,
        "sweep_axes": {
            "reactor_kwe": REACTOR_POWERS_KWE,
            "chunk_t": CHUNK_MASSES_T,
            "isp_s": ISP_VALUES_S,
        },
    }
    sweeps = {sp: run_sweep_for(sp) for sp in SPECIFIC_POWERS}
    closures = {sp: closure_counts(rows) for sp, rows in sweeps.items()}
    out["closure_counts"] = {str(sp): closures[sp] for sp in SPECIFIC_POWERS}
    bests = {}
    for sp in SPECIFIC_POWERS:
        bests[str(sp)] = {
            f"best_at_{c}yr": best_cell(sweeps[sp], c)
            for c in (20, 25, 30)
        }
    out["best_cells"] = bests

    # Cliff-detect: find largest single-step drop in 25-yr close-cell count
    counts_25 = [(sp, closures[sp]["n_close_25yr"]) for sp in SPECIFIC_POWERS]
    counts_25.sort(key=lambda x: x[0])
    monotonic_dec = True
    largest_step = (0, 0.0, 0.0)  # (delta, sp_low, sp_high)
    for (sp_lo, n_lo), (sp_hi, n_hi) in zip(counts_25[:-1], counts_25[1:]):
        if n_lo > n_hi:
            monotonic_dec = False
        delta = n_hi - n_lo
        if delta > largest_step[0]:
            largest_step = (delta, sp_lo, sp_hi)
    out["cliff_detection"] = {
        "monotonic_increasing_with_specific_power": monotonic_dec,
        "largest_single_step_increase": {
            "delta_close_cells": largest_step[0],
            "between_w_per_kg": (largest_step[1], largest_step[2]),
        },
        "first_specific_power_with_zero_close": next(
            (sp for sp, n in counts_25 if n == 0), None),
        "last_specific_power_with_nonzero_close": (
            counts_25[-1][0] if counts_25[-1][1] > 0 else
            next((sp for sp, n in reversed(counts_25) if n > 0), None)
        ),
    }

    # ----- Hypothesis grading -----
    grading = {}
    grading["H_10_a_monotonic"] = {
        "predicted": "monotonic increase in close-cell count with specific power",
        "measured": f"monotonic = {out['cliff_detection']['monotonic_increasing_with_specific_power']}",
        "status": "HELD" if out["cliff_detection"]["monotonic_increasing_with_specific_power"] else "FALSIFIED",
    }
    # Cliff range
    first_zero = out["cliff_detection"]["first_specific_power_with_zero_close"]
    last_nonzero = out["cliff_detection"]["last_specific_power_with_nonzero_close"]
    grading["H_10_b_cliff_location"] = {
        "predicted": "cliff (drop to 0 close at 25-yr) lies between 7 and 9 W/kg inclusive",
        "measured": f"first zero-close sp = {first_zero} W/kg; last nonzero-close sp = {last_nonzero} W/kg",
        "status": "HELD" if (last_nonzero is not None and 7 <= last_nonzero <= 9) else "FALSIFIED",
    }
    # Per-level brackets
    n9 = closures[9.0]["n_close_25yr"]
    n8 = closures[8.0]["n_close_25yr"]
    n7 = closures[7.0]["n_close_25yr"]
    n6 = closures[6.0]["n_close_25yr"]
    grading["H_10_c_9wpkg"] = {"predicted": "5-9 close at 25-yr",
                                "measured": f"{n9}/60",
                                "status": "HELD" if 5 <= n9 <= 9 else "FALSIFIED"}
    grading["H_10_d_8wpkg"] = {"predicted": "2-6 close at 25-yr",
                                "measured": f"{n8}/60",
                                "status": "HELD" if 2 <= n8 <= 6 else "FALSIFIED"}
    grading["H_10_e_7wpkg"] = {"predicted": "0-3 close at 25-yr",
                                "measured": f"{n7}/60",
                                "status": "HELD" if 0 <= n7 <= 3 else "FALSIFIED"}
    grading["H_10_f_6wpkg"] = {"predicted": "0-1 close at 25-yr",
                                "measured": f"{n6}/60",
                                "status": "HELD" if 0 <= n6 <= 1 else "FALSIFIED"}
    # H-10-g gradient
    max_step = largest_step[0]
    grading["H_10_g_gradient"] = {
        "predicted": "no sharp single-step cliff (max-step <5 between adjacent levels)",
        "measured": f"largest step = {max_step} cells between {largest_step[1]} and {largest_step[2]} W/kg",
        "status": "HELD" if max_step < 5 else "FALSIFIED",
    }
    # H-10-h aggregate
    rates = {sp: closures[sp]["n_close_25yr"] / 60.0 for sp in SPECIFIC_POWERS}
    grading["H_10_h_aggregate"] = {
        "predicted": "5-10 W/kg yields 5-10 percentage-point spread in L0-05-25yr closure rate; midpoint near 6-8 W/kg",
        "measured": "; ".join(f"{sp} W/kg: {rates[sp]*100:.1f}%"
                              for sp in SPECIFIC_POWERS),
        "status_short": "see component hypotheses",
    }
    out["hypothesis_grading"] = grading

    # Write
    out_path = Path(__file__).parent / "results" / "specific_power_cliff.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, default=str)

    # Print
    print("\n=== R-specific-power-cliff — RESULTS ===\n")
    print(f"{'W/kg':>6s} {'25-yr':>8s} {'30-yr':>8s} {'pos-pay':>8s} {'best-25-deliv':>14s}")
    for sp in SPECIFIC_POWERS:
        c = closures[sp]
        b = bests[str(sp)]["best_at_25yr"]
        bd = f"{b['delivered_t']:.1f}t @{b['reactor_kwe']:.0f}kWe" if b else "—"
        print(f"{sp:>6.1f} {c['n_close_25yr']:>4d}/60 {c['n_close_30yr']:>4d}/60 "
              f"{c['n_pos_payload']:>4d}/60 {bd:>14s}")
    print()
    print("Cliff detection:")
    print(f"  monotonic_increasing: {out['cliff_detection']['monotonic_increasing_with_specific_power']}")
    print(f"  largest single-step delta: {out['cliff_detection']['largest_single_step_increase']}")
    print(f"  first sp with 0 close-25: {first_zero} W/kg")
    print(f"  last sp with >0 close-25: {last_nonzero} W/kg")
    print()
    print("Hypothesis grading:")
    for k, v in grading.items():
        print(f"  {k}: {v.get('status', v.get('status_short', '?'))}")
        print(f"    measured: {v['measured']}")
    print(f"\nResults written to {out_path}")


if __name__ == "__main__":
    main()
