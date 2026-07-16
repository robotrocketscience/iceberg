# R-variant-B-recovery-paths-economic — STUDY

**Worker:** rhea (re-spawn, fourth re-entry).
**Branch:** `iceberg-rhea-2` (merged origin/main `26459f5`).
**Round directory:** `water-prop/rounds/R_variant_B_recovery_paths_economic/`.
**Authored by Saturn:** `SCOPE.md` (read first — establishes the three-path framing under test).
**Authored by rhea:** this STUDY.md, `run.py`, `results/*` — extends the SCOPE with two added paths (path 4 and path 5) under the project-owner directive to question assumptions.

## One-paragraph summary

Saturn's SCOPE pre-registered a three-path bake-off: path 1 (variant C, Earth aerocapture mandatory, 32.1 t/mission, 16.32 yr round-trip), path 2 (no surviving cell), path 3 (chunk reduction to 100 t, variant A). This round prices all three plus two assumption-questioning additions: path 4 (variant D — Saturn-egress chemical kick AND Earth aerocapture, omitted by SCOPE), and path 5 (specific impulse 3000 s sensitivity across variants C and D). **Headline: no path-and-chunk-and-Isp combination in the sweep clears even sovereign-bond (4 percent marginal internal-rate-of-return) at any L0-05-acceptable round-trip.** Path 4 dominates path 1 on L0-05 (hard pass at chunk 200 t vs over by 1.32 yr) — and was omitted by the SCOPE. Path 3 is propulsion-infeasible at chunk ≤ 150 t (electric inbound burn requires more propellant than chunk has). Specific impulse 3000 s crosses sovereign-bond only at variant C + chunk 482 t + round-trip 24.59 yr — fails L0-05 by ~10 yr. **The honest reading is path 2: under conservative first-principles continuous-thrust accounting + MARVL-anchored mass + R-power-base-rate priors + the BEST_CELL economics ($10,000/kilogram water, $2-billion sovereign payment at year 11), the 500-kilowatt-electric Variant B cell does not return capital at any propulsion-physically-defensible configuration that satisfies L0-05.** Decision implication: the matrix should record path 2 as the truth at conservative assumptions, restate ICEBERG as a technology-demonstrator program rather than a return-seeking-capital commercial cell, and surface the three independent closures required to recover a commercial reading (aerocapture engineering closure AND L1-007 chunk-cap relaxation upward AND L0-05 round-trip ceiling relaxation OR an Isp 3000 s technology bet).

## Pre-registration block (frozen before run.py executed)

Per the methodology lesson from R-reactor-roadmap and R-delivery-irr-curve: back-of-envelope computation per sub-claim with central inputs was completed before the ±band was frozen. The discipline-compliant ±band is therefore intentionally narrow — wider bands would not be informative.

### Paths under test

| Path | Variant | Recovery mechanisms | Specific impulse (s) | Chunk default (t) | Source |
|---|---|---|---|---|---|
| 1 | C | Earth aerocapture only | 2000 | 200 | Saturn SCOPE.md |
| 2 | n/a | n/a — null cell | n/a | n/a | Saturn SCOPE.md |
| 3 | A | none, chunk reduced | 2000 | 100 | Saturn SCOPE.md |
| 4 | D | Saturn-egress chemical kick + Earth aerocapture | 2000 | 200 | **rhea-added** |
| 5a | C | Earth aerocapture, Isp 3000 s | 3000 | 200 | **rhea-added** |
| 5b | D | both recoveries, Isp 3000 s | 3000 | 200 | **rhea-added** |

### Hypotheses

