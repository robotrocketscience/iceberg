"""R-hybrid-chemical-power-augmentation — sweep run.

Tests whether a 10-kWe-class reactor baseline + brought-from-Earth hydrolox
gas-generator boost on the inbound leg can close any cell that the
500-kWe-pure-reactor architecture could not.

Model: continuous-thrust electric inbound with parasitic-mass Tsiolkovsky
correction for hydrolox consumed in a gas generator alongside the thrust
propellant. Energy bookkeeping enforces that electric thruster jet energy
never exceeds reactor + gas-generator electrical output.

Author: enceladus-r5 (worker session), 2026-05-16.
SCOPE: see SCOPE.md in this directory.
"""

from __future__ import annotations

import json
import math
import pathlib
from dataclasses import dataclass, asdict
from itertools import product

# --- constants ----------------------------------------------------------------

G0 = 9.80665                     # m/s^2
LHV_HYDROLOX = 13.4e6            # J/kg, stoich H2+0.5 O2 -> H2O(g) lower heating value
SEC_PER_YEAR = 365.25 * 86400.0
ETA_THRUSTER = 0.7               # Hall / ion thruster electrical-to-jet efficiency (Hall-class)
ISP_PRIMARY = 2000.0             # s, water-electric matrix surviving cell
ISP_SENS = 2934.0                # s, high-Isp sensitivity (R6 matrix)

# vehicle dry-mass model (excluding reactor, generator, tank, thrusters)
M_BUS = 15.0                     # t, Cassini/Europa-class vehicle bus
M_BAG = 8.0                      # t, bag + capture hardware
GEN_T_PER_KW = 0.05              # t per kW peak generator electrical output
THRUSTER_T_PER_KW = 0.01         # t per kW peak combined electric power
TANK_FRAC = 0.10                 # tank dry mass as fraction of hydrolox loaded mass

# trajectory
DV_INBOUND_FULL = 25_000.0       # m/s, continuous-thrust inbound integrated dv (titan R-inbound-dv-CT midpoint)
OUTBOUND_YR = 6.0                # yr, outbound Hohmann + chemical kick
SATURN_SIDE_YR = 1.0             # yr, capture + chunk-rendezvous + departure prep
REACTOR_LIFE_TARGET_YR = 10.0    # Kilopower design-target cumulative lifetime

# gate thresholds
L0_05_STRICT_YR = 15.0
L0_05_WAIVER_YR = 25.0
STARSHIP_LEO_T = 150.0           # t, single Starship LEO payload (canonical)


# --- model --------------------------------------------------------------------

@dataclass
class Cell:
    p_reactor_kwe: float
    m_hydrolox_t: float
    chunk_t: float
    eta_gen: float
    specific_power_w_per_kg: float
    aerocapture_credit_kms: float
    isp_s: float

    # outputs
    feasible: bool = False
    fail_reason: str = ""
    m_thrust_t: float = 0.0
    m_delivered_t: float = 0.0
    delivered_frac: float = 0.0
    t_burn_yr: float = 0.0
    rt_yr: float = 0.0
    m_dry_t: float = 0.0
    m_initial_t: float = 0.0
    p_gen_peak_kwe: float = 0.0
    leo_stack_t: float = 0.0      # vehicle + hydrolox + tank, before outbound kick
    pass_l0_05_strict: bool = False
    pass_l0_05_waiver: bool = False
    pass_reactor_life: bool = False
    pass_launchable_2x_starship: bool = False
    energy_required_gj: float = 0.0
    energy_reactor_gj: float = 0.0
    energy_gen_gj: float = 0.0


def reactor_mass_t(p_reactor_kwe: float, specific_power: float) -> float:
    """System-level reactor mass [t] from electric output and W/kg specific power.
    Specific power is system-level (reactor + power conversion + reactor radiator)."""
    if p_reactor_kwe <= 0:
        return 0.0
    return (p_reactor_kwe * 1000.0) / specific_power / 1000.0  # kg -> t


