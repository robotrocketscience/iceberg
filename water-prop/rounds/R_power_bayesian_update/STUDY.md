# R-power-bayesian-update — prior-sensitivity bracket on Fission-Surface-Power-Phase-2 → flight by 2035, plus matrix programmatic-risk overlay

**Status:** pre-result.

## Question

R-power-base-rate (hyperion, 2026-05-15) ran a Beta(1, 7) prior with FSP-specific likelihood multipliers and produced posterior 9.1% on "any United States fission orbit by 2035." That was a single-prior result. Two open issues:

1. **Prior sensitivity is unbounded.** Beta(1, 7) embeds a Laplace-style "one pseudo-success" charity (SNAP-10A reached orbit, even if it failed at 43 days) and is one defensible choice. A skeptic would argue the program-management problem has not structurally changed since SP-100 cancellation in 1994 and would prefer Beta(0.5, 5) (informative-skeptical). A reference-Bayesian would prefer Beta(0.5, 0.5) (Jeffreys, the conjugate non-informative). The headline 9.1% number depends on which you pick. Until the bracket is on paper, the matrix's "architecture-program risk" framing has no defensible numerical anchor.

2. **The matrix has no programmatic-risk overlay.** The architecture decision matrix (`water-prop/docs/ARCHITECTURE-DECISION-MATRIX.md`) lists a "Status (post-evening)" column noting that the surviving Variant B cell is contingent on a 500-kilowatt-electric reactor program five times Fission Surface Power Phase 2 scope, but does not propagate that contingency into expected delivered mass or expected round-trip time. The orchestrator has no integrated "matrix row weighted by P(reactor program reaches orbit by demonstrator window)" output to point at.

This round closes both gaps. It (a) sweeps three priors against the same 0-of-6 likelihood and same Fission-Surface-Power-specific multiplier set as the upstream round, and (b) produces a matrix-overlay JSON keyed by the matrix's existing reactor-era rows, giving the orchestrator a drop-in patch.

## Pre-registered hypotheses

See `HYPOTHESES.md` for the full block (added in same commit). Summary:

