"""Figure for R-lunar-ga-arrival-fidelity: R12 vs honest lunar tour + root cause."""
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
import sys
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent.parent / "src"))
from run import (honest_tour, r12_tour_instrumented, vinf_globe_bound, V_INF_ARRIVAL)

res = json.load(open(HERE / "results" / "lunar_ga_fidelity.json"))

# Build per-flyby residual v_inf tracks
honest = honest_tour(V_INF_ARRIVAL, n_max=60, phi_deg=0.0)
r12 = r12_tour_instrumented(V_INF_ARRIVAL, 16)
bound = vinf_globe_bound(V_INF_ARRIVAL)

h_n = [0] + [p["flyby"] for p in honest["per_flyby"]]
h_v = [V_INF_ARRIVAL] + [p["vinf_E"] for p in honest["per_flyby"]]
r_n = [0] + [p["flyby"] for p in r12["per_flyby"]]
r_v = [V_INF_ARRIVAL] + [p["vinf_out"] for p in r12["per_flyby"]]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.2))

# Panel 1: residual v_inf vs flyby number
ax1.plot(r_n, r_v, "o-", color="#c0392b", label="R12 model (U_m recomputed each flyby)")
ax1.plot(h_n, h_v, "s-", color="#2471a3", label="Honest (U_m conserved)")
ax1.axhline(bound["vinf_floor"], ls="--", color="#2471a3", lw=1,
            label=f"v∞-globe floor {bound['vinf_floor']:.2f} km/s")
ax1.axhline(4.47, ls=":", color="#c0392b", lw=1, label="R12 claimed residual 4.47 km/s")
ax1.annotate(f"R12: 10 flybys → 4.47\n(shed 5.83 km/s)", (10, 4.47),
             xytext=(18, 2.6), fontsize=8, color="#c0392b",
             arrowprops=dict(arrowstyle="->", color="#c0392b"))
ax1.annotate(f"Honest: 51 flybys → 8.23\n(shed 2.07 km/s, ~4.1 yr phasing)",
             (51, bound["vinf_floor"]), xytext=(24, 9.2), fontsize=8, color="#2471a3",
             arrowprops=dict(arrowstyle="->", color="#2471a3"))
ax1.set_xlabel("lunar flyby number")
ax1.set_ylabel("Earth-frame v∞ (km/s)")
ax1.set_title("Inbound lunar tour: R12 vs v∞-conservation")
ax1.set_ylim(0, 11)
ax1.legend(fontsize=8, loc="upper right")
ax1.grid(alpha=0.3)

# Panel 2: root cause — R12 implied U_m decays; honest U_m conserved
ru_n = [p["flyby"] for p in r12["per_flyby"]]
ru_u = [p["U_m_implied"] for p in r12["per_flyby"]]
ax2.plot(ru_n, ru_u, "o-", color="#c0392b", label="R12 implied U_m (recomputed)")
ax2.axhline(honest["U_m"], ls="-", color="#2471a3", lw=2,
            label=f"conserved U_m = {honest['U_m']:.2f} km/s (correct)")
ax2.axhline(1.022, ls=":", color="gray", lw=1, label="v_Moon orbital 1.02 km/s")
ax2.annotate(f"U_m falls 73%\n(11.42 → 3.10)\n→ inflates late-flyby Δv",
             (8, 5.5), fontsize=9, color="#c0392b")
ax2.set_xlabel("lunar flyby number")
ax2.set_ylabel("Moon-relative speed U_m (km/s)")
ax2.set_title("Root cause: R12 violates v∞-conservation")
ax2.set_ylim(0, 12)
ax2.legend(fontsize=8, loc="upper right")
ax2.grid(alpha=0.3)

fig.suptitle("R-lunar-ga-arrival-fidelity — a lunar tour sheds ≤ 2.07 km/s of a 10.30 km/s "
             "Earth arrival, not 5.83", fontsize=11, y=1.00)
fig.tight_layout()
fig.savefig(HERE / "results" / "lunar_ga_fidelity.png", dpi=130, bbox_inches="tight")
print("wrote", HERE / "results" / "lunar_ga_fidelity.png")
