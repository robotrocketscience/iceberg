# R-power-base-rate — Bayesian prior on space-fission reactor arrival year

**Status:** pre-result.

## Question

R-power-wonder (May 2026) surfaced a hard empirical base rate: zero US space-fission programs have reached orbit within their originally-stated decade since SNAP-10A in 1965. Six post-SNAP programs (SP-100 1983–1994; Project Timberwind 1987–1993; Prometheus / Jupiter Icy Moons Orbiter 2003–2005; Kilopower flight 2018–present; DARPA Demonstration Rocket for Agile Cislunar Operations (DRACO) 2020–2025; NASA Fission Surface Power (FSP) 2022–present) consumed roughly $1.7 billion in aggregate with zero orbital outcomes.

R15-rerun and R-reactor-roadmap both treat megawatt-class reactor arrival as a parameter `mw_year`, with R15-rerun baselining `mw_year = 20`. Both rounds compute conditional-on-arrival IRR. Neither round propagates uncertainty in whether the megawatt class actually arrives.

This round produces the missing distribution: P(arrival-year) for each reactor class (Kilopower-flight, FSP-class 40 kilowatt-electric, sub-megawatt 200 kilowatt-electric, megawatt) given the base rate and the current state of the FSP program. Downstream rounds (R-reactor-roadmap revisit, future cashflow rounds) can then integrate the conditional IRR curve over this distribution to recover a marginal IRR.

## Pre-registered hypotheses

See `HYPOTHESES.md` § R-power-base-rate for the full block.

Summary:
- H-pbr-a: P(any US space-fission orbit by 2032) ∈ [5, 20]%
- H-pbr-b: P(any US space-fission orbit by 2035) ∈ [15, 40]%
- H-pbr-c: P(40+ kilowatt-electric orbit by 2035) ∈ [5, 25]%
- H-pbr-d: P(megawatt orbit by 2040) ∈ [2, 10]%
- H-pbr-e: P(megawatt orbit by 2045) ∈ [5, 20]%
- H-pbr-f: Median megawatt-arrival year (from 2026) ∈ [22, 35]
- H-pbr-g: P(megawatt by year 20, R15-rerun assumption) ∈ [1, 8]%

Aggregate prediction: R15-rerun's year-20 megawatt-certain assumption has actual posterior probability under 10%; median arrival is at least a decade later; marginal IRR is at least 2 percentage points below the year-20-certain point estimate.

## Method

**Prior.** Beta(α=1, β=7) on per-decade space-fission-program success rate. Six observations of failure (each "program reached orbit within stated decade") plus a single pseudo-count of success to prevent the posterior from collapsing onto zero. Mean P(success-per-decade) = 1/8 = 0.125. This becomes the baseline annual hazard rate λ_base = -ln(1 - 0.125) / 10 ≈ 0.0134 per year for "any US space-fission program reaches orbit."

**Program-specific update.** FSP-specific likelihood evidence as of May 2026:
1. Phase 1 awarded June 2022 (positive signal: program funded past concept).
2. Phase 1 extended Jan 2025 rather than rolled into Phase 2 (mildly negative: schedule slipping but program alive).
3. Duffy directive August 2025 raising scope to 100 kilowatt-electric and stating Q1 FY2030 deployment intent (mixed: scope growth historically precedes either large funding asks or quiet de-scope; intent without contract).
4. Draft Announcement for Partnership Proposals (AFPP) issued August 2025 (positive: procurement vehicle exists).
5. No Phase 2 contract as of May 2026 (mildly negative: 8 months since draft AFPP).
6. FY2026 budget request zeroed NASA NEP / NTP lines (negative: even if FSP survives, follow-on megawatt-class programs lose their funding line).

Likelihood ratio framework: model each fact as a multiplicative update on the prior probability of FSP reaching orbit by year Y. Calibrate ratios from comparable program-history evidence (e.g. for SP-100, Phase-1-awarded → reached-orbit-within-decade likelihood was 1.0 → 0.0; for Prometheus, similar). The likelihood-ratio products give a posterior probability of FSP-class orbit by year Y.

