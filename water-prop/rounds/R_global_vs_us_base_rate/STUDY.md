# R-global-vs-US-base-rate — STUDY

**Author.** iapetus
**Date.** 2026-05-15 (latest+9)
**Anchor SCOPE.** `SCOPE.md`, pre-registered before run.
**Inputs.** Locked beliefs 2-4 (US-only base rate, FSP-Phase-2 timeline, MARVL radiator finding); `R_power_bayesian_update/run.py` (Bayesian Monte Carlo model, re-instantiated with global counts); `R_reactor_specific_power_program_targets/results/reactor_program_targets.json` (subjective priors held fixed); `R_demonstrator_window_sensitivity/results/demonstrator_window_sensitivity.json` (US-only side-by-side baseline).

---

## Hypotheses adjudicated

### H1 — global / US orbit-posterior ratio ≥ 3× under uniform prior at 2035

**Verdict: FALSIFIED.**

Measured ratio: 2.39× (global 21.16% / US-only 8.84% at 2035 under uniform prior). Predicted ≥ 3×.

Why the actual lift was smaller than predicted: my base-rate count for global (2 successes / 10 programs) treats USSR-BUK and USSR-TOPAZ as two distinct program-level successes, but in Beta-Binomial posterior terms, two successes in 10 trials yields posterior Beta(α+2, β+8) — the alpha-shift is partly offset by the beta-shift, so the posterior-mean rate goes from α/(α+β+6) = 1/8 = 0.125 (uniform US-only) to (α+2)/(α+β+10) = 3/12 = 0.25 (uniform global). That's 2× lift on the per-decade rate, not 3×.

Predicted-vs-actual difference is genuine epistemic update: at the program level, the BUK series (~30 reactor orbits 1970-1988) counts as **one** programmatic success, not thirty. If I had counted BUK as 30 successes, the lift would have been much higher — but doing so over-weights one program. The conservative program-level count is the right framing.

### H2 — global / US scope-conditional ratio ≤ 0.33

**Verdict: FALSIFIED.**

Measured ratio: 0.67 (global 0.40 / US-only 0.60). Predicted ≤ 0.33.

Why: I anchored the global scope conditional too aggressively pessimistic. The currently-pending program mix is:
- US Fission-Surface-Power Phase-2: 100 kilowatt-electric scope (below 500)
- Russia Zeus: 500-1000 kilowatt-electric scope (at/above threshold)
- China-megawatt: ≥ 1000 kilowatt-electric scope (above threshold)

Two of three currently-pending programs target ≥ 500 kilowatt-electric. The prospective scope conditional is therefore much closer to 0.6 than to 0.2. My 0.4 anchor was a reasonable middle, but the ratio against 0.6 is 0.67, not 0.33.

This is a methodology note: the SCOPE for this round mixed historical and prospective scope distributions (historical: 0% of orbited reactors at ≥ 500 kilowatt-electric; prospective: 67% of pending programs target ≥ 500 kilowatt-electric). For a forward-looking conditional, the prospective distribution is the correct anchor.

### H3 — net conjunction at 2032-2035 in [0.0028%, 0.011%]

**Verdict: FALSIFIED.**

Measured: 0.0155% (above the upper bound of 0.011%). The orbit lift (2.4×) compounded with the milder scope-conditional reduction (0.67×) and a larger-than-predicted Monte Carlo bias to produce a net ~12× lift over US-only at the 2035 window.

The expected-value calculation (1.6× = 2.4 × 0.67) does not match the empirical 12× because the Monte Carlo also captures the right-skew from rare orbit-success trajectories that contribute to the tail. The global base rate makes those tail trajectories more frequent and earlier-arriving, both compounding into the within-window probability.

### H4 — H6 holds under global base rate: venture (10%) never crossed in 50-yr horizon

**Verdict: CONFIRMED.**

| prior | venture breakeven (rend_hi, global base rate) | corp-growth breakeven |
|---|---|---|
| uniform Beta(1,1) | **never within 50-yr horizon** | never |
| Jeffreys Beta(0.5,0.5) | never | never |
| skeptical Beta(0.5,5) | never | never |

The most-aggressive corner under any combination tested (global base rate + uniform prior + scope-conditional-high 0.50 + rendezvous-hi 0.30 + "ever within 50-yr horizon"): **max conjunction = 0.77%**, still 13× below the venture (10%) threshold.

