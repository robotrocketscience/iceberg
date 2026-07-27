"""R-chunk-capture-closing-velocity-window — floor vs ceiling window-existence test.

Derives, per chunk mass, (1) a FLOOR on achievable closing velocity from B-ring
dynamics (chunk spin surface velocity omega*r + Hill shear + dispersion + GNC
deadband) and (2) a mass-scaled containment CEILING on survivable closing velocity
(bag-fabric strain-energy limit + peak-deceleration membrane-tear limit), and asks
whether floor < ceiling (a feasible window) at achievable operating points. Also
computes a secondary chunk-fragmentation threshold.

Pre-registered H-J1..H-J5. See SCOPE.md. Deterministic.

Sources for anchors: Cassini spin prior (tier_0_5_spin_prior.md: Spilker 2006,
Morishima 2010/2012, Ohtsuki 2005); Zylon PBO Toyobo datasheet (5.8 GPa UTS, 3.5%
strain, 1540 kg/m3); Kevlar-49 DuPont (3.6 GPa, 2.4%, 1440); ring-ice tensile
1-100 kPa (cometary/rubble-pile analog).
"""
from __future__ import annotations

import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent

# ---------------- anchors ----------------
RHO_ICE = 500.0                                  # kg/m^3 porous ring aggregate
OMEGA_BRING = 2 * math.pi / (11.0 * 3600.0)      # rad/s (B-ring period 11.0 h)
SPIN_RPM = {"p50": 0.01, "p95": 0.05, "fast": 0.28}   # 1-10 m bin (tier_0_5)
V_DISP = 1.0e-3                                   # m/s dispersion (cold B-ring)
V_GNC = 1.0e-3                                    # m/s GNC deadband (conops Hill drift)
SHEAR_UPPER_M_S_PER_KM = 1.95                     # fine-structure round upper anchor

# fabric toughness U = 0.5*sigma*eps/rho  [J/kg]
FABRIC = {
    "zylon":       {"U": 0.5 * 5.8e9 * 0.035 / 1540.0, "spec_str": 5.8e9 / 1540.0, "areal": 0.30},
    "kevlar":      {"U": 0.5 * 3.6e9 * 0.024 / 1440.0, "spec_str": 3.6e9 / 1440.0, "areal": 0.30},
    "lightweight": {"U": 0.5 * 3.6e9 * 0.024 / 1440.0 * 0.5, "spec_str": 3.6e9 / 1440.0, "areal": 0.10},
}
K_BAG = 2.0                                       # bag area / chunk surface (aperture > chunk)
ICE_TENSILE_PA = {"weak_1kPa": 1e3, "mid_10kPa": 1e4, "strong_100kPa": 1e5}
MASSES_T = [1, 10, 50, 200]


def radius(mass_t, rho=RHO_ICE):
    return (3.0 * mass_t * 1000.0 / (4.0 * math.pi * rho)) ** (1.0 / 3.0)


# ---------------- floor ----------------
def v_spin(mass_t, rpm):
    return rpm * 2 * math.pi / 60.0 * radius(mass_t)


def v_shear_hill(mass_t):
    return 1.5 * OMEGA_BRING * (2.0 * radius(mass_t))     # (3/2) Omega * envelope(=diameter)


def v_shear_upper(mass_t):
    return SHEAR_UPPER_M_S_PER_KM / 1000.0 * (2.0 * radius(mass_t))


def floor(mass_t, spin_key, despun=False, shear="hill"):
    vs = 0.0 if despun else v_spin(mass_t, SPIN_RPM[spin_key])
    vsh = v_shear_upper(mass_t) if shear == "upper" else v_shear_hill(mass_t)
    return math.sqrt(vs**2 + vsh**2 + V_DISP**2 + V_GNC**2)


# ---------------- ceiling ----------------
def ceiling_energy(mass_t, fabric, f_part):
    r = radius(mass_t)
    A_bag = K_BAG * 4 * math.pi * r**2
    m_fab = FABRIC[fabric]["areal"] * A_bag * f_part
    return math.sqrt(2 * FABRIC[fabric]["U"] * m_fab / (mass_t * 1000.0))


def ceiling_force(mass_t, fabric, stroke_frac=1.0):
    """Peak-decel membrane-tear limit. F=m v^2/(2s) reacted as line load around
    perimeter 2*pi*r_bag; N_cap = areal * specific_strength. v = sqrt(4 pi areal
    spec_str r^2 / m) with stroke s = stroke_frac*r, r_bag = r."""
    r = radius(mass_t)
    s = stroke_frac * r
    N_cap = FABRIC[fabric]["areal"] * FABRIC[fabric]["spec_str"]     # N/m
    F_cap = N_cap * 2 * math.pi * r
    return math.sqrt(2 * s * F_cap / (mass_t * 1000.0))


