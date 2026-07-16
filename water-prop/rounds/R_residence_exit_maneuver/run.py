"""Residence-class exit-Δv closure sweep.

Evaluates whether ICEBERG's residence-class architecture (ram-scoop accretion
of B-ring material at v_rel ~ 10 m/s, circularised at r ~ 100,000 km Saturn
orbit) closes to delivered fraction ≥ 10% (and ideally ≥ 17%, Option A parity)
under any candidate propulsion / trajectory / mission-profile configuration.

Eight configurations (A1–A8) plus composite A3+A5+A6 swept against H1–H9 in
STUDY.md.

Outputs:
  results/exit_dv_floor.csv          — H1: exit Δv from various residence orbits / strategies
  results/baseline_a1.csv            — H2 anchor: A1 baseline replicates 3.5%
  results/inbound_dv_reduction.csv   — H4: A2 / A3 aerocapture + Jupiter GA
  results/chemical_exit_a4.csv       — H3: A4 chemical-exit feasibility
  results/isp_uplift_a5.csv          — H5: A5 Isp 7000 exit-only
  results/jettison_hardware_a6.csv   — H6: A6 dry-mass reduction
  results/moon_ga_cascade_a7.csv     — H7: A7 inner-moon resonance pumping
  results/saturn_aerobrake_a8.csv    — H8: A8 entry-only aerobrake (control)
  results/composite_a3_a5_a6.csv     — H9: composite architecture
  results/summary.json               — headline numbers
"""

from __future__ import annotations

import csv
import json
from math import exp, log, sin, atan, sqrt, pi
from pathlib import Path

# -----------------------------------------------------------------------------
# Constants (SI, km-based for orbital mechanics; SI for propulsion)
# -----------------------------------------------------------------------------

G0 = 9.80665                 # m/s^2 (Isp -> exhaust velocity)
GM_SATURN = 3.7931187e7      # km^3/s^2
R_SATURN  = 60268.0          # km

# Saturnian moon catalogue (Mimas through Titan): GM [km^3/s^2], a [km], R [km]
# Sources: NASA JPL Solar System Dynamics, Saturn satellite ephemerides.
MOONS = [
    # name,        GM,       a (orbital radius, km),  R (mean radius, km)
    ("Mimas",      2.503,    185539.0,                198.2),
    ("Enceladus",  7.211,    238042.0,                252.1),
    ("Tethys",     41.21,    294672.0,                531.1),
    ("Dione",      73.116,   377415.0,                561.4),
    ("Rhea",       153.94,   527068.0,                763.8),
    ("Titan",      8978.14,  1221865.0,               2574.7),
    ("Iapetus",    120.51,   3560820.0,               734.5),
]

# Spacecraft model (central-estimate per R-conops-chunk-vs-ram-scoop and matrix lock)
M_DRY_T = 200.0              # tonnes — Variant B 500-kWe class spacecraft dry mass
M_COLLECTED_T = 200.0        # tonnes — collected B-ring slurry at residence point

# Reference Δv values (km/s) from prior rounds
DV_INBOUND_BASELINE = 24.7   # R-variant-B-impulsive-vs-continuous (hyperion, e6467ab)
                              # — continuous-thrust integrated inbound including 2 Edelbaum spirals
DV_EARTH_SPIRAL = 1.5         # one Earth-side Edelbaum capture spiral (R-inbound-dv-continuous-thrust)
DV_JUPITER_GA   = 2.5         # bounded v_∞ swing-by savings (standard patched-conic, max bending)

# Isp values (s)
ISP_NEP_BASELINE = 5000.0     # megawatt-electric NEP at near-term grid life (R-cathode-life-water-plasma)
ISP_NEP_UPLIFT   = 7000.0     # extended-mode NEP at higher grid voltage; admissible at low thrust
ISP_CHEM_LOXLH2  = 450.0      # LOX/LH2 from electrolysed water (RL-10 class)

# Residence orbit candidates (km)
R_RESIDENCE_CANDIDATES = [95000.0, 100000.0, 105000.0, 110000.0, 115000.0, 117000.0]

# Saturn Hill sphere (~km) for bi-elliptic high-apoapsis upper bound
R_HILL_SATURN = 65e6

# Earth-Saturn departure heliocentric v_∞ (rough)
V_INF_EARTH_DEP = 6.0         # km/s, typical low-energy outbound — bounds Jupiter GA savings

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

def v_circ(r: float, GM: float = GM_SATURN) -> float:
    """Circular orbital velocity at radius r [km] around body of GM [km^3/s^2]."""
    return sqrt(GM / r)