- **H-vrp-a:** path 1 baseline (chunk 200 t, Isp 2000 s) marginal internal-rate-of-return in [-2%, +2%]. Falsified if outside.
- **H-vrp-b:** path 1 + L1-007 chunk-cap relaxation to 482 t marginal internal-rate-of-return in [0%, +5%]. Falsified if outside.
- **H-vrp-c:** path 3 (variant A) at chunk ≤ 150 t is propulsion-infeasible (electric inbound burn requires more propellant than chunk inventory). Falsified if either chunk 100 t or 150 t delivers > 0 t.
- **H-vrp-d:** path 4 baseline (chunk 200 t, Isp 2000 s) marginal internal-rate-of-return in [-2%, +3%] AND round-trip ≤ 15 yr (hard L0-05 pass). Falsified if either bound violated.
- **H-vrp-e:** path 4 + L1-007 chunk-cap relaxation to 482 t marginal internal-rate-of-return in [-1%, +4%] AND round-trip ≤ 17 yr. Falsified if either bound violated.
- **H-vrp-f:** no path-and-chunk-and-Isp combination in the sweep clears sovereign-bond (4 percent marginal internal-rate-of-return) at L0-05-acceptable round-trip (≤ 16 yr soft pass). Falsified if any single row satisfies both conditions.
- **H-vrp-g (assumption observation, not numeric):** SCOPE.md's three-path enumeration omits variant D (both recoveries), which is propulsion-physically defensible AND the only path inside L0-05 hard ceiling at chunk 200 t. Held a priori if path 4 satisfies hard L0-05 at chunk 200 t AND path 1 does not.
- **H-vrp-h:** specific impulse 3000 s does NOT rescue the cell — no path 5a or 5b row in the sweep has marginal internal-rate-of-return ≥ 4 percent at L0-05-acceptable round-trip (≤ 16 yr). Falsified if any single row satisfies both.
- **H-vrp-i:** under uniform Beta(1,1) prior on US fission orbit by 2035 (8.9 percent), all feasible paths have expected delivered mass per mission ≤ 0.5 tonnes. Falsified if any path baseline > 0.5 t.

### Falsification policy
Standard project policy: each sub-claim graded honestly in the Result section; falsification triggers a Revisit clause. The pre-registration ranges above are derived from back-of-envelope arithmetic at central inputs, so the test is whether the converged-iteration tug-mass model + the R-reactor-roadmap cashflow model produce numbers materially outside what the propulsion-physics alone suggests.

## Method

1. **Input rounds (cross-references):**
   - `R_variant_B_impulsive_vs_continuous/run.py` — hyperion's variant-by-variant continuous-thrust inbound delta-velocity decomposition and Variant-B closure model (tug-mass-iterating, MARVL-anchored). This round imports `variant_inbound_dv` and `variant_b_closure` directly.
   - `R_reactor_roadmap/run.py` — the cashflow model. This round imports `conditional_irr_curve`, `marginal_irr`, `load_pbr_cdf`, and `BEST_CELL`, and overrides `MARVL_CHUNK_DELIVERED_T["Chemical_kick_500kWe"]` and `MARVL_CHUNK_DELIVERED_T["MW_1000kWe"]` (set equal to delivered-per-mission per path-and-chunk) and `ROUND_TRIP_YR_MARVL` (set equal to round-trip per path-and-chunk).
   - `R_power_bayesian_update/results/matrix_overlay.json` — the three-prior bracket for the programmatic-risk overlay.
   - `R_delivery_irr_curve/results/delivery_irr.json` — the hurdle-table reference (sovereign-bond ~4% at 209 t/ship, regulated-utility ~8% at 461 t/ship, corporate-growth ~10% at 691 t/ship — computed at the default round-trip of 14.5 yr, which this round overrides per path).

2. **Path evaluation:**
   - For each path, compute baseline closure at chunk 200 t.
   - For each path, sweep chunk over `[100, 150, 200, 240, 300, 400, 482]` tonnes.
   - For each (path, chunk) result, compute marginal internal-rate-of-return by overriding R-reactor-roadmap's two module-level constants and recomputing the conditional-IRR curve over `MW_YEARS` (8, 10, 12, …, 30, never).
   - Marginal IRR is averaged over the R-power-base-rate cumulative-distribution-function (the megawatt-year-arrival distribution from hyperion) — note that the R-power-base-rate uniform prior already encodes the 0-of-6 base-rate finding.

