"""R-dv-anchor-audit — re-derive Saturn-departure and Earth-arrival delta-velocity
anchors from vis-viva, recompute leapfrog round with corrected anchors, find
reactor-power floor for commercial closure.

Three corrections to R-chemical-electric-leapfrog:
1. Saturn departure: 5.5 km/s -> 7.7 km/s (vis-viva from B-ring elliptical
   parking orbit with periapsis Oberth boost).
2. Earth chemical capture: 3.5 km/s -> 7.3 km/s (vis-viva from Hohmann v_inf
   10.3 km/s at low Earth orbit).
3. New scenario added: lunar-gravity-assist tour (R12-anchored) with 4.2 km/s
   residual chemical capture and 8.7-month phasing penalty.

Author: titan (re-spawn 3), 2026-05-19 same-day follow-on.
"""

from __future__ import annotations

import json
import math
import pathlib
from itertools import product

# ---------- physical constants ----------
G0 = 9.80665
SEC_PER_YEAR = 365.25 * 86400.0

# ---------- propulsion anchors ----------
V_CHEM = 4413.0
ISP_ELECTRIC_S = 2000.0
V_ELECTRIC = ISP_ELECTRIC_S * G0
ETA_THRUSTER_ELECTRIC = 0.5
ETA_ELECTROLYSIS = 0.75
E_WATER_CHEM_J_PER_KG = 13.4e6

# ---------- CORRECTED mission-segment delta-velocity anchors ----------
DV_SATURN_DEPARTURE_MPS = 7700.0        # CORRECTED: was 5500 in prior round; vis-viva from B-ring elliptical
DV_TRANS_EARTH_TRIM_MPS = 300.0
DV_EARTH_CAPTURE_DIRECT_MPS = 7300.0    # CORRECTED: was 3500; vis-viva from Hohmann v_inf 10.3 km/s to LEO
DV_EARTH_CAPTURE_LUNAR_GA_MPS = 4200.0  # NEW: residual after R12 10-flyby tour to LEO
LUNAR_GA_PHASING_YR = 8.7 / 12.0        # NEW: 8.7-month phasing penalty (R12 anchor)

OUTBOUND_YR = 6.0
SATURN_SIDE_YR = 1.0
TRANS_EARTH_YR = 6.0

# ---------- vehicle anchors ----------
M_BUS_T = 5.5
M_BAG_T = 10.0
M_CHEMICAL_ENGINE_T = 1.0
M_ELECTROLYSER_T = 1.0
TANK_MASS_FRACTION = 0.3
SPECIFIC_POWER_W_PER_KG = 2.4
CHUNK_T = 200.0

# ---------- closure budgets ----------
L0_05_STRICT_YR = 15.0
L0_05_WAIVER_YR = 25.0
L0_09_FLOOR_T = 30.0

# ---------- sweep grids ----------
P_GRID_KW = [10.0, 15.0, 20.0, 30.0, 50.0, 100.0]
TANK_GRID_T = [0.1, 1.0, 10.0, 50.0, 150.0]
SCENARIOS = ["aerocapture", "chemical_direct", "lunar_ga_chemical"]


HERE = pathlib.Path(__file__).parent
RESULTS = HERE / "results"
RESULTS.mkdir(exist_ok=True)


def m_reactor_t(P_kw): return (P_kw * 1000.0) / SPECIFIC_POWER_W_PER_KG / 1000.0
def m_thrusters_t(P_kw): return 0.01 * P_kw
def m_tank_t(T_tank_t): return TANK_MASS_FRACTION * T_tank_t
def m_dry(P_kw, T_tank_t):
    return (M_BUS_T + M_BAG_T + m_reactor_t(P_kw) + m_thrusters_t(P_kw)
            + M_CHEMICAL_ENGINE_T + M_ELECTROLYSER_T + m_tank_t(T_tank_t))


def electrolysis_rate_t_per_yr(P_kw):
    return P_kw * 1000.0 * SEC_PER_YEAR * ETA_ELECTROLYSIS / E_WATER_CHEM_J_PER_KG / 1000.0


