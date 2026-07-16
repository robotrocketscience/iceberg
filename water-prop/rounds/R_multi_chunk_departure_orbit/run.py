"""R-multi-chunk-departure-orbit — correct multi-chunk math for B-ring departure delta-velocity.

Same Tsiolkovsky model as R-multi-chunk-per-mission, but tests both
Case BR-direct (Δv=40.2 km/s, B-ring direct departure) and
Case HE-graze (Δv=24.4 km/s, ring-grazing from high-elliptical).
"""

from __future__ import annotations

import math
import json
from pathlib import Path

ROUND_DIR = Path(__file__).resolve().parent
RESULTS_DIR = ROUND_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)


V_E_KM_S = 19.62
DV_RING_TRAVERSAL_KM_S = 0.10
M_DRY_STRUCTURAL_T = 50.0

CASES = {
    "BR_direct": 40.2,
    "HE_graze":  24.4,
}

N_SWEEP = [1, 2, 3, 5, 8, 10, 15, 20, 25]
M_EACH_SWEEP_T = [200.0, 482.0]

HURDLE_TONNES = {
    "sovereign_bond_4pct":       220.0,
    "regulated_utility_8pct":    460.0,
    "corporate_growth_10pct":    700.0,
    "venture_class_15pct_extrap": 1200.0,
}


def delivered_chunk_t(n: int, m_each: float, m_dry: float, dv_base: float) -> dict:
    dv_total = dv_base + (n - 1) * DV_RING_TRAVERSAL_KM_S
    R = math.exp(dv_total / V_E_KM_S)
    captured = n * m_each
    delivered = (captured + m_dry) / R - m_dry
    delivered = max(0.0, delivered)
    return {
        "n": n, "m_each_t": m_each, "m_dry_t": m_dry,
        "dv_total_km_s": dv_total, "mass_ratio": R,
        "captured_t": captured, "delivered_t": delivered,
        "delivered_fraction": delivered / captured if captured > 0 else 0.0,
    }


def min_n_for_delivery(target_t: float, m_each: float, m_dry: float, dv_base: float,
                        n_max: int = 100) -> int | None:
    """Smallest integer N such that delivered_t >= target_t."""
    for n in range(1, n_max + 1):
        r = delivered_chunk_t(n, m_each, m_dry, dv_base)
        if r["delivered_t"] >= target_t:
            return n
    return None


# ---------------------------------------------------------------------------
# IRR cashflow (same as R-multi-chunk-per-mission)
# ---------------------------------------------------------------------------

DEMONSTRATOR_NRE = 500e6
GROUND_OPS_PER_YEAR = 50e6
ROUND_TRIP_YR_MARVL = 14.5
HORIZON_YR = 45
SHIP_COST_NEW = 650e6
PRICE_PER_KG = 10000.0
SOVEREIGN_AMOUNT = 2e9
SOVEREIGN_YEAR = 11


def build_fleet_schedule(horizon_yr: int = HORIZON_YR):
    s = [{"ship_no": 1, "launch_year": 0.0}, {"ship_no": 2, "launch_year": 7.0}]
    ship_no = 3
    year = 8.0
    while year < horizon_yr:
        s.append({"ship_no": ship_no, "launch_year": year})
        ship_no += 1
        year += 13.0 / 12.0
    return s


def cashflow_yearly(delivered_t: float, launch_plus_tsi: float, horizon_yr: int = HORIZON_YR):
    s = build_fleet_schedule(horizon_yr)
    y = {yr: {"cost": 0.0, "revenue": 0.0} for yr in range(horizon_yr)}
    y[0]["cost"] += DEMONSTRATOR_NRE
    for ship in s:
        ly = int(ship["launch_year"])
        if ly >= horizon_yr:
            continue
        y[ly]["cost"] += SHIP_COST_NEW + launch_plus_tsi
        dy = ly + int(round(ROUND_TRIP_YR_MARVL))
        if dy < horizon_yr:
            y[dy]["revenue"] += delivered_t * 1000.0 * PRICE_PER_KG
    for yr in range(horizon_yr):
        y[yr]["cost"] += GROUND_OPS_PER_YEAR
    if 0 <= SOVEREIGN_YEAR < horizon_yr:
        y[SOVEREIGN_YEAR]["revenue"] += SOVEREIGN_AMOUNT
    return y


def npv(y, rate, horizon=HORIZON_YR):
    return sum((y[t]["revenue"] - y[t]["cost"]) / ((1 + rate) ** t) for t in range(horizon))


def perp_tv(y, rate, horizon=HORIZON_YR):
    last5 = [y[t]["revenue"] - y[t]["cost"] for t in range(horizon - 5, horizon)]
    cf = sum(last5) / 5.0
    if cf <= 0 or rate <= 0:
        return 0.0
    return cf / rate / ((1 + rate) ** horizon)


def irr_bisect(y, horizon=HORIZON_YR):
    def f(r):
        return npv(y, r, horizon) + perp_tv(y, r, horizon)
    lo, hi = 1e-4, 0.50
    if f(lo) <= 0:
        return None
    if f(hi) > 0:
        return hi
    for _ in range(70):
        mid = 0.5 * (lo + hi)
        if f(mid) > 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


