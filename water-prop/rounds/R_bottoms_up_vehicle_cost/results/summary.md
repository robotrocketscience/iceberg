# R-bottoms-up-vehicle-cost — summary

## First-unit cost distributions

| Arch | 5%ile | median | mean | 95%ile | spread (95/5) | R7 placeholder | median / placeholder |
|---|---:|---:|---:|---:|---:|---:|---:|
| VariantB_500kWe | $2656M | $4143M | $4512M | $7609M | 2.86× | $500M | 8.29× |
| E_500kWe_200t | $2938M | $4589M | $4962M | $8197M | 2.79× | $300M | 15.30× |
| E_200kWe_100t | $1527M | $2361M | $2550M | $4210M | 2.76× | $250M | 9.44× |

## Recurring unit cost (Wright LR 15%, unit 33; factor 0.441)

| Arch | recurring p50 | first-unit p50 | R7 placeholder | recurring vs placeholder |
|---|---:|---:|---:|---:|
| VariantB_500kWe | $1825M | $4143M | $500M | 3.65× |
| E_500kWe_200t | $2022M | $4589M | $300M | 6.74× |
| E_200kWe_100t | $1040M | $2361M | $250M | 4.16× |

## P(NPV ≥ 0) at key cells

| Arch | regime | WACC | LR | P(NPV+) |
|---|---|---:|---:|---:|
| VariantB_500kWe | r8_placeholder_constant | 0.030 | 0.15 | 50.0% |
| VariantB_500kWe | bottoms_up_first_unit | 0.030 | 0.15 | 8.6% |
| VariantB_500kWe | bottoms_up_first_unit | 0.030 | 0.00 | 3.8% |
| VariantB_500kWe | bottoms_up_first_unit | 0.087 | 0.15 | 2.9% |
| E_500kWe_200t | r8_placeholder_constant | 0.030 | 0.15 | 42.1% |
| E_500kWe_200t | bottoms_up_first_unit | 0.030 | 0.15 | 2.5% |
| E_500kWe_200t | bottoms_up_first_unit | 0.030 | 0.00 | 1.1% |
| E_500kWe_200t | bottoms_up_first_unit | 0.087 | 0.15 | 0.2% |
| E_200kWe_100t | r8_placeholder_constant | 0.030 | 0.15 | 35.0% |
| E_200kWe_100t | bottoms_up_first_unit | 0.030 | 0.15 | 3.3% |

## Scoring: 7 HELD / 7 FALSIFIED of 14

See `hypothesis_scoring.md` for per-hypothesis verdicts.

## Discussion

### Headline

Replacing R7/R8's first-unit cost placeholders with a subsystem-level Monte Carlo, anchored against Cassini / Curiosity / Europa Clipper $/kg, PPE / DRACO power-and-propulsion CERs, and FSP / KRUSTY reactor extrapolation, the median first-unit cost is **8–15× the R7 placeholder** for every architecture. Round-8's P(NPV+) headline collapses correspondingly:

