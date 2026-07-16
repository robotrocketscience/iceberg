# R-framework-matrix-parity — does the mission_graph framework reproduce the matrix's surviving cells once remaining constraints are encoded?

**Status:** scope, pre-study. Authored by Saturn (orchestrator), 2026-05-22 latest+15 → 16, walking `SATURN-PUNCH-LIST-20260521.md` items M-4 + S-1.

---

## Why this round

The mission_graph framework (under `water-prop/sims/mission_graph/`, merged this pass via `33e3062`) provides a unified phase-graph simulator that should be able to replay every round in the campaign as a single sweep. Saturn-worker's canonical sweep at L0-04 = 25 tonnes provisional (`20260521T193329Z`) surfaces ONLY chunk_mass_kg = 200,000 closing — the smaller-chunk band (5 / 10 / 25 / 50 / 100 tonnes) delivers below the L0-04 floor after ~80 percent rocket-equation losses during chunk-fed-spiral departure.

This DISAGREES with two prior matrix verdicts at conservative anchors:

- **titan-3 R-chunk-size-pareto (`1997a51`):** 4 cells close strict + L0-09 floor at chunk 50-60 tonnes / P = 30 kilowatt-electric / R12 lunar-gravity-assist Earth-arrival; 30 cells close waiver across 50-150 tonnes / 20-30 kilowatt-electric.
- **enceladus-r5 R-bus-mass-anchor-sweep (`3700de7` + `95565cf`):** 9 commercial+strict cells exist at Cassini-bus + hybrid aerocapture; 6 / 9 survive realistic 500-kilowatt-electric radiation shadow shield + power-control-unit + cables.

Both prior verdicts assumed architectures that the current mission_graph framework does NOT yet encode:

1. **Reactor lifetime versus cumulative full-power burn time** (axis 20, per enceladus-r5 R-reactor-lifetime-vs-burn-time `c685c52`). KRUSTY 28-hour flight-heritage is 3-4 orders of magnitude short of the 8-12 year cumulative burn the 25-year-window Architecture-E cells require. Cells at Kilowatt Reactor Using Stirling Technology specific power 2.4 watts-per-kilogram and L=5 year lifetime ceiling drop out entirely.
2. **Modular Assembled Radiators for Very Large systems bundled radiator-mass formula** (`5 t + reactor_kilowatt-electric × 0.1 t`, per locked belief `0418e2c9`). At megawatt-electric scale the bundled formula is closer to correct than the decomposed model that the framework currently inherits as default; the 40-watts-per-kilogram target essentially bets on deployable ultra-low-areal-density radiators that have not flown.
3. **Bus-mass conservative anchor floor on initial dry mass.** Heritage Cassini bus (~600 kilograms) and conservative bus (~2000 kilograms) give different cell counts; the framework needs the conservative anchor as the matrix basis-of-record per latest+12 retraction (preserved at line 25 of the matrix Current section).
4. **Corrected vis-viva delta-velocity anchors** (titan-3 R-delta-velocity-anchor-audit `42120cf`): Saturn-departure 7.7 kilometres-per-second (not 5.5); Earth-arrival 7.3 kilometres-per-second direct or 4.2 kilometres-per-second post-R12 lunar-gravity-assist (not 3.5). Mission_graph's Phase 4 departure and Phase 6 arrival need these anchors encoded as option preconditions.

**The framework-versus-matrix divergence is the load-bearing reading for whether the framework is matrix-replay-trustworthy.** If the framework reproduces titan-3's 4 cells + enceladus-r5's 6 / 9 cells once constraints 1-4 are encoded, the framework can replace ad-hoc per-round Python scripts as the canonical sweep substrate. If the framework still disagrees with the matrix after encoding constraints 1-4, the divergence is a bug in EITHER the framework OR the matrix — and tracking down which is the load-bearing engineering finding of this round.

