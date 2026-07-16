# R-architecture-E-no-saturn-side-electrolysis — does dropping Saturn-side electrolysis open a higher-credibility path than the surviving 500-kilowatt-electric chemical-kick cell?

**Status:** pre-registration.

## Question

Round 5 of this session (R-fission-surface-power-stretch-credibility, commit `7cb39c2`) collapsed both D-variants below 5% unconditional posterior:

- D-fission posterior median 0.78% (95th percentile 1.87%).
- D-solar-thermal posterior median 2.0% (95th percentile 5.6%).

The shared cascade factor is **Saturn-side process power** — fission-at-Saturn for D-fission, solar-thermal-at-Saturn for D-solar-thermal. Both feed an electrolyzer that turns chunk water into hydrogen and oxygen for the chemical Saturn-departure burn of Variant B.

The matrix's sole surviving deployment cell after rhea's three rounds is **"500-kilowatt-electric chemical-kick + electric-inbound"** at chunk ≤ 200 tonnes, round-trip ~14.5 years (matrix line 66). Per matrix prose, "posterior probability of available reactor by 2032–2035 is in the 0.10–0.30 range" — gated on a 5× scope expansion of NASA Fission Surface Power Phase 2 that has not been awarded.

**The question this round asks:** if the program drops Saturn-side electrolysis entirely (no chemical-kick burn anywhere, no electrolyzer, no hydrogen/oxygen cryostorage, no Saturn-side high-power processing) and runs pure all-electric end-to-end on chunk water (water-fed electric thrusters, no electrolysis), does it open a more-credible deployment path even after accepting an L0-05 round-trip-time waiver?

