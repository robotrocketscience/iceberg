"""R-eccentric-harvest-departure — does an eccentric harvest orbit rescue the
megawatt departure floor?

(1) Harvest-from-eccentric is killed by the ring relative velocity (gentle
capture needs velocity-matching ~m/s; eccentric periapsis is km/s). (2) But
departing the required CIRCULAR orbit via periapsis-concentrated burns recovers
Oberth (Δv ~8.5 not 21.9 km/s, correcting Round C's continuous-spiral 1248 kWe);
this sim pins the duty-cycle peak-power penalty.

Pre-registered H-D1..H-D4. See SCOPE.md. Deterministic.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent

G0 = 9.80665
MU_S = 3.793e16
R_RING = 1.07e8
R_TITAN = 1.2217e9
VINF = 6210.0
VE_MET = 800.0 * G0
ETA = 0.6
YEAR = 3.156e7
M = 100_000.0

V_CIRC = math.sqrt(MU_S / R_RING)
V_ESC = math.sqrt(2 * MU_S / R_RING)
V_HYP = math.sqrt(VINF ** 2 + 2 * MU_S / R_RING)      # periapsis speed for hyperbolic v_inf
DV_IMPULSIVE = V_HYP - V_CIRC


def v_peri(r_a):
    a = (R_RING + r_a) / 2.0
    return math.sqrt(MU_S * (2.0 / R_RING - 1.0 / a))


def peak_power_kwe(F):
    """Peak electrical power for constant thrust F (during firing): 0.5 m_dot v_e^2 / eta,
    m_dot = F / v_e -> 0.5 F v_e / eta."""
    return 0.5 * F * VE_MET / ETA / 1e3


def periapsis_burn_departure(F, m=M, r_burn_mult=2.0, max_years=60.0, max_revs=2_000_000):
    """From the circular ring orbit, fire constant thrust F only within r < r_burn
    near periapsis each pass (Oberth burn at r_p). Raise apoapsis until escape,
    then complete to v_inf. Return totals."""
    a_thrust = F / m
    r_burn = r_burn_mult * R_RING
    v_p = V_CIRC
    dv_total = 0.0
    elapsed = 0.0
    firing = 0.0
    revs = 0
    while True:
        E = 0.5 * v_p ** 2 - MU_S / R_RING
        if E >= 0.0:                       # escaped to >= parabolic
            break
        a_sma = -MU_S / (2.0 * E)
        e = 1.0 - R_RING / a_sma
        T = 2.0 * math.pi * math.sqrt(a_sma ** 3 / MU_S)
        # arc time within r < r_burn near periapsis (both sides)
        cosEb = (a_sma - r_burn) / (a_sma * e) if e > 1e-9 else -1.0
        cosEb = max(-1.0, min(1.0, cosEb))
        Eb = math.acos(cosEb)
        d = (Eb - e * math.sin(Eb)) / math.pi
        tau = d * T
        dv_pass = a_thrust * tau
        v_p += dv_pass                     # Oberth burn at periapsis (r_p fixed)
        dv_total += dv_pass
        firing += tau
        elapsed += T
        revs += 1
        if elapsed > max_years * YEAR or revs > max_revs:
            return {"escaped": False, "dv_total": dv_total, "elapsed_yr": elapsed / YEAR,
                    "firing_yr": firing / YEAR, "revs": revs, "duty": firing / elapsed}
    # complete to hyperbolic v_inf with a final periapsis burn
    if v_p < V_HYP:
        dv_extra = V_HYP - v_p
        dv_total += dv_extra
        firing += dv_extra / a_thrust
    return {"escaped": True, "dv_total": dv_total, "elapsed_yr": elapsed / YEAR,
            "firing_yr": firing / YEAR, "revs": revs,
            "duty": firing / elapsed if elapsed > 0 else 1.0}


def main():
    out = {"anchors": {"v_circ": V_CIRC, "v_esc": V_ESC, "vinf": VINF,
                       "dv_impulsive_at_ring": DV_IMPULSIVE, "ve_met": VE_MET}}

    # H-D1: ring relative velocity vs eccentricity
    hd1 = {}
    for mult in (1.0, 1.1, 1.3, 2.0, 5.0, R_TITAN / R_RING):
        r_a = mult * R_RING
        hd1[f"apoapsis_{mult:.2f}x_rp"] = {"v_peri_kms": v_peri(r_a) / 1000,
                                           "v_rel_ms": v_peri(r_a) - V_CIRC}
    out["HD1"] = {"ring_relative_velocity": hd1,
                  "v_rel_at_1p3x_rp_ms": v_peri(1.3 * R_RING) - V_CIRC,
                  "capture_threshold_ms": "~1 (mm/s-low-m/s, locked finding 1)"}

    # H-D2 + H-D3: periapsis-burn departure sim, sweep thrust to find min peak power for 2 yr
    sweep = []
    for F in (10, 15, 20, 25, 30, 40, 50, 75, 100, 150, 200, 300):
        r = periapsis_burn_departure(float(F))
        r["F_N"] = float(F)
        r["peak_kwe"] = peak_power_kwe(float(F))
        sweep.append(r)
    # min peak power completing within 2 yr
    completing = [s for s in sweep if s["escaped"] and s["elapsed_yr"] <= 2.0]
    min_2yr = min(completing, key=lambda s: s["peak_kwe"]) if completing else None
    # also the relaxed 5-yr window
    completing5 = [s for s in sweep if s["escaped"] and s["elapsed_yr"] <= 5.0]
    min_5yr = min(completing5, key=lambda s: s["peak_kwe"]) if completing5 else None
    # representative Δv (from a mid-thrust completing case)
    dv_rep = (min_2yr or (completing and completing[0]) or sweep[-1])["dv_total"]
    out["HD2"] = {"periapsis_burn_dv_kms": dv_rep / 1000,
                  "continuous_spiral_dv_kms": 21.9, "impulsive_dv_kms": DV_IMPULSIVE / 1000}
    out["HD3"] = {"sweep": [{"F_N": s["F_N"], "peak_kwe": round(s["peak_kwe"]),
                             "dv_kms": round(s["dv_total"] / 1000, 2),
                             "elapsed_yr": round(s["elapsed_yr"], 2),
                             "duty": round(s["duty"], 3), "escaped": s["escaped"]}
                            for s in sweep],
                  "min_peak_kwe_2yr": round(min_2yr["peak_kwe"]) if min_2yr else None,
                  "min_2yr_duty": round(min_2yr["duty"], 3) if min_2yr else None,
                  "min_peak_kwe_5yr": round(min_5yr["peak_kwe"]) if min_5yr else None,
                  "r179_impulsive_kwe": 175, "roundC_continuous_kwe": 1248}

    # verdicts
    hd1v = out["HD1"]["v_rel_at_1p3x_rp_ms"] >= 1000.0
    hd2v = 8000.0 <= dv_rep <= 15000.0
    m2 = out["HD3"]["min_peak_kwe_2yr"]
    hd3v = (m2 is not None and 250.0 <= m2 <= 1248.0)
    hd4v = (m2 is None or m2 >= 250.0)   # not relieved below ~250 kWe electric
    out["verdicts"] = {"H-D1": hd1v, "H-D2": hd2v, "H-D3": hd3v, "H-D4": hd4v,
                       "held": sum([hd1v, hd2v, hd3v, hd4v]), "of": 4}
    return out


if __name__ == "__main__":
    r = main()
    (HERE / "results").mkdir(exist_ok=True)
    json.dump(r, open(HERE / "results" / "eccentric_harvest.json", "w"), indent=2)
    v = r["verdicts"]
    print(f"H-D1  v_rel at ring: 1.3x r_p = {r['HD1']['v_rel_at_1p3x_rp_ms']:.0f} m/s, "
          f"2x r_p = {r['HD1']['ring_relative_velocity']['apoapsis_2.00x_rp']['v_rel_ms']:.0f} m/s "
          f"(vs ~1 m/s capture) -> {v['H-D1']}")
    print(f"H-D2  periapsis-burn departure Δv = {r['HD2']['periapsis_burn_dv_kms']:.2f} km/s "
          f"(vs continuous spiral 21.9, impulsive {r['HD2']['impulsive_dv_kms']:.2f}) -> {v['H-D2']}")
    print(f"H-D3  min peak power (2-yr window) = {r['HD3']['min_peak_kwe_2yr']} kWe "
          f"(duty {r['HD3']['min_2yr_duty']}); 5-yr = {r['HD3']['min_peak_kwe_5yr']} kWe; "
          f"vs Round C 1248 / R179 175 -> {v['H-D3']}")
    print(f"      thrust sweep (F N -> peak kWe / Δv km/s / elapsed yr / duty / escaped):")
    for s in r["HD3"]["sweep"]:
        print(f"        F={s['F_N']:5.0f} -> {s['peak_kwe']:5.0f} kWe  Δv {s['dv_kms']:5.2f}  "
              f"{s['elapsed_yr']:6.2f} yr  duty {s['duty']:.3f}  esc={s['escaped']}")
    print(f"H-D4  bet #3 not relieved below ~250 kWe electric -> {v['H-D4']}")
    print(f"\nHELD {v['held']}/{v['of']}")
