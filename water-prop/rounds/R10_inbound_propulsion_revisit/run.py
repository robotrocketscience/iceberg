"""Round 10 — Inbound propulsion architecture revisit.

Compares water-compatible propulsion candidates at the R8-corrected
chunk-fed inbound delta-velocity, across realistic power classes.

Adds a split-prop architecture (C6) that uses Earth-launched xenon for
inbound braking and chunk-fed water for Saturn egress — questioning the
"chunk-fed only" assumption baked into every prior round.

Pre-registered hypothesis in STUDY.md before this script runs.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass, field
from pathlib import Path

from waterprop.constants import G0

# Inputs
GRAPPLED_CHUNK_T = 14.0  # conops Phase 6
DRY_SPACECRAFT_T = 5.0  # conops
EFFICIENCY = 0.4  # first-order constant; see validity caveat in STUDY.md
REACTOR_SPECIFIC_POWER_W_PER_KG = 5.0  # mid-band per R1 (2.5-6.5)
DUTY = 0.5  # cruise duty cycle

# R8 corrected inbound delta-velocity cases (chunk-fed only):
CASE_B_CHUNKFED_KM_S = 5.94  # Slow transfer to v_inf 6 + single lunar gravity assist
CASE_C_CHUNKFED_KM_S = 2.85  # Slower transfer to v_inf 4 + single lunar gravity assist
SATURN_EGRESS_KM_S = 2.09  # mirror-of-ingress portion (chunk-fed regardless of inbound choice)

POWER_CLASSES_KWE = {
    "Kilopower_10kWe": 10.0,
    "FissionSurfacePower_40kWe": 40.0,
    "subMW_100kWe": 100.0,
}

INBOUND_CASES = {
    "case_B_chunkfed_5.94km_s": CASE_B_CHUNKFED_KM_S,
    "case_C_chunkfed_2.85km_s": CASE_C_CHUNKFED_KM_S,
}


@dataclass(frozen=True)
class Candidate:
    id: str
    name: str
    isp_s: float
    eta: float
    propellant: str
    notes: str


CANDIDATES = [
    Candidate("C1", "Water resistojet", 200.0, 0.7, "water", "TRL 9 (HYDROS-C)"),
    Candidate("C2", "Water microwave electrothermal", 500.0, 0.3, "water", "TRL 4-5; R0 baseline"),
    Candidate("C3", "Water Hall thruster", 1500.0, 0.55, "water", "TRL 2-3 (no flown water-Hall)"),
    Candidate("C4", "Water radio-frequency ion (Pale Blue class)", 2000.0, 0.65, "water", "TRL 7-8"),
    Candidate("C5", "Water dual-ion (electrolyzed)", 5000.0, 0.55, "water", "TRL 1-2 as integrated"),
]
# C6 is split-prop; handled separately.

C6_WATER_ISP_S = 500.0  # microwave electrothermal for Saturn egress
C6_WATER_ETA = 0.3
C6_XENON_ISP_S = 2000.0  # Hall-Xe for inbound braking (flight heritage)
C6_XENON_ETA = 0.55


def reactor_mass_t(power_kwe: float) -> float:
    """Reactor dry mass given specific power 5 W/kg (R1 mid-band)."""
    return (power_kwe * 1000.0) / REACTOR_SPECIFIC_POWER_W_PER_KG / 1000.0


def chunk_delivery_single_prop(
    candidate: Candidate, inbound_dv_km_s: float, power_kwe: float
) -> dict:
    """Single-propellant chunk-fed architecture.

    The chunk-fed inbound burn must cover both Saturn egress (mirror of
    ingress, ~2.09 km/s) and the residual after lunar gravity assist
    (the inbound_dv_km_s argument MINUS the Saturn egress, since R8's
    inbound_dv numbers already bundle these).

    Wait — R8's case_B/case_C chunk_fed_inbound_total_km_s already
    INCLUDES the Saturn egress mirror. So we use it as-is.
    """
    v_e = candidate.isp_s * G0  # m/s
    m_reactor = reactor_mass_t(power_kwe)
    m0 = GRAPPLED_CHUNK_T + DRY_SPACECRAFT_T + m_reactor
    dv = inbound_dv_km_s * 1000.0
    prop_frac = 1.0 - math.exp(-dv / v_e)
    prop_req = m0 * prop_frac
    delivered_chunk = max(GRAPPLED_CHUNK_T - prop_req, 0.0)
    delivery_frac = delivered_chunk / GRAPPLED_CHUNK_T
    # Thrust at this power
    F_N = 2.0 * candidate.eta * power_kwe * 1000.0 / v_e
    # Cruise time estimate (closed-form, average mass)
    m_avg = m0 - prop_req / 2.0
    accel_avg = F_N / (m_avg * 1000.0)  # m/s^2
    cruise_time_s = dv / (accel_avg * DUTY) if accel_avg > 0 else float("inf")
    cruise_time_yr = cruise_time_s / (365.25 * 86400)
    return {
        "candidate_id": candidate.id,
        "candidate_name": candidate.name,
        "isp_s": candidate.isp_s,
        "v_e_m_s": v_e,
        "power_kwe": power_kwe,
        "reactor_mass_t": m_reactor,
        "m0_t": m0,
        "inbound_dv_km_s": inbound_dv_km_s,
        "prop_req_t": prop_req,
        "delivered_chunk_t": delivered_chunk,
        "delivery_frac": delivery_frac,
        "thrust_N": F_N,
        "cruise_time_yr_estimate": cruise_time_yr,
    }


def split_prop_c6(
    inbound_dv_after_lga_km_s: float,
    saturn_egress_dv_km_s: float,
    power_kwe: float,
    xenon_t: float,
) -> dict:
    """Split-prop architecture:
      - chunk-fed water-microwave-electrothermal for Saturn egress only
      - Earth-launched xenon Hall thruster for inbound braking only
    """
    v_e_water = C6_WATER_ISP_S * G0
    v_e_xenon = C6_XENON_ISP_S * G0
    m_reactor = reactor_mass_t(power_kwe)
    xenon_tank_t = 0.10 * xenon_t  # 10% tank mass fraction (heuristic)

    # At Saturn departure: chunk + dry + reactor + xenon + tanks
    m0_egress = (
        GRAPPLED_CHUNK_T + DRY_SPACECRAFT_T + m_reactor + xenon_t + xenon_tank_t
    )
    # Chunk-fed Saturn egress
    prop_frac_egress = 1.0 - math.exp(-saturn_egress_dv_km_s * 1000.0 / v_e_water)
    water_used_egress = m0_egress * prop_frac_egress
    chunk_remaining = GRAPPLED_CHUNK_T - water_used_egress
    if chunk_remaining < 0:
        return {
            "infeasible": True,
            "reason": "Saturn egress consumes more than the chunk",
            "xenon_t": xenon_t,
            "water_used_egress_t": water_used_egress,
        }

    # Post-egress mass entering inbound cruise
    m0_inbound = (
        chunk_remaining + DRY_SPACECRAFT_T + m_reactor + xenon_t + xenon_tank_t
    )
    # Xenon-driven inbound braking
    prop_frac_xenon = 1.0 - math.exp(-inbound_dv_after_lga_km_s * 1000.0 / v_e_xenon)
    xenon_needed = m0_inbound * prop_frac_xenon
    if xenon_needed > xenon_t:
        # Insufficient xenon; would need to dip into chunk water via water-ion
        # For this round, mark as infeasible at this xenon allocation.
        return {
            "infeasible": True,
            "reason": "insufficient xenon for inbound braking",
            "xenon_t": xenon_t,
            "xenon_needed_t": xenon_needed,
            "chunk_remaining_t": chunk_remaining,
        }
    xenon_remaining = xenon_t - xenon_needed
    delivered_chunk = chunk_remaining  # the chunk itself is preserved post-egress
    delivery_frac = delivered_chunk / GRAPPLED_CHUNK_T

    # Earth-launch wet mass implication (informational)
    earth_launch_extra_t = xenon_t + xenon_tank_t

    return {
        "infeasible": False,
        "xenon_loaded_t": xenon_t,
        "xenon_tank_t": xenon_tank_t,
        "earth_launch_extra_t": earth_launch_extra_t,
        "reactor_mass_t": m_reactor,
        "m0_egress_t": m0_egress,
        "water_used_egress_t": water_used_egress,
        "chunk_after_egress_t": chunk_remaining,
        "m0_inbound_t": m0_inbound,
        "inbound_dv_after_lga_km_s": inbound_dv_after_lga_km_s,
        "xenon_needed_t": xenon_needed,
        "xenon_remaining_t": xenon_remaining,
        "delivered_chunk_t": delivered_chunk,
        "delivery_frac": delivery_frac,
    }


def find_optimal_c6_xenon(
    inbound_dv_after_lga_km_s: float,
    saturn_egress_dv_km_s: float,
    power_kwe: float,
) -> dict:
    """Sweep xenon mass to find the minimum that closes the inbound burn.

    Returns the configuration where xenon is just enough (xenon_remaining ≈ 0).
    """
    best = None
    for xenon_t in [x / 10.0 for x in range(5, 100)]:  # 0.5 to 9.9 tonnes
        result = split_prop_c6(
            inbound_dv_after_lga_km_s, saturn_egress_dv_km_s, power_kwe, xenon_t
        )
        if not result.get("infeasible", True):
            if best is None or result["earth_launch_extra_t"] < best["earth_launch_extra_t"]:
                best = result
                break  # first feasible is minimum-xenon by construction
    return best if best is not None else {"infeasible": True, "reason": "no feasible xenon mass found"}


def main() -> dict:
    results = {
        "inputs": {
            "grappled_chunk_t": GRAPPLED_CHUNK_T,
            "dry_spacecraft_t": DRY_SPACECRAFT_T,
            "reactor_specific_power_w_per_kg": REACTOR_SPECIFIC_POWER_W_PER_KG,
            "duty": DUTY,
            "case_B_chunkfed_km_s": CASE_B_CHUNKFED_KM_S,
            "case_C_chunkfed_km_s": CASE_C_CHUNKFED_KM_S,
            "saturn_egress_km_s": SATURN_EGRESS_KM_S,
        },
        "single_prop_sweep": {},
        "split_prop_sweep": {},
    }

    # --- Single-prop candidates ---
    for case_label, dv in INBOUND_CASES.items():
        results["single_prop_sweep"][case_label] = {}
        for power_label, power_kwe in POWER_CLASSES_KWE.items():
            row = []
            for cand in CANDIDATES:
                r = chunk_delivery_single_prop(cand, dv, power_kwe)
                row.append(r)
            results["single_prop_sweep"][case_label][power_label] = row

    # --- Split-prop (C6) ---
    # The split-prop inbound braking delta-velocity = (inbound_total - Saturn_egress).
    # For Case B: 5.94 - 2.09 = 3.85 km/s of inbound braking, on Hall-xenon at 2000 s.
    # For Case C: 2.85 - 2.09 = 0.76 km/s.
    for case_label, dv in INBOUND_CASES.items():
        inbound_braking = dv - SATURN_EGRESS_KM_S
        results["split_prop_sweep"][case_label] = {
            "inbound_braking_dv_km_s": inbound_braking,
            "per_power_class": {},
        }
        for power_label, power_kwe in POWER_CLASSES_KWE.items():
            optimal = find_optimal_c6_xenon(
                inbound_braking, SATURN_EGRESS_KM_S, power_kwe
            )
            results["split_prop_sweep"][case_label]["per_power_class"][power_label] = optimal

    # --- Hypothesis grading at Kilopower / Case B ---
    case_b_kilopower = results["single_prop_sweep"]["case_B_chunkfed_5.94km_s"][
        "Kilopower_10kWe"
    ]
    by_id = {r["candidate_id"]: r for r in case_b_kilopower}
    grading = {}
    grading["H10a_C1_resistojet"] = {
        "predicted": "0% delivery (≤ 0.1 t)",
        "measured_delivered_t": by_id["C1"]["delivered_chunk_t"],
        "held": by_id["C1"]["delivered_chunk_t"] <= 0.1,
    }
    grading["H10b_C2_microwave_electrothermal"] = {
        "predicted_range_t": [0.1 * 14 / 100, 5.0 * 14 / 100],
        "measured_delivered_t": by_id["C2"]["delivered_chunk_t"],
        "held": 0.014 <= by_id["C2"]["delivered_chunk_t"] <= 0.7,
    }
    grading["H10c_C3_hall"] = {
        "predicted_range_t": [0.40 * 14, 0.65 * 14],
        "measured_delivered_t": by_id["C3"]["delivered_chunk_t"],
        "held": 0.40 * 14 <= by_id["C3"]["delivered_chunk_t"] <= 0.65 * 14,
    }
    grading["H10d_C4_rf_ion"] = {
        "predicted_range_t": [0.60 * 14, 0.80 * 14],
        "measured_delivered_t": by_id["C4"]["delivered_chunk_t"],
        "held": 0.60 * 14 <= by_id["C4"]["delivered_chunk_t"] <= 0.80 * 14,
    }
    grading["H10e_C5_dual_ion"] = {
        "predicted_range_t": [0.80 * 14, 0.95 * 14],
        "measured_delivered_t": by_id["C5"]["delivered_chunk_t"],
        "held": 0.80 * 14 <= by_id["C5"]["delivered_chunk_t"] <= 0.95 * 14,
    }
    c6_case_b_kilo = results["split_prop_sweep"]["case_B_chunkfed_5.94km_s"][
        "per_power_class"
    ]["Kilopower_10kWe"]
    if c6_case_b_kilo.get("infeasible", True):
        grading["H10f_C6_split_prop"] = {
            "predicted_range_t": [0.70 * 14, 0.90 * 14],
            "verdict": "infeasible at any feasible xenon mass",
            "reason": c6_case_b_kilo.get("reason"),
        }
    else:
        grading["H10f_C6_split_prop"] = {
            "predicted_range_t": [0.70 * 14, 0.90 * 14],
            "measured_delivered_t": c6_case_b_kilo["delivered_chunk_t"],
            "earth_launch_extra_t": c6_case_b_kilo["earth_launch_extra_t"],
            "held": 0.70 * 14 <= c6_case_b_kilo["delivered_chunk_t"] <= 0.90 * 14,
        }

    results["hypothesis_grading"] = grading

    # --- Output ---
    out_dir = Path(__file__).parent / "results"
    out_dir.mkdir(exist_ok=True)
    with (out_dir / "propulsion_sweep.json").open("w") as f:
        json.dump(results, f, indent=2)

    # Console summary
    print("=" * 88)
    print("R10 — Inbound Propulsion Architecture Revisit")
    print("=" * 88)
    print()
    print("Chunk = 14.0 t, dry = 5.0 t, reactor 5 W/kg, η = 0.4 (constant), duty = 0.5")
    print()

    for case_label, dv in INBOUND_CASES.items():
        print(f"=== {case_label} (chunk-fed inbound delta-velocity = {dv:.2f} km/s) ===")
        for power_label, power_kwe in POWER_CLASSES_KWE.items():
            rows = results["single_prop_sweep"][case_label][power_label]
            print(f"  Power class: {power_label} ({power_kwe:.0f} kWe, reactor "
                  f"{reactor_mass_t(power_kwe):.1f} t)")
            print(f"  {'cand':<3} {'name':<46} {'Isp(s)':>7} {'prop(t)':>9} "
                  f"{'delivered(t)':>12} {'frac':>7} {'thrust(N)':>10} {'cruise(yr)':>11}")
            for r in rows:
                print(
                    f"  {r['candidate_id']:<3} {r['candidate_name'][:45]:<46} "
                    f"{r['isp_s']:>7.0f} {r['prop_req_t']:>9.2f} "
                    f"{r['delivered_chunk_t']:>12.2f} {r['delivery_frac']:>7.1%} "
                    f"{r['thrust_N']:>10.3f} {r['cruise_time_yr_estimate']:>11.2f}"
                )

            # C6 row
            c6_braking = dv - SATURN_EGRESS_KM_S
            c6 = results["split_prop_sweep"][case_label]["per_power_class"][power_label]
            if c6.get("infeasible"):
                print(f"  C6 split-prop (water egress + Hall-xenon inbound {c6_braking:.2f} km/s): "
                      f"INFEASIBLE — {c6.get('reason', '?')}")
            else:
                print(f"  C6 split-prop (water egress + Hall-xenon inbound {c6_braking:.2f} km/s): "
                      f"xenon launched {c6['xenon_loaded_t']:.2f} t, "
                      f"chunk delivered {c6['delivered_chunk_t']:.2f} t "
                      f"({c6['delivery_frac']:.1%}), Earth-launch extra "
                      f"{c6['earth_launch_extra_t']:.2f} t")
            print()
        print()

    print("Hypothesis grading (Kilopower / Case B):")
    for h, g in grading.items():
        verdict = "HELD" if g.get("held") else g.get("verdict", "FALSIFIED")
        print(f"  {h}: {verdict}")
    print()
    print(f"Result JSON written to {out_dir / 'propulsion_sweep.json'}")

    return results


if __name__ == "__main__":
    main()
