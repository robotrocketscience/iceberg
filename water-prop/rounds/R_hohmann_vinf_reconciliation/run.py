#!/usr/bin/env python3
"""R-hohmann-vinf-reconciliation — full computation vs H1-H4. Deterministic.

Reconciles the campaign's 6.21 km/s Saturn-departure v_inf against the two-body
minimum (5.44), and propagates it through departure Delta-v and the R179 reactor
floor. Reactor + Saturn-side anchors reproduce R179 exactly. Grids span scope_bounds.
"""
import json
import math
from pathlib import Path

RESULTS = Path(__file__).resolve().parent / "results"
RESULTS.mkdir(parents=True, exist_ok=True)

# heliocentric
MU_SUN = 1.32712440018e20
AU = 1.495978707e11
R_E = AU
A_SAT = {"9.537": 9.537, "9.5388": 9.5388, "9.582": 9.582}

# Saturn-centric (R179 anchors, verbatim)
MU_S = 3.793e16
R_RING = 1.07e8
G0 = 9.80665
VE_MET = 800.0 * G0
ETA = 0.6
YEAR = 3.156e7
V_CIRC = math.sqrt(MU_S / R_RING)
V_ESC = math.sqrt(2) * V_CIRC
TITAN_CAP = 3.2       # R186 bound-chain ceiling, km/s
VINF_CAMPAIGN = 6210.0


def hohmann_vinf(a_au):
    r_S = a_au * AU
    v_S = math.sqrt(MU_SUN / r_S)
    a_t = (r_S + R_E) / 2.0
    return v_S - math.sqrt(MU_SUN * (2.0 / r_S - 1.0 / a_t))


def perihelion_for_vinf(vinf, a_au=9.5388):
    """q (AU) of a Saturn->? transfer with aphelion at r_S giving this vinf."""
    r_S = a_au * AU
    v_S = math.sqrt(MU_SUN / r_S)
    v_aph = v_S - vinf
    inv_a = 2.0 / r_S - v_aph ** 2 / MU_SUN
    a = 1.0 / inv_a
    return (2 * a - r_S) / AU


def dv_single_burn(vinf):
    return math.sqrt(vinf ** 2 + 2 * MU_S / R_RING) - V_CIRC


def reactor_kwe(dv, m_f=100_000.0):
    prop = m_f * (math.exp(dv / VE_MET) - 1.0)
    return 0.5 * VE_MET ** 2 * prop / ETA / (2 * YEAR) / 1e3


vinf_min = hohmann_vinf(9.5388)
results = {}

# H1
results["H1"] = {
    "vinf_by_a_saturn_km_s": {k: round(hohmann_vinf(v) / 1000, 3) for k, v in A_SAT.items()},
    "min_energy_vinf_km_s": round(vinf_min / 1000, 2),
    "campaign_value_km_s": 6.21,
    "gap_pct": round((VINF_CAMPAIGN - vinf_min) / VINF_CAMPAIGN * 100, 1),
}

# H2
q621 = perihelion_for_vinf(VINF_CAMPAIGN)
results["H2"] = {
    "perihelion_for_6.21_AU": round(q621, 3),
    "tangent_hohmann_perihelion_AU": 1.0,
    "reading": "6.21 is a faster transfer (perihelion inside Venus orbit ~0.65 AU), "
               "conservative by 14%, not the minimum-energy Hohmann.",
}

# H3
dv_621 = dv_single_burn(VINF_CAMPAIGN)
dv_544 = dv_single_burn(vinf_min)
results["H3"] = {
    "v_circ_ring_km_s": round(V_CIRC / 1000, 2),
    "v_esc_ring_km_s": round(V_ESC / 1000, 2),
    "dv_at_6.21_km_s": round(dv_621 / 1000, 3),
    "dv_at_5.44_km_s": round(dv_544 / 1000, 3),
    "dv_change_km_s": round((dv_621 - dv_544) / 1000, 3),
    "dv_change_pct": round((dv_621 - dv_544) / dv_621 * 100, 1),
    "d_dv_d_vinf": round(VINF_CAMPAIGN / math.sqrt(V_ESC ** 2 + VINF_CAMPAIGN ** 2), 2),
    "reproduces_R179_8.51": abs(dv_621 / 1000 - 8.51) < 0.02,
}

