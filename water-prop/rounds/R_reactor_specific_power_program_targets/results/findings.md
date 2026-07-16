# R-reactor-specific-power-program-targets — findings.md

**Author:** rhea
**Date:** 2026-05-15 (latest+8)
**Inputs:** four enceladus-r5 closure tables; R-power-bayesian-update three-prior bracket; this round's pre-registered conditional priors.

---

## Hypotheses adjudicated

| H | predicted | measured | status |
|---|---|---|---|
| H1 | min sp at L0-05 strict (15-yr) Hohmann cruise = 50–65 W/kg (extrapolated; no in-envelope point closes) | 57.0 W/kg via burn-time-scales-1/sp; in-envelope closure = False at every (sp, X, L) tested | **HELD** |
| H2a | min-point at X=0 km/s aerocapture = `(8 W/kg, 10 yr)` | surface_min_X at sp=8, L=10 = 0.0 km/s | **HELD** |
| H2b | min-point at X=5 km/s aerocapture = `(6 W/kg, 15 yr)` | surface_min_X at sp=6, L=15 = 5.0 km/s | **HELD** |
| H2c | min-point at X=10 km/s aerocapture = `(5 W/kg, 15 yr)` and `(6 W/kg, 10 yr)` | both confirmed at surface_min_X = 10.0 km/s | **HELD** |
| H3 | joint posterior at H2a min-point ∈ [0.2%, 1.0%] across three-prior bracket | uniform 0.667%, skeptical 0.218%; bracket [0.22%, 0.67%] | **HELD** |
| H4 | joint posterior at H2c-alt `(6, 10, X=10)` min-point ∈ [0.5%, 1.7%] uniform | uniform 1.602% | **HELD** (at upper edge) |
| H5 | best full conjunction posterior across all min-points × priors ≤ 0.20% | best = 0.167% (H2a @ uniform) | **HELD** |
| H6 | program-class at conservative anchors = technology-demonstrator-only | best conjunction 0.167%; no row > 10% | **HELD** |
| H7 | program NPV(0) structurally negative across all min-points × priors | max NPV(0) = $-132.5B; 0 of 12 rows with positive NPV(0) | **HELD** (emphatic) |

**Aggregate: 9 of 9 sub-claims HELD.** No falsifications. The pre-registration BOE — anchored on the constraint surface extracted from R-reactor-lifetime regrade, the H1 extrapolation arithmetic, and the R-power-bayesian-update three-prior bracket — survived contact with the joint computation. Per methodology lesson 1, the pre-registered ranges were comparative and BOE-anchored; per lesson 10, the program-level NPV check was the load-bearing distinction, not per-mission cashflow.

---

## Headline

**There is no reactor-program profile inside the ICEBERG demonstrator window 2032–2035 that puts a surviving cell in the matrix at any return-seeking-capital threshold.** The conjunction posterior at the cheapest survivable point (H2a: 8 W/kg specific power, 10 yr cumulative lifetime, no aerocapture credit required, uniform prior on US fission orbit by 2035) is **0.167%**. The conjunction-weighted expected delivered mass at that point is **70 kg per mission**. Program NPV(0) over a 25-mission, 25-year campaign at $2.5M/tonne BEST_CELL clearing price is **$-132.5B**. No row in the synthesis table — across H2a/H2b/H2c/H2c_alt min-points × three R-power-base-rate priors × the credit-laddered engineering conjunction — produces positive NPV(0). The matrix is empty under every defensible composite assumption.

---

## Reading

The matrix decision-point #1 (program-class commitment) has a clean answer at conservative anchors: **technology-demonstrator is the only honest program-class.** The conditioning weight is the load-bearing finding. If the project is conditional on a reactor program that hits 8 W/kg specific power and 10-yr cumulative full-power lifetime, the conditional propulsion-physics closure at L0-05 ≥ 25-yr waiver is achievable — but the conditioning weight is ~0.7% under the most charitable defensible prior. The hyperion R-power-bayesian-update finding ("chained-multiplicative collapse erases the surviving Variant B cell") is corroborated here at a different min-point. Variant B's 500 kWe / 14.5-yr-round-trip cell was 1% conjunction-weighted; this round's "best replacement min-point" for the L0-05-≥-25-yr-waiver Architecture-E successor is 0.17% conjunction-weighted. **The campaign's chained-conjunction floor sits in the 0.1–1% range across every reactor-program-target point investigated.**

