# R-reactor-specific-power-program-targets — what reactor-program profile restores any surviving cell?

**Status:** scope, pre-study. Authored by Saturn (orchestrator), 2026-05-15 latest+7, after the five-handoff integration pass that falsified Architecture E and surfaced reactor lifetime as a third independent viability axis.

**Context.** The matrix is empty under every anchor and waiver tested as of latest+7. Three findings from enceladus-r5 rounds 9-12 together pin down where the surviving cell *would* sit if a reactor program existed:

1. **R-arch-E-specific-power-flown-anchored (`62f7079`).** Architecture E does not close L0-05 at any ceiling under KRUSTY-anchored 2.4 W/kg specific power. Round-6's "two mass models" (decomposed_marvl + bundled_10) are mathematically equivalent — the prior sensitivity check was effectively single-model.
2. **R-specific-power-cliff (`2d63291`).** Architecture-E L0-05-closure cliff sits sharply between 7 and 8 W/kg specific power at the 25-year ceiling. At 2.4 W/kg: 0 of 60 cells close. At 7 W/kg: 0. At 8 W/kg: cells begin to close.
3. **R-aerocapture-cliff-shift (`12058b5`).** Inbound aerocapture rescues the 5-8 W/kg specific-power band (closure-cliff min-sp = 8 W/kg at X=0, drops to 5 W/kg at X=10 km/s aerocapture credit). At KRUSTY-anchored 2.4 W/kg, **even closing aerocapture perfectly does not rescue the cell** — the outbound burn becomes the binding constraint.
4. **R-reactor-lifetime-vs-burn-time (`c685c52`).** Every viable Architecture-E cell needs 8-12 years cumulative reactor full-power burn time. KRUSTY 2018 ground-test heritage is 28 hours. 3-4 orders of magnitude short.

The conjunction of these findings says: any reactor program that would put a cell back in the matrix needs to deliver simultaneously (a) specific power above the 5-8 W/kg closure cliff, depending on aerocapture credit, (b) cumulative full-power lifetime in the 10-year range, (c) scope to 500 kWe or higher (axis 05). The known programs are nowhere close.

This round answers: **what is the minimum reactor-program profile that restores any surviving cell to the matrix, and what does the conjunction-probability of that profile delivering inside the ICEBERG demonstrator window 2032-2035 look like under R-power-base-rate-style program-risk priors?**

The round is a *synthesis* round (in the style of R-conops-chunk-vs-ram-scoop or R-power-bayesian-update), not a new physics or economics round. The work is to compose four prior findings into a single joint constraint set and bound the program-risk conjunction posterior.

---

## What the enceladus-r5 rounds said about the joint constraints (PRIMARY-text quotes)

Per methodology lesson 9 (anchor SCOPE on prior aggregate verdict, not cherry-picked sub-finding), anchor on the four enceladus-r5 STUDY.md primary-text Reading sections.

**R-specific-power-cliff (`2d63291`) result table:**

> | specific power (W/kg) | close cells at 25-yr ceiling (of 60) |
> | 2.4 (KRUSTY)          |  0 |
> | 5                     |  0 |
> | 6                     |  0 |
> | 7                     |  0 |
> | 8                     |  cells begin to close |
> | 9                     |  intermediate |
> | 10                    |  full grid closes |

The 7→8 cliff is the load-bearing data — at the architecturally-relevant chunk × reactor envelope, closure happens discontinuously in specific power.

**R-aerocapture-cliff-shift (`12058b5`) cliff-location-at-each-aerocapture-credit table:**

> | aerocapture Δv credit X (km/s) | min specific power for any close-25-yr cell (W/kg) |
> | 0   | 8.0 (round-10 baseline) |
> | 5   | 6.0 |
> | 10  | 5.0 |
> | 20  | KRUSTY 2.4 still infeasible — outbound becomes binding |

Aerocapture rescues the 5-8 W/kg band linearly but flatlines below 5: the outbound burn dominates and aerocapture credit (which is inbound) does not help.

**R-reactor-lifetime-vs-burn-time (`c685c52`) survival-under-lifetime-ceiling table:**

> | reactor lifetime ceiling L (yr) | heritage anchor | surviving cells |
> | 5  | Brayton-flight-rated minimum | only 9-10 W/kg at X≥20 km/s |
> | 10 | Kilopower design target      | ~80% of grid survives |
> | 15 | effectively non-binding      | all close cells survive |
> | 0.003 (KRUSTY 28 hours)         | sole flown anchor | 0 |

