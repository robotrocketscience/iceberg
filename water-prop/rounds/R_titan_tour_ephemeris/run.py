#!/usr/bin/env python3
"""R-titan-tour-ephemeris — full sweep vs H1-H4. Deterministic.
Grids identical in span to scope_bounds.py (R182 lesson)."""
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
E_TITAN = 0.0288
MU_T = 8.97814e12
R_T_BODY = 2.5747e6
ALT_NOM = 1.0e6
ALT_SENS = 1.5e6
VINF_DEP = 6210.0
TRIMS_TOUR = 300.0
TRIMS_ONE = 50.0
VE_MET = 800.0 * G0
ETA_THR = 0.6
YEAR = 3.156e7
T_TITAN_D = 15.945
OBLIQ = 26.73
T_SAT_YR = 29.457
T_EQUINOX = 2025.37
DV_DIRECT = 8.45e3
DV_SINGLE = 8.51e3
R179_FLOOR = 7.0e3


def vis(r, a):
    return math.sqrt(MU_S * (2.0 / r - 1.0 / a))


def v_esc_at(r):
    return math.sqrt(2.0 * MU_S / r)


def turn(vinf_t, rp):
    return 2.0 * math.asin(1.0 / (1.0 + rp * vinf_t ** 2 / MU_T))


def exit_vinf(vinf_t, r_enc, rp):
    v_t = vis(r_enc, A_TITAN)
    vesc = v_esc_at(r_enc)
    ca = (vesc ** 2 - v_t ** 2 - vinf_t ** 2) / (2.0 * v_t * vinf_t)
    if ca > 1.0:
        return 0.0
    a_out = max(math.acos(max(ca, -1.0)) - turn(vinf_t, rp), 0.0)
    v2 = v_t ** 2 + vinf_t ** 2 + 2.0 * v_t * vinf_t * math.cos(a_out)
    return math.sqrt(max(v2 - vesc ** 2, 0.0))


def raise_state(ra, r_enc):
    a = (R_RING + ra) / 2.0
    dv = vis(R_RING, a) - vis(R_RING, R_RING)
    if ra < r_enc:
        return dv, None
    v_sc = vis(r_enc, a)
    v_th = R_RING * vis(R_RING, a) / r_enc
    v_r = math.sqrt(max(v_sc ** 2 - v_th ** 2, 0.0))
    return dv, math.hypot(v_th - vis(r_enc, A_TITAN), v_r)


def s3_powered(vinf_t, r_enc, rp):
    v_t = vis(r_enc, A_TITAN)
    vesc = v_esc_at(r_enc)
    ca = (vesc ** 2 - v_t ** 2 - vinf_t ** 2) / (2.0 * v_t * vinf_t)
    if ca > 1.0:
        return None
    a_esc = math.acos(max(ca, -1.0))
    target = VINF_DEP ** 2 + vesc ** 2
    lo, hi = 0.0, 6000.0
    for _ in range(60):
        dv_p = 0.5 * (lo + hi)
        vp_in = math.sqrt(vinf_t ** 2 + 2.0 * MU_T / rp)
        vout = math.sqrt(max((vp_in + dv_p) ** 2 - 2.0 * MU_T / rp, 0.0))
        half = math.asin(1.0 / (1.0 + rp * vinf_t ** 2 / MU_T)) \
            + math.asin(1.0 / (1.0 + rp * vout ** 2 / MU_T))
        a_out = max(a_esc - half, 0.0)
        v2 = v_t ** 2 + vout ** 2 + 2.0 * v_t * vout * math.cos(a_out)
        if v2 < target:
            lo = dv_p
        else:
            hi = dv_p
    return hi if hi < 5999.0 else None


def s5_contour_peri(vinf_t, r_enc):
    v_t = vis(r_enc, A_TITAN)
    h = (MU_S / r_enc - (vinf_t ** 2 - v_t ** 2) / 2.0) * r_enc / v_t
    if h <= 0.0:
        return None
    r_pb = h ** 2 / (2.0 * MU_S)
    if r_pb < R_RING or r_pb > r_enc:
        return None
    return math.sqrt(VINF_DEP ** 2 + 2.0 * MU_S / r_pb) \
        - math.sqrt(2.0 * MU_S / r_pb)


CORNERS = [(A_TITAN * (1 - E_TITAN), "peri"), (A_TITAN, "mean"),
           (A_TITAN * (1 + E_TITAN), "apo")]
N = 400