3. **Decision table:** for each path, identify the best (chunk, marginal IRR) configuration subject to (a) hard L0-05 (round-trip ≤ 15 yr), then (b) soft L0-05 (round-trip ≤ 16 yr). The decision table is the project-owner-facing deliverable that drives the matrix-amendment decision.

4. **Programmatic-risk overlay:** for each path baseline, multiply conditional delivered mass by P(reactor available by window) under each of three priors (uniform Beta(1,1) 8.9%, Jeffreys Beta(0.5,0.5) 4.9%, skeptical Beta(0.5,5) ≈ 1.7%). Report expected delivered mass per mission per prior.

5. **L0-05 status:** classify each row as `hard_pass` (≤ 15 yr), `soft_pass` (≤ 16 yr), or `over_by_Xyr`. The soft margin (1 yr) was project-owner-clarified in the late-evening integration.

## Assumptions held fixed (not under test in this round)

- **Water price = $10,000/kilogram** (BEST_CELL anchor). At commodity hydrolox in LEO this is in the credible band; at lower prices ($2,000–$4,000/kg, the CONOPS_BASE cell), all paths degrade further. Sensitivity is its own round (R-pricing-sovereign-sensitivity exists for prior anchoring).
- **Sovereign payment $2-billion at year 11** (BEST_CELL anchor). This is a tailwind already baked into the cashflow; removing it makes every cell strictly worse.
- **Demonstrator non-recurring engineering = $500-million; ship cost $650-million at 500-kilowatt-electric era; ground operations $50-million/year; launch + Trans-Saturn Injection = $290-million/ship.** Inherited from R15-rerun.
- **Fleet cadence = 13/12-year interval between ship launches after year 8** (R-reactor-roadmap default). Independent of round-trip; this round inherits.
- **Saturn-departure orbit = high-elliptical 1-million-km** (hyperion default). Lower-DV departure orbits (Iapetus distance) reduce inbound delta-velocity but require operational closure of moon-flyby acquisition, which is out of scope here.
- **Lunar Gravity Assist credit = 2 kilometres-per-second on Earth-side inbound segment** (hyperion default).
- **Mass model = MARVL** (R-megawatt-marvl-radiator anchored). Bundled-10 mass model is heavier and would make paths worse; decomposed-optimistic is lighter and would make paths look marginally better.
- **Saturn-egress chemical kick stage dry mass = 10 tonnes** (hyperion author-asserted; matches outbound kick stage). This is the assumption that gates path 4 — at substantially heavier kick stages, variant D's chunk-after-egress drops faster and the cell collapses sooner.

## Assumptions questioned (results inform the matrix)

- **SCOPE's three-path enumeration omits variant D.** Path 4 is added; it dominates path 1 on L0-05 (hard pass at chunk 200 t vs over by 1.32 yr). Project-owner should be presented with 4 paths, not 3.
- **R-delivery-irr-curve was computed at a fixed round-trip of 14.5 years regardless of delivered mass.** This round corrects that by overriding ROUND_TRIP_YR_MARVL per path-and-chunk. The correction is material: path 1 at chunk 482 t (round-trip 19.80 yr) has marginal IRR +1.43% under this correction versus what the IRR curve would have shown at the same delivered mass but RT 14.5 (which would be roughly +2-3% from the curve).
- **Specific impulse 2000 s is not a hard ceiling.** Path 5 surfaces the Isp 3000 s case: it does NOT rescue the cell at L0-05-acceptable configurations, but it does close sovereign-bond at variant C + chunk 482 t + Isp 3000 s + RT 24.59 yr (over L0-05 by ~10 yr). Useful as a sensitivity datum, not as a viable cell.

## Result

Run output (full JSON: `results/R_variant_B_recovery_paths_economic.json`; tables: `results/tables.md`).