The two axes (specific power and lifetime) compound: KRUSTY misses both. Even a hypothetical reactor at 10 W/kg with 28-hr lifetime would not survive lifetime gating; even one at 10-yr lifetime with 2.4 W/kg would not survive specific-power gating.

---

## Question this round answers

For the held chunk-rendezvous architecture (axis 19) at the conservative anchors (latest+7 matrix state), and conditional on R-hybrid-aerocapture-aerobraking and R-bring-rendezvous-survivability both closing (i.e. the architecture's engineering questions are resolved):

1. **What is the minimum (specific power × lifetime × reactor scope) point that puts at least one cell back in the matrix at L0-05 strict?**
2. **What is the minimum point at L0-05 ≥ 25-yr waiver?**
3. **Conditional on R-power-base-rate priors (0-of-6 US space-fission programs reaching orbit since SNAP-10A; FSP Phase 2 not yet awarded), what is the posterior probability that a reactor delivering each candidate (specific power × lifetime × scope) point flies inside the ICEBERG demonstrator window 2032-2035?**
4. **Does the conjunction posterior (reactor delivers AND both engineering rounds close) exceed any meaningful capital-class threshold (technology-demonstrator vs sovereign-grant vs regulated-utility)?**

The round's deliverable is a synthesis table for the project owner: each candidate reactor-program point → flown-anchor distance (in W/kg and years) → posterior probability of delivery in window → joint probability with engineering closures.

---

## Pre-registered hypotheses (numeric ranges + falsification bands)

| # | Hypothesis | Predicted range | Falsification band |
|---|---|---|---|
| H1 | The minimum reactor-program point that puts a cell back at L0-05 strict requires specific power ≥ 8 W/kg AND lifetime ≥ 5 yr cumulative full-power burn. | min-point = (8 W/kg, 5 yr) at L0-05 strict | H1 falsified if min-point is achievable at ≤ 6 W/kg OR ≤ 3 yr lifetime |
| H2 | The minimum reactor-program point at L0-05 ≥ 25-yr waiver requires specific power ≥ 5 W/kg AND lifetime ≥ 10 yr cumulative full-power burn, conditional on R-hybrid-aerocapture-aerobraking closing with ≥ 10 km/s of inbound aerocapture Δv credit. | min-point = (5 W/kg, 10 yr) at waiver + aerocapture-10 | H2 falsified if min-point is achievable at ≤ 4 W/kg OR ≤ 7 yr lifetime, OR if aerocapture credit ≥ 10 km/s doesn't help (per R-aerocapture-cliff-shift outbound-binding finding extrapolated) |
| H3 | Posterior probability that any US fission program flies inside 2032-2035 demonstrator window delivering ≥ 8 W/kg specific power AND ≥ 5 yr cumulative lifetime is ≤ 3 percent under R-power-base-rate priors (0-of-6 base rate; 3-9 percent posterior on any US fission orbit by 2035 per hyperion bracket; conditional probability of "any fission orbit" × "delivers required specific power and lifetime" gives the joint). | joint posterior ≤ 3 percent | H3 falsified if a credible argument puts the joint at > 10 percent |
| H4 | Posterior probability that any US fission program flies inside 2032-2035 demonstrator window delivering ≥ 5 W/kg AND ≥ 10 yr cumulative lifetime is ≤ 1 percent under same priors. | joint posterior ≤ 1 percent | H4 falsified if the joint exceeds 5 percent |
| H5 | Conjunction posterior (reactor-program delivers a viable point AND R-hybrid-aerocapture-aerobraking closes AND R-bring-rendezvous-survivability closes) is ≤ 1 percent under the most optimistic credible reactor-program assumption (H3) and ≤ 0.1 percent under the more pessimistic (H4). The architecture is not financeable on this conjunction probability under any return-seeking-capital structure. | conjunction posterior ≤ 1 percent (optimistic) / ≤ 0.1 percent (conservative) | H5 falsified if either engineering round has independent prior > 50 percent (which would lift the conjunction) |
| H6 | Reading-level conclusion (load-bearing): the program-class decision (matrix decision point #1) at conservative anchors is **technology-demonstrator-only**. Restoring regulated-utility-class framing requires (a) reactor-program targets that no current US program funds, AND (b) two engineering closures that have not run. Until at least one of those constraints relaxes (e.g. a new reactor-program announcement or a positive R-hybrid-aerocapture-aerobraking result), the honest pitch posture remains technology-demonstrator. | reading-level: technology-demonstrator is the honest reading | H6 falsified if any combination of H1-H5 produces a joint posterior > 10 percent for a return-seeking-capital-class cell |

---

## Method sketch (worker drafts the actual computation in `run.py`)

1. **Re-fetch the enceladus-r5 closure_verdict tables** from rounds 6, 9, 10, 11, 12 — `water-prop/rounds/R_{architecture_E_no_saturn_side_electrolysis,arch_E_specific_power_flown_anchored,specific_power_cliff,aerocapture_cliff_shift,reactor_lifetime_vs_burn_time}/results/*.json`. The closure tables are the worker's input; do not re-run propulsion physics.

2. **Compose the joint constraint surface** (specific-power × lifetime × aerocapture-Δv-credit) by overlaying the four closure tables. Identify the minimum point at L0-05 strict (no aerocapture, conservative lifetime) and at L0-05 ≥ 25-yr waiver (with aerocapture credit X = 5, 10, 20 km/s and lifetime L = 5, 10, 15 yr).

3. **Apply R-power-base-rate priors** (hyperion three-prior bracket: 2.9-8.9 percent posterior on any US fission orbit by 2035). Condition on "delivers required specific power" and "delivers required lifetime" — these conditionals can be bounded from known reactor programs (KRUSTY, FSP-Phase-1, SP-100 retrospective, Project Timberwind retrospective). For each of the candidate joint constraint points, compute the conditional posterior.

4. **Compute conjunction posteriors** with engineering-closure priors. For R-hybrid-aerocapture-aerobraking, use a generous prior (50 percent — it's a single SCOPE-pending round, no strong prior either way). For R-bring-rendezvous-survivability, use a more pessimistic prior (20-30 percent — the engineering question is hard and mitigation candidates each have known limitations per the SCOPE.md).

5. **Produce a synthesis table** for the project owner: rows are candidate (specific power × lifetime) points; columns are L0-05 strict / waiver, aerocapture credit, conditional-on-each-engineering-round joint posterior, capital-class-threshold met (yes/no for sovereign-grant / sovereign-bond / regulated-utility / corporate-growth / venture).

6. **Reading-level recommendation** to project owner: under current reactor-program-priors, is any cell restorable? If H5 holds, project-owner is looking at technology-demonstrator unambiguously. If H5 falsifies (e.g. R-hybrid-aerocapture-aerobraking comes back with a higher prior), there's a narrow band of reactor programs worth lobbying for.

---

## Reading template (5-section round template, worker fills in after run)

- **Hypotheses adjudicated.** Verdict per H1-H6, predicted vs measured numeric posteriors.
- **Headline.** One-line: under what reactor-program profile, if any, does the matrix have a surviving cell at conservative anchors + conditional on engineering closures?
- **Reading.** Project-owner-decision level: does the program have a reactor-program-targets path that a sovereign or government partner could underwrite, or is technology-demonstrator the only honest reading?
- **Cross-learning.** Connection to R-power-bayesian-update, R-power-wonder findings, R-reactor-roadmap. Does this round update any of those?
- **Next-round candidates.** If H6 holds: pitch rewrite anchor on technology-demonstrator program-class. If H5 falsifies: which engineering round to run first for highest joint-posterior lift?

---

## Worker assignment notes

- **Round priority:** **high.** Resolves the program-class decision (matrix decision point #1) at conservative anchors. Without this round the project-owner is making the program-class decision on intuition; with it, on a quantified joint posterior.
- **Worker fit:** synthesis-friendly worker (rhea has done two recent synthesis rounds; enceladus-r5 owns the input rounds). The work is composition of existing closure tables + Bayesian conjunction, not new physics. R-power-bayesian-update author (hyperion) has the priors framework already.
- **Inputs the worker needs:** the four enceladus-r5 STUDY.md files for rounds 9-12; `water-prop/rounds/R_power_bayesian_update/STUDY.md` for the three-prior bracket on US fission orbit posterior; this SCOPE; the four locked R-power-wonder belief findings from May 2026 (user memory).
- **Out-of-scope for this round:** any consideration of non-US fission programs (CNSA, Roscosmos, NewCleo, etc.) — the campaign's reactor-program-priors are US-anchored and a non-US program would require its own R-power-base-rate. Worth flagging in cross-learning.
- **Methodology lessons:** lesson 7 (pessimistic anchor first — apply conservative reactor-program-priors); lesson 8 (program-level NPV check — joint posterior matters more than per-mission); lesson 9 (anchor SCOPE on prior aggregate verdict — this SCOPE explicitly anchors on the four enceladus-r5 rounds' primary-text result tables, not on summary).