def v_escape(r: float, GM: float = GM_SATURN) -> float:
    """Escape velocity at radius r."""
    return sqrt(2.0 * GM / r)

def v_on_ellipse(r: float, a: float, GM: float = GM_SATURN) -> float:
    """Velocity at radius r on an ellipse with semi-major axis a (vis-viva)."""
    return sqrt(GM * (2.0 / r - 1.0 / a))

def tsiolkovsky_mass_ratio(dv_kms: float, isp_s: float) -> float:
    """m_initial / m_final for a single burn at given Δv [km/s] and Isp [s]."""
    return exp(dv_kms * 1000.0 / (isp_s * G0))

def delivered_fraction_segmented(segments, m_dry_t: float, m_collected_t: float) -> tuple[float, float]:
    """Apply a sequence of (Δv_kms, Isp_s) segments. Spacecraft starts at residence
    exit point with m_dry + m_collected; propellant is drawn from collected mass
    (chunk-fed accounting). Solve for the delivered water mass at Earth such
    that the propellant burned across all segments exactly equals the collected
    mass minus delivered.

    Equation: m_initial = (m_dry + m_delivered) × Π_i exp(Δv_i / (Isp_i · g₀))
             m_initial = m_dry + m_collected  (chunk-fed; no extra propellant)

    Solve for m_delivered:
      m_delivered = (m_dry + m_collected) / Π - m_dry

    Returns (delivered_tonnes, delivered_fraction_of_collected).
    """
    pi_ratio = 1.0
    for dv_kms, isp_s in segments:
        pi_ratio *= tsiolkovsky_mass_ratio(dv_kms, isp_s)
    m_initial = m_dry_t + m_collected_t
    m_final = m_initial / pi_ratio
    m_delivered = m_final - m_dry_t
    if m_delivered < 0.0:
        return (m_delivered, m_delivered / m_collected_t)  # negative = does not close
    return (m_delivered, m_delivered / m_collected_t)


# -----------------------------------------------------------------------------
# Body 1 — Exit Δv floor (H1)
# -----------------------------------------------------------------------------

def exit_dv_direct(r_residence: float) -> float:
    """Direct propulsive escape from circular orbit at r_residence."""
    return v_escape(r_residence) - v_circ(r_residence)

def exit_dv_bielliptic_low_perihelion(r_residence: float, r_perihelion: float) -> float:
    """Bi-elliptic via low perihelion: drop periapsis, escape from low r."""
    # Burn 1: at r_residence, lower periapsis to r_perihelion (apoapsis stays at r_residence)
    a1 = (r_residence + r_perihelion) / 2.0
    v_at_res_on_ellipse_1 = v_on_ellipse(r_residence, a1)
    dv1 = v_circ(r_residence) - v_at_res_on_ellipse_1  # positive if slowing to lower periapsis
    # Burn 2: at r_perihelion of new ellipse, escape Saturn
    v_at_per_on_ellipse_1 = v_on_ellipse(r_perihelion, a1)
    v_escape_per = v_escape(r_perihelion)
    dv2 = v_escape_per - v_at_per_on_ellipse_1
    return dv1 + dv2

def exit_dv_bielliptic_high_apoapsis(r_residence: float, r_apoapsis: float) -> float:
    """Bi-elliptic via high apoapsis: raise apoapsis, escape from high r (cheap)."""
    a1 = (r_residence + r_apoapsis) / 2.0
    v_at_res_on_ellipse_1 = v_on_ellipse(r_residence, a1)
    dv1 = v_at_res_on_ellipse_1 - v_circ(r_residence)
    v_at_apo_on_ellipse_1 = v_on_ellipse(r_apoapsis, a1)
    v_escape_apo = v_escape(r_apoapsis)
    dv2 = v_escape_apo - v_at_apo_on_ellipse_1
    return dv1 + dv2

def body1_exit_dv_floor(out: Path) -> dict:
    rows = []
    for r in R_RESIDENCE_CANDIDATES:
        direct = exit_dv_direct(r)
        bi_low_15 = exit_dv_bielliptic_low_perihelion(r, 1.5 * R_SATURN)
        bi_low_10 = exit_dv_bielliptic_low_perihelion(r, 1.0 * R_SATURN)
        bi_high = exit_dv_bielliptic_high_apoapsis(r, R_HILL_SATURN)
        rows.append({
            "r_residence_km": r,
            "v_circ_kms": v_circ(r),
            "dv_direct_kms": direct,
            "dv_bielliptic_low_1p5Rs_kms": bi_low_15,
            "dv_bielliptic_low_1p0Rs_kms": bi_low_10,
            "dv_bielliptic_high_hill_kms": bi_high,
            "min_dv_kms": min(direct, bi_low_15, bi_low_10, bi_high),
        })
    _write_csv(out, rows)
    # Headline: minimum exit Δv across strategy × radius
    headline_min = min(r["min_dv_kms"] for r in rows)
    headline_max = max(r["dv_direct_kms"] for r in rows)
    return {
        "exit_dv_min_kms": headline_min,
        "exit_dv_max_direct_kms": headline_max,
        "headline": f"Exit Δv from residence orbit (any strategy): [{headline_min:.2f}, {headline_max:.2f}] km/s",
    }


