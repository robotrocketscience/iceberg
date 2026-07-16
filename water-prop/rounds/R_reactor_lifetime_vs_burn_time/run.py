"""R-reactor-lifetime-vs-burn-time — round 12.

Re-grades R11's 2D grid (specific power x aerocapture) under reactor
lifetime ceilings L in {5, 8, 10, 15, infinity} years.

Pre-registration in STUDY.md (H-12-a..h).
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

# Reuse R11's sweep_cell via explicit module-spec import to avoid `run` collision
import importlib.util

_R9_PATH = Path(__file__).parent.parent / "R_arch_E_specific_power_flown_anchored" / "run.py"
_R11_PATH = Path(__file__).parent.parent / "R_aerocapture_cliff_shift" / "run.py"
_r9_spec = importlib.util.spec_from_file_location("r9_run", _R9_PATH)
_r9_mod = importlib.util.module_from_spec(_r9_spec)
sys.modules["r9_run"] = _r9_mod
_r9_spec.loader.exec_module(_r9_mod)
# Pre-register R9 module under bare name 'run' so R11 can import it
sys.modules["run"] = _r9_mod
_r11_spec = importlib.util.spec_from_file_location("r11_run", _R11_PATH)
_r11_mod = importlib.util.module_from_spec(_r11_spec)
_r11_spec.loader.exec_module(_r11_mod)
sweep_cell = _r11_mod.sweep_cell


SPECIFIC_POWERS = [2.4, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
AEROCAPTURE_X_KM_S = [0.0, 5.0, 10.0, 15.0, 20.0, 25.0]
LIFETIME_CEILINGS_YR = [5.0, 8.0, 10.0, 15.0, float("inf")]


def cumulative_burn_yr(cell: dict) -> float:
    """outbound burn + inbound burn (years). Reactor idle during cruise."""
    if not cell.get("feasible", False):
        return math.inf
    out_b = cell.get("t_outbound_burn_yr", math.inf)
    in_b = cell.get("t_inbound_burn_yr", math.inf)
    if not (math.isfinite(out_b) and math.isfinite(in_b)):
        return math.inf
    return out_b + in_b


def closes_under_lifetime(cell: dict, L: float) -> bool:
    return (cell.get("closes_25yr", False)
            and cell.get("delivered_t", -math.inf) > 0
            and cumulative_burn_yr(cell) <= L)


def regrade_per_lifetime(rows: list[dict]) -> dict[float, int]:
    return {L: sum(1 for r in rows if closes_under_lifetime(r, L))
            for L in LIFETIME_CEILINGS_YR}


def main():
    out: dict = {
        "round": "R-reactor-lifetime-vs-burn-time",
        "author": "enceladus-r5",
        "date": "2026-05-15",
        "pre_registration": "STUDY.md (H-12-a..h)",
        "specific_power_levels_w_per_kg": SPECIFIC_POWERS,
        "aerocapture_X_levels_km_s": AEROCAPTURE_X_KM_S,
        "lifetime_ceilings_yr": [str(L) for L in LIFETIME_CEILINGS_YR],
    }

    # Re-run R11's grid and capture per-cell cumulative burn
    grid_rows: dict[tuple[float, float], list[dict]] = {}
    for sp in SPECIFIC_POWERS:
        for x in AEROCAPTURE_X_KM_S:
            grid_rows[(sp, x)] = sweep_cell(sp, x)

    # Per (sp, X), regrade close-25 count under each lifetime ceiling
    regrade: dict[tuple[float, float], dict[float, int]] = {}
    for k, rows in grid_rows.items():
        regrade[k] = regrade_per_lifetime(rows)
    out["regraded_close_25yr_count"] = {
        f"sp_{sp}": {
            f"X_{x}": {f"L_{L}": regrade[(sp, x)][L] for L in LIFETIME_CEILINGS_YR}
            for x in AEROCAPTURE_X_KM_S
        }
        for sp in SPECIFIC_POWERS
    }

    # Cumulative-burn stats per cell, for hypothesis pre-checks
    # H-12-a, H-12-b: 10 W/kg / X=0
    cells_10_X0 = grid_rows[(10.0, 0.0)]
    close_25_at_10_X0 = [c for c in cells_10_X0
                         if c.get("closes_25yr") and c.get("delivered_t", -math.inf) > 0]
    cum_burns_close_10_X0 = sorted(cumulative_burn_yr(c) for c in close_25_at_10_X0)
    out["H_12_a_b_cumulative_burns_10wpkg_X0"] = {
        "n_close_cells": len(close_25_at_10_X0),
        "cumulative_burn_yr_sorted": cum_burns_close_10_X0,
        "max": cum_burns_close_10_X0[-1] if cum_burns_close_10_X0 else None,
        "n_under_5yr": sum(1 for b in cum_burns_close_10_X0 if b <= 5.0),
        "n_under_2yr": sum(1 for b in cum_burns_close_10_X0 if b <= 2.0),
    }

    # H-12-c: at 8 W/kg / X=0 (R10 cliff): how many of 4 close cells fall under L=10?
    close_25_at_8_X0 = [c for c in grid_rows[(8.0, 0.0)]
                        if c.get("closes_25yr") and c.get("delivered_t", -math.inf) > 0]
    cum_burns_8_X0 = sorted(cumulative_burn_yr(c) for c in close_25_at_8_X0)
    n_8_X0_under_10 = sum(1 for b in cum_burns_8_X0 if b <= 10.0)
    n_8_X0_fall_under_10 = len(cum_burns_8_X0) - n_8_X0_under_10

    # H-12-d: at 5 W/kg / X=10: 3 close cells. How many fall under L=10? L=5?
    close_25_at_5_X10 = [c for c in grid_rows[(5.0, 10.0)]
                         if c.get("closes_25yr") and c.get("delivered_t", -math.inf) > 0]
    cum_burns_5_X10 = sorted(cumulative_burn_yr(c) for c in close_25_at_5_X10)
    n_5_X10_under_10 = sum(1 for b in cum_burns_5_X10 if b <= 10.0)
    n_5_X10_under_5 = sum(1 for b in cum_burns_5_X10 if b <= 5.0)

    # H-12-e: 5 W/kg / X=25: 44 close cells. Fraction surviving L=10
    close_25_at_5_X25 = [c for c in grid_rows[(5.0, 25.0)]
                         if c.get("closes_25yr") and c.get("delivered_t", -math.inf) > 0]
    n_5_X25_under_10 = sum(1 for c in close_25_at_5_X25
                           if cumulative_burn_yr(c) <= 10.0)
    frac_5_X25_under_10 = (n_5_X25_under_10 / len(close_25_at_5_X25)
                           if close_25_at_5_X25 else 0.0)

    # H-12-f: across full grid, what fraction of close-25 cells survive L=10?
    total_close_25 = 0
    total_close_25_under_10 = 0
    for k, rows in grid_rows.items():
        close = [r for r in rows if r.get("closes_25yr")
                 and r.get("delivered_t", -math.inf) > 0]
        total_close_25 += len(close)
        total_close_25_under_10 += sum(1 for r in close
                                       if cumulative_burn_yr(r) <= 10.0)
    fraction_removed_at_L10 = (
        1 - total_close_25_under_10 / total_close_25 if total_close_25 else 0.0)

    # H-12-g: at every specific power tested, does some cell close at L=5?
    sp_with_L5_close = []
    for sp in SPECIFIC_POWERS:
        any_close_L5 = False
        for x in AEROCAPTURE_X_KM_S:
            close_L5 = [r for r in grid_rows[(sp, x)]
                        if closes_under_lifetime(r, 5.0)]
            if close_L5:
                any_close_L5 = True
                break
        sp_with_L5_close.append((sp, any_close_L5))

    # ----- Hypothesis grading -----
    grading = {}
    max10_X0 = out["H_12_a_b_cumulative_burns_10wpkg_X0"]["max"]
    grading["H_12_a_all_10wpkg_X0_under_5yr"] = {
        "predicted": "all 9 close-cells at 10 W/kg X=0 have cumulative burn <= 5 yr",
        "measured": f"max cumulative = {max10_X0:.2f} yr "
                    f"of {len(close_25_at_10_X0)} close cells",
        "status": "HELD" if (max10_X0 is not None and max10_X0 <= 5.0) else "FALSIFIED",
    }
    n_under_2 = out["H_12_a_b_cumulative_burns_10wpkg_X0"]["n_under_2yr"]
    grading["H_12_b_at_least_4_under_2yr"] = {
        "predicted": ">= 4 close cells at 10 W/kg X=0 have cumulative <= 2 yr",
        "measured": f"{n_under_2} cells under 2 yr (of {len(close_25_at_10_X0)})",
        "status": "HELD" if n_under_2 >= 4 else "FALSIFIED",
    }
    grading["H_12_c_8wpkg_X0_fall"] = {
        "predicted": "2-3 of 4 close cells at 8 W/kg X=0 fall under L=10 yr",
        "measured": f"{n_8_X0_fall_under_10} fall under L=10 of {len(cum_burns_8_X0)}; "
                    f"cumulative burns: {[f'{b:.2f}' for b in cum_burns_8_X0]}",
        "status": "HELD" if 2 <= n_8_X0_fall_under_10 <= 3 else "FALSIFIED",
    }
    grading["H_12_d_5wpkg_X10"] = {
        "predicted": "of 3 close cells at 5 W/kg X=10: 2-3 fall under L=10, 0 survive L=5",
        "measured": f"under L=10: {n_5_X10_under_10}; under L=5: {n_5_X10_under_5}; "
                    f"cumulative burns: {[f'{b:.2f}' for b in cum_burns_5_X10]}",
        "status": ("HELD" if (2 <= len(cum_burns_5_X10) - n_5_X10_under_10 <= 3
                              and n_5_X10_under_5 == 0) else "FALSIFIED"),
    }
    grading["H_12_e_5wpkg_X25_majority_fall"] = {
        "predicted": "of 44 close cells at 5 W/kg X=25, < 50% survive L=10",
        "measured": f"{n_5_X25_under_10} survive L=10 of {len(close_25_at_5_X25)}; "
                    f"survival fraction = {frac_5_X25_under_10:.1%}",
        "status": "HELD" if frac_5_X25_under_10 < 0.50 else "FALSIFIED",
    }
    grading["H_12_f_overall_removal"] = {
        "predicted": "L=10 reactor lifetime removes 30-50% of close-25 cells (full grid)",
        "measured": f"{total_close_25_under_10}/{total_close_25} survive L=10; "
                    f"fraction removed = {fraction_removed_at_L10:.1%}",
        "status": "HELD" if 0.30 <= fraction_removed_at_L10 <= 0.50 else "FALSIFIED",
    }
    n_sp_with_L5 = sum(1 for sp, has in sp_with_L5_close if has)
    grading["H_12_g_every_sp_has_L5_cell"] = {
        "predicted": "at every specific power tested, some cell closes under L=5",
        "measured": f"{n_sp_with_L5} of {len(SPECIFIC_POWERS)} specific powers have at least one L=5 close cell; "
                    f"breakdown: {sp_with_L5_close}",
        "status": "HELD" if n_sp_with_L5 == len(SPECIFIC_POWERS) else "FALSIFIED",
    }
    grading["H_12_h_aggregate"] = {
        "predicted": "L=10 is secondary to specific power (most cells survive); L=5 is primary (most cells fall)",
        "measured": f"L=10 survival = {1-fraction_removed_at_L10:.1%}; "
                    f"breakdown across grid in regraded_close_25yr_count",
        "status_short": "see component hypotheses",
    }
    out["hypothesis_grading"] = grading

    # Write JSON
    out_path = Path(__file__).parent / "results" / "reactor_lifetime_regrade.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, default=str)

    # Print headline tables
    print("\n=== R-reactor-lifetime-vs-burn-time — RESULTS ===\n")
    print("Survival of close-25yr cells under reactor lifetime ceiling L (years).")
    print("Each value = count of cells in (sp, X) bucket that ALSO have cumulative burn <= L.\n")
    for L in LIFETIME_CEILINGS_YR:
        Lstr = "inf" if math.isinf(L) else f"{L:.0f}"
        print(f"--- Lifetime ceiling L = {Lstr} yr ---")
        print(f"{'sp \\\\ X':>8s}", *(f"{x:>6.1f}" for x in AEROCAPTURE_X_KM_S))
        for sp in SPECIFIC_POWERS:
            row = [regrade[(sp, x)][L] for x in AEROCAPTURE_X_KM_S]
            print(f"{sp:>8.1f}", *(f"{c:>6d}" for c in row))
        print()

    print("Hypothesis grading:")
    for k, v in grading.items():
        print(f"  {k}: {v.get('status', v.get('status_short', '?'))}")
        print(f"    measured: {v['measured']}")
    print(f"\nResults written to {out_path}")


if __name__ == "__main__":
    main()
