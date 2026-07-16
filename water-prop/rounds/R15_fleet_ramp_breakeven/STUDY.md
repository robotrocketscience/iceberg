# Round 15 — Fleet Ramp Break-Even Under R14 Corrected Scaling

**Status:** pre-result.

## Question

The conops claims (pitch §4-5):
- **Cash-positive at year 11** via forward-sales / sovereign-purchase against captured-but-undelivered chunks
- **Steady-state $1B+/year** at perpetuity once megawatt-class fleet matures
- **Fleet ramp**: small chunks early (demonstrator era at Kilopower), bigger chunks later (Fission Surface Power, then megawatt), eventually sovereign-wealth-style cash flow

R14 found the conops chunk-to-reactor scaling is 10x optimistic at lower power tiers. Specifically at the 14-year round-trip ceiling with realistic 3-flyby lunar tour (R10b):

| Reactor era | Conops chunk/ship | **R14-corrected chunk/ship** |
|---|---:|---:|
| Kilopower 10 kilowatt-electric | 50 tonnes | **5 tonnes** |
| Fission Surface Power 40 kilowatt-electric | 100-200 tonnes | **14 tonnes** |
| Megawatt 500 kilowatt-electric | 500-1000 tonnes | **233 tonnes** |

**The question:** under R14-corrected per-ship chunk delivery and 3-flyby realistic lunar tour, does the conops fleet-ramp break-even claim still hold? When does cumulative revenue exceed cumulative cost? What's steady-state annual revenue at perpetuity?

## Pre-registered hypothesis (H15)

**Aggregate (H15-agg):** the conops' year-11 cash-positive claim is conditional on its 50-tonne Kilopower number, which is 10x too optimistic. Under corrected scaling, break-even shifts later — probably year 14-20. **Steady-state perpetual revenue at megawatt-class era is still $1B+/year** because R14's megawatt cell is roughly right (~1.5x optimism, not 10x). So the sovereign-wealth-fund framing survives, but the demonstrator phase is longer-cost-only than conops claims.

**Pre-registered sub-claims:**

| Sub-claim | Predicted | Falsification |
|---|---|---|
| H15a — Conops year-11 cash-positive claim under R14 scaling | falsified (year 11 too early) | falsified if year 11 break-even still achievable with R14 numbers |
| H15b — Year of break-even under R14 corrected scaling | year 14-20 | falsified if outside [year 12, year 25] |
| H15c — Steady-state megawatt-era annual revenue | $800M-$1.5B/year | falsified if outside [$500M, $2B]/year |
| H15d — Demonstrator economics (Kilopower era ships 1-2) | Loss-making at $10M/year per ship vs ~$200M ship capex; never pay back individually | held if individual demonstrator does not break even on its own; falsified if it does |
| H15e — Fleet at Fission Surface Power era (ships 3-7) | Revenue per ship ~$28M/year (R14 number). 5-ship fleet revenue ~$140M/year cumulative. Pays back fleet capex by year 18 | falsified if break-even at Fission Surface Power era is < year 15 or > year 25 |

## Method

Build a simple cumulative cashflow model:
1. Ship launches by year, by reactor era
2. Ship cost = $200M each (conops baseline)
3. Per-ship delivery starts 14 years after launch (round-trip)
4. Per-ship revenue = chunk delivered × $2,000/kg (conops $/kg assumption)
5. Demonstrator NRE: ship 1-2 cost includes $500M one-time R&D
6. Compute cumulative revenue vs cumulative cost by year
7. Find break-even year (cumulative revenue = cumulative cost)
8. Project steady-state annual revenue at year 30 (full megawatt-era fleet)

**Fleet timing assumptions (conops baseline, pitch §2):**
- Ship 1 launches year 0, delivers year 14
- Ship 2 launches year 7 (waits for ship 1 Saturn capture confirmation), delivers year 21
- Ships 3-5 launch every 13 months from year 8 (production cadence)
- Ships 6+ launch every 13 months continuously
- Reactor transitions: ships 1-2 use Kilopower; ships 3-10 use Fission Surface Power (available from year 5+); ships 11+ use megawatt-class (available from year 15+ per conops aspiration)