# ---------------------------------------------------------------------------
# Main sweep
# ---------------------------------------------------------------------------

def main() -> None:
    rows = []
    for case_name, dv_base in CASES.items():
        for m_each in M_EACH_SWEEP_T:
            for n in N_SWEEP:
                r = delivered_chunk_t(n, m_each, M_DRY_STRUCTURAL_T, dv_base)
                irrs = {}
                for launch_M, label in [(290, "current_290M"), (50, "starship_50M")]:
                    y = cashflow_yearly(r["delivered_t"], launch_M * 1e6)
                    i = irr_bisect(y)
                    irrs[label] = round(i * 100, 2) if i is not None else None
                # Hurdle classification
                d = r["delivered_t"]
                if d >= HURDLE_TONNES["venture_class_15pct_extrap"]:
                    hurdle = "venture_class_15pct"
                elif d >= HURDLE_TONNES["corporate_growth_10pct"]:
                    hurdle = "corporate_growth_10pct"
                elif d >= HURDLE_TONNES["regulated_utility_8pct"]:
                    hurdle = "regulated_utility_8pct"
                elif d >= HURDLE_TONNES["sovereign_bond_4pct"]:
                    hurdle = "sovereign_bond_4pct"
                else:
                    hurdle = "below_sovereign_bond"
                rows.append({**r, "case": case_name, "dv_base_km_s": dv_base,
                             "irr_pct": irrs, "hurdle_class": hurdle})

    # Minimum-N for each hurdle, under each case, at M_each=482, structural
    min_n = {}
    for case_name, dv_base in CASES.items():
        min_n[case_name] = {}
        for m_each in M_EACH_SWEEP_T:
            min_n[case_name][f"M_each_{int(m_each)}"] = {}
            for hurdle_name, target in HURDLE_TONNES.items():
                n_req = min_n_for_delivery(target, m_each, M_DRY_STRUCTURAL_T, dv_base)
                min_n[case_name][f"M_each_{int(m_each)}"][hurdle_name] = n_req

    # Comparison: ratio of HE-graze delivered to BR-direct delivered at each N
    ratio_table = {}
    for m_each in M_EACH_SWEEP_T:
        ratio_table[f"M_each_{int(m_each)}"] = {}
        for n in N_SWEEP:
            r_he = delivered_chunk_t(n, m_each, M_DRY_STRUCTURAL_T, 24.4)
            r_br = delivered_chunk_t(n, m_each, M_DRY_STRUCTURAL_T, 40.2)
            ratio = r_he["delivered_t"] / r_br["delivered_t"] if r_br["delivered_t"] > 0 else None
            ratio_table[f"M_each_{int(m_each)}"][f"N_{n}"] = round(ratio, 3) if ratio else None

    # Pre-registration grading
    grading = grade_predictions(rows, min_n, ratio_table)

    result = {
        "rows": rows,
        "min_n_for_hurdle": min_n,
        "he_to_br_delivered_ratio": ratio_table,
        "grading": grading,
        "constants": {
            "v_e_km_s": V_E_KM_S,
            "cases": CASES,
            "m_dry_structural_t": M_DRY_STRUCTURAL_T,
            "hurdles_t": HURDLE_TONNES,
        },
    }

    out_path = RESULTS_DIR / "departure_orbit_sweep.json"
    with out_path.open("w") as f:
        json.dump(result, f, indent=2)

    print("\nDELIVERED MASS AND IRR — M_each=482 t, structural anchor (m_dry=50 t)\n")
    print(f"{'case':<11} {'N':>3} {'captured':>9} {'delivered':>10} {'frac':>6} {'hurdle':>22} {'IRR@290M':>10} {'IRR@50M':>9}")
    for case_name in CASES:
        for r in [x for x in rows if x["case"] == case_name and x["m_each_t"] == 482.0]:
            h = r["hurdle_class"].replace("_", " ")
            irr1 = r["irr_pct"]["current_290M"]
            irr2 = r["irr_pct"]["starship_50M"]
            irr1_s = f"{irr1:>9.2f}%" if irr1 is not None else "    None"
            irr2_s = f"{irr2:>8.2f}%" if irr2 is not None else "    None"
            print(f"{case_name:<11} {r['n']:>3} {r['captured_t']:>9.0f} {r['delivered_t']:>10.1f} {r['delivered_fraction']*100:>5.1f}% {h:>22} {irr1_s} {irr2_s}")

    print("\nMINIMUM N CHUNKS FOR EACH HURDLE (M_each=482, structural)\n")
    print(f"{'hurdle':>30}  {'BR-direct':>10}  {'HE-graze':>10}")
    for hurdle in HURDLE_TONNES:
        n_br = min_n['BR_direct']['M_each_482'][hurdle]
        n_he = min_n['HE_graze']['M_each_482'][hurdle]
        n_br_s = f"N={n_br}" if n_br else "unreachable"
        n_he_s = f"N={n_he}" if n_he else "unreachable"
        print(f"{hurdle:>30}  {n_br_s:>10}  {n_he_s:>10}")

    print("\nHE-GRAZE / BR-DIRECT DELIVERED RATIO (M_each=482)\n")
    for n in N_SWEEP:
        ratio = ratio_table['M_each_482'][f'N_{n}']
        print(f"  N={n:>3}: {ratio if ratio else 'N/A'}")

    print("\nPre-registration grading:")
    for hid, g in grading.items():
        print(f"  {hid}: {g['verdict']:<25} — {g['note']}")


