#!/usr/bin/env python3
"""R-fast-first-chunk-decaying-price — full sweep vs H1-H4. Deterministic.

Folds R188's decaying clearing price into R_heterogeneous_cadence's exact engine
(schedule builders copied verbatim; the ONLY change is revenue uses a time-varying
price(t) = P0*exp(-rate*t) instead of a constant per-tonne value). Grids span
scope_bounds.py.
"""
import json
import math
from dataclasses import dataclass
from pathlib import Path

RESULTS = Path(__file__).resolve().parent / "results"
RESULTS.mkdir(parents=True, exist_ok=True)

# --- constants pinned to R_heterogeneous_cadence ---
BASE_CHUNK, BASE_RT, BASE_DELIV = 200.0, 14.5, 80.0
DELIV_FRAC = BASE_DELIV / BASE_CHUNK           # 0.40
RT_FLOOR, RT_SLOPE = 11.5, 3.0
FIRST_UNIT_COST_M = 500.0
CADENCE_PER_YR = 2.0
HORIZON_YR = 40.0
LR = 0.15

# --- R188 price anchors ---
RATES = {"static": 0.0, "cons": 0.092, "central": 0.128, "median": 0.177, "bull": 0.324}
P0_BAND = [3.0, 3.5, 4.0]
P0_CENTRAL = 3.5
P0_HET = 2.5
CHUNKS = [25.0, 50.0, 100.0, 150.0, 200.0]
WACCS = [0.03, 0.087]


def price(t, P0, rate):
    return P0 * math.exp(-rate * t)


def discount(amount_M, year, wacc):
    if wacc <= -0.999:
        return amount_M
    return amount_M / (1.0 + wacc) ** year


def wright_unit_cost(unit_index, first_unit_M, lr):
    if lr <= 0.0 or unit_index <= 1:
        return first_unit_M
    return first_unit_M * (unit_index ** (math.log(1.0 - lr) / math.log(2.0)))


def m1_params(chunk_1):
    return RT_FLOOR + RT_SLOPE * (chunk_1 / BASE_CHUNK), DELIV_FRAC * chunk_1


@dataclass
class Schedule:
    chunk_1_t: float
    reusable: bool = False
    cadence_per_yr: float = CADENCE_PER_YR
    horizon_yr: float = HORIZON_YR

    @property
    def rt1(self):
        return m1_params(self.chunk_1_t)[0]

    @property
    def deliv1(self):
        return m1_params(self.chunk_1_t)[1]


# --- schedule builders (verbatim logic from R_heterogeneous_cadence) ---
def regime_D_schedule(s):
    slot_dt = 1.0 / s.cadence_per_yr
    launches, deliveries, avail = [], [], []
    launches.append((0.0, 1, s.chunk_1_t, s.deliv1))
    if s.rt1 <= s.horizon_yr:
        deliveries.append((s.rt1, 1, s.chunk_1_t, s.deliv1))
    avail.append(float("inf") if not s.reusable else s.rt1)
    k = 1
    while True:
        t = k * slot_dt
        if t > s.horizon_yr:
            break
        if not s.reusable and t + BASE_RT > s.horizon_yr:
            break
        if s.reusable and avail:
            i = min(range(len(avail)), key=lambda j: avail[j])
            if avail[i] <= t:
                avail[i] = t + BASE_RT
                launches.append((t, i + 1, BASE_CHUNK, BASE_DELIV))
                if t + BASE_RT <= s.horizon_yr:
                    deliveries.append((t + BASE_RT, i + 1, BASE_CHUNK, BASE_DELIV))
                k += 1
                continue
        sid = len(avail) + 1
        avail.append(t + BASE_RT)
        launches.append((t, sid, BASE_CHUNK, BASE_DELIV))
        if t + BASE_RT <= s.horizon_yr:
            deliveries.append((t + BASE_RT, sid, BASE_CHUNK, BASE_DELIV))
        k += 1
    return launches, deliveries


