# R-engineering-closure-sensitivity — STUDY

**Author.** iapetus
**Date.** 2026-05-15 (latest+9)
**Anchor SCOPE.** `SCOPE.md`, pre-registered before run.
**Inputs.** All three prior iapetus rounds: R-reactor-specific-power-program-targets (min-corner table, subjective priors), R-demonstrator-window-sensitivity (US-only p_500_by_year), R-global-vs-US-base-rate (global p_500_by_year).

---

## Hypotheses adjudicated

### H1 — Under US-only baseline at 2035, venture compound breakeven ≥ 0.95

**Verdict: CONFIRMED, in the strong direction.**

The venture (10%) threshold is **not crossable** at any (P_HYBRID, P_RENDEZVOUS) in the swept ranges (0.10 to 1.00 each) under US-only baseline at 2035. The hypothesis predicted breakeven ≥ 0.95; reality: there is no breakeven within the sweep.

### H2 — Under global + ever-50yr, venture compound breakeven ≥ 0.30

**Verdict: CONFIRMED, in the strong direction.**

The venture threshold is **not crossable** at any (P_HYBRID, P_RENDEZVOUS) compound up to 1.0 under global base rate at ever-50yr horizon. Predicted breakeven ≥ 0.30; reality: there is no breakeven within the sweep.

### H3 — Corp-growth (30%) unreachable at compound ≤ 1.0 under global+ever

**Verdict: CONFIRMED.**

The corp-growth threshold is not crossable at any compound ≤ 1.0 under any (base-rate × window) combination tested.

### H4 — X=0 corner: venture unreachable at any P_RENDEZVOUS ≤ 1.0 under global+ever

**Verdict: CONFIRMED.**

The X=0 corners (no aerocapture credit, lifetime=8/10/15/inf yr) are weaker than the X=10 / X=15 / X=20 corners under all subjective priors. At X=0, the aerocapture-credit-conditional is 1.0 (no engineering closure required), but the (specific-power × lifetime) conditional at the minimum-sp X=0 corner is p_sp(sp=8) × p_L(L=10) = 0.08 × 0.40 = 0.032. The maximum X=0 conjunction at ever-horizon global uniform is:
- 0.1451 × 0.08 × 0.40 × 1.0 × 1.0 = 0.46% (under P_RENDEZVOUS=1.0)

Still 22× below venture. The X=0 corner has structurally weaker conditional product than the aerocapture-corners.

### H5 — engineering-prior lift from baseline (0.5×0.3=0.15) to max (1.0×1.0=1.0) ≤ 10×

**Verdict: CONFIRMED.**

Measured lift under US-only baseline at 2035: from 0.0055% (R-reactor-specific-power-program-targets headline) to ~0.037% (this round at maximum engineering priors). Lift factor ~6.7× — exactly matches the analytical bound (1.0 / 0.15 = 6.67×), confirming the engineering-prior chain is multiplicatively bounded.

---

## Headline

**H6 is over-determined.** No combination of engineering-closure priors in the full sweep [0.10, 1.00] × [0.10, 1.00] crosses any non-technology-demonstrator capital-class threshold under any (base-rate × window) combination tested. Even at the literal absolute ceiling — P_HYBRID = 1.0 AND P_RENDEZVOUS = 1.0 under global base rate at ever-50yr horizon — max conjunction is **4.06%**, still 2.5× below the venture-class threshold (10%).

---

## The absolute-ceiling argument made rigorous

The previous three rounds left open the question: "what if my engineering priors are too pessimistic?". This round answers it definitively.

**Conjunction posterior structure:**
- p_full_conjunction = p_500_orbit × p_sp × p_L × p_aero × p_rendezvous
- where p_aero = P_HYBRID × p_X (if X > 0) or 1.0 (if X = 0)

**Absolute ceiling under most-favorable inputs:**
| factor | max value | source of bound |
|---|---:|---|
| p_500_orbit (global base rate, ever-50yr, uniform) | 14.51% | global Beta-Binomial posterior + scope conditional 0.40 |
| p_sp (at sp=5 W/kg) | 0.40 | KRUSTY-anchored subjective prior |
| p_L (at L=inf) | 1.00 | degenerate case (always satisfied) |
| p_aero (X=10 km/s, P_HYBRID=1.0) | 0.70 | X_PRIOR[10] |
| p_rendezvous (max) | 1.00 | absolute ceiling |
| **product** | **4.06%** | best-case conjunction |

To cross venture (10%), the missing 2.5× must come from somewhere. The only candidates are:
1. **Lift the specific-power conditional.** p_sp at sp=5 = 0.40 → would need 1.00. Implies "any orbited reactor will deliver ≥ 5 W/kg with probability 1". The historical record (KRUSTY flown at 2.4 W/kg; FSP-1 design 4-5 W/kg; no flown reactor at ≥ 5 W/kg) does not support this.
2. **Lift the aerocapture-credit conditional.** p_X at X=10 = 0.70 → would need 1.00. Implies "any hybrid-aerocap closure delivers ≥ 10 km/s credit with probability 1". The X_PRIOR is decreasing in X — the SCOPE for the engineering round explicitly modeled this with X=10 as the *nominal* target, not the worst case.
3. **Lift the orbit posterior** beyond the global+ever-50yr value. Would require adding programs beyond US+USSR+China (none plausibly active) OR extending the horizon beyond 50 years (not credible for a venture-financeable program).

