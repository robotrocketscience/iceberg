"""R-hybrid-power-generator-exhaust-revisit — fixes the load-bearing assumption
from R-hybrid-chemical-power-augmentation (commit `98a9ded`) that gas-generator
exhaust contributes zero thrust.

Prior round assumed configuration (a): exhaust vented perpendicular to thrust
axis, no impulse contribution. That is structurally pessimistic — physically
the exhaust must go somewhere, and venting it through a vacuum-expansion nozzle
along the thrust axis is strictly better. This round runs configuration (b):
two-stream rocket equation with water-electric thrust at high specific impulse
AND hydrolox-chemical thrust at the post-turbine residual specific impulse.

Two-stream rocket equation (constant-rate consumption of both streams):
    dv = v_e_effective × ln(m_0 / m_f)
    v_e_effective = (M_water × v_e_water + M_hydrolox × v_e_hydrolox)
                  / (M_water + M_hydrolox)

Energy conservation: hydrolox LHV = η_gen × LHV (electrical) + (1 − η_gen) × LHV
(thermal). The electrical fraction routes through reactor + thrusters at high
v_e_water; the thermal residual expands through a nozzle at
v_e_hydrolox = sqrt(2 × (1 − η_gen) × LHV × η_nozzle).

This is the same hardware as the prior round (reactor + gas-generator + tank +
electric thrusters), with an exit nozzle added on the gas-generator outlet.

Author: enceladus-r5 (worker session), 2026-05-16.
"""

from __future__ import annotations

import json
import math
import pathlib
from dataclasses import dataclass, asdict
from itertools import product

# --- constants ----------------------------------------------------------------

G0 = 9.80665
LHV_HYDROLOX = 13.4e6
SEC_PER_YEAR = 365.25 * 86400.0

# revised efficiency anchors (water-electric is less efficient than Hall-class)
ETA_THRUSTER = 0.5            # water-electric MET / arcjet class, was 0.7 in prior round
ETA_NOZZLE = 0.85             # vacuum-expansion gas-generator outlet nozzle

ISP_PRIMARY = 2000.0
ISP_SENS = 2934.0

# mass model (unchanged from prior round)
M_BUS = 15.0
M_BAG = 8.0
GEN_T_PER_KW = 0.05
THRUSTER_T_PER_KW = 0.01
TANK_FRAC = 0.10

DV_INBOUND_FULL = 25_000.0
OUTBOUND_YR = 6.0
SATURN_SIDE_YR = 1.0
REACTOR_LIFE_TARGET_YR = 10.0

L0_05_STRICT_YR = 15.0
L0_05_WAIVER_YR = 25.0
STARSHIP_LEO_T = 150.0

# also try a sub-demonstrator-class lightweight bus + bag (questions a second assumption)
M_BUS_DEMO = 5.0   # CubeSat / SmallSat-derived stack
M_BAG_DEMO = 2.0   # demonstrator-class bag at <= 10-t chunk


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
    bus_class: str   # "full" or "demo"

    # outputs
    feasible: bool = False
    fail_reason: str = ""
    m_water_t: float = 0.0       # water thrust mass
    m_delivered_t: float = 0.0
    delivered_frac: float = 0.0
    t_burn_yr: float = 0.0
    rt_yr: float = 0.0
    m_dry_t: float = 0.0
    m_initial_t: float = 0.0
    v_e_w_mps: float = 0.0
    v_e_h_mps: float = 0.0
    v_e_eff_mps: float = 0.0
    p_gen_peak_kwe: float = 0.0
    leo_stack_t: float = 0.0
    pass_l0_05_strict: bool = False
    pass_l0_05_waiver: bool = False
    pass_reactor_life: bool = False
    pass_launchable_2x_starship: bool = False
    dv_achieved_mps: float = 0.0
    dv_required_mps: float = 0.0


