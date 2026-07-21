#!/usr/bin/env python3
"""R-leo-depot-bootstrap — water interest rate + fleet ledger vs H1-H4."""
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
CASES = {"canonical_40t": (40_000.0, 20_000.0 + 79.8e3 * 1.2 + 2_500.0),
         "big_80t": (80_000.0, 20_000.0 + 58.8e3 * 1.2 + 2_500.0)}
MODES = {"lit_spiral_800s": (15_700.0, VE_MET),
         "depot_kick_450s": (7_300.0, 450.0 * G0),
         "depot_kick_480s": (7_300.0, 480.0 * G0)}

rates, ledger = {}, {}
for case, (dm, hw) in CASES.items():
    for mode, (dv, ve) in MODES.items():
        prop = hw * (math.exp(dv / ve) - 1)
        r = prop / dm
        rates[f"{case}_{mode}"] = round(r, 1)
        lvl, levels = 500_000.0, [500.0]          # 500 t seed depot
        for _ in range(10):
            lvl += dm - prop
            levels.append(lvl / 1000)
        ledger[f"{case}_{mode}"] = levels
be = {c: round(v * math.log(1 + CASES[c][0] / CASES[c][1]))
      for c, v in (("canonical_40t", VE_MET), ("big_80t", VE_MET))}
salv = {c: round((20_000.0 + CASES[c][0]) * (1 - math.exp(-1000.0 / VE_MET)) / CASES[c][0], 3)
        for c in CASES}
worst_net = min(CASES[c][0] / 1000 - min(
    CASES[c][1] * (math.exp(dv / ve) - 1) for dv, ve in MODES.values()) / 1000
    for c in CASES)  # most favorable per-mission net, t
best_rate = min(rates.values())
findings = {
    "H1": {"rates": rates, "held": bool(4.3 <= best_rate and max(rates.values()) <= 18.9)},
    "H2": {"break_even_dv_800s": be, "cheapest_real_outbound": 7300,
           "held": bool(max(be.values()) < 7300)},
    "H3": {"best_net_per_mission_t": round(worst_net, 1),
           "drain_per_delivered_t": round(-worst_net / 80.0, 2),
           "held": bool(worst_net < 0 and (-worst_net / 80.0) >= 3.3)},
    "H4": {"salvage_rates": salv, "held": bool(all(0.15 <= v <= 0.18 for v in salv.values()))},
}
fig, ax = plt.subplots(figsize=(9, 5))
for k, lv in ledger.items():
    ls = "-" if "big" in k else "--"
    ax.plot(range(len(lv)), lv, ls, lw=1.6, label=k.replace("_", " "))
ax.axhline(0, color="#26251f", lw=1)
ax.set_xlabel("missions flown on depot water")
ax.set_ylabel("depot inventory [t] (500 t seed)")
ax.set_title("The bootstrap drains: every depot-fueled outbound empties the depot it feeds")
ax.grid(True, alpha=0.25)
ax.legend(fontsize=7.5)
fig.tight_layout()
fig.savefig(RESULTS / "depot_ledger.png", dpi=160)
with open(RESULTS / "findings.json", "w") as fh:
    json.dump(findings, fh, indent=1, default=float)
for h in ("H1", "H2", "H3", "H4"):
    print(h, "HELD" if findings[h]["held"] else "FALSIFIED")
print("rates:", rates, "| break-even:", be, "| salvage:", salv)
