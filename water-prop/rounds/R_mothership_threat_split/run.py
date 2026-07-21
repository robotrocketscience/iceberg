#!/usr/bin/env python3
"""R-mothership-threat-split — full sweep vs H1-H4. Deterministic.
Grids span scope_bounds.py."""
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
RESULTS.mkdir(exist_ok=True)

STAGES = {"rendezvous": (0.985, 0.99, 0.995), "proxops": (0.95, 0.97, 0.99),
          "berth_bag": (0.88, 0.92, 0.95), "mate": (0.95, 0.97, 0.99),
          "sep": (0.985, 0.99, 0.995)}
THREAT = {"rendezvous": 0.00, "proxops": 0.05, "berth_bag": 0.35,
          "mate": 0.25, "sep": 0.15}
SWAP_BERTH = (0.92, 0.95, 0.97)
SWAP_THREAT_SCALE = 0.6
OPS_LPD = 0.453
MONO_LPD = 1.02
DELAY = 10.4


def chain(idx, berth=None):
    p = 1.0
    for k, v in STAGES.items():
        p *= (berth[idx] if (berth and k == "berth_bag") else v[idx])
    return p


def phi_ms(idx, scale=1.0):
    num = den = 0.0
    for k, v in STAGES.items():
        fail = 1.0 - v[idx]
        num += fail * min(THREAT[k] * scale, 1.0)
        den += fail
    return num / den


def retry(p_att, f_dmg, tries):
    b = (1.0 - p_att) * (1.0 - f_dmg)
    d = (1.0 - p_att) * f_dmg
    succ = sum(p_att * b ** k for k in range(tries))
    dmg = sum(d * b ** k for k in range(tries))
    return succ, dmg


def swap_terms(idx):
    _, dmg_sw = retry(chain(idx, SWAP_BERTH), 0.10, 3)
    return dmg_sw * phi_ms(idx, SWAP_THREAT_SCALE)


# --- H1 ---
phi_central = phi_ms(1)
phi_lo = min(phi_ms(i, 0.7) for i in (0, 1, 2))
phi_hi = max(phi_ms(i, 1.3) for i in (0, 1, 2))
h1 = 0.15 <= phi_lo and phi_hi <= 0.35 and 0.17 <= phi_central <= 0.31

# --- H2 ---
m_sw_c = swap_terms(1)
_, dmg_c = retry(chain(1), 0.10, 3)
m_hf_c = dmg_c * phi_central
p_surv_c = (1 - m_hf_c) ** 4 * (1 - m_sw_c)
loss_c = 1 - p_surv_c
risk_lpd_c = OPS_LPD / p_surv_c
h2 = 0.015 <= loss_c <= 0.025 and 0.46 <= risk_lpd_c <= 0.47

# --- H3 ---
phi_stress = phi_ms(0, 1.3)
_, dmg_s = retry(chain(0), 0.20, 3)
m_hf_s = dmg_s * phi_stress
p_surv_s = (1 - m_hf_s) ** 5 * (1 - m_sw_c)
loss_s = 1 - p_surv_s
risk_lpd_s = OPS_LPD / p_surv_s
h3 = 0.07 <= loss_s <= 0.12 and 0.49 <= risk_lpd_s <= 0.52

# --- H4 ---
def optimal_tries(idx, f_dmg, phi):
    p_att = chain(idx)
    best_t, best_ev = 0, -1.0
    for tries in range(1, 7):
        succ, dmg = retry(p_att, f_dmg, tries)
        ev = succ ** 4 * (1 - dmg * phi) ** 4
        if ev > best_ev:
            best_ev, best_t = ev, tries
    return best_t


def third_retry_ratio(idx, f_dmg, phi):
    p_att = chain(idx)
    s2, d2 = retry(p_att, f_dmg, 2)
    s3, d3 = retry(p_att, f_dmg, 3)
    return (s3 - s2) / max((d3 - d2) * phi, 1e-9)


corners = {"central": (1, 0.10, phi_central), "stress": (0, 0.20, phi_stress)}
opt = {k: optimal_tries(*v) for k, v in corners.items()}
ratio = {k: third_retry_ratio(*v) for k, v in corners.items()}
loss_by_n_c = [1 - (1 - m_hf_c) ** n * (1 - m_sw_c) for n in range(1, 7)]
monotone = all(loss_by_n_c[i] < loss_by_n_c[i + 1] for i in range(5))
h4 = all(v >= 3 for v in opt.values()) and all(r >= 50 for r in ratio.values()) \
    and monotone

# --- full surface ---
surface = []
for idx, band in ((0, "low"), (1, "central"), (2, "high")):
    phi = phi_ms(idx)
    m_sw = swap_terms(idx)
    for f_dmg in (0.05, 0.10, 0.20):
        _, dmg = retry(chain(idx), f_dmg, 3)
        m_hf = dmg * phi
        for n in (1, 2, 3, 4, 5, 6):
            surv = (1 - m_hf) ** n * (1 - m_sw)
            surface.append({"band": band, "f_dmg": f_dmg, "n": n,
                            "phi_ms": round(phi, 3),
                            "total_loss_pct": round((1 - surv) * 100, 2),
                            "risk_lpd": round(OPS_LPD / surv, 3)})