def regime_R_schedule(s, p):
    slot_dt = 1.0 / s.cadence_per_yr
    start = s.rt1 + 0.5
    launches, deliveries, avail = [], [], []
    launches.append((0.0, 1, s.chunk_1_t, s.deliv1, 1.0))
    if s.rt1 <= s.horizon_yr:
        deliveries.append((s.rt1, 1, s.chunk_1_t, s.deliv1, 1.0))
    avail.append(float("inf") if not s.reusable else s.rt1)
    k = 0
    while True:
        t = start + k * slot_dt
        if t > s.horizon_yr:
            break
        if not s.reusable and t + BASE_RT > s.horizon_yr:
            break
        if s.reusable and len(avail) > 1:
            elig = [i for i in range(len(avail)) if avail[i] <= t]
            if elig:
                i = min(elig, key=lambda j: avail[j])
                avail[i] = t + BASE_RT
                launches.append((t, i + 1, BASE_CHUNK, BASE_DELIV, p))
                if t + BASE_RT <= s.horizon_yr:
                    deliveries.append((t + BASE_RT, i + 1, BASE_CHUNK, BASE_DELIV, p))
                k += 1
                continue
        sid = len(avail) + 1
        avail.append(t + BASE_RT)
        launches.append((t, sid, BASE_CHUNK, BASE_DELIV, p))
        if t + BASE_RT <= s.horizon_yr:
            deliveries.append((t + BASE_RT, sid, BASE_CHUNK, BASE_DELIV, p))
        k += 1
    return launches, deliveries, p


def npv_D(s, wacc, P0, rate, shift=0.0):
    """Regime-D NPV. shift>0 pulls the whole program `shift` years earlier
    (launches and deliveries), floored at year 0 — the fleet-compression lever."""
    launches, deliveries = regime_D_schedule(s)
    pv_cap, seen, n = 0.0, set(), 0
    for (t, sid, _, _) in launches:
        if sid not in seen:
            n += 1
            pv_cap -= discount(wright_unit_cost(n, FIRST_UNIT_COST_M, LR),
                               max(t - shift, 0.0), wacc)
            seen.add(sid)
    pv_rev = sum(discount(price(max(td - shift, 0.0), P0, rate) * dt,
                          max(td - shift, 0.0), wacc)
                 for (td, _, _, dt) in deliveries)
    return pv_cap + pv_rev


def npv_D_decomposed(s, wacc, P0, rate, shift=0.0):
    """Return (pv_capital, pv_revenue) separately for mechanism reporting."""
    launches, deliveries = regime_D_schedule(s)
    pv_cap, seen, n = 0.0, set(), 0
    for (t, sid, _, _) in launches:
        if sid not in seen:
            n += 1
            pv_cap -= discount(wright_unit_cost(n, FIRST_UNIT_COST_M, LR),
                               max(t - shift, 0.0), wacc)
            seen.add(sid)
    pv_rev = sum(discount(price(max(td - shift, 0.0), P0, rate) * dt,
                          max(td - shift, 0.0), wacc)
                 for (td, _, _, dt) in deliveries)
    return pv_cap, pv_rev


def npv_R(s, wacc, P0, rate, p):
    launches, deliveries, _ = regime_R_schedule(s, p)
    pv_cap, seen, n = 0.0, set(), 0
    for (t, sid, _, _, g) in launches:
        if sid not in seen:
            n += 1
            pv_cap -= g * discount(wright_unit_cost(n, FIRST_UNIT_COST_M, LR), t, wacc)
            seen.add(sid)
    pv_rev = sum(g * discount(price(td, P0, rate) * dt, td, wacc)
                 for (td, _, _, dt, g) in deliveries)
    return pv_cap + pv_rev


# closed-form Regime-D single-flight Delta (het schedule minus homogeneous baseline)
def delta_D_closed(c, P0, rate, wacc):
    rt_c, dl_c = m1_params(c)
    D = lambda t: math.exp(-rate * t) / (1.0 + wacc) ** t
    return P0 * (dl_c * D(rt_c) - BASE_DELIV * D(BASE_RT))


# ---------------------------------------------------------------------------
results = {"H1_xc": {}, "H2_decay": {}, "H3_time": {}, "H4_regimeR": {}, "grades": {}}

# --- H1: decay off reproduces het ---
base = Schedule(BASE_CHUNK)
h1_curve = {c: delta_D_closed(c, P0_HET, 0.0, 0.03) for c in CHUNKS}
# cross-check: closed form vs full-engine Delta at rate 0
full_delta_25 = npv_D(Schedule(25.0), 0.03, P0_HET, 0.0) - npv_D(base, 0.03, P0_HET, 0.0)
results["H1_xc"] = {
    "cell_alpha_closed": round(h1_curve[25.0], 1),
    "cell_alpha_full_engine": round(full_delta_25, 1),
    "chunk200_zero": round(h1_curve[200.0], 6),
    "monotonic_curve": {str(int(c)): round(h1_curve[c], 1) for c in CHUNKS},
    "het_reference": -112.7,
}

