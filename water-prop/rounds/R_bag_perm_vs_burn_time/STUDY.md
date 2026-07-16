# R-bag-permeability-vs-burn-time — does relaxing the 7-yr burn cap let Kilopower all-electric beat Variant B?

**Status:** pre-result.

## Question

R-chunk-fed-chemical's 7-year inbound-burn cap was the binding constraint at Kilopower. All-electric at Kilopower (10 kilowatt-electric) for chunks ≥ 50 t could in principle deliver more chunk mass than Variant B, but its burn time exceeded 7 years and so it was disqualified by the schedule-feasibility test. The "(slow)" notation in the three-way comparison showed all-electric delivering ~70 tonnes at 100 t chunk vs Variant B's 33 tonnes — but at a longer burn time.

The 7-year cap is not from the rocket equation. It comes from prior conops: 14 year round-trip target, minus 6.09 yr outbound Hohmann, minus 1 yr Saturn dwell, gives ~7 yr inbound budget. The **physical** reason to cap inbound time is bag permeability — bag wall material allows water vapor to escape over time, so a longer inbound coast means more sublimated water loss before delivery.

Per the bag-engineering analysis, end-of-mission cumulative leak is ~6 t against a ~67 t collected mass = ~9% across the full 14 years, with the inbound 7-year leg contributing roughly half — call it 4.5% over 7 years, or ~0.65%/year. Real-world the rate could be ±2× depending on bag laminate, sun-facing wall temperature, multi-layer-insulation seam quality.

**The question:** at each permeability loss rate, what burn-time budget makes all-electric at Kilopower beat Variant B on delivered mass after accounting for permeability tax?

## Pre-registered hypothesis (H-bp)

**Aggregate (H-bp-agg):** at low permeability (≤ 0.5%/year) the all-electric Kilopower architecture beats Variant B at every burn time up to ~25 years, because the permeability tax (≤ 12.5% over 25 years) does not overcome Variant B's chunk-depletion penalty (~50% of chunk consumed at the 3-km/s offload Variant B uses to close 7-year burns at Kilopower). At high permeability (≥ 2%/year) Variant B wins because all-electric's longer burn time accumulates too much loss. The crossover sits in the 0.5–1.5%/year permeability band at the Kilopower / 100-tonne-chunk cell.

**Pre-registered sub-claims:**

| Sub-claim | Predicted | Falsification |
|---|---|---|
| H-bp-a — Permeability rate at which all-electric Kilopower (100 t chunk) breaks even with Variant B | 0.8–1.5%/year | outside ±0.5%/year |
| H-bp-b — All-electric Kilopower burn time at optimum specific impulse | 18–28 years | outside ±5 years |
| H-bp-c — Permeability rate at which all-electric Fission Surface Power (40 kilowatt-electric / 200 t chunk) breaks even with Variant B | > 2%/year (Fission Surface Power burn time already fits in 7 yr, so all-electric is already the winner; no permeability rate flips it back) | falsified if any reasonable permeability rate makes Variant B win at Fission Surface Power |
| H-bp-d — At 0.65%/year (the bag-engineering empirical rate) and 25-year inbound burn, all-electric Kilopower delivered mass after loss | 50–60 tonnes | outside ±15 t |
| H-bp-e — The campaign's 14-year round-trip ceiling forecloses all-electric Kilopower regardless of permeability rate (because total round-trip becomes 30+ yr) | yes | falsified only by an explicit decision to accept longer round-trip |

**Aggregate decision:** if H-bp-a holds at 0.8–1.5%/year, the architecture decision matrix is *sensitive to bag-laminate qualification*. A bag-engineering result better than ~1%/year permeability flips Kilopower-era to all-electric, eliminating Variant B's only winning cells. Worse than 1.5%/year keeps Variant B as the Kilopower architecture. This makes the Gate-A bag bench test (per the bag-engineering doc) a load-bearing program decision.

## Method

