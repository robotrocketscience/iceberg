"""B-ring fine-structure rendezvous viability and residence-class architecture.

Five sweeps mapping to pre-registered H1–H5 in STUDY.md.

Outputs:
  results/bring_tau_profile.csv      — H1, H3: literature B-ring τ(r) catalogue
  results/cassini_division_sub.csv   — H2: Cassini Division gap/ringlet τ values
  results/impact_prob_by_zone.csv    — H3: impact probability with size-binned τ
  results/residence_accretion.csv    — H4: residence-class accretion rate model
  results/residence_dv_budget.csv    — H5: residence-class propulsive cost
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

GM_SATURN = 37931207.7    # km^3 / s^2
R_SATURN  = 60268.0       # km
R_TITAN   = 1208547.0     # km

# B-ring + Cassini Division literature τ profile
# Source synthesis: Colwell et al. 2009 (Saturn book ch 13); Hedman et al. 2007
# AJ "Sat ring partition"; Esposito et al. 2008 Icarus; Cuzzi et al. 2010 Icarus.
# Format: (r_km, τ_typical, description)

BRING_TAU_PROFILE = [
    # B-ring inner edge and B1 region
    (92000.0,  0.30, "B-ring inner edge"),
    (94000.0,  0.80, "B1 inner"),
    (96000.0,  1.50, "B1 outer / B2 transition"),
    (99000.0,  1.80, "B2 inner"),
    (101000.0, 2.20, "B2 central"),
    (103000.0, 2.50, "B2 outer / B3 transition"),
    (104500.0, 3.00, "B3 inner (densest region begins)"),
    (107000.0, 4.50, "B3 core — densest part of B-ring"),
    (110000.0, 3.50, "B3 outer / B4 transition"),
    (113000.0, 2.20, "B4 central"),
    (115000.0, 1.50, "B4 outer / B5 transition"),
    (116500.0, 0.80, "B5 — B-ring outer region"),
    (117000.0, 0.40, "B-ring outer 580 km"),
    (117400.0, 0.10, "B-ring outermost ~180 km"),
    (117580.0, 0.03, "B-ring nominal outer edge"),
    # Cassini Division
    (117680.0, 0.001, "Huygens Gap (just inside CD inner)"),  # 285 km wide, τ < 0.001
    (117800.0, 0.001, "Huygens Gap centre"),
    (117900.0, 0.30,  "Huygens Ringlet (within Huygens Gap)"),
    (118000.0, 0.001, "Huygens Gap, post-ringlet"),
    (118250.0, 0.05,  "Outer Huygens Gap shoulder"),
    (118400.0, 0.08,  "CD inner background"),
    (118900.0, 0.10,  "CD plateau region"),
    (119900.0, 0.05,  "CD low-density 'lane' (Triple Band)"),
    (120000.0, 0.04,  "CD outer plateau"),
    (120800.0, 0.08,  "Outer CD"),
    (121850.0, 0.001, "Laplace Gap (near outer CD)"),  # narrow gap
    (122050.0, 0.40,  "Laplace Ringlet"),
    (122170.0, 0.40,  "Cassini Division outer edge / A-ring inner"),
]

# Particle size distribution: differential N(D) ~ D^(-q) over D_min to D_max
SIZE_DIST_Q     = 3.0   # power-law slope (Cuzzi 2010 B-ring)
SIZE_DIST_DMIN  = 0.001  # m  (1 mm) — extends below Whipple cutoff so shieldable fraction is meaningful
SIZE_DIST_DMAX  = 10.0  # m  (10 m)

# Whipple-shieldable particle size at hypervelocity (8 km/s):
WHIPPLE_CUTOFF_M = 0.01  # 1 cm; particles larger than this cause structural damage

# B-ring vertical scale height (Colwell 2009)
H_BRING_M = 10.0  # m

# B-ring particle bulk density (icy)
RHO_PARTICLE = 700.0  # kg / m^3 (water ice with porosity)


# -----------------------------------------------------------------------------
# Physics
# -----------------------------------------------------------------------------

def impact_prob_per_crossing(tau: float, inclination_deg: float) -> float:
    i_rad = np.radians(max(0.5, inclination_deg))
    return float(min(1.0, 1.0 - np.exp(-tau / np.sin(i_rad))))


def size_dist_normalization(tau_total: float, q: float = SIZE_DIST_Q,
                            d_min: float = SIZE_DIST_DMIN, d_max: float = SIZE_DIST_DMAX) -> float:
    """Find the normalization N0 of dN/dD = N0 · D^(-q) such that the integrated
    geometric cross-section column matches τ_total.

    τ_total = ∫ N(D) · π D²/4 dD  with N(D) summed column density of particles per m^2
    """
    # ∫ D^(-q) · π D²/4 dD from d_min to d_max = π/4 · ∫ D^(2-q) dD
    # For q = 3: ∫ D^(-1) dD = ln(D_max/D_min)
    if abs(q - 3.0) < 1e-6:
        integral = np.log(d_max / d_min)
    else:
        integral = (d_max ** (3 - q) - d_min ** (3 - q)) / (3 - q)
    return tau_total / (np.pi / 4 * integral)


def tau_above_cutoff(tau_total: float, d_cutoff: float, q: float = SIZE_DIST_Q,
                     d_min: float = SIZE_DIST_DMIN, d_max: float = SIZE_DIST_DMAX) -> float:
    """Fraction of τ contributed by particles of size > d_cutoff (unshieldable).

    Returns absolute τ_unshieldable = τ_total · (fraction).
    """
    if abs(q - 3.0) < 1e-6:
        full_int = np.log(d_max / d_min)
        cut_int = np.log(d_max / max(d_cutoff, d_min))
    else:
        full_int = (d_max ** (3 - q) - d_min ** (3 - q)) / (3 - q)
        cut_int = (d_max ** (3 - q) - max(d_cutoff, d_min) ** (3 - q)) / (3 - q)
    return tau_total * (cut_int / full_int)


def mean_particle_mass_kg(q: float = SIZE_DIST_Q, d_min: float = SIZE_DIST_DMIN,
                          d_max: float = SIZE_DIST_DMAX) -> float:
    """Mass-weighted (cross-section-weighted) mean particle mass.

    The encounter-rate weighting is by N(D) · v · A_sc, which is proportional
    to N(D). The mass per encounter is m(D) = (4/3) π (D/2)^3 · ρ. So the mean
    mass per encounter weighted by N(D):
        ⟨m⟩_encounter = ∫ m(D) · N(D) dD / ∫ N(D) dD
                     = (ρ π / 6) ∫ D^3 · D^(-q) dD / ∫ D^(-q) dD
                     = (ρ π / 6) · ∫ D^(3-q) dD / ∫ D^(-q) dD
    """
    if abs(q - 3.0) < 1e-6:
        num = (d_max ** 1 - d_min ** 1) / 1.0   # ∫ D^0 dD
    else:
        num = (d_max ** (4 - q) - d_min ** (4 - q)) / (4 - q)
    den = (d_max ** (1 - q) - d_min ** (1 - q)) / (1 - q)
    return (RHO_PARTICLE * np.pi / 6.0) * (num / den)


def encounter_rate_per_m2(tau_local: float, v_rel_ms: float) -> dict:
    """Encounter rate per m^2 of bag opening in residence mode at v_rel."""
    # 3D particle number density: N_V = τ / (h · ⟨σ⟩) where σ = π D²/4
    # ⟨σ⟩ for cross-section-weighted is just τ / (h · column density of particles)
    # Equivalent: number per m^2 of ring plane = τ / ⟨σ_per_particle⟩.
    # But we want number per m^3 of ring volume.
    # ⟨σ⟩ in units of m² per particle, averaged over distribution:
    if abs(SIZE_DIST_Q - 3.0) < 1e-6:
        # ⟨σ⟩ = ∫ D^(-q) σ(D) dD / ∫ D^(-q) dD; with σ=πD²/4 and q=3:
        # ⟨σ⟩ = π/4 · ln(d_max/d_min) / [(d_min^-2 - d_max^-2)/2]
        sig_top = (np.pi / 4) * np.log(SIZE_DIST_DMAX / SIZE_DIST_DMIN)
        sig_bot = (SIZE_DIST_DMIN ** -2 - SIZE_DIST_DMAX ** -2) / 2.0
        sig_avg = sig_top / sig_bot
    else:
        sig_top = (np.pi / 4) * (SIZE_DIST_DMAX ** (3 - SIZE_DIST_Q) - SIZE_DIST_DMIN ** (3 - SIZE_DIST_Q)) / (3 - SIZE_DIST_Q)
        sig_bot = (SIZE_DIST_DMAX ** (1 - SIZE_DIST_Q) - SIZE_DIST_DMIN ** (1 - SIZE_DIST_Q)) / (1 - SIZE_DIST_Q)
        sig_avg = sig_top / sig_bot
    # column number density of particles per m² of ring plane:
    N_col_per_m2 = tau_local / sig_avg
    # volume number density per m³:
    N_vol = N_col_per_m2 / H_BRING_M
    # encounter rate per m² of bag = N_vol · v_rel  (particles per s per m²)
    rate_per_m2 = N_vol * v_rel_ms
    # mass per encounter:
    m_per_enc = mean_particle_mass_kg()
    # mass accretion rate per m² of bag opening:
    mdot_per_m2 = rate_per_m2 * m_per_enc
    return {
        "tau_local": tau_local,
        "v_rel_ms": v_rel_ms,
        "sigma_avg_m2_per_particle": float(sig_avg),
        "N_col_per_m2": float(N_col_per_m2),
        "N_vol_per_m3": float(N_vol),
        "rate_per_m2_per_s": float(rate_per_m2),
        "m_per_encounter_kg": float(m_per_enc),
        "mdot_per_m2_kg_per_s": float(mdot_per_m2),
    }


def residence_class_dv(r_a_initial_km: float, r_p_initial_km: float,
                       r_target_km: float = 100000.0) -> dict:
    """Δv to circularise at r_target from a (r_p_initial, r_a_initial) ellipse.

    Two-burn Hohmann-style approach: (1) drop apoapsis to r_target via burn at
    r_p, (2) drop periapsis up to r_target at r_target. Total Δv = sum.

    For ICEBERG post-Titan-tour, the standard state is r_p ≈ 92,000 km (B-ring
    outer) and r_a ≈ r_titan. Circularising at r_target = 100,000 km (B-ring
    operations) requires raising periapsis from 92,000 to 100,000 km AND
    lowering apoapsis from r_titan to 100,000 km — a generalised maneuver.
    """
    # Current orbit
    a1 = 0.5 * (r_p_initial_km + r_a_initial_km)
    v_p1 = float(np.sqrt(GM_SATURN * (2 / r_p_initial_km - 1 / a1)))
    v_a1 = float(np.sqrt(GM_SATURN * (2 / r_a_initial_km - 1 / a1)))

    # Transfer orbit from r_p_initial to r_target
    a_t = 0.5 * (r_p_initial_km + r_target_km)
    v_p_t = float(np.sqrt(GM_SATURN * (2 / r_p_initial_km - 1 / a_t)))
    v_t_at_target = float(np.sqrt(GM_SATURN * (2 / r_target_km - 1 / a_t)))

    # Circular target orbit
    v_target_circ = float(np.sqrt(GM_SATURN / r_target_km))

    burn1 = abs(v_p_t - v_p1)         # at original periapsis, brake to transfer
    burn2 = abs(v_target_circ - v_t_at_target)  # at r_target, circularise

    return {
        "r_a_initial_km": r_a_initial_km,
        "r_p_initial_km": r_p_initial_km,
        "r_target_km": r_target_km,
        "v_p_initial_kms": v_p1,
        "v_p_after_burn1_kms": v_p_t,
        "v_at_target_pre_kms": v_t_at_target,
        "v_circular_target_kms": v_target_circ,
        "burn1_kms": burn1,
        "burn2_kms": burn2,
        "total_dv_in_kms": burn1 + burn2,
        # exit dv: reverse the sequence
        "total_dv_round_trip_kms": 2 * (burn1 + burn2),
    }


# -----------------------------------------------------------------------------
# Sweep drivers
# -----------------------------------------------------------------------------

def write_bring_tau_profile(out_dir: Path) -> None:
    """H1, H3 — literature B-ring + CD τ profile."""
    rows = []
    for r_km, tau, desc in BRING_TAU_PROFILE:
        rows.append({
            "r_km": r_km,
            "tau": tau,
            "description": desc,
            "p_impact_inc_26p7deg": impact_prob_per_crossing(tau, 26.7),
            "tau_unshieldable_above_1cm": tau_above_cutoff(tau, WHIPPLE_CUTOFF_M),
            "p_impact_unshieldable_inc_26p7deg": impact_prob_per_crossing(
                tau_above_cutoff(tau, WHIPPLE_CUTOFF_M), 26.7
            ),
        })
    write_csv(out_dir / "bring_tau_profile.csv", rows)

    fig, axes = plt.subplots(2, 1, figsize=(11, 7), sharex=True)
    # τ panel
    rs = [r["r_km"] for r in rows]
    taus = [r["tau"] for r in rows]
    axes[0].semilogy(rs, taus, marker="o", color="tab:blue")
    axes[0].axhline(0.01, ls="--", color="tab:green", alpha=0.7, label="H1 target τ = 0.01")
    axes[0].axhline(1.0, ls="--", color="tab:red", alpha=0.7, label="τ = 1 (optically thick)")
    axes[0].set_ylabel("vertical optical depth τ")
    axes[0].set_title("H1/H3 — B-ring + Cassini Division τ(r) from Cassini occultations")
    axes[0].legend(); axes[0].grid(alpha=0.3, which="both")

    # impact-probability panel
    pimps = [r["p_impact_inc_26p7deg"] for r in rows]
    pimps_us = [r["p_impact_unshieldable_inc_26p7deg"] for r in rows]
    axes[1].semilogy(rs, pimps, marker="o", color="tab:red", label="total impact (incl. shieldable)")
    axes[1].semilogy(rs, pimps_us, marker="s", color="tab:orange", label="unshieldable impact (D > 1 cm)")
    axes[1].axhline(0.01, ls="--", color="tab:green", alpha=0.5, label="1% threshold")
    axes[1].set_xlabel("radius from Saturn [km]")
    axes[1].set_ylabel("P(impact) per crossing at i = 26.7°")
    axes[1].legend(); axes[1].grid(alpha=0.3, which="both")
    axes[1].axvspan(92000, 117580, color="tab:blue", alpha=0.1, label="B-ring")
    axes[1].axvspan(117580, 122170, color="tab:green", alpha=0.1, label="Cassini Division")
    fig.tight_layout()
    fig.savefig(out_dir / "bring_tau_profile.png", dpi=130)
    plt.close(fig)


def write_cassini_division_focus(out_dir: Path) -> None:
    """H2 — Focus on Cassini Division gaps and ringlets."""
    rows = [r for r in BRING_TAU_PROFILE if 117500 <= r[0] <= 122200]
    out = []
    for r_km, tau, desc in rows:
        out.append({
            "r_km": r_km,
            "tau": tau,
            "description": desc,
            "p_impact_inc_26p7deg": impact_prob_per_crossing(tau, 26.7),
            "p_impact_unshieldable": impact_prob_per_crossing(
                tau_above_cutoff(tau, WHIPPLE_CUTOFF_M), 26.7
            ),
            "viable_for_rendezvous (P_imp < 0.01)": impact_prob_per_crossing(tau, 26.7) < 0.01,
        })
    write_csv(out_dir / "cassini_division_sub.csv", out)


def write_residence_accretion(out_dir: Path) -> None:
    """H4 — residence-class accretion rate vs τ and v_rel."""
    rows = []
    # Sweep across representative B-ring radii / τ values and relative velocities.
    sample_locations = [
        ("B2 central (τ=2.2)",         2.2,  100000.0),
        ("B3 core (τ=4.5)",            4.5,  107000.0),
        ("B5 outer (τ=0.8)",           0.8,  116500.0),
        ("B-ring outer 200 km (τ=0.1)", 0.1, 117400.0),
        ("Huygens Gap (τ=0.001)",      0.001, 117800.0),
    ]
    v_rel_sweep = [1.0, 5.0, 10.0, 30.0, 100.0]  # m/s
    for name, tau, r in sample_locations:
        for v_rel in v_rel_sweep:
            res = encounter_rate_per_m2(tau, v_rel)
            v_orbit_local_ms = float(np.sqrt(GM_SATURN / r)) * 1000.0  # m/s
            # Convert per-m² rates to a 100-m² bag-opening
            rows.append({
                "location": name,
                "r_km": r,
                "v_orbit_local_ms": v_orbit_local_ms,
                "tau": tau,
                "v_rel_ms": v_rel,
                "rate_per_m2_per_s": res["rate_per_m2_per_s"],
                "rate_per_100m2_per_s": res["rate_per_m2_per_s"] * 100,
                "m_per_encounter_kg": res["m_per_encounter_kg"],
                "mdot_per_100m2_kg_per_s": res["mdot_per_m2_kg_per_s"] * 100,
                "time_to_fill_482t_hours_at_100m2": (
                    482000.0 / (res["mdot_per_m2_kg_per_s"] * 100) / 3600.0
                    if res["mdot_per_m2_kg_per_s"] > 0 else float("inf")
                ),
                "ke_per_encounter_j_per_kg": 0.5 * v_rel ** 2,
            })
    write_csv(out_dir / "residence_accretion.csv", rows)


def write_residence_dv_budget(out_dir: Path) -> None:
    """H5 — Δv to enter and exit B-ring residence orbit."""
    rows = []
    # Three initial-state cases (post-Titan-tour):
    initial_states = [
        ("Post-Titan-tour (r_p=92000, r_a=r_titan)", 92000.0,  R_TITAN),
        ("Post-Titan-tour (r_p=92000, r_a=2 r_titan)", 92000.0, 2 * R_TITAN),
        ("Direct-chemical capture (r_p=92000, r_a=r_titan)", 92000.0, R_TITAN),
    ]
    target_radii = [95000.0, 100000.0, 105000.0, 110000.0]  # B-ring radii
    for state_name, rp, ra in initial_states:
        for r_target in target_radii:
            d = residence_class_dv(ra, rp, r_target)
            d["case"] = state_name
            rows.append(d)
    write_csv(out_dir / "residence_dv_budget.csv", rows)


# -----------------------------------------------------------------------------
# IO
# -----------------------------------------------------------------------------

def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    ordered = list(rows[0].keys())
    for r in rows:
        for k in r.keys():
            if k not in ordered:
                ordered.append(k)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=ordered)
        w.writeheader()
        for row in rows:
            w.writerow(row)


def main() -> int:
    out_dir = Path(__file__).parent / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    print("[H1, H3] B-ring τ profile + impact-prob ..."); write_bring_tau_profile(out_dir)
    print("[H2] Cassini Division focus ..."); write_cassini_division_focus(out_dir)
    print("[H4] Residence-class accretion ..."); write_residence_accretion(out_dir)
    print("[H5] Residence-class Δv budget ..."); write_residence_dv_budget(out_dir)
    print("\nDone. Outputs in", out_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
