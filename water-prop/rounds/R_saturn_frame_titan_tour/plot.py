#!/usr/bin/env python3
"""Figure for R-saturn-frame-titan-tour. Reads results/tour_findings.json."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

RESULTS = Path(__file__).resolve().parent / "results"
F = json.loads((RESULTS / "tour_findings.json").read_text())
M = F["moons"]
REQ = F["requirement_kms"]
order = ["Tethys", "Dione", "Rhea", "Titan", "Iapetus"]

fig, ax = plt.subplots(2, 2, figsize=(13, 9))
fig.suptitle("R-saturn-frame-titan-tour — the R186 crack CLOSED (all H1–H4 HELD): "
             "no Saturn-moon tour reaches the 5.44 km/s departure requirement",
             fontsize=11.5, fontweight="bold")

# -- Panel 1: departure excess per moon vs requirement --
a = ax[0, 0]
de = [M[n]["dep_excess"] for n in order]
cols = ["#c1121f" if n != "Titan" else "#1b4965" for n in order]
bars = a.bar(order, de, color=cols, width=0.62)
for b, v in zip(bars, de):
    a.text(b.get_x() + b.get_width() / 2, v + 0.08, f"{v:.2f}", ha="center", fontsize=9)
a.axhline(REQ, color="#8ac926", ls="--", lw=1.8, label=f"departure requirement ({REQ})")
a.axhspan(REQ, 6.2, color="#8ac926", alpha=0.10)
a.set_ylim(0, 6.0)
a.set_ylabel("max Saturn-centric departure excess (km/s)")
a.set_title("H2/H3 [S] — Titan (4.15) is the best moon, still short of 5.44",
            fontsize=10)
a.legend(fontsize=8.5, loc="upper left")
a.grid(alpha=0.3, axis="y")

# -- Panel 2: vinf provided (B-ring) vs needed (5.44) per moon --
a = ax[0, 1]
x = np.arange(len(order))
prov = [M[n]["vinf_bring"] for n in order]
need = [M[n]["vinf_needed_5p44"] for n in order]
a.bar(x - 0.2, prov, 0.38, color="#5fa8d3", label="v∞ provided (from B-ring)")
a.bar(x + 0.2, need, 0.38, color="#e07a5f", label="v∞ needed (for 5.44)")
for xi, p_, n_ in zip(x, prov, need):
    a.annotate("", (xi + 0.2, p_), (xi + 0.2, n_),
               arrowprops=dict(arrowstyle="<->", color="0.3", lw=0.8))
a.axvline(3 + 0.5, color="0", lw=0)  # noop for spacing
a.text(3, 4.9, "Titan gap\n+0.67", ha="center", fontsize=8, color="#1b4965")
a.set_xticks(x)
a.set_xticklabels(order)
a.set_ylabel("Titan-relative excess v∞_T (km/s)")
a.set_title("H1/H4 [S] — every moon underprovides v∞; the B-ring fixes v∞_T",
            fontsize=9.5)
a.legend(fontsize=8, loc="upper left")
a.grid(alpha=0.3, axis="y")

# -- Panel 3: per-flyby turn (pumping ability) --
a = ax[1, 0]
turns = [M[n]["flyby_turn_deg"] for n in order]
bcols = ["#c1121f" if n in ("Rhea", "Dione", "Tethys", "Iapetus") else "#1b4965"
         for n in order]
bars = a.bar(order, turns, color=bcols, width=0.62)
for b, v in zip(bars, turns):
    a.text(b.get_x() + b.get_width() / 2, v + 0.4, f"{v:.1f}°", ha="center", fontsize=9)
a.axhline(2.0, color="0.3", ls=":", lw=1.2, label="pumping-relevant floor (~2°)")
a.set_ylabel("per-flyby turn δmax (deg)")
a.set_title("H4 [W] — inner moons turn <1°/flyby → cannot pump v∞_T; "
            "Titan (21°) conserves it", fontsize=9.3)
a.legend(fontsize=8, loc="upper right")
a.grid(alpha=0.3, axis="y")

# -- Panel 4: synthesis --
a = ax[1, 1]
a.axis("off")
a.set_title("The crack, closed", fontsize=10.5)
txt = (
    "THE CRACK (from R-ephemeris-departure-anchor):\n"
    "  R186's Titan revocation is conditional — a Titan pump\n"
    "  reaches the 5.44 km/s requirement IF v∞_T ≥ 4.01.\n\n"
    "THIS ROUND (Saturn-frame, trajectory-bot primitives):\n"
    "  • harvest is at the B-ring → the minimal transfer to\n"
    "    Titan FIXES v∞_T = 3.34 km/s (reproduces R186's ~3.3\n"
    "    from first principles).\n"
    "  • Titan flybys CONSERVE v∞_T → Titan-only cap = 4.15.\n"
    "  • Titan is the sweet spot: inner moons are deeper and\n"
    "    give LESS (Rhea 0.99, Tethys/Dione ~0); Iapetus 3.41.\n"
    "  • the only way to pump v∞_T is a non-Titan handoff, but\n"
    "    the inner moons turn <1°/flyby (µ 41–154 ≪ Titan 8978)\n"
    "    — far too weak to make up the 0.67 km/s gap.\n"
    "  • + a direction cosine penalty makes 4.15 optimistic.\n\n"
    "VERDICT:  reaching v∞_T = 4 needs propulsion = supplying\n"
    "the departure energy the tour was meant to save.\n"
    "→ R186's revocation CONFIRMED (now derived, not asserted).\n"
    "→ 155–175 kWe reactor floor & bet #3 stand; the Titan\n"
    "  117 kWe branch stays dead.")
a.text(0.02, 0.98, txt, transform=a.transAxes, va="top", ha="left",
       fontsize=8.4, family="monospace")

fig.tight_layout(rect=(0, 0, 1, 0.96))
out = RESULTS / "tour.png"
fig.savefig(out, dpi=130)
print(f"wrote {out}")
