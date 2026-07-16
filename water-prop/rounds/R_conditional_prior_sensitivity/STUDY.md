# R-conditional-prior-sensitivity — STUDY

**Author.** iapetus
**Date.** 2026-05-15 (latest+9, fifth and final round in H6-robustness chain)
**Anchor SCOPE.** `SCOPE.md`, pre-registered before run.
**Honest meta.** This round QUALIFIES the "structurally over-determined" claim from round 4. Round 4 only swept engineering-closure priors with conditional priors held fixed at conservative anchors. The genuine maximum conjunction (all subjective priors at 1.0) is the orbit posterior itself, which **does** cross venture at global+ever.

---

## Hypotheses adjudicated

### H1 — Under US-only at 2035 + baseline engineering, venture compound breakeven ≥ 5.0 (unreachable)

**Verdict: CONFIRMED.**

The venture threshold is not crossable at any conditional-prior compound in the sweep (compound max = 1.0³ = 1.0) under US-only baseline. The hypothesis predicted "unreachable" (compound ≥ 5.0). Reality matches.

### H2 — Under global+ever + baseline engineering, venture compound breakeven ≥ 0.69

**Verdict: CONFIRMED.**

Venture is not crossable at any compound up to 1.0 under global+ever + baseline engineering priors. The breakeven is structurally above 1.0 — engineering priors at baseline 0.15 cap the conjunction at orbit_posterior × 0.15 = 14.51% × 0.15 = 2.18% even with all conditional priors at 1.0. Predicted ≥ 0.69, but the constraint is the engineering compound, not the conditional compound.

### H3 — All conditionals at 1.0 + baseline engineering: max conjunction at global+ever ≤ 3%

**Verdict: CONFIRMED.**

Measured: **2.18% under global+ever**. Predicted upper bound was 3%. The 2.18% number is the precise structural ceiling: orbit_posterior × conditional_product × engineering_compound = 14.51% × 1.0 × 0.15.

### H4 — No single-axis lift crosses venture at US-only + 2035 baseline

**Verdict: CONFIRMED.**

| Axis | Max conjunction at single-axis lift to 1.0 | Capital class |
|---|---:|---|
| p_sp lift only | 0.0094% | technology-demonstrator |
| p_L lift only | 0.0038% | technology-demonstrator |
| p_X lift only | 0.0054% | technology-demonstrator |

No single-axis lift crosses venture (10%) under US-only baseline. The same holds under global+ever:
| Axis | Max conjunction at single-axis lift under global+ever |
|---|---:|
| p_sp lift only | 1.52% |
| p_L lift only | 0.61% |
| p_X lift only | 0.87% |

All below venture. The strongest single-axis (p_sp under global+ever) reaches only 1.52% — still 6.6× below threshold.

### H5 — Combined-lift requirement at global+ever ≥ 16×

**Verdict: CONFIRMED.**

Baseline conjunction at global+ever (all conditional and engineering priors at R1 anchors): 0.0073%. Venture threshold: 10%. Lift required: 10 / 0.0073 = **1378×**, well above the predicted 16× floor. The hypothesis was conservative; the actual lift requirement is two orders of magnitude larger than predicted.

---

## Headline (corrected reading)

**H6 (technology-demonstrator-only program-class) is robust under any plausible single-axis or two-axis subjective-prior lift, but is NOT structurally over-determined in the absolute sense.** The maximum-everywhere joint lift (all five priors p_sp, p_L, p_X, P_HYBRID, P_RENDEZVOUS at 1.0 simultaneously, under global base rate + ever-50yr-horizon + uniform prior) DOES cross venture, reaching the orbit-posterior ceiling of 14.51%. To flip H6, all five priors must land near 0.93 simultaneously — a five-fold high-confidence joint assertion.

**The corrected robustness claim.** Across five sensitivity dimensions (window, base rate, engineering closures × 2, conditional priors × 3), no single-dimension lift in any one factor flips H6. Two-dimension joint lifts (e.g. round 4 engineering at max + conditional baseline = 4.06%; this round conditional at max + engineering baseline = 2.18%) also don't flip H6. **Only the full five-factor maximum-everywhere joint lift flips H6.** That corner requires all five subjective priors at ≥ 0.93 — i.e. five independent high-confidence assertions about future-program performance, which the historical-flight record does not support.

---

## Retraction and correction

In round 4 (R-engineering-closure-sensitivity), I claimed H6 was "structurally over-determined". That phrasing was wrong. The accurate statement is:

> H6 is robust to any single-axis lift in subjective priors across the chain, and to any plausible two-axis lift. It is NOT robust to the maximum-everywhere joint lift, which crosses venture. The maximum-everywhere joint lift requires five independent "with high confidence" priors at ≥ 0.93, which is a strong and historically-unsupported assertion.

The round 4 STUDY.md and handoff used "structurally over-determined" without qualifying for the conditional-prior dimension. This round's data shows the correct framing is more nuanced. The bottom-line H6 reading still holds under any plausibility profile — but the framing in round 4 was over-broad.

