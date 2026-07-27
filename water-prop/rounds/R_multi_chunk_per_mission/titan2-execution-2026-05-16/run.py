"""R-multi-chunk-per-mission — Tsiolkovsky chunk-fed scaling under N-chunk captures.

Question: under multi-chunk capture, does delivered mass cross corporate-growth
hurdle (~700 t/ship per R-delivery-irr-curve)? And what does the marginal-IRR
look like as N rises?

Inputs:
- Inbound delta-velocity 24.4 km/s (rhea-2 round 3 Scenario B all-electric)
- Water electric thruster specific impulse 2000 s, v_e = 19.62 km/s
- Ring-traversal Δv 100 m/s per inter-chunk transit (conservative midpoint)
- Dry mass: two anchors — rhea-2 face-value 8.27 t (implausible) and structural 50 t

Outputs:
- (N, M_each, m_dry) → captured, delivered, delivered_fraction
- IRR at delivered values under $290M and $50M launch costs
- Probabilistic delivered under per-capture p ∈ {0.85, 0.95}
- Pre-registration grading
"""

from __future__ import annotations

import math
import json
from pathlib import Path

ROUND_DIR = Path(__file__).resolve().parent
RESULTS_DIR = ROUND_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------------------------
# Tsiolkovsky chunk-fed model
# ---------------------------------------------------------------------------

DV_INBOUND_KM_S = 24.4              # rhea-2 round 3 Scenario B all-electric total
V_E_KM_S = 19.62                    # specific impulse 2000 s, water electric
DV_RING_TRAVERSAL_KM_S = 0.10       # per inter-chunk hop, conservative midpoint
M_DRY_FACE_VALUE_T = 8.27           # calibrated to rhea-2 50 t → 8.51 t at 24.4 km/s
M_DRY_STRUCTURAL_T = 50.0           # plausible 500-kWe vehicle without chunk

N_SWEEP = [1, 2, 3, 5, 8, 10]
M_EACH_SWEEP_T = [100.0, 200.0, 482.0]
P_CAPTURE_SWEEP = [0.85, 0.95]
M_DRY_SWEEP = [("face_value", M_DRY_FACE_VALUE_T), ("structural", M_DRY_STRUCTURAL_T)]

# Hurdle anchors from R-delivery-irr-curve
HURDLE_TONNES = {
    "sovereign_bond_4pct": 220.0,
    "regulated_utility_8pct": 460.0,
    "corporate_growth_10pct": 700.0,
    "venture_class_15pct_extrap": 1200.0,  # extrapolation; R-delivery-irr-curve only swept to 2000
}


def delivered_chunk_t(n_chunks: int, m_each_t: float, m_dry_t: float,
                       dv_extra_km_s: float = 0.0) -> dict:
    """Compute delivered chunk mass under chunk-fed Tsiolkovsky.

    Total Δv = inbound + (N-1)*ring-traversal + dv_extra.
    Mass at start of inbound = N × M_each + m_dry.
    Mass at end of inbound  = (delivered chunk) + m_dry.
    """
    captured = n_chunks * m_each_t
    dv_total = DV_INBOUND_KM_S + (n_chunks - 1) * DV_RING_TRAVERSAL_KM_S + dv_extra_km_s
    R = math.exp(dv_total / V_E_KM_S)
    delivered = (captured + m_dry_t) / R - m_dry_t
    delivered = max(0.0, delivered)
    return {
        "n": n_chunks,
        "m_each_t": m_each_t,
        "m_dry_t": m_dry_t,
        "captured_t": captured,
        "dv_total_km_s": dv_total,
        "mass_ratio": R,
        "delivered_t": delivered,
        "delivered_fraction": delivered / captured if captured > 0 else 0.0,
    }


# ---------------------------------------------------------------------------
# IRR cashflow (copied from R-launch-cost-sensitivity for self-contained run)
# ---------------------------------------------------------------------------

