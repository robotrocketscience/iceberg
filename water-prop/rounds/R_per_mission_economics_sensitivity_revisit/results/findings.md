# R-per-mission-economics-sensitivity-revisit — findings.md

**Author:** rhea
**Date:** 2026-05-15 (latest+8, immediately after R-reactor-specific-power-program-targets)
**Self-questioning round.** Tests round-9 R-reactor-specific-power-program-targets H7's cost-anchor assumption and decision-frame framing.

---

## Hypotheses adjudicated

| H | predicted | measured | status |
|---|---|---|---|
| H1 | corrected conditional program net-present-value at zero discount, central anchors, in [-$15 billion, -$3 billion] | -$22.0 billion | **FALSIFIED** pessimistic — I forgot to multiply launch cost by launches-per-mission in the back-of-envelope; corrected number is 3× more negative than predicted |
| H2 | break-even clearing price for conditional cashflow in [$5, $40] million per tonne | central $22.4 million per tonne; sweep range $22–$60 million per tonne | **HELD** at central anchor |
| H3 | conjunction-weighted program net-present-value at corrected anchors in [-$15 billion, -$5 billion]; magnitude correction from H7 in 8–15× range | -$24.6 billion; correction ratio 5.4× | **FALSIFIED** — magnitude correction was 5.4×, smaller than predicted 8–15×; the cost-anchor error (5.3× over) drove the correction proportionally |
| H4 | total program cost in Flagship-class band [$3 billion, $11 billion] | $24.6 billion | **FALSIFIED** — ICEBERG demonstrator at conservative anchors sits between Mars Sample Return ($11 billion) and Apollo (~$140 billion). **Super-Flagship class, not Flagship class.** |
| H5 | two-track framing (return-seeking-ruled-out + sovereign-grant-viable-in-principle) is internally consistent | track A ruled out (-$24.6 billion conjunction-weighted); track B viable conditional on Apollo-class policy commitment, not Flagship | **HELD** with refinement — two-track framing valid but sovereign-grant track is harder than initially framed |
| H6 | methodology-lesson candidate #12 (cross-validate cost anchors) is the dominant single source of H7 magnitude error | cost-correction ratio 5.3× ≈ net-present-value correction ratio 5.4× | **HELD** |

**Aggregate: 3 of 6 held, 3 falsified.** All three falsifications were pessimistic — I systematically under-counted the corrected magnitude in pre-registration. The reason is a separate arithmetic error in my own back-of-envelope (forgot launches-per-mission multiplier on launch cost). This is methodology lesson candidate #13: **double-check arithmetic in pre-registration back-of-envelope, especially in a round whose stated purpose is to question prior assumptions.** Falsifying my own self-questioning round's pre-registration is its own little lesson.

---

## Headline

**Round-9 H7's net-present-value magnitude was off by 5.4× due to cost over-counting (used $5 billion per mission instead of corrected $0.94 billion). Direction was correct; magnitude was inflated. Corrected conjunction-weighted program net-present-value at zero discount is -$24.6 billion at central anchors, not -$132.5 billion.** Corrected conditional-on-success program net-present-value is -$22.0 billion. **Both decision frames remain net-present-value-negative at central anchors.** ICEBERG demonstrator at conservative anchors sits in the **super-Flagship class** at $24.6 billion total program cost (between Mars Sample Return and half-Apollo), not the Flagship class I initially framed in H4. The two-track decision-frame distinction (return-seeking vs sovereign-grant) is structurally valid but the sovereign-grant track is harder than I claimed: it requires Apollo-class policy commitment, not Flagship-class commitment.

---

## Reading

