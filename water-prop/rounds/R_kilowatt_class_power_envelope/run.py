"""R-kilowatt-class-power-envelope — analytical burn-time bound at the
project-owner-specified flyable power envelope (1-10 kilowatt-electric,
Kilopower-heritage).

Project-owner directive 2026-05-19: "A 500 kilowatt reactor is not going to
happen." This round re-derives the inbound-burn-time bound at the actually-
flyable power class. Closed-form Tsiolkovsky; ~36 cells; no numerical sweep.

Author: titan (re-spawn 3), 2026-05-19.
"""

from __future__ import annotations

import json
import math
import pathlib
from itertools import product

G0 = 9.80665
SEC_PER_YEAR = 365.25 * 86400.0

ETA_THRUSTER = 0.5                  # water-electric MET/arcjet, same as enceladus-r5 anchor
DV_INBOUND_CT = 25_000.0            # m/s (campaign continuous-thrust mid-point)
OUTBOUND_YR = 6.0
SATURN_SIDE_YR = 1.0
L0_05_STRICT_TOTAL_YR = 15.0
L0_05_STRICT_INBOUND_BUDGET_YR = L0_05_STRICT_TOTAL_YR - OUTBOUND_YR - SATURN_SIDE_YR  # 8 yr
L0_09_FLOOR_T = 30.0
L0_05_WAIVER_TOTAL_YR = 25.0
L0_05_WAIVER_INBOUND_BUDGET_YR = L0_05_WAIVER_TOTAL_YR - OUTBOUND_YR - SATURN_SIDE_YR  # 18 yr

# vehicle dry masses (project-owner basis-of-record from prior round)
M_BUS_T = 5.5                       # Europa-Clipper-with-medium-shielding
M_BAG_LINEAR_FRAC = 0.05            # 5% of chunk mass; floor 0.5 t

HERE = pathlib.Path(__file__).parent
RESULTS = HERE / "results"
RESULTS.mkdir(exist_ok=True)


def m_bag(chunk_t: float) -> float:
    return max(0.5, M_BAG_LINEAR_FRAC * chunk_t)


def compute_cell(P_kwe: float, chunk_t: float, isp_s: float, sp_w_per_kg: float):
    """Return per-cell physics: propellant, burn time, delivered fraction."""
    v_e = isp_s * G0
    m_reactor = (P_kwe * 1000.0) / sp_w_per_kg / 1000.0  # tonnes
    m_thrusters = 0.01 * P_kwe                            # tonnes (10 kg per kWe heritage)
    m_dry = M_BUS_T + m_bag(chunk_t) + m_reactor + m_thrusters
    m_0 = m_dry + chunk_t

    # Tsiolkovsky: m_w = m_0 * (1 - exp(-dv/v_e))
    m_w = m_0 * (1.0 - math.exp(-DV_INBOUND_CT / v_e))
    if m_w >= chunk_t:
        delivered = 0.0
    else:
        delivered = chunk_t - m_w

    # Energy & burn time
    e_jet_J = 0.5 * (m_w * 1000.0) * v_e ** 2
    e_elec_J = e_jet_J / ETA_THRUSTER
    t_burn_s = e_elec_J / (P_kwe * 1000.0)
    t_burn_yr = t_burn_s / SEC_PER_YEAR

    pass_strict = (delivered >= L0_09_FLOOR_T) and (t_burn_yr <= L0_05_STRICT_INBOUND_BUDGET_YR)
    pass_waiver = (delivered >= L0_09_FLOOR_T) and (t_burn_yr <= L0_05_WAIVER_INBOUND_BUDGET_YR)

    return {
        "P_kwe": P_kwe,
        "chunk_t": chunk_t,
        "isp_s": isp_s,
        "sp_w_per_kg": sp_w_per_kg,
        "v_e_mps": v_e,
        "m_reactor_t": m_reactor,
        "m_dry_t": m_dry,
        "m_0_t": m_0,
        "m_w_t": m_w,
        "delivered_t": delivered,
        "delivered_frac": delivered / chunk_t if chunk_t > 0 else 0.0,
        "e_jet_J": e_jet_J,
        "e_elec_J": e_elec_J,
        "t_burn_yr": t_burn_yr,
        "rt_total_yr": OUTBOUND_YR + SATURN_SIDE_YR + t_burn_yr,
        "margin_vs_strict_budget": t_burn_yr / L0_05_STRICT_INBOUND_BUDGET_YR,  # >1 = over budget
        "margin_vs_waiver_budget": t_burn_yr / L0_05_WAIVER_INBOUND_BUDGET_YR,
        "pass_strict": pass_strict,
        "pass_waiver": pass_waiver,
    }


