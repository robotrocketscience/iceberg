#!/usr/bin/env python3
"""R-clearing-price-time-path — full sweep vs H1-H4. Deterministic.
Externally anchored (see SCOPE). Grids span scope_bounds.py."""
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

LAUNCH_2025 = 3868.0
LAUNCH_2040_MED = 273.0
DISCOUNT = 0.25
P_LEO_LO, P_LEO_HI, P_LEO_C = 3000.0, 4000.0, 3500.0
YRS = 15.0
R183_KILL = 0.03
VE_CHEM = 450.0 * 9.80665
HURDLES = {"8% utility": 0.08, "10% growth": 0.10}
T_RT, T_FULL = 13.0, 23.5

# --- H1 ---
p_leo_isru = LAUNCH_2025 * (1.0 - DISCOUNT)
h1 = (P_LEO_LO <= P_LEO_C <= P_LEO_HI
      and P_LEO_LO * 0.9 <= p_leo_isru <= P_LEO_HI)

# --- H2 ---
rate_cons = -math.log(0.25) / YRS
rate_med = math.log(LAUNCH_2025 / LAUNCH_2040_MED) / YRS
rate_bull = math.log(LAUNCH_2025 / 30.0) / YRS
rate_central = math.sqrt(rate_cons * rate_med)
ratio_lo, ratio_hi = rate_cons / R183_KILL, rate_med / R183_KILL
h2 = (0.09 <= rate_cons <= 0.10 and 0.17 <= rate_med <= 0.18
      and 0.12 <= rate_central <= 0.14 and 3.0 <= ratio_lo
      and ratio_hi <= 6.0 and rate_central > 0.06)

# --- H3 ---
def fall(r, T):
    return math.exp(r * T)


deliv_frac = {}
for T, ttag in ((T_RT, "rt13"), (T_FULL, "full235")):
    for r, rtag in ((rate_cons, "cons"), (rate_central, "central"),
                    (rate_med, "median")):
        deliv_frac[f"{ttag}_{rtag}"] = round(1.0 / fall(r, T) * 100.0, 1)
eff = {}
for htag, h in HURDLES.items():
    e = h + rate_central
    eff[htag] = {"rate_pct": round(e * 100, 1),
                 "df_235_pct": round(math.exp(-e * T_FULL) * 100, 2)}
h3 = (5.0 <= deliv_frac["full235_central"] <= 19.0
      and all(v["df_235_pct"] < 2.0 for v in eff.values())
      and rate_central > max(HURDLES.values()))

# --- H4 ---
deep = {}
for dv in (10e3, 15e3, 20e3):
    mult = math.exp(dv / VE_CHEM)
    deep[f"{dv/1e3:.0f}km_s"] = {"mult": round(mult, 1),
                                 "price_k$_kg": round(P_LEO_C * mult / 1000)}
h4 = (9.0 <= deep["10km_s"]["mult"] <= 11.0
      and 28.0 <= deep["15km_s"]["mult"] <= 32.0
      and 85.0 <= deep["20km_s"]["mult"] <= 100.0)

findings = {
    "H1": {"p_leo_band_$_kg": [P_LEO_LO, P_LEO_HI], "central": P_LEO_C,
           "isru_crosscheck_$_kg": round(p_leo_isru), "held": bool(h1)},
    "H2": {"rate_cons_pct": round(rate_cons * 100, 1),
           "rate_central_pct": round(rate_central * 100, 1),
           "rate_median_pct": round(rate_med * 100, 1),
           "rate_bull_pct": round(rate_bull * 100, 1),
           "r183_kill_pct": R183_KILL * 100,
           "ratio_vs_kill": [round(ratio_lo, 1), round(ratio_hi, 1)],
           "held": bool(h2)},
    "H3": {"delivery_price_pct_of_decision": deliv_frac,
           "combined_effective": eff,
           "decline_exceeds_both_hurdles": rate_central > max(HURDLES.values()),
           "held": bool(h3)},
    "H4": {"deep_space_substitute": deep,
           "dilemma": "cheap (LEO, racing substitute) vs dear (deep space, "
                      "no customers)", "held": bool(h4)},
}

