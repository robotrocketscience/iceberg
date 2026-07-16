"""R-bus-mass-anchor-sweep — does the matrix's "Architecture E falsified, Variant B Active"
verdict survive a Cassini-anchored bus+bag mass model?

Surfaced by R-hybrid-power-generator-exhaust-revisit: predecessor rounds used m_bus=15 t
and m_bag=8 t without anchoring. Cassini was 2.15 t dry. Europa Clipper 5.9 t. The
matrix-resident "Architecture E falsified" verdict (rhea / hyperion / enceladus-r5 R6+)
may be artefact of an over-conservative bus anchor.

This round: hold the rocket model fixed (pure-electric inbound, single-stream Tsiolkovsky),
sweep bus + bag dry mass across a heritage-anchored range, count closure cells for
the matrix's surviving architectures.

Author: enceladus-r5, 2026-05-16.
"""

from __future__ import annotations

import json
import math
import pathlib
from dataclasses import dataclass, asdict
from itertools import product

G0 = 9.80665
SEC_PER_YEAR = 365.25 * 86400.0

ETA_THRUSTER = 0.5         # water-electric MET / arcjet class (R-hybrid-revisit anchor)
THRUSTER_T_PER_KW = 0.01

ISP_PRIMARY = 2000.0       # matrix surviving cell (water-electric Variant B / Arch E)
ISP_HIGH = 2934.0          # high-Isp R6 sensitivity

DV_INBOUND_CT = 25_000.0   # m/s (titan / rhea continuous-thrust midpoint)
OUTBOUND_YR = 6.0
SATURN_SIDE_YR = 1.0
REACTOR_LIFE_TARGET_YR = 10.0

L0_05_STRICT_YR = 15.0
L0_05_WAIVER_YR = 25.0
STARSHIP_LEO_T = 150.0
L0_09_FLOOR_T = 30.0       # per-mission delivered floor (commercial-class)


@dataclass
class Cell:
    p_reactor_kwe: float
    chunk_t: float
    m_bus_t: float
    m_bag_t: float
    bag_scaling: str            # "flat" or "linear"  (linear: m_bag = 0.05 * chunk_t)
    specific_power_w_per_kg: float
    aerocapture_credit_kms: float
    isp_s: float

    feasible: bool = False
    m_water_t: float = 0.0
    m_delivered_t: float = 0.0
    delivered_frac: float = 0.0
    t_burn_yr: float = 0.0
    rt_yr: float = 0.0
    m_dry_t: float = 0.0
    leo_stack_t: float = 0.0
    pass_l0_05_strict: bool = False
    pass_l0_05_waiver: bool = False
    pass_reactor_life: bool = False
    pass_launchable: bool = False
    pass_l0_09_commercial: bool = False
    effective_bag_t: float = 0.0