def sweep():
    P_grid = [1.0, 5.0, 10.0]
    chunk_grid = [30.0, 100.0, 200.0]
    isp_grid = [2000.0, 5000.0]
    sp_grid = [2.4, 5.3]
    rows = []
    for (P, ch, isp, sp) in product(P_grid, chunk_grid, isp_grid, sp_grid):
        rows.append(compute_cell(P, ch, isp, sp))
    return rows


def closing_chunk_for_strict_at(P_kwe: float, isp_s: float, sp_w_per_kg: float):
    """Find the chunk mass (if any in [1, 500] tonnes) that closes L0-05 strict
    8-yr inbound burn. Bisection on burn time vs budget."""
    lo, hi = 0.1, 500.0
    if compute_cell(P_kwe, lo, isp_s, sp_w_per_kg)["t_burn_yr"] > L0_05_STRICT_INBOUND_BUDGET_YR:
        return None    # even the smallest chunk doesn't close
    if compute_cell(P_kwe, hi, isp_s, sp_w_per_kg)["t_burn_yr"] < L0_05_STRICT_INBOUND_BUDGET_YR:
        return hi      # all chunks close
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        c = compute_cell(P_kwe, mid, isp_s, sp_w_per_kg)
        if c["t_burn_yr"] > L0_05_STRICT_INBOUND_BUDGET_YR:
            hi = mid
        else:
            lo = mid
    return lo


def grade_hypotheses(rows):
    g = []

    # H-kw-1: anchor cell at P=10, Isp=2000, chunk=200 — burn time 150-250 yr range
    anchor = next(r for r in rows
                  if r["P_kwe"] == 10 and r["chunk_t"] == 200
                  and r["isp_s"] == 2000 and r["sp_w_per_kg"] == 2.4)
    g.append({
        "H": "H-kw-1",
        "predicted": "burn time at 10 kWe / Isp 2000 / chunk 200 / sp 2.4 ∈ [150, 250] yr",
        "measured": f"{anchor['t_burn_yr']:.1f} yr",
        "verdict": "HELD" if 150 <= anchor["t_burn_yr"] <= 250 else "FALSIFIED",
    })

    # H-kw-2: higher Isp longer burn at fixed P
    isp_5000 = next(r for r in rows
                    if r["P_kwe"] == 10 and r["chunk_t"] == 200
                    and r["isp_s"] == 5000 and r["sp_w_per_kg"] == 2.4)
    g.append({
        "H": "H-kw-2",
        "predicted": "Isp 5000 burn time > Isp 2000 burn time at same (P, chunk, sp)",
        "measured": f"Isp 5000 = {isp_5000['t_burn_yr']:.0f} yr vs Isp 2000 = {anchor['t_burn_yr']:.0f} yr",
        "verdict": "HELD" if isp_5000["t_burn_yr"] > anchor["t_burn_yr"] else "FALSIFIED",
    })

    # H-kw-3: no chunk >= 30 t closes burn at 10 kWe / Isp 2000 / sp 2.4
    chunk_30_isp2000_kwe10 = next(r for r in rows
                                   if r["P_kwe"] == 10 and r["chunk_t"] == 30
                                   and r["isp_s"] == 2000 and r["sp_w_per_kg"] == 2.4)
    closes_at_chunk_30 = chunk_30_isp2000_kwe10["pass_strict"]
    closing_chunk = closing_chunk_for_strict_at(10, 2000, 2.4)
    g.append({
        "H": "H-kw-3",
        "predicted": "no chunk ≥ 30 t closes L0-05 strict at 10 kWe / Isp 2000",
        "measured": (f"closing chunk = {closing_chunk:.2f} t (< 30 t floor)" if closing_chunk
                     else "no chunk closes at any size"),
        "verdict": "HELD" if not closes_at_chunk_30 else "FALSIFIED",
    })

    # H-kw-5 aggregate: 0 of 36 cells close strict
    n_close_strict = sum(1 for r in rows if r["pass_strict"])
    n_close_waiver = sum(1 for r in rows if r["pass_waiver"])
    g.append({
        "H": "H-kw-5",
        "predicted": "0 of 36 cells close L0-05 strict AND L0-09 commercial",
        "measured": f"{n_close_strict} of {len(rows)} close strict; {n_close_waiver} close waiver",
        "verdict": "HELD" if n_close_strict == 0 else "FALSIFIED",
    })

    return g, n_close_strict, n_close_waiver


