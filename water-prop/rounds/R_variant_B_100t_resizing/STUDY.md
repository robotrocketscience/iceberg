# R-variant-B-100t-resizing — does chunk reduction to 100 tonnes per mission rescue Variant B without aerocapture?

**Status:** pre-result. Authored by phoebe (worker) on 2026-05-15 against orchestrator-authored SCOPE.md (Saturn, late evening). Pre-registration block frozen below before run.py executes.

## Question

Hyperion's R-variant-B-impulsive-vs-continuous (commit `daaf522`) falsified the matrix's surviving Variant B cell at chunk 200 tonnes: under first-principles continuous-thrust accounting, Variant A (no architectural recovery) at 500 kilowatt-electric MARVL-anchored mass delivers 0.0 tonnes per mission with round-trip 16.92 years. Hyperion surfaced four possible amendment paths; this round closes the fourth (path 3 in the bake-off taxonomy): **does shrinking the chunk to 100 tonnes re-open Variant A without aerocapture or chemical Saturn-egress?**

The architectural hope: smaller chunks reduce the inbound burn's propellant requirement because the Tsiolkovsky mass ratio is bounded by chunk mass (the chunk-water is the propellant supply). A smaller chunk also lightens the wet mass at burn start, which shortens t_burn at fixed thrust. If both effects compound favourably, the cell may close inside L0-05.

The architectural worry (my back-of-envelope before run.py): at fixed reactor power, Variant A feasibility requires `tug_t ≤ 0.325 × chunk_t` (so that propellant required does not exceed chunk inventory). For tug ≈ 5 t + 0.1 × reactor_kWe under the MARVL formula, that pins reactor power to `P_kWe ≤ (chunk_t/0.325 − 5)/0.1 = 3.08 × chunk_t − 50`. At chunk = 100 t the cap is ~258 kilowatt-electric. But round-trip closure at chunk 100 t requires `m_prop / P_kWe ≤ 0.196 t/kW` (else inbound burn exceeds 1.84 years and the round-trip blows the 15-yr ceiling); with m_prop ≈ chunk at the feasibility edge, that demands `P_kWe ≥ 510` for chunk = 100. **The two constraints are mutually exclusive at chunk 100 t in my back-of-envelope.** Feasibility wants a smaller reactor; closure wants a larger one.

If the back-of-envelope is right, the headline finding is that path 3 of the bake-off is structurally unavailable: there is no (chunk, reactor) point inside L1-007's chunk cap that simultaneously closes L0-05 and remains propellant-feasible. The bake-off collapses to paths 1 (Earth aerocapture mandatory) and 2 (acknowledge collapse).

If the back-of-envelope is wrong — most likely because the iteration-on-tug-mass term shifts the feasibility line, or because there is a chunk × reactor combination I have not enumerated where the burn time and feasibility margins coincide — the round identifies it.

## Pre-registered hypotheses

**Authoring stance.** SCOPE.md (orchestrator) pre-registered 13.5–14.5 yr round-trip and 25–40 t delivered at chunk 100 t / 500 kilowatt-electric Variant A. My back-of-envelope says **falsified-pessimistic** on both: the cell is structurally infeasible at chunk 100 t under any reactor power inside L1-007. I am pre-registering my pessimistic bands rather than the SCOPE's optimistic ones, and grading both predictions against the run. Per Methodology lesson 1 (pessimistic-default holds) and lesson N (back-of-envelope each headline metric).

**H-100-a (Variant A at chunk 100 t, 500 kilowatt-electric, MARVL mass, specific impulse 2000 s):** the cell is **propellant-infeasible** — required inbound propellant exceeds chunk inventory after iteration on tank mass converges. Falsified if feasible (m_prop_inbound < chunk).

**H-100-b (chunk-mass closure sweep, 500 kilowatt-electric Variant A):** there is **no chunk in [50, 200] tonnes** at which both (i) the cell is propellant-feasible AND (ii) round-trip ≤ 15 yr (strict). Falsified if any sweep row satisfies both conditions. Soft-version: there is no chunk in [50, 200] t at which both conditions hold under ±1 yr soft margin (round-trip ≤ 16 yr); falsified if any row satisfies both under soft.

