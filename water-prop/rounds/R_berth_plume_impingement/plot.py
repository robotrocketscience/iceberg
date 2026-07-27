#!/usr/bin/env python3
"""Figure for R-berth-plume-impingement. Reads results/plume_findings.json."""
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

RESULTS = Path(__file__).resolve().parent / "results"
F = json.loads((RESULTS / "plume_findings.json").read_text())

V_E = 686.5
KAPPA, BETA = 4.0, 1e-2
A_BAG, R_OFF = 50.0, 5.0
TAU_DUMP, TAU_TH = 50.0, 2.5
THETA = math.radians(25.0)


def p_iso(Fn, r):
    return Fn / (2 * math.pi * r ** 2)


fig, ax = plt.subplots(2, 2, figsize=(13, 9))
fig.suptitle("R-berth-plume-impingement — the trade pivot (all H1–H4 HELD): "
             "plume benign, leg A viable under a placement constraint",
             fontsize=12.5, fontweight="bold")

r = np.linspace(1.5, 10, 120)

# -- Panel 1 (H1): pressure vs standoff --
a = ax[0, 0]
a.plot(r, [KAPPA * p_iso(10, x) for x in r], color="#c1121f", lw=2,
       label="core, F=10 N, κ=4 (worst)")
a.plot(r, [KAPPA * p_iso(5, x) for x in r], color="#e07a5f", lw=1.6, ls="--",
       label="core, F=5 N")
a.plot(r, [BETA * p_iso(5, x) for x in r], color="#5fa8d3", lw=2,
       label="backflow, F=5 N, β=1e-2")
a.axhline(1e4, color="0.2", lw=1.5, ls="-", label="aerogel damage limit (10 kPa)")
a.axhline(100, color="0.5", lw=1, ls=":", label="falsify line (100 Pa)")
a.set_yscale("log")
a.set_xlabel("bag standoff r (m)")
a.set_ylabel("plume pressure (Pa, log)")
a.set_title("H1 [S] — pressure 3.6 orders below structural limit (no damage)",
            fontsize=10)
a.legend(fontsize=7.5, loc="upper right")
a.grid(alpha=0.3, which="both")

# -- Panel 2 (H2): plume torque vs standoff, core vs backflow --
a = ax[1, 0]
tau_bf = [BETA * p_iso(5, x) * A_BAG * R_OFF for x in r]
a_illum = [math.pi * (x * math.tan(THETA)) ** 2 for x in r]
tau_core = [KAPPA * p_iso(5, x) * ai * R_OFF for x, ai in zip(r, a_illum)]
a.plot(r, tau_core, color="#c1121f", lw=2, label="bag in CORE (re-excites)")
a.plot(r, tau_bf, color="#5fa8d3", lw=2, label="bag in BACKFLOW (safe)")
a.axhline(TAU_TH, color="0.2", ls="--", lw=1.4,
          label="re-perturb threshold (2.5 N·m)")
a.axhline(TAU_DUMP, color="0.6", ls=":", lw=1, label="dump torque (50 N·m)")
a.axvspan(3, 10, color="#8ac926", alpha=0.15)
a.text(6.5, 0.045, "operating region\n(boom ≥ 3 m, backflow)", fontsize=8,
       color="#5a8a12", ha="center")
a.set_yscale("log")
a.set_xlabel("bag standoff r (m)")
a.set_ylabel("plume torque on bag (N·m, log)")
a.set_title("H2 [S] — geometry-conditioned: backflow safe, core re-excites "
            "(the design constraint)", fontsize=9.5)
a.legend(fontsize=7.5, loc="upper right")
a.grid(alpha=0.3, which="both")

# -- Panel 3 (H3): cumulative ice vs N berths --
a = ax[0, 1]
N = np.arange(0, 51)
ice_c = 2 * (5 / V_E) * 100 * 1e-3 * 0.10 * N * 1e3         # g, central
ice_w = 2 * (10 / V_E) * 100 * 1e-2 * 0.20 * N * 1e3        # g, worst backflow
a.plot(N, ice_c, color="#5fa8d3", lw=2, label="central (β_m=1e-3, f=0.1)")
a.plot(N, ice_w, color="#1b4965", lw=2, label="stress corner (β_m=1e-2, f=0.2)")
a.axhline(500, color="#c1121f", ls="--", lw=1.4, label="clog threshold (500 g, 1%)")
a.annotate(f"{ice_w[-1]:.0f} g\n(0.58% of intake)", (50, ice_w[-1]),
           (38, 350), fontsize=8, color="#1b4965",
           arrowprops=dict(arrowstyle="->", color="#1b4965", lw=0.8))
a.set_xlabel("berths (N)")
a.set_ylabel("cumulative water-ice on aerogel intake (g)")
a.set_title("H3 [S] — intake icing is grams over 50 berths (no clog)",
            fontsize=10)
a.legend(fontsize=8, loc="upper left")
a.grid(alpha=0.3)

# -- Panel 4 (H4): the trade resolution --
a = ax[1, 1]
a.axis("off")
a.set_title("H4 [W] — the pivot resolves: cost drops MANDATORY → OPTIONAL",
            fontsize=9.5)
txt = (
    "BEFORE this round (R-berth-momentum-management):\n"
    "  leg A cost = 'N plume firings at the bag' — unquantified.\n"
    "  If plume damages/re-excites → leg C or B MANDATORY\n"
    "  (precision capture, or +300–600 kg CMG + days cadence).\n\n"
    "AFTER (this round):\n"
    "  • H1 pressure 3.6 orders below aerogel limit → no damage\n"
    "  • H3 intake ice = grams over 50 berths → no clog\n"
    "  • H2 re-perturbation is GEOMETRY-conditioned:\n"
    "       backflow (boom ≥ 3 m) → 0.2 N·m (1/250 of dump) ✓\n"
    "       core geometry          → 11 N·m (22% of dump) ✗\n\n"
    "VERDICT:  leg A VIABLE under a thruster-placement /\n"
    "boom-length constraint (bag in backflow, standoff ≥ 3 m).\n"
    "→ CMG (leg B) & precision-capture (leg C) become OPTIONAL\n"
    "   risk-reduction for the worst-case-dump-axis residual,\n"
    "   not mandatory hardware.\n\n"
    "'Fire the thrusters; place them for backflow; boom ≥ 3 m;\n"
    " hold C/B as the worst-axis backstop.'")
a.text(0.02, 0.98, txt, transform=a.transAxes, va="top", ha="left",
       fontsize=8.6, family="monospace")

fig.tight_layout(rect=(0, 0, 1, 0.96))
out = RESULTS / "plume.png"
fig.savefig(out, dpi=130)
print(f"wrote {out}")
