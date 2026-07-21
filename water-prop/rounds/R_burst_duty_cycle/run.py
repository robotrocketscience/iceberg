#!/usr/bin/env python3
"""R-burst-duty-cycle — envelope map + task adjudication vs H1-H4.

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

LHV = 13.3e6
ETA_FC = 0.55
ETA_CHG = 0.66
ETA_RT = ETA_FC * ETA_CHG
FC_KG_PER_KWE = 10.0
TANK = 0.20
BATT_KG_PER_KWEH = 3.6e6 / (250 * 3600.0) / 0.80
GAS_KG_PER_KWEH = 3.6e6 / ETA_FC / LHV * (1 + TANK)
DAY = 86400.0
HOUR = 3600.0

P_RE_GRID = [0.8, 2.2, 10.0, 30.0, 100.0]
P_B_GRID = np.array([5, 10, 15, 25, 50, 100, 200], dtype=float)
T_B_GRID_H = np.array([0.1, 0.5, 1, 2.27, 6, 16.9, 24, 72, 168], dtype=float)


def cadence_days(pb, tb_h, p_re):
    return pb * tb_h / (p_re * ETA_RT) / 24.0


rows = []
for p_re in P_RE_GRID:
    for pb in P_B_GRID:
        for tb in T_B_GRID_H:
            rows.append({"p_re_kwe": p_re, "p_b_kwe": float(pb),
                         "t_b_h": float(tb),
                         "cadence_d": round(cadence_days(pb, tb, p_re), 1),
                         "duty_frac": round(p_re * ETA_RT / pb, 4)})

# H1
h1_law = ETA_RT
c100_22 = cadence_days(100, 24, 2.2)
c100_08 = cadence_days(100, 24, 0.8)
h1 = 0.34 <= h1_law <= 0.39 and 115 <= c100_22 <= 135 and 320 <= c100_08 <= 370

# H2
t_batt = FC_KG_PER_KWE / (BATT_KG_PER_KWEH - GAS_KG_PER_KWEH)
t_inv = FC_KG_PER_KWE / GAS_KG_PER_KWEH
h2 = 2.0 <= t_batt <= 2.6 and 15.0 <= t_inv <= 20.0

# H3
c50_22 = cadence_days(50, 24, 2.2)
c100x3_22 = cadence_days(100, 72, 2.2)
p_weekly = 50 * 24 / 7 / 24 / ETA_RT
h3 = c50_22 >= 60 and c100x3_22 >= 360 and 15.0 <= p_weekly <= 25.0

# H4
duty_demo_h = ETA_RT * 100.0 / 100.0 * 24.0
oneshot_d = 10_000.0 * LHV * ETA_FC / 100e3 / DAY
h4 = duty_demo_h >= 6.0

findings = {
    "H1": {"eta_rt": round(h1_law, 3), "cadence_100kWe_1d_at_2.2": round(c100_22, 0),
           "at_0.8": round(c100_08, 0), "held": bool(h1)},
    "H2": {"battery_bank_crossover_h": round(t_batt, 2),
           "plant_inventory_crossover_h": round(t_inv, 1), "held": bool(h2)},
    "H3": {"cadence_50kWe_1d_at_2.2": round(c50_22, 0),
           "cadence_100kWe_3d_at_2.2": round(c100x3_22, 0),
           "recharge_for_weekly_50kWed_kwe": round(p_weekly, 1),
           "held": bool(h3)},
    "H4": {"demo_100kWe_h_per_day": round(duty_demo_h, 1),
           "oneshot_100kWe_days_per_10t": round(oneshot_d, 1), "held": bool(h4)},
}

# --- figure ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 5.2))
pb = np.logspace(math.log10(5), math.log10(200), 120)
tb = np.logspace(math.log10(0.1), math.log10(200), 120)
PB, TB = np.meshgrid(pb, tb)
for p_re, color in ((2.2, "#256abf"), (10.0, "#eda100"), (30.0, "#e34948")):
    C = PB * TB / (p_re * ETA_RT) / 24.0
    cs = ax1.contour(PB, TB, C, levels=[7, 30, 90, 365], colors=color,
                     linewidths=1.3, alpha=0.85)
    ax1.clabel(cs, fmt=lambda v: f"{v:.0f} d", fontsize=7)
ax1.plot([50, 100], [24, 72], "s", ms=8, mfc="none", mec="#26251f", mew=1.8)
ax1.annotate("R172 burst class", (52, 20), fontsize=8.5)
ax1.set_xscale("log")
ax1.set_yscale("log")
ax1.set_xlabel("burst power [kWe]")
ax1.set_ylabel("burst duration [h]")
ax1.set_title("Sustainable cadence contours (blue 2.2 / amber 10 / red 30 kWe recharge)")
ax1.grid(True, which="both", alpha=0.2)

t = np.logspace(math.log10(0.1), math.log10(200), 200)
m_batt = BATT_KG_PER_KWEH * t
m_bank = FC_KG_PER_KWE + GAS_KG_PER_KWEH * t
ax2.plot(t, m_batt, color="#eda100", lw=1.8, label="battery (250 Wh/kg, 80% DoD)")
ax2.plot(t, m_bank, color="#256abf", lw=1.8, label="H2/O2 bank (plant + cycled gas)")
ax2.axvline(t_batt, color="#26251f", lw=1, ls=":")
ax2.text(t_batt * 1.1, 300, f"crossover {t_batt:.1f} h", fontsize=8.5, rotation=90,
         va="center")
ax2.axvline(t_inv, color="#5a6378", lw=1, ls=":")
ax2.text(t_inv * 1.1, 300, f"plant/inventory {t_inv:.0f} h", fontsize=8.5,
         rotation=90, va="center", color="#5a6378")
ax2.set_xscale("log")
ax2.set_yscale("log")
ax2.set_xlabel("burst duration [h]")
ax2.set_ylabel("storage mass per kWe of burst [kg]")
ax2.set_title("Who carries the burst: the bank's niche is 2 h to multi-day")
ax2.grid(True, which="both", alpha=0.25)
ax2.legend(fontsize=8.5)
fig.tight_layout()
fig.savefig(RESULTS / "burst_duty_envelope.png", dpi=160)

with open(RESULTS / "findings.json", "w") as fh:
    json.dump({"findings": findings, "grid": rows}, fh, indent=1, default=float)

for h in ("H1", "H2", "H3", "H4"):
    print(h, "HELD" if findings[h]["held"] else "FALSIFIED")
print(findings)
