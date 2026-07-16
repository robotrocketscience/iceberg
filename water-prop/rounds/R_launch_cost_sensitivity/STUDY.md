# R-launch-cost-sensitivity — does Starship-class launch economics change the program's economic case?

**Author:** Titan (re-spawn)
**Status:** pre-registered.
**Branch:** `iceberg-titan-2`.
**Date:** 2026-05-16.
**Protocol:** per `water-prop/PROTOCOL.md`.
**Predecessor this session:** R-conops-phase12-reuse (commit `d29a4d9`).

---

## Motivation

R-conops-phase12-reuse surfaced an un-named assumption in the R-reactor-roadmap cashflow framework: every mission pays $290 million for launch and kick stage ($150 million Falcon Heavy expendable + $140 million Vulcan-Centaur-class kick). This is the second-largest per-mission cost line after the ship itself, and unlike the ship cost it is *not* reducible by vehicle reuse. The reuse round's cross-learning identified this as a candidate downstream round under Starship-class launch economics.

The question this round asks: **at what launch + kick price point does the program's economic case change qualitatively** — that is, when does single-use single-chunk delivery at L1-007's 200-tonne per-ship cap cross the regulated-utility hurdle (8 percent) or corporate-growth hurdle (10 percent) without any architecture change?

SpaceX's publicly-claimed Starship economics range from $10 million marginal to $90 million listed price per launch. With on-orbit refuelling, Starship can serve as both LEO injector and kick stage, eliminating the separate Vulcan-Centaur-class hardware. A plausible Starship-class total launch + Saturn-kick cost is therefore in the range $40 million to $150 million, depending on which Starship economics one credits.

R-power-base-rate's 0-of-6 base rate on US space-fission programs implies pessimism on the reactor side. The same kind of base-rate pessimism applied to Starship: SpaceX claims have historically been delivered late and at higher cost than initially priced (Falcon Heavy was initially $90 million, currently $150 million for expendable). A 2× cost factor over claims would land Starship LEO at $50-100 million and full-stack Saturn-kick at $100-150 million. This round sweeps the range openly and lets the project owner pick the credible point.

## The assumptions being questioned

This round tests two distinct claims simultaneously:

1. **Titan's R-conops-phase12-reuse claim** that the per-mission fixed-cost floor (launch + ground-ops) dominates and makes reuse non-load-bearing. If launch cost can drop to Starship-class, ship cost dominates again and reuse leverage should grow.

2. **The implicit project assumption** that Falcon Heavy + Vulcan-Centaur-class kick is the only credible launch profile. If Starship is credible by program-start (2032-ish), the entire R-delivery-irr-curve sovereign-bond / regulated-utility / corporate-growth crossover analysis shifts.

## Pre-registered hypotheses (H-lcs)

**Aggregate (H-lcs-agg):** Under Starship-class launch + kick economics ($50 million combined, midpoint of the publicly-claimed range), the single-use baseline at L1-007's 200-tonne per-ship cap crosses the regulated-utility hurdle (8 percent) and approaches but does not cross the corporate-growth hurdle (10 percent). Vehicle reuse uplift in absolute pp-of-internal-rate-of-return terms is similar to the high-launch-cost case (about 0.3 to 1.1 pp), but in relative terms the leverage ratio between reuse and delivery uplift narrows from 13:1 to roughly 8:1. **Launch-cost reduction is therefore a larger near-term economic lever than vehicle reuse, but smaller than per-ship delivery uplift.**