- **H-pbu-a (uniform-prior headline):** posterior P(any United States fission orbit by 2035) under Beta(1, 1) prior + 0-of-6 likelihood + Fission-Surface-Power multipliers ∈ [7%, 14%]. Pre-registered point estimate 10%.
- **H-pbu-b (Jeffreys):** same posterior under Beta(0.5, 0.5) prior ∈ [4%, 9%]. Pre-registered point estimate 6%.
- **H-pbu-c (skeptical):** same posterior under Beta(0.5, 5) prior ∈ [2%, 6%]. Pre-registered point estimate 3.5%.
- **H-pbu-d (bracket width):** the ratio (uniform posterior) / (skeptical posterior) at the 2035 horizon ∈ [2.0, 4.5]. Pre-registered point estimate 2.9. (Tests whether prior choice dominates the headline number; if the bracket collapses, the matrix can quote a single number; if it spans 4×, the matrix must quote a range.)
- **H-pbu-e (matrix overlay sign):** the programmatic-risk-adjusted delivered mass for the Variant B 500-kilowatt-electric cell ∈ [10, 35] tonnes per mission averaged over reactor-program-success uncertainty (the rhea-measured 90 t deliverable × P(500 kilowatt-electric reactor program reaches orbit by 2035)). Pre-registered point estimate 18 t. (Sub-hypothesis to test whether the matrix's "Variant B is the surviving cell" framing survives one-step Bayesian propagation.)

Aggregate prediction: prior choice moves the headline by a factor of 2–4×, the uniform-prior posterior is the most defensible-to-skeptics single number, and the matrix's surviving Variant B cell delivers a programmatic-risk-adjusted mass under 25 t per mission across all three priors. The matrix's current presentation, which quotes 90 t conditional-on-reactor-availability without the conditioning weight, overstates expected delivered mass by 4–10×.

## Method

**Three priors, same likelihood.** The likelihood is the upstream R-power-base-rate model, unchanged: 0-of-6 observed program failures since SNAP-10A (SP-100, Project Timberwind, Prometheus / Jupiter Icy Moons Orbiter, Kilopower flight, Defense Advanced Research Projects Agency Demonstration Rocket for Agile Cislunar Operations, Fission Surface Power as of May 2026), Fission-Surface-Power-specific multiplier set from the upstream round (six multiplicative factors: Phase-1 award, Phase-1 extension, Duffy directive scope grew, draft Announcement for Partnership Proposals, no Phase-2 contract, FY2026 budget zero-out of nuclear-electric-propulsion / nuclear-thermal-propulsion lines).

The three priors:

| Prior | Beta(α, β) | Posterior after 0-of-6 | Posterior mean (per-decade rate) | Rationale |
|---|---|---|---|---|
| Uniform | Beta(1, 1) | Beta(1, 7) | 12.5% | Laplace; matches upstream R-power-base-rate's prior choice exactly. Gives partial credit for "the program-management problem might have changed since 1994." |
| Jeffreys | Beta(0.5, 0.5) | Beta(0.5, 6.5) | 7.1% | Conjugate non-informative reference prior. No structural-change credit; no penalty either. |
| Skeptical | Beta(0.5, 5) | Beta(0.5, 11.5) | 4.3% | Informative-skeptical: encodes a prior belief that the program-management problem has not structurally changed since SP-100. Treats the four post-1994 cancellations (Prometheus, Defense Advanced Research Projects Agency Demonstration Rocket for Agile Cislunar Operations, Kilopower-flight no-go, Fission Surface Power Phase-2 delay) as evidence of a stable failure regime, not a transient one. |

**Same Monte-Carlo harness.** 10,000 trajectories per prior, seed = 0, deterministic. Per-decade rate sampled from the prior's posterior, converted to annual hazard via 1 − exp(−10 λ_annual) = λ_decade, multiplied by the Fission-Surface-Power factor product, exponential waiting time gives Fission-Surface-Power-class orbit year. Megawatt-class arrival is conditional via the same 7-year gap + 45% funded-after-success + independent decade-rate draw, copied verbatim from upstream.

**Matrix overlay propagation.** Each matrix cell that names a reactor power class gets a programmatic-risk-adjusted delivered-mass column:

```
expected_delivered_mass = P(reactor_class_orbit_by_demonstrator_window) × delivered_mass_conditional_on_reactor
```

Demonstrator window: 2032–2035 per the matrix's stated horizon. Three Fission-Surface-Power-class delivered-mass figures from the matrix or from rhea's R-megawatt-marvl-radiator: 90 t (Variant B 500 kilowatt-electric, rhea-derived), 0 t (megawatt all-electric, falsified), 0 t (year-twenty-plus megawatt end-to-end, falsified). The 500 kilowatt-electric class is treated as Fission-Surface-Power-derivative — five times the August 2025 Duffy-directive scope. The Bayesian model treats it as P(Fission-Surface-Power-class orbit by 2035) × P(500 kilowatt-electric scale-up funded conditional on Fission-Surface-Power-class orbit), with the second factor pre-registered at 0.6 (less penalized than megawatt-class because a 5× scale-up is materially less ambitious than a 25× scale-up).

The matrix overlay is written to `results/matrix_overlay.json` keyed by reactor era, with three sub-keys per row (uniform, Jeffreys, skeptical posterior). The orchestrator can drop this directly into a new column without re-running Monte Carlo.

## Validity caveats

1. **Same likelihood, same vulnerabilities.** This round inherits every validity caveat from R-power-base-rate's STUDY.md (small-N base rate, structural-change biases, independence assumption, no upside from non-United-States programs, R-reactor-roadmap pre-result). The contribution here is prior-sensitivity bracketing only; if the upstream model is biased, all three priors are biased the same direction.

2. **Skeptical prior could be argued harder either way.** Beta(0.5, 5) is one informative-skeptical choice; Beta(0.5, 10) (twice as skeptical) would push the headline another factor of two lower. The pre-registration anchors at Beta(0.5, 5) as the "most skeptical defensible-without-advocacy" choice. A skeptic-advocate would push further; a charity-advocate would push to Beta(2, 6) (treating SNAP-10A as worth two pseudo-successes). The bracket width is itself a defensibility question that this round does not close.

3. **Matrix overlay multiplies two model outputs.** Both factors carry uncertainty; combining them by multiplication (rather than full convolution) understates the total uncertainty band. The overlay is therefore a central-estimate tool, not a credible-interval tool. The hypothesis pre-registration ranges H-pbu-e accordingly.

4. **"Demonstrator window" is a moving target.** The matrix uses 2032–2035; the August 2025 Duffy directive used "Q1 FY2030 deployment intent." If the demonstrator window slips to 2037–2040 in the next matrix revision, all overlay numbers move (in a direction the upstream model can predict — see results table).

5. **No correlation between priors and likelihood multipliers.** The three priors are evaluated against an identical Fission-Surface-Power-multiplier set. A more sophisticated treatment would let the skeptical prior also scale up the magnitude of the negative multipliers (treating "FY2026 budget zero-out" as evidence in favor of the skeptical prior, not as a separate independent fact). This round does not do that — it isolates prior choice from likelihood, which is the cleaner sensitivity test but understates the difference between skeptical and charitable analyses.

## Result

Ran 10,000 trajectories per prior, seed = 0, deterministic. Full summary: `results/R_power_bayesian_update_summary.json`. Matrix overlay: `results/matrix_overlay.json`.

**Headline three-prior bracket on P(any United States fission orbit by 2035):**

| Prior | Posterior Beta(α, β) | Posterior mean per-decade rate | P(orbit by 2032) | **P(orbit by 2035)** | P(orbit by 2040) |
|---|---|---:|---:|---:|---:|
| Uniform Beta(1, 1) → Beta(1, 7) | 12.5% | 5.5% | **8.9%** | 14.1% |
| Jeffreys Beta(0.5, 0.5) → Beta(0.5, 6.5) | 7.1% | 2.9% | **4.9%** | 8.4% |
| Skeptical Beta(0.5, 5) → Beta(0.5, 11.5) | 4.3% | 1.8% | **2.9%** | 4.5% |

**Bracket ratio (uniform / skeptical) at 2035 horizon: 3.05.** Pre-registered range 2.0–4.5; held.

**Pre-registration grading:**

| Sub-claim | Predicted range | Point estimate | Measured | Held? |
|---|---|---:|---:|---|
| H-pbu-a — uniform P(fission by 2035) | 7–14% | 10% | **8.9%** | HELD |
| H-pbu-b — Jeffreys P(fission by 2035) | 4–9% | 6% | **4.9%** | HELD |
| H-pbu-c — skeptical P(fission by 2035) | 2–6% | 3.5% | **2.9%** | HELD |
| H-pbu-d — bracket ratio uniform / skeptical | 2.0–4.5 | 2.9 | **3.05** | HELD |
| H-pbu-e — Variant B 500-kilowatt-electric overlay (uniform) | 10–35 t | 18 t | **0.12 t** | FALSIFIED-pessimistic, 150× below low edge |

**Matrix programmatic-risk overlay (`matrix_overlay.json`), expected delivered mass per mission integrated over reactor-availability uncertainty:**

| Architecture cell | Conditional delivered mass | Uniform expected | Jeffreys expected | Skeptical expected |
|---|---:|---:|---:|---:|
| Variant B 500-kilowatt-electric chemical-kick + electric-inbound | 90 t | **0.12 t** | 0.03 t | 0.01 t |
| All-electric megawatt | 0 t (falsified) | 0 t | 0 t | 0 t |
| Year-twenty-plus megawatt end-to-end | 0 t (falsified) | 0 t | 0 t | 0 t |

**Extended-window sensitivity (uniform prior):** P(500-kilowatt-electric class orbit by 2040) = 0.46% (a ~3.5× lift over the 2035 figure). P(megawatt orbit ever within 50-year horizon) = 4.3%. Median megawatt-class arrival year offset from 2026 = 42.9 years (i.e., 2069). Skeptical-prior median = 39.3 years (2065 — earlier because the lower per-decade rate gates more trajectories at "never" rather than spreading them across the tail).

## Reading

Two distinct findings, only one of which the pre-registration anticipated.

**Finding 1 (anticipated): the prior bracket is real but narrow.** The headline P(fission by 2035) moves from 8.9% (uniform / charity) to 2.9% (skeptical), a 3.05× spread. This is large enough that a single-number quote in the matrix would be misleading, but small enough that the qualitative reading is the same under all three priors: **the United-States space-fission program reaching orbit by the demonstrator window is a low-probability event under any defensible prior choice.** The matrix's "architecture-program risk" framing is correctly directional. The number to quote is **3–9%**, with the headline anchored at the uniform prior's 8.9% per the response to the prior-choice question. This is consistent with the user-locked finding that the 0-of-6 base rate should be used as a Bayesian prior on Fission-Surface-Power Phase 2 → flight by 2035; this round numerically anchors that prior at 3–9% with explicit prior-sensitivity documentation.

**Finding 2 (unanticipated, load-bearing): chained-multiplicative collapse erases the surviving Variant B cell under one-step Bayesian propagation.** Pre-registration anchored H-pbu-e at 18 t expected, treating the 500-kilowatt-electric class as roughly Fission-Surface-Power-class-equivalent in arrival probability (with a small downweight for the 5× scope grow). This was wrong by two orders of magnitude. The model collapses because Variant B's reactor requires *(a)* Fission-Surface-Power-class succeeds AND *(b)* a 500-kilowatt-electric scale-up program is funded conditional on Fission-Surface-Power success (60% pre-registered) AND *(c)* that program reaches orbit within its decade attempt AND *(d)* all of this happens inside a 9-year window from base year 2026. Each factor is plausible alone; their product is 0.13% under the uniform prior, falling to 0.01% under skeptical.

**The matrix can no longer claim Variant B as "the surviving cell" without naming the conditioning weight.** Quoting "90 t per mission, 14.5-year round trip" without "× P(reactor available) ≈ 1%" is the same kind of conditional-without-conditioning-weight error R-mission-success-probability flagged for the L0-10 reliability column. The corrected matrix presentation is one of:

1. **Conditional on reactor program success** (current matrix style): explicitly add the conditioning sentence "× P(500-kilowatt-electric reactor on orbit by 2035) ≈ 0.1%–0.5%" to the Variant B row.
2. **Programmatic-risk-adjusted (this overlay)**: replace the delivered-mass figure with the expected value 0.01–0.12 t per mission, marking the cell as a sub-tonne expected-value bet.
3. **Window-extended**: relax the demonstrator window to 2040–2045 and re-run. Under uniform prior, P(500-kilowatt-electric by 2040) is 0.46% — still ~5× below the implicit 20% that an 18-tonne pre-registration assumes.

None of the three corrected presentations leaves Variant B as a "surviving" cell in any commercially-meaningful sense. **The matrix's defensible position post-this-round is: there is no architecture cell at any reactor era with positive integrated expected delivered mass on the demonstrator-window timeline.** The cells that close conditional on reactor are all conditioning on tail events.

**Why the conditional / unconditional distinction matters here.** Program planning of this style is normally entitled to condition on reactor availability — "if the reactor program flies, here's what we deliver." Under the 0-of-6 prior, that conditioning is doing more work than is normal. An equivalent example: a 1990 NEP program plan conditioned on SP-100 availability would have looked technically reasonable; in retrospect, the program-failure mode dominated all the technical-architecture-choice modes. This round's contribution is to make that conditioning weight explicit and defensible-against-skeptics.

## Revisit

**Pre-registration accuracy: four of five sub-claims held inside their pre-registered ranges.** H-pbu-a, b, c, d held — confirming that the prior-bracket calculation reproduces a defensible single-step posterior under each prior. The only falsified claim, H-pbu-e, was falsified pessimistic by ~150×, recapitulating the recurring-lesson #N from R-power-base-rate's Revisit clause: **chained-multiplicative pre-registrations are systematically over-bullish if each factor is ranged from intuition.** The pre-registration (18 t expected) implicitly assumed P(500-kilowatt-electric by 2035) ≈ 20% by working backwards from "Variant B is the surviving cell, so it must integrate to a meaningful expected mass." The model surfaces that the joint probability is ~0.1%, two orders of magnitude lower.

This is the second instance of the same recurring lesson in the campaign. R-power-base-rate's Revisit added a candidate lesson; this round elevates it to an empirical pattern. **Future pre-registrations involving chained probabilities should compute the multiplicative product of central estimates first, then range around that.** I did not do this for H-pbu-e despite the lesson being on the books — pre-registration discipline is a separate failure mode from the model itself.

**The 500-kilowatt-electric scale-up parameters (P_500_FUNDED_GIVEN_FSP = 0.6, FSP_TO_500_GAP_MEAN = 4 years) are author-asserted, not data-derived.** A skeptic could argue P = 0.45 (matching the megawatt-class number, on the grounds that "5× scope is still a clean-sheet vendor decision"); a charity-advocate could argue 0.8 (treating it as an iterative Phase-3-after-Phase-2 award). Re-running with P = 0.8 and 1-year gap roughly triples the expected-mass overlay to ~0.4 t — still falsified-pessimistic against the H-pbu-e range. The qualitative finding survives; the exact number does not.

**Validity caveat #2 (skeptical prior) untested.** The bracket reports the spread across three pre-selected priors. It does not test what happens if a skeptic argues for Beta(0.5, 10) or a charity-advocate argues for Beta(2, 6). Future round (if needed): full-prior-grid sensitivity heatmap.

## Cross-learning

- **Negative for `water-prop/docs/ARCHITECTURE-DECISION-MATRIX.md` "Net effect on the architecture decision (post-evening)" section, year-zero-through-fifteen Variant B cell.** Currently quoted as the surviving cell with 90 t per mission and 14.5-year round trip. **The matrix should add a "P(reactor available by demonstrator window)" conditioning column** (this round provides the numbers in `matrix_overlay.json`) **and acknowledge expected delivered mass under that overlay is 0.01–0.12 t per mission across the three priors.** The orchestrator's choice between the three matrix presentation options (conditional with explicit weight; programmatic-risk-adjusted; window-extended) is a presentation decision, not a technical one.
- **Negative for `ICEBERG-pitch.md`'s patience-capital framing.** R-power-base-rate's Revisit already flagged this; this round confirms the same direction across priors. Expected delivered mass per mission integrated over reactor uncertainty is sub-tonne under every prior. Either the pitch reframes around extended-horizon (post-2040) economics, or it surfaces the reactor-program dependency as the load-bearing risk.
- **Positive for any future R-non-fission-baseline round.** The expected delivered mass integrated over reactor uncertainty is a meaningful baseline that solar-electric (or other non-fission) architectures need to exceed only at the few-tonne level, not the 90-tonne level — substantially lowering the bar for non-fission alternatives to be economically interesting.
- **Methodology issue elevated to recurring lesson:** "chained-multiplicative pre-registrations are systematically over-bullish if each factor is ranged from intuition." Second instance in two rounds. Add to a campaign-level lessons file when the orchestrator next sweeps.
- **For the next two rounds in this hyperion-2 batch (R-megawatt-relaxed-specific-power, R-variant-B-500kWe-sizing):** both produce conditional-on-reactor numbers. Either or both can quote this round's matrix overlay to put the reactor-availability conditioning weight on paper alongside the technical-conditional results. Pre-registration of those rounds should include the matrix overlay propagation step explicitly to avoid recurring-lesson-#N a third time.