**Round type:** primarily framework engineering (encode the four constraints in the framework's option executors and re-run sweeps), with a small amount of comparative cell-diff analysis. Bounded scope: this round does NOT introduce new architectural cells; it audits parity between two existing artifacts.

---

## The question this round answers

**Once the framework encodes constraints 1-4 above, do the framework's surviving cells reproduce the matrix's surviving cells at conservative anchors?**

Three sub-questions decompose this:

1. **titan-3 reproducibility:** does the framework reproduce titan-3's 4 cells at chunk 50-60 tonnes / P = 30 kilowatt-electric / Kilowatt Reactor Using Stirling Technology specific power 2.4 watts-per-kilogram / R12 lunar-gravity-assist Earth-arrival once constraints 1, 3, 4 are encoded?
2. **enceladus-r5 reproducibility:** does the framework reproduce enceladus-r5's 6 / 9 cells at Cassini-bus + hybrid aerocapture + 500 kilowatt-electric radiation-shielded power-control-unit once constraints 1, 2, 3 are encoded? (Note: 500-kilowatt-electric is retired per project-owner directive; this sub-question is preserved as a parity check on enceladus-r5's methodology, not as a live architectural option. If the round confirms enceladus-r5's cell count under enceladus-r5's anchors, the framework is methodologically validated against that body of work; the cells themselves remain retired.)
3. **mission_graph self-consistency:** does mission_graph's current 200-tonne-only closure cell (at sp = 800 seconds water-electrothermal, chunk-fed-spiral departure, direct propulsive inbound) survive the encoding of constraints 1, 2, 4? If the 200-tonne cell collapses under reactor lifetime or Modular Assembled Radiators for Very Large systems bundled radiator-mass, mission_graph's canonical sweep at L0-04 = 25 tonnes returns to zero surviving cells under conservative anchors.

The round's deliverable is a **cell-by-cell diff** between the framework's post-encoding surviving set and the matrix's surviving set, with a Reading at the bottom identifying any bug-class divergences and proposing where the bug lives (framework or matrix).

---

## Pre-registered hypotheses (worker's honest predictions)

| # | Hypothesis | Predicted range | Falsification band |
|---|---|---|---|
| H1 | Constraint 1 (reactor lifetime) drops mission_graph's 200-tonne closure cell at Kilowatt Reactor Using Stirling Technology specific power 2.4 watts-per-kilogram and any L ≤ 10 years. The cell currently anchors on water-electrothermal at 800 seconds; under realistic reactor lifetime, the cumulative full-power burn time across 11.93 years round-trip exceeds 28-hour flight heritage by 3-4 orders of magnitude, and the cell collapses on the same physics that killed Architecture E in enceladus-r5 R-reactor-lifetime-vs-burn-time. | mission_graph 200-tonne cell collapses at L = 5 years; survives at L = 15 years (effectively non-binding); transitional at L = 10 years. | H1 falsified if mission_graph cell survives at L ≤ 5 years AND Kilowatt Reactor Using Stirling Technology specific power 2.4 watts-per-kilogram. |
| H2 | Constraint 2 (Modular Assembled Radiators for Very Large systems bundled formula) shifts mission_graph's reactor-mass budget upward at flyable power. At P = 30 kilowatt-electric, bundled radiator mass = 5 + 30 × 0.1 = 8 tonnes versus current decomposed-model estimate of ~2-3 tonnes. The 5-tonne mass delta absorbs into the chunk budget, narrowing the closing chunk-mass band but not collapsing the 200-tonne cell. | Closing chunk band narrows by 20-40 tonnes; 200-tonne cell survives; smaller-chunk cells stay below L0-04 = 25 tonne floor. | H2 falsified if 200-tonne cell collapses purely on radiator-mass delta. |
| H3 | Constraint 4 (corrected vis-viva delta-velocity anchors) is the load-bearing constraint that splits mission_graph from titan-3. mission_graph's Phase 4 currently uses an informal 5.5-kilometres-per-second Saturn-departure anchor; encoding 7.7 kilometres-per-second forces ~38 tonnes of additional chemical propellant per 200-tonne mission, shifting mission_graph's closing chunk down from 200 tonnes toward the titan-3 40-80 tonne band. | mission_graph closing chunk shifts from 200 tonnes to 60-150 tonnes after vis-viva encoding. | H3 falsified if mission_graph closing chunk stays at 200 tonnes after vis-viva encoding. |
| H4 | Joint encoding of constraints 1 + 2 + 3 + 4 reproduces titan-3's 4 cells within ±20 percent on delivered mass and ±15 percent on round-trip time. Both frameworks model the same physics; differences should reduce to encoding choices, not architectural facts. | Cell-by-cell agreement within tolerance bands for the 4 titan-3 strict cells. | H4 falsified if any titan-3 strict cell disagrees with the framework's reproduction by > 30 percent on delivered mass OR > 25 percent on round-trip. |
| H5 | enceladus-r5 reproducibility (sub-question 2) is moot for live architecture but is methodologically valuable as a parity check on the framework. The 9 cells at Cassini-bus + hybrid aerocapture + 500 kilowatt-electric reproduce within tolerance; the 6 / 9 shielding-survival subset reproduces within tolerance. The cells themselves stay retired per the 500-kilowatt-electric directive. | enceladus-r5 cells reproduce within ±20 percent on delivered mass. | H5 falsified if enceladus-r5 cells disagree with framework reproduction by > 30 percent. |
| H6 (load-bearing reading) | After encoding constraints 1-4, the framework reproduces titan-3's 4 cells + enceladus-r5's 9-then-6 cells within tolerance. The framework is matrix-replay-trustworthy. The current 200-tonne mission_graph closure cell either survives (H1 + H2 falsify) and becomes a second-architecture surviving cell distinct from titan-3, OR collapses (H1 holds) and matrix returns to titan-3's 40-80 tonne band as the sole surviving cell. Either way, the framework can replace per-round Python scripts as the canonical sweep substrate; new architectural rounds work in the framework rather than in copy-paste files (which is what mimas's R-shared-physics-audit lesson 17 candidate calls "round-local redefinition with per-round drift"). | Reading-level: framework is matrix-replay-trustworthy; mimas lesson-17 cleanup completes via this round; 75-percent chunk-tow delivery anchor (matrix-item M-3) gets a framework-derived replacement. | H6 falsified if cell-by-cell diff shows persistent > 30 percent disagreement on any matrix surviving cell even after constraint encoding. The divergence then needs root-cause investigation in either the framework or the matrix. |

