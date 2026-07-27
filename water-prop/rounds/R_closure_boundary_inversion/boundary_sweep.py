"""R-closure-boundary-inversion — boundary sweep driver.

Inverts the closure question: given the closed-loop saturn_water_v1 oracle
(0 of 1,744 paths close at the record baseline), find per-parameter thresholds
and minimal joint scenarios at which >= 1 path closes.

Stages (per STUDY.md):
  1. per-axis monotonicity spot-check + bisection (arms A and B)
  2. dense scans on declared-non-monotone axes (propellant_fraction, chunk grid)
  3. 2-D boundary maps around found thresholds
  4. named joint scenarios S1..S7
  5. scalar lambda-bisection along the baseline->aspirational-2035 direction

Run from repo root:
  PYTHONPATH=water-prop/sims water-prop/.venv/bin/python \
      water-prop/rounds/R_closure_boundary_inversion/boundary_sweep.py

Writes results/boundary_results.json (small, committed per project convention).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SIMS = HERE.parents[1] / "sims"
if str(SIMS) not in sys.path:
    sys.path.insert(0, str(SIMS))

from mission_graph.framework import SweepAxis, VehicleAxis, VehicleState, sweep  # noqa: E402
from mission_graph.missions.saturn_water_v1 import (  # noqa: E402
    saturn_water_v1,
    make_derived_mass_transform,
)

# ------------------------------------------------------------------ #
# Oracle
# ------------------------------------------------------------------ #

RECORD_POWER = (1.0, 10.0, 11.0, 20.0, 30.0, 55.0)
RECORD_CHUNK = (10_000.0, 25_000.0, 50_000.0, 100_000.0, 200_000.0)
RECORD_THRUST = (1.0, 2.5, 5.0, 10.0, 25.0)

BASE_PARAMS = {
    "chemical_isp_s": 340.0,
    "electric_isp_s": 3000.0,
    "electric_thrust_n": 5.0,
    "water_met_isp_s": 800.0,
    "chunk_mass_kg": 50_000.0,
    "multi_falcon_launch_count": 6,
    "launch_epoch_jd": 0.0,
}

# Arm B: honest posture (STUDY, arm definitions).
ARM_B_PARAMS = {
    "visviva_capture": True,
    "chunk_fed_dv_km_s": 18.0,
    "reactor_lifetime_years": 10.0,
}

PREDICATES = ("arrived_at_depot", "delivered_floor_10t", "delivered_floor")

_oracle_calls = 0


def run_grid(extra_params=None, power=RECORD_POWER, chunk=RECORD_CHUNK,
             thrust=RECORD_THRUST):
    global _oracle_calls
    _oracle_calls += 1
    bp = dict(BASE_PARAMS)
    if extra_params:
        bp.update(extra_params)
    state = VehicleState(
        mass_kg=50_000.0, propellant_kg=0.0, payload_kg=0.0,
        location="pre_launch", v_inf_km_s=0.0, time_elapsed_s=0.0,
        epoch_jd=None, power_available_kwe=30.0,
    )
    return sweep(
        saturn_water_v1, state, bp,
        param_axes=[SweepAxis("chunk_mass_kg", chunk),
                    SweepAxis("electric_thrust_n", thrust)],
        vehicle_axes=[VehicleAxis("power_kwe", power, "power_available_kwe")],
        state_transform=make_derived_mass_transform(bp),
    )


def summarize(cells):
    """Closure counts per predicate + max delivered payload + failure taxonomy."""
    out = {p: 0 for p in PREDICATES}
    max_delivered = 0.0
    taxonomy: dict[str, int] = {}
    n_paths = 0
    for c in cells:
        if c.skipped_reason is not None:
            continue
        cell_close = {p: False for p in PREDICATES}
        for r in c.results:
            n_paths += 1
            if r.is_feasible:
                for p in PREDICATES:
                    if r.closure_verdicts.get(p) in ("close", "close_strict", "close_waiver"):
                        cell_close[p] = True
                if r.leaf_state.location == "LEO_depot":
                    max_delivered = max(max_delivered, r.leaf_state.payload_kg)
            else:
                ph = r.infeasible_at or "unknown"
                taxonomy[ph] = taxonomy.get(ph, 0) + 1
        for p in PREDICATES:
            if cell_close[p]:
                out[p] += 1
    out["max_delivered_t"] = round(max_delivered / 1000.0, 2)
    out["paths"] = n_paths
    out["taxonomy"] = dict(sorted(taxonomy.items(), key=lambda kv: -kv[1]))
    return out


def closes(extra_params, predicate="arrived_at_depot", **grid_kw) -> bool:
    return summarize(run_grid(extra_params, **grid_kw))[predicate] >= 1


# ------------------------------------------------------------------ #
# Stage 1: per-axis bisection
# ------------------------------------------------------------------ #

AXES = {
    # name: (lo, hi, direction) — direction +1 means closure expected at HIGH end
    "water_met_isp_s": (800.0, 20_000.0, +1),
    "electric_isp_s": (3_000.0, 20_000.0, +1),
    "chemical_isp_s": (340.0, 480.0, +1),
    "launcher_cap_multiplier": (1.0, 16.0, +1),
    "reactor_specific_power_w_per_kg": (2.4, 400.0, +1),
    "capture_efficiency_multiplier": (0.25, 1.0, +1),
}


def bisect_axis(name, lo, hi, arm_params, predicate="arrived_at_depot",
                rel_tol=0.02, extra=None):
    """Find smallest value in [lo, hi] where closes() flips True, else None."""
    base = dict(arm_params)
    if extra:
        base.update(extra)
    if closes(dict(base, **{name: lo}), predicate):
        return lo  # already closes at the record value
    if not closes(dict(base, **{name: hi}), predicate):
        return None  # no threshold inside the bracket
    while (hi - lo) / hi > rel_tol:
        mid = 0.5 * (lo + hi)
        if closes(dict(base, **{name: mid}), predicate):
            hi = mid
        else:
            lo = mid
    return hi


def stage1(arm_params, arm_name):
    print(f"\n== Stage 1 (per-axis bisection, {arm_name}) ==")
    results = {}
    for name, (lo, hi, _d) in AXES.items():
        # monotonicity spot-check at 3 points
        pts = [lo, 0.5 * (lo + hi), hi]
        flags = [closes(dict(arm_params, **{name: p})) for p in pts]
        mono = flags == sorted(flags)
        thr = bisect_axis(name, lo, hi, arm_params) if mono else None
        results[name] = {"bracket": [lo, hi], "spot_flags": flags,
                         "monotone": mono, "threshold": thr}
        print(f"  {name:34s} spot={flags} thr={thr}")
    # power-grid extension is a grid change, not a param: probe extended grids
    for extra_power in ((100.0,), (100.0, 200.0), (100.0, 200.0, 500.0, 1000.0)):
        grid = RECORD_POWER + extra_power
        s = summarize(run_grid(arm_params, power=grid))
        results[f"power_grid_+{'_'.join(str(int(p)) for p in extra_power)}"] = {
            p: s[p] for p in PREDICATES}
        print(f"  power grid +{extra_power}: {[s[p] for p in PREDICATES]}")
    return results


# ------------------------------------------------------------------ #
# Stage 2: dense scans (non-monotone axes)
# ------------------------------------------------------------------ #

def stage2(arm_params, arm_name):
    print(f"\n== Stage 2 (dense scans, {arm_name}) ==")
    out = {}
    f_scan = {}
    f = 0.05
    while f <= 0.901:
        s = summarize(run_grid(dict(arm_params, propellant_fraction=f)))
        f_scan[round(f, 3)] = [s[p] for p in PREDICATES]
        f += 0.025
    out["propellant_fraction_scan"] = f_scan
    any_close = {k: v for k, v in f_scan.items() if v[0] > 0}
    print(f"  propellant_fraction values with >=1 arrival: {list(any_close) or 'NONE'}")

    demo_chunk = (500.0, 1_000.0, 2_000.0, 5_000.0)
    big_chunk = (300_000.0, 500_000.0)
    for label, grid in (("demonstrator_chunk_0.5-5t", demo_chunk),
                        ("big_chunk_300-500t", big_chunk)):
        s = summarize(run_grid(arm_params, chunk=grid))
        out[label] = {p: s[p] for p in PREDICATES} | {
            "max_delivered_t": s["max_delivered_t"], "taxonomy": s["taxonomy"]}
        print(f"  {label}: {[s[p] for p in PREDICATES]} max_t={s['max_delivered_t']}")
    return out


# ------------------------------------------------------------------ #
# Stage 4: named joint scenarios
# ------------------------------------------------------------------ #

def scenarios(arm_params):
    S = {}
    S["S1_starship_refill_x5"] = {"launcher_cap_multiplier": 5.0}
    S["S2_S1_plus_f_scan_best"] = None  # filled dynamically below
    S["S3_S1_plus_nstm3_100kwe_33wkg"] = {
        "launcher_cap_multiplier": 5.0,
        "reactor_specific_power_w_per_kg": 33.0,
    }
    S["S4_S3_plus_met_900s"] = dict(S["S3_S1_plus_nstm3_100kwe_33wkg"],
                                    water_met_isp_s=900.0)
    S["S5_S3_plus_rf_ion_2000s"] = dict(S["S3_S1_plus_nstm3_100kwe_33wkg"],
                                        water_met_isp_s=2000.0)
    S["S5b_S5_plus_f_0p4"] = dict(S["S5_S3_plus_rf_ion_2000s"],
                                  propellant_fraction=0.40)
    return S


def stage4(arm_params, arm_name):
    print(f"\n== Stage 4 (named scenarios, {arm_name}) ==")
    out = {}
    power_ext = RECORD_POWER + (100.0, 200.0)
    # S2: find the best propellant fraction under S1
    best_f, best_arr = None, 0
    f = 0.20
    while f <= 0.861:
        s = summarize(run_grid(dict(arm_params, launcher_cap_multiplier=5.0,
                                    propellant_fraction=f), power=power_ext))
        if s["arrived_at_depot"] > best_arr:
            best_arr, best_f = s["arrived_at_depot"], round(f, 3)
        f += 0.05
    out["S2_S1_plus_f_scan_best"] = {"best_f": best_f, "arrived_cells": best_arr}
    print(f"  S2 best propellant_fraction under S1: {best_f} ({best_arr} cells)")

    for name, extra in scenarios(arm_params).items():
        if extra is None:
            continue
        params = dict(arm_params, **extra)
        if best_f is not None and name.startswith("S2"):
            params["propellant_fraction"] = best_f
        s = summarize(run_grid(params, power=power_ext))
        out[name] = {p: s[p] for p in PREDICATES} | {
            "max_delivered_t": s["max_delivered_t"],
            "taxonomy_top3": dict(list(s["taxonomy"].items())[:3])}
        print(f"  {name}: arrived={s['arrived_at_depot']} 10t={s['delivered_floor_10t']} "
              f"30t={s['delivered_floor']} max_t={s['max_delivered_t']}")

    # S7 demonstrator grid: small chunk, modest power, single launcher
    s = summarize(run_grid(dict(arm_params), chunk=(500.0, 1000.0, 2000.0, 5000.0),
                           power=(1.0, 10.0, 20.0, 30.0)))
    out["S7_demonstrator_record_tech"] = {p: s[p] for p in PREDICATES} | {
        "taxonomy": s["taxonomy"]}
    s = summarize(run_grid(dict(arm_params, water_met_isp_s=1500.0,
                                chunk_fed_min_power_kwe=10.0),
                           chunk=(500.0, 1000.0, 2000.0, 5000.0),
                           power=(10.0, 20.0, 30.0)))
    out["S7b_demonstrator_isp1500_powergate10"] = {p: s[p] for p in PREDICATES} | {
        "max_delivered_t": s["max_delivered_t"], "taxonomy_top3": dict(list(s["taxonomy"].items())[:3])}
    print(f"  S7 record: {[out['S7_demonstrator_record_tech'][p] for p in PREDICATES]}  "
          f"S7b isp1500: {[out['S7b_demonstrator_isp1500_powergate10'][p] for p in PREDICATES]}")
    return out


# ------------------------------------------------------------------ #
# Stage 5: lambda-bisection along baseline -> aspirational-2035
# ------------------------------------------------------------------ #

ASPIRATIONAL = {
    "launcher_cap_multiplier": (1.0, 5.0),
    "reactor_specific_power_w_per_kg": (2.4, 40.0),
    "water_met_isp_s": (800.0, 3000.0),
    "propellant_fraction": (0.80, 0.36),
}


def lam_params(lam, arm_params):
    p = dict(arm_params)
    for k, (a, b) in ASPIRATIONAL.items():
        p[k] = a + lam * (b - a)
    return p


def stage5(arm_params, arm_name, predicate="delivered_floor_10t"):
    print(f"\n== Stage 5 (lambda bisection, {arm_name}, {predicate}) ==")
    power_ext = RECORD_POWER + (100.0, 200.0)
    if not closes(lam_params(1.0, arm_params), predicate, power=power_ext):
        print("  aspirational endpoint does NOT close; no lambda threshold")
        return {"lambda_threshold": None, "endpoint_closes": False}
    lo, hi = 0.0, 1.0
    while hi - lo > 0.02:
        mid = 0.5 * (lo + hi)
        if closes(lam_params(mid, arm_params), predicate, power=power_ext):
            hi = mid
        else:
            lo = mid
    print(f"  lambda* = {hi:.3f}")
    return {"lambda_threshold": round(hi, 3), "endpoint_closes": True,
            "direction": {k: list(v) for k, v in ASPIRATIONAL.items()}}


# ------------------------------------------------------------------ #
# Main
# ------------------------------------------------------------------ #

def main():
    results = {"oracle": "saturn_water_v1 closed-loop, record grid 6x5x5",
               "arms": {}}

    base = summarize(run_grid({}))
    print(f"Baseline replication: paths={base['paths']} "
          f"arrived={base['arrived_at_depot']} taxonomy={base['taxonomy']}")
    assert base["paths"] == 1744 and base["arrived_at_depot"] == 0
    results["baseline"] = base

    for arm_name, arm_params in (("armA_record", {}), ("armB_honest", ARM_B_PARAMS)):
        arm = {}
        arm["stage1"] = stage1(arm_params, arm_name)
        arm["stage2"] = stage2(arm_params, arm_name)
        arm["stage4"] = stage4(arm_params, arm_name)
        arm["stage5"] = stage5(arm_params, arm_name)
        results["arms"][arm_name] = arm

    results["oracle_calls"] = _oracle_calls
    out = HERE / "results"
    out.mkdir(exist_ok=True)
    with open(out / "boundary_results.json", "w") as f:
        json.dump(results, f, indent=1)
    print(f"\noracle calls: {_oracle_calls}")
    print(f"wrote {out / 'boundary_results.json'}")


if __name__ == "__main__":
    main()
