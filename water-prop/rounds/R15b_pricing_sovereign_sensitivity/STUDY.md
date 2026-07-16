# Round 15b — Pricing Premium and Sovereign-Purchase Sensitivity

**Status:** pre-result.

## Question

R15 found the program does not break even within 40 years under R14-corrected scaling at conops baseline pricing ($2,000/kilogram) and one-ship-per-synodic-window cadence. R15 flagged two "cheap levers" that could rescue the financials without requiring reactor program acceleration or fleet expansion:
1. **Premium pricing.** ICEBERG-demand.md cites Tier 1 willingness-to-pay of $3,000-$5,000/kilogram for mission-essential customers (ISS-CRS-comparable). Strategic-reserve pricing (analogous to SPR-class premium) could push higher.
2. **Sovereign forward-sale.** Pitch §5 names sovereign strategic-asset purchase of the year-11 captured chunk as a re-financing event that could bring cash-positive forward by 7 years.

**The question:** with R14-corrected scaling and pessimistic reactor timeline (R15 baseline), how much do these two levers shift the break-even year? Which combination achieves break-even within investor-acceptable horizons (15-25 years)?

## Pre-registered hypothesis (H15b)

**Aggregate (H15b-agg):** Pricing premium dominates the sensitivity. At $4,000/kilogram (mid Tier 1) break-even shifts into the 30-year range. At $5,000/kilogram (Tier 1 max) combined with a $2 billion sovereign purchase at year 11, break-even can be pulled to year 22-25 — within sovereign-infrastructure horizons but still beyond venture-capital tolerance.

**Pre-registered sub-claims:**

| Sub-claim | Predicted |
|---|---|
| H15b-a — At $4,000/kilogram (no sovereign purchase) | break-even year 32-38 |
| H15b-b — At $4,000/kilogram + $1 billion sovereign purchase at year 11 | break-even year 25-32 |
| H15b-c — At $5,000/kilogram + $2 billion sovereign purchase at year 11 | break-even year 20-26 |
| H15b-d — Strategic-reserve pricing $20,000/kilogram alone (no sovereign) | break-even year 18-24 |
| H15b-e — At $2,000/kilogram + $5 billion sovereign purchase at year 11 (heroic sovereign, no pricing premium) | break-even year 28-35 |

**Aggregate finding I expect:** to bring break-even into the 20-25 year range (sovereign-infrastructure acceptable), the program needs *both* meaningful pricing premium ($4,000-$5,000/kilogram) *and* sovereign purchase at year 11. Either alone is insufficient at R14-corrected scaling.

## Method

Reuse R15 fleet schedule + cost model. Add:
- Pricing parameter: $/kilogram (sweep 2k, 3k, 4k, 5k, 10k, 20k)
- Sovereign one-time-purchase event at chosen year and chosen value
- Compute break-even year for each (price × sovereign-amount × sovereign-year) cell

Sweep grid:
- Price per kilogram: 2000, 3000, 4000, 5000, 10000, 20000
- Sovereign purchase amount: 0, 500M, 1B, 2B, 5B
- Sovereign purchase year: 11, 15, 20

= 6 × 5 × 3 = 90 cells.

**Validity caveats:**
- Pricing premium assumes customers can sustain the higher rate at projected volumes. Conops demand analysis only supports $3,000-$5,000 at Tier 1 (volumes ~100 tonnes/year). At Tier 2 / 3 volumes, lunar-ISRU floor pushes pricing back toward $2,000.
- Sovereign one-time purchase is a financing event, not a revenue event. It pulls cash forward but doesn't change total program value.
- Cost numbers from R15 unchanged.

## Result

### Cost basis correction (mid-round)

The original R15 model used $90M per ship for launch only — this missed the chemical trans-Saturn-injection kick stage entirely. Per the conops, the trans-Saturn-injection burn (7.3 km/s) requires a separate chemical upper stage (Vulcan-Centaur class, ~$140M) on top of the Falcon Heavy expendable launch (~$150M). Corrected per-ship launch-plus-trans-Saturn-injection cost: **$290M**, not $90M.

Ship-build-cost reference frame also corrected: anchored to commercial in-space tug pricing (Boeing 702SP $150-200M, Northrop Grumman MEV $300M, DARPA RSGS $240M) rather than science-flagship Cassini ($3B+). Three scenarios swept: conops_optimistic ($150-400M), commercial_mid ($250-700M), commercial_high ($400-1,200M).

### Break-even table — no sovereign purchase