---

## Method (worker drafts the actual implementation)

**Step 1 — Encode constraint 1 (reactor lifetime).** Add `reactor_lifetime_years` field to `VehicleState` in `water-prop/sims/mission_graph/framework/state.py`. In each phase executor that runs the reactor at full power for non-trivial duration (Phase 1 chemical-electric departure, Phase 4 Saturn-departure, Phase 5 inbound cruise), accumulate burn-time into a derived `cumulative_full_power_burn_hours`. Add a phase precondition that rejects the option if `cumulative_full_power_burn_hours > reactor_lifetime_years × 8760`. Test against enceladus-r5 R-reactor-lifetime-vs-burn-time numbers as ground truth.

**Step 2 — Encode constraint 2 (Modular Assembled Radiators for Very Large systems bundled radiator-mass formula).** Replace whatever decomposed radiator-mass calculation the framework currently uses with the bundled formula `radiator_mass_kg = 5000 + reactor_kilowatt_electric × 100`. This is a single-function change; the math is locked-belief-anchored.

**Step 3 — Encode constraint 3 (bus-mass conservative anchor floor).** Add a phase precondition on `initial_dry_mass_kg` that rejects the option if `bus_mass_kg < 2000`. Document the heritage Cassini-bus alternative (~600 kilograms) as a comment but use 2000 as the conservative anchor per matrix latest+12 reading.

**Step 4 — Encode constraint 4 (vis-viva delta-velocity anchors).** Update Phase 4 (Saturn departure) option preconditions to use 7.7 kilometres-per-second as the Saturn-departure delta-velocity anchor when the architecture uses Oberth-optimised periapsis ellipse. Update Phase 6 (Earth arrival) option preconditions to use 7.3 kilometres-per-second direct OR 4.2 kilometres-per-second post-R12 lunar-gravity-assist tour. Document the corrections inline with reference to titan-3 R-delta-velocity-anchor-audit (`42120cf`).

**Step 5 — Re-run canonical sweep.** Run `water-prop/sims/mission_graph/missions/sweeps/saturn_water_canonical_sweep.py` at L0-04 = 25 tonnes provisional after constraints 1-4 land. Diff the surviving cell set against the pre-encoding sweep (saved as `20260521T193329Z`) and against titan-3's 4 cells + 30 cells.

**Step 6 — enceladus-r5 reproduction sub-sweep.** Author a one-off sweep that mimics enceladus-r5 R-bus-mass-anchor-sweep's parameter space (Cassini-bus + hybrid aerocapture + 500-kilowatt-electric radiation-shielded power-control-unit). Run it against the framework. Diff against enceladus-r5's stated 9 + 6 cells. The cells themselves are retired per project-owner directive; this sub-sweep is methodological parity check only.