# --- exit-ceiling curves ---
vt_grid = np.linspace(2350.0, 9000.0, N)
ceil_curves = {}
ceil_max = {}
for r_enc, rtag in CORNERS:
    for rp, atag in ((R_T_BODY + ALT_NOM, "1000"), (R_T_BODY + ALT_SENS, "1500")):
        c = np.array([exit_vinf(v, r_enc, rp) for v in vt_grid])
        ceil_curves[f"{rtag}_{atag}"] = c
        ceil_max[f"{rtag}_{atag}"] = float(c.max())

# --- strategy sweeps (mean radius, 1000 km nominal) ---
r_enc, rp = A_TITAN, R_T_BODY + ALT_NOM
ra_grid = r_enc * 1.001 * (20.0 / 1.001) ** (np.arange(N) / (N - 1.0))
s2c, s3c, s5c = [], [], []
for ra in ra_grid:
    dv_r, vinf_t = raise_state(ra, r_enc)
    if vinf_t is None or vinf_t <= 0.0:
        s2c.append(np.nan), s3c.append(np.nan), s5c.append(np.nan)
        continue
    s2c.append(dv_r + max(0.0, VINF_DEP - exit_vinf(vinf_t, r_enc, rp))
               + TRIMS_TOUR)
    p = s3_powered(vinf_t, r_enc, rp)
    s3c.append(dv_r + p + TRIMS_TOUR if p is not None else np.nan)
    res = s5_contour_peri(vinf_t, r_enc)
    s5c.append(dv_r + res + TRIMS_TOUR if res is not None else np.nan)
s2c, s3c, s5c = map(np.array, (s2c, s3c, s5c))

v0_grid = np.linspace(0.0, VINF_DEP, N)
s4c = []
v_circ = vis(R_RING, R_RING)
for v0 in v0_grid:
    v_peri = math.sqrt(v0 ** 2 + 2.0 * MU_S / R_RING)
    v_sc = math.sqrt(v0 ** 2 + 2.0 * MU_S / r_enc)
    v_th = R_RING * v_peri / r_enc
    v_r = math.sqrt(max(v_sc ** 2 - v_th ** 2, 0.0))
    vinf_t = math.hypot(v_th - vis(r_enc, A_TITAN), v_r)
    kick = 2.0 * vinf_t * math.sin(turn(vinf_t, rp) / 2.0)
    v1 = math.sqrt(max((v_sc + kick) ** 2 - 2.0 * MU_S / r_enc, 0.0))
    s4c.append((v_peri - v_circ) + max(0.0, VINF_DEP - v1) + TRIMS_ONE)
s4c = np.array(s4c)

best = {"S2": float(np.nanmin(s2c)), "S3": float(np.nanmin(s3c)),
        "S4": float(np.nanmin(s4c)), "S5": float(np.nanmin(s5c))}
floor = min(best.values())
floor_by = min(best, key=best.get)

# floors at the other Titan-radius corners (S4 dominates; recompute)
floors_corner = {}
for r_e, rtag in CORNERS:
    tots = []
    for v0 in v0_grid:
        v_peri = math.sqrt(v0 ** 2 + 2.0 * MU_S / R_RING)
        v_sc = math.sqrt(v0 ** 2 + 2.0 * MU_S / r_e)
        v_th = R_RING * v_peri / r_e
        v_r = math.sqrt(max(v_sc ** 2 - v_th ** 2, 0.0))
        vinf_t = math.hypot(v_th - vis(r_e, A_TITAN), v_r)
        kick = 2.0 * vinf_t * math.sin(turn(vinf_t, rp) / 2.0)
        v1 = math.sqrt(max((v_sc + kick) ** 2 - 2.0 * MU_S / r_e, 0.0))
        tots.append((v_peri - v_circ) + max(0.0, VINF_DEP - v1) + TRIMS_ONE)
    floors_corner[rtag] = float(min(tots))

# --- H3 power repricing ---
GRAV_LOSS = 9000.0 / DV_DIRECT
dv_raise_h = vis(R_RING, (R_RING + A_TITAN) / 2.0) - v_circ
dv_lt = dv_raise_h * GRAV_LOSS + (VINF_DEP - ceil_max["mean_1000"]) \
    + TRIMS_TOUR


def p_2yr(dv):
    prop = 1e5 * (math.exp(dv / VE_MET) - 1.0)
    return 0.5 * VE_MET ** 2 * prop / ETA_THR / (2.0 * YEAR) / 1e3


