"""R-aerocapture-cliff-shift — round 11.

Sweeps the Architecture-E closure cliff as a function of aerocapture
inbound dv credit. Reuses R9 physics with parameterized inbound dv.

Pre-registration in STUDY.md (H-11-a..g).
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

# Reuse R9 physics
sys.path.insert(0, str(Path(__file__).parent.parent / "R_arch_E_specific_power_flown_anchored"))
from run import (  # type: ignore
    REACTOR_POWERS_KWE,
    CHUNK_MASSES_T,
    ISP_VALUES_S,
    DV_OUTBOUND_HE_NO_LGA_KM_S,
    DV_INBOUND_TITAN_HE_LGA_KM_S,
    round_trip_E,
    closure_counts,
    best_cell,
)


SPECIFIC_POWERS = [2.4, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
AEROCAPTURE_X_KM_S = [0.0, 5.0, 10.0, 15.0, 20.0, 25.0]


def build_model(sp: float) -> dict:
    return {"kind": "bundled", "m_fixed_t": 5.0, "specific_power_total_w_per_kg": sp}


def sweep_cell(sp: float, x_km_s: float) -> list[dict]:
    model = build_model(sp)
    dv_in = max(DV_INBOUND_TITAN_HE_LGA_KM_S - x_km_s, 0.0)
    rows = []
    for r in REACTOR_POWERS_KWE:
        for c in CHUNK_MASSES_T:
            for isp in ISP_VALUES_S:
                cell = round_trip_E(model, r, c, isp,
                                    dv_outbound_km_s=DV_OUTBOUND_HE_NO_LGA_KM_S,
                                    dv_inbound_km_s=dv_in)
                cell.update({
                    "specific_power_w_per_kg": sp,
                    "aerocapture_X_km_s": x_km_s,
                    "dv_inbound_effective_km_s": dv_in,
                    "reactor_kwe": r,
                    "chunk_t": c,
                    "isp_s": isp,
                })
                rows.append(cell)
    return rows


def main():
    out: dict = {
        "round": "R-aerocapture-cliff-shift",
        "author": "enceladus-r5",
        "date": "2026-05-15",
        "pre_registration": "STUDY.md (H-11-a..g)",
        "specific_power_levels_w_per_kg": SPECIFIC_POWERS,
        "aerocapture_X_levels_km_s": AEROCAPTURE_X_KM_S,
        "constants": {
            "dv_outbound_km_s": DV_OUTBOUND_HE_NO_LGA_KM_S,
            "dv_inbound_baseline_km_s": DV_INBOUND_TITAN_HE_LGA_KM_S,
        },
    }

    # 2D grid: (sp, X) -> closure_counts
    grid: dict[tuple[float, float], dict] = {}
    bests: dict[tuple[float, float], dict | None] = {}
    for sp in SPECIFIC_POWERS:
        for x in AEROCAPTURE_X_KM_S:
            rows = sweep_cell(sp, x)
            grid[(sp, x)] = closure_counts(rows)
            bests[(sp, x)] = best_cell(rows, 25.0)

    # Persist as nested dicts keyed by stringified specific power
    out["closure_count_grid"] = {
        f"sp_{sp}": {f"X_{x}": grid[(sp, x)] for x in AEROCAPTURE_X_KM_S}
        for sp in SPECIFIC_POWERS
    }
    out["best_cell_25yr_grid"] = {
        f"sp_{sp}": {f"X_{x}": (bests[(sp, x)] if bests[(sp, x)] else None)
                     for x in AEROCAPTURE_X_KM_S}
        for sp in SPECIFIC_POWERS
    }

    # Cliff location at each X: lowest sp with >=1 close-25 cell
    cliff_per_X: dict[float, float | None] = {}
    for x in AEROCAPTURE_X_KM_S:
        sps_with_closure = sorted(sp for sp in SPECIFIC_POWERS
                                  if grid[(sp, x)]["n_close_25yr"] >= 1)
        cliff_per_X[x] = sps_with_closure[0] if sps_with_closure else None
    out["cliff_min_sp_per_X"] = {f"X_{x}": cliff_per_X[x]
                                  for x in AEROCAPTURE_X_KM_S}

    # ----- Hypothesis grading -----
    grading = {}

    # H-11-a monotonic: cliff_min_sp is non-increasing in X
    sp_curve = [cliff_per_X[x] for x in AEROCAPTURE_X_KM_S]
    monotonic_nonincreasing = True
    for a, b in zip(sp_curve[:-1], sp_curve[1:]):
        if a is None or b is None:
            continue
        if b > a:
            monotonic_nonincreasing = False
    grading["H_11_a_monotonic"] = {
        "predicted": "min-sp curve non-increasing in X",
        "measured": f"sp curve: {sp_curve}",
        "status": "HELD" if monotonic_nonincreasing else "FALSIFIED",
    }

    # H-11-b slope linearity: fit linear regression to (X, cliff_min_sp) where defined
    xs = [x for x in AEROCAPTURE_X_KM_S if cliff_per_X[x] is not None]
    ys = [cliff_per_X[x] for x in xs]
    if len(xs) >= 2:
        # ordinary least squares slope
        x_mean = sum(xs) / len(xs)
        y_mean = sum(ys) / len(ys)
        num = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys))
        den = sum((x - x_mean) ** 2 for x in xs)
        slope = num / den if den else 0.0
        grading["H_11_b_slope"] = {
            "predicted": "d(sp_min)/d(X) in [-0.35, -0.20] W/kg per km/s",
            "measured": f"slope = {slope:.3f} W/kg per km/s over points {list(zip(xs,ys))}",
            "status": "HELD" if -0.35 <= slope <= -0.20 else "FALSIFIED",
        }
    else:
        grading["H_11_b_slope"] = {
            "predicted": "slope in [-0.35, -0.20]",
            "measured": "insufficient points to fit",
            "status": "VACUOUS",
        }

    # H-11-c cliff to <=5.3 W/kg requires X in [10, 15]
    x_for_5p3: float | None = None
    for x in AEROCAPTURE_X_KM_S:
        if cliff_per_X[x] is not None and cliff_per_X[x] <= 5.3:
            x_for_5p3 = x
            break
    grading["H_11_c_5p3"] = {
        "predicted": "cliff <= 5.3 W/kg first achieved at X in [10, 15] km/s",
        "measured": f"first X with cliff <= 5.3 W/kg = {x_for_5p3}",
        "status": ("HELD" if x_for_5p3 is not None and 10 <= x_for_5p3 <= 15 else "FALSIFIED"),
    }

    # H-11-d cliff to <=2.4 W/kg requires X in [15, 25]
    x_for_2p4: float | None = None
    for x in AEROCAPTURE_X_KM_S:
        if cliff_per_X[x] is not None and cliff_per_X[x] <= 2.4:
            x_for_2p4 = x
            break
    grading["H_11_d_2p4"] = {
        "predicted": "cliff <= 2.4 W/kg first achieved at X in [15, 25] km/s",
        "measured": f"first X with cliff <= 2.4 W/kg = {x_for_2p4}",
        "status": ("HELD" if x_for_2p4 is not None and 15 <= x_for_2p4 <= 25 else "FALSIFIED"),
    }

    # H-11-e: at X = 25 km/s (near full inbound aerocapture), >=1 close-25 cell at 2.4 W/kg
    # (Note: full aerocapture is X = 24.7; nearest tested is 25.)
    g_e = grid.get((2.4, 25.0))
    n_close = g_e["n_close_25yr"] if g_e else 0
    grading["H_11_e_full_aerocapture"] = {
        "predicted": "at X=25 km/s (near full inbound aerocapture), >=1 close-25 cell at 2.4 W/kg",
        "measured": f"n_close_25 at (sp=2.4, X=25) = {n_close}",
        "status": "HELD" if n_close >= 1 else "FALSIFIED",
    }

    # H-11-g: RT delta at 500/200/2934/5 W/kg, X=10 vs X=0
    def find(sp, x, r, c, isp):
        rows = sweep_cell(sp, x)
        for cell in rows:
            if (cell["reactor_kwe"] == r and cell["chunk_t"] == c
                    and cell["isp_s"] == isp):
                return cell
        return None
    c0 = find(5.0, 0.0, 500.0, 200.0, 2934.0)
    c10 = find(5.0, 10.0, 500.0, 200.0, 2934.0)
    if c0 and c10:
        rt_delta = c10["round_trip_yr"] - c0["round_trip_yr"]
        grading["H_11_g_rt_delta"] = {
            "predicted": "RT delta at 5W/kg / 500/200/2934 / X=10 vs X=0 in [-1.4, -0.8] yr",
            "measured": f"RT(X=0) = {c0['round_trip_yr']:.2f} yr, RT(X=10) = {c10['round_trip_yr']:.2f} yr, delta = {rt_delta:.2f} yr; delivered: {c0['delivered_t']:.1f} -> {c10['delivered_t']:.1f} t",
            "status": "HELD" if -1.4 <= rt_delta <= -0.8 else "FALSIFIED",
        }

    # Aggregate verdict
    grading["H_11_aggregate"] = {
        "predicted": "aerocapture credit X linearly buys lower minimum specific power; ~10-15 km/s buys flown-RTG anchor; ~15-25 km/s buys KRUSTY anchor",
        "measured": f"cliff curve {dict(zip(AEROCAPTURE_X_KM_S, sp_curve))}",
        "status_short": "see component hypotheses",
    }

    out["hypothesis_grading"] = grading

    # Write JSON
    out_path = Path(__file__).parent / "results" / "aerocapture_cliff_shift.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    # Best-cell dicts may contain inf; convert to strings via default=str at dump time
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, default=str)

    # Print
    print("\n=== R-aerocapture-cliff-shift — RESULTS ===\n")
    print("Close-25yr cell count grid (rows: specific power W/kg, cols: aerocapture X km/s):")
    print(f"{'sp \\\\ X':>8s}", *(f"{x:>6.1f}" for x in AEROCAPTURE_X_KM_S))
    for sp in SPECIFIC_POWERS:
        cells = [grid[(sp, x)]["n_close_25yr"] for x in AEROCAPTURE_X_KM_S]
        print(f"{sp:>8.1f}", *(f"{c:>6d}" for c in cells))

    print("\nCliff location (min sp with >=1 close-25 cell) at each X:")
    for x in AEROCAPTURE_X_KM_S:
        cp = cliff_per_X[x]
        print(f"  X = {x:>5.1f} km/s -> min-sp = {cp if cp is not None else 'no closure':}")

    print("\nHypothesis grading:")
    for k, v in grading.items():
        print(f"  {k}: {v.get('status', v.get('status_short', '?'))}")
        print(f"    measured: {v['measured']}")
    print(f"\nResults written to {out_path}")


if __name__ == "__main__":
    main()
