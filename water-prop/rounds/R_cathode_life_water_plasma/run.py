"""R-cathode-life-water-plasma — does the all-electric end-to-end architecture have a
cathode-life closure problem, and if so, at what fraction of xenon-heritage life does
the architecture die?

Budget round (not a sweep). Compares per-mission and multi-mission cathode-on time at
the surviving year-twenty-plus winner cell against (a) xenon-heritage cathode envelope,
(b) three water-plasma life anchors (optimistic = xenon heritage; mid = half; pessimistic
= Wang et al. 2025 work-function-degradation-derived).

Pre-registration: see STUDY.md (H-clwp-a through H-clwp-h).
"""

from __future__ import annotations

import json
from pathlib import Path


YEAR_HR = 365.25 * 24.0    # 8766 hour per year

# Per-mission burn times at the year-twenty-plus winner cell
# (water-radio-frequency-ion, 1 megawatt-electric, specific impulse 2000 s, chunk 200 t,
#  continuous-thrust delta-velocities from R-electric-outbound + R-inbound).
# Outbound: from R-electric-outbound decomposed-mid at 1000 kWe = 0.17 yr
# Inbound:  from R-all-electric-thruster-sweep canonical RFI 1000 kWe chunk 200 t = 1.50 yr
PER_MISSION_BURN_CANONICAL_YR = {
    "outbound": 0.17,
    "inbound": 1.50,
}

# Realistic-efficiency burn times. Efficiency 0.65 → 0.30 = 2.17× longer burn at fixed power.
EFFICIENCY_CANONICAL = 0.65
EFFICIENCY_REALISTIC = 0.30
EFF_RATIO = EFFICIENCY_CANONICAL / EFFICIENCY_REALISTIC

PER_MISSION_BURN_REALISTIC_YR = {
    leg: t * EFF_RATIO for leg, t in PER_MISSION_BURN_CANONICAL_YR.items()
}

# Heritage cathode life envelope (xenon)
HERITAGE = {
    "NSTAR_wear_test_demonstrated_hr": 30352,
    "NSTAR_design_life_hr": 28000,
    "AEPS_qualification_wear_test_hr": 23000,
    "AEPS_design_life_hr": 50000,
    "LaB6_Polk_Goebel_half_mass_life_hr": 3.5e7,
}

# Water-plasma life anchors (three brackets)
WATER_PLASMA_LIFE_HR = {
    "optimistic_matches_xenon_heritage": 50000,
    "mid_case_half_of_xenon": 25000,
    "pessimistic_Wang_2025_work_function": 3000,    # midpoint of 1,000–5,000 hr band
}

# Mission-count sweep
MISSION_COUNTS = [1, 5, 10, 20]


def per_mission_cathode_on_hr(regime: str) -> float:
    """Sum outbound + inbound burn in hours for the given efficiency regime."""
    if regime == "canonical":
        burns = PER_MISSION_BURN_CANONICAL_YR
    elif regime == "realistic":
        burns = PER_MISSION_BURN_REALISTIC_YR
    else:
        raise ValueError(regime)
    return (burns["outbound"] + burns["inbound"]) * YEAR_HR


def variant_b_per_mission_cathode_on_hr() -> float:
    """Variant B per-mission cathode-on time.

    Variant B uses chemical kick at Earth departure and chemical capture at Saturn arrival;
    electric is only for the small residual maneuvers and the spiral phase of the inbound
    after lunar gravity assist. Approximate: outbound electric burn ~0 (chemical handles it);
    inbound electric burn ~0.4 yr (small residual delta-velocity 6.42 km/s at megawatt, RFI
    canonical eta, from R-all-electric-thruster-sweep matrix-impulsive row showing 13.80 yr
    round-trip and ~0.4 yr inbound burn).
    """
    # Read directly from R-all-electric-thruster-sweep result: chunk 200 t, RFI canonical
    # 1000 kWe, matrix-impulsive: round-trip 13.80 yr. Decomposition:
    #   t_out_burn + 6.09 (Hohmann out) + 1 (Saturn) + 6.09 (Hohmann in) + t_in_burn = 13.80
    #   so t_out_burn + t_in_burn = 0.62 yr.
    # Under Variant B, the outbound is impulsive chemical (cathode-off for the chemical kick).
    # The "electric on outbound" is zero for Variant B if we treat chemical as the only
    # outbound impulse. The 0.62 yr is then all-inbound, including the post-lunar-flyby
    # residual electric burn.
    return 0.62 * YEAR_HR