def solve(c: Cell) -> Cell:
    v_e = c.isp_s * G0
    dv_required = max(0.0, DV_INBOUND_CT - c.aerocapture_credit_kms * 1000.0)

    if c.bag_scaling == "linear":
        m_bag = max(0.5, 0.05 * c.chunk_t)
    else:
        m_bag = c.m_bag_t
    c.effective_bag_t = m_bag

    m_reactor = c.p_reactor_kwe / c.specific_power_w_per_kg
    m_thrusters = THRUSTER_T_PER_KW * c.p_reactor_kwe
    m_dry = c.m_bus_t + m_bag + m_reactor + m_thrusters

    m_0 = m_dry + c.chunk_t

    # Tsiolkovsky for required dv: m_0 / m_f = exp(dv / v_e)
    ratio = math.exp(dv_required / v_e) if v_e > 0 else 1
    m_f_required = m_0 / ratio
    m_w_required = m_0 - m_f_required  # propellant needed to achieve dv

    if m_w_required > c.chunk_t:
        c.feasible = False
        c.m_dry_t = m_dry
        return c
    if m_w_required < 0:
        m_w_required = 0

    m_delivered = c.chunk_t - m_w_required
    c.m_water_t = m_w_required
    c.m_delivered_t = m_delivered
    c.delivered_frac = m_delivered / c.chunk_t if c.chunk_t > 0 else 0.0

    # energy & burn time
    e_jet = 0.5 * m_w_required * 1000.0 * v_e * v_e
    e_elec = e_jet / ETA_THRUSTER
    t_burn_s = e_elec / (c.p_reactor_kwe * 1000.0) if c.p_reactor_kwe > 0 else float('inf')

    c.t_burn_yr = t_burn_s / SEC_PER_YEAR
    c.rt_yr = OUTBOUND_YR + SATURN_SIDE_YR + c.t_burn_yr
    c.m_dry_t = m_dry
    c.leo_stack_t = m_dry   # no hydrolox in this round

    c.feasible = m_delivered > 0
    if c.feasible:
        c.pass_l0_05_strict = c.rt_yr <= L0_05_STRICT_YR
        c.pass_l0_05_waiver = c.rt_yr <= L0_05_WAIVER_YR
        c.pass_reactor_life = c.t_burn_yr <= REACTOR_LIFE_TARGET_YR
        c.pass_launchable = c.leo_stack_t <= 2 * STARSHIP_LEO_T
        c.pass_l0_09_commercial = c.m_delivered_t >= L0_09_FLOOR_T
    return c


def sweep():
    p_grid = [50.0, 200.0, 500.0]
    chunk_grid = [10.0, 50.0, 100.0, 200.0]
    bus_grid = [2.0, 5.0, 10.0, 15.0]
    bag_flat_grid = [0.5, 2.0, 5.0, 8.0]
    sp_grid = [5.0, 10.0]
    aero_grid = [0.0, 10.0]
    isp_grid = [ISP_PRIMARY, ISP_HIGH]

    rows = []
    # flat-bag cells
    for (p, ch, bus, bag, sp, ac, isp) in product(
        p_grid, chunk_grid, bus_grid, bag_flat_grid, sp_grid, aero_grid, isp_grid):
        c = Cell(p_reactor_kwe=p, chunk_t=ch, m_bus_t=bus, m_bag_t=bag,
                 bag_scaling="flat", specific_power_w_per_kg=sp,
                 aerocapture_credit_kms=ac, isp_s=isp)
        solve(c)
        rows.append(asdict(c))
    # linear-bag cells (chunk-scaled, parameterised by a flag, bag value ignored)
    for (p, ch, bus, sp, ac, isp) in product(
        p_grid, chunk_grid, bus_grid, sp_grid, aero_grid, isp_grid):
        c = Cell(p_reactor_kwe=p, chunk_t=ch, m_bus_t=bus, m_bag_t=0.0,
                 bag_scaling="linear", specific_power_w_per_kg=sp,
                 aerocapture_credit_kms=ac, isp_s=isp)
        solve(c)
        rows.append(asdict(c))
    return rows


