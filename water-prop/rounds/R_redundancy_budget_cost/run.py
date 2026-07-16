"""R-redundancy-budget-cost — mass + round-trip + cost overlay of L0-10 redundancy.

For each of the two architecture-decision-matrix cells (Kilopower variant B at
10 kWe, and megawatt all-electric at 1 MWe decomposed-mid), compute:

1. Per-subsystem redundancy mass overlay using engineering-form-of-redundancy
   table from STUDY.md.
2. Round-trip time impact via R-electric-outbound's trajectory math (re-implemented
   locally to keep this round self-contained).
3. Per-vehicle cost overlay using qualified-replicate pricing (NOT first-flight $/kg).

Outputs:
    results/mass_overlay.json
    results/round_trip_impact.json
    results/cost_overlay.json
    results/tables.md

Deterministic; no random seeds; runtime < 1 s.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from dataclasses import dataclass, asdict


# ---------------- constants (matched to R_electric_outbound) ---------------- #

G0 = 9.81
GM_SUN = 1.32712440018e11  # km^3/s^2
GM_EARTH = 398600.4418     # km^3/s^2
R_EARTH = 6378.137         # km
A_EARTH = 149597870.7      # km (1 AU)
A_SATURN = 9.5826 * A_EARTH
YEAR_S = 365.25 * 86400.0
LEO_ALT_KM = 400.0
ETA_THR = 0.65
DV_INBOUND_KM_S = 6.42
SATURN_OPS_YR = 1.0


# ---------------- subsystem redundancy table ---------------- #

@dataclass
class RedundancyItem:
    name: str
    form_KP_B: str
    form_MWe: str
    mass_overlay_KP_B_t: float
    mass_overlay_MWe_t: float
    R_lift: tuple[float, float]  # (R_baseline, R_with_redundancy)
    cost_USD_M: tuple[float, float]  # (KP-B cost in $M, MWe cost in $M)


SUBSYSTEMS = [
    RedundancyItem(
        "reactor_power",
        "parallel: second 10-kWe Kilopower unit",
        "internal: dual coolant loops + dual power conditioning + derated operation",
        1.5, 6.0,
        (0.95, 0.978),  # parallel of 0.95+0.95 = 0.9975; internal lift ~0.97-0.98
        (300.0, 400.0),
    ),
    RedundancyItem(
        "primary_propulsion",
        "spare thruster + power-processing unit",
        "spare power-processing units; thruster redundancy structural",
        0.05, 0.3,
        (0.90, 0.99),
        (50.0, 30.0),
    ),
    RedundancyItem(
        "rcs",
        "second RCS branch (block redundancy)",
        "second RCS branch",
        0.2, 0.2,
        (0.97, 0.999),
        (15.0, 15.0),
    ),
    RedundancyItem(
        "gnc_compute",
        "dual flight-computer + dual IMU + dual star-tracker",
        "same",
        0.5, 0.5,
        (0.95, 0.998),
        (40.0, 40.0),
    ),
    RedundancyItem(
        "comms",
        "dual HGA + redundant transponders",
        "same",
        0.8, 0.8,
        (0.93, 0.995),
        (60.0, 60.0),
    ),
    RedundancyItem(
        "bag_harvest",
        "dual-aperture trawl bag",
        "dual-aperture at commercial-class scale",
        1.0, 2.0,
        (0.85, 0.978),
        (50.0, 80.0),
    ),
    RedundancyItem(
        "thermal_control",
        "redundant coolant loops + redundant heat-pipes",
        "same plus ammonia-loop redundancy",
        0.5, 1.5,
        (0.95, 0.9975),
        (30.0, 60.0),
    ),
    RedundancyItem(
        "return_handoff",
        "redundant valve trains + secondary docking adapter",
        "same",
        0.3, 0.3,
        (0.95, 0.9975),
        (20.0, 25.0),
    ),
]

INTEGRATION_TAX = 0.10


def mass_overlay() -> dict:
    sum_kp_b = sum(s.mass_overlay_KP_B_t for s in SUBSYSTEMS)
    sum_mwe = sum(s.mass_overlay_MWe_t for s in SUBSYSTEMS)
    overlay_kp_b = sum_kp_b * (1.0 + INTEGRATION_TAX)
    overlay_mwe = sum_mwe * (1.0 + INTEGRATION_TAX)
    return {
        "per_subsystem": [asdict(s) for s in SUBSYSTEMS],
        "sum_KP_B_t": sum_kp_b,
        "sum_MWe_t": sum_mwe,
        "integration_tax": INTEGRATION_TAX,
        "total_overlay_KP_B_t": overlay_kp_b,
        "total_overlay_MWe_t": overlay_mwe,
    }


# ---------------- trajectory math (lifted from R_electric_outbound) ---------------- #


def hohmann_cruise_yr() -> float:
    a_h_km = (A_EARTH + A_SATURN) / 2.0
    t_half_s = math.pi * math.sqrt(a_h_km ** 3 / GM_SUN)
    return t_half_s / YEAR_S


def outbound_dv_km_s() -> float:
    """All-electric outbound: Edelbaum LEO-to-escape + heliocentric to Hohmann perihelion."""
    r_leo = R_EARTH + LEO_ALT_KM
    v_circ_leo = math.sqrt(GM_EARTH / r_leo)
    v_earth = math.sqrt(GM_SUN / A_EARTH)
    a_h = (A_EARTH + A_SATURN) / 2.0
    v_peri = math.sqrt(GM_SUN * (2.0 / A_EARTH - 1.0 / a_h))
    v_inf = v_peri - v_earth
    return v_circ_leo + v_inf


def constant_thrust_burn(m_initial_t: float, dv_km_s: float,
                         power_kwe: float, isp_s: float) -> dict:
    """Constant-thrust burn under Tsiolkovsky; consistent with R_electric_outbound."""
    v_e = isp_s * G0
    thrust_N = 2.0 * ETA_THR * power_kwe * 1000.0 / v_e
    mass_ratio = math.exp(dv_km_s * 1000.0 / v_e)
    m_prop_t = m_initial_t * (1.0 - 1.0 / mass_ratio)
    t_burn_s = m_prop_t * 1000.0 * v_e / thrust_N
    return {"thrust_N": thrust_N, "m_prop_t": m_prop_t,
            "t_burn_s": t_burn_s, "t_burn_yr": t_burn_s / YEAR_S}


# ---------------- per-cell round-trip computation ---------------- #


@dataclass
class CellResult:
    cell: str
    reactor_kwe: float
    isp_s: float
    chunk_t: float
    m_dry_baseline_t: float
    m_dry_with_overlay_t: float
    outbound_burn_yr_baseline: float
    outbound_burn_yr_overlay: float
    inbound_burn_yr_baseline: float
    inbound_burn_yr_overlay: float
    cruise_yr: float
    saturn_ops_yr: float
    round_trip_baseline_yr: float
    round_trip_overlay_yr: float
    L0_05_margin_baseline_yr: float
    L0_05_margin_overlay_yr: float
    L0_05_clears_baseline: bool
    L0_05_clears_overlay: bool


def cell_round_trip(cell: str, reactor_kwe: float, isp_s: float, m_dry_baseline_t: float,
                    overlay_t: float, chunk_t: float, dv_outbound_km_s: float,
                    inbound_chunkfed: bool) -> CellResult:
    """Compute round-trip for one matrix cell, baseline and with redundancy overlay.

    inbound_chunkfed = True: Variant B convention. Outbound is chemical-kick
    (impulsive, treat as ~0.3 yr fixed for staging + post-escape coast). Inbound
    is 3 km/s chemical-kick from harvested water + 3.42 km/s electric residual.

    inbound_chunkfed = False: all-electric end-to-end. Outbound is the full
    Edelbaum + heliocentric continuous burn.
    """
    cruise_yr = hohmann_cruise_yr()
    CHEM_OUTBOUND_FIXED_YR = 0.3

    def round_trip(m_dry: float) -> dict:
        if inbound_chunkfed:
            # Variant B: chemical-kick outbound, treat as ~0.3 yr fixed
            t_outbound_yr = CHEM_OUTBOUND_FIXED_YR
            # Inbound = 3 km/s chemical-kick (chunk water) + 3.42 km/s electric
            m_initial_inbound = m_dry + chunk_t
            v_e_kick = 450.0 * G0
            m_after_kick = m_initial_inbound / math.exp(3000.0 / v_e_kick)
            burn_in_elec = constant_thrust_burn(m_after_kick, 3.42, reactor_kwe, isp_s)
            t_inbound_yr = burn_in_elec["t_burn_yr"]  # chemical kick burn time ~ days, ignored
        else:
            # All-electric outbound, no chunk
            burn_out = constant_thrust_burn(m_dry, dv_outbound_km_s, reactor_kwe, isp_s)
            t_outbound_yr = burn_out["t_burn_yr"]
            burn_in = constant_thrust_burn(m_dry + chunk_t, DV_INBOUND_KM_S, reactor_kwe, isp_s)
            t_inbound_yr = burn_in["t_burn_yr"]
        rt = t_outbound_yr + cruise_yr + SATURN_OPS_YR + t_inbound_yr + cruise_yr
        return {"out_yr": t_outbound_yr, "in_yr": t_inbound_yr, "rt_yr": rt}

    base = round_trip(m_dry_baseline_t)
    over = round_trip(m_dry_baseline_t + overlay_t)

    return CellResult(
        cell=cell,
        reactor_kwe=reactor_kwe,
        isp_s=isp_s,
        chunk_t=chunk_t,
        m_dry_baseline_t=m_dry_baseline_t,
        m_dry_with_overlay_t=m_dry_baseline_t + overlay_t,
        outbound_burn_yr_baseline=base["out_yr"],
        outbound_burn_yr_overlay=over["out_yr"],
        inbound_burn_yr_baseline=base["in_yr"],
        inbound_burn_yr_overlay=over["in_yr"],
        cruise_yr=cruise_yr,
        saturn_ops_yr=SATURN_OPS_YR,
        round_trip_baseline_yr=base["rt_yr"],
        round_trip_overlay_yr=over["rt_yr"],
        L0_05_margin_baseline_yr=15.0 - base["rt_yr"],
        L0_05_margin_overlay_yr=15.0 - over["rt_yr"],
        L0_05_clears_baseline=base["rt_yr"] <= 15.0,
        L0_05_clears_overlay=over["rt_yr"] <= 15.0,
    )


# ---------------- cost overlay ---------------- #


def cost_overlay() -> dict:
    kp_b = sum(s.cost_USD_M[0] for s in SUBSYSTEMS)
    mwe = sum(s.cost_USD_M[1] for s in SUBSYSTEMS)
    return {
        "per_subsystem": [
            {"name": s.name, "KP_B_USD_M": s.cost_USD_M[0],
             "MWe_USD_M": s.cost_USD_M[1]} for s in SUBSYSTEMS
        ],
        "total_KP_B_USD_M": kp_b,
        "total_MWe_USD_M": mwe,
    }


# ---------------- post-overlay mission-success projection ---------------- #


def mission_success_projection() -> dict:
    """Re-multiply the serial product using R_with_redundancy from the table."""
    prod_with = 1.0
    prod_without = 1.0
    for s in SUBSYSTEMS:
        prod_without *= s.R_lift[0]
        prod_with *= s.R_lift[1]
    return {
        "baseline_single_string": prod_without,
        "after_redundancy": prod_with,
        "clears_L0_10_0p90": prod_with >= 0.90,
    }


# ---------------- driver ---------------- #


def main():
    here = Path(__file__).parent
    out = here / "results"
    out.mkdir(exist_ok=True)

    mov = mass_overlay()
    cov = cost_overlay()
    msp = mission_success_projection()

    # Matrix-cell parameters
    # Kilopower variant B: 10 kWe, Variant B uses chunk-fed chemical inbound;
    # bundled-formula tug dry mass ~ 16 t (5 t tug + 1 t reactor stack at 10 W/kg + 10 t electrolyzer/chemical-stage).
    # Variant B isp_s for electric portion of inbound = 1500 s (Hall, per matrix).
    # All-electric outbound from low Earth orbit even for Variant B? Per matrix, outbound is also
    # chemical-kick for Variant B (single-stage with chemical to Earth-departure). For this
    # round, treat Variant B's outbound as already "subsumed" — round-trip baseline 14 yr per matrix.
    # We compute the *inbound* impact of the overlay only.
    dv_out = outbound_dv_km_s()

    kp_b = cell_round_trip(
        cell="Kilopower variant B (10 kWe, chunk-fed chemical inbound)",
        reactor_kwe=10.0, isp_s=1500.0,
        m_dry_baseline_t=16.0,  # matrix bundled-formula
        overlay_t=mov["total_overlay_KP_B_t"],
        chunk_t=100.0,           # matrix mid-cell chunk
        dv_outbound_km_s=dv_out, # not actually used for KP-B since outbound is chemical-kick;
                                  # but the function still computes electric outbound for comparison
        inbound_chunkfed=True,
    )

    mwe = cell_round_trip(
        cell="Megawatt all-electric (1 MWe, decomposed-mid)",
        reactor_kwe=1000.0, isp_s=2000.0,
        m_dry_baseline_t=29.0,  # R_radiator_mass_penalty decomposed-mid
        overlay_t=mov["total_overlay_MWe_t"],
        chunk_t=200.0,
        dv_outbound_km_s=dv_out,
        inbound_chunkfed=False,
    )

    (out / "mass_overlay.json").write_text(json.dumps(mov, indent=2))
    (out / "cost_overlay.json").write_text(json.dumps(cov, indent=2))
    (out / "round_trip_impact.json").write_text(json.dumps({
        "Kilopower_variant_B": asdict(kp_b),
        "megawatt_all_electric": asdict(mwe),
    }, indent=2))
    (out / "mission_success_projection.json").write_text(json.dumps(msp, indent=2))

    # Markdown summary table
    md = [
        "# R-redundancy-budget-cost — results tables",
        "",
        "## 1. Per-subsystem mass + cost overlay",
        "",
        "| Subsystem | Kilopower-B form | MWe form | Mass +Δt KP-B | Mass +Δt MWe | Cost $M KP-B | Cost $M MWe |",
        "|---|---|---|---|---|---|---|",
    ]
    for s in SUBSYSTEMS:
        md.append(
            f"| {s.name} | {s.form_KP_B} | {s.form_MWe} | {s.mass_overlay_KP_B_t:.2f} | "
            f"{s.mass_overlay_MWe_t:.2f} | {s.cost_USD_M[0]:.0f} | {s.cost_USD_M[1]:.0f} |"
        )
    md.append("")
    md.append(f"**Sum (no integration tax):** Kilopower-B = {mov['sum_KP_B_t']:.2f} t; megawatt = {mov['sum_MWe_t']:.2f} t.")
    md.append(f"**Total overlay with {int(INTEGRATION_TAX*100)} % integration tax:** Kilopower-B = **{mov['total_overlay_KP_B_t']:.2f} t**; megawatt = **{mov['total_overlay_MWe_t']:.2f} t**.")
    md.append(f"**Total cost overlay:** Kilopower-B = **${cov['total_KP_B_USD_M']:.0f}M**; megawatt = **${cov['total_MWe_USD_M']:.0f}M**.")
    md.append("")

    md += [
        "## 2. Round-trip impact at L0-05 ceiling (15 yr)",
        "",
        "Hohmann round-trip cruise = {:.2f} yr (each way).".format(hohmann_cruise_yr() * 2),
        "",
        "### Kilopower variant B (10 kWe, chunk-fed chemical inbound)",
        "",
        f"| Metric | Baseline | With redundancy overlay |",
        f"|---|---|---|",
        f"| Tug dry mass (tonne) | {kp_b.m_dry_baseline_t:.2f} | {kp_b.m_dry_with_overlay_t:.2f} |",
        f"| Outbound burn (yr) | {kp_b.outbound_burn_yr_baseline:.3f} | {kp_b.outbound_burn_yr_overlay:.3f} |",
        f"| Inbound burn (yr) | {kp_b.inbound_burn_yr_baseline:.3f} | {kp_b.inbound_burn_yr_overlay:.3f} |",
        f"| Round-trip (yr) | {kp_b.round_trip_baseline_yr:.3f} | {kp_b.round_trip_overlay_yr:.3f} |",
        f"| L0-05 margin (yr) | {kp_b.L0_05_margin_baseline_yr:.3f} | {kp_b.L0_05_margin_overlay_yr:.3f} |",
        f"| Clears L0-05? | {'yes' if kp_b.L0_05_clears_baseline else 'NO'} | {'yes' if kp_b.L0_05_clears_overlay else 'NO'} |",
        "",
        "*Note: for Variant B, the outbound burn in this table is the all-electric calculation for cross-comparison; matrix-baseline outbound is chemical-kick which is fast and not modelled here. The relevant overlay impact for Variant B is inbound burn time + chemical-stage propellant overhead.*",
        "",
        "### Megawatt all-electric (1 MWe decomposed-mid, all-electric inbound)",
        "",
        f"| Metric | Baseline | With redundancy overlay |",
        f"|---|---|---|",
        f"| Tug dry mass (tonne) | {mwe.m_dry_baseline_t:.2f} | {mwe.m_dry_with_overlay_t:.2f} |",
        f"| Outbound burn (yr) | {mwe.outbound_burn_yr_baseline:.3f} | {mwe.outbound_burn_yr_overlay:.3f} |",
        f"| Inbound burn (yr) | {mwe.inbound_burn_yr_baseline:.3f} | {mwe.inbound_burn_yr_overlay:.3f} |",
        f"| Round-trip (yr) | {mwe.round_trip_baseline_yr:.3f} | {mwe.round_trip_overlay_yr:.3f} |",
        f"| L0-05 margin (yr) | {mwe.L0_05_margin_baseline_yr:.3f} | {mwe.L0_05_margin_overlay_yr:.3f} |",
        f"| Clears L0-05? | {'yes' if mwe.L0_05_clears_baseline else 'NO'} | {'yes' if mwe.L0_05_clears_overlay else 'NO'} |",
        "",
        "## 3. Post-redundancy mission-success projection",
        "",
        f"Single-string baseline (from R-mission-success-probability): **{msp['baseline_single_string']:.4f}**",
        f"With per-subsystem R-lift from the table above (full redundancy on all 8): **{msp['after_redundancy']:.4f}**",
        f"Clears L0-10 ≥ 0.90? **{'yes' if msp['clears_L0_10_0p90'] else 'no'}**",
        "",
    ]

    (out / "tables.md").write_text("\n".join(md))
    print((out / "tables.md").read_text())


if __name__ == "__main__":
    main()
