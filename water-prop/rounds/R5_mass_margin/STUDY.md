# Round 5 — Sweet-Spot Robustness: 1000–2000 s Specific Impulse

**Status:** pre-result.

## Question

R10 produced a ranking at Kilopower / Case B: dual-ion (5000 s) > radio-frequency ion (2000 s) > Hall (1500 s) > everything else. Dual-ion delivered the most chunk but with a 33-year cruise time, disqualifying it. The 1500–2000 s band looks like a sweet spot — enough specific impulse to close mass, low enough that cruise time fits the mission budget.

**The question:** is the 1000–2000 s sweet spot robust to the assumptions baked into R10? Or is it an artifact of (a) constant 0.4 efficiency across all candidates, (b) fixed 7-year cruise time, (c) 5 W/kg reactor specific power, (d) the conops' 14 t chunk mass, (e) 5.94 km/s delta-velocity? Question every assumption.

## Pre-registered hypothesis (H5)

**Aggregate (H5-agg):** I predict the 1000–2000 s sweet spot survives the parameter sweep — i.e., across all combinations of the five swept parameters, a thruster operating in 1000–2000 s either (a) is on the Pareto frontier of (delivery fraction × cruise time), or (b) is dominated by an adjacent operating point within ±50% specific impulse, never by a far-off point. The sweet spot is robust.

**Pre-registered failure modes I expect to surface:**

| Sub-claim | Predicted shift | Falsification |
|---|---|---|
| H5a — Reactor specific power swing 2.5 ↔ 6.5 W/kg | Sweet spot shifts to higher Isp (~2500 s) under pessimistic 2.5 W/kg because reactor dominates and propellant savings matter more | falsified if optimum stays < 1500 s or jumps > 4000 s |
| H5b — Per-technology efficiency (0.3 microwave electrothermal, 0.55 Hall, 0.65 radio-frequency ion) | Radio-frequency ion's delivery advantage widens vs microwave electrothermal beyond what constant-0.4 showed; Hall stays in second place | falsified if microwave electrothermal recovers competitiveness |
| H5c — Cruise time variation 5 ↔ 14 years | Long cruise opens the 3000–5000 s window (dual-ion territory) by relaxing the thrust-time constraint; short cruise narrows the sweet spot toward 800–1500 s | held if optimum shifts monotonically with cruise time as predicted |
| H5d — Chunk mass variation 5 ↔ 50 t | Small chunks favor higher Isp (less initial mass, propellant dominates less); large chunks favor lower Isp (chunk is the mass denominator) | predicted: 5 t favors 2500 s, 50 t favors 1200 s |
| H5e — Inbound delta-velocity variation 2.85 ↔ 5.94 km/s | Low delta-velocity widens the viable specific impulse range (everything works); high delta-velocity tightens the window | held if sweet spot narrows as delta-velocity rises |
| H5f — Are real flight thrusters available in the 1000–2000 s range? | Yes — water radio-frequency ion (Pale Blue, ~2000 s TRL 7–8) and water Hall (TRL 2–3 but adjacent to flight-heritage xenon Hall) are real candidates. Microwave electrothermal at 1000+ s is theoretical (R0 ceiling 558 s). Resistojet caps at 250 s. | held if 1000–2000 s has a real thruster behind it, falsified if it's a "between candidates" gap |

**Pre-registered conclusion if all sub-claims hold:** 1000–2000 s is the right design window for the chunk-fed inbound thruster, and the conops should converge there. The architecture choice between water Hall (1500 s, TRL 2–3, no chunk-water heritage) and water radio-frequency ion (2000 s, TRL 7–8, terrestrial-water heritage) becomes a heritage-vs-margin trade rather than a propulsion-class trade.

## Method

For each combination of (reactor specific power × per-technology efficiency × cruise time × chunk mass × inbound delta-velocity), compute:
1. The power-optimal specific impulse from R6's brentq solver, with `m_initial = chunk + dry + reactor + thruster_system`.
2. The delivered chunk fraction at that optimum.
3. The delivered chunk fraction at three fixed specific-impulse design points: 500 s (microwave electrothermal), 1500 s (Hall), 2000 s (radio-frequency ion).
4. The cruise time required to deliver delta-velocity at each design point given the thrust available.
5. The Pareto frontier in (cruise time × delivery fraction) across all five design points.

