# R-engineering-closure-sensitivity — what engineering-closure compound is required to flip H6?

**Status.** Pre-registration. Authored by iapetus, 2026-05-15 (latest+9, after R-global-vs-US-base-rate).

**Why.** The three prior iapetus rounds all used placeholder engineering-closure priors:
- P_HYBRID_AEROCAP = 0.50 (R-hybrid-aerocapture-aerobraking SCOPE-pending; reasonable middle estimate)
- P_RENDEZVOUS_LOW = 0.20 / P_RENDEZVOUS_HI = 0.30 (R-bring-rendezvous-survivability — pessimistic given known mitigation limitations per SCOPE.md)

These have been held fixed across all sensitivity rounds. They are my own subjective anchors, not derived from the engineering rounds themselves (which have not been run). This round questions them: **what engineering-closure-prior compound (P_HYBRID × P_RENDEZVOUS) is required for the max conjunction posterior to cross the venture (10%) threshold?**

If the breakeven compound is plausible (e.g. ≤ 0.5 × 0.5 = 0.25), then H6 is fragile to better engineering closures. If the breakeven compound is implausible (≥ 0.8 × 0.8 = 0.64), then H6 is robust. The answer informs the project owner's expected-value-of-information calculation for running the engineering rounds.

**Approach.** Sweep (P_HYBRID, P_RENDEZVOUS) over plausible ranges. At each (P_HYBRID, P_RENDEZVOUS, window, base-rate) combination, compute max conjunction over the min-corner table and check whether it crosses venture / corp-growth / regulated-utility thresholds. Produce a 2D heatmap-equivalent: for each base-rate × window pair, the breakeven curve in (P_HYBRID, P_RENDEZVOUS) space.

**The other conditionals** (specific-power, lifetime, aerocapture-credit conditionals) are held fixed at R-reactor-specific-power-program-targets values. This round only varies engineering-closure priors. A separate round would be required to sweep all four conditional priors jointly.

---

## Pre-registered hypotheses

| # | Hypothesis | Predicted | Falsification |
|---|---|---|---|
| H1 | Under the prior-round US-only base rate at 2032-2035 window, the engineering-closure compound (P_HYBRID × P_RENDEZVOUS) required to cross venture (10%) threshold is ≥ 0.95 — effectively unreachable. | breakeven compound ≥ 0.95 | H1 falsified if breakeven < 0.80 |
| H2 | Under global base rate + ever-50yr horizon (the most-favorable case from R-global-vs-US-base-rate), the engineering-closure compound required to cross venture is ≥ 0.3. Plausibility: each engineering prior at ~0.55 (yielding compound 0.30) is achievable in principle. | breakeven compound at global+ever ≥ 0.30 | H2 falsified if breakeven < 0.15 |
| H3 | Under global base rate + ever-50yr horizon, the engineering-closure compound required to cross corporate-growth (30%) threshold is ≥ 1.0 — i.e. unreachable even at perfect engineering closure. | breakeven for corp-growth = unreachable | H3 falsified if any compound ≤ 1.0 crosses corp-growth at global+ever |
| H4 | At the X=0 corner (no aerocapture credit, lifetime=10 yr, sp=8 W/kg), only P_RENDEZVOUS matters (P_HYBRID is not in the chain). The breakeven P_RENDEZVOUS for venture at global+ever-uniform = 1.0 (unreachable, because the X=0 corner has weaker conditional probability than aerocapture-credit corners). | X=0 venture-breakeven P_RENDEZVOUS = unreachable | H4 falsified if X=0 corner reaches venture at any P_RENDEZVOUS < 1.0 |
| H5 | The base-rate-broadening from R-global-vs-US-base-rate (round 3) had ~10× lift on conjunction. Engineering-closure-prior lift is bounded by P_HYBRID × P_RENDEZVOUS_HI normalization: max lift from prior round's (0.5 × 0.3 = 0.15) to maximum (1.0 × 1.0 = 1.0) is 6.67×. So engineering-closure-prior is a LESS-load-bearing sensitivity than base-rate-broadening. | engineering-prior max lift < base-rate-broadening lift (~10×) | H5 falsified if engineering-prior lift exceeds 10× anywhere |

