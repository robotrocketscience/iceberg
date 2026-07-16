# R-smaller-vehicle-demonstrator-envelope — does ICEBERG demonstrator close at sub-50-t vehicle?

**Status:** scope, pre-study. Authored by Saturn (orchestrator, in-session), 2026-05-26.
**Predecessors:** project-owner H6 cascade decision 2026-05-26 (demonstrator-class promoted); R-chunk-capture-monte-carlo Tier 1 (`464927e`, ram-scoop posterior median 0.405); R_assumption_audit_2026_05_21 A12 ("vehicle mass grid anchored to launcher capacities, not vehicle physics minimums").

## Premise

The R_assumption_audit_2026_05_21 BEST_ARCHITECTURES_25T.md sweep found vehicle mass floors at {50, 63, 100} t — not because of physics, but because the sweep grid was anchored to single-Falcon-Heavy-or-larger launcher capacities. Project owner question 2026-05-26: "why does the initial vehicle need to be 50 t?"

Audit A12 already SCOPE'd a smaller-vehicle sweep (`audit_smaller_vehicle_and_water_met_isp.py`) that extends vehicle_mass_kg DOWN to 10 t and chunk_mass_kg DOWN to 5 t — explicitly to probe the demonstrator-mission corner. The sweep was authored but **never run**. This round runs it and applies Tier-1 capture-probability realism on top.

Under the project-owner H6 cascade decision (2026-05-26), demonstrator-class missions operate under the §7.5 waiver: "any non-zero mass delivered." The 25-tonne L0-04 floor that the 50 t vehicle sweep was anchored to is moot for demonstrator-class. **This round's success criterion is therefore non-zero delivered, not 25 t delivered.**

## Pre-registered hypotheses

H1: **A sub-30-tonne vehicle dry mass closes the demonstrator-class envelope** (any non-zero delivered at LEO_depot, Tier-1 capture-probability applied). Falsified if no vehicle below 30 t produces a non-zero closure at any chunk size or specific impulse.

H2: **The vehicle-mass floor scales with chunk mass.** Specifically: the smallest vehicle that closes is roughly linear in chunk mass, because the chunk-as-propellant-tank delta-velocity lever scales with chunk mass and the vehicle's subsystem floor (communications, guidance, control) is roughly chunk-independent. Falsified if vehicle-mass floor is constant across chunk sizes.

H3 (load-bearing): **At least one (vehicle ≤ 20 t, chunk ≤ 50 t) cell closes the demonstrator envelope** with a delivered mass posterior above 0.5 t (a credible engineering minimum for "non-zero delivered" — anything below this is essentially a sample-return). Falsified if the smallest-closing cell requires vehicle > 20 t or chunk > 50 t.

H4: **Water-electrothermal specific impulse is the dominant axis** at the demonstrator scale. At 200 t chunk and 50 t vehicle, specific impulse was second-order behind capture-efficiency (per the assumption audit). At 10-30 t vehicle and small chunk, the chunk-as-propellant-tank lever is smaller, so specific impulse becomes more load-bearing. Falsified if vehicle mass or chunk mass shows higher marginal-closure sensitivity than specific impulse in the sweep.

## Methodology

1. Run the existing `audit_smaller_vehicle_and_water_met_isp.py` sweep (288 cells, ~5 minutes runtime).
2. Apply Tier-1 capture-probability realism: multiply each cell's delivered mass by 0.48 (the ratio of Tier-1 ram-scoop median 0.405 to the audit's 0.85 anchor). Honest disclosure: this is a first-order correction, not a recomputation — the sweep's framework uses the 0.85 anchor in its Phase 3 capture stage, and a proper redo would re-derive each cell with the new capture probability per the framework's mission-graph executor. The first-order multiplier is defensible at this fidelity tier; a Tier-2 redo would carry the full Tier-1 capture-probability posterior through the framework.
3. Verdict on H1-H4 against the corrected cells.

Out of scope: contact-fidelity (Tier 2/3); financial NPV; Earth-aerocapture demonstrator profile.

## Deliverables

1. This SCOPE.md.
2. STUDY.md with H1-H4 pre-registered.
3. `run_sweep.py` — invokes the existing audit sweep with Tier-1 capture-probability realism applied post-hoc.
4. `results/sweep_report.md` — raw sweep output (at 0.85 anchor) plus Tier-1-corrected closure tables.
5. FINDINGS.md — verdict on H1-H4 and matrix amendment specification.

## Priority

**MEDIUM-HIGH.** Directly addresses the project-owner question. Cheap to run. Outcome determines whether the demonstrator-class promotion has a clear architectural floor or whether it's bounded by launcher economics rather than physics.
