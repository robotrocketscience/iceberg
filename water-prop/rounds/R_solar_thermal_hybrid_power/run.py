#!/usr/bin/env python3
"""
R-solar-thermal-hybrid-power — run.py

Answers the SCOPE's decision gate: does a hybrid reactor+solar architecture move
ICEBERG closure thresholds enough to justify the invasive location-aware-power
framework refactor? Focused model, NOT the full refactor (the refactor is the
decision this round informs).

Model: the inbound continuous-thrust delta-v is spent across heliocentric
distance bins (Saturn 9.5 AU -> Earth 1.0 AU). Solar power scales as 1/r^2.
For fixed delta-v + Isp, propellant is fixed by Tsiolkovsky and is INDEPENDENT
of power (F = 2P/v_e); more power buys shorter BURN TIME, not less propellant.
So the hybrid can only shorten round-trip / cumulative reactor-hours, and only
on the near-sun fraction of the inbound delta-v. It does nothing for the
mass-floor kill (static) that makes Saturn 0/150 closed-loop (titan-6).

Deterministic; stdlib only. Author: hyperion (re-spawn 2), 2026-05-26.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

ROUND = Path(__file__).parent
RESULTS = ROUND / "results"
RESULTS.mkdir(exist_ok=True)

G0 = 9.80665
ISP_S = 2000.0                 # RF-ion (bet-2 audit)
VE = ISP_S * G0                # exhaust velocity m/s
REACTOR_KWE = 10.0
SOLAR_LEO_KWE = 20.0           # at 1 AU
INBOUND_DV_KM_S = 27.56        # R-all-electric-thruster-sweep mid-case

# Inbound delta-v allocation by heliocentric distance bin (Saturn -> Earth).
# Nominal: bulk of the spiral delta-v is outer (Saturn departure + cruise),
# Earth-capture spiral is the near-sun minority. Generous-to-hybrid shifts
# more delta-v near-sun to bound the benefit.
BINS = ["Saturn_9.5AU", "Jupiter_5.2AU", "belt_2.7AU", "Mars_1.5AU", "Earth_1.0AU"]
DIST_AU = {"Saturn_9.5AU": 9.5, "Jupiter_5.2AU": 5.2, "belt_2.7AU": 2.7,
           "Mars_1.5AU": 1.5, "Earth_1.0AU": 1.0}
DV_ALLOC_NOMINAL = {"Saturn_9.5AU": 12.0, "Jupiter_5.2AU": 6.0, "belt_2.7AU": 4.0,
                    "Mars_1.5AU": 3.0, "Earth_1.0AU": 2.56}   # sums 27.56
DV_ALLOC_GENEROUS = {"Saturn_9.5AU": 6.0, "Jupiter_5.2AU": 4.0, "belt_2.7AU": 4.56,
                     "Mars_1.5AU": 6.0, "Earth_1.0AU": 7.0}   # sums 27.56, near-sun heavy


def solar_kwe(dist_au: float) -> float:
    return SOLAR_LEO_KWE / (dist_au ** 2)


def power_at(dist_au: float, hybrid: bool) -> float:
    return REACTOR_KWE + (solar_kwe(dist_au) if hybrid else 0.0)


def inbound_burn(dv_alloc: dict, hybrid: bool, dry_plus_payload_t: float = 60.0) -> dict:
    """Staged Tsiolkovsky inbound: from Earth-arrival mass back-propagated.

    We process bins Earth->Saturn for staging (propellant added going outward),
    but burn-time per bin uses the local power. Returns total burn time (yr),
    cumulative reactor-on hours, propellant fraction per bin, and burn time per bin.
    """
    # Work outward from the post-arrival dry+payload mass, accumulating propellant.
    m_end = dry_plus_payload_t * 1000.0  # kg at Earth arrival (dry + delivered payload)
    mass = m_end
    total_burn_s = 0.0
    per_bin = {}
    prop_total = 0.0
    # Process from Earth (innermost, last burned) outward to Saturn (first burned).
    for b in reversed(BINS):
        dv = dv_alloc[b] * 1000.0
        m_before = mass * math.exp(dv / VE)     # mass before this bin's burn (heavier)
        prop = m_before - mass
        prop_total += prop
        P = power_at(DIST_AU[b], hybrid) * 1000.0  # W
        burn_s = prop * VE / (2.0 * P / VE)        # = prop*VE^2/(2P)
        total_burn_s += burn_s
        per_bin[b] = {"dv_km_s": dv_alloc[b], "dist_au": DIST_AU[b],
                      "solar_kwe": round(solar_kwe(DIST_AU[b]), 2),
                      "power_kwe": round(power_at(DIST_AU[b], hybrid), 2),
                      "propellant_t": round(prop / 1000.0, 1),
                      "burn_time_yr": round(burn_s / (3600 * 24 * 365.25), 3)}
        mass = m_before
    # propellant fractions
    for b in per_bin:
        per_bin[b]["prop_fraction"] = round((per_bin[b]["propellant_t"] * 1000.0) / prop_total, 3)
    return {
        "total_burn_time_yr": total_burn_s / (3600 * 24 * 365.25),
        "cumulative_reactor_hours": total_burn_s / 3600.0,
        "total_propellant_t": round(prop_total / 1000.0, 1),
        "per_bin": per_bin,
    }


def main() -> None:
    out = {"round": "R-solar-thermal-hybrid-power", "author": "hyperion (re-spawn 2)",
           "date": "2026-05-26", "isp_s": ISP_S, "inbound_dv_km_s": INBOUND_DV_KM_S,
           "reactor_kwe": REACTOR_KWE, "solar_leo_kwe": SOLAR_LEO_KWE}

    # H1: solar contribution by bin
    out["H1_solar_share_by_bin"] = {
        b: {"dist_au": DIST_AU[b], "solar_kwe": round(solar_kwe(DIST_AU[b]), 2),
            "solar_share_of_hybrid_power": round(solar_kwe(DIST_AU[b]) / (REACTOR_KWE + solar_kwe(DIST_AU[b])), 3)}
        for b in BINS}

    results = {}
    for label, alloc in [("nominal", DV_ALLOC_NOMINAL), ("generous_to_hybrid", DV_ALLOC_GENEROUS)]:
        ro = inbound_burn(alloc, hybrid=False)
        hy = inbound_burn(alloc, hybrid=True)
        reduction = (ro["total_burn_time_yr"] - hy["total_burn_time_yr"]) / ro["total_burn_time_yr"]
        results[label] = {
            "reactor_only_burn_yr": round(ro["total_burn_time_yr"], 3),
            "hybrid_burn_yr": round(hy["total_burn_time_yr"], 3),
            "burn_time_reduction_pct": round(reduction * 100, 1),
            "reactor_only_reactor_hours": round(ro["cumulative_reactor_hours"], 0),
            "hybrid_reactor_hours": round(hy["cumulative_reactor_hours"], 0),
            "per_bin_hybrid": hy["per_bin"],
        }
    out["H2_burn_time_reduction"] = results

    # H3/H5 verdict synthesis
    nominal_red = results["nominal"]["burn_time_reduction_pct"]
    generous_red = results["generous_to_hybrid"]["burn_time_reduction_pct"]
    out["verdict"] = {
        "H1_solar_negligible_beyond_2AU": all(
            out["H1_solar_share_by_bin"][b]["solar_share_of_hybrid_power"] < 0.10
            for b in ["Saturn_9.5AU", "Jupiter_5.2AU", "belt_2.7AU"]),
        "H2_reduction_nominal_pct": nominal_red,
        "H2_reduction_generous_pct": generous_red,
        "H3_moves_closed_loop_closure": False,
        "H3_reason": ("Saturn closed-loop is 0/150 on the mass-floor + reactor-lifetime axes "
                      "(titan-6). Hybrid power shortens inbound BURN TIME only (propellant is "
                      "fixed by Tsiolkovsky, independent of power); it does not reduce vehicle "
                      "dry mass and so cannot relieve the mass-floor kill. The burn-time / "
                      "reactor-hours benefit is bounded and helps round-trip + lifetime margin, "
                      "not the binding mass constraint."),
        "H5_invasive_refactor_justified_for_closure": False,
        "H5_recommendation": ("A local power(r) function in the inbound burn-time accounting "
                              "captures the dial-up effect for round-trip/reactor-hours fidelity "
                              "and conops. The full VehicleState two-field split + per-executor "
                              "recompute + new sweep axes is NOT justified by the closure verdict "
                              "under the closed-loop framework."),
    }
    (RESULTS / "hybrid_power_summary.json").write_text(json.dumps(out, indent=2, default=str))

    # console
    print("=" * 74)
    print("R-solar-thermal-hybrid-power — does hybrid move closure? (closed-loop)")
    print("=" * 74)
    print(f"\nIsp {ISP_S:.0f} s, inbound dv {INBOUND_DV_KM_S} km/s, reactor {REACTOR_KWE} kWe + solar {SOLAR_LEO_KWE} kWe(1AU)")
    print("\nH1 solar share of hybrid power by bin:")
    for b in BINS:
        d = out["H1_solar_share_by_bin"][b]
        print(f"  {b:<16} {d['dist_au']:>4} AU  solar {d['solar_kwe']:>6.2f} kW  "
              f"share {d['solar_share_of_hybrid_power']*100:>5.1f}%")
    print("\nH2 inbound burn-time reduction (hybrid vs reactor-only):")
    for label in ("nominal", "generous_to_hybrid"):
        r = results[label]
        print(f"  {label:<18}: {r['reactor_only_burn_yr']:.2f} yr -> {r['hybrid_burn_yr']:.2f} yr "
              f"= {r['burn_time_reduction_pct']:.1f}% reduction")
    v = out["verdict"]
    print(f"\nH1 solar negligible beyond 2 AU: {v['H1_solar_negligible_beyond_2AU']}")
    print(f"H3 moves closed-loop closure: {v['H3_moves_closed_loop_closure']}")
    print(f"H5 invasive refactor justified for closure: {v['H5_invasive_refactor_justified_for_closure']}")
    print(f"\nWrote {RESULTS/'hybrid_power_summary.json'}")


if __name__ == "__main__":
    main()