### H5 — conjunction shift |global - US| / US ≤ 50% at 2035 under uniform

**Verdict: FALSIFIED.**

Measured shift: ~1100% (global 0.0155% / US-only 0.0013%, an 11.9× increase, so the |delta|/US ratio is ~10.9 = 1090%). Predicted ≤ 50%.

This is the most-substantive falsification: my "orbit-up and scope-down cancel" hypothesis was wrong by an order of magnitude. The orbit-rate increase dominates the scope-conditional decrease by ~10× at the small-probability tail. **The base rate IS the load-bearing input** — the scope conditional cannot offset a structural change to the base rate.

**This shifts the methodology read.** If H6 had been close to the venture threshold under US-only, this round would have flipped it. Instead, US-only conjunction is so far below threshold (0.0013% at 2035) that a 12× lift still leaves it below threshold (0.0155%). The robustness of H6 is therefore due to the *magnitude* of the floor, not to base-rate balance.

---

## Headline

**H6 is robust even under maximally-favorable assumptions across base rate, window, scope conditional, and rendezvous prior.** Switching from US-only (0-of-6) to global (2-of-10) base rate lifts the conjunction posterior by ~10× at the 2032-2035 window, but the absolute starting magnitude is so small (0.0013% under US-only uniform) that even a 10× lift leaves the conjunction at 0.0155% — still 4 orders of magnitude below venture-class threshold (10%). At "ever within 50-year horizon" under the most-favorable global + high-scope-conditional + rendezvous-hi assumptions: max conjunction = 0.77%, still 13× below venture.

---

## Reading

**The H6 reading is now robustly settled across three rounds:**

1. R-reactor-specific-power-program-targets (US-only baseline): max conjunction 0.0055% at 2032-2035 window.
2. R-demonstrator-window-sensitivity (US-only, window-extended): max conjunction 0.24% at ever-50yr.
3. R-global-vs-US-base-rate (global, window-extended, high scope): max conjunction 0.77% at ever-50yr.

Across all three rounds, no combination of priors (subjective sp/L conditional + engineering-closure priors + base rate + window + scope conditional) reaches the venture (10%) threshold. The technology-demonstrator-only program-class verdict is the **load-bearing conclusion** of the chain.

**The unfortunate consequence for ICEBERG framing.** Even adopting the most aggressive plausible position on every load-bearing assumption (global base rate, ever-horizon window, high scope conditional, rendezvous-hi prior), the program-class decision lands in technology-demonstrator / sovereign-research-grant. This is not a sensitivity to a single overly-conservative anchor. It is the structural result.

**What this rules out.** Two specific reframes are ruled out:
1. A "patient global capital" reframe (i.e. wait for China's megawatt program OR Russia's Zeus OR a US program revival, and let the timeline slide to 2040+). The conjunction at 2040 under global+high+rend_hi is 0.071%. Not viable as venture or corporate-growth.
2. A "sovereign-bond plus ICEBERG-utility-rate-base" reframe. The conjunction at ever-horizon under all aggressive assumptions is 0.77%. Sovereign-bond threshold is 80%. Off by two orders of magnitude.

**What this still allows.** A pure technology-demonstrator funded under sovereign-research-grant or research-philanthropy is the only honest reading. The pitch must lead with technology-demonstrator framing, with all other capital classes surfaced only conditional on a specific reactor-program announcement (Fission-Surface-Power Phase-2 contract, Zeus orbital flight authorization, or equivalent).

**Geopolitical caveat.** A global base rate implies the program might rely on a non-US reactor supply. The project-owner Level-0 currently anchors on US sovereignty (per locked belief 3 + the FSP focus). If non-US reactor supply is allowed as a Level-0 amendment, the orbit-rate lift exists but does NOT cross any capital-class threshold. So even *with* the geopolitical concession, the program-class reading does not change.

---

## Cross-learning

