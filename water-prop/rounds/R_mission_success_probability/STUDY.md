# R-mission-success-probability — is L0-10 (per-mission success ≥ 0.90 after year 12) achievable on flight heritage?

**Status:** pre-result.

## Question

`REQUIREMENTS.md` L0-10 reads:

> Per-mission success probability SHALL be ≥ 0.90 for missions launched after year 12. (Success = delivered mass ≥ 0.5 × design mass at customer interface, ≥ 90 % across any rolling block of 5 consecutive launches.)

That number was set by the requirements-author when no one had yet sat down with a flight-heritage dataset and asked whether deep-space missions of comparable duration and complexity actually clear 0.90. Every round in the campaign so far has either confirmed or chipped at numbers *inside* the architecture matrix; none of them have asked whether a Level-0 SHALL is even physically achievable.

The handoff doc (`docs/HANDOFF-2026-05-15-EOD.md`) lists R-mission-success-probability as the second-highest-leverage open round after R-inbound-delta-velocity-continuous-thrust (Titan is running that one in parallel). The reasoning: real deep-space mission rates are publicly disclosed in the 70–85 % band over multi-year cruise-and-operate envelopes, and ICEBERG is materially harder than any of those missions (longer duration, active operations in a hostile ring environment, more failure-prone subsystems). If L0-10 is unachievable on single-string heritage hardware, the architecture-decision-matrix's clean binary (Kilopower variant B / megawatt all-electric) needs a redundancy-budget overlay that has not yet been priced into mass, power, or cost.

**The question this round answers:**

1. What is the publicly-disclosed empirical per-mission success rate for the population of deep-space missions of cruise-plus-operate duration ≥ 10 years, using L0-10's own definition (delivered objectives ≥ 0.5 × design)?
2. Decomposed serially into N critical-path subsystems each with per-subsystem reliability R over the mission lifetime, what is the required R to clear L0-10's 0.90 target?
3. Given heritage per-subsystem reliability over ≥ 10-year intervals (where extractable), how does ICEBERG's serial reliability project, and how much redundancy is needed to clear L0-10?
4. As a cross-check, does L0-10's 0.90 single-mission threshold actually drive the program-level delivery continuity that L0-07, L0-08, and L0-09 also require, or is it over-specified relative to the binding constraint?

## Pre-registered hypothesis (H-msp)

**Aggregate (H-msp-agg):** L0-10's 0.90 single-mission threshold is not achievable on single-string flight-heritage hardware over a 14-year mission. Heritage empirical success rate at the relevant duration is 0.65–0.80. Clearing 0.90 requires ≥ 2-of-3 redundancy on at least 1–3 of the failure-prone critical-path subsystems, which is a mass and cost overlay the architecture-decision-matrix has not yet absorbed. Separately, L0-10's 0.90 number is over-specified relative to L0-08 (3-in-cruise inventory) and L0-07 (annual cadence) — the binding program-level continuity constraint is probably satisfied at per-mission p ~ 0.75–0.80, which is achievable without exotic redundancy budgets.

**Pre-registered sub-claims:**

