#!/usr/bin/env python3
"""R-waiver-value-consolidation — NPV partition vs H1-H4. Deterministic."""
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

DELAY = 23.5 - 13.1
TIERS = {"paper": 1.02 / 0.36, "capped": 1.02 / 0.46, "flown": 2.41 / 1.33}

d_grid = np.arange(0.04, 0.1401, 0.005)
decay_grid = np.arange(0.0, 0.0801, 0.005)


def ratio(adv, d, decay):
    eff = (1 + d) * (1 + decay) - 1
    return adv / (1 + eff) ** DELAY


d_star = {t: math.exp(math.log(a) / DELAY) - 1 for t, a in TIERS.items()}
cells = {t: ratio(a, 0.08, 0.0) for t, a in TIERS.items()}
r_8_3 = ratio(TIERS["paper"], 0.08, 0.03)
r_10_0 = ratio(TIERS["paper"], 0.10, 0.0)
r_fl_8 = ratio(TIERS["flown"], 0.08, 0.0)

h1 = (0.102 <= d_star["paper"] <= 0.108 and 0.056 <= d_star["flown"] <= 0.062
      and 0.077 <= d_star["capped"] <= 0.083)
h2 = 1.22 <= cells["paper"] <= 1.32 and 1.00 <= r_10_0 <= 1.10 \
    and 0.75 <= r_fl_8 <= 0.85
h3 = r_8_3 < 1.0
h4 = h1 and h2 and h3

findings = {
    "H1": {"d_star": {t: round(v, 4) for t, v in d_star.items()}, "held": bool(h1)},
    "H2": {"paper_at_8pct": round(cells["paper"], 2),
           "paper_at_10pct": round(r_10_0, 2),
           "flown_at_8pct": round(r_fl_8, 2), "held": bool(h2)},
    "H3": {"paper_at_8pct_3decay": round(r_8_3, 2), "held": bool(h3)},
    "H4": {"statement": "waiver value is conditional on paper-kappa + utility "
                        "hurdle + stable price; waiver and specific power are "
                        "coupled levers",
           "delay_sensitivity_pct_per_yr": round((math.exp(math.log(TIERS["paper"]) / DELAY) - 1) * 100, 1),
           "held": bool(h4)},
}

fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.6), sharey=True)
D, K = np.meshgrid(d_grid, decay_grid)
for ax, (tier, adv) in zip(axes, TIERS.items()):
    R = adv / (1 + ((1 + D) * (1 + K) - 1)) ** DELAY
    pc = ax.pcolormesh(D * 100, K * 100, R, cmap="RdBu", vmin=0.4, vmax=1.6,
                       shading="auto")
    ax.contour(D * 100, K * 100, R, levels=[1.0], colors="#26251f",
               linewidths=1.8)
    ax.axvline(8, color="#26251f", lw=0.8, ls=":")
    ax.axvline(10, color="#26251f", lw=0.8, ls=":")
    ax.set_title(f"{tier}: advantage {adv:.2f}x, d* = {d_star[tier]*100:.1f}%",
                 fontsize=10)
    ax.set_xlabel("discount rate [%]")
axes[0].set_ylabel("water-price decay [%/yr]")
axes[0].text(4.3, 0.4, "relay+waiver wins", fontsize=8.5)
axes[2].text(7.6, 5.5, "strict monolithic wins", fontsize=8.5, color="#fcfcfb")
fig.suptitle("NPV ratio: relay-with-waiver vs strict monolithic (black line = parity; dotted = campaign hurdles)",
             fontsize=11)
cb = fig.colorbar(pc, ax=axes, shrink=0.85)
cb.set_label("NPV per launched tonne, relay ÷ monolithic")
fig.savefig(RESULTS / "waiver_value.png", dpi=160, bbox_inches="tight")

with open(RESULTS / "findings.json", "w") as fh:
    json.dump({"findings": findings}, fh, indent=1, default=float)

for h in ("H1", "H2", "H3", "H4"):
    print(h, "HELD" if findings[h]["held"] else "FALSIFIED")
print("d*:", {t: f"{v*100:.1f}%" for t, v in d_star.items()})
print("paper@8%:", round(cells["paper"], 2), "| @10%:", round(r_10_0, 2),
      "| @8%+3%decay:", round(r_8_3, 2), "| flown@8%:", round(r_fl_8, 2))