| Architecture | R8 placeholder P(NPV+) at sov 3% LR 15% | Bottoms-up first-unit P(NPV+) at sov 3% LR 15% | Multiplicative drop |
|---|---:|---:|---:|
| Variant B | 50.0% (reproduces R8's 51.1%) | **8.6%** | 5.8× |
| Arch E_500 | 42.1% | **2.5%** | 16.8× |
| Arch E_200 | 35.0% | **3.3%** | 10.5× |

R8's strict-dominance ordering (Variant B > E_500 > E_200 on P(NPV+)) **survives** under bottoms-up cost — H-bvc-l HELD with 0 violations across the full (WACC, LR) grid. R8's "Starship-and-markup-conditional with sovereign-financing dependency" headline becomes substantially stronger: at bottoms-up first-unit cost, the program needs a *very* favorable Starship-and-markup combination AND sovereign financing AND learning AND probably a reset of program-overhead and reactor cost assumptions to clear NPV-positive with even a 10% probability.

### Recurring lesson #7 strike 8 (pre-registration arithmetic vs model mismatch)

The STUDY.md reference cell A described Variant B as "Kilopower-class 10-kWe reactor, chemical Saturn-departure kick stage, ~$1.17B median first-unit." But R7's `Architecture("VariantB_500kWe", 500.0, 200.0, 2000.0, 14.50, 80.0, 500.0)` uses a **500-kWe reactor** with chemical kick. These are different vehicles. The Monte Carlo run used the R7-matched 500-kWe stack (correct), but the pre-registered H-bvc-a/d/g were arithmetic-anchored on the Kilopower-class stack (wrong).

Result: H-bvc-a (Variant B median in $900M–$1.6B) falsified at $4.14B; H-bvc-d (E_500/B ratio 3–5×) falsified at 1.11× because both architectures share the same 500-kWe reactor line item; H-bvc-g (recurring VB $400M–$700M) falsified at $1.83B.

**These three falsifications are protocol violations, not informative findings.** The actual measured numbers (VB first-unit $4.14B, ratio 1.11×, recurring $1.83B) are the load-bearing outputs. The pre-registered bands described a *different architecture* than the one R7/R8 actually models.

**Recurring-lesson-7 v4 protocol fix:** before pre-registering ranges, READ the architecture parameters from the upstream module being re-used, do NOT re-construct the architecture from prose. The R7 `Architecture` dataclass is the source of truth for `reactor_kwe`, `chunk_t`, `isp_s` etc., and the cost stack must match those parameters not the matrix prose.

### Informative findings

The other 11 hypotheses divide into 7 HELD (H-bvc-b, c, h, i, j, l, m) and 4 FALSIFIED-informatively (H-bvc-e, f, k, n).

- **H-bvc-b, c, h HELD:** the bottoms-up reference cells for Arch E_500 ($4.59B), E_200 ($2.36B), and E_500 recurring ($2.02B) match the pre-registered bands well. The CER stack reproduces independently of the Variant B confusion.

- **H-bvc-i, j HELD strongly:** at bottoms-up first-unit with no learning, sov 3% P(NPV+) collapses to 3.8% (VB) and 1.1% (E_500). The R8 strict-dominance ordering survives because every architecture takes the same multiplicative hit from the cost-uplift; differences in NPV-probability shrink in absolute terms but the ordering does not change. **Round-8's "Variant B is NPV-probability dominant" finding is robust to cost uncertainty.**

- **H-bvc-l HELD:** strict-dominance survives across all (WACC, LR, regime) cells.

- **H-bvc-m HELD strongly:** at corporate 8.7% WACC + bottoms-up first-unit, max P(NPV+) across any architecture and any LR is 3.6%. **The corporate-financing path is closed under bottoms-up cost.** Sovereign financing is now not optional — it is mandatory for any meaningful P(NPV+).

- **H-bvc-e FALSIFIED-informatively** at 50.9% (predicted >55%): reactor + PMAD + thrusters are dominant in *hardware* (77%) but I&T and program-overhead inflate the first-unit-total denominator, dropping the share to ~51%. Lesson: cite shares against the right denominator.

- **H-bvc-f FALSIFIED:** max 95/5 spread is 2.86× (predicted ≥3.5×). The log-normal subsystem sigmas summed under the central-limit theorem more tightly than predicted. The reactor's factor-3 individual spread doesn't propagate to factor-3 total because it's only 30–35% of total, and the other components are tighter.

- **H-bvc-k FALSIFIED:** Variant B sov 3% LR 15% bottoms-up is 8.6%, not 35–60%. Reason: bottoms-up median ($4.14B first-unit) is so much larger than the placeholder ($500M) that LR 15% applied through fleet ramp does not bring the program-level capital cost back into the placeholder's neighborhood. **The R7/R8 placeholder was likely already a recurring-with-learning estimate**, but recurring-with-learning *from a $4.14B first-unit base* is $1.83B at unit 33 — still ~3.7× the placeholder, not equal to it.

- **H-bvc-n FALSIFIED at the threshold:** E_500/E_200 cost ratio 1.94 vs mass ratio 1.89, i.e. cost scales slightly *super-linearly* with mass — by 2.6%. Reason: the reactor-cost-per-kWe scales roughly linearly with reactor mass (both halve from E_500 to E_200), but the program-level overhead has a floor cost that doesn't halve. Falsified by a hair; the qualitative finding (cost ratio ≈ mass ratio) holds.

### Architecture decision matrix consequences

1. **R7/R8 placeholders ($300–500M) are NOT defensible as first-unit cost.** They are approximately right as recurring-with-learning estimates *only if* the first-unit base is in the $1–2B range. With a $4–5B bottoms-up first-unit base, even recurring-with-learning is $1.5–2B per ship — 3–7× the placeholders.

2. **The R8 P(NPV+) headline must be footnoted.** Round 8 reported "Variant B 51.1% / Arch E_500 42.8% at sov 3% LR15." Under bottoms-up first-unit cost, these become **8.6% / 2.5%**. The matrix should carry both numbers with a regime label, and treat the bottoms-up number as the load-bearing one for go/no-go decisions.

3. **Strict-dominance of Variant B over Arch E on P(NPV+) survives — and strengthens in relative terms.** Variant B at 8.6% is 3.4× Arch E_500's 2.5% under bottoms-up; under placeholders it was only 1.2× (50.0%/42.1%). Variant B's narrower architectural commitment (chemical kick + electric cruise) is *more* dominant under realistic costs because Arch E's all-electric stack pays an extra cost premium on the bigger thruster array and radiator.

4. **The R8 joint-expected-value flip (Arch E_500 wins on credibility × NPV-probability) needs re-running.** With Arch E_500's P(NPV+) at 2.5% instead of 42.8%, the joint Arch E_500 number drops from 4.78% × 42.8% = 2.05% to **4.78% × 2.5% = 0.12%**. Variant B's joint: 0.78% × 8.6% = 0.067%. **Arch E_500 still wins the joint expected-value calc, but the ordering is now a near-tie (~2× rather than ~5×) at a much lower absolute level. The "favored architecture" question is no longer load-bearing — the program is so far below 1% joint expected-value that the architecture-ordering debate is a footnote.**

5. **Corporate financing path is closed.** Max P(NPV+) under any (arch, LR) at 8.7% WACC + bottoms-up cost is 3.6%. The program is sovereign-only under realistic cost.

6. **Reactor + PMAD + thruster array is ~51% of first-unit cost.** The single highest-leverage cost-reduction lever is the reactor; the thruster array is a softer (modular, mass-producible) target. Bag, structure, thermal, and avionics are bargain-bin in comparison.

### What this round did NOT do

- No covariance modeling between subsystem cost overruns. Real programs covary positively; this is the main reason the upper tail is likely too low. A correlated-cost MC is the natural follow-up.
- No cost-escalation modeling over the 23-year build window. ~3% inflation × 23 yr = ~2× nominal escalation, which would push first-unit upper-tail to $10–15B for Arch E_500.
- No GAO-style schedule slip / cost growth uplift. Aerospace MDAP programs typically run 30–80% over budget at ATP+5 years; not modeled.
- No bottoms-up NRE separation. Program overhead bundles in NRE today; splitting would lower the per-unit recurring cost but raise the year-0 sunk cost.
- No exploration of Variant B with a Kilopower-class reactor instead of 500-kWe. The matrix prose actually describes Variant B that way; R7's `Architecture` does not. If a true Kilopower-class Variant B exists (small reactor + chemical kick, no Saturn-side electrolysis), its bottoms-up first-unit would land near my STUDY.md reference cell A: **$1.17B median.** That ship has different round-trip-time and delivered-mass numbers than R7's `VariantB_500kWe`, and would need its own R7-style NPV cell to compare apples-to-apples. **This is the cleanest follow-up round: R-variant-B-kilopower-vs-500kWe.**