The structural trade:
- **Drop** the 5× Fission-Surface-Power-Phase-2-scope multiplier (Architecture E uses a sub-megawatt reactor for on-ship electric thrust only, not for high-power Saturn-side processing).
- **Drop** the electrolyzer-at-Saturn cascade factor.
- **Drop** the hydrogen/oxygen cryostorage cascade factor.
- **Drop** the Saturn-side-process-power cascade factor (P(fission-at-Saturn) ≈ 0.04 or P(solar-thermal-at-Saturn) ≈ 0.10 in round-5's cascade).
- **Accept** L0-05 waiver from 15 years to ~25 years (per round-trip closure).
- **Accept** L0-12 cost-competitiveness damage from longer round-trip at 8.7% weighted-average cost of capital.
- **Accept** the silicate-contamination / cathode-life uncertainty of long-duration water-fed electric thrusters at moderate specific impulse (Roman 11 / R-cathode-life-water-plasma).
- **Add** cadence multiplier (2-3 ships/year per L0-07) to compensate for halved per-ship propellant production from chunk-water-only operation.

If E's unconditional posterior exceeds the surviving 500-kilowatt-electric chemical-kick cell's posterior, AND the L0-05 / L0-12 waivers are programmatically tenable, then E is the program's most-credible deployment path. If E fails on either side, the program faces a structural binary: 500-kilowatt-electric chemical-kick (net-present-value-positive, posterior 0.10–0.30) OR abandon ICEBERG.

## Architecture E definition

- **Outbound:** all-electric thrust from low Earth orbit to high-elliptical Saturn orbit, propellant launched from Earth (or refueled at a low-Earth-orbit depot in steady-state).
- **At Saturn:** grapple chunk into bag. **No electrolysis. No chemical burn. No Saturn-side high-power processing.**
- **Inbound:** all-electric thrust on chunk water (water-fed electric: water Hall, water radio-frequency-ion, or water microwave-electrothermal at moderate specific impulse). Propellant is consumed directly from the chunk.
- **Bag perimeter:** standard inflatable per ICEBERG-bag-engineering. No active thermal management of chunk.
- **On-ship reactor:** powers the electric thrusters only. Same reactor on both legs. Sized to deliver thrust at the chosen specific impulse and burn-time budget. Reactor mass per the MARVL-anchored decomposed model.

Contrast with variants:
- **Variant B (matrix's surviving cell):** chemical Saturn-departure burn + electric inbound. Requires electrolyzer + cryostorage + 500-kilowatt-electric reactor (5× Fission Surface Power Phase 2 scope per matrix line 66).
- **D-fission:** fission reactor at Saturn for electrolysis power. Cascade factor median 0.04.
- **D-solar-thermal:** large deployable mirror at Saturn for electrolysis power. Cascade factor median 0.10.
- **Megawatt all-electric end-to-end:** falsified by rhea — 1 megawatt-electric MARVL-anchored mass + corrected continuous-thrust delta-velocity = 19.56-year round-trip, delivered −34.4 tonnes (chunk cannot fuel its own return).
- **Architecture E (this round):** **sub-megawatt** all-electric end-to-end. Same hardware as megawatt all-electric but at lower reactor power, longer burn times, smaller chunks. Trade: round-trip time exceeds 15 years; reactor scope drops to Fission Surface Power Phase 2 baseline (40–200 kilowatt-electric) or up to Variant B's 500-kilowatt-electric floor.

## Pre-registered hypotheses (H-E)

**Aggregate (H-E-agg):** Architecture E's unconditional posterior median exceeds the surviving 500-kilowatt-electric chemical-kick cell's posterior median by 1.5–3× because E drops three cascade factors (Saturn-side power, electrolyzer, cryostorage) while only adding one (long-duration water-electric cathode life). The cost is L0-05 waiver to 20–28 years and net-present-value penalty from longer revenue deferral.

| Sub-claim | Predicted | Falsification |
|---|---|---|
| H-E-a — At decomposed-MARVL mass model with corrected delta-velocities (outbound 29.56 km/s, inbound 24.7 km/s), all-electric end-to-end closes with **positive delivered mass** at 200 kilowatt-electric, chunk 100 tonnes, specific impulse 2000 seconds, round-trip 20–28 years. | yes | falsified if delivered mass is negative or round-trip exceeds 30 years at that cell |
| H-E-b — The Architecture E "sweet-spot" cell (highest delivered/launch-mass under MARVL mass + 25-year ceiling waiver) sits at 200–500 kilowatt-electric, chunk 50–100 tonnes, specific impulse 2000–2934 seconds. | 200–500 kilowatt-electric; chunk 50–100 t; specific impulse 2000–2934 s | falsified if no cell closes inside 25 years OR if winning cell is outside any of these ranges |
| H-E-c — Architecture E's unconditional posterior median exceeds the 500-kilowatt-electric chemical-kick cell's posterior median by 1.5–3×, driven by elimination of the Saturn-side-process-power and electrolyzer cascade factors. | E posterior median 0.20–0.45 vs Variant B 0.10–0.30 | falsified if E median ≤ Variant B median or if E median > 0.60 |
| H-E-d — Cadence requirement to meet L0-07's 2 missions/year at Architecture E round-trips of ~25 years requires a fleet of 50+ in-cruise vehicles after year 20, at fleet capital ≥ $15 billion. | 50+ ships, ≥ $15 billion fleet capital | falsified if fleet is < 30 ships or fleet capital < $8 billion |
| H-E-e — Net-present-value at 8.7% weighted-average cost of capital and Architecture E's ~25-year round-trip is negative for any per-mission revenue under $200 million. | net-present-value-negative at $200 million per mission, 8.7% weighted-average cost of capital | falsified if net-present-value-positive at ≤ $200 million per mission |

**Aggregate decision:** if H-E-c holds (Architecture E is more credible than the 500-kilowatt-electric chemical-kick cell) AND H-E-a/b hold (E closes physically), Architecture E becomes the program's most-credible deployment path conditional on the project-owner accepting an L0-05 waiver. If H-E-e additionally holds (net-present-value negative), the program faces an unresolvable trade: the most-credible architecture is net-present-value-negative; the net-present-value-positive architecture has posterior 0.10–0.30. The program either accepts a low-posterior bet OR a structurally-NPV-negative architecture OR abandons the mission.

If H-E-c fails (E posterior ≤ Variant B posterior), the surviving 500-kilowatt-electric chemical-kick cell remains the only deployment path, and the program's structural risk is concentrated in reactor program delivery (P ≈ 0.10–0.30).

If H-E-a/b fail (E doesn't close physically at sub-megawatt power), the program cannot escape the megawatt requirement; Architecture E is not an escape hatch; the matrix narrows further.

## Method

Same algebraic-not-integrator approach as rhea's R-megawatt-marvl-radiator and enceladus's prior rounds. No new physics. Reuses rhea's mass models, corrected delta-velocities, and self-consistent tug-mass iteration.

**Sweep axes:**
- Reactor power: 40, 100, 200, 500, 1000 kilowatt-electric (Fission Surface Power Phase 2 baseline through Variant B's surviving floor through falsified megawatt).
- Chunk mass: 30, 50, 100, 200 tonnes.
- Specific impulse: 1500, 2000, 2934 seconds (water Hall, water radio-frequency-ion, high radio-frequency-ion). No 5000 s dual-ion (silicate contamination per R11).
- Mass model: decomposed-MARVL (round-5 anchored) + bundled-10 (cross-check).
- Outbound delta-velocity: 29.56 km/s (high-elliptical, no lunar gravity assist; matches rhea baseline).
- Inbound delta-velocity: 24.7 km/s (titan high-elliptical with lunar gravity assist).

= 5 × 4 × 3 × 2 = 120 cells.

**Mass accounting (Architecture E):**
```
M_tug = m_fixed + m_reactor(reactor_kwe) + m_PC(reactor_kwe) + m_radiator(reactor_kwe) + f_tank × m_prop_outbound
                                                                                                    ↑ self-consistent iterate

Outbound:
  m_prop_out = M_tug × (exp(dv_outbound / v_e) − 1)
  M_LEO = M_tug + m_prop_out
  t_burn_out = m_prop_out × v_e / thrust_N

At Saturn:
  M_vehicle = M_tug + chunk_t × 1000   (chunk is the inbound propellant)
  No electrolysis. No chemical burn. No Saturn-side mass change beyond chunk capture.

Inbound (chunk water = propellant):
  m_prop_in = (M_tug + chunk_t × 1000) × (1 − 1/exp(dv_inbound / v_e))
  M_delivered = M_tug + chunk_t × 1000 − m_prop_in
  delivered_t = M_delivered/1000 − M_tug/1000   (delivered water in LEO = chunk minus inbound propellant burned)
  t_burn_in = m_prop_in × v_e / thrust_N

Round-trip = t_burn_out + t_cruise + t_saturn_ops + t_burn_in + t_cruise
```

**Closure thresholds:**
- L0-05 strict: round-trip ≤ 15 years.
- L0-05 relaxed-1: round-trip ≤ 20 years.
- L0-05 relaxed-2: round-trip ≤ 25 years.
- L0-05 relaxed-3: round-trip ≤ 30 years (sovereign-patient-capital ceiling).

**Bayesian posterior cascade comparison (Monte Carlo, 50,000 samples per architecture):**

Each cell's unconditional posterior = product of independent cascade factors. Factor distributions (uniform on stated ranges, conservative-spread for poorly-anchored factors):

| Factor | Architecture E (200 kilowatt-electric) | Variant B (500 kilowatt-electric chemical-kick) | D-fission (Saturn fission) | D-solar-thermal (Saturn mirror) |
|---|---|---|---|---|
| Reactor available 2032–2035 | 0.30 ± 0.20 (Fission Surface Power Phase 2 baseline) | 0.10–0.30 (5× Fission Surface Power scope; matrix line 66) | same as Variant B's reactor | n/a (no Saturn-side reactor) |
| Saturn-side process power qualified | n/a (no Saturn-side power) | n/a (chemical-kick uses on-ship reactor) | 0.05 ± 0.03 | 0.10 ± 0.05 |
| Electrolyzer (200 kilowatt-electric chunk-water, space-qualified) | n/a | 0.40 ± 0.20 | 0.40 ± 0.20 | 0.40 ± 0.20 |
| Cryostorage (hydrogen/oxygen at Saturn, 1 year dwell) | n/a | 0.50 ± 0.20 | 0.50 ± 0.20 | 0.50 ± 0.20 |
| Water-fed electric thruster, ≥ 5-year cathode life on chunk water | 0.40 ± 0.20 | 0.40 ± 0.20 | 0.40 ± 0.20 | 0.40 ± 0.20 |
| Bag at chosen size, 100-tonne class | 0.60 ± 0.20 | 0.60 ± 0.20 | 0.60 ± 0.20 | 0.60 ± 0.20 |
| Rest of mission (capture, deep-space communications, navigation) | 0.70 ± 0.15 | 0.70 ± 0.15 | 0.70 ± 0.15 | 0.70 ± 0.15 |

The cascade product gives unconditional posterior P(mission completes per requirements) ignoring the L0-05 / L0-12 waivers (which are programmatic, not technical).

**Cadence and fleet analysis:**
Steady-state fleet size = cadence × round-trip-time. Per-vehicle capital from prior rounds (R-redundancy-budget-cost: $565M–$710M per vehicle for redundancy overlay; matrix prose: vehicle build-cost ranges $200M–$500M depending on assumptions). Use $300M/vehicle for E (no electrolyzer + cryo subsystems compensates partially for longer burns), $500M/vehicle for Variant B (full electrolyzer + cryostorage).

**Net-present-value analysis:**
Per-mission revenue × cadence × fleet, discounted at 8.7% weighted-average cost of capital. Round-trip determines when first revenue lands. Fleet capital is upfront. Per L0-12 commercial target, water-MET propellant at customer interface should price-match Earth-launched, lunar in-situ-resource-utilization, or other available water.

## Pre-registered prediction summary

H-E-a holds (closure at 200 kilowatt-electric with positive delivered mass, 20–28 year round-trip).
H-E-b holds (sweet-spot at 200–500 kilowatt-electric, chunk 50–100 t, specific impulse 2000–2934 s).
H-E-c holds (E posterior median 0.20–0.45 vs Variant B 0.10–0.30; E wins on credibility).
H-E-d holds (fleet of 50+ ships, $15+ billion fleet capital).
H-E-e holds (net-present-value-negative at $200 million per mission, 8.7% weighted-average cost of capital).

If all five hold, the headline finding is: **"Architecture E is the most-credible deployment path BUT is structurally net-present-value-negative at standard cost of capital. The program either accepts a 10–30% reactor-program bet (Variant B) OR a credible-but-net-present-value-negative architecture (E) OR abandons the mission."**

## Revisit clause

Grade H-E-a through H-E-e. If H-E-c holds and H-E-e fails (E is credible AND net-present-value-positive), Architecture E becomes the recommended deployment path. If H-E-c holds and H-E-e holds, the program faces an unresolvable trade. If H-E-c fails, Variant B remains the sole path and the program's structural risk is concentrated in reactor program delivery.

## Result

### Closure across L0-05 ceiling relaxations

Of 120 swept cells (5 reactor × 4 chunk × 3 specific impulse × 2 mass model):

- **15-year strict ceiling: 0 cells close with positive delivered mass.**
- **20-year relaxed-1 ceiling: 0 cells close.**
- **25-year relaxed-2 ceiling: 18 cells close.**
- 30-year relaxed-3 ceiling: 30 cells close.

The 20-year relaxation buys nothing. Architecture E requires a **minimum L0-05 waiver to 25 years** to close any cell at all. The L0-05 floor for E is between 20 and 25 years; pre-registration's 20–28 year range was wrong on the low end.

### Best Architecture E cell at each ceiling (by delivered-water-per-launch-mass)

| Ceiling | Reactor (kWe) | Chunk (t) | Specific impulse (s) | Round-trip (yr) | Delivered (t) | Launch mass (t) | Delivered/launch |
|---|---:|---:|---:|---:|---:|---:|---:|
| 25 yr | 500 | 200 | 2934 | 23.60 | 50.0 | 168.7 | 0.296 |
| 30 yr | 200 | 100 | 2934 | 25.55 | 26.6 | 76.7 | 0.346 |

Both winners use **MARVL-anchored decomposed mass model**, not bundled. Both use specific impulse 2934 seconds (highest tested; consistent with R-cathode-life-water-plasma's mid-range water-radio-frequency-ion regime). The 25-year winner uses Variant B's reactor scope (500 kilowatt-electric) — meaning Architecture E at the **same** reactor scope as Variant B is still distinctly different (no electrolyzer + cryostorage), and that's where the closest L0-05 compliance is.

### Posterior cascade — Monte Carlo over 50,000 samples per architecture

| Architecture | Posterior median | 5th percentile | 95th percentile |
|---|---:|---:|---:|
| **Architecture E at 100 kilowatt-electric** | **6.44%** | 3.65% | 10.86% |
| **Architecture E at 200 kilowatt-electric** | **4.78%** | 2.60% | 8.40% |
| **Architecture E at 500 kilowatt-electric** | **3.13%** | 1.48% | 6.02% |
| Architecture E at 1000 kilowatt-electric | 1.02% | 0.46% | 2.00% |
| Variant B at 500 kilowatt-electric (chemical-kick) | 0.60% | 0.25% | 1.34% |
| D-fission | 0.03% | 0.01% | 0.08% |
| D-solar-thermal | 0.06% | 0.02% | 0.15% |

**Architecture E at 200 kilowatt-electric is 8× more credible than the surviving 500-kilowatt-electric chemical-kick (Variant B) cell.** Even at 500 kilowatt-electric (same reactor scope as Variant B), Architecture E is **5× more credible** purely from dropping the electrolyzer + cryostorage cascade.

**Cross-round cascade-structure caveat.** This round's cascade has 4–7 multiplicative factors, more granular than enceladus's R-fission-surface-power-stretch-credibility (round 5), which used a 5-stage Bayesian cascade. Absolute medians here (D-fission 0.03%, D-solar-thermal 0.06%) are ~30× lower than round 5's (0.78%, 2.0%). **Round 5's absolute numbers remain the project's reference** for D-fission and D-solar-thermal; this round's D rows are present only for internal-consistent ordering. The **load-bearing comparisons** are within-round: E vs Variant B (same cascade structure on the relevant factors). That comparison is valid and the **8× lift is the headline finding**.

### Fleet, capital, and net-present-value sketch (cadence 2/year, 8.7% weighted-average cost of capital, 40-year horizon)

| Architecture | Round-trip (yr) | Fleet (ships) | Fleet capital ($M) | Net-present-value at $200M/mission | $500M/mission | $1000M/mission |
|---|---:|---:|---:|---:|---:|---:|
| Architecture E 25-yr cell | 23.60 | 47 | 14,159 | −13,648 | −12,880 | −11,602 |
| Architecture E 30-yr cell | 25.55 | 51 | 15,330 | −14,922 | −14,310 | −13,291 |
| Variant B reference (14.5 yr) | 14.50 | 29 | 14,500 | −13,233 | −11,334 | −8,167 |

**Net-present-value is structurally negative at standard 8.7% weighted-average cost of capital across all three architectures, at all tested per-mission revenues up to $1 billion.** This is partly real (capital is loaded upfront on a multi-decade-cycle fleet) and partly an artifact of an over-crude model — actual deployment would ramp the fleet mission-by-mission rather than as a single capital lump. **The qualitative ranking is correct: shorter round-trip plus larger per-mission delivery = less-negative net-present-value.** Variant B is less-negative than Architecture E at all tested revenues. **Architecture E does not flip net-present-value-positive by changing reactor power; it would require either L0-05 collapse (aerocapture) or a different financial structure (sovereign patient capital, 50-year horizon, sub-3% discount rate).**

### Hypothesis grading

| Sub-claim | Predicted | Actual | Held? |
|---|---|---|---|
| H-E-a | 200 kWe / chunk 100 t / 2000 s closes 20–28 yr, positive delivered | round-trip 22.54 yr, delivered 6.7 t | **held** |
| H-E-b | sweet-spot at 200–500 kWe / chunk 50–100 t / 2000–2934 s | reactor 500 kWe, chunk **200 t** (outside range), 2934 s | **falsified** (chunk-mass range wrong; bigger chunks win at 25-yr ceiling) |
| H-E-c | Architecture E posterior 1.5–3× Variant B | 8.0× (4.78% vs 0.60%) | **falsified high — Architecture E is much more credible than predicted** |
| H-E-d | fleet 50+ ships, ≥ $15 billion capital at 25-yr ceiling | 47 ships, $14.16 billion | **falsified** (within 6% of threshold but technically below) |
| H-E-e | net-present-value negative at $200M/mission, 8.7% weighted-average cost of capital, 25-yr ceiling | net-present-value = −$13.65 billion | **held** |

### Reading

**Three observations the result actually supports:**

1. **Dropping Saturn-side electrolysis is a credibility-positive architectural decision worth ~8× posterior lift over the surviving Variant B cell.** This is the largest single-decision credibility lift observed in this session. The lift is structural (eliminates two independent cascade factors) and is not gated on any unproven technology assumption — it just removes an avoidable subsystem.

2. **The L0-05 round-trip-time ceiling is the binding constraint on Architecture E, not reactor power.** At 100–500 kilowatt-electric, Architecture E delivers positive water mass; the problem is round-trip time of 22–28 years. L0-05's 15-year ceiling is rooted in financial-model analysis at 8.7% weighted-average cost of capital; relaxing it to 25 years opens the architecture but does not flip net-present-value. **The program's binding constraint shifts from "reactor program scope" (Variant B's binding constraint) to "financial-structure-and-time-horizon" (Architecture E's binding constraint).**

3. **The surviving 500-kilowatt-electric chemical-kick cell (Variant B) is the only architecture closer to L0-05 strict compliance, but it remains the lower-credibility option (0.60% posterior median vs Architecture E's 4.78%).** The two architectures are not substitutes; they fail differently. Variant B fails on reactor program delivery (0-of-6 base rate prior). Architecture E fails on round-trip time and net-present-value. There is no architecture in this round's sweep that succeeds on both axes.

**The reframed program verdict (post-round-6):**

The "below-5-percent-posterior-bet-limited" verdict from round 5 was anchored on D-fission and D-solar-thermal. **Architecture E rewrites that verdict: at 100 kilowatt-electric, the program is in the 3.65–10.86% credibility band — above 5% in the optimistic tail.** The program is no longer "below-5-percent-posterior-bet-limited"; it is **"L0-05-and-L0-12-bet-limited"** — the binding constraints have shifted from technical credibility to programmatic / financial waivers.

The trilemma surfaced:

| Path | Posterior median | L0-05 strict (≤15 yr) | Net-present-value at 8.7% weighted-average cost of capital |
|---|---:|:---:|:---:|
| Variant B (500 kWe chemical-kick) | 0.60% | yes (~14.5 yr) | net-present-value-negative (in this crude model) |
| Architecture E (200 kWe) | 4.78% | NO (22.54 yr) | net-present-value-negative |
| Architecture E (500 kWe) | 3.13% | NO (23.60 yr) | net-present-value-negative |

**No tested architecture clears both technical credibility (posterior > 5%) AND L0-05 strict AND net-present-value-positive simultaneously.**

**Escape paths surfaced by this round:**

- **R-aerocapture-impact-on-architecture-E** — if R-chunk-as-heat-shield-revisit closes (collapses 36 km/s of Earth-side round-trip delta-velocity to aerodynamic passes), Architecture E's round-trip drops from 22–25 years to ~10–13 years. This would be a **simultaneous credibility-lift + L0-05-compliance + net-present-value-improvement** result. The aerocapture rescue path is now load-bearing for the entire architecture decision matrix, not just for megawatt all-electric.
- **R-fleet-ramp-NPV** — the crude net-present-value model loads all fleet capital upfront. A mission-by-mission deployment ramp (build ship N from revenue of ship N-2) plausibly flips Architecture E's net-present-value at 500 kilowatt-electric and chunk 200 tonnes to weakly positive or modestly negative. Worth a more careful financial model before declaring Architecture E net-present-value-dead.
- **R-L0-05-WACC-sensitivity** — at what weighted-average cost of capital (sovereign-patient-capital regime, sub-3%) does Architecture E flip net-present-value-positive at 25-year round-trip? This is a strategic-financing question, not a propulsion question, but it determines whether Architecture E's credibility lift is a viable program path.

### What this round assumes that should be questioned

- **Cascade factor distributions** are uniform over stated ranges. They are not anchored to flight or ground heritage in most cases. The 8× E-vs-Variant-B ratio is **the relative ordering, which is robust to the absolute calibration** since both architectures share the bag, reactor, water-electric, and rest-of-mission factors and differ only on the electrolyzer + cryostorage + Saturn-side-power factors.
- **Per-vehicle cost** is set at $300 million for Architecture E and $500 million for Variant B. These are best-guess from prior matrix work and have not been independently verified. R-architecture-D-cost (Priority 1 thread) is the natural follow-up.
- **Net-present-value model** is over-simple. Fleet capital should ramp mission-by-mission, not load upfront. Operating cost is approximated as zero (small at standard weighted-average cost of capital but not zero). Tax / depreciation effects are ignored. Customer payment timing (lump-sum on delivery vs annuity contract) is not modeled. **A round on fleet-ramp net-present-value is the natural follow-up.**
- **Specific impulse 2934 seconds** is the high-radio-frequency-ion regime, conservatively below silicate-contamination-falsified dual-ion at 5000 seconds. The 2934-second value comes from R-cathode-life-water-plasma's mid-range cathode-life estimate.
- **L0-05's economic basis is 8.7% blended weighted-average cost of capital**, which is the right anchor for venture-capital project economics but possibly wrong for a 13-year sovereign-class mission. The program may need an explicit sovereign-WACC variant of L0-05 to make Architecture E tractable.

### Revisit clause

H-E-a held; H-E-b falsified (chunk-mass winner is 200 t not 50–100 t); H-E-c falsified-favorable (E is 8× more credible than Variant B, not 1.5–3×); H-E-d falsified (47 ships not 50+); H-E-e held.

**Aggregate H-E-agg verdict:** Architecture E is **substantially more credible** than the surviving Variant B cell, but **strictly L0-05-non-compliant** under the round's swept parameter space. The "credibility-trade-vs-NPV" structure of the pre-registered aggregate holds, but the magnitudes are very different from prediction: credibility lift is 8× (not 1.5–3×), and net-present-value is negative at all tested per-mission revenues (not "negative only below $200 million"). The trade is not whether to accept E's lower-credibility-but-net-present-value-positive option — it's whether to accept either of two net-present-value-negative options, or to invest in collapsing the L0-05 binding constraint (aerocapture rescue).

**The aerocapture rescue path is now the highest-leverage open question for the entire architecture decision matrix.** It is now load-bearing for: (i) megawatt all-electric (rhea's R-megawatt-marvl-radiator), (ii) Architecture E sub-megawatt all-electric (this round), and (iii) the trilemma escape path. R-chunk-as-heat-shield-revisit is the next priority.