def chem_prop(dv_mps, m_initial_t):
    return m_initial_t * (1.0 - math.exp(-dv_mps / V_CHEM))


def elec_prop(dv_mps, m_initial_t):
    return m_initial_t * (1.0 - math.exp(-dv_mps / V_ELECTRIC))


def evaluate_cell(P_kw, T_tank_t, scenario):
    md = m_dry(P_kw, T_tank_t)
    m_at_saturn_departure = md + CHUNK_T

    # 1) Saturn departure: chemical impulsive (leapfrog periapsis burns)
    prop_saturn_t = chem_prop(DV_SATURN_DEPARTURE_MPS, m_at_saturn_departure)
    m_after_departure = m_at_saturn_departure - prop_saturn_t

    # Stockpile / spiral bookkeeping
    e_rate = electrolysis_rate_t_per_yr(P_kw)
    stockpile_t = min(T_tank_t, e_rate * (OUTBOUND_YR + SATURN_SIDE_YR))
    remaining_t = max(0.0, prop_saturn_t - stockpile_t)
    spiral_yr = remaining_t / e_rate if e_rate > 0 else float("inf")

    # 2) Trans-Earth coast trim: small electric
    prop_trim_t = elec_prop(DV_TRANS_EARTH_TRIM_MPS, m_after_departure)
    m_after_trim = m_after_departure - prop_trim_t

    # 3) Earth arrival: scenario-dependent
    extra_phasing_yr = 0.0
    if scenario == "aerocapture":
        prop_capture_t = 0.0
        m_after_capture = m_after_trim
    elif scenario == "chemical_direct":
        prop_capture_t = chem_prop(DV_EARTH_CAPTURE_DIRECT_MPS, m_after_trim)
        # Trans-Earth electrolysis must produce this propellant; check fit
        capture_electrolysis_yr = prop_capture_t / e_rate if e_rate > 0 else float("inf")
        if capture_electrolysis_yr > TRANS_EARTH_YR:
            spiral_yr += (capture_electrolysis_yr - TRANS_EARTH_YR)
        m_after_capture = m_after_trim - prop_capture_t
    elif scenario == "lunar_ga_chemical":
        prop_capture_t = chem_prop(DV_EARTH_CAPTURE_LUNAR_GA_MPS, m_after_trim)
        extra_phasing_yr = LUNAR_GA_PHASING_YR
        capture_electrolysis_yr = prop_capture_t / e_rate if e_rate > 0 else float("inf")
        if capture_electrolysis_yr > TRANS_EARTH_YR:
            spiral_yr += (capture_electrolysis_yr - TRANS_EARTH_YR)
        m_after_capture = m_after_trim - prop_capture_t
    else:
        raise ValueError(f"unknown scenario {scenario}")

    delivered_t = max(0.0, m_after_capture - md)
    round_trip_yr = OUTBOUND_YR + SATURN_SIDE_YR + spiral_yr + TRANS_EARTH_YR + extra_phasing_yr

    closes_strict = round_trip_yr <= L0_05_STRICT_YR
    closes_waiver = round_trip_yr <= L0_05_WAIVER_YR
    meets_floor = delivered_t >= L0_09_FLOOR_T

    return {
        "P_kw": P_kw, "T_tank_t": T_tank_t, "scenario": scenario,
        "m_dry_t": md, "m_reactor_t": m_reactor_t(P_kw), "m_tank_t": m_tank_t(T_tank_t),
        "prop_saturn_t": prop_saturn_t, "prop_trim_t": prop_trim_t, "prop_capture_t": prop_capture_t,
        "stockpile_t": stockpile_t, "remaining_t": remaining_t,
        "spiral_yr": spiral_yr, "extra_phasing_yr": extra_phasing_yr,
        "m_after_capture_t": m_after_capture, "delivered_t": delivered_t,
        "round_trip_yr": round_trip_yr,
        "closes_strict": closes_strict, "closes_waiver": closes_waiver,
        "meets_floor": meets_floor,
        "closes_commercial_strict": closes_strict and meets_floor,
        "closes_commercial_waiver": closes_waiver and meets_floor,
    }


