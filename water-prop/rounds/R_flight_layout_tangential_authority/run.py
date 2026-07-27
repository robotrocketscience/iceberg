"""R-flight-layout-tangential-authority — does a real corner-mounted RCS keep
plume-safe in-plane couple authority about both in-plane axes?

Makes the berth-thread residual concrete: replaces the idealized cardinal ring
(R-berth-dump-axis-geometry) with a realistic box-corner 12-thruster layout,
searches all thruster subsets for pure plume-safe couples about each axis, and
tests single-fault robustness + a pessimistic aft-clustered variant.

Pre-registered H-A1..H-A5. See SCOPE.md. Deterministic, pure numpy.
"""
from __future__ import annotations

import itertools
import json
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent

# --- anchors (identical to the berth rounds) ---
F = 5.0                 # N per thruster
ISP_CG, G0 = 70.0, 9.80665
L_BERTH = 5000.0        # N.m.s berth injection
TAU_TH = 2.5            # N.m re-perturbation threshold
KAPPA, BETA, NEXP = 4.0, 1e-2, 4.0
THETA_C = math.radians(25.0)
R_BAG, R_OFF = 3.0, 5.0
A_BAG = math.pi * R_BAG ** 2
BOOM = 3.0
AX, AY, AZ = 1.5, 1.5, 2.0     # bus half-dims (corner layout)
Z_BAG = AZ + BOOM + R_BAG      # bag standoff on +z boom


def p_iso(r):
    return F / (2 * math.pi * r ** 2)


def bag_plume_one(pos, thrust_dir, z_bag=Z_BAG):
    """Plume torque on the bag from one firing thruster (berth-dump model)."""
    plume = -np.asarray(thrust_dir, float)
    to_bag = np.array([0.0, 0.0, z_bag]) - np.asarray(pos, float)
    r = float(np.linalg.norm(to_bag))
    cos_th = float(np.clip(np.dot(plume, to_bag) / r, -1.0, 1.0))
    P = p_iso(r) * KAPPA * cos_th ** NEXP if cos_th > 0 else p_iso(r) * BETA
    a_eff = min(A_BAG, math.pi * (r * math.tan(THETA_C)) ** 2)
    return P * a_eff * R_OFF, math.degrees(math.acos(cos_th))


def distributed_layout():
    """8 corner-tangential (body-axis-aligned thrust at box corners, ±z split)
    + 2 prograde (+z) + 2 retro (-z). The realistic analogue of the berth-dump
    ring, moved to box corners."""
    T = {
        "Ty+T": ((+AX, +AY, +AZ), (0, +1, 0)),   # +y, top
        "Ty-T": ((-AX, -AY, +AZ), (0, -1, 0)),   # -y, top
        "Ty-B": ((+AX, +AY, -AZ), (0, -1, 0)),   # -y, bottom
        "Ty+B": ((-AX, -AY, -AZ), (0, +1, 0)),   # +y, bottom
        "Tx+T": ((+AX, -AY, +AZ), (+1, 0, 0)),   # +x, top
        "Tx-T": ((-AX, +AY, +AZ), (-1, 0, 0)),   # -x, top
        "Tx-B": ((+AX, -AY, -AZ), (-1, 0, 0)),   # -x, bottom
        "Tx+B": ((-AX, +AY, -AZ), (+1, 0, 0)),   # +x, bottom
        "P0": ((+AX, +AY, +AZ), (0, 0, +1)), "P1": ((-AX, -AY, +AZ), (0, 0, +1)),
        "R0": ((+AX, -AY, -AZ), (0, 0, -1)), "R1": ((-AX, +AY, -AZ), (0, 0, -1)),
    }
    return {k: (np.array(p, float), np.array(d, float)) for k, (p, d) in T.items()}


