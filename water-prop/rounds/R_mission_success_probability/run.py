"""R-mission-success-probability — deterministic reliability analysis.

Three computations, all deterministic, no random seeds:

1. Empirical per-mission success rate across the heritage dataset of deep-space
   missions with design cruise-plus-operate duration >= 10 years.
2. Serial-reliability sweep: required per-subsystem reliability R to clear
   L0-10's 0.90 target across critical-path subsystem counts N = 4..12.
3. Projected ICEBERG single-string mission success at per-subsystem heritage
   reliability, and redundancy budget required to lift it to 0.90.

Outputs:
    results/heritage.json
    results/serial_reliability.json
    results/redundancy_budget.json
    results/tables.md

Usage:
    python run.py
"""

import json
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Literal


# ------------------------------- 1. heritage ------------------------------- #


Outcome = Literal["success", "partial", "lost", "operating"]


@dataclass
class HeritageMission:
    name: str
    launch_year: int
    design_duration_years: float
    actual_duration_years: float | None  # None if still operating
    outcome: Outcome
    primary_objectives_fraction: float  # analyst call, vs. L0-10's 0.5 threshold
    note: str
    citation: str


HERITAGE: list[HeritageMission] = [
    # Outer-planet flybys / orbiters
    HeritageMission(
        "Voyager 1", 1977, 12.0, None, "operating", 1.0,
        "All four giant-planet flyby objectives met. Still returning interstellar data 49 yr in.",
        "NASA JPL Voyager mission status page; Stone et al. 2013",
    ),
    HeritageMission(
        "Voyager 2", 1977, 12.0, None, "operating", 1.0,
        "All giant-planet flybys met (Jupiter, Saturn, Uranus, Neptune). Operating.",
        "NASA JPL Voyager mission status page",
    ),
    HeritageMission(
        "Pioneer 10", 1972, 21.0, 31.0, "success", 1.0,
        "Jupiter flyby objectives met. Signal lost 2003 at ~80 AU. Long-duration baseline.",
        "NASA Ames Pioneer page",
    ),
    HeritageMission(
        "Pioneer 11", 1973, 21.0, 22.0, "success", 1.0,
        "Jupiter + Saturn flybys met. RTG decayed below telemetry threshold 1995.",
        "NASA Ames Pioneer page",
    ),
    HeritageMission(
        "Galileo", 1989, 8.0, 14.0, "success", 0.70,
        "High-gain antenna failed to deploy 1991; mission proceeded via low-gain. ~70 % of "
        "design data return. Above L0-10's 0.5 threshold but a textbook borderline case.",
        "Johnson 1994 (Galileo HGA anomaly); JPL final report 2003",
    ),
    HeritageMission(
        "Cassini", 1997, 11.0, 19.7, "success", 1.0,
        "Saturn orbit insertion and all extended-mission objectives met. Several thruster "
        "and reaction-wheel degradations through life, none mission-killing.",
        "NASA JPL Cassini mission overview; Spilker 2019",
    ),
    HeritageMission(
        "Juno", 2011, 7.0, None, "operating", 1.0,
        "Jupiter orbital science returned; main-engine valve anomaly forced longer-period orbit "
        "but did not block primary objectives.",
        "Bolton et al. 2017",
    ),
    HeritageMission(
        "New Horizons", 2006, 10.0, None, "operating", 1.0,
        "Pluto + Arrokoth flybys met. Operating in extended mission.",
        "Stern et al. 2015; NASA APL NH page",
    ),
    HeritageMission(
        "Dawn", 2007, 9.0, 11.4, "success", 1.0,
        "Vesta + Ceres orbital science met. Lost two reaction wheels in cruise; reassigned "
        "ion-thruster gimbal for attitude control. Mission preserved.",
        "Rayman et al. 2007; mission-end NASA release 2018",
    ),
    HeritageMission(
        "Rosetta", 2004, 10.0, 12.5, "success", 1.0,
        "Comet 67P rendezvous + Philae lander deployment met. Philae landing partial "
        "(bounced, ended up in shadow) but Rosetta orbital science = full success.",
        "Glassmeier et al. 2007; ESA mission-end report 2016",
    ),
    HeritageMission(
        "Stardust", 1999, 7.0, 12.0, "success", 1.0,
        "Wild-2 comet sample return met. Sample successfully recovered at Earth.",
        "Brownlee et al. 2006; NASA mission overview",
    ),
    HeritageMission(
        "Genesis", 2001, 3.0, 3.5, "partial", 0.30,
        "Solar-wind sample return; parachute failed on Earth re-entry. Sample recovered but "
        "contaminated and partially fragmented; science return ~30 % of design.",
        "Burnett et al. 2003; mishap report NASA-TM-2006",
    ),
    HeritageMission(
        "Hayabusa", 2003, 4.0, 7.0, "partial", 0.10,
        "Itokawa sample return; multiple ion-engine + reaction-wheel failures, sample "
        "container returned with ~1500 micron-scale grains. Science return well below "
        "0.5x design; counts as 'partial', not 'lost'.",
        "Yano et al. 2006; JAXA mission report",
    ),
    HeritageMission(
        "Hayabusa2", 2014, 6.0, 6.5, "success", 1.0,
        "Ryugu sample return met. Sample recovered intact 2020.",
        "Watanabe et al. 2019; JAXA mission overview",
    ),
    HeritageMission(
        "OSIRIS-REx", 2016, 7.0, 7.2, "success", 1.0,
        "Bennu sample return met 2023. ~250 g recovered, design target 60 g.",
        "Lauretta et al. 2017; NASA SRC 2023",
    ),
    # Inner-planet orbiters with long cruise
    HeritageMission(
        "Magellan", 1989, 4.0, 4.5, "success", 1.0,
        "Venus radar mapping met. Aerobrake demonstration also met.",
        "Saunders et al. 1992",
    ),
    HeritageMission(
        "Mars Global Surveyor", 1996, 5.0, 10.0, "success", 1.0,
        "Mars mapping met. Extended-mission anomaly 2006 (battery / attitude error) ended life "
        "but after primary objectives + 5 years of extension.",
        "Albee et al. 2001; mishap report 2007",
    ),
    HeritageMission(
        "Mars Reconnaissance Orbiter", 2005, 5.0, None, "operating", 1.0,
        "Mars high-res imaging and relay met. Still operating 21 yr.",
        "Zurek & Smrekar 2007",
    ),
    HeritageMission(
        "Akatsuki", 2010, 4.0, 16.0, "success", 0.80,
        "Venus orbit insertion failed first attempt 2010; second attempt 2015 succeeded with "
        "reduced orbit (highly elliptical vs designed). Most science objectives recovered, "
        "some lost. Operating.",
        "Nakamura et al. 2016",
    ),
    # Lost-before-arrival missions (designed for >= 10 yr cruise+operate, did not fly that long)
    HeritageMission(
        "Mars Observer", 1992, 2.0, 0.9, "lost", 0.0,
        "Lost just before Mars orbit insertion (fuel line rupture suspected). Design "
        "duration not as long as outer-planet population but was the design analog at the time.",
        "Coffey 1993",
    ),
    HeritageMission(
        "Mars Climate Orbiter", 1999, 2.0, 0.8, "lost", 0.0,
        "Lost on orbit insertion (unit conversion error). Pre-flight failure mode, not cruise.",
        "Stephenson 1999",
    ),
    HeritageMission(
        "Mars Polar Lander", 1999, 0.5, 0.8, "lost", 0.0,
        "Lost on EDL (premature thrust shutdown). Short design duration; arguably outside our "
        "10-year-design filter, but included as a heritage data point for completeness.",
        "Casani 2000 (MPL failure review)",
    ),
    HeritageMission(
        "Phobos-Grunt", 2011, 3.0, 0.05, "lost", 0.0,
        "Failed to leave low Earth orbit (upper-stage controller hang). Pre-cruise failure.",
        "Russian state commission 2012",
    ),
]


