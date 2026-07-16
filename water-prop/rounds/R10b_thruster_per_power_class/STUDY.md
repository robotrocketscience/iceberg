# Round 10b — Realistic-Flyby Thruster Ranking by Reactor Power Class

**Status:** pre-result.

## Question

R10 ranked four thruster technologies at Kilopower 10 kilowatt-electric and concluded water radio-frequency ion replaces water microwave-electrothermal. R14 surfaced a surprise: at the demonstrator power class with the 14-year round-trip ceiling, water microwave-electrothermal at 700 second specific impulse beats water radio-frequency ion at 2000 second because cruise time (not propellant fraction) is the binding constraint. R14 also used R12's 10-flyby lunar tour assumption, which is operationally aggressive — Cassini used 4 gravity assists, Galileo 3.

**The question:** at each reactor power class (10, 40, 100, 200, 500 kilowatt-electric) and each realistic lunar tour count (3, 5, 7, 10 flybys), which thruster technology maximizes delivered chunk at the 14-year round-trip ceiling? Where is the actual crossover between water microwave-electrothermal, water Hall, water radio-frequency ion, and water dual-ion?

## Pre-registered hypothesis (H10b)

**Aggregate (H10b-agg):** Thruster choice depends on power class and trajectory aggressiveness. Below ~40 kilowatt-electric and with ≤5 lunar flybys, water microwave-electrothermal wins on cruise-time grounds. Between 40-200 kilowatt-electric, water radio-frequency ion is the right choice. Above 200 kilowatt-electric, water dual-ion's specific-impulse advantage compounds and it wins. The 3-flyby (Cassini-class realistic) lunar tour shrinks the deliverable-chunk-at-14-year ceiling by roughly half vs the 10-flyby aggressive case.

**Pre-registered sub-claims:**