def grade_predictions(rows, min_n, ratio_table):
    out = {}

    def find(case, n, m_each):
        return next((r for r in rows if r["case"] == case and r["n"] == n
                                       and r["m_each_t"] == m_each), None)

    def grade_range(obs, lo, hi, flo, fhi):
        if lo <= obs <= hi:
            return "held"
        if flo <= obs <= fhi:
            return "wrong-but-informative"
        return "wrong-and-load-bearing"

    # H-dvc-a: delivered fraction N=1, 482 t, BR-direct ∈ [11, 14]%
    r = find("BR_direct", 1, 482.0)
    obs = r["delivered_fraction"] * 100
    out["H-dvc-a"] = {"observed_pct": round(obs, 2), "predicted_pct": [11, 14],
                      "verdict": grade_range(obs, 11, 14, 9, 16),
                      "note": f"delivered fraction N=1, 482 t, BR-direct: {obs:.1f}%"}

    # H-dvc-b: delivered tonnes N=5, 482, BR-direct ∈ [240, 290]
    r = find("BR_direct", 5, 482.0)
    obs = r["delivered_t"]
    out["H-dvc-b"] = {"observed_t": round(obs, 1), "predicted_t": [240, 290],
                      "verdict": grade_range(obs, 240, 290, 200, 340),
                      "note": f"delivered N=5×482, BR-direct: {obs:.1f} t"}

    # H-dvc-c: delivered tonnes N=8, 482, BR-direct ∈ [420, 490]
    r = find("BR_direct", 8, 482.0)
    obs = r["delivered_t"]
    out["H-dvc-c"] = {"observed_t": round(obs, 1), "predicted_t": [420, 490],
                      "verdict": grade_range(obs, 420, 490, 380, 530),
                      "note": f"delivered N=8×482, BR-direct: {obs:.1f} t"}

    # H-dvc-d: minimum N for corporate-growth (700 t) under BR-direct ∈ [15, 17]
    n_obs = min_n['BR_direct']['M_each_482']['corporate_growth_10pct']
    if n_obs is None:
        v = "wrong-and-load-bearing"; note = "corporate-growth unreachable under BR-direct"
    else:
        v = grade_range(n_obs, 15, 17, 13, 20); note = f"min N for corp-growth under BR-direct: {n_obs}"
    out["H-dvc-d"] = {"observed_N": n_obs, "predicted_N": [15, 17], "verdict": v, "note": note}

    # H-dvc-e: minimum N for venture-class (1200 t) under BR-direct ∈ [20, 25]
    n_obs = min_n['BR_direct']['M_each_482']['venture_class_15pct_extrap']
    if n_obs is None:
        v = "wrong-and-load-bearing"; note = "venture-class unreachable under BR-direct"
    else:
        v = grade_range(n_obs, 20, 25, 18, 30); note = f"min N for venture-class under BR-direct: {n_obs}"
    out["H-dvc-e"] = {"observed_N": n_obs, "predicted_N": [20, 25], "verdict": v, "note": note}

    # H-dvc-f: asymptotic delivered fraction under BR-direct = 1/R ∈ [12.5, 13.5]%
    R_br = math.exp(40.2 / V_E_KM_S)
    obs = 100.0 / R_br
    out["H-dvc-f"] = {"observed_pct": round(obs, 2), "predicted_pct": [12.5, 13.5],
                      "verdict": grade_range(obs, 12.5, 13.5, 12, 14),
                      "note": f"asymptotic delivered fraction under BR-direct (1/R): {obs:.2f}%"}

    # H-dvc-g: HE-graze / BR-direct ratio at N=5 ∈ [2.0, 2.5]
    obs = ratio_table['M_each_482']['N_5']
    out["H-dvc-g"] = {"observed_ratio": obs, "predicted_ratio": [2.0, 2.5],
                      "verdict": grade_range(obs, 2.0, 2.5, 1.8, 2.8),
                      "note": f"HE-graze/BR-direct delivered ratio at N=5, 482 t: {obs:.2f}×"}

    # H-dvc-h: IRR at N=5×482, BR-direct, $50M Starship ∈ [5, 9]
    r = find("BR_direct", 5, 482.0)
    obs = r["irr_pct"]["starship_50M"]
    if obs is None:
        v = "incomputable"; note = "IRR failed"
    else:
        v = grade_range(obs, 5, 9, 3, 11); note = f"IRR N=5×482, BR-direct, $50M: {obs:.2f}%"
    out["H-dvc-h"] = {"observed_pct": obs, "predicted_pct": [5, 9], "verdict": v, "note": note}

    return out


if __name__ == "__main__":
    main()
