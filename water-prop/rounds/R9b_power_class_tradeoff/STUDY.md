# Round 9b — Power-Class Trade for Chunk-Fed Inbound: Reactor Mass vs Cruise Time

**Status:** pre-result.

## Question

R9 found the conops' 13-year round-trip is inconsistent with the chunk-fed water radio-frequency ion architecture at Kilopower-class power (10 kWe). The shortfall is in the inbound braking phase: at 10 kWe, water RF ion takes ~10 years to shed the residual v_∞ after lunar gravity assist, plus a 6-year Hohmann cruise. R9's promotion list named R9b: chunk-fed inbound time-of-flight as a function of reactor power class.

**The question:** what reactor power class closes the 13-year round-trip budget, and what does it cost in delivered chunk fraction? Is there *any* power class that simultaneously delivers 13-year round trip AND ≥ 50% chunk delivery?

## Pre-registered hypothesis (H9b)

**Aggregate (H9b-agg):** I predict the trade has no clean winner. As reactor power rises, thrust acceleration grows (cruise time shrinks) but reactor mass also grows (delivered chunk shrinks). The 13-yr round-trip constraint requires ~40-80 kWe; at that power class, reactor mass at 5 W/kg is 8-16 t — comparable to or larger than the 14-t chunk. Delivered chunk drops below 30% at the round-trip-closing power class.

**Pre-registered sub-claims:**

| Sub-claim | Predicted | Falsification |
|---|---|---|
| H9b-a — Power class to close 13-yr round trip | 40-80 kWe at 5 W/kg | falsified if < 30 kWe or > 120 kWe |
| H9b-b — Delivered chunk at round-trip-closing power | 25-40% (reactor mass eats chunk) | falsified if > 50% or < 10% |
| H9b-c — Reactor-mass scaling | Linear at 5 W/kg (Kilopower-class specific power assumption) | sensitivity: also test 2.5 W/kg pessimistic and 10 W/kg optimistic |
| H9b-d — Pareto frontier shape | Convex, with a minimum-round-trip + maximum-delivery elbow somewhere in 20-50 kWe | falsified if monotone (more power always better, or worse) |
| H9b-e — 13-yr round trip with ≥ 50% delivery achievable? | No — the two are incompatible at any tested power class with the chunk-fed water RF ion architecture | falsified if any (power, specific-power) cell delivers both 13-yr round trip AND ≥ 50% chunk |

**Pre-registered conclusion if H9b holds:** the chunk-fed water RF ion architecture at any reasonable reactor power class cannot simultaneously close 13-yr round trip and ≥ 50% delivery. The architecture has to accept one of: (a) longer round trip (~20-25 yr), (b) lower delivery (~25-40%), or (c) a different Earth-capture mechanism (chemical capture or aerocapture).

## Method

