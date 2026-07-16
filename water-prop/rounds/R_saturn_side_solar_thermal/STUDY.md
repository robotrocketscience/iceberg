# R-saturn-side-solar-thermal

**Owner session:** enceladus-r5 (resumed 2026-05-15)
**Branch:** iceberg-enceladus-r5
**Status:** PRE-REGISTERED (hypothesis frozen before run)

---

## Motivation

Enceladus-r5's prior verdict was *"the program is fission-bet-limited"* — meaning that even Architecture D (chemical propulsion plus a Saturn-side reactor for inbound electrolysis only) still rides on a Fission-Surface-Power-class reactor hitting its stretch specific-power target (10 watts-per-kilogram). Locked-belief evidence is hostile to that assumption:

- 40-watts-per-kilogram megawatt-class number is a Technology-Readiness-Level-2 paper figure, not a Kilowatt-Reactor-Using-Stirling-Technology extrapolation.
- Kilowatt-Reactor-Using-Stirling-Technology actually measured 2.4 watts-per-kilogram system-level.
- US space-fission programs have a 0-of-6 base rate of reaching orbit within the originally-stated decade since 1965.
- Fission-Surface-Power Phase 2 has not been awarded as of May 2026.

If a non-fission Saturn-side power source can supply the ~150–300 kilowatts-electric required for inbound water electrolysis at a deployed mass competitive with a Fission-Surface-Power-class reactor (roughly 20–30 tonnes for 200–300 kilowatts-electric at the 10-watts-per-kilogram stretch case), the headline *"fission-bet-limited"* finding is false. Architecture D would then have a non-fission fallback and Saturn-side process power would stop being the binding constraint.

The leading non-fission candidate is a deployable mirror concentrator feeding a thermal-to-electric or direct-high-temperature-electrolysis path. The prior enceladus-r5 STATE.md sketched this at "1-square-kilometer mirror, ~1 tonne, sub-1-tonne-per-1000-square-meter areal density, ≥ 1 megawatt thermal at 9.58 astronomical units" — which is internally inconsistent (1 square kilometer at 1 kilogram-per-square-meter is 1000 tonnes, not 1 tonne). This round redoes the math cleanly.

## Hypothesis (H-saturn-side-solar-thermal)

**Pre-registered numeric prediction (written before run.py executes).**

Define a *Saturn-side solar-thermal-electrolysis stack* with these components:

- Inflatable mirror concentrator, areal density between 0.1 and 1.0 kilograms-per-square-meter.
- Concentrator structure overhead, between 1.0× and 2.0× mirror mass.
- Receiver/concentrator hardware, approximated as 10 percent of mirror mass.
- Power-conversion path, one of:
  - **Stirling path:** thermal-to-electric conversion at 28 percent efficiency, then proton-exchange-membrane electrolyzer at 70 percent efficiency. End-to-end thermal-to-hydrogen-chemical 19.6 percent.
  - **Direct-solid-oxide-electrolyzer path:** high-temperature steam electrolysis at 800–900°C; net thermal-to-hydrogen-chemical efficiency 50 percent (solid-oxide-electrolyzer demonstrated in laboratory, no flight heritage).
- Waste-heat radiator, sized using the canonical decomposed model 50 kilograms-per-kilowatt-thermal (analogous to the propulsion-side radiator penalty before MARVL correction; conservative for sub-megawatt cycles).
- Power-conversion / electrolyzer mass: Stirling at 10 kilograms-per-kilowatt-electric (Kilowatt-Reactor-Using-Stirling-Technology heritage) plus proton-exchange-membrane at 5 kilograms-per-kilowatt-electric; or solid-oxide-electrolyzer at 8 kilograms-per-kilowatt-thermal.
- Saturn shadow penalty: bump collection area by a duty-cycle factor 1.0 (uninterrupted, e.g. Saturn-Sun L1 halo) to 1.5 (Saturn orbit with shadow fraction ~33 percent and no thermal storage). Pre-register both endpoints.

