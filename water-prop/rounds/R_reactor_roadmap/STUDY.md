# R-reactor-roadmap — marginal internal-rate-of-return integrated over reactor-arrival distribution

**Status:** pre-result (second pre-registration, after retirement of the original).

## Pre-registration history

The original R-reactor-roadmap pre-registration (committed earlier in the campaign) swept megawatt-arrival year ∈ {8, 10, 12, 15, 18, 20, 22, 25, 28, 30} and asked at what year internal-rate-of-return crossed the regulated-utility hurdle (8%). It was built on two upstream inputs that subsequent rounds falsified:

1. **Per-ship megawatt-class deliverable mass = 588 tonnes** (from `R15_rerun_audited`). This number was computed under the `decomposed_mid` reactor-mass model, which R-megawatt-marvl-radiator showed is **optimistic-wrong at megawatt scale** by 3.6× (1 megawatt-electric tug under MARVL anchoring is 104.9 tonnes, not 29.2 tonnes; matches the `bundled_10_W_per_kg` formula to within 0.1 tonne). At MARVL realism, the 1 megawatt-electric all-electric end-to-end architecture **delivers −34.4 tonnes** (chunk cannot fuel its own return). The 588-tonne number is therefore the load-bearing falsified input.
2. **Megawatt-arrival-year is a free parameter to sweep without weighting.** R-power-base-rate measured the posterior probability of the original baseline (megawatt by year-20) at **0.5%**, an order of magnitude below the lowest pre-registered range. Median megawatt arrival offset is 40.8 years; probability of megawatt-class ever arriving in a 50-year horizon is 4.85%. The conditional-on-arrival internal-rate-of-return curve was therefore integrating against a tail event.

The original sub-claims H-rxr-a through H-rxr-i are retired. They were testing the right shape (does internal-rate-of-return improve with earlier megawatt arrival?) on the wrong cashflow assumptions and without weighting the arrival probability.

This re-pre-registration replaces them with H-rxr2-a through H-rxr2-g, structured around two questions: **(A)** what does the conditional internal-rate-of-return curve look like under MARVL-anchored per-ship deliverable mass, and **(B)** what is the marginal internal-rate-of-return integrated over R-power-base-rate's reactor-arrival distribution?

## Question

(A) **Conditional curve.** Take R15-rerun's cashflow framework, swap its `decomposed_mid` per-ship chunk-delivery numbers for MARVL-anchored numbers consistent with R-megawatt-marvl-radiator's findings, and recompute internal-rate-of-return as a function of megawatt-arrival-year ∈ {8, 12, 15, 20, 25, 30, never}. The "never" branch is the surviving architecture cell — chemical-kick + electric-inbound at 500 kilowatt-electric saturation — running indefinitely.

(B) **Marginal internal-rate-of-return.** Integrate the conditional curve against R-power-base-rate's measured megawatt cumulative-distribution-function. Define:

  marginal-internal-rate-of-return = sum over y of [ P(megawatt arrives at year y) × internal-rate-of-return(megawatt-at-year-y) ]
                                   + P(megawatt never arrives in horizon) × internal-rate-of-return(no-megawatt branch)

The conditional curve is what R15-rerun and the original R-reactor-roadmap were implicitly producing. The marginal curve is what an investor with R-power-base-rate's prior actually faces.

## Pre-registered hypotheses (H-rxr2)

