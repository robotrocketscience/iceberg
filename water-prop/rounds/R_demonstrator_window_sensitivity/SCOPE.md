# R-demonstrator-window-sensitivity — does extending the window flip H6?

**Status.** Pre-registration. Authored by iapetus, 2026-05-15 (latest+9, immediately after R-reactor-specific-power-program-targets).

**Why.** R-reactor-specific-power-program-targets H6 verdict (technology-demonstrator-only) is anchored on a demonstrator window of 2032-2035 (9-year horizon from base year 2026). That window is a SCOPE-honored choice from R-power-bayesian-update, but it is not derived from program physics — it is a project-owner timeline preference. This round questions that anchor.

**Question.** What demonstrator-window endpoint (year T) is required for the max full-conjunction posterior to cross each capital-class threshold (venture 10%, corporate-growth 30%, regulated-utility 50%, sovereign-bond 80%)? Equivalently: how far into the future must the ICEBERG demonstrator slide for any non-technology-demonstrator financing class to be even marginally rational under the same conservative subjective priors used in R-reactor-specific-power-program-targets?

This is a sensitivity test, not a competing reading. Per methodology lesson 7 (pessimistic-anchor-first), the prior round used the conservative window. This round confirms whether the H6 reading is robust to window-extension or whether it inverts at some plausible horizon.

**Anchoring.** The Bayesian Monte Carlo model is the same as R-power-bayesian-update (Beta-Binomial posterior on per-decade rate × exponential waiting time × Fission-Surface-Power likelihood adjustments × scope conditional 0.6 for 500 kilowatt-electric). The model is re-instantiated in this round's `run.py` with the demonstrator-window endpoint extended to years 2035, 2040, 2045, 2050, 2055, 2060, 2070, 2076-ever. All other priors (specific-power conditional, lifetime conditional, aerocapture-credit conditional, engineering-closure priors, capital-class thresholds) are held fixed at the R-reactor-specific-power-program-targets values.

The min-corner table from the prior round is held fixed — it depends only on the closure physics, not on the window.

---

## Pre-registered hypotheses

| # | Hypothesis | Predicted | Falsification |
|---|---|---|---|
| H1 | The demonstrator-window endpoint at which max full-conjunction posterior first crosses the venture-class 10% threshold is ≥ 2055 under uniform prior, and never under Jeffreys or skeptical priors within the 50-year Monte-Carlo horizon. | breakeven year ≥ 2055 (uniform); never (Jeffreys, skeptical) | H1 falsified if breakeven year ≤ 2050 under uniform OR < ever-50yr under Jeffreys/skeptical |
| H2 | Extending the window to "ever in the 50-year horizon" (i.e. orbit ever by ~2076) does NOT lift max full-conjunction posterior above the corporate-growth 30% threshold under any of the three priors. | max conjunction at ever-50yr < 30% under all priors | H2 falsified if any prior produces max conjunction ≥ 30% at ever-50yr |
| H3 | At the breakeven year T (if it exists for any prior), the resulting first-water-delivery year (T + 14-yr ICEBERG round-trip) lands beyond 2065 under uniform prior. This degrades the program-economics-class further: a 2065 first-revenue delivery has a much lower net-present-value at any non-zero discount rate than 2049 (the 2035-window equivalent). | first-delivery year at uniform breakeven ≥ 2065 | H3 falsified if breakeven uniform pushes first-delivery before 2060 |
| H4 | H6 from R-reactor-specific-power-program-targets is robust to a 10-year window extension: max conjunction at 2045 demonstrator window remains < 10% under all priors. | max conjunction at 2045 < 10% under all priors | H4 falsified if any prior produces max conjunction ≥ 10% at 2045 window |
| H5 | The window-extension lift is approximately linear-to-sub-linear in window length under uniform prior (because Fission-Surface-Power-likelihood multipliers are not symmetric over time). Specifically, the lift from 2035 to 2045 is ≤ 4× under uniform. | uniform lift 2035 → 2045 ≤ 4× | H5 falsified if lift exceeds 4× under uniform |

---

## Method sketch

1. **Re-instantiate the Bayesian Monte Carlo** from `R_power_bayesian_update/run.py` (same priors, same likelihood multipliers, same scope conditional). Seed 0. N=10,000 trajectories.
2. **Sweep demonstrator-window endpoint** across {2035, 2040, 2045, 2050, 2055, 2060, 2070} plus "ever within 50-yr horizon".
3. **At each (window, prior) pair**, extract p(reactor with scope ≥ 500 kilowatt-electric orbit by year T).
4. **Apply the same conditional-prior chain** from R-reactor-specific-power-program-targets:
   - Specific-power conditional (from prior round's table).
   - Lifetime conditional (from prior round's table).
   - Aerocapture-credit conditional (from prior round's table).
   - Engineering-closure priors (P_HYBRID=0.5, P_RENDEZVOUS=0.20 low / 0.30 high).
5. **For each (window, prior, rendezvous-prior) cell**, compute the max conjunction posterior over the min-corner table (held fixed from prior round).
6. **Find breakeven years** for each capital-class threshold under each prior.
7. **Output sensitivity table**: rows = demonstrator-window endpoint years, columns = (prior, rendezvous-prior) → max conjunction → capital class.

---

## Reading template

- **Hypotheses adjudicated.** H1-H5 verdicts.
- **Headline.** Does H6 from prior round survive window-extension? Under what year does it first fail?
- **Reading.** Recommendation: if H6 survives even at ever-50yr horizon, the program-class decision is settled in the prior round's reading. If H6 fails at year T, project owner gets a quantified trade: "delay the demonstrator program to year T for venture-class financing rationality, but degrade first-delivery NPV by N years."
- **Cross-learning.** Updates to R-power-bayesian-update (do their year-2032/2035/2040 numbers match my re-derivation? Sanity check.). Connection to R-delivery-IRR-curve (does the first-delivery-year shift collide with hurdle-crossover findings?).
- **Next-round candidates.** If H4 fails (H6 inverts at 2045), spawn R-program-class-reframe to update L0-13 framing. If H1 falsifies, run the non-US-reactor-program follow-on (e.g. China + Roscosmos base rates).

---

## Method caveats

- Re-running the Monte Carlo means slight Monte-Carlo noise vs hyperion's published numbers. Use the same seed (0) to minimize divergence; report uniform-2035 sanity-check delta.
- The Fission-Surface-Power likelihood multipliers (six factors with means 1.40 to 0.70) are tied to events between 2022 and 2026 — they do not re-multiply at extended horizons. The model treats them as a one-time prior adjustment, which is correct.
- The exponential-waiting-time model has memorylessness — once Fission-Surface-Power succeeds, the time to 500-kilowatt-electric is geometric. Extending the window past the median Fission-Surface-Power-success-year (~19-20 years per the three priors) gives sub-linear lift because most trajectories are already counted in earlier windows.

---

## Worker assignment

- **Round priority:** medium. The prior round's H6 verdict is what's binding; this round only changes that verdict if H4 falsifies. If H4 holds, this round reinforces the prior reading.
- **Worker fit:** iapetus (this session) — the synthesis machinery is already loaded and the prior-round outputs are still in scope.
- **Inputs:** `R_power_bayesian_update/run.py` (Bayesian Monte Carlo model); `R_reactor_specific_power_program_targets/results/reactor_program_targets.json` (min-corner table, subjective priors, capital-class thresholds).
- **Out-of-scope:** non-US reactor-program base rates (saved for separate R-non-US-reactor-program-priors round). Modifications to the underlying physics closure tables (those are upstream of this synthesis).