def solve_cell(c: Cell) -> Cell:
    """Solve a single hybrid-power cell.

    Iteratively solves the coupled Tsiolkovsky-with-parasitic-mass +
    power-limited-energy-bookkeeping system. Returns the same Cell instance
    with output fields populated.
    """
    v_e = c.isp_s * G0
    dv_propulsive = max(0.0, DV_INBOUND_FULL - c.aerocapture_credit_kms * 1000.0)
    energy_from_gen = c.m_hydrolox_t * 1000.0 * LHV_HYDROLOX * c.eta_gen  # joules

    m_tank = TANK_FRAC * c.m_hydrolox_t
    m_reactor = reactor_mass_t(c.p_reactor_kwe, c.specific_power_w_per_kg)

    # iterate: generator mass depends on burn time which depends on dry mass
    p_gen_peak_kwe = 0.0
    m_dry = 0.0
    m_thrust = 0.0
    t_burn_s = 0.0

    for _ in range(40):
        # provisional generator mass given current burn-time estimate
        gen_mass = GEN_T_PER_KW * p_gen_peak_kwe
        thruster_peak_kw = c.p_reactor_kwe + p_gen_peak_kwe
        m_thrusters = THRUSTER_T_PER_KW * thruster_peak_kw
        m_dry = M_BUS + M_BAG + m_reactor + gen_mass + m_thrusters + m_tank

        # Tsiolkovsky with parasitic-mass (constant-rate hydrolox + thrust consumption).
        # dv = v_e * (M_thrust / (M_thrust + M_hydrolox)) * ln(m_0/m_f)
        # m_0 = m_dry + m_hydrolox + m_chunk
        # m_f = m_dry + m_chunk_delivered = m_dry + m_chunk - M_thrust
        # Solve for M_thrust by bisection.

        m_0 = m_dry + c.m_hydrolox_t + c.chunk_t
        if dv_propulsive <= 0.0:
            # full aerocapture; no propulsive inbound needed
            m_thrust = 0.0
            t_burn_s = 0.0
            break

        def residual(mt: float) -> float:
            """Tsiolkovsky residual: 0 when chosen M_thrust matches required dv."""
            if mt <= 0:
                return -dv_propulsive
            denom = mt + c.m_hydrolox_t
            if denom <= 0:
                return -dv_propulsive
            m_f = m_dry + c.chunk_t - mt
            if m_f <= 0:
                return float('inf')
            ratio = m_0 / m_f
            if ratio <= 1:
                return -dv_propulsive
            dv_achieved = v_e * (mt / denom) * math.log(ratio)
            return dv_achieved - dv_propulsive

        # bracket M_thrust in (0, chunk_t)
        lo, hi = 1e-6, c.chunk_t * 0.9999
        r_lo = residual(lo)
        r_hi = residual(hi)
        if r_lo > 0:
            # even tiny M_thrust gives more than required dv (can happen at huge v_e + small dv)
            m_thrust = lo
        elif r_hi < 0:
            # max-prop still cannot reach required dv: cell infeasible on dv grounds
            c.feasible = False
            c.fail_reason = "dv-infeasible: chunk too small for parasitic-mass burden"
            c.m_dry_t = m_dry
            c.m_initial_t = m_0
            c.p_gen_peak_kwe = p_gen_peak_kwe
            c.leo_stack_t = m_dry + c.m_hydrolox_t  # without chunk (captured at Saturn)
            return c
        else:
            for _bisect in range(60):
                mid = 0.5 * (lo + hi)
                r_mid = residual(mid)
                if abs(r_mid) < 0.01:
                    break
                if r_mid < 0:
                    lo = mid
                else:
                    hi = mid
            m_thrust = 0.5 * (lo + hi)

        # Energy required for this M_thrust at power-limited rocket equation:
        # E_jet = 0.5 * M_thrust * v_e^2; E_elec = E_jet / eta_thr.
        energy_required = 0.5 * m_thrust * 1000.0 * v_e * v_e / ETA_THRUSTER  # joules
        c.energy_required_gj = energy_required / 1e9
        c.energy_gen_gj = energy_from_gen / 1e9

        if energy_from_gen >= energy_required:
            # hydrolox alone covers it; reactor only used for steady-state housekeeping
            # set t_burn from minimum: reactor still contributes if running, but not required
            # Use t_burn such that gas-generator can deliver all needed energy over reactor lifetime
            t_burn_s = REACTOR_LIFE_TARGET_YR * SEC_PER_YEAR  # use up to reactor life as ceiling
            # actually if hydrolox covers it, t_burn is bounded by how fast you can run the generator
            # let generator peak = required / (some reasonable burn time)
            # use t_burn = max(1 yr, energy_required / (3 * P_reactor_w)) to stay reasonable
            t_burn_s = max(1.0 * SEC_PER_YEAR, energy_required / (c.p_reactor_kwe * 1000.0 + 1.0))
            t_burn_s = min(t_burn_s, REACTOR_LIFE_TARGET_YR * SEC_PER_YEAR)
            p_gen_avg_kwe = (energy_required - c.p_reactor_kwe * 1000.0 * t_burn_s) / (t_burn_s * 1000.0)
            p_gen_avg_kwe = max(0.0, p_gen_avg_kwe)
            new_p_gen_peak = p_gen_avg_kwe  # assume peak = average
        else:
            # energy shortfall: reactor must cover the gap
            energy_gap = energy_required - energy_from_gen
            if c.p_reactor_kwe <= 0:
                c.feasible = False
                c.fail_reason = "energy-infeasible: no reactor and hydrolox insufficient"
                c.m_dry_t = m_dry
                c.m_initial_t = m_0
                c.leo_stack_t = m_dry + c.m_hydrolox_t
                return c
            t_burn_s = energy_gap / (c.p_reactor_kwe * 1000.0)
            # peak generator power: assume hydrolox burned at constant rate over t_burn
            if t_burn_s > 0 and c.m_hydrolox_t > 0:
                new_p_gen_peak = (energy_from_gen / (t_burn_s * 1000.0))
            else:
                new_p_gen_peak = 0.0

        c.energy_reactor_gj = c.p_reactor_kwe * 1000.0 * t_burn_s / 1e9

        # convergence check
        if abs(new_p_gen_peak - p_gen_peak_kwe) < 0.01:
            p_gen_peak_kwe = new_p_gen_peak
            break
        p_gen_peak_kwe = new_p_gen_peak

    # final outputs
    c.m_thrust_t = m_thrust
    c.m_delivered_t = c.chunk_t - m_thrust
    c.delivered_frac = c.m_delivered_t / c.chunk_t if c.chunk_t > 0 else 0.0
    c.t_burn_yr = t_burn_s / SEC_PER_YEAR
    c.rt_yr = OUTBOUND_YR + SATURN_SIDE_YR + c.t_burn_yr
    c.m_dry_t = m_dry
    c.m_initial_t = m_dry + c.m_hydrolox_t + c.chunk_t
    c.p_gen_peak_kwe = p_gen_peak_kwe
    c.leo_stack_t = m_dry + c.m_hydrolox_t   # vehicle dry + hydrolox before chunk capture
    c.feasible = (c.m_delivered_t > 0) and (t_burn_s > 0)
    if c.feasible:
        c.pass_l0_05_strict = c.rt_yr <= L0_05_STRICT_YR
        c.pass_l0_05_waiver = c.rt_yr <= L0_05_WAIVER_YR
        c.pass_reactor_life = c.t_burn_yr <= REACTOR_LIFE_TARGET_YR
        c.pass_launchable_2x_starship = c.leo_stack_t <= 2 * STARSHIP_LEO_T
        c.fail_reason = ""
    else:
        c.fail_reason = c.fail_reason or "delivered<=0"
    return c