def heritage_rates() -> dict:
    """Compute empirical success rates under several definitions."""
    n = len(HERITAGE)

    # L0-10 literal: success = primary_objectives_fraction >= 0.5
    l0_10 = sum(1 for m in HERITAGE if m.primary_objectives_fraction >= 0.5)

    # Strict: success = primary_objectives_fraction >= 0.9 (more like sci-class)
    strict = sum(1 for m in HERITAGE if m.primary_objectives_fraction >= 0.9)

    # Survival to operations: outcome in ('success','partial','operating')
    survived = sum(1 for m in HERITAGE if m.outcome in ("success", "partial", "operating"))

    # Restricted to >=10-year design duration (the closest analog to ICEBERG cruise+operate)
    long_pop = [m for m in HERITAGE if m.design_duration_years >= 10.0]
    long_l0_10 = sum(1 for m in long_pop if m.primary_objectives_fraction >= 0.5)

    # Restricted to outer-planet (the closest dynamical analog: Saturn cruise + operate)
    outer_planet_names = {
        "Voyager 1", "Voyager 2", "Pioneer 10", "Pioneer 11",
        "Galileo", "Cassini", "Juno", "New Horizons",
    }
    outer = [m for m in HERITAGE if m.name in outer_planet_names]
    outer_l0_10 = sum(1 for m in outer if m.primary_objectives_fraction >= 0.5)

    return {
        "n_missions_total": n,
        "rate_L0_10_definition_all": l0_10 / n,
        "n_L0_10_successes_all": l0_10,
        "rate_strict_definition_all": strict / n,
        "n_long_design_subset": len(long_pop),
        "rate_L0_10_long_design_subset": long_l0_10 / len(long_pop),
        "n_outer_planet_subset": len(outer),
        "rate_L0_10_outer_planet_subset": outer_l0_10 / len(outer),
        "n_survival_to_operations": survived,
        "rate_survival_all": survived / n,
    }