# --- H2: decay on, chunk-25 penalty vs rate; flip rate ---
h2 = {}
for tag, r in RATES.items():
    h2[tag] = round(delta_D_closed(25.0, P0_CENTRAL, r, 0.03), 1)
central_band = [delta_D_closed(25.0, p, 0.128, 0.03) for p in P0_BAND]
static_band = [delta_D_closed(25.0, p, 0.0, 0.03) for p in P0_BAND]
A = (DELIV_FRAC * 25.0) / (1.03) ** m1_params(25.0)[0]
B = BASE_DELIV / (1.03) ** BASE_RT
flip = math.log(A / B) / (m1_params(25.0)[0] - BASE_RT)
results["H2_decay"] = {
    "chunk25_delta_vs_rate_P0_3.5": h2,
    "all_negative": all(v < 0 for v in h2.values()),
    "central_penalty_band": [round(min(central_band), 1), round(max(central_band), 1)],
    "static_penalty_band": [round(min(static_band), 1), round(max(static_band), 1)],
    "narrowing_pct": [round((1 - abs(max(central_band)) / abs(min(static_band))) * 100),
                      round((1 - abs(min(central_band)) / abs(max(static_band))) * 100)],
    "flip_rate_pct_per_yr": round(flip * 100),
}

# --- H3: time vs mass. Per-mission gain (BOE) AND fleet-level compression (full engine) ---
eff = 0.128 + math.log(1.03)
full_pv_m1 = P0_CENTRAL * BASE_DELIV * math.exp(-0.128 * BASE_RT) / 1.03 ** BASE_RT
gain_1yr = full_pv_m1 * (math.exp(eff) - 1.0)          # single-mission BOE
# fleet-level: pull the WHOLE baseline program 1 yr earlier, measure NPV delta
cap0, rev0 = npv_D_decomposed(base, 0.03, P0_CENTRAL, 0.128, shift=0.0)
cap1, rev1 = npv_D_decomposed(base, 0.03, P0_CENTRAL, 0.128, shift=1.0)
fleet_compress_1yr = (cap1 + rev1) - (cap0 + rev0)
chunk25_shrink = abs(delta_D_closed(25.0, P0_CENTRAL, 0.128, 0.03))
results["H3_time"] = {
    "combined_eff_rate_pct": round(eff * 100, 1),
    "full_m1_revenue_pv_M": round(full_pv_m1, 1),
    "gain_per_year_per_mission_M": round(gain_1yr, 1),
    "fleet_compression_1yr_M": round(fleet_compress_1yr, 1),
    "compression_capex_delta_M": round(cap1 - cap0, 1),
    "compression_revenue_delta_M": round(rev1 - rev0, 1),
    "chunk25_shrink_loss_M": round(chunk25_shrink, 1),
    "fleet_compression_beats_shrink": fleet_compress_1yr > chunk25_shrink,
    "reading": "per-mission revenue-timing gain is real ($4.9M, in band) and confirms "
               "chunk-shrink is dominated -- BUT naive whole-fleet compression is "
               "NET-NEGATIVE: it un-discounts committed capex faster than it rescues "
               "already-decayed revenue. The lever is DEFERRING unneeded capex "
               "(Regime R, H4), not compressing the committed fleet.",
}

# --- H4: Regime-R advantage (stage-gate same fleet), static vs decay ---
p_succ = 0.90
# het's headline advantage: NPV_R(chunk200) - NPV_D(chunk200), rev $2.5M/t, WACC 3%, static
adv_static_het = npv_R(base, 0.03, P0_HET, 0.0, p_succ) - npv_D(base, 0.03, P0_HET, 0.0)
adv_static_p35 = npv_R(base, 0.03, P0_CENTRAL, 0.0, p_succ) - npv_D(base, 0.03, P0_CENTRAL, 0.0)
adv_decay = npv_R(base, 0.03, P0_CENTRAL, 0.128, p_succ) - npv_D(base, 0.03, P0_CENTRAL, 0.128)
results["H4_regimeR"] = {
    "advantage_static_het_P0_2.5_M": round(adv_static_het),
    "het_reference_M": 2733,
    "advantage_static_P0_3.5_M": round(adv_static_p35),
    "advantage_central_decay_P0_3.5_M": round(adv_decay),
    "stays_positive": adv_decay > 0,
    "below_static": adv_decay < adv_static_p35,
    "direction_finding": "FALSIFIED-in-direction: pre-registered to SHRINK under "
                         "decay; instead GROWS (decay destroys Regime-D's late "
                         "deliveries whose capex was already committed, so "
                         "stage-gating the fleet is MORE valuable under decay).",
}

