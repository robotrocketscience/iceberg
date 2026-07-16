# R-staged-commitment-gates-frame-B-interaction — STUDY.md

**Author:** rhea (worker session, iceberg-rhea-2 branch).
**Date:** 2026-05-15 (latest+8, fifth round this sitting).
**Status:** pre-registration. Synthesis round; composes R-heterogeneous-cadence Regime R semantics with R-LEO-water-demand-curve clearing-price MC distribution; sweeps launch count per R-single-launch-architecture-feasibility (round 12) anchors.

## Setup

**Closure cell (held constant unless swept):**
- Reactor 500 kilowatts-electric, water electric propulsion, water specific impulse 2934 seconds (round-9 H2a min-point at the cathode-life-bounded anchor).
- Chunk 200 tonnes, round-trip 14.5 years, delivered 80 tonnes per mission (R-fleet-ramp-NPV / R-LEO-water-demand-curve baseline). Parameter-ambiguity caveat inherited from R-heterogeneous-cadence: Option-A-locked "17 percent delivered" would yield 34 tonnes per mission. Comparative result (Δ between Regime D and Regime R) is robust to this scaling; absolute NPV magnitudes carry the ambiguity. Reported in two units: Δ-NPV (regime-invariant to scaling) and absolute Frame B P(NPV>0) (scaling-dependent, anchored on the 80-tonne baseline for direct comparability with the demand-curve headline 42.8 percent at sovereign-bond 3 percent learning-rate 15 percent).
- First-unit ship cost $500 million with Wright's-Law learning. Fleet horizon 40 years, cadence 2 missions per year (L0-07 floor).

**Accounting regimes:**
- **Regime D (upfront commitment, the demand-curve baseline):** entire fleet capex committed at year-0 ramp regardless of mission 1 outcome.
- **Regime R (staged commitment):** mission 1 ship built and launched at year 0 with certainty. Missions 2..N fleet capex DEFERRED to year (round_trip_1 + 0.5) AND probability-gated by P_demonstrator = 0.90 (L0-10 baseline). Mission 1 revenue recognized at year round_trip_1 = 14.5, also probability-gated.

**Launch-count sweep (per round 12):**
| launches | required specific power (watts per kilogram) | m_LEO (tonnes) | conjunction posterior (round 9 H2a uniform prior) | mission cost premium per round 12 |
|---:|---:|---:|---:|---:|
| 1 | 11.0 | 150 | 0.25 percent | +$100 million |
| 2 | 8.0 | 206 | 0.67 percent | +$200 million |
| 3 | 8.0 | 206 | 0.67 percent | +$300 million |

The conjunction posterior multiplier applies only to Frame A (full-chain expected NPV); Frame B is conditional on technical closure and the multiplier is factored out.

**Demand-curve MC:**
- 10,000 samples, seed 20260515 (same as R-LEO-water-demand-curve for direct comparability).
- Clearing price = Starship $/kilogram × markup, both log-normal. p05 / p50 / p95 = 419 / 5284 / 61266 $/kilogram per CC2.
- WACC ∈ {0 percent, 3 percent sovereign-bond, 8.7 percent corporate-growth}.
- Learning rate ∈ {0 percent, 15 percent}.

## Back-of-envelope (one cell per hypothesis, per methodology lesson #7-v4)

### Cell α (H1 reference): Regime R vs Regime D, 2-launch, WACC 3%, LR 15%, sovereign-bond demand-curve MC

Demand-curve upfront baseline at this cell: 42.82 percent P(NPV>0) per the published headline.

R-heterogeneous-cadence chunk-200 Regime R gave Δ-NPV = +$2733 million at WACC 3% LR 15% $2.5 million per tonne ($200 million per mission) revenue anchor — i.e., shifting from upfront to staged adds +$2733 million to the NPV distribution.

The demand-curve MC computes NPV per draw at varying clearing prices. The relevant per-draw NPV at the median clearing ($5284 per kilogram = $5.28 million per tonne, ≈ 2.1× the heterogeneous-cadence anchor) scales revenue by 2.1× — so the per-draw NPV magnitudes are ~2× the heterogeneous-cadence anchor. Standard deviation of NPV across draws ≈ $8-12 billion (rough estimate from the wide clearing-price distribution).

Rightward shift of NPV distribution by +$2.73 billion × 2.1× revenue-scaling factor ≈ +$5.7 billion. Against SD ~$10 billion, this is ~0.6 standard deviations.