Reuse R-chunk-fed-chemical mass accounting. Add:
- For all-electric: drop the 7-year burn-time cap. Sweep specific impulse and find the optimum that maximizes delivered_after_permeability.
- For each (chunk, reactor, permeability) cell, compute:
  - All-electric delivered (raw) and burn time at each candidate specific impulse
  - All-electric delivered after permeability = delivered_raw × (1 − loss_rate × inbound_time_yr). Negative values treated as infeasible.
  - Variant B delivered from R-chunk-fed-chemical's winner cell (Variant B's burn time is short, so permeability loss applied at its actual burn time).
- Pick the winner by delivered_after_permeability.

**Sweep axes:**

- Permeability loss rate: 0%, 0.5%, 0.65% (bag-engineering empirical), 1.0%, 2.0% per year
- Reactor power: 10, 40, 100 kilowatt-electric (where the 7-yr burn cap was binding or close)
- Chunk mass: 50, 100, 200 tonnes
- Electric specific impulse for all-electric: 1500, 2000, 2934, 5000 s

For Variant B comparison, use the R-chunk-fed-chemical winners at each (reactor, chunk).

**Validity caveats:**

- Linear permeability loss model: loss_fraction = rate × time. Real-world this may saturate (bag fills up with cold-trapped frost) or accelerate (thermal cycling damage). Linear is a defensible first cut.
- Inbound coast time equals burn time. In a real spiral profile, burn time is concentrated near periapsis; coast time between burns is longer. For low-thrust continuous burn this approximation is acceptable.
- Outbound permeability not modeled. The bag is empty outbound; no loss to penalize.
- Saturn-dwell permeability not modeled. The bag is being filled during dwell; loss rate may differ.
- Discount-rate effect of longer round-trip not modeled. A 30-year round-trip vs a 14-year round-trip is roughly half the net-present-value at 5% commercial discount, regardless of delivered mass. Flagged in the Reading; not part of the sizing.

## Result

### Winning architecture by (reactor × chunk × permeability rate)

Format: architecture · delivered_after_perm · burn_time

**Reactor = 10 kilowatt-electric (Kilopower):**

| Chunk | 0% / yr | 0.5% / yr | 0.65% / yr (empirical) | 1.0% / yr | 2.0% / yr |
|---:|---|---|---|---|---|
|  50 t | all-electric · 43.1 t · 47.6 yr | all-electric · 34.4 t · 22.6 yr | all-electric · 33.1 t · 22.6 yr | all-electric · 30.0 t · 22.6 yr | all-electric · 24.3 t · 14.7 yr |
| 100 t | all-electric · 78.8 t · 42.8 yr | all-electric · 61.9 t · 42.8 yr | all-electric · 57.7 t · 27.7 yr | all-electric · 50.9 t · 27.7 yr | **Variant B · 35.4 t · 18.7 yr** |
| 200 t | all-electric · 127.1 t · 45.4 yr | all-electric · 98.3 t · 45.4 yr | all-electric · 89.6 t · 45.4 yr | **Variant B · 74.1 t · 36.7 yr** | **Variant B · 54.4 t · 14.9 yr** |

**Reactor = 40 kilowatt-electric (Fission Surface Power):**

| Chunk | 0% / yr | 0.5% / yr | 0.65% / yr | 1.0% / yr | 2.0% / yr |
|---:|---|---|---|---|---|
|  50 t | all-electric · 42.8 t · 12.5 yr | all-electric · 40.1 t · 12.5 yr | all-electric · 39.3 t · 12.5 yr | all-electric · 37.4 t · 12.5 yr | all-electric · 33.7 t · 6.0 yr |
| 100 t | all-electric · 86.6 t · 23.2 yr | all-electric · 76.6 t · 23.2 yr | all-electric · 73.6 t · 23.2 yr | all-electric · 69.6 t · 11.0 yr | all-electric · 61.0 t · 11.0 yr |
| 200 t | all-electric · 174.4 t · 44.4 yr | all-electric · 141.5 t · 21.1 yr | all-electric · 136.5 t · 21.1 yr | all-electric · 124.8 t · 21.1 yr | all-electric · 102.9 t · 13.7 yr |

**Reactor = 100 kilowatt-electric:**

