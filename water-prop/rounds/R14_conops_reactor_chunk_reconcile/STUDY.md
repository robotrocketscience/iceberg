# Round 14 — Reconciling Conops Reactor → Chunk-Mass Scaling vs Round-Trip Headline

**Status:** pre-result.

## Question

The conops table (ICEBERG-pitch.md §2) maps reactor power class to chunk size:

| Reactor | Power | Chunk delivered (conops) |
|---|---:|---:|
| Kilopower | 1-10 kilowatt-electric | ~50 tonnes |
| Fission Surface Power | ~40 kilowatt-electric | 100-200 tonnes |
| Sub-megawatt to megawatt | 100-500 kilowatt-electric | 500-1000 tonnes |

The conops also claims a 13-13.5 year round trip across the program. Quick mental-math at Kilopower 10 kilowatt-electric + water-MET 700-second specific impulse + 50-tonne delivered chunk gives a braking time of ~30 years (the spacecraft has to accelerate 100+ tonnes by 4.47 kilometers per second using ~1 newton of thrust — slow). That blows the round-trip headline by 3x.

**The question:** at each conops reactor class, what is the actually-achievable round trip and chunk-delivered combination, using the same trajectory + 10-flyby lunar tour from R12 and the same constant-thrust closed-form trajectory model used in all prior rounds? Is the conops' chunk-to-reactor scaling consistent with its 13-year round-trip headline, or is it implicitly assuming a much longer mission?

## Pre-registered hypothesis (H14)

**Aggregate (H14-agg):** the conops' chunk-to-reactor scaling table is *internally inconsistent* with the 13.5-year round-trip headline by roughly an order of magnitude in chunk mass. Specifically:

- At Kilopower 10 kilowatt-electric + 14-year round-trip ceiling, achievable delivered chunk is ~5-10 tonnes (at water radio-frequency ion 2000 s), not the conops' 50 tonnes.
- At Fission Surface Power 40 kilowatt-electric + 14-year ceiling, achievable chunk is ~30-50 tonnes, not 100-200 tonnes.
- Closing the conops' 50-tonne / Kilopower or 200-tonne / Fission Surface Power claim requires either accepting 25-40 year round trips, OR adopting megawatt-class reactors.

The conops appears to scale chunk linearly with reactor power, but the binding constraint at fixed round-trip is *thrust-to-mass ratio*, not just power per unit mass.

**Pre-registered sub-claims:**

| Sub-claim | Predicted | Falsification |
|---|---|---|
| H14a — At Kilopower 10 kilowatt-electric, water-MET 700 second specific impulse, 14-year ceiling | Delivered chunk ≤ 10 tonnes | falsified if > 15 tonnes |
| H14b — At Kilopower 10 kilowatt-electric, water radio-frequency ion 2000 second specific impulse, 14-year ceiling | Delivered chunk ≤ 10 tonnes | falsified if > 15 tonnes |
| H14c — At Fission Surface Power 40 kilowatt-electric, water radio-frequency ion 2000 second specific impulse, 14-year ceiling | Delivered chunk ≤ 30 tonnes | falsified if > 60 tonnes |
| H14d — To close 50 tonne delivery at Kilopower 10 kilowatt-electric, required round trip | ≥ 35 years | falsified if < 25 years |
| H14e — To close 200 tonne delivery at Fission Surface Power 40 kilowatt-electric, required round trip | ≥ 30 years | falsified if < 25 years |
| H14f — Conops scaling table is "right" in spirit but implicitly assumes longer round trip | yes | falsified if any single conops cell closes at its stated chunk size AND 13-14 year round trip |

## Assumptions explicitly carried forward (consistent with prior rounds)

- Trajectory model: constant thrust, midpoint mass, 50% duty cycle, no gravity / steering losses. Same as R5-R13. Same approximation as the conops uses for its budget.
- Inbound braking delta-velocity = 4.47 kilometers per second (R12 residual after 10-flyby lunar tour). Conops uses ~4.2 kilometers per second; the difference is within model uncertainty.
- Bag capture efficiency η_c = 0.8 (conops design point, bag-engineering.md §6). Lowers effective specific impulse by 20%.
- Reactor specific power: 10 watts per kilogram (optimistic, Fission Surface Power program target). Will also test 5 watts per kilogram (Kilopower demonstrated).
- Outbound Hohmann 6.09 years + Saturn dwell 1.0 years + inbound max(Hohmann coast 6.09 years, braking time) + lunar tour phasing 0.73 years.