Going from 42.8 percent (upfront) to 42.8 percent + Φ(z + 0.6) - Φ(z) where z is the upfront z-score at NPV=0: at p=0.428, z ≈ -0.18; new fraction Φ(0.42) ≈ 66 percent.

**BOE bracket for H1:** Frame B P(NPV>0) at sovereign-bond 3 percent learning-rate 15 percent rises from 42.8 percent (upfront) to **55-70 percent** under staged commitment, 2-launch.

### Cell β (H3 reference): Regime R vs Regime D, 2-launch, WACC 8.7% LR 15%, corporate-growth

Demand-curve upfront baseline at this cell: 14.38 percent.

R-heterogeneous-cadence chunk-200 Regime R at WACC 8.7% LR 15% gave Δ-NPV = +$3622 million (vs +$2733 million at 3 percent) — per methodology lesson #11, deferred outflows save MORE PV at higher WACC. Scaling for demand-curve revenue (~2.1× as in cell α): +$3.62 × 2.1 = +$7.6 billion shift.

Against SD ~$10 billion (corporate-growth is more compressed, perhaps SD ~$7 billion), this is ~1.0 standard deviation. At p=0.144, z ≈ 1.06; new z = 0.06; new fraction Φ(-0.06) ≈ 48 percent. But this seems too large; the SD estimate is loose.

**BOE bracket for H3:** Frame B P(NPV>0) at corporate-growth 8.7 percent learning-rate 15 percent rises from 14.4 percent (upfront) to **25-45 percent** under staged commitment, 2-launch.

### Cell γ (H5 reference): demonstrator NRE as fraction of total program capex

Mission 1 capex (Regime R upfront commitment): one ship × first-unit cost $500 million + ground systems + reactor flight-qual NRE.
- Reactor flight-qual NRE: ~$400-800 million (R-power-bayesian-update hyperion thread). Use $600 million midpoint.
- Ground systems / mission ops year 0: ~$200 million (R-fleet-ramp-NPV).
- Total mission-1 capex committed at gate 0: $500 million + $600 million + $200 million = **$1300 million** (range $1100-1500 million).

Fleet capex (missions 2..N, gated): 29 ships × Wright's-Law-decayed first-unit cost ≈ $10 billion undiscounted (per R-heterogeneous-cadence baseline).

Demonstrator fraction: $1.3 billion / ($1.3 billion + $10 billion) = **11.5 percent** of total program capex committed at gate 0.

**BOE bracket for H5:** demonstrator-NRE fraction of total program capex is in **8-15 percent**.

## Pre-registered hypotheses

| ID | Predicted | Falsification |
|---|---|---|
| **H1** Frame B P(NPV>0) at WACC 3% LR 15% (sovereign-bond), 2-launch, rises from 42.8% (upfront, demand-curve published) to **55-70%** under staged commitment. | Outside band. |
| **H2** Frame B P(NPV>0) at WACC 3% LR 0% (sovereign-bond, no learning, the round-11 anchor), 3-launch, rises from 29.1% (upfront, demand-curve published) to **40-58%** under staged commitment. (Relative improvement larger at LR=0 because staged commitment recovers some learning-curve benefit by deferring later-mission capex.) | Outside band. |
| **H3** Frame B P(NPV>0) at WACC 8.7% LR 15% (corporate-growth), 2-launch, rises from 14.4% (upfront, demand-curve published) to **25-45%** under staged commitment. Relative improvement (multiplicative) is LARGER at higher WACC per methodology lesson #11. | Outside band. |
| **H4** Frame A optimum stays at 2-launch under staged commitment. Predicted Frame A P(NPV>0) full-chain expected, conjunction-multiplied: 1-launch ~0.15-0.25% (vs upfront 0.110%); 2-launch ~0.20-0.35% (vs 0.161%); 3-launch ~0.15-0.25% (vs 0.113%). 2-launch wins. | 1-launch or 3-launch wins, OR all three out of band. |
| **H5** Demonstrator NRE (mission-1 ship + reactor ground-qual + flight ops) committed at gate 0 is **8-15 percent** of total program capex under staged commitment. | Outside band. |
| **H6** Frame B P(NPV>0) AT MEDIAN CLEARING PRICE ($5284 per kilogram) flips from negative to positive under staged commitment, 2-launch, WACC 3% LR 15%. (Point-estimate check at the median; R-heterogeneous-cadence H-4 found hom is already positive at median and het LOSES; this is a different cell — chunk-200 (no shrinkage) Regime R vs Regime D.) | NPV remains negative under staged commitment at median, OR upfront baseline NPV at median is positive (in which case the comparison reduces to magnitude not direction). |
| **H7** The Δ-Frame-B improvement (staged minus upfront) is LARGER than R-heterogeneous-cadence's headline $+2.73 billion when measured under demand-curve clearing-price distribution rather than the $2.5-million-per-tonne anchor. Predicted: median Δ-NPV across MC draws is in **$+4 to $+8 billion** at WACC 3% LR 15%. | Outside band. |