---

## Method sketch

1. **Sweep P_HYBRID** across [0.10, 0.30, 0.50, 0.70, 0.90, 1.00].
2. **Sweep P_RENDEZVOUS** across [0.10, 0.20, 0.30, 0.50, 0.70, 0.90, 1.00].
3. **At each (P_HYBRID, P_RENDEZVOUS, base-rate-model, window-year)** combination, re-compute max conjunction posterior over the min-corner table from R-reactor-specific-power-program-targets.
4. **Two base-rate models** swept: US-only (from R-reactor-specific-power-program-targets baseline) and global (from R-global-vs-US-base-rate, scope-conditional=0.40).
5. **Window years swept**: 2035 (baseline), 2045 (decadal extension), 2055 (mid-extension), ever-50yr.
6. **For each (base-rate, window) pair**, find the breakeven curve in (P_HYBRID, P_RENDEZVOUS) at each capital-class threshold: venture (10%), corp-growth (30%), regulated-utility (50%).
7. **Plausibility check**: what (P_HYBRID, P_RENDEZVOUS) values are physically plausible for an engineering closure? Aerocapture flight heritage suggests P_HYBRID ≤ 0.8 even for a charitable closure (no hybrid-aerocap mission has flown). P_RENDEZVOUS bounded by the 99-percent-per-pass impact probability finding from titan's prior rounds — suggesting P_RENDEZVOUS ≤ 0.5 even with all credible mitigations.

---

## Method caveats

- The engineering-closure-prior is in the chain BEFORE the per-mission delivered-mass closure. So even if engineering rounds close with prior 1.0, the per-mission economics still need to clear the IRR threshold (a separate decision from program-class). The two decisions are linked but distinct.
- Specific-power × lifetime independence assumption is still held. If anti-correlated (per MARVL radiator-area argument), conjunction is overestimated. This round does not test that.
- Subjective specific-power and lifetime conditional priors are held fixed. A "compounding all the way" round (engineering-priors AND specific-power AND lifetime priors all aggressive) would be the maximally-aggressive variant; this round is one-axis (engineering-priors only).

---

## Reading template

- **Hypotheses adjudicated.** H1-H5 verdicts.
- **Headline.** What engineering-closure compound is required to flip H6 at each (base-rate, window) combination?
- **Reading.** Recommendation: if the breakevens are plausible (compound ≤ 0.5), running the engineering rounds becomes high-value-of-information. If implausible (compound ≥ 0.7), H6 is essentially over-determined by engineering-closure ceilings and the engineering rounds are research-grade-only.
- **Cross-learning.** Connection to R-bring-rendezvous-survivability SCOPE.md (does the SCOPE's own assessment match my prior?); connection to R-hybrid-aerocapture-aerobraking (open SCOPE; the prior here is essentially uninformed).
- **Next-round candidates.** If H1/H2 hold (engineering-prior breakeven implausible), the four-round chain is the load-bearing answer and no further sensitivity is informative. If H1/H2 fail, the engineering rounds become the load-bearing path.

---

## Worker assignment

- **Round priority:** medium-high. Final sensitivity round in the H6-robustness chain. After this, if H6 holds, the conclusion is over-determined.
- **Worker fit:** iapetus (this session) — synthesis machinery already loaded.
- **Inputs:** `R_reactor_specific_power_program_targets/results/reactor_program_targets.json` (min-corner table, subjective priors); `R_global_vs_us_base_rate/results/global_vs_us_base_rate.json` (global base-rate-conditional p_500_by_year).
- **Out-of-scope:** anti-correlation between sp and L; engineering-prior anchored on actual hybrid-aerocap or rendezvous-survivability physics (those are the engineering rounds themselves).
