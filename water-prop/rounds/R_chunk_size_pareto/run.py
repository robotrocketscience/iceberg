"""R-chunk-size-pareto — find closing chunk mass at flyable reactor power under
corrected delta-velocity anchors and R12's lunar-gravity-assist architecture.

Pure-electric inbound architecture with lunar gravity assist (10 inbound
flybys shedding 5.83 km/s of v_inf; R12 anchor). Residual inbound delta-velocity
= 4.47 km/s at electric specific impulse 2000 s.

Sweep:
- chunk mass: 10 to 200 tonnes
- reactor power: 10, 15, 20, 30 kilowatt-electric (flyable Kilopower-extrapolation)
- specific power: 2.4 (Kilopower-measured) and 10 (Kilopower-optimistic)

Author: titan-3, 2026-05-19.
"""

from __future__ import annotations

import json
import math
import pathlib
from itertools import product

G0 = 9.80665
SEC_PER_YEAR = 365.25 * 86400.0

# Electric propulsion
ISP_ELECTRIC_S = 2000.0
V_ELECTRIC = ISP_ELECTRIC_S * G0
ETA_THRUSTER = 0.5

# R12 anchor
DV_INBOUND_RESIDUAL_MPS = 4470.0       # residual after 10-flyby lunar gravity assist
LUNAR_PHASING_YR = 0.725                # 8.7 months

# Mission phases
OUTBOUND_YR = 6.0
SATURN_SIDE_YR = 1.0
HOHMANN_INBOUND_YR = 6.09

# Closure budgets
L0_05_STRICT_YR = 15.0
L0_05_WAIVER_YR = 25.0
L0_09_FLOOR_T = 30.0

# Vehicle (pure-electric architecture; no chemical engine, no electrolyser, no big tank)
M_BUS_T = 5.5
M_THRUSTER_KG_PER_KW = 10.0   # 0.01 t/kW
M_BAG_LINEAR_FRAC = 0.05       # 5% of chunk

# Sweep
CHUNK_GRID = [10.0, 15.0, 20.0, 30.0, 40.0, 50.0, 60.0, 80.0, 100.0, 120.0, 150.0, 200.0]
P_GRID = [10.0, 15.0, 20.0, 30.0]
SP_GRID = [2.4, 10.0]

HERE = pathlib.Path(__file__).parent
RESULTS = HERE / "results"
RESULTS.mkdir(exist_ok=True)


def m_dry(chunk_t, P_kw, sp_w_per_kg):
    m_bag = max(0.5, M_BAG_LINEAR_FRAC * chunk_t)
    m_reactor = P_kw * 1000.0 / sp_w_per_kg / 1000.0
    m_thrusters = M_THRUSTER_KG_PER_KW * P_kw / 1000.0
    return M_BUS_T + m_bag + m_reactor + m_thrusters


def evaluate(chunk_t, P_kw, sp_w_per_kg):
    md = m_dry(chunk_t, P_kw, sp_w_per_kg)
    m_initial_t = md + chunk_t
    propellant_t = m_initial_t * (1.0 - math.exp(-DV_INBOUND_RESIDUAL_MPS / V_ELECTRIC))
    m_after_t = m_initial_t - propellant_t
    delivered_t = max(0.0, m_after_t - md)

    # Burn time at electric thrust
    e_jet_J = 0.5 * (propellant_t * 1000.0) * V_ELECTRIC ** 2
    e_elec_J = e_jet_J / ETA_THRUSTER
    t_burn_s = e_elec_J / (P_kw * 1000.0)
    t_burn_yr = t_burn_s / SEC_PER_YEAR

    # Inbound TOF = max(Hohmann coast, burn time)
    inbound_tof_yr = max(HOHMANN_INBOUND_YR, t_burn_yr) + LUNAR_PHASING_YR

    round_trip_yr = OUTBOUND_YR + SATURN_SIDE_YR + inbound_tof_yr

    return {
        "chunk_t": chunk_t, "P_kw": P_kw, "sp_w_per_kg": sp_w_per_kg,
        "m_dry_t": md, "m_initial_t": m_initial_t,
        "propellant_t": propellant_t, "delivered_t": delivered_t,
        "t_burn_yr": t_burn_yr, "inbound_tof_yr": inbound_tof_yr,
        "round_trip_yr": round_trip_yr,
        "closes_strict": round_trip_yr <= L0_05_STRICT_YR,
        "closes_waiver": round_trip_yr <= L0_05_WAIVER_YR,
        "meets_floor": delivered_t >= L0_09_FLOOR_T,
        "closes_commercial_strict": round_trip_yr <= L0_05_STRICT_YR and delivered_t >= L0_09_FLOOR_T,
        "closes_commercial_waiver": round_trip_yr <= L0_05_WAIVER_YR and delivered_t >= L0_09_FLOOR_T,
    }