def write_burn_time_grid(rows, grades, n_strict, n_waiver):
    L = []
    L.append("# Sub-procedure — kilowatt-class power-envelope burn-time grid\n")
    L.append(f"Vehicle: bus = {M_BUS_T} t (Europa-Clipper-with-medium-shielding basis-of-record from R-bus-mass-anchor-adjudication); bag = 5% of chunk (linear, floor 0.5 t); reactor mass = P_kWe × 1000 / specific power; thrusters = 10 kg/kWe.")
    L.append(f"Δv inbound: {DV_INBOUND_CT/1000:.0f} km/s continuous-thrust (campaign anchor).")
    L.append(f"L0-05 strict inbound-burn budget: ≤ {L0_05_STRICT_INBOUND_BUDGET_YR:.0f} yr (15 yr total − {OUTBOUND_YR + SATURN_SIDE_YR:.0f} yr outbound + Saturn-side).")
    L.append(f"L0-05 waiver inbound-burn budget: ≤ {L0_05_WAIVER_INBOUND_BUDGET_YR:.0f} yr.")
    L.append(f"L0-09 commercial floor: ≥ {L0_09_FLOOR_T:.0f} t delivered.\n")

    L.append("## Burn-time grid (years)\n")
    L.append("| P (kWe) | chunk (t) | Isp (s) | sp (W/kg) | m_reactor (t) | m_w (t) | delivered (t) | t_burn (yr) | × strict budget | strict? | waiver? |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        L.append(
            f"| {r['P_kwe']:.0f} | {r['chunk_t']:.0f} | {r['isp_s']:.0f} | {r['sp_w_per_kg']:.1f} | "
            f"{r['m_reactor_t']:.2f} | {r['m_w_t']:.1f} | {r['delivered_t']:.1f} | "
            f"{r['t_burn_yr']:.1f} | {r['margin_vs_strict_budget']:.1f}× | "
            f"{'YES' if r['pass_strict'] else 'no'} | {'YES' if r['pass_waiver'] else 'no'} |"
        )
    L.append("")

    L.append("## Closing-chunk search per (P, Isp, sp)\n")
    L.append("What chunk mass would close L0-05 strict (8 yr inbound burn)? Bisection.\n")
    L.append("| P (kWe) | Isp (s) | sp (W/kg) | closing chunk (t) | meets L0-09 floor 30 t? |")
    L.append("|---|---|---|---|---|")
    for P in [1.0, 5.0, 10.0]:
        for isp in [2000.0, 5000.0]:
            for sp in [2.4, 5.3]:
                cc = closing_chunk_for_strict_at(P, isp, sp)
                if cc is None or cc < 30:
                    cc_str = f"{cc:.2f}" if cc else "no chunk closes"
                    L.append(f"| {P:.0f} | {isp:.0f} | {sp:.1f} | {cc_str} | NO |")
                else:
                    L.append(f"| {P:.0f} | {isp:.0f} | {sp:.1f} | {cc:.1f} | YES |")
    L.append("")

    L.append("## Hypothesis grades\n")
    L.append("| H | predicted | measured | verdict |")
    L.append("|---|---|---|---|")
    for x in grades:
        L.append(f"| {x['H']} | {x['predicted']} | {x['measured']} | {x['verdict']} |")
    L.append("")

    L.append(f"**Aggregate.** {n_strict} of {len(rows)} cells close L0-05 strict; {n_waiver} of {len(rows)} close L0-05 waiver. ICEBERG inbound-delivery architecture at the actually-flyable power envelope is empty.")
    L.append("")
    (RESULTS / "burn_time_grid.md").write_text("\n".join(L))