**Step 7 — Diff report.** Produce `RESULTS.md` containing: the cell-by-cell diff for titan-3 reproducibility; the cell-by-cell diff for enceladus-r5 reproducibility; identification of any > 30 percent disagreements with root-cause analysis (framework bug versus matrix bug versus anchor-choice difference); reading-level recommendation on whether the framework is matrix-replay-trustworthy.

**Step 8 — Refresh 75-percent chunk-tow delivery anchor.** If H6 holds, the framework supplies a corrected per-mission delivery ratio that can replace the 75-percent pitch-headline number. Compute the delivery ratio at the framework's surviving cells and produce a one-page note for the pitch (input to a future R-pitch-arithmetic-audit pass).

---

## Out of scope

- Authoring new architectural cells. This round audits parity between two existing artifacts; new architecture goes in a separate SCOPE.
- Resolving project-owner decision points #14 or #15. The framework parity audit is upstream of those decisions; it produces a clean substrate for future rounds, not a verdict on power class or L0-04 strict.
- Modifying the matrix's HISTORY entries or the surviving-cell readings in the matrix Current section. Those reflect adjudicated state; this round produces inputs for a future matrix update, not the update itself.
- Per-round migration of contaminated rounds onto the canonical `waterprop.propulsion.burn_from_wet` / `burn_from_dry_end` helper pair. That migration is mimas's open follow-on (READING.md "Next-round candidates"); not this round.

---

## Inputs to acquire (reading order)

1. `water-prop/sims/mission_graph/README.md` — framework overview.
2. `water-prop/sims/mission_graph/framework/state.py`, `phase.py`, `option.py`, `sweep.py` — framework internals.
3. `water-prop/rounds/R_chunk_size_pareto/` — titan-3 source rounds.
4. `water-prop/rounds/R_bus_mass_anchor_sweep/` — enceladus-r5 source rounds.
5. `water-prop/rounds/R_reactor_lifetime_vs_burn_time/` — enceladus-r5 reactor-lifetime ground truth.
6. `water-prop/rounds/R_megawatt_marvl_radiator/` — Modular Assembled Radiators for Very Large systems formula source.
7. `water-prop/rounds/R_assumption_audit_2026_05_21/` — saturn-worker canonical sweep `20260521T193329Z` and audit findings.

---

## Deliverables (in commit order)

1. `STUDY.md` — pre-registered hypotheses H1-H6 frozen before running the framework sweeps.
2. Framework constraint encoding commits (Step 1-4) as separate atomic commits per constraint.
3. Canonical sweep re-run output saved to `results/canonical_sweep_post_encoding.json`.
4. enceladus-r5 reproduction sub-sweep output saved to `results/enceladus_r5_reproduction.json`.
5. `RESULTS.md` — cell-by-cell diff and reading-level recommendation.
6. `READING.md` — load-bearing reading (H6 verdict); 75-percent chunk-tow delivery anchor replacement note.
7. Handoff doc to orchestrator (`~/.claude/handoffs/iceberg-<worker>-<date>-framework-matrix-parity.md`).

---

## Suggested worker

Any moon, but best fit: comfortable with Python framework engineering (the round is mostly framework-encoding) AND with the matrix's history of conservative-anchor adjudications. Mimas would be a good fit (already familiar with the framework substrate from R-shared-physics-audit); iapetus would be a good fit (familiar with the staged-options program-class reframing that depends on this audit landing).

---

## Cross-references

- Matrix `water-prop/docs/ARCHITECTURE-DECISION-MATRIX.md` — axis 02 (surviving cell), axis 05 (reactor power floor), axis 09 (chunk-mass cap), axis 20 (reactor lifetime), and the High-leverage open rounds section flag this round as `R-framework-matrix-parity` (punch-list M-4 / S-1).
- Design-axes `design-axes/05-reactor-power-floor.md` and `design-axes/09-chunk-mass-cap.md` — both Current sections flag this round as the load-bearing reading for framework-versus-matrix divergence.
- Punch list `SATURN-PUNCH-LIST-20260521.md` items M-4 (framework-parity check) + S-1 (R-framework-matrix-parity SCOPE) + M-3 (75-percent chunk-tow delivery anchor refresh).
- Mimas READING.md "Next-round candidates" → per-round migration onto canonical `waterprop.propulsion` helper-pair is the follow-on after this round confirms the framework is matrix-replay-trustworthy.