def reactor_mass_t(p_reactor_kwe: float, specific_power: float) -> float:
    if p_reactor_kwe <= 0:
        return 0.0
    return p_reactor_kwe / specific_power  # kW / (W/kg) = kg ... but want tonnes
    # Hmm: P[kWe] = P*1000 [W]. (P*1000)/sp[W/kg] = mass [kg]. Then /1000 -> tonnes.
    # So mass_t = P_kWe / sp. Same number, units check.


def solve_cell(c: Cell) -> Cell:
    """Two-stream rocket equation: water-electric at v_e_w + hydrolox-chemical at v_e_h.

    Energy balance:
        E_elec_required = 0.5 * M_water * v_e_w^2 / eta_thr
        E_elec_available = P_reactor * t_burn + M_hydrolox * eta_gen * LHV
    Rocket equation (Tsiolkovsky with mass-flow-weighted v_e):
        dv = v_e_eff * ln(m_0 / m_f)
        v_e_eff = (M_water * v_e_w + M_hydrolox * v_e_h) / (M_water + M_hydrolox)

    Solve for (M_water, t_burn) iteratively.
    """
    v_e_w = c.isp_s * G0
    v_e_h = math.sqrt(2.0 * (1.0 - c.eta_gen) * LHV_HYDROLOX * ETA_NOZZLE)
    c.v_e_w_mps = v_e_w
    c.v_e_h_mps = v_e_h
    dv_required = max(0.0, DV_INBOUND_FULL - c.aerocapture_credit_kms * 1000.0)
    c.dv_required_mps = dv_required

    m_tank = TANK_FRAC * c.m_hydrolox_t
    m_reactor = reactor_mass_t(c.p_reactor_kwe, c.specific_power_w_per_kg)
    m_bus = M_BUS_DEMO if c.bus_class == "demo" else M_BUS
    m_bag = M_BAG_DEMO if c.bus_class == "demo" else M_BAG

    p_gen_peak_kwe = 0.0
    m_dry = 0.0
    m_water = 0.0
    t_burn_s = 0.0

    for _outer in range(40):
        gen_mass = GEN_T_PER_KW * p_gen_peak_kwe
        thruster_peak_kw = c.p_reactor_kwe + p_gen_peak_kwe
        m_thrusters = THRUSTER_T_PER_KW * thruster_peak_kw
        m_dry = m_bus + m_bag + m_reactor + gen_mass + m_thrusters + m_tank

        m_0 = m_dry + c.m_hydrolox_t + c.chunk_t
        if dv_required <= 0.0:
            m_water = 0.0
            t_burn_s = 0.0
            break

        # Rocket equation: solve for M_water that achieves dv_required.
        def residual(mw: float) -> float:
            if mw <= 0 and c.m_hydrolox_t <= 0:
                return -dv_required
            denom = mw + c.m_hydrolox_t
            if denom <= 0:
                return -dv_required
            v_e_eff = (mw * v_e_w + c.m_hydrolox_t * v_e_h) / denom
            m_f = m_dry + c.chunk_t - mw
            if m_f <= 0:
                return float('inf')
            if m_0 / m_f <= 1:
                return -dv_required
            return v_e_eff * math.log(m_0 / m_f) - dv_required

        # Special case: chunk = 0 + hydrolox > 0. Pure chemical rocket (M_water = 0).
        if c.chunk_t <= 0:
            # No water-electric thrust; check pure chemical
            if c.m_hydrolox_t <= 0:
                c.feasible = False
                c.fail_reason = "no propellant at all"
                return c

        # bisection
        lo = 0.0 if c.m_hydrolox_t > 0 else 1e-6
        hi = c.chunk_t * 0.9999 if c.chunk_t > 0 else 0.0

        if hi <= lo:
            mw = 0.0
            # check if pure chemical (M_water = 0) closes
            r = residual(0.0)
            if r >= 0:
                m_water = 0.0
            else:
                c.feasible = False
                c.fail_reason = "chunk=0 and pure-chemical short of dv"
                c.m_dry_t = m_dry
                c.m_initial_t = m_0
                c.dv_achieved_mps = v_e_h * math.log(m_0 / (m_dry)) if m_dry > 0 else 0
                return c
        else:
            r_lo = residual(lo)
            r_hi = residual(hi)
            if r_lo >= 0:
                m_water = lo
            elif r_hi < 0:
                # max water + full hydrolox can't reach required dv
                # record dv-achievable for analysis
                denom = hi + c.m_hydrolox_t
                v_e_eff_max = (hi * v_e_w + c.m_hydrolox_t * v_e_h) / denom if denom > 0 else 0
                m_f_max = m_dry + c.chunk_t - hi
                dv_max = v_e_eff_max * math.log(m_0 / m_f_max) if m_f_max > 0 else 0
                c.feasible = False
                c.fail_reason = f"dv-infeasible (max dv {dv_max:.0f} < {dv_required:.0f} m/s)"
                c.dv_achieved_mps = dv_max
                c.m_dry_t = m_dry
                c.m_initial_t = m_0
                c.leo_stack_t = m_dry + c.m_hydrolox_t
                return c
            else:
                for _b in range(60):
                    mid = 0.5 * (lo + hi)
                    rm = residual(mid)
                    if abs(rm) < 0.05:
                        break
                    if rm < 0:
                        lo = mid
                    else:
                        hi = mid
                m_water = 0.5 * (lo + hi)

        # energy bookkeeping
        e_water_needed = 0.5 * m_water * 1000.0 * v_e_w * v_e_w / ETA_THRUSTER  # joules
        e_hydrolox_elec = c.m_hydrolox_t * 1000.0 * c.eta_gen * LHV_HYDROLOX

        if e_water_needed <= e_hydrolox_elec:
            # hydrolox alone supplies enough electrical energy; reactor's role is reduced
            # set t_burn from reactor capacity (run reactor at rated for full e_water_needed if needed)
            # default: burn over 1 yr or more to keep thruster peak reasonable
            t_burn_s = max(1.0 * SEC_PER_YEAR, e_water_needed / max(c.p_reactor_kwe * 1000.0 + 1.0, 1e-6))
            t_burn_s = min(t_burn_s, REACTOR_LIFE_TARGET_YR * SEC_PER_YEAR)
            p_gen_avg_kwe = max(0.0, (e_hydrolox_elec) / (t_burn_s * 1000.0))
        else:
            energy_gap = e_water_needed - e_hydrolox_elec
            if c.p_reactor_kwe <= 0:
                c.feasible = False
                c.fail_reason = "no reactor and hydrolox-elec insufficient"
                c.m_dry_t = m_dry
                c.m_initial_t = m_0
                c.leo_stack_t = m_dry + c.m_hydrolox_t
                return c
            t_burn_s = energy_gap / (c.p_reactor_kwe * 1000.0)
            p_gen_avg_kwe = (e_hydrolox_elec / (t_burn_s * 1000.0)) if (t_burn_s > 0 and c.m_hydrolox_t > 0) else 0.0

        new_p_gen_peak = p_gen_avg_kwe
        if abs(new_p_gen_peak - p_gen_peak_kwe) < 0.01:
            p_gen_peak_kwe = new_p_gen_peak
            break
        p_gen_peak_kwe = new_p_gen_peak

    c.m_water_t = m_water
    c.m_delivered_t = c.chunk_t - m_water if c.chunk_t > 0 else 0.0
    c.delivered_frac = (c.m_delivered_t / c.chunk_t) if c.chunk_t > 0 else 0.0
    c.t_burn_yr = t_burn_s / SEC_PER_YEAR
    c.rt_yr = OUTBOUND_YR + SATURN_SIDE_YR + c.t_burn_yr
    c.m_dry_t = m_dry
    c.m_initial_t = m_dry + c.m_hydrolox_t + c.chunk_t
    c.p_gen_peak_kwe = p_gen_peak_kwe
    c.leo_stack_t = m_dry + c.m_hydrolox_t
    denom = m_water + c.m_hydrolox_t
    c.v_e_eff_mps = ((m_water * v_e_w + c.m_hydrolox_t * v_e_h) / denom) if denom > 0 else 0.0
    if denom > 0 and (m_dry + c.chunk_t - m_water) > 0:
        c.dv_achieved_mps = c.v_e_eff_mps * math.log(c.m_initial_t / (m_dry + c.chunk_t - m_water))
    c.feasible = (c.m_delivered_t > 0) and (c.dv_achieved_mps >= dv_required - 1.0)
    if c.feasible:
        c.pass_l0_05_strict = c.rt_yr <= L0_05_STRICT_YR
        c.pass_l0_05_waiver = c.rt_yr <= L0_05_WAIVER_YR
        c.pass_reactor_life = c.t_burn_yr <= REACTOR_LIFE_TARGET_YR
        c.pass_launchable_2x_starship = c.leo_stack_t <= 2 * STARSHIP_LEO_T
    else:
        c.fail_reason = c.fail_reason or "delivered<=0"
    return c


