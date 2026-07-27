#!/usr/bin/env python3
"""Pre-script: R-fast-first-chunk-decaying-price bounds.

Re-tests the project-owner USER-NOTES hypothesis (design-axes/02, lines 18-20):
    "mission 1 is return a chunk, any size chunk, as fast as possible, using
     water as the propellant ... but then subsequent vehicles can take longer
     round trips, which would eventually get us into the green right?"

`R_heterogeneous_cadence` (rhea, 2026-05-15) already tested this and FALSIFIED it
in three senses -- BUT under a STATIC clearing price, and its own SCOPE explicitly
deferred "time-evolution of clearing price." R188 `R_clearing_price_time_path` has
since anchored that decay to the launch experience curve (~12.8%/yr central). This
round folds R188's decaying price into het_cadence's exact engine and asks the one
new question: does front-loading revenue (fast small mission 1, delivering EARLY
into a HIGHER price) revive the case that a static price killed?

Isolation of variables (the control): this round changes EXACTLY ONE thing vs
het_cadence -- the clearing price is now time-decaying. Vehicle parametric, cadence,
Wright's law, NRE, WACC grid are all held at het_cadence's values, so any verdict
change is attributable to the decay alone. The 500-kWe Variant B vehicle is RETIRED
(no-large-fission); absolute NPV levels are NOT the claim -- the SCHEDULE-SHAPE delta
under decay is. The matrix already settles absolute viability.

Key derived identity (verified against het_cadence cell alpha = -$112.7M exactly):
in Regime D single-flight, missions 2..N are identical between the het schedule
(chunk_1<200) and the homogeneous baseline (chunk_1=200) -- same slots, same ships,
same build costs. So the entire Regime-D Delta-NPV is the mission-1 delivery term:

    Delta_NPV(c) = P0 * [ deliv(c)*D(rt(c)) - 80*D(14.5) ]
    D(t) = exp(-rate*t) / (1+wacc)**t          # decay AND wacc discount
    deliv(c) = 0.40*c ;  rt(c) = 11.5 + 3.0*(c/200)

Grids here SPAN the run grids (R182 lesson): chunk_1 in {25..200}, rate in
{0, 0.092, 0.128, 0.177, 0.324}, WACC in {0.03, 0.087}, P0 in {2.5, 3.0, 3.5, 4.0}.
"""
import math

# --- vehicle parametric (pinned to het_cadence) ---
BASE_CHUNK, BASE_RT, BASE_DELIV = 200.0, 14.5, 80.0
DELIV_FRAC = BASE_DELIV / BASE_CHUNK      # 0.40
RT_FLOOR, RT_SLOPE = 11.5, 3.0            # rt(c) = 11.5 + 3.0*(c/200)
CHUNKS = [25.0, 50.0, 100.0, 150.0, 200.0]

# --- price anchors (R188) ---
P0_HET = 2.5           # $M/tonne = $2,500/kg : het_cadence headline (decay-off XC)
P0_BAND = (3.0, 3.5, 4.0)   # $M/t : R188 LEO 2025 band $3,000-4,000/kg, central 3,500
RATE_CONS, RATE_CENTRAL, RATE_MED, RATE_BULL = 0.092, 0.128, 0.177, 0.324  # R188 H2
WACC_SOV, WACC_GROWTH = 0.03, 0.087

def rt(c):     return RT_FLOOR + RT_SLOPE * (c / BASE_CHUNK)
def deliv(c):  return DELIV_FRAC * c
def D(t, rate, wacc):  return math.exp(-rate * t) / (1.0 + wacc) ** t

def delta_npv_D(c, P0, rate, wacc):
    """Regime-D single-flight Delta-NPV (het schedule minus homogeneous baseline)."""
    return P0 * (deliv(c) * D(rt(c), rate, wacc) - BASE_DELIV * D(BASE_RT, rate, wacc))

print("=" * 72)
print("H1 [XC] -- decay OFF reproduces het_cadence exactly")
print("=" * 72)
# het cell alpha: Regime D, chunk_1=25, WACC 3%, LR 15%, $2.5M/t rev -> -$112.7M
a = delta_npv_D(25.0, P0_HET, 0.0, WACC_SOV)
print(f"  Delta-NPV(chunk_1=25, rate=0, P0=2.5, WACC 3%) = ${a:7.1f}M "
      f"(het cell alpha -$112.7M; XC band [-130,-95])")
print(f"  Delta-NPV(chunk_1=200, rate=0)                 = "
      f"${delta_npv_D(200.0, P0_HET, 0.0, WACC_SOV):7.1f}M (must be 0.0 exactly)")
print("  monotonic in chunk_1 (rate=0, P0=2.5, WACC 3%):")
for c in CHUNKS:
    print(f"    chunk {c:5.0f} t -> Delta ${delta_npv_D(c,P0_HET,0.0,WACC_SOV):8.1f}M")

