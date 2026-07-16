"""R-outbound-architecture — compare all-electric / chemical-kick / depot-refueled outbound.

Three outbound architectures evaluated against the architecture matrix's cells:
  A. All-electric (status quo assumption, Isp 2000s, dv 9 km/s, ratio 1.583)
  B. Chemical hydrolox kick + electric Saturn capture (realistic conops)
  C. Depot-refueled chemical kick (mission 2+ steady state)

Compute per-mission low Earth orbit mass, delivered-per-launch ratio, mission-to-mission
breakeven for depot-fed steady state.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from waterprop.constants import G0

YEAR_S = 365.25 * 86400.0

DV_TOTAL_INBOUND_KM_S = 6.42
DV_KICK_KM_S = 7.3
DV_SATURN_CAPTURE_KM_S = 2.0
DV_OUTBOUND_ALL_ELEC_KM_S = 9.0

ISP_KICK_HYDROLOX_S = 450.0
ISP_ELEC_OUTBOUND_S = 2000.0
ISP_HYDROLOX_S = 450.0
ISP_HYPERGOLIC_S = 320.0

KICK_DRY_TO_WET = 0.10
TAU_BURN_MAX_INBOUND_YR = 7.0  # consistent with prior rounds
M_TUG_KG = 5000.0
M_CHEM_DRY_INBOUND_KG = 10000.0
SPECIFIC_POWER_W_PER_KG = 10.0

ETA_THR = {"Hall": 0.55, "RF_ion": 0.65, "dual_ion": 0.55}

REACTORS_KWE = [10.0, 40.0, 100.0, 200.0, 500.0, 1000.0]
CHUNKS_T = [100.0, 200.0, 500.0]
DV_CHEM_INBOUND_OPTIONS = [0.0, 1.0, 2.0, 3.0]
ELECTRIC_ISPS = [1500.0, 2000.0, 2934.0, 5000.0]


def vehicle_dry_t(reactor_kwe: float) -> float:
    return (M_TUG_KG + reactor_kwe * 1000.0 / SPECIFIC_POWER_W_PER_KG) / 1000.0


def thruster_class(isp_s: float) -> tuple[str, float]:
    if isp_s <= 1800.0:  return "Hall", ETA_THR["Hall"]
    if isp_s <= 3000.0:  return "RF_ion", ETA_THR["RF_ion"]
    return                       "dual_ion", ETA_THR["dual_ion"]


def outbound_mass_at_LEO(M_at_saturn_arrival_t: float, architecture: str) -> dict:
    """Return mass at LEO and breakdown for each outbound architecture.

    M_at_saturn_arrival_t = vehicle dry + any chemical-stage-inbound dry + any electric capture prop.
    """
    if architecture == "A_all_electric":
        v_e = ISP_ELEC_OUTBOUND_S * G0
        M_at_LEO = M_at_saturn_arrival_t * math.exp(DV_OUTBOUND_ALL_ELEC_KM_S * 1000.0 / v_e)
        return {
            "M_at_LEO_t": M_at_LEO,
            "outbound_prop_t": M_at_LEO - M_at_saturn_arrival_t,
            "kick_dry_t": 0.0,
            "earth_launched_t": M_at_LEO,
            "depot_sourced_t": 0.0,
        }
    elif architecture == "B_chem_kick":
        # Backwards from Saturn capture
        v_e_elec = ISP_ELEC_OUTBOUND_S * G0
        v_e_kick = ISP_KICK_HYDROLOX_S * G0
        # Mass before Saturn capture = M_v after capture × exp(dv_cap / v_e_elec)
        # In our case, M_at_saturn_arrival_t already represents the mass at Saturn arrival
        # which is BEFORE the capture burn for arch B.
        # The vehicle plus electric Saturn capture propellant arrives via Hohmann.
        # M_after_capture = M_at_saturn_arrival_t × exp(-dv_cap / v_e_elec)
        # Wait — in arch B, the kick stage delivers (M_v + capture_prop + kick_dry) to trans-Saturn,
        # then jettisons kick stage. Vehicle arrives at Saturn with capture_prop + M_v.
        # So M_at_saturn_arrival_t in arch B = M_v + capture_prop.
        # Therefore: M_at_saturn_arrival_t = M_v × exp(dv_cap / v_e_elec)
        # Given M_at_saturn_arrival_t, M_v is implicit. But we'll just use M_at_saturn_arrival_t.

        # Kick stage burns: M_after_kick = (M_at_saturn_arrival_t + M_kick_dry); M_before_kick = M_after_kick × exp(dv_kick / v_e_kick)
        # Where M_kick_dry = f/(1-f) × M_kick_prop = f/(1-f) × (M_before_kick − M_after_kick)
        # Let R = exp(dv_kick / v_e_kick). M_before_kick = M_after_kick × R
        # M_kick_prop = M_after_kick × (R - 1)
        # M_kick_dry = (f / (1-f)) × M_after_kick × (R - 1)
        # But M_after_kick includes M_kick_dry. So this is self-referential. Solve algebraically:
        #
        # Define M_p = payload at Saturn arrival (= M_at_saturn_arrival_t).
        # M_after_kick = M_p + M_kick_dry
        # M_before_kick = (M_p + M_kick_dry) × R
        # M_kick_prop = M_before_kick − M_after_kick = (M_p + M_kick_dry) × (R − 1)
        # M_kick_dry = f × M_kick_wet = f × (M_kick_prop + M_kick_dry)
        #   => M_kick_dry × (1 − f) = f × M_kick_prop
        #   => M_kick_dry = (f/(1-f)) × (M_p + M_kick_dry) × (R − 1)
        # Let α = f/(1-f) × (R − 1). Then M_kick_dry = α × M_p + α × M_kick_dry
        #   => M_kick_dry × (1 − α) = α × M_p
        #   => M_kick_dry = α × M_p / (1 − α)
        #
        # Check feasibility: if α >= 1, no feasible kick stage at this dv_kick + f.

        R = math.exp(DV_KICK_KM_S * 1000.0 / v_e_kick)
        alpha = (KICK_DRY_TO_WET / (1.0 - KICK_DRY_TO_WET)) * (R - 1.0)
        if alpha >= 1.0:
            return {
                "M_at_LEO_t": float("inf"),
                "outbound_prop_t": float("inf"),
                "kick_dry_t": float("inf"),
                "earth_launched_t": float("inf"),
                "depot_sourced_t": 0.0,
                "feasible": False,
            }
        M_p = M_at_saturn_arrival_t
        M_kick_dry = alpha * M_p / (1.0 - alpha)
        M_after_kick = M_p + M_kick_dry
        M_kick_prop = M_after_kick * (R - 1.0)
        M_at_LEO = M_after_kick + M_kick_prop  # = M_before_kick
        return {
            "M_at_LEO_t": M_at_LEO,
            "outbound_prop_t": M_kick_prop,
            "kick_dry_t": M_kick_dry,
            "earth_launched_t": M_at_LEO,
            "depot_sourced_t": 0.0,
            "feasible": True,
        }
    elif architecture == "C_depot_kick":
        # Same as B but kick propellant comes from depot, not Earth launch.
        # Marginal Earth-launched = M_p + M_kick_dry.
        v_e_kick = ISP_KICK_HYDROLOX_S * G0
        R = math.exp(DV_KICK_KM_S * 1000.0 / v_e_kick)
        alpha = (KICK_DRY_TO_WET / (1.0 - KICK_DRY_TO_WET)) * (R - 1.0)
        if alpha >= 1.0:
            return {"feasible": False}
        M_p = M_at_saturn_arrival_t
        M_kick_dry = alpha * M_p / (1.0 - alpha)
        M_after_kick = M_p + M_kick_dry
        M_kick_prop = M_after_kick * (R - 1.0)
        M_at_LEO_total = M_after_kick + M_kick_prop
        return {
            "M_at_LEO_t": M_at_LEO_total,                # total mass on orbit (for reference)
            "outbound_prop_t": M_kick_prop,
            "kick_dry_t": M_kick_dry,
            "earth_launched_t": M_p + M_kick_dry,        # marginal Earth-launch
            "depot_sourced_t": M_kick_prop,
            "feasible": True,
        }


def saturn_arrival_payload_t(M_v_t: float, outbound_arch: str, m_chem_dry_inbound_t: float = 0.0) -> float:
    """Mass that must arrive at Saturn arrival point.

    For arch A (all-electric outbound): all the propulsion is upstream; mass at Saturn arrival = M_v + chem dry (if Variant B).
    For arch B/C (chemical kick): vehicle arrives on Hohmann trajectory with electric-Saturn-capture propellant.
                                  Saturn capture is electric, so capture_prop comes from outbound launch.
    """
    if outbound_arch == "A_all_electric":
        return M_v_t + m_chem_dry_inbound_t
    else:
        # Need to carry electric Saturn capture propellant
        v_e_elec = ISP_ELEC_OUTBOUND_S * G0
        M_after_capture = M_v_t + m_chem_dry_inbound_t
        M_before_capture = M_after_capture * math.exp(DV_SATURN_CAPTURE_KM_S * 1000.0 / v_e_elec)
        return M_before_capture


def all_electric_inbound(reactor_kwe: float, chunk_t: float, isp_s: float) -> dict:
    M_v_t = vehicle_dry_t(reactor_kwe)
    M_initial_t = M_v_t + chunk_t
    v_e = isp_s * G0
    M_final_t = M_initial_t * math.exp(-DV_TOTAL_INBOUND_KM_S * 1000.0 / v_e)
    if M_final_t < M_v_t:
        return {"feasible": False}
    delivered_t = M_final_t - M_v_t
    m_prop_t = M_initial_t - M_final_t
    _, eta = thruster_class(isp_s)
    thrust_N = 2.0 * eta * reactor_kwe * 1000.0 / v_e
    tau_yr = m_prop_t * 1000.0 * v_e / thrust_N / YEAR_S
    return {
        "feasible": tau_yr <= TAU_BURN_MAX_INBOUND_YR,
        "architecture": "all_electric",
        "isp_s": isp_s,
        "dv_chem_km_s": 0.0,
        "delivered_water_t": delivered_t,
        "M_v_t": M_v_t,
        "m_chem_dry_inbound_t": 0.0,
        "burn_time_yr": tau_yr,
    }


def variant_b_inbound(reactor_kwe: float, chunk_t: float, dv_chem_km_s: float, isp_s: float) -> dict:
    dv_elec = DV_TOTAL_INBOUND_KM_S - dv_chem_km_s
    if dv_elec <= 0:
        return {"feasible": False}
    M_v_t = vehicle_dry_t(reactor_kwe)
    M_chem_dry_t = M_CHEM_DRY_INBOUND_KG / 1000.0
    M_initial_t = M_v_t + M_chem_dry_t + chunk_t
    v_e_chem = ISP_HYDROLOX_S * G0
    M_after_chem_t = M_initial_t * math.exp(-dv_chem_km_s * 1000.0 / v_e_chem)
    consumed_chem_t = M_initial_t - M_after_chem_t
    if consumed_chem_t > chunk_t:
        return {"feasible": False}
    M_after_jet_t = M_after_chem_t - M_chem_dry_t
    v_e_elec = isp_s * G0
    M_final_t = M_after_jet_t * math.exp(-dv_elec * 1000.0 / v_e_elec)
    if M_final_t < M_v_t:
        return {"feasible": False}
    delivered_t = M_final_t - M_v_t
    m_prop_elec_t = M_after_jet_t - M_final_t
    _, eta = thruster_class(isp_s)
    thrust_N = 2.0 * eta * reactor_kwe * 1000.0 / v_e_elec
    tau_yr = m_prop_elec_t * 1000.0 * v_e_elec / thrust_N / YEAR_S
    return {
        "feasible": tau_yr <= TAU_BURN_MAX_INBOUND_YR,
        "architecture": "variant_b",
        "isp_s": isp_s,
        "dv_chem_km_s": dv_chem_km_s,
        "delivered_water_t": delivered_t,
        "M_v_t": M_v_t,
        "m_chem_dry_inbound_t": M_chem_dry_t,
        "burn_time_yr": tau_yr,
    }


def best_inbound(reactor_kwe: float, chunk_t: float) -> dict | None:
    candidates = []
    for isp in ELECTRIC_ISPS:
        ae = all_electric_inbound(reactor_kwe, chunk_t, isp)
        if ae.get("feasible"):
            candidates.append(ae)
        for dv_c in DV_CHEM_INBOUND_OPTIONS:
            if dv_c == 0.0:
                continue
            vb = variant_b_inbound(reactor_kwe, chunk_t, dv_c, isp)
            if vb.get("feasible"):
                candidates.append(vb)
    if not candidates:
        return None
    return max(candidates, key=lambda c: c["delivered_water_t"])


def evaluate_cell(reactor_kwe: float, chunk_t: float, outbound_arch: str) -> dict:
    inbound = best_inbound(reactor_kwe, chunk_t)
    if inbound is None:
        return {"feasible": False}
    saturn_arrival = saturn_arrival_payload_t(
        inbound["M_v_t"], outbound_arch, inbound["m_chem_dry_inbound_t"]
    )
    out = outbound_mass_at_LEO(saturn_arrival, outbound_arch)
    if not out.get("feasible", True):
        return {"feasible": False, "reason": "infeasible kick stage"}
    return {
        "feasible": True,
        "reactor_kwe": reactor_kwe,
        "chunk_t": chunk_t,
        "outbound_arch": outbound_arch,
        "inbound_arch": inbound["architecture"],
        "inbound_isp_s": inbound["isp_s"],
        "inbound_dv_chem_km_s": inbound["dv_chem_km_s"],
        "delivered_water_t": inbound["delivered_water_t"],
        "M_v_t": inbound["M_v_t"],
        "saturn_arrival_payload_t": saturn_arrival,
        "M_at_LEO_t": out["M_at_LEO_t"],
        "earth_launched_t": out["earth_launched_t"],
        "depot_sourced_t": out["depot_sourced_t"],
        "delivered_per_earth_launched": inbound["delivered_water_t"] / out["earth_launched_t"]
            if out["earth_launched_t"] > 0 else 0.0,
        "delivered_per_total_LEO": inbound["delivered_water_t"] / out["M_at_LEO_t"]
            if out["M_at_LEO_t"] > 0 else 0.0,
    }


def main() -> dict:
    grid = []
    for reactor in REACTORS_KWE:
        for chunk in CHUNKS_T:
            for arch in ("A_all_electric", "B_chem_kick", "C_depot_kick"):
                cell = evaluate_cell(reactor, chunk, arch)
                grid.append(cell)

    # Pairwise compare A vs B at each (reactor, chunk)
    comparisons = []
    for reactor in REACTORS_KWE:
        for chunk in CHUNKS_T:
            cells = {arch: next((g for g in grid if g.get("feasible")
                                 and g["reactor_kwe"] == reactor
                                 and g["chunk_t"] == chunk
                                 and g["outbound_arch"] == arch), None)
                     for arch in ("A_all_electric", "B_chem_kick", "C_depot_kick")}
            a = cells.get("A_all_electric")
            b = cells.get("B_chem_kick")
            c = cells.get("C_depot_kick")
            if a is None or b is None:
                continue
            mult_AB = b["M_at_LEO_t"] / a["M_at_LEO_t"]
            mult_AC = c["earth_launched_t"] / a["M_at_LEO_t"] if c else None
            comparisons.append({
                "reactor_kwe": reactor,
                "chunk_t": chunk,
                "A_M_LEO_t": a["M_at_LEO_t"],
                "B_M_LEO_t": b["M_at_LEO_t"],
                "C_earth_launched_t": c["earth_launched_t"] if c else None,
                "C_depot_sourced_t": c["depot_sourced_t"] if c else None,
                "A_delivered_per_LEO": a["delivered_per_total_LEO"],
                "B_delivered_per_LEO": b["delivered_per_total_LEO"],
                "C_delivered_per_earth_launched": c["delivered_per_earth_launched"] if c else None,
                "multiplier_B_over_A": mult_AB,
                "multiplier_C_over_A": mult_AC,
                "inbound_arch": a["inbound_arch"],
                "delivered_water_t": a["delivered_water_t"],
            })

    # Mission ramp: how many missions until depot is full?
    # Assume one mission's depot need = kick stage propellant for ONE next outbound mission
    # Compute kick propellant for each cell, then mission_breakeven = ceil(kick_prop / delivered)
    ramp = []
    for c in comparisons:
        if c["C_earth_launched_t"] and c["C_depot_sourced_t"]:
            kick_prop = c["C_depot_sourced_t"]
            delivered = c["delivered_water_t"]
            missions_to_fill_depot_for_one_next = math.ceil(kick_prop / delivered) if delivered > 0 else float("inf")
            ramp.append({
                "reactor_kwe": c["reactor_kwe"],
                "chunk_t": c["chunk_t"],
                "delivered_per_mission_t": delivered,
                "kick_prop_per_mission_t": kick_prop,
                "missions_to_fill_depot_for_next_mission": missions_to_fill_depot_for_one_next,
            })

    out = {
        "axes": {
            "reactor_kwe": REACTORS_KWE,
            "chunk_t": CHUNKS_T,
            "outbound_architectures": ["A_all_electric", "B_chem_kick", "C_depot_kick"],
        },
        "constants": {
            "dv_kick_km_s": DV_KICK_KM_S,
            "dv_saturn_capture_km_s": DV_SATURN_CAPTURE_KM_S,
            "isp_kick_s": ISP_KICK_HYDROLOX_S,
            "isp_elec_outbound_s": ISP_ELEC_OUTBOUND_S,
            "kick_dry_to_wet": KICK_DRY_TO_WET,
        },
        "grid": grid,
        "comparisons": comparisons,
        "mission_ramp": ramp,
    }
    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)
    (results_dir / "outbound.json").write_text(json.dumps(out, indent=2, default=str))

    # Markdown tables
    lines = []
    lines.append("### Launch mass (tonnes) under three outbound architectures\n")
    lines.append("- A = all-electric outbound (status-quo assumption from prior rounds)\n")
    lines.append("- B = chemical hydrolox kick stage + electric Saturn capture (realistic concept of operations)\n")
    lines.append("- C = depot-refueled chemical kick (steady state with low Earth orbit depot)\n")
    lines.append("Format per cell: A / B / C-earth-launched (multiplier B/A)\n")
    lines.append("| Reactor (kWe) | 100 t | 200 t | 500 t |")
    lines.append("|---:|---|---|---|")
    for reactor in REACTORS_KWE:
        row = [f"{reactor:.0f}"]
        for chunk in CHUNKS_T:
            c = next((c for c in comparisons if c["reactor_kwe"] == reactor and c["chunk_t"] == chunk), None)
            if c is None:
                row.append("-")
            else:
                row.append(
                    f"{c['A_M_LEO_t']:.0f} / {c['B_M_LEO_t']:.0f} / {c['C_earth_launched_t']:.0f} "
                    f"(×{c['multiplier_B_over_A']:.1f})"
                )
        lines.append("| " + " | ".join(row) + " |")

    lines.append("\n### Delivered-water per launch-mass under three outbound architectures\n")
    lines.append("Format per cell: A / B / C-earth-launched-only\n")
    lines.append("| Reactor (kWe) | 100 t | 200 t | 500 t |")
    lines.append("|---:|---|---|---|")
    for reactor in REACTORS_KWE:
        row = [f"{reactor:.0f}"]
        for chunk in CHUNKS_T:
            c = next((c for c in comparisons if c["reactor_kwe"] == reactor and c["chunk_t"] == chunk), None)
            if c is None:
                row.append("-")
            else:
                row.append(
                    f"{c['A_delivered_per_LEO']:.2f} / {c['B_delivered_per_LEO']:.2f} / "
                    f"{c['C_delivered_per_earth_launched']:.2f}"
                )
        lines.append("| " + " | ".join(row) + " |")

    lines.append("\n### Mission-ramp: how many ICEBERG missions fill the depot for ONE next outbound kick stage?\n")
    lines.append("| Reactor (kWe) | Chunk (t) | Delivered per mission (t) | Kick propellant per mission (t) | Missions to fill depot |")
    lines.append("|---:|---:|---:|---:|---:|")
    for r in ramp:
        lines.append(
            f"| {r['reactor_kwe']:.0f} | {r['chunk_t']:.0f} | "
            f"{r['delivered_per_mission_t']:.1f} | {r['kick_prop_per_mission_t']:.1f} | "
            f"{r['missions_to_fill_depot_for_next_mission']} |"
        )

    lines.append("\n### Chemical kick stage details at 100 t chunk × 40 kilowatt-electric (H-out-a check)\n")
    cell = next((c for c in comparisons if c["reactor_kwe"] == 40.0 and c["chunk_t"] == 100.0), None)
    if cell:
        lines.append(f"- Vehicle dry mass: {(M_TUG_KG + 40*1000/SPECIFIC_POWER_W_PER_KG)/1000:.1f} t")
        lines.append(f"- Saturn arrival payload (incl. electric capture propellant): tbd")
        lines.append(f"- A (all-electric outbound) launch mass: {cell['A_M_LEO_t']:.1f} t")
        lines.append(f"- B (chemical kick) launch mass: {cell['B_M_LEO_t']:.1f} t")
        lines.append(f"- Multiplier B/A: ×{cell['multiplier_B_over_A']:.2f}")

    (results_dir / "tables.md").write_text("\n".join(lines))
    return out


if __name__ == "__main__":
    out = main()
    print(f"Sweep complete. {len(out['grid'])} cells, {len(out['comparisons'])} comparisons, {len(out['mission_ramp'])} ramps.")
    print(f"  Wrote results/outbound.json and results/tables.md")