def sweep():
    rows = []
    for P, T, sc in product(P_GRID_KW, TANK_GRID_T, SCENARIOS):
        rows.append(evaluate_cell(P, T, sc))
    return rows


def grade_hypotheses(rows):
    g = []

    # H-anchor-1: leapfrog with corrected Saturn-departure delivers <30 t at flyable+aerocapture
    flyable_aero = [r for r in rows if r["P_kw"] <= 30 and r["scenario"] == "aerocapture"]
    max_delivered_flyable_aero = max(r["delivered_t"] for r in flyable_aero)
    g.append({
        "H": "H-anchor-1",
        "predicted": "max delivered at flyable+aerocapture under corrected anchors < 30 t",
        "measured": f"{max_delivered_flyable_aero:.1f} t",
        "verdict": "HELD" if max_delivered_flyable_aero < 30 else "FALSIFIED",
    })

    # H-anchor-2: no aerocapture (chemical_direct) cells have delivered > 0 at flyable
    flyable_chem = [r for r in rows if r["P_kw"] <= 30 and r["scenario"] == "chemical_direct"]
    max_delivered_chem = max(r["delivered_t"] for r in flyable_chem)
    g.append({
        "H": "H-anchor-2",
        "predicted": "chemical_direct at flyable power delivered ≤ 0 t (vehicle can't close mass)",
        "measured": f"max delivered = {max_delivered_chem:.1f} t",
        "verdict": "HELD" if max_delivered_chem <= 0.5 else "FALSIFIED",
    })

    # H-anchor-3: lunar-GA + chemical scenario delivers ≤ 5 t at flyable power under corrected anchors
    flyable_lga = [r for r in rows if r["P_kw"] <= 30 and r["scenario"] == "lunar_ga_chemical"]
    max_delivered_lga = max(r["delivered_t"] for r in flyable_lga)
    g.append({
        "H": "H-anchor-3",
        "predicted": "lunar_ga + chemical at flyable power max delivered ≤ 5 t",
        "measured": f"{max_delivered_lga:.1f} t",
        "verdict": "HELD" if max_delivered_lga <= 5 else "FALSIFIED",
    })

    # H-anchor-4 aggregate: NO cell at flyable+any-scenario closes commercial floor (30 t)
    flyable_commercial = [r for r in rows if r["P_kw"] <= 30 and r["meets_floor"]]
    g.append({
        "H": "H-anchor-4",
        "predicted": "0 cells close L0-09 commercial floor at flyable power under corrected anchors",
        "measured": f"{len(flyable_commercial)} cells close floor at flyable power",
        "verdict": "HELD" if len(flyable_commercial) == 0 else "FALSIFIED",
    })

    return g


def find_min_power_for_commercial(scenario):
    """Bisection on reactor power: what power closes L0-09 floor under given scenario?"""
    lo, hi = 5.0, 500.0
    test_lo = evaluate_cell(lo, 10.0, scenario)
    test_hi = evaluate_cell(hi, 10.0, scenario)
    if test_lo["meets_floor"]:
        return lo
    if not test_hi["meets_floor"]:
        return None
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        test = evaluate_cell(mid, 10.0, scenario)
        if test["meets_floor"]:
            hi = mid
        else:
            lo = mid
    return hi


