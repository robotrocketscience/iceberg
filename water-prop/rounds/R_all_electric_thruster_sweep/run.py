"""R-all-electric-thruster-sweep — re-run R10b's thruster sweep at continuous-thrust
delta-velocities from R-electric-outbound and R-inbound-dv-continuous-thrust, under
both R10b's optimistic-canonical efficiencies and wonder-pass measured-realistic
efficiencies.

The architecture:
    round-trip = t_outbound_burn + t_hohmann + saturn_dwell + t_hohmann + t_inbound_burn

Outbound delta-velocity: 17.97 km/s continuous (R-electric-outbound mid-case)
Inbound delta-velocity:  27.56 km/s continuous (R-inbound high-elliptical with LGA)
Hohmann one-way:          6.09 yr (ballistic)
Saturn dwell:             1.00 yr
Round-trip ceiling:      15.00 yr per level-zero requirement L0-05.

Pre-registration: see STUDY.md (H-aets-a through H-aets-g).
"""

from __future__ import annotations

import json
import math
from pathlib import Path


G0 = 9.80665                # standard gravity, m/s^2
YEAR_S = 365.25 * 86400.0


# Trajectory constants
T_HOHMANN_ONE_WAY_YR = 6.09
SATURN_DWELL_YR = 1.00
ROUND_TRIP_CEILING_YR = 15.0

# Delta-velocity cases
DV_OUTBOUND_IMPULSIVE_KM_S = 9.0
DV_OUTBOUND_CONTINUOUS_KM_S = 17.97

DV_INBOUND_IMPULSIVE_KM_S = 6.42
DV_INBOUND_CONTINUOUS_KM_S = 27.56     # high-elliptical Saturn-departure with lunar gravity assist credit

# Tug dry mass at each reactor power (from R-electric-outbound decomposed-mid)
TUG_DRY_T_BY_KWE = {
    100.0: 5.5,
    200.0: 7.5,
    500.0: 10.0,
    1000.0: 12.1,
    2000.0: 16.4,
}

# Thruster definitions: (canonical_isp, canonical_eta, realistic_isp, realistic_eta)
# Canonical values are R10b's. Realistic values are the wonder-pass measured envelope.
THRUSTERS = [
    {
        "name": "water_microwave_electrothermal",
        "canonical_isp_s": 700.0,
        "canonical_eta": 0.30,
        "realistic_isp_s": 520.0,    # R0 flight-realistic, mid-band
        "realistic_eta": 0.20,
    },
    {
        "name": "water_Hall",
        "canonical_isp_s": 1500.0,
        "canonical_eta": 0.55,
        "realistic_isp_s": 1500.0,
        "realistic_eta": 0.125,       # Tsikata et al. 2023 anode efficiency
    },
    {
        "name": "water_radio_frequency_ion",
        "canonical_isp_s": 2000.0,
        "canonical_eta": 0.65,
        "realistic_isp_s": 2000.0,
        "realistic_eta": 0.30,        # ion-class on water is mid-bracket; Pale Blue heritage
    },
    {
        "name": "water_dual_ion",
        "canonical_isp_s": 5000.0,
        "canonical_eta": 0.55,
        "realistic_isp_s": 5000.0,
        "realistic_eta": 0.25,
    },
]

REACTOR_POWERS_KWE = [100.0, 200.0, 500.0, 1000.0, 2000.0]
CHUNK_MASSES_T = [50.0, 100.0, 200.0, 500.0]


def constant_thrust_burn(m_initial_t: float, dv_km_s: float, power_kwe: float,
                          isp_s: float, eta: float) -> dict:
    """Tsiolkovsky propellant; constant-thrust burn-time.

    Thrust = 2·eta·P / v_exhaust. Burn time = m_prop · v_exhaust / Thrust.
    """
    v_e = isp_s * G0                                       # m/s
    thrust_n = 2.0 * eta * power_kwe * 1000.0 / v_e        # N
    mass_ratio = math.exp(dv_km_s * 1000.0 / v_e)
    m_prop_t = m_initial_t * (1.0 - 1.0 / mass_ratio)
    if thrust_n <= 0.0:
        return {"thrust_N": 0.0, "m_prop_t": float("inf"), "mass_ratio": mass_ratio,
                "t_burn_yr": float("inf")}
    t_burn_s = m_prop_t * 1000.0 * v_e / thrust_n
    return {
        "thrust_N": thrust_n,
        "m_prop_t": m_prop_t,
        "mass_ratio": mass_ratio,
        "t_burn_yr": t_burn_s / YEAR_S,
    }