DEMONSTRATOR_NRE = 500e6
GROUND_OPS_PER_YEAR = 50e6
ROUND_TRIP_YR_MARVL = 14.5
HORIZON_YR = 45
SHIP_COST_NEW = 650e6
PRICE_PER_KG = 10000.0
SOVEREIGN_AMOUNT = 2e9
SOVEREIGN_YEAR = 11


def build_fleet_schedule(horizon_yr: int = HORIZON_YR) -> list[dict]:
    schedule = [{"ship_no": 1, "launch_year": 0.0},
                {"ship_no": 2, "launch_year": 7.0}]
    ship_no = 3
    year = 8.0
    while year < horizon_yr:
        schedule.append({"ship_no": ship_no, "launch_year": year})
        ship_no += 1
        year += 13.0 / 12.0
    return schedule


def cashflow_yearly(delivered_t: float, launch_plus_tsi: float,
                     horizon_yr: int = HORIZON_YR) -> dict[int, dict]:
    schedule = build_fleet_schedule(horizon_yr)
    yearly = {yr: {"cost": 0.0, "revenue": 0.0} for yr in range(horizon_yr)}
    yearly[0]["cost"] += DEMONSTRATOR_NRE
    for ship in schedule:
        ly = int(ship["launch_year"])
        if ly >= horizon_yr:
            continue
        yearly[ly]["cost"] += SHIP_COST_NEW + launch_plus_tsi
        dy = ly + int(round(ROUND_TRIP_YR_MARVL))
        if dy < horizon_yr:
            yearly[dy]["revenue"] += delivered_t * 1000.0 * PRICE_PER_KG
    for yr in range(horizon_yr):
        yearly[yr]["cost"] += GROUND_OPS_PER_YEAR
    if 0 <= SOVEREIGN_YEAR < horizon_yr:
        yearly[SOVEREIGN_YEAR]["revenue"] += SOVEREIGN_AMOUNT
    return yearly


def npv(yearly: dict, rate: float, horizon: int = HORIZON_YR) -> float:
    return sum((yearly[t]["revenue"] - yearly[t]["cost"]) / ((1.0 + rate) ** t)
               for t in range(horizon))


def perpetuity_terminal_value(yearly: dict, rate: float, horizon: int = HORIZON_YR) -> float:
    last5 = [yearly[t]["revenue"] - yearly[t]["cost"] for t in range(horizon - 5, horizon)]
    cf_terminal = sum(last5) / 5.0
    if cf_terminal <= 0 or rate <= 0:
        return 0.0
    return cf_terminal / rate / ((1.0 + rate) ** horizon)