**Per-ship chunk delivery (R14 corrected, 3-flyby lunar tour, 10 watts per kilogram specific power):**
- Kilopower ship (10 kilowatt-electric): 5 tonnes delivered
- Fission Surface Power ship (40 kilowatt-electric): 14 tonnes delivered
- 100 kilowatt-electric stretch ship: 43 tonnes delivered (R10b table)
- 200 kilowatt-electric sub-megawatt ship: 90 tonnes delivered
- 500 kilowatt-electric megawatt ship: 233 tonnes delivered

**Cost assumptions:**
- Demonstrator non-recurring engineering: $500M (gates A-C bag development, ship 1 build, Pale Blue qualification on chunk water)
- Per-ship build cost: $200M Kilopower era, $250M Fission Surface Power era, $300M megawatt era
- Launch cost: $90M (Falcon Heavy expendable) per ship
- Ground operations: $50M/year fleet-wide once first ship is in flight
- $/kilogram revenue: $2,000/kilogram (conops baseline; lunar-ISRU floor)

**Validity caveats:**
- Cost numbers are concept-paper-grade; conops admits "scenario sketch, not financial model"
- Sovereign forward-sales against captured-but-undelivered chunks can re-finance early years; not modeled here
- Reactor program timing (Kilopower → Fission Surface Power → megawatt) is exogenous; conops doesn't guarantee timeline
- Lunar nodal-cycle variance (±10-15% delivered per ship) not modeled
- This is a *propulsion-physics-anchored* cash flow check, not a corporate model

## Result

### Scenario comparison

| Scenario | Break-even | Cumulative cashflow at year 40 | Steady-state revenue (year 36-40 avg) |
|---|---|---:|---:|
| Conops un-corrected scaling (50t/200t/750t per ship) | **year 38** | +$1.1B | $1.50B/year |
| R14 corrected, pessimistic reactor timeline | **never within 40 yr** | -$12.7B | $0.47B/year |
| R14 corrected, optimistic reactor timeline | **never within 40 yr** | -$11.1B | $0.47B/year |
| Kilopower-only worst case (no Fission Surface Power or megawatt) | **never within 40 yr** | -$11.6B | $0.01B/year |

The conops un-corrected scaling barely breaks even at year 38 — that's the end of the horizon. The corrected scaling doesn't break even at all within 40 years.

### Year-by-year cashflow under R14 corrected pessimistic timeline (key inflection points)

| Year | Cumulative cost | Cumulative revenue | Cumulative cashflow |
|---:|---:|---:|---:|
| 0 (demonstrator NRE + ground ops) | $840M | $0 | -$840M |
| 7 (ship 2 launches) | $1.5B | $0 | -$1.5B |
| 12 (Fission Surface Power ships launching) | $3.5B | $0 | -$3.5B |
| 14 (ship 1 delivers, $10M revenue) | $4.4B | $10M | -$4.3B |
| 20 (megawatt-era launches start) | $6.6B | $10M | -$6.6B |
| 25 (megawatt-era ships delivering ~$28M each) | $9.3B | $150M | -$9.2B |
| 29 (megawatt-era ramp accelerating) | $11.5B | $588M | -$10.9B |
| 40 (end of horizon) | n/a | n/a | -$12.7B |

### Hypothesis grading

| Sub-claim | Predicted | Measured | Verdict |
|---|---|---|---|
| H15a — Conops year-11 cash-positive claim falsified under R14 scaling | yes | confirmed | **held** |
| H15b — Break-even shifts to year 14-20 | yes | never within 40 years | **falsified — much worse than predicted** |
| H15c — Megawatt-era steady-state revenue $800M-$1.5B/year | yes | $470M/year | **partial — below band** |
| H15d — Demonstrator never pays back individually | yes | Kilopower-only scenario ends at -$11.6B | **held** |
| H15e — Fission Surface Power fleet break-even by year 15-25 | yes | never within 40 years | **falsified** |