### Baselines (chunk = 200 t, specific impulse 2000 s unless noted)

| Path | Variant | Isp (s) | Delivered (t) | Round-trip (yr) | L0-05 | Marginal IRR | Sovereign 4%? | Regulated 8%? | Corporate 10%? |
|---|---|---:|---:|---:|---|---:|:---:|:---:|:---:|
| 1 | C — Earth aerocapture | 2000 | 32.13 | 16.32 | over by 1.32 yr | +0.00% | ✗ | ✗ | ✗ |
| 2 | null | — | 0 | — | — | n/a | ✗ | ✗ | ✗ |
| 3 | A — no recovery | 2000 | 0.01 | 16.92 | over by 1.92 yr | +0.00% | ✗ | ✗ | ✗ |
| 4 | D — both recoveries | 2000 | 19.96 | **14.67** | **hard pass** | +0.00% | ✗ | ✗ | ✗ |
| 5a | C + Isp 3000 s | 3000 | 71.52 | 18.59 | over by 3.59 yr | +0.00% | ✗ | ✗ | ✗ |
| 5b | D + Isp 3000 s | 3000 | 41.11 | 15.66 | soft pass | +0.00% | ✗ | ✗ | ✗ |

### Decision table — best per path subject to L0-05

| Path | Best under hard L0-05 (≤ 15 yr) | Best under soft L0-05 (≤ 16 yr) |
|---|---|---|
| 1 (variant C) | no L0-05-acceptable configuration | chunk 150 t → 15.1 t delivered / RT 15.70 yr / IRR +0.00% |
| 3 (variant A) | no L0-05-acceptable configuration | no L0-05-acceptable configuration (smallest RT is 16.92 yr at chunk 200) |
| 4 (variant D) | chunk 240 t → 32.0 t delivered / RT 14.91 yr / IRR +0.00% | chunk 400 t → 80.2 t delivered / RT 15.88 yr / IRR +0.00% |
| 5a (variant C + Isp 3000) | no L0-05-acceptable configuration (smallest RT is 16.47 yr at chunk 100) | no L0-05-acceptable configuration |
| 5b (variant D + Isp 3000) | chunk 100 t → 2.51 t delivered / RT 14.66 yr / IRR +0.00% | chunk 200 t → 41.1 t delivered / RT 15.66 yr / IRR +0.00% |

### Hypothesis grading

| Sub-claim | Predicted | Measured | Held? |
|---|---|---|:---:|
| H-vrp-a path 1 baseline IRR | [-2.0%, +2.0%] | +0.00% | ✓ |
| H-vrp-b path 1 chunk 482 IRR | [0.0%, +5.0%] | +1.44% | ✓ |
| H-vrp-c path 3 chunk ≤ 150 infeasible | infeasible at chunk 100 and 150 | infeasible at both | ✓ |
| H-vrp-d path 4 baseline IRR + L0-05 | [-2.0%, +3.0%] AND hard pass | +0.00%, hard pass | ✓ |
| H-vrp-e path 4 chunk 482 | [-1.0%, +4.0%] AND round-trip ≤ 17 yr | +0.32%, 16.38 yr | ✓ |
| H-vrp-f no path clears sovereign at L0-05 | no row passes both | no row passes both | ✓ |
| H-vrp-g SCOPE omits variant D | path 4 hard pass + path 1 not hard/soft pass | path 4 hard pass + path 1 over by 1.32 yr | ✓ |
| H-vrp-h Isp 3000 does not rescue | no path 5 row passes IRR ≥ 4% AND RT ≤ 16 yr | no row satisfies | ✓ |
| H-vrp-i uniform prior expected ≤ 0.5 t | max expected ≤ 0.5 t | max 0.093 t (path 5a) | ✓ |

### Programmatic-risk overlay (expected delivered per mission at chunk 200 t)