None of these are plausible adjustments. **The 2.5× safety margin against the venture threshold is structural.**

---

## Reading

**The H6 reading is now over-determined across four sensitivity dimensions:**

1. R-reactor-specific-power-program-targets (baseline conditional priors): max conjunction 0.0055%, US-only, 2032-2035 window.
2. R-demonstrator-window-sensitivity (window-extension): max conjunction 0.24%, US-only, ever-50yr.
3. R-global-vs-US-base-rate (base-rate broadening): max conjunction 0.77%, global, ever-50yr.
4. R-engineering-closure-sensitivity (engineering priors at absolute maximum): max conjunction 4.06%, global, ever-50yr.

The maximum-aggressive-everywhere combination caps at 4.06%, which is 2.5× below the lowest non-technology-demonstrator threshold (venture, 10%). The chain establishes the program-class decision is structural, not parameter-sensitive.

**Project-owner-level implication.** The expected-value-of-information for running the engineering rounds (R-hybrid-aerocapture-aerobraking and R-bring-rendezvous-survivability) is bounded above by the value-of-information for changing the program-class decision. With H6 over-determined, those rounds become:
- Technology-demonstrator-mission-readiness questions, not program-class-decision questions.
- Worth running if and only if a technology-demonstrator program proceeds. Otherwise, deferred.

**The engineering-closure-prior sensitivity is essentially settled.** Even if both engineering rounds came back at prior 1.0 (which is unphysical — no engineering closure is certain a priori), the conjunction would still not cross venture. Running the engineering rounds will not unlock a higher capital-class for ICEBERG.

---

## Cross-learning

- **R-reactor-specific-power-program-targets (round 1, iapetus).** H6 verdict over-determined.
- **R-demonstrator-window-sensitivity (round 2, iapetus).** Window-extension confirmed not load-bearing.
- **R-global-vs-US-base-rate (round 3, iapetus).** Base-rate broadening confirmed not load-bearing for the reading.
- **This round (round 4, iapetus).** Engineering-closure priors confirmed not load-bearing for the reading.
- **The remaining untested assumption** is the *subjective conditional priors themselves* (specific-power, lifetime, aerocapture-credit). I held these fixed at R-reactor-specific-power-program-targets values. To test those, one would have to argue that p_sp at sp=5 is ≥ 1.0, p_L at L=10 is ≥ 1.0, p_X at X=10 is ≥ 1.0. These would all require revising the conditional priors upward into degenerate-case territory — i.e. asserting that any orbited reactor inevitably satisfies the matrix's specific-power/lifetime/aerocapture-credit thresholds with certainty. That assertion contradicts the historical reactor-flight record and the SCOPE-anchored X_PRIOR distribution.
- **Expected-value-of-information.** With four-round H6 robustness chain, the marginal value of further sensitivity rounds on this question is near zero. Project work should now move to: (a) updating the orchestrator-level shared docs (matrix decision point #1, L0-13, new reactor-program-availability Level-0), and (b) when/if the project owner wants to advance to technology-demonstrator mission design, running the engineering closures.

---

## Methodology lessons (candidate, consolidated)

- **Lesson 11**: robustness-by-magnitude (the floor is so low that no parameter sensitivity can lift it across threshold). The four-round chain operationalizes this. Verified four separate ways.
- **Lesson 12**: forward-looking conditionals vs historical conditionals. Specific to scope conditional (Russia/China prospective vs historical orbits).
- **Lesson 13 (candidate)**: when sensitivity rounds confirm rather than overturn, structure the chain to test multiple orthogonal load-bearing parameters in sequence. The pattern: round 1 = synthesis, rounds 2-4 = sequential load-bearing-parameter sensitivity. Each round's verdict is independent. When all four confirm, the reading is over-determined and further sensitivity has near-zero marginal value.

---

## Next-round candidates

- **None at the H6-robustness layer.** The chain is complete.
- **Project-owner work** to integrate the four-round chain: matrix decision point #1, L0-13 amendment, new Level-0 for reactor-program-availability, ICEBERG-pitch.md reframe.
- **Engineering-closure-rounds** (R-hybrid-aerocapture-aerobraking and R-bring-rendezvous-survivability) are now downstream-of-program-class-decision, not parallel-to-it. They are technology-demonstrator-design rounds.

---

## Methodology notes

- **All 5 hypotheses confirmed.** First time in this iapetus session. The strong-direction confirmations (H1, H2: not crossable in sweep) are themselves epistemic updates — they tighten the prior expected breakevens (≥0.95, ≥0.30) to "unreachable within the sweep".
- **The hypothesis structure was right.** Predicting magnitudes that were ALREADY conservative produced clean confirmations. Per methodology lesson 7 (pessimistic-anchor-first), the engineering-closure-sensitivity SCOPE was anchored on the absolute-ceiling argument I had already sketched in the handoff for round 3 — this round formalized it.
- **The sweep range is honest.** P_HYBRID and P_RENDEZVOUS both swept up to 1.00, beyond physically-plausible engineering priors. That is the right framing for an "absolute-ceiling" analysis.

---

## Files

- `SCOPE.md` — pre-registration (5 hypotheses)
- `run.py` — 2D sweep over (P_HYBRID, P_RENDEZVOUS) × (base-rate × window) → max conjunction; breakeven curves
- `results/engineering_closure_sensitivity.json` — full heatmaps, breakeven table, X=0-corner-only sub-table, H1-H5 verdicts