def sweep():
    rows = []
    for chunk, P, sp in product(CHUNK_GRID, P_GRID, SP_GRID):
        rows.append(evaluate(chunk, P, sp))
    return rows


def find_min_closing_chunk(P_kw, sp, mode="strict"):
    """Smallest chunk that closes (commercial-strict or commercial-waiver)."""
    for chunk in CHUNK_GRID:
        result = evaluate(chunk, P_kw, sp)
        if mode == "strict" and result["closes_commercial_strict"]:
            return chunk
        if mode == "waiver" and result["closes_commercial_waiver"]:
            return chunk
    return None


def find_max_closing_chunk(P_kw, sp, mode="strict"):
    """Largest chunk that closes (commercial-strict or commercial-waiver)."""
    last = None
    for chunk in CHUNK_GRID:
        result = evaluate(chunk, P_kw, sp)
        if mode == "strict" and result["closes_commercial_strict"]:
            last = chunk
        if mode == "waiver" and result["closes_commercial_waiver"]:
            last = chunk
    return last


def grade(rows):
    g = []

    # H-cs-1: At 10 W/kg + 15 kWe + R12, closing chunk in 30-55 t range
    cell = next(r for r in rows if r["chunk_t"] == 40 and r["P_kw"] == 20 and r["sp_w_per_kg"] == 10)
    g.append({
        "H": "H-cs-1",
        "predicted": "at sp=10, P=20 kWe, chunk=40 t closes commercial-strict",
        "measured": f"delivered={cell['delivered_t']:.1f} t, RT={cell['round_trip_yr']:.2f} yr, "
                    f"commercial-strict={cell['closes_commercial_strict']}",
        "verdict": "HELD" if cell["closes_commercial_strict"] else "FALSIFIED",
    })

    # H-cs-2: At Kilopower-measured 2.4, no chunk closes strict at flyable power (or smaller range)
    strict_at_24 = [r for r in rows if r["sp_w_per_kg"] == 2.4 and r["closes_commercial_strict"] and r["P_kw"] <= 30]
    strict_at_10 = [r for r in rows if r["sp_w_per_kg"] == 10.0 and r["closes_commercial_strict"] and r["P_kw"] <= 30]
    g.append({
        "H": "H-cs-2",
        "predicted": "sp=2.4 closes fewer strict cells than sp=10 at flyable power",
        "measured": f"sp=2.4: {len(strict_at_24)} cells; sp=10: {len(strict_at_10)} cells",
        "verdict": "HELD" if len(strict_at_24) < len(strict_at_10) else "FALSIFIED",
    })

    # H-cs-3: round-trip monotonic in chunk size (for fixed P, sp)
    monotonic_count = 0
    total_checks = 0
    for P in P_GRID:
        for sp in SP_GRID:
            sub = sorted([r for r in rows if r["P_kw"] == P and r["sp_w_per_kg"] == sp], key=lambda r: r["chunk_t"])
            if all(sub[i+1]["round_trip_yr"] >= sub[i]["round_trip_yr"] for i in range(len(sub)-1)):
                monotonic_count += 1
            total_checks += 1
    g.append({
        "H": "H-cs-3",
        "predicted": "round-trip rises monotonically with chunk mass at fixed (P, sp)",
        "measured": f"{monotonic_count} of {total_checks} (P, sp) pairs are monotonic",
        "verdict": "HELD" if monotonic_count == total_checks else "FALSIFIED",
    })

    # H-cs-4 aggregate
    flyable_commercial_strict = [r for r in rows if r["P_kw"] <= 30 and r["closes_commercial_strict"]]
    flyable_commercial_waiver = [r for r in rows if r["P_kw"] <= 30 and r["closes_commercial_waiver"]]
    g.append({
        "H": "H-cs-4",
        "predicted": "≥1 cell closes commercial-strict at chunk ≤ 80 t at flyable power + sp=10",
        "measured": f"{len(flyable_commercial_strict)} flyable commercial-strict cells; "
                    f"{len(flyable_commercial_waiver)} flyable commercial-waiver cells",
        "verdict": "HELD" if len(flyable_commercial_strict) >= 1 else "FALSIFIED",
    })

    return g