# --- figure ---
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15.5, 4.8))
yrs = np.linspace(0, T_FULL, 200)
for r, c, lab in ((rate_cons, "#256abf", f"conservative {rate_cons*100:.0f}%/yr"),
                  (rate_central, "#eda100", f"central {rate_central*100:.0f}%/yr"),
                  (rate_med, "#e34948", f"median {rate_med*100:.0f}%/yr")):
    ax1.plot(yrs, P_LEO_C * np.exp(-r * yrs), color=c, lw=2, label=lab)
ax1.plot(yrs, P_LEO_C * np.exp(-R183_KILL * yrs), color="#5a6378", lw=1.6,
         ls=":", label=f"R183 hand-set {R183_KILL*100:.0f}%/yr")
ax1.axvline(T_RT, color="#cbd2dc", lw=1.1)
ax1.text(T_RT + 0.2, 1900, "round\ntrip 13 yr", fontsize=7.5, color="#5a6378")
ax1.axvline(T_FULL, color="#cbd2dc", lw=1.1)
ax1.text(T_FULL - 4.5, 1900, "full timeline\n23.5 yr", fontsize=7.5,
         color="#5a6378")
ax1.set_xlabel("years from decision")
ax1.set_ylabel("LEO water clearing price [$/kg]")
ax1.set_title("The substitute races away: launch experience curve")
ax1.set_ylim(0, 3700)
ax1.grid(True, alpha=0.25)
ax1.legend(fontsize=8, loc="upper right")

rates = np.linspace(0.03, 0.20, 200)
for T, c, lab in ((T_RT, "#256abf", "13 yr (round trip)"),
                  (T_FULL, "#e34948", "23.5 yr (full timeline)")):
    ax2.plot(rates * 100, 100.0 / np.exp(rates * T), color=c, lw=2, label=lab)
ax2.axvspan(rate_cons * 100, rate_med * 100, color="#eda100", alpha=0.18,
            label="empirical band")
ax2.axvline(R183_KILL * 100, color="#5a6378", lw=1.4, ls=":")
ax2.text(R183_KILL * 100 + 0.2, 70, "R183 kill\n3%/yr", fontsize=8,
         color="#5a6378")
ax2.set_xlabel("annual price-decline rate [%/yr]")
ax2.set_ylabel("delivery price [% of decision-time]")
ax2.set_title("Empirical decline is 3–6× R183's kill threshold")
ax2.set_ylim(0, 100)
ax2.grid(True, alpha=0.25)
ax2.legend(fontsize=8, loc="upper right")

labels = ["LEO\n(now)", "LEO\ndelivery\n(23.5yr)", "deep space\n10 km/s",
          "deep space\n15 km/s", "deep space\n20 km/s"]
vals = [P_LEO_C / 1000,
        P_LEO_C / 1000 / fall(rate_central, T_FULL),
        deep["10km_s"]["price_k$_kg"], deep["15km_s"]["price_k$_kg"],
        deep["20km_s"]["price_k$_kg"]]
colors = ["#256abf", "#e34948", "#7a9a3a", "#7a9a3a", "#7a9a3a"]
x = np.arange(len(labels))
ax3.bar(x, vals, color=colors, width=0.6)
for xi, v in zip(x, vals):
    ax3.text(xi, v * 1.25 if v > 1 else v + 3, f"{v:.1f}" if v < 10 else
             f"{v:.0f}", ha="center", fontsize=8.5)
ax3.set_yscale("log")
ax3.set_xticks(x, labels, fontsize=7.5)
ax3.set_ylabel("clearing price [k$/kg, log]")
ax3.set_title("The dilemma: cheap-racing vs dear-no-market")
ax3.set_ylim(0.05, 1000)
ax3.grid(True, axis="y", alpha=0.25)
fig.tight_layout()
fig.savefig(RESULTS / "clearing_price.png", dpi=160)

with open(RESULTS / "findings.json", "w") as fh:
    json.dump({"findings": findings}, fh, indent=1, default=float)

for h in ("H1", "H2", "H3", "H4"):
    print(h, "HELD" if findings[h]["held"] else "FALSIFIED")
print(f"central decline {rate_central*100:.1f}%/yr = {ratio_lo:.1f}-{ratio_hi:.1f}x "
      f"R183 kill | delivery price @23.5yr central = "
      f"{deliv_frac['full235_central']}% | eff df @8% = "
      f"{eff['8% utility']['df_235_pct']}%")