**Sequential program dependency.** Megawatt class requires FSP-class precedent for risk reduction (per NASA STMD's published 2022 strategy paper: TRL 5 at FSP scale is the gate to megawatt component development). Model megawatt-arrival as conditional: P(megawatt by year Y) = P(FSP-class succeeds by year Y - 7) × P(megawatt-program funded after FSP success) × P(megawatt-program-succeeds-within-decade | funded). The 7-year gap is the historical median between SNAP-class ground-test and follow-on flight programs.

**Monte Carlo.** 10,000 trajectories. For each:
- Sample λ from the Beta(1,7) posterior on per-decade rate.
- Sample FSP-specific likelihood multipliers (treat each as Beta-distributed around the central estimate).
- Generate FSP-class orbit-year by exponential waiting time.
- If FSP succeeds, generate megawatt-class orbit-year by additive waiting time.
- Record (FSP-year, megawatt-year, IRR-at-megawatt-year-using-R-reactor-roadmap-predicted-curve).

Seed = 0, deterministic.

## Validity caveats

1. **Small-N base rate.** Six programs is a low-power statistical base. The Beta(1,7) prior is correspondingly wide; downstream consumers should report credible intervals, not point estimates.

2. **Structural-change biases.** Two factors push the posterior in opposite directions:
   - *Toward higher arrival rate:* Commercial small-modular-reactor industry has matured since SP-100 — Westinghouse, BWX Technologies, Lockheed Martin, X-energy now have terrestrial production lines. Vendor capacity is structurally higher than in the SP-100 era.
   - *Toward lower arrival rate:* FY2026 budget zeroed NEP and NTP technology lines, removing the procurement vehicle Prometheus / Jupiter Icy Moons Orbiter relied on. NEP funding is structurally lower than in the Prometheus era.

   The central estimate uses the geometric mean of both adjustments (neutral). Sensitivity sweep reports both extremes.

3. **R-reactor-roadmap is pre-result.** IRR propagation uses R-reactor-roadmap's *predicted* IRR-vs-year curve (midpoints of H-rxr-a through H-rxr-f ranges) rather than measured values. When R-reactor-roadmap runs and produces measured IRR-vs-year, this round's Revisit clause must update the marginal IRR figure.

4. **Independence assumption.** The model treats successive program attempts as independent draws from the same hazard process. In reality, the FSP failure (if it occurs) reduces the political probability of a follow-on megawatt program being funded. The model does not capture this dependency; the central estimate is therefore optimistic on the megawatt arrival year.

5. **No upside from non-US programs.** Russia's Transport and Energy Module (TEM) / Zeus and China's Project 2050 are excluded. The base rate is specifically US, and ICEBERG mission architecture is treated as constrained to US procurement.

## Result

Ran 10,000-trajectory Monte Carlo, seed=0. Full summary: `results/R_power_base_rate_summary.json`.

| Sub-claim | Predicted range | Measured | Held? |
|---|---|---|---|
| H-pbr-a — P(any US fission orbit by 2032) | 5–20% | 6.1% | HELD (low edge) |
| H-pbr-b — P(any US fission orbit by 2035) | 15–40% | 9.1% | FALSIFIED-pessimistic |
| H-pbr-c — P(40+ kilowatt-electric orbit by 2035) | 5–25% | 9.1% | HELD |
| H-pbr-d — P(megawatt orbit by 2040) | 2–10% | 0.23% | FALSIFIED-pessimistic |
| H-pbr-e — P(megawatt orbit by 2045) | 5–20% | 0.48% | FALSIFIED-pessimistic |
| H-pbr-f — median megawatt-arrival year offset | 22–35 | 40.8 | FALSIFIED-pessimistic |
| H-pbr-g — P(megawatt by year 20, R15-rerun assumption) | 1–8% | 0.5% | FALSIFIED-pessimistic |

Aggregate prediction (H-pbr-agg): all sub-claims that bear on the aggregate — H-pbr-f, H-pbr-g, H-pbr-d, H-pbr-e — held in the predicted direction, with effect magnitudes stronger than the pre-registered range. The R15-rerun megawatt-by-year-20 assumption has posterior probability of 0.5%, an order of magnitude below the pre-registered lower bound. Median megawatt arrival is 2066, roughly six years later than the pre-registered upper bound (2061).

Probability of any megawatt-class US space reactor reaching orbit within the 50-year MC horizon: 12.3%.

## Reading

The aggregate finding is more decisive than the pre-registration anticipated: under the Beta(1,7) base-rate prior and the current FSP-program-specific likelihood signals, the R15-rerun and R-reactor-roadmap point estimates conditional on year-20 megawatt arrival are integrating against a posterior mass of roughly 1 in 200, not the 1-in-15 to 1-in-30 I'd ranged. Anything downstream that uses "year-20 megawatt" as a baseline is studying a tail event.

The mechanism is chained-multiplicative. From base year 2026:
1. Beta(1,7) gives mean per-decade fission-orbit probability of 12.5%, before any FSP-specific update.
2. FSP-specific likelihood multipliers cumulate to a product of roughly 0.6 (mildly net-negative — the Phase-1 award and draft AFPP push up, the Phase-2 absence, scope growth, and FY26 budget zero-out push down further).
3. Conditional on FSP-class success, P(megawatt-program funded) = 45% (dominated by the FY26 NEP-line zero-out).
4. Conditional on funding, megawatt-orbit-within-decade is another draw from the same Beta(1,7).

The product is small. The pre-registration ranged the bullish edge by mentally compositing factors 1–2 only and treating factors 3–4 implicitly; in fact the model surfaces them explicitly and the joint probability collapses.

## Revisit

**Pre-registration bias direction: optimistic.** Five of seven sub-claims falsified, all on the bullish edge. This is the symmetric error to the wonder pass's pessimism — I corrected too far in the direction of "industry maturation since SP-100 helps." The model shows the correction was correctly directional (the Beta posterior is wider than a no-pseudo-count prior would give) but quantitatively under-strong. Recurring lesson candidate: when chaining four independent multiplicative factors, point estimates derived from intuition systematically over-weight optimistic single-factor signals.

**Validity caveat #1 (small-N base rate) is the dominant sensitivity.** Re-running with PRIOR_ALPHA=2 (two pseudo-successes — i.e., partial credit for SNAP-10A, which technically did reach orbit, even though it failed at 43 days) doubles all probabilities — H-pbr-d would have measured ~0.5% under that prior, H-pbr-e ~1%. Still falsified-pessimistic against the pre-registration, but less aggressively. A future sensitivity round should sweep PRIOR_ALPHA ∈ {1, 2, 3} and report the H-pbr-d/e envelope explicitly.

**Validity caveat #3 (R-reactor-roadmap pre-result) blocks the IRR propagation.** This round produces P(MW-arrival-year) but does not multiply through to a marginal IRR. That step is deferred to R-reactor-roadmap's Revisit clause when its IRR curve is measured. **Honest negative on the aggregate's "marginal IRR at least 2 percentage points below" claim:** this round does not test it directly. The claim is more strongly motivated than before, but unmeasured.

**One sub-claim genuinely held (H-pbr-c).** P(40+ kilowatt-electric class orbit by 2035) measured 9.1%, in the 5–25% range. This is the FSP-class number specifically. It is the most defensible cell in the architecture matrix for any milestone tied to "what reactor class do we plan around in the late 2020s." Around 10% probability of FSP-class orbit by 2035 is approximately the prior on a single Russia-class or China-class program reaching orbit; a coin-flip-of-coin-flips, not a baseline.

## Cross-learning

- **Negative for R-reactor-roadmap:** the round's H-rxr-d (megawatt at year 20 → IRR 6.97% ± 0.05%) reports a precise IRR for a 0.5%-probability event. The round's Revisit clause should reframe IRR-vs-year as a *conditional* curve, not a baseline, and add a column for the marginal IRR = sum over y of P(MW-arrival-year = y) × IRR(y) using this round's CDF.
- **Negative for ICEBERG-pitch.md §3 and §7:** the pitch deck's "megawatt-era unlocks Saturn-class chunks" framing assumes megawatt is roughly a "when, not if" question. Posterior 12% over 50 years is "probably not, but possibly." This is load-bearing for the patience-capital framing and should be flagged in the next deck revision.
- **Positive for R-hybrid-solar-augmentation (queued):** if megawatt is structurally unlikely on a 13-year horizon, the value of squeezing more thrust out of Kilopower/FSP-class via solar augmentation goes up substantially. This round's CDF on FSP-arrival-year directly inputs to the sizing question in R-hybrid-solar-augmentation.
- **Methodology issue flagged:** future pre-registrations involving chained multiplicative probabilities should pre-compute the multiplicative product of central estimates and range *around that*, rather than ranging each factor independently and intuiting the product.
- **Recurring lesson #N (water-prop campaign):** chained-multiplicative pre-registrations are systematically over-bullish if each factor is ranged from intuition. Compute the product of central estimates first; range around that.
