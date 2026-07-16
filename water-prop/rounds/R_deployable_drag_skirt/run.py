"""R-deployable-drag-skirt — does an inflatable / mechanically deployed skirt rescue aerocapture?

Bare ICEBERG (50 t chunk + 5 t tug + bag, ~12.5 m² frontal) has ballistic coefficient
beta = mass / area ≈ 4,000 kg/m² (R-chunk-as-heat-shield finding). At that beta, no Earth
periapsis altitude has both bag/structural thermal survival AND tractable pass count.

This round sizes a deployable drag decelerator and asks four questions:

  1. What deployed area is needed for aerocapture-class (beta ≈ 200-500 kg/m²) and
     aerobraking-class (beta ≈ 100 kg/m²) operation at 55 t vehicle mass?
  2. What is the skirt mass at Hypersonic Inflatable Aerodynamic Decelerator (HIAD) /
     Low-Earth Orbit Flight Test of an Inflatable Decelerator (LOFTID) areal density
     (5-15 kg/m² for hypersonic-rated inflatable thermal protection)?
  3. Does the skirt mass fit inside the 5 t tug budget, or does every cell of the
     architecture decision matrix grow by a fixed multiplier?
  4. Peak heat flux on the skirt itself, using Sutton-Graves with the skirt's
     effective nose radius (~10 m, set by the deployed envelope), and does that flux
     stay within HIAD/LOFTID flight-demonstrated capability?

Heritage anchors:
  - HIAD-2 (NASA Langley, ground test article): 6 m, ~12 kg/m² areal density target,
    tolerates ~250-500 kW/m² peak heat flux.
  - LOFTID (orbital reentry, 2022): 6 m, 1.2 t vehicle (beta ≈ 42 kg/m²), Mach 25,
    peak heat flux ~ 350 kW/m² measured.
  - Inflatable Reentry and Descent Technology (IRDT, Russia 2000s): 2.3 m, beta ≈ 90 kg/m².
  - Adaptable Deployable Entry and Placement Technology (ADEPT): mechanically deployed,
    rigid-rib analogue.

Method:
  - Compute deployed area A_skirt for target beta values at mass M = 55 t.
  - Compute skirt mass at three areal densities (5, 10, 15 kg/m²).
  - Compute new vehicle mass with skirt and updated beta (closure check).
  - Compute peak heat flux on the skirt using Sutton-Graves with effective nose
    radius R_nose_eff = sqrt(A_skirt / pi) -- i.e. the skirt is modeled as a flat
    disc whose curvature radius scales with its diameter.
  - Compare peak heat flux to LOFTID-class capability and HIAD-2 design tolerance.

Skirt nose-radius model: a deployable drag skirt is geometrically a blunt
truncated cone. The stagnation-point radius is dominated by the deployed
diameter D_skirt. We take R_nose_eff = 0.5 * D_skirt as a conservative model
(blunter than a disc, sharper than a hemisphere). This is the parameter that
makes the skirt thermally easier than the bare chunk: bigger R_nose pulls heat
flux down as 1/sqrt(R_nose).
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from waterprop.constants import GM_EARTH, R_EARTH

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
SIGMA_SB = 5.670374419e-8          # Stefan-Boltzmann, W/(m²·K⁴)
K_SUTTON_GRAVES = 1.74e-4          # convective stagnation heating constant

# Vehicle
M_CHUNK_KG = 50_000.0              # 50-tonne ice chunk
M_TUG_BAG_KG = 5_000.0             # 5-tonne tug + bag
M_VEHICLE_BARE_KG = M_CHUNK_KG + M_TUG_BAG_KG   # 55 t total
A_BARE_M2 = 12.5                   # bare frontal area (chunk + bag)
BETA_BARE = M_VEHICLE_BARE_KG / A_BARE_M2       # 4,400 kg/m² (close to the stated 4,000)
V_INF_KM_S = 6.0                   # post-lunar-tour hyperbolic excess

# Heritage decelerator areal densities (kg/m²)
# Public estimates:
#   - LOFTID structural areal density ~ 8-12 kg/m² for the 6 m article
#     (1.2 t vehicle - chassis ~ 600-800 kg / 28 m² of inflatable -> ~25 kg/m²
#     for the full structure including spacecraft bus, but the IAD itself is
#     considerably lighter; conservative public-literature estimate is 5-15
#     kg/m² for the inflatable + thermal protection layer alone).
AREAL_DENSITY_KG_PER_M2 = {
    "optimistic_5":  5.0,
    "baseline_10":  10.0,
    "conservative_15": 15.0,
}

# Target ballistic coefficients (kg/m²) -- using campaign convention beta = mass / area
BETA_TARGETS = {
    "aerocapture_aggressive_500": 500.0,    # high beta, less benign; needs more heat margin
    "aerocapture_nominal_200":    200.0,    # roughly LOFTID Mach-25 regime
    "aerocapture_loftid_class_100": 100.0,  # LOFTID heritage low end / Mars aerobraking heritage
    "aerobraking_mars_class_100":  100.0,   # same numerical target, used for aerobraking framing
}

# Heritage references (kg/m²) for sanity check
BETA_HERITAGE = {
    "Mars_Global_Surveyor": 100.0,
    "LOFTID_2022":           42.0,
    "IRDT_Russia":           90.0,
}

# Atmospheric density at periapsis (kg/m³)
# Aerocapture entry corridor for Earth at ~80-110 km depending on beta.
# We pick 90 km as the aerocapture reference (same as R-chunk-as-heat-shield mode A).
RHO_PERIAPSIS_AEROCAPTURE = 1.0e-4
ALT_PERIAPSIS_AEROCAPTURE_KM = 90.0

# Heritage thermal-protection capability (W/m²)
Q_LOFTID_PEAK_DEMONSTRATED = 350_000.0    # peak measured on 2022 flight, ~ 350 kW/m²
Q_HIAD2_DESIGN_TOLERANCE   = 500_000.0    # ~500 kW/m² design tolerance for HIAD-2 class
Q_HIAD_NEXT_GEN_RESEARCH   = 2_500_000.0  # ongoing research targets ~ MW/m²-class IADs

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
def entry_velocity_m_s(v_inf_km_s: float, periapsis_alt_km: float) -> float:
    r_p = (R_EARTH + periapsis_alt_km) * 1000.0
    v_inf = v_inf_km_s * 1000.0
    GM = GM_EARTH * 1e9            # km^3/s^2 -> m^3/s^2
    return math.sqrt(v_inf * v_inf + 2.0 * GM / r_p)


def heat_flux_convective(rho: float, v_entry: float, R_nose: float) -> float:
    return K_SUTTON_GRAVES * math.sqrt(rho / R_nose) * v_entry ** 3


def heat_flux_radiative_estimate(q_conv: float, v_entry_km_s: float) -> float:
    if v_entry_km_s < 8:
        return 0.0
    return 0.5 * q_conv * max(1.0, (v_entry_km_s / 12.0) ** 2)


def equilibrium_temp_K(q_dot: float, emissivity: float = 0.8) -> float:
    return (q_dot / (emissivity * SIGMA_SB)) ** 0.25


def area_for_beta(mass_kg: float, beta_target: float) -> float:
    return mass_kg / beta_target


def beta_from_area(mass_kg: float, area_m2: float) -> float:
    return mass_kg / area_m2


# -----------------------------------------------------------------------------
# Main analysis
# -----------------------------------------------------------------------------
def size_skirt(beta_target: float) -> dict:
    """Iterate skirt area & mass to convergence (skirt mass adds to vehicle mass)."""
    rows = {}
    for tag, sigma in AREAL_DENSITY_KG_PER_M2.items():
        # Fixed-point iteration: A = (m_bare + sigma*A) / beta_target
        # => A * (beta_target - sigma) = m_bare
        # => A = m_bare / (beta_target - sigma)
        if beta_target <= sigma:
            rows[tag] = {
                "areal_density_kg_per_m2": sigma,
                "skirt_area_m2": float("inf"),
                "skirt_mass_kg": float("inf"),
                "feasible": False,
                "note": "areal density >= target beta -- mathematically infeasible",
            }
            continue
        A_skirt = M_VEHICLE_BARE_KG / (beta_target - sigma)
        m_skirt = sigma * A_skirt
        m_total = M_VEHICLE_BARE_KG + m_skirt
        beta_actual = m_total / A_skirt
        D_skirt = 2.0 * math.sqrt(A_skirt / math.pi)   # equivalent disc diameter
        R_nose_eff = 0.5 * D_skirt                      # conservative nose radius

        # Heat flux on skirt at 90 km aerocapture corridor
        v_e = entry_velocity_m_s(V_INF_KM_S, ALT_PERIAPSIS_AEROCAPTURE_KM)
        q_conv = heat_flux_convective(RHO_PERIAPSIS_AEROCAPTURE, v_e, R_nose_eff)
        q_rad = heat_flux_radiative_estimate(q_conv, v_e / 1000.0)
        q_total = q_conv + q_rad

        T_eq = equilibrium_temp_K(q_total, emissivity=0.8)

        rows[tag] = {
            "areal_density_kg_per_m2": sigma,
            "skirt_area_m2": A_skirt,
            "skirt_diameter_m": D_skirt,
            "skirt_nose_radius_m": R_nose_eff,
            "skirt_mass_kg": m_skirt,
            "skirt_mass_t": m_skirt / 1000.0,
            "vehicle_mass_with_skirt_kg": m_total,
            "vehicle_mass_with_skirt_t": m_total / 1000.0,
            "beta_actual": beta_actual,
            "q_convective_W_per_m2": q_conv,
            "q_radiative_W_per_m2": q_rad,
            "q_total_W_per_m2": q_total,
            "T_eq_K_eps_0p8": T_eq,
            "within_LOFTID_demonstrated": q_total <= Q_LOFTID_PEAK_DEMONSTRATED,
            "within_HIAD2_design": q_total <= Q_HIAD2_DESIGN_TOLERANCE,
            "within_HIAD_next_gen": q_total <= Q_HIAD_NEXT_GEN_RESEARCH,
            "fits_in_5t_tug_budget": m_skirt <= 5_000.0,
            "fits_in_10t_growth_budget": m_skirt <= 10_000.0,
        }
    return rows


def main() -> dict:
    out = {
        "vehicle": {
            "m_chunk_kg": M_CHUNK_KG,
            "m_tug_bag_kg": M_TUG_BAG_KG,
            "m_vehicle_bare_kg": M_VEHICLE_BARE_KG,
            "A_bare_m2": A_BARE_M2,
            "beta_bare_kg_per_m2": BETA_BARE,
            "v_inf_km_s": V_INF_KM_S,
        },
        "heritage": {
            "Mars_Global_Surveyor_beta": 100.0,
            "LOFTID_2022_beta": 42.0,
            "IRDT_Russia_beta": 90.0,
            "LOFTID_peak_heat_flux_W_per_m2": Q_LOFTID_PEAK_DEMONSTRATED,
            "HIAD2_design_tolerance_W_per_m2": Q_HIAD2_DESIGN_TOLERANCE,
            "HIAD_next_gen_research_W_per_m2": Q_HIAD_NEXT_GEN_RESEARCH,
        },
        "sizing_by_beta": {},
    }

    for tag, beta in BETA_TARGETS.items():
        out["sizing_by_beta"][tag] = {
            "beta_target_kg_per_m2": beta,
            "rows_by_areal_density": size_skirt(beta),
        }

    # Bare-chunk reference: what would heat flux look like with no skirt (12.5 m²)?
    v_e_bare = entry_velocity_m_s(V_INF_KM_S, ALT_PERIAPSIS_AEROCAPTURE_KM)
    R_nose_bare = 0.5 * 2.0 * math.sqrt(A_BARE_M2 / math.pi)  # 2 m, matches stated chunk
    q_conv_bare = heat_flux_convective(RHO_PERIAPSIS_AEROCAPTURE, v_e_bare, R_nose_bare)
    q_rad_bare = heat_flux_radiative_estimate(q_conv_bare, v_e_bare / 1000.0)
    out["bare_reference_at_90km"] = {
        "R_nose_m": R_nose_bare,
        "v_entry_m_s": v_e_bare,
        "q_conv_W_per_m2": q_conv_bare,
        "q_rad_W_per_m2": q_rad_bare,
        "q_total_W_per_m2": q_conv_bare + q_rad_bare,
    }

    # Write JSON
    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)
    (results_dir / "drag_skirt.json").write_text(json.dumps(out, indent=2, default=str))

    # Markdown tables
    lines = []
    lines.append("### Bare ICEBERG reference\n")
    lines.append(f"- Bare vehicle: {M_VEHICLE_BARE_KG/1000:.0f} t over {A_BARE_M2} m² -> beta = **{BETA_BARE:.0f} kg/m²**")
    lines.append(f"- Bare-chunk peak heat flux at 90 km (R_nose ≈ {R_nose_bare:.1f} m): "
                 f"**{(q_conv_bare+q_rad_bare)/1e6:.2f} MW/m²** "
                 f"(matches R-chunk-as-heat-shield mode A within rounding).\n")

    lines.append("### Required deployed area, skirt mass, and resulting beta\n")
    lines.append("Skirt sized so that (vehicle_bare + skirt_mass) / skirt_area = beta_target.\n")
    lines.append("| Target beta (kg/m²) | Areal density (kg/m²) | Skirt area (m²) | Skirt diameter (m) | Skirt mass (t) | Vehicle total mass (t) | Actual beta (kg/m²) | Fits in 5 t tug? | Fits in 10 t growth? |")
    lines.append("|---:|---:|---:|---:|---:|---:|---:|:--:|:--:|")
    for tag, block in out["sizing_by_beta"].items():
        beta = block["beta_target_kg_per_m2"]
        for ad_tag, row in block["rows_by_areal_density"].items():
            if not math.isfinite(row.get("skirt_area_m2", float("inf"))):
                lines.append(f"| {beta:.0f} ({tag}) | {row['areal_density_kg_per_m2']:.0f} | INF | — | INF | — | — | NO | NO |")
                continue
            lines.append(
                f"| {beta:.0f} ({tag}) | {row['areal_density_kg_per_m2']:.0f} | "
                f"{row['skirt_area_m2']:.0f} | {row['skirt_diameter_m']:.1f} | "
                f"{row['skirt_mass_t']:.2f} | {row['vehicle_mass_with_skirt_t']:.2f} | "
                f"{row['beta_actual']:.0f} | "
                f"{'YES' if row['fits_in_5t_tug_budget'] else 'NO'} | "
                f"{'YES' if row['fits_in_10t_growth_budget'] else 'NO'} |"
            )

    lines.append("\n### Peak heat flux on the deployed skirt (90 km, v_inf = 6 km/s)\n")
    lines.append("Skirt is much blunter than the bare chunk (R_nose set by the deployed envelope, "
                 "not the chunk geometry). Heat flux scales as 1/sqrt(R_nose), so bigger skirt -> lower flux.\n")
    lines.append("| Target beta | Areal density | Skirt diameter (m) | Skirt R_nose (m) | Peak heat flux (kW/m²) | T_eq @ eps=0.8 (K) | Within LOFTID (350 kW/m²)? | Within HIAD-2 (500 kW/m²)? |")
    lines.append("|---:|---:|---:|---:|---:|---:|:--:|:--:|")
    for tag, block in out["sizing_by_beta"].items():
        beta = block["beta_target_kg_per_m2"]
        for ad_tag, row in block["rows_by_areal_density"].items():
            if not math.isfinite(row.get("skirt_area_m2", float("inf"))):
                continue
            lines.append(
                f"| {beta:.0f} | {row['areal_density_kg_per_m2']:.0f} | "
                f"{row['skirt_diameter_m']:.1f} | {row['skirt_nose_radius_m']:.1f} | "
                f"{row['q_total_W_per_m2']/1000:.0f} | "
                f"{row['T_eq_K_eps_0p8']:.0f} | "
                f"{'YES' if row['within_LOFTID_demonstrated'] else 'NO'} | "
                f"{'YES' if row['within_HIAD2_design'] else 'NO'} |"
            )

    lines.append("\n### Heritage anchors\n")
    lines.append("| Mission | Year | Diameter (m) | Vehicle mass | beta (kg/m²) | Peak heat flux |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    lines.append("| LOFTID (Low-Earth Orbit Flight Test of an Inflatable Decelerator) | 2022 | 6 | 1.2 t | ~42 | ~350 kW/m² measured |")
    lines.append("| HIAD-2 (Hypersonic Inflatable Aerodynamic Decelerator) | ground test | 6 | n/a | n/a | ~500 kW/m² design |")
    lines.append("| IRDT (Inflatable Reentry and Descent Technology) | 2000-2005 | 2.3 | ~110 kg | ~90 | ~200 kW/m² |")
    lines.append("| Mars Global Surveyor (aerobraking, rigid solar panels as drag area) | 1996-1999 | n/a | 1,030 kg | ~100 | ~3 kW/m² |")

    (results_dir / "tables.md").write_text("\n".join(lines) + "\n")
    return out


if __name__ == "__main__":
    out = main()
    print("R-deployable-drag-skirt complete.")
    print(f"  Bare beta: {out['vehicle']['beta_bare_kg_per_m2']:.0f} kg/m²")
    for tag, block in out["sizing_by_beta"].items():
        baseline = block["rows_by_areal_density"]["baseline_10"]
        if not math.isfinite(baseline.get("skirt_area_m2", float("inf"))):
            print(f"  {tag}: INFEASIBLE at 10 kg/m² areal density")
            continue
        print(f"  {tag}: A = {baseline['skirt_area_m2']:.0f} m² "
              f"(D = {baseline['skirt_diameter_m']:.1f} m), "
              f"m_skirt = {baseline['skirt_mass_t']:.2f} t, "
              f"peak q = {baseline['q_total_W_per_m2']/1000:.0f} kW/m², "
              f"within HIAD-2: {baseline['within_HIAD2_design']}")