# -----------------------------------------------------------------------------
# Body 2 — Baseline A1 anchor (H2)
# -----------------------------------------------------------------------------

def body2_a1_baseline(out: Path) -> dict:
    # Use direct escape from 100,000 km circular (R-bring-fine-structure value: 7.4 km/s)
    # Note R-bring-fine-structure reported 7.4 km/s as half the round-trip 14.7 km/s.
    # Direct escape from circular 100k is 0.414 * v_circ = 0.414 * 19.467 = 8.06 km/s.
    # The 7.4 figure folds an optimal departure direction / Saturn rotation gain.
    # For A1 anchor, use the prior round's quoted 7.4 km/s so we replicate 3.5%.
    rows = []
    for dv_exit, label in [(7.4, "as-reported (prior round)"), (8.06, "direct from 100k circular")]:
        segments = [(dv_exit, ISP_NEP_BASELINE), (DV_INBOUND_BASELINE, ISP_NEP_BASELINE)]
        m_del, frac = delivered_fraction_segmented(segments, M_DRY_T, M_COLLECTED_T)
        rows.append({
            "label": label,
            "dv_exit_kms": dv_exit,
            "dv_inbound_kms": DV_INBOUND_BASELINE,
            "isp_s": ISP_NEP_BASELINE,
            "m_dry_t": M_DRY_T,
            "m_collected_t": M_COLLECTED_T,
            "m_delivered_t": m_del,
            "delivered_fraction": frac,
        })
    _write_csv(out, rows)
    return {
        "a1_delivered_fraction_as_reported": rows[0]["delivered_fraction"],
        "a1_delivered_fraction_direct": rows[1]["delivered_fraction"],
        "headline": f"A1 baseline delivered fraction: {rows[0]['delivered_fraction']:.3f} (as-reported), {rows[1]['delivered_fraction']:.3f} (direct 8.06 km/s)",
    }


# -----------------------------------------------------------------------------
# Body 3 — Configurations A2, A3 (inbound Δv reduction) (H4)
# -----------------------------------------------------------------------------

def body3_inbound_dv_reduction(out: Path) -> dict:
    dv_exit = 7.4
    rows = []
    configs = [
        ("A2 Earth aerocapture", DV_INBOUND_BASELINE - DV_EARTH_SPIRAL),
        ("A3 Earth aerocapture + Jupiter GA", DV_INBOUND_BASELINE - DV_EARTH_SPIRAL - DV_JUPITER_GA),
        ("A3- Jupiter GA only (no aerocapture)", DV_INBOUND_BASELINE - DV_JUPITER_GA),
    ]
    for label, dv_in in configs:
        segments = [(dv_exit, ISP_NEP_BASELINE), (dv_in, ISP_NEP_BASELINE)]
        m_del, frac = delivered_fraction_segmented(segments, M_DRY_T, M_COLLECTED_T)
        rows.append({
            "label": label,
            "dv_exit_kms": dv_exit,
            "dv_inbound_kms": dv_in,
            "isp_s": ISP_NEP_BASELINE,
            "m_delivered_t": m_del,
            "delivered_fraction": frac,
        })
    _write_csv(out, rows)
    a3 = next(r for r in rows if r["label"] == "A3 Earth aerocapture + Jupiter GA")
    return {
        "a2_delivered_fraction": rows[0]["delivered_fraction"],
        "a3_delivered_fraction": a3["delivered_fraction"],
        "headline": f"A2: {rows[0]['delivered_fraction']:.3f}; A3 (aerocapture + Jupiter GA): {a3['delivered_fraction']:.3f}",
    }


# -----------------------------------------------------------------------------
# Body 4 — Configuration A4 (chemical-electric hybrid) (H3)
# -----------------------------------------------------------------------------

