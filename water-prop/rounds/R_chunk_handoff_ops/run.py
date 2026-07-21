#!/usr/bin/env python3
"""R-chunk-handoff-ops — decomposition sweep vs H1-H4. Deterministic."""
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

STAGES = {"rendezvous": (0.985, 0.99, 0.995), "proxops": (0.95, 0.97, 0.99),
          "berth_bag": (0.88, 0.92, 0.95), "mate": (0.95, 0.97, 0.99),
          "sep": (0.985, 0.99, 0.995)}
SWAP_BERTH = (0.92, 0.95, 0.97)
STEADY_LPD = 0.365
MONO_LPD = 1.02
DELAY = 10.4
HW_LPD = (0.8 + 0.4 + 0.2) * 5.84 / 160


def chain(idx, berth=None):
    p = 1.0
    for k, v in STAGES.items():
        p *= (berth[idx] if (berth and k == "berth_bag") else v[idx])
    return p


def retry(p_att, f_dmg, tries):
    b = (1 - p_att) * (1 - f_dmg)
    d = (1 - p_att) * f_dmg
    succ = sum(p_att * b ** k for k in range(tries))
    dmg = sum(d * b ** k for k in range(tries))
    return succ, dmg


rows = []
for idx, band in ((0, "low"), (1, "central"), (2, "high")):
    for f_dmg in (0.05, 0.10, 0.20):
        for tries in (1, 2, 3):
            p = chain(idx)
            s, d = retry(p, f_dmg, tries)
            s_sw, _ = retry(chain(idx, SWAP_BERTH), f_dmg, tries)
            for n in (2, 3, 4, 5):
                keep = s ** n * s_sw
                rows.append({"band": band, "f_dmg": f_dmg, "tries": tries,
                             "n": n, "p_att": round(p, 3),
                             "p_eventual": round(s, 3),
                             "dmg_per_handoff": round(d, 4),
                             "retention": round(keep, 3)})


def pick(band, f_dmg, tries, n):
    return next(r for r in rows if r["band"] == band and r["f_dmg"] == f_dmg
                and r["tries"] == tries and r["n"] == n)


c = pick("central", 0.10, 3, 4)
lo = pick("low", 0.10, 3, 4)
hi = pick("high", 0.10, 3, 4)

h1 = (0.77 <= c["p_att"] <= 0.92 and lo["p_att"] >= 0.75
      and 0.96 <= c["p_eventual"] <= 0.99
      and 0.008 <= c["dmg_per_handoff"] <= 0.029)
risk_lpd = STEADY_LPD / c["retention"]
h2 = 0.89 <= c["retention"] <= 0.93 and 0.39 <= risk_lpd <= 0.42
ops_lpd = risk_lpd + HW_LPD
h3 = 0.045 <= HW_LPD <= 0.060 and 0.44 <= ops_lpd <= 0.47
adv = MONO_LPD / ops_lpd
d_star = math.exp(math.log(adv) / DELAY) - 1
h4 = (min(r["retention"] for r in rows if r["tries"] == 3) > 0.85
      and 0.080 <= d_star <= 0.085)

findings = {
    "H1": {"central": {k: c[k] for k in ("p_att", "p_eventual", "dmg_per_handoff")},
           "low_high_p_att": [lo["p_att"], hi["p_att"]], "held": bool(h1)},
    "H2": {"retention_n4": c["retention"], "risk_lpd": round(risk_lpd, 3),
           "held": bool(h2)},
    "H3": {"hw_lpd": round(HW_LPD, 3), "ops_honest_lpd": round(ops_lpd, 3),
           "held": bool(h3)},
    "H4": {"capture_band_bet1": [0.46, 0.85],
           "min_retention_any_cell": min(r["retention"] for r in rows
                                         if r["tries"] == 3),
           "composed_advantage": round(adv, 2),
           "d_star_pct": round(d_star * 100, 1),
           "knife_edge": "third consecutive honesty pass lands at the 8% utility hurdle",
           "held": bool(h4)},
}

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 5.0))
for tries, color in ((1, "#e34948"), (2, "#eda100"), (3, "#256abf")):
    ns = [2, 3, 4, 5]
    ks = [pick("central", 0.10, tries, n)["retention"] for n in ns]
    ax1.plot(ns, ks, "o-", color=color, lw=1.8, label=f"{tries} attempt(s)")
band_lo = [pick("low", 0.10, 3, n)["retention"] for n in (2, 3, 4, 5)]
band_hi = [pick("high", 0.10, 3, n)["retention"] for n in (2, 3, 4, 5)]
ax1.fill_between([2, 3, 4, 5], band_lo, band_hi, color="#256abf", alpha=0.15,
                 label="desk-anchor band (3 attempts)")
ax1.axhspan(0.46, 0.85, color="#cbd2dc", alpha=0.5, zorder=0)
ax1.text(2.1, 0.62, "bet #1 capture-efficiency band\n(the binding bottleneck)",
         fontsize=8.5, color="#5a6378")
ax1.set_xticks([2, 3, 4, 5])
ax1.set_xlabel("chunk handoffs per mission N")
ax1.set_ylabel("mission water-throughput retention")
ax1.set_ylim(0.4, 1.02)
ax1.set_title("Handoff risk vs the bottleneck that already exists")
ax1.grid(True, alpha=0.25)
ax1.legend(fontsize=8.5, loc="lower left")

ladder = [("R184 fleet\nsteady state", STEADY_LPD, "#cbd2dc"),
          ("+ handoff risk\n(retention 0.91)", risk_lpd, "#eda100"),
          ("+ hardware\n(ops-honest)", ops_lpd, "#e34948")]
x = np.arange(len(ladder))
bars = ax2.bar(x, [v for _, v, _ in ladder], color=[c_ for _, _, c_ in ladder],
               width=0.55)
for b, (_, v, _) in zip(bars, ladder):
    ax2.text(b.get_x() + b.get_width() / 2, v + 0.006, f"{v:.3f}", ha="center",
             fontsize=9)
ax2.axhline(0.456, color="#26251f", lw=1.2, ls="--")
ax2.text(0.35, 0.462, "single-mission lifetime-capped (0.456)", fontsize=8.5)
ax2.set_xticks(x, [n for n, _, _ in ladder], fontsize=8.5)
ax2.set_ylabel("launch mass per delivered tonne [t/t]")
ax2.set_ylim(0.3, 0.52)
ax2.set_title(f"Ops honesty consumes the fleet gain: d* back to {d_star*100:.1f}%")
ax2.grid(True, axis="y", alpha=0.25)
fig.tight_layout()
fig.savefig(RESULTS / "handoff_ops.png", dpi=160)

with open(RESULTS / "findings.json", "w") as fh:
    json.dump({"findings": findings, "sweep": rows}, fh, indent=1, default=float)

for h in ("H1", "H2", "H3", "H4"):
    print(h, "HELD" if findings[h]["held"] else "FALSIFIED")
print("central:", c, "| risk lpd:", round(risk_lpd, 3), "| ops:", round(ops_lpd, 3),
      "| d*:", round(d_star * 100, 2), "%")