| Sub-claim | Description | Predicted | Falsification |
|---|---|---|---|
| H-lcs-a | Single-use baseline IRR at delivery = 200 tonnes per ship under $50 million launch + kick | 10–13% | outside [8.5%, 14.5%] |
| H-lcs-b | Single-use baseline IRR at delivery = 200 tonnes per ship under $150 million launch + kick (Starship-stretch) | 7.5–9.5% | outside [6%, 11%] |
| H-lcs-c | 2x basic-refurb reuse uplift at delivery = 200 tonnes per ship under $50 million launch | 1.0–1.5 pp | outside [0.5, 2.0] pp |
| H-lcs-d | At delivery = 200 tonnes per ship, the launch+kick cost at which single-use IRR crosses 10% (corporate-growth) | $30 million to $80 million | outside [$0, $150 million] |
| H-lcs-e | Launch-cost-driven IRR uplift from current $290 million baseline to $50 million Starship-class at delivery = 200 tonnes per ship | 4.5–6.0 pp | outside [3.0, 7.5] pp |
| H-lcs-f | At delivery = 482 tonnes per ship (B-ring physical cap), single-use IRR under $50 million launch crosses 15% (venture-class threshold) | held | falsified if max IRR < 14% or > 18% |
| H-lcs-g | At zero launch + kick + ground-ops (theoretical maximum), single-use IRR at delivery = 200 tonnes per ship is < 20% (i.e., even free launches do not put 200-tonne missions in venture-class) | held | falsified if IRR ≥ 20% |

**Aggregate grading rule:**

- If H-lcs-a + H-lcs-c hold, the recommendation is: pursue Starship-class launch contracts as a primary near-term economic lever. Reuse stays secondary.
- If H-lcs-d shows the threshold inside Starship's publicly-claimed range ($40–150 million), then **Starship-availability becomes a binary go/no-go for crossing the corporate-growth hurdle on single-chunk delivery**. This would be the single largest economic-case finding in the campaign — comparable in leverage to the chunk-as-heat-shield rescue path.
- If H-lcs-g holds, even free launches cannot put 200-tonne single-chunk missions in venture-class. **The corporate-growth hurdle then remains structurally tied to per-ship delivery uplift (R-chunk-as-heat-shield-revisit), not to launch-cost reduction.**

## Method

### Cashflow model

Reuse R-conops-phase12-reuse's reuse-aware cashflow framework (which already extends R-reactor-roadmap's). The single modification: parameterise LAUNCH_PLUS_TSI as a sweep axis.

LAUNCH_PLUS_TSI ∈ {$290 million (current), $200 million, $150 million (Starship-stretch), $100 million, $60 million, $50 million (Starship-midpoint), $30 million, $0 million (theoretical max)}.

For each launch-cost point, run all five reuse scenarios (single-use, 2x basic, 2x reactor-swap, 3x, 4x) at all three delivery points (128.8, 200, 482 tonnes per ship). This gives 8 × 5 × 3 = 120 cashflow runs.

### Crossover identification

For each (reuse scenario, delivery) pair, bisect on launch + kick cost to find:

- Sovereign-bond crossover: launch cost at which IRR = 4 percent
- Regulated-utility crossover: launch cost at which IRR = 8 percent
- Corporate-growth crossover: launch cost at which IRR = 10 percent
- Venture-class crossover: launch cost at which IRR = 15 percent

### Sensitivity floor

Run a single "theoretical maximum" case at launch+kick = $0, ground-ops = $0, demonstrator-NRE = $0. This isolates the structural ceiling on per-mission revenue net of ship cost only.

### Validity caveats

1. Ground-ops at $50 million per year is held constant across launch-cost scenarios. Realistically, ground-ops may scale with the operational complexity of the launch + kick stack (Falcon-class needs Vulcan-class integration); a Starship-only stack might have lower mission-operations cost. This is unmodelled — possibly understates Starship benefit by 5-10 percent of ground-ops baseline.

2. Ship cost is held constant at $650 million across launch-cost scenarios. A Starship-class launch with larger payload capacity (100+ tonnes to LEO) could enable larger ship architectures or single-stage ICEBERG vehicles. The full benefit of Starship is therefore likely understated by this round, which treats Starship purely as a cheaper Falcon Heavy.

3. The $290 million launch+kick baseline matches R-reactor-roadmap. The $0 floor is a theoretical bound, not a credible operational scenario. Intermediate points are interpolations of publicly-claimed numbers and should be read as ranges, not point estimates.

4. Year-of-program for launch cost is not modelled. If Starship is operationally credible by 2030 (program year 5) but ICEBERG launches start at year 0 (2026 demonstrator NRE + year 7 first mission), the early-fleet launches may pay Falcon-class prices and only later launches benefit from Starship. The model below assumes constant launch cost across the fleet — i.e., Starship is available from program start. This is the upside-bound case.

