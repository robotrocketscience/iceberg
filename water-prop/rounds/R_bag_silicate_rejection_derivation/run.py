"""R-bag-silicate-rejection-derivation — derive the bag rejection factor from physics.

The bag is a sublimation still: ring ice sublimates, water vapor feeds the thruster,
silicate inclusions are left behind IF they are not entrained. Derives the carryover
(pass) fraction f_pass = (silicate PSD mass fraction that is both lofted and
transported to the collector), from:
  - free-molecular (Epstein) entrainment cutoff d_max(T) = rho_gas(T)*L/rho_grain,
  - van-der-Waals adhesion (holds fine grains unless electrostatically lofted),
  - electrostatic lofting of the sub-micron nano-tail (residual leak even when cold),
integrated over a silicate inclusion PSD, then closes the loop through R11's
silicate -> grid-wear mapping to grid life vs the multi-year burn.

Pre-registered H-K1..H-K5. See SCOPE.md. Deterministic.

Sources: Marti & Mauersberger 1993 (ice sublimation P_sat); Hsu 2011 (Nature 471,
393) + Hsu 2018 (Science 362) nanometre SiO2 in Saturn ring-fall/stream particles
(inclusion PSD within main-ring ice is NOT directly measured -- the load-bearing
gap); R11_grid_life_silicate_contamination (NSTAR 30352 h/235 kg Xe; 400 g -> 2.4%
grid thickness; silicate:Xe sputter 3.5x).
"""
from __future__ import annotations

import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent

# --- constants ---
M_H2O = 0.018015
R_UNIV = 8.314
R_SPEC = R_UNIV / M_H2O
RHO_GRAIN = 3000.0
L_TRANSPORT = 1.0
MDOT = 5.0e-4                      # kg/s (0.5 g/s)
TEMPS = [200, 220, 250, 273]

# PSD anchors
Q_POW = 3.5                       # power-law dN/dr ~ r^-q
R_MIN = 5e-9                      # 5 nm (Hsu nano-silica floor)
R_MAX_CASES = {"rmax_1um": 1e-6, "rmax_100um": 1e-4}
PHI_NANO_CASES = {"low_1e-3": 1e-3, "hsu_0.1": 0.1, "hsu_0.3": 0.3}   # sub-100nm mass frac
D_NANO = 100e-9                   # nano-mode upper bound (diameter)

# electrostatic residual
G_GEOM = {"optimistic": 1e-2, "pessimistic": 1e-1}   # frac of lofted nano reaching collector

# grid-life loop (R11)
SILICATE_FRAC = 0.003             # 0.3% non-icy in ring water
M_PROP_T = 690.0                  # t water processed over the burn (Round F H2/O2)
GRID_SILICATE_BUDGET_KG = 0.400 / 0.024   # R11: 400 g -> 2.4% thickness => 16.7 kg to 100%


def p_sat_ice(T):
    return 10 ** (-2663.5 / T + 12.537)


def vapor(T):
    P = p_sat_ice(T)
    rho_g = P * M_H2O / (R_UNIV * T)
    J = P / math.sqrt(2 * math.pi * R_SPEC * T)
    d_max = rho_g * L_TRANSPORT / RHO_GRAIN
    A_ice = MDOT / J
    return {"P_sat": P, "rho_g": rho_g, "J": J, "d_max": d_max, "A_ice": A_ice}


def massfrac_below_powerlaw(r_cut, r_max, q=Q_POW, r_min=R_MIN):
    """Mass fraction of a dN/dr ~ r^-q PSD with radius below r_cut."""
    if r_cut <= r_min:
        return 0.0
    r_cut = min(r_cut, r_max)
    num = r_cut ** (4 - q) - r_min ** (4 - q)
    den = r_max ** (4 - q) - r_min ** (4 - q)
    return max(0.0, num / den)


def f_pass_gas(T, r_max):
    d_max = vapor(T)["d_max"]
    return massfrac_below_powerlaw(d_max / 2.0, r_max)


def f_pass_electrostatic(phi_nano, g_geom):
    """Nano-tail (< D_NANO) electrostatically lofted, fraction g_geom reaches collector.
    Residual leak even when gas entrainment is off (cold bag)."""
    return phi_nano * g_geom