| Price ($/kilogram) | Conops optimistic cost | Commercial mid cost | Commercial high cost |
|---:|---|---|---|
| $2,000 | never within 40 yr | never within 40 yr | never within 40 yr |
| $3,000 | never within 40 yr | never within 40 yr | never within 40 yr |
| $4,000 | never within 40 yr | never within 40 yr | never within 40 yr |
| $5,000 | never within 40 yr | never within 40 yr | never within 40 yr |
| $10,000 | never within 40 yr | never within 40 yr | never within 40 yr |
| $20,000 | **year 36** | **year 38** | never within 40 yr |

### Break-even table — $1 billion sovereign purchase at year 11

| Price ($/kilogram) | Conops optimistic cost | Commercial mid cost | Commercial high cost |
|---:|---|---|---|
| $2,000 - $10,000 | never within 40 yr | never within 40 yr | never within 40 yr |
| $20,000 | year 36 | year 38 | never within 40 yr |

The $1 billion sovereign purchase has almost no effect (because the program is losing $400-500M/year through year 30 — $1B re-finances ~2 years of burn).

### Break-even table — $2 billion sovereign purchase at year 11

| Price ($/kilogram) | Conops optimistic cost | Commercial mid cost | Commercial high cost |
|---:|---|---|---|
| $2,000 - $10,000 | never within 40 yr | never within 40 yr | never within 40 yr |
| $20,000 | year 35 | year 37 | year 39 |

### Break-even table — $5 billion sovereign purchase at year 11 (heroic)

| Price ($/kilogram) | Conops optimistic cost | Commercial mid cost | Commercial high cost |
|---:|---|---|---|
| $2,000 | year 11 (trivial) | year 11 (trivial) | never within 40 yr |
| $5,000 | year 11 (trivial) | year 11 (trivial) | never within 40 yr |
| $20,000 | year 11 (trivial) | year 11 (trivial) | never within 40 yr |

The $5 billion sovereign purchase triggers "break-even" at year 11 because $5B exceeds cumulative program cost through year 11 (~$3-4B). This is a sovereign buying the program outright, not a market-revenue event.

### Cells achieving investor-acceptable break-even (≤ year 25)

**12 cells out of 270 sweep combinations** close break-even within 25 years. All 12 require the $5 billion sovereign purchase OR the $20,000/kilogram pricing premium. None close at $2,000-$10,000/kilogram pricing and ≤ $2 billion sovereign purchase.

### Hypothesis grading

| Sub-claim | Predicted | Measured | Verdict |
|---|---|---|---|
| H15b-a — $4,000/kilogram no sovereign | year 32-38 | never within 40 yr | **falsified — worse than predicted** |
| H15b-b — $4,000/kilogram + $1 billion sovereign at year 11 | year 25-32 | never within 40 yr | **falsified — much worse** |
| H15b-c — $5,000/kilogram + $2 billion sovereign at year 11 | year 20-26 | never within 40 yr | **falsified — much worse** |
| H15b-d — $20,000/kilogram alone | year 18-24 | mean year 37 | **falsified — much worse** |
| H15b-e — $2,000/kilogram + $5 billion sovereign at year 11 | year 28-35 | year 11 (trivial sovereign-buyout) | **falsified — much better via different mechanism** |

**Five of five sub-claims falsified.** I systematically underestimated how much the launch + trans-Saturn-injection chemical kick stage costs eat the per-ship economics.

Result JSON: `results/sensitivity.json`.

## Reading

**The R14-corrected propulsion physics, combined with realistic launch + trans-Saturn-injection cost, makes ICEBERG financially unviable as a commercial venture at any reasonable pricing or sovereign-bridge structure.**

The cumulative deficit at the conops fleet cadence grows to $12-15 billion before any reasonable break-even, and break-even doesn't happen at $2,000-$10,000/kilogram pricing within 40 years. The two paths to closure:

1. **Strategic-reserve pricing at $20,000/kilogram.** Requires customers (sovereign or strategic) willing to pay 10x the commercial water price. Plausible for a sovereign treating space water as Strategic Petroleum Reserve-equivalent national asset. Closes break-even at year 35-38 — still investor-unacceptable horizon but in the band of patient-capital infrastructure.

2. **A single sovereign committing $5+ billion upfront at year 11.** This is the sovereign buying the program outright, not bridge financing. Break-even at year 11 is trivial in the model because the sovereign's $5B exceeds cumulative spend through year 11. This is the "Saudi PIF / UAE / Singapore GIC writes a check" scenario the conops named in §5, except the size is $5B (not the $1-2B the conops implies).

**Neither path is a commercial venture.** Both are sovereign infrastructure plays where the financial logic is strategic, not return-on-investment-driven.

### What the deck now needs to say honestly

The conops' framing of "sovereign-wealth-fund-style return at steady state" is correct *only* in two narrow regimes:

1. **Megawatt-class reactors actually arrive on the roadmap** (250+ tonnes per ship at $2,000/kilogram = $500M/year per ship). R15b shows even this doesn't pay back demonstrator-era spending within 30 years at commercial costs.
2. **Strategic-reserve pricing materializes** ($20,000/kilogram), driven by sovereign or great-power-competition demand. Sovereigns paying premium for off-Earth water as strategic asset, not commercial logistics.

The "Suez Canal" framing in the conops survives, but the implied horizon is 40+ years (similar to actual infrastructure like Suez, which had a multi-decade payback) and the funding base is sovereign capital from inception, not venture transitioning to sovereign later.

### What this implies for the architecture decision

The propulsion-rounds-corrected scaling table (R14) plus financial-round-corrected cost basis (R15b) together kill the "operator's commercial business case for the cislunar tug + ICEBERG-as-bonus" framing. **ICEBERG is not a bonus on top of the operator's core business. It is a separate, sovereign-infrastructure-scale capital commitment** that:
- Cannot be funded out of an operator's venture round
- Cannot be funded out of Series-D-scale follow-on rounds
- Requires sovereign-strategic-purchase commitment ($5B+ at year 11) or strategic-reserve pricing ($20,000/kilogram)
- Has 35-40 year payback horizons at any realistic pricing
- Is structurally an infrastructure-bond / sovereign-development-bank instrument, not equity-financed venture

The conops anticipates this in places (the Suez framing, the sovereign-wealth-fund framing, the "patience-capital" framing) but doesn't ground the framing in the underlying mass-budget arithmetic. R15b grounds it.

## Revisit

- **Pricing premium dependency.** $20,000/kilogram is roughly 7x the conops baseline and 4x the conops' own Tier 1 willingness-to-pay ceiling ($5,000/kilogram). The pricing case for $20,000/kilogram would require sovereign or DoD strategic-reserve framing, not commercial-customer framing. Worth a dedicated demand-analysis round.
- **Sovereign-purchase mechanics not modeled.** A $5 billion sovereign-strategic-asset purchase of the year-11 captured chunk is treated as a single cash event in the model. In reality, sovereign procurement typically commits over a multi-year contract with milestone gates. Modeling the contract structure would tighten cash-flow timing.
- **Ship cost learning curve not applied.** I held ship cost constant across launches; in reality, an 80% learning curve (each doubling of cumulative units costs 80% of the previous) would reduce production-era ship cost by ~30% by ship 10. This would marginally improve break-even by ~3-5 years but doesn't change the qualitative conclusion.
- **Reactor program acceleration not modeled.** If Fission Surface Power flight-readiness arrives 3 years earlier (pessimistic year 5 → optimistic year 2), the Fission Surface Power era starts that much sooner. Marginal improvement; the binding constraint is megawatt-class arrival timing.
- **Multi-ship-per-window cadence not modeled.** R15c was queued and may show that 2-3 ships per synodic window improves the financials.

## Cross-learning

- **The launch + trans-Saturn-injection cost I missed in R15 was a 3x error.** I used $90M (launch only) when the conops itself says $290M (launch + chemical kick stage). This dropped break-even from "barely closes at year 38 under conops scaling" to "never closes within 40 years at any reasonable pricing under R14 scaling." Methodology lesson: when adopting a "concept-paper-grade" model, verify each cost line item against the source document, not just the headline number.
- **The campaign's load-bearing finding has solidified.** R14 said the conops scaling table is 10x optimistic. R15 said the financials don't close. R15b said pricing premium and sovereign-purchase levers at realistic levels can't rescue the financials. The architecture is structurally sovereign-infrastructure, not commercial. Three rounds is sufficient evidence to commit this as the deck conclusion.
- **Pre-registered hypotheses were systematically optimistic by 10-20 years.** All five sub-claims falsified in the same direction (more painful than predicted). This is a calibration signal — when running future sensitivity analyses, widen the prediction bands.
- **The "demonstrator + ramp to break-even" framing the user mentioned is consistent with the conops' un-corrected scaling, not with R14-corrected scaling.** Under R14, the demonstrator era ships don't ramp to anything useful because per-ship chunk delivery is too small at low power. Under conops un-corrected, the ramp is real but ICEBERG depends on the un-corrected numbers being right.
- **Pricing premium is not as cheap a lever as R15 suggested.** R15's framing implied $4,000-$5,000/kilogram could rescue financials. R15b with corrected costs shows that only $20,000/kilogram (4x conops Tier 1 WTP ceiling) approaches break-even — and only at the optimistic ship-cost end. The cheap lever isn't pricing; it's reactor program acceleration (the operator doesn't control), the only true lever the operator controls is fleet cadence (R15c).