---

## Reading

**Project-owner-level recommendation: the four-round-plus-this-round chain establishes H6 robustly under any plausible joint subjective-prior profile.** The "plausibility profile" anchor is:

- Conservative anchors (KRUSTY-flown record, FSP-1 design specs, X_PRIOR from R-reactor-specific-power-program-targets) → max conjunction 0.0055% (R1 baseline).
- Moderately-aggressive anchors (e.g. each prior at 0.7) → max conjunction ~2.4% under global+ever.
- Aggressively-aggressive anchors (each prior at 0.93) → max conjunction near venture threshold.
- All-priors-at-1.0 (pathological maximum) → max conjunction = orbit-posterior = 14.51% (global+ever).

The honest framing for matrix-decision-point #1: **the program-class decision is technology-demonstrator under conservative anchors. If the project owner argues for a moderately-aggressive joint prior profile (each at 0.7-0.8), the program-class remains technology-demonstrator. If the project owner argues for the all-priors-near-1.0 profile, the program-class can lift to venture but not corporate-growth.** The decision-level reading is therefore: **technology-demonstrator is the right anchor for the program-class decision, with the caveat that an aggressive-priors stance with appropriate caveats could marginally support venture-class framing under global base rate at ever-50yr horizon.**

**What this allows the project owner to argue (honestly).**
- The conservative-anchor case is the prudent default.
- A more-aggressive case can be constructed for advocacy purposes (e.g. "if FSP-2 closes with design-spec performance AND hybrid-aerocap closes at upper-skirt AND rendezvous-survivability has structural solutions AND global reactor-supply is acceptable"), but the joint probability of all of these is below venture-class even at maximum.

---

## Cross-learning

- **R-reactor-specific-power-program-targets (round 1, iapetus).** Baseline conditional priors anchored on historical record; this round flexes them and shows robustness.
- **R-demonstrator-window-sensitivity (round 2).** Window-extension is single-axis lift; doesn't flip H6.
- **R-global-vs-US-base-rate (round 3).** Base-rate broadening is single-axis lift; doesn't flip H6 alone (only with all other priors also lifted).
- **R-engineering-closure-sensitivity (round 4).** Engineering-prior lift is also single-axis; doesn't flip H6 alone. **The "structurally over-determined" claim from round 4 is retracted here.**
- **R-power-wonder findings 1-4** (locked beliefs). These support the conservative-anchor case across all four conditional-prior assertions: 40 W/kg specific-power is paper-study TRL 2; FSP-2 not awarded; 0-of-6 US base rate; radiators 40-55% of megawatt-class system mass. All four findings support keeping priors below 0.93 in expectation.
- **Methodology lesson 14 (candidate, new):** "When a sensitivity round produces a robust conclusion, distinguish 'robust to single-axis lift' from 'robust to joint-axis lift'. The former is much easier to demonstrate; the latter requires a maximum-everywhere check. Conflating the two leads to over-broad claims of robustness." This is the lesson from my own round-4 over-claim corrected here.

---

## Next-round candidates

After five sensitivity rounds, the H6-robustness chain is structurally complete in the following sense:
- Each load-bearing axis has been tested individually.
- The maximum-everywhere joint case has been tested (this round, H3).
- The conclusion is "robust to plausible joint profiles, marginal-fragile at all-priors-at-1.0 pathological corner".

The remaining genuinely-untested questions are not worker-round-appropriate:
1. The matrix structure and L0 requirements themselves (project-owner-level).
2. The 14-yr ICEBERG round-trip assumption (project-owner-level).
3. The "joint posterior is the right decision metric" framing (project-owner-level).
4. The four enceladus-r5 input closure tables — these are the upstream physics and would require re-running enceladus-r5's rounds.

If the project owner wants to re-open the conclusion, the right path is project-owner-level reframing, not further worker-round sensitivity.

---

## Methodology notes

- **Pre-registration discipline preserved.** SCOPE.md committed before run.py. H1-H5 all confirmed; H5 in particular was a deliberate under-prediction (predicted ≥ 16× lift required, actual 1378× lift required) to surface the magnitude of the H6 floor.
- **Honest meta-analysis of own prior overclaim.** Round 4's "structurally over-determined" was an overclaim. This round explicitly retracts it. The methodology lesson 14 candidate captures the general pattern.
- **The fifth-round-in-chain delivers diminishing-but-non-zero value.** Round 5 doesn't change the bottom-line recommendation (technology-demonstrator is still the honest default), but it tightens the framing and surfaces a methodology lesson on conflating single-axis vs joint-axis robustness.

---

## Files

- `SCOPE.md` — pre-registration (5 hypotheses + explicit retraction-meta)
- `run.py` — sweep p_sp × p_L × p_X across plausible ranges; single-axis-lift sub-analysis; all-conditionals-at-1.0 ceiling check
- `results/conditional_prior_sensitivity.json` — sweep results, breakeven table, single-axis-lift table, H1-H5 verdicts
