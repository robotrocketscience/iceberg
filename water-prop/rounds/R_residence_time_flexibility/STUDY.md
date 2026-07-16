# R-residence-time-flexibility

**Worker:** titan (Block 7)
**Owner:** project owner / orchestrator
**Pre-registration date:** 2026-05-15

---

## Motivation — the most promising remaining Jupiter-gravity-assist lever

Block 5 (R-launch-window-cadence-revisit) found Jupiter return gravity-assist is available at 2.78% of Earth-Saturn launches under fixed-cruise Hohmann inbound. Block 6 (R-jupiter-ga-saturn-exit-flexibility) ruled out Saturn-exit Δv variation as a meaningful additional lever (combined fraction at ≤ 1 km/s budget rises only to 3.48%).

There is one more lever worth testing: **residence-time-flexibility.** The Saturn residence duration was set to 0.5 years in Block 4, but this number is arbitrary — accretion fill takes seconds (Finding 5), so residence is mostly engineering-checkout time. If the chunk can wait at Saturn for some integer number of synodic-relevant time before exit, it can shift Jupiter-Saturn relative geometry by 18.1° per year of residence extension at *zero delta-velocity cost*. The costs are mission duration and radiation dose to electronics, not propellant.

If a 1-2 year residence extension gives meaningful Jupiter-alignment flexibility, Block 5's verdict needs partial revision: Jupiter return gravity-assist remains a lever, but at the cost of slower steady-state launch cadence (extended residence pushes everything back).

**This round questions whether the 0.5-yr residence time was a load-bearing assumption.**

---

## Pre-registered hypotheses

| # | Hypothesis | Prediction | Falsification rule |
|---|---|---|---|
| H1 | Residence-time-flexibility provides ~18.1° of Jupiter-Saturn relative-phase tuning per year. (Saturn moves 12.2°/yr in heliocentric longitude; Jupiter 30.3°/yr; relative motion 18.1°/yr.) | Phase-shift per residence-year ≥ 17°. | Falsified if phase-shift per residence-year is < 15° or > 22°. |
| H2 | Each year of residence extension widens the effective Jupiter-viable tolerance window by ~18°. Combined with the natural ±5° at zero extension: 1 year of extension gives ±13° equivalent, 2 years gives ±21°. | At 1 yr residence-extension budget: Jupiter-viable fraction at ±5° tolerance ≥ 0.30. | Falsified if fraction at 1-yr budget is < 0.20 (lever weaker than expected) or > 0.55 (some artefact). |
| H3 | The maximum useful residence extension is bounded by the Jupiter-Saturn synodic period: at ≥ 19.85-yr extension every window becomes accessible (modulo Jupiter cycling), but the practical-cost ceiling is more like 2-3 yr before mission-duration impact dominates. | At 3-yr residence-extension budget: viable fraction at ±5° ≥ 0.70. | Falsified if fraction at 3-yr budget is < 0.50 or > 0.85. |
| H4 | Campaign-mean delivered fraction at 1-yr residence-budget recovers most of the Jupiter-gravity-assist benefit: ∈ [0.18, 0.21]. | Campaign-mean at 1-yr budget: ~0.20. | Falsified if < 0.17 or > 0.22. |
| H5 | Mission-duration impact at the campaign level: under skip-unaligned for Jupiter alignment, average residence time is half of budget. At 1-yr budget that's +0.5 yr per mission, on a 13.5-yr round-trip — a 3.7 percent mission extension. | Mission-duration impact at 1-yr budget: 3-4 percent extension. | Falsified if < 2 percent or > 6 percent extension. |

---

## Method

**Model.** Same coplanar-circular Sun-Earth-Jupiter-Saturn model as Blocks 5 and 6. Inbound trajectory: Hohmann ellipse from Saturn aphelion (9.55 astronomical units) to Earth perihelion (1.0 astronomical units), descending leg crosses Jupiter at true anomaly 216.4° about 4.63 years after Saturn-exit. Chunk's Jupiter-crossing heliocentric longitude is anchored to Saturn-exit position.

**Residence-time as a free parameter.** For each launch n in [0, 57], sweep Saturn-residence duration over a fine grid [0.5, 3.5] years at 0.05-year resolution. Residence-extension budget B means the campaign accepts residence ∈ [0.5, 0.5 + B] years.

**Per-launch viable test.** Window n is "Jupiter-viable at tolerance T° within residence-budget B years" if any residence-time τ ∈ [0.5, 0.5 + B] yields |chunk-Jupiter separation at Jupiter-crossing| ≤ T°. Phase-average over 360 Jupiter initial-phase samples.

**Tolerance and budget sweep.**
- Tolerances: ±2°, ±5°, ±10°, ±15°.
- Residence-extension budgets: 0.0, 0.25, 0.5, 1.0, 2.0, 3.0 years.

