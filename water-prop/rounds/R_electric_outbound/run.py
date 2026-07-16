"""R-electric-outbound — at what reactor era does all-electric end-to-end close inside L0-05's 15-year ceiling?

For each (reactor power, dry-mass model, electric specific impulse), compute:
  - outbound delta-velocity (Edelbaum spiral from low Earth orbit to Earth-escape, plus heliocentric leg to Hohmann perihelion)
  - outbound propellant and burn time at constant thrust
  - cruise time (Hohmann transfer to Saturn)
  - Saturn-side operations (fixed 1 year)
  - inbound burn time at chunk-fed delta-velocity 6.42 km/s
  - cruise back (Hohmann)
  - round-trip total

Headline question: which reactor classes deliver all-electric end-to-end inside the 15-year L0-05 ceiling?
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from waterprop.constants import (
    G0,
    GM_SUN,
    GM_EARTH,
    AU,
    R_EARTH,
    A_EARTH,
    A_SATURN,
)

YEAR_S = 365.25 * 86400.0

# Mission constants (shared with prior rounds for cross-comparison).
DV_INBOUND_KM_S = 6.42        # post-lunar-gravity-assist residual, chunk-fed (R8 / R10)
SATURN_OPS_YR = 1.0           # capture + bag deployment + harvest + departure
LEO_ALT_KM = 400.0            # standard low Earth orbit altitude assumption
ETA_THR = 0.65                # RF ion thruster efficiency at 2000 s (held for cross-cell comparison)
ROUND_TRIP_CEILING_YR = 15.0  # L0-05

# Chemical-kick reference (for the 6.9× re-derivation check)
ISP_KICK_S = 450.0
DV_KICK_KM_S = 7.3
KICK_DRY_TO_WET = 0.10
DV_CAP_ELEC_KM_S = 2.0
ISP_ELEC_CAP_S = 2000.0

CHUNK_T_BASELINE = 200.0
CHUNK_SENSITIVITY_T = [100.0, 200.0, 500.0]
REACTOR_POWERS_KWE = [10.0, 40.0, 100.0, 200.0, 500.0, 1000.0]
ISP_SWEEP_S = [2000.0, 3000.0, 4000.0]

# Dry-mass models (from R-radiator-mass-penalty).
MASS_MODELS: dict[str, dict] = {
    "bundled_10_W_per_kg": {
        "kind": "bundled",
        "m_fixed_t": 5.0,
        "specific_power_total_w_per_kg": 10.0,
    },
    "decomposed_mid": {
        "kind": "decomposed",
        "m_fixed_t": 3.0,
        "alpha_reactor_W_per_kg": 50.0,
        "alpha_PC_W_per_kg": 200.0,
        "alpha_radiator_kW_th_per_kg": 2.0,
        "eta_conv": 0.30,
        "f_tank": 0.05,
    },
}


def dry_mass_t(model: dict, reactor_kwe: float, m_prop_t: float = 0.0) -> float:
    """Return tug dry mass in tonnes, including tank scaled with propellant mass."""
    if model["kind"] == "bundled":
        m_stack = reactor_kwe / model["specific_power_total_w_per_kg"]
        return model["m_fixed_t"] + m_stack + m_prop_t * 0.05
    eta = model["eta_conv"]
    p_th_waste_kw = reactor_kwe * (1.0 - eta) / eta
    m_reactor = reactor_kwe / model["alpha_reactor_W_per_kg"]
    m_pc = reactor_kwe / model["alpha_PC_W_per_kg"]
    m_rad = p_th_waste_kw / model["alpha_radiator_kW_th_per_kg"] / 1000.0
    m_tank = m_prop_t * model["f_tank"]
    return model["m_fixed_t"] + m_reactor + m_pc + m_rad + m_tank


def outbound_delta_v_km_s() -> dict:
    """Derive the all-electric outbound integrated delta-velocity from first principles.

    Edelbaum spiral from low Earth orbit to Earth-escape integrates to v_circ_LEO.
    Post-escape, the spacecraft sits at Earth's heliocentric orbital speed; reaching
    Hohmann perihelion velocity requires the heliocentric excess v_∞_Earth.

    Returns the components plus the impulsive-equivalent (for the chemical-kick
    cross-check).
    """
    # Low Earth orbit circular speed
    r_leo_km = R_EARTH + LEO_ALT_KM
    v_circ_leo_km_s = math.sqrt(GM_EARTH / r_leo_km)

    # Heliocentric: Earth and Saturn circular speeds
    v_earth_helio = math.sqrt(GM_SUN / A_EARTH)
    # Hohmann semi-major axis (in km)
    a_h_km = (A_EARTH + A_SATURN) / 2.0
    # Hohmann perihelion velocity (Earth's distance, on the transfer ellipse)
    v_hohmann_peri = math.sqrt(GM_SUN * (2.0 / A_EARTH - 1.0 / a_h_km))
    # v_∞ at Earth on outbound Hohmann
    v_inf_earth = v_hohmann_peri - v_earth_helio

    # All-electric outbound integrated delta-velocity:
    #   Edelbaum LEO-to-escape: v_circ_LEO
    #   Heliocentric continuous burn from Earth's speed to Hohmann perihelion: v_inf
    dv_electric = v_circ_leo_km_s + v_inf_earth

    # Impulsive-equivalent (Oberth-discounted): combined departure burn at perigee
    # Δv_impulsive = sqrt(v_escape^2 + v_inf^2) - v_circ
    v_escape_leo = math.sqrt(2.0) * v_circ_leo_km_s
    dv_impulsive = math.sqrt(v_escape_leo ** 2 + v_inf_earth ** 2) - v_circ_leo_km_s

    return {
        "v_circ_LEO_km_s": v_circ_leo_km_s,
        "v_earth_helio_km_s": v_earth_helio,
        "v_hohmann_peri_km_s": v_hohmann_peri,
        "v_inf_earth_km_s": v_inf_earth,
        "dv_outbound_electric_km_s": dv_electric,
        "dv_outbound_impulsive_km_s": dv_impulsive,
    }


def hohmann_cruise_yr() -> float:
    """Hohmann transfer time, Earth to Saturn, in years."""
    a_h_km = (A_EARTH + A_SATURN) / 2.0
    # Convert to m for SI: but GM_SUN above is km^3/s^2, so keep km.
    # Period of full ellipse: T = 2π sqrt(a^3 / μ); Hohmann = T/2
    t_half_s = math.pi * math.sqrt(a_h_km ** 3 / GM_SUN)
    return t_half_s / YEAR_S


def constant_thrust_burn(m_initial_t: float, dv_km_s: float, power_kwe: float,
                          isp_s: float, eta: float = ETA_THR) -> dict:
    """Compute propellant mass and burn time for a constant-thrust electric burn.

    Approximation: thrust held constant over the burn while mass decreases. For
    mass ratios under ~2 this is accurate within ~5% versus the true Tsiolkovsky-
    consistent integration. Consistent with prior rounds.
    """
    v_e = isp_s * G0  # m/s
    thrust_N = 2.0 * eta * power_kwe * 1000.0 / v_e
    mass_ratio = math.exp(dv_km_s * 1000.0 / v_e)
    m_prop_t = m_initial_t * (1.0 - 1.0 / mass_ratio)
    # Burn time: m_prop × v_e / F
    t_burn_s = m_prop_t * 1000.0 * v_e / thrust_N  # m_prop in kg
    return {
        "thrust_N": thrust_N,
        "m_prop_t": m_prop_t,
        "mass_ratio": mass_ratio,
        "t_burn_s": t_burn_s,
        "t_burn_yr": t_burn_s / YEAR_S,
    }


def chemical_kick_multiplier(m_v_t: float) -> float:
    """Re-derive the R-outbound-architecture 6.9× multiplier from rocket equation.

    Mass accounting (working backward from Saturn capture):
      M_after_cap = m_v_t (vehicle clean)
      M_before_cap = m_v × exp(Δv_cap / v_e_elec)        (carry electric capture prop)
      M_after_kick = M_before_cap + M_kick_dry            (still has kick stage attached)
      M_before_kick = M_after_kick × exp(Δv_kick / v_e_chem)
      M_kick_prop = M_before_kick - M_after_kick
      M_kick_dry = (dry/wet) / (1 - dry/wet) × M_kick_prop

    Solve self-consistently for M_kick_dry; M_LEO = M_before_kick.
    """
    v_e_chem = ISP_KICK_S * G0
    v_e_elec = ISP_ELEC_CAP_S * G0
    m_before_cap = m_v_t * math.exp(DV_CAP_ELEC_KM_S * 1000.0 / v_e_elec)
    # Solve fixed point: M_kick_dry = k × (M_after_kick × (e^x − 1)) and M_after_kick = M_before_cap + M_kick_dry
    k = KICK_DRY_TO_WET / (1.0 - KICK_DRY_TO_WET)
    expo = math.exp(DV_KICK_KM_S * 1000.0 / v_e_chem) - 1.0
    # M_after_kick × (1) = M_before_cap + k × expo × M_after_kick
    # => M_after_kick × (1 - k × expo) = M_before_cap  -> only valid if k × expo < 1
    # Otherwise iterate. Compute:
    denom = 1.0 - k * expo
    if denom <= 0.0:
        # Kick stage dry mass grows faster than payload — pathological; iterate.
        m_after = m_before_cap
        for _ in range(100):
            m_kick_prop = m_after * expo
            m_kick_dry = k * m_kick_prop
            m_after_new = m_before_cap + m_kick_dry
            if abs(m_after_new - m_after) < 1e-6:
                break
            m_after = m_after_new
    else:
        m_after = m_before_cap / denom
    m_kick_prop = m_after * expo
    m_kick_dry = k * m_kick_prop
    m_leo = m_after + m_kick_prop
    return {
        "m_v_t": m_v_t,
        "m_after_kick_t": m_after,
        "m_kick_prop_t": m_kick_prop,
        "m_kick_dry_t": m_kick_dry,
        "m_LEO_t": m_leo,
        "multiplier": m_leo / m_v_t,
    }


def all_electric_round_trip(model: dict, reactor_kwe: float, chunk_t: float,
                             isp_s: float,
                             dv_outbound_km_s: float) -> dict:
    """Compute the full round-trip timeline at constant-thrust electric.

    Outbound: empty vehicle (m_tug + outbound prop), spirals to escape and on to Hohmann perihelion velocity.
    Cruise out: Hohmann ballistic.
    Saturn ops: 1 yr fixed.
    Inbound: vehicle + chunk burns Δv_inbound at electric Isp.
    Cruise back: Hohmann ballistic.
    """
    # Dry tug mass — first pass without propellant in tank (tank fraction depends on prop)
    # Solve self-consistently for outbound: m_tug depends on m_prop_out (via tank), and vice versa.
    m_tug_t = dry_mass_t(model, reactor_kwe, m_prop_t=0.0)
    for _ in range(6):
        burn_out = constant_thrust_burn(m_tug_t, dv_outbound_km_s, reactor_kwe, isp_s)
        new_m_tug = dry_mass_t(model, reactor_kwe, m_prop_t=burn_out["m_prop_t"])
        if abs(new_m_tug - m_tug_t) < 1e-4:
            m_tug_t = new_m_tug
            break
        m_tug_t = new_m_tug
    # Final outbound burn
    burn_out = constant_thrust_burn(m_tug_t, dv_outbound_km_s, reactor_kwe, isp_s)
    m_initial_out_t = m_tug_t  # at LEO (this is vehicle + outbound prop; the rocket eq already factored prop)
    # Actually m_initial = m_tug + m_prop_out
    m_leo_allelectric_t = m_tug_t + burn_out["m_prop_t"]

    # Inbound: m_initial = m_tug + chunk; same propellant tank but full again for the inbound burn
    burn_in = constant_thrust_burn(m_tug_t + chunk_t, DV_INBOUND_KM_S, reactor_kwe, isp_s)

    t_cruise_yr = hohmann_cruise_yr()
    round_trip_yr = (
        burn_out["t_burn_yr"] + t_cruise_yr + SATURN_OPS_YR + burn_in["t_burn_yr"] + t_cruise_yr
    )

    # Chemical-kick comparison for the same m_tug_t (no chunk on outbound — chunk picked up at Saturn)
    chemkick = chemical_kick_multiplier(m_tug_t)

    delivered_t = chunk_t - (
        # what reduces "delivered" is the inbound propellant; chunk arrives at Saturn intact (= chunk_t),
        # but on the way back the vehicle burns chunk-mass-equivalent propellant. Final delivered:
        burn_in["m_prop_t"]
    )

    return {
        "feasible": True,
        "m_tug_t": m_tug_t,
        "m_prop_outbound_t": burn_out["m_prop_t"],
        "m_LEO_allelectric_t": m_leo_allelectric_t,
        "m_LEO_chemkick_t": chemkick["m_LEO_t"],
        "chemkick_multiplier": chemkick["multiplier"],
        "thrust_N": burn_out["thrust_N"],
        "t_outbound_burn_yr": burn_out["t_burn_yr"],
        "t_cruise_each_yr": t_cruise_yr,
        "t_saturn_ops_yr": SATURN_OPS_YR,
        "m_prop_inbound_t": burn_in["m_prop_t"],
        "t_inbound_burn_yr": burn_in["t_burn_yr"],
        "round_trip_yr": round_trip_yr,
        "closes_15yr": round_trip_yr <= ROUND_TRIP_CEILING_YR,
        "delivered_t": delivered_t,
    }


def main() -> dict:
    results: dict = {}

    # 1. Outbound delta-velocity derivation
    dv_block = outbound_delta_v_km_s()
    results["outbound_dv_derivation"] = dv_block
    dv_out = dv_block["dv_outbound_electric_km_s"]

    # 2. Hohmann cruise time
    cruise_yr = hohmann_cruise_yr()
    results["hohmann_cruise_yr"] = cruise_yr

    # 3. Main sweep at baseline Isp 2000 s, chunk 200 t
    main_sweep = []
    for name, model in MASS_MODELS.items():
        for reactor in REACTOR_POWERS_KWE:
            row = all_electric_round_trip(model, reactor, CHUNK_T_BASELINE, 2000.0, dv_out)
            row.update({"mass_model": name, "reactor_kwe": reactor,
                         "chunk_t": CHUNK_T_BASELINE, "isp_s": 2000.0})
            main_sweep.append(row)
    results["main_sweep"] = main_sweep

    # 4. Isp sensitivity at 1000 kWe, decomposed-mid, chunk 200 t
    isp_sens = []
    for isp in ISP_SWEEP_S:
        row = all_electric_round_trip(MASS_MODELS["decomposed_mid"], 1000.0,
                                       CHUNK_T_BASELINE, isp, dv_out)
        row.update({"isp_s": isp})
        isp_sens.append(row)
    results["isp_sensitivity_1mwe"] = isp_sens

    # 5. Chunk sensitivity at 1000 kWe, decomposed-mid, Isp 2000 s
    chunk_sens = []
    for chunk in CHUNK_SENSITIVITY_T:
        row = all_electric_round_trip(MASS_MODELS["decomposed_mid"], 1000.0,
                                       chunk, 2000.0, dv_out)
        row.update({"chunk_t": chunk})
        chunk_sens.append(row)
    results["chunk_sensitivity_1mwe"] = chunk_sens

    # 6. 6.9× chemical-kick multiplier re-derivation check at a few m_v values
    chemkick_check = [chemical_kick_multiplier(m_v) for m_v in (5.0, 14.0, 29.0, 105.0)]
    results["chemkick_recheck"] = chemkick_check

    # 7. Smallest reactor class that closes inside 15 years, per mass model
    closes = {}
    for name in MASS_MODELS.keys():
        closing = [r for r in main_sweep
                   if r["mass_model"] == name and r["closes_15yr"]]
        if closing:
            min_r = min(closing, key=lambda r: r["reactor_kwe"])
            closes[name] = {
                "min_reactor_kwe": min_r["reactor_kwe"],
                "round_trip_yr": min_r["round_trip_yr"],
            }
        else:
            closes[name] = {"min_reactor_kwe": None, "round_trip_yr": None}
    results["close_threshold"] = closes

    # 8. Hypothesis grading
    def get_row(name, kwe):
        for r in main_sweep:
            if r["mass_model"] == name and r["reactor_kwe"] == kwe:
                return r
        return None

    dec = "decomposed_mid"
    bun = "bundled_10_W_per_kg"
    r_1mwe = get_row(dec, 1000.0)
    r_200kwe = get_row(dec, 200.0)
    r_40kwe = get_row(dec, 40.0)

    # H-eo-a: outbound delta-velocity 8.5–9.5 km/s (NB this is the prompt's stated band;
    # we have re-derived a much higher number for the all-electric continuous-burn case)
    h_eo_a_predicted_band = [8.5, 9.5]
    h_eo_a_held = h_eo_a_predicted_band[0] <= dv_out <= h_eo_a_predicted_band[1]

    h_eo_b_predicted = [1.5, 3.0]
    h_eo_b_actual = r_1mwe["t_outbound_burn_yr"]
    h_eo_b_held = h_eo_b_predicted[0] <= h_eo_b_actual <= h_eo_b_predicted[1]

    h_eo_c_predicted = [5.0, 9.0]
    h_eo_c_actual = r_200kwe["t_outbound_burn_yr"]
    h_eo_c_held = h_eo_c_predicted[0] <= h_eo_c_actual <= h_eo_c_predicted[1]

    h_eo_d_predicted = "> 15 yr (infeasible)"
    h_eo_d_actual = r_40kwe["t_outbound_burn_yr"]
    h_eo_d_held = h_eo_d_actual > 15.0

    h_eo_e_predicted = [12.0, 14.0]
    h_eo_e_actual = r_1mwe["round_trip_yr"]
    h_eo_e_held = h_eo_e_predicted[0] <= h_eo_e_actual <= h_eo_e_predicted[1]

    close_dec = closes[dec]["min_reactor_kwe"]
    close_bun = closes[bun]["min_reactor_kwe"]
    h_eo_f_predicted = "200 ≤ close-reactor ≤ 1000 kWe"
    h_eo_f_held = (close_dec is not None and 200.0 <= close_dec <= 1000.0)

    if close_dec is None or close_bun is None:
        h_eo_g_held = (close_dec is None and close_bun is None)
    else:
        powers = REACTOR_POWERS_KWE
        i_dec = powers.index(close_dec)
        i_bun = powers.index(close_bun)
        h_eo_g_held = abs(i_dec - i_bun) <= 1

    results["hypothesis_grading"] = {
        "H_eo_a": {"predicted_band_km_s": h_eo_a_predicted_band,
                   "actual_km_s": dv_out, "held": h_eo_a_held},
        "H_eo_b": {"predicted_band_yr": h_eo_b_predicted,
                   "actual_yr": h_eo_b_actual, "held": h_eo_b_held},
        "H_eo_c": {"predicted_band_yr": h_eo_c_predicted,
                   "actual_yr": h_eo_c_actual, "held": h_eo_c_held},
        "H_eo_d": {"predicted": h_eo_d_predicted,
                   "actual_yr": h_eo_d_actual, "held": h_eo_d_held},
        "H_eo_e": {"predicted_band_yr": h_eo_e_predicted,
                   "actual_yr": h_eo_e_actual, "held": h_eo_e_held},
        "H_eo_f": {"predicted": h_eo_f_predicted,
                   "actual_min_kwe_decomposed_mid": close_dec, "held": h_eo_f_held},
        "H_eo_g": {"predicted": "decomposed-mid and bundled close within 1 reactor class",
                   "actual_min_kwe_bundled": close_bun,
                   "actual_min_kwe_decomposed_mid": close_dec, "held": h_eo_g_held},
    }

    # Write outputs
    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)
    (results_dir / "electric_outbound.json").write_text(json.dumps(results, indent=2, default=str))

    # Tables
    lines = []
    lines.append("### Outbound delta-velocity derivation (first-principles)\n")
    lines.append(f"- Low Earth orbit circular speed at {LEO_ALT_KM:.0f} km altitude: "
                 f"{dv_block['v_circ_LEO_km_s']:.3f} km/s")
    lines.append(f"- Earth heliocentric orbital speed: {dv_block['v_earth_helio_km_s']:.3f} km/s")
    lines.append(f"- Hohmann perihelion velocity (Earth's distance): {dv_block['v_hohmann_peri_km_s']:.3f} km/s")
    lines.append(f"- v_∞ at Earth on outbound Hohmann: {dv_block['v_inf_earth_km_s']:.3f} km/s")
    lines.append(f"- **All-electric outbound integrated Δv (Edelbaum + heliocentric): "
                 f"{dv_block['dv_outbound_electric_km_s']:.3f} km/s**")
    lines.append(f"- Impulsive-equivalent Δv (Oberth-discounted, chemical-kick reference): "
                 f"{dv_block['dv_outbound_impulsive_km_s']:.3f} km/s")
    lines.append(f"- Hohmann cruise time, each way: {cruise_yr:.3f} years")
    lines.append("")
    lines.append("**Assumption check:** the prompt cites ~9 km/s for outbound. That figure is the *impulsive* delta-velocity (which gets the Oberth bonus from a single high-thrust burn at perigee). All-electric continuous-thrust does NOT get the Oberth bonus; the integrated delta-velocity is substantially higher (the Edelbaum spiral alone integrates to v_circ_LEO ≈ 7.67 km/s before the spacecraft even reaches Earth-escape).\n")

    lines.append("\n### Main sweep — all-electric round-trip per reactor class, decomposed-mid and bundled tug, chunk 200 t, electric Isp 2000 s\n")
    lines.append("Round-trip = outbound burn + cruise out (Hohmann) + Saturn ops (1 yr) + inbound burn + cruise back (Hohmann).\n")
    lines.append("| Reactor (kWe) | Model | m_tug (t) | t_out (yr) | cruise (yr) | t_in (yr) | Round-trip (yr) | Closes 15 yr? |")
    lines.append("|---:|---|---:|---:|---:|---:|---:|:--:|")
    for r in main_sweep:
        flag = "**yes**" if r["closes_15yr"] else "no"
        lines.append(
            f"| {r['reactor_kwe']:.0f} | {r['mass_model']} | "
            f"{r['m_tug_t']:.1f} | {r['t_outbound_burn_yr']:.2f} | "
            f"{r['t_cruise_each_yr']:.2f} | {r['t_inbound_burn_yr']:.2f} | "
            f"{r['round_trip_yr']:.2f} | {flag} |"
        )

    lines.append("\n### Specific-impulse sensitivity — 1 megawatt-electric, decomposed-mid, chunk 200 t\n")
    lines.append("| Isp (s) | t_out (yr) | t_in (yr) | Round-trip (yr) | Closes 15 yr? |")
    lines.append("|---:|---:|---:|---:|:--:|")
    for r in isp_sens:
        flag = "**yes**" if r["closes_15yr"] else "no"
        lines.append(
            f"| {r['isp_s']:.0f} | {r['t_outbound_burn_yr']:.2f} | "
            f"{r['t_inbound_burn_yr']:.2f} | {r['round_trip_yr']:.2f} | {flag} |"
        )

    lines.append("\n### Chunk sensitivity — 1 megawatt-electric, decomposed-mid, Isp 2000 s\n")
    lines.append("Outbound burn is chunk-independent; inbound scales linearly with chunk.\n")
    lines.append("| Chunk (t) | t_out (yr) | t_in (yr) | Round-trip (yr) | Closes 15 yr? |")
    lines.append("|---:|---:|---:|---:|:--:|")
    for r in chunk_sens:
        flag = "**yes**" if r["closes_15yr"] else "no"
        lines.append(
            f"| {r['chunk_t']:.0f} | {r['t_outbound_burn_yr']:.2f} | "
            f"{r['t_inbound_burn_yr']:.2f} | {r['round_trip_yr']:.2f} | {flag} |"
        )

    lines.append("\n### Chemical-kick multiplier re-derivation\n")
    lines.append("Per R-outbound-architecture, chemical-kick versus all-electric-outbound launch mass should be ~6.9×.\n")
    lines.append("Re-derivation here: M_LEO_chemkick / m_v_clean. The 6.9× R-outbound figure is "
                 "M_LEO_chemkick / M_LEO_allelectric_outbound; the all-electric-outbound LEO mass already "
                 "includes outbound propellant (mass ratio 1.583 at Δv = 9 km/s, Isp = 2000 s impulsive-equivalent). "
                 "10.92× / 1.583 = 6.9×. Both numbers are correct relative to their own baseline.\n")
    lines.append("| m_v (t) | m_kick_dry (t) | m_kick_prop (t) | m_LEO (t) | Multiplier vs m_v_clean |")
    lines.append("|---:|---:|---:|---:|---:|")
    for c in chemkick_check:
        lines.append(
            f"| {c['m_v_t']:.1f} | {c['m_kick_dry_t']:.1f} | "
            f"{c['m_kick_prop_t']:.1f} | {c['m_LEO_t']:.1f} | "
            f"{c['multiplier']:.2f}× |"
        )

    lines.append("\n### Close-threshold — smallest reactor that fits inside L0-05's 15-year ceiling\n")
    lines.append("| Mass model | Smallest reactor closing inside 15 yr (kWe) | Round-trip at that reactor (yr) |")
    lines.append("|---|---:|---:|")
    for name, info in closes.items():
        kwe = info["min_reactor_kwe"]
        rt = info["round_trip_yr"]
        kwe_str = f"{kwe:.0f}" if kwe is not None else "no class closes"
        rt_str = f"{rt:.2f}" if rt is not None else "—"
        lines.append(f"| {name} | {kwe_str} | {rt_str} |")

    lines.append("\n### Hypothesis grading\n")
    h = results["hypothesis_grading"]
    lines.append("| Sub-claim | Predicted | Actual | Held? |")
    lines.append("|---|---|---|---|")
    lines.append(f"| H-eo-a — Outbound Δv per first-principles derivation | "
                 f"{h['H_eo_a']['predicted_band_km_s']} km/s | "
                 f"{h['H_eo_a']['actual_km_s']:.2f} km/s | "
                 f"{'yes' if h['H_eo_a']['held'] else '**no**'} |")
    lines.append(f"| H-eo-b — Outbound burn at 1 MWe (decomposed-mid) | "
                 f"{h['H_eo_b']['predicted_band_yr']} yr | "
                 f"{h['H_eo_b']['actual_yr']:.2f} yr | "
                 f"{'yes' if h['H_eo_b']['held'] else '**no**'} |")
    lines.append(f"| H-eo-c — Outbound burn at 200 kWe (decomposed-mid) | "
                 f"{h['H_eo_c']['predicted_band_yr']} yr | "
                 f"{h['H_eo_c']['actual_yr']:.2f} yr | "
                 f"{'yes' if h['H_eo_c']['held'] else '**no**'} |")
    lines.append(f"| H-eo-d — Outbound burn at 40 kWe exceeds 15 yr | "
                 f"{h['H_eo_d']['predicted']} | "
                 f"{h['H_eo_d']['actual_yr']:.2f} yr | "
                 f"{'yes' if h['H_eo_d']['held'] else '**no**'} |")
    lines.append(f"| H-eo-e — Round-trip at 1 MWe (decomposed-mid) | "
                 f"{h['H_eo_e']['predicted_band_yr']} yr | "
                 f"{h['H_eo_e']['actual_yr']:.2f} yr | "
                 f"{'yes' if h['H_eo_e']['held'] else '**no**'} |")
    lines.append(f"| H-eo-f — Smallest reactor closing inside 15 yr (decomposed-mid) | "
                 f"{h['H_eo_f']['predicted']} | "
                 f"{h['H_eo_f']['actual_min_kwe_decomposed_mid']} kWe | "
                 f"{'yes' if h['H_eo_f']['held'] else '**no**'} |")
    lines.append(f"| H-eo-g — Bundled and decomposed-mid close within 1 reactor class | "
                 f"{h['H_eo_g']['predicted']} | "
                 f"bundled {h['H_eo_g']['actual_min_kwe_bundled']} kWe / "
                 f"decomposed-mid {h['H_eo_g']['actual_min_kwe_decomposed_mid']} kWe | "
                 f"{'yes' if h['H_eo_g']['held'] else '**no**'} |")

    (results_dir / "tables.md").write_text("\n".join(lines))
    return results


if __name__ == "__main__":
    out = main()
    dv = out["outbound_dv_derivation"]
    print("R-electric-outbound complete.")
    print(f"  Outbound Δv (electric continuous): {dv['dv_outbound_electric_km_s']:.2f} km/s")
    print(f"  Outbound Δv (impulsive equiv):     {dv['dv_outbound_impulsive_km_s']:.2f} km/s")
    print(f"  Hohmann cruise (each way):         {out['hohmann_cruise_yr']:.2f} yr")
    print()
    print("  Round-trip closures:")
    for name, info in out["close_threshold"].items():
        kwe = info["min_reactor_kwe"]
        rt = info["round_trip_yr"]
        if kwe is None:
            print(f"    {name}: NO class closes inside 15 yr")
        else:
            print(f"    {name}: closes at {kwe:.0f} kWe (round-trip {rt:.2f} yr)")
    print()
    print("  Hypothesis grading summary:")
    for k, v in out["hypothesis_grading"].items():
        print(f"    {k}: {'held' if v['held'] else 'FALSIFIED'}")
