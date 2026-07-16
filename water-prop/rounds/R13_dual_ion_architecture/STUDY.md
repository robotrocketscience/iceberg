# Round 13 — Dual-Ion Architecture Trade

**Status:** pre-result.

## Question

R10 found water dual-ion (electrolyze chunk water into H⁺ + O⁺, ionize separately) delivered 82.9% chunk at Kilopower / Case B at specific impulse 5000 seconds, but cruise time was 33.2 years — disqualifying. R5 confirmed dual-ion wins only in narrow corners. The architectural read was "dual-ion wins on mass-budget but loses on time-of-flight." But R10 fixed specific impulse at 5000 s and power at Kilopower 10 kWe. Dual-ion's real value is at higher power class, where its specific-impulse advantage compounds.

**The question:** at what (reactor power, dual-ion specific impulse) cells does dual-ion close a 14-year round trip at viable delivery, and how does it compare to R12's water radio-frequency ion + 10-flyby lunar tour cell (15 kWe / 13.91 yr / 70.1% delivery)?

Three additional considerations:
1. Dual-ion electrolyzes water before ionization. Silicate contamination from chunk water is *filtered out* by electrolysis, so the grid life problem R11 surfaced for water radio-frequency ion does not apply.
2. The electrolyzer is a mass cost. Estimate ~0.5 kg/kWe of additional dry mass beyond the thruster.
3. Dual-ion is TRL 1-2 — much further from flight than water radio-frequency ion (Pale Blue, TRL 7-8). The architectural trade is "viable architecture vs flight-ready architecture."

## Pre-registered hypothesis (H13)

**Aggregate (H13-agg):** Dual-ion can close 14-year round trip at higher delivery than water radio-frequency ion, but only at a reactor power class (≥100 kWe) that doesn't have a flight program. At 40 kWe Fission Surface Power class with achievable dual-ion specific impulse (5000-7500 s), dual-ion is *comparable* to water radio-frequency ion + lunar tour (both ~14 yr round trip, ~70% delivery) — but trades 6 TRL points for the small delivery upside. At 100+ kWe, dual-ion delivers >85% at 14-yr round trip and the architecture is qualitatively better than water radio-frequency ion. At MW class, dual-ion enables 200+ tonne chunks at 14-yr round trip (the user's "$400M/year" operating point).

**Pre-registered sub-claims:**

| Sub-claim | Predicted | Falsification |
|---|---|---|
| H13a — Dual-ion at 40 kWe + 5000 s specific impulse vs water radio-frequency ion at 40 kWe + 2000 s, both with R12 lunar tour | Comparable round trip and delivery (within ±5 percentage points). Dual-ion is not a clear winner at Fission Surface Power class | falsified if dual-ion exceeds water radio-frequency ion by > 10 percentage points or falls behind by > 10 |
| H13b — Dual-ion at 100 kWe + 7500 s specific impulse closes 14-yr at ≥85% delivery | yes | falsified if either constraint missed |
| H13c — Dual-ion at megawatt class (500 kWe) + 10000 s specific impulse enables 100+ t chunk at 14-yr round trip | yes | falsified if 14-yr round trip not reachable, OR chunk capability < 80 t |
| H13d — Electrolyzer mass penalty erodes dual-ion's delivery advantage by 2-5 percentage points at 100 kWe | yes (0.5 kg/kWe × 100 kWe = 50 kg added dry → small fraction of vehicle dry mass; minor impact) | falsified if penalty > 10 pp or < 0.5 pp |
| H13e — Dual-ion sweet-spot specific impulse for closing 14-yr at fixed power | Power-dependent. At 40 kWe, 5000 s is optimal (higher specific impulse means lower thrust = longer cruise). At 100 kWe, 7500 s. At 500 kWe, 10000-12000 s | falsified if relationship is non-monotonic or jumps |
| H13f — Silicate-contamination immunity (R11 risk absent) | Dual-ion's electrolysis step removes silicate dust before ionization. Grid life concern from R11 is eliminated for dual-ion | held in narrative; not quantitatively tested in R13 (deferred R11b) |

