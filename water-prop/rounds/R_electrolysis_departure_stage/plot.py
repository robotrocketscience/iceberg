"""Figure for R-electrolysis-departure-stage."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
r = json.load(open(HERE / "results" / "electrolysis_departure.json"))
a = r["architectures"]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.2))

# Panel 1: reactor power + water propellant, electric vs H2/O2
labels = ["Electric\nspiral\n(Round C)", "H₂/O₂\n(1-yr dwell)", "H₂/O₂\n(2-yr dwell)", "H₂/O₂\n(3-yr dwell)"]
reactor = [1248, 437, 219, 146]
water = [1531, 690, 690, 690]
x = np.arange(len(labels))
ax1b = ax1.twinx()
b1 = ax1.bar(x - 0.2, reactor, 0.4, color="#c0392b", label="reactor power (kWe)")
b2 = ax1b.bar(x + 0.2, water, 0.4, color="#2471a3", label="water propellant (t)")
ax1.axhspan(500, 1300, color="#c0392b", alpha=0.06)
ax1.text(0, 1180, "megawatt band", color="#c0392b", fontsize=8)
ax1.axhline(30, ls=":", color="#1e8449", lw=1.2)
ax1.text(3.2, 45, "Kilopower ~30 kWe", color="#1e8449", fontsize=7, ha="right")
for xi, v in zip(x - 0.2, reactor):
    ax1.text(xi, v + 20, f"{v}", ha="center", fontsize=8, color="#c0392b")
for xi, v in zip(x + 0.2, water):
    ax1b.text(xi, v + 20, f"{v}", ha="center", fontsize=8, color="#2471a3")
ax1.set_xticks(x); ax1.set_xticklabels(labels, fontsize=8)
ax1.set_ylabel("departure reactor power (kWe)", color="#c0392b")
ax1b.set_ylabel("departure water propellant (t)", color="#2471a3")
ax1.set_ylim(0, 1400); ax1b.set_ylim(0, 1700)
ax1.set_title("H₂/O₂ stage: 3–9× less reactor power AND less water")

# Panel 2: the cryo-vs-power tension (electrolysis window)
windows_d = [30, 90, 180, 365, 730, 1095]
jit = r["just_in_time_electrolysis_kwe"]
E = a["h2o2_isp420"]["prop_t"] * 1000 * 20e6
YEAR = 3.156e7
kwe = [E / (w * 86400) / 1e3 for w in windows_d]
ax2.plot(np.array(windows_d) / 365, kwe, "o-", color="#7d3c98", lw=2)
ax2.axhspan(500, 6000, color="#c0392b", alpha=0.06)
ax2.axhline(1248, ls="--", color="#c0392b", lw=1, label="electric spiral 1248 kWe")
ax2.axhline(30, ls=":", color="#1e8449", lw=1.2, label="Kilopower ~30 kWe")
ax2.annotate("avoid cryo H₂ →\nshort window →\nmegawatt+ spike", (30 / 365, 5325),
             xytext=(0.5, 3500), fontsize=8, color="#c0392b",
             arrowprops=dict(arrowstyle="->", color="#c0392b"))
ax2.annotate("long dwell →\nfew-hundred kWe\nbut 1–3 yr cryo-H₂ storage", (2, 219),
             xytext=(1.2, 900), fontsize=8, color="#7d3c98",
             arrowprops=dict(arrowstyle="->", color="#7d3c98"))
ax2.set_xlabel("electrolysis window / dwell (years)")
ax2.set_ylabel("electrolysis reactor power (kWe)")
ax2.set_yscale("log")
ax2.set_title("The tension: low power forces long cryo-H₂ storage")
ax2.legend(fontsize=8, loc="upper right")
ax2.grid(alpha=0.3, which="both")

fig.suptitle("R-electrolysis-departure-stage — the leading lever: megawatt → few-hundred-kWe "
             "(+cryo-H₂), not Kilopower", fontsize=11, y=1.00)
fig.tight_layout()
fig.savefig(HERE / "results" / "electrolysis_departure.png", dpi=130, bbox_inches="tight")
print("wrote", HERE / "results" / "electrolysis_departure.png")
