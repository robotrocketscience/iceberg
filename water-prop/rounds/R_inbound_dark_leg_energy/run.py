#!/usr/bin/env python3
"""R-inbound-dark-leg-energy — non-fission inbound sweep vs H1-H4.

Bank size x array x lit-radius sweep on the return leg. Deterministic.
"""
import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
RESULTS.mkdir(exist_ok=True)

G0 = 9.80665
YEAR = 3.156e7
SATURN_R = 9.54
A = (1 + SATURN_R) / 2
ECC = (SATURN_R - 1) / (SATURN_R + 1)
T_FULL = A ** 1.5 * YEAR
VE_MET = 800.0 * G0
VE_CHEM = 450.0 * G0
ETA_THR = 0.6
ETA_CHG = 0.66
LHV = 13.3e6
SHIP_DRY = 20_000.0
CHUNK = 40_000.0
DV_BUDGET = 4200.0
DV_DEPART = 1500.0
MARGIN = 1.05
TANK_FRAC = 0.20
ZBO_KG_PER_T_GAS = 1.5 * 50 / 9        # cold tier: 1.5 W/t-LH2 * 50 kg/W, LH2=gas/9
BASELINE_LAUNCH_PER_DELIVERED = 50.0 / 40.0   # reactor baseline: ~50 t stack / 40 t chunk

n = 4000
E = np.linspace(0, math.pi, n)
M = E - ECC * np.sin(E)
t_grid = M / (2 * math.pi) * T_FULL
r_grid = A * (1 - ECC * np.cos(E))


def harvest(array_kw, r_max):
    m = r_grid <= r_max
    return float(np.trapezoid(array_kw * 1e3 / r_grid[m] ** 2, t_grid[m]))


def lit_dv(array_kw, r_lit, stack_kg):
    e = harvest(array_kw, r_lit)
    prop = e * ETA_THR / (0.5 * VE_MET ** 2)
    return VE_MET * math.log((stack_kg + prop) / stack_kg), prop


def departure_gas(bank_total_kg):
    """Gas consumed by the 1.5 km/s departure with the whole bank aboard."""
    m0 = SHIP_DRY + CHUNK + bank_total_kg * (1 + TANK_FRAC)
    return m0 * (1 - math.exp(-DV_DEPART / VE_CHEM))


findings = {}

# --- H1 ---
dv_l, prop_l = lit_dv(83.0, 3.5, SHIP_DRY + CHUNK)
findings["H1"] = {"lit_dv_m_s": round(dv_l), "lit_prop_t": round(prop_l / 1000, 1),
                  "held": bool(1340 <= dv_l <= 1810)}

# --- H2 ---
gas_dep = departure_gas(26_400.0)
charge = gas_dep * LHV / ETA_CHG
harv_out = harvest(83.0, 3.0)
findings["H2"] = {"gas_depart_t": round(gas_dep / 1000, 1),
                  "charge_GJ": round(charge / 1e9), "harvest_GJ": round(harv_out / 1e9),
                  "held": bool(22_400 <= gas_dep <= 30_400 and charge <= harv_out)}

# --- H3: sweep ---
banks = np.arange(20_000, 55_001, 2_500)
arrays = np.arange(60, 151, 10)
r_lits = [3.0, 3.5, 4.0]
best = None
closure_grid = np.zeros((len(arrays), len(banks)))
for ia, akw in enumerate(arrays):
    for ib, bank in enumerate(banks):
        for r_l in r_lits:
            gas_d = departure_gas(bank)
            if gas_d > bank:
                continue
            resid_gas = bank - gas_d
            # residual gas burned direct at 450 s mid-cruise on post-departure stack
            m_mid = SHIP_DRY + CHUNK + resid_gas * (1 + TANK_FRAC)
            dv_gas_resid = VE_CHEM * math.log(m_mid / (m_mid - resid_gas)) if resid_gas > 0 else 0.0
            dvl, _ = lit_dv(akw, r_l, SHIP_DRY + CHUNK)
            total = DV_DEPART + dv_gas_resid + dvl
            # charge feasibility on the outbound window
            if bank * LHV / ETA_CHG > harvest(akw, 3.0):
                continue
            if total >= DV_BUDGET * MARGIN:
                closure_grid[ia, ib] = 1
                penalty = bank * (1 + TANK_FRAC) + bank / 1000 * ZBO_KG_PER_T_GAS \
                    + (akw - 83) * 1000 / 120 if akw > 83 else bank * (1 + TANK_FRAC) + bank / 1000 * ZBO_KG_PER_T_GAS
                if best is None or penalty < best["penalty_kg"]:
                    best = {"bank_t": bank / 1000, "array_kW": int(akw), "r_lit_AU": r_l,
                            "total_dv": round(total), "penalty_kg": penalty}
if best:
    best["penalty_t"] = round(best.pop("penalty_kg") / 1000, 1)
closes = best is not None
h3_held = bool(closes and 40.0 <= best["penalty_t"] <= 55.0)
findings["H3"] = {"closes": closes, "best": best, "held": h3_held}

# --- H4 ---
if closes:
    launch_variant = 50.0 + best["penalty_t"]     # baseline stack + penalty
    ratio = (launch_variant / 40.0) / BASELINE_LAUNCH_PER_DELIVERED
    findings["H4"] = {"launch_per_delivered_ratio": round(ratio, 2),
                      "held": bool(ratio >= 1.6)}
else:
    findings["H4"] = {"held": False, "note": "no closing corner"}

# --- figure ---
fig, ax = plt.subplots(figsize=(9, 5.5))
im = ax.imshow(closure_grid, origin="lower", aspect="auto",
               cmap=plt.matplotlib.colors.ListedColormap(["#e34948", "#256abf"]),
               extent=[banks[0] / 1000, banks[-1] / 1000, arrays[0], arrays[-1]])
if best:
    ax.plot(best["bank_t"], best["array_kW"], "o", ms=12, mfc="none",
            mec="#26251f", mew=2.5)
    ax.annotate(f"cheapest closing corner:\n{best['bank_t']:.0f} t bank, "
                f"{best['array_kW']} kW, {best['penalty_t']} t penalty",
                (best["bank_t"], best["array_kW"]), textcoords="offset points",
                xytext=(14, -34), fontsize=9, color="#fcfcfb")
ax.set_xlabel("banked H2/O2 [t]")
ax.set_ylabel("array rating at 1 AU [kW]")
ax.set_title("Non-fission inbound: blue closes the 4.2 km/s budget (best lit-radius per cell)")
fig.tight_layout()
fig.savefig(RESULTS / "dark_leg_closure.png", dpi=160)

with open(RESULTS / "findings.json", "w") as fh:
    json.dump(findings, fh, indent=1, default=float)

for h in ["H1", "H2", "H3", "H4"]:
    print(h, "HELD" if findings[h]["held"] else "FALSIFIED")
print("H1 lit dv:", findings["H1"]["lit_dv_m_s"], "| H2 gas:", findings["H2"]["gas_depart_t"])
print("H3 best:", findings["H3"]["best"])
print("H4:", findings["H4"])