**Campaign-mean delivered fraction.** For each (tolerance, budget) pair, weighted average of 21.8% (Jupiter-aligned) and 15.5% (no Jupiter).

**Mission-duration impact.** For each viable window at each budget, record the *minimum* residence extension that achieves alignment. Average over viable windows to get the campaign-mean residence extension. Express as percent of total round-trip (13.5 years).

**Control.** At budget = 0, viable fraction at ±5° should be 2.78% (Block 5 baseline).

**Outputs.**
- `results/per_window_min_extension.csv` — per-launch: minimum residence extension to achieve alignment at each tolerance.
- `results/viable_fraction_grid.csv` — phase-averaged viable fraction at each (tolerance, residence-budget) pair.
- `results/campaign_mean_grid.csv` — campaign-mean delivered fraction at each pair.
- `results/duration_impact.csv` — average residence extension per viable mission, by (tolerance, budget) pair, with percent-of-round-trip.
- `results/summary.json` — hypothesis adjudication.

---

## Limitations of this model

- **Radiation dose to electronics not modeled.** Saturn-radiation-dose-vs-electronics-lifetime is a pending open round (R-saturn-side-residence-radiation in titan's pending list). At residence radii inside the magnetosphere (Saturn's main-radiation-belt envelope is ~3-12 Saturn radii), dose accumulates rapidly. The chunk's residence orbit (B-ring at ~1.5 Saturn radii) is inside this; multi-year residence may be electronics-killing. Not bookkeept in this round.
- **Station-keeping fuel for extended residence.** The ram-scoop residence orbit requires active station-keeping against Saturnian gravity perturbations. Block 4's mass budget assumed 0.5 yr; extending to 2-3 yr requires either more fuel or a different residence-orbit choice. Not bookkeept here.
- **Operations-team standing-cost.** Each extra year of residence is a year of ground-team labour and tracking-network use. Not bookkeept here.
- **Earth-arrival alignment.** Extending residence shifts the Earth-arrival epoch. A real campaign must also satisfy Earth-arrival geometry (Earth in the right place when the chunk reaches 1.0 AU). This round assumes Earth-arrival is a separately-tunable parameter, which is approximately true under a continuous-thrust inbound but not under strict Hohmann. Flagged as an approximation.
- **Synodic-window slipping.** The campaign launches at every Earth-Saturn synodic window (1.035 yr); extending residence by N years means the chunk arrives at Earth N years later than nominal. Other ships launched later in the campaign overtake it in delivery order. This is a programmatic logistics question, not a physics question.

---

## Decision rule

If H2 holds (Jupiter-viable fraction at ±5° and 1-yr residence-budget ≥ 0.30):
- Residence-time-flexibility is the missing Jupiter-gravity-assist lever. Block 5's verdict needs partial revision: Jupiter alignment is achievable at ~30% of launches via residence extension. The composite steady-state delivered fraction rises from ~16% toward ~19-20%.
- Per-mission cost: residence extension averages ~0.5 yr per Jupiter-aligned mission. Bookkeep in the demand model as mission-duration extension.

If H2 falsified low (< 0.20):
- Residence-time-flexibility doesn't help much either. Block 5's verdict is robust across all three trajectory-degree-of-freedom levers tested (cruise reshape, Saturn-exit Δv, residence time). Composite steady-state stays at ~16%.

If H2 falsified high (> 0.55):
- Residence-time-flexibility is so powerful that the campaign should plan around it as a primary lever. Re-elevate Jupiter return gravity-assist to central-case status. Demand model and concept-of-operations need significant rewrites.

---

## Results

### Hypothesis adjudication

| # | Prediction | Realized | Status |
|---|---|---|---|
| H1 | Saturn-Jupiter relative phase shift per residence-year ∈ [15°, 22°] | 18.13° | **held** |
| H2 | Viable fraction at ±5° / 1-yr extension ≥ 0.30 | 7.81% | **falsified low** |
| H3 | Viable fraction at ±5° / 3-yr extension ∈ [0.50, 0.85] | 17.88% | **falsified low** |
| H4 | Campaign-mean delivered fraction at ±5° / 1-yr ∈ [0.18, 0.21] | 15.99% | **falsified low** |
| H5 | Mission-duration impact at ±5° / 1-yr ∈ [2%, 6%] | 2.63% | **held** |

Block 5 reproduction (budget = 0, ±5°): 2.78% — sanity check passed.

### Viable-fraction grid (phase-averaged)

| Tolerance | Budget 0 yr | 0.5 yr | 1 yr | 2 yr | 3 yr |
|---|---|---|---|---|---|
| ±5°  | 2.78% | 5.29% | 7.81% | 12.84% | 17.88% |
| ±10° | 5.56% | 8.07% | 10.59% | 15.62% | 20.66% |
| ±15° | 8.33% | 10.85% | 13.37% | 18.40% | 23.43% |