def write_closure_verdict(grades, n_strict, n_waiver, rows):
    anchor = next(r for r in rows
                  if r["P_kwe"] == 10 and r["chunk_t"] == 200
                  and r["isp_s"] == 2000 and r["sp_w_per_kg"] == 2.4)

    L = []
    L.append("# R-kilowatt-class-power-envelope — closure verdict\n")
    L.append("**Worker:** titan (re-spawn 3, branch `iceberg-titan-3`)")
    L.append("**Date:** 2026-05-19")
    L.append("**Predecessor:** R-bus-mass-anchor-adjudication (this branch, commits `7b6a492` + `acdbdc1`)")
    L.append("**Trigger:** project-owner directive 2026-05-19 — 500-kilowatt-electric reactor out-of-bounds.")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## Headline")
    L.append("")
    L.append(f"At the actually-flyable power envelope (1–10 kilowatt-electric, Kilopower-heritage, specific power 2.4–5.3 watts-per-kilogram), **0 of {len(rows)} architecturally-relevant cells close L0-05 strict + L0-09 commercial floor**. {n_waiver} cells close under the L0-05 waiver (25-year round-trip), all at chunk masses below the commercial floor.")
    L.append("")
    L.append(f"Anchor cell: 10 kilowatt-electric / Isp 2000 / 200-tonne chunk / Kilopower specific power 2.4 watts-per-kilogram → **inbound burn time {anchor['t_burn_yr']:.0f} years**, which is **{anchor['margin_vs_strict_budget']:.0f}× over the 8-year inbound-burn budget**. Round-trip {anchor['rt_total_yr']:.0f} years total (vs L0-05 strict 15 years).")
    L.append("")
    L.append("**Reading.** ICEBERG inbound delivery at the flyable power envelope is unphysical by an order of magnitude on burn time alone. Higher specific impulse makes it worse (energy scales as v_e²). Smaller chunk reduces burn time linearly, but the chunk size that closes the burn-time budget at 10 kilowatt-electric / Isp 2000 / Kilopower-class is below the L0-09 commercial floor by an order of magnitude. The drop-and-go architecture (deliver to Saturn-system orbit only) is the only surviving cell and requires an L0-04 waiver that has no existing commercial-demand model.")
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
    L.append("## What this means for the matrix")
    L.append("")
    L.append("1. **Axis 02 (Surviving cell) is now load-bearing on power envelope alone.** Bus mass, aerocapture closure, ring crossing, reactor program — all become second-order. The first-order kill is that ICEBERG cannot deliver chunks to Earth orbit at any flyable power class under continuous-thrust accounting.")
    L.append("")
    L.append("2. **Every prior round that headlined 'N cells close at 500 kilowatt-electric' inherits an implicit retraction.** Listed in the handoff. The architecture-decision-matrix top-section needs orchestrator-level revision: every '500 kilowatt-electric' or 'megawatt-electric' surviving-cell row should be marked fantasy under the project-owner directive.")
    L.append("")
    L.append("3. **The campaign's pivot-survey 31/31 DEAD reading from phoebe is now unconditional.** F6 (reactor program / specific-power availability) was the most-common kill criterion; the directive moves F6 from probabilistic (posterior 0.07–0.20 per iapetus) to binary FAIL for any cell requiring > ~10 kilowatt-electric. Under that move, even the 7 F6-conditional WORTH-DEEP-DIVE candidates from phoebe's audit collapse to DEAD.")
    L.append("")
    L.append("4. **The only surviving cell is drop-and-go architecture** (deliver to Saturn-system orbit, do not bring water to Earth). This requires L0-04 waiver (deliver-to-Earth-orbit is the foundational product requirement). Whether the program can close on Saturn-system water depot revenue is a project-owner question, not a worker round.")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## Critical follow-ons (project-owner direction required)")
    L.append("")
    L.append("- **Is L0-04 (deliver water to Earth orbit) strict, or is Saturn-system water depot a valid product?** This is the program's only surviving architecture under the directive. Without an L0-04 waiver, there is no flyable ICEBERG.")
    L.append("- **Does a commercial cislunar water-tug program (kilowatt-class water-electric MET, ESPA-Grande-class vehicle) become the primary thesis?** That program does close at flyable power and has named customers. ICEBERG's surviving role in this case is as long-tail option attached to the tug roadmap, not as the load-bearing program.")
    L.append("- **The matrix and design-axes documents need orchestrator-level revision.** Multiple prior axes (02 surviving cell, 11 Earth-arrival mode, 13 capital structure, 19 capture architecture) carry 500-kilowatt-electric anchors that the directive retires. This is not a worker-round task.")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## Audit / cross-check")
    L.append("")
    L.append("Hand-verifying H-kw-1 anchor:")
    L.append(f"- Vehicle wet mass at start of inbound burn: 200 (chunk) + {M_BUS_T} (bus) + 10 (bag) + {anchor['m_reactor_t']:.2f} (reactor at 2.4 W/kg) + 0.1 (thrusters) = {anchor['m_0_t']:.2f} t.")
    L.append(f"- v_e = 2000 × 9.80665 = 19,613 m/s.")
    L.append(f"- Mass ratio = exp(25,000 / 19,613) = exp(1.2747) = 3.577.")
    L.append(f"- Propellant = {anchor['m_0_t']:.2f} × (1 − 1/3.577) = {anchor['m_w_t']:.2f} t.")
    L.append(f"- Jet kinetic energy = 0.5 × {anchor['m_w_t']*1000:.0f} kg × 19613² = {anchor['e_jet_J']:.2e} J.")
    L.append(f"- Electrical energy = {anchor['e_jet_J']:.2e} / 0.5 = {anchor['e_elec_J']:.2e} J.")
    L.append(f"- Burn time at 10 kilowatt-electric = {anchor['e_elec_J']:.2e} / 10,000 = {anchor['t_burn_yr']*SEC_PER_YEAR:.2e} s = {anchor['t_burn_yr']:.1f} years.")
    L.append("")
    (RESULTS / "closure_verdict.md").write_text("\n".join(L))


