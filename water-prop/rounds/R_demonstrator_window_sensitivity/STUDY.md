# R-demonstrator-window-sensitivity — STUDY

**Author.** iapetus
**Date.** 2026-05-15 (latest+9)
**Anchor SCOPE.** `SCOPE.md`, pre-registered before run.
**Inputs.** `R-power-bayesian-update/run.py` (Bayesian Monte Carlo model, re-instantiated verbatim); `R-reactor-specific-power-program-targets/results/reactor_program_targets.json` (subjective priors, min-corner table, capital-class thresholds — all held fixed).

---

## Hypotheses adjudicated

### H1 — venture breakeven year ≥ 2055 under uniform, never under Jeffreys/skeptical

**Verdict: CONFIRMED, in the strong direction.**

| prior | venture (≥10%) breakeven | corporate-growth (≥30%) | regulated-utility (≥50%) |
|---|---|---|---|
| uniform Beta(1,1) | **never within 50-yr horizon** | never | never |
| Jeffreys Beta(0.5,0.5) | never | never | never |
| skeptical Beta(0.5,5) | never | never | never |

Predicted ≥ 2055 for uniform; actual is never-in-horizon. The hypothesis was already conservative — reality is more conservative still.

### H2 — max conjunction at ever-50yr-horizon < 30% under all priors

**Verdict: CONFIRMED.**

At the ever-50yr-horizon (orbit at any time before ~2076), max conjunction under rendezvous-survivability-high (0.30) prior:
- uniform: 0.24%
- Jeffreys: 0.10%
- skeptical: 0.039%

Three orders of magnitude below the 30% corporate-growth threshold.

### H3 — at uniform breakeven, first-delivery year ≥ 2065

**Verdict: CONFIRMED (vacuously).**

Uniform never reaches venture in horizon, so there is no breakeven year to compute first-delivery against. The hypothesis is trivially confirmed because the antecedent is empty.

This is a finding in its own right: the **trade between window-extension and first-delivery degradation never gets to be made**. The conjunction is so far below threshold that no plausible window-shift rescues it.

### H4 — max conjunction at 2045 window < 10% under all priors (H6 robust to 10-yr extension)

**Verdict: CONFIRMED.**

| prior | max conjunction at 2045 window |
|---|---|
| uniform | 0.031% |
| Jeffreys | 0.010% |
| skeptical | 0.0046% |

Max under most-optimistic prior is 0.031%, two orders of magnitude below the 10% venture threshold. R-reactor-specific-power-program-targets H6 reading holds under a 10-year window extension.

### H5 — uniform lift 2035 → 2045 ≤ 4×

**Verdict: FALSIFIED.**

Measured lift uniform-2035 → uniform-2045 = 8.1×. Predicted upper-bound was 4×.

**Why:** The lift is super-linear in window length because two conditionals are compounding. The Fission-Surface-Power orbit posterior grows in the window, AND the 500-kilowatt-electric scope-conditional (4-yr gap after Fission-Surface-Power orbit, then another exponential waiting time) ALSO grows in the window. Each decade of window-extension roughly doubles both conditionals. The hypothesis assumed FSP-orbit was the binding constraint and the scope-conditional grew sub-linearly. In fact both grow super-linearly during the window where the FSP-orbit median has not yet been reached (~year 19-20 offset from base year).

**Consequence.** Above 2055 the lift slows (because the median FSP-success year is in the rearview), but the compounding factor in the early window-extension is bigger than predicted. None of this changes the H4/H6 reading because the absolute starting magnitude is so small.

---

## Sanity check vs hyperion's R-power-bayesian-update

| metric | hyperion reported | iapetus re-derived | delta |
|---|---:|---:|---:|
| uniform p_500kWe_orbit_by_2035 | 0.13% | 0.09% | -30.8% |

The deviation is within the 2σ Monte-Carlo standard-error for N=10,000 trajectories on a probability of 0.13%: SE = sqrt(p(1-p)/N) ≈ 0.036%, so the 2σ band is roughly [0.058%, 0.20%]. The iapetus value 0.09% is well inside. The deviation likely stems from a different per-prior RNG branching (iapetus uses `SEED + hash(prior_name) % 1000`; hyperion runs the priors sequentially with the same `SEED` and consumes the RNG state in order). Order of magnitude matches; the H4/H6 readings do not depend on this deviation.

---

## Headline

**H6 from R-reactor-specific-power-program-targets is robust to demonstrator-window extension across the full 50-year Monte-Carlo horizon.** Under the most-optimistic prior bracket (uniform Beta(1,1)) and the most-favorable rendezvous prior (0.30), max full-conjunction posterior at "ever within 50-yr horizon" is **0.24%** — still in technology-demonstrator class. Under all three (prior × rendezvous) combinations, no demonstrator-window endpoint within the 50-year horizon lifts the conjunction across the venture (10%), corporate-growth (30%), or regulated-utility (50%) thresholds.

---

## Reading

