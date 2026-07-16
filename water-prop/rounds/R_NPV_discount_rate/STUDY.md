# R-NPV — Discount-rate NPV of ICEBERG cashflow

**Status:** pre-result.

## Question

R15-rerun explicitly flagged: *"Discount rate not applied. Real financial modeling would discount the year-30+ cash flows substantially. At 8% discount, $1 billion at year 30 is worth $99 million in year-0 dollars. NPV calculation may make even the audited scenario look worse than the un-discounted picture suggests."*

Every financial round to date (R15, R15b, R15-rerun) has reported **undiscounted cumulative cashflow** and **undiscounted break-even year**. Both metrics are misleading when (a) the round trip is 18 years and (b) steady-state revenue does not arrive until year 20+.

This round attaches a discount rate to the R15-rerun cashflow stream and asks: under what combination of discount rate, pricing, sovereign purchase, and ship cost is the project NPV-positive at year 0?

## Pre-registered hypothesis (H-NPV)

**Aggregate (H-NPV-agg):** ICEBERG is **NPV-negative at any commercial discount rate (≥8%)** across all tested pricing × sovereign × ship-cost cells. NPV becomes positive only at sovereign-development discount rates (≤5%) and only at premium pricing ($5,000+ per kilogram) or with sovereign purchase. The R15-rerun "year 40 break-even" finding translates to "NPV-negative or marginal" once time-value-of-money is applied. The asset class is sovereign-treasury bond rates, not commercial infrastructure or venture.

**Pre-registered sub-claims:**

| Sub-claim | Predicted | Falsification threshold |
|---|---|---|
| H-NPV-a — NPV at 8% discount, best-case audited cell ($10k/kg + $2B sovereign at year 11 + commercial_mid ship cost) | NPV ∈ [-$5B, +$2B] | outside ±$3B |
| H-NPV-b — NPV at 5% infrastructure discount, same best-case cell | NPV ∈ [+$1B, +$8B] | outside ±$3B |
| H-NPV-c — NPV at 3% sovereign discount, same best-case cell | NPV ∈ [+$5B, +$15B] | outside ±$5B |
| H-NPV-d — NPV at 8% discount, conops-baseline cell ($2k/kg, no sovereign, commercial_mid) | NPV ∈ [-$15B, -$8B] | outside ±$3B |
| H-NPV-e — Cells with positive NPV at 10% commercial discount | 0 of 90 cells | held if 0; falsified if ≥1 |
| H-NPV-f — Cells with positive NPV at 5% infrastructure discount | 5–25 of 90 cells | outside range |
| H-NPV-g — Cells with positive NPV at 3% sovereign discount | 25–60 of 90 cells | outside range |

**Aggregate decision:** if H-NPV-e holds (no positive NPV at commercial discount), the conops cannot honestly be pitched as a venture or growth-equity opportunity at any pricing. The "Suez Canal not Amazon" framing is reinforced and made quantitative.

## Method

Reuse the R15-rerun cashflow model (audited assumptions: duty cycle 0.7, 18-year round trip, 3-flyby tour, water radio-frequency ion thruster). Apply discount rate `r` to the per-year (revenue − cost) stream:

```
NPV = Σ_{t=0..44} (revenue_t − cost_t) / (1 + r)^t
```

Discount rates tested:
- **3%** — long-duration sovereign infrastructure bond benchmark (US 30-year Treasury, World Bank IDA)
- **5%** — established multilateral infrastructure (World Bank IBRD, IFC long-tenor)
- **8%** — commercial infrastructure benchmark (regulated utility weighted-average-cost-of-capital)
- **10%** — commercial growth / corporate benchmark
- **15%** — venture-capital hurdle rate (sanity floor)

Sweep grid: 5 prices × 3 sovereign amounts × 2 sovereign years × 3 ship-cost scales × 5 discount rates = **450 cells**. Per-cell output: NPV at year 0, undiscounted cumulative cashflow at year 45, undiscounted break-even year.

**Validity caveats:**
- Discount-rate-driven NPV is the right metric for capital-allocation decisions but does NOT capture optionality value (each delivered ship buys information about the next). A real-options DCF model (e.g. Black-Scholes on per-ship value) would tilt slightly more positive — out of scope for this round.
- 45-year horizon is artificial; real ICEBERG operations would continue indefinitely. Truncation undercounts terminal value. A perpetuity-growth terminal value at year 45 would add a tail. Tested as sensitivity.
- Inflation not separated. All numbers are real dollars; discount rates are real rates.
- Rate-of-return on sovereign-treasury cash held during the 18-year delay before first revenue is omitted (would slightly improve NPV — opportunity-cost of capital is partly captured by the discount rate itself).

## Result

### Best-case audited cell ($10k/kg + $2B sovereign at year 11 + commercial_mid)

