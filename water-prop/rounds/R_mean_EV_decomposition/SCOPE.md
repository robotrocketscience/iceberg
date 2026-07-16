# R-mean-EV-decomposition — SCOPE

**Author:** rhea (worker session, iceberg-rhea-2 branch).
**Date:** 2026-05-16 (latest+8, seventh round this sitting; queued from R-staged-commitment-underwriter-anchor priority-1 thread #1).

## Goal

Decompose round 14's load-bearing finding (**mean Δ-NPV = -$10.6 B across the demand-curve MC at 2-launch W3 LR15**) into a per-clearing-price-percentile contribution table. Answer:

1. **Which clearing-price percentile bins drive the negative mean?** Concentrated in upper-tail (p75+), uniform across p50+, or smeared across all clearings?
2. **Where is the sign-inflection?** R14 H7 reported Δ = +$7.67 B at clearing p25, +$3.34 B at p50, –$8.72 B at p75. So the inflection is somewhere in (p50, p75). Locate it more precisely.
3. **Is the loss capturable / truncatable?** If a sovereign-mandated price cap is imposed at some clearing percentile, does mean Δ-NPV flip positive? At what cap level? (Stub for round-14 pending thread #7.)
4. **What does the decomposition say about matrix axis 17?** If the loss is concentrated in upper-tail draws that a public-purpose ICEBERG program would not be permitted to capture anyway (cap, windfall tax, treaty-bound clearing-price ceiling), the "EV story disfavors staged" R14 finding may be a regulatory-counterfactual artifact rather than a load-bearing economic conclusion.

## What this round does

1. **Inherit R14 harness without modification.** Same 10,000 demand-curve clearing draws, same seed 20260515, same 2-launch W3 LR15 cell, same NRE/learning/launch-opex parameters. No re-derivation.
2. **Per-percentile decomposition.** Sort the 10,000 ordered (clearing, Δ-NPV) pairs by clearing price. Bin into deciles (1,000 draws each, 10% probability mass each). For each bin: report mean Δ, median Δ, sign-fraction, mean clearing $/kg. Sum bin-means × 0.10 = grand mean (cross-check vs R14 -$10.6 B).
3. **Finer-grain sign-inflection.** Bin into vigintiles (5% mass each) over p40-p80 to locate the inflection bin where bin-mean Δ crosses zero.
4. **Cap-truncation sweep.** For caps at clearing-p70, p80, p90, p95, p99, ∞ (no cap): recompute mean Δ-NPV with clearing capped at that percentile's value. Identify the cap level at which mean Δ flips sign.
5. **Upper-tail contribution.** Report cumulative-Δ contribution from top-quartile, top-decile, top-5%, top-1% of clearings. Use as the matrix-amendment headline.
6. **Smart-gate interaction check.** Round 14 reports smart-gate abandons 65.3% of draws. Decompose smart-gate abandonment rate by clearing decile — confirm/refute the intuition that smart-gate abandons low-clearing draws (where post-gate fleet is unprofitable) but holds in high-clearing draws (where staged's smart-gate ≈ upfront's mechanical-commitment, so the gap shrinks).

## What this round does NOT do

- Does NOT re-derive trajectory, propulsion, conjunction, reactor-mass, specific-power, or any physical input. All physics inherited.
- Does NOT vary the load-bearing cell (2-launch W3 LR15 chunk-200). A 3-launch or LR=0 sensitivity is queued as a follow-up if the decomposition flips at this cell.
- Does NOT compute regulatory feasibility of a sovereign-mandated price cap. The cap-truncation sweep is a *math sensitivity*, not a policy claim. Whether a cap is achievable in treaty/policy is a separate question.
- Does NOT extend to Option-A (17%-delivered, 34 t/mission) sizing. R14 caveat applies: absolute NPVs scale ~2.4× downward without changing comparative direction; same applies here.
- Does NOT re-evaluate the locked anchor-investor framing. R14 already concluded the framing is downside-protection > NPV-improvement; this round is a forensic on the NPV side specifically.
- Does NOT propose a new Frame (Frame D). Inherits the three Frames (Frame A goal-feasibility; Frame B P(NPV>0); Frame C capital-source-specific metrics from R14).
- Does NOT compute or assume insurance-market pricing for the tail (R-tail-insurance is queued).

## Why now

R14 dissolved the binary-vs-EV dichotomy from R13 by showing both disfavor staged. But "mean Δ = -$10.6 B" is opaque — the matrix should know WHY (which slice of the distribution generates the loss) before adopting the conclusion. Two scenarios change the matrix-axis-17 amendment language differently:

- **Scenario A (concentrated upper-tail):** ≥ 70% of the loss comes from clearings > p75. *Then* the loss is "asymmetric exposure to upside the sovereign-funded program wouldn't capture anyway." Matrix language: "staged commitment dominates ON ANY DOWNSIDE-PROTECTED METRIC; loses on mean EV only because of unrestricted upper-tail revenue capture by the upfront-committed fleet, which a price-capped program would not realize." This is a much weaker indictment of staged.

- **Scenario B (uniform across p50+):** the loss is roughly uniform from p50 upward. *Then* the matrix amendment must say "staged loses on mean EV not just at upper-tail extremes but across the entire upper half of the clearing distribution; the downside-protection argument is bounded to specific gate-failure scenarios only."

R14 left this ambiguous. The matrix is being amended (rounds 9-14 unintegrated); this round's findings affect what the amendment says.

## Methodology lessons inherited (from rounds 9-14)

- **#7-v5 (validated in R14):** Convex-hull check on distribution-aware BOE. *Applied below in §"Convex-hull check on H1."*
- **#11:** Grade SCOPE against primary input data. *Applied below.*
- **#13:** Double-check BOE arithmetic.
- **#14:** Distribution-aware BOE (p25/p50/p75).
- **#15:** Sign-of-Δ at WACC=0 is revenue-dependent.
- **#16 (R14, new):** Scale-invariant ratio metrics produce zero-difference by construction. *Applied: the decomposition metric is an absolute contribution per bin, not a ratio.*

## Primary input grading (per lesson #11)

| Input | Source | Status | Notes |
|---|---|---|---|
| R14 results JSON | `R_staged_commitment_underwriter_anchor/results/underwriter_anchor_summary.json` | exists | confirms -$10.6 B mean Δ; -$8.3 B smart-gate-adjusted |
| R14 run.py | `R_staged_commitment_underwriter_anchor/run.py` | exists | composes R13; will be imported here for the same metric primitives |
| R13 NPV cell / clearing sampler | via R13 run.py reached through R14 | exists | identity-preserving import chain |
| Cap-truncation prior | round 14 pending thread #7 description | exists | not yet a formal study; this round prototypes it |
| Convex-hull check helper | inline; trivial sort + min/max | n/a | implemented in run.py |
| anchor-investor locked framing | locked belief `76fd04cdba8b2c3b` | locked | informs the "what does sovereign-purpose program capture from upper tail?" framing only |

## Convex-hull check on H1 (per lesson #7-v5, SCOPE time)

H1 (predicted below) brackets the upper-quartile cumulative contribution to mean Δ at 60-85% of total. The distribution-integrated quantity is C(top-quartile) = E[Δ | clearing > p75] × 0.25.

Three points across the distribution:
- At clearing p75 alone: Δ = -$8.72 B (R14 H7); bin-contribution to mean = -$8.72 B × 0.05 (one vigintile mass) ≈ -$0.44 B → top-quartile contribution from this slice alone.
- Top-quartile midpoint (p87.5): expected larger negative; R13 reports p95 of clearing → larger fleet revenue → larger Δ in absolute magnitude. Rough scaling: p87.5 clearing ≈ $25k/kg vs p75 $16k/kg → 1.6× scale → Δ ≈ -$14 B.
- Top-quartile endpoint (p99): clearing → $60k/kg per R14 BOE → revenue scale 3.8× p75 → Δ ≈ -$33 B.

Approximate top-quartile mean: average of three rough points ≈ (-8.72 -14 -33) / 3 ≈ -$18.6 B. Top-quartile contribution to mean Δ = -$18.6 B × 0.25 ≈ -$4.65 B. Total mean Δ = -$10.6 B. Top-quartile fraction = 44%.

That's below my H1 floor of 60% — meaning the loss is NOT concentrated in the top quartile alone. Some mass comes from p50-p75 too. Adjusting the H1 bracket accordingly: top-quartile contribution in [35%, 65%] of total mean-Δ loss.

Convex hull of the three rough-quartile-mean-Δ points: [-$33 B, -$8.72 B]. Mean of distribution sits inside hull. Hull check passes for the upper-quartile-only bracket but I'm widening the H1 bracket on the strength of this exercise. *Lesson #7-v5 has already moved my pre-reg before run-time. Good.*

## Pre-registered hypotheses (full text in STUDY.md)

| ID | Predicted | Falsification |
|---|---|---|
| **H1** Top-quartile (p75-p100) clearing draws contribute **[35%, 65%]** of the total negative mean Δ-NPV. | Outside band. |
| **H2** Sign-inflection (bin where mean Δ crosses zero) is between clearing **p55 and p70**. | Outside this percentile range. |
| **H3** \|mean Δ at clearing p95 decile\| / \|mean Δ at clearing p05 decile\| ≥ **3**. Tests left-vs-right tail asymmetry. | Ratio < 3. |
| **H4** Cap at clearing p90 ($25k/kg-ish) flips mean Δ-NPV to **positive** ($0 to +$5 B band). | Mean Δ remains negative, OR > +$5 B. |
| **H5** Smart-gate abandonment rate is **monotone decreasing** in clearing decile: abandonment fraction in bottom decile ≥ abandonment fraction in top decile. | Non-monotone OR no clear top-vs-bottom ordering. |
| **H6** (cross-check) Per-decile mean Δ × 0.10 summed across 10 deciles equals R14 grand mean within ±5%. | Sum mismatches R14 by > 5%. |
| **H7** (load-bearing reframe) IF H1 + H4 both HOLD, the matrix axis-17 amendment language should foreground the upper-tail-capture distinction. IF H1 HOLDS but H4 FALSIFIES, the language should remain "staged loses on EV under unrestricted distribution." | H7 is a routing rule, not a numeric prediction; recorded for completeness. |

## Cross-checks (must pass before grading)

| ID | Check | Tolerance |
|---|---|---|
| XC-1 | R14 grand-mean replication: per-decile sum reproduces -$10.6 B | ±$0.5 B (5%) |
| XC-2 | R14 H7 reproduces at clearing p25, p50, p75 within ±5% per-point | ±5% |
| XC-3 | Top-quartile (p75-p100) total contribution = sum of vigintile 16-20 contributions | exact |
| XC-4 | Cap at clearing p99 (one-bin truncation) is more positive than cap at clearing p70 | qualitative monotone |
| XC-5 | Smart-gate abandonment frac per decile sums to R14's 65.3% within ±1% | ±1 pp |

## Estimated runtime

Under 30 seconds. No new physics; one extra MC pass with per-draw bookkeeping and a 5-cap sensitivity sweep.

## Files produced

- `STUDY.md` — full pre-registration with BOE for each H.
- `run.py` — extends R14 with per-decile decomposition + cap sweep + smart-gate stratification.
- `results/mean_ev_decomposition_summary.json` — outputs.
- One commit on iceberg-rhea-2 with `exp:` prefix.
- One handoff entry under `~/.claude/handoffs/iceberg-rhea-20260516-mean-ev-decomposition.md`.
- State refresh in `.session/STATE.md` (gitignored; not committed).

No shared-doc edits (REQUIREMENTS, matrix, design-axes, pitch, SESSION-LOG, RUNNING_DOC, .planning/active-sessions.md). Orchestrator integrates.
