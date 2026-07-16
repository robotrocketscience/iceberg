# R-vehicle-mass-fidelity-refinement — derive propellant from delta-velocity, audit mass-demand functions against Wertz, add path-conditional thermal protection

**Status:** scope, pre-study. Authored by Saturn (orchestrator), 2026-05-26 latest+24.
**Predecessor:** R-vehicle-mass-closure-refactor (titan-6, integrated at merge `08fbef9`) — the closed-loop framework lands and produces a self-consistent dry mass at the canonical cell of 120.8 tonnes vs the audit's mis-read 50 tonne (wet) anchor. Titan flagged three coordination items (D1, D2, D5) at handoff; D5 names this round as the successor.

## Premise

Titan-6's `saturn_water_v1` closed-loop framework produces self-consistent vehicle dry mass via per-subsystem demand-function fixed-point iteration, fixing the lesson-21 methodology gap. The framework lands with three known-soft anchors that the closure result is sensitive to:

1. **Propellant fraction is hard-coded at 0.80.** Heavier dry mass cannot do the 7.3 km/s chemical departure burn at 80 percent propellant fraction. The "0 cells arrive" headline is sensitive to this constant: relaxing the propellant fraction (e.g., deriving it per phase from delta-velocity and specific impulse via Tsiolkovsky) could move the collapse from "uniform" to "partial" — collapse *direction* is robust per titan-6 H4 verdict, but collapse *completeness* is not. (titan-6 D5.)

2. **Per-subsystem mass-demand functions** use a mix of locked beliefs (KRUSTY 2.4 W/kg + MARVL anchors at locked finding 4) and first-pass SCOPE anchors. Some demand functions (e.g., reactor + shield, radiators, power conversion) are well-anchored against flown / desk-study data. Others (capture mechanism, thermal protection system, primary structure, communications floor) are first-pass anchors not yet reviewed against published spacecraft mass-fraction references.

3. **Thermal protection mass is currently a single scalar.** It should be path-conditional: Earth-aerocapture demands different thermal protection from direct-propulsive return, and Saturn-aerocapture (if revisited) demands different thermal protection from Saturn-orbit-insertion-propulsive. Hard-coded single TPS mass hides the path choice's mass impact.

## Pre-registered hypotheses

H1: **Deriving propellant fraction per-phase from delta-velocity and specific impulse (Tsiolkovsky-anchored, with margin) moves the closed-loop closure count from 0 of 150 to a non-zero count at ≥ one architecture.** Falsified if closed-loop closure count stays at 0 of 150 under any reasonable per-phase propellant-fraction derivation.

H2: **The reactor + shield + radiators mass-demand functions are within 30 percent of Wertz Space Mission Engineering (SMAD) chapter 11-anchored values, OR the discrepancy is fully attributable to the locked-finding KRUSTY 2.4 W/kg + MARVL flown anchors being more conservative than SMAD's published mass fractions.** Falsified if a Wertz-anchored review surfaces a more-than-30-percent unexplained discrepancy in either direction.

H3: **The capture mechanism mass-demand function (currently parameterised per architecture: harpoon, ram-scoop bag, everting sleeve) is the largest single source of dry-mass uncertainty in `saturn_water_v1`.** Falsified if total-order sensitivity index for the capture-mechanism mass-demand parameters is below 0.15 in a sensitivity analysis.

H4: **Path-conditional thermal protection (Earth-aerocapture vs direct-propulsive vs Saturn-aerocapture vs Saturn-orbit-insertion-propulsive) changes the closed-loop closure count by at least 5 percent of cells.** Falsified if path-conditional thermal protection produces less than 5 percent change in closure count vs the current single-scalar treatment.

H5 (load-bearing): **None of H1, H3, H4 alone or in conjunction produces a closed-loop closure rate above 5 percent at L0-04 = 25 tonnes.** I.e., the refactor's overall verdict (titan-6 H4 held: closures collapse) survives all the fidelity refinements this round considers. Falsified if any combination of refinements produces > 5 percent closure rate at L0-04 = 25 t. Reading-if-held: the campaign's structural verdict that no architecture closes commercial-class L0-04 is robust to mass-model fidelity. Reading-if-falsified: the refactor was too pessimistic; specific subsystem-mass anchors need revising before the matrix amendment cascades through.

H6: **Wet-vs-dry confusions exist in at least one other prior round's anchor.** Titan-6's BACK_TEST surfaced the "50 t was WET, not DRY" 12× error in the audit baseline. This is likely not unique; lesson 22 candidate implies "confirm wet-vs-dry before comparing a derived number to a prior anchor." Falsified if a sweep across all prior rounds' published vehicle-mass anchors finds no other wet-vs-dry misreading.

## Methodology

### Implementation slices

1. **Per-phase propellant-fraction derivation.** Add a `propellant_fraction(phase)` function to the framework that returns Tsiolkovsky-anchored values per phase given the phase's Δv and specific-impulse contract. Conservative margin (factor 1.10 propellant + 0.05 residual) per standard space-systems practice. New cells in the sweep carry per-phase propellant fractions instead of the hardcoded 0.80.

