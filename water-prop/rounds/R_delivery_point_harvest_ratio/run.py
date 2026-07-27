"""R-delivery-point-harvest-ratio — where is the depot prize?

Maps the Saturn-water harvest ratio (water harvested / t delivered) across the
delivery-point spectrum (Saturn-orbit depot -> heliocentric-at-Saturn -> cislunar
-> LEO), reusing the Round H mass cascade, to pinpoint where the depot pivot pays
off and to decompose the penalty into its departure-leg and capture-leg halves.

Pre-registered H-I1..H-I3. See SCOPE.md. Deterministic.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent

G0 = 9.80665
MU_E = 398600.4418
R_LEO = 6578.0
VINF_E = 10.3
ISP_CHEM = 420.0
VE = ISP_CHEM * G0
P_CHEM = 350.0                # kWe electrolysis reactor
M_DRY = 15.0 + 2.7           # base + electrolysis plant/engine (t)
TANK_FRAC = 0.05             # cryo H2/O2 tank fraction
CAP_DRY_FRAC, CAP_DRY_FIXED = 0.05, 0.5

# Earth-capture Δv (km/s) by target orbit
v_hyp_leo = math.sqrt(VINF_E ** 2 + 2 * MU_E / R_LEO)
DV_CAP_LEO = v_hyp_leo - math.sqrt(MU_E / R_LEO)          # to LEO circular (7.29)
DV_CAP_BARELY = v_hyp_leo - math.sqrt(2 * MU_E / R_LEO)   # barely bound / cislunar (4.07)

DELIVERY = {  # name: (departure_km_s, earth_capture_km_s, earth_transit?)
    "Saturn ring/orbit depot": (2.0, 0.0, False),
    "heliocentric-at-Saturn":  (8.5, 0.0, False),
    "Earth cislunar/high-ell": (8.5, DV_CAP_BARELY, True),
    "LEO":                     (8.5, DV_CAP_LEO, True),
}


def transport_prop(D, sp, dv_dep_kms):
    """Fixed-point departure/transport propellant to accelerate D + dry + reactor
    + tanks through dv_dep (H2/O2)."""
    m_reactor = P_CHEM * 1000.0 / sp / 1000.0
    m_inbound = D + M_DRY + m_reactor
    prop = 0.0
    for _ in range(200):
        m_burnout = m_inbound + TANK_FRAC * prop
        new = m_burnout * (math.exp(dv_dep_kms * 1000.0 / VE) - 1.0)
        if abs(new - prop) < 1e-6:
            prop = new
            break
        prop = new
    return prop, m_reactor


def capture_prop(D, dv_cap_kms):
    if dv_cap_kms <= 0:
        return 0.0
    cap_dry = CAP_DRY_FRAC * D + CAP_DRY_FIXED
    return (D + cap_dry) * (math.exp(dv_cap_kms * 1000.0 / VE) - 1.0)


def main():
    D = 30.0
    out = {"anchors": {"D_t": D, "isp_chem": ISP_CHEM, "P_kwe": P_CHEM,
                       "dv_cap_leo": DV_CAP_LEO, "dv_cap_cislunar": DV_CAP_BARELY},
           "grid": {}}
    for sp in (2.4, 40.0):
        rows = {}
        for name, (dv_dep, dv_cap, transit) in DELIVERY.items():
            dep, m_reactor = transport_prop(D, sp, dv_dep)
            cap = capture_prop(D, dv_cap)
            harvest = dep + cap
            rows[name] = {"dv_dep": dv_dep, "dv_cap": dv_cap, "reactor_t": round(m_reactor, 1),
                          "dep_prop_t": round(dep), "cap_prop_t": round(cap),
                          "harvest_ratio": round(harvest / D, 1),
                          "delivery_eff_pct": round(100 * D / harvest, 2) if harvest > 0 else None,
                          "earth_transit": transit,
                          "capture_share_of_penalty_pct": round(100 * cap / harvest, 0) if harvest > 0 else 0}
        out["grid"][f"sp_{sp}"] = rows

    g24 = out["grid"]["sp_2.4"]
    # H-I1: monotonic drop toward source
    order = ["LEO", "Earth cislunar/high-ell", "heliocentric-at-Saturn", "Saturn ring/orbit depot"]
    ratios = [g24[n]["harvest_ratio"] for n in order]
    hi1 = all(ratios[i] > ratios[i + 1] for i in range(len(ratios) - 1)) and g24["Saturn ring/orbit depot"]["harvest_ratio"] < 5
    # H-I2: Earth-vicinity stays >25:1; LEO->cislunar only ~halves
    hi2 = (g24["Earth cislunar/high-ell"]["harvest_ratio"] > 25 and
           g24["heliocentric-at-Saturn"]["harvest_ratio"] >= 10)
    # H-I3: Saturn-orbit depot <=3:1 at any sp
    hi3 = (g24["Saturn ring/orbit depot"]["harvest_ratio"] <= 3 and
           out["grid"]["sp_40.0"]["Saturn ring/orbit depot"]["harvest_ratio"] <= 3)
    out["decomposition"] = {
        "LEO_ratio": g24["LEO"]["harvest_ratio"],
        "cislunar_ratio": g24["Earth cislunar/high-ell"]["harvest_ratio"],
        "LEO_to_cislunar_saving_x": round(g24["LEO"]["harvest_ratio"] / g24["Earth cislunar/high-ell"]["harvest_ratio"], 2),
        "heliocentric_ratio": g24["heliocentric-at-Saturn"]["harvest_ratio"],
        "saturn_depot_ratio": g24["Saturn ring/orbit depot"]["harvest_ratio"],
        "note": "departure leg (8.5 km/s) is paid for all Earth-vicinity delivery; "
                "moving LEO->cislunar only removes the capture-leg part"}
    out["verdicts"] = {"H-I1": hi1, "H-I2": hi2, "H-I3": hi3,
                       "held": sum([hi1, hi2, hi3]), "of": 3}
    return out


if __name__ == "__main__":
    r = main()
    (HERE / "results").mkdir(exist_ok=True)
    json.dump(r, open(HERE / "results" / "delivery_point.json", "w"), indent=2)
    v = r["verdicts"]
    print("Harvest ratio by delivery point (D=30 t, H2/O2 stage):")
    print(f"  {'delivery point':26} | {'2.4 W/kg':>10} | {'40 W/kg':>9} | capture-share")
    for name in ["Saturn ring/orbit depot", "heliocentric-at-Saturn", "Earth cislunar/high-ell", "LEO"]:
        a = r["grid"]["sp_2.4"][name]; b = r["grid"]["sp_40.0"][name]
        print(f"  {name:26} | {a['harvest_ratio']:>8.1f}:1 | {b['harvest_ratio']:>7.1f}:1 | "
              f"{a['capture_share_of_penalty_pct']:.0f}%")
    d = r["decomposition"]
    print()
    print(f"H-I1  monotonic drop toward source; Saturn-depot <5:1 -> {v['H-I1']}")
    print(f"H-I2  LEO {d['LEO_ratio']}:1 -> cislunar {d['cislunar_ratio']}:1 is only "
          f"{d['LEO_to_cislunar_saving_x']}x (departure 8.5 km/s is the other half); "
          f"Earth-vicinity stays >25:1 -> {v['H-I2']}")
    print(f"H-I3  Saturn-orbit depot {d['saturn_depot_ratio']}:1 (deep-well penalty gone; "
          f"but rests on demand AT Saturn) -> {v['H-I3']}")
    print(f"\nHELD {v['held']}/{v['of']}")
