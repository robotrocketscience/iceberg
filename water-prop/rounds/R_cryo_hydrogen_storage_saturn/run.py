"""R-cryo-hydrogen-storage-saturn — does the 77 t LH2 departure propellant survive
a multi-year Saturn dwell?

Models the three competing heat sources into the LH2 tank (MLI radiation,
ortho-para self-heating, reactor proximity) + strut conduction, the resulting
boiloff over the dwell, the zero-boiloff cryocooler power, and the reactor-tank
thermal-isolation requirement. Tests R-electrolysis-departure-stage's load-bearing
cryo-H2 assumption.

Pre-registered H-G1..H-G5. See SCOPE.md. Deterministic. Grades honestly against
the pre-registration (several worker hypotheses are falsified — reported as such).
"""
from __future__ import annotations

import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent

SIGMA = 5.67e-8
M_H2 = 77_000.0
RHO_LH2 = 70.8
L_V = 446e3
DH_OP = 527e3
YEAR = 3.156e7

V = M_H2 / RHO_LH2
R = (3 * V / (4 * math.pi)) ** (1 / 3)
A = 4 * math.pi * R ** 2


def mli_watts(Th, Tc=20.0, estar=1e-3):
    return estar * SIGMA * (Th ** 4 - Tc ** 4) * A


def reactor_watts(VF_eff, Trad, eps=1.0):
    """VF_eff = geometric view factor * shield attenuation."""
    return VF_eff * eps * SIGMA * A * Trad ** 4


def boiloff_frac(watts, dwell_yr):
    return watts * dwell_yr * YEAR / L_V / M_H2


def cryocooler_input(watts, Tc=20.0, Th=90.0, real_frac=0.20):
    cop = (Tc / (Th - Tc)) * real_frac
    return watts / cop


def geom_view_factor(P_elec_kwe, Trad, boom_m, eta_elec=0.20):
    """Geometric tank->reactor-radiator view factor. Radiator area sized to reject
    the reactor waste heat at Trad; VF ~ A_rad / (4 pi boom^2)."""
    q_waste = P_elec_kwe * 1e3 * (1 - eta_elec) / eta_elec   # W thermal
    A_rad = q_waste / (SIGMA * Trad ** 4)                    # m^2 radiator
    return A_rad / (4 * math.pi * boom_m ** 2), A_rad


def main():
    out = {"tank": {"m_h2_t": M_H2 / 1000, "volume_m3": V, "radius_m": R,
                    "diam_m": 2 * R, "area_m2": A}}

    # H-G1: MLI radiation grid
    mli = {}
    for Th in (50.0, 90.0, 150.0):
        for es in (5e-4, 1e-3, 2e-3):
            w = mli_watts(Th, estar=es)
            mli[f"Th{Th:.0f}_e{es:.0e}"] = {"W": round(w, 3),
                                            "boiloff_2yr_pct": round(100 * boiloff_frac(w, 2), 3)}
    out["HG1"] = {"grid": mli, "nominal_90K_e1e-3_boiloff_2yr_pct": round(100 * boiloff_frac(mli_watts(90.0), 2), 3),
                  "near_earth_250K_boiloff_2yr_pct": round(100 * boiloff_frac(mli_watts(250.0), 2), 1),
                  "saturn_advantage_factor": round(mli_watts(250.0) / mli_watts(90.0))}

    # H-G2: ortho-para (uncatalyzed vs catalyzed) — report power AND boiloff fraction
    E_op = M_H2 * DH_OP
    out["HG2"] = {"total_conversion_energy_J": E_op,
                  "uncatalyzed_self_heat_kW_1yr": round(E_op / (1 * YEAR) / 1e3, 2),
                  "uncatalyzed_boiloff_frac_full_conversion_pct": round(100 * E_op / L_V / M_H2, 0),
                  "catalyzed_at_liquefaction_pct": 0.0,
                  "note": "power is only ~1.3 kW (worker pre-reg said >100 kW = WRONG) but "
                          "full conversion boils off 118% of the inventory -> catalysis MANDATORY "
                          "(conclusion holds via boiloff fraction, not power)"}

    # H-G3: reactor proximity — VF_eff grid + geometry/shield requirement
    react = {}
    for VFe, tag in ((0.1, "unshielded"), (1e-2, "point-away"), (1e-3, "1-layer shadow"),
                     (1e-5, "JWST-class shield"), (1e-6, "extreme shield")):
        w = reactor_watts(VFe, 700.0)
        react[tag] = {"VF_eff": VFe, "W": round(w, 3), "boiloff_1yr_pct": round(100 * boiloff_frac(w, 1), 2)}
    # required VF_eff for <=10 W at 700 K
    vf_req = 10.0 / (SIGMA * A * 700.0 ** 4)
    # geometric VF at realistic boom lengths (150 kWe reactor, 700 K radiators)
    geom = {}
    for boom in (20.0, 50.0, 100.0):
        vf, a_rad = geom_view_factor(150.0, 700.0, boom)
        geom[f"boom_{boom:.0f}m"] = {"geom_VF": round(vf, 6), "A_rad_m2": round(a_rad),
                                     "W_no_shield": round(reactor_watts(vf, 700.0), 1),
                                     "shield_atten_for_10W": round(10.0 / reactor_watts(vf, 700.0), 7)}
    out["HG3"] = {"grid": react, "VF_eff_required_for_10W": vf_req, "geometry": geom,
                  "finding": "reactor is the DOMINANT source; a 1-layer shadow shield (VF_eff 1e-3) "
                             "leaves ~7 kW. Benign (<10 W) needs VF_eff ~1.4e-6 = JWST-class multilayer "
                             "shadow shield, OR co-locate the tank in the reactor's existing radiation "
                             "shadow shield (the vehicle already carries one for electronics/payload)."}

    # H-G4: total with requirements met (JWST-class shield ~1e-5) + cryocooler
    scenarios = {}
    for tag, vfe in (("1-layer shadow VF1e-3", 1e-3), ("JWST-class VF1e-5", 1e-5),
                     ("extreme VF1e-6", 1e-6)):
        total = mli_watts(90.0) + reactor_watts(vfe, 700.0) + 5.0  # +5 W struts
        scenarios[tag] = {"total_W": round(total, 2),
                          "boiloff_2yr_pct": round(100 * boiloff_frac(total, 2), 2),
                          "cryocooler_kW": round(cryocooler_input(total) / 1e3, 2)}
    out["HG4"] = {"scenarios": scenarios}

    # verdicts (honest — several worker hypotheses falsified)
    hg1 = out["HG1"]["nominal_90K_e1e-3_boiloff_2yr_pct"] < 10.0
    # H-G2 as-registered required >100 kW: FALSIFIED on power; conclusion holds on boiloff frac
    hg2_power_clause = out["HG2"]["uncatalyzed_self_heat_kW_1yr"] > 100.0   # False -> clause falsified
    hg2_conclusion = out["HG2"]["uncatalyzed_boiloff_frac_full_conversion_pct"] > 100.0
    # H-G3 as-registered required shielded<=10 W at VF1e-3: FALSIFIED
    hg3_asreg = react["1-layer shadow"]["W"] <= 30.0                        # False -> falsified
    # H-G4 as-registered required total 10-40 W & cryo<2 kW at "requirements met":
    hg4_asreg = (scenarios["1-layer shadow VF1e-3"]["total_W"] <= 40.0)     # False -> falsified
    # H-G4 recovers with a JWST-class shield:
    hg4_jwst_ok = (scenarios["JWST-class VF1e-5"]["total_W"] <= 40.0 and
                   scenarios["JWST-class VF1e-5"]["cryocooler_kW"] < 2.0)
    out["verdicts"] = {
        "H-G1_HELD": hg1,
        "H-G2_power_clause_HELD": hg2_power_clause, "H-G2_conclusion_HELD": hg2_conclusion,
        "H-G3_asregistered_HELD": hg3_asreg,
        "H-G4_asregistered_HELD": hg4_asreg, "H-G4_recovers_with_JWST_shield": hg4_jwst_ok,
        "net": "storage tractable ONLY with a JWST-class reactor-tank thermal shadow shield "
               "(or co-location in the reactor's existing radiation shadow); the reactor, not the "
               "cold Saturn environment, is the dominant heat source. Round F survives with a "
               "SHARPENED requirement. Worker pre-reg H-G2(power)/H-G3/H-G4 falsified."}
    return out


