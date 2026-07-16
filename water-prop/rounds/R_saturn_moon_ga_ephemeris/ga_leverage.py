"""Patched-conic gravity-assist leverage + pump-down model for Saturnian-moon capture.

R-saturn-moon-ga-ephemeris (phoebe, 2026-05-26).

Computes, as optimistic UPPER bounds (best-case tangential coplanar geometry, optimal
turn every pass):
  - v_inf relative to each moon as a function of arrival v_inf at Saturn
  - per-flyby Saturn-relative Delta-v and max turn angle
  - the hard per-flyby ceiling sqrt(mu_moon / r_p)
  - a sequential pump-down: flybys needed to fully capture (v_inf,S -> 0), and to hit
    the framework's documentary reduction anchor; tour time via resonant re-encounter
  - small-moon marginal contribution (H8: are they inert leverage-wise?)

Method notes in STUDY.md. All distances km, speeds km/s, GM km^3/s^2.

Emits results/ephemeris_dv_table.json.
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass, asdict
from pathlib import Path

MU_SATURN = 3.7931206e7  # km^3/s^2 (Saturn system GM)
DAY_S = 86400.0


@dataclass(frozen=True)
class Moon:
    name: str
    mu: float          # km^3/s^2
    radius_km: float
    a_km: float        # orbital semi-major axis (Saturn-centred)
    min_alt_km: float  # minimum safe flyby altitude

    @property
    def r_p(self) -> float:
        return self.radius_km + self.min_alt_km

    @property
    def v_orb(self) -> float:
        return math.sqrt(MU_SATURN / self.a_km)

    @property
    def period_days(self) -> float:
        return 2 * math.pi * math.sqrt(self.a_km**3 / MU_SATURN) / DAY_S

    @property
    def dv_ceiling(self) -> float:
        """Absolute max single-flyby Saturn-relative Delta-v = sqrt(mu/r_p)."""
        return math.sqrt(self.mu / self.r_p)


# IAU/JPL standard values; orbital radii confirmed against Horizons pull (see
# results/horizons_moon_states.json). Min flyby altitude: Titan 1000 km (atmosphere
# ~600 km; Cassini min ~880 km), others 100 km.
MOONS = {
    "Titan":     Moon("Titan",     8978.14, 2574.7, 1_221_870, 1000.0),
    "Rhea":      Moon("Rhea",       153.94,  763.8,   527_108,  100.0),
    "Dione":     Moon("Dione",       73.116, 561.4,   377_396,  100.0),
    "Tethys":    Moon("Tethys",      41.21,  531.1,   294_619,  100.0),
    "Enceladus": Moon("Enceladus",    7.211, 252.1,   237_948,  100.0),
    "Mimas":     Moon("Mimas",        2.503, 198.2,   185_539,  100.0),
}


def v_esc_at_orbit(moon: Moon) -> float:
    """Saturn escape speed at the moon's orbital radius."""
    return math.sqrt(2 * MU_SATURN / moon.a_km)


def v_sc_at_moon(v_inf_S: float, moon: Moon) -> float:
    """Spacecraft Saturn-relative speed at the moon's orbit (vis-viva)."""
    return math.sqrt(v_inf_S**2 + 2 * MU_SATURN / moon.a_km)


def turn_angle(v_inf_m: float, moon: Moon) -> float:
    """Max single-flyby turn angle (rad). sin(d/2) = 1/(1 + r_p v^2 / mu)."""
    e = 1.0 + moon.r_p * v_inf_m**2 / moon.mu
    return 2.0 * math.asin(1.0 / e)


def per_flyby_dv(v_inf_m: float, moon: Moon) -> float:
    """Saturn-relative Delta-v from one optimal flyby = 2 v_inf_m sin(delta/2)."""
    return 2.0 * v_inf_m * math.sin(turn_angle(v_inf_m, moon) / 2.0)