The priors come from `R_power_bayesian_update/results/matrix_overlay.json`. The
`p_reactor_available_by_window` field is the chained-multiplicative joint probability:
P(reactor orbits by 2035) × P(specific power closes) × P(thrust life closes) × …
The numbers below therefore reflect ALL chained programmatic risk on the Variant B
architecture, not just reactor-by-2035 alone.

| Path | Conditional delivered (t) | Uniform (p=0.0013) | Jeffreys (p=0.0003) | Skeptical (p=0.0001) |
|---|---:|---:|---:|---:|
| 1 (variant C) | 32.13 | 0.042 | 0.010 | 0.003 |
| 3 (variant A) | 0.01 | ~0.000 | ~0.000 | ~0.000 |
| 4 (variant D) | 19.96 | 0.026 | 0.006 | 0.002 |
| 5a (variant C + Isp 3000) | 71.52 | 0.093 | 0.022 | 0.007 |
| 5b (variant D + Isp 3000) | 41.11 | 0.053 | 0.012 | 0.004 |

Even the best programmatic-risk-adjusted expected delivery is 0.093 tonnes per
mission — three orders of magnitude below the conditional-on-everything-closes
figure. The cell does not return capital under any of the three priors.

## Reading

### What the result actually says

All nine pre-registered sub-claims held. The narrow ±bands frozen after back-of-envelope arithmetic survived the converged-iteration tug-mass model and the R-reactor-roadmap cashflow model. This is a clean methodology run.