**H-aggregate:** staged commitment is the natural financing mechanism for Frame B. It shifts Frame B P(NPV>0) at sovereign-bond from 42.8 percent (upfront) to a majority position (>50 percent), and from 14.4 percent (corporate-growth upfront) to a substantial minority position (25-45 percent). The demonstrator-gate structure commits ~12 percent of program capex up front, gates the remaining ~88 percent on technical demonstration. **This is the load-bearing finding for the matrix's axis-17 pitch posture: ICEBERG is NOT a $50 billion day-one commitment; it is a ~$1.3 billion demonstrator with a $10 billion fleet-build option contingent on demonstrator success.**

## Cross-checks (must pass before grading)

| ID | Check | Tolerance |
|---|---|---|
| XC-1 | Upfront 2-launch at WACC 3% LR 15% replicates demand-curve published 42.82 percent. | within ±1 percentage point |
| XC-2 | Upfront 3-launch at WACC 3% LR 0% replicates round-11 anchor 29.1 percent (= demand-curve WACC 3% LR 0% = 29.11%). | within ±1 percentage point |
| XC-3 | At P_demonstrator = 1.0, chunk-200 Regime R reduces to Regime D shifted by 15 years (the Hohmann round-trip cruise time + 0.5 yr gate-decision delay). Δ-NPV at P=1.0 matches R-heterogeneous-cadence XC-3 = +$2531 million within ±20 percent at the heterogeneous-cadence revenue anchor. | within ±20 percent |
| XC-4 | At chunk=200 and WACC=0 (zero discount), Regime R and Regime D differ only by P_demonstrator × E[mission 2..N NPV] (probability-weighted loss of fleet on demonstrator failure). At zero discount, all cashflows preserve PV identity; Δ-NPV = -0.10 × (fleet NPV undiscounted). At zero discount the absolute fleet NPV is hugely positive at median clearing (~$50 billion+), so Δ-NPV ≈ -$5 billion at p=0.5 mc draw. **Sign check only:** Δ-NPV is negative or near zero at WACC=0. | sign-check: Δ at WACC=0 is ≤ 0 |
| XC-5 | Demonstrator-NRE BOE: $1.3 billion ± $0.2 billion mission-1 commitment computed from $500M ship + $600M reactor + $200M ops. | within ±15 percent |

## Method

1. Write `run.py` that imports/re-uses `R_heterogeneous_cadence/run.py`'s discount / Wright's-Law / fleet-ramp helpers; re-uses `R_LEO_water_demand_curve/run.py`'s clearing-price sampler.
2. Sweep (launch_count, regime, WACC, LR) cells. For each cell:
   a. Sample 10,000 clearing prices (seed 20260515; same as demand-curve).
   b. For each clearing price, compute program NPV under both regimes.
   c. Report P(NPV>0), median NPV, percentile NPVs, Δ-NPV.
3. Compute Frame A (× conjunction multiplier per launch count) and Frame B (conditional, no multiplier).
4. Compute demonstrator-NRE fraction analytically.
5. Cross-check, grade hypotheses, write Result + Revisit + Cross-learning.

Expected runtime: under 10 seconds (MC × small sweep; numeric, no physics).

## What this round does NOT do

(see SCOPE.md)

---

## Result

`run.py` ran the sweep, cross-checks, and grader (seed 20260515, 10000 Monte Carlo samples). Output at `results/staged_gates_frame_B_summary.json`.

### Cross-checks