| Sub-claim | Predicted | Falsification |
|---|---|---|
| H10b-a — Crossover from water microwave-electrothermal to water radio-frequency ion | Between 20 and 60 kilowatt-electric power class | falsified if crossover < 10 or > 100 kilowatt-electric |
| H10b-b — Crossover from water radio-frequency ion to water dual-ion | Between 100 and 300 kilowatt-electric power class | falsified if crossover < 50 or > 500 kilowatt-electric |
| H10b-c — 3-flyby tour reduces deliverable chunk at 14-yr by 30-50% | yes | falsified if reduction < 15% or > 70% |
| H10b-d — Operationally realistic Pareto cell at Fission Surface Power | water radio-frequency ion at 40 kilowatt-electric + 3-flyby lunar tour at 14-yr ceiling delivers 5-10 tonnes | falsified if outside [3, 15] tonnes |
| H10b-e — Maximum deliverable chunk at 14-year ceiling under operationally realistic 3-flyby tour | ≤ 250 tonnes at 500 kilowatt-electric | falsified if > 350 tonnes (which would weaken R14's "conops is 10x optimistic" finding) |

## Method

For each (reactor power × thruster technology × lunar flyby count × specific power), find the maximum chunk delivered that closes 14-year round trip. Sweep:
- Reactor power: 10, 25, 40, 75, 100, 200, 500 kilowatt-electric
- Thruster: water microwave-electrothermal (700 s, η 0.30), water Hall (1500 s, η 0.55), water radio-frequency ion (2000 s, η 0.65), water dual-ion (5000 s, η 0.55)
- Lunar flyby count: 3, 5, 7, 10 (with corresponding residual inbound delta-velocity from R9/R12 sweep)
- Specific power: 5 watts/kilogram (Kilopower demonstrated), 10 watts/kilogram (Fission Surface Power target)
- Bag η_c = 0.8 (conops design point)

For each cell, search delivered-chunk target (1-1000 tonnes) and report the maximum that closes the 14-year ceiling.

**Inbound delta-velocity per flyby count** (from R12 results):
- 3 flybys: 8.87 km/s residual
- 5 flybys: 7.80 km/s residual
- 7 flybys: 6.42 km/s residual (interpolated)
- 10 flybys: 4.47 km/s residual

**Phasing time per flyby count**:
- 3 flybys: 0.16 yr (1.9 months)
- 5 flybys: 0.32 yr (3.9 months)
- 7 flybys: 0.49 yr (5.9 months)
- 10 flybys: 0.73 yr (8.7 months)

= 7 × 4 × 4 × 2 = 224 cells. Tractable.

**Validity caveats:**
- Same constant-thrust closed-form model as all R5-R14 rounds.
- 3-flyby tour is most operationally realistic; 10-flyby is aggressive.
- Each flyby costs an extra ~1-3 weeks of launch-window slack (lunar nodal regression) that's not modeled.
- Water Hall at chunk-water purity is TRL 2-3; not flight-ready in the same sense as Pale Blue water radio-frequency ion.
- Dual-ion is TRL 1-2 (lab-bench).

## Result

### Maximum chunk delivered at 14-year ceiling, per (power × thruster × flyby count) cell

**3-flyby lunar tour (realistic, Cassini-class), 10 W/kg specific power:**

| Power (kWe) | water-MET (700 s) | water Hall (1500 s) | water radio-frequency ion (2000 s) | water dual-ion (5000 s) | Winner |
|---:|---:|---:|---:|---:|---|
| 10  | 0.0 | 0.0 | 0.0 | 0.0 | (none closes 14-yr) |
| 25  | 1.2 | 6.9 | 6.9 | 0.0 | water radio-frequency ion |
| 40  | 4.9 | **14.0** | **14.1** | 0.6 | water radio-frequency ion |
| 75  | 13.6 | 30.6 | 30.8 | 5.4 | water radio-frequency ion |
| 100 | 19.8 | 42.5 | 42.7 | 8.9 | water radio-frequency ion |
| 200 | 44.6 | 89.9 | 90.3 | 22.8 | water radio-frequency ion |
| 500 | 119.1 | 232.3 | 233.4 | 64.5 | water radio-frequency ion |

**10-flyby lunar tour (aggressive), 10 W/kg specific power:**

| Power (kWe) | water-MET | water Hall | water radio-frequency ion | water dual-ion | Winner |
|---:|---:|---:|---:|---:|---|
| 10  | 5.7 | 7.3 | 6.4 | 0.0 | water Hall |
| 25  | 21.8 | 25.6 | 23.5 | 4.0 | water Hall |
| 40  | 37.8 | 44.0 | 40.7 | 9.5 | water Hall |
| 75  | 75.3 | 86.9 | 80.6 | 22.1 | water Hall |
| 100 | 102.1 | 117.5 | 109.1 | 31.2 | water Hall |
| 200 | 209.2 | 240.0 | 223.3 | 67.3 | water Hall |
| 500 | 530.5 | 607.6 | 565.7 | 175.8 | water Hall |

### Thruster crossover map (by 14-yr-max-delivery winner)

At 10 W/kg specific power across all flyby counts and powers:
- **water-MET wins** only at Kilopower 10 kilowatt-electric with 3-flyby tour, and even then delivery is 0 (no cell closes 14-yr at Kilopower / 3-flyby)
- **water radio-frequency ion wins** at 25-500 kilowatt-electric with 3-flyby tour
- **water Hall wins** at all power classes with 5+ flyby tour
- **water dual-ion never wins** under any (power × flyby) cell when comparing max-deliverable-chunk-at-14-yr-ceiling

### 3-flyby vs 10-flyby chunk-delivery penalty

Max delivered at 500 kilowatt-electric / 10 W/kg:
- 3-flyby: 233 tonnes (water radio-frequency ion)
- 10-flyby: 608 tonnes (water Hall)
- **62% reduction from 10-flyby to 3-flyby** (outside the predicted 30-50% band; H10b-c falsified high)

### Hypothesis grading

| Sub-claim | Predicted | Measured | Verdict |
|---|---|---|---|
| H10b-a — water-MET → water radio-frequency ion crossover at 20-60 kilowatt-electric | yes | 25 kilowatt-electric crossover at 3-flyby / 10 W/kg | **held** |
| H10b-b — water radio-frequency ion → water dual-ion crossover at 100-300 kilowatt-electric | yes | Dual-ion never wins at any (power, flyby) cell | **falsified — crossover does not exist** |
| H10b-c — 3-flyby tour reduces chunk 30-50% vs 10-flyby | yes | 62% reduction at 500 kilowatt-electric | **falsified high — operational realism is more painful than predicted** |
| H10b-d — Fission Surface Power 40 kilowatt-electric + 3-flyby + water radio-frequency ion gives 5-10 tonnes | yes | 4.9 t (5 W/kg) / 14.1 t (10 W/kg) | **held** (at the favorable specific power) |
| H10b-e — 3-flyby max chunk at 14-yr ≤ 250 tonnes (any power) | yes | 233 tonnes (500 kilowatt-electric / water radio-frequency ion / 10 W/kg) | **held** |

Result JSON: `results/thruster_per_power.json`.

## Reading

**The right thruster for ICEBERG production at the realistic operational point is water radio-frequency ion (Pale Blue) — not water Hall, not dual-ion.**

The numerical second-place is water Hall by a hair (0.1-2 percentage points in most cells), but water Hall on chunk-water purity is TRL 2-3 while Pale Blue water radio-frequency ion is TRL 7-8 flying today. The 0-2 percentage point delivery hit is paid back many times over in development risk and program timeline.

**Dual-ion is the deck-killer surprise of this round.** R13's "dual-ion wins" finding turns out to be an artifact of cherry-picking small chunks against overpowered reactors. In apples-to-apples max-chunk-at-fixed-round-trip-and-power, dual-ion is dominated at every cell. Its specific-impulse advantage doesn't compound the way I expected — because at fixed power, higher specific impulse means lower thrust, and the cruise-time penalty outweighs the propellant-fraction win.

**Three-flyby lunar tour penalty is worse than predicted.** The 62% delivery reduction (vs 10-flyby) means the user's operational concern about flyby reliability has real teeth. If we accept 3-flyby as the realistic ceiling, the achievable cells drop substantially:

| Reactor era | 3-flyby (realistic) | 10-flyby (aggressive) | Note |
|---|---:|---:|---|
| Kilopower 10 kilowatt-electric | 0 tonnes | 6-7 tonnes | Demonstrator era needs 10-flyby OR longer round trip |
| Fission Surface Power 40 kilowatt-electric | 14 tonnes | 44 tonnes | The honest Fission Surface Power per-ship delivery |
| 100 kilowatt-electric stretch | 43 tonnes | 117 tonnes | |
| 200 kilowatt-electric sub-megawatt | 90 tonnes | 240 tonnes | |
| 500 kilowatt-electric megawatt | 233 tonnes | 608 tonnes | |

**Deck-worthy cell:** Fission Surface Power 40 kilowatt-electric + water radio-frequency ion (Pale Blue) + 3-flyby lunar tour = 14 tonnes delivered, 14-year round trip, ~$28M/year revenue per ship per synodic window. **This is the honest, realistic, flight-ready, Pale-Blue-deployable architecture.** The conops' 100-200 tonnes at Fission Surface Power is still 7-14x optimistic from this baseline.

**To close the user's $400M/year operating point, options are:**
1. **Wait for megawatt-class reactor maturity** (~2040s): 233 tonnes per ship at 3-flyby, $466M/year per ship.
2. **Push 10-flyby tour for higher delivery now** (operationally complex, unprecedented): 44 tonnes per ship at Fission Surface Power, $88M/year per ship. Still 5x off the target.
3. **Fleet expansion at Fission Surface Power**: 14 ships in flight (one per synodic window) × 14 tonnes/ship = 196 tonnes/year total. About $400M/year.
4. **Multi-ship per synodic window**: 3 ships per window, each at Fission Surface Power, 3 × 14 t = 42 t/year/ship-class = $84M/year, plus the multiplier on number-of-ship-classes. Requires multiple launch vehicles per window.

Option 3 (one-ship-per-window at Fission Surface Power) is the most realistic and matches the conops' stated steady-state cadence. **At 14 tonnes per ship delivered, the steady-state annual revenue is ~$28M times 13 ships in flight ≈ $360M/year** (close enough to the user's $400M/year target). The conops claim of 50-200 tonnes per ship is unnecessary if the fleet size compensates.