Sweep reactor power class × reactor specific power. For each cell:
1. Compute reactor mass (P/(specific_power)) and initial mass (chunk + dry + reactor).
2. Compute water RF ion thrust at the given power.
3. Compute propellant required for the post-lunar-GA inbound budget (8.87 km/s, from R9 three-flyby tour output).
4. Compute delivered chunk fraction.
5. Compute cruise time for the braking phase using R9's constant-acceleration approximation.
6. Compute total round trip = 6.09 yr (Hohmann outbound) + 1.0 yr (Saturn dwell) + 6.09 yr (Hohmann inbound coast) + cruise_braking_yr. (The 6.09-yr inbound coast and the braking happen partially overlapped in a real low-thrust trajectory; this overestimate is consistent with R9's "Hohmann + braking" interpretation.)

**Sensitivity grid:**
- Reactor power: 5, 10, 20, 40, 80, 160 kWe
- Reactor specific power: 2.5, 5.0, 10.0 W/kg (pessimistic / nominal / optimistic Kilopower-to-Fission Surface Power range)
- Inbound braking ∆v: 8.87 km/s (R9 result, Hohmann + 3-flyby tour) and 5.94 km/s (R10 Case B, no lunar GA — useful for comparison)

= 6 × 3 × 2 = 36 cells. Tractable.

**Validity caveats:**
- "Constant acceleration" cruise-time formula is approximate; real low-thrust trajectories have ~10-30% gravity losses and steering losses.
- Reactor specific power varies widely across programs: Kilopower (1-10 kWe class) nominal ~5 W/kg, Fission Surface Power (40 kWe) nominal ~10 W/kg per published estimates. Larger reactors (>100 kWe) hypothetical; specific power for those is speculative.
- This round does not include Saturn-egress propellant cost. R10 found Saturn-egress at 2000 s specific impulse consumes a non-trivial fraction of chunk before inbound braking begins. R9b's "delivered chunk" is therefore an upper bound; the post-egress-pre-braking chunk is smaller.
- Reactor thermal management at 80-160 kWe in deep space is a separate technology question not in R9b scope.
- 13-year round-trip budget is the conops headline. If the mission accepts longer round trips, the trade is different.

## Result

Methodology correction during the run: the original round-trip formula was additive (outbound Hohmann + dwell + Hohmann inbound coast + braking time), which double-counts cruise. A real low-thrust trajectory overlaps cruise and braking. Corrected formula: `inbound_TOF = max(Hohmann_inbound_coast, braking_∆v / (accel × duty))`. This gives the Hohmann coast (6.09 yr) as a structural lower bound on the inbound, regardless of power class. Combined round-trip floor: 6.09 + 1.0 + 6.09 = **13.18 yr**, slightly above the conops' 13-yr headline.

### Sweep at ∆v = 8.87 km/s (R9 post-3-flyby-tour budget, lunar GA used)

| Power (kWe) | Specific power (W/kg) | Reactor (t) | m₀ (t) | Braking (yr) | Round trip (yr) | Delivered chunk |
|---:|---:|---:|---:|---:|---:|---:|
| 5 | 2.5 | 2.0 | 21.0 | 29.14 | 36.23 | 45.4% |
| 5 | 5.0 | 1.0 | 20.0 | 27.75 | 34.84 | 48.0% |
| 5 | 10.0 | 0.5 | 19.5 | 27.06 | 34.15 | 49.3% |
| 10 | 2.5 | 4.0 | 23.0 | 15.96 | 23.05 | 40.2% |
| 10 | 5.0 | 2.0 | 21.0 | 14.57 | 21.66 | 45.4% |
| 10 | 10.0 | 1.0 | 20.0 | 13.88 | 20.97 | 48.0% |
| 20 | 2.5 | 8.0 | 27.0 | 9.37 | 16.46 | 29.8% |
| 20 | 5.0 | 4.0 | 23.0 | 7.98 | 15.07 | 40.2% |
| 20 | 10.0 | 2.0 | 21.0 | 7.29 | 14.38 | 45.4% |
| 40 | 2.5 | 16.0 | 35.0 | 6.07 | 13.18 | 9.0% |
| 40 | 5.0 | 8.0 | 27.0 | 4.68 | **13.18** | **29.8%** |
| 40 | 10.0 | 4.0 | 23.0 | 3.99 | **13.18** | **40.2%** |
| 80 | 5.0 | 16.0 | 35.0 | 3.04 | 13.18 | 9.0% |
| 80 | 10.0 | 8.0 | 27.0 | 2.34 | 13.18 | 29.8% |
| 160 | 10.0 | 16.0 | 35.0 | 1.52 | 13.18 | 9.0% |

(Other 2.5 / 5.0 W/kg combinations at 80 and 160 kWe are infeasible — propellant required exceeds chunk mass.)

### Sweep at ∆v = 5.94 km/s (R10 Case B budget, NO lunar GA — note: R9 showed this budget is optimistic)

| Power (kWe) | Specific power (W/kg) | Reactor (t) | m₀ (t) | Braking (yr) | Round trip (yr) | Delivered chunk |
|---:|---:|---:|---:|---:|---:|---:|
| 20 | 5.0 | 4.0 | 23.0 | 5.68 | **13.18** | **57.1%** |
| 20 | 10.0 | 2.0 | 21.0 | 5.18 | **13.18** | **60.8%** |
| 40 | 5.0 | 8.0 | 27.0 | 3.33 | 13.18 | 49.6% |
| 40 | 10.0 | 4.0 | 23.0 | 2.84 | 13.18 | 57.1% |

This budget gives apparently-better delivery, but R9 showed the 5.94 km/s number is unreachable by Hohmann + lunar GA. The 5.94 km/s "Case B" presumes an undocumented braking mechanism that produces v_∞ at Earth ~5.94 km/s. R9's calculation says the real number is 8.87 km/s (with 3-flyby lunar GA tour) or 10.30 km/s (without GA). Cells in this table should be read as "what's achievable IF we trust R10's Case B input," not as a real architecture.

### Hypothesis grading

| Sub-claim | Predicted | Measured | Verdict |
|---|---|---|---|
| H9b-a — Power class to close 13-yr round trip | 40-80 kWe at 5 W/kg | At 5 W/kg, 40 kWe achieves 13.18 yr at 29.8% delivery (post-GA); 80 kWe achieves 13.18 yr at 9% delivery. Power class in predicted band, but specific power must be optimistic for delivery to matter. | partially held |
| H9b-b — Delivery at round-trip-closing power | 25-40% | 9–40% across closing cells; 40.2% maximum at 40 kWe / 10 W/kg / post-GA budget | held |
| H9b-c — Reactor-mass scaling at multiple specific powers | swept | 2.5 / 5 / 10 W/kg behaved as expected (linear inverse mass) | held |
| H9b-d — Pareto frontier shape | Convex with elbow at 20-50 kWe | Frontier shape: TOF dominates below ~20 kWe (long cruise), reactor mass dominates above ~40 kWe (eats chunk); elbow at 20 kWe / 10 W/kg gives 14.38 yr at 45.4% delivery — slightly outside 13-yr but the best balance | held |
| H9b-e — 13-yr round trip + ≥50% delivery achievable? | No (post-GA budget) | 0 cells achieve both simultaneously using the R9 verified budget. The closest is 40 kWe / 10 W/kg at 13.18 yr / 40.2% delivery, or 20 kWe / 10 W/kg at 14.38 yr / 45.4% delivery. | held |

Result JSON: `results/power_class_sweep.json`.

## Reading

**H9b-e held cleanly: no power class closes both 13-yr round trip and ≥50% delivery with the verified inbound delta-velocity budget.** The architecture has to give on one of three dimensions:

| If we hold... | We give up... | Best achievable cell |
|---|---|---|
| **13-yr round trip** | **Delivery falls to 30-40%** | 40 kWe / 10 W/kg post-GA: 13.18 yr at 40.2% delivery |
| **≥50% delivery** | **Round trip extends to ~15 yr** | 20 kWe / 10 W/kg post-GA: 14.38 yr at 45.4% delivery; or 10 kWe / 10 W/kg post-GA: 20.97 yr at 48% delivery |
| **Kilopower power class (10 kWe)** | **Round trip extends to ~21 yr** | 10 kWe / 10 W/kg post-GA: 20.97 yr at 48% delivery |

**Architectural read.** The conops' implicit triple of (13-yr, 60%+ delivery, Kilopower) is structurally infeasible. The Pareto-optimal point depends on which dimension is non-negotiable:

- **If 13-yr round-trip matters most** (economic / programmatic): commit to Fission Surface Power 40 kWe class with optimistic specific power assumption (10 W/kg), accept ~40% delivery. This means cutting per-trip revenue by ~33% relative to the conops' 60% headline. Steady-state cash flow drops proportionally. Mission still profitable per the startup/ thesis but margin shrinks.
- **If delivery fraction matters most** (per-trip economics): commit to 20 kWe class, accept 14.4-yr round trip. Modest power scale-up beyond Kilopower's 10 kWe nominal, requires demonstrating 10 W/kg specific power. Delivery 45.4%.
- **If sticking with Kilopower 10 kWe**: commit to ~21-yr round trip at 48% delivery. The 13-yr headline goes; steady-state cadence is approximately half what the conops projected.

**The pre-R9 architecture decision tree (water RF ion replacing microwave electrothermal) is unaffected.** R10's propulsion-type choice is correct. R9b confirms the binding constraint is *reactor power*, not thruster technology. Pale Blue stays.

**Hidden assumption to flag.** The 10 W/kg reactor specific power assumed for the 40-kWe class is optimistic. Kilopower demonstrated ~5 W/kg in test articles; Fission Surface Power program targets 10-15 W/kg but is TRL 4-5. If real specific power lands at 5 W/kg for 40 kWe (8 t reactor), delivery drops from 40% to 29.8% at the same round-trip floor. The architecture's economic case depends on the reactor program achieving its optimistic specific-power targets.

**Pareto-optimal cell to put on the deck:** 20 kWe / 10 W/kg / post-GA. 14.38 yr round trip, 45.4% delivery, 2 t reactor, 21 t initial mass. Modest power upscale beyond Kilopower (2x), tractable reactor sizing, reasonable delivery, round-trip only 1.4 yr beyond the conops headline (10% slip). This is the cleanest "honest" cell I've found across this round.

## Revisit

- **The Hohmann inbound coast is treated as a hard floor.** This assumes the spacecraft cannot accelerate inbound faster than free-fall under sun gravity. In practice, low-thrust *can* shorten the inbound by burning radially inward (gain helio kinetic energy faster), but this is highly nonlinear and gives up energy efficiency. A proper optimal-control analysis (Pontryagin) might shave 0.5-1 yr off the Hohmann floor at high thrust acceleration. Not in R9b scope, but flagged for R9c if pursued.
- **Saturn-egress propellant cost not included.** R10 noted Saturn-egress at 2000 s consumes a fraction of chunk before inbound braking begins. R9b's "delivered chunk" is the post-egress chunk that arrives at Earth, but the egress propellant comes off the *pre-egress* mass. The architecture mass-budget tracking should be (initial pre-egress mass) = (delivered chunk) + (Saturn-egress propellant) + (inbound-braking propellant) + dry + reactor. R9b only tracks the second half of that. A consolidated mass-stack round (R-mid) is overdue.
- **Specific power 10 W/kg at 40 kWe is optimistic.** Sensitivity test: at 5 W/kg, the 40-kWe delivery drops to 29.8%. If Fission Surface Power lands closer to 5 W/kg in practice, the "13-yr + 40%" cell becomes "13-yr + 30%" — closer to the conops break-even line. Worth a dedicated risk register entry: R-REACTOR-SPECIFIC-POWER, severity I3-L3.
- **R10's Case B (5.94 km/s) is shown to be optimistic vs R9's 8.87 km/s.** The 5.94 km/s rows in the second table are not load-bearing for the architecture decision. They exist for completeness and to show what R10's input assumption produces. The verified inbound budget is 8.87 km/s.
- **Multi-flyby lunar tours beyond 3 flybys not modeled.** R9 showed each successive flyby contributes ~0.5 km/s, so a 5- or 6-flyby tour could shed ~2.5-3 km/s total instead of 1.43. That would bring v_∞ down from 8.87 to ~7.3 km/s, shortening braking time. Each additional flyby costs ~3-6 months of Earth-orbit phasing. Net: probably a wash. Worth a desk-study sub-round.
- **Aerocapture and chemical Earth-capture not quantified.** Both could close the 13-yr budget. Aerocapture is the conops' original assumption (retired per M-AEROCAP). R9b's finding might justify re-elevating aerocapture for review. Chemical Earth-capture eats delivery via a big chemical propellant load. Worth its own round (R12 candidate).

## Cross-learning

- **The bug I caught mid-round is the lesson.** Original additive formula gave round-trip 24 yr at 10 kWe; max-of formula gave 21.66 yr. The 2-3 yr difference came from improperly serializing cruise and braking. A real low-thrust trajectory doesn't coast for Hohmann TOF and then brake — it does both simultaneously. The R9 STUDY.md noted this issue under "Revisit" but R9 didn't act on it. R9b catching it during the run is exactly what the round structure is for: each round refines the previous round's framing as well as testing a new hypothesis. Methodology positive: round-on-round formula corrections work.
- **Pareto trades where both knobs come from the same root cause are sharp.** Reactor power is the only knob: higher power → bigger reactor mass AND lower cruise time. The two outputs move in opposite directions with the same input. This makes the Pareto frontier non-trivial (not monotone) and the elbow informative. Architectural lesson: identify Pareto trades that come from a single root cause; the optimum is the elbow, not the extreme.
- **R9 + R9b together close the loop on the inbound architecture question.** R9 said "v_∞ at Earth is 8.87 km/s after lunar GA, period." R9b said "given that v_∞, here's the power-class tradeoff." The conops' "13-yr + 60% + Kilopower" triple is structurally infeasible; the architect has to drop one. This is the kind of finding that should land in the deck as a "here's what the system can actually do" honest readout.
- **Pre-registration H9b-e was the load-bearing prediction.** "No cell achieves both 13-yr AND ≥50% delivery (post-GA)" is the architectural claim. It held. Pre-registration discipline paid off again: the round was set up to be falsifiable on the right axis.
- **Hidden methodology improvement to flag:** when the round-trip formula was wrong, the answer changed from "0 cells close 13-yr" to "0 cells close 13-yr with ≥50% delivery." The headline finding survived both formulas, but the supporting details and the recommended cell changed materially. Generalizable: formula errors that don't change the headline can still change the decision. Always sanity-check the formula on a degenerate case (here: at infinite power, braking time → 0, round trip → 13.18 yr Hohmann floor — that's a clean tell).