def irr_bisect(yearly: dict, horizon: int = HORIZON_YR) -> float | None:
    def f(r):
        return npv(yearly, r, horizon) + perpetuity_terminal_value(yearly, r, horizon)
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
    for n in N_SWEEP:
        for m_each in M_EACH_SWEEP_T:
            for anchor_name, m_dry in M_DRY_SWEEP:
                r = delivered_chunk_t(n, m_each, m_dry)
                # IRR at $290M and $50M launch cost
                irrs = {}
                for launch_M, label in [(290, "current_290M"), (50, "starship_50M")]:
                    y = cashflow_yearly(r["delivered_t"], launch_M * 1e6)
                    irr = irr_bisect(y)
                    irrs[label] = round(irr * 100, 2) if irr is not None else None
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
                rows.append({**r, "m_dry_anchor": anchor_name,
                             "irr_pct": irrs, "hurdle_class": hurdle})

    # Probabilistic accounting: all-N-success only
    prob_rows = []
    for n in N_SWEEP:
        for p in P_CAPTURE_SWEEP:
            full_success_p = p ** n
            # At the M_each=482, m_dry=structural anchor (most pessimistic)
            r = delivered_chunk_t(n, 482.0, M_DRY_STRUCTURAL_T)
            expected_delivered_binary = full_success_p * r["delivered_t"]
            prob_rows.append({
                "n": n,
                "p_capture": p,
                "full_success_p": round(full_success_p, 4),
                "full_success_delivered_t": round(r["delivered_t"], 1),
                "expected_delivered_binary_t": round(expected_delivered_binary, 1),
            })

    # Pre-registration grading
    grading = grade_predictions(rows, prob_rows)

    result = {
        "rows": rows,
        "prob_rows": prob_rows,
        "grading": grading,
        "constants": {
            "dv_inbound_km_s": DV_INBOUND_KM_S,
            "v_e_km_s": V_E_KM_S,
            "dv_ring_traversal_km_s": DV_RING_TRAVERSAL_KM_S,
            "m_dry_anchors_t": dict(M_DRY_SWEEP),
            "hurdles_t": HURDLE_TONNES,
        },
    }

    out_path = RESULTS_DIR / "multi_chunk_sweep.json"
    with out_path.open("w") as f:
        json.dump(result, f, indent=2)

    # Console tables
    print("\nDELIVERED MASS AND IRR — M_each=482 t (B-ring single-chunk physical cap)\n")
    print(f"{'N':>3} {'dry':>10} {'captured':>10} {'delivered':>10} {'frac':>7} {'hurdle':>22} {'IRR@290M':>10} {'IRR@50M':>9}")
    for r in [x for x in rows if x["m_each_t"] == 482.0]:
        h = r["hurdle_class"].replace("_", " ")
        print(f"{r['n']:>3} {r['m_dry_anchor']:>10} {r['captured_t']:>10.0f} {r['delivered_t']:>10.1f} {r['delivered_fraction']*100:>6.1f}% {h:>22} "
              f"{r['irr_pct']['current_290M'] if r['irr_pct']['current_290M'] is not None else 'None':>9}% "
              f"{r['irr_pct']['starship_50M'] if r['irr_pct']['starship_50M'] is not None else 'None':>8}%")

    print("\nDELIVERED MASS — M_each=200 t (per-chunk class likely under realistic chunk-availability)\n")
    print(f"{'N':>3} {'dry':>10} {'captured':>10} {'delivered':>10} {'frac':>7} {'hurdle':>22}")
    for r in [x for x in rows if x["m_each_t"] == 200.0]:
        h = r["hurdle_class"].replace("_", " ")
        print(f"{r['n']:>3} {r['m_dry_anchor']:>10} {r['captured_t']:>10.0f} {r['delivered_t']:>10.1f} {r['delivered_fraction']*100:>6.1f}% {h:>22}")

    print("\nPROBABILISTIC ACCOUNTING (M_each=482 t, structural dry anchor)\n")
    print(f"{'N':>3} {'p_capture':>10} {'full_success_p':>15} {'all-success delivered':>22} {'expected delivered (binary)':>28}")
    for p in prob_rows:
        print(f"{p['n']:>3} {p['p_capture']:>10.2f} {p['full_success_p']:>15.4f} {p['full_success_delivered_t']:>21.1f} t {p['expected_delivered_binary_t']:>26.1f} t")

    print("\nPre-registration grading:")
    for hid, g in grading.items():
        print(f"  {hid}: {g['verdict']:<25} — {g['note']}")