# H4
p_621 = reactor_kwe(dv_621)
p_544 = reactor_kwe(dv_544)
p_spiral = reactor_kwe(9000.0)
results["H4"] = {
    "reactor_kwe_at_6.21": round(p_621),
    "reactor_kwe_at_5.44": round(p_544),
    "reactor_change_kwe": round(p_621 - p_544),
    "R179_headline_9.0_spiral_kwe": round(p_spiral),
    "existing_band_kwe": [155, 175],
    "titan_cap_km_s": TITAN_CAP,
    "titan_cap_below_min_vinf": TITAN_CAP < vinf_min / 1000,
    "revocation_holds": TITAN_CAP < vinf_min / 1000,
}

# grading
g = {}
g["H1"] = "HELD" if 5.3 <= vinf_min / 1000 <= 5.6 else "FALSIFIED"
g["H2"] = "HELD" if 0.55 <= q621 <= 0.75 else "FALSIFIED"
g["H3"] = "HELD" if (0.10 <= (dv_621 - dv_544) / 1000 <= 0.25
                     and results["H3"]["reproduces_R179_8.51"]) else "FALSIFIED"
g["H4"] = "HELD" if (150 <= p_544 <= 175 and abs(p_621 - p_544) < 10
                     and TITAN_CAP < vinf_min / 1000) else "FALSIFIED"
results["grades"] = g

(RESULTS / "findings.json").write_text(json.dumps(results, indent=2))

# figure
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 4.4))

    # panel 1: vinf vs transfer perihelion (where 5.44 and 6.21 sit)
    qs = [i / 100 for i in range(30, 101)]
    vs = []
    r_S = 9.5388 * AU
    v_S = math.sqrt(MU_SUN / r_S)
    for q in qs:
        a = (r_S + q * AU) / 2.0
        v_aph = math.sqrt(MU_SUN * (2.0 / r_S - 1.0 / a))
        vs.append((v_S - v_aph) / 1000)
    ax1.plot(qs, vs, "-", color="#268")
    ax1.axhline(5.44, color="#2a2", ls="--", lw=1); ax1.text(0.32, 5.44, " 5.44 min-energy", color="#2a2", va="bottom", fontsize=8)
    ax1.axhline(6.21, color="#c44", ls="--", lw=1); ax1.text(0.32, 6.21, " 6.21 campaign", color="#c44", va="bottom", fontsize=8)
    ax1.axvline(1.0, color="#888", ls=":", lw=1); ax1.text(1.0, min(vs), " tangent\n (Hohmann)", fontsize=7, va="bottom")
    ax1.plot([q621], [6.21], "o", color="#c44")
    ax1.set_xlabel("transfer perihelion q (AU)"); ax1.set_ylabel("Saturn departure v∞ (km/s)")
    ax1.set_title("6.21 is a faster transfer (q≈0.65 AU),\nnot the tangent minimum (5.44)")

    # panel 2: departure dv vs vinf (Oberth quadrature)
    vv = [i / 100 for i in range(500, 651)]
    dvv = [dv_single_burn(v * 1000) / 1000 for v in vv]
    ax2.plot(vv, dvv, "-", color="#268")
    for v, c, t in ((5.44, "#2a2", "5.44"), (6.21, "#c44", "6.21")):
        ax2.axvline(v, color=c, ls="--", lw=1)
        ax2.plot([v], [dv_single_burn(v * 1000) / 1000], "o", color=c)
    ax2.set_xlabel("departure v∞ (km/s)"); ax2.set_ylabel("single-burn departure Δv (km/s)")
    ax2.set_title(f"Δv change only {(dv_621-dv_544)/1000:.2f} km/s\n(Oberth quadrature, d/d={results['H3']['d_dv_d_vinf']})")

    # panel 3: reactor floor bars
    labels = ["v∞ 6.21\n(campaign)", "v∞ 5.44\n(min-energy)", "R179 9.0\nspiral (SoR)"]
    vals = [p_621, p_544, p_spiral]
    ax3.bar(labels, vals, color=["#c44", "#2a2", "#88a"])
    ax3.axhspan(155, 175, color="#ddd", alpha=0.5)
    ax3.text(2.4, 165, "155-175\nband", fontsize=7, ha="left", va="center")
    for i, v in enumerate(vals):
        ax3.text(i, v, f"{v:.0f}", ha="center", va="bottom", fontsize=9)
    ax3.set_ylabel("reactor floor (kWe)")
    ax3.set_title("v∞ correction moves the floor ~5 kWe:\nimmaterial")

    fig.tight_layout()
    fig.savefig(RESULTS / "vinf_reconciliation.png", dpi=150)
    print("figure -> results/vinf_reconciliation.png")
except Exception as e:  # pragma: no cover
    print(f"figure skipped: {e}")

print(json.dumps(results, indent=2))
print("\nGRADES:", g)