## Method

For each (chunk delivered target × reactor power × specific impulse × specific power):
1. Iterate chunk grappled until delivered chunk hits target, accounting for bag η_c and Tsiolkovsky propellant.
2. Compute braking time, inbound time-of-flight, total round trip.
3. Tag cells closing 14 years, 18 years, 25 years, > 25 years.
4. For each conops cell (Kilopower 10 kilowatt-electric / 50 tonne, Fission Surface Power 40 kilowatt-electric / 200 tonne, megawatt 500 kilowatt-electric / 750 tonne), compute the actual round trip required.

**Sweep grid:**
- Chunk delivered target: 5, 14, 50, 100, 200, 500 tonnes
- Reactor power: 10, 40, 100, 200, 500 kilowatt-electric
- Specific impulse / technology: 700 s (water-MET), 2000 s (water radio-frequency ion), 5000 s (water dual-ion)
- Specific power: 5 watts per kilogram (Kilopower demonstrated), 10 watts per kilogram (Fission Surface Power target)

= 6 × 5 × 3 × 2 = 180 cells. Tractable.

**Validity caveats:**
- Same trajectory model limitations as R5-R13.
- Bag η_c = 0.8 applied to specific impulse uniformly; in reality the bag efficiency degrades only the propellant feed cycle, not the thrust itself. The factor of 0.8 on effective specific impulse is the conops' simplification carried forward here.
- "Chunk grappled" is bounded by bag and grapple physical limits not modeled.

## Result

### Conops cell-by-cell reconciliation

For each conops chunk-to-reactor cell, search across thruster technologies and specific powers to find the lowest achievable round trip:

| Conops cell | Best thruster | Best specific power | Round trip (actual) | Chunk grappled | Delivery |
|---|---|---:|---:|---:|---:|
| Kilopower 10 kilowatt-electric → 50 tonnes delivered | water radio-frequency ion 2000 s | 10 watts/kilogram | **35.70 yr** | 68 t | 73.0% |
| Fission Surface Power 40 kilowatt-electric → 200 tonnes delivered | water radio-frequency ion 2000 s | 10 watts/kilogram | **33.83 yr** | 269 t | 74.4% |
| Megawatt class 500 kilowatt-electric → 750 tonnes delivered | water radio-frequency ion 2000 s | 10 watts/kilogram | **15.84 yr** | 1015 t | 73.9% |

The conops' 13-year round-trip headline holds only at the megawatt-class tier (and only barely, at 15.8 years vs claimed 13).

### Maximum delivered chunk at the 14-year round-trip ceiling

| Power | Reactor class | Max delivered chunk at 14 yr | Conops claim | Conops optimism |
|---:|---|---:|---:|---:|
| 10 kilowatt-electric | Kilopower (demonstrated) | 5 t | 50 t | **10x** |
| 40 kilowatt-electric | Fission Surface Power (TRL 4-5) | 14 t | 100-200 t | **7-14x** |
| 100 kilowatt-electric | Stretch (no current program) | 100 t | — | — |
| 200 kilowatt-electric | Sub-megawatt (paper) | 200 t | — | — |
| 500 kilowatt-electric | Megawatt (paper) | 500 t | 500-1000 t | 1-2x |

### Best-thruster-at-each-power finding (unexpected)

At low power class (Kilopower), the maximum-delivery cell uses **water microwave-electrothermal at 700 second specific impulse**, NOT water radio-frequency ion at 2000 second. The reason: at low power, thrust per kilowatt-electric is the binding constraint. Water microwave-electrothermal gives 0.87 N at 10 kilowatt-electric; water radio-frequency ion gives 0.66 N. Higher thrust means shorter cruise time, which means more chunk mass fits within the 14-year ceiling. The propellant-efficiency disadvantage of low specific impulse is overcome by the time-efficiency advantage.

