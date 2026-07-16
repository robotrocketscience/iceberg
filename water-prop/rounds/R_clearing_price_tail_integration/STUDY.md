# R-clearing-price-tail-integration-decision-frame — STUDY.md

**Author:** rhea (worker session, iceberg-rhea-2 branch)
**Date:** 2026-05-15 (latest+8, third round this sitting)
**Status:** pre-registration. Synthesis round; no new physics or economics; integrates R-LEO-water-demand-curve distribution over R-per-mission-economics-sensitivity-revisit break-even thresholds.

## Why this round

R-per-mission-economics-sensitivity-revisit (round 10, just shipped) found:
- Round-9 H7 magnitude correction of 5.4× (return-seeking framing ruled out at conjunction-weighted)
- Conditional-success break-even clearing price $22 million per tonne at 3 launches per mission

But round 10 anchored on BEST_CELL clearing price ($2.5 million per tonne) — a single-point estimate. R-LEO-water-demand-curve (enceladus-r5, Saturn integration `e7d43dd`) ran a Monte Carlo on the clearing price with a wide distribution:

- p05: $0.42 million per tonne
- p25: $1.86 million per tonne
- p50: $5.28 million per tonne (already above BEST_CELL anchor)
- p75: $14.59 million per tonne
- p95: $61.27 million per tonne

My round-10 break-even ($22 million per tonne) sits between p75 and p95. **A meaningful tail fraction of the demand-curve distribution lies above break-even.** Round-10's "return-seeking-capital ruled out" was anchored at point-estimate $2.5 million per tonne; that framing ignores the distribution tail.

This round integrates the demand-curve distribution over the break-even threshold to compute P(market clearing price ≥ break-even) at three launch-count anchors, then composes with the full conjunction posterior from round 9 to articulate three distinct decision frames.

---

## Pre-registered hypotheses

The demand-curve distribution is approximated as log-normal from its percentiles. Log-base-10 percentiles: p05 = 2.62, p50 = 3.72, p95 = 4.79. Sigma_log10 ≈ 0.65, mu_log10 ≈ 3.72.

### H1 — 3-launch architecture, conditional break-even

Break-even at 3 launches per mission, ship reuse 15, H2a delivered 42 tonnes: $22.4 million per tonne (per round-10 H2).

Log10($22.4 million per tonne / 1 million per tonne) = log10(22.4 × 1000 / 1000) = log10($22,400 per kg) = 4.35.

Z-score in log space = (4.35 - 3.72) / 0.65 = 0.97.

P(clearing price ≥ break-even) = P(Z ≥ 0.97) ≈ **0.166 (16.6%)**.

| | predicted | falsification |
|---|---|---|
| H1 | P(clearing price ≥ break-even at 3 launches) integrated over demand-curve log-normal fit is in [10%, 25%]; central 17% | falsified if outside, or if the log-normal fit produces a poor match to the empirical percentiles |

### H2 — 1-launch architecture, conditional break-even

Break-even at 1 launch per mission, ship reuse 15: cost = $0.65/15 + 1 × $0.30 = $0.343 billion. Per delivered tonne (42 tonnes): $0.343 billion / 42 = $8.17 million per tonne.

Log10($8170 per kg) = 3.91. Z = (3.91 - 3.72) / 0.65 = 0.30.

P(clearing price ≥ break-even) = P(Z ≥ 0.30) ≈ **0.382 (38.2%)**.

| | predicted | falsification |
|---|---|---|
| H2 | P(clearing price ≥ break-even at 1 launch / mission) is in [30%, 50%]; central 38% | falsified if outside |

### H3 — conditional-success program net-present-value distribution

Compose P(clearing price ≥ break-even) with the assumption that price-above-break-even implies positive per-mission cashflow (proxy for positive program net-present-value at zero discount). At 3 launches per mission, conditional-success program net-present-value at zero discount is positive with probability ≈ H1's 17%.

Compare to R-LEO-water-demand-curve's `E_500kWe_200t` P(NPV>0) at zero discount = 0.47, at sovereign-bond 3% = 0.29, at corporate-growth 8.7% = 0.08.

Difference between this round's 17% and demand-curve's 47%: the demand-curve calculation appears to allow for fleet-scale revenue (multiple ship-lifetimes, learning-rate price evolution) that my point-estimate per-mission analysis doesn't. **Treat 17% as a conservative lower bound on conditional-success P(positive net-present-value at zero discount); 47% as an upper bound from the demand curve's fleet calculation.**

| | predicted | falsification |
|---|---|---|
| H3 | Conditional-success P(positive program net-present-value at zero discount), bracketed by my point-estimate calc and demand-curve fleet calc, is in [10%, 50%] | falsified if either anchor is outside |

### H4 — full conjunction × conditional-success P(positive net-present-value)

Multiply full conjunction posterior (round 9, H2a uniform-prior, 0.167%) by conditional-success P(positive net-present-value at zero discount) bracket from H3 [17%, 47%]:

- Lower bound: 0.167% × 17% = **0.028%**
- Upper bound: 0.167% × 47% = **0.078%**

**Three orders of magnitude smaller than the conditional-success-only number.** The conjunction multiplier dominates.

