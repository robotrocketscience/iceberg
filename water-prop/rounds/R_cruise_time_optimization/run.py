"""R-cruise-time-optimization — sweep transfer-orbit aphelion to find the
cruise time that minimizes round-trip time for Variant C at 500 kilowatt-electric.

Tests whether Hohmann (which minimizes delta-velocity) is also approximately
optimal for round-trip TIME under the integrated-burn constraint, or whether a
faster-than-Hohmann transfer wins overall by trading cruise time for burn time.

See STUDY.md for the pre-registered hypothesis block.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from waterprop.constants import A_EARTH, A_SATURN, G0, GM_SUN

YEAR_S = 365.25 * 86400.0
DAY_S = 86400.0

ETA_THR_ELECTRIC = 0.65
SATURN_OPS_YR = 1.0
ROUND_TRIP_CEILING_YR = 15.0
ROUND_TRIP_SOFT_MARGIN_YR = 1.0
ROUND_TRIP_DOUBLE_SOFT_MARGIN_YR = 2.0

# Heliocentric reference speeds (vis-viva for circular Earth and Saturn orbits)
V_EARTH_ORBIT_KM_S = math.sqrt(GM_SUN / A_EARTH)
V_SATURN_ORBIT_KM_S = math.sqrt(GM_SUN / A_SATURN)

# Round D / Round E inputs
ISP_ELECTRIC_S = 2000.0
ISP_HYDROLOX_S = 450.0
CHUNK_BASELINE_T = 200.0
M_OUTBOUND_KICK_DRY_T = 10.0

# Variant C non-cruise-time-dependent inbound segments (Round D)
DV_SATURN_SPIRAL_HE_KM_S = 6.159  # segment 1 at high-elliptical 1Mkm departure
LGA_CREDIT_KM_S = 2.0  # applied to Earth-side helio segment

# MARVL-anchored mass model (rhea baseline)
MARVL_MODEL = {
    "m_fixed_t": 5.0,
    "alpha_reactor_W_per_kg": 33.0,
    "alpha_PC_W_per_kg": 50.0,
    "alpha_radiator_kW_th_per_kg": 0.047,
    "eta_conv": 0.30,
    "f_tank": 0.05,
}


def hohmann_baseline() -> dict:
    """Return Hohmann transfer parameters for sanity-check (magnitudes)."""
    a_h_km = (A_EARTH + A_SATURN) / 2.0
    v_peri = math.sqrt(GM_SUN * (2.0 / A_EARTH - 1.0 / a_h_km))
    v_apo = math.sqrt(GM_SUN * (2.0 / A_SATURN - 1.0 / a_h_km))
    cruise_yr = math.pi * math.sqrt(a_h_km ** 3 / GM_SUN) / YEAR_S
    return {
        "a_km": a_h_km,
        "r_apo_km": A_SATURN,
        "v_perihelion_km_s": v_peri,
        "v_at_r_Saturn_km_s": v_apo,
        "dv_departure_km_s": abs(v_peri - V_EARTH_ORBIT_KM_S),
        "dv_arrival_km_s": abs(v_apo - V_SATURN_ORBIT_KM_S),
        "dv_total_helio_km_s": abs(v_peri - V_EARTH_ORBIT_KM_S) + abs(v_apo - V_SATURN_ORBIT_KM_S),
        "cruise_yr": cruise_yr,
    }


def time_to_r_on_ellipse(a_km: float, r_apo_km: float, r_target_km: float) -> float:
    """Time from perihelion to r_target on an ellipse with semi-major a, aphelion r_apo.

    Uses Kepler's equation. Eccentric anomaly E from cos E = (1 - r/a) / e.
    True anomaly is positive on the outbound leg (from perihelion toward aphelion).
    Time = (E - e sin E) / n where n = sqrt(mu/a^3).
    """
    e = 1.0 - (a_km - r_apo_km) / a_km - 1.0  # = r_apo/a - 1
    e = (r_apo_km - a_km) / a_km
    if e < 0 or e >= 1:
        raise ValueError(f"invalid eccentricity {e} for a={a_km}, r_apo={r_apo_km}")
    if r_target_km > r_apo_km:
        return math.inf  # cannot reach target
    if r_target_km < a_km * (1 - e):
        return 0.0  # below perihelion shouldn't happen
    cos_E = (1.0 - r_target_km / a_km) / e
    cos_E = max(-1.0, min(1.0, cos_E))
    E = math.acos(cos_E)  # in [0, pi]; outbound from perihelion
    n = math.sqrt(GM_SUN / a_km ** 3)
    t_s = (E - e * math.sin(E)) / n
    return t_s


def transfer_at_r_apo(r_apo_km: float) -> dict:
    """Compute transfer parameters for Type-I half-orbit transfer with chosen aphelion."""
    if r_apo_km < A_SATURN:
        return {"feasible": False, "reason": f"r_apo {r_apo_km/1.5e8:.2f} AU below Saturn"}
    a_km = (A_EARTH + r_apo_km) / 2.0
    e = (r_apo_km - a_km) / a_km  # eccentricity = (r_apo - a) / a
    # Speeds via vis-viva
    v_peri = math.sqrt(GM_SUN * (2.0 / A_EARTH - 1.0 / a_km))
    v_total_at_r_Saturn = math.sqrt(GM_SUN * (2.0 / A_SATURN - 1.0 / a_km))
    cruise_s = time_to_r_on_ellipse(a_km, r_apo_km, A_SATURN)
    cruise_yr = cruise_s / YEAR_S

    # Departure dV: at perihelion ship velocity is purely tangential (= v_peri).
    # Earth's velocity is tangential at v_Earth_orbit. So dV magnitude = |v_peri - v_Earth_orbit|.
    dv_dep_mag = abs(v_peri - V_EARTH_ORBIT_KM_S)

    # Arrival dV: at r_Saturn the ship has both tangential and radial velocity components.
    # Angular momentum conserved: h = v_peri × r_perihelion (since v at perihelion is tangential)
    # v_theta at r = h / r
    # v_radial = sqrt(v_total^2 - v_theta^2)
    # Saturn's velocity is purely tangential at v_Saturn_orbit.
    # dV vector = (v_theta - v_Saturn_orbit) tangential + v_radial radial.
    # |dV| = sqrt((v_theta - v_Saturn_orbit)^2 + v_radial^2)
    h_km2_per_s = v_peri * A_EARTH
    v_theta_at_r_Saturn = h_km2_per_s / A_SATURN
    v_radial_at_r_Saturn_sq = v_total_at_r_Saturn ** 2 - v_theta_at_r_Saturn ** 2
    v_radial_at_r_Saturn = math.sqrt(max(0.0, v_radial_at_r_Saturn_sq))
    dv_arr_mag = math.sqrt(
        (v_theta_at_r_Saturn - V_SATURN_ORBIT_KM_S) ** 2 + v_radial_at_r_Saturn ** 2
    )

    return {
        "feasible": True,
        "r_apo_km": r_apo_km,
        "r_apo_AU": r_apo_km / 1.4959787e8,
        "a_km": a_km,
        "eccentricity": e,
        "v_perihelion_km_s": v_peri,
        "v_total_at_r_Saturn_km_s": v_total_at_r_Saturn,
        "v_theta_at_r_Saturn_km_s": v_theta_at_r_Saturn,
        "v_radial_at_r_Saturn_km_s": v_radial_at_r_Saturn,
        "dv_departure_helio_km_s": dv_dep_mag,
        "dv_arrival_helio_km_s": dv_arr_mag,
        "dv_total_helio_km_s": dv_dep_mag + dv_arr_mag,
        "cruise_yr": cruise_yr,
    }


def variant_C_closure_at_cruise(transfer: dict, reactor_kwe: float, isp_electric_s: float) -> dict:
    """Variant C closure with non-Hohmann cruise transfer.

    Outbound: chemical kick at the heliocentric departure delta-velocity (impulsive,
              chemical propellant from Earth — not chunk-derived).
    Cruise outbound: ballistic, time = transfer["cruise_yr"].
    Saturn ops: 1 yr.
    Inbound: electric continuous-thrust at Saturn-spiral + heliocentric (mirrored
             dv_arrival from outbound, since inbound is symmetric) + LGA credit.
             Earth aerocapture replaces LEO spiral.
    """
    if not transfer.get("feasible"):
        return {"feasible": False, "reason": transfer.get("reason", "?")}

    cruise_yr = transfer["cruise_yr"]
    dv_helio_dep = transfer["dv_departure_helio_km_s"]  # outbound chemical kick
    dv_helio_arr = transfer["dv_arrival_helio_km_s"]    # outbound arrival = inbound departure (mirror)

    # Tug dry mass (MARVL-anchored)
    eta = MARVL_MODEL["eta_conv"]
    p_th_waste_kw = reactor_kwe * (1.0 - eta) / eta
    m_reactor = reactor_kwe / MARVL_MODEL["alpha_reactor_W_per_kg"]
    m_pc = reactor_kwe / MARVL_MODEL["alpha_PC_W_per_kg"]
    m_rad = p_th_waste_kw / MARVL_MODEL["alpha_radiator_kW_th_per_kg"] / 1000.0
    m_tug_dry_t = MARVL_MODEL["m_fixed_t"] + m_reactor + m_pc + m_rad

    # Inbound electric DV: Saturn spiral (segment 1) + helio retrograde (matched to faster cruise)
    # + LGA. No LEO spiral (aerocapture).
    # For symmetric inbound: helio retrograde dV = dv_arrival (mirror).
    # Actually, symmetric inbound from Saturn at heliocentric dV ~ same as outbound arrival.
    # Helio departure at Saturn (inbound side) = dv_arrival (from outbound = arrival heliocentric)
    # Helio arrival at Earth (inbound side) = dv_departure (from outbound = departure heliocentric)
    # These mirror cleanly because the transfer ellipse is symmetric.
    dv_inbound_electric_km_s = (
        DV_SATURN_SPIRAL_HE_KM_S + dv_helio_arr + dv_helio_dep - LGA_CREDIT_KM_S
    )

    # Iterate on tug-mass for inbound tank fraction
    m_tug_t = m_tug_dry_t
    for _ in range(20):
        v_e_elec = isp_electric_s * G0
        m_initial_inbound_t = m_tug_t + CHUNK_BASELINE_T
        mr_inbound = math.exp(dv_inbound_electric_km_s * 1000.0 / v_e_elec)
        m_prop_inbound_t = m_initial_inbound_t * (1.0 - 1.0 / mr_inbound)
        if m_prop_inbound_t > CHUNK_BASELINE_T:
            return {
                "feasible": False,
                "reason": f"electric inbound {dv_inbound_electric_km_s:.2f} km/s requires {m_prop_inbound_t:.1f} t > chunk {CHUNK_BASELINE_T} t",
                "cruise_yr": cruise_yr,
                "dv_inbound_electric_km_s": dv_inbound_electric_km_s,
                "round_trip_yr": math.inf,
                "delivered_t": -math.inf,
            }
        new_tug = (
            MARVL_MODEL["m_fixed_t"] + m_reactor + m_pc + m_rad + m_prop_inbound_t * MARVL_MODEL["f_tank"]
        )
        if abs(new_tug - m_tug_t) < 1e-4:
            m_tug_t = new_tug
            break
        m_tug_t = new_tug

    delivered_t = CHUNK_BASELINE_T - m_prop_inbound_t

    # Inbound burn time
    P_elec_w = reactor_kwe * 1000.0
    thrust_inbound_N = 2.0 * ETA_THR_ELECTRIC * P_elec_w / v_e_elec
    t_inbound_burn_s = m_prop_inbound_t * 1000.0 * v_e_elec / thrust_inbound_N
    t_inbound_burn_yr = t_inbound_burn_s / YEAR_S

    # Outbound chemical kick (at the heliocentric departure dV)
    v_e_chem = ISP_HYDROLOX_S * G0
    mr_chem = math.exp(dv_helio_dep * 1000.0 / v_e_chem)
    m_at_start_kick_t = (m_tug_t + M_OUTBOUND_KICK_DRY_T) * mr_chem
    m_outbound_kick_prop_t = m_at_start_kick_t - (m_tug_t + M_OUTBOUND_KICK_DRY_T)
    m_LEO_mission1_t = m_at_start_kick_t  # all kick prop launched from Earth

    round_trip_yr = cruise_yr + SATURN_OPS_YR + t_inbound_burn_yr + cruise_yr  # symmetric in/out

    closes_strict = (round_trip_yr <= ROUND_TRIP_CEILING_YR) and (delivered_t > 0)
    closes_soft1 = (round_trip_yr <= ROUND_TRIP_CEILING_YR + ROUND_TRIP_SOFT_MARGIN_YR
                    and delivered_t > 0)
    closes_soft2 = (round_trip_yr <= ROUND_TRIP_CEILING_YR + ROUND_TRIP_DOUBLE_SOFT_MARGIN_YR
                    and delivered_t > 0)

    return {
        "feasible": True,
        "reactor_kwe": reactor_kwe,
        "cruise_yr": cruise_yr,
        "r_apo_AU": transfer["r_apo_AU"],
        "dv_helio_departure_km_s": dv_helio_dep,
        "dv_helio_arrival_km_s": dv_helio_arr,
        "dv_helio_total_km_s": dv_helio_dep + dv_helio_arr,
        "dv_inbound_electric_km_s": dv_inbound_electric_km_s,
        "m_tug_t": m_tug_t,
        "m_outbound_kick_prop_t": m_outbound_kick_prop_t,
        "m_LEO_mission1_t": m_LEO_mission1_t,
        "m_prop_inbound_t": m_prop_inbound_t,
        "delivered_t": delivered_t,
        "delivered_fraction": delivered_t / CHUNK_BASELINE_T,
        "thrust_inbound_N": thrust_inbound_N,
        "mass_ratio_inbound": mr_inbound,
        "t_inbound_burn_yr": t_inbound_burn_yr,
        "round_trip_yr": round_trip_yr,
        "closes_strict_15yr": closes_strict,
        "closes_soft_16yr": closes_soft1,
        "closes_double_soft_17yr": closes_soft2,
    }


def main() -> dict:
    AU = 1.4959787e8  # km
    # Sweep r_apo from r_Saturn (Hohmann) up through 30 AU
    r_apo_grid = [A_SATURN] + [
        r_au * AU for r_au in [10.5, 11.0, 12.0, 14.0, 17.0, 20.0, 25.0, 30.0, 40.0, 60.0]
    ]
    transfers = [transfer_at_r_apo(r) for r in r_apo_grid]
    closures_500 = [variant_C_closure_at_cruise(t, 500.0, ISP_ELECTRIC_S) for t in transfers]
    closures_1000 = [variant_C_closure_at_cruise(t, 1000.0, ISP_ELECTRIC_S) for t in transfers]

    # Hypothesis grading.
    # H-cto-a: at cruise ~4 yr, helio sum dv. Find closest grid point.
    target_cruise_yr = 4.0
    best_idx = min(
        (i for i, c in enumerate(closures_500) if c.get("feasible")),
        key=lambda i: abs(closures_500[i]["cruise_yr"] - target_cruise_yr),
    )
    helio_at_4yr = closures_500[best_idx]["dv_helio_total_km_s"]
    cruise_at_4yr = closures_500[best_idx]["cruise_yr"]

    # H-cto-b: round-trip at 4-yr cruise, Variant C 500 kWe
    rt_at_4yr = closures_500[best_idx]["round_trip_yr"] if closures_500[best_idx].get("feasible") else math.inf
    delivered_at_4yr = closures_500[best_idx]["delivered_t"] if closures_500[best_idx].get("feasible") else -math.inf

    # H-cto-c: optimal cruise time minimizing round-trip
    feasible_500 = [c for c in closures_500 if c.get("feasible")]
    if feasible_500:
        opt_500 = min(feasible_500, key=lambda c: c["round_trip_yr"])
        opt_cruise_yr = opt_500["cruise_yr"]
        opt_round_trip = opt_500["round_trip_yr"]
    else:
        opt_500 = None
        opt_cruise_yr = math.inf
        opt_round_trip = math.inf

    # H-cto-d: round-trip improvement at optimum vs Hohmann
    hohmann_closure = closures_500[0]  # first entry is Hohmann (r_apo = A_SATURN)
    hohmann_rt = hohmann_closure["round_trip_yr"] if hohmann_closure.get("feasible") else math.inf
    rt_improvement = hohmann_rt - opt_round_trip

    # H-cto-e: chemical-kick prop requirement at 4-yr cruise
    kick_prop_at_4yr = closures_500[best_idx].get("m_outbound_kick_prop_t", math.inf)

    h_cto_a = {
        "predicted_range_km_s": [24.0, 32.0],
        "point_km_s": 28.0,
        "actual_helio_total_km_s_at_4yr_cruise": helio_at_4yr,
        "actual_cruise_yr": cruise_at_4yr,
        "held": 24.0 <= helio_at_4yr <= 32.0,
    }
    h_cto_b = {
        "predicted_range_yr": [15.0, 18.0],
        "point_yr": 16.5,
        "actual_round_trip_yr": rt_at_4yr,
        "actual_delivered_t": delivered_at_4yr,
        "held": 15.0 <= rt_at_4yr <= 18.0 if math.isfinite(rt_at_4yr) else False,
    }
    h_cto_c = {
        "predicted_range_yr": [5.5, 6.5],
        "point_yr": 6.0,
        "actual_optimal_cruise_yr": opt_cruise_yr,
        "held": 5.5 <= opt_cruise_yr <= 6.5,
    }
    h_cto_d = {
        "predicted_range_yr": [0.0, 0.7],
        "point_yr": 0.3,
        "actual_round_trip_improvement_yr": rt_improvement,
        "hohmann_rt": hohmann_rt,
        "optimal_rt": opt_round_trip,
        "held": 0.0 <= rt_improvement <= 0.7,
    }
    h_cto_e = {
        "predicted_range_t": [200.0, math.inf],
        "point_t": 280.0,
        "actual_kick_prop_t_at_4yr": kick_prop_at_4yr,
        "held": kick_prop_at_4yr > 200.0 if math.isfinite(kick_prop_at_4yr) else False,
    }

    results = {
        "config": {
            "isp_electric_s": ISP_ELECTRIC_S,
            "isp_hydrolox_s": ISP_HYDROLOX_S,
            "chunk_t": CHUNK_BASELINE_T,
            "v_earth_orbit_km_s": V_EARTH_ORBIT_KM_S,
            "v_saturn_orbit_km_s": V_SATURN_ORBIT_KM_S,
            "dv_saturn_spiral_he_km_s": DV_SATURN_SPIRAL_HE_KM_S,
            "lga_credit_km_s": LGA_CREDIT_KM_S,
            "ceiling_yr": ROUND_TRIP_CEILING_YR,
        },
        "hohmann_baseline": hohmann_baseline(),
        "transfers": transfers,
        "closures_500kwe": closures_500,
        "closures_1000kwe": closures_1000,
        "hypothesis_grading": {
            "H-cto-a_helio_dv_at_4yr_cruise": h_cto_a,
            "H-cto-b_round_trip_at_4yr_cruise": h_cto_b,
            "H-cto-c_optimal_cruise_yr": h_cto_c,
            "H-cto-d_round_trip_improvement": h_cto_d,
            "H-cto-e_kick_prop_at_4yr": h_cto_e,
        },
    }
    out_dir = Path(__file__).parent / "results"
    out_dir.mkdir(exist_ok=True)
    (out_dir / "R_cruise_time_optimization.json").write_text(
        json.dumps(results, indent=2, default=str)
    )

    # Tables
    lines = []
    lines.append("### Cruise-time sweep at Variant C (500 kilowatt-electric, MARVL-anchored mass, chunk 200 t, specific impulse 2000 s)\n")
    lines.append("Hohmann is r_apo = r_Saturn (10.07 AU). Faster cruise corresponds to larger r_apo (higher-energy transfer ellipse).\n")
    lines.append("| r_apo (AU) | Cruise (yr) | Helio dep DV (km/s) | Helio arr DV (km/s) | Inbound electric DV (km/s) | Inbound prop (t) | Delivered (t) | t_inbound (yr) | Round-trip (yr) | Closes ±2 yr (17)? | LEO mission-1 (t) |")
    lines.append("|---:|---:|---:|---:|---:|---:|---:|---:|---:|:--:|---:|")
    for c in closures_500:
        if not c.get("feasible"):
            r_au = c.get('r_apo_AU')
            r_au_str = f"{r_au:.2f}" if isinstance(r_au, (int, float)) else "?"
            lines.append(f"| {r_au_str} | INFEASIBLE: {c.get('reason', '?')} |")
            continue
        flag = "**yes**" if c["closes_double_soft_17yr"] else "no"
        lines.append(
            f"| {c['r_apo_AU']:.2f} | {c['cruise_yr']:.2f} | "
            f"{c['dv_helio_departure_km_s']:.2f} | {c['dv_helio_arrival_km_s']:.2f} | "
            f"{c['dv_inbound_electric_km_s']:.2f} | {c['m_prop_inbound_t']:.1f} | "
            f"{c['delivered_t']:.1f} | {c['t_inbound_burn_yr']:.2f} | "
            f"{c['round_trip_yr']:.2f} | {flag} | {c['m_LEO_mission1_t']:.0f} |"
        )
    lines.append("")

    lines.append("### Same sweep at 1000 kilowatt-electric\n")
    lines.append("| r_apo (AU) | Cruise (yr) | Inbound electric DV (km/s) | Delivered (t) | t_inbound (yr) | Round-trip (yr) | Closes ±2 yr? | LEO mission-1 (t) |")
    lines.append("|---:|---:|---:|---:|---:|---:|:--:|---:|")
    for c in closures_1000:
        if not c.get("feasible"):
            r_au = c.get('r_apo_AU')
            r_au_str = f"{r_au:.2f}" if isinstance(r_au, (int, float)) else "?"
            lines.append(f"| {r_au_str} | INFEASIBLE: {c.get('reason', '?')} |")
            continue
        flag = "**yes**" if c["closes_double_soft_17yr"] else "no"
        lines.append(
            f"| {c['r_apo_AU']:.2f} | {c['cruise_yr']:.2f} | "
            f"{c['dv_inbound_electric_km_s']:.2f} | {c['delivered_t']:.1f} | "
            f"{c['t_inbound_burn_yr']:.2f} | {c['round_trip_yr']:.2f} | {flag} | "
            f"{c['m_LEO_mission1_t']:.0f} |"
        )
    lines.append("")

    lines.append("### Hypothesis grading\n")
    lines.append("| Sub-claim | Predicted | Measured | Held? |")
    lines.append("|---|---|---|---|")
    h = results["hypothesis_grading"]
    a = h["H-cto-a_helio_dv_at_4yr_cruise"]
    lines.append(f"| H-cto-a — heliocentric DV at 4-yr cruise | 24-32 km/s (point 28) | "
                 f"{a['actual_helio_total_km_s_at_4yr_cruise']:.2f} km/s "
                 f"(actual cruise {a['actual_cruise_yr']:.2f} yr) | "
                 f"{'yes' if a['held'] else '**no**'} |")
    b = h["H-cto-b_round_trip_at_4yr_cruise"]
    lines.append(f"| H-cto-b — round-trip at ~4-yr cruise | 15-18 yr (point 16.5) | "
                 f"{b['actual_round_trip_yr']:.2f} yr | {'yes' if b['held'] else '**no**'} |")
    c = h["H-cto-c_optimal_cruise_yr"]
    lines.append(f"| H-cto-c — optimal cruise time | 5.5-6.5 yr (point 6.0) | "
                 f"{c['actual_optimal_cruise_yr']:.2f} yr | {'yes' if c['held'] else '**no**'} |")
    d = h["H-cto-d_round_trip_improvement"]
    lines.append(f"| H-cto-d — round-trip improvement vs Hohmann | 0.0-0.7 yr (point 0.3) | "
                 f"{d['actual_round_trip_improvement_yr']:.2f} yr "
                 f"(Hohmann {d['hohmann_rt']:.2f}, optimal {d['optimal_rt']:.2f}) | "
                 f"{'yes' if d['held'] else '**no**'} |")
    e = h["H-cto-e_kick_prop_at_4yr"]
    lines.append(f"| H-cto-e — chemical-kick prop at 4-yr cruise | > 200 t (point 280) | "
                 f"{e['actual_kick_prop_t_at_4yr']:.1f} t | {'yes' if e['held'] else '**no**'} |")

    (out_dir / "tables.md").write_text("\n".join(lines))
    return results


if __name__ == "__main__":
    out = main()
    print("R-cruise-time-optimization complete.\n")
    print("Hohmann baseline:")
    h = out["hohmann_baseline"]
    print(f"  cruise {h['cruise_yr']:.2f} yr, helio dep {h['dv_departure_km_s']:.2f}, "
          f"helio arr {h['dv_arrival_km_s']:.2f}, helio total {h['dv_total_helio_km_s']:.2f} km/s")
    print()
    print("500 kWe Variant C closure across cruise-time sweep:")
    print(f"  {'r_apo (AU)':>10} {'cruise yr':>10} {'helio_tot':>10} {'inb DV':>8} {'inb prop':>9} {'deliv':>7} {'RT_yr':>7} {'soft17':>7} {'LEO_m1':>8}")
    for c in out["closures_500kwe"]:
        if not c.get("feasible"):
            print(f"  {c.get('r_apo_AU', 0):>10.2f} INFEASIBLE: {c.get('reason', '?')}")
            continue
        print(f"  {c['r_apo_AU']:>10.2f} {c['cruise_yr']:>10.2f} "
              f"{c['dv_helio_total_km_s']:>10.2f} {c['dv_inbound_electric_km_s']:>8.2f} "
              f"{c['m_prop_inbound_t']:>9.1f} {c['delivered_t']:>7.1f} "
              f"{c['round_trip_yr']:>7.2f} "
              f"{'yes' if c['closes_double_soft_17yr'] else 'no':>7} "
              f"{c['m_LEO_mission1_t']:>8.0f}")
    print()
    print("Hypothesis grading:")
    for k, v in out["hypothesis_grading"].items():
        print(f"  {k}: {'HELD' if v['held'] else 'FALSIFIED'}")