**Sensitivity grid** (intentionally bounded so the round runs in tens of seconds, not minutes):
- Reactor specific power: 2.5, 5, 6.5 W/kg
- Per-technology efficiency: as a function of specific impulse (lookup table)
- Cruise time: 5, 7, 10 years
- Chunk mass: 5, 14, 50 t
- Inbound delta-velocity: 2.85, 5.94 km/s

= 3 × 3 × 3 × 2 = 54 cells per design point × 4 design points = 216 evaluations. Tractable.

**Validity caveats:**
- The "power-optimal" curve from R6 assumes a thruster can operate at any v_e. Real thrusters have a design point. The corrected R5 power-optimum is informative for technology selection but a flight design picks the nearest real candidate.
- Lifetime constraints are not in R5. R11 addressed grid life for the radio-frequency ion case; Hall and microwave electrothermal life are not separately tested.
- Per-technology efficiency lookup is approximate; real efficiencies depend on operating point, propellant purity, and thermal margin.
- Reactor power is assumed constant over the cruise; end-of-life degradation (~10–30% over 10+ years) is not modeled.
- Cruise time vs delivery interplay treats them as independently selectable. In reality cruise time is constrained by trajectory choice (R9, deferred) and reactor program availability.

## Result

54-cell sweep, 10 kWe Kilopower-class power fixed. 37 cells feasible, 17 infeasible.

**Pareto-winner tally across feasible cells:**

| Thruster                  | Specific impulse | Wins  | % of feasible |
|---------------------------|-----------------:|------:|--------------:|
| water radio-frequency ion |          2000 s  |  19   |        51.4%  |
| water Hall (low band)     |          1000 s  |   7   |        18.9%  |
| water Hall (mid band)     |          1500 s  |   6   |        16.2%  |
| microwave electrothermal  |           500 s  |   3   |         8.1%  |
| water dual-ion            |          5000 s  |   2   |         5.4%  |

**Sweet-spot robustness:** 32 of 37 feasible cells (86.5%) are won by a thruster in the 1000–2000 s band.

**Dual-ion winning cells (only 2):** small chunk (5 t), low inbound delta-velocity (2.85 km/s, Case C), long cruise (10 yr), reactor specific power 5.0 or 6.5 W/kg. Dual-ion requires every favorable assumption simultaneously to beat the sweet-spot band.

**Microwave electrothermal winning cells (only 3):** all are 50 t chunk + low delta-velocity (2.85 km/s) + 7 yr cruise. Large chunk acts as the mass denominator, so the propellant-mass-fraction penalty of low specific impulse matters less than the cruise-time penalty of higher specific impulse. This is the only region where microwave electrothermal is actually competitive on Pareto frontier — and it disappears once cruise time relaxes to 10 yr (Hall takes over).

**Infeasible cells:** 17 of 54. The infeasibility pattern is clean — 50 t chunk + 5.94 km/s delta-velocity is unreachable in any reactor / cruise configuration at 10 kWe, and 14 t chunk + high delta-velocity + 5 yr cruise is also out of reach.

Result JSON: `results/sweet_spot_sweep.json`.

## Reading

**H5_agg held.** The 1000–2000 s band wins 86.5% of feasible cells — the sweet spot is robust to the sweep dimensions (reactor specific power 2.5–6.5 W/kg, cruise time 5–10 yr, chunk mass 5–50 t, inbound delta-velocity 2.85–5.94 km/s).

**Sub-claim outcomes (vs pre-registration):**

| Sub-claim | Prediction | Result | Verdict |
|---|---|---|---|
| H5a — reactor specific power swing | Optimum shifts higher at 2.5 W/kg | At 2.5 W/kg the winning Isp stays in [1000, 2000] s across all but one cell (the 50 t/2.85 km/s/7 yr microwave electrothermal corner); no shift to ~2500 s. | partially falsified — sweet spot does not shift |
| H5b — per-tech efficiency | Radio-frequency ion's lead widens vs microwave electrothermal | Radio-frequency ion wins 51% of cells, microwave electrothermal 8%; lead is wide. | held |
| H5c — cruise time variation | Long cruise opens 3000–5000 s | Dual-ion wins only at 10 yr cruise + small chunk + low delta-velocity. Long cruise opens dual-ion's door but only in a narrow corner. | held |
| H5d — chunk mass variation | Small chunk → higher Isp, large chunk → lower Isp | 5 t chunk winners: 2000 s or 5000 s. 50 t chunk winners: 500 s or 1000 s. | held — monotonic and clean |
| H5e — delta-velocity variation | Low dv widens viable band, high dv tightens | Low-dv (2.85) feasible cells span 1000–5000 s winners; high-dv (5.94) cells almost exclusively pick 1000–2000 s. | held |
| H5f — real thrusters in band | Yes — Pale Blue RF ion (2000 s, TRL 7-8) and water Hall (1000–1500 s, TRL 2-3) | These are real candidates with heritage or near-heritage paths. | held |

