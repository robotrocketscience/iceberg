#!/usr/bin/env python3
"""R-bag-dynamics-envelope — full sweep vs H1-H4. Deterministic.
Lumped-parameter desk envelope; coupled stability -> Basilisk follow-on.
Grids span scope_bounds.py."""
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

M_WATER = 40_000.0
RHO = 1000.0
V = M_WATER / RHO
R_BAG = (3.0 * V / (4.0 * math.pi)) ** (1.0 / 3.0)
V_C = (0.01, 0.05, 0.10)
K_C = (1e3, 1e4, 1e5)
F_S_FRAC = 0.5
ACS_BW = (0.01, 0.10)
RW_AUTH, THR_AUTH = 5.0, 50.0
BERTH_WINDOW = 30.0 * 60.0
MS_DRY = {"relay_bus": 4_000.0, "monolithic": 20_000.0}
R_OFF = 2.0
X_S = 0.10
m_s = F_S_FRAC * M_WATER

# --- H1 ---
contact = {}
for v_c in V_C:
    for k_c in K_C:
        contact[f"{v_c}_{k_c:.0e}"] = round(v_c * math.sqrt(k_c * M_WATER) / 1e3, 2)
soft = max(contact[f"{v}_{k:.0e}"] for v in (0.01, 0.05) for k in (1e3, 1e4))
# registered falsification (SCOPE H1): any soft-capture corner > 10 kN.
# Descriptive envelope max is 6.32 kN (SCOPE rounded to 6.3 — rounding
# blemish noted in STUDY bug-catch; corrections live forward).
h1 = soft <= 1.0 and max(contact.values()) <= 10.0

# --- H2 ---
ts_grid = np.linspace(10, 300, 100)
f_grid = 1.0 / ts_grid
overlap_ts = [t for t in ts_grid if ACS_BW[0] <= 1.0 / t <= ACS_BW[1]]
h2 = len(overlap_ts) > 0 and max(overlap_ts) >= 90

# --- H3 ---
ratios = {k: round(M_WATER / v, 1) for k, v in MS_DRY.items()}
torque = {t: m_s * X_S * (2 * math.pi / t) ** 2 * R_OFF for t in (10, 100, 300)}
h3 = (min(ratios.values()) >= 2 and torque[100] > RW_AUTH
      and torque[10] > THR_AUTH and 1.5 <= torque[300] <= 2.5)

# --- H4: viable-corner fraction ---
gts = np.linspace(10, 300, 60)
gz = np.linspace(0.01, 0.10, 40)
rw_ok = thr_ok = tot = 0
heat = np.zeros((len(gz), len(gts)))
for i, t_s in enumerate(gts):
    w = 2 * math.pi / t_s
    tq = m_s * X_S * w ** 2 * R_OFF
    for j, zeta in enumerate(gz):
        t_set = 4.0 / (zeta * w)
        tot += 1
        code = 0
        if t_set <= BERTH_WINDOW and tq <= THR_AUTH:
            thr_ok += 1
            code = 1
        if t_set <= BERTH_WINDOW and tq <= RW_AUTH:
            rw_ok += 1
            code = 2
        heat[j, i] = code
frac_rw = rw_ok / tot
frac_thr = thr_ok / tot
h4 = frac_rw <= 0.50 and 0.05 <= frac_rw <= 0.15 and 0.25 <= frac_thr <= 0.45

findings = {
    "H1": {"contact_kN": contact, "soft_capture_max_kN": soft,
           "arrest_impulse_kNs": [round(M_WATER * v / 1e3, 1) for v in V_C],
           "held": bool(h1)},
    "H2": {"slosh_f_hz_band": [round(1 / 300, 3), round(1 / 10, 3)],
           "acs_band_hz": list(ACS_BW),
           "overlap_up_to_ts_s": round(max(overlap_ts)), "held": bool(h2)},
    "H3": {"mass_ratios": ratios,
           "torque_Nm": {str(k): round(v, 1) for k, v in torque.items()},
           "rw_authority_Nm": RW_AUTH, "thruster_authority_Nm": THR_AUTH,
           "held": bool(h3)},
    "H4": {"viable_corner_rw_pct": round(frac_rw * 100),
           "viable_corner_thruster_pct": round(frac_thr * 100),
           "prescribes": "T_s~100-180s AND zeta>=0.1, unprecedented at 40t",
           "coupled_stability": "needs Basilisk 6-DOF linearSpringMassDamper",
           "held": bool(h4)},
}