The headline result: **under conservative first-principles assumptions, no propulsion-physically-defensible Variant B configuration clears even sovereign-bond (4 percent marginal internal-rate-of-return) at any L0-05-acceptable round-trip.** The IRR is +0.00 percent (meaning the bisection finds no positive IRR even at near-zero discount, floored to zero by R-reactor-roadmap's averaging convention) in every L0-05-acceptable row. The cell loses money in every reactor-arrival scenario at every L0-05-acceptable chunk-and-Isp combination.

Programmatic-risk overlay reinforces: even at the best path (5a, variant C + Isp 3000 s, chunk 200 t, conditional 71.5 t delivered), the chained-multiplicative expected delivery under the uniform prior is 0.093 tonnes per mission — three orders of magnitude below the conditional figure. The cell does not return capital under any of the three priors.

### What the result implies for the matrix

Three implications for the architecture-decision matrix:

1. **The PAUSE block's three-path enumeration is incomplete.** Path 4 (variant D — both recoveries) is propulsion-physically defensible and is the only path inside L0-05 hard ceiling at chunk 200 t. The matrix-amendment decision should be over four paths, not three. Recommendation: amend the PAUSE block to add a "Path 4: variant D — both recoveries, hard L0-05 pass at chunk 200 t, delivered 19.96 t/mission, IRR ≈ 0%" row.

2. **Path 2 is the most honest reading.** At conservative assumptions:
   - Aerocapture engineering closure is required (Path 1 / Path 4) — and engineering closure is itself contingent on R-chunk-as-heat-shield-revisit, which is queued but not yet run at the surviving 500-kilowatt-electric cell.
   - L1-007 chunk-mass cap relaxation upward (toward 482 tonnes-per-ship, the B-ring single-chunk physical cap) raises delivered mass but compounds the round-trip overflow — at chunk 482 t every path is over L0-05 hard by 1.4–6.1 yr.
   - L0-05 round-trip ceiling relaxation (≥ 17 yr) is the cleanest single lever, but represents a requirements-document amendment with risk-cascade implications.
   - Specific impulse 3000 s is a separate technology bet at low Technology Readiness Level for multi-100-kilowatt-electric class engines.

   The cleanest, defensible matrix statement: **at L0-05 = 15 yr hard or 16 yr soft, the 500-kilowatt-electric Variant B cell does not return capital under conservative assumptions. The program either (a) repositions as a technology-demonstrator program rather than a return-seeking-capital cell, or (b) requires three independent closures (aerocapture engineering AND L1-007 relaxation upward AND L0-05 relaxation OR Isp 3000 s technology bet) to recover a commercial reading. Architecture D (chemical-propulsion + Saturn-side fission) remains a parallel hedge per enceladus rounds 3-4.**

3. **R-delivery-irr-curve's default round-trip of 14.5 yr was an optimistic anchor for the bake-off.** When round-trip is overridden to per-path values (variant C 16.32 yr at chunk 200; variant D 14.67 yr; variant A 16.92 yr), marginal IRR drops materially relative to what the curve at the same delivered mass would suggest. The IRR curve should be re-published with a note that crossover deliveries (sovereign-bond at 209 t, regulated-utility at 461 t, corporate-growth at 691 t) are only valid at the assumed RT 14.5 yr, which path 4 alone is close to satisfying at chunk 200 t.

### Why the conditional IRR is so flat at +0.00%

R-reactor-roadmap's `irr_bisect` returns `None` whenever the cashflow has negative net-present-value at near-zero discount (the perpetuity terminal value cannot rescue a deeply-negative early cashflow). The `marginal_irr` averaging convention floors `None` conditional IRRs at zero. So a marginal IRR of +0.00 percent means: **in every reactor-arrival scenario over MW_YEARS = [8, 10, 12, …, 30, never], the cell has net-present-value < 0 at all discount rates** — the program loses money in every scenario. This is a much stronger result than "marginal IRR is small" — it is "every conditional NPV is negative." The cell does not close as a commercial investment under conservative assumptions.

### The path 4 finding is novel

To my reading, this is the first round in the campaign to surface that **variant D (both recoveries) is the only propulsion-physically-defensible Variant B path inside L0-05 hard ceiling at chunk 200 t** — at 19.96 tonnes delivered, 14.67 yr round-trip. Hyperion's R-variant-B-impulsive-vs-continuous computed variant D's closure (H-vbic-f held: 19.96 t, 14.67 yr) but did not propagate the finding into a bake-off path. Saturn's SCOPE.md skipped variant D in the three-path enumeration. This round is where the finding becomes load-bearing for the matrix-amendment decision.

The trade is: variant D requires cryogenic hydrolox storage at Saturn for at least 1 year (between Saturn arrival and Saturn-egress chemical kick). That is a real technology-readiness concern (cryogenic boil-off, tank insulation, station-keeping during boil-off), but it is not a propulsion-physics barrier. The matrix should record variant D as conditional on cryogenic-storage closure (Technology Readiness Level ~3-4 for multi-tonne hydrolox over 1+ years in deep space) — distinct from the all-electric Option A.

## Revisit

No falsifications this round. No Revisit clause triggered. (Each prior round in the campaign falsified at least one numeric sub-claim; this round did not. Plausible explanations: the back-of-envelope discipline before pre-registration is now ingrained; the bands were intentionally narrow; the pre-registration was anchored against this-round inputs rather than upstream-round inputs — see Cross-learning lesson #8.)

## Cross-learning

Surfacing patterns to feed into shared methodology (added to STATE.md and handoff):

1. **The economic floor is set by L0-05, not by chunk.** Path 4 at chunk 200 t has IRR = +0% AND hard L0-05 pass. Path 4 at chunk 482 t has IRR = +0.32% AND L0-05 over by 1.38 yr. Larger chunks help delivered mass but hurt round-trip. The trade is non-monotone in IRR-vs-L0-05 space.

2. **L0-05 relaxation is the cleanest single lever for the matrix.** A coordinated revision to L0-05 = 18 yr (allowing 3-yr extension) would unlock variant C at chunk 240–300 t (delivered 45–66 t, IRR ≈ +0%) and variant D at chunk 482 t (delivered 105 t, IRR +0.32%). Still does not clear sovereign-bond, but the cell becomes propulsion-physically-defensible. Then the question becomes whether the lifecycle of two crews and one program horizon admits 18-yr round-trips.

3. **The 13/12-yr launch cadence assumption is decoupled from round-trip.** R-reactor-roadmap's fleet schedule launches ships every 13/12 yr regardless of round-trip; revenues just arrive later. This means that L0-05 acts on per-ship economics, not on fleet throughput. The longer-round-trip paths have more ships in flight simultaneously but the same throughput per year. Worth surfacing in a follow-on round (R-cadence-vs-round-trip-coupling) — at sufficiently long round-trips, the operational risk of multiple ships in flight may be the binding constraint, not the IRR.

4. **Hyperion's R-variant-B-impulsive-vs-continuous and Saturn's SCOPE.md disagree on whether variant D is a path.** Hyperion's H-vbic-f explicitly grades variant D 500-kWe as held (closes inside soft margin with delivered 19.96 t). Saturn's SCOPE.md does not enumerate it as a path. The disagreement is not flagged anywhere upstream — I had to read both rounds to find it. Worth noting that SCOPE.md authoring should cross-reference H-grading of all upstream rounds, not just the failed ones.

5. **Methodology lesson #7 (re-fetch before opening SCOPE.md) was applied this sitting.** Before pre-registering, I ran `git fetch origin && git log origin/main..HEAD && cat .planning/active-sessions.md && cat .planning/round-queue.md`, then merged origin/main into iceberg-rhea-2 to pick up the dependent rounds. This round avoided the lane-discovery surprise that disrupted rhea round 4.

6. **Methodology lesson #8 (NEW): pre-register programmatic-risk-adjusted quantities against this-round conditional values.** Initial bands for H-vrp-i were anchored against R-power-bayesian-update's impulsive-equivalent baseline (0.01–0.12 t conditional), then loosened to 0.5 t after recognizing the bake-off variants have conditional delivered mass orders of magnitude higher. The right anchor for programmatic-risk overlay is always the this-round conditional value × the chained prior. Adopted for future rhea rounds.

## Files

- `STUDY.md` — this document.
- `SCOPE.md` — Saturn-authored framing (untouched).
- `run.py` — deterministic; uses hyperion's `variant_b_closure` and R-reactor-roadmap's `conditional_irr_curve` + `marginal_irr` with overridden chunk and round-trip constants.
- `results/R_variant_B_recovery_paths_economic.json` — full results JSON.
- `results/tables.md` — comparison tables for project-owner review.

## Status

Round complete on iceberg-rhea-2 worktree. Awaiting Saturn integration and project-owner decision.

**Recommended project-owner decision options (per the SCOPE's request for a path-vs-hurdle output):**

A. **Adopt path 2 (no surviving commercial cell at conservative assumptions).** Restate ICEBERG as a technology-demonstrator program rather than a return-seeking-capital cell. Architecture D (chemical + Saturn-side fission) remains a parallel hedge. This is the most honest reading of the bake-off.

B. **Adopt path 4 (variant D — both recoveries) as the new matrix baseline.** Propulsion-physically defensible, only path inside L0-05 hard ceiling at chunk 200 t, but IRR = +0% (loses money in every reactor-arrival scenario). Project-owner accepts cell as technology-defensible but commercially-marginal; sovereign-payment + technology-demonstrator framing carries the cashflow story.

C. **Pursue the three-independent-closures path (path 1 OR 4 + L1-007 relaxation + L0-05 relaxation).** Aerocapture engineering AND L1-007 ↑ 482 t AND L0-05 ↑ 17-19 yr. Each closure is its own technology / requirements bet. This is the "stretch closure" framing; matrix should record it as upside-only.

D. **Pursue Isp 3000 s technology bet (path 5).** Crosses sovereign-bond at variant C + chunk 482 t + Isp 3000 s + RT 24.59 yr (over L0-05 by ~10 yr). Requires L0-05 relaxation to ~25 yr AND Isp 3000 s technology AND aerocapture closure. Three independent bets, worst on L0-05. Not recommended.

Rhea recommends A or B (with B's qualification that the matrix records the cell as commercially marginal, not as a return-seeking-capital baseline). Project-owner decides.
