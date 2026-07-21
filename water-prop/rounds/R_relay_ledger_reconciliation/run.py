#!/usr/bin/env python3
"""R-relay-ledger-reconciliation — full sweep vs H1-H4. Deterministic.
Grids span the pre-script's (R182 lesson)."""
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
MU_S = 3.7931206e16
R_RING = 1.07e8
A_TITAN = 1.22187e9
MU_T = 8.97814e12
R_T_BODY = 2.5747e6
ALT = 1.0e6
VINF_DEP = 6210.0
VE_MET = 800.0 * G0
VE_GAS = 480.0 * G0
ETA_THR = 0.6
YEAR = 3.156e7
KICK = 5.84
CHUNK = 40_000.0
M_BUS = 4_000.0
MONO_LPD = 1.02
FLEET_LPD = 0.365
RETENTION_N = {2: 0.946, 3: 0.927, 4: 0.908, 5: 0.890}   # R185 findings.json
HW_LPD = (0.8 + 0.4 + 0.2) * 5.84 / 160
DELAY = 10.4
L_FPY = 10.0
T_TRANSIT_YR = 8.0
E_ELEC = 20.2e6
P_SHUTTLE = 30.0
TRIMS_TOUR, TRIMS_ONE = 300.0, 50.0
EPS = 0.08


def vis(r, a):
    return math.sqrt(MU_S * (2.0 / r - 1.0 / a))


def turn(vinf_t, rp):
    return 2.0 * math.asin(1.0 / (1.0 + rp * vinf_t ** 2 / MU_T))


def exit_vinf(vinf_t, r_enc, rp):
    v_t = vis(r_enc, A_TITAN)
    vesc = math.sqrt(2.0 * MU_S / r_enc)
    ca = (vesc ** 2 - v_t ** 2 - vinf_t ** 2) / (2.0 * v_t * vinf_t)
    if ca > 1.0:
        return 0.0
    a_out = max(math.acos(max(ca, -1.0)) - turn(vinf_t, rp), 0.0)
    v2 = v_t ** 2 + vinf_t ** 2 + 2.0 * v_t * vinf_t * math.cos(a_out)
    return math.sqrt(max(v2 - vesc ** 2, 0.0))


# --- H1: the omitted departure line ---
a_ell = (R_RING + A_TITAN) / 2.0
v_peri_ell = vis(R_RING, a_ell)
rp = R_T_BODY + ALT
best_imp = None
for i in range(400):
    v0 = VINF_DEP * i / 399.0
    v_peri = math.sqrt(v0 ** 2 + 2.0 * MU_S / R_RING)
    v_sc = math.sqrt(v0 ** 2 + 2.0 * MU_S / A_TITAN)
    v_th = R_RING * v_peri / A_TITAN
    v_r = math.sqrt(max(v_sc ** 2 - v_th ** 2, 0.0))
    vinf_t = math.hypot(v_th - vis(A_TITAN, A_TITAN), v_r)
    kick = 2.0 * vinf_t * math.sin(turn(vinf_t, rp) / 2.0)
    v1 = math.sqrt(max((v_sc + kick) ** 2 - 2.0 * MU_S / A_TITAN, 0.0))
    tot = (v_peri - v_peri_ell) + max(0.0, VINF_DEP - v1) + TRIMS_ONE
    if best_imp is None or tot < best_imp[0]:
        best_imp = (tot, v0)
dv_imp = best_imp[0]
vinf_ell = vis(A_TITAN, A_TITAN) - vis(A_TITAN, a_ell)
v_exit = exit_vinf(vinf_ell, A_TITAN, rp)
dv_spiral = (VINF_DEP - v_exit) + TRIMS_TOUR
h1 = 1600.0 <= dv_imp <= 1800.0 and 3200.0 <= dv_spiral <= 3500.0