def grade(rows):
    grades = []

    # H1: Cassini-anchor (m_bus=2 t + linear bag) opens Variant B / Arch E (500 kWe, 200 t chunk, sp=10, aero=10, isp=2000)
    cassini = [r for r in rows if r["p_reactor_kwe"] == 500 and r["chunk_t"] == 200
               and r["m_bus_t"] == 2 and r["bag_scaling"] == "linear"
               and r["specific_power_w_per_kg"] == 10 and r["aerocapture_credit_kms"] == 10
               and r["isp_s"] == ISP_PRIMARY]
    cassini_pass = [r for r in cassini if r["feasible"] and r["pass_l0_05_waiver"]
                    and r["pass_reactor_life"] and r["pass_launchable"]]
    grades.append({"hypothesis": "H1",
                   "predicted": "Cassini-anchor opens 500-kWe/200-t Arch-E cell at sp=10, aero=10, Isp=2000",
                   "measured": f"{len(cassini_pass)} of {len(cassini)} cells all-pass",
                   "verdict": "HELD" if cassini_pass else "FALSIFIED"})

    # H2: Cassini opens >= 3x more all-pass-waiver cells than full-bus (m_bus=15 + m_bag=8)
    full_bus_count = sum(1 for r in rows if r["m_bus_t"] == 15 and r["bag_scaling"] == "flat"
                         and r["m_bag_t"] == 8 and r["feasible"] and r["pass_l0_05_waiver"]
                         and r["pass_reactor_life"] and r["pass_launchable"])
    cassini_count = sum(1 for r in rows if r["m_bus_t"] == 2 and r["bag_scaling"] == "linear"
                        and r["feasible"] and r["pass_l0_05_waiver"]
                        and r["pass_reactor_life"] and r["pass_launchable"])
    grades.append({"hypothesis": "H2",
                   "predicted": "Cassini-anchor opens >= 3x more all-pass-waiver cells than full-bus",
                   "measured": f"Cassini={cassini_count} all-pass-waiver, full-bus={full_bus_count} all-pass-waiver, ratio={(cassini_count/full_bus_count) if full_bus_count else 'inf':.2f}" if full_bus_count else f"Cassini={cassini_count}, full-bus={full_bus_count} (ratio inf)",
                   "verdict": "HELD" if (full_bus_count == 0 and cassini_count > 0) or (full_bus_count > 0 and cassini_count / full_bus_count >= 3) else "FALSIFIED"})

    # H3: at flown-anchor sp=5, AND Cassini bus, no commercial cell (chunk >=100, delivered >=30 t) closes L0-05 strict
    sp5_commercial = [r for r in rows if r["m_bus_t"] == 2 and r["bag_scaling"] == "linear"
                      and r["specific_power_w_per_kg"] == 5 and r["chunk_t"] >= 100
                      and r["isp_s"] == ISP_PRIMARY and r["feasible"]
                      and r["pass_l0_05_strict"] and r["pass_l0_09_commercial"]
                      and r["pass_reactor_life"] and r["pass_launchable"]]
    grades.append({"hypothesis": "H3",
                   "predicted": "at sp=5 W/kg + Cassini bus, no commercial cell (chunk>=100, delivered>=30 t) closes L0-05 strict",
                   "measured": f"{len(sp5_commercial)} cells satisfy commercial + L0-05 strict",
                   "verdict": "HELD" if len(sp5_commercial) == 0 else "FALSIFIED"})

    # H4: chunk-scaled bag (linear, 5% of chunk) is more permissive at small chunks but less at large chunks.
    # Test: at chunk=10, count all-pass-waiver across all (bus, sp, aero, isp) for flat-bag=8 vs linear-bag.
    small_chunk_linear = sum(1 for r in rows if r["chunk_t"] == 10 and r["bag_scaling"] == "linear"
                             and r["feasible"] and r["pass_l0_05_waiver"]
                             and r["pass_reactor_life"] and r["pass_launchable"])
    small_chunk_flat8 = sum(1 for r in rows if r["chunk_t"] == 10 and r["bag_scaling"] == "flat"
                            and r["m_bag_t"] == 8 and r["feasible"] and r["pass_l0_05_waiver"]
                            and r["pass_reactor_life"] and r["pass_launchable"])
    large_chunk_linear = sum(1 for r in rows if r["chunk_t"] == 200 and r["bag_scaling"] == "linear"
                             and r["feasible"] and r["pass_l0_05_waiver"]
                             and r["pass_reactor_life"] and r["pass_launchable"])
    large_chunk_flat8 = sum(1 for r in rows if r["chunk_t"] == 200 and r["bag_scaling"] == "flat"
                            and r["m_bag_t"] == 8 and r["feasible"] and r["pass_l0_05_waiver"]
                            and r["pass_reactor_life"] and r["pass_launchable"])
    crossover = small_chunk_linear > small_chunk_flat8 and large_chunk_linear < large_chunk_flat8
    grades.append({"hypothesis": "H4",
                   "predicted": "chunk-scaled bag is more permissive at small chunks (10 t), less at large (200 t)",
                   "measured": f"chunk=10: linear={small_chunk_linear} flat-8={small_chunk_flat8}; chunk=200: linear={large_chunk_linear} flat-8={large_chunk_flat8}",
                   "verdict": "HELD" if crossover else "FALSIFIED"})

    # H5: matrix's "Architecture E falsified at 23.6 yr" is artefact of full-bus anchor — at Cassini bus, the cell now passes waiver.
    # The R6 verdict used 500 kWe / 200 t chunk / Isp 2934 / mass model MARVL (~10 W/kg system specific power).
    archE_R6 = [r for r in rows if r["p_reactor_kwe"] == 500 and r["chunk_t"] == 200
                and r["specific_power_w_per_kg"] == 10 and r["isp_s"] == ISP_HIGH
                and r["aerocapture_credit_kms"] == 0  # no aerocapture in R6 model
                and r["bag_scaling"] == "linear"]
    archE_pass_at_cassini = [r for r in archE_R6 if r["m_bus_t"] == 2 and r["feasible"]
                             and r["pass_l0_05_waiver"] and r["pass_reactor_life"]]
    archE_pass_at_full = [r for r in archE_R6 if r["m_bus_t"] == 15 and r["feasible"]
                          and r["pass_l0_05_waiver"] and r["pass_reactor_life"]]
    grades.append({"hypothesis": "H5",
                   "predicted": "matrix R6 Arch-E falsified verdict (23.6 yr) reverses at Cassini bus",
                   "measured": f"Arch-E-R6 at Cassini-bus (m_bus=2): {len(archE_pass_at_cassini)} pass waiver; at full-bus (m_bus=15): {len(archE_pass_at_full)} pass waiver",
                   "verdict": "HELD" if (archE_pass_at_cassini and not archE_pass_at_full) else "FALSIFIED"})

    return grades


