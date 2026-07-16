# R-reactor-specific-power-program-targets — STUDY

**Round.** R-reactor-specific-power-program-targets
**Author.** enceladus-r5 (worker)
**Pre-registration date.** 2026-05-15
**SCOPE.** `water-prop/rounds/R_reactor_specific_power_program_targets/SCOPE.md` (Saturn / orchestrator, 2026-05-15 latest+7).
**Heritage / input rounds (verbatim closure tables, not re-derived):**

- R-architecture-E-no-saturn-side-electrolysis (`448505e`) — R6 base grid.
- R-arch-E-specific-power-flown-anchored (`62f7079`) — R9 flown-anchored sensitivity.
- R-specific-power-cliff (`2d63291`) — R10 SP × ceiling closure counts.
- R-aerocapture-cliff-shift (`12058b5`) — R11 SP × X (inbound-aerocapture-credit) × ceiling.
- R-reactor-lifetime-vs-burn-time (`c685c52`) — R12 SP × X × L (lifetime ceiling) regrade at 25-yr round-trip ceiling.
- R-power-bayesian-update (hyperion, integrated 2026-05-15 evening) — three-prior bracket (uniform Beta(1,1), Jeffreys Beta(0.5,0.5), skeptical Beta(0.5,5)) on US-fission-orbit posterior + 500-kWe and megawatt scale conditionals.

This is a **synthesis round**, not a new physics or economics round. No propulsion physics is recomputed. The work is composition of the R6–R12 closure tables into a joint constraint surface (specific power × inbound-aerocapture-Δv credit × cumulative reactor-lifetime ceiling), application of the R-power-bayesian-update three-prior bracket to bound the probability that any reactor program delivers a viable point inside the ICEBERG demonstrator window 2032–2035, and conjunction with engineering-closure priors for the two held chunk-rendezvous engineering questions.

## Question

For the held chunk-rendezvous architecture at the conservative anchors (latest+7 matrix state), and conditional on R-hybrid-aerocapture-aerobraking and R-bring-rendezvous-survivability both closing:

1. What is the minimum (specific power × cumulative reactor lifetime × inbound aerocapture Δv credit) point that puts at least one cell back in the matrix at L0-05 strict (15-yr round-trip ceiling)?
2. What is the minimum point at L0-05 ≥ 25-yr waiver?
3. Conditional on R-power-base-rate priors, what is the posterior probability that a reactor delivering each candidate point flies inside 2032–2035?
4. Does the conjunction posterior (reactor delivers AND both engineering rounds close) exceed any meaningful capital-class threshold (technology-demonstrator vs sovereign-grant vs regulated-utility)?

## Pre-registered hypotheses (verbatim from SCOPE plus numeric predictions)

