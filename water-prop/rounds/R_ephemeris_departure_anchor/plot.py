#!/usr/bin/env python3
"""Figure for R-ephemeris-departure-anchor. Reads results/ephemeris_findings.json."""
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

RESULTS = Path(__file__).resolve().parent / "results"
F = json.loads((RESULTS / "ephemeris_findings.json").read_text())


def jd_to_year(jd):
    return (jd - 2451545.0) / 365.25 + 2000.0


fig, ax = plt.subplots(2, 2, figsize=(13, 9))
fig.suptitle("R-ephemeris-departure-anchor — first real-JPL-ephemeris ICEBERG round "
             "(all H1–H4 HELD): hand 5.44 km/s confirmed", fontsize=12, fontweight="bold")

# -- Panel 1: porkchop scatter --
a = ax[0, 0]
sc = np.array(F["_scatter"])
yr = jd_to_year(sc[:, 0])
tof = sc[:, 1]
vinf = sc[:, 2]
p = a.scatter(yr, tof, c=vinf, s=6, cmap="viridis", vmin=5.2, vmax=8.0)
# mark global min
gi = int(np.argmin(vinf))
a.scatter([yr[gi]], [tof[gi]], marker="*", s=180, color="#c1121f",
          edgecolor="white", zorder=5, label=f"min {F['H1']['vinf_min_kms']:.2f} km/s")
cb = fig.colorbar(p, ax=a)
cb.set_label("departure v∞ (km/s)")
a.set_xlabel("departure year")
a.set_ylabel("time of flight (yr)")
a.set_title("H1 [S] — Saturn→Earth Lambert porkchop (real Horizons ephemeris)",
            fontsize=10)
a.legend(fontsize=8, loc="upper right")

# -- Panel 2: min v_inf per departure epoch (synodic modulation) --
a = ax[0, 1]
em = np.array(F["_epoch_min"])
a.plot(jd_to_year(em[:, 0]), em[:, 1], color="#1b4965", lw=1.6,
       label="min v∞ per departure epoch")
a.axhline(5.44, color="#5fa8d3", ls="--", lw=1.5, label="hand min-energy (5.44)")
a.axhline(6.21, color="#e07a5f", ls="--", lw=1.5, label="campaign anchor (6.21)")
a.axhline(F["H1"]["vinf_min_kms"], color="#c1121f", ls=":", lw=1.3,
          label=f"real min ({F['H1']['vinf_min_kms']:.2f})")
a.set_xlabel("departure year")
a.set_ylabel("minimum departure v∞ (km/s)")
a.set_title("H1/H2 [S] — real min brackets hand 5.44; 6.21 is a faster-transfer value",
            fontsize=9.5)
a.legend(fontsize=8, loc="upper right")
a.grid(alpha=0.3)

# -- Panel 3: Titan cap sensitivity --
a = ax[1, 0]
MU_S, V_T, R_TO = 3.793e7, 5.57, 3.793e7 / 5.57 ** 2
vt = np.linspace(1.5, 4.5, 120)
exc = [math.sqrt(max(0, (V_T + x) ** 2 - 2 * MU_S / R_TO)) for x in vt]
a.plot(vt, exc, color="#1b4965", lw=2, label="max Saturn-centric departure excess")
a.axhline(5.44, color="#c1121f", ls="--", lw=1.5, label="departure requirement (5.44)")
a.scatter([3.0], [F["H3"]["cap_at_vinfT3_kms"]], color="#5fa8d3", s=90, zorder=5,
          label=f"R186-consistent ({F['H3']['cap_at_vinfT3_kms']:.2f} at v∞_T=3)")
a.axvline(F["H3"]["vinfT_threshold_5p44"], color="#8ac926", ls=":", lw=1.5,
          label=f"re-open threshold (v∞_T={F['H3']['vinfT_threshold_5p44']:.2f})")
a.axvspan(F["H3"]["vinfT_threshold_5p44"], 4.5, color="#8ac926", alpha=0.12)
a.set_xlabel("Titan-relative excess v∞_T (km/s)")
a.set_ylabel("max Saturn-centric departure excess (km/s)")
a.set_title("H3 [S] — reproduces R186 ~3.3 at v∞_T=3, but the cap is CONDITIONAL",
            fontsize=9.5)
a.legend(fontsize=7.5, loc="upper left")
a.grid(alpha=0.3)

# -- Panel 4: synthesis --
a = ax[1, 1]
a.axis("off")
a.set_title("H4 [W] — reactor floor unmoved; a methodology weakness retired",
            fontsize=10)
txt = (
    "WHAT THIS ROUND DID (first ephemeris round in ICEBERG):\n"
    "  replaced hand vis-viva with a real JPL-Horizons Lambert\n"
    "  porkchop (134,396 cells; Lambert cross-validated to\n"
    f"  {F['lambert_validation_err_kms']:.0e} km/s vs Curtis Ex 5.2).\n\n"
    "RESULTS:\n"
    f"  • real min departure v∞ = {F['H1']['vinf_min_kms']:.2f} km/s\n"
    "    → brackets hand 5.44 (within ~3.4%); 6.21 is a\n"
    "      realizable faster transfer, as claimed.\n"
    "    → retires design-axes/04 'vis-viva-default anchoring'\n"
    "      (Methodology lesson 20) for this anchor.\n"
    f"  • reactor floor unmoved: {F['H4']['floor_min_kwe']:.0f} kWe at real min\n"
    f"    (5.44→{F['H4']['floor_544_kwe']:.0f}, 6.21→{F['H4']['floor_621_kwe']:.0f});"
    " Oberth-suppressed.\n\n"
    "NEW FINDING (H3):\n"
    "  Titan pump cap reproduces R186 ~3.3 km/s at the\n"
    "  natural v∞_T≈3, BUT scales with v∞_T and reaches the\n"
    f"  5.44 requirement at v∞_T≥{F['H3']['vinfT_threshold_5p44']:.2f}.\n"
    "  → R186's Titan revocation holds at nominal params but\n"
    "    is CONDITIONAL on the arrival-orbit v∞_T — a nuance\n"
    "    the magnitude-bound-only R186 did not quantify.\n"
    "  → does NOT move the reactor floor; re-opens a design\n"
    "    question (Saturn-frame Titan-tour optimizer = follow-on).")
a.text(0.02, 0.98, txt, transform=a.transAxes, va="top", ha="left",
       fontsize=8.2, family="monospace")

fig.tight_layout(rect=(0, 0, 1, 0.96))
out = RESULTS / "ephemeris.png"
fig.savefig(out, dpi=130)
print(f"wrote {out}")
