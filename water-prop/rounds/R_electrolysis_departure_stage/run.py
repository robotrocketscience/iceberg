"""R-electrolysis-departure-stage — does a reactor-charged H2/O2 departure stage
relieve the megawatt departure?

Evaluates the high-thrust departure lever: the reactor electrolyzes harvested
water into H2/O2 over the Saturn dwell (average power), then a high-thrust engine
does the Oberth-efficient impulsive 8.5 km/s departure — vs the electric
low-thrust spiral (Round C, 1248 kWe / 1531 t water). Also checks the water
thermal-steam alternative and the cryo-storage-vs-power-spike tension.

Pre-registered H-F1..H-F4. See SCOPE.md. Deterministic.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent

G0 = 9.80665
MU_S = 3.793e16
R_RING = 1.07e8
VINF = 6210.0
YEAR = 3.156e7

V_CIRC = math.sqrt(MU_S / R_RING)
V_HYP = math.sqrt(VINF ** 2 + 2 * MU_S / R_RING)
DV_IMPULSIVE = V_HYP - V_CIRC          # chemical/thermal high-thrust, Oberth at ring
DV_ELECTRIC_SPIRAL = 21900.0          # Round C continuous electric spiral
M_F = 100_000.0                       # kg mass continuing inbound (delivered chunk + dry)
E_ELECTROLYSIS = 20e6                 # J/kg water (~70% efficient)


def prop(dv, isp, m_f=M_F):
    return m_f * (math.exp(dv / (isp * G0)) - 1.0)


def delivery_eff(prop_dep, m_f=M_F):
    """departure-leg mass efficiency = payload / (payload + departure propellant)."""
    return m_f / (m_f + prop_dep)


def main():
    out = {"anchors": {"dv_impulsive_kms": DV_IMPULSIVE / 1000,
                       "dv_electric_spiral_kms": DV_ELECTRIC_SPIRAL / 1000,
                       "v_circ": V_CIRC, "v_hyp": V_HYP, "m_f_t": M_F / 1000}}

    # --- architectures ---
    arch = {}
    # 1. electric low-thrust spiral (baseline, Round C)
    p_e = prop(DV_ELECTRIC_SPIRAL, 800.0)
    arch["electric_spiral"] = {"dv_kms": DV_ELECTRIC_SPIRAL / 1000, "isp": 800,
                               "prop_t": p_e / 1000, "reactor_kwe": 1248,
                               "reactor_note": "PEAK, 2-yr continuous departure burn",
                               "delivery_eff": delivery_eff(p_e),
                               "added_dry_t": 0.0, "risk": "megawatt reactor; retired-as-fantasy band"}
    # 2. reactor-charged H2/O2 chemical impulsive
    for isp in (380.0, 420.0, 450.0):
        p = prop(DV_IMPULSIVE, isp)
        E = p * E_ELECTROLYSIS
        m_h2, m_o2 = p * 2 / 18, p * 16 / 18
        power = {f"dwell_{d:.0f}yr_kwe": round(E / (d * YEAR) / 1e3) for d in (1, 2, 3)}
        # added dry mass: electrolysis plant (~10 kg/kW at the 2-yr-dwell power) +
        # cryo tanks (H2 ~13% of H2 mass, O2 ~4% of O2 mass) + engine (~0.5 t)
        plant_t = 10.0 * (E / (2 * YEAR) / 1e3) / 1000        # 10 kg/kW at 2-yr dwell power
        tank_t = (0.13 * m_h2 + 0.04 * m_o2) / 1000
        engine_t = 0.5
        added = plant_t + tank_t + engine_t
        arch[f"h2o2_isp{isp:.0f}"] = {
            "dv_kms": DV_IMPULSIVE / 1000, "isp": isp, "prop_t": p / 1000,
            "h2_t": m_h2 / 1000, "o2_t": m_o2 / 1000,
            "reactor_kwe_by_dwell": power, "reactor_note": "AVERAGE, electrolysis over dwell",
            "delivery_eff": delivery_eff(p),
            "added_dry_t": round(added, 1),
            "added_breakdown_t": {"electrolysis_plant": round(plant_t, 1),
                                  "cryo_tanks_jettisonable": round(tank_t, 1),
                                  "engine": engine_t},
            "risk": "cryo H2 storage (77 t H2 at 20 K over the dwell) is first-order"}
    # 3. reactor-thermal steam (no electrolysis, no cryo, but low Isp)
    p_t = prop(DV_IMPULSIVE, 190.0)
    arch["thermal_steam_isp190"] = {"dv_kms": DV_IMPULSIVE / 1000, "isp": 190,
                                    "prop_t": p_t / 1000, "delivery_eff": delivery_eff(p_t),
                                    "reactor_note": "thrust from heating stored liquid water — no cryo",
                                    "risk": "Isp too low -> propellant-prohibitive"}
    out["architectures"] = arch

    # --- Kilopower window: dwell for electrolysis at 30 kWe ---
    E420 = prop(DV_IMPULSIVE, 420.0) * E_ELECTROLYSIS
    out["kilopower_window_yr"] = E420 / 30e3 / YEAR

    # --- cryo-vs-power tension: just-in-time electrolysis spike ---
    jit = {}
    for window_days in (30, 90, 180):
        jit[f"{window_days}d"] = round(E420 / (window_days * 86400) / 1e3)
    out["just_in_time_electrolysis_kwe"] = jit  # avoid H2 storage -> power spikes

    # --- headline framing: departure propellant dwarfs payload either way ---
    out["delivery_framing"] = {
        "electric_departure_leg_eff": round(delivery_eff(p_e), 3),
        "h2o2_isp420_departure_leg_eff": round(delivery_eff(prop(DV_IMPULSIVE, 420.0)), 3),
        "note": "Saturn's deep well makes chunk-return departure intrinsically "
                "propellant-hungry; H2/O2 roughly doubles the departure-leg mass "
                "efficiency vs the electric spiral, but both are single-digit-to-teens %"}

    # --- verdicts ---
    p_chem_min = min(prop(DV_IMPULSIVE, i) for i in (380, 420, 450))
    p_chem_max = max(prop(DV_IMPULSIVE, i) for i in (380, 420, 450))
    hf1 = p_chem_max < p_e                                     # chemical < electric
    kwe_1yr = prop(DV_IMPULSIVE, 420.0) * E_ELECTROLYSIS / (1 * YEAR) / 1e3
    kwe_3yr = prop(DV_IMPULSIVE, 420.0) * E_ELECTROLYSIS / (3 * YEAR) / 1e3
    hf2 = (100.0 <= kwe_3yr) and (kwe_1yr < 1248)             # few-hundred kWe, not Kilopower, < electric
    hf3 = arch["h2o2_isp420"]["added_dry_t"] >= 1.0 and out["kilopower_window_yr"] > 10
    hf4 = (kwe_3yr >= 40.0)                                    # not relieved to Kilopower (<40 kWe)
    out["verdicts"] = {"H-F1": hf1, "H-F2": hf2, "H-F3": hf3, "H-F4": hf4,
                       "held": sum([hf1, hf2, hf3, hf4]), "of": 4}
    return out


if __name__ == "__main__":
    r = main()
    (HERE / "results").mkdir(exist_ok=True)
    json.dump(r, open(HERE / "results" / "electrolysis_departure.json", "w"), indent=2)
    v = r["verdicts"]
    a = r["architectures"]
    print("Departure architecture trade (Δv / Isp / water prop / reactor / delivery-eff):")
    e = a["electric_spiral"]
    print(f"  electric spiral : {e['dv_kms']:.1f} km/s Isp 800 -> {e['prop_t']:5.0f} t water, "
          f"{e['reactor_kwe']} kWe PEAK, eff {e['delivery_eff']:.1%}")
    h = a["h2o2_isp420"]
    print(f"  H2/O2 Isp 420   : {h['dv_kms']:.2f} km/s -> {h['prop_t']:5.0f} t water, "
          f"reactor {h['reactor_kwe_by_dwell']} AVG, eff {h['delivery_eff']:.1%}, "
          f"+{h['added_dry_t']} t dry")
    t = a["thermal_steam_isp190"]
    print(f"  thermal steam   : Isp 190 -> {t['prop_t']:5.0f} t water (prohibitive), eff {t['delivery_eff']:.1%}")
    print()
    print(f"H-F1  chemical water prop < electric ({a['h2o2_isp420']['prop_t']:.0f} vs "
          f"{e['prop_t']:.0f} t) -> {v['H-F1']}")
    print(f"H-F2  electrolysis reactor few-hundred kWe not Kilopower "
          f"(1yr {r['just_in_time_electrolysis_kwe']}; Kilopower-window "
          f"{r['kilopower_window_yr']:.0f} yr) -> {v['H-F2']}")
    print(f"      (H2/O2 reactor by dwell: {h['reactor_kwe_by_dwell']})")
    print(f"H-F3  added dry {h['added_dry_t']} t {h['added_breakdown_t']}; "
          f"cryo H2 {h['h2_t']:.0f} t -> {v['H-F3']}")
    print(f"      just-in-time electrolysis (avoid cryo) spikes power: "
          f"{r['just_in_time_electrolysis_kwe']} kWe -> cryo storage is forced")
    print(f"H-F4  not relieved to Kilopower class -> {v['H-F4']}")
    print(f"\nHELD {v['held']}/{v['of']}")
