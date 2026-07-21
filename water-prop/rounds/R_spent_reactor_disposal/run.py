#!/usr/bin/env python3
"""R-spent-reactor-disposal — sweep vs H1-H4. Deterministic.
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

MU_S = 3.793e16
R_1BAR = 6.0268e7
R_ATM = 6.1e7
R_RING = 1.07e8
A_TITAN = 1.2217e9
MU_T = 8.978e12
R_T_BODY = 2.5747e6
ALT = 1.0e6
G0 = 9.80665
VE_MET = 800.0 * G0
U235_PER_UNIT = 27.7
KAPPA = {"paper": 100.0, "flown": 417.0}
DV_DEPART = 8.45e3


def vis(r, a):
    return math.sqrt(MU_S * (2.0 / r - 1.0 / a))


# --- H1 ---
v_circ = vis(R_RING, R_RING)
dv_deorbit = v_circ - vis(R_RING, (R_RING + R_ATM) / 2.0)
v_apo_stage = vis(A_TITAN, (R_RING + A_TITAN) / 2.0)
dv_peri_lower = v_apo_stage - vis(A_TITAN, (R_ATM + A_TITAN) / 2.0)
vinf_t = vis(A_TITAN, A_TITAN) - v_apo_stage
rp = R_T_BODY + ALT
flyby_cap = 2.0 * vinf_t * math.sin(
    math.asin(1.0 / (1.0 + rp * vinf_t ** 2 / MU_T)))
h1 = (2.6e3 <= dv_deorbit <= 3.0e3 and 0.4e3 <= dv_peri_lower <= 0.6e3
      and flyby_cap > dv_peri_lower and 1.1e3 <= flyby_cap <= 1.3e3)

# --- H2 ---
burnup = 500e3 * 3.0 * 3.156e7 / 3.2e-11 * 235e-3 / 6.022e23
deorbit_prop = {}
for tag, kap in KAPPA.items():
    m_react = kap * 155.0 / 1000.0
    prop = m_react * (math.exp(dv_deorbit / VE_MET) - 1.0)
    deorbit_prop[tag] = {"reactor_t": round(m_react), "prop_t": round(prop, 1),
                         "frac_pct": round(prop / m_react * 100)}
h2 = (0.4 <= burnup <= 0.8 and 6.0 <= deorbit_prop["paper"]["prop_t"] <= 8.0
      and 26.0 <= deorbit_prop["flown"]["prop_t"] <= 30.0)

# --- H3/H4 qualitative flags (structural, not banded) ---
h3 = True     # framing held if precedent-anchored + two-arch split (narrative)
h4 = dv_deorbit < DV_DEPART and flyby_cap > dv_peri_lower

# --- sweeps ---
peri_targets = np.linspace(R_1BAR, R_RING, 100)
dv_deorbit_curve = [v_circ - vis(R_RING, (R_RING + rt) / 2.0)
                    for rt in peri_targets]
powers = np.linspace(30, 175, 100)
prop_paper = [KAPPA["paper"] * p / 1000.0 * (math.exp(dv_deorbit / VE_MET) - 1)
              for p in powers]
prop_flown = [KAPPA["flown"] * p / 1000.0 * (math.exp(dv_deorbit / VE_MET) - 1)
              for p in powers]

findings = {
    "H1": {"co_orbital_deorbit_km_s": round(dv_deorbit / 1e3, 2),
           "staging_peri_lower_km_s": round(dv_peri_lower / 1e3, 3),
           "titan_flyby_capacity_km_s": round(flyby_cap / 1e3, 3),
           "disposal_free_via_titan": bool(flyby_cap > dv_peri_lower),
           "asymmetry": "Titan lowers periapsis (disposal) but cannot raise "
                        "v_inf (departure, R186)", "held": bool(h1)},
    "H2": {"u235_per_unit_kg": U235_PER_UNIT,
           "operational_burnup_kg": round(burnup, 2),
           "deorbit_propellant": deorbit_prop, "held": bool(h2)},
    "H3": {"protected_targets": ["Enceladus (subsurface ocean)",
                                 "Titan (organics, subsurface water)"],
           "precedent": "Cassini 2017 Saturn plunge, ~1e-6 strike refusal",
           "monolithic_concern": "cislunar (activated reactor returns)",
           "held": bool(h3)},
    "H4": {"binding_bet": False,
           "constraints": ["separable + independently disposable reactor",
                           "fleet: reserve one Titan disposal flyby per core",
                           "monolithic: UNPRICED cislunar activated-reactor "
                           "constraint"], "held": bool(h4)},
}

# --- figure ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.8, 5.0))
ladder = [("co-orbital\ndeorbit", dv_deorbit / 1e3, "#e34948", ""),
          ("staging peri-\nlower needed", dv_peri_lower / 1e3, "#256abf", ""),
          ("one Titan\nflyby capacity", flyby_cap / 1e3, "#7a9a3a", ""),
          ("departure\n(reference)", DV_DEPART / 1e3, "#cbd2dc", "")]
x = np.arange(len(ladder))
for xi, (lab, v, c, h) in zip(x, ladder):
    ax1.bar(xi, v, color=c, width=0.6)
    ax1.text(xi, v + 0.15, f"{v:.2f}", ha="center", fontsize=9)
ax1.annotate("", xy=(1, dv_peri_lower / 1e3), xytext=(2, flyby_cap / 1e3),
             arrowprops=dict(arrowstyle="->", color="#7a9a3a", lw=1.5))
ax1.text(1.5, 0.95, "flyby covers\nit → FREE", fontsize=8, color="#5a7a2a",
         ha="center")
ax1.set_xticks(x, [l for l, _, _, _ in ladder], fontsize=8.5)
ax1.set_ylabel("Δv [km/s]")
ax1.set_title("Disposal is cheap: free via Titan, ≤ 2.8 km/s direct")
ax1.set_ylim(0, 9.3)
ax1.grid(True, axis="y", alpha=0.25)

ax2.plot(powers, prop_paper, color="#256abf", lw=2, label="paper κ (100 kg/kWe)")
ax2.plot(powers, prop_flown, color="#e34948", lw=2, label="flown κ (417 kg/kWe)")
ax2.axvspan(155, 175, color="#eda100", alpha=0.15, label="bet #3 band (R186)")
ax2.set_xlabel("reactor electric power [kWe]")
ax2.set_ylabel("co-orbital deorbit propellant [t]")
ax2.set_title("Deorbiting a co-orbital spent core: 43% of reactor mass")
ax2.grid(True, alpha=0.25)
ax2.legend(fontsize=8.5, loc="upper left")
fig.tight_layout()
fig.savefig(RESULTS / "reactor_disposal.png", dpi=160)

with open(RESULTS / "findings.json", "w") as fh:
    json.dump({"findings": findings}, fh, indent=1, default=float)

for h in ("H1", "H2", "H3", "H4"):
    print(h, "HELD" if findings[h]["held"] else "FALSIFIED")
print(f"deorbit {dv_deorbit/1e3:.2f} | staging peri {dv_peri_lower/1e3:.3f} < "
      f"flyby {flyby_cap/1e3:.3f} (free) | burnup {burnup:.2f} kg | "
      f"deorbit prop {deorbit_prop}")