def body4_a4_chemical(out: Path) -> dict:
    """Chemical exit using collected water → LOX/LH2 (Isp 450), electric inbound."""
    dv_exit = 7.4
    # A4a: chemical exit uses electrolysed-water LOX/LH2.
    # Engineering deductions from the collected payload before propulsive accounting:
    #   - electrolyser mass: assume 10 kg/kW × ~500 kW = 5 t (industrial-scale water electrolysis)
    #   - cryogen tankage: ~5% of stored propellant mass (insulated tank)
    #   - boiloff over 6-month Saturn residence: ~10% of stored cryogens
    # Effective collected mass available for chemical propellant after deductions.
    # We compute closure under two sub-cases: (a) electrolyser+tankage charged to collected mass,
    # (b) charged to dry mass.

    rows = []
    # A4a — chemical exit, electric inbound
    # Step 1: chemical burn at exit, mass ratio = exp(dv_exit / (Isp_chem * g₀))
    mass_ratio_chem = tsiolkovsky_mass_ratio(dv_exit, ISP_CHEM_LOXLH2)
    # Wet mass at exit start = m_dry + m_collected - electrolyser - tankage_for_chem_prop - boiloff
    electrolyser_t = 5.0
    boiloff_frac = 0.10
    tankage_frac = 0.05

    # Iterate: chemical propellant needed = (m_initial * (1 - 1/MR))
    # where m_initial = m_dry + m_collected_available
    # m_collected_available = m_collected - electrolyser - tankage_t - boiloff_t
    # tankage_t and boiloff_t depend on chemical propellant mass burned

    # Solve fixed point: P_chem = (m_dry + m_collected_available) * (1 - 1/MR_chem)
    #                    m_collected_available = m_collected - electrolyser - (tankage_frac + boiloff_frac) * P_chem
    # P_chem * (1 + (tankage_frac + boiloff_frac) * (1 - 1/MR_chem)) = (m_dry + m_collected - electrolyser) * (1 - 1/MR_chem)
    # actually let's just compute: after chemical, mass left = m_initial / MR_chem
    # but mass we *need* to deliver to inbound entry = m_dry + m_inbound_prop + m_finally_delivered

    # Let m_inbound_initial = mass at start of inbound burn (after chemical exit).
    # m_inbound_initial = m_initial / MR_chem where m_initial is the wet mass at exit start.
    # m_inbound_final = m_inbound_initial / MR_elec_inbound (with MR_elec_inbound at Isp 5000)
    # m_inbound_final = m_dry + m_delivered

    # We need to budget chemical propellant FROM the collected mass.
    # collected_used_as_chem = m_initial - m_inbound_initial = m_initial * (1 - 1/MR_chem)
    # collected_used_as_elec_inbound = m_inbound_initial - (m_dry + m_delivered)
    # collected_total_used = collected_used_as_chem + collected_used_as_elec_inbound
    # = m_initial - (m_dry + m_delivered)
    # Set m_initial = m_dry + (m_collected - electrolyser - other_losses)

    MR_elec_in = tsiolkovsky_mass_ratio(DV_INBOUND_BASELINE, ISP_NEP_BASELINE)
    other_losses = electrolyser_t  # baseline overhead

    # Now: collected_used_as_chem = m_initial * (1 - 1/MR_chem)
    # tankage + boiloff scale on this amount
    # so m_initial_effective = m_dry + m_collected - electrolyser - (tankage_frac + boiloff_frac) * collected_used_as_chem
    # Fixed-point iterate.

    m_collected_eff = M_COLLECTED_T - electrolyser_t
    for _ in range(50):
        m_initial = M_DRY_T + m_collected_eff
        p_chem = m_initial * (1 - 1.0 / mass_ratio_chem)
        tankage_boiloff = (tankage_frac + boiloff_frac) * p_chem
        m_collected_eff_new = M_COLLECTED_T - electrolyser_t - tankage_boiloff
        if abs(m_collected_eff_new - m_collected_eff) < 1e-4:
            m_collected_eff = m_collected_eff_new
            break
        m_collected_eff = m_collected_eff_new

    m_initial = M_DRY_T + m_collected_eff
    m_after_chem = m_initial / mass_ratio_chem
    m_after_inbound = m_after_chem / MR_elec_in
    m_delivered = m_after_inbound - M_DRY_T

    rows.append({
        "label": "A4a — chemical exit (LOX/LH2 from electrolysed water) + electric inbound",
        "dv_exit_kms": dv_exit,
        "isp_exit_s": ISP_CHEM_LOXLH2,
        "dv_inbound_kms": DV_INBOUND_BASELINE,
        "isp_inbound_s": ISP_NEP_BASELINE,
        "electrolyser_t": electrolyser_t,
        "tankage_t_est": tankage_frac * (m_initial * (1 - 1.0 / mass_ratio_chem)),
        "boiloff_t_est": boiloff_frac * (m_initial * (1 - 1.0 / mass_ratio_chem)),
        "p_chem_t": m_initial * (1 - 1.0 / mass_ratio_chem),
        "m_collected_effective_t": m_collected_eff,
        "m_initial_t": m_initial,
        "m_after_chem_t": m_after_chem,
        "m_after_inbound_t": m_after_inbound,
        "m_delivered_t": m_delivered,
        "delivered_fraction": m_delivered / M_COLLECTED_T,
    })

    # A4b — chemical propellant brought from Earth (no electrolysis)
    # Lift cost: outbound stack uses electric at Isp 5000, outbound Δv ~ 22 km/s (R-conops-skeleton)
    # 1 kg delivered to Saturn residence requires exp(22/49.05) ≈ 1.57 kg Earth-departure mass.
    # If we want to use chemical exit with mass ratio 5.34, propellant required = m_initial × (1 - 1/5.34) = 0.813 × m_initial
    # m_initial at residence = m_dry + m_collected + p_chem (brought from Earth, sits in tanks during accretion)
    # so p_chem = 0.813 × (M_DRY_T + M_COLLECTED_T + p_chem)
    # p_chem × (1 - 0.813) = 0.813 × (M_DRY_T + M_COLLECTED_T)
    # p_chem = 0.813 × 400 / 0.187 = 1739 t  — at residence
    # Lift cost: 1739 t × 1.57 = 2730 t at Earth departure (just for the chemical exit propellant)
    # Compared to baseline outbound dry+payload+returned-propellant budget, this is architecturally infeasible.

    p_chem_b = 0.813 * (M_DRY_T + M_COLLECTED_T) / (1.0 - 0.813)
    lift_factor = exp(22.0 * 1000.0 / (ISP_NEP_BASELINE * G0))  # ~1.57
    lift_cost = p_chem_b * lift_factor

    rows.append({
        "label": "A4b — chemical exit (Earth-brought LOX/LH2) + electric inbound",
        "dv_exit_kms": dv_exit,
        "isp_exit_s": ISP_CHEM_LOXLH2,
        "dv_inbound_kms": DV_INBOUND_BASELINE,
        "isp_inbound_s": ISP_NEP_BASELINE,
        "p_chem_required_at_residence_t": p_chem_b,
        "earth_departure_lift_mass_t": lift_cost,
        "verdict": "infeasible — 1700+ t of Earth-brought cryogen at residence, ~2700 t Earth departure",
        "m_delivered_t": float("nan"),
        "delivered_fraction": float("nan"),
    })

    _write_csv(out, rows)
    return {
        "a4a_delivered_fraction": rows[0]["delivered_fraction"],
        "a4b_p_chem_at_residence_t": rows[1]["p_chem_required_at_residence_t"],
        "a4b_earth_lift_t": rows[1]["earth_departure_lift_mass_t"],
        "headline": f"A4a: {rows[0]['delivered_fraction']:.3f}; A4b: infeasible ({rows[1]['p_chem_required_at_residence_t']:.0f} t cryogen at residence)",
    }