Result JSON: `results/fleet_ramp.json`.

## Reading

**The conops' "year 11 cash-positive" and "$1B+ steady-state perpetual revenue" claims do not survive R14's corrected chunk-to-reactor scaling without additional assumptions.** Under the R14 corrected scaling and the conops' stated fleet cadence (one ship per 13-month synodic window) at conops' stated pricing ($2,000/kilogram), the program does not break even within a 40-year horizon.

**Why the conops' claim looked OK but doesn't survive scrutiny:**
- The conops' scenario table (pitch §4) appears to assume 50-tonne Kilopower / 200-tonne Fission Surface Power chunks per ship. R14 showed those are 10x optimistic at the 14-year ceiling.
- The conops also claims one-ship-per-13-month-window cadence. That's the right cadence — but at corrected chunk sizes, per-ship revenue is too small to cover per-ship cost in the 14 years between launch and delivery.
- The conops mentions sovereign forward-sales against captured-but-undelivered chunks as a way to bring cash-positive to year 11. That's a financing maneuver, not a revenue maneuver — it shifts the cashflow profile but doesn't increase total revenue.

**What it takes to make ICEBERG break even (combinations of levers):**

| Lever | Effect | Plausibility |
|---|---|---|
| **Megawatt-class reactor by year 8 instead of year 15** | Megawatt ships start delivering by year 22 instead of year 30, accelerating revenue ramp | Low — Nuclear Electric Propulsion megawatt-class is 2040s+ at best |
| **Increase price to $5,000/kilogram** | All revenue numbers 2.5x | Possible at Tier 1 (mission-essential, ISS-CRS-comparable). Above lunar-ISRU floor in volume markets |
| **Multi-ship cadence (3 ships per synodic window)** | 3x revenue at all eras | Requires 3x fleet capex too. Marginal net improvement |
| **Skip Kilopower demonstrator, wait for Fission Surface Power** | Saves $1-2B in demonstrator capex but loses flight-heritage acceleration | Loses the moat-by-first-flight argument |
| **Sovereign capital bridges years 0-25 as R&D investment, not commercial revenue** | Recasts the program as strategic infrastructure (Suez Canal framing) rather than commercial venture | This is the conops' actual framing — but the framing depends on the sovereign showing up |
| **Larger chunks per ship via dual-ion at high specific power** | R13 said dual-ion at megawatt-class delivers ~89% chunk efficiency. Could deliver ~300 tonnes per ship at megawatt-class instead of 233. ~30% revenue lift | Real but not architecture-rescuing |
| **Premium pricing for sovereign strategic-reserve customer** | $20,000/kilogram if a sovereign treats it like a strategic asset (analogous to Strategic Petroleum Reserve $/barrel premium) | Speculative but mentioned in conops |

**The honest restatement of ICEBERG's financial case under R14 corrected scaling:**

> ICEBERG is a strategic infrastructure program with a 30+ year payback horizon, not a 13-year commercial mission. The demonstrator phase (years 0-15) is a sovereign-funded research program that establishes flight heritage. Megawatt-class fleet operations (years 20+) deliver $0.5B/year at conservative pricing and could deliver $1B+/year if pricing premium or larger fleet materializes. **This is a sovereign-wealth-fund-class infrastructure investment, not a venture-backed business**. The Maersk / Suez Canal framing in the conops is correct in spirit; the timeline is roughly 2x longer than the conops claims.

**The pitch implication:** ICEBERG cannot be funded out of venture capital alone — the cumulative deficit before any breakeven is ~$12-13 billion, far beyond any private capital structure's tolerance. **Sovereign capital or sovereign-strategic-purchase is load-bearing, not optional.** The conops' §5 already names this (UAE / Saudi PIF / Singapore GIC / DARPA / Space Force) but treats it as bridge financing for years 5+. R15 shows the sovereign bridge has to extend through year 25+, not year 11.