# ----------------------- 2. serial reliability sweep ----------------------- #


def serial_reliability_sweep() -> dict:
    """For N critical-path subsystems and a target mission success P_target,
    compute required per-subsystem reliability R = P_target^(1/N)."""
    targets = [0.70, 0.75, 0.80, 0.85, 0.90, 0.95]
    n_range = list(range(4, 13))  # 4..12 subsystems

    out: dict = {"targets": targets, "n_subsystems": n_range, "required_R": {}}
    for t in targets:
        row = {}
        for n in n_range:
            row[str(n)] = t ** (1.0 / n)
        out["required_R"][f"{t:.2f}"] = row

    # Inverse: at heritage R per subsystem, projected mission success vs N
    heritage_R_values = [0.93, 0.95, 0.97, 0.99]
    proj = {"heritage_R_values": heritage_R_values, "projected_success": {}}
    for r in heritage_R_values:
        row = {}
        for n in n_range:
            row[str(n)] = r ** n
        proj["projected_success"][f"{r:.2f}"] = row

    out["projected_at_heritage"] = proj
    return out


# -------------------- 3. redundancy budget calculation -------------------- #


@dataclass
class SubsystemReliability:
    name: str
    R_single: float  # single-string reliability over 14 yr
    heritage: Literal["AVAILABLE", "ADJACENT", "NONE"]
    note: str


