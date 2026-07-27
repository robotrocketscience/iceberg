"""R-roundtrip-closure-departure-stage — does the H2/O2 departure stage help the
round-trip, or does its mass eat the gains?

Backward mass cascade (departure + Earth-capture legs, both paid with harvested
water) comparing the H2/O2 departure stage vs all-electric, across delivered chunk
mass x reactor specific power. Metric: harvest ratio (water harvested at Saturn
per tonne delivered to Earth) and delivery efficiency.

Pre-registered H-H1..H-H4. See SCOPE.md. Deterministic.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent

G0 = 9.80665
ISP_CHEM, ISP_ELEC = 420.0, 800.0
VE_CHEM, VE_ELEC = ISP_CHEM * G0, ISP_ELEC * G0
DV_DEP_CHEM, DV_DEP_ELEC = 8500.0, 21900.0
DV_EARTH_CAP = 7300.0
P_CHEM, P_ELEC = 350.0, 1248.0        # kWe
M_DRY_BASE = 15.0                     # t (structure, electric thruster, comms, capture hardware)
PLANT_ENGINE = 2.7                    # t (electrolysis plant + H2/O2 engine, carried inbound, chem only)
TANK_FRAC_CRYO, TANK_FRAC_WATER = 0.05, 0.03
CAP_DRY_FRAC = 0.05                   # Earth-capture stage dry as fraction of chunk
CAP_DRY_FIXED = 0.5                   # t


def departure_prop(D, sp, chem):
    """Fixed-point cascade for departure propellant (tanks jettisoned at burnout)."""
    ve = VE_CHEM if chem else VE_ELEC
    dv = DV_DEP_CHEM if chem else DV_DEP_ELEC
    P = P_CHEM if chem else P_ELEC
    m_reactor = P * 1000.0 / sp / 1000.0
    m_inbound = D + M_DRY_BASE + (PLANT_ENGINE if chem else 0.0) + m_reactor
    tank_frac = TANK_FRAC_CRYO if chem else TANK_FRAC_WATER
    prop = 0.0
    for _ in range(200):
        m_burnout = m_inbound + tank_frac * prop      # tanks sized to propellant
        new = m_burnout * (math.exp(dv / ve) - 1.0)
        if abs(new - prop) < 1e-6:
            prop = new
            break
        prop = new
    return prop, m_reactor


def earth_capture_prop(D):
    """H2/O2 impulsive capture of the released chunk at Earth (electrolyzed in
    the 6-yr inbound cruise -> low power, not a reactor driver)."""
    cap_dry = CAP_DRY_FRAC * D + CAP_DRY_FIXED
    return (D + cap_dry) * (math.exp(DV_EARTH_CAP / VE_CHEM) - 1.0)


def cascade(D, sp, chem):
    dep, m_reactor = departure_prop(D, sp, chem)
    cap = earth_capture_prop(D)
    harvest = dep + cap
    return {"chem": chem, "D_t": D, "sp": sp, "reactor_t": round(m_reactor, 1),
            "dep_prop_t": round(dep), "cap_prop_t": round(cap), "harvest_t": round(harvest),
            "harvest_ratio": round(harvest / D, 1),
            "delivery_eff_pct": round(100 * D / harvest, 2),
            "closes_positive": harvest > 0 and m_reactor < 1e6}


def main():
    out = {"anchors": {"dv_dep_chem": DV_DEP_CHEM, "dv_dep_elec": DV_DEP_ELEC,
                       "dv_earth_cap": DV_EARTH_CAP, "isp_chem": ISP_CHEM, "isp_elec": ISP_ELEC,
                       "P_chem_kwe": P_CHEM, "P_elec_kwe": P_ELEC}}
    grid = []
    for D in (20.0, 30.0, 50.0):
        for sp in (2.4, 10.0, 40.0):
            grid.append(cascade(D, sp, True))
            grid.append(cascade(D, sp, False))
    out["grid"] = grid

    def get(D, sp, chem):
        return next(g for g in grid if g["D_t"] == D and g["sp"] == sp and g["chem"] == chem)

    # H-H1: H2/O2 harvest ratio much lower than electric at flown sp (D=30)
    c = get(30, 2.4, True); e = get(30, 2.4, False)
    out["HH1"] = {"h2o2_ratio_2.4": c["harvest_ratio"], "electric_ratio_2.4": e["harvest_ratio"],
                  "improvement_x": round(e["harvest_ratio"] / c["harvest_ratio"], 1)}
    # H-H2: reactor mass dominant at flown sp
    out["HH2"] = {"reactor_h2o2_2.4_t": c["reactor_t"], "reactor_electric_2.4_t": e["reactor_t"],
                  "delivered_chunk_t": 30}
    # H-H3: closure — H2/O2 poor-but-positive at flown; both improve at aspirational
    out["HH3"] = {"h2o2_2.4_ratio": c["harvest_ratio"], "h2o2_2.4_delivery_pct": c["delivery_eff_pct"],
                  "electric_2.4_ratio": e["harvest_ratio"],
                  "h2o2_40_ratio": get(30, 40, True)["harvest_ratio"],
                  "h2o2_40_delivery_pct": get(30, 40, True)["delivery_eff_pct"]}
    # H-H4: does H2/O2 reach viable (<10:1) at flown 2.4? at aspirational 40?
    out["HH4"] = {"h2o2_viable_lt10to1_at_2.4": get(30, 2.4, True)["harvest_ratio"] < 10,
                  "h2o2_viable_lt10to1_at_40": get(30, 40, True)["harvest_ratio"] < 10,
                  "min_h2o2_ratio_over_grid": min(g["harvest_ratio"] for g in grid if g["chem"]),
                  "note": "intrinsic round-trip cost: Δv at BOTH ends of a deep-well round-trip"}

    hh1 = (c["harvest_ratio"] <= 50 and e["harvest_ratio"] > 150 and
           e["harvest_ratio"] / c["harvest_ratio"] >= 2)
    hh2 = c["reactor_t"] >= 100 and e["reactor_t"] >= 400
    hh3 = (c["closes_positive"] and 20 <= c["harvest_ratio"] <= 80 and e["harvest_ratio"] > 150)
    hh4 = get(30, 2.4, True)["harvest_ratio"] >= 10   # NOT viable at flown -> bet #3 mass wall binds
    out["verdicts"] = {"H-H1": hh1, "H-H2": hh2, "H-H3": hh3, "H-H4": hh4,
                       "held": sum([hh1, hh2, hh3, hh4]), "of": 4}
    return out


if __name__ == "__main__":
    r = main()
    (HERE / "results").mkdir(exist_ok=True)
    json.dump(r, open(HERE / "results" / "roundtrip.json", "w"), indent=2)
    v = r["verdicts"]
    print("Round-trip harvest ratio (water harvested / tonne delivered), D=30 t:")
    print(f"  {'sp W/kg':>8} | {'H2/O2 reactor':>13} {'ratio':>7} {'deliv%':>7} | "
          f"{'electric reactor':>16} {'ratio':>7}")
    for sp in (2.4, 10.0, 40.0):
        c = next(g for g in r["grid"] if g["D_t"] == 30 and g["sp"] == sp and g["chem"])
        e = next(g for g in r["grid"] if g["D_t"] == 30 and g["sp"] == sp and not g["chem"])
        print(f"  {sp:>8.1f} | {c['reactor_t']:>10.0f} t {c['harvest_ratio']:>7.1f} "
              f"{c['delivery_eff_pct']:>6.1f}% | {e['reactor_t']:>13.0f} t {e['harvest_ratio']:>7.1f}")
    print()
    print(f"H-H1  H2/O2 {r['HH1']['h2o2_ratio_2.4']}:1 vs electric {r['HH1']['electric_ratio_2.4']}:1 "
          f"({r['HH1']['improvement_x']}x better) -> {v['H-H1']}")
    print(f"H-H2  reactor mass at 2.4 W/kg: H2/O2 {r['HH2']['reactor_h2o2_2.4_t']} t / "
          f"electric {r['HH2']['reactor_electric_2.4_t']} t (chunk 30 t) -> {v['H-H2']}")
    print(f"H-H3  H2/O2 closes at flown: {r['HH3']['h2o2_2.4_ratio']}:1 ({r['HH3']['h2o2_2.4_delivery_pct']}% deliv); "
          f"electric {r['HH3']['electric_2.4_ratio']}:1 -> {v['H-H3']}")
    print(f"H-H4  H2/O2 NOT viable (<10:1) at flown 2.4 ({r['HH4']['h2o2_viable_lt10to1_at_2.4']}); "
          f"at aspirational 40 W/kg = {r['HH3']['h2o2_40_ratio']}:1 "
          f"(viable {r['HH4']['h2o2_viable_lt10to1_at_40']}); "
          f"min over grid {r['HH4']['min_h2o2_ratio_over_grid']}:1 -> {v['H-H4']}")
    print(f"\nHELD {v['held']}/{v['of']}")
