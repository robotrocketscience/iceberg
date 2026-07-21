#!/usr/bin/env python3
"""R-chunk-relay-staging — relay vs monolithic sweep vs H1-H4.

Closed form, deterministic.
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
VE = 800.0 * G0
ETA = 0.6
YEAR = 3.156e7
DV_WELL = 6700.0
KICK = 5.84
CHUNK = 40_000.0
BUS_BAG = 4_000.0
M_SHIP_BUS = 4_000.0
SHUTTLE_BUS_BAG = 2_500.0
P_MONO = 30.0
T_TOUR = 1.0
RES_STRICT = 15.0 - 12.1
RES_WAIVER = 25.0 - 12.1
R_WELL = math.exp(DV_WELL / VE) - 1


def sortie(m_shuttle, p_kwe):
    prop = (m_shuttle + CHUNK) * R_WELL + m_shuttle * R_WELL
    e = 0.5 * VE ** 2 * prop / ETA
    return prop, e / (p_kwe * 1e3) / YEAR


def relay(kappa, p_s, n):
    m_sh = SHUTTLE_BUS_BAG + kappa * p_s
    water, t_s = sortie(m_sh, p_s)
    launch = (M_SHIP_BUS + m_sh) * KICK / 1000.0
    res = T_TOUR + n * t_s
    return {"launch_t": round(launch, 1), "lpd": round(launch / (n * CHUNK / 1000), 2),
            "water_t": round(water / 1000, 1), "t_sortie": round(t_s, 2),
            "residence": round(res, 1), "strict": res <= RES_STRICT,
            "waiver": res <= RES_WAIVER}


def monolithic(kappa):
    dry = BUS_BAG + kappa * P_MONO
    prop = (dry + CHUNK) * (math.exp(9000.0 / VE) - 1)
    return {"launch_t": round(dry * KICK / 1000.0, 1),
            "lpd": round(dry * KICK / 1000.0 / (CHUNK / 1000), 2),
            "water_t": round(prop / 1000, 1)}


MONO = {100.0: monolithic(100.0), 417.0: monolithic(417.0)}
rows = []
for kappa in (100.0, 417.0):
    for p_s in range(20, 251, 10):
        for n in range(1, 6):
            r = relay(kappa, float(p_s), n)
            r.update({"kappa": kappa, "p_s": p_s, "n": n})
            rows.append(r)

# H1: N=1 strictly loses everywhere
h1_margin = min(r["lpd"] / MONO[r["kappa"]]["lpd"] for r in rows if r["n"] == 1)
h1 = h1_margin >= 1.10

# H2: waiver-legal optima per tier; optimum at min feasible power
best = {}
for kappa in (100.0, 417.0):
    legal = [r for r in rows if r["kappa"] == kappa and r["waiver"] and r["n"] >= 2]
    b = min(legal, key=lambda r: r["lpd"])
    pmin_feasible = min(r["p_s"] for r in legal if r["n"] == b["n"])
    best[kappa] = {"cell": b, "edge_vs_mono": round(1 - b["lpd"] / MONO[kappa]["lpd"], 2),
                   "at_min_power": b["p_s"] == pmin_feasible}
h2 = (0.42 <= best[100.0]["cell"]["lpd"] <= 0.50
      and 1.30 <= best[417.0]["cell"]["lpd"] <= 1.50
      and best[100.0]["at_min_power"] and best[417.0]["at_min_power"])

# H3: bisect strict-N=2 power frontier (paper kappa), test if it beats mono
lo, hi = 20.0, 2000.0
for _ in range(60):
    mid = 0.5 * (lo + hi)
    _, t_s = sortie(SHUTTLE_BUS_BAG + 100.0 * mid, mid)
    if T_TOUR + 2 * t_s <= RES_STRICT:
        hi = mid
    else:
        lo = mid
p_frontier = hi
strict_cells = [r for r in rows if r["strict"] and r["n"] >= 2
                and r["lpd"] < MONO[r["kappa"]]["lpd"]]
lpd_frontier = relay(100.0, p_frontier, 2)["lpd"]
h3 = len(strict_cells) == 0 and lpd_frontier > MONO[100.0]["lpd"]

# H4: harvest ledger at winning cells
harv_relay = (best[100.0]["cell"]["water_t"] + 40) / 40
harv_mono = (MONO[100.0]["water_t"] + 40) / 40
worst_harv = max((r["water_t"] + 40) / 40 for r in rows if r["kappa"] == 417.0)
h4 = harv_relay < harv_mono

findings = {
    "H1": {"worst_n1_lpd_ratio_vs_mono": round(h1_margin, 2), "held": bool(h1)},
    "H2": {"best_paper": best[100.0], "best_flown": best[417.0],
           "mono_lpd": {str(k): v["lpd"] for k, v in MONO.items()},
           "held": bool(h2)},
    "H3": {"strict_n2_power_frontier_kwe": round(p_frontier, 0),
           "lpd_at_frontier": lpd_frontier,
           "strict_cells_beating_mono": len(strict_cells), "held": bool(h3)},
    "H4": {"harvest_ratio_relay_win_cell": round(harv_relay, 1),
           "harvest_ratio_mono": round(harv_mono, 1),
           "worst_flown_harvest_ratio": round(worst_harv, 1),
           "mothership_ring_crossings": 0, "monolithic_ring_crossings": 2,
           "held": bool(h4)},
}

# --- figure ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 5.2))
for p_s, color in ((30, "#256abf"), (60, "#eda100"), (117, "#e34948"),
                   (190, "#5a6378")):
    pts = sorted([r for r in rows if r["kappa"] == 100.0 and r["p_s"] == p_s],
                 key=lambda r: r["n"])
    ns = [r["n"] for r in pts]
    lp = [r["lpd"] for r in pts]
    ok = [r["waiver"] for r in pts]
    ax1.plot(ns, lp, "-", color=color, lw=1.6, label=f"{p_s} kWe shuttle")
    ax1.plot([n for n, o in zip(ns, ok) if o], [l for l, o in zip(lp, ok) if o],
             "o", color=color, ms=7)
    ax1.plot([n for n, o in zip(ns, ok) if not o],
             [l for l, o in zip(lp, ok) if not o], "x", color=color, ms=8,
             mew=2)
ax1.axhline(MONO[100.0]["lpd"], color="#26251f", lw=1.4, ls="--")
ax1.text(3.0, MONO[100.0]["lpd"] + 0.06, "monolithic (one mission per chunk)",
         fontsize=8.5)
ax1.set_xticks([1, 2, 3, 4, 5])
ax1.set_xlabel("chunks per mission N")
ax1.set_ylabel("launch mass per delivered tonne ÷ 1 [t/t]")
ax1.set_title("Relay vs monolithic, paper-κ (dots: waiver-legal; x: schedule bust)")
ax1.grid(True, alpha=0.25)
ax1.legend(fontsize=8.5)

ps = np.arange(20, 251, 5, dtype=float)
for n, color in ((2, "#256abf"), (3, "#eda100"), (4, "#e34948")):
    res = [T_TOUR + n * sortie(SHUTTLE_BUS_BAG + 100.0 * p, p)[1] for p in ps]
    ax2.plot(ps, res, color=color, lw=1.7, label=f"N={n}")
ax2.axhline(RES_STRICT, color="#26251f", lw=1.3, ls="--")
ax2.text(150, RES_STRICT + 0.25, "strict L0-05 residence budget (2.9 yr)",
         fontsize=8.5)
ax2.axhline(RES_WAIVER, color="#5a6378", lw=1.3, ls=":")
ax2.text(150, RES_WAIVER + 0.25, "25-yr waiver budget (12.9 yr)", fontsize=8.5,
         color="#5a6378")
ax2.set_xlabel("shuttle power [kWe] (paper-κ; reactor mass grows with power)")
ax2.set_ylabel("Saturn residence [yr] (tour + N sorties)")
ax2.set_title("The schedule wall: multi-chunk lives only under the waiver")
ax2.set_ylim(0, 22)
ax2.grid(True, alpha=0.25)
ax2.legend(fontsize=8.5)
fig.tight_layout()
fig.savefig(RESULTS / "relay_staging.png", dpi=160)

with open(RESULTS / "findings.json", "w") as fh:
    json.dump({"findings": findings, "sweep": rows}, fh, indent=1, default=float)

for h in ("H1", "H2", "H3", "H4"):
    print(h, "HELD" if findings[h]["held"] else "FALSIFIED")
print("best paper:", best[100.0], "| best flown:", best[417.0])
print("strict N=2 frontier:", round(p_frontier), "kWe, lpd there:", lpd_frontier)
print("harvest: relay-win", round(harv_relay, 1), "x vs mono", round(harv_mono, 1), "x")