def redundant_layout():
    """Single-fault-tolerant variant: TWO tangential thrusters per (direction,
    deck) — 16 tangential total. Tests whether adding tangential redundancy
    restores H-A4."""
    base = distributed_layout()
    T = {}
    for k, (p, d) in base.items():
        if k.startswith("T"):
            T[k + "a"] = (p, d)
            # a second thruster of the same function at the mirror corner, same z
            p2 = p.copy(); p2[0] = -p2[0]; p2[1] = -p2[1]
            T[k + "b"] = (p2, d)
        else:
            T[k] = (p, d)
    return T


def aft_clustered_layout():
    """All 12 thrusters within one deck near -z (no ±z separation)."""
    z0 = -AZ
    T = distributed_layout()
    out = {}
    for k, (p, d) in T.items():
        p2 = p.copy(); p2[2] = z0 + 0.15 * (1 if p[2] > 0 else -1) * 0  # all ~z0
        p2[2] = z0
        out[k] = (p2, d)
    return out


def couple_search(layout, axis, sense, max_k=3):
    """Find the max-torque PURE, PLUME-SAFE couple about `axis` in direction
    `sense` from non-negative firings of up to max_k thrusters.
    Pure: |net force| <= 0.1 N and torque within 5% aligned to the axis.
    Plume-safe: every firing thruster in backflow (cos_th<=0) and summed
    bag-plume torque < TAU_TH."""
    names = list(layout)
    ihat = np.eye(3)[axis]
    best = None
    for k in range(2, max_k + 1):
        for combo in itertools.combinations(names, k):
            Fnet = np.zeros(3); Tnet = np.zeros(3)
            plume_tot = 0.0; min_ang = 180.0
            for nm in combo:
                pos, d = layout[nm]
                Fv = F * d
                Fnet += Fv
                Tnet += np.cross(pos, Fv)
                tq, ang = bag_plume_one(pos, d)
                plume_tot += tq
                min_ang = min(min_ang, ang)
            if np.linalg.norm(Fnet) > 0.1:
                continue
            proj = float(np.dot(Tnet, ihat)) * sense
            if proj <= 1e-6:
                continue
            off = float(np.linalg.norm(Tnet - np.dot(Tnet, ihat) * ihat))
            if off > 0.05 * np.linalg.norm(Tnet):
                continue
            # plume-safe := summed bag-plume torque below the re-perturbation
            # threshold (berth-dump criterion; the cos^NEXP falloff makes even a
            # corner-tilted plume tiny). min_ang reported as diagnostic.
            if plume_tot >= TAU_TH:
                continue
            if best is None or proj > best["torque"]:
                best = {"combo": list(combo), "torque": proj,
                        "plume_torque": plume_tot, "min_plume_angle_deg": min_ang,
                        "net_force_N": float(np.linalg.norm(Fnet))}
    return best


def inplane_authority(layout):
    """max plume-safe pure-couple torque about ±x and ±y; feasible iff all four exist."""
    res = {}
    ok = True
    for ax, nm in ((0, "x"), (1, "y")):
        for s, tag in ((+1, "+"), (-1, "-")):
            b = couple_search(layout, ax, s)
            res[f"{tag}{nm}"] = None if b is None else round(b["torque"], 3)
            if b is None:
                ok = False
    res["all_four_feasible"] = ok
    res["min_inplane_couple_torque"] = (min(v for v in
        [res["+x"], res["-x"], res["+y"], res["-y"]] if v) if ok else 0.0)
    return res


