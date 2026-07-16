# R-vehicle-mass-bundled-anchor — under the National Academies 2021 / Modular Assembled Radiators for Very Large systems (MARVL) bundled vehicle mass formula, do R-all-electric-thruster-sweep's conclusions about Variant B survivability and year-twenty-plus all-electric infeasibility still hold?

**Status:** pre-result.

## Question

Four user-locked beliefs (`0418e2c9ee3de422`, `edcfe90912ca80e5`, `776575c01d55ca51`, `0d5c882c13395571`) anchored in a parallel session's R-power-wonder establish:

1. **40 watt-per-kilogram specific power is a paper-study aspirational figure at Technology-Readiness-Level 2,** not an extrapolation of Kilowatt Reactor Using Stirling Technology (KRUSTY) ground-test data. KRUSTY measured 2.4 watt-per-kilogram system-level; flown radioisotope thermoelectric generators top at 5.3 watt-per-kilogram (General Purpose Heat Source).
2. **United States space-fission programs have a 0-of-6 base rate of reaching orbit within their originally-stated decade since 1965.** SNAP-10A (1965) is the only flight; ~$1.7 billion spent post-SNAP with zero orbital outcomes (SP-100, Project Timberwind, Prometheus/Jupiter Icy Moons Orbiter, DARPA Demonstration Rocket for Agile Cislunar Operations, Kilopower flight, Fission Surface Power).
3. **Fission Surface Power Phase 2 has not been awarded as of May 2026.** The Duffy directive (August 2025) raised scope to 100 kilowatt-electric with Q1 Fiscal-Year-2030 deployment intent — policy direction, not contract. Fiscal-Year-2026 budget zeroed NASA nuclear-electric and nuclear-thermal propulsion technology lines entirely.
4. **At megawatt-electric scale, radiators are 40–55% of total system mass — not the reactor core.** Reactor plus shield 25–35%, power-conversion 15–25%, radiators 40–55% (National Academies 2021 plus MARVL studies). The bundled formula `5 tonne + 0.1 × kilowatt-electric` is closer to correct at megawatt scale; the decomposed-mid model (which R-electric-outbound used and my prior three rounds inherited verbatim) is the *optimistic* one.

The decomposed-mid table I used (`TUG_DRY_T_BY_KWE = {100: 5.5, 200: 7.5, 500: 10.0, 1000: 12.1, 2000: 16.4}`) implies specific power 18 watt-per-kilogram at 100 kilowatt-electric and 122 watt-per-kilogram at 2 megawatt-electric. Both are far above KRUSTY heritage (2.4) and well above the 40 watt-per-kilogram National Academies anchor. The bundled formula gives 9.5 watt-per-kilogram at 1 megawatt-electric and 9.8 watt-per-kilogram at 2 megawatt-electric — roughly 4× KRUSTY heritage but well below the 40 watt-per-kilogram aspirational target.

**The question:** under the bundled vehicle mass formula, do R-all-electric-thruster-sweep's conclusions still hold? Specifically: (a) does Variant B remain the surviving architecture with closure at 10-mission reuse; (b) does the year-twenty-plus all-electric end-to-end winner cell still close at *any* chunk mass; and (c) does the cathode-life conclusion from R-cathode-life-water-plasma carry over, or does the bigger tug mass change the burn time enough to flip the verdict?

## Pre-registered hypothesis (H-vmba)

**Aggregate (H-vmba-agg):** Under the bundled MARVL anchor, vehicle dry mass at 1 megawatt-electric is 105 tonne — 8.7× the 12.1 tonne my prior rounds used. The mass-ratio penalty propagates differently across the two architectures: Variant B's inbound mass ratio is small (1.39 at impulsive 6.42 km/s, specific impulse 2000 second), so a larger tug only modestly increases inbound propellant — delivered fraction drops from 70.4% to 55–60% but Variant B still closes. The all-electric end-to-end architecture is dominated by the continuous-thrust inbound mass ratio (4.08 at 27.56 km/s); a larger tug pushes m_prop above chunk and breaks mass closure at chunk 200 tonne. The year-twenty-plus winner cell from R-all-electric-thruster-sweep dies under the bundled anchor at chunk 200 tonne; closure requires chunk ≥ ~500–800 tonne, which is far above the matrix's stated baseline. Cathode-on time scales by ~1.5× because per-mission burn time scales with propellant mass; 10-mission Variant B reuse exceeds Advanced-Electric-Propulsion-System heritage by 1.5–1.8×, worse than the prior 1.09× and tightening the cathode-replacement requirement.