R-reactor-specific-power-program-targets H7 said "sovereign-grant only." This round refines: **sovereign-grant only AND only at super-Flagship-class policy commitment.** The cost anchor that landed at $24.6 billion total program is not arbitrary — it's launch-dominated (3 launches per mission × 25 missions × $0.30 billion = $22.5 billion of $24.6 billion). The ship capital expenditure and nonrecurring engineering are second-order. **Launch cost is the binding cost lever for ICEBERG demonstrator viability at the sovereign-grant decision frame.** Drops in per-launch cost (Starship optimistic at $0.10 billion versus my $0.30 billion central) or in launches-per-mission (1 launch per mission instead of 3) move the program cost back into Flagship class. The whole-program break-even on launches-per-mission at Flagship-class ceiling $11 billion: 25 × launches × $0.30 = $7.5 billion + nonrecurring $1.0 billion + ship $1.08 billion = $9.58 billion at 1 launch per mission; **single-launch architecture at Starship pricing keeps ICEBERG inside Flagship class.** Two launches per mission ($14.6 billion total) is super-Flagship. Three launches (central anchor) is comfortably super-Flagship.

The 99-of-324 sweep rows that produced positive conditional-success net-present-value are concentrated at (clearing price ≥ $25 million per tonne, launches-per-mission = 3, ship reuse = 5, missions ≥ 25, low nonrecurring engineering). Inspection: the cheapest positive-net-present-value anchor combo is (price $25 million per tonne, launches 3, reuse 5, missions 25, nonrecurring engineering $0.5 billion) giving cashflow +$0.02 billion per mission and net-present-value +$0.03 billion. **Conditional-success closure exists, but only at speculative clearing-price scenarios (10× BEST_CELL).** R-LEO-water-demand-curve's clearing-price Monte Carlo bracket presumably includes some tail probability of $25 million per tonne; without the full distribution, this is an upside-only sensitivity.

Zero of 324 sweep rows produced positive conjunction-weighted net-present-value. This is the same finding as round 9 H7: **return-seeking-capital framing is ruled out under any defensible reactor-program-prior**, even at aggressively-optimistic cost + clearing-price + cadence anchors. The conjunction posterior (0.167%) is the binding constraint, not the per-mission economics.

The H4 falsification is the most matrix-relevant. R-reactor-specific-power-program-targets H6 said "technology-demonstrator-only." H4 attempted to refine to "Flagship-class technology-demonstrator." Corrected: **super-Flagship-class technology-demonstrator at conservative anchors.** The relevant policy comparison is not Cassini ($3.9 billion) or Europa Clipper ($5 billion) but rather Mars Sample Return ($11 billion baseline, current cost estimates $25–30 billion) or the Space Launch System program ($50+ billion cumulative). **ICEBERG at conservative anchors sits in the same policy commitment class as Mars Sample Return — which is currently under sustained political review and budget pressure.** This is a material change to the matrix's pitch posture framing.

---

## Cross-learning

1. **Updates R-reactor-specific-power-program-targets H7.** H7's $132.5 billion magnitude was anchored on inflated cost numbers ($5 billion per mission, no ship-reuse, no nonrecurring-engineering bracket against R-architecture-D-cost). Corrected: $24.6 billion. **Round-9 H7 is direction-correct, magnitude-wrong-by-5×.** Methodology lesson candidate #12 holds: cross-validate cost anchors against recent rounds before back-of-envelope.

2. **Two-track decision-frame distinction.** Round-9 mixed return-seeking-capital and sovereign-grant decision frames under a single "structurally negative" verdict. This round separates them. Return-seeking-capital framing is ruled out under every sweep tested. Sovereign-grant framing is viable in principle but requires super-Flagship-class policy commitment at conservative anchors. Matrix axis 17 should distinguish.

3. **Launch cost is the binding lever.** Of $24.6 billion total program cost, $22.5 billion is launches. The closure path to Flagship-class is single-launch architecture, not cheaper-ship or shorter-nonrecurring-engineering. titan-2 R-launch-cost-sensitivity flagged $0.20 billion Starship vs $0.70 billion mixed Falcon-Heavy as a 2–3 percentage-point internal-rate-of-return swing for Variant B; for the ICEBERG demonstrator, **launches-per-mission is the dominant cost driver, not per-launch price.** Reducing launches-per-mission from 3 to 1 is a $15 billion program-level saving. Worth a round on what architecture supports single-launch per mission.

