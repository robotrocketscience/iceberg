# R-exit-burn-power-audit

**Worker:** titan (Block 10)
**Owner:** project owner / orchestrator
**Pre-registration date:** 2026-05-16
**Predecessor:** R-no-jupiter-composite-headroom (Block 9), R-residence-exit-maneuver (Block 4), R-cathode-life-water-plasma

---

## Motivation

Block 9 surfaced the headroom levers above Block 8's 15.37 percent baseline. In so doing it re-categorised L3 (exit Isp 7000 → 9000 s) as "cathode-life-conditional" — i.e. promised to audit whether the cathode budget admits the Isp uplift. While beginning that audit, a more fundamental problem surfaced in the *baseline* Block 4 composite, not the L3 uplift: **the exit burn at the assumed 500 kilowatt-electric power class does not fit in the 6-month residence dwell.**

Block 4 (R-residence-exit-maneuver) flagged this as a validity caveat without numerically closing it:

> Validity caveat: Isp 7000 s NEP requires a reactor + grid + plasma source. Thrust at fixed power scales 1/Isp; doubling Isp halves thrust. Need to verify 6-month exit burn is executable at half thrust without exceeding power-system duty cycle limits.

Back-of-envelope check at the composite's nominal parameters:

- Spacecraft mass at exit: 380 t (200 t collected water + 180 t dry-effective after 20 t jettison).
- Exit delta-velocity: 7.4 km/s.
- Exit Isp: 7000 s; exhaust velocity 68,670 m/s.
- Power: 500 kilowatt-electric, anode efficiency 0.65 (matrix canonical).
- Jet power: 325 kilowatt; thrust at Isp 7000: 9.5 newton.
- Mass-ratio exp(7400/68670) = 1.114; propellant mass ≈ 39 tonne.
- Mass flow ≈ 1.38e-4 kg/s.
- Burn time ≈ 39,000 / 1.38e-4 = 2.83e8 s ≈ **9 years**.

This is ~18× the assumed 6-month residence dwell. Block 4's H5 hypothesis adjudicated on delivered fraction (8-11 percent predicted, 8.5 percent observed — held) but did *not* check whether the exit burn fits in the residence dwell.

If the exit burn requires 9 years at 500 kilowatt-electric, the composite architecture has one of three resolutions:

1. **Higher exit power.** A reactor sized for ~9 megawatt-electric residence-only operation closes the burn in 6 months. This re-opens the entire power-class trade — hyperion's R-variant-B-500kWe-sizing established 500 kilowatt-electric as the risk-adjusted optimum, and the matrix's megawatt rows depend on Fission Surface Power Phase 2 that has not been awarded (per locked memory finding).
2. **Multi-year residence dwell.** Extend Saturn-side dwell from 6 months to ~9 years to accommodate the exit burn at 500 kilowatt-electric. This adds ~9 years to round-trip and likely violates L0-05 (15-year ceiling).
3. **Lower exit Isp.** Drop exit from Isp 7000 to Isp 5000 s; thrust rises 40 percent (13.25 N), burn time drops to ~6 years (still too long), and delivered fraction collapses toward the pre-uplift baseline (Block 4 A1 ≈ 3.9 percent).

This round closes the burn-time arithmetic and computes the (exit_power, exit_isp, exit_dwell_months) admissible region. If H1 falsifies — which the back-of-envelope says it should — Block 4's "composite at 21.8 percent / Block 9's 15.73 percent honest-floor" verdicts inherit a load-bearing closure condition.

---

## Pre-registered hypotheses

