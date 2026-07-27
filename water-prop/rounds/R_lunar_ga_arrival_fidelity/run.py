"""R-lunar-ga-arrival-fidelity — honest vectorial lunar-GA braking vs R12.

Tests whether R12's inbound N-flyby lunar tour (which sheds 5.83 km/s of a
10.30 km/s Earth arrival in 10 flybys and feeds the axis-10 strict L0-05
closure) survives v-infinity conservation. A lunar flyby ROTATES the
Moon-relative velocity vector at fixed magnitude U_m; it cannot shrink U_m.
R12 recomputes U_m = v_sc(v_inf) + v_M from the REDUCED Earth-frame v_inf each
flyby, which violates that invariant.

Pre-registered H-B1..H-B6. See SCOPE.md. Deterministic, pure numpy.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

# R12's own primitives, for the H-B6 instrumentation (import from installed pkg)
from waterprop.constants import G0
from waterprop.trajectory.lunar_flyby import (
    GM_MOON, R_MOON, V_MOON_ORBITAL, R_LUNAR_ORBIT, GM_EARTH_KM3_S2,
    v_sc_earth_at_lunar_distance, turning_angle, single_flyby_braking,
)

GM_MOON_ = GM_MOON
R_MOON_ = R_MOON
V_MOON = V_MOON_ORBITAL          # 1.0220 km/s
R_LO = R_LUNAR_ORBIT
GM_E = GM_EARTH_KM3_S2

V_INF_ARRIVAL = 10.30            # km/s, R12 V_INF_INBOUND_KM_S (Hohmann arrival excess)
PERI_ALT = 100.0                 # km, R12 default
HERE = Path(__file__).resolve().parent


# --------------------------------------------------------------------------
# Shared helpers
# --------------------------------------------------------------------------
def v_sc_at_moon(v_inf_E: float) -> float:
    return math.sqrt(v_inf_E ** 2 + 2.0 * GM_E / R_LO)


def v_inf_E_from_speed(v_sc: float) -> float:
    arg = v_sc ** 2 - 2.0 * GM_E / R_LO
    return math.sqrt(arg) if arg > 0.0 else 0.0


def delta_max_rad(U_m: float) -> float:
    """Flyby turn angle (rad): 2 arcsin(1/(1 + r_p U_m^2 / GM_moon)). Identical
    closed form to trajectory-bot flyby_leverage.delta_max / inclination_flyby."""
    r_p = R_MOON_ + PERI_ALT
    e = 1.0 + r_p * U_m ** 2 / GM_MOON_
    return 2.0 * math.asin(1.0 / e)


def _rotate_toward(a: np.ndarray, target: np.ndarray, angle: float) -> np.ndarray:
    """Rotate vector `a` toward direction `target` by `angle` rad, in the plane
    they span, preserving |a|. If already (anti)parallel, return a unchanged."""
    na = np.linalg.norm(a)
    if na < 1e-15:
        return a
    a_hat = a / na
    t = target / np.linalg.norm(target)
    perp = t - np.dot(t, a_hat) * a_hat
    npp = np.linalg.norm(perp)
    if npp < 1e-12:
        return a
    perp_hat = perp / npp
    return na * (math.cos(angle) * a_hat + math.sin(angle) * perp_hat)


# --------------------------------------------------------------------------
# H-B1 / H-B4: honest single-flyby braking, swept over approach geometry
# --------------------------------------------------------------------------
def honest_single_flyby(v_inf_E_in: float, phi_deg: float = 0.0, n_theta: int = 1441) -> dict:
    """Max Earth-frame braking from ONE honest lunar flyby: rotate the v_inf_moon
    VECTOR (magnitude U_m conserved) by <= delta_max toward -v_M, minimizing the
    outgoing Earth-frame speed, swept over the incoming approach geometry theta.
    phi_deg = inclination of the spacecraft's velocity plane vs the Moon's
    orbital plane (out-of-plane tilt about the v_M axis)."""
    v_sc = v_sc_at_moon(v_inf_E_in)
    vM = np.array([V_MOON, 0.0, 0.0])
    phi = math.radians(phi_deg)
    best = {"brake": 0.0}
    for theta in np.linspace(1e-4, math.pi, n_theta):
        # incoming spacecraft velocity direction, tilted out-of-plane by phi
        vsc = v_sc * np.array([math.cos(theta),
                               math.sin(theta) * math.cos(phi),
                               math.sin(theta) * math.sin(phi)])
        vinf_moon = vsc - vM
        U_m = float(np.linalg.norm(vinf_moon))
        dmax = delta_max_rad(U_m)
        # rotate v_inf_moon toward -v_M by up to dmax
        ang_to_antiM = math.acos(max(-1.0, min(1.0, float(np.dot(vinf_moon, -vM)) / (U_m * V_MOON))))
        rot = min(dmax, ang_to_antiM)
        vinf_out = _rotate_toward(vinf_moon, -vM, rot)
        vsc_out = vM + vinf_out
        vinf_E_out = v_inf_E_from_speed(float(np.linalg.norm(vsc_out)))
        brake = v_inf_E_in - vinf_E_out
        if brake > best["brake"]:
            best = {"brake": brake, "theta_deg": math.degrees(theta),
                    "U_m": U_m, "delta_max_deg": math.degrees(dmax),
                    "vinf_E_out": vinf_E_out}
    return best


# --------------------------------------------------------------------------
# H-B2 / H-B3: honest N-flyby tour (U_m conserved) + analytic globe bound
# --------------------------------------------------------------------------
def vinf_globe_bound(v_inf0: float) -> dict:
    """Analytic floor: U_m conserved => min Earth-frame speed = |U_m - v_M|;
    minimized over arrival geometry at U_m = v_sc - v_M => v_sc - 2 v_M."""
    v_sc = v_sc_at_moon(v_inf0)
    v_sc_floor = v_sc - 2.0 * V_MOON
    vinf_floor = v_inf_E_from_speed(v_sc_floor)
    return {"v_sc_arrival": v_sc, "U_m_tour": v_sc - V_MOON,
            "v_sc_floor": v_sc_floor, "vinf_floor": vinf_floor,
            "max_total_shed": v_inf0 - vinf_floor}


def honest_tour(v_inf0: float, n_max: int = 120, phi_deg: float = 0.0) -> dict:
    """Best-case honest braking tour. Arrive with the min-U_m geometry
    (v_sc parallel v_M => U_m = v_sc - v_M, v_inf_moon aligned with +v_M, beta0=0),
    then rotate v_inf_moon toward -v_M by <= delta_max each flyby. U_m is CONSERVED.
    A per-flyby cos(phi) efficiency models an off-node inclination penalty on the
    achievable rotation-toward-antiM (phi=0 => node-targeted, full efficiency)."""
    v_sc = v_sc_at_moon(v_inf0)
    U_m = v_sc - V_MOON                      # conserved, minimal (deepest floor)
    dmax = delta_max_rad(U_m)
    eff = math.cos(math.radians(phi_deg))    # off-node penalty on per-flyby rotation
    beta = 0.0                               # angle of v_inf_moon from +v_M
    per = []
    vinf_prev = v_inf0
    for i in range(n_max):
        beta = min(math.pi, beta + dmax * eff)
        v_sc_out = math.sqrt(V_MOON ** 2 + U_m ** 2 + 2.0 * V_MOON * U_m * math.cos(beta))
        vinf_E = v_inf_E_from_speed(v_sc_out)
        per.append({"flyby": i + 1, "beta_deg": math.degrees(beta),
                    "vinf_E": vinf_E, "shed_this": vinf_prev - vinf_E})
        vinf_prev = vinf_E
        if math.pi - beta < 1e-6:
            break
    return {"U_m": U_m, "delta_max_deg": math.degrees(dmax), "phi_deg": phi_deg,
            "n_flybys": len(per), "vinf_final": vinf_prev,
            "total_shed": v_inf0 - vinf_prev, "per_flyby": per}


def flybys_to_reach(v_inf0: float, target_shed: float, phi_deg: float = 0.0) -> int:
    """How many honest flybys to shed target_shed km/s (None if unreachable)."""
    t = honest_tour(v_inf0, n_max=100000, phi_deg=phi_deg)
    acc = 0.0
    for p in t["per_flyby"]:
        acc = v_inf0 - p["vinf_E"]
        if acc >= target_shed:
            return p["flyby"]
    return -1  # unreachable (target exceeds the globe bound)


# --------------------------------------------------------------------------
# H-B6: instrument R12's model to exhibit U_m decay (conservation violation)
# --------------------------------------------------------------------------
def r12_tour_instrumented(v_inf0: float, n: int) -> dict:
    """Replicate R12 n_flyby_tour(mode=braking) and record the U_m it IMPLICITLY
    uses each flyby (= v_sc(v_inf_in) + v_M, its leading-side recomputation)."""
    v_inf = v_inf0
    per = []
    total = 0.0
    for i in range(n):
        U_m_implied = v_sc_earth_at_lunar_distance(v_inf) + V_MOON
        v_inf_new, dv = single_flyby_braking(v_inf, PERI_ALT, 0.0)
        per.append({"flyby": i + 1, "vinf_in": v_inf, "vinf_out": v_inf_new,
                    "dv": dv, "U_m_implied": U_m_implied})
        total += dv
        v_inf = v_inf_new
        if v_inf < 0.5:
            break
    return {"n": len(per), "vinf_final": v_inf, "total_shed": total, "per_flyby": per}


# --------------------------------------------------------------------------
# H-B5: R12's OWN delivery cell(), reused verbatim (apples-to-apples)
# --------------------------------------------------------------------------
DRY_T, CHUNK_T, ISP_S, ETA, DUTY = 5.0, 14.0, 2000.0, 0.65, 0.5
OUTBOUND_YR, DWELL_YR, INBOUND_COAST_YR = 6.09, 1.0, 6.09
YEAR_S = 365.25 * 86400.0
SYNODIC_YR = 29.5 / 365.25


def cell(power_kwe, sp_w_kg, residual_vinf, phasing_yr):
    """Verbatim copy of R12 run.py cell() (delivery-fraction + cruise-time model)."""
    v_e = ISP_S * G0
    reactor_t = (power_kwe * 1000.0) / sp_w_kg / 1000.0
    m0 = CHUNK_T + DRY_T + reactor_t
    dv = residual_vinf
    prop_frac = 1.0 - math.exp(-dv * 1000.0 / v_e)
    prop = m0 * prop_frac
    delivered = max(CHUNK_T - prop, 0.0)
    F_N = 2.0 * ETA * power_kwe * 1000.0 / v_e
    m_avg = (m0 - prop / 2.0) * 1000.0
    if F_N <= 0 or m_avg <= 0 or delivered <= 0:
        return {"power_kwe": power_kwe, "sp": sp_w_kg, "feasible": False}
    accel = F_N / m_avg
    cruise_yr = (dv * 1000.0) / (accel * DUTY) / YEAR_S
    inbound_tof = max(INBOUND_COAST_YR, cruise_yr) + phasing_yr
    rt = OUTBOUND_YR + DWELL_YR + inbound_tof
    return {"power_kwe": power_kwe, "sp": sp_w_kg, "residual_vinf": dv,
            "delivered_t": delivered, "delivery_frac": delivered / CHUNK_T,
            "round_trip_yr": rt, "closes_15yr_strict": rt <= 15.0,
            "closes_14yr": rt <= 14.0, "feasible": True}


def main() -> dict:
    out: dict = {"anchor": {"v_inf_arrival": V_INF_ARRIVAL,
                            "v_sc_arrival": v_sc_at_moon(V_INF_ARRIVAL),
                            "v_moon": V_MOON, "peri_alt_km": PERI_ALT}}

    # --- delta_max cross-check vs trajectory-bot closed form (same formula) ---
    U_probe = 9.378
    tb_form = 2.0 * math.asin(1.0 / (1.0 + (R_MOON_ + PERI_ALT) * U_probe ** 2 / GM_MOON_))
    out["delta_max_crosscheck"] = {
        "U_m": U_probe, "this_round_deg": math.degrees(delta_max_rad(U_probe)),
        "closed_form_2arcsin_deg": math.degrees(tb_form),
        "match": abs(delta_max_rad(U_probe) - tb_form) < 1e-12,
        "note": "identical to trajectory-bot flyby_leverage.delta_max / inclination_flyby form"}

    # --- H-B1: honest first-flyby braking vs R12 0.458 ---
    r12_first = single_flyby_braking(V_INF_ARRIVAL, PERI_ALT, 0.0)
    honest_first = honest_single_flyby(V_INF_ARRIVAL, phi_deg=0.0)
    out["HB1"] = {"r12_first_flyby_shed": V_INF_ARRIVAL - r12_first[0],
                  "r12_first_flyby_brake": r12_first[1],
                  "honest_first_flyby_brake": honest_first["brake"],
                  "honest_theta_deg": honest_first.get("theta_deg"),
                  "honest_U_m": honest_first.get("U_m"),
                  "ratio_r12_over_honest": r12_first[1] / max(honest_first["brake"], 1e-9)}

    # --- H-B2: globe bound + honest tour total shed (many flybys) ---
    bound = vinf_globe_bound(V_INF_ARRIVAL)
    tour = honest_tour(V_INF_ARRIVAL, n_max=200, phi_deg=0.0)
    out["HB2"] = {"analytic_max_total_shed": bound["max_total_shed"],
                  "analytic_vinf_floor": bound["vinf_floor"],
                  "honest_tour_total_shed": tour["total_shed"],
                  "honest_tour_vinf_final": tour["vinf_final"],
                  "honest_tour_n_flybys": tour["n_flybys"],
                  "r12_claim_10flyby_shed": 5.83}

    # --- H-B3: flyby count to reach ~2 km/s vs R12's ~4 ---
    n_for_bound = flybys_to_reach(V_INF_ARRIVAL, bound["max_total_shed"] - 0.02, 0.0)
    n_for_2 = flybys_to_reach(V_INF_ARRIVAL, min(2.0, bound["max_total_shed"] - 1e-3), 0.0)
    out["HB3"] = {"honest_flybys_to_within_0p02_of_bound": n_for_bound,
                  "honest_flybys_to_shed_2kms": n_for_2,
                  "phasing_yr_for_bound": (n_for_bound * SYNODIC_YR) if n_for_bound > 0 else None,
                  "r12_flybys_for_2kms": "~4 (R12 sheds 2.50 in 5 flybys per its table)"}

    # --- H-B4: inclination is second-order for the ceiling ---
    incl = {}
    for phi in (0.0, 5.0, 10.0, 20.0):
        t = honest_tour(V_INF_ARRIVAL, n_max=100000, phi_deg=phi)
        f = honest_single_flyby(V_INF_ARRIVAL, phi_deg=phi)
        incl[f"phi_{phi:g}"] = {"tour_total_shed": t["total_shed"],
                                "tour_n_flybys": t["n_flybys"],
                                "single_flyby_brake": f["brake"]}
    base = incl["phi_0"]["tour_total_shed"]
    incl["max_frac_change_vs_phi0"] = max(
        abs(incl[f"phi_{p:g}"]["tour_total_shed"] - base) / base for p in (5.0, 10.0, 20.0))
    out["HB4"] = incl

    # --- H-B6: R12 U_m decay (conservation violation) ---
    r12_inst = r12_tour_instrumented(V_INF_ARRIVAL, 20)
    U_first = r12_inst["per_flyby"][0]["U_m_implied"]
    U_last = r12_inst["per_flyby"][-1]["U_m_implied"]
    out["HB6"] = {"r12_U_m_first": U_first, "r12_U_m_last": U_last,
                  "r12_U_m_frac_drop": (U_first - U_last) / U_first,
                  "r12_n_flybys_to_vinf_lt_0p5": r12_inst["n"],
                  "r12_total_shed": r12_inst["total_shed"],
                  "note": "U_m should be CONSTANT; R12 lets it fall => inflates late-flyby dv"}

    # --- H-B5: axis-10 strict closure under honest tour ---
    POWERS = [10.0, 15.0, 20.0, 30.0, 40.0]
    SPS = [5.0, 10.0]
    honest_residual = bound["vinf_floor"]                    # ~8.23 km/s (best case)
    honest_phasing = n_for_bound * SYNODIC_YR                # ~4.3 yr
    r12_residual, r12_phasing = 4.47, 10 * SYNODIC_YR        # R12 best cell inputs
    cells_honest, cells_r12 = [], []
    for p in POWERS:
        for sp in SPS:
            cells_honest.append(cell(p, sp, honest_residual, honest_phasing))
            cells_r12.append(cell(p, sp, r12_residual, r12_phasing))
    strict_honest = [c for c in cells_honest
                     if c.get("feasible") and c["closes_15yr_strict"] and c["delivery_frac"] >= 0.30]
    strict_r12 = [c for c in cells_r12
                  if c.get("feasible") and c["closes_15yr_strict"] and c["delivery_frac"] >= 0.30]
    out["HB5"] = {"honest_residual_vinf": honest_residual, "honest_phasing_yr": honest_phasing,
                  "r12_residual_vinf": r12_residual, "r12_phasing_yr": r12_phasing,
                  "n_strict_cells_honest": len(strict_honest),
                  "n_strict_cells_r12_reproduce": len(strict_r12),
                  "best_honest_delivery_frac": max((c["delivery_frac"] for c in cells_honest
                                                    if c.get("feasible")), default=0.0),
                  "best_honest_round_trip_yr": min((c["round_trip_yr"] for c in cells_honest
                                                    if c.get("feasible")), default=None),
                  "example_honest_cell_15kwe10": cell(15.0, 10.0, honest_residual, honest_phasing)}

    # --- verdicts ---
    hb1 = 0.01 <= out["HB1"]["honest_first_flyby_brake"] <= 0.25
    hb2 = out["HB2"]["honest_tour_total_shed"] <= 2.5
    hb3 = out["HB3"]["honest_flybys_to_within_0p02_of_bound"] >= 40
    hb4 = out["HB4"]["max_frac_change_vs_phi0"] <= 0.15
    hb5 = out["HB5"]["n_strict_cells_honest"] == 0
    hb6 = out["HB6"]["r12_U_m_frac_drop"] > 0.05
    out["verdicts"] = {"H-B1": hb1, "H-B2": hb2, "H-B3": hb3,
                       "H-B4": hb4, "H-B5": hb5, "H-B6": hb6,
                       "held": sum([hb1, hb2, hb3, hb4, hb5, hb6]), "of": 6}
    return out


if __name__ == "__main__":
    res = main()
    (HERE / "results").mkdir(exist_ok=True)
    with open(HERE / "results" / "lunar_ga_fidelity.json", "w") as f:
        json.dump(res, f, indent=2)
    v = res["verdicts"]
    print(f"delta_max cross-check: {res['delta_max_crosscheck']['this_round_deg']:.4f} deg "
          f"== closed form {res['delta_max_crosscheck']['closed_form_2arcsin_deg']:.4f} deg "
          f"(match={res['delta_max_crosscheck']['match']})")
    print()
    print(f"H-B1  honest first-flyby brake = {res['HB1']['honest_first_flyby_brake']:.4f} km/s "
          f"vs R12 {res['HB1']['r12_first_flyby_brake']:.4f} "
          f"({res['HB1']['ratio_r12_over_honest']:.1f}x)  -> {v['H-B1']}")
    print(f"H-B2  honest total shed = {res['HB2']['honest_tour_total_shed']:.3f} km/s "
          f"(analytic bound {res['HB2']['analytic_max_total_shed']:.3f}) vs R12 claim 5.83 "
          f"-> {v['H-B2']}")
    print(f"H-B3  honest flybys to bound = {res['HB3']['honest_flybys_to_within_0p02_of_bound']} "
          f"(~{res['HB3']['phasing_yr_for_bound']:.1f} yr phasing) -> {v['H-B3']}")
    print(f"H-B4  inclination max frac change vs phi=0 = {res['HB4']['max_frac_change_vs_phi0']:.4f} "
          f"-> {v['H-B4']}")
    print(f"H-B5  strict-15yr cells: honest {res['HB5']['n_strict_cells_honest']} vs "
          f"R12-repro {res['HB5']['n_strict_cells_r12_reproduce']}; best honest delivery "
          f"{100*res['HB5']['best_honest_delivery_frac']:.0f}%, best RT "
          f"{res['HB5']['best_honest_round_trip_yr']:.1f} yr -> {v['H-B5']}")
    print(f"H-B6  R12 implied U_m drop = {100*res['HB6']['r12_U_m_frac_drop']:.0f}% "
          f"({res['HB6']['r12_U_m_first']:.2f} -> {res['HB6']['r12_U_m_last']:.2f}) -> {v['H-B6']}")
    print()
    print(f"HELD {v['held']}/{v['of']}")