| Discount rate | NPV at year 0 ($B) | NPV with perpetuity terminal value ($B) | Undisc. break-even |
|---|---:|---:|---:|
| 3% (sovereign) | +1.66 | +44.32 | year 40 |
| 5% (infrastructure) | −2.15 | +8.62 | year 40 |
| 8% (commercial) | −3.51 | −1.62 | year 40 |
| 10% (growth) | −3.45 | −2.79 | year 40 |
| 15% (venture) | −2.74 | −2.68 | year 40 |

**Internal-rate-of-return on this cell:** 3.63% (no terminal value) / 6.97% (with perpetuity terminal value, growth 0%). The project IRR brackets sovereign-treasury / long-duration-infrastructure rates exactly — never reaches commercial-equity hurdles.

### Conops-baseline cell ($2k/kg + no sovereign + commercial_mid)

| Discount rate | NPV ($B) | NPV+TV ($B) | Undisc. break-even |
|---|---:|---:|---:|
| 3% | −14.14 | −12.95 | never |
| 5% | −10.28 | −9.97 | never |
| 8% | −6.82 | −6.76 | never |
| 10% | −5.41 | −5.39 | never |
| 15% | −3.43 | −3.43 | never |

The conops baseline pricing is structurally infeasible at any discount rate — never recovers cost.

### Positive-NPV cell counts (out of 90 price × sovereign × ship-cost cells per rate)

| Discount rate | NPV > 0 | NPV+TV > 0 |
|---|---:|---:|
| 3% sovereign | 12 / 90 (13%) | 48 / 90 (53%) |
| 5% infrastructure | 4 / 90 (4%) | 24 / 90 (27%) |
| 8% commercial | 0 / 90 (0%) | 1 / 90 (1%) |
| 10% growth | 0 / 90 (0%) | 0 / 90 (0%) |
| 15% venture | 0 / 90 (0%) | 0 / 90 (0%) |

**At any commercial discount rate (≥8%), there is no combination of pricing, sovereign purchase, and ship cost that yields positive NPV (the lone NPV+TV>0 cell at 8% requires premium-pricing + max-sovereign + lowest ship cost — a corner).**

### Hypothesis grading

| Sub-claim | Predicted | Measured (no TV / with TV) | Verdict |
|---|---|---|---|
| H-NPV-a — NPV at 8%, best-case cell | [−$5B, +$2B] | −$3.51B / −$1.62B | **held** |
| H-NPV-b — NPV at 5%, best-case cell | [+$1B, +$8B] | −$2.15B / +$8.62B | **falsified without TV; held at upper edge with TV** |
| H-NPV-c — NPV at 3%, best-case cell | [+$5B, +$15B] | +$1.66B / +$44.32B | **falsified both directions; uncertainty band missed terminal-value sensitivity** |
| H-NPV-d — NPV at 8%, conops baseline | [−$15B, −$8B] | −$6.82B | **falsified-conservative** by ~$1B |
| H-NPV-e — Positive-NPV cells at 10% | 0 of 90 | 0 / 0 | **held — load-bearing** |
| H-NPV-f — Positive-NPV cells at 5% | 5–25 of 90 | 4 / 24 | **held with TV; falsified-conservative without** |
| H-NPV-g — Positive-NPV cells at 3% | 25–60 of 90 | 12 / 48 | **held with TV; falsified-conservative without** |

**Aggregate H-NPV-agg: HELD as stated.** ICEBERG is NPV-negative at any commercial discount rate (≥8%) across all 270 cells tested at 8% / 10% / 15%. NPV becomes positive only at sovereign-development rates (3%) and only with premium pricing and / or sovereign purchase. The "Suez Canal not Amazon" framing is now quantitative: IRR ≈ 4–7% — sovereign-bond territory, never commercial-equity territory.

## Reading

**The single most load-bearing financial finding of the campaign.** R15-rerun showed that under audited propulsion assumptions, the conops' steady-state revenue claim is real *and* the undiscounted break-even is year 40+. R-NPV closes the loop: under any discount rate above ~7%, that "year 40 break-even" never recovers in present-value terms. The project IRR is 3.6% (no terminal value) to 7.0% (with perpetuity terminal value, growth 0%). For comparison:

- US 30-year Treasury yield: ~4–5% (2026)
- World Bank IDA / multilateral infrastructure lending: 1–4%
- Regulated-utility weighted-average-cost-of-capital: 7–10%
- Corporate growth-equity hurdle: 12–20%
- Venture-capital hurdle: 25–40%

**ICEBERG can clear sovereign-treasury and IDA-multilateral hurdles. It cannot clear regulated-utility hurdles. It cannot remotely clear venture or growth-equity hurdles.**