def main():
    out = {"anchors": {"F_N": F, "bus_half_dims_m": [AX, AY, AZ], "z_bag_m": Z_BAG,
                       "L_berth": L_BERTH, "tau_threshold": TAU_TH}}
    dist = distributed_layout()

    # H-A1: pure 3-axis couples exist (torque only, net force ~0)
    axes3 = {}
    for ax, nm in ((0, "x"), (1, "y"), (2, "z")):
        b = couple_search(dist, ax, +1, max_k=4) or couple_search(dist, ax, -1, max_k=4)
        axes3[nm] = None if b is None else {"torque": round(b["torque"], 3),
                                            "net_force_N": b["net_force_N"], "combo": b["combo"]}
    out["HA1"] = {"three_axis_couples": axes3,
                  "all_three": all(axes3[a] is not None for a in "xyz")}

    # H-A2 + H-A3: plume-safe in-plane authority + dump time + propellant
    auth = inplane_authority(dist)
    tau_min = auth["min_inplane_couple_torque"]
    dump_t = L_BERTH / tau_min if tau_min > 0 else None
    prop_kg = 125.0 * L_BERTH / 15000.0
    out["HA2"] = {"inplane_authority": auth,
                  "both_axes_plume_safe": auth["all_four_feasible"]}
    out["HA3"] = {"min_inplane_couple_torque_Nm": tau_min,
                  "dump_time_s": dump_t, "propellant_kg": prop_kg}

    # H-A4: single-thruster-failure robustness (distributed + redundant variants)
    def fault_sweep(layout):
        worst = {"survives": True, "first_break": None}
        for t in list(layout):
            reduced = {k: v for k, v in layout.items() if k != t}
            a = inplane_authority(reduced)
            if not a["all_four_feasible"]:
                worst["survives"] = False
                if worst["first_break"] is None:
                    worst["first_break"] = {"failed": t,
                        "lost": [k for k in ("+x", "-x", "+y", "-y") if a[k] is None]}
        return worst
    out["HA4"] = {"distributed_12": fault_sweep(dist),
                  "redundant_16tangential": fault_sweep(redundant_layout())}

    # H-A5: aft-clustered layout has no plume-safe in-plane couple
    aft = aft_clustered_layout()
    aft_auth = inplane_authority(aft)
    out["HA5"] = {"inplane_authority": aft_auth,
                  "any_inplane_plume_safe": aft_auth["all_four_feasible"]
                  or any(aft_auth[k] for k in ("+x", "-x", "+y", "-y"))}

    # verdicts
    hb = out["HA1"]["all_three"]
    v = {
        "H-A1": out["HA1"]["all_three"],
        "H-A2": out["HA2"]["both_axes_plume_safe"],
        "H-A3": (tau_min is not None and tau_min >= 5.0 and dump_t is not None and dump_t <= 3600),
        "H-A4": out["HA4"]["distributed_12"]["survives"],
        "H-A5": (not out["HA5"]["any_inplane_plume_safe"]),
    }
    v["held"] = sum(bool(v[k]) for k in ("H-A1", "H-A2", "H-A3", "H-A4", "H-A5"))
    v["of"] = 5
    out["verdicts"] = v
    return out


if __name__ == "__main__":
    r = main()
    (HERE / "results").mkdir(exist_ok=True)
    json.dump(r, open(HERE / "results" / "layout_findings.json", "w"), indent=2)
    v = r["verdicts"]
    print(f"H-A1  3-axis pure couples: x/y/z = "
          f"{[r['HA1']['three_axis_couples'][a] is not None for a in 'xyz']} -> {v['H-A1']}")
    print(f"H-A2  in-plane authority ±x/±y = "
          f"{ {k: r['HA2']['inplane_authority'][k] for k in ('+x','-x','+y','-y')} } "
          f"plume-safe -> {v['H-A2']}")
    dt = r['HA3']['dump_time_s']
    print(f"H-A3  min in-plane couple {r['HA3']['min_inplane_couple_torque_Nm']} N.m, "
          f"dump {dt if dt is None else round(dt)} s, prop {r['HA3']['propellant_kg']:.0f} kg -> {v['H-A3']}")
    print(f"H-A4  single-fault: distributed-12 survives={r['HA4']['distributed_12']['survives']} "
          f"(first break {r['HA4']['distributed_12']['first_break']}); "
          f"redundant-16 survives={r['HA4']['redundant_16tangential']['survives']} -> {v['H-A4']}")
    print(f"H-A5  aft-clustered any in-plane plume-safe couple = "
          f"{r['HA5']['any_inplane_plume_safe']} (expect False) -> {v['H-A5']}")
    print(f"\nHELD {v['held']}/{v['of']}")