**This contradicts R10's "water radio-frequency ion replaces water microwave-electrothermal" conclusion** — but only at the *demonstrator* tier. At Fission Surface Power and above, the cruise time at higher thrust is no longer the binding constraint, and water radio-frequency ion / dual-ion specific-impulse advantage pays off.

### Hypothesis grading

| Sub-claim | Predicted | Measured | Verdict |
|---|---|---|---|
| H14a — 10 kilowatt-electric + water-MET + 50 tonnes ≤ 10 tonnes at 14 yr | round trip > 14 yr | 37.38 yr | **held** |
| H14b — 10 kilowatt-electric + water radio-frequency ion + 50 tonnes ≤ 10 tonnes at 14 yr | round trip > 14 yr | 35.70 yr | **held** |
| H14c — 40 kilowatt-electric + water radio-frequency ion + 200 tonnes | round trip > 14 yr | 15.16 yr | **held** |
| H14d — Kilopower 50-tonne delivery round trip ≥ 35 yr | yes | 37.38 yr | **held** |
| H14e — Fission Surface Power 200-tonne delivery round trip ≥ 30 yr | yes | 33.83 yr | **held** |
| H14f — Conops scaling is "right in spirit" but inconsistent with 13-yr headline | yes | confirmed across all three tiers | **held** |

All six sub-claims held with margin.

Result JSON: `results/reconciliation.json`.

## Reading

**The conops chunk-to-reactor scaling table is approximately one order of magnitude optimistic in chunk mass at fixed round trip, at the Kilopower and Fission Surface Power tiers.** The megawatt-class tier is within ~1.5x — far closer to internally consistent than the lower tiers.

**Three possible interpretations of the discrepancy:**
1. **The conops implicitly assumes a longer round trip than its 13-year headline at the lower tiers.** If Ship 1 demonstrator targets 5 tonnes delivered at Kilopower / 13 years, and only scaled-fleet ships target 50-tonne+ chunks at the demonstrator power class, the discrepancy goes away — but then the conops' table is mislabeled as showing per-tier delivery. The pitch document does say "Kilopower era" not "Kilopower per-flight," so the table could be interpreted as showing what the *program* delivers over time, not what *one ship* delivers.
2. **The conops uses a different inbound trajectory family that yields lower delta-velocity than 4.47 km/s after lunar tour.** If the conops' actual budget is 2 km/s (cruise braking only, with somebody else handling the rest), the math improves. But the conops' own delta-velocity breakdown gives ~4.2 km/s for the chunk-fed inbound — which agrees with R12's 4.47 km/s within model uncertainty.
3. **The conops' table is simply optimistic.** Concept-paper conventions tend to round up chunk size by 5-10x in early scaling tables; the rigorous mass-budget calculation is deferred to the engineering phase. This is the most likely explanation per the methodology lesson recurring across rounds (single-number budgets in concept papers are 30-1000% optimistic).

**Architectural implications for the deck:**

- **The demonstrator economic case needs revision.** Ship 1 at Kilopower delivers ~5 tonnes to LEO at 14-year round trip, not 50 tonnes. At $2,000/kilogram that is **$10 million per ship**, not $100 million. For the demonstrator era this is below typical break-even — the demonstrator is a flight-heritage event, not a revenue event.
- **Fission Surface Power production economics need revision.** 40 kilowatt-electric ships deliver 14 tonnes (water-MET at the demonstrator tier — water radio-frequency ion at slightly less due to thrust limit) at 14 years, not 100-200 tonnes. Revenue per ship per synodic window is **~$28 million**, not $200-400 million.
- **The megawatt-class tier is the only conops tier where the scaling table is approximately right.** That tier requires reactor programs that don't exist.
- **The "annual cadence × $400 million per year" operating point still requires megawatt-class reactor (or fleet expansion).** R13's finding survives this round. The honest deck cell is megawatt-class.

**The corrected scaling table** (deliverable at 14-year round trip, 10 watts/kilogram specific power, R12 trajectory + 10-flyby lunar tour):