findings = {
    "H1": {"phi_central": round(phi_central, 2),
           "phi_band": [round(phi_lo, 2), round(phi_hi, 2)],
           "driver": "berth_bag", "held": bool(h1)},
    "H2": {"total_loss_pct": round(loss_c * 100, 1),
           "risk_lpd": round(risk_lpd_c, 3), "held": bool(h2)},
    "H3": {"total_loss_pct": round(loss_s * 100, 1),
           "risk_lpd": round(risk_lpd_s, 3), "phi_stress": round(phi_stress, 2),
           "held": bool(h3)},
    "H4": {"optimal_tries": opt, "third_retry_ratio": {k: round(v)
           for k, v in ratio.items()}, "tail_monotone_in_N": monotone,
           "verdict": "retry policy mothership-safe; tail is N-driven",
           "held": bool(h4)},
}

# --- figure ---
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15.5, 4.8))
for f_dmg, color in ((0.05, "#256abf"), (0.10, "#eda100"), (0.20, "#e34948")):
    for band, ls in (("central", "-"), ("low", "--")):
        pts = [r for r in surface if r["band"] == band and r["f_dmg"] == f_dmg]
        pts = sorted(pts, key=lambda r: r["n"])
        lab = f"{int(f_dmg*100)}% dmg" + ("" if band == "central" else ", low band")
        ax1.plot([r["n"] for r in pts], [r["total_loss_pct"] for r in pts],
                 ls, color=color, lw=1.7 if band == "central" else 1.1,
                 label=lab if band == "central" else None)
ax1.axhspan(7, 12, color="#e34948", alpha=0.10)
ax1.text(3.4, 10.9, "program-defining tail (stress corner)", fontsize=8,
         color="#a33")
ax1.set_xticks([1, 2, 3, 4, 5, 6])
ax1.set_xlabel("chunk handoffs per mission N")
ax1.set_ylabel("mission-total-loss probability [%]")
ax1.set_title("The mothership tail grows with N (solid: central, dashed: low band)")
ax1.grid(True, alpha=0.25)
ax1.legend(fontsize=8, loc="upper left")

stagenames = list(STAGES.keys())
fails = [1 - STAGES[s][1] for s in stagenames]
threats = [THREAT[s] for s in stagenames]
contrib = [f * t for f, t in zip(fails, threats)]
x = np.arange(len(stagenames))
ax2.bar(x, contrib, color="#256abf", width=0.6)
for xi, (f, t, c) in enumerate(zip(fails, threats, contrib)):
    ax2.text(xi, c + 0.0008, f"fail {f:.2f}\n×thr {t:.2f}", ha="center",
             fontsize=7.5)
ax2.set_xticks(x, stagenames, fontsize=8, rotation=15)
ax2.set_ylabel("contribution to φ_ms  [fail × threat]")
ax2.set_title(f"berth_bag drives the threat (φ_ms = {phi_central:.2f})")
ax2.set_ylim(0, max(contrib) * 1.35)
ax2.grid(True, axis="y", alpha=0.25)

for corner, color in (("central", "#256abf"), ("stress", "#e34948")):
    idx, f_dmg, phi = corners[corner]
    p_att = chain(idx)
    tries = list(range(1, 7))
    evs = []
    for t in tries:
        succ, dmg = retry(p_att, f_dmg, t)
        evs.append(succ ** 4 * (1 - dmg * phi) ** 4)
    ax3.plot(tries, evs, "o-", color=color, lw=1.8,
             label=f"{corner} (opt={opt[corner]})")
ax3.set_xticks(tries)
ax3.set_xlabel("retry attempts per handoff")
ax3.set_ylabel("catastrophic-weighted mission EV")
ax3.set_title("Retries stay EV-optimal: the tension does not bind")
ax3.grid(True, alpha=0.25)
ax3.legend(fontsize=8.5, loc="lower right")
fig.tight_layout()
fig.savefig(RESULTS / "mothership_threat.png", dpi=160)

with open(RESULTS / "findings.json", "w") as fh:
    json.dump({"findings": findings, "surface": surface}, fh, indent=1,
              default=float)

for h in ("H1", "H2", "H3", "H4"):
    print(h, "HELD" if findings[h]["held"] else "FALSIFIED")
print(f"phi_ms {phi_central:.2f} | central loss {loss_c*100:.1f}% lpd "
      f"{risk_lpd_c:.3f} | stress loss {loss_s*100:.1f}% lpd {risk_lpd_s:.3f} "
      f"| opt tries {opt} ratio {[round(r) for r in ratio.values()]}")