4. **R-LEO-water-demand-curve clearing-price tail is load-bearing.** 99 of 324 sweep rows produce positive conditional-success net-present-value when clearing price ≥ $25 million per tonne (10× BEST_CELL). This is in the upper tail of the demand-curve Monte Carlo. If the demand-curve distribution has any meaningful probability mass above $25 million per tonne — which it might, under aggressive Mars-bound traffic scenarios — then the **conditional-success return-seeking framing closes at upside scenarios.** Worth a follow-on round that re-reads the demand-curve full distribution and computes P(clearing price ≥ break-even) integrated over the demand curve.

5. **Methodology lesson candidate #13 (new):** double-check arithmetic in pre-registration back-of-envelope, especially in a round whose stated purpose is to question prior assumptions. I forgot to multiply launch cost by launches-per-mission in my own back-of-envelope (`$0.65 / 15 + $0.30 = $0.343 billion per mission` should have been `$0.65 / 15 + 3 × $0.30 = $0.943 billion per mission`). H1, H3, H4 all falsified pessimistic because of this error. The round caught its own arithmetic error via the run.py output; pre-registration discipline detected the failure mode at grading time. **Worker who pre-registers numeric ranges should compute the central anchor twice via different paths and check they match.**

---

## Next-round candidates

1. **R-single-launch-architecture-feasibility.** Question: what mission architecture supports 1 launch per mission (vs 3 central / 5 conservative)? Starship 100-tonne payload to low-Earth orbit limits the outbound vehicle stack mass. ICEBERG demonstrator needs ≥ 200-tonne chunk outbound + reactor + tug + propellant. Single-launch requires either smaller chunk (loss of L0-05 compliance per phoebe R-variant-B-100t-resizing) or lighter reactor (10× specific power lift, paper-aspiration territory) or smaller propellant stack. This is the highest-leverage cost-driver round.

2. **R-clearing-price-tail-integration.** Re-read R-LEO-water-demand-curve full Monte Carlo. Compute P(clearing price ≥ $25 million per tonne) integrated over the distribution. If non-negligible (say ≥ 5%), the conditional-success return-seeking framing has upside-tail closure under aggressive Mars-traffic scenarios.

3. **R-mars-sample-return-program-comparison.** Sovereign-grant policy precedent. Mars Sample Return is the closest analog to ICEBERG demonstrator (super-Flagship class, technology-demonstration-heavy, multi-decade timeline, sovereign-funded). MSR's current $25–30 billion cost estimate, sustained political review, and probable de-scoping inform what ICEBERG's policy reception would look like.

4. **R-fast-cruise-impact-on-h1-floor** (still queued from round 9's findings; unchanged).

5. **R-non-aerocapture-engineering-prior-update** (still queued from round 9's findings; unchanged).

---

## Revisit

Pre-registration accuracy: 3 of 6 held; 3 falsified pessimistic. The methodology-lesson-candidate-#13 finding (arithmetic error in self-questioning round's own back-of-envelope) is the dominant lesson. **The round produced its own pre-registration falsifications by recapitulating the same class of error it was designed to catch.** Cross-round cost-anchor inconsistency caught at round 10; intra-round arithmetic error caught at run-time. Both should be caught at STUDY.md drafting time. The asymmetry between methodology lesson 11 (grade SCOPE against input data) and 13 (double-check own arithmetic) is that lesson 11 catches SCOPE errors, lesson 13 catches your-own-back-of-envelope errors. Worker needs both.

H1 / H3 / H4 falsifications are direction-correct and methodologically informative; the structural reading (round-9 H7 corrected magnitude is -$22 to -$25 billion, return-seeking ruled out, sovereign-grant requires super-Flagship commitment) is robust to the arithmetic error. The matrix recommendations from this round stand despite the falsifications.