### Campaign-mean delivered fraction (phase-averaged)

| Tolerance | Budget 0 yr | 1 yr | 2 yr | 3 yr |
|---|---|---|---|---|
| ±5° | 15.68% | 15.99% | 16.31% | 16.63% |

### Mission-duration impact (% of 12.6-yr round trip)

| Tolerance | Budget 1 yr | 2 yr | 3 yr |
|---|---|---|---|
| ±5° | 2.63% | 6.35% | 10.21% |

---

## Findings (this round)

**Finding 19 — Residence-time-flexibility is a linear lever, weaker than expected.** Each year of residence extension shifts Saturn-Jupiter relative geometry by 18.1°, widening the effective Jupiter-alignment tolerance window. The closed-form analytic limit is **viable_fraction = (2 × tolerance + 18.1° × budget_years) / 360°**. The realized phase-ensemble matches this analytic limit to within 0.3 percentage points.

**Finding 20 — Practical residence-extension cost to reach Jupiter-alignment-ubiquity is prohibitive.** To reach 30% viable fraction at ±5° tolerance requires residence extension of (108°-10°)/18.1° ≈ 5.4 years (47% mission-duration increase). To reach 50% requires ~9.4 years (84% mission-duration increase). These are programmatically unacceptable — they push the round-trip from 13.5 to 19-23 years.

**Finding 21 — Campaign-mean delivered fraction at the realistic 1-yr residence-budget is 15.99%, still below Option A's 17%.** Residence-time-flexibility provides 31 basis points of uplift (15.68% → 15.99%) at 2.63% mission-duration cost. The lever exists but is weak; Block 5's verdict (composite ~16%, Option-A-equivalent not -superior) is robust across all three trajectory-degree-of-freedom levers tested.

**Finding 22 — None of the three Block 5/6/7 levers materially fixes Jupiter-GA availability.** Summary of the three counter-questions:

| Lever | Block | Δv cost | Viable fraction at ±5° | Campaign-mean delivered fraction |
|---|---|---|---|---|
| (Block 5 baseline: no lever) | 5 | 0 | 2.78% | 15.68% |
| Cruise reshape (±13.5° self-consistent) | 5 | 2.5 km/s | 7.50% | 15.97% |
| Saturn-exit Δv flexibility | 6 | 1.0 km/s | 3.48% | 15.72% |
| Residence-time-flexibility (1 yr) | 7 | 0 (calendar 2.6%) | 7.81% | 15.99% |

The best single lever buys ~5% additional viable fraction, at meaningful cost (Δv or mission-duration). Combined optimization (joint cruise-reshape × residence-extension) would likely give modestly higher coverage but with cumulative costs. **The structural conclusion stands: Jupiter return gravity-assist is not a load-bearing operational lever; composite architecture steady-state delivered fraction is ~16%.**

---

## Methodology lesson 9

**"Three-body alignment availability scales linearly in any single trajectory-degree-of-freedom that costs delta-velocity or calendar time, with the proportionality constant set by the relative-orbital-motion rate between the constraint bodies."** For Saturn-Jupiter alignment, this constant is 18.1°/yr or ~5°/km/s in cruise reshape. To compensate for a missing degree of freedom (such as choosing launch year directly, which is not available because Earth-Saturn synodic only repeats every 1.035 yr), the cost in the available degrees grows linearly. Going from 2.78% to 50% viable requires ~25× the budget — almost always programmatically infeasible.

---

## Wrap-up of the three-round Jupiter-GA sub-campaign

Blocks 5, 6, and 7 form a sub-campaign that tests the load-bearingness of Jupiter return gravity-assist in three ways:
- **Block 5:** Cruise-reshape Δv. Self-consistent ±13.5° tolerance, 7.5% viable.
- **Block 6:** Saturn-exit Δv flexibility (perihelion 0.5-1.0 AU). Marginal — adds ~0.6 percentage points.
- **Block 7:** Residence-time-flexibility. Adds ~5 percentage points per year of extension.

**Conclusion (cumulative):** Jupiter return gravity-assist is structurally not reliably available. The composite architecture's steady-state delivered fraction is ~16% (vs Block 4's 21.8% best-window claim), making the residence-class architecture Option-A-equivalent rather than Option-A-superior. The pivot from chunk-graze to ram-scoop residence remains justified on **physical-feasibility** grounds (Option A's chunk-graze was independently falsified by physics), not on **delivered-fraction-headline** grounds.

This sub-campaign is closed.

---

## Status

All work pre-registered before running. Five hypotheses adjudicated; H1 and H5 held, H2/H3/H4 falsified low (lever weaker than predicted). Block 5's verdict survives the third (and most promising) counter-question. The three-round Jupiter-GA sub-campaign is closed; orchestrator integration should treat composite steady-state at ~16% as the headline number.

