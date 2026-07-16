"""R-water-electrothermal-flight-scale-audit — run.py (bet #2)

Three deterministic computations:

  1. MET branch — continuous-flight effective Isp (anchored on R0 frozen-flow,
     NOT the 800 s ground/pulse anchor) mapped to matrix closure rate via the
     locked A1 closure sensitivity (0% @600 s, 0.5% @700 s, 4% @800 s,
     12% @900 s at the 30 t floor). Answers H1/H2.

  2. RF-ion branch — the Isp-sufficient (2000 s) but contamination-SENSITIVE
     architecture. Continuous-months flight-readiness as a conjunction of
     three reliability factors anchored on R11 (bag silicate rejection) and
     R-MET-cathode-escape-hatch (cathode/grid life). Answers H3.

  3. Flight gap — cumulative-operating-time ratio between ICEBERG's
     continuous-months inbound burn and the closest flown precedent
     (Vigoride-5 pulse firings; AQUARIUS deep-space resistojet). Answers H4.

Anchors documented in inputs/flight_heritage.csv and SCOPE.md. No randomness.
"""

import json
import pathlib

HERE = pathlib.Path(__file__).parent
RESULTS = HERE / "results"
RESULTS.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# Locked A1 closure sensitivity (R-power-wonder; 30 t floor). Isp (s) -> % of
# feasible paths that close. Piecewise-linear; flat 0 below 600 s.
# ---------------------------------------------------------------------------
CLOSURE_POINTS = [(600, 0.0), (700, 0.5), (800, 4.0), (900, 12.0)]


def closure_rate_pct(isp_s):
    if isp_s <= CLOSURE_POINTS[0][0]:
        return 0.0
    if isp_s >= CLOSURE_POINTS[-1][0]:
        # linear extrapolation on the last segment slope
        (x0, y0), (x1, y1) = CLOSURE_POINTS[-2], CLOSURE_POINTS[-1]
        return y1 + (isp_s - x1) * (y1 - y0) / (x1 - x0)
    for (x0, y0), (x1, y1) in zip(CLOSURE_POINTS, CLOSURE_POINTS[1:]):
        if x0 <= isp_s <= x1:
            return y0 + (isp_s - x0) * (y1 - y0) / (x1 - x0)
    return 0.0


# ---------------------------------------------------------------------------
# 1. MET branch — continuous-flight effective Isp (R0-anchored)
# ---------------------------------------------------------------------------
# R0 frozen-flow: realistic continuous water-MET ~480-650 s; equilibrium
# ceiling ~700-750 s. The 800 s A1 anchor is a ground/clean/~50 s-pulse figure
# ABOVE this continuous ceiling. Continuous-flight bracket:
MET_ISP = {"low": 500, "mid": 575, "high": 700}   # s, continuous-flight on Saturn water
MET_GROUND_PULSE_ANCHOR = 800                       # s, A1 ground/clean/pulse figure


def met_branch():
    out = {"ground_pulse_anchor_s": MET_GROUND_PULSE_ANCHOR,
           "ground_pulse_closure_pct": round(closure_rate_pct(MET_GROUND_PULSE_ANCHOR), 2),
           "continuous_flight": {}}
    for k, isp in MET_ISP.items():
        out["continuous_flight"][k] = {"isp_s": isp,
                                       "closure_pct": round(closure_rate_pct(isp), 3)}
    return out


# ---------------------------------------------------------------------------
# 2. RF-ion branch — continuous-months flight-readiness conjunction
# ---------------------------------------------------------------------------
# RF-ion (Pale Blue class) at 2000 s CLOSES on Isp (matrix uses it). The bet is
# whether its continuous-months operation on Saturn water holds. Three factors:
#   p_bag      = P(bag sublimation-distillation silicate rejection holds over the
#                multi-year burn). R11: negligible grid wear under nominal bag op;
#                18 months to grid failure if bag thermal control fails. So this
#                tracks bag-thermal-control reliability over years.
#   p_cathode  = P(cathode/grid life >= multi-year burn). R-MET-cathode-escape-hatch:
#                RF-ion needs cathode swaps under Wang-pessimistic 3000 hr life;
#                Dawn <=1% per-swap; grid life >7 yr nominal.
#   p_no_anom  = P(no continuous-operation anomaly over months). Vigoride flight
#                heritage is PULSES on clean water; V-3 had difficulties.
RFION_FACTORS = {
    "p_bag":      {"low": 0.65, "mid": 0.80, "high": 0.90},
    "p_cathode":  {"low": 0.65, "mid": 0.80, "high": 0.92},
    "p_no_anom":  {"low": 0.60, "mid": 0.75, "high": 0.88},
}