The cheapest min-point (H2a) does not require aerocapture closure — that's why its conjunction posterior is highest. The credit-laddered aerocapture prior (0.20 marginal at X ≥ 10 km/s closure) is more expensive than the lifetime/specific-power lift from H2a's `(8, 10)` to H2c-alt's `(6, 10)`. Counter-intuitively, **the path with the highest conjunction posterior is the one that does NOT depend on hybrid-aerocapture-aerobraking closing.** This inverts a project-default reading that hybrid-aerocapture is the architectural-recovery candidate; from this round's posterior table, hybrid-aerocapture-aerobraking closure is a *downside* engineering dependency at every aerocapture-required min-point because the credit-laddered prior multiplies into the conjunction without sufficient compensating reactor-prior lift.

The H1 extrapolation (~57 W/kg specific power at L0-05 strict 15-yr) sits beyond the TRL-2 paper aspiration (40 W/kg) and 24× KRUSTY-anchored flown heritage (2.4 W/kg). The Hohmann-cruise assumption is doing some work here — fast-cruise relaxation (hyperion R-cruise-time-optimization unintegrated for Architecture-E successor cells) could reduce the strict-15-yr floor to perhaps 30–40 W/kg, still well above any flown anchor. **L0-05 strict is structurally unreachable at conservative anchors regardless of the engineering closures.** The L0-05 waiver to ≥ 25-yr (project-owner decision point #2) is necessary for any cell to exist at any reactor-program profile this round investigates.

H7 is the load-bearing structural finding: the **conjunction-weighted expected delivered mass is sub-100-kg per mission across every (min-point × prior) combination.** At $2.5M/tonne BEST_CELL clearing, per-mission revenue is sub-$0.2M against per-mission cost of ~$5B (ship CapEx + Starship-anchored launch). The clearing-price assumption almost doesn't matter — even a 100× lift to $250M/tonne keeps per-mission revenue sub-$20M against $5B/mission cost. The program is structurally CapEx-dominated, not revenue-dominated, at every reasonable conjunction-weighted expected mass. **The matrix's "return-seeking-capital framing" is now structurally ruled out at conservative anchors — sovereign-grant class only, no return required, technology-demonstrator framing is mandatory for any defensible pitch.**

---

## Cross-learning

1. **Corroborates R-power-bayesian-update (hyperion).** The "chained-multiplicative collapse" finding generalizes: every reactor-program-target point investigated in this round shows the same 100×–1000× collapse from conditional-on-reactor delivered-mass to programmatic-risk-adjusted expected mass. Not just Variant B at 500 kWe (~1% conjunction → 0.12 t expected); also H2a `(8, 10)` Architecture-E-successor (~0.17% conjunction → 0.07 t expected). The pattern is **not architecture-specific** — it's a property of the campaign's reactor-program prior under any defensible single-prior choice.

2. **Updates R-architecture-D-cost (rhea, this session, prior round).** R-architecture-D-cost found Architecture D structurally money-losing at zero discount under every conservative anchor swept (48 cells, NPV(0) max -$16.1B). This round finds Architecture-E-successor min-points NPV(0) max -$132.5B. The Architecture D vs E comparison is now: D is NPV-negative because of conditional cost > revenue at conditional anchors; E-successor is NPV-negative because of *unconditional* expected revenue ≈ 0 due to conjunction collapse. Different mechanism, same direction. The matrix should not present "Architecture D vs E" as a choice between two viable options — both are structurally negative at conservative anchors, by different mechanisms.

3. **Counter-intuitive engineering-priority update.** Hybrid-aerocapture-aerobraking is currently the matrix's "sole architectural-recovery candidate" on axis 02. This round shows its closure is a *liability* at every aerocapture-required min-point — the credit-laddered prior cuts conjunction posterior below the no-aerocapture H2a path. **Engineering priority should re-rank** if the goal is maximising conjunction posterior: the "no-aerocapture" lifetime-and-specific-power path is the highest-conjunction recovery candidate at conservative anchors.

4. **The matrix's "L0-05 strict vs ≥ 25-yr waiver" decision point is now decisively waiver.** Strict requires extrapolation to ~57 W/kg; waiver requires ~8 W/kg + 10-yr lifetime. The 5–7× specific-power gap between these two is qualitative, not incremental: strict requires technology that doesn't exist on any roadmap, waiver requires technology that exists in FSP Phase-1 paper aspirations. If the project owner does not waive L0-05 to ≥ 25 yr, the matrix has no answer at conservative anchors.

5. **Methodology lesson candidate #11 (new):** **When pre-registering against a SCOPE that asks for an answer at a specific (X, Y) point, inspect the input-data closure surface BEFORE accepting the SCOPE's prediction.** The SCOPE's H2 at `(5 W/kg, 10 yr, X=10)` was internally inconsistent with the input data the SCOPE referenced; the constraint surface shows (5, 10, X=10) has 0 cells closing. A SCOPE deviation that's caught at the STUDY.md stage is cheap; one caught in run.py grading is expensive; one missed entirely is a pre-registration validity failure. **Worker should always grade the SCOPE against the primary input data before drafting hypotheses.**

---

## Next-round candidates

Given H6 is HELD (technology-demonstrator-only is the honest reading at conservative anchors), the natural next rounds are:

1. **R-technology-demonstrator-conops-framing.** Convert the campaign's pitch posture from "regulated-utility-class infrastructure" to "technology-demonstrator with sovereign-grant funding." Re-derive ICEBERG-pitch.md (currently a venture-class retire-in-progress) anchored on technology-demonstrator. Anchors: this round's H6 reading; rhea R-heterogeneous-cadence's staged-commitment finding; titan-2 R-conops-skeleton's clean-room rebuild. **Project-owner decision needed before opening.**

2. **R-no-aerocapture-recovery-path-engineering.** This round surfaces the counter-intuitive "no-aerocapture H2a path has highest conjunction." But H2a is only meaningfully accessible if R-bring-rendezvous-survivability closes (the 25% engineering prior dominates). Worth a round that asks: given the no-aerocapture H2a min-point as the architectural recovery candidate, what are the engineering requirements on B-ring rendezvous survival (the load-bearing 25% prior)? **Independent of hybrid-aerocapture-aerobraking entirely.**

3. **R-fast-cruise-trajectory-impact-on-strict-L005.** Hyperion R-cruise-time-optimization (Variant C) found 3–6 yr fast-cruise savings; this finding is unintegrated for Architecture-E-successor cells. H1's 57 W/kg extrapolation assumes Hohmann cruise. A fast-cruise re-derivation might reduce the strict-15-yr floor to ~30–40 W/kg, which is still TRL-2 paper-aspiration but closer to a plausible reactor-program target.

4. **R-non-US-reactor-program-sensitivity.** Out-of-scope for this round but flagged: China (CASC megawatt-class paper-target by 2040), historical Russia (Project Zeus). A non-US reactor in the demonstrator window would lift the joint posterior, but adds geopolitical-procurement uncertainty (and ICEBERG's pitch posture is US-anchored). Worth scoping as a sensitivity addendum, not a full round.

5. **R-clearing-price-sensitivity-revisit.** H7's NPV finding is structurally insensitive to clearing price (CapEx-dominated). But a sufficiently extreme clearing-price lift (e.g., $25M/tonne for Saturn-source water vs LEO-source) might close the per-mission cashflow gap if mission cadence rises. Worth re-running the H7 NPV at a 10×–100× clearing-price ladder.

6. **R-deliverable-mass-multiplier-from-architecture-pivot.** If chunk-rendezvous architecture stays held but the matrix admits a different deliverable form (e.g., chunk-as-radiator after delivery, chunk-as-reactor-shield for re-use, chunk-as-prop-tank for second mission), the per-mission revenue might lift in ways the current model doesn't capture. Outside this round's scope.

---

## Revisit

Pre-registration accuracy: **9 of 9 sub-claims HELD.** No falsifications. This is the first round in the cumulative rhea record with no falsifications — the SCOPE-deviation discipline (catching SCOPE's H1 and H2 inconsistencies against input data at STUDY.md time) drove the pre-registration to land inside its ranges. Methodology lesson candidate #11 (grade SCOPE against primary input data before drafting hypotheses) is the takeaway.

The H7 NPV finding is structurally CapEx-dominated, which means it's robust to clearing-price assumptions but vulnerable to mission-cadence assumptions. 25 missions over 25 years (one per year) is the campaign's stated cadence; if cadence drops to 0.25 missions/year (one per four years), program revenue collapses further but program NRE doesn't drop proportionally — the NPV gets worse, not better. The model is conservative on the cadence axis.

The conditional probabilities `P(delivers ≥ θ specific power | flies by 2035)` are best-guesses, not measurements. The most load-bearing of these (P(≥ 8 W/kg | flies) = 0.25) could swing the H3 posterior 2× in either direction. Sensitivity sweep is in `run.py` priors block; results not separately reported in this findings.md but available in `synthesis.json`.