def grid_consumed(f_pass):
    silicate_to_grid = f_pass * SILICATE_FRAC * M_PROP_T * 1000.0   # kg
    return silicate_to_grid / GRID_SILICATE_BUDGET_KG               # fraction of grid life


def main():
    vap = {str(T): {k: (round(v, 4) if k not in ("d_max",) else v) for k, v in vapor(T).items()}
           for T in TEMPS}
    for T in TEMPS:
        vap[str(T)]["d_max_nm"] = round(vapor(T)["d_max"] * 1e9, 3)

    # gas-entrainment carryover grid: T x r_max
    gas = {}
    for T in TEMPS:
        gas[str(T)] = {tag: f_pass_gas(T, rm) for tag, rm in R_MAX_CASES.items()}

    # electrostatic residual: phi_nano x g_geom
    es = {pk: {gk: f_pass_electrostatic(pv, gv) for gk, gv in G_GEOM.items()}
          for pk, pv in PHI_NANO_CASES.items()}

    # effective f_pass corners (max of active channels)
    # cold bag (200K, gas off) + small nano-tail + optimistic geom
    f_cold_small = max(f_pass_gas(200, 1e-4), f_pass_electrostatic(PHI_NANO_CASES["low_1e-3"], G_GEOM["optimistic"]))
    # warm bag (273K) + power-law rmax_1um (gas dominated)
    f_warm = f_pass_gas(273, 1e-6)
    # cold bag + Hsu nano-tail (electrostatic residual dominates)
    f_cold_hsu = max(f_pass_gas(200, 1e-4), f_pass_electrostatic(PHI_NANO_CASES["hsu_0.3"], G_GEOM["pessimistic"]))
    # warm bag + Hsu (both channels; gas already ~0.88)
    f_warm_hsu = max(f_pass_gas(273, 1e-6), f_pass_electrostatic(PHI_NANO_CASES["hsu_0.3"], G_GEOM["pessimistic"]))

    corners = {
        "cold200_smallnano_opt": f_cold_small,
        "warm273_powerlaw_1um": f_warm,
        "cold200_hsu_pessim": f_cold_hsu,
        "warm273_hsu_pessim": f_warm_hsu,
        "r11_assumed_central": 1e-4,
    }
    grid = {k: {"f_pass": v, "grid_consumed": grid_consumed(v),
                "life_limited": grid_consumed(v) > 1.0} for k, v in corners.items()}

    # ---------------- grade ----------------
    d250 = vapor(250)["d_max"]
    d273 = vapor(273)["d_max"]
    d200 = vapor(200)["d_max"]
    hk1 = (50e-9 <= d250 <= 1e-6) and (1e-6 <= d273 <= 2e-6) and (d200 < 1e-9)

    a200 = vapor(200)["A_ice"]
    hk2 = a200 <= 20.0

    # H-K3: f_pass_gas ~0 cold, 1e-2..3e-1 warm; NOT robustly <1e-3 nor >1e-1 everywhere
    gas_cold = max(f_pass_gas(200, rm) for rm in R_MAX_CASES.values())
    gas_warm_lo = f_pass_gas(273, 1e-4)      # least-bad warm (rmax 100um)
    gas_warm_hi = f_pass_gas(273, 1e-6)      # worst warm (rmax 1um)
    all_vals = [f_pass_gas(T, rm) for T in TEMPS for rm in R_MAX_CASES.values()]
    hk3_gated = (gas_cold < 1e-3) and (gas_warm_hi >= 1e-2)          # spans the assumed value
    hk3_not_robust = not (all(v < 1e-3 for v in all_vals) or all(v > 1e-1 for v in all_vals))
    hk3 = hk3_gated and hk3_not_robust

    # H-K4: electrostatic residual >= 1e-3 for Hsu at pessimistic geom
    es_hsu_pess = f_pass_electrostatic(PHI_NANO_CASES["hsu_0.3"], G_GEOM["pessimistic"])
    hk4 = es_hsu_pess >= 1e-3

    # H-K5: grid fails at Hsu/warm (~1e-2) but survives at cold+smallnano (~1e-4)
    hk5_fails_hsu = grid[("warm273_hsu_pessim")]["life_limited"]
    hk5_survives_cold = not grid[("cold200_smallnano_opt")]["life_limited"]
    hk5 = hk5_fails_hsu and hk5_survives_cold

    verdicts = {
        "H-K1": {"held": bool(hk1), "d_max_nm": {str(T): round(vapor(T)["d_max"]*1e9, 3) for T in TEMPS}},
        "H-K2": {"held": bool(hk2), "A_ice_200K_m2": round(a200, 3)},
        "H-K3": {"held": bool(hk3), "gas_cold_max": gas_cold, "gas_warm_rmax1um": gas_warm_hi,
                 "gas_warm_rmax100um": gas_warm_lo, "spans_assumed_1e-4": bool(hk3_gated),
                 "not_robust_either_way": bool(hk3_not_robust)},
        "H-K4": {"held": bool(hk4), "es_hsu_pessim": es_hsu_pess},
        "H-K5": {"held": bool(hk5), "grid_consumed_warm_hsu": round(grid["warm273_hsu_pessim"]["grid_consumed"], 2),
                 "grid_consumed_cold_small": round(grid["cold200_smallnano_opt"]["grid_consumed"], 4)},
    }
    verdicts["held_count"] = sum(1 for k in ("H-K1","H-K2","H-K3","H-K4","H-K5") if verdicts[k]["held"])
    verdicts["of"] = 5

    out = {
        "anchors": {"rho_grain": RHO_GRAIN, "L_transport": L_TRANSPORT, "mdot_kg_s": MDOT,
                    "q_powerlaw": Q_POW, "r_min_nm": R_MIN*1e9, "silicate_frac": SILICATE_FRAC,
                    "m_prop_t": M_PROP_T, "grid_silicate_budget_kg": round(GRID_SILICATE_BUDGET_KG, 2)},
        "vapor": vap, "f_pass_gas": gas, "f_pass_electrostatic": es,
        "corners": grid, "verdicts": verdicts,
    }
    (HERE / "results").mkdir(exist_ok=True)
    json.dump(out, open(HERE / "results" / "bag_rejection.json", "w"), indent=2)

    # ---------------- print ----------------
    print("Derived bag silicate rejection -- carryover f_pass vs bag temperature")
    print(f"  {'T(K)':>5} {'d_max':>10} {'A_ice(m2)':>10} | {'f_pass(rmax1um)':>16} {'f_pass(rmax100um)':>18}")
    for T in TEMPS:
        v = vapor(T); dnm = v["d_max"]*1e9
        ds = f"{dnm:.2f}nm" if dnm < 1000 else f"{dnm/1000:.2f}um"
        print(f"  {T:>5} {ds:>10} {v['A_ice']:>10.3g} | {f_pass_gas(T,1e-6):>16.3e} {f_pass_gas(T,1e-4):>18.3e}")
    print(f"\n  Electrostatic residual (cold-bag leak): Hsu phi=0.3 x g_geom "
          f"{G_GEOM['optimistic']}-{G_GEOM['pessimistic']} = "
          f"{f_pass_electrostatic(0.3,1e-2):.1e}-{f_pass_electrostatic(0.3,1e-1):.1e}")
    print(f"\n  Grid-life loop (M_prop={M_PROP_T} t, 0.3% silicate, budget "
          f"{GRID_SILICATE_BUDGET_KG:.1f} kg to grid):")
    for k, g in out["corners"].items():
        flag = "LIFE-LIMITED" if g["life_limited"] else "survives"
        print(f"    {k:26} f_pass={g['f_pass']:.2e} -> grid consumed {g['grid_consumed']*100:8.2f}%  {flag}")
    print()
    for k in ("H-K1","H-K2","H-K3","H-K4","H-K5"):
        print(f"  {k}: {'HELD' if verdicts[k]['held'] else 'FALSIFIED':>9}  {verdicts[k]}")
    print(f"\n  HELD {verdicts['held_count']}/{verdicts['of']}")


if __name__ == "__main__":
    main()