### Revisit clause

Per-claim grading vs H-lcs-a..g. Cross-learning identifies whether launch-cost reduction promotes to a load-bearing program-decision lever or remains a "nice to have."

## Result

**Single-use internal-rate-of-return across launch+kick cost:**

| Launch+TSI ($M) | IRR at 128.8 t/ship | IRR at 200 t/ship | IRR at 482 t/ship |
|---:|---:|---:|---:|
| 0 (free) | 4.77% | 7.95% | 14.14% |
| 30 | 4.45% | 7.64% | 13.87% |
| 50 (Starship-midpoint) | 4.24% | 7.45% | 13.69% |
| 60 | 4.14% | 7.35% | 13.60% |
| 100 | 3.75% | 6.97% | 13.25% |
| 150 (Starship-stretch) | 3.28% | 6.52% | 12.84% |
| 200 | 2.84% | 6.09% | 12.44% |
| 290 (current baseline) | 2.10% | 5.38% | 11.77% |

**Hurdle crossover (launch+kick cost at which single-use IRR crosses target):**

| Delivery (t/ship) | 4% sovereign-bond | 8% regulated-utility | 10% corporate-growth | 15% venture-class |
|---:|---:|---:|---:|---:|
| 128.8 | $74M | unreachable | unreachable | unreachable |
| 200.0 | $488M (saturates) | unreachable even at free launch | unreachable even at free launch | unreachable |
| 482.0 | clears at all tested costs | clears at all tested costs | clears at all tested costs | unreachable even at free launch |

**Theoretical maximum** (zero launch + zero ground-ops + zero demonstrator NRE — all fixed costs eliminated):

| Delivery (t/ship) | Max possible IRR |
|---:|---:|
| 128.8 | 6.12% |
| 200.0 | 9.78% |
| 482.0 | 16.92% |

**Reuse uplift at delivery = 200 t/ship across launch costs** (2x basic refurb reuse, the most favourable reuse scenario):

| Launch+TSI ($M) | Single-use IRR | 2x basic reuse IRR | Uplift |
|---:|---:|---:|---:|
| 0 | 7.95% | 8.99% | +1.04 pp |
| 50 | 7.45% | 8.48% | +1.03 pp |
| 290 | 5.38% | 6.33% | +0.95 pp |

Reuse uplift is approximately constant in absolute terms across all launch costs.

**Combined-leverage scan at 482 t/ship (the regulated-utility-class regime):**

| Launch+TSI | Single-use | 2x basic reuse | 2x reactor-swap reuse |
|---:|---:|---:|---:|
| $0M | 14.14% | 14.65% | 14.31% |
| $50M | 13.69% | 14.19% | 13.86% |
| $290M | 11.77% | 12.28% | 11.94% |

Even with all three levers fully pulled (B-ring physical cap delivery + free launches + best-case reuse), the venture-class 15% hurdle is **not** cleared.

**Pre-registration grading:**

| Sub-claim | Predicted | Observed | Verdict |
|---|---|---|---|
| H-lcs-a (single-use IRR at 200 t / $50M launch ∈ [10, 13]%) | [10, 13] | 7.45% | **wrong-and-load-bearing** |
| H-lcs-b (single-use IRR at 200 t / $150M launch ∈ [7.5, 9.5]%) | [7.5, 9.5] | 6.52% | wrong-but-informative |
| H-lcs-c (2x basic reuse uplift at 200 t / $50M ∈ [1.0, 1.5] pp) | [1.0, 1.5] | +1.03 pp | held |
| H-lcs-d (launch cost at 10% crossover at 200 t ∈ [$30, $80M]) | [30, 80] | unreachable even at $0 | **wrong-and-load-bearing** |
| H-lcs-e (launch-cost uplift $290M → $50M at 200 t ∈ [4.5, 6.0] pp) | [4.5, 6.0] | +2.07 pp | **wrong-and-load-bearing** |
| H-lcs-f (single-use at 482 t / $50M launch ∈ [14, 18]%, crosses venture-class) | [14, 18] | 13.69% | wrong-but-informative |
| H-lcs-g (theoretical max at 200 t < 20%) | held | 9.78% | held |

