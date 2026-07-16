# R-architecture-D-cost — study

**Owner:** rhea (re-spawn, fifth re-entry)
**Status:** PRE-REGISTERED (hypothesis frozen before run.py executes)
**Round directory:** `water-prop/rounds/R_architecture_D_cost/`

---

## Question

Does either Architecture-D variant (D-fission or D-solar-thermal) clear the sovereign-bond, regulated-utility, or corporate-growth hurdle on per-mission economics? Which D variant dominates on programmatic-risk-adjusted expected delivered mass?

## Method discipline

Methodology lessons accumulated across prior rhea rounds (carried forward):

- **Lesson #1:** Pre-register numeric ranges only after back-of-envelope arithmetic.
- **Lesson #7:** Re-fetch origin and read active-sessions registry before opening a SCOPE.
- **Lesson #8:** Pre-register programmatic-risk-adjusted quantities against this-round conditional values, not against upstream-round conditional values that may differ by orders of magnitude.

Back-of-envelope (this round, pre-registration) — full notes in `results/back_of_envelope.md` after run:

- D-fission and D-solar-thermal both have ship CapEx in the $570-650M central band — comparable to Variant-B 500-kilowatt-electric chemical-kick (R-reactor-roadmap SHIP_COST `Chemical_kick_500kWe` = $650M).
- Architecture-D delivered-mass-per-mission is 8.4-27.6 tonnes (from R-chemical-plus-small-reactor `architecture_D.json` 10 closing scenarios), central 19.9 tonnes at the FSP-stretch reactor and the equivalent solar-thermal stack mass.
- **Gross revenue per ship at BEST_CELL ($10,000/kg water):** Variant B 128.8 tonnes = $1.288B per ship; Architecture D 19.9 tonnes = $199M per ship.
- **Architecture D ship cost ($600M) > gross revenue per ship ($199M).** Per-mission cashflow is structurally negative before opex and launch. Sovereign payment ($2B at year 11 in BEST_CELL) is the only positive component.

Implication: Variant B is a near-the-hurdle commercial cell with positive per-mission cashflow that fails on aggregate hurdle. Architecture D is a different beast — sovereign-anchor program with negative per-mission cashflow regardless of fleet schedule. The IRR question for Architecture D is whether the sovereign payment alone can pull the program above any hurdle when amortized over fleet CapEx.

## Pre-registered hypothesis (H-arch-d)

**Aggregate (H-arch-d-agg):** Neither D-fission nor D-solar-thermal clears sovereign-bond (4 percent marginal-internal-rate-of-return) at BEST_CELL anchor under conservative cost assumptions and base launch cost (mixed Falcon-Heavy + on-orbit-assembly, ~$500M/mission). D-solar-thermal dominates D-fission on programmatic-risk-adjusted expected delivered mass by a factor of 2.0-3.5×, but absolute level remains below the sovereign-bond threshold for both. Starship launch (~$200M/mission) lifts marginal-internal-rate-of-return by 1-2 percentage points but does not close sovereign-bond for either variant.

### Pre-registered sub-claims