def departure_option(name, n_ch):
    """Return (harvest_t, launch_t, residence_yr) for the mothership
    departure with n_ch chunks aboard."""
    stack_dry = M_BUS + n_ch * CHUNK
    if name == "gas":
        m = stack_dry
        for _ in range(2):
            r = math.exp(dv_imp / 2.0 / VE_GAS)
            w = m * (r - 1.0) / (1.0 - EPS * r)
            m += w
        gas = m - stack_dry
        return (gas / 1e3, EPS * gas / (1.0 - EPS) * KICK / 1e3,
                gas * E_ELEC / (P_SHUTTLE * 1e3) / YEAR)
    kappa = 100.0 if name == "met_paper" else 417.0
    m_react = 0.0
    for _ in range(6):
        m_f = stack_dry + m_react
        prop = m_f * (math.exp(dv_spiral / VE_MET) - 1.0)
        p_m = 0.5 * VE_MET ** 2 * prop / ETA_THR / (T_TRANSIT_YR * YEAR) / 1e3
        m_react = kappa * p_m
    return (prop / 1e3,
            m_react * KICK / 1e3 * (T_TRANSIT_YR / L_FPY), 0.52)


# --- H2: ladder sweep over options x N ---
cells = []
for name in ("gas", "met_paper", "met_flown"):
    for n_ch in (2, 3, 4, 5):
        harv, launch, res = departure_option(name, n_ch)
        dlpd = launch / (n_ch * CHUNK / 1e3)
        lpd = FLEET_LPD / RETENTION_N[n_ch] + HW_LPD + dlpd
        adv = MONO_LPD / lpd
        d_star = (math.exp(math.log(adv) / DELAY) - 1.0) * 100.0
        cells.append({"option": name, "n": n_ch, "harvest_t": round(harv),
                      "launch_t": round(launch, 1), "res_yr": round(res, 2),
                      "dlpd": round(dlpd, 3), "lpd": round(lpd, 3),
                      "adv": round(adv, 2), "d_star_pct": round(d_star, 1)})
best_cell = min(cells, key=lambda c: c["lpd"])
h2 = (0.49 <= best_cell["lpd"] <= 0.53
      and 6.4 <= best_cell["d_star_pct"] <= 7.5
      and all(c["d_star_pct"] < 8.0 for c in cells))

# --- H3: harvest ledger ---
R_WELL = math.exp(6700.0 / VE_MET) - 1.0
m_sh = 2500.0 + 100.0 * 30.0
sortie_w = (m_sh + CHUNK) * R_WELL + m_sh * R_WELL
harv4, _, _ = departure_option(best_cell["option"], 4)
harv_shipped = (sortie_w + CHUNK) / CHUNK
harv_honest = (sortie_w + CHUNK + harv4 * 1e3 / 4) / CHUNK
mono_dry = 4000.0 + 100.0 * 30.0
harv_mono = ((mono_dry + CHUNK) * (math.exp(9000.0 / VE_MET) - 1.0)
             + CHUNK) / CHUNK
relief_shipped = (1 - harv_shipped / harv_mono) * 100.0
relief_honest = (1 - harv_honest / harv_mono) * 100.0
h3 = 3.2 <= harv_honest <= 3.4 and 5.0 <= relief_honest <= 10.0

# --- H4: lit-leg footnote ---
SATURN_R = 9.54
A_ELL = (1 + SATURN_R) / 2
ECC = (SATURN_R - 1) / (SATURN_R + 1)
_E = np.linspace(0, math.pi, 4000)
T_GRID = (_E - ECC * np.sin(_E)) / (2 * math.pi) * A_ELL ** 1.5 * YEAR
R_GRID = A_ELL * (1 - ECC * np.cos(_E))
mask = R_GRID <= 4.0
foot = {}
for akw in (100.0, 300.0):
    e_lit = float(np.trapezoid(akw * 1e3 / R_GRID[mask] ** 2, T_GRID[mask]))
    prop = e_lit * ETA_THR / (0.5 * VE_MET ** 2)
    for chunk in (40_000.0, 80_000.0):
        foot[f"{akw:.0f}kW_{chunk/1e3:.0f}t"] = {
            "prop_t": round(prop / 1e3, 1),
            "dv_km_s": round(VE_MET * math.log(
                (20_000.0 + chunk + prop) / (20_000.0 + chunk)) / 1e3, 2),
            "delivered_debit_pct": round(prop / chunk * 100.0)}
p300 = foot["300kW_80t"]["prop_t"]
h4 = 45.0 <= p300 <= 55.0 and 60 <= foot["300kW_80t"]["delivered_debit_pct"] <= 66