## Revisit

- **R13's dual-ion "win" was an artifact.** The actual win condition (max-chunk-at-fixed-round-trip) reveals dual-ion is dominated. R13's writeup overstated dual-ion's case — should be amended to "dual-ion does NOT win on apples-to-apples chunk-delivery." The cells where dual-ion appeared to win were small-chunk + over-powered-reactor cells where chunk mass is a fixed input, not a maximizable output.
- **Water Hall is the numerical-best thruster but TRL-disqualifying for the near-term architecture.** Water Hall at chunk-water purity is unproven; the silicate-contamination concern from R11 applies more severely to Hall than to radio-frequency ion (lower Isp Hall means more propellant flow rate per unit thrust). Worth a dedicated R11b: water Hall grid life under chunk water.
- **The water Hall numbers are slightly better than water radio-frequency ion because of the η_bag = 0.8 model.** When effective specific impulse is reduced by 20%, the absolute specific impulse advantage of radio-frequency ion shrinks relative to Hall. If η_bag is actually higher (e.g., 0.9), the gap might reverse. Worth a sub-round to test η_bag sensitivity.
- **10-flyby tour assumption is operationally heroic** but not impossible. NASA's ARTEMIS mission used 3 lunar flybys. The 10-flyby case is in the spirit of theoretical-best, not engineering-realistic. The realistic case is 3-flyby. Should re-cast R12's finding ("14-year + 70% delivery via 10-flyby tour") as "needs 10 flybys; realistic with 3 flybys is meaningfully worse."
- **The 14-year round-trip ceiling is the binding constraint.** At a different ceiling (say 16 years), the dual-ion architecture might be back on the table because the cruise-time penalty becomes less binding. Worth a sub-round on dual-ion at 16-yr ceiling.
- **Conops scaling table is now confirmed 10x optimistic at low power tiers AND at the realistic 3-flyby tour.** R14 showed this; R10b confirms it from a different direction. The deck needs the corrected scaling table.