# --- grading vs SCOPE bands ---
g = results["grades"]
g["H1"] = ("HELD" if (-130 <= h1_curve[25.0] <= -95 and abs(h1_curve[200.0]) < 1e-6
           and abs(full_delta_25 - h1_curve[25.0]) < 1.0) else "FALSIFIED")
g["H2"] = ("HELD" if (results["H2_decay"]["all_negative"]
           and -40 <= min(central_band) and max(central_band) <= -8
           and 65 <= round(flip * 100) <= 90) else "FALSIFIED")
# H3 pre-registered TEXT: per-mission gain in [$4,$10]M AND (fleet-level compression
# dwarfs the chunk-shrink). Grading-code bug-catch: v1 compared per-MISSION gain to the
# shrink; the registered claim is FLEET-level. Fixed to the registered intent.
g["H3"] = ("HELD" if (4.0 <= gain_1yr <= 10.0
           and results["H3_time"]["fleet_compression_beats_shrink"]) else "FALSIFIED")
# H4 [W]: pre-registered POSITIVE and in [+300,+2000], SHRINKING under decay.
# Advantage is positive but GROWS above static and exceeds the band -> honest
# directional falsification (kept as FALSIFIED; mechanism reported).
g["H4"] = ("HELD" if (adv_decay > 0 and 300 <= adv_decay <= 2000
           and adv_decay < adv_static_p35) else "FALSIFIED")

(RESULTS / "findings.json").write_text(json.dumps(results, indent=2))

# --- figure ---
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 4.4))

    # panel 1: Delta-NPV(chunk_1) static vs central decay (P0=3.5)
    stat = [delta_D_closed(c, P0_CENTRAL, 0.0, 0.03) for c in CHUNKS]
    dec = [delta_D_closed(c, P0_CENTRAL, 0.128, 0.03) for c in CHUNKS]
    ax1.axhline(0, color="#888", lw=1)
    ax1.plot(CHUNKS, stat, "o-", color="#c44", label="static price")
    ax1.plot(CHUNKS, dec, "s-", color="#268", label="decaying 12.8%/yr")
    ax1.set_xlabel("mission-1 chunk (t)"); ax1.set_ylabel("Δ-NPV het−hom ($M)")
    ax1.set_title("Chunk-shrink still loses;\ndecay collapses the penalty"); ax1.legend()

    # panel 2: chunk-25 penalty vs decay rate, flip point
    rr = [i / 100 for i in range(0, 90)]
    pen = [delta_D_closed(25.0, P0_CENTRAL, r, 0.03) for r in rr]
    ax2.axhline(0, color="#888", lw=1)
    ax2.plot([r * 100 for r in rr], pen, "-", color="#268")
    for r, tag in ((9.2, "cons"), (12.8, "central"), (17.7, "median"), (32.4, "bull")):
        ax2.axvline(r, color="#bbb", ls=":", lw=1)
        ax2.text(r, min(pen) * 0.9, tag, rotation=90, va="bottom", fontsize=7)
    ax2.axvline(flip * 100, color="#c44", ls="--", lw=1.2)
    ax2.text(flip * 100, 0, f"  break-even\n  {flip*100:.0f}%/yr", color="#c44", fontsize=8, va="top")
    ax2.set_xlabel("price-decline rate (%/yr)"); ax2.set_ylabel("chunk-25 Δ-NPV ($M)")
    ax2.set_title("Break-even needs ~76%/yr —\nfar above any anchored rate")

    # panel 3: Regime-R advantage static vs decay
    labels = ["static\n$2.5/t (het)", "static\n$3.5/t", "central decay\n$3.5/t"]
    vals = [adv_static_het, adv_static_p35, adv_decay]
    ax3.bar(labels, vals, color=["#c9a", "#c44", "#268"])
    ax3.axhline(0, color="#888", lw=1)
    for i, v in enumerate(vals):
        ax3.text(i, v, f"${v:,.0f}M", ha="center", va="bottom", fontsize=8)
    ax3.set_ylabel("Regime-R advantage ($M)")
    ax3.set_title("Stage-gating wins bigger under decay\n(H4 [W] falsified-in-direction)")

    fig.tight_layout()
    fig.savefig(RESULTS / "fast_first_decay.png", dpi=150)
    print("figure -> results/fast_first_decay.png")
except Exception as e:  # pragma: no cover
    print(f"figure skipped: {e}")

# --- console summary ---
print(json.dumps(results, indent=2))
print("\nGRADES:", results["grades"])