findings = {
    "H1": {"dv_impulsive_km_s": round(dv_imp / 1e3, 2),
           "dv_spiral_km_s": round(dv_spiral / 1e3, 2),
           "exit_ceiling_km_s": round(v_exit / 1e3, 2),
           "r182_carried": 0.0, "held": bool(h1)},
    "H2": {"best_cell": best_cell,
           "canonical_n4": next(c for c in cells
                                if c["option"] == "met_paper"
                                and c["n"] == 4),
           "all_below_8pct": all(c["d_star_pct"] < 8.0 for c in cells),
           "knife_edge_passes_d_star": [8.0, 10.4, 8.12,
                                        best_cell["d_star_pct"]],
           "held": bool(h2)},
    "H3": {"harvest_mono": round(harv_mono, 2),
           "harvest_relay_shipped": round(harv_shipped, 2),
           "harvest_relay_honest": round(harv_honest, 2),
           "relief_pct_shipped_to_honest": [round(relief_shipped),
                                            round(relief_honest)],
           "held": bool(h3)},
    "H4": {"lit_leg": foot, "held": bool(h4)},
}

# --- figure ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.8, 5.0))
passes = ["R183 NPV\n(lifetime-capped)", "R184 fleet\n(swap steady)",
          "R185 handoff\n(ops)", "R187 departure\n(this round)"]
dstars = [8.0, 10.4, 8.12, best_cell["d_star_pct"]]
colors = ["#cbd2dc", "#cbd2dc", "#cbd2dc", "#e34948"]
x = np.arange(len(passes))
ax1.bar(x, dstars, color=colors, width=0.55)
for xi, v in zip(x, dstars):
    ax1.text(xi, v + 0.15, f"{v:.1f}%", ha="center", fontsize=9)
ax1.axhline(8.0, color="#26251f", lw=1.3, ls="--")
ax1.text(2.42, 8.18, "8% utility hurdle", fontsize=8.5)
ax1.axhline(10.0, color="#5a6378", lw=1.1, ls=":")
ax1.text(-0.4, 10.2, "10% growth hurdle", fontsize=8.5, color="#5a6378")
ax1.set_xticks(x, passes, fontsize=8)
ax1.set_ylabel("break-even discount rate d* [%]")
ax1.set_ylim(0, 11.5)
ax1.set_title("The knife-edge resolves: honest departure drops d* to "
              f"{best_cell['d_star_pct']:.1f}%")
ax1.grid(True, axis="y", alpha=0.25)

opts = ["met_paper", "met_flown", "gas"]
labels = {"met_paper": "MET, paper κ", "met_flown": "MET, flown κ",
          "gas": "in-situ gas kick"}
markers = {"met_paper": "o", "met_flown": "s", "gas": "^"}
cmap = {"met_paper": "#256abf", "met_flown": "#eda100", "gas": "#e34948"}
for o in opts:
    pts = sorted([c for c in cells if c["option"] == o], key=lambda c: c["n"])
    ax2.plot([c["n"] for c in pts], [c["d_star_pct"] for c in pts],
             marker=markers[o], color=cmap[o], lw=1.7, ms=7,
             label=labels[o])
ax2.axhline(8.0, color="#26251f", lw=1.3, ls="--")
ax2.text(4.05, 8.12, "8% hurdle: no cell reaches it", fontsize=8.5)
ax2.set_xticks([2, 3, 4, 5])
ax2.set_xlabel("chunks per mission N")
ax2.set_ylabel("break-even discount rate d* [%]")
ax2.set_ylim(0, 9.0)
ax2.set_title("Every honest departure option, every N: below the hurdle")
ax2.grid(True, alpha=0.25)
ax2.legend(fontsize=8.5, loc="lower right")
fig.tight_layout()
fig.savefig(RESULTS / "relay_ledger.png", dpi=160)

with open(RESULTS / "findings.json", "w") as fh:
    json.dump({"findings": findings, "cells": cells}, fh, indent=1,
              default=float)

for h in ("H1", "H2", "H3", "H4"):
    print(h, "HELD" if findings[h]["held"] else "FALSIFIED")
print(f"best: {best_cell} | harvest mono {harv_mono:.2f} shipped "
      f"{harv_shipped:.2f} honest {harv_honest:.2f} | lit-leg {p300} t")