## Reading

**The headline:** Starship-class launch economics provide a real but modest economic lever — about 2 percentage points of internal-rate-of-return uplift at L1-007's 200-tonne per-ship cap, taking single-use IRR from 5.38 percent to 7.45 percent. **The 10 percent corporate-growth hurdle at 200 tonnes per ship is structurally unreachable regardless of launch cost** — even with free launches AND zero ground-operations AND zero demonstrator NRE, theoretical maximum IRR at 200 tonnes per ship is only 9.78 percent. **The 15 percent venture-class hurdle is structurally unreachable even at the B-ring physical single-chunk cap (482 tonnes per ship) with all three levers pulled** (cheap launch + reuse + max delivery) — maximum achievable IRR is 14.65 percent.

**Five of seven sub-hypotheses falsified again,** this time in two directions. My H-lcs-a / H-lcs-e predictions were too optimistic on Starship-driven uplift (predicted 4.5-6.0 pp; observed 2.07 pp). My H-lcs-d prediction assumed a finite launch-cost threshold for corporate-growth crossover; observed that no finite threshold exists. The methodology lesson recurs — **compute the product of central estimates before ranging around it.** A 25% reduction in per-mission costs (launch $290M → $0M against a $1B per-mission gross expense) cannot lift IRR by 5 pp because the revenue side and time-discounting are unchanged. A back-of-envelope `2 × cost_reduction / revenue` would have given the right order-of-magnitude.

**Why launch-cost reduction is less powerful than predicted:**

1. **Revenue is fixed by physics, not by launch cost.** Per-mission revenue at 200 t/ship is $2 billion (200,000 kg × $10,000/kg). No launch-cost reduction touches this number.

2. **Time discounting bites the same way regardless of launch cost.** The 14.5-year round trip means revenue lands at year 14.5+ for each mission. Launch-cost savings land at year 7+. The savings are slightly less discounted than the revenue, so reducing launch costs helps a bit more than proportionally — but not by enough to dominate.

3. **Ground operations and demonstrator NRE are the floor.** Of a ~$1 billion per-mission gross expense at current ($290M) launch costs, $290M is launch, ~$50M is ground-ops allocation, $13M is demonstrator-NRE allocation. Reducing launch to zero saves $290M; ground-ops + NRE still cost $63M per mission. Per-mission cost-floor at zero launch is still $713M (ship + ground-ops share) — a 29 percent reduction at best.

4. **The 14.5-year round trip is the dominant time-domain feature.** A reduction in early-year costs is partially offset by terminal-value discounting because the revenue-bearing tail is so far out. Internal-rate-of-return bisection is dominated by the long delivery-tail timing, not by short-run cost reduction.

**The corporate-growth structural barrier at 200 tonnes per ship:**

R-delivery-irr-curve previously found the 10 percent corporate-growth hurdle requires ~691 tonnes per ship at current launch costs. This round extends that finding: **even with free launches, the 10 percent hurdle is unreachable at 200 tonnes per ship.** The 200-tonne L1-007 cap is fundamentally below the corporate-growth threshold under any plausible cost-side optimisation. R-chunk-as-heat-shield-revisit (relaxation of L1-007 toward the 482-tonne physical cap) is the only path to corporate-growth class.

**The combined-leverage envelope:**

At 482 tonnes per ship (B-ring physical cap, requires R-chunk-as-heat-shield closure), the program is comfortably in regulated-utility class (>8% IRR) at current launch costs, and approaches but does not cross venture-class (15%) at any plausible launch + reuse combination. The maximum achievable IRR under the combined scenario (free launch + 2x basic reuse + 482 t/ship) is 14.65 percent — within striking distance of 15 percent but not over.

**What this implies for the program's economic positioning:**