p_direct, p_hybrid, p_lt, p_r179 = (p_2yr(9000.0), p_2yr(floor),
                                    p_2yr(dv_lt), p_2yr(R179_FLOOR))

# --- H4 survivors ---
dv_circ_cap = vis(R_RING, (R_RING + A_TITAN) / 2.0) - v_circ
rt = floor + dv_circ_cap
dv_r, vinf_h = raise_state(A_TITAN * 1.0000001, A_TITAN)
v_t = vis(A_TITAN, A_TITAN)
v_apo_h = vis(A_TITAN, (R_RING + A_TITAN) / 2.0)
a0 = math.acos(max(min((v_apo_h - v_t) / vinf_h, 1.0), -1.0))
d_h = turn(vinf_h, R_T_BODY + ALT_NOM)
ca = (v_esc_at(A_TITAN) ** 2 - v_t ** 2 - vinf_h ** 2) / (2 * v_t * vinf_h)
a_esc = math.acos(max(min(ca, 1.0), -1.0))
n_fly = math.ceil((a0 - a_esc) / d_h)
tour_yr = n_fly * 2 * T_TITAN_D / 365.25
epochs = np.linspace(2026.0, 2050.0, 289)
dec = OBLIQ * np.abs(np.cos(2 * np.pi * (epochs - T_EQUINOX) / T_SAT_YR))
crank = dec / math.degrees(d_h)
w = (epochs >= 2030) & (epochs <= 2045)
R_IAP, MU_IAP, RP_IAP = 3.5613e9, 1.205e11, 8.35e5
v_out = math.sqrt(3.2e3 ** 2 + 2 * MU_S / R_IAP)
vinf_i = v_out - math.sqrt(MU_S / R_IAP)
kick_i = 2 * vinf_i * math.sin(
    math.asin(1.0 / (1.0 + RP_IAP * vinf_i ** 2 / MU_IAP)))
v_iap_exit = math.sqrt((v_out + kick_i) ** 2 - 2 * MU_S / R_IAP)

# --- adjudication ---
h1 = (all(3000.0 <= v <= 3400.0 for v in ceil_max.values())
      and max(ceil_max.values()) <= 0.55 * VINF_DEP)
h2 = (8300.0 <= floor <= 8450.0 and 50.0 <= DV_DIRECT - floor <= 150.0
      and all(v >= 8000.0 for v in best.values()))
h3 = 150.0 <= p_hybrid <= 160.0 and 210.0 <= p_lt <= 235.0 \
    and min(p_hybrid, p_lt) >= 130.0
h4 = (abs(dv_circ_cap - 6700.0) <= 50.0 and 14950.0 <= rt <= 15250.0
      and 4 <= n_fly <= 8 and 0.3 <= tour_yr <= 0.7
      and float(crank[w].max()) <= 3.0
      and 0.15 <= (v_iap_exit - 3200.0) / 1e3 <= 0.30)

findings = {
    "H1": {"ceil_max_by_corner_km_s": {k: round(v / 1e3, 2)
                                       for k, v in ceil_max.items()},
           "required_km_s": 6.21, "held": bool(h1)},
    "H2": {"best_km_s": {k: round(v / 1e3, 2) for k, v in best.items()},
           "floor_km_s": round(floor / 1e3, 2), "floor_strategy": floor_by,
           "floors_by_titan_radius": {k: round(v / 1e3, 2)
                                      for k, v in floors_corner.items()},
           "saving_vs_direct_km_s": round((DV_DIRECT - floor) / 1e3, 2),
           "r179_floor_falsified": True, "held": bool(h2)},
    "H3": {"P_kwe": {"direct_spiral": round(p_direct), "hybrid_best":
                     round(p_hybrid), "low_thrust_honest": round(p_lt),
                     "r179_claim_dead": round(p_r179)},
           "bet3_band_kwe": [round(p_hybrid), round(p_direct)],
           "held": bool(h3)},
    "H4": {"capture_circ_km_s": round(dv_circ_cap / 1e3, 2),
           "round_trip_km_s": round(rt / 1e3, 2),
           "exit_flybys": n_fly, "tour_yr": round(tour_yr, 2),
           "crank_flybys_2030_2045": [round(float(crank[w].min()), 1),
                                      round(float(crank[w].max()), 1)],
           "iapetus_exit_km_s": round(v_iap_exit / 1e3, 2),
           "held": bool(h4)},
}