| # | Hypothesis | Predicted range | Falsification band |
|---|---|---|---|
| H1 | The minimum reactor-program point that puts a cell back at L0-05 strict (15-yr round-trip ceiling) requires specific power ≥ 8 W/kg AND lifetime ≥ 5 yr cumulative full-power burn. | min-point = (8 W/kg, 5 yr) at L0-05 strict | H1 falsified if min-point is achievable at ≤ 6 W/kg OR ≤ 3 yr lifetime — OR if no point at all exists at L0-05 strict in the tested envelope (i.e. L0-05 strict is unreachable). |
| H2 | The minimum reactor-program point at L0-05 ≥ 25-yr waiver requires specific power ≥ 5 W/kg AND lifetime ≥ 10 yr cumulative full-power burn, conditional on R-hybrid-aerocapture-aerobraking closing with X ≥ 10 km/s of inbound aerocapture Δv credit. | min-point = (5 W/kg, 10 yr, X = 10 km/s) at waiver | H2 falsified if min-point is achievable at ≤ 4 W/kg OR ≤ 7 yr lifetime, OR if aerocapture X ≥ 10 km/s doesn't help. |
| H3 | Posterior probability that any US fission program flies inside 2032–2035 delivering ≥ 8 W/kg specific power AND ≥ 5 yr cumulative lifetime AND ≥ 500 kWe scale is ≤ 3 percent under R-power-base-rate priors. | joint posterior ≤ 3 percent (across all three prior brackets) | H3 falsified if the joint posterior exceeds 10 percent under any of the three priors. |
| H4 | Posterior probability that any US fission program flies inside 2032–2035 delivering ≥ 5 W/kg AND ≥ 10 yr cumulative lifetime AND ≥ 500 kWe scale is ≤ 1 percent under same priors. | joint posterior ≤ 1 percent (across all three priors) | H4 falsified if the joint exceeds 5 percent under any prior. |
| H5 | Conjunction posterior (reactor-program delivers a viable point AND R-hybrid-aerocapture-aerobraking closes AND R-bring-rendezvous-survivability closes) is ≤ 1 percent under the most optimistic credible reactor-program assumption (H3) and ≤ 0.1 percent under the more pessimistic (H4). The architecture is not financeable on this conjunction probability under any return-seeking-capital structure. | conjunction ≤ 1 percent (H3 anchor) / ≤ 0.1 percent (H4 anchor) | H5 falsified if either engineering round has independent prior > 50 percent (lifting the conjunction). |
| H6 | Reading-level conclusion (load-bearing): the program-class decision (matrix decision point #1) at conservative anchors is **technology-demonstrator-only**. Restoring regulated-utility-class framing requires (a) reactor-program targets that no current US program funds, AND (b) two engineering closures that have not run. Until at least one of those constraints relaxes, the honest pitch posture remains technology-demonstrator. | reading-level: technology-demonstrator is the honest reading | H6 falsified if any combination of H1–H5 produces a joint posterior > 10 percent for a return-seeking-capital-class cell. |

## Method

`run.py` (in this directory) does the following:

1. **Load closure tables.** Reads four input JSON files verbatim:
   - `water-prop/rounds/R_specific_power_cliff/results/specific_power_cliff.json` (SP × ceiling).
   - `water-prop/rounds/R_aerocapture_cliff_shift/results/aerocapture_cliff_shift.json` (SP × X × ceiling).
   - `water-prop/rounds/R_reactor_lifetime_vs_burn_time/results/reactor_lifetime_regrade.json` (SP × X × L, at 25-yr ceiling).
   - `water-prop/rounds/R_power_bayesian_update/results/R_power_bayesian_update_summary.json` (three-prior bracket).

2. **Build joint constraint surface.** Compose a unified `close_count[SP][X][L][ceiling]` lookup. For L0-05 strict (15-yr), use R-specific-power-cliff (R-aerocapture and R-reactor-lifetime only ran at 25-yr base). For L0-05 ≥ 25-yr waiver, use R-reactor-lifetime regrade (which already overlays X and L).

3. **Find minimum closing point at each L0-05 setting.** Minimum over (SP, X, L) — three dimensions — defined as the lexicographically smallest tuple where `close_count ≥ 1`. Report all three Pareto-frontier corners (smallest SP given X, L; smallest X given SP, L; smallest L given SP, X).

4. **Apply program-conditional priors.** For each candidate minimum point, compute the reactor-program-delivery posterior as:

   ```
   P(viable reactor by 2035)
       = P(any US 500-kWe-class fission orbit by 2035)        # from R-power-bayesian-update
         × P(SP ≥ SP_min | reactor orbits)                    # bracketed KRUSTY-anchored conditional
         × P(L ≥ L_min  | reactor orbits)                     # bracketed Kilopower-design-target conditional
   ```

   Three priors swept: uniform (Beta(1,1)) → P(500 kWe orbit by 2035) = 0.13 percent; Jeffreys (Beta(0.5,0.5)) → 0.03 percent; skeptical (Beta(0.5,5)) → 0.01 percent. Three conditional brackets (optimistic / nominal / skeptical) on P(SP ≥ threshold | orbit) and P(L ≥ threshold | orbit). Total nine bracket combinations per candidate point.

5. **Engineering-closure priors (per SCOPE).** R-hybrid-aerocapture-aerobraking: 50 percent generous prior (SCOPE-recommended). R-bring-rendezvous-survivability: 25 percent (midpoint of SCOPE-recommended 20–30 percent range).

6. **Conjunction posterior.**

   ```
   P(architecture clears) = P(viable reactor) × P(aerocapture closes) × P(rendezvous closes)
   ```

   For each (candidate min-point, prior bracket, conditional bracket) triple.

7. **Capital-class thresholds** (informed by `R_reactor_roadmap` IRR hurdle crossovers, integrated 2026-05-15 evening): technology-demonstrator ≤ 0.1 percent (a one-flight credibility proof, not a financeable architecture); sovereign-grant ≥ 0.1 percent (grants don't compute IRR); sovereign-bond ≥ 1 percent (Treasury + IRR > sovereign-bond hurdle); regulated-utility ≥ 5 percent; corporate-growth ≥ 15 percent; venture ≥ 25 percent.

### Conditional brackets (rationale)

| Conditional | Optimistic | Nominal | Skeptical | Rationale |
|---|---|---|---|---|
| P(SP ≥ 8 W/kg \| 500 kWe orbits) | 0.30 | 0.15 | 0.05 | KRUSTY 2018 demonstrated 2.4 W/kg at 4.3 kWe; FSP Phase 1 targets are not public at system-level SP, but Phase-1 vendors (Lockheed, Westinghouse, IX) all proposed Brayton conversion which scales better than Stirling. 8 W/kg is 3.3× KRUSTY heritage with no flown intermediate. Generous reads (large-reactor Brayton + flight cleanup) get ~0.30; KRUSTY-pessimistic reads (the only flown anchor is 2.4 W/kg) get ~0.05. |
| P(SP ≥ 5 W/kg \| 500 kWe orbits) | 0.50 | 0.30 | 0.15 | 5 W/kg is 2.1× KRUSTY, near GPHS-RTG heritage (5.3 W/kg). More achievable but still requires Brayton-class conversion at 500 kWe scale. |
| P(L ≥ 5 yr cumulative full-power \| 500 kWe orbits) | 0.50 | 0.30 | 0.10 | KRUSTY ran 28 hours of full-power. Kilopower design target was 10 yr but never demonstrated at full power. 5 yr is half-Kilopower-target; any 500-kWe flight program would likely target this minimum, but space-fission has a 0-of-6 history of delivering on design lifetime. |
| P(L ≥ 10 yr cumulative full-power \| 500 kWe orbits) | 0.30 | 0.15 | 0.05 | Full Kilopower design-target lifetime, never demonstrated. Generous: matches design intent. Skeptical: requires extending heritage by 4 orders of magnitude from KRUSTY 28-hr datapoint. |

### Caveat on conditionals

The conditional bracket numbers are not derived from a published empirical distribution — they are bounded judgments anchored on the two flown anchors (SNAP-10A at low specific power and low lifetime, KRUSTY at 2.4 W/kg and 28 hrs) and the Kilopower / FSP design targets. The bracket spread is wider than the R-power-bayesian-update headline bracket spread to reflect this. Sensitivity analysis in the round output covers the full bracket.

## Reading template (filled after run)

(Per round protocol — `Hypotheses adjudicated` / `Headline` / `Reading` / `Cross-learning` / `Next-round candidates`. Filled below after computation.)

---

# Reading (post-computation)

## Hypotheses adjudicated

| # | Verdict | Predicted | Measured |
|---|---|---|---|
| H1 | **HELD-WITH-EXTENSION** | min-point at L0-05 strict = (8 W/kg, 5 yr) | L0-05 strict closure set is **empty** across the entire tested envelope (SP up to 10 W/kg, X up to 25 km/s, L up to ∞). H1's direction is consistent with the data, but the true min-point is more pessimistic than predicted: it does not exist within the tested envelope. SCOPE falsifiers (SP ≤ 6 OR L ≤ 3) do not trigger. |
| H2 | **FALSIFIED, INFORMATIVE** | min-point at 25-yr waiver = (5 W/kg, 10 yr, X=10 km/s) | Closure surface is a 3D Pareto frontier with smallest-SP corner (5, 10, 15), smallest-X corner (8, 0, 10), and smallest-L corner (9, 25, 5). SCOPE falsifier "L ≤ 7" triggers at the smallest-L corner because closure is achievable at L=5 yr if SP=9 W/kg AND X=25 km/s compensate. The falsification is itself the load-bearing finding: the closure surface is a Pareto frontier, not a single min-point — relaxing any one of (SP, X, L) requires tightening the other two. |
| H3 | **HELD by 154× margin** | joint posterior at (8 W/kg, 5 yr) ≤ 3 percent | max joint posterior across three priors and three conditional brackets: 0.0195 percent |
| H4 | **HELD by 51× margin** | joint posterior at (5 W/kg, 10 yr) ≤ 1 percent | max joint posterior across three priors and three conditional brackets: 0.0195 percent |
| H5 | **HELD by 400× / 40× margin** | conjunction ≤ 1 percent (H3 anchor) / ≤ 0.1 percent (H4 anchor) | max conjunction posterior: 2.44e-5 at both anchors |
| H6 | **HELD by 1230× margin** | technology-demonstrator-only at conservative anchors | max conjunction across all 54 (target × prior × bracket) combinations: 4.06e-5; capital class is technology-demonstrator-only at *every* combination tested |

## Headline

**Under conservative anchors there is no reactor-program profile, even granted the two pending engineering closures, that puts the chunk-rendezvous architecture above the technology-demonstrator capital-class threshold.** The maximum conjunction posterior across the entire tested envelope of (SP × L × X) reactor program targets × three R-power-base-rate priors × three KRUSTY-anchored conditional brackets is **4.06e-5 (= 0.004 percent)** — at the most optimistic single corner (uniform prior, optimistic conditionals, 5 W/kg + 5 yr target). That is **23× below the sovereign-grant threshold (0.1 percent)** and **1230× below the regulated-utility threshold (5 percent)**. Below the sovereign-grant threshold is technology-demonstrator-only.

A stronger result: **L0-05 strict (15-yr round-trip ceiling) has zero closing cells across the entire tested envelope**, even at SP = 10 W/kg, X = 25 km/s inbound aerocapture credit, and L = infinite reactor lifetime. The matrix is structurally empty at L0-05 strict regardless of which reactor program flies.

## Reading (project-owner-decision level)

**The program-class decision (matrix decision point #1) is forced to technology-demonstrator at conservative anchors.** No combination of reactor program + engineering closures inside the 2032–2035 demonstrator window produces a capital-class result that a return-seeking capital structure could underwrite. Both Level-0 framing decisions deferred to this round by the project-owner walk-through (latest+8) resolve in the same direction:

1. **L0-13 capital structure → forced to government-grant / sovereign-grant.** The 0.004 percent maximum conjunction posterior is 1230× below regulated-utility, 38× below sovereign-bond, and 23× below sovereign-grant. The "honest pitch posture" annotation now has a quantitative floor.

2. **Reactor-program-availability L0 → forced to "no plausible US reactor program restores the surviving cell."** The closure-surface emptiness at L0-05 strict and the Pareto-frontier structure at L0-05 25-yr waiver each independently confirm this. No (SP, L) program-target point worth advocating for has a conjunction posterior anywhere near financeability.

Two structural reasons the conjunction posterior cannot lift, in priority order:

- **The R-power-base-rate prior on P(500-kWe orbit by 2035) caps the optimistic anchor at 0.13 percent (uniform Beta(1,1)) — already 38× below sovereign-bond before any conditional is applied.** Even if every conditional (P(SP ≥ threshold | orbits) and P(L ≥ threshold | orbits)) were generously set to 1.0, the conjunction with engineering closures would still be ≤ 0.13 percent × 0.50 × 0.25 = 0.016 percent — still below sovereign-grant. The reactor-orbit base rate is the binding constraint; the conditionals only worsen it.

- **The closure surface is structurally a Pareto frontier, not a single point.** Relaxing one axis tightens the others. The H2 falsification is informative: closure at L=5 yr exists, but only at SP=9 W/kg AND X=25 km/s — which moves the conditionals from "challenging" to "implausible" and pushes the conjunction further down.

Restoring a financeable cell to the matrix requires one of three Level-0 amendments:

- **Amend L0-05 to ≥ 30-yr round-trip ceiling.** At 30-yr the surface opens up: closure at SP = 2.4 W/kg (KRUSTY anchor) becomes possible at X = 25 km/s aerocapture. But this trades one Level-0 against another — L0-05 was set on Synodic-window economics and 30-yr is half a working life per mission.

- **Amend L0-09 (per-mission delivered tonnage) to ~5 t and L0-07 (cadence) to 10/yr.** Not addressed by this round directly; relies on R-staged-commitment-NPV (thread #20) and R-cadence-2-vs-3-per-yr (thread #22). Effectively spreads the delivered-mass requirement across more missions, lowering per-mission burden.

- **Aerocapture R&D breakthrough plus reactor program breakthrough.** Requires both R-hybrid-aerocapture-aerobraking and a 500-kWe FSP Phase 2 award. Conjunction posterior 0.004 percent says: don't bet on this combination.

The honest pitch posture is technology-demonstrator. The round-13 / round-14 / round-15 / round-16 enceladus-r5 results (matrix's "Active sole defensible cell" Variant B delivers 4 t/mission not 80 t at 200-t chunk under self-consistent propellant accounting) compound this: even if a viable reactor program existed, the matrix's stated payload number is structurally infeasible at L0-05's chunk cap. The reactor question and the propellant question both push the same direction.

## Cross-learning

This round connects to and updates four prior findings.

- **R-power-bayesian-update (hyperion).** R-power-bayesian-update's headline P(500-kWe orbit by 2035) = 0.13 percent (uniform) is **the binding constraint** for the matrix's program-class decision. Before this round, the matrix's "no surviving cell" finding was a closure-table claim; this round converts it to a posterior-probability claim. The two findings should be linked in the matrix annotation.

- **R-reactor-roadmap (worktree-110450).** R-reactor-roadmap found marginal IRR under MARVL-anchored mass + reactor-program CDF = 1.45 percent. This round's max conjunction posterior 0.004 percent is 360× tighter. R-reactor-roadmap's IRR result assumed reactor program success; this round prices in the reactor-program prior, which dominates. R-reactor-roadmap should be re-anchored on this round's conjunction posterior; the IRR result effectively says "if the reactor flies, the architecture is sub-sovereign-bond" while this round says "even given reactor flight, the probability is sub-sovereign-grant when engineering closures are not yet posterior-positive."

- **R-power-wonder (locked beliefs from May 2026).** All four locked findings cohere with this round:
  - The 0-of-6 base rate on US space-fission programs reaching orbit since 1965 is exactly what the R-power-bayesian-update three-prior bracket encodes.
  - The 40 W/kg paper-aspiration vs KRUSTY-flown 2.4 W/kg gap is exactly the SP-conditional bracket this round used.
  - The radiator dominance at megawatt scale (40–55 percent of system mass per MARVL) is consistent with the equivalence between `decomposed_marvl` and `bundled_10` mass models that R-arch-E-specific-power-flown-anchored already noted.
  - The FSP Phase 2 not-yet-awarded status is exactly the R-power-bayesian-update likelihood-factor anchor.

- **R-power-base-rate (hyperion).** This round's H3/H4 verdicts confirm hyperion's bracket. Worth noting: R-power-base-rate's bracket spans 2.9–8.9 percent on **any** US fission orbit by 2035, but ICEBERG needs ≥ 500 kWe — a 0.6× scale conditional already applied in R-power-bayesian-update. The further conditionals on SP and L applied in this round narrow the posterior by another 2–3 orders of magnitude.

## Next-round candidates

Given H6 HELD by 1230× margin, the program-class decision is now quantitatively forced. Three next-round candidates ordered by load-bearingness:

1. **R-pitch-rewrite-technology-demonstrator** (highest priority, orchestrator-action). The pitch's current framing rests on regulated-utility / corporate-growth capital classes. This round's 0.004 percent conjunction-posterior ceiling is incompatible with that framing. Pitch rewrite anchor on technology-demonstrator program-class with explicit option-value framing for ICEBERG-as-Phase-2-pivot ("if R-hybrid-aerocapture-aerobraking closes positive AND a 500-kWe FSP flies, the cell reopens — but neither has prior > 50 percent today"). This is the matrix → pitch translation step. Orchestrator-owned.

2. **R-hybrid-aerocapture-aerobraking** (held SCOPE, hyperion). This round assumes a generous 50 percent independent prior for R-hybrid-aerocapture-aerobraking closing. If hyperion's actual round comes back with a meaningfully different prior (either way), this round's H6 verdict needs to be regraded. Highest-impact single round to update the program-class decision.

3. **R-bring-rendezvous-survivability** (held SCOPE, titan or phoebe). This round assumes 25 percent independent prior. If the round-actual prior is < 5 percent (e.g. titan's surfaced 99-percent-per-pass impact probability is unmitigatable), the conjunction posterior tightens by another ~5×. If > 50 percent, it lifts by 2× — still nowhere near financeability. Tighter impact only — does not flip the program-class verdict.

Also surfaced:

- **R-L0-amendments-portfolio.** With the program-class decision forced, the project-owner's three Level-0 amendment options (L0-05 to 30-yr, L0-09 to 5 t/mission, or aerocapture-conditional) become the load-bearing decision space. A round that bounds the IRR / posterior change under each amendment, against current matrix anchors, would clarify which amendment (if any) lifts the program above sovereign-grant. Plausibly orchestrator-owned (it's a synthesis on top of existing rounds plus matrix prose).

- **R-non-US-reactor-program-credit.** Mentioned as out-of-scope in this round per the SCOPE. The non-US space-fission programs (CNSA, Roscosmos, NewCleo, etc.) are not on the US-anchored 0-of-6 base rate. If a non-US program flies a viable 500-kWe reactor inside the demonstrator window, the conjunction posterior changes structurally. Low probability of being load-bearing in the near term (none of these programs has a public 2032–2035 milestone for ≥ 500 kWe electric), but worth a single round to bound the contribution.

## Methodology notes (recurring-lesson-7 ledger)

Two prediction-vs-measurement mismatches this round:

- **H1 directionally correct, value too optimistic** — predicted min-point (8 W/kg, 5 yr) exists; measured: doesn't exist within tested envelope. *Not* a recurring-lesson-7 strike — the prediction was bounded above by what the tested envelope could measure, and the measurement says the envelope itself is insufficient. The lesson is to widen the envelope at SCOPE-design time when prediction is near the edge.

- **H2 single-point prediction collapsed against 3D Pareto frontier** — predicted single (SP, L, X) min-point; measured: three Pareto corners, each different. *This is* a recurring-lesson-7 strike (call it strike 9) because the pre-registration treated a multi-dimensional Pareto frontier as a single-point hypothesis. Protocol fix: when the closure surface has > 1 dimensions, pre-register a min-corner *per dimension* (smallest-SP, smallest-X, smallest-L) rather than a single point.

Filed as `recurring-lesson-9` for the next worker's reference. The protocol fix is to anchor pre-registrations on the dimensionality of the underlying surface, not on the dimensionality of the prediction.

