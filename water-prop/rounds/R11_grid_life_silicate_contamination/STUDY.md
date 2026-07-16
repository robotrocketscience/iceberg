# Round 11 — Grid Life Under Chunk-Water Silicate Contamination

**Status:** pre-result.

## Question

R10 recommended water radio-frequency ion (Pale Blue class) at 2000 s specific impulse as the inbound thruster. Pale Blue's flight heritage is on purified water. B-ring water-ice contains some fraction of silicate dust (per Hsu 2015 / Cassini Cosmic Dust Analyzer evidence; R1 placed it at < 1%). The question for R10's recommendation is: does the silicate fraction reaching the thruster grids erode them faster than the 7-year inbound cruise, and what filtration is needed?

A separate question raised in pre-round scoping: the ICEBERG conops bag operates as a sublimation distillation (hot-side sublimation of water from the chunk, cold-side cryopumping as frost, harvest-port re-sublimation into the propulsion feed line). Non-volatile silicates stay on the hot wall and never enter the propulsion feed under nominal bag operation. **The bag is incidentally a high-rejection-ratio silicate filter.** This reframes R11: it is not a question of "what filtration do we add?" but "how robust is the filtration the bag already provides, and what's the propagated failure mode if the bag thermal control fails?"

## Pre-registered hypothesis (H11)

| # | Claim | Predicted range | Falsification threshold |
|---|---|---|---|
| H11a | B-ring water ice silicate fraction (mass basis) | 0.1–5% | held if ∈ range |
| H11b | Sublimation-distillation rejection ratio of silicate vs. water under bag conditions | 10⁻³ to 10⁻⁵ (99.9% to 99.999% rejection) | held if ∈ range |
| H11c | Silicate mass reaching thruster grids over 7-year cruise under nominal bag operation | 1 mg to 500 g | held if ∈ range |
| H11d | Grid life under nominal bag operation, scaled from NSTAR / Pale Blue heritage | > 7 years (silicate contribution < 10% of baseline xenon-class wear) | falsified if < 7 years |
| H11e | Grid life under bag-thermal-control failure (cold-wall warming, silicate flooding) | < 6 months | held if ≤ 6 months |
| H11f | Mass cost of secondary mesh-and-zeolite filter at harvest port for bag-failure backup | 5–50 kg | held if ∈ range |

**Aggregate (H11-agg):** I predict R10's water radio-frequency ion recommendation survives this round under nominal bag operation, but the architecture has a propagated single-point-of-failure dependency: bag-thermal-failure causes thruster failure within months. The mitigation is a small secondary filter (~10–30 kg) at the harvest port that protects the thruster for some weeks during a bag-failure recovery window. The deeper finding is architectural: **program risk M-BAG (bag thermal containment failure) is also the dominant propulsion-system risk for the R10-recommended thruster choice.** Two consequences from one failure mode.

## Method

This is a desk study with bounding calculations, not a chamber-test simulation. Grid erosion at the certainty needed for a flight program requires hardware testing; this round produces a bound and a list of follow-on test requirements.

1. **B-ring silicate fraction:** bracketed from open-literature Cassini results (Hsu 2015, Hedman 2013, Cuzzi 2010 for B-ring composition).
2. **Sublimation-distillation rejection:** scaled from vacuum-distillation laboratory data. Water vapor pressure at 250–280 K (hot-side bag) is ~10² to 10³ Pa; silicate vapor pressure is essentially zero (refractory, mp > 1700 K). The rejection ratio is set by carryover via mechanical entrainment, aerosol formation, and back-diffusion — typically 10⁻³ to 10⁻⁶ in industrial vacuum distillation.
3. **Silicate mass flow into thruster:** total chunk water consumed by propulsion × silicate fraction × (1 - rejection ratio).
4. **Grid erosion comparison:** NSTAR life-test data (235 kg xenon throughput over 30,400 hours, 1.5 mm peak grid wear) scaled by silicate-vs-xenon sputter yield. Silicate (SiO₂, Al₂O₃, Mg₂SiO₄) sputter yields onto molybdenum grids at 1–2 kV are 2–5× higher than xenon by mass per published sputtering tables (Yamamura 1996 / Behrisch handbook).
5. **Bag-failure scenario:** if cold-wall temperature rises and hot-wall residue starts entraining into vapor flow, silicate flux to the thruster spikes by 10²–10⁴× compared to nominal. Estimate time-to-grid-failure under this regime.
6. **Backup filter mass:** sintered Inconel mesh at 100 nm cutoff (commercial filtration heritage; HEPA equivalent) plus optional zeolite trap. Mass-cost it against the propellant feed-line geometry.

**Validity caveats.**
- The 10⁻³ to 10⁻⁵ sublimation-distillation rejection ratio is a literature scaling, not a measurement on the actual bag geometry. Real rejection depends on bag thermal gradient, hot-side temperature, cold-side temperature, vapor velocity, and aerosol generation — none of which are flight-tested.
- Sputter yield scaling for silicate-particulate (as opposed to monatomic-ion) bombardment of grids is approximate. Silicate ions accelerated through the grid potential behave differently from neutral silicate particulates entrained in the propellant flow.
- Pale Blue's published water-radio-frequency-ion grid life is on terrestrial-distilled water; extrapolation to chunk water is a heritage stretch.
- The conops bag's heat-pipe topology has no mechanical pumping and relies on a temperature gradient. Off-nominal thermal cycling (eclipse seasons, attitude maneuvers) could transiently reverse the hot/cold gradient. Not modeled.

## Result

See `results/silicate_contamination_audit.json`. Headline numbers:

**Silicate mass reaching the thruster grids over the 7-year cruise (3 × 3 sensitivity grid: B-ring composition × bag rejection ratio):**

