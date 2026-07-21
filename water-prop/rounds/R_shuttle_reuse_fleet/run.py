#!/usr/bin/env python3
"""R-shuttle-reuse-fleet — lifetime-honest fleet economics vs H1-H4."""
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
KICK = 5.84
CHUNK = 40_000.0
R_WELL = math.exp(6700.0 / VE) - 1
RES_WAIVER = 12.9
MONO_LPD = 1.02
DELAY = 10.4


def sortie_fpy(m_shuttle, p_kwe):
    prop = (m_shuttle + CHUNK) * R_WELL + m_shuttle * R_WELL
    return 0.5 * VE ** 2 * prop / ETA / (p_kwe * 1e3) / YEAR


def cell(kappa, p_s, life):
    m_sh = 2500.0 + kappa * p_s
    t_s = sortie_fpy(m_sh, p_s)
    n = min(int(life // t_s), int((RES_WAIVER - 1.0) // t_s))
    if n < 1:
        return None
    first = (4000.0 + m_sh) * KICK / 1000
    # swap mission: mothership bus + fresh reactor module (registered model)
    swap = (4000.0 + kappa * p_s) * KICK / 1000
    pooled_reactors = n * t_s / life
    pooled = (4000.0 + pooled_reactors * kappa * p_s) * KICK / 1000
    return {"n": n, "t_sortie": round(t_s, 2), "fpy": round(n * t_s, 1),
            "first_lpd": round(first / (n * 40), 3),
            "swap_lpd": round(swap / (n * 40), 3),
            "pooled_lpd": round(pooled / (n * 40), 3)}


# H1: R182 adjudication
c_paper = cell(100.0, 60.0, 10.0)
c_flown = cell(417.0, 50.0, 10.0)
fpy_182_paper = 5 * sortie_fpy(2500.0 + 6000.0, 60.0)
fpy_182_flown = 3 * sortie_fpy(2500.0 + 417.0 * 50.0, 50.0)
h1 = (fpy_182_paper > 10.0 and fpy_182_flown > 10.0 and c_paper["n"] == 4
      and 0.44 <= c_paper["first_lpd"] <= 0.48 and c_flown["n"] == 2
      and 1.9 <= c_flown["first_lpd"] <= 2.1)

# H2: discrete steady state at paper/60
h2_steady = c_paper["swap_lpd"]
reactor_share = 6000.0 * KICK / 1000 / (c_paper["swap_lpd"] * c_paper["n"] * 40)
fleet_k3 = (c_paper["first_lpd"] + 2 * c_paper["swap_lpd"]) / 3
h2 = (0.35 <= h2_steady <= 0.38 and 0.55 <= reactor_share <= 0.65
      and 0.38 <= fleet_k3 <= 0.41)

# H3: life sensitivity (pooled)
life_curve = {}
for L in (10.0, 15.0, 20.0, 40.0):
    m_sh = 2500.0 + 6000.0
    t_s = sortie_fpy(m_sh, 60.0)
    reactors_per_mission = 4.0 * t_s / L
    life_curve[L] = round((4000.0 + reactors_per_mission * 6000.0) * KICK
                          / 1000 / 160, 3)
h3 = (0.32 <= life_curve[10.0] <= 0.34 and 0.26 <= life_curve[15.0] <= 0.28
      and 0.23 <= life_curve[20.0] <= 0.25 and life_curve[40.0] > 0.146)

# H4: NPV restoration
adv = MONO_LPD / h2_steady
d_star = math.exp(math.log(adv) / DELAY) - 1
h4 = 2.7 <= adv <= 2.9 and 0.102 <= d_star <= 0.106

findings = {
    "H1": {"r182_fpy": {"paper": round(fpy_182_paper, 1),
                        "flown": round(fpy_182_flown, 1)},
           "capped_paper": c_paper, "capped_flown": c_flown, "held": bool(h1)},
    "H2": {"steady_lpd": h2_steady, "reactor_share": round(reactor_share, 2),
           "fleet_avg_k3": round(fleet_k3, 3),
           "naive_dream_lpd": round(4000.0 * KICK / 1000 / 160, 3),
           "held": bool(h2)},
    "H3": {"pooled_lpd_by_life": {str(k): v for k, v in life_curve.items()},
           "dream_requires_fpy": ">=40", "held": bool(h3)},
    "H4": {"steady_advantage": round(adv, 2), "d_star_pct": round(d_star * 100, 1),
           "held": bool(h4)},
}

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 5.0))
Ls = np.linspace(8, 45, 150)
t_s = sortie_fpy(8500.0, 60.0)
pooled = [(4000.0 + 4.0 * t_s / L * 6000.0) * KICK / 1000 / 160 for L in Ls]
ax1.plot(Ls, pooled, color="#256abf", lw=1.9, label="pooled steady-state lpd")
ax1.axhline(4000.0 * KICK / 1000 / 160, color="#eda100", lw=1.4, ls="--",
            label="reactor-immortal dream (0.146)")
ax1.axhline(MONO_LPD, color="#26251f", lw=1.4, ls=":",
            label="strict monolithic (1.02)")
ax1.axvspan(8, 10, color="#e34948", alpha=0.15)
ax1.text(8.3, 0.62, "design-life\ntarget region\n(unmeasured)", fontsize=8,
         color="#b53332")
ax1.set_xlabel("reactor design life [full-power-years]")
ax1.set_ylabel("launch mass per delivered tonne [t/t]")
ax1.set_ylim(0, 1.1)
ax1.set_title("The reactor is the propellant: fleet economics vs life")
ax1.grid(True, alpha=0.25)
ax1.legend(fontsize=8.5)

ladder = [("R182 claim\n(N=5, no life cap)", 0.36, "#cbd2dc"),
          ("lifetime-capped\nsingle mission (N=4)", c_paper["first_lpd"], "#e34948"),
          ("fleet swap\nsteady state", h2_steady, "#eda100"),
          ("pooled life\nL=10 fpy", life_curve[10.0], "#256abf"),
          ("dream\n(immortal reactor)", 0.146, "#5a6378")]
x = np.arange(len(ladder))
bars = ax2.bar(x, [v for _, v, _ in ladder], color=[c for _, _, c in ladder],
               width=0.6)
for b, (_, v, _) in zip(bars, ladder):
    ax2.text(b.get_x() + b.get_width() / 2, v + 0.008, f"{v:.2f}", ha="center",
             fontsize=9)
ax2.set_xticks(x, [n for n, _, _ in ladder], fontsize=8)
ax2.set_ylabel("launch mass per delivered tonne [t/t]")
ax2.set_title("The honest ladder (paper-κ, 60 kWe shuttle)")
ax2.grid(True, axis="y", alpha=0.25)
fig.tight_layout()
fig.savefig(RESULTS / "fleet_reuse.png", dpi=160)

with open(RESULTS / "findings.json", "w") as fh:
    json.dump({"findings": findings}, fh, indent=1, default=float)

for h in ("H1", "H2", "H3", "H4"):
    print(h, "HELD" if findings[h]["held"] else "FALSIFIED")
print("capped:", c_paper, "|", c_flown)
print("steady:", h2_steady, "| share:", round(reactor_share, 2),
      "| life curve:", life_curve, "| d*:", round(d_star * 100, 1), "%")
