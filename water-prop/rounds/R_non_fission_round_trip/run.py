#!/usr/bin/env python3
"""R-non-fission-round-trip — end-to-end sweep vs H1-H4. Deterministic."""
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
VE_MET = 800.0 * G0
YEAR = 3.156e7
SATURN_R = 9.54
A_ELL = (1 + SATURN_R) / 2
ECC = (SATURN_R - 1) / (SATURN_R + 1)
T_FULL = A_ELL ** 1.5 * YEAR
_E = np.linspace(0, math.pi, 4000)
_M = _E - ECC * np.sin(_E)
T_GRID = _M / (2 * math.pi) * T_FULL
R_GRID = A_ELL * (1 - ECC * np.cos(_E))


def lit_dv_proper(akw, chunk):
    # bug-catch 2026-07-20: first version scaled R173's 1575 m/s linearly with
    # array and ignored stack mass, inflating lit braking ~4x at heavy corners
    # and manufacturing a false 1.4x "closing" cell. Proper form below.
    m = R_GRID <= 4.0
    e = float(np.trapezoid(akw * 1e3 / R_GRID[m] ** 2, T_GRID[m]))
    prop = e * 0.6 / (0.5 * VE_MET ** 2)
    m1 = SHIP_DRY + chunk
    return VE_MET * math.log((m1 + prop) / m1)
SHIP_DRY = 20_000.0
TANK = 0.20
ZBO_KG_PER_T = 1.5 * 50 / 9
HOTEL_GAS = 2_600.0
DV_DEPART = 1500.0
DV_BUDGET_IN = 4200.0
BASELINE = 50.0 / 40.0


def chain_bank(chunk, ve_gas, dv_cap, dv_ops, lit_dv):
    bank = 40_000.0
    parts = {}
    for _ in range(80):
        m_cap = SHIP_DRY + bank * (1 + TANK)
        g_cap = m_cap * (1 - math.exp(-dv_cap / ve_gas))
        rem = bank - g_cap
        m_ops = SHIP_DRY + max(rem, 0) * (1 + TANK)
        g_ops = m_ops * (1 - math.exp(-dv_ops / ve_gas))
        rem -= g_ops + HOTEL_GAS
        m_dep = SHIP_DRY + chunk + max(rem, 0) * (1 + TANK)
        g_dep = m_dep * (1 - math.exp(-DV_DEPART / ve_gas))
        rem -= g_dep
        need = max(DV_BUDGET_IN - DV_DEPART - lit_dv, 0.0)
        m_mid = SHIP_DRY + chunk + max(rem, 0) * (1 + TANK)
        g_res = m_mid * (1 - math.exp(-need / ve_gas))
        # bug-catch 2: max(rem,0) here hid a bank deficit whenever the lit leg
        # zeroed the residual need — the loop exited at its seed value.
        shortfall = g_res - rem
        bank += shortfall * 0.7
        parts = {"cap": g_cap, "ops": g_ops, "dep": g_dep, "res": g_res}
        if abs(shortfall) < 5:
            break
    return bank, parts


results = []
for chunk in (25_000.0, 40_000.0, 80_000.0, 200_000.0):
    for akw in (100.0, 200.0, 300.0):
        for relief, (dv_cap, dv_ops) in {"nominal": (1000.0, 500.0),
                                          "moon-tour": (600.0, 300.0)}.items():
            for isp_gas in (450.0, 480.0):
                lit = lit_dv_proper(akw, chunk)
                bank, parts = chain_bank(chunk, isp_gas * G0, dv_cap, dv_ops, lit)
                if bank <= 0 or bank > 5e6:
                    continue
                array_m = akw * 1000 / 120.0
                stack = SHIP_DRY + bank * (1 + TANK) + bank / 1000 * ZBO_KG_PER_T + array_m
                kick = stack * (math.exp(7300.0 / (isp_gas * G0)) - 1) * 1.12
                spiral = stack * (math.exp(15_700.0 / VE_MET) - 1)
                for mode, extra in (("kick", kick), ("spiral", spiral)):
                    launch = (stack + extra) / 1000.0
                    ratio = (launch / (chunk / 1000.0)) / BASELINE
                    results.append({"chunk_t": chunk / 1000, "array_kW": akw,
                                    "relief": relief, "isp": isp_gas, "mode": mode,
                                    "bank_t": round(bank / 1000, 1),
                                    "launch_t": round(launch, 0),
                                    "outbound_frac": round(extra / (extra + stack), 2),
                                    "ratio": round(ratio, 1)})

canonical = [r for r in results if r["chunk_t"] == 40 and r["array_kW"] == 100
             and r["relief"] == "nominal" and r["isp"] == 450]
# note: SCOPE's scripted canonical used 83 kW / lit 1575; sweep floor is 100 kW,
# so H1 compares at the nearest swept corner — deviation recorded in STUDY.
best = min(results, key=lambda r: r["ratio"])
h1_bank = next(r["bank_t"] for r in canonical if r["mode"] == "kick")
findings = {
    "H1": {"canonical_bank_t": h1_bank, "held": bool(86 <= h1_bank <= 105)},
    "H2": {"best_corner": best, "held": bool(best["ratio"] >= 6.0)},
    "H3": {"min_outbound_frac": min(r["outbound_frac"] for r in results),
           "held": bool(all(r["outbound_frac"] >= 0.55 for r in results))},
}
findings["H4"] = {"held": bool(all(findings[h]["held"] for h in ("H1", "H2", "H3"))),
                  "statement": "R173 1.74x reframe falsified end-to-end; non-fission assets survive as components only"}

fig, ax = plt.subplots(figsize=(9, 5.5))
for mode, color in (("kick", "#e34948"), ("spiral", "#eda100")):
    pts = [r for r in results if r["mode"] == mode and r["relief"] == "moon-tour"
           and r["isp"] == 480]
    ax.scatter([r["chunk_t"] for r in pts], [r["ratio"] for r in pts],
               s=[r["array_kW"] / 3 for r in pts], color=color, alpha=0.75,
               label=f"outbound: {mode} (best-relief corners)")
ax.axhline(1.74, color="#256abf", ls="--", lw=1.2)
ax.text(120, 2.1, "R173's inbound-only 1.74x (the boundary it warned about)",
        fontsize=8.5, color="#256abf")
ax.axhline(6.0, color="#26251f", ls=":", lw=1.2)
ax.text(120, 6.6, "H2 bound: nothing under 6x", fontsize=8.5, color="#26251f")
ax.set_yscale("log")
ax.set_xlabel("chunk mass [t]")
ax.set_ylabel("launch mass per delivered tonne, ÷ reactor baseline")
ax.set_title("Non-fission round trip, end to end: the compounding the inbound round could not see")
ax.grid(True, which="both", alpha=0.25)
ax.legend(fontsize=9)
fig.tight_layout()
fig.savefig(RESULTS / "round_trip_ratio.png", dpi=160)

with open(RESULTS / "findings.json", "w") as fh:
    json.dump({"findings": findings, "sweep": results}, fh, indent=1, default=float)

for h in ("H1", "H2", "H3", "H4"):
    print(h, "HELD" if findings[h]["held"] else "FALSIFIED")
print("canonical bank:", h1_bank, "t | best corner:", best)