| # | Hypothesis | Prediction | Falsification rule |
|---|---|---|---|
| H1 | Block 4's nominal exit burn (Isp 7000 s, power 500 kilowatt-electric, η 0.65, dv 7.4 km/s, m_spacecraft 380 t) completes in 5-7 months. | Exit burn time ∈ [5, 7] months. | Falsified if outside [3, 12] months. **Back-of-envelope predicts ~9 years.** |
| H2 | Power required for 6-month exit burn at Isp 7000 / dv 7.4 / m_spacecraft 380 t / η 0.65 is 1-3 megawatt-electric. | Required power ∈ [1, 3] MWe. | Falsified if outside [0.5, 15] MWe. **Back-of-envelope predicts ~9 MWe.** |
| H3 | At realistic Block 4 power 500 kilowatt-electric and Block 4 Isp 7000 s, exit burn requires 5-15 years. | Burn time ∈ [5, 15] years. | Falsified if < 1 year or > 20 years. |
| H4 | Minimum exit-only power that fits 6-month residence dwell at Isp 5000 s, 7.4 km/s, 380 t is 1-3 megawatt-electric. | Min power ∈ [1, 3] MWe. | Falsified if outside [0.5, 10] MWe. |
| H5 | **Architecture claim:** Block 4's composite (Isp 7000 exit at 500 kilowatt-electric / 6-month dwell) does NOT close in burn time. The composite requires either (a) megawatt-class residence power (~1-10 MWe), (b) multi-year residence dwell (incompatible with L0-05 15-year ceiling), or (c) reverting exit Isp to ~5000 s with lower delivered fraction. The Block 4 / Block 5 / Block 6 / Block 7 / Block 8 / Block 9 delivered-fraction headlines all inherit one of these three resolutions. | H1 falsified-high (burn takes years not months) AND H2 falsified-high (power needed >> 500 kilowatt-electric). | Falsified if H1 holds (burn fits 6 months at 500 kilowatt-electric). |
| H6 | The "extend dwell" resolution path is L0-05-incompatible. At 500 kilowatt-electric and Isp 7000, exit burn time ~9 years adds to the existing inbound burn (~1.5 years from Block 4) and Hohmann cruise (~12 years round-trip), giving total mission duration > 22 years vs L0-05 15-year ceiling. | Mission duration with 9-year exit > 20 years; > L0-05 ceiling. | Falsified if mission duration fits inside L0-05. |
| H7 | The "lower Isp" resolution path collapses delivered fraction toward Block 4 A1 baseline (~3.9 percent). At Isp 5000 exit, 500 kilowatt-electric, 7.4 km/s, burn time is still > 5 years (does not save the architecture; just degrades both delivered fraction and burn time). | Composite at Isp 5000 exit delivered fraction < 12 percent; burn time still > 5 years. | Falsified if Isp 5000 closes burn time in < 1 year OR delivered fraction stays > 14 percent. |
| H8 | The "raise exit power" resolution path is the only one that survives, and it requires ~5-15 megawatt-electric residence-only power. This re-opens hyperion's R-variant-B-500kWe-sizing verdict and propagates into the matrix's reactor-roadmap row, which (per locked memory) depends on Fission Surface Power Phase 2 that has not been awarded as of May 2026. | Min residence power for 6-month exit closure at Isp 5000-7000 range is in [3, 15] MWe. | Falsified if min power < 2 MWe (still 4× Variant B baseline but plausibly within hyperion's "hybrid" rounds). |

---

## Method

**Variables.**
- exit_dv (km/s): fixed at 7.4 (Block 4).
- exit_isp (s): swept across [3000, 5000, 7000, 9000].
- exit_power (kilowatt-electric): swept across [500, 1000, 2000, 5000, 10000].
- spacecraft_mass_at_exit (t): 380 (Block 4 composite).
- anode_efficiency: 0.65 canonical (matrix optimistic) and 0.30 realistic (per R-cathode-life sensitivity). Report both.
- residence_dwell (months): nominal 6, sensitivity 12, 24, 36.

**Calculations.**
- thrust_N = 2 × exit_power × η / (Isp × g0)
- mr_exit = exp(dv/(Isp × g0))
- m_propellant = m_start × (1 - 1/mr_exit)
- mass_flow = thrust_N / (Isp × g0)
- burn_time_seconds = m_propellant / mass_flow
- burn_time_years = burn_time_seconds / (365.25 × 86400)

**Cathode-on time per mission** = exit_burn + inbound_burn (Block 4's inbound at Isp 5000 / 500 kilowatt-electric / 24.7 km/s / m_start = 344.86 t after exit).

**Outputs.**
- `results/burn_time_grid.csv` — (exit_power, exit_isp) × (burn time months, burn time years).
- `results/closure_envelope.csv` — minimum exit power to fit 6-month dwell at each Isp.
- `results/cathode_budget.csv` — per-mission cathode hours and × reuse cadence vs Advanced-Electric-Propulsion-System design life.
- `results/summary.json` — hypothesis adjudication and architecture verdict.

**Verification cross-checks.**
- Variant B per-mission cathode-on time from R-cathode-life round (5,435 hour canonical at 6.42 km/s inbound) recovered when running my model at Variant B's parameters.
- Block 4's "8.5 percent delivered fraction at A5 (Isp 7000 exit, Isp 5000 inbound, baseline)" recovered when running with same dv and Tsiolkovsky math (already verified in Block 9 by reproducing 15.37 percent).

---

## Limitations

- **Thruster efficiency at Isp 7000-9000.** This round uses matrix canonical η = 0.65, with realistic 0.30 as sensitivity. Real water-fed thrusters at Isp 7000+ have no published efficiency anchor (per R-all-electric-thruster-sweep limitations). The canonical number is a xenon-Hall-heritage extrapolation; the realistic number is from R-aets sensitivity.
- **Reactor sizing for "exit-only" higher power.** This round computes "minimum exit power to fit 6-month dwell," which is an exit-only requirement. A real spacecraft would have a fixed reactor sized for cruise+inbound+exit needs together. The minimum exit power computed here is a lower bound on the residence power-class requirement — the actual reactor must also serve inbound and outbound at their respective burn-time / Isp needs.
- **Continuous-thrust assumption.** All burns are assumed continuous, no duty-cycle constraints (radiator deployment, attitude-control swap-outs, etc). Real-mission duty cycle would extend burn-time wall-clock at ~80-90 percent on/off ratio.
- **L0-05 ceiling interpretation.** L0-05 is "15-year mission from launch to delivered water in cislunar orbit." This round assumes the residence dwell counts against that ceiling (it is part of mission duration). If L0-05 is reinterpreted to exclude residence dwell or to allow multi-year extensions, H6 falsification rule shifts.
- **Cathode-life budget at higher Isp.** Higher Isp at fixed power means lower thrust means longer burn time per kg propellant; total cathode-on time scales with propellant mass divided by mass flow. R-cathode-life round established Variant B at 5,435 hour single-mission; this round extends to the composite's exit + inbound burn. Cathode life *replacement* count scales with this round's number divided by Advanced-Electric-Propulsion-System 50,000-hour design life.

---

## Decision rule

- **H1 held** (exit fits 6 months at 500 kilowatt-electric) → Block 4 composite is sound; Block 9's verdict survives. No architecture revision needed.
- **H1 falsified-high + H5 held** (Block 4 composite doesn't close in burn time) → All composite delivered-fraction numbers (Block 4 21.8%, Block 5 15.97%, Block 8 15.79% campaign-mean, Block 9 15.73% honest-floor) inherit a closure condition on residence power class or dwell extension. Pitch, matrix, requirements all need revision.
- **H8 held** (resolution requires megawatt-class residence power) → Architecture inherits Fission Surface Power Phase 2 dependency that the locked memory finding flags as un-awarded as of May 2026. Reactor roadmap critical-path question.
- **H8 falsified-low** (resolution closes at 1-3 megawatt-electric) → Architecture inherits a "1-3 MWe residence reactor" requirement that is more plausible than full megawatt-class but still requires a power-architecture round to derive.

The orchestrator should integrate this round's finding before the Block-5-and-onward delivered-fraction headlines propagate to the pitch deck. If H1 falsifies, every Titan round from Block 4 forward depends on an unaudited assumption that this round closes.

---

## Results (2026-05-16)

### Headline number

**Block 4's nominal exit burn at 500 kilowatt-electric / Isp 7000 s / 7.4 km/s / 380 tonne / efficiency 0.65 takes 8.92 years — 17.8× the 6-month residence dwell budget Block 4 assumed.** Back-of-envelope confirmed numerically.

| Parameter | Block 4 assumed | Actual |
|---|---|---|
| Exit burn time | 6 months | **107.1 months (8.92 years)** |
| Thrust at 500 kilowatt-electric / Isp 7000 / η=0.65 | (not stated) | 9.47 N |
| Propellant mass for 7.4 km/s on 380 t | ~40 t | 38.83 t (close) |
| Ratio of actual to assumed burn time | 1× | **17.8×** |

### Minimum residence power to close 6-month exit burn

| Exit Isp | Minimum power (megawatt-electric) |
|---|---|
| 3000 s | 3.57 |
| 5000 s | **6.24** |
| 7000 s | **8.92** |
| 9000 s | 11.6 |

To close exit burn in 6 months at Block 4's Isp 7000, the spacecraft needs **8.9 megawatt-electric** — 18× Variant B's 500 kilowatt-electric. To close at Isp 5000 (the "revert" path), still needs **6.2 megawatt-electric**. The composite cannot close in 6-month dwell at 500-kilowatt-electric class power for any Isp examined.

### Resolution paths

| Path | Verdict |
|---|---|
| (a) Megawatt-class residence power | **High Bayesian-risk-adjusted unlikelihood.** Per locked memory: US space-fission programs have 0-of-6 base rate of reaching orbit within their originally-stated decade; FSP Phase 2 not awarded; 40-W/kg specific-power is TRL-2 paper-study; radiator subsystem alone is 40-55 percent of megawatt-class system mass per MARVL. The 6.2-11.6 MWe requirement here lands squarely in territory the program has Bayesian reason to discount. |
| (b) Extend residence dwell to ~9 years | **L0-05-violating.** Total mission duration with 8.92-year exit burn = 12 (cruise) + 1.5 (inbound burn) + 8.92 (exit burn) = 22.4 years, vs L0-05 15-year ceiling. **H6 held.** |
| (c) Revert exit Isp to 5000 s | **Does not save the architecture.** Delivered fraction collapses to 10.84 percent (vs 15.37 percent at Isp 7000); AND burn time is still 6.24 years at 500 kilowatt-electric (does not fit 6-month dwell). **H7 held.** |
| (d) Reframe exit burn to span cruise leg (not residence-bounded) | **Not modeled here; needs separate round.** If the exit burn is operationally a spiral-out during outbound cruise (analogous to Variant B's spiral-in inbound), the 8.92-year burn time is compatible with the ~6-year outbound cruise — but the spacecraft is no longer "at residence." Concept needs explicit definition and re-analysis. |

### Hypothesis adjudication

| Hyp | Prediction | Observed | Status |
|---|---|---|---|
| H1 (burn 5-7 months at Block 4 nominal) | [5, 7] mo | 107.1 mo | **falsified-high (17.8×)** |
| H2 (1-3 MWe for 6-mo at Isp 7000) | [1, 3] MWe | 8.92 MWe | marginal (within [0.5, 15] band; intuition off by 3×) |
| H3 (burn 5-15 years at 500 kWe / Isp 7000) | [5, 15] yr | 8.92 yr | **held** |
| H4 (1-3 MWe at Isp 5000) | [1, 3] MWe | 6.24 MWe | marginal (intuition off by 2×) |
| H5 (Block 4 composite doesn't close in burn time) | — | — | **held** |
| H6 (mission > L0-05 ceiling under dwell-extension) | — | 22.4 yr > 15 yr | **held** |
| H7 (Isp 5000 revert doesn't save: df < 12% and burn > 5 yr) | — | 10.84%, 6.24 yr | **held** |
| H8 (resolution requires 3-15 MWe) | [3, 15] MWe | 6.24-11.6 | **held** |

H2 and H4 are technically "marginal" (within tolerance band) but the predicted central values [1, 3] MWe were 2-3× too low. This is another instance of Lesson 8: prediction anchored on intuition (Variant B is 500 kWe, residence-class would scale 2-6×), not on physics computation (scaling is actually 12-18×). Documented as Lesson 8 instance #4.

### What this means for the Titan campaign

**Block 4's "composite architecture closes residence-class to 21.8 percent central delivered fraction" — the architecture-rescue verdict that survived Blocks 5/6/7/8/9 audit on delivered-fraction grounds — has a load-bearing closure condition that was flagged as a validity caveat in Block 4 and NEVER NUMERICALLY CLOSED.**

The composite delivered-fraction headlines from Blocks 4 through 9 (21.8 percent Block 4; 15.97 percent Block 5; 15.79 percent Block 8 campaign-mean; 15.73 percent Block 9 honest floor) are all *conditional on the exit-burn power-class assumption that this round invalidates.*

Three sub-implications:

1. **Pitch and matrix should NOT quote any Block-4-or-later composite delivered fraction without footnoting the resolution path.** The composite is honestly conditional on Path (a), (b), or (d) closing favourably; Path (c) is independently retired by this round.

2. **The residence-class architecture's structural claim is reduced.** The chunk → ram-scoop pivot (Block 2 R-conops-chunk-vs-ram-scoop) survives as physically feasible. The composite delivered-fraction headline does not survive as burn-time-closed. The architecture is "physically-feasible-but-not-burn-time-closed" until one of the resolution paths is proven.

3. **The locked-memory ICEBERG power findings 1-4 now directly bite the architecture's headline.** Block 9 found composite Option-A-equivalent under inert-mass assumptions; Block 10 finds composite ALSO conditional on a power-class scaling that locked memory says the program has Bayesian reason to discount.

### Follow-on rounds surfaced

1. **R-spiral-out-exit-architecture (new, critical-path).** Model Path (d): exit burn as a spiral-out during outbound cruise, not at residence. If this closes at 500 kilowatt-electric, the architecture's burn-time problem is resolved without requiring megawatt-class power. **Most-likely-to-save-the-architecture path.**
2. **R-residence-power-class-required (new, critical-path).** Audit reactor-mass scaling at 6-12 MWe residence-only operation, against MARVL-anchored radiator-mass model (per locked memory). Likely outcome: spacecraft dry mass at megawatt-class is much higher than 200 t, which propagates back to Block 9's L5 lever (dry mass goes UP, not down). Composite at this regime may not even close on delivered fraction.
3. **R-hybrid-exit-power-source (new).** Could a fission battery / radioisotope / chemical augmenter provide exit-only peak power at residence without sizing the cruise reactor up? At 6-12 MWe for 6 months, the energy required is substantial (~31 GJ) but a chemical augmenter or short-life isotope is plausible.
4. **R-exit-burn-extends-into-cruise (variation of #1).** If exit burn is allowed to extend partially into cruise (e.g. 50/50 residence/cruise split), what's the closure regime?

### Files

- `STUDY.md` — this document.
- `run.py` — composite exit-burn power and time calculator.
- `results/burn_time_grid.csv` — (exit_power, exit_isp) × burn time grid.
- `results/closure_envelope.csv` — minimum exit power for various dwell durations.
- `results/cathode_budget.csv` — per-mission cathode-on time at various power classes.
- `results/summary.json` — full hypothesis adjudication.