def rfion_branch():
    # At 2000 s RF-ion CLOSES on Isp per the matrix / mission_graph cells that
    # already use it (governed by the bet #1 / #3 audits, not the MET closure
    # curve). The MET closure-sensitivity curve is only defined 600-900 s and
    # must NOT be extrapolated to 2000 s. The bet here is flight-readiness.
    out = {"isp_s": 2000, "isp_closes_matrix": True,
           "note": "closes on Isp per matrix cells; bet is continuous-flight readiness, not Isp",
           "joint_flight_readiness": {}, "factors": RFION_FACTORS}
    for bracket in ("low", "mid", "high"):
        j = 1.0
        for f in RFION_FACTORS.values():
            j *= f[bracket]
        out["joint_flight_readiness"][bracket] = round(j, 3)
    return out


# ---------------------------------------------------------------------------
# 3. Flight gap — cumulative-operating-time ratio
# ---------------------------------------------------------------------------
# ICEBERG inbound continuous burn (titan-3 / mission_graph): ~2-7 yr continuous
# thrust-on. Use a conservative LOW end of "continuous months" = 6 months and a
# representative mission burn = 5 yr. Flown precedent cumulative thrust-on:
# Vigoride-5 35 pulse firings of varying durations ~ tens of hours; AQUARIUS
# deep-space resistojet ~ tens of hours. Use 30 hr as the flown anchor.
FLOWN_PRECEDENT_HR = 30.0
ICEBERG_BURN_HR = {"continuous_6mo": 6 * 30 * 24, "mission_5yr": 5 * 365.25 * 24}


def flight_gap():
    return {"flown_precedent_hr": FLOWN_PRECEDENT_HR,
            "iceberg_burn_hr": ICEBERG_BURN_HR,
            "gap_ratio": {k: round(v / FLOWN_PRECEDENT_HR) for k, v in ICEBERG_BURN_HR.items()}}


def main():
    met = met_branch()
    rf = rfion_branch()
    gap = flight_gap()

    summary = {
        "round": "R-water-electrothermal-flight-scale-audit", "worker": "hyperion",
        "date": "2026-05-22", "bet": "#2 of three engineering bets",
        "closure_sensitivity_30t_floor": CLOSURE_POINTS,
        "met_branch": met, "rfion_branch": rf, "flight_gap": gap,
    }
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2))

    print("=" * 74)
    print("R-water-electrothermal-flight-scale-audit  (bet #2)")
    print("=" * 74)
    print("\n[1] MET branch (contamination-tolerant; R0-anchored continuous Isp)")
    print(f"    ground/clean/pulse anchor 800 s -> closure {met['ground_pulse_closure_pct']}%")
    for k in ("low", "mid", "high"):
        c = met["continuous_flight"][k]
        print(f"    continuous-flight {k:<4} {c['isp_s']} s -> closure {c['closure_pct']}%")
    print("    => MET continuous-flight Isp on Saturn water does NOT reach matrix-closing Isp")

    print("\n[2] RF-ion branch (Isp-sufficient at 2000 s; closes matrix on Isp IF flight-ready)")
    for k in ("low", "mid", "high"):
        print(f"    continuous-months flight-readiness {k:<4} = {rf['joint_flight_readiness'][k]}")
    print("    => closes on Isp but continuous-months-on-Saturn-water is the unproven conjunction")

    print("\n[3] Flight gap (cumulative operating time)")
    print(f"    flown precedent ~{gap['flown_precedent_hr']:.0f} hr (Vigoride pulses / AQUARIUS)")
    for k, r in gap["gap_ratio"].items():
        print(f"    vs ICEBERG {k}: {r}x")
    print(f"\nWrote {RESULTS}/summary.json")


if __name__ == "__main__":
    main()