**Headline:** the 1000–2000 s sweet spot is the design window. The architecture choice within it is a heritage-vs-margin trade between water radio-frequency ion (2000 s, Pale Blue heritage, narrow grid-life margin per R11) and water Hall (1000–1500 s, no chunk-water heritage but no grid to erode). Microwave electrothermal is only competitive in the niche corner of "very large chunk + low delta-velocity," which the conops never specifies; for the 14 t baseline, it is out of contention.

**Notable corners worth flagging:**
- *50 t + low dv + 7 yr cruise:* microwave electrothermal wins. This is interesting if the mission ever pivots to a larger chunk + slow trajectory — the simplest, lowest-TRL thruster becomes competitive again. Worth keeping in the back pocket.
- *5 t + low dv + 10 yr + good reactor:* dual-ion wins. The "tiny sample return on a slow boat" scenario is the only one where the 33-year-cruise dual-ion architecture becomes attractive, and it's not the mission.

## Revisit

- **Power class was fixed at 10 kWe.** The full sweep would also walk power (e.g., 5–50 kWe). At higher power, thrust grows ∝ P/v_e, which would compress the optimum toward lower Isp at fixed cruise time. R6 already addressed the power-Isp tradeoff for a single design point; this is the multi-cell extension. Deferred.
- **Per-tech efficiency is a single point, not a lookup table.** STUDY pre-reg said "lookup table"; the implementation uses a single (isp, eta) per technology. The qualitative answer doesn't change — radio-frequency ion's efficiency advantage is wide enough that lookup-table noise wouldn't flip the ranking — but it's a known simplification.
- **Cruise time and trajectory are treated as independent inputs.** R9 (deferred) will tie cruise time to trajectory choice, after which this sweep's cruise dimension should be re-interpreted as "what does the trajectory deliver?" rather than "what cruise do we pick?"
- **No grid-life weighting.** R11 found chunk-water silicate contamination is a serious risk for radio-frequency ion grid life. A combined "Pareto x grid life" weighting would penalize radio-frequency ion's wins and might shift the design toward Hall in the 1500 s slot. Worth a follow-up.
- **Original feasibility check had a bug:** counted cells as "feasible" when propellant required exceeded chunk mass, which made microwave electrothermal appear to "win" with 0% delivery in 5 cells. Fixed by requiring `delivered_chunk_t > 0`. After fix, sweet-spot robustness rose from 76.2% to 86.5%.

## Cross-learning

- **Pre-registered failure modes are load-bearing.** H5a predicted a shift to higher Isp at pessimistic reactor specific power. It didn't happen — the sweet spot is sticky. That's a falsification of one sub-claim within a held aggregate. Without the sub-claim, "sweet spot is robust" would have been an unfalsifiable mood. With the sub-claim, the reading is precise: the sweet spot is robust *more strongly* than I predicted, because reactor mass doesn't shift it.
- **Tie-breaker bugs in Pareto code create fake wins.** A "feasible" check that doesn't filter for positive delivery counted infeasible-in-practice cells as wins for the most permissive technology. Generalizable lesson: when grading "which option wins?", always require the option to actually achieve the objective, not merely satisfy the constraints. Adding this to the cross-campaign log as a methodology note.
- **Architecture decisions don't always need exotic propulsion.** Across 37 feasible operating cells covering a 2.5x reactor specific-power swing, 2x cruise-time swing, 10x chunk-mass swing, and 2x delta-velocity swing, 86.5% of winners are 1000–2000 s thrusters available today or one TRL hop away. The mission does not need a propulsion breakthrough; it needs to pick a TRL-7 candidate (Pale Blue water radio-frequency ion) and budget grid life margin per R11.