2. **Wertz / SMAD anchor review** for each subsystem mass-demand function:
   - Reactor + shield (current: 5,000 + 0.2 × power_kWe; locked finding KRUSTY 2.4 W/kg)
   - Radiators (current: power_kWe × 1000 / specific_power; MARVL anchors)
   - Power conversion (current: 0.1 × power_kWe + 500)
   - Thrusters + tankage (current: 50 × thrust_N + 0.05 × propellant)
   - Capture mechanism per architecture (harpoon, ram-scoop bag, everting sleeve — first-pass)
   - Earth-aerocapture TPS (current: 0.10 × chunk + 200 × entry_v_km_s — first-pass)
   - Primary structure (current: 0.05 × chunk + 100 × max_load_kN — first-pass)
   - Communications + guidance + computers (current: 2,000 kg floor — invariant)
   - Dry margin (current: 0.20 × subtotal — standard NASA Class B)

   For each: cite Wertz SMAD chapter, NASA reference, or flown-spacecraft mass-statement; flag any > 30 percent discrepancy.

3. **Path-conditional thermal protection.** Refactor `tps_mass_demand(context)` to dispatch on `context.return_path` ∈ {earth_aerocapture, direct_propulsive, saturn_aerocapture, saturn_orbit_insertion}. Each path gets its own anchor — Earth-aerocapture from Stardust + Genesis + Hayabusa heritage; direct-propulsive at zero (no TPS needed but propellant penalty in H1's bookkeeping); Saturn-aerocapture from Cassini Huygens + the latest+18 falsified phoebe round's anchors as upper bound; Saturn-orbit-insertion-propulsive from Cassini SOI mass statement.

4. **Sweep re-run.** Repeat titan-6's canonical 150-cell sweep with H1 + H3 + H4 changes layered in. Three sub-sweeps: (a) H1 only; (b) H1 + H4; (c) H1 + H3 + H4. Report closed-loop closure counts at L0-04 = {0, 10, 25 t}. Tests H5.

5. **Wet-vs-dry audit (H6).** Across all prior rounds' STUDY.md / SCOPE.md / FINDINGS.md / READING.md, grep for any vehicle-mass / dry-mass / launch-mass anchor with units. Cross-reference against the framework's wet-vs-dry distinction. Flag every prior-round anchor that is ambiguous or misnamed. Report as a methodology-cleanup table; the round does not re-derive the prior verdicts (per titan-6 verdict — structural readings survive), only catalogs.

## Out of scope

- Contact-fidelity simulation (R-chunk-capture-contact-fidelity SCOPE'd separately).
- Capture-architecture trade resolution (rhea's R-ramscoop-foundational-premise-revisit already decisive: harpoon wins after delta-velocity bookkeeping; contact-fidelity will refine).
- Adding new phases or architectures to `saturn_water_v1`.
- Re-running every prior round's full sweep (catalog only; specific re-runs are gated on H5 verdict).

## Deliverables

1. This SCOPE.md.
2. STUDY.md with H1-H6 pre-registered.
3. `framework/propellant_fraction.py` — per-phase Tsiolkovsky-anchored derivation.
4. `framework/tps_path_conditional.py` — path-conditional thermal protection dispatch.
5. `wertz_anchor_review.md` — per-subsystem citation + discrepancy table.
6. `sweep_re_run.py` + `results/refinement_closure_counts.json` — three sub-sweeps comparing baseline vs H1 / H1+H4 / H1+H3+H4.
7. `wet_vs_dry_audit.md` — prior-round anchor catalog with wet-vs-dry annotations.
8. FINDINGS.md with verdict on H1-H6 + matrix amendment specification.

## Predecessor work

- R-vehicle-mass-closure-refactor (titan-6, integrated `08fbef9`) — established the closed-loop framework and surfaced the 50-t-was-wet 12× error.
- PROTOCOL methodology lesson 21 (Saturn, integrated `65d2f48`) — vehicle dry mass is a derived quantity, not a sweep axis.
- PROTOCOL methodology lesson 22 candidate (titan-6, awaiting ratification) — confirm wet-vs-dry before comparing a derived number to a prior anchor.
- Locked findings 1, 4 (KRUSTY 2.4 W/kg + MARVL anchors) — the well-anchored half of the per-subsystem demand functions.

## Priority

**HIGH.** The refactor verdict (no closures) is currently the campaign's most consequential structural finding. Its robustness to fidelity refinements is load-bearing for the matrix amendment cascade. If H5 holds, the matrix amendment can land with confidence; if H5 falsifies, the refactor needs revision before cascading.

## Suggested worker

titan (re-spawn 7) is best-fit — framework familiarity, prior delta-velocity bookkeeping rounds, just authored `saturn_water_v1`. Alternative: hyperion (mass-anchor audit experience from R-bus-mass-anchor-adjudication, R-marvl-mass-anchor-validation).