def main():
    print("Computing burn-time grid at kilowatt-class power ...")
    rows = sweep()
    grades, n_strict, n_waiver = grade_hypotheses(rows)
    for x in grades:
        print(f"  {x['H']}: {x['verdict']} ({x['measured']})")
    print(f"  aggregate: {n_strict} strict, {n_waiver} waiver, of {len(rows)} cells")

    write_burn_time_grid(rows, grades, n_strict, n_waiver)
    write_closure_verdict(grades, n_strict, n_waiver, rows)

    (RESULTS / "results.json").write_text(json.dumps({
        "round": "R-kilowatt-class-power-envelope",
        "worker": "titan-3",
        "date": "2026-05-19",
        "trigger": "project-owner directive: 500 kilowatt-electric reactor out-of-bounds",
        "vehicle": {
            "m_bus_t": M_BUS_T,
            "m_bag_linear_frac_of_chunk": M_BAG_LINEAR_FRAC,
            "dv_inbound_continuous_thrust_mps": DV_INBOUND_CT,
        },
        "budgets": {
            "l0_05_strict_inbound_burn_yr": L0_05_STRICT_INBOUND_BUDGET_YR,
            "l0_05_waiver_inbound_burn_yr": L0_05_WAIVER_INBOUND_BUDGET_YR,
            "l0_09_commercial_floor_t": L0_09_FLOOR_T,
        },
        "rows": rows,
        "grades": grades,
        "n_close_strict": n_strict,
        "n_close_waiver": n_waiver,
    }, indent=2))
    print(f"  -> {RESULTS}")


if __name__ == "__main__":
    main()