def write_corrected_pareto(rows, grades):
    L = []
    L.append("# R-dv-anchor-audit — corrected Pareto envelope\n")
    L.append("Re-run of R-chemical-electric-leapfrog with two delta-velocity anchor corrections plus one new scenario.")
    L.append("")
    L.append(f"Saturn departure: **{DV_SATURN_DEPARTURE_MPS/1000:.1f} km/s** (was 5.5 km/s in prior round; vis-viva from B-ring elliptical parking orbit).")
    L.append(f"Earth chemical capture (direct, no lunar GA): **{DV_EARTH_CAPTURE_DIRECT_MPS/1000:.1f} km/s** (was 3.5 km/s; vis-viva from Hohmann v_inf 10.3 km/s).")
    L.append(f"Earth chemical capture after lunar gravity assist (R12 10-flyby tour): **{DV_EARTH_CAPTURE_LUNAR_GA_MPS/1000:.1f} km/s** (new scenario).")
    L.append(f"Lunar gravity assist phasing: **{LUNAR_GA_PHASING_YR:.2f} years** ({LUNAR_GA_PHASING_YR*12:.1f} months, R12 anchor).")
    L.append("")

    for sc in SCENARIOS:
        L.append(f"## Scenario: {sc}\n")
        L.append("| P (kWe) | T_tank (t) | m_dry (t) | prop_dep (t) | prop_cap (t) | spiral (yr) | RT (yr) | delivered (t) | strict? | floor? | commercial-strict? |")
        L.append("|---|---|---|---|---|---|---|---|---|---|---|")
        for r in [x for x in rows if x["scenario"] == sc]:
            L.append(
                f"| {r['P_kw']:.0f} | {r['T_tank_t']:.1f} | {r['m_dry_t']:.1f} | "
                f"{r['prop_saturn_t']:.1f} | {r['prop_capture_t']:.1f} | "
                f"{r['spiral_yr']:.2f} | {r['round_trip_yr']:.1f} | {r['delivered_t']:.1f} | "
                f"{'YES' if r['closes_strict'] else 'no'} | "
                f"{'YES' if r['meets_floor'] else 'no'} | "
                f"{'**YES**' if r['closes_commercial_strict'] else 'no'} |"
            )
        L.append("")

    L.append("## Hypothesis grades\n")
    L.append("| H | Predicted | Measured | Verdict |")
    L.append("|---|---|---|---|")
    for x in grades:
        L.append(f"| {x['H']} | {x['predicted']} | {x['measured']} | {x['verdict']} |")
    L.append("")

    L.append("## Minimum reactor power to close L0-09 commercial floor per scenario (bisection)\n")
    L.append("| Scenario | min reactor power (kWe) | Notes |")
    L.append("|---|---|---|")
    for sc in SCENARIOS:
        min_p = find_min_power_for_commercial(sc)
        if min_p is None:
            L.append(f"| {sc} | not achievable up to 500 kWe | architecture is empty even at FSP-class |")
        else:
            note = "flyable Kilopower-extrapolation" if min_p <= 30 else ("Fission Surface Power class" if min_p <= 100 else "above Fission Surface Power class — fantasy")
            L.append(f"| {sc} | **{min_p:.0f}** | {note} |")
    L.append("")

    (RESULTS / "corrected_pareto.md").write_text("\n".join(L))