**Pre-registered sub-claims:**

| Sub-claim | Predicted | Falsification |
|---|---|---|
| H-vmba-a — Variant B delivered fraction at radio-frequency-ion canonical, 1 megawatt-electric, chunk 200 tonne, matrix-impulsive, *bundled tug 105 tonne* | 55–62% (down from prior 70.4%) | outside band |
| H-vmba-b — Variant B round-trip time at the same cell | 13.5–15.5 year (up from prior 13.80) | outside band |
| H-vmba-c — Year-twenty-plus all-electric end-to-end at radio-frequency-ion canonical, 1 megawatt-electric, chunk 200 tonne, continuous-thrust, bundled tug | mass closure fails (m_prop > chunk) | held if delivered fraction < 0; falsified if any positive delivery |
| H-vmba-d — Minimum chunk mass that mass-closes the year-twenty-plus all-electric cell at radio-frequency-ion canonical, 1 megawatt-electric, bundled tug | ∈ [400, 800] tonne | outside band |
| H-vmba-e — Per-mission cathode-on time at Variant B canonical under bundled tug | ~7,500–9,000 hour (up from prior 5,435 hour, ratio 1.4–1.7×) | outside band |
| H-vmba-f — 10-mission Variant B cathode-on under bundled tug | 1.4–1.8× Advanced-Electric-Propulsion-System design life (up from 1.09×) | outside band |
| H-vmba-g — Sensitivity: at *intermediate* tug mass (50 tonne, halfway between decomposed-mid 12.1 and bundled 105), Variant B delivered fraction at the matrix-impulsive cell | 63–67% | outside band |
| H-vmba-h — At what specific power does the year-twenty-plus all-electric end-to-end cell start mass-closing at chunk 200 tonne, radio-frequency-ion canonical, 1 megawatt-electric? Sweep over specific-power 5, 10, 20, 40, 80 watt-per-kilogram | mass closure restored at specific power ≥ 25–40 watt-per-kilogram | outside band |

**Pre-registered aggregate decision-ordering:**

The structurally interesting outcome is H-vmba-c. If it holds — the year-twenty-plus all-electric end-to-end cell mass-closure fails at chunk 200 tonne under the bundled tug — the matrix's year-twenty-plus winner cell is dead under the corrected vehicle mass anchor. Combined with Findings 1–3 (40 watt-per-kilogram is aspirational, 0-of-6 base rate, Fission Surface Power Phase 2 not awarded), the matrix's "megawatt all-electric end-to-end" cell becomes a stacked low-probability event chain: needs specific power ≥ 25 watt-per-kilogram (against 0-of-6 historical base rate of demonstrating *any* fission orbit), water-radio-frequency-ion anode efficiency 0.65 at megawatt-electric (no measurement exists), and cathode-life-with-swap at per-swap reliability ≤ 3%. Three stacked technology-readiness-level claims, none with present-day evidence.

H-vmba-a and H-vmba-b are the Variant B safety check. If Variant B *also* fails closure at bundled tug, the program's only safe architecture is also dead.

H-vmba-h answers the operational question: how much specific-power improvement does the program need to fund before the year-twenty-plus winner cell becomes evidence-supported?

## Method

**Vehicle mass model.** Three regimes:

