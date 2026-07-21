#!/usr/bin/env python3
"""R-departure-anchor-reconciliation — sequence sweep + repricing vs H1-H4.

Closed-form patched-conic. Deterministic.
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

G0 = 9.80665
MU_S = 3.793e16
R_RING = 1.07e8
R_TITAN = 1.2217e9
VE_MET = 800.0 * G0
VE_GAS = 480.0 * G0
ETA_THR = 0.6
YEAR = 3.156e7
TRIMS = 300.0
KICK_MULT = 5.84
BASELINE = 50.0 / 40.0
MU_MOON = {"Titan": 8.978e12, "Rhea": 1.539e11, "Enceladus": 7.21e9,
           "Mimas": 2.503e9}
R_MOON_ORB = {"Titan": 1.2217e9, "Rhea": 5.271e8, "Enceladus": 2.380e8,
              "Mimas": 1.855e8}
R_MOON_MIN = {"Titan": 3.575e6, "Rhea": 8.64e5, "Enceladus": 3.02e5,
              "Mimas": 2.48e5}


def vis(r, a):
    return math.sqrt(MU_S * (2.0 / r - 1.0 / a))


def a_of(rp, ra):
    return (rp + ra) / 2.0


def hyp_v(r, vinf):
    return math.sqrt(vinf ** 2 + 2 * MU_S / r)


V_CIRC = vis(R_RING, R_RING)

# --- sequence sweep ---
sequences = {}
for vinf in (5400.0, 6210.0, 7000.0):
    seqs = {"single": hyp_v(R_RING, vinf) - V_CIRC}
    for rp in (6.0e7, 6.5e7, 7.0e7, 7.5e7, 8.0e7):
        drop = V_CIRC - vis(R_RING, a_of(rp, R_RING))
        burn = hyp_v(rp, vinf) - vis(rp, a_of(rp, R_RING))
        seqs[f"oberth_{rp/1e6:.0f}Mm"] = drop + burn
    for r_i in (R_TITAN, 2 * R_TITAN, 3.0e9):
        b1 = vis(R_RING, a_of(R_RING, r_i)) - V_CIRC
        b2 = abs(vis(r_i, a_of(6.0e7, r_i)) - vis(r_i, a_of(R_RING, r_i)))
        b3 = hyp_v(6.0e7, vinf) - vis(6.0e7, a_of(6.0e7, r_i))
        seqs[f"bielliptic_{r_i/R_TITAN:.0f}xTitan"] = b1 + b2 + b3
    seqs["titan_tour"] = (vis(R_RING, a_of(R_RING, R_TITAN)) - V_CIRC) + TRIMS
    sequences[vinf] = {k: round(v, 1) for k, v in seqs.items()}

DV_RAISE = vis(R_RING, a_of(R_RING, R_TITAN)) - V_CIRC
DV_TITAN = DV_RAISE + TRIMS
moonless = {k: v for k, v in sequences[6210.0].items() if k != "titan_tour"}
dv_min_moonless = min(moonless.values())
dv_oberth_audit = sequences[6210.0]["oberth_60Mm"] \
    - (V_CIRC - vis(R_RING, a_of(6.0e7, R_RING)))

# inner-moon ladder: max deflection dv per flyby at tour-typical v_inf 2 km/s
moon_kick = {}
for m in MU_MOON:
    vinf_m = 2000.0
    delta = 2 * math.asin(1 / (1 + vinf_m ** 2 * R_MOON_MIN[m] / MU_MOON[m]))
    moon_kick[m] = round(2 * vinf_m * math.sin(delta / 2), 1)

# capture-side symmetry
DV_CAPTURE_CIRC = DV_RAISE
RT_HONEST = DV_CAPTURE_CIRC + DV_TITAN

# --- repricing ---
def staged_gas(payload, dv):
    m = payload
    for _ in range(2):
        r = math.exp(dv / 2 / VE_GAS)
        w = m * (r - 1) / (1 - 0.08 * r)
        if w <= 0 or not math.isfinite(w):
            return float("inf")
        m += w
    return m - payload


CORNERS = {"canonical": {"payload": 65_000.0, "base_launch": 555.0,
                         "delivered": 32.3},
           "best": {"payload": 105_000.0, "base_launch": 503.0,
                    "delivered": 76.7}}
repricing = {}
for cname, c in CORNERS.items():
    out = {}
    out["desk_1.5_reference"] = {
        "launch_t": c["base_launch"],
        "ratio": round((c["base_launch"] / c["delivered"]) / BASELINE, 1),
        "note": "as shipped by R178; departure already paid at 1.5 km/s"}
    for oname, dv in (("titan_gas_7.0", DV_TITAN),
                      ("direct_gas_8.5", dv_min_moonless)):
        gas = staged_gas(c["payload"], dv)
        launch = c["base_launch"] + gas * 1.2 * KICK_MULT / 1000.0
        out[oname] = {"gas_at_saturn_t": round(gas / 1000, 0),
                      "launch_t": round(launch, 0),
                      "ratio": round((launch / c["delivered"]) / BASELINE, 1)}
    for oname, dv in (("chunk_fed_9.0", 9000.0),
                      ("chunk_fed_titan", DV_TITAN)):
        m_f = c["payload"] - 5_000.0
        prop = m_f * (math.exp(dv / VE_MET) - 1)
        e_jet = 0.5 * VE_MET ** 2 * prop
        years = {p: round(e_jet / ETA_THR / (p * 1e3) / YEAR, 1)
                 for p in (2.2, 50.0, 110.0, 175.0, 300.0)}
        out[oname] = {"prop_t": round(prop / 1000, 0), "burn_years_by_kwe": years}
    repricing[cname] = out

# power requirement curve (best corner, 100 t final mass)
P_GRID = np.linspace(2.2, 300.0, 300)
curves = {}
for name, dv in (("direct 9.0 km/s", 9000.0), ("Titan-assisted 7.0", DV_TITAN)):
    prop = 100_000.0 * (math.exp(dv / VE_MET) - 1)
    e_jet = 0.5 * VE_MET ** 2 * prop
    curves[name] = e_jet / ETA_THR / (P_GRID * 1e3) / YEAR
p_req = {name: round(float(0.5 * VE_MET ** 2 * 100_000.0
                           * (math.exp(dv / VE_MET) - 1) / ETA_THR
                           / (2 * YEAR) / 1e3), 0)
         for name, dv in (("direct", 9000.0), ("titan", DV_TITAN))}

# --- hypotheses ---
h1 = (7500 <= dv_oberth_audit <= 7800 and 8300 <= dv_min_moonless <= 8700
      and abs(sequences[6210.0]["bielliptic_1xTitan"]
              - sequences[6210.0]["single"]) <= 200
      and dv_min_moonless >= 8000)
saving = 1 - DV_TITAN / dv_min_moonless
h2 = (6800 <= DV_TITAN <= 7300 and 0.15 <= saving <= 0.20
      and 6500 <= DV_CAPTURE_CIRC <= 6900 and 13300 <= RT_HONEST <= 14100
      and DV_TITAN >= 6000)
best_rep = repricing["best"]
h3 = (best_rep["titan_gas_7.0"]["ratio"] >= 35
      and best_rep["direct_gas_8.5"]["ratio"] >= 35
      and best_rep["chunk_fed_9.0"]["burn_years_by_kwe"][2.2] > 100)
prop_saving = 1 - repricing["best"]["chunk_fed_titan"]["prop_t"] \
    / repricing["best"]["chunk_fed_9.0"]["prop_t"]
h4 = (100 <= p_req["titan"] <= 190 and 100 <= p_req["direct"] <= 190
      and 0.25 <= prop_saving <= 0.40)

findings = {
    "H1": {"audit_oberth": round(dv_oberth_audit, 0),
           "min_moonless": round(dv_min_moonless, 0),
           "sequences_at_6210": sequences[6210.0], "held": bool(h1)},
    "H2": {"titan_assisted": round(DV_TITAN, 0), "saving": round(saving, 3),
           "capture_circ": round(DV_CAPTURE_CIRC, 0),
           "round_trip_honest": round(RT_HONEST, 0),
           "inner_moon_kick_m_s": moon_kick, "held": bool(h2)},
    "H3": {"repricing": repricing,
           "verdict": "R173-R178 non-fission round-trip headline falsified at honest anchor",
           "held": bool(h3)},
    "H4": {"p_req_2yr_kwe": p_req, "prop_saving_titan": round(prop_saving, 2),
           "held": bool(h4)},
}

# --- figure ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 5.2))
bars = [("desk arc ledger (R173-R178)", 1.5, "#e34948"),
        ("Titan pump-up tour (+1-2 yr)", DV_TITAN / 1e3, "#256abf"),
        ("audit Oberth (parking orbit)", dv_oberth_audit / 1e3, "#5a6378"),
        ("honest impulsive minimum", dv_min_moonless / 1e3, "#26251f"),
        ("chunk-fed spiral (framework)", 9.0, "#eda100")]
y = np.arange(len(bars))
ax1.barh(y, [b[1] for b in bars], color=[b[2] for b in bars], height=0.6)
for i, b in enumerate(bars):
    ax1.text(b[1] + 0.12, i, f"{b[1]:.1f}", va="center", fontsize=9)
ax1.set_yticks(y, [b[0] for b in bars], fontsize=9)
ax1.invert_yaxis()
ax1.set_xlabel("Saturn-departure delta-v from co-orbital B-ring [km/s]")
ax1.set_title("The departure line, five ways")
ax1.grid(True, axis="x", alpha=0.25)
ax1.set_xlim(0, 10.5)

for name, c, color in (("direct 9.0 km/s", curves["direct 9.0 km/s"], "#eda100"),
                       ("Titan-assisted 7.0", curves["Titan-assisted 7.0"], "#256abf")):
    ax2.plot(P_GRID, c, color=color, lw=1.8, label=f"chunk-fed burn, {name}")
ax2.axhline(2.0, color="#26251f", lw=1.2, ls="--")
ax2.text(150, 2.3, "2-yr burn window", fontsize=8.5)
ax2.axvspan(100, 200, color="#cbd2dc", alpha=0.5, zorder=0)
ax2.text(105, 40, "Kilopower-class band", fontsize=8.5, color="#5a6378")
ax2.plot([2.2], [curves["direct 9.0 km/s"][0]], "o", ms=9, mfc="none",
         mec="#e34948", mew=2)
ax2.annotate("non-fission variant:\n2.2 kWe -> 159 yr", xy=(4.5, 150),
             xytext=(32, 45), fontsize=8.5, color="#e34948",
             arrowprops=dict(arrowstyle="->", color="#e34948", lw=1.1))
ax2.set_yscale("log")
ax2.set_xlabel("Saturn-side electric power [kWe]")
ax2.set_ylabel("departure burn duration [yr]")
ax2.set_title("Why the departure burn IS bet #3")
ax2.grid(True, which="both", alpha=0.25)
ax2.legend(fontsize=8.5)
fig.tight_layout()
fig.savefig(RESULTS / "departure_anchor.png", dpi=160)

with open(RESULTS / "findings.json", "w") as fh:
    json.dump({"findings": findings, "sequences": sequences}, fh, indent=1,
              default=float)

for h in ("H1", "H2", "H3", "H4"):
    print(h, "HELD" if findings[h]["held"] else "FALSIFIED")
print("min moonless:", round(dv_min_moonless), "| titan:", round(DV_TITAN),
      "| RT honest:", round(RT_HONEST))
print("best-corner repricing:", {k: v.get("ratio") for k, v in best_rep.items()
                                 if "ratio" in v})
print("chunk-fed at 2.2 kWe:", best_rep["chunk_fed_9.0"]["burn_years_by_kwe"][2.2], "yr")
print("P req 2-yr:", p_req, "| titan prop saving:", round(prop_saving, 2))
print("inner-moon per-flyby kick [m/s]:", moon_kick)