# Per-subsystem reliability calibrated from heritage as discussed in STUDY.md.
# Each R is best-paper-estimate; uncertainty notes are inline.
ICEBERG_SUBSYSTEMS: list[SubsystemReliability] = [
    SubsystemReliability(
        "reactor_power", 0.95, "NONE",
        "Kilopower / fission surface power has NO flight heritage. SNAP-10A "
        "(1965) partial-failed after 43 days. 0.95 is a placeholder lift from "
        "RTG heritage (which is excellent: Voyager / Cassini / NH all >0.99 "
        "over 10-30 yr); active fission is meaningfully harder.",
    ),
    SubsystemReliability(
        "primary_propulsion", 0.90, "ADJACENT",
        "Deep-space ion-thruster heritage from Dawn (3 thrusters, 1 grid wear "
        "failure, system survived) and Hayabusa (4 thrusters, multiple "
        "anomalies, mission limped). 0.90 per system. Water-MET is HERITAGE-NONE "
        "and likely lower without redundancy.",
    ),
    SubsystemReliability(
        "rcs", 0.97, "AVAILABLE",
        "Standard monoprop or cold-gas RCS heritage is high. Cassini, Juno, etc.",
    ),
    SubsystemReliability(
        "gnc_compute", 0.95, "AVAILABLE",
        "Flight-computer + IMU + star-tracker chain. Reaction-wheel anomalies "
        "are common (Kepler, Hayabusa, MRO, Dawn) and bring the chain reliability "
        "below the individual-component spec.",
    ),
    SubsystemReliability(
        "comms", 0.93, "AVAILABLE",
        "HGA + radio + DSN. Galileo HGA failure is the canonical degradation "
        "(brought Galileo mass-return to ~0.70 not 1.0). Voyager 49 yr operating "
        "is the upper-bound demonstration.",
    ),
    SubsystemReliability(
        "bag_harvest", 0.85, "NONE",
        "No flight heritage for ring-mining bag at this scale. AstroMesh-class "
        "deployable structures have >0.98 heritage but at radio-frequency mesh "
        "apertures, not 1 m apertures. Bag-engineering doc treats this as the "
        "highest-risk subsystem; 0.85 is the analyst's paper estimate.",
    ),
    SubsystemReliability(
        "thermal_control", 0.95, "ADJACENT",
        "Cruise spacecraft thermal heritage is high (~0.99 per loop). Megawatt-"
        "class radiator stack with two-phase ammonia loop is heritage-adjacent "
        "(ISS) but never run in cruise for 14 yr. 0.95 is the paper estimate.",
    ),
    SubsystemReliability(
        "return_handoff", 0.95, "AVAILABLE",
        "Sample-return / customer-interface heritage from Stardust, OSIRIS-REx, "
        "Hayabusa2. 0.95 is the heritage average; ICEBERG hand-off is propellant "
        "transfer, which is technically harder than passive sample release.",
    ),
]


def single_string_projection() -> dict:
    """Naive serial product over the 8 critical-path subsystems."""
    prod = 1.0
    for s in ICEBERG_SUBSYSTEMS:
        prod *= s.R_single
    return {
        "n_subsystems": len(ICEBERG_SUBSYSTEMS),
        "subsystems": [asdict(s) for s in ICEBERG_SUBSYSTEMS],
        "single_string_mission_success": prod,
    }


def redundancy_budget(target: float = 0.90) -> dict:
    """Sweep: which subsystems, ranked by R_single ascending, must be 2-of-3'd
    to lift mission success from single-string to >= target?

    Assumption: 2-of-3 redundancy on a subsystem with single-string R lifts
    that subsystem to 1 - (1-R)^2 (treating the two-of-three as "any one of two
    surviving copies"). This is the standard parallel-redundancy formula and is
    conservative versus true 2-of-3 voting (which is slightly worse than parallel)."""
    sorted_subs = sorted(ICEBERG_SUBSYSTEMS, key=lambda s: s.R_single)
    R_list = [s.R_single for s in sorted_subs]

    history = []
    n_redundant = 0
    while True:
        prod = 1.0
        for r in R_list:
            prod *= r
        history.append({
            "n_redundant_subsystems": n_redundant,
            "redundancy_applied_to": [s.name for s in sorted_subs[:n_redundant]],
            "projected_mission_success": prod,
        })
        if prod >= target:
            break
        if n_redundant >= len(R_list):
            break
        # Apply parallel redundancy to the next weakest subsystem
        weakest_idx = n_redundant
        r_weak = R_list[weakest_idx]
        R_list[weakest_idx] = 1.0 - (1.0 - r_weak) ** 2
        n_redundant += 1

    return {
        "target": target,
        "history": history,
        "n_redundancies_needed": history[-1]["n_redundant_subsystems"],
        "final_success": history[-1]["projected_mission_success"],
    }