def theta_for_vsc(v_sc: float, v_inf_m: float, moon: Moon) -> float:
    """Angle (rad) between v_inf,m and moon velocity giving Saturn-relative speed v_sc.
    v_sc^2 = V^2 + v_inf_m^2 + 2 V v_inf_m cos(theta). Clamped to [0, pi]."""
    V = moon.v_orb
    c = (v_sc**2 - V**2 - v_inf_m**2) / (2 * V * v_inf_m)
    c = max(-1.0, min(1.0, c))
    return math.acos(c)


def best_case_v_inf_m(v_inf_S: float, moon: Moon) -> float:
    """Best-case (tangential prograde) relative speed at the moon = |v_sc - V_orb|.
    This minimises v_inf,m, which (for these regimes, v_inf,m > sqrt(mu/r_p)) maximises
    leverage AND lets the spacecraft pump deepest toward capture."""
    return abs(v_sc_at_moon(v_inf_S, moon) - moon.v_orb)


def pump_down(v_inf_S_arrival: float, moon: Moon, target_v_inf_S: float,
              resonance_periods: float = 2.0):
    """Sequential same-moon flyby pump-down from arrival v_inf to a target v_inf.

    v_inf,m is conserved at the moon; each flyby rotates it by up to the max turn angle,
    changing the Saturn-relative speed. We count flybys to rotate v_inf,m from its
    arrival orientation to the orientation giving target v_sc. Returns None if the
    target is not reachable (target v_sc outside the achievable [|V-v|, V+v] band).
    """
    V = moon.v_orb
    v_inf_m = best_case_v_inf_m(v_inf_S_arrival, moon)
    v_sc_arrival = v_sc_at_moon(v_inf_S_arrival, moon)
    v_esc = v_esc_at_orbit(moon)
    # target v_sc: if target_v_inf_S <= 0 we want capture (v_sc = v_esc, i.e. v_inf_S=0)
    tgt = max(0.0, target_v_inf_S)
    v_sc_target = math.sqrt(tgt**2 + 2 * MU_SATURN / moon.a_km)

    v_sc_min = abs(V - v_inf_m)
    v_sc_max = V + v_inf_m
    reachable = v_sc_min <= v_sc_target <= v_sc_max + 1e-9
    # deepest reachable v_inf,S via this moon (best case):
    if v_sc_min <= v_esc:
        deepest_v_inf_S = 0.0  # can capture
    else:
        deepest_v_inf_S = math.sqrt(v_sc_min**2 - 2 * MU_SATURN / moon.a_km)

    delta_max = turn_angle(v_inf_m, moon)
    theta_arr = theta_for_vsc(v_sc_arrival, v_inf_m, moon)
    theta_tgt = theta_for_vsc(v_sc_target, v_inf_m, moon)
    total_turn = abs(theta_tgt - theta_arr)
    flybys = math.ceil(total_turn / delta_max) if delta_max > 0 else math.inf
    tour_days = flybys * resonance_periods * moon.period_days
    return {
        "moon": moon.name,
        "v_inf_S_arrival": round(v_inf_S_arrival, 3),
        "target_v_inf_S": round(target_v_inf_S, 3),
        "v_inf_m_kms": round(v_inf_m, 4),
        "v_sc_arrival_kms": round(v_sc_arrival, 4),
        "v_esc_at_orbit_kms": round(v_esc, 4),
        "per_flyby_dv_kms": round(per_flyby_dv(v_inf_m, moon), 5),
        "dv_ceiling_kms": round(moon.dv_ceiling, 5),
        "turn_max_deg": round(math.degrees(delta_max), 3),
        "target_reachable": bool(reachable),
        "deepest_v_inf_S_reachable_kms": round(deepest_v_inf_S, 4),
        "max_reduction_kms": round(v_inf_S_arrival - deepest_v_inf_S, 4),
        "flybys_to_target": flybys,
        "tour_months_est": round(tour_days / 30.44, 2),
        "resonance_periods_assumed": resonance_periods,
        "moon_period_days": round(moon.period_days, 4),
    }