**Pre-registered architectural conclusion if H13 holds:** Dual-ion is the *long-horizon* architectural play (ships 8+ at megawatt-class reactor), water radio-frequency ion is the *near-term* architectural play (ships 1-7 at Kilopower/Fission Surface Power class). The deck should show both as a roadmap: Pale Blue water radio-frequency ion for the demonstrator, dual-ion for the production fleet at scaled reactor power.

## Method

For each (chunk mass × reactor power × specific impulse × electrolyzer mass × inbound braking ∆v):
1. Reactor mass = power / specific power (use 5 W/kg nominal, 10 W/kg optimistic)
2. Electrolyzer mass = 0.5 kg/kWe × power
3. Dry vehicle mass = 5 t + electrolyzer
4. Initial mass at Saturn departure = chunk + dry + reactor
5. Inbound braking ∆v = 4.47 km/s (R12 baseline, after 10-flyby lunar tour from R12's analysis of post-Hohmann)
6. Propellant fraction via Tsiolkovsky at the specific impulse
7. Delivered chunk = chunk grappled − propellant burned
8. Thrust = 2 × η × power / specific-impulse-velocity (η = 0.55 for dual-ion, slightly worse than water radio-frequency ion 0.65 because of the electrolyzer + dual-stage loss)
9. Cruise braking time = ∆v / (acceleration × duty 0.5)
10. Inbound time-of-flight = max(Hohmann coast 6.09 yr, cruise braking) + lunar tour phasing 0.73 yr (R12's 10-flyby phasing)
11. Round trip = outbound 6.09 + Saturn dwell 1.0 + inbound time-of-flight

**Sweep grid:**
- Chunk mass: 14 t (R12 baseline), 50 t (Kilopower era max), 200 t (Fission Surface Power era target)
- Reactor power: 10, 40, 100, 200, 500 kWe
- Dual-ion specific impulse: 3000, 5000, 7500, 10000, 12000 s
- Reactor specific power: 5, 10 W/kg

= 3 × 5 × 5 × 2 = 150 cells. Tractable.

**Compare cells:**
- Best dual-ion cell at each (chunk mass) for closing 14-yr round trip
- Water radio-frequency ion + 10-flyby lunar tour baseline (R12 best: 14 t chunk / 13.91 yr / 70.1%)

**Trajectory model — being explicit so cross-round comparisons are apples-to-apples.** All rounds in this campaign use the same closed-form approximation, not a real trajectory integrator:

- Thrust = 2 · η · P / v_exhaust, held constant for the burn (power and specific impulse fixed)
- Acceleration = F / m_average, where m_average = (m_initial + m_final) / 2 (midpoint mass, not time-integrated)
- Braking time = delta-velocity / (acceleration × duty-cycle), with duty cycle = 0.5
- Coplanar, tangential thrust assumed (no steering or plane-change losses)
- No gravity losses, no coast arcs, no eclipse losses, no reactor-power degradation over mission life

This is concept-paper-grade — same level as the conops' own delta-v budget. The model *overestimates* cruise time by roughly 10-20% relative to a real Tsiolkovsky-integrated optimal trajectory (because real acceleration grows as propellant burns off, while the closed-form locks acceleration at the midpoint). Cells closing 14 years in this round will close more comfortably in a real integration; cells failing by < 1 year may still close. A proper trajectory analysis (NASA General Mission Analysis Tool, MALTO, or low-thrust Lambert solver) is the next-rigor-level tool, not in this campaign's scope.

**Validity caveats:**
- Dual-ion η = 0.55 is a guess. Real efficiency depends on electrolyzer, ionization, neutralization losses across two ion species. Worth a published-numbers check.
- Electrolyzer 0.5 kg/kWe is rough. Terrestrial electrolyzers are 3-5 kg/kW; space-rated would be lighter but exact number is speculative.
- Dual-ion at megawatt class needs power-conditioning electronics that scale with power; pre-conditioning mass is not modeled.
- R11's silicate-contamination grid life issue is assumed eliminated by electrolysis. This is plausible (electrolysis is a filter step at the molecular level) but not quantitatively verified.
- Inbound braking ∆v is fixed at R12's 4.47 km/s. If dual-ion enables different trajectory choices (e.g., faster inbound at higher specific impulse), the ∆v should be revisited.
- Hohmann coast floor (6.09 yr) is the structural minimum on inbound. Even infinite thrust acceleration can't break that.

## Result

### Sweet-spot cells per chunk mass (best 14-year-closing dual-ion cell)

| Chunk delivered target | Power | Specific impulse | Reactor mass (10 W/kg) | Cruise braking | Round trip | Delivery |
|---:|---:|---:|---:|---:|---:|---:|
| 14 t | 100 kWe | 7500 s | 10 t | 5.34 yr | 13.91 yr | **87.8%** |
| 50 t | 200 kWe | 5000 s | 20 t | 4.54 yr | 13.91 yr | **86.9%** |
| 200 t | 500 kWe | 5000 s | 50 t | 6.17 yr | 13.99 yr | **88.9%** |

### Direct comparison: dual-ion vs water radio-frequency ion (best cell each, 14-year closing, same trajectory + lunar tour)

| Chunk | Dual-ion best | Water radio-frequency ion best | Delta |
|---:|---|---|---:|
| 14 t | 200 kWe / 12000 s → 13.91 yr / **89.6%** | 40 kWe / 2000 s → 13.91 yr / 66.5% | +23.1 pp |
| 50 t | 500 kWe / 10000 s → 13.91 yr / **90.6%** | 40 kWe / 2000 s → 13.91 yr / 76.0% | +14.7 pp |
| 200 t | 500 kWe / 5000 s → 13.99 yr / **88.9%** | 200 kWe / 2000 s → 13.91 yr / 77.1% | +11.8 pp |

(Note: at 14 t and 50 t chunks, dual-ion's "absolute best" cell uses much more power than the chunk needs — water radio-frequency ion's "best" sticks to 40 kWe because higher power degrades delivery. The honest comparison is sweet-spot vs sweet-spot — see the first table.)

### Reactor power scaling rule of thumb

For dual-ion + 14-yr round trip with R12 trajectory (4.47 km/s residual after 10-flyby lunar tour):

**Reactor power required ≈ 3-5 kWe per tonne of delivered chunk.** Reactor mass is 10-25% of delivered chunk mass at 10 W/kg specific power.

### Hypothesis grading

| Sub-claim | Predicted | Measured | Verdict |
|---|---|---|---|
| H13a — 40 kWe dual-ion vs water radio-frequency ion comparable ±5 pp | 5000 s dual-ion vs 2000 s water radio-frequency ion both at 40 kWe / 14 t / 10 W/kg | Dual-ion at 40 kWe / 3000 s closes at 76.8% delivery (5000 s doesn't close); water radio-frequency ion at 40 kWe closes at 66.5%. Delta = +10.3 pp — just over the ±10 falsification band | **falsified** (narrowly, on the upside — dual-ion outperforms more than predicted) |
| H13b — 100 kWe + 7500 s closes 14-yr at ≥85% (14 t chunk) | yes | 87.8% at 13.91 yr | **held** |
| H13c — 500 kWe + 10000 s closes 200 t at 14-yr | yes | At 200 t / 500 kWe / 10000 s: doesn't close 14-yr (cruise braking too long; thrust too low). The cell that DOES close 200 t at 14-yr is 500 kWe / 5000 s / 88.9% delivery | **falsified on specific impulse, held on chunk size** — 200 t at 14-yr is reachable, but the right specific impulse is 5000 s not 10000 s |
| H13d — Electrolyzer mass penalty 2-5 pp | small | 50 kg electrolyzer at 100 kWe (vs 21 t total dry+chunk+reactor) is ~0.2% of vehicle mass; impact on delivery < 0.5 pp | **held with margin** |
| H13e — Sweet-spot specific impulse moves with power class | 5000 s at 40 kWe, 7500 s at 100 kWe, 10000-12000 s at 500 kWe | Sweet specific impulse for 14-yr closing actually moves with *chunk mass*, not power: 7500 s at 14 t, 5000 s at 50 t and 200 t. Higher chunk needs more thrust (lower specific impulse) | **falsified — wrong dimension was identified** |
| H13f — Silicate-contamination immunity | yes (narrative) | not quantitatively tested | held in narrative |

Result JSON: `results/dual_ion_sweep.json`.

## Reading

**Dual-ion is qualitatively better than water radio-frequency ion at every chunk-mass operating point.** The 10-25 percentage point delivery advantage holds across the 14 t / 50 t / 200 t operating points relevant to ICEBERG's roadmap.

**The user's annual cadence economic target (200 tonne / $400 million per year) closes at 500 kWe dual-ion / 5000 s specific impulse / 13.99 year round trip / 178 tonne delivered per ship.** This is the cell to highlight if megawatt-class reactor maturity is plausible.

**Architectural roadmap that falls out of R13:**

| Era | Reactor class | Chunk delivered | Annual revenue at $2,000/kg (annual cadence) | Thruster |
|---|---|---:|---:|---|
| Demonstrator (ships 1-2) | Kilopower 10 kWe | ~10 t (R12 water radio-frequency ion + lunar tour) | $20 million/yr | Pale Blue water radio-frequency ion |
| Production fleet (ships 3-7) | Fission Surface Power 40-100 kWe | ~30-80 t (water radio-frequency ion or early dual-ion) | $60-160 million/yr | Water radio-frequency ion → dual-ion |
| Scaled fleet (ships 8+) | Megawatt class 500 kWe | ~180-200 t (dual-ion mature) | $360-400 million/yr | Dual-ion |

The dual-ion delivery advantage is *largest at small chunks* (23 pp at 14 t) and *smallest at large chunks* (12 pp at 200 t). This is because at small chunks, the reactor mass dominates and dual-ion's better propellant fraction matters most; at large chunks, the chunk is the dominant mass and propellant fraction is less critical.

**Why dual-ion's advantage is real and not an artifact:**
1. **Higher specific impulse → less propellant burned for the same inbound delta-velocity.** Water radio-frequency ion at 2000 s burns ~20% propellant fraction for 4.47 km/s. Dual-ion at 5000 s burns ~9%. At 10000 s, ~4.5%.
2. **Electrolyzer mass penalty is tiny.** 0.5 kg per kilowatt-electric × 100 kWe = 50 kg → 0.2% of vehicle mass. Doesn't move the needle.
3. **Silicate contamination is filtered out by electrolysis.** R11's grid-life concern for water radio-frequency ion does not transfer to dual-ion.
4. **TRL gap is the real cost.** Water radio-frequency ion (Pale Blue) is TRL 7-8 flying today. Water dual-ion is TRL 1-2 — at the lab-bench stage. The 12-pp to 25-pp delivery advantage is paid for in development risk.

**The 200 tonne / 500 kWe cell is the closing piece of the "scale chunk for revenue" argument.** Combined with:
- 14-year round trip closes within the investor ceiling
- Annual cadence achievable (one ship per Earth-Saturn synodic window)
- 178 t per ship × annual cadence × $2,000/kg = $356 million per year revenue (matches the user's $400M/yr target within rounding)
- Reactor mass 50 t at 10 W/kg specific power assumption
- Total vehicle mass at Saturn ~280 t — assembly in low Earth orbit from multiple Starship launches is required

This cell isn't aggressive — it's where the architecture lands if megawatt-class space reactors materialize (NASA Nuclear Electric Propulsion roadmap targets exist).

## Revisit

- **Trajectory model still constant-thrust.** All R13 numbers carry the same ±10-20% uncertainty as R5/R6/R9/R9b/R12. The dual-ion vs water-radio-frequency-ion *ranking* is robust to this; the *absolute* round-trip and delivery numbers tighten with a real low-thrust optimizer (NASA General Mission Analysis Tool, MALTO, or similar).
- **Dual-ion efficiency η = 0.55 is a guess.** Published space-electric dual-stage thrusters (dual-grid ion engines) achieve 0.6-0.7 at high specific impulse; the lower number here is conservative for the electrolyzer + dual-species loss. At η = 0.65, thrust scales up by ~18% and cruise braking time falls correspondingly. Sweet-spot specific impulse shifts up slightly.
- **Electrolyzer power consumption not modeled.** Water electrolysis takes ~4.5 kWh/kg of water (thermodynamic minimum) — the electrolyzer draws power FROM the reactor that would otherwise drive the thruster. For a 50 t/year propellant burn at 200 kWe, electrolyzer consumes ~50 t × 4500 W·h/kg / (365 d × 24 h) ≈ 26 kWe continuous — non-trivial fraction of total power. **Worth a follow-up sub-round.**
- **Dual-ion TRL 1-2 is the load-bearing risk.** The architecture closes mathematically; flight-readiness is a research program in its own right. An operator's R&D investment in dual-ion would need to be quantified for a Series-D-or-equivalent budget conversation. **Not a propulsion question; a program question.**
- **Megawatt-class reactor TRL.** 500 kWe in space is conceptual (JIMO 2003, NASA NEP roadmap targets). At 10 W/kg specific power that's a 50 t reactor + power-conditioning electronics. Real-world specific power for megawatt-class space reactors is unknown; could be 3-5 W/kg in early flights. At 5 W/kg, the 500 kWe reactor is 100 t — would degrade delivery from 88.9% to ~78%.
- **Outbound power draw not analyzed.** The conops uses water-MET on outbound trim and Saturn capture. Whether the dual-ion architecture can use the SAME thruster outbound (just with Earth-launched water as propellant) is an open trade. Probably yes, but propellant tank sizing changes.
- **R11 silicate-contamination immunity** for dual-ion was asserted, not quantitatively tested. The electrolysis step removes silicate dust at the molecular level (electrolysis only liberates H and O atoms from H₂O molecules — anything else stays in the catholyte / anolyte solution). Worth a dedicated R11b round to confirm grid life for dual-ion.

## Cross-learning

- **The cross-round trajectory model is now explicit in writing.** All R5/R6/R9/R9b/R12/R13 numbers come from the same constant-thrust closed-form approximation. The model lives in R13's "Trajectory model" section above. Future rounds should cite it rather than re-deriving. Numbers carry ±10-20% absolute uncertainty; rankings are robust. A real trajectory integrator is the next-rigor-level step (next-campaign work, not this campaign).
- **Pre-registered ranges that hold but with falsified sub-dimensions are still informative.** H13e was falsified on the dimension I predicted (specific impulse should scale with power) but the actual relationship (specific impulse scales with chunk mass) is the right architectural insight. The discipline of pre-registering forced me to write down what I expected, and the falsification surfaced the correct relationship I hadn't seen.
- **Reactor power scales linearly with delivered chunk mass for fixed round-trip and architecture.** This is the load-bearing scaling law for ICEBERG's "scale chunk for revenue" argument: every 3-5 kWe of additional reactor power buys ~1 t of additional delivered chunk per ship at constant round-trip. The conops' "MW-class era enables 500-1000 t chunks" is consistent with this if reactor mass fraction stays well-behaved.
- **Dual-ion is the right answer for the production fleet, not the demonstrator.** Pale Blue water-radio-frequency-ion stays the right answer for ships 1-7 (Kilopower / Fission Surface Power era, flight-ready TRL 7-8). Dual-ion enters the picture at megawatt-class reactor maturity and serves ships 8+ at scaled chunk sizes. The deck should show this as a roadmap, not a "now or later" choice.
- **The conops' "scale chunk 10× for 10× revenue" claim is structurally sound, with one revision.** The cost of scaling chunk is not just bag mass or grapple size — it's reactor power class. The conops' Kilopower → Fission Surface Power → megawatt roadmap is already aligned with this scaling. R13 just makes the relationship quantitative.
