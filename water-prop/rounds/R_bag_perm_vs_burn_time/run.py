"""R-bag-permeability-vs-burn-time — does relaxing the 7-yr cap let Kilopower all-electric beat Variant B?

For each (reactor, chunk, permeability rate) cell:
  - Compute all-electric delivered mass at each candidate specific impulse, ignoring the 7-yr cap
  - Apply permeability tax: delivered_actual = delivered_raw * (1 - rate * burn_time_yr)
  - Find optimum specific impulse for max delivered_actual
  - Compute Variant B delivered mass at its winner cell (from R-chunk-fed-chemical), apply same permeability
  - Pick winner

Pure algebra. Reuses R-chunk-fed-chemical mass accounting.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from waterprop.constants import G0

YEAR_S = 365.25 * 86400.0

DV_TOTAL_KM_S = 6.42
DV_OUTBOUND_KM_S = 9.0
ISP_OUTBOUND_S = 2000.0
ISP_HYDROLOX_S = 450.0
M_TUG_KG = 5000.0
M_CHEM_DRY_KG = 10000.0
SPECIFIC_POWER_W_PER_KG = 10.0

ETA_THR = {"Hall": 0.55, "RF_ion": 0.65, "dual_ion": 0.55}

PERM_RATES_PER_YR = [0.0, 0.005, 0.0065, 0.010, 0.020]
REACTORS_KWE = [10.0, 40.0, 100.0]
CHUNKS_T = [50.0, 100.0, 200.0]
ELECTRIC_ISPS = [1500.0, 2000.0, 2934.0, 5000.0]
DV_CHEM_OPTIONS = [1.0, 2.0, 3.0]
BURN_TIME_HARD_CAP_YR = 50.0  # truly infeasible above this


def thruster_class(isp_s: float) -> tuple[str, float]:
    if isp_s <= 1800.0:  return "Hall", ETA_THR["Hall"]
    if isp_s <= 3000.0:  return "RF_ion", ETA_THR["RF_ion"]
    return                       "dual_ion", ETA_THR["dual_ion"]


def vehicle_dry_t(reactor_kwe: float) -> float:
    return (M_TUG_KG + reactor_kwe * 1000.0 / SPECIFIC_POWER_W_PER_KG) / 1000.0


def outbound_LEO_t(mass_at_saturn_t: float) -> float:
    v_e = ISP_OUTBOUND_S * G0
    return mass_at_saturn_t * math.exp(DV_OUTBOUND_KM_S * 1000.0 / v_e)


def all_electric_uncapped(reactor_kwe: float, chunk_t: float, isp_s: float) -> dict:
    M_v_t = vehicle_dry_t(reactor_kwe)
    M_initial_t = M_v_t + chunk_t
    v_e = isp_s * G0
    M_final_t = M_initial_t * math.exp(-DV_TOTAL_KM_S * 1000.0 / v_e)
    if M_final_t < M_v_t:
        return {"feasible": False}
    delivered_t = M_final_t - M_v_t
    m_prop_t = M_initial_t - M_final_t
    _, eta = thruster_class(isp_s)
    thrust_N = 2.0 * eta * reactor_kwe * 1000.0 / v_e
    tau_yr = m_prop_t * 1000.0 * v_e / thrust_N / YEAR_S
    return {
        "feasible": tau_yr <= BURN_TIME_HARD_CAP_YR,
        "isp_s": isp_s,
        "delivered_t_raw": delivered_t,
        "burn_time_yr": tau_yr,
        "M_v_t": M_v_t,
        "M_LEO_t": outbound_LEO_t(M_v_t),
    }


def variant_b(reactor_kwe: float, chunk_t: float, dv_chem_km_s: float, isp_s: float) -> dict:
    dv_elec = DV_TOTAL_KM_S - dv_chem_km_s
    if dv_elec <= 0:
        return {"feasible": False}
    M_v_t = vehicle_dry_t(reactor_kwe)
    M_initial_t = M_v_t + M_CHEM_DRY_KG / 1000.0 + chunk_t
    v_e_c = ISP_HYDROLOX_S * G0
    M_after_chem = M_initial_t * math.exp(-dv_chem_km_s * 1000.0 / v_e_c)
    consumed_chem = M_initial_t - M_after_chem
    if consumed_chem > chunk_t:
        return {"feasible": False}
    M_after_jet = M_after_chem - M_CHEM_DRY_KG / 1000.0
    v_e_e = isp_s * G0
    M_final = M_after_jet * math.exp(-dv_elec * 1000.0 / v_e_e)
    if M_final < M_v_t:
        return {"feasible": False}
    delivered_t = M_final - M_v_t
    m_prop_e = M_after_jet - M_final
    _, eta = thruster_class(isp_s)
    thrust_N = 2.0 * eta * reactor_kwe * 1000.0 / v_e_e
    tau_yr = m_prop_e * 1000.0 * v_e_e / thrust_N / YEAR_S
    M_at_saturn = M_v_t + M_CHEM_DRY_KG / 1000.0
    return {
        "feasible": tau_yr <= BURN_TIME_HARD_CAP_YR,
        "dv_chem_km_s": dv_chem_km_s,
        "isp_s": isp_s,
        "delivered_t_raw": delivered_t,
        "burn_time_yr": tau_yr,
        "M_v_t": M_v_t,
        "M_LEO_t": outbound_LEO_t(M_at_saturn),
    }


def apply_permeability(delivered_raw: float, burn_time_yr: float, rate_per_yr: float) -> float:
    loss = rate_per_yr * burn_time_yr
    if loss >= 1.0:
        return 0.0
    return delivered_raw * (1.0 - loss)


def best_all_electric(reactor_kwe: float, chunk_t: float, rate_per_yr: float) -> dict | None:
    candidates = []
    for isp in ELECTRIC_ISPS:
        ae = all_electric_uncapped(reactor_kwe, chunk_t, isp)
        if not ae.get("feasible"):
            continue
        ae["delivered_t_after_perm"] = apply_permeability(
            ae["delivered_t_raw"], ae["burn_time_yr"], rate_per_yr
        )
        ae["architecture"] = "all_electric"
        ae["dv_chem_km_s"] = 0.0
        candidates.append(ae)
    if not candidates:
        return None
    return max(candidates, key=lambda c: c["delivered_t_after_perm"])


def best_variant_b(reactor_kwe: float, chunk_t: float, rate_per_yr: float) -> dict | None:
    candidates = []
    for dv_c in DV_CHEM_OPTIONS:
        for isp in ELECTRIC_ISPS:
            vb = variant_b(reactor_kwe, chunk_t, dv_c, isp)
            if not vb.get("feasible"):
                continue
            vb["delivered_t_after_perm"] = apply_permeability(
                vb["delivered_t_raw"], vb["burn_time_yr"], rate_per_yr
            )
            vb["architecture"] = "variant_b"
            candidates.append(vb)
    if not candidates:
        return None
    return max(candidates, key=lambda c: c["delivered_t_after_perm"])


def main() -> dict:
    grid = []
    for reactor in REACTORS_KWE:
        for chunk in CHUNKS_T:
            for rate in PERM_RATES_PER_YR:
                ae = best_all_electric(reactor, chunk, rate)
                vb = best_variant_b(reactor, chunk, rate)
                winner = None
                if ae and vb:
                    winner = ae if ae["delivered_t_after_perm"] > vb["delivered_t_after_perm"] else vb
                elif ae:
                    winner = ae
                elif vb:
                    winner = vb
                row = {
                    "reactor_kwe": reactor,
                    "chunk_t": chunk,
                    "perm_rate_per_yr": rate,
                    "all_electric": ae,
                    "variant_b": vb,
                    "winner": winner["architecture"] if winner else "none",
                    "winner_delivered_t": winner["delivered_t_after_perm"] if winner else 0.0,
                    "winner_burn_time_yr": winner["burn_time_yr"] if winner else 0.0,
                }
                grid.append(row)

    # Find breakeven permeability rate per (reactor, chunk) cell
    breakevens = []
    for reactor in REACTORS_KWE:
        for chunk in CHUNKS_T:
            cells = [g for g in grid if g["reactor_kwe"] == reactor and g["chunk_t"] == chunk]
            # Find the permeability rate where the winner switches
            prev_winner = None
            breakeven_rate = None
            for c in sorted(cells, key=lambda c: c["perm_rate_per_yr"]):
                if prev_winner and c["winner"] != prev_winner:
                    breakeven_rate = c["perm_rate_per_yr"]
                    break
                prev_winner = c["winner"]
            breakevens.append({
                "reactor_kwe": reactor,
                "chunk_t": chunk,
                "winner_at_zero_perm": next(
                    (c["winner"] for c in cells if c["perm_rate_per_yr"] == 0.0), "none"
                ),
                "winner_at_2pct": next(
                    (c["winner"] for c in cells if c["perm_rate_per_yr"] == 0.020), "none"
                ),
                "breakeven_rate_per_yr": breakeven_rate,
            })

    out = {
        "axes": {
            "perm_rates_per_yr": PERM_RATES_PER_YR,
            "reactor_kwe": REACTORS_KWE,
            "chunk_t": CHUNKS_T,
            "electric_isps": ELECTRIC_ISPS,
        },
        "grid": grid,
        "breakevens": breakevens,
    }
    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)
    (results_dir / "bag_perm.json").write_text(json.dumps(out, indent=2, default=str))

    # Markdown tables
    lines = []
    lines.append("### Winning architecture by (reactor × chunk × permeability rate)\n")
    lines.append("Format: architecture · delivered_after_perm (t) · burn_time (yr)\n")
    for reactor in REACTORS_KWE:
        lines.append(f"\n**Reactor = {reactor:.0f} kilowatt-electric:**\n")
        lines.append("| Chunk (t) | 0% / yr | 0.5% / yr | 0.65% / yr | 1.0% / yr | 2.0% / yr |")
        lines.append("|---:|---|---|---|---|---|")
        for chunk in CHUNKS_T:
            row = [f"{chunk:.0f}"]
            for rate in PERM_RATES_PER_YR:
                g = next((g for g in grid if g["reactor_kwe"] == reactor
                          and g["chunk_t"] == chunk
                          and g["perm_rate_per_yr"] == rate), None)
                if not g or not g["winner"] or g["winner"] == "none":
                    row.append("-")
                else:
                    row.append(f"{g['winner']} · {g['winner_delivered_t']:.1f} t · {g['winner_burn_time_yr']:.1f} yr")
            lines.append("| " + " | ".join(row) + " |")

    lines.append("\n### Breakeven permeability rate per (reactor × chunk)\n")
    lines.append("'Breakeven' is the permeability rate at which the winning architecture switches.\n")
    lines.append("| Reactor (kWe) | Chunk (t) | Winner at 0% / yr | Winner at 2.0% / yr | Breakeven rate (% / yr) |")
    lines.append("|---:|---:|---|---|---:|")
    for b in breakevens:
        be_str = f"{b['breakeven_rate_per_yr']*100:.2f}%" if b['breakeven_rate_per_yr'] is not None else "no switch"
        lines.append(
            f"| {b['reactor_kwe']:.0f} | {b['chunk_t']:.0f} | "
            f"{b['winner_at_zero_perm']} | {b['winner_at_2pct']} | {be_str} |"
        )

    lines.append("\n### All-electric Kilopower (10 kWe) at 100 t chunk: sweep specific impulse vs permeability\n")
    lines.append("Delivered mass after permeability tax. Burn time in parens.\n")
    lines.append("| Specific impulse (s) | 0% / yr | 0.5% / yr | 0.65% / yr | 1.0% / yr | 2.0% / yr |")
    lines.append("|---:|---|---|---|---|---|")
    for isp in ELECTRIC_ISPS:
        ae = all_electric_uncapped(10.0, 100.0, isp)
        if not ae.get("feasible"):
            row = [f"{isp:.0f}"] + ["-"] * len(PERM_RATES_PER_YR)
        else:
            row = [f"{isp:.0f}"]
            for rate in PERM_RATES_PER_YR:
                d_after = apply_permeability(ae["delivered_t_raw"], ae["burn_time_yr"], rate)
                row.append(f"{d_after:.1f} t ({ae['burn_time_yr']:.1f} yr)")
        lines.append("| " + " | ".join(row) + " |")

    (results_dir / "tables.md").write_text("\n".join(lines))
    return out


if __name__ == "__main__":
    out = main()
    print(f"Sweep complete. {len(out['grid'])} cells.")
    print(f"  Wrote results/bag_perm.json and results/tables.md")