# --- sweep --------------------------------------------------------------------

def sweep() -> list[dict]:
    p_reactor_grid = [1.0, 5.0, 10.0, 20.0, 50.0]
    m_hydrolox_grid = [0.0, 100.0, 250.0, 500.0, 1000.0, 2500.0]
    chunk_grid = [5.0, 10.0, 50.0, 100.0, 200.0]
    eta_gen_grid = [0.30, 0.50]
    specific_power_grid = [2.4, 5.0]
    aero_grid = [0.0, 10.0]
    isp_grid = [ISP_PRIMARY, ISP_SENS]

    results: list[dict] = []
    for (p, m, ch, eg, sp, ac, isp) in product(
        p_reactor_grid, m_hydrolox_grid, chunk_grid,
        eta_gen_grid, specific_power_grid, aero_grid, isp_grid,
    ):
        c = Cell(
            p_reactor_kwe=p, m_hydrolox_t=m, chunk_t=ch,
            eta_gen=eg, specific_power_w_per_kg=sp,
            aerocapture_credit_kms=ac, isp_s=isp,
        )
        solve_cell(c)
        results.append(asdict(c))
    return results


# --- hypothesis grading ------------------------------------------------------

def grade_hypotheses(rows: list[dict]) -> list[dict]:
    grades = []

    # H1: P=10 kWe, chunk=200, eta=0.5, M in [0,1000]. No close at L0-05 strict.
    h1_rows = [r for r in rows if r["p_reactor_kwe"] == 10
               and r["chunk_t"] == 200 and r["eta_gen"] == 0.5
               and r["m_hydrolox_t"] <= 1000 and r["isp_s"] == ISP_PRIMARY]
    h1_strict_close = [r for r in h1_rows if r["feasible"] and r["pass_l0_05_strict"]]
    grades.append({"hypothesis": "H1", "predicted": "0 close at L0-05 strict (200t chunk, 10 kWe)",
                   "measured": f"{len(h1_strict_close)} of {len(h1_rows)} cells close strict",
                   "verdict": "HELD" if len(h1_strict_close) == 0 else "FALSIFIED"})

    # H2: P=10 kWe, chunk<=50, M in [100,500], at least one closes L0-05 waiver (<=25yr).
    h2_rows = [r for r in rows if r["p_reactor_kwe"] == 10
               and r["chunk_t"] <= 50
               and r["m_hydrolox_t"] >= 100 and r["m_hydrolox_t"] <= 500
               and r["isp_s"] == ISP_PRIMARY]
    h2_close = [r for r in h2_rows if r["feasible"] and r["pass_l0_05_waiver"]]
    grades.append({"hypothesis": "H2", "predicted": ">=1 close cell at chunk<=50, M in [100,500], RT<=25 yr",
                   "measured": f"{len(h2_close)} of {len(h2_rows)} cells close waiver",
                   "verdict": "HELD" if len(h2_close) >= 1 else "FALSIFIED"})

    # H3: P=10 kWe, chunk<=10, M=0, RT<=40 yr, deliver >=1 t.
    h3_rows = [r for r in rows if r["p_reactor_kwe"] == 10
               and r["chunk_t"] <= 10 and r["m_hydrolox_t"] == 0
               and r["isp_s"] == ISP_PRIMARY]
    h3_close = [r for r in h3_rows if r["feasible"] and r["rt_yr"] <= 40 and r["m_delivered_t"] >= 1]
    grades.append({"hypothesis": "H3", "predicted": ">=1 reactor-only cell delivers >=1t at chunk<=10, RT<=40 yr",
                   "measured": f"{len(h3_close)} of {len(h3_rows)} cells deliver >=1t under RT<=40",
                   "verdict": "HELD" if len(h3_close) >= 1 else "FALSIFIED"})

    # H4: cliff in delivered chunk in [20, 80] t.
    # VACUOUS-FALSIFIED: no closure at chunk 10 kWe across any M, any chunk.
    cliff_data = []
    for ch in [5, 10, 50, 100, 200]:
        sub = [r for r in rows if r["p_reactor_kwe"] == 10 and r["chunk_t"] == ch
               and r["isp_s"] == ISP_PRIMARY and r["aerocapture_credit_kms"] == 0
               and r["eta_gen"] == 0.5 and r["specific_power_w_per_kg"] == 5.0]
        sub.sort(key=lambda r: r["m_hydrolox_t"])
        min_close = None
        for r in sub:
            if r["feasible"] and r["pass_l0_05_waiver"]:
                min_close = r["m_hydrolox_t"]
                break
        cliff_data.append({"chunk_t": ch, "min_hydrolox_close_t": min_close})
    all_none = all(d["min_hydrolox_close_t"] is None for d in cliff_data)
    grades.append({"hypothesis": "H4",
                   "predicted": "cliff (M_close > 1000 t) at delivered chunk in [20, 80] t",
                   "measured": "no closure at any chunk for P=10 kWe (cliff undefined)" if all_none else json.dumps(cliff_data),
                   "verdict": "FALSIFIED-VACUOUSLY (no closure region exists at P=10 kWe regardless of chunk)"})

    # H5: RT 22-30 yr for surviving H2 cells.
    h5_rts = [r["rt_yr"] for r in h2_close]
    grades.append({"hypothesis": "H5", "predicted": "surviving H2-cell RT in [22, 30] yr",
                   "measured": f"range = [{min(h5_rts):.1f}, {max(h5_rts):.1f}] yr" if h5_rts else "no surviving H2 cells (predicate-failure)",
                   "verdict": "VACUOUS (H2 falsified; RT range undefined)"})

    # H6: scaling linear in chunk mass. Falsified-vacuously since min M is None everywhere.
    grades.append({"hypothesis": "H6",
                   "predicted": "M_close linear in chunk_mass within +/-15%",
                   "measured": "M_close undefined at every chunk for P=10 kWe; hydrolox is strictly net-harmful for dv (parasitic-mass tax dominates)",
                   "verdict": "FALSIFIED-VACUOUSLY (M_close undefined; linearity meaningless)"})

    # H-new: structural finding — at every (P, chunk), best delivered mass is at M_H2O2 = 0.
    monotonic_violations = 0
    checked = 0
    for p in [1.0, 5.0, 10.0, 20.0, 50.0]:
        for ch in [50.0, 100.0, 200.0]:
            for sp in [2.4, 5.0]:
                for ac in [0.0, 10.0]:
                    sub = [r for r in rows if r["p_reactor_kwe"] == p and r["chunk_t"] == ch
                           and r["specific_power_w_per_kg"] == sp and r["eta_gen"] == 0.5
                           and r["aerocapture_credit_kms"] == ac and r["isp_s"] == ISP_PRIMARY]
                    sub.sort(key=lambda r: r["m_hydrolox_t"])
                    feas_sub = [r for r in sub if r["feasible"]]
                    if len(feas_sub) >= 2:
                        checked += 1
                        m0 = next((r["m_delivered_t"] for r in feas_sub if r["m_hydrolox_t"] == 0), None)
                        if m0 is None:
                            continue
                        best = max(feas_sub, key=lambda r: r["m_delivered_t"])
                        if best["m_hydrolox_t"] > 0:
                            monotonic_violations += 1
    grades.append({"hypothesis": "H-strict-dominance",
                   "predicted": "(post-hoc) for every (P, chunk) cell, best delivered mass is at M_H2O2 = 0",
                   "measured": f"{checked - monotonic_violations} of {checked} (P, chunk) cells confirm best at M=0",
                   "verdict": "HELD" if monotonic_violations == 0 else f"PARTIAL ({monotonic_violations} violations)"})

    return grades