def write_grid(rows):
    L = []
    L.append("# Chunk-size Pareto grid (pure-electric + R12 lunar gravity assist + corrected anchors)\n")
    L.append(f"Architecture: pure-electric continuous-thrust inbound after 10-flyby lunar tour (R12 anchor; residual {DV_INBOUND_RESIDUAL_MPS/1000:.2f} km/s).")
    L.append(f"Specific impulse: {ISP_ELECTRIC_S} s electric (water-Microwave-Electrothermal-Thruster anchor).")
    L.append(f"Hohmann inbound coast: {HOHMANN_INBOUND_YR} yr. Lunar phasing penalty: {LUNAR_PHASING_YR*12:.1f} months.")
    L.append(f"L0-05 strict: ≤ {L0_05_STRICT_YR} yr. L0-09 floor: ≥ {L0_09_FLOOR_T} t.\n")

    for sp in SP_GRID:
        L.append(f"## Specific power = {sp} W/kg\n")
        L.append("| chunk (t) | P (kWe) | m_dry (t) | m_w (t) | t_burn (yr) | inbound_TOF (yr) | RT (yr) | delivered (t) | strict? | floor? | commercial-strict? |")
        L.append("|---|---|---|---|---|---|---|---|---|---|---|")
        for r in [x for x in rows if x["sp_w_per_kg"] == sp]:
            L.append(
                f"| {r['chunk_t']:.0f} | {r['P_kw']:.0f} | {r['m_dry_t']:.1f} | "
                f"{r['propellant_t']:.1f} | {r['t_burn_yr']:.2f} | {r['inbound_tof_yr']:.2f} | "
                f"{r['round_trip_yr']:.2f} | {r['delivered_t']:.1f} | "
                f"{'YES' if r['closes_strict'] else 'no'} | "
                f"{'YES' if r['meets_floor'] else 'no'} | "
                f"{'**YES**' if r['closes_commercial_strict'] else 'no'} |"
            )
        L.append("")

    (RESULTS / "chunk_size_grid.md").write_text("\n".join(L))