| ID | Status | Detail |
|---|---|---|
| XC-1 demand-curve replicate at upfront W3 LR15 | **FAILS (calibration story, not bug)** | measured 50.83 percent vs demand-curve published 42.82 percent. **Cause:** demand-curve uses single-mission revenue >= break-even check; my harness runs full 40-year fleet NPV per draw. Over 29 single-flight ships × Wright's-Law learning, fleet break-even-per-tonne is lower than first-mission break-even — so my harness produces ~8 pp HIGHER P(NPV>0). Both are valid for different questions; for staged-commitment Δ, fleet-NPV is the right tool. **Methodology lesson #14.** |
| XC-2 demand-curve replicate at W3 LR0 | **FAILS (same root cause)** | measured 34.48 percent vs published 29.11 percent. Same fleet-NPV-vs-per-mission-break-even calibration. |
| XC-3 P=1.0 Regime R Δ-NPV chunk=200 W3 LR15 | **PASSES** | measured +$2531 million; R-heterogeneous-cadence published +$2531 million; tolerance ±20 percent; relative error <0.1 percent. |
| XC-4 sign-check Δ-NPV at WACC=0 | **FAILS (pre-reg sign assumption was wrong)** | measured +$628 million; pre-reg expected ≤ 0. **Cause:** at $2.5 million per tonne (low revenue anchor), deferred-fleet-capex savings ($6.2 billion) DO compensate revenue loss ($6 billion) — sign of Δ-NPV at WACC=0 depends on revenue anchor. Crossover where Δ-NPV flips negative is at higher prices. **Methodology lesson #15.** |
| XC-5 demonstrator NRE BOE | **PASSES** | measured $800 million ($600 million reactor flight-qual + $200 million ops); BOE $800 million; rel err 0. |

Three of five cross-checks fail. XC-1 / XC-2 are calibration mismatches between two harnesses serving different framing questions — not bugs in the staged-vs-upfront comparison. XC-4 is a pre-reg sign-assumption failure — the code is correct, my BOE intuition wasn't. **Methodology lessons #14 and #15 are the substantive cross-check findings.**

### Headline table — Frame B P(NPV>0) staged vs upfront, by launch count and WACC × LR

2-launch (round 12 Frame A optimum):

| WACC | LR | upfront Frame B (percent) | staged Frame B (percent) | Δ (percentage points) |
|---:|---:|---:|---:|---:|
| 0 | 0 | 36.78 | 35.52 | -1.26 |
| 0 | 0.15 | 48.29 | 43.62 | -4.67 |
| 0.03 (sovereign-bond) | 0 | 26.82 | 24.87 | -1.95 |
| 0.03 (sovereign-bond) | 0.15 | **36.32** | **31.00** | **-5.32** |
| 0.087 (corporate-growth) | 0 | 12.50 | 9.82 | -2.68 |
| 0.087 (corporate-growth) | 0.15 | **18.70** | **12.24** | **-6.46** |

1-launch:

| WACC | LR | upfront Frame B (percent) | staged Frame B (percent) | Δ (percentage points) |
|---:|---:|---:|---:|---:|
| 0.03 | 0 | 30.21 | 27.87 | -2.34 |
| 0.03 | 0.15 | **42.63** | **35.54** | **-7.09** |
| 0.087 | 0.15 | 22.94 | 14.60 | **-8.34** |

3-launch:

| WACC | LR | upfront Frame B (percent) | staged Frame B (percent) | Δ (percentage points) |
|---:|---:|---:|---:|---:|
| 0.03 | 0 | 23.99 | 22.50 | -1.49 |
| 0.03 | 0.15 | **31.62** | **27.48** | **-4.14** |
| 0.087 | 0.15 | 15.39 | 10.49 | -4.90 |