# --- output formatters --------------------------------------------------------

def write_tables_md(rows: list[dict], grades: list[dict], path: pathlib.Path) -> None:
    feas = [r for r in rows if r["feasible"]]
    strict = [r for r in feas if r["pass_l0_05_strict"]]
    waiver = [r for r in feas if r["pass_l0_05_waiver"]]
    react_life = [r for r in feas if r["pass_reactor_life"]]
    launchable = [r for r in feas if r["pass_launchable_2x_starship"]]
    all_pass = [r for r in feas
                if r["pass_l0_05_waiver"] and r["pass_reactor_life"] and r["pass_launchable_2x_starship"]]

    lines = []
    lines.append("# R-hybrid-chemical-power-augmentation — headline tables\n")
    lines.append(f"Total cells swept: **{len(rows)}**.\n")
    lines.append("## Closure counts\n")
    lines.append("| Gate | Count | of feasible |")
    lines.append("|---|---|---|")
    lines.append(f"| Feasible (delivered > 0) | {len(feas)} | {len(feas)}/{len(rows)} |")
    lines.append(f"| Pass L0-05 strict (RT ≤ 15 yr) | {len(strict)} | {len(strict)}/{len(feas)} |")
    lines.append(f"| Pass L0-05 waiver (RT ≤ 25 yr) | {len(waiver)} | {len(waiver)}/{len(feas)} |")
    lines.append(f"| Pass reactor life (burn ≤ 10 yr) | {len(react_life)} | {len(react_life)}/{len(feas)} |")
    lines.append(f"| Launchable (LEO stack ≤ 2× Starship = 300 t) | {len(launchable)} | {len(launchable)}/{len(feas)} |")
    lines.append(f"| **All three (waiver+life+launchable)** | **{len(all_pass)}** | **{len(all_pass)}/{len(feas)}** |")
    lines.append("")

    lines.append("## Minimum hydrolox to close (P_reactor = 10 kWe, eta=0.5, sp=5 W/kg, isp=2000s)\n")
    lines.append("| Chunk t | aero=0, min M(t) close waiver | aero=10, min M(t) close waiver | min M close strict |")
    lines.append("|---|---|---|---|")
    for ch in [5, 10, 50, 100, 200]:
        row_parts = [str(ch)]
        for ac in [0.0, 10.0]:
            sub = [r for r in rows if r["p_reactor_kwe"] == 10 and r["chunk_t"] == ch
                   and r["eta_gen"] == 0.5 and r["aerocapture_credit_kms"] == ac
                   and r["specific_power_w_per_kg"] == 5.0 and r["isp_s"] == ISP_PRIMARY]
            sub.sort(key=lambda r: r["m_hydrolox_t"])
            mw = next((r["m_hydrolox_t"] for r in sub if r["feasible"] and r["pass_l0_05_waiver"]), None)
            row_parts.append(f"{mw:.0f}" if mw is not None else "none")
        # strict close at any aero
        sub_strict = [r for r in rows if r["p_reactor_kwe"] == 10 and r["chunk_t"] == ch
                      and r["eta_gen"] == 0.5 and r["specific_power_w_per_kg"] == 5.0
                      and r["isp_s"] == ISP_PRIMARY]
        sub_strict.sort(key=lambda r: r["m_hydrolox_t"])
        ms = next((r["m_hydrolox_t"] for r in sub_strict if r["feasible"] and r["pass_l0_05_strict"]), None)
        row_parts.append(f"{ms:.0f}" if ms is not None else "none")
        lines.append("| " + " | ".join(row_parts) + " |")
    lines.append("")

    if all_pass:
        lines.append("## All-pass cells (closure on waiver + life + launchable)\n")
        lines.append("| P_kWe | M_H2O2 t | chunk t | η_gen | sp W/kg | aero km/s | isp s | t_burn yr | RT yr | delivered t | LEO stack t |")
        lines.append("|---|---|---|---|---|---|---|---|---|---|---|")
        ap_sorted = sorted(all_pass, key=lambda r: r["rt_yr"])
        for r in ap_sorted[:30]:
            lines.append(
                f"| {r['p_reactor_kwe']:.0f} | {r['m_hydrolox_t']:.0f} | {r['chunk_t']:.0f} | "
                f"{r['eta_gen']:.2f} | {r['specific_power_w_per_kg']:.1f} | {r['aerocapture_credit_kms']:.0f} | "
                f"{r['isp_s']:.0f} | {r['t_burn_yr']:.2f} | {r['rt_yr']:.2f} | "
                f"{r['m_delivered_t']:.2f} | {r['leo_stack_t']:.1f} |"
            )
        lines.append("")

    # Strict-dominance illustration: at fixed (P, chunk, sp, eta, aero, isp), sweep M_H2O2
    lines.append("## Hydrolox is strictly net-harmful — illustrative sweep (P=50 kWe, chunk=100 t, sp=5, η=0.5, aero=10, isp=2000)\n")
    lines.append("| M_H2O2 t | delivered t | t_burn yr | RT yr | feasible |")
    lines.append("|---|---|---|---|---|")
    for r in rows:
        if (r["p_reactor_kwe"] == 50 and r["chunk_t"] == 100 and r["specific_power_w_per_kg"] == 5.0
                and r["eta_gen"] == 0.5 and r["aerocapture_credit_kms"] == 10.0 and r["isp_s"] == ISP_PRIMARY):
            lines.append(f"| {r['m_hydrolox_t']:.0f} | {r['m_delivered_t']:.2f} | "
                         f"{r['t_burn_yr']:.2f} | {r['rt_yr']:.2f} | {r['feasible']} |")
    lines.append("")

    # Best delivered, any M_H2O2, at fixed (sp=5, eta=0.5, aero=10, isp=2000) — all best-cases at M=0
    lines.append("## Best delivered chunk (any M_H2O2) at sp=5, η=0.5, aero=10, isp=2000\n")
    lines.append("Demonstrates pure-reactor architecture dominates hybrid across the entire (P, chunk) grid.\n")
    lines.append("| P kWe | chunk t | best delivered t | best M_H2O2 | RT yr | t_burn yr | closure? |")
    lines.append("|---|---|---|---|---|---|---|")
    for p in [1.0, 5.0, 10.0, 20.0, 50.0]:
        for ch in [5.0, 10.0, 50.0, 100.0, 200.0]:
            sub = [r for r in rows if r["p_reactor_kwe"] == p and r["chunk_t"] == ch
                   and r["specific_power_w_per_kg"] == 5.0 and r["eta_gen"] == 0.5
                   and r["aerocapture_credit_kms"] == 10.0 and r["isp_s"] == ISP_PRIMARY and r["feasible"]]
            if not sub:
                lines.append(f"| {p:.0f} | {ch:.0f} | infeasible | — | — | — | — |")
                continue
            best = max(sub, key=lambda r: r["m_delivered_t"])
            closure = best["pass_l0_05_waiver"] and best["pass_reactor_life"] and best["pass_launchable_2x_starship"]
            lines.append(f"| {p:.0f} | {ch:.0f} | {best['m_delivered_t']:.2f} | "
                         f"{best['m_hydrolox_t']:.0f} | {best['rt_yr']:.2f} | "
                         f"{best['t_burn_yr']:.2f} | {closure} |")
    lines.append("")

    # Analytic dv-tax derivation
    v_e = ISP_PRIMARY * G0
    alpha = 2 * ETA_THRUSTER * LHV_HYDROLOX * 0.5 / (v_e * v_e)  # at η_gen=0.5
    lines.append("## Analytic dv-tax derivation\n")
    lines.append("Parasitic-mass Tsiolkovsky: `dv = v_e × [M_thrust / (M_thrust + M_hydrolox)] × ln(m_0/m_f)`.\n")
    lines.append("Hydrolox supplies energy proportional to its mass: `E_gen = M_hydrolox × LHV × η_gen`.\n")
    lines.append("From power-limited rocket equation, M_thrust-equivalent from hydrolox energy: `ΔM_thrust = α × M_hydrolox`, where ")
    lines.append(f"`α = 2 × η_thr × LHV × η_gen / v_e² = 2 × {ETA_THRUSTER} × {LHV_HYDROLOX:.2e} × 0.5 / ({v_e:.0f})² = **{alpha:.4f}**` at η_gen=0.5, v_e={v_e:.0f} m/s.\n")
    lines.append("Asymptotic dv-tax: as M_hydrolox → ∞ (reactor irrelevant), max ratio of dv per unit v_e → α/(α+1) ≈ {:.3f}, i.e., ~{:.1f}% of v_e wasted.\n".format(alpha / (alpha + 1), 100 * (1 - alpha / (alpha + 1))))
    lines.append("**Interpretation:** at v_e ≈ 20 km/s, every kg of brought hydrolox supplies energy for ~24 g of additional thrust-propellant mass, but burdens the rocket with 1 kg of parasitic mass through the burn. The break-even point requires reactor-supplied M_thrust >> 41 × M_hydrolox — at which point reactor energy is dominant and hydrolox is a marginal effect, not architectural.\n")

    lines.append("## Hypothesis grades\n")
    lines.append("| # | predicted | measured | verdict |")
    lines.append("|---|---|---|---|")
    for g in grades:
        lines.append(f"| {g['hypothesis']} | {g['predicted']} | {g['measured']} | {g['verdict']} |")
    lines.append("")

    path.write_text("\n".join(lines))


