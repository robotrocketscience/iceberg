# R-conditional-prior-sensitivity — flexing the load-bearing subjective priors

**Status.** Pre-registration. Authored by iapetus, 2026-05-15 (latest+9, fifth round in H6-robustness chain).

**Why this round retracts a claim from round 4.** Round 4 (R-engineering-closure-sensitivity) concluded H6 was "structurally over-determined" — even at perfect engineering closures, max conjunction caps at 4.06% under global+ever+uniform. **That claim was conditional on my subjective conditional-prior anchors being correct** (p_sp at sp=5 W/kg = 0.40; p_X at X=10 km/s = 0.70; p_L at L=∞ = 1.0). I held those priors fixed across all four sensitivity rounds. They were never tested.

**The honest framing.** Max conjunction = orbit_posterior × p_sp × p_L × p_X × P_HYBRID × P_RENDEZVOUS. Round 4 swept the last two factors. This round sweeps the first three. The absolute upper bound on conjunction is orbit_posterior itself (when all conditional and engineering priors are 1.0). Under global+ever+uniform: orbit_posterior = 14.51%. That **already crosses venture (10%)** — without any engineering-closure or conditional-prior conservatism, the ceiling is above venture.

So the question is not "is H6 absolutely robust?" but **"what conditional-prior compound is required to flip H6, and is that compound plausible given the historical reactor-flight record?"**.

**What this round answers.**
1. The conditional-prior compound (p_sp × p_L × p_X) breakeven for venture (10%), corp-growth (30%), regulated-utility (50%) at each (base-rate, window, engineering-prior) combination.
2. Whether the breakeven point is plausible given (a) the KRUSTY-anchored flown specific-power record, (b) the FSP-1 design-target band, (c) the X_PRIOR distribution from R-reactor-specific-power-program-targets.
3. The minimum single-axis lift required (lift only p_sp, only p_L, only p_X) to cross threshold.

---

## Pre-registered hypotheses

| # | Hypothesis | Predicted | Falsification |
|---|---|---|---|
| H1 | Under US-only baseline at 2032-2035 + baseline engineering priors (0.5, 0.3), the conditional-prior compound (p_sp × p_L × p_X) required to cross venture is ≥ 5.0 — physically unreachable (compound max 1.0 × 1.0 × 1.0 = 1.0). | breakeven compound ≥ 5.0 (unreachable) | H1 falsified if breakeven ≤ 1.0 (i.e. reachable in physical sweep range) |
| H2 | Under global+ever + baseline engineering priors, the conditional-prior compound to cross venture is ≥ 0.69. Plausibility: each conditional at ~0.90 (compound 0.73) is at the upper end of plausible defenses; each at ~0.95 (compound 0.86) requires asserting historical anchors are not representative. | breakeven compound ≥ 0.69 at global+ever | H2 falsified if breakeven < 0.50 |
| H3 | With ALL conditional priors at 1.0 (degenerate) AND baseline engineering priors (0.5, 0.3), max conjunction under global+ever-uniform = 14.51% × 1.0 × 0.5 × 0.3 ≈ 2.18%. Still below venture. | max conjunction at conditional=1.0, engineering=baseline ≤ 3% | H3 falsified if conjunction at maximum-conditional with baseline-engineering > 3% |
| H4 | The single-axis lift required to cross venture under US-only+2032-2035 baseline is unreachable for any single conditional prior. Specifically: lifting p_sp from 0.40 to 1.00 alone does not cross venture (orbit posterior too small); same for p_L from 0.40 to 1.00 alone; same for p_X from 0.70 to 1.00 alone. | no single-axis lift crosses venture at US-only baseline | H4 falsified if any single conditional-prior lift to 1.0 crosses venture |
| H5 | The conditional-prior-compound x engineering-prior-compound combined product needs to be ≥ 0.69 to cross venture at global+ever. The conditional-prior compound at the absolute conservative anchor is 0.28 (per round 4); engineering compound at baseline 0.15. Combined: 0.28 × 0.15 = 0.042. Lift needed: 0.69 / 0.042 ≈ 16×. | combined-lift requirement ≥ 16× to cross venture at global+ever | H5 falsified if combined lift requirement < 8× |

---

## Method sketch

1. **Sweep conditional priors** at the load-bearing corners:
   - p_sp at sp=5 W/kg across [0.40, 0.60, 0.80, 0.95, 1.00].
   - p_L at L=10 yr across [0.40, 0.60, 0.80, 0.95, 1.00]. (L=∞ is degenerate at 1.0.)
   - p_X at X=10 km/s across [0.70, 0.85, 0.95, 1.00]. (X=0 corner is engineering-compound-independent.)