# -----------------------------------------------------------------------------
# Body 5 — Configuration A5 (Isp 7000 exit-only) (H5)
# -----------------------------------------------------------------------------

def body5_isp_uplift(out: Path) -> dict:
    dv_exit = 7.4
    rows = []
    isp_exit_sweep = [5000.0, 6000.0, 7000.0, 8000.0, 9000.0]
    for isp_exit in isp_exit_sweep:
        segments = [(dv_exit, isp_exit), (DV_INBOUND_BASELINE, ISP_NEP_BASELINE)]
        m_del, frac = delivered_fraction_segmented(segments, M_DRY_T, M_COLLECTED_T)
        rows.append({
            "isp_exit_s": isp_exit,
            "isp_inbound_s": ISP_NEP_BASELINE,
            "dv_exit_kms": dv_exit,
            "dv_inbound_kms": DV_INBOUND_BASELINE,
            "m_delivered_t": m_del,
            "delivered_fraction": frac,
        })
    # A5 headline at Isp_exit = 7000 s
    a5_row = next(r for r in rows if r["isp_exit_s"] == 7000.0)
    _write_csv(out, rows)
    return {
        "a5_delivered_fraction_at_isp7000": a5_row["delivered_fraction"],
        "headline": f"A5 (Isp 7000 exit, Isp 5000 inbound): {a5_row['delivered_fraction']:.3f}",
    }


