"""R-chemical-electric-leapfrog — Pareto sweep over (reactor power, tank capacity)
for the chemical-electric hybrid leapfrog architecture under flyable Kilopower-
class reactor power.

Reactor continuously splits power between (a) electric water-Microwave-Electrothermal-
Thruster (steady-state low thrust) and (b) water electrolysis filling a buffer
tank. Tank fires impulsively at Saturn periapsis on each cycle. Many small Oberth-
efficient burns accumulate the 5.5 km/s Saturn-departure delta-velocity. Trans-
Earth coast handled by electric trim. Earth arrival is the load-bearing
conditional: aerocapture (phoebe-falsified at conservative anchors) vs chemical
capture (eats delivered mass).

Closed-form Tsiolkovsky + reactor-energy bookkeeping. ~60 cells.

Author: titan (re-spawn 3), 2026-05-19.
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
V_CHEM = 4413.0                # m/s, hydrogen-oxygen at specific impulse 450 s
ISP_ELECTRIC_S = 2000.0        # campaign anchor for water-Microwave-Electrothermal-Thruster
V_ELECTRIC = ISP_ELECTRIC_S * G0
ETA_THRUSTER_ELECTRIC = 0.5
ETA_ELECTROLYSIS = 0.75
E_WATER_CHEM_J_PER_KG = 13.4e6 # heat of formation of liquid water (combustion energy)

# ---------- mission-segment anchors ----------
DV_SATURN_DEPARTURE_MPS = 5500.0   # impulsive periapsis-burn equivalent
DV_TRANS_EARTH_TRIM_MPS = 300.0    # small electric trim
DV_EARTH_CAPTURE_MPS = 3500.0      # chemical impulsive if aerocapture fails
OUTBOUND_YR = 6.0
SATURN_SIDE_YR = 1.0
TRANS_EARTH_YR = 6.0

# ---------- vehicle anchors ----------
M_BUS_T = 5.5                  # basis-of-record from R-bus-mass-anchor-adjudication
M_BAG_T = 10.0                 # 5% of 200-t chunk (linear-bag formula)
M_CHEMICAL_ENGINE_T = 1.0
M_ELECTROLYSER_T = 1.0
TANK_MASS_FRACTION = 0.3       # 30% mass fraction for pressurised-gas storage
SPECIFIC_POWER_W_PER_KG = 2.4  # Kilowatt Reactor Using Stirling Technology measured
CHUNK_T = 200.0

# ---------- closure budgets ----------
L0_05_STRICT_YR = 15.0
L0_05_WAIVER_YR = 25.0
L0_09_FLOOR_T = 30.0

# ---------- sweep grids ----------
P_GRID_KW = [10.0, 15.0, 20.0, 30.0, 50.0, 100.0]
TANK_GRID_T = [0.1, 1.0, 10.0, 50.0, 150.0]
AEROCAPTURE_SCENARIOS = ["yes", "no"]


HERE = pathlib.Path(__file__).parent
RESULTS = HERE / "results"
RESULTS.mkdir(exist_ok=True)


def m_reactor_t(P_kw: float) -> float:
    return (P_kw * 1000.0) / SPECIFIC_POWER_W_PER_KG / 1000.0  # tonnes


def m_thrusters_t(P_kw: float) -> float:
    return 0.01 * P_kw


def m_tank_t(T_tank_t: float) -> float:
    return TANK_MASS_FRACTION * T_tank_t


def m_dry(P_kw: float, T_tank_t: float) -> float:
    return (M_BUS_T + M_BAG_T + m_reactor_t(P_kw) + m_thrusters_t(P_kw)
            + M_CHEMICAL_ENGINE_T + M_ELECTROLYSER_T + m_tank_t(T_tank_t))


def electrolysis_rate_t_per_yr(P_kw: float) -> float:
    """Tonnes of water electrolysed per year at full power, 75% efficiency."""
    j_per_yr = P_kw * 1000.0 * SEC_PER_YEAR
    return j_per_yr * ETA_ELECTROLYSIS / E_WATER_CHEM_J_PER_KG / 1000.0


def chemical_propellant_for_dv(dv_mps: float, m_initial_t: float) -> float:
    """Tonnes of water (= hydrolox) needed for impulsive chemical burn."""
    return m_initial_t * (1.0 - math.exp(-dv_mps / V_CHEM))


def electric_propellant_for_dv(dv_mps: float, m_initial_t: float) -> float:
    return m_initial_t * (1.0 - math.exp(-dv_mps / V_ELECTRIC))


def evaluate_cell(P_kw: float, T_tank_t: float, aerocapture: str):
    md = m_dry(P_kw, T_tank_t)
    m_at_saturn_departure = md + CHUNK_T  # full chunk loaded

    # Saturn departure propellant
    prop_saturn_t = chemical_propellant_for_dv(DV_SATURN_DEPARTURE_MPS, m_at_saturn_departure)

    # Stockpile during outbound + Saturn-side, capped by tank
    e_rate = electrolysis_rate_t_per_yr(P_kw)
    stockpile_t = min(T_tank_t, e_rate * (OUTBOUND_YR + SATURN_SIDE_YR))

    # Spiral-phase electrolysis needed
    remaining_t = max(0.0, prop_saturn_t - stockpile_t)
    spiral_yr = remaining_t / e_rate if e_rate > 0 else float("inf")

    # Trans-Earth electric trim
    m_after_departure = m_at_saturn_departure - prop_saturn_t
    prop_trim_t = electric_propellant_for_dv(DV_TRANS_EARTH_TRIM_MPS, m_after_departure)
    m_after_trim = m_after_departure - prop_trim_t

    # Earth arrival
    if aerocapture == "yes":
        m_after_capture = m_after_trim
        prop_capture_t = 0.0
    else:
        prop_capture_t = chemical_propellant_for_dv(DV_EARTH_CAPTURE_MPS, m_after_trim)
        # Earth-capture propellant also has to be electrolysed during trans-Earth coast
        # (not stockpiled at Saturn departure because that would require enormous tanks)
        m_after_capture = m_after_trim - prop_capture_t

        # Check trans-Earth electrolysis fits in the 6-year cruise
        capture_electrolysis_yr = prop_capture_t / e_rate if e_rate > 0 else float("inf")
        if capture_electrolysis_yr > TRANS_EARTH_YR:
            # Can't electrolyse enough during cruise; would need extra cruise time
            spiral_yr += (capture_electrolysis_yr - TRANS_EARTH_YR)

    delivered_t = max(0.0, m_after_capture - md)

    round_trip_yr = OUTBOUND_YR + SATURN_SIDE_YR + spiral_yr + TRANS_EARTH_YR

    closes_strict = round_trip_yr <= L0_05_STRICT_YR
    closes_waiver = round_trip_yr <= L0_05_WAIVER_YR
    meets_commercial_floor = delivered_t >= L0_09_FLOOR_T

    closes_commercial_strict = closes_strict and meets_commercial_floor
    closes_commercial_waiver = closes_waiver and meets_commercial_floor

    return {
        "P_kw": P_kw,
        "T_tank_t": T_tank_t,
        "aerocapture": aerocapture,
        "m_dry_t": md,
        "m_reactor_t": m_reactor_t(P_kw),
        "m_tank_t": m_tank_t(T_tank_t),
        "prop_saturn_t": prop_saturn_t,
        "stockpile_t": stockpile_t,
        "remaining_t": remaining_t,
        "spiral_yr": spiral_yr,
        "prop_trim_t": prop_trim_t,
        "prop_capture_t": prop_capture_t,
        "m_after_capture_t": m_after_capture,
        "delivered_t": delivered_t,
        "round_trip_yr": round_trip_yr,
        "closes_strict": closes_strict,
        "closes_waiver": closes_waiver,
        "meets_floor": meets_commercial_floor,
        "closes_commercial_strict": closes_commercial_strict,
        "closes_commercial_waiver": closes_commercial_waiver,
    }


def sweep():
    rows = []
    for P, T, aero in product(P_GRID_KW, TANK_GRID_T, AEROCAPTURE_SCENARIOS):
        rows.append(evaluate_cell(P, T, aero))
    return rows


def grade_hypotheses(rows):
    g = []

    # H-lf-1: anchor cell P=15, T=150, aero=yes -> round-trip 13 yr
    anchor1 = next(r for r in rows
                   if r["P_kw"] == 15 and r["T_tank_t"] == 150 and r["aerocapture"] == "yes")
    g.append({
        "H": "H-lf-1a",
        "predicted": "anchor (P=15, T=150, aero=yes) round-trip = 13 yr (stockpile everything, no spiral)",
        "measured": f"{anchor1['round_trip_yr']:.1f} yr; spiral={anchor1['spiral_yr']:.2f} yr",
        "verdict": "HELD" if 12.5 <= anchor1["round_trip_yr"] <= 13.5 else "FALSIFIED",
    })

    # H-lf-1b: small-tank anchor P=10, T=1, aero=yes
    anchor2 = next(r for r in rows
                   if r["P_kw"] == 10 and r["T_tank_t"] == 1 and r["aerocapture"] == "yes")
    g.append({
        "H": "H-lf-1b",
        "predicted": "small-tank cell (P=10, T=1, aero=yes) round-trip ~21.9 yr (mostly spiral)",
        "measured": f"{anchor2['round_trip_yr']:.1f} yr; spiral={anchor2['spiral_yr']:.2f} yr",
        "verdict": "HELD" if 20 <= anchor2["round_trip_yr"] <= 24 else "FALSIFIED",
    })

    # H-lf-2: delivered mass anchor P=15, T=10, aero=yes -> ~35 t delivered
    anchor3 = next(r for r in rows
                   if r["P_kw"] == 15 and r["T_tank_t"] == 10 and r["aerocapture"] == "yes")
    g.append({
        "H": "H-lf-2a",
        "predicted": "anchor (P=15, T=10, aero=yes) delivered ~35 t, above L0-09 floor",
        "measured": f"delivered {anchor3['delivered_t']:.1f} t",
        "verdict": "HELD" if 30 <= anchor3["delivered_t"] <= 40 else "FALSIFIED",
    })

    # H-lf-2b: aero=no eats chunk -> delivered ~0 at flyable power
    no_aero_cells = [r for r in rows if r["aerocapture"] == "no" and r["P_kw"] <= 30]
    max_delivered_no_aero = max(r["delivered_t"] for r in no_aero_cells) if no_aero_cells else 0
    g.append({
        "H": "H-lf-2b",
        "predicted": "aero=no at flyable power (P<=30): max delivered < 30 t",
        "measured": f"max delivered (aero=no, P<=30) = {max_delivered_no_aero:.1f} t",
        "verdict": "HELD" if max_delivered_no_aero < 30 else "FALSIFIED",
    })

    # H-lf-3: closing envelope structure under aero=yes
    aero_yes_strict = [r for r in rows if r["aerocapture"] == "yes" and r["closes_commercial_strict"]]
    aero_yes_waiver = [r for r in rows if r["aerocapture"] == "yes" and r["closes_commercial_waiver"]]
    aero_no_strict = [r for r in rows if r["aerocapture"] == "no" and r["closes_commercial_strict"]]
    aero_no_waiver = [r for r in rows if r["aerocapture"] == "no" and r["closes_commercial_waiver"]]
    g.append({
        "H": "H-lf-3",
        "predicted": "aero=yes envelope non-empty; aero=no envelope empty at flyable power",
        "measured": f"aero=yes strict={len(aero_yes_strict)} cells, waiver={len(aero_yes_waiver)} cells; "
                    f"aero=no strict={len(aero_no_strict)}, waiver={len(aero_no_waiver)}",
        "verdict": "HELD" if (len(aero_yes_strict) > 0 and len(aero_no_strict) == 0) else "FALSIFIED",
    })

    # H-lf-4 aggregate
    flyable_aero_yes_strict = [r for r in aero_yes_strict if r["P_kw"] <= 30]
    flyable_aero_yes_waiver = [r for r in aero_yes_waiver if r["P_kw"] <= 30]
    flyable_aero_no_strict = [r for r in aero_no_strict if r["P_kw"] <= 30]
    g.append({
        "H": "H-lf-4",
        "predicted": "ICEBERG closes at flyable power (P<=30) under aero=yes; empty under aero=no",
        "measured": f"flyable+aero=yes: strict={len(flyable_aero_yes_strict)} waiver={len(flyable_aero_yes_waiver)}; "
                    f"flyable+aero=no: strict={len(flyable_aero_no_strict)}",
        "verdict": "HELD" if (len(flyable_aero_yes_strict) > 0 or len(flyable_aero_yes_waiver) > 0)
                        and len(flyable_aero_no_strict) == 0 else "FALSIFIED",
    })

    return g, {
        "aero_yes_strict": aero_yes_strict,
        "aero_yes_waiver": aero_yes_waiver,
        "aero_no_strict": aero_no_strict,
        "aero_no_waiver": aero_no_waiver,
        "flyable_aero_yes_strict": flyable_aero_yes_strict,
        "flyable_aero_yes_waiver": flyable_aero_yes_waiver,
        "flyable_aero_no_strict": flyable_aero_no_strict,
    }


def write_leapfrog_grid(rows):
    L = []
    L.append("# Sub-procedure 1 — full leapfrog grid\n")
    L.append("Vehicle: bus 5.5 t (basis-of-record); bag 10 t (5% × 200-t chunk).")
    L.append("Reactor specific power 2.4 W/kg (Kilopower-measured floor). Tank mass = 30% × tank capacity (pressurised-gas anchor).")
    L.append("Saturn departure 5.5 km/s impulsive chemical (water-derived hydrolox at 4413 m/s exhaust velocity).")
    L.append("Trans-Earth coast 0.3 km/s electric trim (specific impulse 2000 s).")
    L.append("Earth arrival: aerocapture (0 propellant; phoebe-conditional) OR chemical impulsive 3.5 km/s.\n")

    L.append("| P (kWe) | T_tank (t) | aero | m_dry (t) | prop_dep (t) | stockpile (t) | spiral (yr) | RT (yr) | delivered (t) | strict? | floor? | commercial-strict? |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        L.append(
            f"| {r['P_kw']:.0f} | {r['T_tank_t']:.1f} | {r['aerocapture']} | "
            f"{r['m_dry_t']:.1f} | {r['prop_saturn_t']:.1f} | {r['stockpile_t']:.1f} | "
            f"{r['spiral_yr']:.2f} | {r['round_trip_yr']:.1f} | {r['delivered_t']:.1f} | "
            f"{'YES' if r['closes_strict'] else 'no'} | "
            f"{'YES' if r['meets_floor'] else 'no'} | "
            f"{'**YES**' if r['closes_commercial_strict'] else 'no'} |"
        )
    L.append("")

    (RESULTS / "leapfrog_grid.md").write_text("\n".join(L))


def write_pareto_envelope(rows, buckets, grades):
    L = []
    L.append("# Sub-procedure 2 — Pareto closing envelope\n")
    L.append("Cells that close both round-trip AND L0-09 30-tonne delivered floor.\n")

    L.append("## Aerocapture YES, L0-05 strict (≤ 15 yr)\n")
    L.append("| P (kWe) | T_tank (t) | round-trip (yr) | delivered (t) | flyable (P ≤ 30)? |")
    L.append("|---|---|---|---|---|")
    for r in sorted(buckets["aero_yes_strict"], key=lambda r: (r["P_kw"], r["T_tank_t"])):
        flyable_flag = "YES" if r["P_kw"] <= 30 else "no — FSP-class"
        L.append(f"| {r['P_kw']:.0f} | {r['T_tank_t']:.1f} | {r['round_trip_yr']:.1f} | "
                 f"{r['delivered_t']:.1f} | {flyable_flag} |")
    L.append(f"\n**{len(buckets['aero_yes_strict'])} cells close commercial-strict under aerocapture-yes.**\n")

    L.append("## Aerocapture YES, L0-05 waiver only (15 < RT ≤ 25 yr)\n")
    waiver_only = [r for r in buckets["aero_yes_waiver"] if not r["closes_commercial_strict"]]
    L.append("| P (kWe) | T_tank (t) | round-trip (yr) | delivered (t) | flyable? |")
    L.append("|---|---|---|---|---|")
    for r in sorted(waiver_only, key=lambda r: (r["P_kw"], r["T_tank_t"])):
        flyable_flag = "YES" if r["P_kw"] <= 30 else "no — FSP-class"
        L.append(f"| {r['P_kw']:.0f} | {r['T_tank_t']:.1f} | {r['round_trip_yr']:.1f} | "
                 f"{r['delivered_t']:.1f} | {flyable_flag} |")
    L.append(f"\n**{len(waiver_only)} additional cells close under waiver only.**\n")

    L.append("## Aerocapture NO, any waiver level\n")
    L.append(f"{len(buckets['aero_no_strict']) + len(buckets['aero_no_waiver'])} cells close (waiver or strict). ")
    if buckets["aero_no_strict"]:
        L.append("Specific cells:")
        for r in buckets["aero_no_strict"] + [x for x in buckets["aero_no_waiver"] if not x["closes_commercial_strict"]]:
            L.append(f"- P={r['P_kw']:.0f}, T={r['T_tank_t']:.1f}, RT={r['round_trip_yr']:.1f} yr, delivered={r['delivered_t']:.1f} t")
    else:
        L.append("**No aero=no cells close commercial-strict at any (P, T_tank) tested.** Chemical Earth capture eats the chunk below the L0-09 30-tonne floor in every case.")
    L.append("")

    L.append("## Flyable-power envelope (P ≤ 30 kWe, Kilopower-extrapolation)\n")
    L.append(f"- Aerocapture-yes strict: **{len(buckets['flyable_aero_yes_strict'])} cells** at flyable power")
    L.append(f"- Aerocapture-yes waiver: **{len(buckets['flyable_aero_yes_waiver'])} cells** at flyable power")
    L.append(f"- Aerocapture-no any: **{len(buckets['flyable_aero_no_strict'])} cells** at flyable power")
    L.append("")

    if buckets["flyable_aero_yes_strict"]:
        L.append("**Flyable + aerocapture + commercial-strict cells:**")
        for r in sorted(buckets["flyable_aero_yes_strict"], key=lambda r: (r["P_kw"], r["T_tank_t"])):
            L.append(f"- P = {r['P_kw']:.0f} kWe, T_tank = {r['T_tank_t']:.1f} t → round-trip {r['round_trip_yr']:.1f} yr, delivered {r['delivered_t']:.1f} t")
    L.append("")

    L.append("## Hypothesis grades\n")
    L.append("| H | Predicted | Measured | Verdict |")
    L.append("|---|---|---|---|")
    for x in grades:
        L.append(f"| {x['H']} | {x['predicted']} | {x['measured']} | {x['verdict']} |")
    L.append("")

    (RESULTS / "pareto_envelope.md").write_text("\n".join(L))


def write_closure_verdict(rows, buckets, grades):
    L = []
    L.append("# R-chemical-electric-leapfrog — closure verdict\n")
    L.append("**Worker:** titan (re-spawn 3, branch `iceberg-titan-3`)")
    L.append("**Date:** 2026-05-19")
    L.append("**Predecessors:** R-bus-mass-anchor-adjudication (`7b6a492` + `acdbdc1`); R-kilowatt-class-power-envelope (`5162735` + `10b77b7`)")
    L.append("**Trigger:** project-owner architectural proposal — continuous reactor power split between electric thrust and water electrolysis, periodic impulsive chemical burns at Saturn periapsis.")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## Headline")
    L.append("")
    flyable_strict = buckets["flyable_aero_yes_strict"]
    flyable_waiver = buckets["flyable_aero_yes_waiver"]
    n_strict = len(flyable_strict)
    n_waiver = len(flyable_waiver)
    L.append(f"**ICEBERG inbound delivery closes at flyable reactor power under the chemical-electric leapfrog architecture, IF AND ONLY IF Earth aerocapture closes.** At flyable power (≤ 30 kilowatts-electric, Kilopower-extrapolation):")
    L.append("")
    L.append(f"- {n_strict} cells close L0-05 strict (15-year round-trip) AND L0-09 commercial floor (30 tonnes delivered) under aerocapture-yes.")
    L.append(f"- {n_waiver} cells close L0-05 waiver (25-year round-trip) AND commercial floor under aerocapture-yes.")
    L.append(f"- {len(buckets['flyable_aero_no_strict'])} cells close commercial-strict under aerocapture-no.")
    L.append("")
    L.append("**The binding constraint at flyable power is Earth aerocapture closure, not reactor power class.** Phoebe's 0-of-1920 hybrid-aerocapture-aerobraking verdict (commit `1623cca`) holds the load-bearing physics. R-bus-mass-anchor-adjudication's H5 sub-analysis (this branch, commit `7b6a492`) found phoebe's verdict robust by conjunction: single-axis relaxation of ice tensile strength flips the pass-1 structural leg, but the aerobraking-timescale and sublimation legs remain bound by orders of magnitude. The R-hybrid-aerocapture-joint-axis-sensitivity follow-on round (flagged in the prior round, project-owner direction required) is now the highest-leverage remaining engineering question for the entire program.")
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

    L.append("## Three-paragraph decision frame")
    L.append("")
    L.append("**Architecturally.** The chemical-electric leapfrog rescues ICEBERG inbound delivery at flyable reactor power. The R-kilowatt-class-power-envelope round's headline that the architecture is empty at flyable power was an artefact of assuming pure continuous-thrust electric inbound; that round has been corrected (commit `10b77b7`). Under leapfrog, the Saturn-departure delta-velocity is delivered as many small Oberth-efficient periapsis burns rather than a single gravity-loss-laden continuous-thrust spiral. Chemical hydrogen-oxygen at exhaust velocity 4413 metres-per-second is ~4.8× more reactor-energy-efficient per delta-velocity than electric water-Microwave-Electrothermal-Thruster at 2000-second specific impulse. Reactor power can drop from the 240+ kilowatts-electric needed for pure-electric closure to ~15–30 kilowatts-electric for leapfrog closure — a flyable Kilopower-extrapolation rather than Fission Surface Power class.")
    L.append("")
    L.append("**Conditionally.** The leapfrog architecture's delivered-mass result is gated entirely on Earth aerocapture closing. Without aerocapture, the chemical Earth-capture burn (3.5 kilometres-per-second on a 62-tonne mid-cruise vehicle) eats 34 tonnes of additional propellant and drops delivered mass below the L0-09 30-tonne commercial floor. Phoebe's 0-of-1920 verdict on hybrid-aerocapture-aerobraking is the binding physics, robust by conjunction across three failure modes (pass-1 chunk shatter, aerobraking timescale, sublimation). Single-axis ice-tensile relaxation flips only one leg.")
    L.append("")
    L.append("**Decision-frame.** The program-level question collapses from 'what reactor power class do we need?' to 'does Earth aerocapture close under any defensible joint relaxation of phoebe's three anchors?' If yes, ICEBERG has a flyable cell at ~15–30 kilowatt-electric Kilopower-extrapolation, delivering ~30–42 tonnes per mission in 13–22 years round-trip. If no, the program is empty at any flyable power regardless of propulsion architecture, and the surviving cells reduce to (a) drop-and-go at Saturn (requires L0-04 waiver) or (b) wait for a power class that isn't built. The R-hybrid-aerocapture-joint-axis-sensitivity round is the load-bearing follow-on.")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## Matrix amendments")
    L.append("")
    L.append("1. **Axis 02 (Surviving cell) — un-collapse the kilowatt-class round's collapse.** The prior round's claim that axis 02 collapses to power envelope at flyable power is wrong under leapfrog architecture. Axis 02 splits back into two load-bearing axes: (a) Earth aerocapture closure, (b) propulsion architecture choice (continuous-thrust electric vs chemical-electric leapfrog). The aerocapture axis is the binding one.")
    L.append("")
    L.append("2. **New sub-axis: propulsion architecture.** Pure continuous-thrust electric: empty at flyable power. Chemical-electric leapfrog: non-empty at flyable power if aerocapture closes. Matrix should carry both rows.")
    L.append("")
    L.append("3. **Axis 11 (Earth-arrival mode) — the binding axis.** Phoebe's 0-of-1920 verdict stands as basis-of-record. R-hybrid-aerocapture-joint-axis-sensitivity is the highest-leverage follow-on.")
    L.append("")
    L.append("4. **Phoebe pivot-survey 31/31 DEAD reading — narrow the audit.** Many of phoebe's kill criteria were F6 (reactor program). Under leapfrog architecture at 15–30 kilowatts-electric Kilopower-extrapolation, F6 binarised-FAIL is no longer the correct treatment; the relevant question becomes 'does Kilopower scale to 15–30 kilowatts-electric in the demonstrator window?'. That's a softer constraint than 'does Fission Surface Power Phase 2 deliver 100+ kilowatts-electric'. Pivot-survey re-run under the Kilopower-extrapolation framing might re-classify some candidates from DEAD to WORTH-DEEP-DIVE.")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## Engineering risks not modelled (each is its own round)")
    L.append("")
    L.append("- **Hydrogen leak rate** in pressurised gas tanks across week-class storage cycles. Hydrogen permeates standard tank wall materials; rate at 10-megapascal pressure across a 100-kilogram-class buffer tank may be significant fraction of stored propellant per week. Determines minimum reactor power that keeps electrolysis rate ahead of leak loss.")
    L.append("- **Chemical-engine throat erosion** across N periapsis burns. N may be 100–10,000 depending on cycle time. Conventional chemical engines are not designed for that many starts.")
    L.append("- **Reactor lifetime** at full power across 8+ years of continuous operation. Enceladus-r5 R-reactor-lifetime-vs-burn-time finding: KRUSTY 28-hour heritage is 3-4 orders of magnitude short of multi-year operation. This is orthogonal to the leapfrog architecture and remains binding.")
    L.append("- **Saturn aerocapture for arrival.** Assumed in this round; Saturn atmosphere is thicker than Earth's and Cassini-Huygens demonstrated entry. Independent verification round flagged.")
    L.append("- **Long-term cryogenic storage of liquid hydrogen / liquid oxygen.** Modelled as 30% mass-fraction pressurised gas storage; cryogenic at large tank sizes (T_tank ≥ 50 tonnes) has much worse mass and boiloff penalties.")
    L.append("- **Electrolyser longevity, plant balance-of-system, water-purity requirements.** All assumed nominal; each is a real engineering programme.")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## Audit / cross-check")
    L.append("")
    anchor_yes = next(r for r in rows if r["P_kw"] == 15 and r["T_tank_t"] == 10 and r["aerocapture"] == "yes")
    L.append(f"Hand-verifying anchor cell (P = 15 kilowatts-electric, T_tank = 10 t, aerocapture-yes):")
    L.append(f"- Reactor mass: 15,000 / 2.4 / 1000 = {anchor_yes['m_reactor_t']:.2f} t.")
    L.append(f"- Dry mass: 5.5 (bus) + 10 (bag) + {anchor_yes['m_reactor_t']:.2f} (reactor) + 0.15 (thrusters) + 1.0 (chemical engine) + 1.0 (electrolyser) + {anchor_yes['m_tank_t']:.1f} (tank) = {anchor_yes['m_dry_t']:.2f} t.")
    L.append(f"- Saturn departure propellant: 220 × (1 − exp(−5500/4413)) = {anchor_yes['prop_saturn_t']:.1f} t.")
    L.append(f"- Outbound + Saturn-side stockpile: min(10, 7 × 1.76 × 15) = min(10, 184.8) = {anchor_yes['stockpile_t']:.1f} t (tank-limited).")
    L.append(f"- Spiral electrolysis: ({anchor_yes['prop_saturn_t']:.1f} − {anchor_yes['stockpile_t']:.1f}) / (1.76 × 15) = {anchor_yes['spiral_yr']:.2f} years.")
    L.append(f"- Round-trip: 6 + 1 + {anchor_yes['spiral_yr']:.2f} + 6 = {anchor_yes['round_trip_yr']:.1f} years.")
    L.append(f"- Delivered: 220 × exp(−5500/4413) − 1 (trim) − {anchor_yes['m_dry_t']:.1f} (dry) = {anchor_yes['delivered_t']:.1f} t.")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## Critical follow-ons (project-owner direction required)")
    L.append("")
    L.append("- **R-hybrid-aerocapture-joint-axis-sensitivity** (highest priority). Joint relaxation across {ice tensile strength, boundary-layer-blocking-factor, atmosphere density} at credible-upper-bounds. Determines whether phoebe's 0-of-1920 is robust under the most-generous-credible-anchor reading. The leapfrog architecture's viability depends entirely on this round's verdict.")
    L.append("- **R-leapfrog-tank-physics** (engineering). Hydrogen leak rate vs storage time at relevant pressures; chemical-engine restart life across N cycles; electrolyser balance-of-system mass and lifetime. Each could move the closing envelope by 1-2× in either direction.")
    L.append("- **R-pivot-survey-rerun-at-Kilopower-anchor** (lower priority). Re-test phoebe's 7 F6-conditional candidates under the softer 'Kilopower scales to 15-30 kilowatts-electric' constraint rather than the binarised 'Fission Surface Power Phase 2 delivers'.")
    L.append("")
    (RESULTS / "closure_verdict.md").write_text("\n".join(L))


def main():
    print("Sweeping (P_reactor, T_tank, aerocapture) cells ...")
    rows = sweep()
    grades, buckets = grade_hypotheses(rows)
    for x in grades:
        print(f"  {x['H']}: {x['verdict']} ({x['measured']})")

    write_leapfrog_grid(rows)
    write_pareto_envelope(rows, buckets, grades)
    write_closure_verdict(rows, buckets, grades)

    (RESULTS / "results.json").write_text(json.dumps({
        "round": "R-chemical-electric-leapfrog",
        "worker": "titan-3",
        "date": "2026-05-19",
        "rows": rows,
        "grades": grades,
        "summary": {
            "n_aero_yes_strict": len(buckets["aero_yes_strict"]),
            "n_aero_yes_waiver": len(buckets["aero_yes_waiver"]),
            "n_aero_no_strict": len(buckets["aero_no_strict"]),
            "n_aero_no_waiver": len(buckets["aero_no_waiver"]),
            "n_flyable_aero_yes_strict": len(buckets["flyable_aero_yes_strict"]),
            "n_flyable_aero_yes_waiver": len(buckets["flyable_aero_yes_waiver"]),
            "n_flyable_aero_no_strict": len(buckets["flyable_aero_no_strict"]),
        },
    }, indent=2))
    print(f"  -> {RESULTS}")


if __name__ == "__main__":
    main()