def round_trip(power_kwe: float, isp_s: float, eta: float, chunk_t: float,
                dv_out_km_s: float, dv_in_km_s: float) -> dict:
    """Compute one cell's round-trip timeline.

    Outbound: tug + outbound_propellant + chunk-not-yet-grappled-but-counted-as-launched-mass.
    Conops convention: vehicle launches with outbound propellant; no chunk on outbound.
    So outbound initial mass = tug_dry + m_prop_outbound.

    Inbound: tug + chunk grappled at Saturn. Initial mass = tug_dry + chunk.
    Propellant draws from chunk; delivered chunk = chunk - m_prop_inbound.

    Outbound propellant is also a function of outbound delta-velocity, but the outbound
    initial mass equals (tug_dry + m_prop_out), and m_prop_out solves Tsiolkovsky
    backwards from the requirement that mass-after-burn = tug_dry. We use the closed-form:
        m_prop_out = tug_dry · (mass_ratio_out - 1).
    """
    tug_dry_t = TUG_DRY_T_BY_KWE[power_kwe]
    v_e = isp_s * G0

    # Outbound: solve backwards.
    mass_ratio_out = math.exp(dv_out_km_s * 1000.0 / v_e)
    m_prop_out_t = tug_dry_t * (mass_ratio_out - 1.0)
    m_initial_out_t = tug_dry_t + m_prop_out_t
    # Outbound burn time at the average mass (use initial-mass approx for consistency
    # with R-inbound; minor over-estimate at high mass ratios).
    thrust_n = 2.0 * eta * power_kwe * 1000.0 / v_e
    if thrust_n <= 0:
        return {"feasible": False, "reason": "zero thrust"}
    t_burn_out_yr = m_prop_out_t * 1000.0 * v_e / thrust_n / YEAR_S

    # Inbound: vehicle starts with tug_dry + chunk_t at Saturn after Saturn dwell.
    inbound = constant_thrust_burn(tug_dry_t + chunk_t, dv_in_km_s, power_kwe, isp_s, eta)
    m_prop_in_t = inbound["m_prop_t"]
    delivered_t = chunk_t - m_prop_in_t
    delivered_frac = max(0.0, delivered_t) / chunk_t if chunk_t > 0 else 0.0
    feasible_inbound = delivered_t > 0.0

    round_trip_yr = (
        t_burn_out_yr + T_HOHMANN_ONE_WAY_YR + SATURN_DWELL_YR
        + T_HOHMANN_ONE_WAY_YR + inbound["t_burn_yr"]
    )

    return {
        "feasible": feasible_inbound and round_trip_yr <= ROUND_TRIP_CEILING_YR,
        "feasible_mass_only": feasible_inbound,
        "tug_dry_t": tug_dry_t,
        "m_prop_outbound_t": m_prop_out_t,
        "m_initial_outbound_t": m_initial_out_t,
        "t_burn_outbound_yr": t_burn_out_yr,
        "mass_ratio_inbound": inbound["mass_ratio"],
        "m_prop_inbound_t": m_prop_in_t,
        "delivered_t": delivered_t,
        "delivered_frac": delivered_frac,
        "t_burn_inbound_yr": inbound["t_burn_yr"],
        "round_trip_yr": round_trip_yr,
        "closes_15yr": round_trip_yr <= ROUND_TRIP_CEILING_YR,
    }