| Chunk | 0% / yr | 0.5% / yr | 0.65% / yr | 1.0% / yr | 2.0% / yr |
|---:|---|---|---|---|---|
|  50 t | all-electric · 42.0 t · 5.5 yr | all-electric · 40.9 t · 5.5 yr | all-electric · 40.5 t · 5.5 yr | all-electric · 39.7 t · 5.5 yr | all-electric · 37.4 t · 5.5 yr |
| 100 t | all-electric · 85.9 t · 9.8 yr | all-electric · 81.7 t · 9.8 yr | all-electric · 80.4 t · 9.8 yr | all-electric · 77.5 t · 9.8 yr | all-electric · 69.9 t · 4.6 yr |
| 200 t | all-electric · 173.6 t · 18.3 yr | all-electric · 157.8 t · 18.3 yr | all-electric · 153.0 t · 18.3 yr | all-electric · 143.4 t · 8.7 yr | all-electric · 129.8 t · 8.7 yr |

### Breakeven permeability rate at which architecture switches

| Reactor | Chunk | Winner at 0% / yr | Winner at 2.0% / yr | Breakeven |
|---:|---:|---|---|---:|
|  10 kWe |  50 t | all-electric | all-electric | no switch |
|  10 kWe | 100 t | all-electric | Variant B | **2.0%/yr** |
|  10 kWe | 200 t | all-electric | Variant B | **1.0%/yr** |
|  40 kWe |  50–200 t | all-electric | all-electric | no switch |
| 100 kWe |  50–200 t | all-electric | all-electric | no switch |

### Hypothesis grading

| Sub-claim | Predicted | Actual | Held? |
|---|---|---|---|
| H-bp-a — Breakeven permeability at Kilopower / 100 t | 0.8–1.5% / yr | 2.0% / yr | **falsified-high** (all-electric wins even more broadly than predicted) |
| H-bp-b — Optimum all-electric Kilopower burn time | 18–28 yr | 27.7 yr | held |
| H-bp-c — Fission Surface Power has no permeability-driven switch | yes | held (no switch up to 2.0%/yr) | held |
| H-bp-d — Delivered at 0.65% / yr / 25 yr Kilopower | 50–60 t | 57.7 t | held |
| H-bp-e — 14-yr round-trip ceiling forecloses Kilopower all-electric | yes | held — all Kilopower all-electric winners require 14+ yr burn time | held |

## Reading

**The Variant B winning region collapses to almost nothing once the 7-year burn cap is dropped.** R-chunk-fed-chemical's "Kilopower era = Variant B" finding was an artifact of the artificial burn-time constraint, not a real architectural advantage.

At the bag-engineering empirical permeability rate (0.65%/year), all-electric wins every cell tested — including Kilopower at chunks up to 200 tonnes. Variant B only wins at Kilopower with chunks ≥ 100 tonnes *and* permeability ≥ 1–2%/year, which is 1.5–3× worse than the empirical estimate.

**Five observations the result actually supports:**

1. **The 7-year cap was the binding constraint, not the permeability.** At Kilopower with 100 t chunk, all-electric without the cap delivers 78.8 tonnes (zero permeability) to 50.9 tonnes (1.0%/year permeability) — vs Variant B's 32.7 tonnes from R-chunk-fed-chemical. The cap was eating ~40 tonnes of delivered water that the all-electric architecture could otherwise have produced.

2. **All-electric Kilopower burn times are long.** 22.6 years (50 t chunk) to 45.4 years (200 t chunk). Round-trip becomes 30–50 years. This violates the campaign's prior 14-year-round-trip assumption by a factor of 2–4× and triggers a campaign-level decision about whether to accept that.

3. **Specific impulse selection at long burns is a real trade.** At Kilopower / 100 t, raising specific impulse from 1500 s to 2934 s buys 16 more tonnes delivered (62.5 → 78.8 t) but costs 19 more years of burn time (23.4 → 42.8 yr). At zero permeability, the high-Isp wins on raw delivered mass. At 2%/year permeability, the low-Isp wins (33.3 t vs 11.4 t) because the long burn loses more to leak than the high-Isp gains in propellant efficiency.

4. **Fission Surface Power (40 kilowatt-electric) is the sweet spot for all-electric.** Burn times of 12–23 years at chunks 50–200 t — within an acceptable cycle if the campaign accepts 18–30 yr round-trip. Architecture is robust across the full permeability range tested.