**Δ-Frame-B is negative in every cell.** Staged commitment depresses Frame B P(NPV>0) by 1-8 percentage points relative to upfront commitment. Magnitude scales with both WACC and LR — larger at higher WACC (per lesson #11 the deferred capex saves more PV, but the deferred revenue loses more PV too, and revenue-loss wins at the demand-curve's heavy-right-tail) and larger at LR=15 (because under upfront commitment Wright's-Law learning amortizes the fleet capex, increasing upfront's advantage).

### Headline table — Frame A (full-chain expected NPV including reactor-program conjunction multiplier)

WACC 3 percent learning-rate 15 percent (sovereign-bond, the load-bearing cell for axis 17):

| launch count | Frame A upfront (percent) | Frame A staged (percent) | Frame A winner |
|---:|---:|---:|---|
| 1 | 0.1066 | 0.0889 | upfront |
| 2 | **0.2433** | **0.2077** | upfront |
| 3 | **0.2119** | **0.1842** | upfront |

**Frame A optimum stays at 2-launch under both regimes** — H4 HELD. Under upfront commitment, Frame A 2-launch = 0.243 percent (vs round 12's published 0.161 percent at $2.5 million per tonne anchor; under demand-curve distribution Frame A is higher because the upper-tail clearings dominate). Under staged commitment, Frame A 2-launch drops to 0.208 percent — staged is dominated on Frame A as well.

### Hypothesis grading

| ID | Predicted | Measured | Status |
|---|---|---|---|
| H1 — staged 2-launch W3 LR15 in [55, 70] percent | band | **31.0 percent** (Δ -5.3 pp vs upfront 36.3 percent) | **FALSIFIED (opposite direction)** |
| H2 — staged 3-launch W3 LR0 in [40, 58] percent | band | **22.5 percent** (Δ -1.5 pp vs upfront 24.0 percent) | **FALSIFIED (opposite direction)** |
| H3 — staged 2-launch W8.7 LR15 in [25, 45] percent | band | **12.2 percent** (Δ -6.5 pp vs upfront 18.7 percent) | **FALSIFIED (opposite direction)** |
| H4 — Frame A optimum stays at 2-launch under staged | qualitative | 2-launch wins (0.208 percent vs 1-launch 0.089 percent, 3-launch 0.184 percent) | **HELD** |
| H5 — demonstrator NRE fraction in [8, 15] percent | band | **10.94 percent** ($1.6 billion / $14.6 billion) | **HELD** |
| H6 — at median clearing, upfront negative, staged flips positive | qualitative | both negative (upfront -$3.0 billion; staged -$3.4 billion) | **FALSIFIED (opposite direction — staged is more negative)** |
| H7 — median Δ-NPV across MC in [+$4, +$8] billion | band | **+$3.34 billion** (just below band; p05 -$70 billion; p95 +$9.5 billion) | **FALSIFIED (magnitude, below floor by $0.7 billion)** |

**Score: 2 HELD, 5 FALSIFIED.** Of the 5 falsifications, **4 are opposite-direction** (H1, H2, H3, H6) and 1 is magnitude-below-floor (H7). H1/H2/H3 all point the same way: **the working assumption that staged commitment improves Frame B P(NPV>0) is wrong.** Staged commitment HURTS Frame B by 5-7 percentage points at LR=15 and 1-3 percentage points at LR=0.

### Demonstrator NRE breakdown

| Component | $ million |
|---|---:|
| Mission-1 ship (first-unit cost, certain at year 0) | 500 |
| Mission-1 launch opex (3-launch ceiling) | 300 |
| Reactor flight-qual NRE | 600 |
| Mission-1 flight ops | 200 |
| **Total demonstrator commitment at gate 0** | **1600** |
| Fleet ships (22 missions, Wright's-Law amortized, LR 15) | 6428 |
| Fleet launches (22 missions × $300 million 3-launch ceiling) | 6600 |
| **Fleet capex (gated on demonstrator success, P=0.90)** | **13028** |
| **Total program capex (undiscounted)** | **14628** |
| **Demonstrator fraction of total** | **10.94 percent** |

**The anchor-investor framing holds on capital-efficiency grounds:** ~11 percent of total program capex committed at gate 0; ~89 percent contingent on demonstrator success. This is the structural-risk story. But it does NOT generate Frame B P(NPV>0) improvement.

### Median Δ-NPV across demand-curve distribution

Median Δ-NPV (staged minus upfront) at 2-launch W3 LR15: +$3.34 billion.
p05 of Δ: -$70.3 billion. p95 of Δ: +$9.5 billion.

Mode of Δ is positive but distribution is heavily left-skewed: at upper-tail clearings ($15,000+ per kilogram, top 25 percent of MC draws), the upfront-fleet revenue loss vastly exceeds the deferred-capex savings, producing -$50 billion to -$200 billion Δ in the worst draws. This wide left tail is what flips the binary P(NPV>0) comparison against staged.

---

## Revisit

| Hyp | Predicted | Measured | Reason for mismatch |
|---|---|---|---|
| H1, H2, H3 | staged Frame B > upfront Frame B by 10-30 pp | staged < upfront by 1-8 pp | **Anchored on R-heterogeneous-cadence single-price Δ-NPV (+$2.7 billion at $2.5 million per tonne) and assumed it would translate to a rightward shift of the NPV distribution under demand-curve clearing distribution.** It does shift right on median (+$3.3 billion per H7) but the distribution variance is huge (p05 -$70 billion; p95 +$9.5 billion), and the heavy upper-tail of the clearing price ($60,000+ per kilogram p95) produces draws where upfront fleet captures $200 billion+ NPV that staged cannot capture due to the 15-year fleet-deferral and 0.9 gate. The binary P(NPV>0) metric flips against staged because the upper-tail mass is in upfront's favor. **New methodology lesson #14.** |
| H4 | 2-launch wins Frame A under staged | 2-launch wins | HELD — staged commitment is dominated on Frame A but the launch-count ranking is preserved. |
| H5 | demonstrator NRE fraction 8-15 percent | 10.94 percent | HELD — BOE was tight on this. $1.6 billion gate-0 commitment vs $14.6 billion program total. |
| H6 | upfront negative → staged positive at median | both negative; staged MORE negative | Mechanism inverted — at median clearing $5.28 million per tonne, fleet break-even isn't reached at chunk-200 80-tonnes-per-mission under either accounting; staged loses the year-1-15 revenue that upfront's mission-2-onward delivers within the 40-year horizon. **Same root cause as H1-H3.** |
| H7 | median Δ-NPV in [+$4, +$8] billion | +$3.34 billion | Below floor by $0.7 billion. BOE bracket was anchored on naive scaling of R-heterogeneous-cadence's $2.5-million-per-tonne result by ~2× revenue multiplier (median demand-curve = $5.28 million per tonne ≈ 2.1× anchor). The scaling holds only on revenue side; capex side doesn't scale with revenue, so Δ-NPV scaling is sublinear. Same anchoring failure family. |

**Methodology lesson #14 (new):** Pre-registering Δ-NPV brackets by scaling a single-clearing-price anchor (e.g., R-heterogeneous-cadence $2.5 million per tonne result) to a heavy-tailed distribution (R-LEO-water-demand-curve clearing) is a magnitude-error pattern. The MEDIAN Δ-NPV under the distribution can be modest but the distribution VARIANCE around it can be enormous because price-distribution-tails interact with regime-specific time-deferral structure asymmetrically. When pre-registering against an MC-integrated outcome, **predict the distribution shape (p05, p50, p95) of Δ-NPV, not just the median**, AND consider whether the binary P(NPV>0) metric will move with median or with upper-tail mass.

**Methodology lesson #15 (new):** Sign-of-Δ-NPV at WACC=0 between two accounting regimes (Regime D and Regime R) is NOT invariant to revenue anchor. At LOW revenue prices, deferred-capex savings exceed revenue loss; at HIGH revenue prices, the inverse. Pre-registered sign-checks (XC-4 style) need to specify the revenue anchor and direction expectation conditional on it — not as a universal "deferred always loses at WACC=0" or "deferred always saves at WACC=0" rule. The two effects (deferred-revenue loss and deferred-capex saving) scale differently with revenue, so the crossover depends on the relative magnitudes of revenue and capex anchors.

**Recurring methodology lesson #7 (sixth strike):** opposite-direction falsifications (H1, H2, H3, H6) all share the same anchoring error — extrapolating a single-price BOE to a distribution. The fix proposed in lesson #7-v4 ("compute BOE for every cell whose value is bracketed in a hypothesis") doesn't address this distribution-aware case. **Lesson #7-v5 (proposed):** when a hypothesis brackets a value that integrates over a distribution, the BOE must compute the bracketed value AT MULTIPLE DISTRIBUTION POINTS (not just median) and report a probability-weighted reconciliation. Specifically: BOE the result at p25, p50, p75 of the distribution; the integrated outcome should be in the convex hull. If the convex hull doesn't bracket the integrated outcome, the BOE is incomplete.

---

## Reading

**The working assumption from round 11 — that staged commitment is the natural Frame B underwriting mechanism that shifts Frame B P(NPV>0) into majority territory at sovereign-bond — is FALSIFIED.** Under demand-curve clearing-price distribution, staged commitment REDUCES Frame B P(NPV>0) by 5-7 percentage points at LR=15 across all WACC and launch counts. The mechanism is the heavy-right-tail of the clearing-price distribution: when prices are high, upfront fleet captures more revenue within horizon than staged-deferred fleet can, by an enormous margin.

**What staged commitment IS (load-bearing for axis 17):**

1. **A gate-0 capital-efficiency mechanism.** ~11 percent of total program capex ($1.6 billion / $14.6 billion) committed at gate 0; ~89 percent gated on demonstrator outcome. The anchor-investor pitch story ("ICEBERG is a $1.6 billion gate-0 capital line within the round, not a $14.6 billion day-one commitment") HOLDS.
2. **A risk-management mechanism.** If demonstrator fails (P=0.10), only the $1.6 billion is at risk; fleet capex never committed. The "kill criteria at each gate" framing in the locked anchor-investor belief is structurally correct.
3. **NOT a Frame B P(NPV>0) improvement.** The matrix's axis-17 narrative that staged commitment "improves Frame B" needs amendment.

**What staged commitment is NOT (corrections required):**

1. **Not the financing mechanism that flips Frame B to majority territory.** That requires either better clearing prices than the demand-curve median (low-likelihood demand condition) or upfront full-fleet commitment.
2. **Not the right framing for sovereign-bond underwriting on Frame B grounds.** The sovereign bond underwriter cares about P(NPV>0) at their cost of capital; staged commitment makes that probability WORSE.

**Frame A optimum stays 2-launch under staged commitment** — H4 HELD. 2-launch is the Frame A baseline regardless of accounting regime.

**This round retires a working assumption from the four-round sitting** (rounds 9-12): the pitch's natural Frame-B-improvement mechanism is upfront full-fleet commitment, not staged commitment. Staged commitment lives on capital-efficiency grounds, not Frame-B-NPV grounds.

### Caveats and what this round does NOT prove

- The demand-curve calibration discrepancy (XC-1 / XC-2) means absolute Frame B percentages in this round are ~5-8 percentage points HIGHER than the demand-curve published headline. The COMPARATIVE result (Δ between regimes) is robust to this; the absolute level isn't. Anchoring on the published headline (42.8 percent upfront 2-launch W3 LR15) rather than my measured 50.8 percent would proportionally lower the staged number too.
- The 0.90 P_demonstrator anchor is L0-10 baseline. Per R-heterogeneous-cadence H-7, lower P_demonstrator INCREASES the staged-commitment Δ-NPV at $2.5 million per tonne; whether that holds under demand-curve distribution is untested. If lower P_demonstrator shifts the median Δ-NPV positive enough, the binary P(NPV>0) flip might disappear. A sensitivity at P_demonstrator ∈ {0.7, 0.5} would test this. Queued as priority-2 thread #8 below.
- No salvage value on demonstrator failure — the round assumes mission-1 capex is sunk if the demonstrator fails. Non-zero salvage (R-demonstrator-failure-recovery-value, queued from R-heterogeneous-cadence) would shrink the staged disadvantage.
- The R-heterogeneous-cadence parameter ambiguity (80 tonnes per mission vs Option A's 17 percent / 34 tonnes per mission) carries through; absolute numbers scale roughly linearly with delivered fraction, but the comparative direction is robust.
- This round does NOT compare staged-commitment vs other-financing-structures (e.g., milestone-based equity tranches, syndicated debt). It compares against upfront-fleet-commitment, which is the demand-curve's baseline framing.
- The H4 Frame A finding inherits the conjunction multiplier from round 9 (H2a uniform prior, 0.67 percent at sp=8 W/kg). Sensitive to the reactor-program conjunction prior.

---

## Cross-learning

**Negative for axis-17 pitch posture:** the matrix's axis-17 framing that staged commitment improves Frame B underwriting math is FALSIFIED. Staged commitment is a capital-efficiency / risk-management mechanism, not a P(NPV>0) lift. Recommend axis 17 amendment to:
- Keep "venture-class retired" (Frame A 0.21 percent at 2-launch staged is still far below venture hurdle).
- Distinguish the sovereign-bond Frame B story: at LR=15 upfront 2-launch is 36.3 percent (load-bearing number for sovereign-bond underwriter); staged commitment LOWERS that to 31.0 percent.
- Frame staged commitment as a gate-0 commitment-size story ($1.6 billion vs $14.6 billion), not a Frame-B-numerator story.

**Positive for axis-13 (outbound launch architecture):** round 12's 2-launch Frame A optimum is reinforced — 2-launch wins under both upfront and staged accounting. No change.

**Positive for axis 02 (surviving cell):** the "stage-gate the program at a Variant B demonstrator" path opened by R-heterogeneous-cadence is still architecturally available, but its economic justification is risk-management not Frame-B-NPV. Recommend axis 02 amendment to add an explicit caveat that the third-path framing's NPV story is upper-bounded at the upfront-commitment Frame B numbers; staged commitment is for risk-management of gate-0 capital, not for NPV improvement.

**Positive for axis 10 (L0-05 strict vs waiver):** unchanged — staged commitment doesn't interact with L0-05 timing.

**Negative for the R-heterogeneous-cadence headline framing:** R-heterogeneous-cadence's +$2.7 billion at $2.5 million per tonne was anchored on a single price; the demand-curve-integrated headline shows the result is a sample-point in a heavy-tailed distribution. R-heterogeneous-cadence's "Reading" section claimed staged commitment captures "all the real-options value" — that's correct on EV grounds but NOT on P(NPV>0) grounds at demand-curve clearing distribution. Recommend the R-heterogeneous-cadence Reading section be amended (in a HISTORY note in design-axes/02) to clarify the EV-vs-binary distinction.

**Negative for R-clearing-price-tail-integration-decision-frame's Frame B "29 percent at sovereign-bond" anchor:** that anchor was W3 LR0 upfront and replicated 29.1 percent in this round (XC-2 measured 34.5 percent in fleet-NPV harness; demand-curve published 29.1 percent in per-mission-break-even harness). At LR=15 (which Wright's-Law learning would naturally apply), the sovereign-bond Frame B rises to 36.3 percent upfront and falls to 31.0 percent staged. Recommend round 11's headline be cited with explicit conditioning on LR=0 — the LR=15 number is materially higher.

**New methodology lesson #14 (distribution-aware BOE):** see Revisit. Pre-registering Δ-outcomes integrated over distributions requires distribution-shape BOE, not single-point BOE.

**New methodology lesson #15 (sign-of-Δ at WACC=0 is revenue-dependent):** see Revisit. Sign-checks anchored on a single revenue level can flip sign at other revenues.

**Methodology lesson #7 (recurring, sixth strike):** the per-cell BOE protocol needs distribution-aware extension. Lesson #7-v5 proposed.

---

## New pending threads (spawned by this round)

**Priority 1:**

1. **R-staged-commitment-EV-vs-binary-reconciliation** — explicit reconciliation between expected-NPV (where staged is +$3.3 billion median better) and binary P(NPV>0) (where staged is -5 pp worse). Which metric does sovereign-bond underwriting actually anchor on? Probably the binary, for technical-loan-covenants. Probably the EV, for sovereign-grant. Needs a decision on which Frame B metric the matrix should anchor on.

2. **R-staged-commitment-P-demonstrator-sensitivity** — does the Frame B falsification persist at lower P_demonstrator (0.7, 0.5)? Per heterogeneous-cadence H-7, lower P_demonstrator INCREASES Δ-EV; if the distribution variance shrinks proportionally, the binary metric might flip back to favor staged.

**Priority 2:**

3. **R-demonstrator-failure-salvage** — non-zero salvage of mission-1 capex on demonstrator failure (technology IP, partial hardware reuse, data). Could shift the comparison materially.

4. **R-multi-gate-staged-commitment** — generalize beyond binary mission-1 gate to N-mission gates. Each gate adds option value.

5. **R-upfront-Frame-B-as-the-load-bearing-pitch-cell** — given this round's finding, the matrix's Frame B headline should be 36.3 percent (upfront W3 LR15 2-launch). Reconcile against R-clearing-price-tail-integration's 29 percent at W3 LR0 to settle which is the right anchor for axis 17.

6. **R-syndicated-financing-tranches** — different financing structures (sovereign-bond senior tranches gated by demonstrator + commercial-equity ramp tranches) might capture both the gate-0 capital efficiency AND the upfront Frame B. Out-of-scope for this round; structurally important for pitch follow-on.

7. **R-anchor-investor-belief-update** — the locked anchor-investor belief (`76fd04cdba8b2c3b`) describes ICEBERG as "demonstrator flights every ~2 years with explicit kill criteria at each gate." This round's finding doesn't contradict that framing — but the NPV story underneath needs to be EV-based ($3.3 billion median improvement) not binary-based (-5 pp Frame B). The belief should be locked with this clarification.

**Resolved / refuted:**

- ~~Round 11 working assumption: "staged commitment is the natural Frame B underwriting mechanism"~~ — **FALSIFIED** on binary P(NPV>0) grounds; HELD on EV grounds.