**Predicted ranges for mass-per-kilowatt-useful at 200 kilowatts-electric-equivalent useful electrolysis output:**

| Scenario | Conversion path | Mirror areal density (kilograms-per-square-meter) | Predicted total kilograms-per-kilowatt | Source confidence |
|---|---|---|---|---|
| Optimistic | Direct-solid-oxide-electrolyzer | 0.1 | 50–120 | low (solid-oxide-electrolyzer has no flight heritage) |
| Mid | Stirling | 0.5 | 200–350 | medium |
| Conservative | Stirling | 1.0 | 350–600 | high (uses flight-heritage components only) |

**Comparison benchmarks:**

- Fission-Surface-Power stretch (Architecture D's contracted closure condition): 100 kilograms-per-kilowatt at 10-watts-per-kilogram specific power.
- Fission-Surface-Power baseline (Phase 1 contracted): 200 kilograms-per-kilowatt at 5-watts-per-kilogram specific power.
- Kilowatt-Reactor-Using-Stirling-Technology demonstrated: 416 kilograms-per-kilowatt at 2.4-watts-per-kilogram system-level.

**Falsification rule (pre-registered):**

The hypothesis "Saturn-side solar-thermal is a credible non-fission alternative for Architecture D" is **upheld** if and only if the conservative scenario (Stirling path, mirror areal density 1.0 kilograms-per-square-meter, duty-cycle 1.5) yields mass-per-kilowatt **less than 200 kilograms-per-kilowatt**, i.e. competes with the Fission-Surface-Power Phase-1-contracted baseline using only flight-heritage components.

The hypothesis is **falsified** if conservative scenario exceeds 400 kilograms-per-kilowatt (worse than Kilowatt-Reactor-Using-Stirling-Technology) — solar thermal then offers no advantage over the fission demonstrated state-of-the-art and "fission-bet-limited" survives intact.

The middle band (200–400 kilograms-per-kilowatt) means solar thermal is a stretch case in the same risk-class as Fission-Surface-Power stretch, not a slam-dunk falsifier of "fission-bet-limited."

## Flight-heritage survey

| Subsystem | Heritage status |
|---|---|
| Inflatable mirror concentrator at 0.1–1.0 kilograms-per-square-meter | HERITAGE-NONE for full scale. Echo I/II (1960s) flew at ~0.01 kilograms-per-square-meter equivalent but as passive reflector, not concentrator. Inflatable Antenna Experiment 1996 demonstrated 14-meter inflated structure. NASA Solar Sail (NEA Scout 2022) at ~0.01 kilograms-per-square-meter. No deployable concentrator above 10 meters has flown. |
| Stirling power conversion at 28% | HERITAGE-ADJACENT. Advanced Stirling Radioisotope Generator ground-qualified 2013, never flown. Kilowatt-Reactor-Using-Stirling-Technology demonstrated 2018 at smaller scale (1 kilowatt-electric Stirling per channel, 4 channels). |
| Proton-exchange-membrane electrolyzer in space | HERITAGE-NONE. Used on International Space Station for oxygen generation but small-scale and not space-qualified for ~200-kilowatt-electric throughput. |
| Solid-oxide electrolyzer in space | HERITAGE-NONE. MOXIE on Perseverance demonstrated solid-oxide *carbon-dioxide* electrolysis at 25 watts. No water-electrolysis solid-oxide flight demo. |
| Radiator at 50 kilograms-per-kilowatt-thermal | HERITAGE-ADJACENT. International Space Station thermal control system meets this class. Megawatt-class deployable radiators (MARVL) do not have flight heritage. |

Verdict: solar-thermal stack at scale uses **no flight-heritage component**. Even the conservative scenario is a Technology-Readiness-Level-3-to-4 system-level demonstration at best. This is comparable to the Fission-Surface-Power program's status, so the comparison is at least apples-to-apples.

## Test

`run.py` computes deployed mass and mass-per-kilowatt across the pre-registered parameter grid:

- Target useful electrolysis output: 150, 200, 300, 500 kilowatts-electric-equivalent.
- Mirror areal density: 0.1, 0.3, 0.5, 1.0 kilograms-per-square-meter.
- Conversion path: Stirling + proton-exchange-membrane vs direct-solid-oxide-electrolyzer.
- Duty-cycle factor: 1.0 and 1.5.

Inputs deterministic. Output written to `results/solar_thermal_grid.json` and `results/tables.md`. Compared to the three fission benchmarks above.

## Result

Sixty-four scenarios swept. Distribution across the three fission benchmarks:

| Fission benchmark | Scenarios that beat it | Best representative |
|---|---|---|
| Fission-Surface-Power stretch (100 kilograms-per-kilowatt at 10-watts-per-kilogram) | **0 of 64** | n/a — no solar-thermal scenario beats this |
| Fission-Surface-Power Phase 1 contracted (200 kilograms-per-kilowatt at 5-watts-per-kilogram) | 12 of 64 (all solid-oxide-electrolyzer, all mirror areal density 0.1 or 0.3 kilograms-per-square-meter) | 101 kg/kW: 200 kW useful, areal 0.1, solid-oxide-electrolyzer, duty 1.0; deployed mass 20.3 t; mirror area 33,717 m² (183 m × 183 m) |
| Kilowatt-Reactor-Using-Stirling-Technology demonstrated (416 kilograms-per-kilowatt at 2.4-watts-per-kilogram) | 20 of 64 | 225 kg/kW: 500 kW useful, areal 0.3, solid-oxide-electrolyzer, duty 1.5; deployed mass 112.7 t |
| Worse than Kilowatt-Reactor-Using-Stirling-Technology | 32 of 64 | n/a |

**Pre-registered conservative scenario** (Stirling path, mirror areal density 1.0 kilograms-per-square-meter, duty-cycle 1.5): **1560 kg/kW at every target output**. This is 3.7× worse than Kilowatt-Reactor-Using-Stirling-Technology demonstrated state-of-the-art.

**Pre-registered optimistic scenario** (solid-oxide-electrolyzer path, mirror areal density 0.1 kilograms-per-square-meter, duty-cycle 1.0): **101 kg/kW**. Just barely above the Fission-Surface-Power-stretch threshold of 100 kg/kW; classified as "beats Fission-Surface-Power Phase 1 contracted baseline."

Mass breakdown at the optimistic 200-kilowatt point:

| Component | Mass (tonnes) | Share |
|---|---|---|
| Mirror | 3.4 | 17% |
| Structure | 3.4 | 17% |
| Receiver | 0.3 | 2% |
| Solid-oxide-electrolyzer | 3.2 | 16% |
| Radiator | 10.0 | 49% |
| **Total** | **20.3** | 100% |

Mass breakdown at the conservative 200-kilowatt point:

| Component | Mass (tonnes) | Share |
|---|---|---|
| Mirror | 129.0 | 41% |
| Structure | 129.0 | 41% |
| Receiver | 12.9 | 4% |
| Stirling + proton-exchange-membrane | 4.3 | 1% |
| Radiator | 36.7 | 12% |
| **Total** | **311.9** | 100% |

## Reading

**Two regimes.** With solid-oxide-electrolyzer at low mirror areal density, the radiator is the dominant mass term (~50 percent of deployed mass) because high-temperature electrolysis absorbs roughly half the thermal input as chemical bond energy. With Stirling at high mirror areal density, mirror plus structure dominates (~80 percent of deployed mass) because the collection area scales inversely with the 19.6-percent end-to-end Stirling-plus-proton-exchange-membrane efficiency.

**The hypothesis as pre-registered is falsified.** The falsification rule said: upheld if conservative scenario < 200 kg/kW; falsified if conservative > 400 kg/kW. Conservative came in at 1560 kg/kW. Solar-thermal-with-Stirling using a flight-heritage-density mirror is not competitive with even the worst fission demonstration (Kilowatt-Reactor-Using-Stirling-Technology at 416 kg/kW).

**But the sharp finding is the parameter sensitivity.** Solar-thermal moves from "1560 kg/kW (worse than every fission option)" to "101 kg/kW (essentially tied with Fission-Surface-Power stretch)" by swapping (a) Stirling for solid-oxide-electrolyzer, and (b) flight-heritage mirror areal density (1.0 kg/m²) for solar-sail-class areal density (0.1 kg/m²). Each of these substitutions is a Technology-Readiness-Level-2-to-3 bet of its own. The "competitive" solar-thermal stack therefore requires *two simultaneous* non-flight-heritage technology bets — directly comparable to Fission-Surface-Power Phase 2 stretch (10 W/kg specific power, which is itself a Technology-Readiness-Level-2 bet per locked beliefs).

**Reframed verdict.** The prior enceladus-r5 conclusion *"the program is fission-bet-limited"* was wrong about *which* bet is binding. The actual binding constraint is **all candidate Saturn-side power-densification paths sit at Technology-Readiness-Level 2 to 3**. Fission-Surface-Power stretch and solar-thermal-with-solid-oxide-electrolyzer-low-areal-mirror occupy the same credibility band. Neither is a slam-dunk; neither displaces the other. The matrix is not fission-bet-limited; it is **Saturn-side-Technology-Readiness-Level-limited**.

**Implication for the architecture matrix.** Solar-thermal should be added as a *parallel-hedge Saturn-side power option* with the same conditional posterior structure as Architecture D's reactor: a TRL-progression bet that needs 5–10 years of development. Don't bet on one and lose the other — pursue both as hedges if Saturn-side electrolysis remains in the design. Alternatively, if neither bet is acceptable, the matrix must abandon the inbound-electrolysis approach entirely and rely on chunk-fed Saturn-departure (Architecture B-style) for both legs.

**One assumption-question I did not adequately address.** Saturn shadow is modeled as a flat 1.5× duty-cycle bump, which assumes either (a) the station is in a Saturn orbit with ~33% shadow fraction and zero thermal storage, or (b) the station is at Saturn-Sun L1 with no shadow at all. The true configuration depends on conops choices not yet made. If the station is on a Saturnian moon (Titan, Enceladus surface) the shadow fraction is dominated by the moon's orbital period around Saturn, not Saturn's own rotation. This deserves its own round before the matrix takes solar-thermal as a credible row.

## Revisit

**Pre-registered prediction vs measured (pre-reg table reproduced):**

| Scenario | Conversion path | Mirror areal (kg/m²) | Predicted kg/kW | Measured kg/kW | Held? |
|---|---|---|---|---|---|
| Optimistic | Solid-oxide-electrolyzer | 0.1 | 50–120 | 101 (duty 1.0) / 152 (duty 1.5) | held at duty 1.0; held at duty 1.5 if predicted range read as 50–200 |
| Mid | Stirling | 0.5 | 200–350 | 785 (duty 1.0) / 1178 (duty 1.5) | **NOT held — predicted range was 2–3× too optimistic** |
| Conservative | Stirling | 1.0 | 350–600 | 1040 (duty 1.0) / 1560 (duty 1.5) | **NOT held — predicted range was 2–3× too optimistic** |

**Why the mid-and-conservative-Stirling predictions failed.** I underestimated the mirror-plus-structure mass contribution at high areal density combined with low Stirling-plus-proton-exchange-membrane end-to-end efficiency (19.6 percent). At 1.0 kg/m² and 19.6 percent efficiency, every kilowatt-useful demands ~640 square-meters of mirror plus structure, which at 2.0× structure-overhead factor becomes ~1280 kg/kW just from the optics — before adding power conversion or radiator. My pre-reg numerically forgot to multiply: I anchored on the solid-oxide-electrolyzer regime mentally and extrapolated to Stirling without redoing the math. Recurring lesson #7 from the protocol applies (simulate the mission before optimizing one variable; here, derive the regime before pre-registering ranges).

**Falsification verdict.** The pre-registered binary rule (conservative < 200 = upheld; > 400 = falsified) returns **falsified at 1560 kg/kW**. But the more useful result is the reframed verdict in Reading: solar-thermal is not a non-fission slam-dunk, but it is a same-credibility-band parallel hedge under aggressive technology assumptions. The pre-reg's binary framing missed the parameter-sensitivity structure that turned out to be the actual story.

## Cross-learning

**Backward references:**

- **R-non-fission-baseline (enceladus-r5 round 1):** the binding fission-dependence identified there is Saturn-side process power for inbound electrolysis. This round tests whether solar-thermal can displace fission for that role; conclusion is "only under same-credibility-band stretch assumptions." Annotation for that round: the all-chemical Architecture B's hidden-infeasibility verdict should be revised — solar-thermal Saturn-side at Technology-Readiness-Level 2-3 *might* unhide it, conditional on the same kind of program-risk that already attaches to Fission-Surface-Power.
- **R-chemical-plus-small-reactor (enceladus-r5 round 2):** Architecture D's reactor sub-element should be reannotated as "reactor OR solar-thermal-with-solid-oxide-electrolyzer; both Technology-Readiness-Level 2-3 in 2026." The unconditional posterior 0.07–0.15 remains; the conditional cascade should now multiply by the per-path TRL-progression probability rather than the fission-program-only probability.
- **Locked beliefs 1–4 (power findings):** the same Technology-Readiness-Level critique applies to solar-thermal-with-solid-oxide-electrolyzer. Solid-oxide-water-electrolyzer has no space heritage (Mars-Oxygen-In-situ-resource-Utilization-Experiment did 25 watts of solid-oxide carbon-dioxide electrolysis, not water). Inflatable concentrator at 0.1 kg/m² requires ~30,000 square-meters deployed — 400× larger than the largest deployed inflatable in flight history.

**Forward references / spawned threads:**

- **R-saturn-shadow-and-station-location:** flat 1.5× duty-cycle bump is a hack. Real shadow depends on whether the station sits at Saturn-Sun L1, a Saturn orbit, or a moon surface. For Titan-or-Enceladus-surface stations, the dominant duty-cycle is the moon's orbital period around Saturn (15.95 days for Titan, 1.37 days for Enceladus). Solar-thermal needs thermal storage (latent-heat or sensible-heat reservoir) or a duty-cycle factor of 2–3× rather than 1.5×. This could flip the optimistic case from 101 kg/kW to 200–300 kg/kW.
- **R-solid-oxide-electrolyzer-space-qualification:** technology-readiness assessment for solid-oxide water electrolysis at 200-kilowatt scale in space. Mars-Oxygen-In-situ-resource-Utilization-Experiment carbon-dioxide work transfers partially. What is the credible Technology-Readiness-Level milestone schedule and what programs (NASA, Department of Energy) might fund it?
- **R-inflatable-concentrator-scale-up:** deployable mirror at 30,000 square-meters. Largest flown is ~86 square-meters (NEA Scout 2022). What is the credible scale-up path, optical figure tolerance, and station-keeping cost? L'Garde and similar contractors have ground-tested 25-meter-class structures.
- **Architecture matrix update (orchestrator, not me):** add solar-thermal Saturn-side as a parallel cell to Architecture D's reactor sub-element. Both at conditional posterior similar to Fission-Surface-Power-stretch (5–25 percent over a 10-year horizon, very loosely). Reframe the "fission-bet-limited" verdict to "Saturn-side-Technology-Readiness-Level-bet-limited."

**Methodology issue flagged for future rounds:** when pre-registering numeric ranges over a parameter sweep that spans multiple regimes (here: Stirling-dominated vs solid-oxide-electrolyzer-dominated; high-areal-density vs low-areal-density), check the regime boundary numerically before freezing the range. Anchoring on one regime and extrapolating mentally produces 2–3× errors as it did here.