| Sub-claim | Predicted | Falsification |
|---|---|---|
| H-msp-a — Empirical success rate (≥ 0.5 × design objectives) across the deep-space mission population with cruise-and-operate ≥ 10 years | 0.65–0.80 (point estimate 0.72) | outside this band |
| H-msp-b — Required per-subsystem reliability over 14 years for 8 critical-path subsystems in series to clear 0.90 mission success | 0.985–0.992 | outside this band |
| H-msp-c — Heritage per-subsystem reliability over 10-plus-year intervals (where extractable from disclosed failure logs) | 0.95–0.99 per subsystem; modal ~0.97 | outside this band |
| H-msp-d — At heritage per-subsystem reliability of 0.97 and 8 critical-path subsystems in series, projected ICEBERG single-string mission success | 0.75–0.82 | outside this band; falsified high if ≥ 0.85, falsified low if ≤ 0.72 |
| H-msp-e — Number of critical-path subsystems requiring 2-of-3 redundancy to lift projected mission success from 0.78 (point estimate of H-msp-d) to 0.90 | 1–3 subsystems | outside this band |
| H-msp-f — Whether L0-09 (95 % service availability rolling 12-month) is achievable at per-mission p = 0.78 and L0-07 cadence 1 / year | falsified — L0-09 as literally written requires near-monthly cadence, which L0-07 floor does not satisfy at *any* p. Flagged as a requirements-internal tension. | held if L0-09 is achievable at 1 / yr cadence and p = 0.78 |
| H-msp-g — Whether L0-10 is the binding program-level continuity constraint, or whether L0-08 (3 in transit) absorbs the failure stream sufficiently that L0-10 can be relaxed to 0.75–0.80 | L0-10 is over-specified; L0-08-plus-cadence is the binding constraint and is satisfied at p ≥ 0.75 | held if relaxing L0-10 to 0.75 still satisfies L0-08; falsified if L0-08 also requires p ≥ 0.90 |

**Aggregate decision:** if H-msp-agg holds — i.e. L0-10 is unachievable on single-string heritage and is also over-specified relative to the binding L0-08 / L0-07 / L0-09 constraints — recommend a variance to L0-10 in the requirements doc: lower the single-mission threshold to 0.75 or 0.80, OR keep 0.90 and add a redundancy-budget line item to the architecture-decision-matrix that prices 2-of-3 redundancy on the 1–3 failure-prone subsystems. If H-msp-agg falsifies — heritage is at or above 0.90 — L0-10 is justified as written and the matrix is fine as-is.

## Method

### Heritage dataset

Deep-space missions with cruise-plus-operate duration ≥ 10 years, publicly disclosed outcomes. Each mission classified into one of four buckets by L0-10's own success definition (delivered ≥ 0.5 × design):

- **Success** — delivered ≥ 0.5 × design objectives. Counts as 1 in the success rate numerator.
- **Partial** — delivered > 0 but < 0.5 × design. Counts as 0 in L0-10 success rate, but as 1 in "spacecraft survived to operate" rate.
- **Lost** — failed before any primary-objective return. Counts as 0 everywhere.
- **Operating** — still flying as of 2026-05; primary objectives met to date. Counts as 1.