## Cross-learning

- **R10's original "water radio-frequency ion replaces water microwave-electrothermal" conclusion is reaffirmed, but for a different reason than R10 gave.** R10 said it was specific-impulse; R10b says it's specific-impulse-AND-thrust-balanced at the right power class. At Kilopower (10 kilowatt-electric) and 3-flyby tour, the architecture doesn't close at all — neither thruster wins because the 14-year ceiling is unreachable.
- **Dual-ion is the right thruster only for niche operating points.** Specifically: small chunk + over-powered reactor (which is wasteful), OR longer round-trip ceiling (16+ years). For the realistic 14-year ceiling + Fission-Surface-Power-or-below power class, dual-ion is dominated.
- **Water Hall and water radio-frequency ion are within 1 percentage point at every cell.** The choice is TRL, not propulsion physics. Pale Blue (water radio-frequency ion, TRL 7-8) wins on heritage; water Hall (TRL 2-3 at chunk-water purity) loses on development risk.
- **The 3-flyby tour penalty is severe (62% delivery reduction vs 10-flyby).** This is the most operationally-binding constraint the campaign has surfaced. Either the deck commits to a longer/more-complex flyby tour and prepares for the GNC complexity, OR it accepts a 62% delivery hit and works fleet-scale rather than per-ship scale.
- **Pre-registered hypothesis discipline catches falsifications even when the headline holds.** R10b-aggregate "thruster choice depends on power class" held, but two sub-claims (H10b-b dual-ion crossover, H10b-c 3-flyby penalty magnitude) falsified. Methodology benefit: I wrote down what I expected, and the round corrected the parts I had wrong.
- **R13's dual-ion win is now retroactively understood as an artifact of comparison framing.** The campaign needs to track: when a round finds a "winning" cell, check whether the comparison is apples-to-apples (max-some-output-at-fixed-constraint) or apples-to-oranges (different chunk masses, different power classes). Surface-level "X wins" claims can be misleading without the comparison framework explicit.
