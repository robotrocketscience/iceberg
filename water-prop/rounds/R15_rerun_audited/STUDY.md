# R15-rerun — Cashflow under audited assumptions (duty 0.7, 18-yr round trip)

**Status:** post-result.

## Question

R-mid audit found duty cycle 0.5 was inherited from R5 (Pale Blue commercial reference, wrong class) and propagated through all R-rounds. Realistic deep-space heritage is duty 0.7 (Dawn, BepiColombo). Combined with relaxed 18-yr round-trip ceiling, per-ship chunk delivery rises 1.4-3.3x at all power tiers. Does this rescue the R15 / R15b "financials don't close" finding?

## Method

Same cashflow model as R15b. Inputs changed:
- Per-ship chunk delivery: from audit recompute table (3-flyby tour, duty 0.7, 18-yr ceiling, water radio-frequency ion, 10 watts per kilogram specific power)
- Round trip: 18 years (was 14)
- All other assumptions: unchanged (commercial mid ship cost, launch + trans-Saturn-injection $290 million, conops fleet cadence, sovereign and pricing sweep axes)

Comparison vs R15 baseline scenario (duty 0.5, 14-yr ceiling).

## Result

### Per-ship chunk delivery, R15 baseline vs R15-rerun audited

| Reactor era | R15 baseline (duty 0.5, 14-yr) | R15-rerun audited (duty 0.7, 18-yr) | Ratio |
|---|---:|---:|---:|
| Kilopower 10 kilowatt-electric | 5 t | 7 t | 1.4x |
| Fission Surface Power 40 kilowatt-electric | 14 t | 42 t | 3.0x |
| Stretch 100 kilowatt-electric | 43 t | 114 t | 2.7x |
| Sub-megawatt 200 kilowatt-electric | 90 t | 294 t | 3.3x |
| Megawatt 500 kilowatt-electric | 233 t | 588 t | 2.5x |

### Steady-state annual revenue (year 40-45 average) at commercial_mid ship cost

| Price | R15 baseline | R15-rerun audited |
|---:|---:|---:|
| $2,000 per kilogram | $0.47 billion/year | **$1.18 billion/year (matches conops claim)** |
| $3,000 per kilogram | $0.70 billion/year | $1.76 billion/year |
| $4,000 per kilogram | $0.93 billion/year | $2.35 billion/year |
| $5,000 per kilogram | $1.17 billion/year | $2.94 billion/year |
| $10,000 per kilogram | $2.33 billion/year | $5.88 billion/year |

**The conops' $1 billion+/year steady-state claim is vindicated at megawatt-class era under audited assumptions.**

### Break-even comparison

| Pricing × sovereign | R15 baseline | R15-rerun audited |
|---|---|---|
| $2,000 per kilogram, no sovereign | never within 45 yr | never within 45 yr |
| $5,000 per kilogram, no sovereign | never | never |
| $10,000 per kilogram, no sovereign | never | **year 40** |
| $5,000 per kilogram + $2B sovereign at year 11 | never | never |
| $10,000 per kilogram + $2B sovereign at year 11 | never | **year 40** |

**Best-case audited cell:** commercial_mid ship cost + $10,000 per kilogram + $2 billion sovereign purchase at year 11 → break-even at year 40 with +$22 billion cumulative cashflow at year 45.

### Cells closing within investor (≤25 yr) or sovereign-infrastructure (≤35 yr) horizons

| Horizon | R15 baseline | R15-rerun audited |
|---|---:|---:|
| Investor (≤25 yr) | 0 of 90 cells | **0 of 90 cells** |
| Sovereign-infrastructure (≤35 yr) | 0 of 90 cells | **0 of 90 cells** |

**No cell closes within sovereign-infrastructure horizons (≤35 years) under any tested combination of pricing, sovereign purchase, and ship cost, even with audited assumptions.**

## Reading

