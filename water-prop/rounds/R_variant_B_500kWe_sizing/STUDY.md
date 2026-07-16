# R-variant-B-500kWe-sizing — clean closure on the chemical-kick + electric-inbound surviving cell at 500, 750, 1000 kilowatt-electric

**Status:** pre-result.

## Question

R-megawatt-marvl-radiator (rhea) left Variant B (chemical-kick + electric-inbound) standing as the single surviving architecture cell once the Modular Assembled Radiators for Very Large systems-anchored mass model was applied. Rhea's report:

- Variant B closes inside L0-05 with positive delivered mass under MARVL-anchored mass at reactor power **≥ 500 kilowatt-electric** (5× Fission Surface Power Phase 2 scope).
- Rhea ran one specific-impulse / chunk / Modular-Assembled-Radiators-anchored configuration at 500 kilowatt-electric and reported "closes." Numerical headlines (round-trip time, delivered mass, propellant split between chemical kick and electric inbound, stage masses) were not produced — rhea's run.py only reported the survival fact.

This round produces the missing numerical closure for Variant B at 500 kilowatt-electric and brackets against 750 and 1000 kilowatt-electric to show the slope. Specifically:

- Round-trip time decomposition (Hohmann cruise × 2, Saturn ops, electric inbound burn).
- Delivered chunk mass and delivered fraction.
- Propellant split: chemical-kick delta-velocity for trans-Saturn injection + Saturn capture, electric inbound delta-velocity at the matrix-impulsive 6.42 kilometers-per-second.
- Stage masses: tug dry mass (Modular-Assembled-Radiators-anchored decomposed mass model), chemical kick stage dry mass, chemical-kick propellant mass, electric propellant mass.
- Low-Earth-orbit launch-mass multiplier (mission-1 single-shot vs depot-staged repeat-mission asymptote).
- Programmatic-risk-adjusted expected delivered mass per Round A's matrix overlay propagation.

## Pre-registered hypotheses

See `HYPOTHESES.md` for the full block (added in same commit). Summary:

- **H-vbs-a (500 kilowatt-electric closure round-trip):** round-trip time at 500 kilowatt-electric, MARVL-anchored mass, chunk 200 tonnes, specific impulse 2000 seconds, chemical-kick delta-velocity 9 kilometers-per-second, electric-inbound delta-velocity 6.42 kilometers-per-second. Pre-registered: **12.5–14.5 yr.** Point estimate 13.5 yr.
- **H-vbs-b (500 kilowatt-electric delivered mass):** delivered chunk mass per mission. Pre-registered: **80–110 tonnes.** Point estimate 95 tonnes.
- **H-vbs-c (slope to 1000 kilowatt-electric):** at 1000 kilowatt-electric / chunk 200 tonnes, MARVL-anchored mass, same delta-velocities. Round-trip time and delivered mass should improve modestly. Pre-registered: round-trip 12.0–13.5 yr (point 12.7 yr); delivered 100–125 tonnes (point 110 tonnes). The matrix-impulsive 6.42 kilometers-per-second is fixed by the chemical-kick architecture; only inbound burn time varies with reactor power.
- **H-vbs-d (low-Earth-orbit launch mass single-shot, 500 kilowatt-electric):** total mass at low-Earth-orbit including tug, kick stage, kick propellant. Pre-registered: **350–550 tonnes.** Point estimate 450 tonnes. (Compared against matrix's 6.9× multiplier figure for mission 1.)
- **H-vbs-e (programmatic-risk-adjusted delivered mass at 500 kilowatt-electric, uniform prior from Round A):** the closure-conditional delivered mass at 500 kilowatt-electric weighted by P(500 kilowatt-electric class reactor on orbit by 2035, uniform prior) = 0.0013. Pre-registered range: **0.10–0.15 tonnes per mission.** Point estimate 0.12 tonnes per mission. (This is the matrix-overlay propagation. Round A's H-pbu-e was the same metric; here it's done with the actual measured conditional, not pre-registered.)

Aggregate prediction: Variant B at 500 kilowatt-electric closes with ~13–14 yr round-trip and ~95 t delivered, giving a clean technical-conditional headline that the matrix can quote alongside its programmatic-risk-adjusted ~0.12 t / mission expected value. The slope to 1000 kilowatt-electric is shallow (10% improvement on round-trip, 15% on delivered mass) — the architecture is compute-bound by the impulsive inbound and propellant-bound by the chemical-kick mass ratio, not power-bound.

## Method

**Architecture.** Variant B = chemical-kick outbound + chunk-fed electric inbound. Three stages:

1. **Chemical kick stage** (jettisoned at Saturn arrival). Hydrolox engines (specific impulse 450 seconds). Provides chemical delta-velocity for trans-Saturn injection and Saturn capture. Pre-registered chemical delta-velocity: 9 kilometers-per-second total (matches matrix's all-electric-outbound baseline figure used as an apples-to-apples comparison against rhea's 29.56 kilometers-per-second continuous-thrust outbound; the chemical kick's impulsive nature preserves Oberth-bonus efficiency that the continuous-thrust electric outbound loses). Stage dry mass 10 tonnes (matches `R_chunk_fed_chemical/run.py`'s M_CHEM_DRY_KG).
2. **Tug dry mass** (Modular-Assembled-Radiators-anchored decomposed model from rhea: m_fixed 5 t, alpha_reactor 33 W/kg, alpha_PC 50 W/kg, alpha_radiator 0.047 kW_th/kg, eta_conv 0.30, f_tank 0.05). At 500 kilowatt-electric this gives ~52.6 t tug dry mass before propellant.
3. **Electric inbound** at the matrix-impulsive 6.42 kilometers-per-second. Chunk-fed (water electrolyzed in situ to specific impulse 2000 seconds). Wet-at-start mass = tug + chunk; chunk drops as inbound propellant is consumed.

**Round-trip-time decomposition.** Outbound is chemical-kick + Hohmann cruise (chemical kick is impulsive, so off-budget for time — the kick is delivered in minutes; the cruise is the Hohmann transfer time of 6.05 years). Saturn operations 1 year. Inbound = electric burn time at 6.42 kilometers-per-second + Hohmann cruise (6.05 years). Total = 6.05 + 1.0 + electric-inbound-burn-yr + 6.05 = 13.1 + electric-inbound-burn-yr.

**Closure check.** Round-trip ≤ 15 years AND delivered chunk mass > 0.

**Reactor sweep.** 500, 750, 1000 kilowatt-electric. Rationale: 500 is the survival floor from rhea; 1000 is the matrix's megawatt baseline; 750 anchors the slope between them.

**Low-Earth-orbit launch mass.** Mission-1 single-shot: all chemical-kick propellant launched from low Earth orbit. Compute as kick-propellant-mass × Tsiolkovsky for the 9 kilometers-per-second chemical kick + tug + kick-stage-dry. Mission-N depot-staged: chemical-kick propellant supplied by depot at low Earth orbit (matrix's "1.3× multiplier" footnote). Both reported.

**Programmatic-risk overlay.** Multiply closure-conditional delivered mass by Round A's `p_500kWe_orbit_by_2035` per prior (uniform 0.0013, Jeffreys 0.0003, skeptical 0.0001).

## Validity caveats

1. **Chemical-kick delta-velocity = 9 kilometers-per-second is the all-electric-outbound figure, not the actual Variant B chemical-kick figure.** A real Variant B chemical kick uses a low-Earth-orbit-departure burn (≈ 3.6 kilometers-per-second to trans-Saturn injection) plus a Saturn-arrival capture burn (≈ 1.4 kilometers-per-second to Saturn-orbit insertion). Total impulsive ≈ 5 kilometers-per-second, not 9. Using 9 here as a conservative bound — actual mass-ratio is more favorable. Sensitivity: at 5 kilometers-per-second instead of 9, the chemical-stage propellant mass shrinks from ~7× tug-mass to ~3× tug-mass, dropping low-Earth-orbit launch mass roughly in half. This round reports both the conservative-9 figure and a 5-kilometers-per-second sensitivity row.

2. **Matrix-impulsive 6.42 kilometers-per-second inbound assumes chemical-kick architecture preserves Oberth-bonus efficiency.** Rhea's R-megawatt-marvl-radiator footnote states this is valid for the chemical-kick architecture. This round inherits the assumption and does not re-derive it. If the inbound electric burn cannot fully exploit the impulsive-equivalent figure (because it is electric, not impulsive), the actual continuous-thrust inbound delta-velocity is closer to titan's 24.7 kilometers-per-second, and the closure surface collapses to roughly the megawatt all-electric end-to-end shape. Treat the 6.42 figure as the architectural-aspiration value, not a measured one.

3. **Chemical-stage dry mass 10 tonnes is `R_chunk_fed_chemical/run.py`'s number, not re-derived.** Realistic dry-mass-fraction for hydrolox kick stages is 0.10–0.15 of wet propellant mass; at 9 kilometers-per-second / Isp 450 s, the propellant mass is large enough that 10 tonnes of dry stage may be light. Sensitivity not run; flagged for follow-up.

4. **Modular-Assembled-Radiators-anchored mass model assumes radiator areal density at the standard ~3 kilograms-per-square-meter and reactor / power-conversion at the National Academies 2021 / NASA Modular Assembled Radiators for Very Large systems midpoints.** Round B identified that closure-threshold-implied areal densities for the megawatt all-electric cell are sub-1-kilogram-per-square-meter — physically infeasible. Variant B at 500 kilowatt-electric does not need that low; the implied radiator at 500 kilowatt-electric Modular-Assembled-Radiators-anchored is ~25 tonnes for ~1.16 megawatt-thermal of waste heat (specific impulse 2000 s, eta = 0.3), which corresponds to ~390 square meters at 64 watts-thermal-per-square-meter (consistent with deployable). No areal-density gate failure at this scale — flagged but not blocking.

5. **No Lunar Gravity Assist credit applied.** Rhea's Sweep B applied Lunar-Gravity-Assist credit for both legs; this round does not. The chemical-kick architecture is less sensitive to the credit because outbound burn time is essentially zero; on the inbound, the impulsive-equivalent 6.42 kilometers-per-second already implicitly credits the Saturn-system Oberth bonus. Reapplying Lunar-Gravity-Assist on top would double-count.

6. **500-kilowatt-electric scale-up gap** (Round A's P_500_FUNDED_GIVEN_FSP = 0.6, gap mean 4 yr) is author-asserted, not data-derived. The H-vbs-e overlay number inherits this uncertainty.

## Result

Ran Variant B at 500 / 750 / 1000 kilowatt-electric, MARVL-anchored mass, chunk 200 t, specific impulse 2000 s, electric-inbound 6.42 kilometers-per-second matrix-impulsive, both conservative chemical-kick (9 kilometers-per-second) and realistic chemical-kick (5 kilometers-per-second) scenarios. Full table in `results/tables.md`; raw in `results/R_variant_B_500kWe_sizing.json`.

**Conservative chemical-kick (9 kilometers-per-second):**

| Reactor (kWe) | Tug dry (t) | Kick prop (t) | LEO mission-1 (t) | LEO mission-N (t) | Inbound prop (t) | t_inbound (yr) | Round-trip (yr) | Delivered (t) | Fraction | Strict 15? | Soft 16? | Expected (uniform, t) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:--:|:--:|---:|
| **500** | **58.6** | **458.6** | **527.1** | **68.6** | **72.2** | **1.35** | **14.53** | **127.8** | **0.639** | **yes** | **yes** | **0.1661** |
| 750 | 83.9 | 628.0 | 721.9 | 93.9 | 79.3 | 0.99 | 14.16 | 120.7 | 0.604 | yes | yes | 0.1569 |
| 1000 | 109.3 | 797.4 | 916.7 | 119.3 | 86.3 | 0.81 | 13.98 | 113.7 | 0.568 | yes | yes | 0.1478 |

**Realistic chemical-kick (5 kilometers-per-second; 3.6 trans-Saturn injection + 1.4 Saturn capture):**

| Reactor (kWe) | LEO mission-1 (t) | (other columns identical to conservative) | Round-trip (yr) | Delivered (t) | Strict 15? | Soft 16? |
|---:|---:|---|---:|---:|:--:|:--:|
| **500** | **213.0** | (tug, t_inbound, delivered identical) | 14.53 | 127.8 | yes | yes |
| 750 | 291.6 | … | 14.16 | 120.7 | yes | yes |
| 1000 | 370.3 | … | 13.98 | 113.7 | yes | yes |

**The realistic chemical-kick scenario halves LEO mission-1 launch mass at 500 kilowatt-electric from 527 t to 213 t** while leaving round-trip time and delivered mass unchanged (chemical kick is impulsive, off the time and delivered-mass budgets).

**Pre-registration grading (against conservative 9 kilometers-per-second scenario):**

| Sub-claim | Predicted | Measured | Held? |
|---|---|---|---|
| H-vbs-a — 500 kWe round-trip | 12.5–14.5 yr (point 13.5) | **14.53 yr** | **FALSIFIED** by 0.03 yr — at the edge of the range |
| H-vbs-b — 500 kWe delivered mass | 80–110 t (point 95) | **127.8 t** | **FALSIFIED** optimistic by 16% |
| H-vbs-c — 1000 kWe slope (round-trip 12.0–13.5 AND delivered 100–125) | both ranges | round-trip 13.98 yr, delivered 113.7 t | **FALSIFIED** — round-trip outside range, delivered inside range |
| H-vbs-d — 500 kWe LEO mission-1 launch mass | 350–550 t (point 450) | **527.1 t** | **HELD** |
| H-vbs-e — 500 kWe expected delivered, uniform prior | 0.10–0.15 t (point 0.12) | **0.1661 t** | **FALSIFIED** optimistic by 11% |

## Reading

**Variant B at 500 kilowatt-electric closes well — better than I pre-registered.** Round-trip 14.53 yr (within ±1 yr soft margin per user clarification), delivered 127.8 t (0.64 fraction), tug dry 58.6 t. The cell is genuinely the surviving architecture under MARVL-anchored mass, and it survives with more headroom than rhea's "barely closes" framing implied.

**Three findings worth surfacing:**

1. **Delivered fraction at 500 kilowatt-electric is 0.64** — substantially better than rhea's R-megawatt-marvl-radiator's "delivered fraction 70% → 20%" titan-corrected baseline. Why? The matrix-impulsive 6.42 kilometers-per-second inbound at specific impulse 2000 s gives a mass ratio of only 1.39, consuming 28% of wet mass on inbound propellant. Over a 200 t chunk + 58.6 t tug = 258.6 t wet, that's 72.2 t propellant — leaves 127.8 t delivered. **The architecture's value comes from preserving impulsive-equivalent inbound delta-velocity through the chemical-kick architecture choice.** If that preservation breaks (caveat 2 in the STUDY.md), this collapses to titan's 24.7 kilometers-per-second continuous-thrust delta-velocity, and delivered mass goes to ~0.

2. **Slope to 1000 kilowatt-electric is shallow.** Round-trip improves from 14.53 → 13.98 yr (−0.55 yr) and delivered drops from 127.8 → 113.7 t (−14 t) as reactor power doubles. The negative-delivered slope is because tug mass grows linearly with reactor power (MARVL-anchored ~10 W/kg for the bundled stack), eating into wet-mass headroom on the inbound. **The 500 kilowatt-electric reactor is at the optimum for delivered mass per mission under this configuration; going higher costs delivered mass.** This is the cleanest argument for why Variant B does NOT benefit from pushing toward megawatt-class — it's optimized at the survival floor, not above it.

3. **Realistic chemical-kick delta-velocity (5 kilometers-per-second) cuts LEO mission-1 launch mass by 60%** at 500 kilowatt-electric (527 t → 213 t). This is the launcher-selection finding. At 213 t LEO mission-1, a SpaceX Starship-class fully-reusable vehicle (claimed ~150 t to LEO, single-launch) needs 1–2 launches per mission; at 527 t, it needs 4. The matrix's 6.9× launch-mass multiplier footnote should be revisited with the realistic chemical-kick figure: at 500 kilowatt-electric / chunk 200 t, mission-1 multiplier is 213 / 200 = 1.07× under realistic chem-kick (essentially a wash) versus 527 / 200 = 2.6× under conservative.

**Programmatic-risk overlay.** Expected delivered mass at 500 kilowatt-electric, integrated over reactor-availability uncertainty:

- Uniform Beta(1, 7) prior: **0.166 t per mission**
- Jeffreys Beta(0.5, 6.5) prior: **0.038 t per mission**
- Skeptical Beta(0.5, 11.5) prior: **0.013 t per mission**

This is roughly 2.7× higher than Round B's megawatt all-electric end-to-end expected value at the closure threshold (0.06 t / mission uniform), reflecting the 500-kilowatt-electric-class's higher availability probability (5× scope grow vs 25×) AND Variant B's higher closure-conditional delivered mass. **Variant B is the genuinely lower-risk surviving cell on programmatic-risk-adjusted basis, not just the technically-feasible one.**

But the absolute numbers are still small. 0.17 t per mission uniform is ~170 kg of water delivered to LEO per mission averaged over reactor-availability uncertainty. That is not commercially interesting in any frame. **The matrix's surviving cell is technically defensible but commercially load-bearing only if the orchestrator explicitly conditions on reactor program success in its presentation, which Round A flagged is doing more conditioning work than is normal in propulsion architecture trade studies.**

## Revisit

**Pre-registration accuracy: 1 of 5 held.** Worst pre-registration of the three rounds, but in a different direction than Round B — here the misses are mostly optimistic-falsifications (delivered mass higher than predicted, expected value higher than predicted). I pre-registered 95 t delivered against the actual 127.8 t because I implicitly anchored on rhea's "barely closes" language and assumed the surviving cell would be a marginal one. It is not — it is comfortably in closure with substantial headroom on delivered fraction.

**Source of the error.** I did not back-of-envelope the inbound mass ratio at the matrix-impulsive 6.42 kilometers-per-second figure. With specific impulse 2000 s and inbound delta-velocity 6.42, the mass ratio is e^(6420 / 19620) ≈ 1.39 — modest. A 30-second computation would have shown delivered fraction ~0.6, not the 0.4 I implicitly anchored on from rhea's "barely closes." Same recurring lesson as Round B (back-of-envelope each binding constraint before pre-registering ranges); third instance in three rounds. **The lesson is real and I am not applying it consistently.**

**The 9-kilometers-per-second chemical-kick figure** (used for hypothesis grading) is the conservative bound per the STUDY.md caveat. Realistic figure 5 kilometers-per-second was reported but not used for grading because pre-registration was anchored on the conservative number. If I'd graded against the realistic figure, H-vbs-d (LEO launch mass) would have measured 213 t — well below the 350-550 t pre-registered range, falsified pessimistic. The conservative-bound choice was load-bearing for the one held hypothesis.

**The "shallow slope" finding (H-vbs-c falsified)** is the genuinely informative result — round-trip improves modestly from 500 → 1000 kilowatt-electric AND delivered mass DROPS. Pre-registration anchored "round-trip improves and delivered improves" implicitly, against a measured "round-trip improves marginally and delivered degrades 11%." This is a structural finding about Variant B optimization that the matrix should note: **the optimum is at the survival floor, not above it.** Future reactor-power scaling for Variant B should be motivated by something other than delivered-mass-per-mission (e.g., mission throughput, redundancy, secondary-power applications), because at the architecture level more reactor doesn't buy more delivered chunk.

**Caveat 2 (matrix-impulsive 6.42 kilometers-per-second is architectural-aspirational)** is the dominant unmodeled risk. If chemical-kick architecture cannot in fact preserve Oberth-bonus impulsive efficiency for the inbound burn — i.e., if the inbound electric burn is fundamentally a continuous-thrust burn not an impulsive one — then inbound delta-velocity is closer to titan's 24.7 kilometers-per-second, and the cell collapses to roughly the megawatt all-electric end-to-end shape (negative delivered, round-trip ≥ 17 yr at 1 megawatt-electric). This caveat is the cliff this entire analysis sits on. A future round (R-variant-B-impulsive-vs-continuous) should rebuild the inbound delta-velocity from first principles for the chemical-kick architecture and report whether 6.42 is justified or whether the figure is closer to 18–22 kilometers-per-second once continuous-thrust losses are properly accounted.

## Cross-learning

- **Confirms `water-prop/docs/ARCHITECTURE-DECISION-MATRIX.md` "Year 0–15 deployment path: 500-kilowatt-electric chemical-kick + electric-inbound" cell with stronger numerical anchors.** Round-trip 14.53 yr (in soft-margin closure), delivered 127.8 t (0.64 fraction), tug dry 58.6 t MARVL-anchored, LEO mission-1 launch mass 213 t (realistic chem-kick) or 527 t (conservative chem-kick). The matrix's "≤ 200 t chunk for L0-05 compliance" line is correct; this round confirms 200 t closes with substantial headroom at 500 kilowatt-electric.
- **Negative for the matrix's 6.9× LEO launch-mass multiplier footnote** when applied to Variant B specifically. Realistic chem-kick figure (5 kilometers-per-second) gives mission-1 multiplier = 1.07× at 500 kilowatt-electric / 200 t chunk. The 6.9× figure is a worst-case bound for higher-delta-velocity all-electric outbound architectures. Matrix should split the multiplier into per-architecture rows.
- **Negative for the matrix's "going to 1000 kilowatt-electric is upside" implicit framing.** This round shows delivered mass DROPS from 500 → 1000 kilowatt-electric Variant B. The optimum reactor power for delivered-mass-per-mission under Variant B is at or below 500 kilowatt-electric. **Variant B does not benefit from megawatt-class scale-up.** If megawatt is desired for other reasons (mission cadence, secondary applications, future-architecture insurance), document those reasons explicitly — don't justify it on delivered-mass grounds.
- **Surface caveat 2 (6.42 kilometers-per-second inbound is architectural-aspirational) as the dominant unmodeled risk on the matrix's surviving cell.** Recommend orchestrator schedule a follow-up R-variant-B-impulsive-vs-continuous round to validate or invalidate this assumption from first principles. If invalidated, Variant B collapses to roughly the megawatt all-electric end-to-end shape and the matrix has no surviving cell.
- **Surface 500 kilowatt-electric scale-up gap parameters (Round A's P_500_FUNDED_GIVEN_FSP = 0.6, gap mean 4 yr) as author-asserted for orchestrator review.** These dominate the H-vbs-e overlay number; they should either be defended with vendor-roadmap evidence or sensitivity-tested across plausible alternatives.
- **Recurring lesson #N elevated to third instance.** Pre-registration must back-of-envelope each binding constraint AND each headline metric before naming a numeric range. Three rounds, three instances; treat as a systematic discipline failure on hyperion-2's part rather than three independent slips. Recommend orchestrator fold into a campaign-level lessons file.
- **Methodology note: dual-conservative-vs-realistic scenario reporting is useful.** This round's split between conservative chem-kick (9 km/s, used for hypothesis grading) and realistic chem-kick (5 km/s, reported in tables) gave a meaningful additional finding (60% LEO launch-mass reduction) without adding much complexity. Recommend future architecture-sizing rounds adopt the same pattern when a key parameter has a well-defined conservative bound.