def ceiling(mass_t, fabric, f_part):
    return min(ceiling_energy(mass_t, fabric, f_part), ceiling_force(mass_t, fabric))


def v_fragment(sigma_ice_pa):
    """Deceleration stress on contact area pi r^2 exceeds ice tensile. Mass-independent:
    v = sqrt(3 sigma_ice / (2 rho)) since r^3/m = 3/(4 pi rho)."""
    return math.sqrt(3.0 * sigma_ice_pa / (2.0 * RHO_ICE))


def main():
    strong = ("zylon", 1.0)                    # whole-bag Zylon
    f_patch = 1.0 / (4 * K_BAG)                # contact-patch fraction = pi r^2 / (K 4 pi r^2)
    pessim = ("lightweight", f_patch)          # contact-patch + lightweight

    grid = {}
    for m in MASSES_T:
        r = radius(m)
        row = {
            "radius_m": round(r, 3),
            "floor_mms": {
                "p50": round(floor(m, "p50") * 1e3, 3),
                "p95": round(floor(m, "p95") * 1e3, 3),
                "fast": round(floor(m, "fast") * 1e3, 3),
                "p50_despun": round(floor(m, "p50", despun=True) * 1e3, 3),
                "p95_upper_shear": round(floor(m, "p95", shear="upper") * 1e3, 3),
            },
            "floor_terms_mms": {
                "v_spin_p50": round(v_spin(m, SPIN_RPM["p50"]) * 1e3, 3),
                "v_spin_p95": round(v_spin(m, SPIN_RPM["p95"]) * 1e3, 3),
                "v_shear_hill": round(v_shear_hill(m) * 1e3, 3),
                "v_shear_upper": round(v_shear_upper(m) * 1e3, 3),
                "v_disp": round(V_DISP * 1e3, 3), "v_gnc": round(V_GNC * 1e3, 3),
            },
            "ceiling_ms": {
                "strong_zylon_wholebag": round(ceiling(m, *strong), 2),
                "kevlar_wholebag": round(ceiling(m, "kevlar", 1.0), 2),
                "pessim_patch_light": round(ceiling(m, *pessim), 3),
                "energy_strong": round(ceiling_energy(m, "zylon", 1.0), 2),
                "force_strong": round(ceiling_force(m, "zylon"), 2),
            },
            "window_ratio": {
                "strong_over_floor_p50": round(ceiling(m, *strong) / floor(m, "p50"), 0),
                "pessim_over_floor_p50": round(ceiling(m, *pessim) / floor(m, "p50"), 0),
                "pessim_over_floor_p95": round(ceiling(m, *pessim) / floor(m, "p95"), 0),
                "pessim_over_floor_fast": round(ceiling(m, *pessim) / floor(m, "fast"), 0),
            },
        }
        grid[f"{m}t"] = row

    frag = {k: round(v_fragment(v), 2) for k, v in ICE_TENSILE_PA.items()}

    # ---------------- grade ----------------
    # H-J1: p50 floor <= 30 mm/s all masses; p95 <= ~150 mm/s; spin dominates un-despun
    hj1_p50 = all(grid[f"{m}t"]["floor_mms"]["p50"] <= 30 for m in MASSES_T)
    hj1_p95 = all(grid[f"{m}t"]["floor_mms"]["p95"] <= 150 for m in MASSES_T)
    hj1_spin_dom = all(grid[f"{m}t"]["floor_terms_mms"]["v_spin_p50"] >=
                       grid[f"{m}t"]["floor_terms_mms"]["v_shear_hill"] for m in MASSES_T)
    hj1 = hj1_p50 and hj1_p95 and hj1_spin_dom

    # H-J2: strong ceiling 5-30 m/s; pessim >= 1.5 m/s all masses (secondary); mass-scaling ~ m^-1/6
    hj2_strong = all(5 <= grid[f"{m}t"]["ceiling_ms"]["strong_zylon_wholebag"] <= 30 for m in MASSES_T)
    hj2_pessim = all(grid[f"{m}t"]["ceiling_ms"]["pessim_patch_light"] >= 1.5 for m in MASSES_T)
    # scaling: ceiling ratio 1t/200t vs (200)^(1/6) ~ 2.42
    scale_obs = grid["1t"]["ceiling_ms"]["strong_zylon_wholebag"] / grid["200t"]["ceiling_ms"]["strong_zylon_wholebag"]
    hj2 = hj2_strong  # primary claim; hj2_pessim reported separately (see note)

    # H-J3 LOAD-BEARING: ceiling/floor >= 100 at p50 all masses; >= 10 at p95 pessimistic
    hj3_p50 = all(grid[f"{m}t"]["window_ratio"]["strong_over_floor_p50"] >= 100 for m in MASSES_T)
    hj3_p95 = all(grid[f"{m}t"]["window_ratio"]["pessim_over_floor_p95"] >= 10 for m in MASSES_T)
    hj3 = hj3_p50 and hj3_p95

    # H-J4: 1 kPa fragmentation < strong bag-tear ceiling (binds first) but > p50 floor (contained rubble)
    frag_weak = v_fragment(ICE_TENSILE_PA["weak_1kPa"])
    hj4_binds = all(frag_weak < grid[f"{m}t"]["ceiling_ms"]["strong_zylon_wholebag"] for m in MASSES_T)
    hj4_above_floor = all(frag_weak > floor(m, "p50") for m in MASSES_T)
    hj4 = hj4_binds and hj4_above_floor

    # H-J5: p95 (and fast) un-despun floor >= 10x below pessimistic ceiling all masses
    hj5_p95 = all(grid[f"{m}t"]["window_ratio"]["pessim_over_floor_p95"] >= 10 for m in MASSES_T)
    hj5_fast = all(grid[f"{m}t"]["window_ratio"]["pessim_over_floor_fast"] >= 10 for m in MASSES_T)
    hj5 = hj5_p95 and hj5_fast

    verdicts = {
        "H-J1": {"held": bool(hj1), "p50_le30": bool(hj1_p50), "p95_le150": bool(hj1_p95),
                 "spin_dominates": bool(hj1_spin_dom)},
        "H-J2": {"held": bool(hj2), "strong_5_30": bool(hj2_strong),
                 "pessim_ge_1p5": bool(hj2_pessim), "scale_1t_over_200t": round(scale_obs, 2),
                 "expected_m_pow_1_6": round(200 ** (1 / 6), 2)},
        "H-J3": {"held": bool(hj3), "ge100_at_p50": bool(hj3_p50), "ge10_at_p95_pessim": bool(hj3_p95)},
        "H-J4": {"held": bool(hj4), "frag_weak_1kPa_ms": round(frag_weak, 2),
                 "binds_below_bagtear": bool(hj4_binds), "above_p50_floor": bool(hj4_above_floor)},
        "H-J5": {"held": bool(hj5), "p95_ge10x": bool(hj5_p95), "fast_ge10x": bool(hj5_fast)},
    }
    verdicts["held_count"] = sum(1 for k in ("H-J1", "H-J2", "H-J3", "H-J4", "H-J5") if verdicts[k]["held"])
    verdicts["of"] = 5

    out = {
        "anchors": {"rho_ice": RHO_ICE, "omega_bring": OMEGA_BRING, "spin_rpm": SPIN_RPM,
                    "v_disp_mms": V_DISP * 1e3, "v_gnc_mms": V_GNC * 1e3,
                    "fabric_U_J_per_kg": {k: round(v["U"]) for k, v in FABRIC.items()},
                    "k_bag": K_BAG, "ice_tensile_pa": ICE_TENSILE_PA},
        "grid": grid, "fragmentation_ms": frag, "verdicts": verdicts,
    }
    (HERE / "results").mkdir(exist_ok=True)
    json.dump(out, open(HERE / "results" / "closing_velocity_window.json", "w"), indent=2)

    # ---------------- print ----------------
    print("Closing-velocity WINDOW — floor (mm/s) vs ceiling (m/s), by chunk mass")
    print(f"  {'mass':>5} {'r(m)':>5} | {'floor_p50':>9} {'floor_p95':>9} | "
          f"{'ceil_strong':>11} {'ceil_pessim':>11} | {'ratio_p50':>9} {'ratio_p95p':>10}")
    for m in MASSES_T:
        g = grid[f"{m}t"]
        print(f"  {m:>4}t {g['radius_m']:>5.2f} | {g['floor_mms']['p50']:>7.2f}mm {g['floor_mms']['p95']:>7.2f}mm | "
              f"{g['ceiling_ms']['strong_zylon_wholebag']:>9.1f}   {g['ceiling_ms']['pessim_patch_light']:>9.2f}   | "
              f"{g['window_ratio']['strong_over_floor_p50']:>8.0f}x {g['window_ratio']['pessim_over_floor_p95']:>9.0f}x")
    print(f"\n  Fragmentation threshold (mass-independent): "
          f"1kPa {frag['weak_1kPa']} / 10kPa {frag['mid_10kPa']} / 100kPa {frag['strong_100kPa']} m/s")
    print()
    for k in ("H-J1", "H-J2", "H-J3", "H-J4", "H-J5"):
        print(f"  {k}: {'HELD' if verdicts[k]['held'] else 'FALSIFIED':>9}  {verdicts[k]}")
    print(f"\n  HELD {verdicts['held_count']}/{verdicts['of']}")


if __name__ == "__main__":
    main()