# --- sweep --------------------------------------------------------------------

def sweep() -> list[dict]:
    p_reactor_grid = [0.0, 10.0, 50.0]
    m_hydrolox_grid = [0.0, 50.0, 100.0, 250.0, 500.0, 1000.0, 2500.0]
    chunk_grid = [5.0, 10.0, 50.0, 100.0, 200.0]
    eta_gen_grid = [0.0, 0.30, 0.50]  # eta_gen=0 means pure chemical (no electricity)
    specific_power_grid = [2.4, 5.0]
    aero_grid = [0.0, 10.0]
    isp_grid = [ISP_PRIMARY, ISP_SENS]
    bus_grid = ["full", "demo"]

    rows: list[dict] = []
    for (p, m, ch, eg, sp, ac, isp, bus) in product(
        p_reactor_grid, m_hydrolox_grid, chunk_grid,
        eta_gen_grid, specific_power_grid, aero_grid, isp_grid, bus_grid,
    ):
        c = Cell(
            p_reactor_kwe=p, m_hydrolox_t=m, chunk_t=ch,
            eta_gen=eg, specific_power_w_per_kg=sp,
            aerocapture_credit_kms=ac, isp_s=isp, bus_class=bus,
        )
        solve_cell(c)
        rows.append(asdict(c))
    return rows


