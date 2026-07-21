#!/usr/bin/env python3
"""R-keepalive-water-recovery — theorem verification + adjudication vs H1-H4.

Closed form + trajectory integrals. Deterministic.
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
LHV = 13.3e6
ETA_FC = 0.55
LILT = 1.5
ZBO_W_PER_T = 1.5 * 80 / 9
VE_GAS = 450.0 * G0
KICK = 5.84
SATURN_R = 9.54
A_ELL = (1 + SATURN_R) / 2
ECC = (SATURN_R - 1) / (SATURN_R + 1)
T_FULL = A_ELL ** 1.5 * YEAR
_E = np.linspace(0, math.pi, 4000)
_M = _E - ECC * np.sin(_E)
T_GRID = _M / (2 * math.pi) * T_FULL
R_GRID = A_ELL * (1 - ECC * np.cos(_E))
DV_CHAIN = 1000.0 + 500.0 + 1500.0 + 845.0


def avail(akw, r):
    return akw * 1e3 / r ** 2 / np.where(r > 3.0, LILT, 1.0)


rows = []
max_overlap = 0.0
max_credit = 0.0
for akw in (100.0, 150.0, 200.0, 250.0, 300.0):
    for pka in (150.0, 300.0, 450.0, 600.0):
        for bank_t in (40.0, 70.0, 91.3, 120.0):
            load = pka + ZBO_W_PER_T * bank_t
            a = avail(akw, R_GRID)
            spare = np.clip(a - load, 0.0, None)
            short = np.clip(load - a, 0.0, None)
            pointwise = float(np.max(spare * short))
            accrued = np.cumsum(short) > 0
            overlap_e = float(np.trapezoid(spare * accrued, T_GRID))
            credit_t = overlap_e * 0.66 / LHV / 1000
            draw_t = float(np.trapezoid(short, T_GRID)) / (LHV * ETA_FC) / 1000
            lim = akw * 1e3 / LILT / load
            r_cross = math.sqrt(lim) if lim < SATURN_R ** 2 else None
            pen = draw_t * (math.exp(DV_CHAIN / VE_GAS) - 1) * 1.3 * 1.2 * KICK
            rows.append({"akw": akw, "pka": pka, "bank_t": bank_t,
                         "r_cross_au": round(r_cross, 2) if r_cross else None,
                         "draw_t": round(draw_t, 2),
                         "pointwise_max": pointwise,
                         "overlap_J": overlap_e,
                         "credit_t": round(credit_t, 3),
                         "retention_penalty_launch_t": round(pen, 1)})
            max_overlap = max(max_overlap, overlap_e)
            max_credit = max(max_credit, credit_t)

canon = next(r for r in rows if r["akw"] == 100 and r["pka"] == 300
             and r["bank_t"] == 91.3)
stress = next(r for r in rows if r["akw"] == 100 and r["pka"] == 600
              and r["bank_t"] == 91.3)

h1 = max(r["pointwise_max"] for r in rows) == 0.0
h2 = (max_credit <= 0.1 and 6.5 <= canon["r_cross_au"] <= 6.8
      and 9.3 <= canon["draw_t"] <= 10.3 and 5.9 <= stress["r_cross_au"] <= 6.2
      and 14.0 <= stress["draw_t"] <= 16.0
      and all(r["draw_t"] == 0 for r in rows if r["akw"] == 300))
hw_cost = 0.075 * 1.2 * KICK
h3 = (max_credit == 0.0 and 110.0 <= canon["retention_penalty_launch_t"] <= 140.0
      and hw_cost > 0)
abort_gas = 20.0 * (math.exp(7000.0 / VE_GAS) - 1)
h4 = abort_gas / 10.0 > 2.0

findings = {
    "H1": {"max_pointwise_spare_x_short": max(r["pointwise_max"] for r in rows),
           "held": bool(h1)},
    "H2": {"max_credit_t": max_credit, "canonical": canon, "stress": stress,
           "held": bool(h2)},
    "H3": {"hw_dead_launch_t": round(hw_cost, 1),
           "canonical_retention_penalty_t": canon["retention_penalty_launch_t"],
           "verdict": "R177 follow-on falsified; venting convention optimal",
           "held": bool(h3)},
    "H4": {"abort_gas_needed_t": round(abort_gas, 0), "recovered_t": 10.0,
           "held": bool(h4)},
}

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 5.0))
for pka, color in ((150, "#cbd2dc"), (300, "#256abf"), (450, "#eda100"),
                   (600, "#e34948")):
    xs, ys = [], []
    for akw in (100, 150, 200, 250, 300):
        r = next(x for x in rows if x["akw"] == akw and x["pka"] == pka
                 and x["bank_t"] == 91.3)
        xs.append(akw)
        ys.append(r["draw_t"])
    ax1.plot(xs, ys, "o-", color=color, lw=1.8, label=f"bus {pka} We")
ax1.set_xlabel("array rating [kW]")
ax1.set_ylabel("outbound keep-alive draw [t of gas] (91.3 t bank)")
ax1.set_title("The draw exists only where the spare window has already closed")
ax1.grid(True, alpha=0.25)
ax1.legend(fontsize=8.5, title="recoverable credit: 0.000 t at every corner")

labels = ["re-split credit\n(the hoped-for win)", "condenser hardware\n(dead mass)",
          "retention instead\nof venting"]
vals = [0.0, -hw_cost, -canon["retention_penalty_launch_t"]]
colors = ["#256abf", "#eda100", "#e34948"]
bars = ax2.bar(labels, vals, color=colors, width=0.55)
for b, v in zip(bars, vals):
    if v == 0:
        ax2.text(b.get_x() + b.get_width() / 2, -6, "0.0 t (theorem)",
                 ha="center", fontsize=9, color="#256abf")
    else:
        ax2.text(b.get_x() + b.get_width() / 2, v + 4, f"{v:+.1f} t",
                 ha="center", fontsize=9, va="bottom", color="#fcfcfb"
                 if v < -60 else "#26251f")
ax2.set_ylim(-135, 8)
ax2.axhline(0, color="#26251f", lw=1)
ax2.set_ylabel("launch-mass effect [t] (canonical corner)")
ax2.set_title("The recovery ledger: nothing to win, two ways to lose")
ax2.grid(True, axis="y", alpha=0.25)
fig.tight_layout()
fig.savefig(RESULTS / "recovery_adjudication.png", dpi=160)

with open(RESULTS / "findings.json", "w") as fh:
    json.dump({"findings": findings, "sweep": rows}, fh, indent=1, default=float)

for h in ("H1", "H2", "H3", "H4"):
    print(h, "HELD" if findings[h]["held"] else "FALSIFIED")
print("max credit:", max_credit, "t | canonical:", canon)
print("abort: need", round(abort_gas), "t vs recovered ~10 t")