2. **Hold engineering priors fixed** at baseline (P_HYBRID=0.5, P_RENDEZVOUS=0.30). The combined-sensitivity (conditional + engineering compound) is covered as the multiplicative result.
3. **Sweep base-rate × window**: US-only at 2035, US-only at ever; global at 2035, global at ever.
4. **Identify breakeven curves** in (p_sp, p_L, p_X) space at each capital-class threshold.
5. **Plausibility check** for each breakeven point. Anchors:
   - p_sp at sp=5: historical record has no orbited reactor at ≥ 5 W/kg system-level. KRUSTY ground-test 2.4 W/kg. FSP-1 design target 4-5 W/kg system-level (per Lockheed Martin / Westinghouse / IX joint venture proposals). Subjective p_sp ≥ 0.80 at sp=5 requires asserting "FSP-1 design will hit the target", which is contingent on Phase-2 award + flight execution.
   - p_L at L=10: NASA Kilopower design target is 10-15 yr cumulative full-power burn. FSP design same. Subjective p_L ≥ 0.80 at L=10 requires asserting "the design target translates to flight reality", which has no flown reactor anchor at scale.
   - p_X at X=10: X_PRIOR from R-reactor-specific-power-program-targets has p_X[10]=0.70. Lifting to ≥ 0.85 requires asserting hybrid-aerocap is delivering above its conservative-skirt-closure envelope.
6. **Single-axis-lift analysis**: hold two conditional priors at baseline, sweep the third. Find what single-axis lift (if any) crosses venture.

---

## Method caveats

- **Independence assumption.** I treat p_sp, p_L, p_X as independent factors. In reality, programs that hit aggressive specific-power often have shorter lifetime (radiator-area-aging trade per MARVL finding). And aerocapture closure is independent of reactor design. The independence assumption probably overestimates joint plausibility — if anti-correlated, the joint conditional is below the product, making H6 more robust still.
- **The historical-record anchor itself.** KRUSTY ground-test 2.4 W/kg is the only flown system-level data for fission electric power. Treating it as definitive for orbital programs is conservative. If the project owner argues KRUSTY was not optimized for specific-power (true), the prior could plausibly lift. But the lift would be subjective, not data-anchored.
- **L=∞ degenerate case.** When L=∞, p_L=1.0 trivially. The best-corner search will find this case in some configurations; the headline number should track this carefully.

---

## Reading template

- **Hypotheses adjudicated.** H1-H5 verdicts.
- **Headline.** Does the conditional-prior sensitivity flip H6? If so, what compound is required?
- **Reading.** Recommendation: if the conditional-compound breakeven is plausible (e.g. each at 0.80, compound 0.51), then H6 is sensitive to subjective-prior choices and the matrix-decision-point #1 framing should be qualified accordingly. If the breakeven is implausible (e.g. each at ≥ 0.95), then H6 is robust under any plausible subjective-prior anchor.
- **Cross-learning.** Connection to R-power-wonder locked-belief findings 1-4 (which support conservative anchors). Connection to R-reactor-roadmap (which has reactor-program design-spec cumulative-distribution-functions).
- **Next-round candidates.** If H6 inverts under plausible conditional-prior anchors, the program-class decision becomes subjective-prior-dependent and the chain's load-bearing conclusion is qualified. If H6 holds, this is the fifth and final sensitivity in the chain.

---

## Honest meta-note on this round

This round **retracts and qualifies** my round 4 "structurally over-determined" claim. The qualification is: H6 is over-determined HOLDING the conditional priors at the conservative R1 anchors. Without that holding, the absolute conjunction ceiling is the orbit posterior itself, which under global+ever+uniform is 14.51% — already above venture.

The robust claim is therefore: H6 is over-determined under the conjunction of (a) conservative US-only base rate anchors AND (b) subjective conditional priors anchored on KRUSTY-flown-record + FSP-1-design-spec. Both anchors are defensible; neither is data-proven for orbital programs in the demonstrator window.

The honest framing for the project-owner integration: **the technology-demonstrator-only conclusion is robust under conservative anchors; if a project-owner argues the conservative anchors are wrong, the conclusion is parameter-sensitive.** Which is the right framing to surface for any reading-level decision.

---

## Worker assignment

- **Round priority:** high. Final sensitivity in the H6-robustness chain; this is the genuinely-untested load-bearing assumption.
- **Worker fit:** iapetus (this session) — synthesis machinery already loaded; honest accounting of own-prior-claims is appropriate self-review.
- **Inputs:** all four prior iapetus rounds (especially conditional priors from R-reactor-specific-power-program-targets and orbit posteriors from R-demonstrator-window-sensitivity + R-global-vs-US-base-rate).
- **Out-of-scope:** sp×L correlation (independent-product assumption preserved); deeper-than-flown-record arguments on specific-power achievability (subjective by design).