# ------------------------- L0-09 cross-check ------------------------- #


def l0_09_check() -> dict:
    """Read L0-09 literally: (months in which at least one delivery is made)/12 >= 0.95.
    At launch cadence c per year and per-mission success p:
    expected deliveries per month = c*p/12.
    P(month has at least one delivery, Poisson) = 1 - exp(-c*p/12)."""
    import math
    cases = []
    for c_per_yr in [1, 2, 4, 12]:
        for p in [0.70, 0.80, 0.90, 1.00]:
            month_rate = c_per_yr * p / 12.0
            p_month_has_delivery = 1.0 - math.exp(-month_rate)
            cases.append({
                "launch_cadence_per_yr": c_per_yr,
                "per_mission_p": p,
                "P_month_has_delivery": p_month_has_delivery,
                "satisfies_L0_09_literal_0p95": p_month_has_delivery >= 0.95,
            })
    return {"cases": cases}


# -------------------------------- driver --------------------------------- #


def main():
    here = Path(__file__).parent
    out = here / "results"
    out.mkdir(exist_ok=True)

    h = heritage_rates()
    s = serial_reliability_sweep()
    ss = single_string_projection()
    rb = redundancy_budget(target=0.90)
    rb_080 = redundancy_budget(target=0.80)
    rb_075 = redundancy_budget(target=0.75)
    l9 = l0_09_check()

    (out / "heritage.json").write_text(json.dumps(h, indent=2))
    (out / "serial_reliability.json").write_text(json.dumps(s, indent=2))
    (out / "redundancy_budget.json").write_text(json.dumps(
        {"target_0p90": rb, "target_0p80": rb_080, "target_0p75": rb_075},
        indent=2,
    ))
    (out / "single_string.json").write_text(json.dumps(ss, indent=2))
    (out / "l0_09_check.json").write_text(json.dumps(l9, indent=2))

    # Markdown table summary
    md = [
        "# R-mission-success-probability — results tables",
        "",
        "## Heritage empirical rates",
        "",
        f"- Total missions in dataset: {h['n_missions_total']}",
        f"- L0-10 definition (delivered >= 0.5 x design) across all: **{h['rate_L0_10_definition_all']:.3f}** ({h['n_L0_10_successes_all']}/{h['n_missions_total']})",
        f"- Strict definition (>= 0.9 x design) across all: **{h['rate_strict_definition_all']:.3f}**",
        f"- L0-10 definition, long-design (>= 10 yr) subset: **{h['rate_L0_10_long_design_subset']:.3f}** ({h['n_long_design_subset']} missions)",
        f"- L0-10 definition, outer-planet subset: **{h['rate_L0_10_outer_planet_subset']:.3f}** ({h['n_outer_planet_subset']} missions)",
        f"- Spacecraft survival to operations: **{h['rate_survival_all']:.3f}**",
        "",
        "## Required per-subsystem R to clear target mission success",
        "",
        "Rows = mission-success target. Columns = number of critical-path subsystems N in series.",
        "Required R = target^(1/N).",
        "",
        "| Target \\ N | 4 | 6 | 8 | 10 | 12 |",
        "|---|---|---|---|---|---|",
    ]
    for t_str, row in s["required_R"].items():
        md.append(
            f"| {t_str} | {row['4']:.4f} | {row['6']:.4f} | {row['8']:.4f} | "
            f"{row['10']:.4f} | {row['12']:.4f} |"
        )

    md += [
        "",
        "## Projected mission success at heritage per-subsystem R",
        "",
        "Rows = per-subsystem R. Columns = N. Projected mission success = R^N.",
        "",
        "| R \\ N | 4 | 6 | 8 | 10 | 12 |",
        "|---|---|---|---|---|---|",
    ]
    for r_str, row in s["projected_at_heritage"]["projected_success"].items():
        md.append(
            f"| {r_str} | {row['4']:.4f} | {row['6']:.4f} | {row['8']:.4f} | "
            f"{row['10']:.4f} | {row['12']:.4f} |"
        )

    md += [
        "",
        "## ICEBERG single-string projection (8 critical-path subsystems)",
        "",
        f"Serial product of paper-estimate per-subsystem R: **{ss['single_string_mission_success']:.4f}**",
        "",
        "| Subsystem | R_single | Heritage |",
        "|---|---|---|",
    ]
    for sub in ss["subsystems"]:
        md.append(f"| {sub['name']} | {sub['R_single']:.3f} | {sub['heritage']} |")

    md += [
        "",
        "## Redundancy budget to clear targets",
        "",
        "Apply 2-of-3 parallel redundancy to the weakest single-string subsystem; repeat until target is cleared.",
        "(Parallel redundancy lifts subsystem R from R to 1 - (1-R)^2.)",
        "",
        "### Target = 0.90 (L0-10 as written)",
        "",
        "| Step | Redundancy applied to | Projected mission success |",
        "|---|---|---|",
    ]
    for step in rb["history"]:
        applied = ", ".join(step["redundancy_applied_to"]) or "(none — single-string)"
        md.append(f"| {step['n_redundant_subsystems']} | {applied} | {step['projected_mission_success']:.4f} |")
    md.append(f"")
    md.append(f"**Result:** {rb['n_redundancies_needed']} subsystems need 2-of-3 redundancy to clear 0.90.")
    md.append(f"")

    md += [
        "### Target = 0.80 (relaxed)",
        "",
        "| Step | Redundancy applied to | Projected mission success |",
        "|---|---|---|",
    ]
    for step in rb_080["history"]:
        applied = ", ".join(step["redundancy_applied_to"]) or "(none — single-string)"
        md.append(f"| {step['n_redundant_subsystems']} | {applied} | {step['projected_mission_success']:.4f} |")
    md.append(f"")
    md.append(f"**Result:** {rb_080['n_redundancies_needed']} subsystems need 2-of-3 redundancy to clear 0.80.")
    md.append(f"")

    md += [
        "### Target = 0.75 (relaxed further)",
        "",
        "| Step | Redundancy applied to | Projected mission success |",
        "|---|---|---|",
    ]
    for step in rb_075["history"]:
        applied = ", ".join(step["redundancy_applied_to"]) or "(none — single-string)"
        md.append(f"| {step['n_redundant_subsystems']} | {applied} | {step['projected_mission_success']:.4f} |")
    md.append(f"")
    md.append(f"**Result:** {rb_075['n_redundancies_needed']} subsystems need 2-of-3 redundancy to clear 0.75.")

    md += [
        "",
        "## L0-09 literal-text feasibility check",
        "",
        "P(month has >=1 delivery | launch_cadence_per_yr c, per-mission p) = 1 - exp(-c*p/12).",
        "L0-09 literal: this must be >= 0.95.",
        "",
        "| Cadence per yr | Per-mission p | P(month has delivery) | Clears L0-09 0.95? |",
        "|---|---|---|---|",
    ]
    for case in l9["cases"]:
        md.append(
            f"| {case['launch_cadence_per_yr']} | {case['per_mission_p']:.2f} | "
            f"{case['P_month_has_delivery']:.4f} | "
            f"{'yes' if case['satisfies_L0_09_literal_0p95'] else 'no'} |"
        )

    (out / "tables.md").write_text("\n".join(md))
    print((out / "tables.md").read_text())


if __name__ == "__main__":
    main()