# --- figure ---
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15.5, 4.8))
band_lo = np.min([ceil_curves["apo_1500"], ceil_curves["peri_1000"]], axis=0)
band_hi = np.max([ceil_curves["apo_1500"], ceil_curves["peri_1000"]], axis=0)
ax1.fill_between(vt_grid / 1e3, band_lo / 1e3, band_hi / 1e3,
                 color="#256abf", alpha=0.18, label="corner band")
ax1.plot(vt_grid / 1e3, ceil_curves["mean_1000"] / 1e3, color="#256abf",
         lw=2, label="Titan mean, alt 1000 km")
ax1.axhline(VINF_DEP / 1e3, color="#e34948", lw=1.4, ls="--")
ax1.text(2.45, 6.35, "required 6.21 (Hohmann return)", fontsize=8.5,
         color="#e34948")
ax1.annotate("R179: “v∞ pumped free”\n(assumed, never bound-checked)",
             xy=(3.98, 3.28), xytext=(5.3, 4.4), fontsize=8.5,
             arrowprops=dict(arrowstyle="->", color="#5a6378"),
             color="#5a6378")
ax1.set_xlabel("v∞ relative to Titan [km/s]")
ax1.set_ylabel("max departure v∞ from pure flyby chain [km/s]")
ax1.set_title("The bound-chain ceiling: half the required excess")
ax1.set_ylim(0, 7.0)
ax1.grid(True, alpha=0.25)
ax1.legend(fontsize=8.5, loc="lower right")

ladder = [("direct\nbi-elliptic", DV_DIRECT, "#cbd2dc", ""),
          ("R179 claim\nfalsified", R179_FLOOR, "#ffffff", "//"),
          ("S4 peri\n+1 kick", best["S4"], "#256abf", ""),
          ("S3 powered\nflyby", best["S3"], "#256abf", ""),
          ("S5 contour\nperi", best["S5"], "#256abf", ""),
          ("S2 pump+\npost-esc", best["S2"], "#256abf", "")]
x = np.arange(len(ladder))
for xi, (lab, v, c, hatch) in zip(x, ladder):
    ax2.bar(xi, v / 1e3, color=c, width=0.6, hatch=hatch,
            edgecolor="#e34948" if hatch else "none", lw=1.2)
    ax2.text(xi, v / 1e3 + 0.12, f"{v/1e3:.2f}", ha="center", fontsize=9)
ax2.set_xticks(x, [l for l, _, _, _ in ladder], fontsize=8)
ax2.set_ylabel("departure Δv to v∞ = 6.21 [km/s]")
ax2.set_ylim(0, 11.0)
ax2.set_title(f"Honest floor {floor/1e3:.2f}: saving vs direct "
              f"{(DV_DIRECT-floor)/1e3:.2f} km/s, not 1.45")
ax2.grid(True, axis="y", alpha=0.25)

ax3.plot(epochs, crank, color="#256abf", lw=2)
ax3.fill_between(epochs, 0, crank, color="#256abf", alpha=0.15)
for yr, lab in ((2032.7, "solstice\n(free)"), (2040.1, "equinox\n(worst)")):
    ax3.axvline(yr, color="#5a6378", lw=1.0, ls=":")
    ax3.text(yr + 0.2, 1.45, lab, fontsize=8, color="#5a6378")
ax3.set_xlabel("departure epoch [yr]")
ax3.set_ylabel("declination crank [flybys-worth]")
ax3.set_title("Asymptote declination: schedule, not Δv")
ax3.set_ylim(0, 1.7)
ax3.grid(True, alpha=0.25)
fig.tight_layout()
fig.savefig(RESULTS / "titan_tour_ephemeris.png", dpi=160)

curves = {"vt_km_s": (vt_grid / 1e3).round(3).tolist(),
          "ceiling_mean_1000_km_s": (ceil_curves["mean_1000"] / 1e3
                                     ).round(3).tolist(),
          "epochs": epochs.round(2).tolist(),
          "crank_flybys": crank.round(2).tolist()}
with open(RESULTS / "findings.json", "w") as fh:
    json.dump({"findings": findings, "curves": curves}, fh, indent=1,
              default=float)

for h in ("H1", "H2", "H3", "H4"):
    print(h, "HELD" if findings[h]["held"] else "FALSIFIED")
print(f"floor {floor/1e3:.2f} ({floor_by}) | ceil "
      f"{ceil_max['mean_1000']/1e3:.2f} | P hybrid {p_hybrid:.0f} / lt "
      f"{p_lt:.0f} kWe | rt {rt/1e3:.2f} | flybys {n_fly} ({tour_yr:.2f} yr)")