# Framework's live + documentary anchors (phase2_saturn_capture.py).
ANCHORS = {
    "titan_gravity_assist_capture": {
        "moon": "Titan", "doc_reduction": 4.0, "min_vinf_gate": 3.5,
        "tour_months": 8.0, "trim_dv": 0.3},
    "rhea_gravity_assist_capture": {
        "moon": "Rhea", "doc_reduction": 1.5, "min_vinf_gate": 4.0,
        "tour_months": 12.0, "trim_dv": 0.7},
    "cassini_class_multi_moon_tour": {
        "moon": "Titan", "doc_reduction": 5.5, "min_vinf_gate": 3.0,
        "tour_months": 24.0, "trim_dv": 0.2},
}

# Phase 2 arrival v_inf sweep (per SCOPE: matches Phase-2 v_inf precondition gates).
ARRIVAL_VINF_GRID = [3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5]


def main():
    out = {
        "meta": {
            "method": "patched-conic, best-case tangential coplanar, optimal turn/pass "
                      "(UPPER bounds); resonance = 2x moon period nominal",
            "mu_saturn_km3_s2": MU_SATURN,
            "note": "*_VINF_REDUCTION constants in framework are documentary only "
                    "(not used in any precondition/executor); live anchors are the "
                    "min-vinf gate, trim_dv, and tour_months. Reduction is capped by "
                    "arrival v_inf (cannot bleed more v_inf than you arrive with).",
        },
        "moon_constants": {},
        "per_flyby_ceilings": {},
        "single_moon_capture": {},   # flybys + months to fully capture, per arrival v_inf
        "anchor_assessment": {},
        "small_moon_inertness": {},  # H8
    }

    for name, m in MOONS.items():
        out["moon_constants"][name] = {
            "mu": m.mu, "radius_km": m.radius_km, "a_km": m.a_km,
            "v_orb_kms": round(m.v_orb, 4), "period_days": round(m.period_days, 4),
            "r_p_km": m.r_p, "v_esc_at_orbit_kms": round(v_esc_at_orbit(m), 4),
        }
        out["per_flyby_ceilings"][name] = round(m.dv_ceiling, 5)

    # Single-moon capture-to-zero across arrival v_inf, for Titan and Rhea (the two
    # single-moon options).
    for moon_name in ("Titan", "Rhea"):
        m = MOONS[moon_name]
        out["single_moon_capture"][moon_name] = [
            pump_down(v, m, target_v_inf_S=0.0) for v in ARRIVAL_VINF_GRID
        ]

    # Anchor assessment: for each framework option, at each arrival v_inf >= its gate,
    # what reduction is achievable, how many flybys, how long, vs the documentary anchor.
    for opt, a in ANCHORS.items():
        m = MOONS[a["moon"]]
        rows = []
        for v in ARRIVAL_VINF_GRID:
            if v < a["min_vinf_gate"]:
                continue
            cap = pump_down(v, m, target_v_inf_S=0.0)  # full capture
            achievable_reduction = cap["max_reduction_kms"]  # = v if capture reachable
            doc = a["doc_reduction"]
            # the documentary anchor is only physically meaningful if arrival v_inf >= doc
            doc_reachable = v >= doc and cap["deepest_v_inf_S_reachable_kms"] <= (v - doc) + 1e-9
            rows.append({
                "arrival_v_inf": v,
                "achievable_reduction_kms": achievable_reduction,
                "doc_anchor_reduction_kms": doc,
                "doc_anchor_reachable": bool(doc_reachable),
                "flybys_to_full_capture": cap["flybys_to_target"],
                "tour_months_est_full_capture": cap["tour_months_est"],
                "anchor_tour_months": a["tour_months"],
                "tour_time_consistent": cap["tour_months_est"] <= a["tour_months"] * 1.5,
            })
        out["anchor_assessment"][opt] = {
            "anchor": a,
            "rows": rows,
        }

    # H8: small-moon marginal leverage. Per-flyby dv for each non-Titan moon at a
    # representative arrival v_inf = 4.0 km/s, and flybys each would need for 1 km/s.
    for name in ("Rhea", "Dione", "Tethys", "Enceladus", "Mimas"):
        m = MOONS[name]
        res = pump_down(4.0, m, target_v_inf_S=3.0)  # bleed 1 km/s from 4.0
        out["small_moon_inertness"][name] = {
            "per_flyby_dv_kms": res["per_flyby_dv_kms"],
            "dv_ceiling_kms": res["dv_ceiling_kms"],
            "turn_max_deg": res["turn_max_deg"],
            "flybys_for_1kms_from_4kms": res["flybys_to_target"],
            "tour_months_for_1kms": res["tour_months_est"],
        }

    results = Path(__file__).parent / "results"
    results.mkdir(exist_ok=True)
    (results / "ephemeris_dv_table.json").write_text(json.dumps(out, indent=2))

    # Console summary
    print("=== Per-flyby Saturn-relative Delta-v ceiling sqrt(mu/r_p) ===")
    for name, c in out["per_flyby_ceilings"].items():
        print(f"  {name:10s} {c:.4f} km/s   (V_orb {MOONS[name].v_orb:.2f}, "
              f"period {MOONS[name].period_days:.2f} d)")

    print("\n=== Titan single-moon capture (arrival v_inf -> 0) ===")
    print(f"  {'v_inf':>6} {'v_inf,m':>8} {'dv/pass':>8} {'turn':>6} {'flybys':>7} {'months':>7} {'capturable'}")
    for r in out["single_moon_capture"]["Titan"]:
        print(f"  {r['v_inf_S_arrival']:6.1f} {r['v_inf_m_kms']:8.3f} "
              f"{r['per_flyby_dv_kms']:8.4f} {r['turn_max_deg']:6.2f} "
              f"{r['flybys_to_target']:7d} {r['tour_months_est']:7.2f} "
              f"{r['deepest_v_inf_S_reachable_kms']==0.0}")

    print("\n=== Rhea single-moon capture (arrival v_inf -> 0) ===")
    print(f"  {'v_inf':>6} {'v_inf,m':>8} {'dv/pass':>8} {'turn':>6} {'flybys':>7} {'months':>7} {'capturable'}")
    for r in out["single_moon_capture"]["Rhea"]:
        print(f"  {r['v_inf_S_arrival']:6.1f} {r['v_inf_m_kms']:8.3f} "
              f"{r['per_flyby_dv_kms']:8.4f} {r['turn_max_deg']:6.2f} "
              f"{r['flybys_to_target']:7d} {r['tour_months_est']:7.2f} "
              f"{r['deepest_v_inf_S_reachable_kms']==0.0}")

    print("\n=== H8: small-moon inertness (per-flyby dv, flybys for 1 km/s from v_inf=4) ===")
    for name, d in out["small_moon_inertness"].items():
        print(f"  {name:10s} dv/pass {d['per_flyby_dv_kms']:.5f} km/s  "
              f"turn {d['turn_max_deg']:.3f} deg  "
              f"flybys/1kms {d['flybys_for_1kms_from_4kms']}  "
              f"({d['tour_months_for_1kms']:.1f} months)")

    print("\n=== Anchor assessment ===")
    for opt, blk in out["anchor_assessment"].items():
        a = blk["anchor"]
        print(f"\n  {opt}  (doc_reduction {a['doc_reduction']}, gate {a['min_vinf_gate']}, "
              f"anchor_months {a['tour_months']})")
        print(f"    {'arr_vinf':>8} {'achiev_red':>10} {'doc_reach':>9} {'flybys':>7} "
              f"{'months_est':>10} {'time_ok':>7}")
        for r in blk["rows"]:
            print(f"    {r['arrival_v_inf']:8.1f} {r['achievable_reduction_kms']:10.3f} "
                  f"{str(r['doc_anchor_reachable']):>9} {r['flybys_to_full_capture']:7d} "
                  f"{r['tour_months_est_full_capture']:10.2f} {str(r['tour_time_consistent']):>7}")

    print(f"\nwrote {results/'ephemeris_dv_table.json'}")


if __name__ == "__main__":
    main()