# --- hypothesis grading -------------------------------------------------------

def grade(rows):
    grades = []

    # H1: with exhaust thrust, at P=10 kWe + chunk=50 + aero=10 + full bus, some M_h closes waiver.
    h1 = [r for r in rows if r["p_reactor_kwe"] == 10 and r["chunk_t"] == 50
          and r["aerocapture_credit_kms"] == 10 and r["bus_class"] == "full"
          and r["isp_s"] == ISP_PRIMARY and r["eta_gen"] in (0.30, 0.50)]
    h1_close = [r for r in h1 if r["feasible"] and r["pass_l0_05_waiver"]
                and r["pass_reactor_life"] and r["pass_launchable_2x_starship"]]
    grades.append({"hypothesis": "H1",
                   "predicted": "P=10 kWe + chunk=50 t + aero=10 km/s + full bus closes some M_h",
                   "measured": f"{len(h1_close)} of {len(h1)} cells all-pass",
                   "verdict": "HELD" if len(h1_close) >= 1 else "FALSIFIED"})

    # H2: at v_e_h ~ 2000 m/s (eta_gen=0.5 effectively), still no closure at 200-t chunk + 10 kWe.
    h2 = [r for r in rows if r["p_reactor_kwe"] == 10 and r["chunk_t"] == 200
          and r["bus_class"] == "full" and r["isp_s"] == ISP_PRIMARY
          and r["eta_gen"] == 0.5]
    h2_strict = [r for r in h2 if r["feasible"] and r["pass_l0_05_strict"]
                 and r["pass_reactor_life"] and r["pass_launchable_2x_starship"]]
    grades.append({"hypothesis": "H2",
                   "predicted": "P=10 kWe + chunk=200 + eta=0.5: no L0-05-strict all-pass closure",
                   "measured": f"{len(h2_strict)} of {len(h2)} cells all-pass strict",
                   "verdict": "HELD" if len(h2_strict) == 0 else "FALSIFIED"})

    # H3: optimal eta_gen for delivered mass is interior (not at 0 or 1).
    # Fix (P=10 or 50, chunk=50, aero=10, full bus, isp=2000), sweep eta_gen, find argmax delivered.
    h3_results = []
    for p in [10.0, 50.0]:
        for ch in [50.0, 100.0]:
            for m in [250.0, 500.0]:
                sub = [r for r in rows if r["p_reactor_kwe"] == p and r["chunk_t"] == ch
                       and r["m_hydrolox_t"] == m and r["aerocapture_credit_kms"] == 10
                       and r["bus_class"] == "full" and r["isp_s"] == ISP_PRIMARY
                       and r["specific_power_w_per_kg"] == 5.0 and r["feasible"]]
                if sub:
                    best = max(sub, key=lambda r: r["m_delivered_t"])
                    h3_results.append({"P": p, "chunk": ch, "M_h": m,
                                       "best_eta_gen": best["eta_gen"],
                                       "best_delivered": best["m_delivered_t"]})
    interior_optima = sum(1 for r in h3_results if 0.0 < r["best_eta_gen"] < 0.5)
    grades.append({"hypothesis": "H3",
                   "predicted": "optimal eta_gen is interior (in (0, 0.5))",
                   "measured": f"{interior_optima} of {len(h3_results)} cells show interior optimum; details={json.dumps(h3_results)}",
                   "verdict": "HELD" if interior_optima >= len(h3_results) / 2 else "FALSIFIED"})

    # H4: small-chunk (5-10 t) demonstrator with hydrolox + aero closes.
    h4 = [r for r in rows if r["chunk_t"] <= 10 and r["aerocapture_credit_kms"] == 10
          and r["bus_class"] == "demo" and r["isp_s"] == ISP_PRIMARY
          and r["p_reactor_kwe"] in (0.0, 10.0)]
    h4_close = [r for r in h4 if r["feasible"] and r["pass_l0_05_waiver"]
                and r["pass_reactor_life"] and r["pass_launchable_2x_starship"]]
    grades.append({"hypothesis": "H4",
                   "predicted": "demonstrator-class (chunk<=10, demo bus, aero=10): some closure",
                   "measured": f"{len(h4_close)} of {len(h4)} cells all-pass",
                   "verdict": "HELD" if len(h4_close) >= 1 else "FALSIFIED"})

    # H5: at 200-t chunk + 10 kWe, hybrid still fails L0-05 strict even with exhaust thrust.
    h5 = [r for r in rows if r["chunk_t"] == 200 and r["p_reactor_kwe"] == 10
          and r["bus_class"] == "full" and r["isp_s"] == ISP_PRIMARY]
    h5_strict = [r for r in h5 if r["feasible"] and r["pass_l0_05_strict"]
                 and r["pass_reactor_life"] and r["pass_launchable_2x_starship"]]
    grades.append({"hypothesis": "H5",
                   "predicted": "at 200-t chunk + 10 kWe, hybrid still fails L0-05 strict",
                   "measured": f"{len(h5_strict)} of {len(h5)} cells all-pass strict",
                   "verdict": "HELD" if len(h5_strict) == 0 else "FALSIFIED"})

    # H6: prior-round verdict ("hydrolox strictly net-harmful") is FALSIFIED at correct two-stream physics.
    # At P=10 + chunk=50 + aero=10 + bus=full + isp=2000 + eta_gen=0.0 (pure chem) + sp=5: sweep M_h.
    p10_sweep = [r for r in rows if r["p_reactor_kwe"] == 10 and r["chunk_t"] == 50
                 and r["aerocapture_credit_kms"] == 10 and r["bus_class"] == "full"
                 and r["isp_s"] == ISP_PRIMARY and r["eta_gen"] == 0.0
                 and r["specific_power_w_per_kg"] == 5.0 and r["feasible"]]
    if p10_sweep:
        best_m = max(p10_sweep, key=lambda r: r["m_delivered_t"])
        prior_verdict_holds = (best_m["m_hydrolox_t"] == 0)
    else:
        prior_verdict_holds = True
    grades.append({"hypothesis": "H6",
                   "predicted": "prior-round 'M_h=0 strictly dominates' is FALSIFIED at two-stream physics",
                   "measured": f"best M_h at primary regime = {best_m['m_hydrolox_t'] if p10_sweep else 'n/a'} (delivered {best_m['m_delivered_t']:.2f} t)" if p10_sweep else "no feasible cells in this regime",
                   "verdict": "HELD" if (not prior_verdict_holds and p10_sweep) else "FALSIFIED"})

    return grades