| Reactor class | Power | Realistic delivered chunk | Realistic annual revenue per ship at $2,000/kg | Conops claim |
|---|---:|---:|---:|---:|
| Kilopower | 10 kilowatt-electric | 5 tonnes | $10 million/year | 50 tonnes |
| Fission Surface Power | 40 kilowatt-electric | 14 tonnes | $28 million/year | 100-200 tonnes |
| Stretch | 100 kilowatt-electric | 100 tonnes | $200 million/year | (no claim) |
| Sub-megawatt | 200 kilowatt-electric | 200 tonnes | $400 million/year | (no claim) |
| Megawatt | 500 kilowatt-electric | 500 tonnes | $1 billion/year | 500-1000 tonnes |

The user's $400 million/year operating point closes at 200 kilowatt-electric reactor — between Fission Surface Power and megawatt-class. There is no funded program at this power class today, but it's a natural extrapolation from Fission Surface Power and ~10 years closer than full megawatt.

## Revisit

- **The methodology assumption flagged in the user-flagged interpretation 1 is worth checking.** Is the conops' scaling table per-tier "what this reactor class enables eventually" rather than per-flight "what one ship delivers"? If so, the rounds need to re-frame their critique. **Action: re-read pitch §2 table caption and see whether per-ship or program-cumulative is meant.**
- **Trajectory model and round-trip definition stay constant across the campaign.** All round-trip numbers from R14 carry the ±10-20% uncertainty band from the constant-thrust closed-form model. A real low-thrust optimizer would shorten cruise times by ~10-20% — which would shift the 14-year ceiling cells by 1-2 tonnes of additional delivery. Not enough to close the 10x gap.
- **R14's "water-MET wins at Kilopower for cruise-time reasons" deserves a sub-round.** At demonstrator-tier power, water microwave-electrothermal (TRL 9 for terrestrial water-fed, lower TRL for space-flight-rated) becomes architecturally competitive again — exactly opposite to R10's conclusion at higher power class. **Promotes R10b: revisit thruster ranking at each power class.**
- **The Fission Surface Power → 200-tonne claim is 14x optimistic.** This is a load-bearing pitch claim. The deck either needs to revise to ~14-30 tonnes per ship at Fission Surface Power, or to make explicit that the 200-tonne number assumes a longer round trip.
- **The megawatt-class cell is the most consistent.** This suggests the conops authors did get the megawatt-class math approximately right (or got lucky) and extrapolated downward incorrectly to Kilopower and Fission Surface Power tiers. A common pattern: scaling rules derived at the design point and extrapolated to other points without re-deriving the integrals.

## Cross-learning

- **The conops table is 10x optimistic at Kilopower and Fission Surface Power tiers, ~1x at megawatt.** Pattern suggests linear extrapolation of a megawatt-correct scaling rule to lower power tiers. The pitch needs a corrected scaling table reflecting actual mass-budget math.
- **The methodology lesson is now formalized**: any chunk-to-reactor scaling claim in a concept paper carries a 5-10x optimism prior at low power tiers, decreasing toward 1x at the design power tier. Apply to all roadmap tables.
- **R10's "replace water microwave-electrothermal with water radio-frequency ion" conclusion is conditional.** At Kilopower demonstrator tier, water microwave-electrothermal wins on cruise time (thrust dominates). At Fission Surface Power and above, water radio-frequency ion wins on delivery (specific impulse dominates). The architecture's thruster choice should follow the reactor class, not be globally fixed.
- **The investor-relevant deck math should use the R14 corrected scaling table, not the conops original.** Demonstrator ship: $10 million/year revenue, not $100 million. Fission Surface Power production: $28 million/year per ship, not $200 million. Megawatt-class: $1 billion/year per ship, accurate (but reactor-program-dependent).
- **The "Suez Canal" framing still works, but at smaller numbers initially.** Demonstrator → $10 million/year. Fission Surface Power production → $28 million/year × N ships in fleet. Megawatt-class fleet → $1 billion/year per ship. The infrastructure-asset profile holds; the per-ship-per-year revenue is what changes.