| | predicted | falsification |
|---|---|---|
| H4 | Full-chain P(positive program net-present-value, including reactor program success + engineering closures + clearing-price tail) at H2a min-point is in [0.02%, 0.10%]; central 0.05% | falsified if outside |

### H5 — three decision frames

Three frames produce three distinct verdicts on the H2a minimum-point at conservative anchors (8 W/kg specific power, 10-year lifetime, no aerocapture, 500 kWe reactor, 200-tonne chunk, 3 launches per mission):

- **Frame A (full chain, return-seeking expected-value):** P(positive net-present-value) ≈ 0.05%. **Ruled out.** Same answer as round-9 H6 and round-10 H7.
- **Frame B (conditional on reactor + engineering success, price-tail-integrated):** P(positive net-present-value at zero discount) ≈ 17–47%. **Viable in principle.** This is the decision frame for venture-class capital evaluating ICEBERG conditional on technical closure.
- **Frame C (conditional-success at point-estimate clearing price):** net-present-value -$22 billion at zero discount. **Ruled out at point estimate.** Round-10 H1's framing. Ignores price distribution tail.

Frames A and C agree on "ruled out"; Frame B disagrees. The disagreement is methodologically meaningful: Frame B is the right framing if a decision-maker is willing to underwrite reactor and engineering risk and evaluate the residual market-price risk separately.

| | predicted | falsification |
|---|---|---|
| H5 | Three decision frames give three distinct verdicts on H2a min-point; only Frame B is "viable in principle" at non-trivial probability (≥ 15%) | falsified if Frame B P(positive net-present-value) < 10% or if it agrees with Frame A/C |

### H6 — matrix axis 17 amendment

Round 9 H6 said "technology-demonstrator-only." Round 10 H5 refined to "two-track framing: return-seeking ruled out + sovereign-grant viable." This round refines further to **three decision frames**, of which Frame B is the load-bearing finding for venture-class capital pitching.

**The matrix's "venture-class framing retired" decision (axis 17, latest+5 pitch rewrite) was anchored on Frame A reasoning** (conjunction-weighted expected NPV). Under Frame B, venture-class is not structurally ruled out — it is conditional on reactor + engineering closure with 17–47% P(NPV>0) at zero discount. **The matrix's pitch rewrite that retired venture-class framing may have been over-broad.** Venture-class capital does not P-weight by reactor success; that's the sovereign-grant's job. Venture-class capital evaluates the conditional, with appropriate discount for technical risk built into the WACC.

| | predicted | falsification |
|---|---|---|
| H6 | Matrix axis 17 should be amended to acknowledge Frame B; venture-class is NOT structurally ruled out at conditional-success + price-tail-integrated framing | falsified if Frame B's P(positive NPV) at any realistic venture WACC (≥ 12%) is below 5% |

---

## Method (run.py)

1. Load R-LEO-water-demand-curve `demand_curve_summary.json` clearing-price percentiles.
2. Fit log-normal (mu_log10, sigma_log10) from p05/p50/p95.
3. Compute P(clearing price ≥ break-even) for break-even values $8.17, $13.7, $22.4, $36.7, $60.2 million per tonne (the round-10 break-even ladder across launch counts × ship reuse).
4. Read R-LEO-water-demand-curve `p_npv_positive_summary` for E_500kWe_200t at multiple WACCs.
5. Multiply by round-9 H2a uniform-prior conjunction posterior (0.167%) to get full-chain P(positive net-present-value).
6. Tabulate three decision frames.
7. Grade H1-H6.

Output: `results/three_frames.json`, `results/three_frames_table.csv`, `results/findings.md`.

---

## Validity caveats

1. **Log-normal fit is approximate.** Computed from p05/p50/p95 only; doesn't capture tail-heaviness if demand curve is heavier-than-log-normal in the tail. Validate against p25/p75 internal consistency.
2. **Demand-curve `E_500kWe_200t` uses architecture-E economics** that were partially falsified by enceladus-r5 R-arch-E-specific-power-flown-anchored. The architecture-E surviving cell at conservative anchors is the same (sp=8, 500 kWe, 200 t chunk) so the economics map; specific-power conditional is the falsification axis.
3. **Frame B "conditional on reactor + engineering success" is the load-bearing claim.** This framing assumes the decision-maker is willing to underwrite reactor + engineering risk separately from market risk. Real venture capital does not strictly underwrite reactor risk for free — it discounts by some technical-risk factor. The Frame B probabilities are upper bounds; true venture-class P(NPV>0) is somewhere between Frame A and Frame B.
4. **My round-10 break-even ($22 million per tonne) is point-estimate; demand-curve break-even varies with assumptions** (learning-rate, fleet size, depreciation schedule). Demand curve's 47% P(NPV>0) at zero discount may anchor on different break-even assumptions than my $22 million per tonne. The 17%-vs-47% gap is therefore partly due to assumption mismatch, not just my fleet-scale-revenue under-counting.
5. **Frame B's matrix-amendment recommendation (re-open venture-class framing)** is a meaningful claim. Project owner should weigh: does R-heterogeneous-cadence's staged-commitment finding interact with Frame B? Staged go/no-go gates A-C could be the mechanism by which venture capital underwrites reactor + engineering risk separately from market risk.