The R-mid audit established that under realistic deep-space heritage assumptions (duty 0.7, 18-year round trip ceiling, 3-flyby lunar gravity assist tour), the conops' chunk-per-ship delivery claims are roughly consistent with the propulsion physics. R15-rerun extends this to the cashflow model and finds **two simultaneous truths**:

1. **The conops' $1 billion+/year steady-state revenue claim is vindicated.** At megawatt-class era (ship 11+, year 20+), audited per-ship delivery × conops fleet cadence × $2,000 per kilogram pricing = $1.18 billion per year steady-state revenue. This is the "Suez Canal at perpetuity" framing the conops uses, and it holds under audited propulsion physics.

2. **The break-even horizon is 40+ years, not 11.** Extending the round trip from 14 to 18 years (required to make audited chunk-delivery numbers achievable) means cumulative cost accumulates for 4 additional years before any revenue. The 18-year delay before ship 1 delivers, combined with $400-500 million per year fleet capex during years 1-18, creates an $8-10 billion cumulative deficit by year 18 that takes another 20+ years of steady-state revenue to fill. Break-even is achievable at premium pricing ($10,000 per kilogram) plus sovereign-purchase bridging, but year 40 is the *earliest* close.

**These are not contradictory; they are the two faces of an infrastructure investment.**

The deck framing should be:
- The mission *eventually* produces the cash flow the conops claims (vindicated by R15-rerun)
- The break-even horizon is 30-50 years (longer than any private capital structure)
- The asset class is sovereign-development-bank instrument, not venture or growth equity
- "Suez Canal not Amazon" is the right framing — Suez Canal took 40 years from concept to operational cash flow, with sovereign / treasury / international-bond financing throughout

## Revisit

- **Round-trip extension to 18 years is the load-bearing assumption.** If the conops 13.5-year headline is held instead, per-ship chunk delivery drops back to R14-corrected levels and the steady-state revenue claim collapses again. The deck should explicitly trade these — pick one of (a) 13.5-year headline at low per-ship delivery, (b) 18-year operational reality at full conops chunk numbers.
- **Megawatt-class reactor timing remains exogenous.** R15-rerun assumes megawatt reactors arrive by year 15-20. If the program slips to year 25+, steady-state revenue is delayed and break-even moves past year 50.
- **The "year 40 break-even" cell requires premium pricing ($10,000 per kilogram).** R15b found this is 2-4x conops' Tier 1 willingness-to-pay ceiling. Justifying it requires sovereign-strategic-reserve framing, not commercial-customer framing.
- **Discount rate not applied.** Real financial modeling would discount the year-30+ cash flows substantially. At 8% discount, $1 billion at year 30 is worth $99 million in year-0 dollars. NPV calculation may make even the audited scenario look worse than the un-discounted picture suggests.

## Cross-learning

- **The audit was necessary but not sufficient.** R-mid corrected the duty cycle and round-trip ceiling assumptions, which doubled-or-tripled per-ship delivery and vindicated the conops' steady-state revenue claim. But the cashflow break-even problem is structural, not just a duty-cycle bug. The 18-year delay before any revenue is fundamental to the architecture — even at heroic chunk delivery, you can't break even within 25 years on a single-ship-per-year cadence.
- **The conops' two claims are simultaneously correct and misleading.** "Steady-state $1 billion+/year revenue" is correct (R15-rerun confirms). "Cash-positive at year 11" is correct only with sovereign forward-sale-against-captured-chunk re-financing. The two together create a misleading impression that ICEBERG is a venture-fundable infrastructure. R15-rerun shows it is not.
- **Single-ship-per-synodic-window cadence is the binding constraint on break-even timing.** A 2-3 ship-per-window cadence would multiply revenue per year proportionally. Worth a dedicated round (R15c queued).
- **Methodology lesson:** even after a rigorous mid-cycle audit, finding-validation requires re-running the dependent calculations end-to-end. The "audit corrects propulsion physics" finding does not automatically propagate to "audit corrects financial conclusions" — the financial conclusion has independent structure (the 18-year revenue delay) that the audit didn't touch.