# --- figure ---
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15.5, 4.8))
for v_c, color in ((0.01, "#256abf"), (0.05, "#eda100"), (0.10, "#e34948")):
    kk = np.logspace(3, 5, 50)
    ax1.plot(kk, v_c * np.sqrt(kk * M_WATER) / 1e3, color=color, lw=2,
             label=f"v_c = {v_c} m/s")
ax1.axhline(1.0, color="#5a6378", lw=1.2, ls=":")
ax1.text(1.1e3, 1.15, "1 kN (soft-capture arm)", fontsize=8, color="#5a6378")
ax1.set_xscale("log")
ax1.set_xlabel("soft-capture stiffness k_c [N/m]")
ax1.set_ylabel("peak contact force [kN]")
ax1.set_title("H1: contact is tractable (soft capture ≤ 1 kN)")
ax1.grid(True, alpha=0.25, which="both")
ax1.legend(fontsize=8.5)

ax2.plot(ts_grid, m_s * X_S * (2 * math.pi / ts_grid) ** 2 * R_OFF,
         color="#256abf", lw=2)
ax2.axhline(RW_AUTH, color="#7a9a3a", lw=1.3, ls="--")
ax2.text(150, RW_AUTH * 1.3, "reaction-wheel authority", fontsize=8,
         color="#5a7a2a")
ax2.axhline(THR_AUTH, color="#e34948", lw=1.3, ls="--")
ax2.text(150, THR_AUTH * 1.3, "thruster authority", fontsize=8, color="#a33")
ax2.axvspan(10, 100, color="#eda100", alpha=0.12)
ax2.text(12, 500, "slosh overlaps\nACS band\n(T_s ≲ 100 s)", fontsize=8,
         color="#8a6a00")
ax2.set_yscale("log")
ax2.set_xlabel("slosh period T_s [s]")
ax2.set_ylabel("hub disturbance torque [N·m]")
ax2.set_title("H2/H3: torque defeats wheels; slosh hits ACS band")
ax2.grid(True, alpha=0.25, which="both")

extent = [gts[0], gts[-1], gz[0], gz[-1]]
ax3.imshow(heat, origin="lower", aspect="auto", extent=extent,
           cmap="RdYlGn", vmin=0, vmax=2, interpolation="nearest")
ax3.set_xlabel("slosh period T_s [s]")
ax3.set_ylabel("slosh damping ζ")
ax3.set_title(f"H4: viable corner narrow — {round(frac_rw*100)}% RW / "
              f"{round(frac_thr*100)}% thruster")
ax3.text(0.98, 0.03, "green = RW-controllable & settles in window\n"
         "yellow = thruster-only   red = infeasible",
         transform=ax3.transAxes, fontsize=7.5, ha="right", va="bottom",
         bbox=dict(boxstyle="round", fc="white", ec="#cbd2dc", alpha=0.9))
fig.tight_layout()
fig.savefig(RESULTS / "bag_dynamics.png", dpi=160)

with open(RESULTS / "findings.json", "w") as fh:
    json.dump({"findings": findings}, fh, indent=1, default=float)

for h in ("H1", "H2", "H3", "H4"):
    print(h, "HELD" if findings[h]["held"] else "FALSIFIED")
print(f"R_bag {R_BAG:.2f} m | soft-capture max {soft} kN | mass ratios {ratios} "
      f"| torque@100s {torque[100]:.0f} N·m | viable corner {round(frac_rw*100)}% RW "
      f"/ {round(frac_thr*100)}% thruster")
