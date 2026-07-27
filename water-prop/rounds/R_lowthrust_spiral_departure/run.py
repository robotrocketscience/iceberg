"""R-lowthrust-spiral-departure — is R179's departure reactor floor built on an
impulsive Δv fed through a low-thrust powerplant?

Reproduces R179's impulsive single-burn Δv, computes the honest low-thrust
spiral departure Δv (analytic v_circ + a direct numerical tangential-spiral
integration at the real mission thrust-to-weight), and propagates through
R179's own rocket-equation reactor-power formula.

Pre-registered H-C1..H-C4. See SCOPE.md. Deterministic.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent

G0 = 9.80665
MU_S = 3.793e16
R_RING = 1.07e8
VINF = 6210.0
VE_MET = 800.0 * G0
ETA = 0.6
YEAR = 3.156e7
M_F = 100_000.0
BURN_YEARS = 2.0


def vis(r, a):
    return math.sqrt(MU_S * (2.0 / r - 1.0 / a))


def hyp_v(r, vinf):
    return math.sqrt(vinf ** 2 + 2.0 * MU_S / r)


def reactor_kwe(dv, m_f=M_F, ve=VE_MET, burn_years=BURN_YEARS):
    prop = m_f * (math.exp(dv / ve) - 1.0)
    return 0.5 * ve ** 2 * prop / ETA / (burn_years * YEAR) / 1e3


V_CIRC = vis(R_RING, R_RING)
V_ESC = math.sqrt(2 * MU_S / R_RING)
DV_IMPULSIVE = hyp_v(R_RING, VINF) - V_CIRC


def spiral_integrate(a_thrust, e_target, max_orbits=6000, steps_per_orbit=120):
    """Planar 2-body + constant tangential (prograde) low thrust from the
    circular B-ring. Integrate until specific energy reaches e_target; return
    Δv = ∫|a| dt = a_thrust * t and the number of revolutions. RK4."""
    T_orb = 2 * math.pi * math.sqrt(R_RING ** 3 / MU_S)
    dt = T_orb / steps_per_orbit
    # state [x, y, vx, vy]
    s = [R_RING, 0.0, 0.0, V_CIRC]

    def deriv(st):
        x, y, vx, vy = st
        r = math.hypot(x, y)
        v = math.hypot(vx, vy)
        ax = -MU_S * x / r ** 3
        ay = -MU_S * y / r ** 3
        if v > 0:
            ax += a_thrust * vx / v
            ay += a_thrust * vy / v
        return [vx, vy, ax, ay]

    t = 0.0
    n_steps = int(max_orbits * steps_per_orbit)
    for _ in range(n_steps):
        k1 = deriv(s)
        k2 = deriv([s[i] + 0.5 * dt * k1[i] for i in range(4)])
        k3 = deriv([s[i] + 0.5 * dt * k2[i] for i in range(4)])
        k4 = deriv([s[i] + dt * k3[i] for i in range(4)])
        s = [s[i] + dt / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(4)]
        t += dt
        r = math.hypot(s[0], s[1])
        v = math.hypot(s[2], s[3])
        e = 0.5 * v ** 2 - MU_S / r
        if e >= e_target:
            break
    revs = t / T_orb
    return {"dv": a_thrust * t, "revs": revs, "reached": e >= e_target, "t_s": t}


def main():
    out = {"anchors": {"v_circ": V_CIRC, "v_esc": V_ESC, "vinf": VINF,
                       "impulsive_single_burn_dv": DV_IMPULSIVE,
                       "ve_met": VE_MET, "burn_years": BURN_YEARS}}

    # H-C1: R179's 9.0 is the impulsive value
    out["HC1"] = {"impulsive_dv": DV_IMPULSIVE, "r179_hardcoded": 9000.0,
                  "frac_diff": abs(9000.0 - DV_IMPULSIVE) / DV_IMPULSIVE}

    # H-C2: honest low-thrust spiral Δv (analytic + numerical at mission a)
    # mission thrust-to-weight: thrust = 2*P*eta/v_e at 175 kWe, m=100 t
    a_mission = 2.0 * 175_000.0 * ETA / VE_MET / M_F
    e_para = 0.0
    e_hyp = 0.5 * VINF ** 2
    numer = {}
    for a in (a_mission, 1e-3, 3e-3):
        r_para = spiral_integrate(a, e_para)
        r_hyp = spiral_integrate(a, e_hyp)
        numer[f"a_{a:.2e}"] = {"a_thrust": a,
                               "dv_to_parabolic": r_para["dv"], "revs_para": r_para["revs"],
                               "dv_to_vinf": r_hyp["dv"], "revs_hyp": r_hyp["revs"],
                               "reached_hyp": r_hyp["reached"]}
    dv_spiral_num = numer[f"a_{a_mission:.2e}"]["dv_to_vinf"]
    out["HC2"] = {"analytic_escape_v_circ": V_CIRC,
                  "analytic_total_range": [V_CIRC, V_CIRC + VINF],
                  "a_mission_m_s2": a_mission,
                  "numerical_spiral_dv_to_vinf": dv_spiral_num,
                  "numerical_by_thrust": numer,
                  "ratio_to_r179_9km": dv_spiral_num / 9000.0}

    # H-C3: reactor floor at honest spiral Δv (R179's own formula, Isp 800, 2 yr)
    floors = {}
    for tag, dv in (("impulsive_8.5", DV_IMPULSIVE), ("r179_9.0", 9000.0),
                    ("spiral_numerical", dv_spiral_num),
                    ("spiral_v_circ", V_CIRC), ("spiral_v_circ_plus_vinf", V_CIRC + VINF)):
        floors[tag] = round(reactor_kwe(dv), 0)
    out["HC3"] = {"reactor_kwe_by_dv": floors,
                  "floor_at_spiral_numerical": floors["spiral_numerical"],
                  "ratio_to_r179_175": floors["spiral_numerical"] / 175.0}

    # Alternative: fixed 175 kWe, burn time absorbs Δv
    def burn_years_at_power(dv, kwe=175.0):
        prop = M_F * (math.exp(dv / VE_MET) - 1.0)
        # invert reactor_kwe: kwe = 0.5 ve^2 prop / eta / (t*1) /1e3 -> t
        t_s = 0.5 * VE_MET ** 2 * prop / ETA / (kwe * 1e3)
        return t_s / YEAR
    out["burn_time_alt"] = {"spiral_numerical_burn_yr_at_175kwe":
                            round(burn_years_at_power(dv_spiral_num), 1),
                            "v_circ_burn_yr_at_175kwe": round(burn_years_at_power(V_CIRC), 1)}

    # H-C4: Isp sensitivity
    isp_sweep = {}
    for isp in (800.0, 2000.0, 3000.0):
        ve = isp * G0
        base = reactor_kwe(9000.0, ve=ve)
        spir = reactor_kwe(dv_spiral_num, ve=ve)
        isp_sweep[f"isp_{isp:.0f}"] = {"kwe_9km": round(base), "kwe_spiral": round(spir),
                                       "ratio": round(spir / base, 2)}
    out["HC4"] = {"isp_sweep": isp_sweep,
                  "min_ratio_over_isp": min(v["ratio"] for v in isp_sweep.values())}

    # chemical-kick escape: staged chemical mass for the impulsive 8.5 at Isp 350
    ve_chem = 350.0 * G0
    mr_chem = math.exp(DV_IMPULSIVE / ve_chem)
    out["chemical_kick"] = {"mass_ratio_isp350": round(mr_chem, 2),
                            "prop_t_for_100t_payload": round(M_F * (mr_chem - 1) / 1000, 1),
                            "note": "high-thrust chemical departure recovers the Oberth 8.5 km/s "
                                    "but adds a stage of this propellant mass"}

    # verdicts
    hc1 = out["HC1"]["frac_diff"] < 0.30
    hc2 = dv_spiral_num >= 15000.0
    hc3 = floors["spiral_numerical"] >= 300.0
    hc4 = out["HC4"]["min_ratio_over_isp"] >= 1.3
    out["verdicts"] = {"H-C1": hc1, "H-C2": hc2, "H-C3": hc3, "H-C4": hc4,
                       "held": sum([hc1, hc2, hc3, hc4]), "of": 4}
    return out


if __name__ == "__main__":
    r = main()
    (HERE / "results").mkdir(exist_ok=True)
    json.dump(r, open(HERE / "results" / "spiral_departure.json", "w"), indent=2)
    v = r["verdicts"]
    print(f"H-C1  impulsive single-burn {r['HC1']['impulsive_dv']:.0f} m/s vs R179 9000 "
          f"({100*r['HC1']['frac_diff']:.0f}% diff) -> {v['H-C1']}")
    print(f"H-C2  mission a={r['HC2']['a_mission_m_s2']:.2e} m/s^2; numerical spiral Δv to v_inf "
          f"= {r['HC2']['numerical_spiral_dv_to_vinf']:.0f} m/s "
          f"({r['HC2']['ratio_to_r179_9km']:.2f}x R179 9.0; analytic v_circ {V_CIRC:.0f}) -> {v['H-C2']}")
    print(f"      revs to v_inf at mission a: "
          f"{r['HC2']['numerical_by_thrust'][f'a_{r['HC2']['a_mission_m_s2']:.2e}']['revs_hyp']:.0f}")
    print(f"H-C3  reactor floor at spiral Δv = {r['HC3']['floor_at_spiral_numerical']:.0f} kWe "
          f"({r['HC3']['ratio_to_r179_175']:.2f}x R179's 175) -> {v['H-C3']}")
    print(f"      (or hold 175 kWe -> {r['burn_time_alt']['spiral_numerical_burn_yr_at_175kwe']} yr burn)")
    print(f"H-C4  Isp sweep ratios (spiral/9km): "
          f"{ {k: vv['ratio'] for k, vv in r['HC4']['isp_sweep'].items()} }; "
          f"min {r['HC4']['min_ratio_over_isp']} -> {v['H-C4']}")
    print(f"      chemical-kick escape: {r['chemical_kick']['prop_t_for_100t_payload']} t chem prop "
          f"(Isp 350) for the Oberth 8.5 km/s")
    print(f"\nHELD {v['held']}/{v['of']}")