def main(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    results = []

    for regime in ("canonical", "realistic"):
        per_mission_hr = per_mission_cathode_on_hr(regime)
        for n_missions in MISSION_COUNTS:
            total_hr = per_mission_hr * n_missions
            row = {
                "regime": regime,
                "n_missions": n_missions,
                "per_mission_hr": per_mission_hr,
                "per_mission_yr": per_mission_hr / YEAR_HR,
                "total_hr": total_hr,
                "total_yr": total_hr / YEAR_HR,
                "fraction_NSTAR_design": total_hr / HERITAGE["NSTAR_design_life_hr"],
                "fraction_AEPS_design": total_hr / HERITAGE["AEPS_design_life_hr"],
                "verdict_optimistic": "closes" if total_hr <= WATER_PLASMA_LIFE_HR["optimistic_matches_xenon_heritage"] else "exceeds",
                "verdict_midcase": "closes" if total_hr <= WATER_PLASMA_LIFE_HR["mid_case_half_of_xenon"] else "exceeds",
                "verdict_pessimistic": "closes" if total_hr <= WATER_PLASMA_LIFE_HR["pessimistic_Wang_2025_work_function"] else "exceeds",
            }
            results.append(row)

    variant_b_per_mission_hr = variant_b_per_mission_cathode_on_hr()
    variant_b_rows = []
    for n_missions in MISSION_COUNTS:
        total_hr = variant_b_per_mission_hr * n_missions
        variant_b_rows.append({
            "n_missions": n_missions,
            "per_mission_hr": variant_b_per_mission_hr,
            "per_mission_yr": variant_b_per_mission_hr / YEAR_HR,
            "total_hr": total_hr,
            "total_yr": total_hr / YEAR_HR,
            "fraction_NSTAR_design": total_hr / HERITAGE["NSTAR_design_life_hr"],
            "fraction_AEPS_design": total_hr / HERITAGE["AEPS_design_life_hr"],
            "verdict_optimistic": "closes" if total_hr <= WATER_PLASMA_LIFE_HR["optimistic_matches_xenon_heritage"] else "exceeds",
            "verdict_midcase": "closes" if total_hr <= WATER_PLASMA_LIFE_HR["mid_case_half_of_xenon"] else "exceeds",
            "verdict_pessimistic": "closes" if total_hr <= WATER_PLASMA_LIFE_HR["pessimistic_Wang_2025_work_function"] else "exceeds",
        })

    out = {
        "heritage": HERITAGE,
        "water_plasma_life_anchors_hr": WATER_PLASMA_LIFE_HR,
        "all_electric_end_to_end": results,
        "variant_b": variant_b_rows,
    }
    (out_dir / "cathode_life.json").write_text(json.dumps(out, indent=2))

    # Write tables.md
    lines = []
    lines.append("# R-cathode-life-water-plasma — tables\n\n")

    lines.append("## Heritage cathode-life envelope (xenon)\n\n")
    lines.append("| Anchor | Hour | Year |\n|---|---:|---:|\n")
    for k, v in HERITAGE.items():
        lines.append(f"| {k} | {v:,.0f} | {v/YEAR_HR:.2f} |\n")

    lines.append("\n## Water-plasma cathode-life anchors (bracket)\n\n")
    lines.append("| Anchor | Hour | Year |\n|---|---:|---:|\n")
    for k, v in WATER_PLASMA_LIFE_HR.items():
        lines.append(f"| {k} | {v:,.0f} | {v/YEAR_HR:.2f} |\n")

    lines.append("\n## All-electric end-to-end architecture (water-radio-frequency-ion, 1 MWe, chunk 200 t)\n\n")
    lines.append("| Efficiency regime | N missions | Per-mission (hr) | Total (hr) | Total (yr) | Fraction of NSTAR | Fraction of AEPS | Optimistic | Mid-case | Pessimistic |\n")
    lines.append("|---|---:|---:|---:|---:|---:|---:|:--:|:--:|:--:|\n")
    for r in results:
        lines.append(
            f"| {r['regime']} | {r['n_missions']} | {r['per_mission_hr']:,.0f} | "
            f"{r['total_hr']:,.0f} | {r['total_yr']:.2f} | "
            f"{r['fraction_NSTAR_design']:.2f}x | {r['fraction_AEPS_design']:.2f}x | "
            f"{r['verdict_optimistic']} | {r['verdict_midcase']} | {r['verdict_pessimistic']} |\n"
        )

    lines.append("\n## Variant B (year-zero-through-fifteen, chemical-kick + electric inbound)\n\n")
    lines.append("| N missions | Per-mission (hr) | Total (hr) | Total (yr) | Fraction of NSTAR | Fraction of AEPS | Optimistic | Mid-case | Pessimistic |\n")
    lines.append("|---:|---:|---:|---:|---:|---:|:--:|:--:|:--:|\n")
    for r in variant_b_rows:
        lines.append(
            f"| {r['n_missions']} | {r['per_mission_hr']:,.0f} | "
            f"{r['total_hr']:,.0f} | {r['total_yr']:.2f} | "
            f"{r['fraction_NSTAR_design']:.2f}x | {r['fraction_AEPS_design']:.2f}x | "
            f"{r['verdict_optimistic']} | {r['verdict_midcase']} | {r['verdict_pessimistic']} |\n"
        )

    (out_dir / "tables.md").write_text("".join(lines))

    # Print summary
    summary = {
        "all_electric_canonical_single_mission_hr": results[0]["per_mission_hr"],
        "all_electric_canonical_10_mission_total_hr": next(
            r["total_hr"] for r in results if r["regime"] == "canonical" and r["n_missions"] == 10
        ),
        "all_electric_realistic_single_mission_hr": next(
            r["per_mission_hr"] for r in results if r["regime"] == "realistic" and r["n_missions"] == 1
        ),
        "all_electric_realistic_10_mission_total_hr": next(
            r["total_hr"] for r in results if r["regime"] == "realistic" and r["n_missions"] == 10
        ),
        "variant_b_10_mission_total_hr": next(
            r["total_hr"] for r in variant_b_rows if r["n_missions"] == 10
        ),
        "AEPS_design_life_hr": HERITAGE["AEPS_design_life_hr"],
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main(Path(__file__).parent / "results")