def write_tables(rows, grades, path):
    L = []
    L.append("# R-bus-mass-anchor-sweep — headline tables\n")
    L.append(f"Total cells: **{len(rows)}** (pure-electric inbound, single-stream Tsiolkovsky, no hydrolox).\n")
    L.append(f"Bus mass sweep: {{2, 5, 10, 15}} t. Bag mass: flat {{0.5, 2, 5, 8}} t OR linear (m_bag = 5% × chunk).\n")
    L.append(f"Cassini anchor: m_bus = 2 t. Europa Clipper anchor: m_bus ≈ 5.9 t. Full-bus prior anchor: m_bus = 15 t, m_bag = 8 t.\n")

    # 2D heatmap: bus × bag (flat) closure counts
    L.append("## All-pass-waiver count by (m_bus, m_bag) — FLAT bag, all other params marginalised\n")
    L.append("| m_bus \\ m_bag | 0.5 | 2 | 5 | 8 |")
    L.append("|---|---|---|---|---|")
    for bus in [2, 5, 10, 15]:
        cells = [f"m_bus={bus}"]
        for bag in [0.5, 2, 5, 8]:
            n = sum(1 for r in rows if r["m_bus_t"] == bus and r["bag_scaling"] == "flat"
                    and r["m_bag_t"] == bag and r["feasible"] and r["pass_l0_05_waiver"]
                    and r["pass_reactor_life"] and r["pass_launchable"])
            cells.append(str(n))
        L.append("| " + " | ".join(cells) + " |")
    L.append("")

    L.append("## All-pass-waiver count at LINEAR bag (m_bag = 5% × chunk_t)\n")
    L.append("| m_bus | count |")
    L.append("|---|---|")
    for bus in [2, 5, 10, 15]:
        n = sum(1 for r in rows if r["m_bus_t"] == bus and r["bag_scaling"] == "linear"
                and r["feasible"] and r["pass_l0_05_waiver"]
                and r["pass_reactor_life"] and r["pass_launchable"])
        L.append(f"| {bus} | {n} |")
    L.append("")

    # Cell-detail at Cassini anchor: show all all-pass cells
    cassini_pass = [r for r in rows if r["m_bus_t"] == 2 and r["bag_scaling"] == "linear"
                    and r["feasible"] and r["pass_l0_05_waiver"]
                    and r["pass_reactor_life"] and r["pass_launchable"]]
    L.append(f"## All-pass-waiver cells at Cassini anchor (m_bus=2 t, m_bag=5%×chunk), {len(cassini_pass)} cells\n")
    L.append("| P_kWe | chunk t | bag t | sp W/kg | aero km/s | Isp s | t_burn yr | RT yr | delivered t | LEO t | strict? | commercial? |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in sorted(cassini_pass, key=lambda r: -r["m_delivered_t"])[:50]:
        L.append(f"| {r['p_reactor_kwe']:.0f} | {r['chunk_t']:.0f} | {r['effective_bag_t']:.1f} | "
                 f"{r['specific_power_w_per_kg']:.1f} | {r['aerocapture_credit_kms']:.0f} | "
                 f"{r['isp_s']:.0f} | {r['t_burn_yr']:.2f} | {r['rt_yr']:.2f} | "
                 f"{r['m_delivered_t']:.2f} | {r['leo_stack_t']:.1f} | "
                 f"{r['pass_l0_05_strict']} | {r['pass_l0_09_commercial']} |")
    L.append("")

    # Commercial closures at Cassini anchor
    cassini_commercial = [r for r in cassini_pass if r["pass_l0_09_commercial"] and r["pass_l0_05_strict"]]
    L.append(f"## **Cassini-anchor cells that pass L0-05 strict AND L0-09 commercial floor (delivered ≥ 30 t)**: {len(cassini_commercial)}\n")
    if cassini_commercial:
        L.append("| P_kWe | chunk t | sp | aero | Isp | RT yr | delivered t |")
        L.append("|---|---|---|---|---|---|---|")
        for r in sorted(cassini_commercial, key=lambda r: -r["m_delivered_t"])[:20]:
            L.append(f"| {r['p_reactor_kwe']:.0f} | {r['chunk_t']:.0f} | {r['specific_power_w_per_kg']:.1f} | "
                     f"{r['aerocapture_credit_kms']:.0f} | {r['isp_s']:.0f} | "
                     f"{r['rt_yr']:.2f} | {r['m_delivered_t']:.2f} |")
        L.append("")

    L.append("## Hypothesis grades\n")
    L.append("| # | predicted | measured | verdict |")
    L.append("|---|---|---|---|")
    for g in grades:
        m = g['measured']
        if len(m) > 250:
            m = m[:250] + "..."
        L.append(f"| {g['hypothesis']} | {g['predicted']} | {m} | {g['verdict']} |")
    L.append("")

    path.write_text("\n".join(L))


def main():
    here = pathlib.Path(__file__).parent
    rd = here / "results"
    rd.mkdir(exist_ok=True)
    print("Sweeping bus-mass anchors...")
    rows = sweep()
    feas = sum(1 for r in rows if r["feasible"])
    all_pass = sum(1 for r in rows if r["feasible"]
                   and r["pass_l0_05_waiver"] and r["pass_reactor_life"] and r["pass_launchable"])
    print(f"  total = {len(rows)}, feasible = {feas}, all-pass-waiver = {all_pass}")
    g = grade(rows)
    for x in g:
        print(f"  {x['hypothesis']}: {x['verdict']}")
    feasible_rows = [r for r in rows if r["feasible"]]
    slim = {
        "summary": {"total": len(rows), "feasible": feas, "all_pass_waiver": all_pass},
        "feasible_rows": feasible_rows,
        "grades": g,
    }
    (rd / "results.json").write_text(json.dumps(slim, indent=2))
    write_tables(rows, g, rd / "tables.md")
    print(f"Wrote {rd / 'results.json'} and {rd / 'tables.md'}")


if __name__ == "__main__":
    main()