def grade_predictions(rows: list[dict], prob_rows: list[dict]) -> dict:
    out = {}

    def find(n, m_each, anchor):
        return next((r for r in rows if r["n"] == n and r["m_each_t"] == m_each
                                       and r["m_dry_anchor"] == anchor), None)

    def grade_range(obs, pred_lo, pred_hi, fals_lo, fals_hi):
        if pred_lo <= obs <= pred_hi:
            return "held"
        if fals_lo <= obs <= fals_hi:
            return "wrong-but-informative"
        return "wrong-and-load-bearing"

    # H-mc-a: delivered fraction at N=1, M_each=482, structural anchor ∈ [28, 34]
    r = find(1, 482.0, "structural")
    obs = r["delivered_fraction"] * 100
    v = grade_range(obs, 28, 34, 25, 38)
    out["H-mc-a"] = {"observed_pct": round(obs, 2), "predicted_pct": [28, 34], "verdict": v,
                       "note": f"delivered fraction at N=1, 482 t, structural dry: {obs:.1f}%"}

    # H-mc-b: delivered fraction at N=3, M_each=482, structural ∈ [35, 42]
    r = find(3, 482.0, "structural")
    obs = r["delivered_fraction"] * 100
    v = grade_range(obs, 35, 42, 30, 47)
    out["H-mc-b"] = {"observed_pct": round(obs, 2), "predicted_pct": [35, 42], "verdict": v,
                       "note": f"delivered fraction at N=3, 482 t each, structural dry: {obs:.1f}%"}

    # H-mc-c: delivered fraction at N=5, M_each=482, structural ∈ [38, 45]
    r = find(5, 482.0, "structural")
    obs = r["delivered_fraction"] * 100
    v = grade_range(obs, 38, 45, 33, 50)
    out["H-mc-c"] = {"observed_pct": round(obs, 2), "predicted_pct": [38, 45], "verdict": v,
                       "note": f"delivered fraction at N=5, 482 t each, structural dry: {obs:.1f}%"}

    # H-mc-d: delivered tonnes at N=3, M_each=482, structural ∈ [500, 600]
    r = find(3, 482.0, "structural")
    obs = r["delivered_t"]
    v = grade_range(obs, 500, 600, 430, 680)
    out["H-mc-d"] = {"observed_t": round(obs, 1), "predicted_t": [500, 600], "verdict": v,
                       "note": f"delivered at N=3×482 t, structural dry: {obs:.1f} t (corp-growth threshold 700 t)"}

    # H-mc-e: delivered tonnes at N=5, M_each=482, structural ∈ [850, 1000]
    r = find(5, 482.0, "structural")
    obs = r["delivered_t"]
    v = grade_range(obs, 850, 1000, 800, 1200)
    out["H-mc-e"] = {"observed_t": round(obs, 1), "predicted_t": [850, 1000], "verdict": v,
                       "note": f"delivered at N=5×482 t, structural dry: {obs:.1f} t"}

    # H-mc-f: IRR uplift from N=1 to N=3 at M_each=482, structural, $290M launch
    r1 = find(1, 482.0, "structural")
    r3 = find(3, 482.0, "structural")
    irr1 = r1["irr_pct"]["current_290M"]
    irr3 = r3["irr_pct"]["current_290M"]
    obs = (irr3 - irr1) if (irr1 is not None and irr3 is not None) else None
    if obs is None:
        out["H-mc-f"] = {"verdict": "incomputable", "note": "one or both IRRs failed to converge"}
    else:
        v = grade_range(obs, 2, 4, 1, 5)
        out["H-mc-f"] = {"observed_pp": round(obs, 2), "predicted_pp": [2, 4], "verdict": v,
                          "note": f"IRR uplift N=1→N=3 (482 t each, structural, $290M): +{obs:.2f}pp"}

    # H-mc-g: IRR at N=5×482 under $50M Starship launch ∈ [14, 18]
    r5 = find(5, 482.0, "structural")
    obs = r5["irr_pct"]["starship_50M"]
    if obs is None:
        out["H-mc-g"] = {"verdict": "incomputable", "note": "IRR failed"}
    else:
        v = grade_range(obs, 14, 18, 12, 20)
        out["H-mc-g"] = {"observed_pct": obs, "predicted_pct": [14, 18], "verdict": v,
                          "note": f"IRR at N=5×482 t (structural, $50M launch): {obs:.2f}%"}

    # H-mc-h: probability check
    p3 = next(p for p in prob_rows if p["n"] == 3 and p["p_capture"] == 0.85)
    p5 = next(p for p in prob_rows if p["n"] == 5 and p["p_capture"] == 0.85)
    pred_p3, pred_p5 = 0.61, 0.44
    obs_p3, obs_p5 = p3["full_success_p"], p5["full_success_p"]
    held = abs(obs_p3 - pred_p3) <= 0.05 and abs(obs_p5 - pred_p5) <= 0.05
    out["H-mc-h"] = {"observed_p3": obs_p3, "observed_p5": obs_p5, "verdict": "held" if held else "falsified",
                      "note": f"P(all-N-success | p=0.85): N=3 → {obs_p3}, N=5 → {obs_p5}"}

    return out


if __name__ == "__main__":
    main()