def main(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    results = []
    summary = {"cells_total": 0, "cells_closing": 0}

    # All combinations: thruster × eta regime × power × chunk × delta-velocity regime.
    dv_regimes = [
        {
            "name": "continuous_thrust_both_legs",
            "dv_outbound": DV_OUTBOUND_CONTINUOUS_KM_S,
            "dv_inbound": DV_INBOUND_CONTINUOUS_KM_S,
        },
        {
            "name": "matrix_impulsive_both_legs",
            "dv_outbound": DV_OUTBOUND_IMPULSIVE_KM_S,
            "dv_inbound": DV_INBOUND_IMPULSIVE_KM_S,
        },
    ]
    eta_regimes = ["canonical", "realistic"]

    for thruster in THRUSTERS:
        for eta_regime in eta_regimes:
            isp_s = thruster[f"{eta_regime}_isp_s"]
            eta = thruster[f"{eta_regime}_eta"]
            for power_kwe in REACTOR_POWERS_KWE:
                for chunk_t in CHUNK_MASSES_T:
                    for dv_r in dv_regimes:
                        cell = round_trip(
                            power_kwe=power_kwe,
                            isp_s=isp_s,
                            eta=eta,
                            chunk_t=chunk_t,
                            dv_out_km_s=dv_r["dv_outbound"],
                            dv_in_km_s=dv_r["dv_inbound"],
                        )
                        cell.update({
                            "thruster": thruster["name"],
                            "eta_regime": eta_regime,
                            "isp_s": isp_s,
                            "eta": eta,
                            "power_kwe": power_kwe,
                            "chunk_t": chunk_t,
                            "dv_regime": dv_r["name"],
                            "dv_outbound_km_s": dv_r["dv_outbound"],
                            "dv_inbound_km_s": dv_r["dv_inbound"],
                        })
                        results.append(cell)
                        summary["cells_total"] += 1
                        if cell.get("closes_15yr") and cell.get("feasible_mass_only"):
                            summary["cells_closing"] += 1

    # Write JSON
    (out_dir / "thruster_sweep.json").write_text(json.dumps({
        "summary": summary,
        "results": results,
    }, indent=2))

    # Write a tables.md with the key cells
    lines = []
    lines.append("# R-all-electric-thruster-sweep — tables\n")
    lines.append(f"\nTotal cells: {summary['cells_total']}. Cells closing 15-year ceiling and feasible: {summary['cells_closing']}.\n\n")
    lines.append("## Cells that close 15-year (feasible delivered fraction > 0)\n\n")
    lines.append("| Thruster | Eta regime | Power (kWe) | Chunk (t) | DV regime | Delivered (t) | Delivered % | Round-trip (yr) |\n")
    lines.append("|---|---|---:|---:|---|---:|---:|---:|\n")
    for r in results:
        if r.get("closes_15yr") and r.get("feasible_mass_only"):
            lines.append(
                f"| {r['thruster']} | {r['eta_regime']} | {int(r['power_kwe'])} | "
                f"{int(r['chunk_t'])} | {r['dv_regime']} | {r['delivered_t']:.1f} | "
                f"{r['delivered_frac']*100:.1f}% | {r['round_trip_yr']:.2f} |\n"
            )

    lines.append("\n## H-aets headline cells (chunk 200 t, high-elliptical continuous-thrust DV regime)\n\n")
    lines.append("| Thruster | Eta regime | Power (kWe) | Mass ratio in | Delivered (t) | Delivered % | t_burn_in (yr) | Round-trip (yr) | Closes? |\n")
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|:--:|\n")
    for r in results:
        if (r["chunk_t"] == 200.0 and r["dv_regime"] == "continuous_thrust_both_legs"):
            closes = "yes" if r.get("closes_15yr") else "no"
            mr = r.get("mass_ratio_inbound", float("nan"))
            lines.append(
                f"| {r['thruster']} | {r['eta_regime']} | {int(r['power_kwe'])} | "
                f"{mr:.2f} | {r['delivered_t']:.1f} | {r['delivered_frac']*100:.1f}% | "
                f"{r['t_burn_inbound_yr']:.2f} | {r['round_trip_yr']:.2f} | {closes} |\n"
            )

    lines.append("\n## Variant B cross-check (chunk 200 t, matrix-impulsive DV regime, canonical eta)\n\n")
    lines.append("| Thruster | Power (kWe) | Delivered (t) | Delivered % | Round-trip (yr) | Closes? |\n")
    lines.append("|---|---:|---:|---:|---:|:--:|\n")
    for r in results:
        if (r["chunk_t"] == 200.0 and r["dv_regime"] == "matrix_impulsive_both_legs"
                and r["eta_regime"] == "canonical"):
            closes = "yes" if r.get("closes_15yr") else "no"
            lines.append(
                f"| {r['thruster']} | {int(r['power_kwe'])} | "
                f"{r['delivered_t']:.1f} | {r['delivered_frac']*100:.1f}% | "
                f"{r['round_trip_yr']:.2f} | {closes} |\n"
            )

    (out_dir / "tables.md").write_text("".join(lines))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main(Path(__file__).parent / "results")