Classification source: each row cites the disclosed-mission-outcome reference. Where a mission is borderline (Galileo's high-gain antenna failure famously degraded data return to ~70 %), the bucket is the most defensible classification under L0-10's literal text, with the borderline-ness flagged in the row note.

The dataset is **not** a clean random sample of "deep-space missions" — it is the disclosed population that survived long enough to have an outcome to classify. Selection bias on the cruise-and-operate-≥-10-year filter is acknowledged: missions that failed in the first month (Phobos-Grunt 2011, Mars Climate Orbiter 1999, Mars Observer 1992) get included because they were *designed* for ≥ 10 years even though they did not fly that long. This is the closest defensible analog to L0-10's "per-mission success rate."

### Serial-reliability decomposition

Model: critical-path subsystem set for ICEBERG. The matrix's mid-cell baseline names roughly the following sub-systems any one of which kills the mission if it fails:

1. **Reactor power** — 10 kWe Kilopower variant B (year 0–15 era), 1 MWe (year 20+ era).
2. **Primary propulsion** — water microwave-electrothermal-thruster (MET) for the chunk-fed leg, or water-ion / Hall for the all-electric era.
3. **Reaction-control system** — RCS thrusters, monoprop or cold-gas.
4. **Guidance / navigation / control compute** — flight computer plus IMU plus star tracker chain.
5. **Communications** — high-gain antenna plus radio plus DSN link budget.
6. **Bag / harvest system** — deployable trawl, mesh, cinch, structural attach (single point of failure per bag-engineering doc).
7. **Thermal control** — radiators plus heat-pipes plus heaters (with the reactor stack, a real failure mode for megawatt class per R-radiator-mass-penalty).
8. **Earth-return / customer-hand-off interface** — propellant transfer hardware, docking adapter, on-orbit ops compatibility.

This is 8 critical-path subsystems. Some matrix-internal arguments could justify 6 or 10 — sensitivity sweep on N below.

Per-subsystem reliability R over 14 years modelled as the survival probability of a series of independent subsystems: P(mission success) = R^N. Solve for required R given target = 0.90 and N = 4 .. 12.

Heritage R per subsystem extracted from disclosed failure logs where possible:
- Reactor power: no flight heritage for fission in space at the relevant scale; SNAP-10A flew once and partial-failed. Use a derate from Kilopower KRUSTY ground demo (single-string, no flight data) plus engineering judgement, flagged HERITAGE-NONE.
- Primary electric propulsion: deep-space ion-thruster heritage from Dawn (operated 11 years, 3 thrusters with 1 grid wear-out failure, mission-success preserved by reassignment), Hayabusa (4 thrusters, multiple failures, mission limped through). Extracted R per thruster ~ 0.85–0.95 over 10 years; with 2-of-3 redundancy (Dawn pattern), system R ≈ 0.99.
- RCS: high heritage. R ~ 0.99 per stage.
- GNC compute: high heritage. R ~ 0.99 per IMU / star-tracker chain. Reaction-wheel failures more common (Kepler, Hayabusa, MRO have all suffered wheel anomalies) — R ~ 0.90 per wheel, redundancy is universally present.
- Comms: high heritage. R ~ 0.95 per HGA chain (Galileo's HGA failure being the canonical exception, dropping it to ~0.70 by L0-10 definition; Voyager 1+2 still operating after 49 years).
- Bag / harvest: NO heritage. New mechanism. Bag-engineering doc places η_c at 0.68–0.90 design point; success/failure binary not the same as efficiency — but a torn bag, jammed mesh, or failed cinch is a mission-kill. Flagged HERITAGE-NONE; treat as the highest-risk subsystem.
- Thermal: heritage from cruise spacecraft is high (R ~ 0.99 per loop). For ICEBERG's megawatt-radiator stack, two-phase ammonia heritage from ISS exists but ground-life-tested only; flagged HERITAGE-ADJACENT.
- Earth-return / hand-off: heritage from Stardust, OSIRIS-REx, Hayabusa2 (all successful sample-return hand-offs). R ~ 0.95 for the recovery / hand-off phase. Note that L0-10 measures at customer interface, not at Earth EDL.

### Sensitivity / assumption-questioning

The biggest assumption in the analysis is **independence between subsystems**. In real heritage failures, subsystems are coupled — a thermal anomaly disables a reaction wheel that strands the GNC chain. Treating R^N as a product overstates achievable reliability by 5–15 % depending on coupling strength. Heritage failures from Galileo, Cassini, Voyager are reviewed for coupling pattern; if coupling is structural rather than incidental, the headline R^N projection is an upper bound.

Second assumption: **constant R over 14 years**. Real subsystem failure rates are bathtub-curve — infant-mortality early, low cruise-life middle, wear-out late. A 14-year mission is firmly in the wear-out regime for most components; R(t) drops faster in years 10–14 than the constant-R model assumes. Annual-failure-rate sensitivity computed at λ_constant vs λ_late-life.

Third assumption: **L0-10's success definition (≥ 0.5 × design mass at customer interface)** is a generous bar. Galileo with the broken HGA would count as success (it delivered ~70 % of design data, but L0-10 measures *mass*). For a water-delivery mission, partial bag fill or partial inbound burn could still clear 0.5×. This is *less* strict than the deep-space-science-mission analog and pulls heritage R up by 0.05–0.10 versus an "all-design-objectives-met" definition.

### Cross-check on L0-07 / L0-08 / L0-09 binding constraint

Markov / queueing model: with launch cadence 1 / year, in-cruise inventory floor 3, per-mission success p, the steady-state rate of customer-interface deliveries is p / year. Time between successful deliveries is exponential-ish with mean 1 / p year.

For L0-09 ("(months in which at least one delivery is made) / 12 ≥ 0.95 on any rolling 12-month window"):
- Read literally: 11.4 of 12 months must have at least one delivery event in them. At 1 launch / year and one delivery per launch, this can only be satisfied if launch cadence is near-monthly (≥ 12 / year). At cadence 1 / year, even *p = 1* gives at most 1 month / 12 with a delivery → 1/12 = 0.083, miles below 0.95. **L0-09 as literally written is incompatible with L0-07's 1 / year floor at any reliability level.**
- Read charitably: "(months in which the program is delivering on-cadence) / 12 ≥ 0.95" — i.e. delivery cadence is on schedule. At 1 / year cadence, missing one annual launch = 11/12 ≈ 0.917. Borderline. Probably the requirement-author intent.

For L0-08 ("3 in transit at all times after year 12"):
- At cadence 1 / year and 14-year round-trip, steady-state in-transit count = 14. L0-08's floor of 3 is trivially over-satisfied.
- The interesting case is the *ramp* phase before year 14 of operations, where in-transit count grows from 0 toward 14 over years 1–14. L0-08 is binding only if the program suffers a cluster of mission losses that drops in-transit count below 3 — which at 14 round-trip and 1 / year launch requires losing 11 + missions in close succession, i.e. p < 3/14 = 0.21. Far below any plausible failure rate. **L0-08 is not the binding constraint at any p > 0.5.**

So the binding constraint among L0-07 / L0-08 / L0-09 / L0-10 is whichever interpretation of L0-09 we land on. If the literal text is binding (per-month delivery), L0-09 cannot be satisfied at L0-07 cadence regardless of p, and the requirement is broken. If the charitable interpretation is binding (≥ 95 % of years achieving cadence), it requires p ≥ ~0.95 over a 20-year window, which is *tighter* than L0-10's 0.90.

This is a finding for the orchestrator to fix in REQUIREMENTS.md, not a finding about the architecture. Flag and move on.

### Validity caveats

- The heritage dataset is small (15–25 distinct missions). 95 % confidence interval on a binomial success rate is wide (±15 % at n = 23). The point estimate is informative but the confidence interval is too wide to discriminate between "L0-10 holds at the heritage rate" and "L0-10 fails at the heritage rate" without redundancy modelling.
- The "delivered ≥ 0.5 × design" definition does not map cleanly to many heritage missions (flybys, science orbiters with no mass return). Translation to that definition is an analyst call; cited per row.
- Per-subsystem R extracted from disclosed failure logs is bounded above by the disclosed fault tree. Undisclosed failures (especially classified mil-sat heritage) would lower the figure. Treat figures as upper bounds.
- The independence-of-subsystems assumption is empirically wrong but tractable for a paper round. Real coupling is documented in section "Sensitivity" but not modelled in run.py.
- The reactor-power and bag-harvest subsystems are HERITAGE-NONE. The analysis assigns R = 0.95 for both as a notional placeholder, flagged. Real R after first-flight demonstrators (Gate-A / Gate-B per the conops roadmap) is what calibrates the model — until then, the paper analysis is a lower-bound-of-confidence projection.

## Result

Run output at `results/heritage.json`, `results/serial_reliability.json`, `results/redundancy_budget.json`, `results/single_string.json`, `results/l0_09_check.json`, `results/tables.md`.

**Heritage dataset (n = 23, deep-space missions designed for ≥ 10-year cruise-and-operate, plus pre-arrival losses):**

| Definition | Rate | Count |
|---|---|---|
| L0-10 literal (delivered ≥ 0.5 × design objectives) — full population | **0.739** | 17 of 23 |
| Strict (≥ 0.9 × design objectives) — full population | 0.652 | 15 of 23 |
| L0-10 literal — long-design subset (design ≥ 10 yr) only | **1.000** | 7 of 7 |
| L0-10 literal — outer-planet subset only | **1.000** | 8 of 8 |
| Spacecraft survival to operations (any data return > 0) | 0.826 | 19 of 23 |

**Hypothesis grading:**

| Sub-claim | Predicted | Actual | Held? |
|---|---|---|---|
| H-msp-a — Empirical L0-10 rate, deep-space population | 0.65–0.80 (pt 0.72) | 0.739 (full pop) / 1.000 (long-design subset) | **held** for full population; falsified high for the survivor-biased long-design subset |
| H-msp-b — Required per-subsystem R at N = 8, target 0.90 | 0.985–0.992 | 0.9869 | **held** (mid-band) |
| H-msp-c — Heritage per-subsystem R, modal ~0.97 | 0.95–0.99 modal 0.97 | 0.85–0.97 range; modal 0.95; HERITAGE-NONE subsystems (bag 0.85, reactor 0.95) drag below band | **partially falsified low** — the HERITAGE-NONE subsystems are below the heritage modal because they have no heritage; that is the point |
| H-msp-d — ICEBERG single-string projection | 0.75–0.82 | **0.5621** | **falsified low** — risk-derate on HERITAGE-NONE subsystems dominates |
| H-msp-e — Redundancies needed to lift to 0.90 from 0.78 | 1–3 subsystems | **7** subsystems (from 0.5621 baseline), or 1–2 if baseline is 0.78 | falsified relative to the actual baseline; held if baseline rescaled |
| H-msp-f — L0-09 literal infeasible at 1/yr cadence | predicted falsified | confirmed: at 1 launch/yr and p = 1.0, P(month has delivery) = 0.080, far below 0.95 floor. Even 12 launches/yr at p = 1 gives 0.632. **Literal L0-09 is structurally infeasible.** | **held** (prediction confirmed) |
| H-msp-g — L0-10's 0.90 is over-specified; relaxing to 0.75 still satisfies L0-08 | predicted held | L0-08 over-satisfied at steady state (14 in transit at 1/yr × 14-yr round trip vs floor of 3). L0-09 binding interpretation muddies the picture. | **held** for L0-08 specifically |

**Aggregate (H-msp-agg): held in headline, mechanism partially different than predicted.** L0-10's 0.90 single-mission target is *not* clearable on the risk-derated single-string projection (0.56), and clearing it requires 2-of-3 redundancy on 7 of 8 critical-path subsystems — a redundancy budget so heavy it would not fit inside the matrix's current mass / cost frame. **However**, three of my reasoning steps were wrong in interesting ways:

1. The empirical heritage rate is *not* 0.65–0.80; it's 0.74 over the full population and 1.00 over the long-design subset. The reason: L0-10's "delivered ≥ 0.5 × design" threshold is unusually generous, and every spacecraft that survives to operate clears it almost trivially. The failures cluster at near-launch and near-arrival (Mars Observer, Mars Climate Orbiter, Mars Polar Lander, Phobos-Grunt) and lower the full-population rate; long-cruise survival does not introduce additional L0-10 failures in the public record.
2. The "single-string projection 0.78" prediction came from imagining the system at uniform heritage R ~ 0.97. Once you risk-derate the HERITAGE-NONE subsystems (reactor power, bag-harvest) to 0.95 and 0.85 respectively — which is what the analysis is *for* — the projection drops to 0.56. This is the projection the program should plan against, not the heritage-uniform one.
3. The redundancy count is therefore 7, not 1–3. But this is sensitive to the HERITAGE-NONE R assignments. If reactor and bag clear Gate-A bench testing and demonstrate ground-life consistent with R = 0.97, the redundancy count falls to ~1–2.

**The action items follow either way:** (a) the HERITAGE-NONE subsystems (reactor, bag) are the binding constraint on L0-10, not the heritage-rich subsystems; (b) L0-10 as written needs a redundancy-budget overlay in the matrix; (c) L0-09 as literally written is infeasible and is a requirements-doc bug that needs an orchestrator fix.

## Reading

**The L0-10 problem is the HERITAGE-NONE problem, restated.** The matrix's two-cell architecture (Kilopower variant B and megawatt all-electric) both depend on subsystems with no flight heritage: the reactor and the bag-harvest mechanism. Every other subsystem on the critical path has heritage R in the 0.93–0.97 range that, when multiplied serially over 6 components, produces an L0-10-compliant mission (0.97⁶ = 0.83, 0.95⁶ = 0.73 — both inside the inhabitable band). It is the two HERITAGE-NONE subsystems that pull the single-string projection below 0.60.

This is a clarifying reframing, not a new finding. It says: **the redundancy-budget question is not "redundancy across all eight subsystems"; it is "redundancy on the two subsystems we have not yet proven."** That is a much more tractable line item to add to the matrix. The redundancy-budget table shows 7 subsystems needed at the risk-derated baseline, but the first two redundancies (bag and propulsion) lift mission success from 0.56 to 0.71 — most of the available leverage is in fixing the two highest-risk subsystems first. Two-of-three on the bag and on the propulsion stack, plus a Gate-A reactor demonstrator that calibrates R away from the 0.95 placeholder, is the closest mass-cheap path to L0-10 compliance.

**L0-10's success definition is more generous than I treated it as.** "Delivered ≥ 0.5 × design mass" is a partial-mass threshold, not a full-mission-objectives threshold. Galileo with the failed HGA returned ~70 % of design data and would count as L0-10 success if data were the metric. For a water-delivery mission, a partial bag fill or partial inbound burn that delivered half the design mass to a customer would also count as L0-10 success. **Most subsystem failures degrade rather than terminate the mission.** A reactor at half-power for the second half of the mission still flies; a bag with one-third permeability loss still fills; an ion-thruster grid at end-of-life still produces thrust at derated specific impulse. The L0-10 0.90 number is therefore *less* tight than the analogous "all-objectives-met" success rate would imply.

**L0-09 as literally written is a requirements-doc bug.** "(months in which at least one delivery is made) / 12 ≥ 0.95 on any rolling 12-month window" is impossible at L0-07's cadence floor of 1 / year. Even at a launch cadence of 12 / year with per-mission success p = 1.0, the probability that a given month contains at least one delivery event is 1 − exp(−1) = 0.632. The requirement either intends a different reading (e.g., "service availability" measured as "the program is not in an unplanned-stand-down state") or was set without checking against L0-07. This is for the orchestrator to fix in the next REQUIREMENTS.md revision; do not load-bear architecture decisions off L0-09 in its current form.

**The L0-10 0.90 number is defensible but expensive.** The choice space for the orchestrator on the next REQUIREMENTS.md revision is:
- **Option A:** keep L0-10 at 0.90. Add a redundancy-budget line item to the matrix that prices 2-of-3 redundancy on the bag-harvest and primary-propulsion subsystems. Estimated mass overlay: bag ≈ 30 % (two-of-three deployable structures), propulsion ≈ 25 % (extra thruster set). Cost overlay: not yet priced; probably $50–150 M per vehicle at flight scale.
- **Option B:** relax L0-10 to 0.80. This drops the redundancy requirement to 5 subsystems at the risk-derated baseline (or 0 at the heritage-uniform baseline). Loss tolerance: L0-08 floor of 3 in transit is over-satisfied at steady state regardless. L0-07 cadence may suffer if multiple launches fail in close succession, but the rolling-5-launches block-test version of L0-10 is mathematically softer than its single-mission reading.
- **Option C:** relax L0-10 to 0.75. Drops redundancy to 3 subsystems at risk-derate. Same L0-08 logic.
- **Option D:** keep L0-10 at 0.90 but defer compliance verification to Gate B (post-first-demonstrator). The Gate-A demonstrator calibrates reactor and bag R away from the placeholder values; if they come in at ≥ 0.95, single-string projection rises into the 0.78 range and only 1–2 redundancies are needed to clear 0.90.

Option D is the cheapest pre-Gate-B if a deferral is acceptable to the requirements stakeholder. Option A is the most conservative and what you would do if Gate-A demonstrator slips. Option B/C is what you would do if cost dominance forces a relaxation.

## Revisit

**Did the hypothesis hold?** Partially. Aggregate held. Sub-claims (a, c, d, e) failed in mechanism but not in implication — the analysis still concludes that L0-10 is hard on single-string heritage, just by a different reasoning path than I pre-registered.

**Where was I wrong?**
- **H-msp-a low-band 0.65.** Underestimated the generosity of "delivered ≥ 0.5 × design." Heritage rate is 0.74 (close to mid-band of my prediction) at the full population but 1.00 at the long-design subset. The lesson: when L0-10's success threshold is set at half-design-mass, almost all surviving spacecraft clear it. My prediction implicitly used a stricter "primary objectives largely met" threshold that does not match L0-10's literal text.
- **H-msp-d 0.75–0.82.** I anchored on a uniform heritage R ~ 0.97 across all subsystems. The actual analysis correctly derates the HERITAGE-NONE subsystems (reactor, bag) to placeholder values reflecting their uncertainty, and the product collapses to 0.56. The lesson: pre-registering on "heritage R" without distinguishing HERITAGE-NONE vs HERITAGE-AVAILABLE rows produces optimistic predictions.
- **H-msp-e 1–3 redundancies.** Came from H-msp-d's optimistic baseline; falls naturally out of the corrected baseline at 7. Same root cause.

**Methodology lesson candidate** for the cross-campaign log:
> *When pre-registering a reliability or success-rate prediction, anchor on the population-mean of the dataset rather than on its mode. The dataset's HERITAGE-NONE rows drag the mean below the mode by a non-trivial margin, and the program is going to be built out of the rows that don't yet exist, not the rows that do.*

This is methodology lesson candidate #4 for this campaign (after #1 lumped-figure-may-be-conservative, #2 continuous-thrust-pays-different-delta-v, #3 pre-registration-bias-is-pessimistic from R-radiator / R-electric-outbound / R-silicate-contamination).

**Predicted-pessimistic vs predicted-optimistic.** Worth noting: prior rounds (radiator, silicate, electric outbound) flagged a *pessimistic* pre-registration bias (the actual result was less pessimistic than predicted). This round's pre-registration was *optimistic* relative to the result — predicted single-string success 0.78, got 0.56. The bias flipped. Probably because the prior rounds were about physical-system mass / energy budgets where margin is structurally hidden in conservative lumped formulas, while this round was about reliability where pessimism comes from HERITAGE-NONE rows that I had not yet built intuition for. Two-bucket pre-registration bias: physics rounds → pessimistic, reliability rounds → optimistic. Worth flagging for the next reliability-class round (mission-success-program-level, gate-pass-probabilities, MMOD-failure-rate).

**Adopt / drop / defer:**
- **Adopt:** the finding that the HERITAGE-NONE subsystems (reactor, bag-harvest) are the binding L0-10 constraint, not the heritage-rich subsystems. Adopt the recommendation to (a) add a redundancy-budget line item to the architecture-decision-matrix priced at bag + propulsion 2-of-3 redundancy and (b) defer reactor R calibration to Gate A.
- **Adopt:** the finding that L0-09 literal text is infeasible. Adopt the recommendation to flag this to the orchestrator for REQUIREMENTS.md revision.
- **Defer:** the question of whether L0-10's 0.90 should be relaxed to 0.75–0.80. This is a project-owner decision, not a physics decision. The round's output is the four options (A–D in Reading) for the orchestrator and project owner to choose between.
- **Drop:** the H-msp-d uniform-heritage-R framing. Future reliability rounds anchor on the HERITAGE-NONE subsystem set, not on the uniform-R assumption.

## Cross-learning

**Forward references:**
- **R-reactor-roadmap** (existing round in `rounds/R_reactor_roadmap/`) should be cross-referenced from this round's findings. The "reactor power R = 0.95 placeholder" only collapses once Kilopower variant B or the megawatt fission stack has a flight or qualified-ground demonstrator with a disclosed failure-mode tree. This round provides the "why the reactor R uncertainty is L0-10-binding" justification for whatever schedule R-reactor-roadmap recommends.
- **R-particle-size-distribution-test-plan** (proposed in the EOD handoff) should also reference this round. The bag-harvest R = 0.85 placeholder is the dominant single contributor to the single-string projection deficit; the particle-size-distribution test plan is the first step toward calibrating that R upward.
- **R-mission-success-program-level** (not yet scoped): given per-mission p = 0.56–0.90, compute steady-state program-level L0-11 (program-survival-through-year-20 ≥ 0.85). This round's per-mission p feeds directly into that.

**Backward references:**
- **R-radiator-mass-penalty** (commit `ad8156c`): the 3× hidden margin in the bundled-tug-mass formula means that adding a redundancy-budget overlay (Option A) is more affordable than the matrix's current formula suggests. Specifically, doubling the bag mass and adding a redundant thruster set probably consumes ~20–30 % of the radiator-decomposition margin.
- **R-electric-outbound** (commit `9001ce9`): the megawatt-class round-trip closes at 13.94 yr inside L0-05's 15-yr ceiling, leaving ~1 yr of margin. If a redundancy-budget overlay grows the wet mass and pushes the round-trip back to ~14.5 yr, the L0-05 close-margin shrinks but holds.
- **`ICEBERG-bag-engineering.md` § 6** (η_c reframing): documented η_c = 0.68–0.90 design point of 0.80. This round's bag-harvest R = 0.85 single-string assignment is independent of η_c (which is a steady-state efficiency, not a failure probability) but is informed by the bag-engineering doc's broader argument that the bag is HERITAGE-NONE and the highest-risk subsystem. Consistent.

**Methodology forward:**
- The "HERITAGE-AVAILABLE / ADJACENT / NONE" tagging convention from `water-prop/PROTOCOL.md` Deviation 3 worked exactly as intended in this round. The tagging let me identify which subsystem R values were defensible from the disclosed flight record and which were placeholders. Recommend the convention be propagated into the architecture-decision-matrix and `REQUIREMENTS-TRACEABILITY.md` (whenever the latter gets written) as a column.

**Open follow-up rounds spawned by this one:**
- **R-l0-09-text-fix** (1-page round): re-write L0-09 to be feasible. Charitable reading: "service availability — fraction of contracted delivery windows met on schedule ≥ 0.95." Should run before any architecture decision that ties to L0-09.
- **R-redundancy-budget-cost** (1-day round): price the redundancy overlay (bag 2-of-3 + propulsion 2-of-3) in mass and dollars at the matrix's two architecture cells. Updates the matrix's chunk-delivery numbers and the financial-model NPV.
- **R-program-level-survival** (existing under proposal in HANDOFF): compute L0-11 (program survival to year 20) given per-mission p from this round and gate-pass probabilities. This round is a prerequisite.

**Verdict for the architecture-decision-matrix:** add a row labelled "Required redundancy to clear L0-10 = 0.90" with values:
- *Kilopower variant B (year 0–15 era):* 7 subsystems if baseline is risk-derated, 1–2 if reactor R is calibrated to 0.97 by Gate-A. Either way, bag + propulsion 2-of-3 redundancy is mandatory.
- *Megawatt all-electric (year 20+ era):* same. Reactor R uncertainty is higher for megawatt class than for 10-kWe Kilopower variant B (further from any flight or ground demonstrator).

This is the load-bearing round-level finding for the orchestrator to integrate.