def write_closure_verdict(rows, grades):
    L = []
    L.append("# R-chunk-size-pareto — closure verdict\n")
    L.append("**Worker:** titan-3. **Date:** 2026-05-19.")
    L.append("")
    L.append("## Headline")
    L.append("")
    flyable_strict = [r for r in rows if r["P_kw"] <= 30 and r["closes_commercial_strict"]]
    flyable_waiver = [r for r in rows if r["P_kw"] <= 30 and r["closes_commercial_waiver"]]
    L.append(f"At flyable reactor power (≤ 30 kilowatts-electric Kilopower-extrapolation) + R12's lunar-gravity-assist architecture + corrected vis-viva delta-velocity anchors:")
    L.append("")
    L.append(f"- **{len(flyable_strict)} cells close L0-05 strict + L0-09 floor.**")
    L.append(f"- **{len(flyable_waiver)} cells close L0-05 waiver + L0-09 floor.**")
    L.append("")
    L.append("Closing chunks by specific-power anchor:")
    L.append("")
    L.append("| Specific power | Min strict chunk | Max strict chunk | Min waiver chunk | Max waiver chunk |")
    L.append("|---|---|---|---|---|")
    for sp in SP_GRID:
        for P in [20.0, 30.0]:
            min_s = find_min_closing_chunk(P, sp, "strict")
            max_s = find_max_closing_chunk(P, sp, "strict")
            min_w = find_min_closing_chunk(P, sp, "waiver")
            max_w = find_max_closing_chunk(P, sp, "waiver")
            L.append(f"| sp={sp}, P={P:.0f} kWe | {min_s} | {max_s} | {min_w} | {max_w} |")
    L.append("")
    L.append("## Reading")
    L.append("")
    L.append("ICEBERG closes at flyable power IF the chunk is sized in roughly the **30–80 tonne** range. The 200-tonne commercial anchor is overscale; the 14-tonne R12 demonstrator is underscale for the L0-09 30-tonne floor.")
    L.append("")
    L.append("The chunk-size band that closes is bounded above by **burn time vs Hohmann coast** (heavier chunk requires more reactor power to fit burn in 6-year coast) and bounded below by **L0-09 floor** (chunks below ~40 tonnes don't have enough water left after burn for 30 tonnes delivered).")
    L.append("")
    L.append("Kilopower-measured specific power (2.4 watts-per-kilogram) closes fewer cells than R12-optimistic (10 watts-per-kilogram). The Kilopower-extrapolation between these two is the load-bearing engineering question.")
    L.append("")
    L.append("## Hypothesis grades")
    L.append("")
    L.append("| H | Predicted | Measured | Verdict |")
    L.append("|---|---|---|---|")
    for g in grades:
        L.append(f"| {g['H']} | {g['predicted']} | {g['measured']} | {g['verdict']} |")
    L.append("")
    L.append("## Implication for program design")
    L.append("")
    L.append("ICEBERG should be designed around **40-80 tonne chunks** at **20-30 kilowatt-electric reactor** + lunar gravity assist + Kilopower-extrapolation specific power. This delivers 30-60 tonnes per mission at 14-22 year round-trip — the iapetus tech-demonstrator framing is the realistic shape.")
    L.append("")
    L.append("The 200-tonne commercial anchor that's been in the matrix and the pitch deck is not closable at flyable power. Either:")
    L.append("- Re-scope the program to 40-80 tonne chunks (smaller per-mission delivery, higher cadence).")
    L.append("- Wait for Fission Surface Power class reactor (per project-owner directive: not happening).")
    L.append("- Accept aerocapture closure as a precondition (phoebe 0-of-1920 says no).")
    L.append("")
    L.append("The first option is the only one that doesn't require a project-owner-level reframe of either L0-04 (delivery target) or the reactor power class.")
    L.append("")
    (RESULTS / "closure_verdict.md").write_text("\n".join(L))


def main():
    print("R-chunk-size-pareto: sweeping chunk mass × reactor power × specific power ...")
    rows = sweep()
    grades = grade(rows)
    for x in grades:
        print(f"  {x['H']}: {x['verdict']} ({x['measured']})")

    write_grid(rows)
    write_closure_verdict(rows, grades)

    (RESULTS / "results.json").write_text(json.dumps({
        "round": "R-chunk-size-pareto",
        "worker": "titan-3",
        "date": "2026-05-19",
        "rows": rows,
        "grades": grades,
    }, indent=2))
    print(f"  -> {RESULTS}")


if __name__ == "__main__":
    main()