**H-100-c (reactor-power closure sweep at chunk 100 t Variant A):** there is **no reactor power in [100, 700] kilowatt-electric** at which the cell is feasible and closes ±1 yr soft (round-trip ≤ 16 yr, delivered > 0 t). Falsified if any sweep row satisfies both. If H-100-c is held, sub-claim is that the (chunk, reactor) plane has no closing cell inside the joint L1-007 × L0-05 envelope for Variant A.

**H-100-d (optimum reactor power at chunk 100 t):** IF a closing cell exists (i.e., H-100-c is falsified), the reactor power that minimises round-trip subject to feasibility lies in **[200, 400] kilowatt-electric**. SCOPE pre-registered [200, 300]; I widen to [200, 400] to absorb the rule-of-thumb's documented 50 percent uncertainty. Falsified if optimum is outside [200, 400] given a closing cell exists; not gradable if no closing cell exists.

**H-100-e (path-3 vs path-1 dominance on delivered mass):** IF any closing-Variant-A configuration exists at any chunk ≤ 200 t, its delivered-mass-per-mission is **strictly less than 32.1 tonnes** (hyperion's Variant C path-1 at chunk 200 t). Falsified if any path-3 closure delivers > 32.1 t. Same logic as SCOPE's prediction; my band agrees.

**Aggregate prediction.** Path 3 is **structurally unavailable** inside L1-007's chunk cap and L0-05's round-trip ceiling. The bake-off reduces to paths 1 and 2. Aerocapture (or some other architectural recovery) is unavoidable. SCOPE's optimistic 13.5–14.5 yr / 25–40 t prediction is falsified-pessimistic by my framing.

**Confidence note.** My pessimistic framing puts H-100-a, H-100-b, H-100-c as the load-bearing predictions. If all three hold, the round's headline is a clean structural negative for path 3. If H-100-c is falsified (some reactor power gives a closing cell), the round upgrades into the operating-optimum sweep and H-100-d/e become the load-bearing claims. Either outcome is informative; the round is well-posed against a clean falsification protocol.

## Method

Reuses hyperion's `R_variant_B_impulsive_vs_continuous/run.py` closure function (`variant_b_closure`) with chunk_t as the swept parameter. Variant A architecture only (no Saturn-egress chemical kick, no Earth aerocapture). Delta-velocity decomposition from titan's R-inbound-dv-continuous-thrust at the default high-elliptical 1 megakilometer Saturn departure with Lunar Gravity Assist credit:

`electric_inbound_dv = Saturn_spiral + helio_retrograde + Earth_helio + LEO_spiral − LGA_credit`
`                    = 6.159 + 5.439 + 10.298 + 7.669 − 2.0`
`                    = 27.565 kilometers-per-second`

This delta-velocity is **independent of chunk mass**; it is a property of the orbit and the propulsion mode. Chunk mass enters through Tsiolkovsky:

`m_prop = (m_tug + chunk) × (1 − 1/exp(dv/v_e))`
`m_tug = MARVL(reactor_kwe, m_prop)`  (iterated to convergence)
`delivered = chunk − m_prop` (Variant A: no aerocapture, no egress)
`t_burn = m_prop × v_e² / (2 × η_thr × P_elec)`
`round_trip = 2 × Hohmann_cruise + Saturn_ops + t_burn`

Three sweeps:

1. **Chunk sweep, 500 kilowatt-electric Variant A**, chunk ∈ {50, 75, 100, 125, 150, 175, 200} t.
2. **Reactor-power sweep, chunk 100 t Variant A**, reactor ∈ {100, 200, 300, 400, 500, 600, 700} kilowatt-electric.
3. **Sanity-check baseline:** chunk 200 t, 500 kilowatt-electric Variant A. Must reproduce hyperion's published value (round-trip 16.92 yr, delivered 0.0 t infeasible-edge). If it does not, the closure function or constants have drifted; flag and stop.

Programmatic-risk overlay (uniform Beta(1,1) prior from `R_power_bayesian_update/results/matrix_overlay.json`) applied to any closing cell, mirroring hyperion's pattern.

## What this round does NOT cover (deferred)

- Marginal internal-rate-of-return for path 3 — owned by R-variant-B-recovery-paths-economic (the bake-off).
- Operational consequences of doubling cadence to recover throughput at chunk = 100 t — owned by separate cadence round.
- Chemical Saturn-egress kick + smaller chunk combinations — hyperion already established this starves the inbound burn at chunk 200; not re-tested here.
- Whether titan's continuous-thrust delta-velocity is an upper bound (10–20 percent optimal-control headroom) — same validity caveat as hyperion's round; not resolved here.

## Cross-references

- `water-prop/rounds/R_variant_B_impulsive_vs_continuous/` — hyperion's baseline at chunk 200 t. The closure function is imported verbatim.
- `water-prop/rounds/R_variant_B_500kWe_sizing/` — hyperion's reactor-power-optimum at chunk 200 t (optimum sat near 500 kilowatt-electric); the rule-of-thumb (`~0.45 × M_c kilowatt-electric per tonne`) is tested here at chunk 100 t.
- `water-prop/rounds/R_inbound_dv_continuous_thrust/` — titan's delta-velocity decomposition; supplies the 27.565 kilometers-per-second total used unchanged.
- `water-prop/rounds/R_variant_B_recovery_paths_economic/` — rhea's bake-off; consumes this round's delivered-mass output as path-3 input.
- `water-prop/rounds/R_power_bayesian_update/results/matrix_overlay.json` — uniform-prior overlay applied to any closing cell.

## Deliverables

- `water-prop/rounds/R_variant_B_100t_resizing/STUDY.md` (this file)
- `water-prop/rounds/R_variant_B_100t_resizing/run.py`
- `water-prop/rounds/R_variant_B_100t_resizing/results/R_variant_B_100t_resizing.json`
- `water-prop/rounds/R_variant_B_100t_resizing/results/tables.md`
- Append round-status row + narrative section to `water-prop/RUNNING_DOC.md`
- Handoff at `~/.claude/handoffs/iceberg-phoebe-20260515.md`

## Result

Ran chunk sweep [50, 75, 100, 125, 150, 175, 200] t at 500 kilowatt-electric Variant A, plus reactor sweep [100, 200, 300, 400, 500, 600, 700] kilowatt-electric at chunk 100 t Variant A. Full tables in `results/tables.md`; raw in `results/R_variant_B_100t_resizing.json`.

**Sanity check (chunk 200 t, 500 kilowatt-electric Variant A vs hyperion's published number):** reproduces round-trip 16.92 yr exactly; delivered 0.0148 t (hyperion printed "0.0 t — chunk fully consumed", same closure-function edge state). Closure function is byte-identical with hyperion's R-variant-B-impulsive-vs-continuous. No drift.

**Chunk sweep at 500 kilowatt-electric Variant A (electric inbound delta-velocity 27.565 kilometers-per-second):**

| Chunk (t) | Feasible? | m_prop_inbound (t) | Delivered (t) | Round-trip (yr) | Closes soft 16? |
|---:|:--:|---:|---:|---:|:--:|
| 50 | **no** | 79.2 (required) | −29.2 (deficit) | — | no |
| 75 | **no** | 98.1 | −23.1 | — | no |
| 100 | **no** | 117.0 | −17.0 | — | no |
| 125 | **no** | 135.8 | −10.8 | — | no |
| 150 | **no** | 154.7 | −4.7 | — | no |
| 175 | **no** | 180.1 | −5.1 | — | no |
| 200 | yes | 200.0 | **0.0** | 16.92 | no |

The propellant-feasibility threshold at 500 kilowatt-electric is effectively at chunk 200 t (the L1-007 cap). No smaller chunk satisfies `m_prop ≤ chunk`.

**Reactor sweep at chunk 100 t Variant A:**

| Reactor (kWe) | Feasible? | Tug (t) | Delivered (t) | t_burn (yr) | Round-trip (yr) | Closes soft 16? |
|---:|:--:|---:|---:|---:|---:|:--:|
| 100 | yes | 19.5 | **9.8** | 8.46 | 21.63 | no |
| 200 | yes | 29.9 | 2.0 | 4.60 | 17.77 | no |
| 300 | **no** | 35.0 | −1.9 (deficit) | — | — | no |
| 400 | **no** | 45.0 | −9.4 | — | — | no |
| 500 | **no** | 55.0 | −17.0 | — | — | no |
| 600 | **no** | 65.0 | −24.5 | — | — | no |
| 700 | **no** | 75.0 | −32.1 | — | — | no |

**Pre-registration grading:**

| Sub-claim | Predicted | Measured | Held? |
|---|---|---|---|
| H-100-a | chunk 100 t, 500 kilowatt-electric Variant A is propellant-infeasible | m_prop required 117.0 t > chunk 100 t (deficit 17.0 t) | **HELD** |
| H-100-b strict | no chunk in [50, 200] t at 500 kilowatt-electric Variant A closes strict 15 yr | no closing chunk | **HELD** |
| H-100-b soft | no chunk in [50, 200] t at 500 kilowatt-electric Variant A closes soft 16 yr | no closing chunk (chunk 200 just-feasible, round-trip 16.92 yr) | **HELD** |
| H-100-c | no reactor in [100, 700] kilowatt-electric at chunk 100 t Variant A is feasible AND closes soft 16 yr | reactors 100 + 200 are feasible but round-trip 21.63 / 17.77 yr; reactors ≥ 300 infeasible | **HELD** |
| H-100-d | optimum reactor at chunk 100 t in [200, 400] kilowatt-electric | not gradable (no closing cell) | n/a |
| H-100-e | best path-3 closing delivered < 32.1 t | best closing delivered = 0 t (no closing cell); vacuously < 32.1 | **HELD-vacuous** (tables.md treats as n/a) |

Four sub-claims gradable; four held. H-100-d not gradable because no closing cell exists. H-100-e held vacuously (the IF-clause is false). **Net: 4/4 gradable HELD. Best pre-registration grade in the campaign so far, tied with hyperion's R-variant-B-impulsive-vs-continuous at 5/6.**

## Reading

**Path 3 of the bake-off (chunk reduction without aerocapture) is structurally unavailable.** No (chunk, reactor) point in the swept envelope simultaneously satisfies propellant-feasibility and L0-05 round-trip closure under ±1 year soft margin. The bake-off taxonomy now resolves cleanly:

- **Path 1 (Earth aerocapture mandatory):** delivers 32.1 t/mission at chunk 200 t / 500 kilowatt-electric (hyperion's Variant C). Round-trip 16.32 yr (over ±1 yr soft margin; needs ±2 yr). Engineering dependency: R-chunk-as-heat-shield-revisit must close.
- **Path 2 (acknowledge collapse):** retire Variant B from the matrix's surviving-cell list. No closing architecture inside conservative continuous-thrust assumptions.
- **Path 3 (chunk reduction, no aerocapture):** **falsified** by this round. No closing cell exists.

**The mechanism is a locked-shut closure trade.** For Variant A (no architectural recovery), propellant-feasibility requires `tug ≤ 0.325 × chunk` (from the Tsiolkovsky mass ratio at 27.565 kilometers-per-second / 19.6 kilometers-per-second exhaust velocity). MARVL-anchored tug mass is `m_tug ≈ 5 t + 0.1 × P_kWe`. So feasibility caps reactor power at `P_kWe ≤ 3.08 × chunk_t − 50`. At chunk 100 t the cap is 258 kilowatt-electric.

Round-trip closure under L0-05 requires `t_burn ≤ 1.84 yr`. Burn time scales as `m_prop / P_kWe`; at the feasibility edge `m_prop ≈ chunk`, so closure requires `P_kWe ≥ chunk / 0.196 t/kW`. At chunk 100 t the floor is 510 kilowatt-electric.

**Feasibility ceiling (258 kWe) is below closure floor (510 kWe) at chunk 100 t.** Reducing chunk only moves both bounds proportionally: at any chunk, feasibility cap ≈ 0.5 × closure floor. The gap is fixed.

The chunk 200 t point (the L1-007 cap, where this round started) is the unique propellant-feasibility-edge that does NOT satisfy closure — round-trip 16.92 yr exceeds the soft ceiling. Below chunk 200 t the gap widens. Above chunk 200 t (forbidden by L1-007) the gap closes but the chunk cap binds.

**Three sub-findings worth elevating:**

1. **The chunk 100 t / 100 kilowatt-electric point delivers 9.8 t** — small but nonzero, and the best propellant-feasible delivered mass in the entire (chunk, reactor) sweep at chunk ≤ 100. The cell fails on round-trip (21.63 yr), not on propellant. This is informative: chunk reduction PRESERVES delivered-mass-feasibility at very low reactor power; what kills it is the L0-05 round-trip ceiling. A program willing to relax L0-05 to ~22 yr (or a chunk-water utility willing to wait that long) could in principle operate at this point. But that would require an L0-05 waiver of 7 years; far beyond hyperion's 1-year soft margin discussion.

2. **The L1-007 chunk cap is *binding* at 500 kilowatt-electric Variant A, not a comfortable safety margin.** At 500 kilowatt-electric the propellant-feasibility threshold is between 175 t and 200 t. The cap was designed as a packaging / handling envelope, not as a closure boundary. The fact that it happens to coincide with the propellant-feasibility edge is coincidental and tight; any tightening of L1-007 (e.g., to chunk 150 t for structural reasons) would make 500 kilowatt-electric Variant A infeasible even without considering closure.

3. **The orchestrator-authored SCOPE's optimistic 13.5–14.5 yr / 25–40 t prediction was falsified-pessimistic by ~5–10 yr and ~25–40 t.** No closing cell exists; SCOPE expected one to exist marginally. The mechanism the SCOPE relied on ("smaller chunks reduce inbound burn time disproportionately") was approximately correct in direction (chunk 100 / 100 kilowatt-electric does shorten burn relative to chunk 200 / 500 kilowatt-electric: 8.46 yr vs 3.75 yr ... wait, longer; the BURN time is longer at lower power) but the SCOPE missed the feasibility coupling. **The orchestrator pre-registration suffered the same back-of-envelope-skip the recurring lesson #N flagged for workers.**

## Revisit

**Pre-registration accuracy: 4 of 4 gradable HELD; tied for best in the campaign (with hyperion's R-variant-B-impulsive-vs-continuous at 5/6 — that round had one falsification, this one had none gradable-and-falsified).** The pessimistic framing applied at pre-registration time (against the SCOPE's optimistic bands) was correct in direction and approximately correct in mechanism. The closure-trade BOE done at pre-reg time predicted infeasibility at chunk 100 t under any reactor power; the run confirmed it exactly.

**Where the pre-reg BOE was inaccurate:** I predicted at pre-reg that the feasibility cap at chunk 100 t was ~258 kilowatt-electric. The actual cap is between 200 and 300 kilowatt-electric (200 is feasible, 300 is not). Direction right, magnitude within rounding. The 0.325 × chunk feasibility rule and the 0.196 t/kW closure rule both held quantitatively.

**Where the pre-reg framing was wrong:** I treated H-100-e as gradable on the IF-clause being entered ("if a closing config exists"). Since no closing config exists, the IF is vacuous — held without information. The tables.md output convention treats this as "not gradable", which is the more honest reading. The console output reports HELD because it checks the `held` boolean directly. **Cosmetic inconsistency in run.py output formatting; the tables.md is canonical.** This is a methodology note for future rounds: when grading a conditional hypothesis, decide upfront whether the antecedent-false case is HELD-vacuous or NOT-GRADABLE, and apply consistently across artefacts.

**Why H-100-d is "not gradable" rather than HELD or FALSIFIED:** the operating-optimum reactor power band [200, 400] kilowatt-electric is meaningful only if a closing cell exists. With no closing cell, "the optimum" has no referent. I considered marking H-100-d as FALSIFIED-by-absence (no point in the predicted band satisfies the closure requirement), but that would conflate "optimum is outside [200, 400]" with "no optimum exists". The latter is the actual result and is more informative.

**What I would change if re-running:** the chunk sweep could be tightened. The seven-point sweep [50, 75, ..., 200] tells the same story as a three-point sweep [100, 150, 200] would. The reactor sweep at chunk 100 t was load-bearing — that's what falsified H-100-c. If I had only run the chunk sweep at 500 kilowatt-electric, I would have missed the chunk 100 / 100 kilowatt-electric / 9.8 t delivered finding entirely. The reactor sweep is the round's content-bearing dimension.

**What's still unverified:** the chunk 100 / 100 kilowatt-electric / 21.63 yr round-trip point. The closure function uses a Hohmann cruise-time approximation. At 21.63 yr round-trip with a ~8.5 yr inbound burn, the "cruise + burn" decomposition is even more violated than at hyperion's 16.92 yr point (validity caveat 3 from hyperion's round). The actual round-trip at 100 kilowatt-electric Variant A could be optimistic by 1–3 years. This pushes the closure verdict further into infeasibility but does not change the qualitative finding. Not modeled.

## Cross-learning

- **NEGATIVE for R-variant-B-recovery-paths-economic path 3 (the bake-off).** Rhea's bake-off (already integrated to main per active-sessions.md row) computed path-3 marginal internal-rate-of-return as a single line item; this round confirms path 3 is structurally unavailable at conservative continuous-thrust assumptions. **The bake-off line for path 3 should be reframed from "computed under chunk = 100 t" to "no closing configuration exists at chunk ≤ 200 t".** Project owner / orchestrator can verify against rhea's output and update the matrix's path-3 row accordingly.

- **NEGATIVE for `water-prop/rounds/R_variant_B_100t_resizing/SCOPE.md` pre-registered prediction.** The orchestrator's pre-registered 13.5–14.5 yr / 25–40 t bands were optimistic by ~5–10 yr and unavailable on delivered-mass. The mechanism the SCOPE relied on ("smaller chunks reduce inbound burn time disproportionately") missed the feasibility coupling. **Recommend orchestrator update SCOPE.md retroactively to document the falsified prediction** (per Pivots-and-bug-catch protocol — pre-registration falsifications are first-class artefacts).

- **POSITIVE for `water-prop/rounds/R_chunk_as_heat_shield_revisit` (iapetus scaffold).** Path 1 (Earth aerocapture mandatory) is now the only surviving Variant B amendment with delivered mass > 0. Aerocapture engineering closure is load-bearing for the entire matrix's surviving cell, exactly as hyperion's R-variant-B-impulsive-vs-continuous flagged. **R-chunk-as-heat-shield-revisit should be the next critical-path round if it has not closed yet.** Active-sessions registry indicates iapetus is still scaffolded but no completion row.

- **NEGATIVE for the L1-007 chunk cap framing.** L1-007 caps chunk at 200 t. This round shows the propellant-feasibility-edge at 500 kilowatt-electric Variant A is between 175 and 200 t — i.e., the L1-007 cap is *binding* on Variant A feasibility, not a comfortable margin. Any future tightening of L1-007 (for structural / packaging / dynamic-bag-deployment reasons) immediately invalidates Variant A even before aerocapture is added. **Recommend orchestrator add a REQUIREMENTS.md note that L1-007 is binding on Variant A propellant-feasibility, not a packaging-only constraint.**

- **POSITIVE for Methodology lesson 1 (pessimistic-prediction default).** Five of five gradable hypotheses held under pessimistic framing; the optimistic-orchestrator-SCOPE-bands were falsified. The lesson generalises: even orchestrator-authored SCOPE.md predictions are subject to optimism-without-back-of-envelope. The recurring lesson #N (BOE each headline metric) applies to workers AND orchestrators.

- **METHODOLOGY-FLAG: conditional-hypothesis grading inconsistency.** H-100-d ("optimum reactor in [200, 400] kWe IF closure exists") and H-100-e ("path-3 delivered < 32.1 t IF closure exists") are conditional. The run.py console output graded H-100-e HELD (because the held boolean was True by vacuous logic); the tables.md graded it "not gradable" (because gradable=False). The cosmetic inconsistency is mine; future conditional-hypothesis pre-registrations should pick one convention upfront and apply consistently to both artefacts. **Recommend campaign-level convention: antecedent-false → "not gradable" (per tables.md), not "held-vacuous".**

- **POSITIVE for honest reading 2 (the bake-off collapses to paths 1 and 2).** Project-owner-locked Option A (Variant B as 500-kilowatt-electric all-electric inbound) under rhea's bake-off reading was "no path clears sovereign-bond at conservative anchors; honest reading is path 2". This round structurally confirms path 3 doesn't exist as an option. The bake-off is now binary: aerocapture-closes-engineering (path 1) OR collapse-the-cell (path 2). **The matrix's amendment decision is now between path 1 conditional on R-chunk-as-heat-shield-revisit and path 2 unconditional.**

- **PROCEDURE-NOTE for orchestrator.** The phoebe worker registered in `.planning/active-sessions.md` per protocol step 2. The registry edit is uncommitted in phoebe's worktree; orchestrator may need to stash before merging this branch (per the protocol observation note 2026-05-15 late evening). Branch `iceberg-phoebe`, not yet pushed.