# -----------------------------------------------------------------------------
# Body 6 — Configuration A6 (jettison residence hardware) (H6)
# -----------------------------------------------------------------------------

def body6_jettison(out: Path) -> dict:
    dv_exit = 7.4
    rows = []
    jettison_t_sweep = [0.0, 10.0, 20.0, 30.0, 40.0]
    for jett in jettison_t_sweep:
        m_dry_eff = M_DRY_T - jett
        # Jettison happens AFTER accretion, BEFORE exit burn. So mass at exit start
        # is (m_dry_eff + m_collected), and dry mass downstream is m_dry_eff.
        segments = [(dv_exit, ISP_NEP_BASELINE), (DV_INBOUND_BASELINE, ISP_NEP_BASELINE)]
        m_del, frac = delivered_fraction_segmented(segments, m_dry_eff, M_COLLECTED_T)
        rows.append({
            "jettison_t": jett,
            "m_dry_effective_t": m_dry_eff,
            "dv_exit_kms": dv_exit,
            "dv_inbound_kms": DV_INBOUND_BASELINE,
            "m_delivered_t": m_del,
            "delivered_fraction": frac,
        })
    a6_row = next(r for r in rows if r["jettison_t"] == 20.0)  # mid-band central estimate
    a6_extreme = next(r for r in rows if r["jettison_t"] == 40.0)
    _write_csv(out, rows)
    return {
        "a6_delivered_fraction_20t_jettison": a6_row["delivered_fraction"],
        "a6_delivered_fraction_40t_jettison": a6_extreme["delivered_fraction"],
        "headline": f"A6 (20 t jettison): {a6_row['delivered_fraction']:.3f}; (40 t): {a6_extreme['delivered_fraction']:.3f}",
    }


# -----------------------------------------------------------------------------
# Body 7 — Configuration A7 (moon GA cascade) (H7)
# -----------------------------------------------------------------------------

def moon_flyby_dv(GM_moon: float, R_moon: float, v_inf_kms: float,
                  min_alt_km: float = 50.0) -> float:
    """Maximum Δv from a single moon flyby at minimum-allowable-altitude pass.

    Δv = 2 v_∞ sin(δ/2),  tan(δ/2) = GM / (v_∞² · r_p)

    r_p = R_moon + min_alt
    """
    r_p = R_moon + min_alt_km
    v_inf_kmps_sq = v_inf_kms ** 2
    tan_half_delta = GM_moon / (v_inf_kmps_sq * r_p)
    half_delta = atan(tan_half_delta)
    return 2.0 * v_inf_kms * sin(half_delta)