5. **The 14-yr round-trip ceiling is structurally inconsistent with Kilopower all-electric across all chunks ≥ 50 t.** Even at the most aggressive specific impulse (1500 s Hall), Kilopower needs 22.6 years to do the 6.42 km/s inbound burn for a 50-tonne chunk. If the campaign retains the 14-yr-ceiling, Kilopower-era flights must use Variant B; if the campaign accepts the R-cadence / R-reactor-roadmap finding that cycle time is not the dominant lever, the ceiling can be relaxed and Kilopower all-electric becomes viable.

**The discount-rate trade I didn't pre-register but matters:**

Raw delivered mass is not the right objective if cycle time materially extends. Comparing Variant B (Kilopower / 100 t, 7-yr burn, 32.7 t delivered) vs all-electric (Kilopower / 100 t, 27.7 yr burn, 57.7 t delivered after empirical permeability):

| Architecture | Delivered | Round-trip | Discount factor @ 5% | Net-present-value of delivered |
|---|---:|---:|---:|---:|
| Variant B | 32.7 t | 14 yr | 0.497 | 16.2 t-equivalent |
| All-electric (no cap) | 57.7 t | 34.7 yr | 0.176 | 10.2 t-equivalent |

**On net-present-value, Variant B beats all-electric at Kilopower** despite delivering nearly half the raw mass, because the 21 extra years of burn time at 5% commercial discount destroys two-thirds of the present value. The architecture decision at Kilopower is therefore not "all-electric vs Variant B on delivered mass" — it is "are we optimizing raw delivered mass or net-present-value-per-mission?" Different answers fall out under each objective.

**What this round still papers over:**

- **Linear permeability model.** Real permeability may saturate (cold-trap on cold-wall absorbs leak), accelerate (thermal cycling damage), or plateau (frost layer thickens and self-passivates). The 0.65%/year empirical rate is a 14-yr-mission average; year-by-year may differ.
- **Inbound coast time equals burn time.** A real spiral profile has burn near periapsis and coast in between. Permeability accumulates over both, so the effective permeability tax may be higher than this round's model.
- **Saturn-dwell permeability not modeled.** The bag is being filled during dwell; loss rate during dwell is separate from inbound and not in this analysis.
- **Discount rate held at 5% commercial.** The R-NPV round found project internal rate of return in the 4–7% range. At higher discount rates the Variant B advantage grows; at lower rates (sovereign-bond, 2–3%) the gap narrows.

## Revisit clause

H-bp-a falsified (favorable to all-electric); H-bp-b/c/d/e held. Aggregate H-bp-agg held in shape (long burns favor all-electric on raw mass, permeability flips it only at high rates) but the practical winner depends on whether the campaign optimizes raw mass or net-present-value.

**Reframed architecture decision matrix (incorporating R-chunk-fed-chemical, R-reactor-specific-power, and this round):**

| Reactor era | Recommended architecture | Burn time | Cycle penalty |
|---|---|---:|---|
| Kilopower (year 0), optimize raw delivered mass | all-electric, Isp 2000–2934 s | 23–45 yr | round-trip 30–50 yr; violates 14-yr ceiling |
| Kilopower (year 0), optimize net-present-value | Variant B at 3 km/s chemical, Isp 1500 s | 7 yr | round-trip 14 yr; raw delivered halved |
| Fission Surface Power (year 7+) | all-electric, Isp 2000–2934 s | 12–23 yr | round-trip 19–30 yr; tolerable |
| Sub-megawatt (year 12+) | all-electric, Isp 2000–5000 s | 5–18 yr | round-trip 12–25 yr |

The pre-Fission-Surface-Power Variant B winning region from R-chunk-fed-chemical is now downgraded to **a conditional architecture choice contingent on the campaign's economic objective.**


## Revisit clause

Grade H-bp-a through H-bp-e. The aggregate decision (whether the bag-laminate qualification is a load-bearing program variable) hinges on H-bp-a. If permeability crossover sits at 0.8–1.5%/year and the empirical rate from the bag-engineering doc is 0.65%/year, **all-electric Kilopower is the recommended architecture if the campaign accepts 25–30 yr round-trip — which R-cadence and R-reactor-roadmap argue may be acceptable.**