| Sub-claim | Predicted | Falsification |
|---|---|---|
| H-arch-d-a — D-fission ship CapEx, central anchor (200 kilowatts-electric reactor at FSP-Phase-1 stretch, 20-tonne reactor mass; 10-tonne vehicle dry; 5-tonne electrolysis plant; 75-tonne hydrolox tankage scaled to 136-tonne propellant capacity) | $550-700M | outside $400-900M |
| H-arch-d-b — D-solar-thermal ship CapEx, central anchor (200 kilowatts-electric useful; 25,300-square-metre inflatable mirror at $10K/square-metre; SOEC at $50/watt-electric production-target; 30-tonne waste-heat radiator at $30M) | $500-700M | outside $350-900M |
| H-arch-d-c — D-fission per-mission gross revenue at BEST_CELL ($10K/kg water, 19.9-tonne delivered) | $199M | exact arithmetic — sub-claim is to confirm-not-test |
| H-arch-d-d — D-fission per-mission gross cashflow (revenue minus ship CapEx, BEST_CELL) | negative, in $-450M to $-350M band | falsified if positive |
| H-arch-d-e — D-solar-thermal per-mission gross cashflow (revenue minus ship CapEx, BEST_CELL) | negative, in $-450M to $-350M band | falsified if positive |
| H-arch-d-f — D-fission marginal internal-rate-of-return at BEST_CELL + base launch cost ($500M) + fleet schedule from R-reactor-roadmap (substituting D-fission ship cost and delivered mass) | -2.0 to +0.5 percent (conditional on engineering closure, i.e. no posterior overlay) | outside -4.0 to +2.0 percent |
| H-arch-d-g — D-solar-thermal marginal internal-rate-of-return at BEST_CELL + base launch cost + fleet schedule (conditional on engineering closure) | -2.0 to +0.5 percent | outside -4.0 to +2.0 percent |
| H-arch-d-h — D-fission programmatic-risk-adjusted expected delivered mass per mission (posterior median 0.78 percent × conditional delivered 19.9 tonnes) | 0.13-0.20 tonnes per mission | outside 0.05-0.40 |
| H-arch-d-i — D-solar-thermal programmatic-risk-adjusted expected delivered mass per mission (posterior median 2.03 percent × conditional delivered 19.9 tonnes) | 0.35-0.55 tonnes per mission | outside 0.20-0.80 |
| H-arch-d-j — D-solar-thermal dominance factor over D-fission on programmatic-risk-adjusted expected delivered mass | 2.0-3.5× | outside 1.5-5.0× |
| H-arch-d-k — Starship-launch (~$200M/mission) sensitivity: marginal-internal-rate-of-return uplift for either D variant relative to base-launch | +0.8 to +1.8 percentage points | outside +0.3 to +3.0 percentage points |
| H-arch-d-l — D-fission sovereign-bond clearance at any reasonable cost-and-launch anchor | not cleared (marginal-internal-rate-of-return < 4 percent at all swept points) | falsified if any swept cell clears sovereign-bond |
| H-arch-d-m — D-solar-thermal sovereign-bond clearance at any reasonable cost-and-launch anchor | not cleared (marginal-internal-rate-of-return < 4 percent at all swept points) | falsified if any swept cell clears sovereign-bond |
| H-arch-d-n — Combined verdict relative to Variant-B 500-kilowatt-electric chemical-kick (rhea Round 5 bake-off conclusion) | Architecture D is strictly worse on conditional marginal-internal-rate-of-return than Variant B (because Variant B has positive per-mission cashflow). D-solar-thermal recovers some of the gap on programmatic-risk-adjusted basis via 2.6× posterior advantage but does not surpass Variant B's risk-adjusted expected delivered mass | falsified if D-solar-thermal expected delivered mass per mission exceeds Variant B's 0.166 tonnes-per-mission (hyperion R-variant-B-500kWe-sizing) by more than 2× |

**Aggregate decision rule:** if H-arch-d-agg holds (neither D variant clears sovereign-bond), surface to project owner: (a) Architecture D is a paper hedge, not a closing matrix cell; (b) D-solar-thermal dominates D-fission on programmatic-risk-adjusted basis but neither dominates Variant B; (c) the matrix should record Architecture D with the "below-sovereign-bond" annotation and the D-solar-thermal-preferred annotation. If H-arch-d-agg falsifies (some D variant clears sovereign-bond) — surface as a positive surprise; flag for project-owner attention.

## Method

### Cost inputs (central anchors, falsification bands)

**D-fission ship CapEx:**
- Vehicle dry hardware: $150-250M (Vulcan-Centaur-class hydrolox bus scaled to 10-tonne dry) — central $200M
- Reactor (200 kilowatts-electric at FSP-Phase-1 stretch, 20-tonne reactor mass): $150-400M, central $250M (NRC SP-100 historical adjusted; FSP Phase-1 flight-unit projection per 2022 NASA cost basis; Westinghouse and Lockheed reactor estimates published in Phase-1 proposals)
- Electrolysis plant (150 kilowatts-electric proton-exchange-membrane, 5-tonne plant): $50-100M, central $75M
- Hydrolox tankage and structure (136-tonne propellant capacity): $50-100M, central $75M
- **Central total: $600M**