**Aggregate (H-rxr2-agg):** Under MARVL-anchored mass + R-megawatt-marvl-radiator's falsification of year-20+ all-electric end-to-end, the conditional-on-arrival internal-rate-of-return curve is **substantially flatter** than the original R-reactor-roadmap's pre-registration assumed, and the marginal internal-rate-of-return (integrated over R-power-base-rate's arrival cumulative-distribution-function) is **below the regulated-utility hurdle of 8% across every tested cell**, including the best-case audited cell ($10,000 per kilogram, $2 billion sovereign at year 11, commercial_mid ship cost). Reactor-roadmap timing is not the dominant internal-rate-of-return lever it appeared to be in the conditional view; it shrinks to second-order once the arrival distribution is applied.

**Sub-claims** (best-case audited cell, with perpetuity terminal value at growth = 0, 45-year horizon, unless noted):

| Sub-claim | Description | Predicted | Falsification |
|---|---|---|---|
| H-rxr2-a | Per-ship chunk delivery at megawatt class, MARVL anchored, chemical-kick + electric-inbound architecture | 100–200 t/ship (saturating around 500 kilowatt-electric, since architecture floor is 500 kilowatt-electric and additional reactor power adds tug mass with limited delivery benefit) | outside [80, 250] t |
| H-rxr2-b | Conditional internal-rate-of-return, megawatt at year 8, MARVL mass | 6.5–8.5% | outside ±1.0 percentage points |
| H-rxr2-c | Conditional internal-rate-of-return, megawatt at year 20, MARVL mass | 4.0–6.0% | outside ±1.0 percentage points |
| H-rxr2-d | Conditional internal-rate-of-return, megawatt never (chemical-kick saturated only) | 3.0–5.0% | outside ±1.0 percentage points |
| H-rxr2-e | Year at which conditional-on-arrival internal-rate-of-return crosses 8% under MARVL mass | never, or only at megawatt-year ≤ 5 (essentially immediate) | falsification if crossover at megawatt-year ∈ [6, 20] |
| H-rxr2-f | Marginal internal-rate-of-return (integrated over R-power-base-rate's measured megawatt cumulative-distribution-function) | 3.0–5.0% | outside ±1.0 percentage points |
| H-rxr2-g | Marginal-internal-rate-of-return uplift from a maximally-aggressive reactor program (shift the megawatt cumulative-distribution-function so median arrival drops from 40.8 yr to 10 yr) over the baseline R-power-base-rate cumulative-distribution-function | 0.3–1.5 percentage points | outside ±0.5 percentage points |

**Aggregate decision rule:**

- If H-rxr2-e holds (conditional internal-rate-of-return never crosses 8% under MARVL mass within a plausible megawatt-arrival window), the regulated-utility-eligibility framing R-NPV and R-cadence both implicitly held open as an upside path is **closed** under conservative reactor mass.
- If H-rxr2-f and H-rxr2-g hold (marginal internal-rate-of-return is sovereign-bond territory regardless of program ambition), the architecture-program-risk column in the architecture matrix needs to carry a **marginal internal-rate-of-return** figure, not a conditional figure. Anything downstream that uses a single internal-rate-of-return point estimate is reporting a tail event probability-weighted at less than 5%.

## Method

### Inputs from upstream rounds

**MARVL-anchored per-ship deliverable mass** (replaces R15-rerun's `AUDITED_CHUNK_DELIVERED_T` table). Per R-megawatt-marvl-radiator H-mr-d (closure floor for chemical-kick + electric-inbound architecture is 500 kilowatt-electric, delivered 128.8 tonnes at 14.51-year round trip) and H-mr-e (no realistic-mass-model megawatt all-electric cell closes inside L0-05 at any tested operating point), the per-era per-ship chunk delivery is:

| Reactor era | Reactor power | Architecture survives at MARVL mass? | Delivered chunk per ship |
|---|---:|---|---:|
| Kilopower | 10 kilowatt-electric | no — chemical-kick architecture's floor is 500 kilowatt-electric | 0 t (mission fails) |
| Fission Surface Power | 40 kilowatt-electric | no — under MARVL anchor | 0 t |
| stretch | 100 kilowatt-electric | no — under MARVL anchor | 0 t |
| sub-megawatt | 200 kilowatt-electric | no — chemical-kick at 200 kilowatt-electric closes at 16.12 yr, exceeding L0-05's 15-year ceiling | 0 t |
| 500-kilowatt-electric chemical-kick | 500 kilowatt-electric | **yes** — sole defensible cell | **128.8 t** |
| megawatt class | 1000 kilowatt-electric | all-electric end-to-end **falsified** at MARVL; chemical-kick variant assumed to saturate near 500-kilowatt-electric's delivery curve | **128.8 t** (held flat from 500 kilowatt-electric; see validity caveat) |

This is the load-bearing change. R15-rerun had `MW_500kWe → 588 t` (a 5× delivery jump from sub-megawatt's 294 t). Under MARVL anchoring there is **no delivery jump at megawatt class**. The curve is flat from 500 kilowatt-electric onward, and missions launched before 500-kilowatt-electric availability deliver zero chunk.

**Reactor-era arrival schedule.** Generalize R15-rerun's `reactor_era_for_launch_year()` to slide all era arrivals with megawatt-arrival year, preserving relative spacing:

    megawatt-arrival-year      = parameterized in {8, 12, 15, 20, 25, 30, infinity}
    500-kilowatt-electric-year = megawatt-arrival-year - 3   (chemical-kick architecture floor; 500 kilowatt-electric precedes megawatt by a small gap)
    sub-megawatt-year          = megawatt-arrival-year - 5
    stretch-year               = megawatt-arrival-year - 8
    Fission-Surface-Power-year = megawatt-arrival-year - 13
    Kilopower-year             = 0

For the "megawatt-never" branch, set megawatt-arrival-year = infinity and 500-kilowatt-electric-year to a default (year 12, matching R-power-base-rate's FSP-class central estimate of 9.1% by year 9 → roughly half-mass by year 12). The mission only begins delivering chunks once the 500-kilowatt-electric era arrives.

**Reactor-arrival cumulative-distribution-function.** Pull megawatt-class arrival cumulative-distribution-function from `rounds/R_power_base_rate/results/R_power_base_rate_summary.json`. Use the measured `mw_cdf_by_year_offset` directly.

### Cashflow model

Reuse R15-rerun's cashflow_model() framework, except:

- Replace `AUDITED_CHUNK_DELIVERED_T` with the MARVL-anchored table above.
- Compute per-launch era from the parameterized `reactor_era_for_launch_year(launch_year, mw_arrival_year)`.
- For "megawatt-never" branch: never assign megawatt era; cap at 500-kilowatt-electric.

Compute internal-rate-of-return per cell via bisection on discount rate to find net-present-value = 0 (matching R-NPV's approach), with perpetuity terminal value at growth = 0 (R-NPV's H-NPV-aggregate held with terminal value).

### Marginal-internal-rate-of-return integration

Given the conditional internal-rate-of-return curve `irr(megawatt-arrival-year)` and R-power-base-rate's `P(megawatt-arrives-by-y) - P(megawatt-arrives-by-(y-1)) = density at year y`:

    marginal-internal-rate-of-return = sum over y in {1, 2, ..., 50}: density(y) × irr(y)
                                     + (1 - sum_y density(y)) × irr_no_megawatt

Use the cumulative-distribution-function from R-power-base-rate verbatim.

### Aggressive-program counterfactual

For H-rxr2-g, construct a "maximally-aggressive" reactor cumulative-distribution-function by shifting R-power-base-rate's megawatt cumulative-distribution-function so the median offset moves from 40.8 years to 10 years (4× compression). Re-integrate the marginal curve against the shifted cumulative-distribution-function. Compare against the baseline marginal internal-rate-of-return; the difference is the upper bound on internal-rate-of-return uplift available from a reactor-program acceleration.

## Validity caveats

1. **Chemical-kick + electric-inbound delivery held flat from 500 kilowatt-electric to megawatt class.** R-megawatt-marvl-radiator tested only the 500-kilowatt-electric closure for the chemical-kick architecture; it did not sweep 500–2000 kilowatt-electric in that architecture. The flat assumption is a structural simplification: higher reactor power adds tug mass under MARVL anchoring at roughly 0.1 tonne per kilowatt-electric, but it also reduces burn time. A follow-on round (R-chemical-kick-power-optimum) could measure this directly. The flat assumption is conservative on the "more reactor power = more delivery" framing R15-rerun used.

2. **500-kilowatt-electric arrival modeled as megawatt-arrival-year minus 3.** This is an architectural guess; R-power-base-rate did not separately model 500-kilowatt-electric arrival. A two-axis sweep (500-kilowatt-electric-year × megawatt-year) would be more rigorous; deferred.

3. **No-megawatt branch sets 500-kilowatt-electric-year = 12.** This is a single-point estimate matching the R-power-base-rate FSP cumulative-distribution-function shape; a proper integration would integrate over the 500-kilowatt-electric arrival distribution too. The single-point assumption is conservative-optimistic — it gives the no-megawatt branch a fixed start year rather than a probabilistic one.

4. **R-power-base-rate's cumulative-distribution-function uses base year 2026.** All "year-X" in this round means offset from 2026.

5. **The 500-kilowatt-electric reactor itself has no funded path.** R-megawatt-marvl-radiator notes this is 5× Fission-Surface-Power Phase 2 scope, and R-power-wonder finding 3 documented that even Phase 2 has not been awarded. The marginal-internal-rate-of-return calculation in this round folds the architectural feasibility into the megawatt-arrival distribution — that is, P(500-kilowatt-electric class) is implicitly ≥ P(megawatt class). This is the right direction (500-kilowatt-electric is easier than megawatt) but the cumulative-distribution-function used here is the megawatt one, which is **more pessimistic** than a 500-kilowatt-electric-specific distribution would be. The marginal internal-rate-of-return computed here is therefore a **lower bound**; a 500-kilowatt-electric-specific cumulative-distribution-function would lift it modestly.

6. **Conditional-on-arrival internal-rate-of-return uses MARVL-anchored decomposed model.** R-megawatt-marvl-radiator showed this matches the bundled `5 tonne + reactor_kilowatt-electric × 0.1 tonne` formula within 0.1 tonne at 1 megawatt-electric. The decomposed model gives slightly cleaner mass decomposition for the cashflow tug-cost line, but the bundled formula would give equivalent results.

7. **The 0.5% probability of megawatt by year 20 from R-power-base-rate may itself be an underestimate.** R-power-base-rate's H-pbr-d through H-pbr-g all measured pessimistic-falsifications against pre-registered ranges; the round's Revisit clause flagged that PRIOR_ALPHA=2 (giving partial credit to SNAP-10A) would roughly double all probabilities. A sensitivity round could re-run with PRIOR_ALPHA=2. For this round I use the published PRIOR_ALPHA=1 cumulative-distribution-function verbatim.

## Result

Ran `run.py` with deterministic inputs. Full output: `results/roadmap.json`.

### Conditional internal-rate-of-return curve — best-case audited cell ($10,000 per kilogram, $2 billion sovereign at year 11, commercial_mid ship cost), with perpetuity terminal value at growth = 0

| Megawatt arrival year | Conditional internal-rate-of-return |
|---:|---:|
| 8 | 1.61% |
| 10 | 1.64% |
| 12 | 1.45% |
| 15 | 1.26% |
| 18 | 1.13% |
| 20 | 1.06% |
| 22 | 1.00% |
| 25 | 0.96% |
| 28 | 0.89% |
| 30 | net-present-value < 0 at 0.01% discount (no positive internal-rate-of-return) |
| never (chemical-kick 500-kilowatt-electric saturated) | 1.48% |

### Conditional internal-rate-of-return curve — conops-baseline cell ($2,000 per kilogram, no sovereign, commercial_mid)

Every megawatt-arrival year, including the "never" branch, has net-present-value negative at 0.01% discount rate. No positive internal-rate-of-return exists at any tested megawatt-arrival year. The cell does not close at any sensitivity within the tested envelope.

### Marginal internal-rate-of-return (best-case audited cell)

| Branch | Value |
|---|---:|
| P(never-branch) per R-power-base-rate | 96.72% |
| P(megawatt-branch) | 3.28% |
| Conditional internal-rate-of-return, never-branch | 1.48% |
| Marginal internal-rate-of-return (baseline) | **1.45%** |
| Marginal internal-rate-of-return (aggressive program, median megawatt arrival shifted to year 10) | 1.49% |
| Uplift over baseline from aggressive program | **+0.04 percentage points** |

### Hypothesis grading

| Sub-claim | Predicted | Actual | Held? |
|---|---|---|---|
| H-rxr2-a — Per-ship chunk delivery at megawatt class, MARVL | 80–250 t | 128.8 t | held |
| H-rxr2-b — Conditional internal-rate-of-return at megawatt-year-8 | 6.5–8.5% | 1.61% | **falsified-pessimistic** (off 5 percentage points) |
| H-rxr2-c — Conditional internal-rate-of-return at megawatt-year-20 | 4.0–6.0% | 1.06% | **falsified-pessimistic** (off 3 percentage points) |
| H-rxr2-d — Conditional internal-rate-of-return, never branch | 3.0–5.0% | 1.48% | **falsified-pessimistic** (off 1.5 percentage points) |
| H-rxr2-e — Year at which conditional internal-rate-of-return crosses 8% | never, or ≤ year 5 | never crosses 8% (or 5%, or 2%) | held in direction |
| H-rxr2-f — Marginal internal-rate-of-return, baseline cumulative-distribution-function | 3.0–5.0% | 1.45% | **falsified-pessimistic** (off 1.5 percentage points) |
| H-rxr2-g — Marginal internal-rate-of-return uplift from aggressive program | 0.3–1.5 percentage points | 0.04 percentage points | **falsified** (40× over-estimate) |

**Aggregate (H-rxr2-agg):** held in direction and qualitative shape — reactor-roadmap timing is **not** the dominant internal-rate-of-return lever it appeared to be in the conditional view; marginal internal-rate-of-return sits below the regulated-utility hurdle at every cell. But the magnitude was further pessimistic than pre-registered: the marginal internal-rate-of-return is in **sub-sovereign-bond territory** (1.45%), not the "sovereign-development-discount-rate but at the floor" territory I'd predicted. Five of seven sub-claims falsified, all on the optimistic edge.

## Reading

**The marginal internal-rate-of-return on ICEBERG, under MARVL-anchored mass and R-power-base-rate's reactor cumulative-distribution-function, is 1.45 percent.**

That number is below every commonly-quoted hurdle rate in capital markets, including the 10-year US Treasury yield (~4 percent), investment-grade corporate bond yields (~5 percent), the World Bank International Development Association concessional rate (~2.5 percent), and the regulated-utility allowed return on equity (~9 percent). It is in subsidy territory — pure-grant or strategic-policy funding territory, not return-seeking-capital territory.

R-NPV's headline of "internal-rate-of-return 3.63 to 6.97 percent" was anchored on R15-rerun's 588-tonne megawatt-class delivery number. That number is falsified by R-megawatt-marvl-radiator: under MARVL-anchored mass, the megawatt all-electric end-to-end architecture **does not deliver any chunk at all** (round-trip 19.56 years, delivered −34.4 tonnes). The surviving cell — 500-kilowatt-electric chemical-kick + electric-inbound — delivers 128.8 tonnes per ship at 14.5-year round trip. That is 22 percent of R15-rerun's headline figure, applied across the same fleet schedule. The internal-rate-of-return collapses accordingly.

**The reactor-roadmap timing lever is essentially dead.** Conditional internal-rate-of-return varies only between 0.89 percent (megawatt at year 28) and 1.64 percent (megawatt at year 10) across the entire tested megawatt-arrival window. The 75-basis-point spread across a 20-year arrival range is dwarfed by the spread between MARVL and decomposed-mid mass models, which is several percentage points. **Mass model anchoring is dramatically more leveraged on internal-rate-of-return than reactor-roadmap timing.**

The aggressive-program counterfactual is the most decisive single number in this round. Shifting the megawatt cumulative-distribution-function so the median arrival year drops from 40.8 to 10 (a 4-fold acceleration consistent with an unprecedented federal program priority) raises marginal internal-rate-of-return by **4 basis points** — from 1.45 percent to 1.49 percent. That is an order of magnitude smaller than my pre-registered range and well below any decision-relevant threshold. **Lobbying for an accelerated reactor program is a near-zero-leverage internal-rate-of-return move under conservative mass anchoring.** This inverts R-cadence's conclusion that "reactor-roadmap timing is the dominant exogenous internal-rate-of-return lever" — that conclusion was correct conditional on R15-rerun's mass model, but R-megawatt-marvl-radiator has since revised that mass model, and the leverage evaporated.

**The non-monotonicity in the conditional curve** (peak at megawatt-year 10, not year 8) is a fleet-scheduling artifact, not a substantive finding. At megawatt-year 8 the 500-kilowatt-electric era arrives at year 5; ship 2 at year 7 launches into 500-kilowatt-electric era. At megawatt-year 10, ship 2 launches at year 7, still during 500-kilowatt-electric (which arrives at year 7 = megawatt - 3). The two scenarios end up with substantially overlapping delivery schedules; the small differences are dominated by which year-by-year cashflows land before/after the 45-year horizon and which ones contribute to the perpetuity terminal value. The curve is best read as **roughly flat at 1.0 to 1.6 percent across the entire range**, including the never branch.

**The conops-baseline cell ($2,000 per kilogram, no sovereign) does not close at any sensitivity.** Net-present-value is negative even at a near-zero discount rate under MARVL mass for every tested megawatt-arrival year. The conops document's water-price assumption (~$2,000 per kilogram, derived from terrestrial-fuel-replacement parity) is structurally below the floor required for any non-loss-making operation under conservative reactor mass. Only the premium-pricing cell ($10,000 per kilogram, the upper bound of R15b's sensitivity sweep) plus sovereign purchase produces any positive internal-rate-of-return at all — and even that is 1.45 percent.

**Reframing of the campaign-level financial picture, post-R_reactor_roadmap revision:**

| View | Internal-rate-of-return | Capital class |
|---|---:|---|
| R-NPV headline (R15-rerun mass, conditional on megawatt at year 20) | 6.97% | sovereign-development |
| R-NPV no-terminal-value (R15-rerun mass, conditional) | 3.63% | sovereign-bond |
| **This round, conditional on megawatt at year 20 (MARVL mass)** | **1.06%** | **sub-sovereign-bond** |
| **This round, marginal (MARVL mass, R-power-base-rate cumulative-distribution-function)** | **1.45%** | **sub-sovereign-bond** |
| **This round, marginal with aggressive program** | **1.49%** | **sub-sovereign-bond** |

The "sovereign-development" capital-class framing R-NPV introduced is **retired** under MARVL anchoring. The new framing is: ICEBERG's economic profile is structurally pure-subsidy — neither commercial-equity nor regulated-utility nor sovereign-development is mathematically reachable on the audited cashflow. The only path back to a return-seeking-capital framing requires one of: (a) a successful chunk-as-heat-shield-revisit (collapses ~36 km/s of round-trip delta-velocity, ~quintuples delivered mass per ship), (b) a successful revival of all-electric end-to-end via ultra-low-areal-density radiator technology (footprint Technology-Readiness 2 today), or (c) a substantially-higher per-kilogram water price than $10,000 per kilogram.

## Revisit

H-rxr2-a held cleanly; H-rxr2-e held in direction (no positive crossover with 8 percent exists at any megawatt-arrival year — the falsification window of [-1, 5] was nominally satisfied, but the spirit of the hypothesis was tested correctly). Five of seven sub-claims falsified-pessimistic. The pre-registration was directionally correct (R-rxr2-agg held qualitatively) but quantitatively under-strong by a factor of two to three on every numeric range.

**Pre-registration error pattern:** I had anchored my conditional internal-rate-of-return predictions (H-rxr2-b through H-rxr2-d) on R-NPV's 6.97 percent point estimate, mechanically reduced by ~30 percent to reflect the MARVL mass cut. The actual reduction was ~85 percent. The mechanism I missed: at 22 percent of R15-rerun's per-ship delivery, the fixed costs (demonstrator non-recurring engineering, ship build, launch and trans-Saturn injection, ground operations) plus the dry-tug mass become a much larger fraction of the cashflow on a relative basis, so the internal-rate-of-return is not linearly scaled with revenue — it collapses faster than the revenue collapse.

**This is the third pre-registration with the same shape mistake** (after H-od-d in R-outbound-dv-continuous-thrust and H-mr-d in R-megawatt-marvl-radiator, per rhea's notes): predict numeric ranges from intuition on order-of-magnitude reductions without doing the cashflow arithmetic first. The convention from rhea — "pre-register numeric ranges only after running the back-of-envelope calculation, not before" — applies here too. The pre-registration could have been tightened to 1.0–2.5 percent on H-rxr2-b through H-rxr2-d if I had run a single back-of-envelope cashflow before locking the hypothesis.

**The single sub-claim that nearly fell outside its falsification window was H-rxr2-e** at the spirit-of-the-hypothesis level. I had predicted "8 percent crossover never reached, or only at megawatt-year ≤ 5." The actual conditional internal-rate-of-return curve does not approach 8 percent at any megawatt-arrival year tested. The "0" code-grade with range [-1, 5] is a marker that no crossover was found; the substantive read is that conditional internal-rate-of-return is bounded above by 1.64 percent across the entire window. Even the upper-bound aggressive program (megawatt at year 8, with terminal value) leaves a 6.4-percentage-point gap between internal-rate-of-return and the regulated-utility hurdle.

## Cross-learning

- **Decision-supporting (load-bearing):** **Retire R-NPV's "sovereign-development discount-rate territory" headline.** Under MARVL-anchored mass, the marginal internal-rate-of-return is 1.45 percent, sub-sovereign-bond. The capital-class framing in `ICEBERG-pitch.md` and `startup/` planning needs a coordinated revision: ICEBERG is structurally pure-subsidy / strategic-policy-funded, not concessional sovereign-development. A pitch that mentions World Bank, Export-Import Bank, or sovereign-development-bank funding needs to acknowledge that the project is below those institutions' typical hurdle rates.

- **Decision-supporting (load-bearing):** **Retire R-cadence's "reactor-roadmap timing is the dominant exogenous internal-rate-of-return lever" conclusion.** Under MARVL anchoring, reactor-roadmap timing moves marginal internal-rate-of-return by ≤ 0.5 percentage points across the entire plausible megawatt-arrival window. Per-ship deliverable mass (which is downstream of architecture + mass model + chunk-mass cap) moves internal-rate-of-return by 4 to 5 percentage points. The dominant lever is now: **per-ship delivery, which is gated by R-chunk-as-heat-shield-revisit** (Earth aerocapture rescue) more than by reactor power. Promote R-chunk-as-heat-shield-revisit to the next named round.

- **Negative for ICEBERG-pitch §3 and §7:** the pitch deck's "megawatt-era unlocks Saturn-class chunks" framing was already weakened by R-power-base-rate's posterior-0.5%-by-year-20 finding. This round goes further: even if megawatt arrives on the original schedule, the all-electric end-to-end cell is falsified at MARVL mass, and the chemical-kick cell does not scale beyond 500-kilowatt-electric. **"Megawatt-era unlocks" is now a falsified premise**, not just a low-probability one. The pitch deck must replace this framing with either (a) chunk-as-heat-shield-rescue-conditional language, or (b) explicit acknowledgment that the project is sub-sovereign-bond.

- **Promotes R-chunk-as-heat-shield-revisit to next round.** Earth aerocapture collapses ~36 kilometres per second of round-trip delta-velocity to aerodynamic passes. Per the architecture matrix, that is the only available rescue path for a year-twenty-plus all-electric end-to-end cell. If chunk-as-heat-shield closes for a ~100-tonne fabric-bagged vehicle (open question per R-chunk-as-heat-shield's original analysis), the delivered chunk per ship at megawatt class could climb from 0 (falsified) to 200 to 500 tonnes, restoring some of the lost internal-rate-of-return. This round predicts that even a 4× delivery uplift (back to ~500 tonnes per ship) would push conditional internal-rate-of-return to roughly 4 to 5 percent — still below the regulated-utility hurdle but in defensible sovereign-bond territory. The round R-chunk-as-heat-shield-revisit should pre-register against that range.

- **Methodology lesson:** when an upstream round (here R-megawatt-marvl-radiator) revises a load-bearing input number by a factor of three to five, the downstream effect on internal-rate-of-return is non-linearly larger because of fixed-cost dilution. Future cashflow rounds with revised per-ship delivery should expect internal-rate-of-return to collapse faster than the revenue collapse, not slower. Add to recurring-lesson log.

- **Methodology lesson (repeated):** pre-register numeric ranges only after running the back-of-envelope calculation, not before. Third occurrence in two days (H-od-d, H-mr-d, this round's H-rxr2-b-through-f). Promote to a hard rule in `PROTOCOL.md` next revision.

- **Validity caveat 5 (R-power-base-rate's 0.5% by year 20 may itself be pessimistic under PRIOR_ALPHA=2)** could shift the marginal internal-rate-of-return calculation modestly. Sensitivity round candidate: re-run this round with R-power-base-rate's PRIOR_ALPHA=2 cumulative-distribution-function. Expected effect: marginal internal-rate-of-return shifts by maybe 0.1 to 0.3 percentage points. Not load-bearing on the headline ("sub-sovereign-bond").

- **Open question for orchestrator integration:** the architecture decision matrix currently lists the 500-kilowatt-electric chemical-kick cell as "the sole defensible deployment cell." This round's internal-rate-of-return for that cell, including all available aggressive levers, is 1.45 percent. The matrix's narrative needs a financial-feasibility column added — propulsion-physically-defensible is no longer the same as economically-defensible. Suggest a new column "marginal internal-rate-of-return at MARVL mass" in the matrix, with this round's number as the entry for the surviving cell.

## Files of record

```
water-prop/rounds/R_reactor_roadmap/STUDY.md
water-prop/rounds/R_reactor_roadmap/run.py
water-prop/rounds/R_reactor_roadmap/results/roadmap.json
```

## Out of scope

- Did not propagate to `ARCHITECTURE-DECISION-MATRIX.md`, `ICEBERG-pitch.md`, `REQUIREMENTS-L1.md`, `RISKS.md`, `startup/` — shared documents, orchestrator-owned.
- Did not run the PRIOR_ALPHA=2 sensitivity on R-power-base-rate. Queued as separate round candidate.
- Did not separately model 500-kilowatt-electric arrival cumulative-distribution-function. Held at megawatt-year minus 3 throughout.
- Did not sweep 500-kilowatt-electric to 2-megawatt-electric in the chemical-kick architecture to test the flat-delivery assumption. Queued as `R-chemical-kick-power-optimum`.
- Did not test the chunk-as-heat-shield rescue branch. Queued as `R-chunk-as-heat-shield-revisit` (promoted to next round).
