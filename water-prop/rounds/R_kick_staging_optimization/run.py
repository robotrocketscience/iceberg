#!/usr/bin/env python3
"""R-kick-staging-optimization — cross-sweep vs H1-H4. Deterministic."""
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
VE_K = 480.0 * G0
HW = 20_000.0 + 58.8e3 * 1.2 + 2_500.0
DV_TSI = 7300.0
PROP_MET_MAX = 684.0 * 300 / 83 * 1e9 * 0.6 / (0.5 * VE_MET ** 2)
CHUNK_T = 80.0
BASELINE = 50.0 / 40.0
R174_TOTAL = 483.0 - 366.0 + 366.0  # R174 best-corner launch (t) for ratio base


def kick_wet(payload, dv, n, eps):
    total = 0.0
    for _ in range(n):
        r = math.exp(dv / n / VE_K)
        w = (payload + total) * 0 + 0  # placeholder clarity
        break
    # stages burn outermost-first; build from the top down
    m = payload
    stages = []
    for _ in range(n):
        r = math.exp(dv / n / VE_K)
        w = m * (r - 1) / (1 - eps * r)
        if w <= 0 or not math.isfinite(w):
            return float("inf")
        stages.append(w)
        m += w
    return m - payload


results = []
for n in (1, 2, 3):
    for eps in (0.06, 0.08, 0.12):
        for dv_k in range(3500, 7301, 100):
            dv_m = DV_TSI - dv_k
            prop_met = HW * (math.exp(dv_m / VE_MET) - 1)
            if prop_met > PROP_MET_MAX:
                continue
            payload = HW + prop_met
            kw = kick_wet(payload, dv_k, n, eps)
            if not math.isfinite(kw):
                continue
            launch = (payload + kw) / 1000.0
            ratio = (launch / CHUNK_T) / BASELINE
            results.append({"n": n, "eps": eps, "dv_kick": dv_k,
                            "met_water_t": round(prop_met / 1000, 1),
                            "launch_t": round(launch, 0),
                            "outbound_frac": round((kw + prop_met) / (payload + kw), 2),
                            "ratio": round(ratio, 2)})

def pick(n, eps, dv):
    return next(r for r in results if r["n"] == n and r["eps"] == eps and r["dv_kick"] == dv)

# H1 at full-kick dv
s1 = {eps: pick(1, eps, 7300)["launch_t"] - HW / 1000 for eps in (0.06, 0.08, 0.12)}
s2 = {eps: pick(2, eps, 7300)["launch_t"] - HW / 1000 for eps in (0.06, 0.08, 0.12)}
s3 = {eps: pick(3, eps, 7300)["launch_t"] - HW / 1000 for eps in (0.06, 0.08, 0.12)}
save2 = {e: 1 - s2[e] / s1[e] for e in s1}
save3 = {e: 1 - s3[e] / s2[e] for e in s1}
h1 = all(0.47 <= v <= 0.55 for v in save2.values()) and all(0.15 <= v <= 0.20 for v in save3.values())

# H2: hybrid optimum at n=1, eps=0.08 (scripted case)
c1 = [r for r in results if r["n"] == 1 and r["eps"] == 0.08]
opt1 = min(c1, key=lambda r: r["launch_t"])
h2 = bool(3900 <= opt1["dv_kick"] <= 4300 and 44.0 <= opt1["met_water_t"] <= 48.2)

# H3: best combined corner
best = min(results, key=lambda r: r["launch_t"])
h3 = bool(best["launch_t"] <= 300.0 and 2.6 <= best["ratio"] <= 3.4)

# H4
h4 = bool(all(r["outbound_frac"] >= 0.55 for r in results)
          and best["outbound_frac"] < 0.81)

findings = {"H1": {"save_2stage": {str(k): round(v, 3) for k, v in save2.items()},
                   "save_3rd": {str(k): round(v, 3) for k, v in save3.items()}, "held": bool(h1)},
            "H2": {"opt_1stage": opt1, "held": h2},
            "H3": {"best": best, "held": h3},
            "H4": {"best_outbound_frac": best["outbound_frac"], "held": h4}}

fig, ax = plt.subplots(figsize=(9, 5.5))
for n, color in ((1, "#e34948"), (2, "#eda100"), (3, "#256abf")):
    pts = sorted([r for r in results if r["n"] == n and r["eps"] == 0.08],
                 key=lambda r: r["dv_kick"])
    ax.plot([r["dv_kick"] / 1000 for r in pts], [r["launch_t"] for r in pts],
            color=color, lw=1.8, label=f"{n}-stage kick (struct 0.08)")
ax.plot(best["dv_kick"] / 1000, best["launch_t"], "o", ms=11, mfc="none",
        mec="#26251f", mew=2.2)
ax.annotate(f"best: {best['n']}-stage, kick {best['dv_kick']/1000:.1f} km/s\n"
            f"{best['launch_t']:.0f} t, ratio {best['ratio']}x",
            (best["dv_kick"] / 1000, best["launch_t"]),
            textcoords="offset points", xytext=(10, 18), fontsize=9)
ax.set_xlabel("kick stage delta-v [km/s]  (lit thruster supplies the rest of 7.3)")
ax.set_ylabel("outbound launch mass [t]")
ax.set_title("Staging x hybrid split: the 81 percent line item, optimized")
ax.grid(True, alpha=0.25)
ax.legend(fontsize=9)
fig.tight_layout()
fig.savefig(RESULTS / "kick_optimization.png", dpi=160)

with open(RESULTS / "findings.json", "w") as fh:
    json.dump(findings, fh, indent=1, default=float)
for h in ("H1", "H2", "H3", "H4"):
    print(h, "HELD" if findings[h]["held"] else "FALSIFIED")
print("2-stage savings:", {k: round(v, 2) for k, v in save2.items()})
print("hybrid opt (1st,0.08):", opt1)
print("best combined:", best)