**The H6 reading is settled, not just defended.** Window-extension was the most-plausible challenge to H6 (per the structure of R-power-bayesian-update's headline numbers, p_fsp_by_2040 / p_fsp_by_2035 ≈ 1.5× under uniform, suggesting time-horizon extension lifts the orbit posterior). The actual lift is even larger (8× over a 10-year extension), but the absolute base is so small that even compounding cannot lift the conjunction across venture threshold.

**What this rules out.** It rules out a "patient capital" or "long-horizon-research-philanthropy" reframe of the program-class decision. A venture or corporate-growth investor cannot be rationally pitched on "wait 30 more years for the reactor program to develop" — the conjunction is below venture-class even at the 50-year horizon.

**What this still allows.** A pure technology-demonstrator program with research-grant or sovereign-grant financing is the only honest reading at conservative anchors. The matrix-decision-point #1 conclusion from the prior round stands.

**What could still flip it.** The two assumptions this round does NOT challenge:
1. **US-only reactor-program base rate.** If non-US fission programs (China Atomic Energy Authority, Roscosmos, NewCleo derivatives) are added, the orbit posterior could rise materially.
2. **The Fission-Surface-Power-likelihood multiplier set.** Six factors from 2022-2026 events. If a new factor appears (e.g. Fission-Surface-Power Phase 2 contract award), the posterior would step up. Conservative bracketing already includes "no_phase2_contract_may_2026" (factor 0.80) which would invert to positive if the contract is announced.

These are the two genuine open assumptions. Worth a follow-on round if the project owner has reason to revisit either.

---

## Cross-learning

- **R-power-bayesian-update (hyperion).** Sanity-checked: my re-derived numbers track hyperion's within 2σ Monte-Carlo noise. The hyperion model is the right anchor for any reactor-program-priors work; window-extension does not change the qualitative reading.
- **R-reactor-specific-power-program-targets (prior round, iapetus).** H6 strengthened: not just "technology-demonstrator at the 2032-2035 window" but "technology-demonstrator at any window extension within 50-year horizon".
- **R-delivery-IRR-curve (worktree-110450 follow-up).** That round mapped (delivered tonnage per ship) to (hurdle-rate-cleared capital classes): sovereign-bond at 209 t/ship, regulated-utility at 461 t/ship, corporate-growth at 691 t/ship. This round adds the timing dimension: even if delivered tonnage clears those thresholds *conditional on the cell closing*, the joint posterior probability of cell-closure-in-window is the binding constraint, and it never clears venture (much less corporate-growth) under any window-extension within horizon.
- **R-architecture-D-cost.** If the reactor program is treated as the bottleneck, Architecture D (chemical-plus-small-reactor) becomes more attractive than Architecture E (megawatt-electric). The window-sensitivity reading is asymmetric across the matrix — Architecture D is far less reactor-program-dependent than Architecture E, so this round's H6-strengthening hits Architecture E harder.

---

## Next-round candidates

1. **R-non-US-reactor-program-priors.** The only remaining lever that could plausibly flip H6 at any horizon. China's high-temperature gas-cooled reactor program has demonstrated commercial-scale operation; Roscosmos has discussed megawatt-class space reactor; NewCleo (Italian/UK private) targets commercial fast-reactor by 2030s. Adding these to the base rate would re-derive p_orbit_by_year_T with a multi-program base rate. Reasonable next round if project owner wants to challenge the US-only anchor.
2. **R-FSP-Phase-2-likelihood-update.** If/when Fission-Surface-Power Phase 2 contract is announced (Draft Announcement was Aug 29 2025; final release anticipated early 2026), the "no_phase2_contract_may_2026" likelihood factor (0.80) inverts to a positive factor. The shock-update of the Bayesian posterior would be material — probably 20-40% lift on p_fsp-orbit. Still wouldn't cross venture threshold unless combined with other priors moving simultaneously, but worth recomputing once the announcement lands.
3. **R-engineering-closure-prior-sensitivity.** I held P_HYBRID=0.5 and P_RENDEZVOUS=0.2/0.3 fixed. If those are wrong (e.g. R-hybrid-aerocapture-aerobraking comes back at 0.10 or 0.90), the conjunction shifts by 2-5×. Pair this with the next-up engineering round results, not now.
4. **Methodology lesson candidate (lesson 11).** "Robust-but-not-load-bearing sensitivity rounds." This round confirms a prior reading rather than overturning it. Pattern: when a prior round produces a load-bearing reading that depends on one anchored choice (here: window), the load-bearing-anchor sensitivity test is worth running for completeness — and the "confirmed-robust" outcome is itself a strong epistemic state-update, not a no-op.

---

## Methodology notes

- **Lesson 7 (pessimistic-anchor-first).** This round inverts the prior round's choice (extends window instead of using conservative window) and shows the prior reading still holds under the more-favorable assumption. That's the right direction for sensitivity testing on a load-bearing reading.
- **Lesson 9 (anchor SCOPE on prior aggregate verdict).** SCOPE explicitly anchored on R-reactor-specific-power-program-targets H6 reading, named in the question and used directly in the falsification bands.
- **Pre-registration discipline.** SCOPE.md was written and committed before `run.py`. Specifically, H1 predicted "≥2055" under uniform — actual was "never in horizon"; H5 predicted "≤ 4×" — actual was 8.1×. Both genuine falsification-band tests. H5 falsified is the only genuinely-surprising outcome.

---

## Files

- `SCOPE.md` — pre-registration
- `run.py` — Bayesian Monte Carlo (re-instantiated from R-power-bayesian-update) + conditional-prior chain re-application + window sweep
- `results/demonstrator_window_sensitivity.json` — sensitivity table, breakeven years, H1-H5 verdicts