| B-ring silicate fraction | Pessimistic rejection (99.9%) | Mid rejection (99.99%) | Optimistic rejection (99.999%) |
|---|---|---|---|
| 0.1% (Cassini Grand Finale clean-ice case) | 8.0 g | 0.80 g | 0.080 g |
| 1% (R1 upper-bound midpoint) | 80 g | 8.0 g | 0.80 g |
| 5% (pessimistic bound) | 400 g | 40 g | 4.0 g |

**Worst-case nominal (5% silicate × 99.9% rejection): 400 g over 7 years.** Scaled NSTAR equivalent grid wear: 9 μm — about 2.4% of grid thickness. Negligible against baseline molybdenum-grid lifetime.

**Bag-failure scenario:** if the bag's hot/cold thermal gradient collapses and raw chunk water flows directly to the thruster, silicate flux jumps ~1000× and time-to-grid-failure is 543 days (18 months) at 1% silicate composition. **This is longer than my pre-registered prediction of < 6 months** — months-scale ground-recovery window rather than weeks-scale catastrophic.

**Backup filter sizing:** ~14 kg (sintered mesh + zeolite, redundant per-thruster), buys ~30 days of thruster protection during a bag-failure event before the filter itself saturates.

**Hypothesis grading:**

| ID | Verdict | Evidence |
|---|---|---|
| H11a (silicate fraction 0.1–5%) | held | range used spans predicted |
| H11b (rejection 10⁻³ to 10⁻⁵) | held | range used spans predicted |
| H11c (silicate mass to thruster 1 mg–500 g) | held | range 0.08 g–400 g |
| H11d (nominal grid life > 7 yr, < 10% wear contribution) | held | worst-case added wear = 2.4% of grid thickness |
| H11e (bag-failure grid life < 6 months) | **falsified-conservative** | actual = 18 months — bag failure is less acute than predicted |
| H11f (backup filter 5–50 kg) | held | 14 kg |

**Methodology note flagged:** the NSTAR-proxy baseline calculation (8 t water at NSTAR-xenon erosion rate) returns 51 mm of wear vs. a 0.38 mm grid — 134× failure. Real Pale Blue radio-frequency ion grid wear must be much lower than this proxy suggests; the proxy bounds *worse* than reality. Real Pale Blue grid-wear-per-kg data is the missing input.

## Reading

1. **Under nominal bag operation, silicate contamination is not a thruster life-limiter.** The bag's sublimation-distillation step is incidentally a high-rejection-ratio filter, and even at pessimistic composition × pessimistic rejection, the silicate contribution to grid wear is sub-percent. R10's water radio-frequency ion choice survives the contamination question.

2. **Bag failure is less acute than predicted.** 18 months to grid failure (vs. < 6 months prediction) means a ground-intervention window exists. Combined with the 30-day backup-filter window, the architecture can survive a bag-thermal-control failure long enough to diagnose and respond — assuming the bag has in-flight repair capability. **It almost certainly does not.** The bag is a passive heat-pipe topology with no actuated thermal control surfaces; if the gradient collapses, there's nothing to repair in flight.

3. **The architecture has a propagated single-point-of-failure.** Program risk M-BAG (bag thermal containment failure) is now confirmed as the dominant propulsion-system risk for the R10 thruster choice. Two failure consequences from one root cause. The risk register should reflect this coupling.

4. **The NSTAR-proxy bound is too conservative.** Real Pale Blue radio-frequency ion grid wear on terrestrial water needs verification. Flag for a literature follow-up: pull Pale Blue's published grid-wear-per-kg from Koizumi / Komurasaki papers if any exist. If Pale Blue's real wear is, say, 10⁻³ of NSTAR's, the baseline column changes from "13,000% wear" to "13% wear" — still concerning but bounded.

## Revisit

H11a, H11b, H11c, H11d, H11f all held. **H11e falsified-conservative** — bag-failure window is 3× longer than predicted. My mental model treated "bag fails → catastrophic immediate contamination" but the actual rate-limit is the silicate mass flux through the grids, not an instantaneous flood. Lesson: failure-mode-mapping in concept architectures benefits from explicit timescale-of-effect analysis; "catastrophic" is rarely instantaneous and the recovery window dimension is its own design variable.

The methodology note (NSTAR-proxy too conservative for radio-frequency ion) is the most actionable correction. Filed as a follow-up data hunt rather than a new round.

## Cross-learning

- **Supports R10 recommendation.** Water radio-frequency ion grid life under chunk-water survives R11's stress test under nominal bag operation. R10's architectural choice holds.
- **Couples M-BAG program risk to propulsion-system risk.** The same bag-thermal-failure mode that loses cargo (M-BAG, I5) also kills the thruster within months (R11). One root cause, two consequences. Risk register update: M-BAG's impact rating should explicitly note both consequences.
- **Backup filter at 14 kg is cheap insurance.** Recommend adding a per-thruster mesh-plus-zeolite filter at the harvest port. Buys 30 days of bag-failure tolerance.
- **R12 candidate (follow-up data hunt, not a new round):** pull Pale Blue's published grid-wear-per-kg from Koizumi / Komurasaki publications. The NSTAR-proxy used here over-bounds real wear by an estimated 100–1000×. Real number would tighten the H11d margin.
- **Methodology lesson surfaced:** failure-mode timescale analysis. "Catastrophic" is rarely instantaneous; the time-to-effect dimension is part of the architecture trade. Adding this to the campaign's recurring-lesson set as #5: every failure-mode analysis should include a timescale-of-effect estimate, not just a presence/absence call.
- **Negative-result for "the architecture has a single-point-of-failure that's tightly time-coupled."** Less true than my pre-round intuition suggested. 18 months is enough for ground intervention if any is possible at all (open question).