print()
print("=" * 72)
print("H2 [S] -- decay ON: chunk-shrink STILL loses at every anchored rate,")
print("         but the penalty COLLAPSES (front-load nearly offsets mass loss)")
print("=" * 72)
print("  Delta-NPV(chunk_1=25) vs rate, at P0=3.5 central, WACC 3%:")
for r, tag in ((0.0,"static"),(RATE_CONS,"cons"),(RATE_CENTRAL,"central"),
               (RATE_MED,"median"),(RATE_BULL,"bull")):
    d = delta_npv_D(25.0, 3.5, r, WACC_SOV)
    print(f"    rate {r*100:5.1f}%/yr ({tag:>7}): Delta ${d:8.1f}M  "
          f"{'LOSES' if d<0 else 'FLIPS +'}")
# central-rate collapse band across the P0 band:
lo = min(delta_npv_D(25.0, p, RATE_CENTRAL, WACC_SOV) for p in P0_BAND)
hi = max(delta_npv_D(25.0, p, RATE_CENTRAL, WACC_SOV) for p in P0_BAND)
stat_lo = min(delta_npv_D(25.0, p, 0.0, WACC_SOV) for p in P0_BAND)
print(f"  central-decay chunk-25 penalty across P0 {P0_BAND}: "
      f"[${lo:.1f}, ${hi:.1f}]M  (SCOPE band [-40, -8]M)")
print(f"  static-price chunk-25 penalty across P0 band: [${stat_lo:.1f}, "
      f"${max(delta_npv_D(25.0,p,0.0,WACC_SOV) for p in P0_BAND):.1f}]M "
      f"-> decay narrows it by {(1-abs(hi)/abs(stat_lo))*100:.0f}-"
      f"{(1-abs(lo)/abs(min(delta_npv_D(25.0,p,0.0,WACC_SOV) for p in P0_BAND)))*100:.0f}%")

# flip rate: solve deliv(25)*exp(-r*rt(25))/1.03^rt = 80*exp(-r*14.5)/1.03^14.5
# P0 and wacc cancel in the ratio -> pure decay threshold
def flip_rate(c, wacc):
    # term_het(r) = term_hom(r) ; both scale with P0 so P0 cancels
    # deliv(c)/(1+w)^rt(c) * e^{-r rt(c)} = 80/(1+w)^14.5 * e^{-r 14.5}
    A = deliv(c) / (1+wacc)**rt(c)
    B = BASE_DELIV / (1+wacc)**BASE_RT
    # A e^{-r rt} = B e^{-r RT}  -> ln(A/B) = r(rt - RT) -> r = ln(A/B)/(rt-RT)
    return math.log(A/B) / (rt(c) - BASE_RT)
fr = flip_rate(25.0, WACC_SOV)
print(f"  decay rate at which chunk-25 shrink BREAKS EVEN: {fr*100:.0f}%/yr "
      f"(>> bull 32.4%; SCOPE: flip rate in [65, 90]%/yr -> robust-falsified)")

print()
print("=" * 72)
print("H3 [S] -- TIME dominates MASS under decay: 1 yr of whole-schedule")
print("         compression outvalues the entire chunk-shrink front-load")
print("=" * 72)
# combined effective rate = decay + wacc-log ; per-year PV gain of pulling the
# full 80t mission-1 delivery 1 yr earlier
eff = RATE_CENTRAL + math.log(1+WACC_SOV)
full_pv = 3.5 * BASE_DELIV * D(BASE_RT, RATE_CENTRAL, WACC_SOV)
gain_1yr = full_pv * (math.exp(eff) - 1.0)
shrink_benefit = abs(delta_npv_D(25.0, 3.5, RATE_CENTRAL, WACC_SOV))
print(f"  combined effective discount (decay+wacc): {eff*100:.1f}%/yr")
print(f"  full mission-1 revenue PV (P0=3.5, central, WACC 3%): ${full_pv:.1f}M")
print(f"  value of pulling it 1 yr earlier: ${gain_1yr:.1f}M/mission  "
      f"(SCOPE band [$4,$10]M across P0 3.0-4.0 x rate cons-median)")
print(f"  ... vs the ENTIRE chunk-25 front-load net effect: ${-shrink_benefit:.1f}M "
      f"(negative -- shrinking is a strictly dominated micro-optimization)")
print(f"  fleet of ~28 deliveries: 1-yr compression ~ 28x per-mission gain, "
      f"orders of magnitude above the single-mission chunk-shrink move")

print()
print("=" * 72)
print("H4 [W] -- Regime R (stage-gate the SAME fleet on mission-1 success):")
print("         het's static +$2.7B advantage SHRINKS under decay (deferred")
print("         revenue now decays) but is pre-registered to stay POSITIVE")
print("=" * 72)
print("  het_cadence Regime R (static, chunk_1=200, WACC 3%): +$2,733M")
print("  mechanism under decay: deferring missions 2..N past mission-1 success")
print("  (~+rt1 yr) still DEFERS CAPEX (good) but now also decays deferred")
print("  REVENUE harder. Net advantage pre-registered POSITIVE but reduced.")
print("  SCOPE band: Regime-R advantage at chunk_1=200 under central decay in")
print("  [+$300M, +$2,000M] (positive, below the static +$2.7B). run.py measures.")
print("  Falsified if it goes negative or exceeds the static value.")