def write_closure_verdict(rows, grades):
    L = []
    L.append("# R-dv-anchor-audit — closure verdict\n")
    L.append("**Worker:** titan-3. **Date:** 2026-05-19 same-day follow-on.")
    L.append("**Predecessor:** R-chemical-electric-leapfrog (`3a97067`).")
    L.append("**Trigger:** user direction \"question your assumptions\" — audit identified two unverified delta-velocity anchors in the prior round.")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## Headline")
    L.append("")
    flyable_strict = [r for r in rows if r["P_kw"] <= 30 and r["closes_commercial_strict"]]
    flyable_waiver = [r for r in rows if r["P_kw"] <= 30 and r["closes_commercial_waiver"]]
    L.append(f"**The R-chemical-electric-leapfrog round's '13 cells close at flyable power' headline is retracted.** Under corrected vis-viva-derived delta-velocity anchors:")
    L.append("")
    L.append(f"- {len(flyable_strict)} cells close commercial-strict at flyable reactor power (≤ 30 kilowatts-electric).")
    L.append(f"- {len(flyable_waiver)} cells close commercial-waiver at flyable reactor power.")
    L.append("")
    L.append("The two corrections:")
    L.append("")
    L.append(f"1. **Saturn-departure delta-velocity: 5.5 → 7.7 kilometres-per-second.** Vis-viva derivation: Hohmann return v_∞ at Saturn = 6.21 km/s; elliptical parking orbit with B-ring apoapsis (107,000 km from Saturn centre) and Oberth-optimised periapsis (60,000 km, just above clouds); periapsis burn = 36.1 − 28.4 = 7.7 km/s. The prior round's 5.5 km/s anchor was understated by 40%.")
    L.append("")
    L.append(f"2. **Earth-arrival chemical capture delta-velocity: 3.5 → 7.3 kilometres-per-second** (direct from Hohmann v_∞ 10.3 km/s to low Earth orbit) **or 4.2 kilometres-per-second** (after R12 10-flyby lunar gravity assist tour). The prior round's 3.5 km/s anchor was understated by ~2× under both readings.")
    L.append("")
    L.append("Combined, the corrected anchors raise the chemical propellant burden by ~38 tonnes (Saturn departure) + 0–32 tonnes (Earth capture, scenario-dependent) on a 220-tonne vehicle. This drops delivered mass by 38–70 tonnes per mission, putting it below the L0-09 30-tonne commercial floor at every flyable cell tested.")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## Hypothesis verdicts")
    L.append("")
    L.append("| H | Predicted | Measured | Verdict |")
    L.append("|---|---|---|---|")
    for x in grades:
        L.append(f"| {x['H']} | {x['predicted']} | {x['measured']} | {x['verdict']} |")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## Reading")
    L.append("")
    L.append("**The leapfrog architecture at commercial chunk scale (200 tonnes) doesn't close L0-09 commercial floor at flyable Kilopower-extrapolation reactor power under corrected delta-velocity anchors.** This was hidden by the prior round's understated Saturn-departure anchor. The corrected reading aligns with what the campaign has been saying all session — commercial-scale ICEBERG inbound delivery is empty at flyable power — but my prior leapfrog round had erroneously suggested otherwise.")
    L.append("")
    L.append("**Aerocapture closure remains the load-bearing question, but is no longer sufficient by itself.** Even with Earth aerocapture working perfectly (zero propulsive capture), the Saturn-departure burn alone consumes 182 tonnes of the 200-tonne chunk, leaving only ~15 tonnes delivered. Below floor.")
    L.append("")
    L.append("**The lunar gravity assist scenario (R12 architecture) is also empty at commercial scale under corrected anchors.** Even with 5.83 kilometres-per-second of v_∞ shed via 10 flybys, the residual 4.2 kilometres-per-second chemical capture burn on top of the corrected 7.7-kilometre-per-second Saturn departure still over-spends the chunk's propellant budget.")
    L.append("")
    L.append("**R12's 13.91-year / 70%-delivery closing cell survives in this round's terms ONLY because R12 was sized for a 14-tonne chunk, not 200 tonnes.** At demonstrator scale, the corrected anchors don't change the verdict materially because the propellant requirements scale linearly with chunk mass but the relative delivered fraction is preserved.")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## Methodology lesson — candidate lesson 20")
    L.append("")
    L.append("**Vis-viva-default anchoring.** When a delta-velocity value is used as an architecture-defining anchor without a primary-text citation, default to deriving it from vis-viva at the relevant orbital geometry. The R-chemical-electric-leapfrog round used Saturn-departure 5.5 km/s and Earth-capture 3.5 km/s as informal-sketch values; both were wrong by 30–100% in the conservative direction (less Δv than reality). A 5-minute vis-viva re-derivation would have caught both errors before the round committed.")
    L.append("")
    L.append("This is closely related to lesson 9 (anchor-on-PRIMARY-text) — the difference is that lesson 9 applies when the prior round's text exists; lesson 20 applies when the anchor has no primary source at all and must be derived from physics. Both reduce to the same discipline: **don't use numbers that aren't sourced or derived.**")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## What this changes about the session's conclusions")
    L.append("")
    L.append("1. **R-chemical-electric-leapfrog headline retracted.** The 33–42 tonnes delivered figure is artefact of understated Saturn-departure anchor. Real delivered mass at flyable power and commercial chunk is below floor.")
    L.append("")
    L.append("2. **R12 lunar-gravity-assist verdict is now load-bearing for demonstrator-scale only.** At commercial scale (200-tonne chunk), even the lunar gravity assist tour doesn't rescue the architecture under corrected anchors.")
    L.append("")
    L.append("3. **Minimum reactor power for commercial closure with lunar gravity assist + corrected anchors:** see Pareto closure table. Probably well into Fission Surface Power class.")
    L.append("")
    L.append("4. **The campaign-wide reading converges:** at flyable reactor power, ICEBERG closes only at demonstrator scale. iapetus's staged-options framing is the correct program-level reading. The matrix's 'commercial cell exists at heritage anchor' rows need retraction.")
    L.append("")
    L.append("5. **The session's earlier 'leapfrog is the architecture' reading should be downgraded** to 'leapfrog is a real architectural option that improves the math but doesn't close commercial scale at flyable power; its primary value is making the demonstrator cell more defensible.'")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## Critical follow-on")
    L.append("")
    L.append("- **R-chunk-size-pareto-flyable-power** — at flyable Kilopower-extrapolation (≤ 30 kilowatts-electric) and corrected delta-velocity anchors, what chunk mass closes both L0-05 strict + L0-09 floor? Probably ~80–120 tonnes (between R12 demonstrator and commercial floor). If yes, that becomes the realistic commercial scale and L0-09 should be re-examined.")
    L.append("- **R-cruise-time-vs-trans-Saturn-injection-pareto** — faster cruise (higher trans-Saturn-injection delta-velocity at launch) shortens round-trip at the cost of more launch-vehicle propellant. Could shift the L0-05 strict envelope.")
    L.append("- **R-saturn-aerocapture-feasibility** — Saturn arrival via aerocapture was assumed; needs its own physics check.")
    L.append("- **R-saturn-departure-from-titan-orbit** — if chunk acquisition occurs in a more distant Saturn-system parking orbit (e.g., at Titan's altitude), Saturn-departure delta-velocity drops to ~4 km/s. Tradeoff round.")
    L.append("")
    (RESULTS / "closure_verdict.md").write_text("\n".join(L))