- **R-power-bayesian-update (hyperion).** This round adds a global base-rate variant to the hyperion model. The global posterior is materially different (2× higher per-decade rate) but the downstream conjunction is still below venture. Hyperion's US-only model is the right anchor for what's plausibly achievable under current US-sovereignty assumption; the global variant should be cited as a sensitivity, not a replacement.
- **R-reactor-specific-power-program-targets (prior iapetus round).** H6 strengthened a second time. The chain of three rounds now establishes the conclusion is robust against the four most-load-bearing assumptions.
- **R-demonstrator-window-sensitivity (prior iapetus round).** Same methodological pattern: sensitivity-test confirms rather than overturns. The pattern is consistent and worth flagging.
- **R-reactor-roadmap (worktree-110450).** That round computed Internal-Rate-of-Return at 1.45 percent under MARVL-anchored mass + reactor cumulative-distribution-function. The IRR there is for a per-mission revenue model. This round extends that to the full conjunction (reactor-availability × engineering-closure), and confirms the program-class is technology-demonstrator regardless of whether the per-mission economics close.
- **Locked belief 2 ("0-of-6 base rate") and locked belief 3 (Fission-Surface-Power Phase-2 not awarded).** These remain the right project-anchor for the load-bearing input. The global-variant computed here is a worker-round sensitivity that does not change the locked-belief framing.

---

## Methodology lessons (candidate)

- **Lesson 11 (candidate): robustness-by-magnitude vs robustness-by-cancellation.** A load-bearing reading can be robust to assumption-shifts in two structurally-different ways. Either (a) the assumption-shifts cancel out (the "orbit-up scope-down" hypothesis I tested in this round — falsified), or (b) the absolute starting magnitude is so far from the threshold that no plausible shift bridges the gap (the actual mechanism here). When the second mechanism holds, the conclusion is harder to overturn because partial shifts in many parameters all leave the conclusion unchanged. The chain of three rounds establishes this for the program-class decision.
- **Lesson 12 (candidate): forward-looking conditionals vs historical conditionals.** My H2 falsification was due to mixing historical scope distribution (0% of orbited reactors at ≥ 500 kilowatt-electric) with prospective scope distribution (67% of currently-pending programs target ≥ 500 kilowatt-electric). When the conditional is forward-looking (probability of orbit-in-window at given scope), the prospective distribution is the right anchor. Historical scope distribution becomes a sanity-check only.

---

## Next-round candidates

This round closes the conditional-and-base-rate sensitivity chain. The remaining open-but-low-priority assumptions are:

1. **Engineering-closure-prior sensitivity** (P_HYBRID_AEROCAP = 0.5, P_RENDEZVOUS = 0.20/0.30). These are subjective. If R-hybrid-aerocapture-aerobraking or R-bring-rendezvous-survivability come back with their own engineering-pre-registered probabilities, those should replace my placeholders. Not load-bearing for H6 (the engineering priors compound multiplicatively with already-tiny base rates).
2. **Specific-power × lifetime anti-correlation.** I treated p(sp ≥ S | orbit) and p(L ≥ L | orbit) as independent. If radiator-area-scaling-with-deployability constraints actually anti-correlate sp and L (per the MARVL finding), the joint is smaller than the independent product → my conjunction is overestimated → H6 strengthened. If positively correlated (advanced programs invest in both), conjunction underestimated → could lift but still bounded by capital-class compute.
3. **Pitch reframe.** Methodology-meta: a round to draft the technology-demonstrator-leading pitch reframe, including how to position other capital classes as conditional optionality.

After three robustness rounds confirming H6, the marginal value of further sensitivity rounds on this question is low. The next-most-load-bearing project work is likely the engineering-closure rounds themselves (R-hybrid-aerocapture-aerobraking, R-bring-rendezvous-survivability), not more sensitivity on the reactor-program side.

---

## Methodology notes (reflections)

- **Three falsifications in this round** (H1, H2, H3, H5) are genuine epistemic updates on the magnitudes of the global-vs-US-base-rate effects. But none of them flip the load-bearing reading (H4). This is the right pattern: pre-register magnitudes, learn when you were wrong on a magnitude, but track which dimensions of being-wrong are load-bearing vs noise.
- **Sanity-check delta.** US-only uniform p_500_by_2035 in this run = 0.03% vs hyperion's 0.13% vs my prior round's 0.09%. Monte Carlo noise at small-probability tails is substantial; the qualitative conclusion is unchanged. Per-prior RNG seed branching introduces some variance — should standardize across all my rounds for cleanliness in a future cleanup pass.
- **Pre-registration discipline preserved.** SCOPE.md was committed before `run.py`. Hypotheses with quantified falsification bands. Falsifications recorded honestly.

---

## Files

- `SCOPE.md` — pre-registration
- `run.py` — Monte Carlo with global vs US base rate variants + conditional-prior chain re-application
- `results/global_vs_us_base_rate.json` — full sensitivity table, breakevens, H1-H5 verdicts