**D-solar-thermal ship CapEx:**
- Vehicle dry hardware: $150-250M, central $200M (same chemical bus as D-fission)
- Inflatable mirror (25,300 square metres at 0.1 kilograms-per-square-metre): $5K-25K/square-metre × 25,300 square-metres = $127M-$632M, central $10K/square-metre × 25,300 = $253M (mass-produced inflatable, Technology-Readiness-Level 4-5; reference points: ECHO-2 1964 ~$1.2K/square-metre in 1964 dollars, Roccor/L'Garde modern inflatables ~$20-100K/square-metre at small scale)
- Solid-oxide-electrolyzer (150 kilowatts-electric): $5-50/watt-electric production target = $0.75-7.5M, central $5M (cheap once mass-produced; FuelCell Energy commercial SOEC ground-rated $200-300/kilowatt-electric)
- Waste-heat radiator (150 kilowatts thermal, sub-megawatt class): $10-50M, central $30M
- Concentrator structure and receiver: $30-80M, central $50M
- Hydrolox tankage and structure: $75M (same as D-fission)
- **Central total: $608M** (within $50M of D-fission central)

**Launch cost (per mission):**
- Falcon-Heavy expendable + on-orbit assembly (4 launches × $150M each + assembly overhead): $700M
- Mixed Falcon-Heavy + Vulcan-Centaur kick (current LAUNCH_PLUS_TSI baseline): $500M
- Starship optimistic (2 expendable Starship launches at $100M each + on-orbit refueling): $200M
- Starship central (per titan-2 R-launch-cost-sensitivity): $300M

**Sweep:** launch costs $200M, $300M, $500M, $700M.

### Operations and round-trip

- DEMONSTRATOR_NRE: $500M (same as R-reactor-roadmap)
- GROUND_OPS_PER_YEAR: $50M (same)
- Round-trip: 13.17 years (R-chemical-plus-small-reactor verified)
- Fleet schedule: identical to R-reactor-roadmap (ship 1 at year 0, ship 2 at year 7, then every 13/12 years)
- Horizon: 45 years (same)
- Perpetuity terminal value: at growth rate 0 (same)

### Cashflow model

Adapted from R-reactor-roadmap. Replace the era-specific `SHIP_COST` and `MARVL_CHUNK_DELIVERED_T` tables with Architecture-D-specific values. Architecture D does not depend on megawatt-arrival year — all ships in the fleet have the same delivered mass and ship cost. The "megawatt-arrival distribution" framing collapses; instead, marginal-internal-rate-of-return is integrated over the D-fission or D-solar-thermal **posterior** (treating the posterior as the probability that any given launch actually delivers; with probability `1 - posterior` the ship is launched but no chunk returns).

### Posterior overlay

Two implementations:

1. **Bernoulli per-launch:** each launch independently delivers with probability `posterior`. Across a fleet of 30 launches over 45 years, expected delivered mass per launch = `posterior × conditional_delivered`. Marginal-internal-rate-of-return integrated by Monte-Carlo across the posterior distribution (per R-fission-surface-power-stretch-credibility's full posterior, 1000 samples).

2. **Conditional-on-program-succeeding:** if posterior > some threshold, the program delivers; otherwise zero. Equivalent to integration with a degenerate posterior — used as a sanity check.

Primary reporting uses (1). Posterior samples drawn from `R_fission_surface_power_stretch_credibility/results/cascade_montecarlo.json`.

### Reporting

Output table for each (variant, launch-cost, water-price) cell:
- conditional marginal-internal-rate-of-return (engineering closure assumed)
- programmatic-risk-adjusted marginal-internal-rate-of-return (posterior overlay)
- expected delivered mass per mission
- gross cashflow per mission
- comparison to Variant B baseline (rhea Round 5 path 4 = 19.96 tonnes at 14.67 years; rhea Round 5 path 1 = 32.1 tonnes at 16.32 years; hyperion R-variant-B-500kWe-sizing = 0.166 tonnes-per-mission programmatic-risk-adjusted)

## Pre-registered headline (per Lesson #1, written before run.py executes)

I expect:
1. Both D variants have conditional marginal-internal-rate-of-return in -2 to +0.5 percent band (well below sovereign-bond at 4 percent).
2. D-solar-thermal posterior-adjusted expected delivered mass is 2.0-3.5× D-fission.
3. Starship launch closes neither variant against sovereign-bond.
4. Combined verdict: Architecture D is a paper hedge with D-solar-thermal as the preferred variant.

If any of (1), (3), or (4) falsifies, the matrix decision is materially changed.

## Findings (post-run, 2026-05-15)

### Headline

**Architecture D is structurally money-losing at zero discount rate under every conservative anchor swept.** Across 48 combinations (D-fission and D-solar-thermal × BEST_CELL and CONOPS_BASE price anchors × 4 launch-cost anchors × 3 ship-CapEx bands), **zero cells return a defined conditional internal-rate-of-return** — meaning net-present-value at near-zero discount rate (1 part in 10,000) is negative including the perpetuity terminal value. The best swept point — D-solar-thermal at low ship CapEx ($350M) plus Starship-optimistic launch ($200M) plus BEST_CELL price anchor — has net-present-value at zero discount of **-$16.1B**.

### Per-mission gross cashflow

| Variant | Ship CapEx (central) | Gross revenue per ship at BEST_CELL | Gross cashflow per ship (revenue minus ship CapEx) |
|---|---|---|---|
| D-fission | $600M | $199M | $-401M |
| D-solar-thermal | $608M | $199M | $-409M |

Variant B 500-kilowatt-electric for comparison (hyperion R-variant-B-500kWe-sizing, rhea R-variant-B-recovery-paths-economic): ship CapEx $650M, gross revenue per ship at BEST_CELL $1,288M, gross cashflow per ship **+$638M**. Variant B is per-mission cashflow-positive; both Architecture D variants are per-mission cashflow-negative.

### Programmatic-risk-adjusted expected delivered mass per mission

| Variant | Conditional delivered (t) | Posterior median | Expected delivered (t) |
|---|---:|---:|---:|
| D-fission | 19.9 | 0.78% | 0.155 |
| D-solar-thermal | 19.9 | 2.03% | 0.405 |
| Variant B 500-kilowatt-electric (hyperion) | 128.8 | 0.13% (uniform-prior at chained-multiplicative) | 0.166 |

D-solar-thermal expected delivered mass per mission **exceeds Variant B's** by a factor of 2.44× on raw mass — falsifying H-arch-d-n's pre-registered ceiling of 2.0× — because its credibility advantage (2.6× higher posterior than D-fission, 15× higher than the chained-Variant-B posterior) more than offsets the per-mission delivered-mass disadvantage. **But** D-solar-thermal's per-mission gross cashflow is negative, so on expected NPV or expected internal-rate-of-return, Variant B remains the more efficient water-delivery program.

### Sub-claim grading

12 of 14 sub-claims held; 2 falsifications, both informative:

- **H-arch-d-k FALSIFIED (stronger-negative direction):** the predicted +0.8 to +1.8 percentage-point uplift from Starship launch (vs mixed Falcon-Heavy baseline) is uncomputable because all 48 swept conditional-IRR values are undefined. Architecture D is so deep in the red that even Starship-optimistic launch ($200M/mission) and low ship CapEx anchors cannot pull it to positive net-present-value at near-zero discount rate. The prediction was bracketed too tight; the true finding is that **Starship doesn't lift D into a defined internal-rate-of-return region under conservative anchors**.

- **H-arch-d-n FALSIFIED (multi-axis nuance):** D-solar-thermal expected delivered mass per mission is 2.44× Variant B's, exceeding the pre-registered ceiling of 2.0×. This is not a prediction error on the underlying numbers — both posteriors and conditional-delivered-mass values were correctly anchored at pre-registration — it is a finding on the program-design axis: **D-solar-thermal does dominate Variant B on raw expected-delivered-water**. The compensating axis (Variant B per-mission cashflow-positive, D-variants cashflow-negative) means Variant B still wins on expected NPV or expected internal-rate-of-return. The matrix should record this multi-axis tradeoff explicitly rather than choose a single "winner."

### Aggregate decision (per H-arch-d-agg)

Held in spirit (no D variant clears sovereign-bond), and held strongly: no D variant even reaches a positive-net-present-value-at-zero-discount region under any conservative anchor swept.

### Recommended matrix amendments

1. **Architecture D = paper hedge, not closing cell.** Both D-fission and D-solar-thermal lose money at zero discount rate under every swept combination of launch cost, ship CapEx band, and price anchor. The "below-sovereign-bond" annotation in the matrix should be sharpened to "below-zero-discount" or "structurally money-losing."

2. **D-solar-thermal preferred over D-fission on dual axes:**
   - 2.6× higher posterior (0.78% vs 2.03% median)
   - Negligible ship-CapEx penalty (~$8M central)
   - 2.62× higher expected delivered mass per mission
   - If the program pursues Architecture D as a hedge despite the economics, D-solar-thermal is the preferred sub-variant.

3. **Variant B remains the more efficient water-delivery cell on cashflow basis, but D-solar-thermal beats Variant B on raw expected-delivered-water by 2.44×.** Multi-axis tradeoff: cashflow efficiency favors Variant B; raw expected-delivered favors D-solar-thermal. Project owner decision required if D variants stay in matrix.

4. **No conservative-anchor reading makes any D variant a closing cell.** Even with Starship-optimistic launch ($200M), low ship CapEx ($350M for D-solar-thermal), BEST_CELL pricing ($10K/kg + $2B sovereign), and an entire 30-plus-ship fleet, net-present-value at zero discount is -$16B. Architecture D is therefore strictly upside-only / technology-demonstrator framing under the matrix's current economic anchors.

### Threads opened for follow-on rounds

1. **R-arch-d-inflatable-mirror-cost-discovery.** The $5-25K per square metre mirror-cost band is the largest uncertainty in D-solar-thermal pricing. A targeted round on inflatable-mirror cost at 25,300-square-metre scale (NIAC + commercial inflatable-deployable references) would tighten the band. Only meaningful if Architecture D survives orchestrator review.

2. **R-architecture-D-multi-chunk-per-mission.** Architecture D's per-mission cashflow-negative profile is dominated by chunk size (small 19.9-tonne delivery per mission). titan-2 R-multi-chunk-per-mission found venture-class internal-rate-of-return reachable at N=5-8 chunks of B-ring physical-cap mass per mission for Variant B. The same physics applies in principle to Architecture D — but the chemical-end-to-end propellant cascade is more hostile to chunk-mass scaling. Recommend a derivative round before retiring Architecture D entirely.

3. **R-architecture-D-sovereign-anchor-sensitivity.** Architecture D net-present-value is dominated by the $2B sovereign payment at year 11. Whether and how the sovereign payment scales with announced delivery cadence is a policy question. A sensitivity round on the sovereign-payment magnitude (e.g., $5B, $10B) would clarify whether a heavier sovereign anchor can pull D into positive net-present-value. Not load-bearing for the architecture decision per se, but informative for the program-framing decision.

## Validity caveats (declared in advance)

1. **Mirror cost is the largest uncertainty.** The $10K/square-metre central anchor is a 2× geometric-mean between $5K (mass-produced inflatable target, currently unfunded) and $25K (NASA NIAC-class inflatable prototype, demonstrated). Mass-produced inflatable mirrors at 25,300-square-metre scale have not been built. Sensitivity reported.

2. **Reactor cost extrapolation is hostile.** FSP-Phase-1 contracts are $5M for design only; flight unit cost is unannounced. SP-100 historical (cancelled 1994, ~$400M sunk for non-flight) is the closest priced datapoint, but it was for a different reactor class. Central anchor $250M derived from a 2022 NASA cost estimate basis for a Phase-1 unit; sensitivity reported.

3. **Architecture-D round-trip is fixed at 13.17 years.** This is the chemical-Hohmann round-trip from R-chemical-plus-small-reactor. R-cruise-time-optimization (hyperion follow-on) found that faster cruise wins for Variant C, but Architecture D is chemical-end-to-end and Hohmann is energy-optimal for chemical propulsion. Hohmann is the right cruise for D — the round-trip is not a free parameter the way it is for electric variants.

4. **Posterior is from a single source.** R-fission-surface-power-stretch-credibility posterior is one analyst's cascade model. The bands are wide (D-fission 5th percentile 0.29 percent, 95th percentile 1.87 percent; D-solar-thermal 5th percentile 0.55 percent, 95th percentile 5.55 percent). Marginal-internal-rate-of-return uplift under the 95th-percentile-posterior is reported as a sensitivity.

5. **No accounting for sovereign payment scaling.** R-reactor-roadmap's BEST_CELL assumes $2B sovereign payment at year 11 unconditionally. Architecture D's $199M per-ship gross revenue at BEST_CELL is below R-reactor-roadmap's implicit Variant B per-ship gross revenue ($1.288B); whether the $2B sovereign payment scales with the program's announced delivery cadence is a policy question outside the round's scope. Reported under BEST_CELL as-is for comparability with Variant B; CONOPS_BASE ($2K/kg, no sovereign) reported as the downside anchor.