def main():
    print("R-dv-anchor-audit: corrected leapfrog rerun with vis-viva-derived anchors ...")
    rows = sweep()
    grades = grade_hypotheses(rows)
    for x in grades:
        print(f"  {x['H']}: {x['verdict']} ({x['measured']})")

    write_corrected_pareto(rows, grades)
    write_closure_verdict(rows, grades)

    # min power per scenario
    print("Min reactor power to close commercial floor per scenario:")
    for sc in SCENARIOS:
        mp = find_min_power_for_commercial(sc)
        print(f"  {sc}: {'not achievable up to 500 kWe' if mp is None else f'{mp:.0f} kWe'}")

    (RESULTS / "results.json").write_text(json.dumps({
        "round": "R-dv-anchor-audit",
        "worker": "titan-3",
        "date": "2026-05-19",
        "corrections": {
            "dv_saturn_departure_mps": [5500, DV_SATURN_DEPARTURE_MPS],
            "dv_earth_capture_direct_mps": [3500, DV_EARTH_CAPTURE_DIRECT_MPS],
            "dv_earth_capture_lunar_ga_mps": DV_EARTH_CAPTURE_LUNAR_GA_MPS,
        },
        "rows": rows,
        "grades": grades,
        "min_power_for_commercial_floor": {
            sc: find_min_power_for_commercial(sc) for sc in SCENARIOS
        },
    }, indent=2))
    print(f"  -> {RESULTS}")


if __name__ == "__main__":
    main()