def body7_moon_ga(out: Path) -> dict:
    # Compute v_∞ at each moon's orbit from a residence-100k-km hyperbolic-equivalent.
    # For a spacecraft at residence circular 100,000 km that wants to fly by Mimas at 185,000 km:
    #   Saturn-relative speed at 185,000 km on a transfer orbit from 100,000 km is computed via vis-viva.
    #   Relative-to-moon v_∞ ≈ |v_spacecraft - v_moon_circ| (rough patched-conic).
    # Apply Δv per flyby. Stack flybys assuming favourable phasing.

    rows = []
    r_res = 100000.0
    v_circ_res = v_circ(r_res)
    # Spacecraft initially in circular residence. To reach a moon at r_moon, raise apoapsis to r_moon.
    # Δv to raise apoapsis from r_res to r_moon: (Hohmann burn at periapsis r_res)
    # Then v at r_moon on transfer ellipse, compute v_∞ vs moon's circular velocity.

    cumulative_dv_gained = 0.0
    for name, GM_moon, a_moon, R_moon in MOONS:
        if a_moon > 1.5e6:  # skip Titan and beyond for the cascade
            continue
        a_transfer = (r_res + a_moon) / 2.0
        v_at_res_on_transfer = v_on_ellipse(r_res, a_transfer)
        dv_raise = v_at_res_on_transfer - v_circ_res  # cost to raise apoapsis to moon orbit
        v_sc_at_moon = v_on_ellipse(a_moon, a_transfer)
        v_moon_circ = v_circ(a_moon)
        v_inf = abs(v_sc_at_moon - v_moon_circ)
        dv_ga = moon_flyby_dv(GM_moon, R_moon, v_inf)
        net = dv_ga - dv_raise  # what we'd gain net, single flyby (round-trip the raise)
        rows.append({
            "moon": name,
            "GM_moon_km3_s2": GM_moon,
            "a_moon_km": a_moon,
            "R_moon_km": R_moon,
            "v_inf_at_moon_kms": v_inf,
            "dv_to_raise_apoapsis_kms": dv_raise,
            "dv_ga_max_per_flyby_kms": dv_ga,
            "net_dv_kms": net,  # negative means GA does not pay for the orbit raise
        })

    # Titan separately: cost of raising to Titan radius, then flyby Δv, then total exit from Titan-radius apoapsis
    titan = next((m for m in MOONS if m[0] == "Titan"), None)
    if titan:
        name, GM_moon, a_moon, R_moon = titan
        a_transfer = (r_res + a_moon) / 2.0
        v_at_res_on_transfer = v_on_ellipse(r_res, a_transfer)
        dv_raise = v_at_res_on_transfer - v_circ_res
        v_sc_at_moon = v_on_ellipse(a_moon, a_transfer)
        v_moon_circ = v_circ(a_moon)
        v_inf = abs(v_sc_at_moon - v_moon_circ)
        dv_ga = moon_flyby_dv(GM_moon, R_moon, v_inf)
        # Escape from Titan-radius apoapsis: very cheap (apoapsis v is small)
        # but we have to count the orbital energy raise.
        rows.append({
            "moon": name + " (apoapsis raise then GA then escape)",
            "GM_moon_km3_s2": GM_moon,
            "a_moon_km": a_moon,
            "R_moon_km": R_moon,
            "v_inf_at_moon_kms": v_inf,
            "dv_to_raise_apoapsis_kms": dv_raise,
            "dv_ga_max_per_flyby_kms": dv_ga,
            "net_dv_kms": dv_ga - dv_raise,
        })

    total_inner_ga = sum(r["dv_ga_max_per_flyby_kms"] for r in rows if r["moon"] != "Titan (apoapsis raise then GA then escape)")
    _write_csv(out, rows)
    return {
        "total_inner_moon_ga_max_kms": total_inner_ga,
        "titan_ga_net_kms": rows[-1]["net_dv_kms"] if rows[-1]["moon"].startswith("Titan") else None,
        "headline": f"Inner-moon cascade max Δv: {total_inner_ga:.3f} km/s; Titan GA net: {rows[-1]['net_dv_kms']:.3f} km/s (positive = lever, negative = penalty)",
    }


# -----------------------------------------------------------------------------
# Body 8 — Configuration A8 (Saturn aerobraking entry control) (H8)
# -----------------------------------------------------------------------------

def body8_aerobrake_entry(out: Path) -> dict:
    """A8 affects only the entry Δv, not the exit, not the inbound. As a delivered-
    fraction control, computes identical numbers to A1 because the chunk is
    collected after entry; subsequent burns (exit, inbound) are unchanged.
    Included to verify H8 numerically."""
    dv_exit = 7.4
    segments = [(dv_exit, ISP_NEP_BASELINE), (DV_INBOUND_BASELINE, ISP_NEP_BASELINE)]
    m_del, frac = delivered_fraction_segmented(segments, M_DRY_T, M_COLLECTED_T)
    rows = [{
        "label": "A8 — Saturn aerobraking entry only (exit + inbound unchanged)",
        "dv_entry_saved_kms": 7.4,
        "dv_exit_kms": dv_exit,
        "dv_inbound_kms": DV_INBOUND_BASELINE,
        "m_delivered_t": m_del,
        "delivered_fraction": frac,
        "note": "Identical to A1 by construction. Aerobraking helps outbound mass budget, not chunk-fed delivered fraction.",
    }]
    _write_csv(out, rows)
    return {
        "a8_delivered_fraction": frac,
        "headline": f"A8: {frac:.3f} (= A1; aerobraking entry does not lift chunk-fed delivered fraction)",
    }


# -----------------------------------------------------------------------------
# Body 9 — Composite A3+A5+A6 (H9)
# -----------------------------------------------------------------------------