ICEBERG is structurally a **regulated-utility-class** investment under realistic launch + reuse economics, provided per-ship delivery reaches the B-ring physical cap. It is **not** a venture-class investment under any combination of cost-side optimisations the campaign has explored. **The 1.45 percent marginal-IRR result from R-reactor-roadmap is conservative against the 200-tonne L1-007 cap; under Starship-class launch and the 482-tonne delivery uplift, marginal-IRR moves to the 10-14 percent band — but the venture-class door stays closed.**

This is a clarifying finding for sovereign or strategic capital pitches. The corporate-venture-fund pitch (ICEBERG as a 20%+ IRR opportunity) was not credible under existing-cap delivery; this round confirms it remains not credible even under cheap-launch counterfactuals. **The right capital partner profile is sovereign + strategic-corporate (regulated-utility-class), not venture.**

## Revisit

This round's pre-registration was wrong in a structurally informative way. I assumed launch-cost was a near-doubling lever for IRR; observed it is a roughly-20-percent lever. The structural ceiling on single-chunk-mission internal-rate-of-return is set primarily by per-mission revenue and round-trip time, not by cost-side variables. **No combination of cost-side optimisations (launch reduction + reuse + ground-ops reduction + zero NRE) can lift 200 tonnes per ship into corporate-growth class.** The chunk-mass cap is the binding constraint.

This is now the sixth consecutive instance of the compute-central-estimate-product-first methodology lesson (after R-outbound-dv-continuous-thrust H-od-d, R-megawatt-marvl-radiator H-mr-d, R-reactor-roadmap H-rxr2-b..f, R-delivery-irr-curve H-dic-d, R-conops-phase12-reuse H-ph12-a..e, and now R-launch-cost-sensitivity H-lcs-a, H-lcs-d, H-lcs-e). Recurring enough that it should be added to PROTOCOL.md if not already; checked, it is — lesson #9 already there. Working as intended; the discipline is producing the corrections it is supposed to produce.

## Cross-learning

Three downstream implications:

1. **Capital-partner profiling is now anchorable.** The ICEBERG-pitch document still positions the program as a Suez-Canal-class moat (a regulated-utility framing) and lists sovereign-bond-floor crossover thresholds. The pitch reader-note from late evening flagged the era-table revenue numbers as needing rewrite; this round's compound-leverage envelope (max realistic IRR 14.65% at all-three-levers + 482 t/ship) is the right number to anchor that rewrite. The pitch language about "venture-class returns" should be retired in favour of "regulated-utility-class with structural moat."

2. **Starship-launch is upside, not architecture-critical.** Worth pursuing as a procurement-side optimisation in years 3-5, but not worth design-locking the early demonstrators against. Falcon Heavy + Vulcan kick is the conservative-procurement architecture and only costs 2 percentage points of IRR — well within program-margin tolerance.

3. **R-chunk-as-heat-shield-revisit is now triply confirmed as the dominant economic lever** (after R-delivery-irr-curve and R-conops-phase12-reuse). The leverage hierarchy is:
   - Delivery uplift 200 t → 482 t: ~6 percentage points
   - Launch cost reduction $290M → $0M: ~2 percentage points
   - Vehicle reuse 1× → 2×: ~1 percentage point
   - Combined effect (all three): ~9.3 percentage points net
   - Maximum achievable single-chunk IRR (all levers + B-ring physical cap): 14.65 percent
   - Venture-class threshold (15%): structurally unreachable without multi-chunk-per-mission

The follow-on round candidate is **R-multi-chunk-per-mission feasibility**: if a single mission can capture multiple chunks summing to >700 tonnes (the corporate-growth crossover from R-delivery-irr-curve), the venture-class door reopens. Without multi-chunk feasibility, the program is structurally regulated-utility-class. This is the natural next round after R-chunk-as-heat-shield-revisit closes.

The conops augmentation A-ph12-reuse and the newly-completed Starship-launch sensitivity both promote to **closed** with bounded uplift in R-conops-skeleton's queue. The remaining open queue items are A-ph4-orbit (moderate), A-c1-contingency (moderate), and the newly-surfaced R-multi-chunk-per-mission (high-leverage, prerequisite is R-chunk-as-heat-shield-revisit closure).