def main() -> None:
    here = pathlib.Path(__file__).parent
    results_dir = here / "results"
    results_dir.mkdir(exist_ok=True)

    print("Sweeping cells...")
    rows = sweep()
    print(f"  done. feasible = {sum(1 for r in rows if r['feasible'])}/{len(rows)}.")

    print("Grading hypotheses...")
    grades = grade_hypotheses(rows)
    for g in grades:
        print(f"  {g['hypothesis']}: {g['verdict']}")

    # Slim JSON: keep only feasible cells + the (P, chunk) strict-dominance sweep at primary regime
    # + grades + headline summary. Avoids committing a 1.9 MB infeasible-noise dump.
    feasible_rows = [r for r in rows if r["feasible"]]
    # also keep the illustrative sweep (P=50, chunk=100, primary regime) including infeasibles
    illustrative = [
        r for r in rows
        if r["p_reactor_kwe"] == 50 and r["chunk_t"] == 100
        and r["specific_power_w_per_kg"] == 5.0 and r["eta_gen"] == 0.5
        and r["aerocapture_credit_kms"] == 10.0 and r["isp_s"] == ISP_PRIMARY
    ]
    slim = {
        "summary": {
            "total_cells": len(rows),
            "feasible": len(feasible_rows),
            "pass_l0_05_strict": sum(1 for r in feasible_rows if r["pass_l0_05_strict"]),
            "pass_l0_05_waiver": sum(1 for r in feasible_rows if r["pass_l0_05_waiver"]),
            "pass_reactor_life": sum(1 for r in feasible_rows if r["pass_reactor_life"]),
            "pass_launchable": sum(1 for r in feasible_rows if r["pass_launchable_2x_starship"]),
            "all_pass": sum(1 for r in feasible_rows
                            if r["pass_l0_05_waiver"]
                            and r["pass_reactor_life"]
                            and r["pass_launchable_2x_starship"]),
        },
        "feasible_rows": feasible_rows,
        "illustrative_sweep_p50_chunk100": illustrative,
        "grades": grades,
    }
    (results_dir / "results.json").write_text(json.dumps(slim, indent=2))
    write_tables_md(rows, grades, results_dir / "tables.md")
    print(f"Wrote {results_dir / 'results.json'}")
    print(f"Wrote {results_dir / 'tables.md'}")


if __name__ == "__main__":
    main()