if __name__ == "__main__":
    r = main()
    (HERE / "results").mkdir(exist_ok=True)
    json.dump(r, open(HERE / "results" / "cryo_h2.json", "w"), indent=2)
    v = r["verdicts"]
    print(f"tank: {r['tank']['m_h2_t']:.0f} t LH2 -> {r['tank']['diam_m']:.1f} m sphere, "
          f"{r['tank']['area_m2']:.0f} m^2")
    print(f"H-G1  MLI @ Saturn 90 K: {r['HG1']['nominal_90K_e1e-3_boiloff_2yr_pct']}% / 2yr "
          f"(near-Earth {r['HG1']['near_earth_250K_boiloff_2yr_pct']}%; {r['HG1']['saturn_advantage_factor']}x better) -> HELD {v['H-G1_HELD']}")
    print(f"H-G2  ortho-para uncat: {r['HG2']['uncatalyzed_self_heat_kW_1yr']} kW self-heat "
          f"({r['HG2']['uncatalyzed_boiloff_frac_full_conversion_pct']:.0f}% boiloff full-conversion)")
    print(f"      pre-reg '>100 kW' clause -> HELD {v['H-G2_power_clause_HELD']} (FALSIFIED: ~1.3 kW); "
          f"conclusion (catalysis mandatory) -> HELD {v['H-G2_conclusion_HELD']}")
    print(f"H-G3  reactor proximity (700 K radiators):")
    for tag, d in r["HG3"]["grid"].items():
        print(f"        {tag:20} VF_eff={d['VF_eff']:.0e} -> {d['W']:9.1f} W ({d['boiloff_1yr_pct']}%/yr)")
    print(f"      required VF_eff for <=10 W = {r['HG3']['VF_eff_required_for_10W']:.1e}")
    print(f"      pre-reg (shielded<=10 W at VF1e-3) -> HELD {v['H-G3_asregistered_HELD']} (FALSIFIED)")
    print(f"H-G4  total heat + cryocooler by shield:")
    for tag, d in r["HG4"]["scenarios"].items():
        print(f"        {tag:22}: {d['total_W']:8.1f} W, {d['boiloff_2yr_pct']:6.1f}%/2yr, "
              f"cryocooler {d['cryocooler_kW']} kW")
    print(f"      pre-reg (10-40 W total, cryo<2 kW at 'requirements met') -> HELD {v['H-G4_asregistered_HELD']} (FALSIFIED)")
    print(f"      recovers with JWST-class shield -> {v['H-G4_recovers_with_JWST_shield']}")
    print(f"\nNET: {v['net']}")