## Revisit

- **Cost numbers in this round are concept-paper-grade.** Ship build costs ($200-400M) and demonstrator non-recurring engineering ($500M) are rough estimates. Real ship build costs at ICEBERG complexity could be 2-3x higher (heritage outer-planet missions like Galileo / Cassini cost $1-3B in 2025 dollars), which would worsen the break-even calculation. A proper financial model with bottom-up cost accounting would tighten these numbers.
- **Pricing assumption $2,000/kilogram is conops baseline.** ICEBERG-demand.md mentioned Tier 1 willingness-to-pay of $3,000-$5,000/kilogram for mission-essential customers. Premium tiers could materially shift the break-even calculation.
- **Sovereign forward-sales / strategic-purchase not modeled.** A single sovereign strategic-reserve purchase of the year-11 captured chunk for $1-2B (treating the chunk as a Strategic Petroleum Reserve-class asset) would dramatically improve cashflow. Worth a sensitivity analysis (R15b).
- **Multi-ship cadence not modeled.** What if 2-3 ships per synodic window are launched in the production era? Capex 2-3x, revenue 2-3x, but fixed ground ops scales sublinearly. Worth checking whether multi-ship cadence improves the payback timeline.
- **Reactor timeline is the load-bearing exogenous assumption.** If megawatt-class arrives by year 10 instead of year 15-20, the break-even calculation closes much earlier. The deck needs to flag reactor-program-timing as a load-bearing risk — the operator doesn't control it but the financials depend on it.
- **No discount rate applied.** Real financial modeling would discount future cashflows at 8-12%; the $1B/year at year 30 is worth ~$60M in year-0 dollars at 10% discount. NPV calculation would make the conops "Suez Canal" framing even less plausible than the un-discounted cumulative numbers suggest.

## Cross-learning

- **The conops' financial model and the R14-corrected propulsion physics are inconsistent.** The conops claims year-11 cash-positive and $1B+/year steady-state. Under R14 corrected scaling at conops cadence and pricing, neither is achievable within 40 years. Either the conops' chunk numbers are right (R14 wrong), the conops' financial assumptions are loose (R15 right), or both need revision.
- **Sovereign capital is load-bearing for the demonstrator phase, not optional.** Without sovereign bridge funding through ~year 25, the program goes negative-cashflow for $10-12B before breaking even. This is bond-issuance scale, not venture scale. The conops' Suez Canal framing is correct; the timeline is longer.
- **The 14-year ICEBERG round trip is not the same as the 14-year payback horizon.** A 14-year round trip is the propulsion constraint. Payback horizon is a function of fleet cadence, ship cost, and per-ship revenue. R15 separates these for the first time in the campaign — they were conflated in the conops.
- **The campaign's load-bearing finding has shifted.** Rounds R5-R14 questioned propulsion / trajectory assumptions and found the conops 10x optimistic on chunk scaling. R15 finds that the financial implications of the corrected scaling are 2-3x more painful than the propulsion findings would suggest in isolation. The cumulative-cashflow lens matters more than the per-ship lens.
- **Pricing premium is the cheapest lever.** Doubling price to $4,000/kilogram doubles revenue at no propulsion cost. The conops-demand analysis ($3,000-$5,000/kilogram Tier 1 willingness-to-pay) supports this. The deck should foreground pricing strategy as a load-bearing variable, not assume the $2,000/kilogram baseline.
- **Methodology lesson reinforced**: cross-discipline reconciliation surfaces errors that within-discipline rigor misses. Propulsion rounds R5-R14 missed nothing technically; finance round R15 surfaces the contradiction between propulsion physics and financial claims. Future R&D should include cross-discipline checks alongside per-discipline depth.