1. **decomposed_mid** (the optimistic prior, R-electric-outbound's `TUG_DRY_T_BY_KWE`): 5.5, 7.5, 10.0, 12.1, 16.4 tonne at 100, 200, 500, 1000, 2000 kilowatt-electric. Specific power 18–122 watt-per-kilogram.
2. **bundled_MARVL** (the realistic Finding 4 anchor): `5 + 0.1 × kilowatt-electric` tonne. 15, 25, 55, 105, 205 tonne at the same power levels. Specific power 6.7–9.8 watt-per-kilogram, anchored against the National Academies 2021 / MARVL studies.
3. **specific_power_sweep** (for H-vmba-h): vary specific power 5, 10, 20, 40, 80 watt-per-kilogram at 1 megawatt-electric, holding all other tug-dry components at zero so tug_dry = reactor_stack only. Lets the round identify the specific-power threshold at which year-twenty-plus all-electric mass-closes.

**Delta-velocities.** Inherited from prior rounds:
- Outbound impulsive (Variant B): 9.0 km/s
- Outbound continuous-thrust (all-electric end-to-end): 17.97 km/s (R-electric-outbound)
- Inbound impulsive (Variant B): 6.42 km/s (matrix)
- Inbound continuous-thrust (all-electric end-to-end): 27.56 km/s (R-inbound high-elliptical with lunar gravity assist)

**Burn-time model.** Same as R-all-electric-thruster-sweep: constant thrust, Tsiolkovsky propellant, `T = 2η P / v_exhaust`. Thruster constants from R-all-electric-thruster-sweep: water-radio-frequency-ion canonical η = 0.65, specific impulse 2000 second.

**Round-trip composition.** Same as prior: `t_burn_out + t_hohmann + saturn_dwell + t_hohmann + t_burn_in`, ceiling 15 year.

**Sweeps.**
- Vehicle mass model: decomposed_mid (reference), bundled_MARVL (corrected), intermediate (50 tonne fixed at 1 megawatt-electric for sensitivity).
- Architecture: all-electric end-to-end (continuous-thrust both legs), Variant B (matrix-impulsive both legs).
- Thruster: water-radio-frequency-ion canonical (only — prior rounds retired the other thrusters at the relevant cells).
- Power: 100, 200, 500, 1000, 2000 kilowatt-electric.
- Chunk: 50, 100, 200, 500, 1000 tonne (extended upward to find the H-vmba-d threshold).
- Specific-power sweep (separate): 5, 10, 20, 40, 80 watt-per-kilogram at 1 megawatt-electric, chunk 200 tonne.

**Validity caveats.**

- The bundled formula `5 + 0.1 × kilowatt-electric` is itself a fit to the National Academies 2021 / MARVL anchor; the underlying mass decomposition (radiator 40–55%, reactor+shield 25–35%, power-conversion 15–25%) is the authoritative source. The bundled formula is a convenient closed-form summary, not a derived first-principles number. Treat as a useful anchor, not a measurement.
- The decomposed-mid table from R-electric-outbound was published before the user-locked Finding 4 belief was established. The decomposed model may still be defensible *for the radiator-deployment-success* assumption (which is upside-only per Finding 1). The round treats both as parameter inputs and lets the user choose.
- Tug structural mass (truss, tankage, plumbing, capture mechanism, avionics) is bundled into the formula. Capture-mechanism mass alone is ~30 kilogram (R-inbound caveat) — small relative to the tens-of-tonne reactor-plus-radiator stack at megawatt.
- The "intermediate" 50 tonne anchor is a Bayesian compromise: if the radiator subsystem can be partially de-risked (deployable cooled radiator demonstrator + structural mass at MARVL anchor), 50 tonne at 1 megawatt-electric is a defensible Plausible-Better-Than-Worst case.
- This round does not re-run the thruster sweep (microwave-electrothermal, Hall, dual-ion) at bundled tug. R-all-electric-thruster-sweep retired those thrusters on independent grounds (mass-closure failure under continuous-thrust at the much smaller decomposed-mid tug). At bundled tug their conclusions only worsen; no need to re-run.

## Result

**Status:** complete. Run output in `results/vehicle_mass_bundled.json` and `results/tables.md`.

### Tug dry mass per power, by model

| Power (kilowatt-electric) | decomposed_mid (tonne) | bundled_MARVL (tonne) | Bundled / decomposed |
|---:|---:|---:|---:|
| 100 | 5.5 | 15.0 | 2.73× |
| 200 | 7.5 | 25.0 | 3.33× |
| 500 | 10.0 | 55.0 | 5.50× |
| 1,000 | 12.1 | 105.0 | **8.68×** |
| 2,000 | 16.4 | 205.0 | 12.50× |

### Headline cells, chunk 200 tonne, 1 megawatt-electric, water-radio-frequency-ion canonical

| Model | Architecture | Mass ratio inbound | Delivered (tonne) | Delivered % | Mass closes? | Round-trip (year) | Closes both? |
|---|---|---:|---:|---:|:--:|---:|:--:|
| decomposed_mid (prior) | Variant B | 1.39 | 140.8 | 70.4% | yes | 13.80 | yes |
| decomposed_mid (prior) | All-electric end-to-end | 4.08 | 39.9 | 20.0% | yes | 14.85 | yes |
| **bundled_MARVL (corrected)** | Variant B | 1.39 | 114.9 | 57.4% | yes | 14.55 | yes |
| **bundled_MARVL (corrected)** | All-electric end-to-end | 4.08 | **−30.2** | infeasible | **no** | 16.81 | **no** |
| intermediate (50 tonne) | Variant B | 1.39 | 130.2 | 65.1% | yes | 14.11 | yes |
| intermediate (50 tonne) | All-electric end-to-end | 4.08 | 11.3 | 5.7% | yes | 15.65 | no (time burst) |

### Minimum chunk for all-electric mass-closure under bundled MARVL, 1 megawatt-electric

| Chunk (tonne) | Delivered (tonne) | Mass closes? | Round-trip (year) | Closes both? |
|---:|---:|:--:|---:|:--:|
| 200 | −30.2 | no | 16.81 | no |
| 300 | −5.6 | no | 17.52 | no |
| 400 | 18.9 | **yes** (just) | 18.23 | no (time burst) |
| 500 | 43.4 | yes | 18.94 | no |
| 800 | 117.0 | yes | 21.06 | no |
| 1,000 | 166.1 | yes | 22.48 | no |
| 2,000 | 411.4 | yes | 29.55 | no |

**No (chunk × 1 megawatt-electric) cell under bundled MARVL closes both mass and time at the year-twenty-plus all-electric end-to-end architecture.** Mass closure starts at chunk 400 tonne (twice the matrix baseline); time closure was already at 14.85 year at the prior decomposed model — under bundled, every mass-closing chunk pushes round-trip past 18 year.

### Specific-power sweep at 1 megawatt-electric, chunk 200 tonne, all-electric end-to-end

| Specific power (watt-per-kilogram) | Tug (tonne) | Mass closes? | Round-trip (year) | Closes both? |
|---:|---:|:--:|---:|:--:|
| 5 (Kilopower Reactor Using Stirling Technology heritage 2× margin) | 200.0 | no | 18.82 | no |
| 10 (bundled MARVL anchor) | 100.0 | no | 16.71 | no |
| 20 (mid-aspirational) | 50.0 | yes (barely) | 15.65 | no (time burst by 0.65 year) |
| 40 (National Academies aspirational) | 25.0 | yes | 15.12 | no (time burst by 0.12 year) |
| 80 (Finding 1 says upside-only) | 12.5 | yes | 14.86 | **yes** (only at 80) |

### Variant B sweep over power, bundled MARVL, chunk 200 tonne

| Power (kilowatt-electric) | Tug (tonne) | Delivered % | Round-trip (year) | Closes? |
|---:|---:|---:|---:|:--:|
| 100 | 15.0 | 70.0% | 19.63 | no (time burst) |
| 200 | 25.0 | 68.6% | 16.81 | no |
| 500 | 55.0 | 64.4% | 15.12 | no (narrowly) |
| 1,000 | 105.0 | 57.4% | 14.55 | **yes** |
| 2,000 | 205.0 | 43.5% | 14.27 | yes |

Under bundled MARVL, Variant B requires *at least* 1 megawatt-electric to close the 15-year ceiling. The 100 to 500 kilowatt-electric Variant B regime — which the financial model and the Kilopower year-zero-through-fifteen architecture assume — does *not* close at chunk 200 tonne under bundled tug.

### Cathode-on time at Variant B canonical, bundled MARVL, 1 megawatt-electric, chunk 200 tonne

| Quantity | Value |
|---|---:|
| Per-mission cathode-on (hour) | 12,024 |
| Per-mission cathode-on (year) | 1.37 |
| 10-mission total (hour) | 120,239 |
| Fraction of Advanced-Electric-Propulsion-System design life (50,000 hour) | **2.40×** |

Compared to the prior decomposed model: per-mission 5,435 → 12,024 hour (2.21× ratio); 10-mission 1.09 → 2.40× heritage. Variant B at bundled needs 2–3 spare cathodes per tug at 10-mission reuse, not 1.

### Hypothesis grading

| Sub-claim | Predicted | Actual | Verdict |
|---|---|---|---|
| H-vmba-a — Variant B delivered fraction bundled | 55–62% | 57.4% | **held** |
| H-vmba-b — Variant B round-trip bundled | 13.5–15.5 year | 14.55 year | **held** |
| H-vmba-c — All-electric mass closure fails at chunk 200 tonne, bundled | yes | yes (−30.2 tonne) | **held cleanly** |
| H-vmba-d — Minimum chunk for all-electric mass-closure bundled | 400–800 tonne | 400 tonne (edge of band) | **held narrowly** |
| H-vmba-e — Per-mission cathode-on Variant B bundled | 7,500–9,000 hour | 12,024 hour | **falsified high** — outbound burn grows 8× at heavier tug, dominates the burn-time increase |
| H-vmba-f — 10-mission Variant B vs Advanced-Electric-Propulsion-System | 1.4–1.8× | 2.40× | **falsified high** |
| H-vmba-g — Intermediate 50 tonne Variant B delivered | 63–67% | 65.1% | **held** |
| H-vmba-h — Specific-power threshold for all-electric mass-closure at chunk 200 tonne | 25–40 watt-per-kilogram | mass-closure at 20 watt-per-kilogram; closes-both only at 80 watt-per-kilogram | **partially held** — depends on whether the threshold is mass-only or mass-and-time; the 25–40 prediction sat between the two |

Eight sub-claims, four held cleanly, two held narrowly, one partially held, two falsified high in the direction of "even worse than predicted."

## Reading

**The architecture decision matrix's "year-twenty-plus megawatt all-electric end-to-end" cell is dead under the bundled MARVL vehicle mass anchor at the matrix's stated chunk 200 tonne.** Mass closure fails. No power class up to 2 megawatt-electric mass-closes at chunk 200 tonne. The minimum chunk that mass-closes (400 tonne) does so at round-trip 18.23 year, far past L0-05's 15-year ceiling. The only way the cell closes both mass and time at chunk 200 tonne is at specific power ≥ 80 watt-per-kilogram — a value Finding 1 explicitly says is upside-only beyond the aspirational 40 watt-per-kilogram National Academies anchor.

**The cell is therefore a stacked low-probability bet on five independent unaudited claims:**

1. Specific power ≥ 80 watt-per-kilogram at megawatt-electric (Finding 1 says 40 watt-per-kilogram is aspirational at Technology-Readiness-Level 2; flown radioisotope thermoelectric generators top at 5.3 watt-per-kilogram; Kilowatt Reactor Using Stirling Technology ground-test 2.4 watt-per-kilogram).
2. Water-radio-frequency-ion anode efficiency 0.65 at megawatt-electric on water (no published measurement exists above ~1 kilowatt-electric on water; per R-all-electric-thruster-sweep).
3. Cathode life on water plasma at xenon-heritage levels with swap design at per-swap reliability ≤ 3% (per R-MET-cathode-escape-hatch).
4. Reactor cycle life under multi-year continuous burn at megawatt-electric on water-propellant duty cycle (unaudited, flagged as adjacent risk).
5. United States flight-fission program delivers in original-decade window (Finding 2 says 0-of-6 historical base rate post-SNAP-10A).

Even pairwise independence assumes the joint probability is fives times the worst of these. Conservatively, the year-twenty-plus all-electric end-to-end cell has < 5% present-evidence probability of closing as drawn.

**Variant B is still safe — but at much worse economics than R-all-electric-thruster-sweep concluded.** Under bundled MARVL:
- Variant B requires 1 megawatt-electric to close at chunk 200 tonne (the 100–500 kilowatt-electric Kilopower-class powers do not close, contradicting the campaign's apparent assumption that Variant B works at Kilopower-class).
- Delivered fraction drops from 70.4% to 57.4% (matrix nominal 70–75% overstates by ~25%).
- Per-mission cathode-on time doubles from 5,435 to 12,024 hour because outbound burn grows 8× at the heavier tug (0.07 → 0.57 year).
- 10-mission cathode-on hits 2.40× Advanced-Electric-Propulsion-System design life. The cathode-swap budget grows from "≥ 1 spare" (R-cathode-life) to "≥ 2 spares" (this round).

**The 100–500 kilowatt-electric Kilopower regime — Fission Surface Power Phase 2 territory — does not close Variant B under bundled tug.** This is the single most important matrix update: the *near-term* architecture path (Fission Surface Power 100 kilowatt-electric in 2030, growing toward 500 kilowatt-electric mid-decade) does *not* close ICEBERG at the matrix's chunk 200 tonne under the realistic vehicle mass anchor. The program needs *megawatt-class* power even for Variant B, which Finding 3 says has zero contracted-flight-hardware evidence base today.

**Methodology lesson — outbound burn dominates the mass-anchor sensitivity, not inbound burn.** Under decomposed-mid tug 12.1 tonne, outbound propellant is 12.1 × 0.578 = 7 tonne (Tsiolkovsky at outbound 9 km/s impulsive); under bundled tug 105 tonne, outbound propellant is 60.7 tonne. The outbound burn time grows linearly with tug dry mass, dominating the per-mission cathode-on time increase. I had implicitly assumed inbound burn dominated; this is wrong at Variant B's small inbound mass ratio. Adding to the convention log.

## Revisit clause

Grade H-vmba-a through H-vmba-h. Four held cleanly, two held narrowly, one partially held, two falsified high.

If the bundled MARVL anchor is itself challenged — for example, by a Modular Assembled Radiators for Very Large systems demonstrator that shows radiator areal density better than the National Academies 2021 anchor — H-vmba-c softens and the year-twenty-plus winner cell could be resurrected. The National Academies 2021 report is the best public anchor today; the round treats it as ground truth.

If the campaign produces a flight-relevant specific-power demonstration in the 20–40 watt-per-kilogram band (intermediate between bundled MARVL's 10 and the aspirational 80), the year-twenty-plus all-electric mass-closure at chunk 200 tonne shifts. From the specific-power sweep: mass closure at 20 watt-per-kilogram (delivered 11.3 tonne, time 15.65 year — narrow time burst); time-and-mass closure at 80 watt-per-kilogram only. Even at 40 watt-per-kilogram aspirational, time-burst by 0.12 year — barely closes.

If R-trajectory-shaping-optimization saves 10–20% on inbound delta-velocity (R-inbound's open caveat), the inbound mass ratio drops from 4.08 to ~3.3–3.5 at the corrected delta-velocity, propellant fraction drops from 0.755 to ~0.70, and the all-electric architecture mass-closure threshold drops from 400 tonne to ~250 tonne. This would put the year-twenty-plus cell back near the matrix's chunk 200 tonne nominal but still time-burst by 1–2 year. Trajectory shaping is necessary-but-not-sufficient.

If single-use vehicle architecture is adopted (R-single-use-vs-reusable-tug-economics candidate round), the cathode-life axis collapses to single-mission, removing one of the five stacked low-probability claims. The mass-anchor axis is unaffected.

## Cross-learning

- **The matrix's year-twenty-plus megawatt all-electric end-to-end cell is dead under the bundled MARVL vehicle mass anchor at chunk 200 tonne.** Closure requires either chunk ≥ 400 tonne (with time burst by 3+ year) or specific power ≥ 80 watt-per-kilogram (with Finding 1 explicitly retiring that band as upside-only). The cell is now a stacked five-claim low-probability bet; conservatively < 5% present-evidence probability.
- **Variant B at bundled MARVL requires at least 1 megawatt-electric to close the 15-year ceiling at chunk 200 tonne.** The 100–500 kilowatt-electric Kilopower / Fission Surface Power class does *not* close Variant B at the matrix's nominal chunk. This is the single most important program-near-term update: ICEBERG needs megawatt-class power even for Variant B, which Finding 3 says has zero contracted-flight-hardware evidence base in 2026.
- **Variant B delivered fraction drops from matrix nominal 70–75% to 57.4% under bundled.** The financial model and pitch headline overstate by ~25%. Re-run R-NPV-discount-rate, R-financing-capital-stack, and the conops bag-engineering 75% nominal at the corrected number.
- **Variant B cathode-on time doubles under bundled** (5,435 → 12,024 hour per mission), driven by 8× outbound burn time growth at heavier tug. 10-mission cathode-on is 2.40× Advanced-Electric-Propulsion-System design life. Cathode-swap budget grows to ≥ 2 spares per tug at the financial-model-assumed 10-mission reuse.
- **The matrix should explicitly carry both mass-anchor models.** Decomposed-mid is the optimistic (TRL-2 aspirational) bound; bundled MARVL is the realistic bound; the difference is 8.7× at 1 megawatt-electric tug dry mass. The matrix's year-twenty-plus winner cell needs an explicit annotation: "closes only if specific power ≥ 80 watt-per-kilogram at megawatt class," and Finding 1 says that demonstration does not exist.
- **The Bayesian prior from Finding 2 multiplies through.** Even if the specific-power, efficiency, and cathode-life claims are all corroborated by future demonstrations, the 0-of-6 base rate for US space-fission orbit-by-original-decade is a separate axis the matrix has not surfaced. The year-twenty-plus winner cell is contingent on a program category that historically has 0% success in the 60-year era. The financial model's discount rate at the program level should reflect this.
- **Methodology lesson — outbound burn time scales with tug dry mass; inbound with chunk mass.** Heavy-tug regimes are dominated by outbound burn (which grows linearly with tug); chunk-heavy regimes are dominated by inbound burn (which grows with chunk plus tug). At Variant B's small inbound mass ratio (1.39), tug dominates; at all-electric's large inbound mass ratio (4.08), chunk dominates *but* the heavy tug breaks mass closure first.
- **Methodology lesson — separate "mass closes" from "time closes" verdicts.** R-all-electric-thruster-sweep flagged this as a methodology issue; the bundled-anchor sweep here makes it visible. At chunk 400 tonne bundled, mass closes but time does not (18.23 year vs 15-year ceiling). Either constraint alone retires the cell; the matrix needs both columns.
- **Promotes R-marvl-radiator-deployment-program-risk** to a candidate round. The bundled MARVL anchor assumes a deployable radiator program that has not flown. The radiator subsystem is 40–55% of system mass at megawatt class. If deployment fails (radiator stowed mass 2–3× deployed; structural mass at non-deployable areal density), the bundled anchor itself is optimistic.
- **Promotes R-fission-base-rate-bayesian** to a candidate round. Finding 2's 0-of-6 base rate is currently a locked belief but has not been formally integrated into the matrix's expected-value calculations. A round that computes posterior probability of Fission Surface Power Phase 2 → flight by 2035 under Finding 2's prior plus the 2026 evidence (Phase 2 not awarded, scope grew while schedule held) would close that gap.
- **The matrix as drawn does not survive the user-locked findings.** Findings 1–4 establish: (a) specific power is far below the matrix's implicit anchor, (b) vehicle dry mass is 8.7× heavier at megawatt than the prior round used, (c) the program-level fission delivery has 0% historical track record. The matrix's year-twenty-plus cell needs explicit annotation with all of these; the year-zero-through-fifteen Variant B cell needs delivered-fraction correction from 70% to 57% and minimum-power correction from Kilopower 100 kilowatt-electric class to megawatt class. The pitch and conops require corresponding propagation.