def body9_composite(out: Path) -> dict:
    dv_exit = 7.4
    dv_inbound = DV_INBOUND_BASELINE - DV_EARTH_SPIRAL - DV_JUPITER_GA  # A3 inbound
    jettison_t = 20.0  # A6 mid-band
    m_dry_eff = M_DRY_T - jettison_t
    isp_exit = ISP_NEP_UPLIFT  # A5

    rows = []
    # Composite point estimate
    segments = [(dv_exit, isp_exit), (dv_inbound, ISP_NEP_BASELINE)]
    m_del, frac = delivered_fraction_segmented(segments, m_dry_eff, M_COLLECTED_T)
    rows.append({
        "label": "Composite A3+A5+A6 (central)",
        "dv_exit_kms": dv_exit,
        "isp_exit_s": isp_exit,
        "dv_inbound_kms": dv_inbound,
        "isp_inbound_s": ISP_NEP_BASELINE,
        "m_dry_effective_t": m_dry_eff,
        "m_delivered_t": m_del,
        "delivered_fraction": frac,
    })

    # Sensitivity: best case (max savings band)
    dv_inbound_best = DV_INBOUND_BASELINE - 2.0 - 3.5  # max Earth aerocapture + max Jupiter GA
    jettison_best = 30.0
    m_dry_best = M_DRY_T - jettison_best
    segments_best = [(dv_exit, isp_exit), (dv_inbound_best, ISP_NEP_BASELINE)]
    m_del_best, frac_best = delivered_fraction_segmented(segments_best, m_dry_best, M_COLLECTED_T)
    rows.append({
        "label": "Composite A3+A5+A6 (best case)",
        "dv_exit_kms": dv_exit,
        "isp_exit_s": isp_exit,
        "dv_inbound_kms": dv_inbound_best,
        "isp_inbound_s": ISP_NEP_BASELINE,
        "m_dry_effective_t": m_dry_best,
        "m_delivered_t": m_del_best,
        "delivered_fraction": frac_best,
    })

    # Worst case
    dv_inbound_worst = DV_INBOUND_BASELINE - 1.0 - 1.5  # min savings
    jettison_worst = 10.0
    m_dry_worst = M_DRY_T - jettison_worst
    segments_worst = [(dv_exit, isp_exit), (dv_inbound_worst, ISP_NEP_BASELINE)]
    m_del_worst, frac_worst = delivered_fraction_segmented(segments_worst, m_dry_worst, M_COLLECTED_T)
    rows.append({
        "label": "Composite A3+A5+A6 (worst case)",
        "dv_exit_kms": dv_exit,
        "isp_exit_s": isp_exit,
        "dv_inbound_kms": dv_inbound_worst,
        "isp_inbound_s": ISP_NEP_BASELINE,
        "m_dry_effective_t": m_dry_worst,
        "m_delivered_t": m_del_worst,
        "delivered_fraction": frac_worst,
    })

    _write_csv(out, rows)
    return {
        "composite_delivered_fraction_central": rows[0]["delivered_fraction"],
        "composite_delivered_fraction_best": rows[1]["delivered_fraction"],
        "composite_delivered_fraction_worst": rows[2]["delivered_fraction"],
        "headline": f"Composite delivered fraction: central {rows[0]['delivered_fraction']:.3f}, range [{rows[2]['delivered_fraction']:.3f}, {rows[1]['delivered_fraction']:.3f}]",
    }


# -----------------------------------------------------------------------------
# CSV helper
# -----------------------------------------------------------------------------

def _write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    # Make sure all rows have all fieldnames (fill missing)
    all_keys: list[str] = []
    seen = set()
    for r in rows:
        for k in r.keys():
            if k not in seen:
                seen.add(k)
                all_keys.append(k)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=all_keys)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in all_keys})


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main() -> None:
    out = Path(__file__).parent / "results"
    out.mkdir(parents=True, exist_ok=True)

    summary = {}
    summary["body1_exit_dv_floor"] = body1_exit_dv_floor(out / "exit_dv_floor.csv")
    summary["body2_a1_baseline"] = body2_a1_baseline(out / "baseline_a1.csv")
    summary["body3_inbound_dv_reduction"] = body3_inbound_dv_reduction(out / "inbound_dv_reduction.csv")
    summary["body4_a4_chemical"] = body4_a4_chemical(out / "chemical_exit_a4.csv")
    summary["body5_isp_uplift"] = body5_isp_uplift(out / "isp_uplift_a5.csv")
    summary["body6_jettison"] = body6_jettison(out / "jettison_hardware_a6.csv")
    summary["body7_moon_ga"] = body7_moon_ga(out / "moon_ga_cascade_a7.csv")
    summary["body8_aerobrake_entry"] = body8_aerobrake_entry(out / "saturn_aerobrake_a8.csv")
    summary["body9_composite"] = body9_composite(out / "composite_a3_a5_a6.csv")

    with (out / "summary.json").open("w") as f:
        json.dump(summary, f, indent=2)

    print("=" * 70)
    print("R-residence-exit-maneuver — headline results")
    print("=" * 70)
    for body, data in summary.items():
        print(f"\n[{body}]")
        if isinstance(data, dict) and "headline" in data:
            print(f"  {data['headline']}")


if __name__ == "__main__":
    main()