def write_tables(rows, grades, path):
    feas = [r for r in rows if r["feasible"]]
    strict = [r for r in feas if r["pass_l0_05_strict"]]
    waiver = [r for r in feas if r["pass_l0_05_waiver"]]
    react_life = [r for r in feas if r["pass_reactor_life"]]
    launchable = [r for r in feas if r["pass_launchable_2x_starship"]]
    all_pass = [r for r in feas
                if r["pass_l0_05_waiver"] and r["pass_reactor_life"] and r["pass_launchable_2x_starship"]]
    all_pass_strict = [r for r in all_pass if r["pass_l0_05_strict"]]

    L = []
    L.append("# R-hybrid-power-generator-exhaust-revisit — headline tables\n")
    L.append("**Revisits R-hybrid-chemical-power-augmentation (commit `98a9ded`).** The prior round assumed gas-generator exhaust contributes zero thrust. This round runs the two-stream rocket equation with hydrolox-chemical thrust at the post-turbine residual specific impulse.\n")
    L.append("## Two-stream rocket equation\n")
    v_e_w_p = ISP_PRIMARY * G0
    v_e_h_p_05 = math.sqrt(2.0 * 0.5 * LHV_HYDROLOX * ETA_NOZZLE)
    v_e_h_p_00 = math.sqrt(2.0 * 1.0 * LHV_HYDROLOX * ETA_NOZZLE)
    L.append(f"At Isp 2000 s: v_e_water = {v_e_w_p:.0f} m/s. At η_gen=0.5 + η_nozzle={ETA_NOZZLE}: v_e_hydrolox = {v_e_h_p_05:.0f} m/s. At η_gen=0.0 (pure chemical): v_e_hydrolox = {v_e_h_p_00:.0f} m/s (~Isp {v_e_h_p_00/G0:.0f} s, close to actual stoichiometric H2/O2 chemical-rocket performance).\n")
    L.append(f"η_thruster revised down to **{ETA_THRUSTER}** (water-electric MET / arcjet class; prior round used 0.7 = Hall-class, optimistic for water propellant).\n")

    L.append(f"## Closure counts (total cells = {len(rows)})\n")
    L.append("| Gate | Count |")
    L.append("|---|---|")
    L.append(f"| Feasible | {len(feas)} |")
    L.append(f"| Pass L0-05 strict (≤15 yr) | {len(strict)} |")
    L.append(f"| Pass L0-05 waiver (≤25 yr) | {len(waiver)} |")
    L.append(f"| Pass reactor life (≤10 yr) | {len(react_life)} |")
    L.append(f"| Launchable (≤300 t LEO stack) | {len(launchable)} |")
    L.append(f"| **All-pass waiver** | **{len(all_pass)}** |")
    L.append(f"| **All-pass strict** | **{len(all_pass_strict)}** |")
    L.append("")

    if all_pass:
        L.append("## All-pass-waiver cells (top 30 by delivered chunk)\n")
        L.append("| P_kWe | M_h t | chunk t | η_gen | sp W/kg | aero km/s | isp s | bus | v_e_eff m/s | t_burn yr | RT yr | delivered t | LEO t |")
        L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
        for r in sorted(all_pass, key=lambda r: -r["m_delivered_t"])[:30]:
            L.append(f"| {r['p_reactor_kwe']:.0f} | {r['m_hydrolox_t']:.0f} | {r['chunk_t']:.0f} | "
                     f"{r['eta_gen']:.2f} | {r['specific_power_w_per_kg']:.1f} | "
                     f"{r['aerocapture_credit_kms']:.0f} | {r['isp_s']:.0f} | "
                     f"{r['bus_class']} | {r['v_e_eff_mps']:.0f} | "
                     f"{r['t_burn_yr']:.2f} | {r['rt_yr']:.2f} | "
                     f"{r['m_delivered_t']:.2f} | {r['leo_stack_t']:.0f} |")
        L.append("")

    # M_h sweep at P=10, chunk=50, aero=10, full bus, isp=2000, sp=5 — across eta_gen
    L.append("## Hydrolox sweep at P=10 kWe, chunk=50, aero=10 km/s, full bus, sp=5 W/kg, Isp=2000\n")
    L.append("| η_gen | M_h t | feasible | dv_ach m/s | t_burn yr | RT yr | delivered t | LEO t |")
    L.append("|---|---|---|---|---|---|---|---|")
    for eg in [0.0, 0.30, 0.50]:
        for r in [r for r in rows if r["p_reactor_kwe"] == 10 and r["chunk_t"] == 50
                  and r["aerocapture_credit_kms"] == 10 and r["bus_class"] == "full"
                  and r["isp_s"] == ISP_PRIMARY and r["specific_power_w_per_kg"] == 5.0
                  and r["eta_gen"] == eg]:
            L.append(f"| {r['eta_gen']:.2f} | {r['m_hydrolox_t']:.0f} | {r['feasible']} | "
                     f"{r['dv_achieved_mps']:.0f} | {r['t_burn_yr']:.2f} | {r['rt_yr']:.2f} | "
                     f"{r['m_delivered_t']:.2f} | {r['leo_stack_t']:.0f} |")
    L.append("")

    L.append("## Hypothesis grades\n")
    L.append("| # | predicted | measured | verdict |")
    L.append("|---|---|---|---|")
    for g in grades:
        m = g['measured']
        if len(m) > 200:
            m = m[:200] + "..."
        L.append(f"| {g['hypothesis']} | {g['predicted']} | {m} | {g['verdict']} |")
    L.append("")

    path.write_text("\n".join(L))


def main():
    here = pathlib.Path(__file__).parent
    rd = here / "results"
    rd.mkdir(exist_ok=True)

    print("Sweeping (two-stream rocket equation)...")
    rows = sweep()
    feas = sum(1 for r in rows if r["feasible"])
    all_pass = sum(1 for r in rows if r["feasible"]
                   and r["pass_l0_05_waiver"] and r["pass_reactor_life"] and r["pass_launchable_2x_starship"])
    print(f"  total = {len(rows)}, feasible = {feas}, all-pass waiver = {all_pass}")

    g = grade(rows)
    for x in g:
        print(f"  {x['hypothesis']}: {x['verdict']}")

    # slim json
    slim = {
        "summary": {
            "total": len(rows), "feasible": feas, "all_pass_waiver": all_pass,
        },
        "feasible_rows": [r for r in rows if r["feasible"]],
        "grades": g,
    }
    (rd / "results.json").write_text(json.dumps(slim, indent=2))
    write_tables(rows, g, rd / "tables.md")
    print(f"Wrote {rd / 'results.json'} and {rd / 'tables.md'}")


if __name__ == "__main__":
    main()