This is a quantitative confirmation of a qualitative claim that was already floating in the campaign documents (see `~/projects/iceberg/ICEBERG-pitch.md` and earlier memory: *"Suez Canal, not Amazon"*). The novelty here is the IRR number: **6.97%** with terminal value. That is *almost exactly* the regulated-utility cost-of-capital cliff. ICEBERG sits structurally below the threshold at which any equity investor — even a patient one — can rationally fund it, but structurally above the rate at which sovereign infrastructure can.

The architectural implication: **ICEBERG is not a private-equity asset.** Investor pitching at any pricing should presume the cap table is sovereign-development bank, treasury-bond-class, or international-multilateral instruments. Any framing of "venture-fundable" or "growth-equity-fundable" is mathematically impossible at the audited cashflow profile.

**The terminal value matters more than I anticipated.** Without a terminal-value tail, NPV at 5% is negative; with one, it is +$8.6B. ICEBERG's value is concentrated in the perpetual-operations tail, not in the 45-year horizon. Any honest financial pitch must include the terminal-value calculation explicitly — and the assumption that operations continue beyond the horizon is then itself load-bearing (e.g. asteroid impact, mission abandonment, or a competitor-driven price collapse at year 50 wipes out most of the value).

## Revisit

- **H-NPV-c (NPV at 3% on best-case cell) was the worst-calibrated prediction.** I anticipated [+$5B, +$15B]; reality is +$1.66B without TV and +$44B with TV. The factor I missed: terminal value swings the answer by an order of magnitude. Lesson: separate point predictions for "cashflow during horizon" vs "perpetuity tail value." Don't aggregate.
- **H-NPV-e was the most important to pre-register correctly.** "Zero cells positive at 10% commercial discount" is the load-bearing claim of the round, and it held. This is the falsifiable test that distinguishes "ICEBERG is sovereign-class" from "ICEBERG could plausibly be commercial-equity-class."
- **Methodology defect surfaced:** every prior round's "best-case cell" framing relied on undiscounted dollars. The best-case cell language is misleading when the implicit discount rate is 0%. Update R15-rerun's reading to include "best-case cell at sovereign-3pct discount: NPV +$1.66B; at commercial-8pct: NPV −$3.51B" instead of just "year-40 break-even."
- **Internal-rate-of-return is the cleanest single number.** 3.6%–7.0% is the campaign's headline financial number going forward. Replace "year 40 break-even" with "IRR 4–7%, sovereign-class instrument" in the deck.

## Cross-learning

- **Decision-supporting:** any pitch deck or investor framing must lead with IRR, not undiscounted cashflow. Specifically: "IRR 4–7%, NPV-positive only at sovereign-development discount rates (≤5%), break-even at commercial discount rates is mathematically impossible at any tested pricing." This makes the "Suez Canal" framing falsifiable rather than rhetorical.
- **Negative for any framing of ICEBERG as venture-fundable.** The R15b "$80–150M demonstrator at even-money odds" framing (memory belief 2391d86c) implies even-money venture odds; this is now untrue at any discount rate above sovereign. The demonstrator is a sovereign-treasury-funded option-purchase on the long-tail asset, not a venture bet.
- **Positive for R-cadence (queued):** if multi-ship-per-window cadence multiplies revenue, IRR rises proportionally. Worth re-running R-NPV with R-cadence outputs once R-cadence resolves. Quick estimate: 2x cadence → IRR rises by ~1.5pp; 3x cadence → IRR rises by ~3pp. Could move ICEBERG from "sovereign-only" to "regulated-utility-eligible."
  - **Retracted by R-cadence (post-result).** Actual maximum IRR lift from cadence alone is **+0.55pp at N=2 compressed schedule** (6.97% → 7.52%). Higher cadences are anti-optimal under the R15-rerun reactor roadmap because schedule compression denies late-launching ships access to the late-era megawatt-class reactor. The "1.5pp at 2x / 3pp at 3x" first-principles estimate above was wrong by 3× and in the wrong direction at N≥3. The actual dominant exogenous IRR lever is reactor-roadmap timing (A-REACTOR), not cadence. See `rounds/R_cadence_multiship/STUDY.md`.
- **Methodology lesson #5:** every cashflow round must report (a) NPV at multiple discount rates, (b) IRR, and (c) terminal-value sensitivity. The R15-rerun reading was technically correct ("break-even at year 40") but operationally misleading. Add discount-rate analysis to the protocol's standard cashflow-round template.
- **Risk register update needed.** Add B-DISCOUNT or update B-FUND: "ICEBERG IRR ≈ 4–7% places it structurally outside any private-equity capital structure. Capital-source risk is now quantitative, not just qualitative." This makes B-FUND a more confident L4-I4 = 16 risk (load-bearing for the company's existence, not just its capital structure).
- **Promotes R-cadence and demotes R-thermal-2.** The single largest IRR lever is cadence (revenue multiplier); thermal duty-cycle improvement is second-order. Sequence R-cadence next.

