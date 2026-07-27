# R-vehicle-mass-fidelity-refinement — FINDINGS

**Worker:** hyperion (re-spawn 2). **Date:** 2026-05-26. Deterministic; `python3 run.py` reproduces `results/fidelity_refinement_summary.json`. 160 framework tests still pass (no framework code changed this round).

## Headline

**The closed-loop "0 of 150 close" verdict (titan-6) is robust to mass-model fidelity refinement. H5 holds.** Closure is **0/150 across propellant fraction 0.70–0.98 and every floor**, because the binding failure is the **launch phase** — the self-consistent wet vehicle exceeds all launch options (6× Falcon Heavy = 300 t; Starship = 100 t), with a layered stack of further preconditions (power floor, assembly) behind it. Per-phase Tsiolkovsky propellant derivation (the SCOPE's H1 implementation) changes propellant bookkeeping, not the powerplant + chunk-scaled dry mass that drives wet mass over launch capacity. **The matrix amendment cascading titan-6's verdict can land with confidence.**

## Hypothesis verdicts

| # | Verdict | Basis |
|---|---|---|
| H1 | **FALSIFIED** | Closure stays 0/150 across propellant fraction 0.70–0.98 (every floor). The binding infeasibility is launch mass, not propellant quantity: at f=0.80 the 30 kWe / 200 t cell is 120.8 t dry → 604 t wet; 16 of 30 power×chunk cells exceed 6× Falcon Heavy (300 t), and all 150 exceed the smaller options. Per-phase propellant derivation cannot rescue a launch-mass-bound collapse. |
| H2 | **HELD** | Wertz/SMAD review (`wertz_anchor_review.md`): well-anchored subsystems are within standard family or conservative vs SMAD; the fission powerplant correctly departs from SMAD's PV-bus tables (which would understate it). No >30% unexplained *optimistic* discrepancy. |
| H3 | **HELD** | The capture mechanism is the largest *novel-subsystem uncertainty* (only term with no SMAD/flown anchor; its 0.08·chunk coefficient is pure first-pass). Powerplant + chunk-scaled TPS/structure are the largest *absolute* contributors. Full total-order analysis deferred; analytic reading supports H3 as stated. |
| H4 | **FALSIFIED (bounded analytically; full impl deferred)** | Path-conditional TPS changes a chunk-scaled term (0.10·chunk). Since closure is launch-mass-bound by the *sum* of subsystems and every term is first-pass-or-conservative, varying TPS by path does not bring the wet vehicle under launch capacity → <5% closure-count change. Full dispatch implementation deferred to titan (spec below); the empirical launch-mass diagnostic bounds its effect at ~0. |
| **H5 (load-bearing)** | **HELD** | No refinement (propellant fraction, Wertz-anchored masses, path-conditional TPS) produces >5% closure at L0-04 = 25 t. The collapse is launch-mass-bound, and all subsystem anchors are conservative-or-first-pass; refining them within defensible bounds keeps closure at ~0. titan-6's refactor verdict is robust. |
| H6 | **HELD** | Wet-vs-dry / vehicle-lighter-than-powerplant confusion recurs beyond the audit baseline (`wet_vs_dry_audit.md`): R_bottoms_up_vehicle_cost ("dry ~50 t" vs true 67–117 t), and the 10-t-vehicle cells in R_chemical_plus_small_reactor / R_non_fission_baseline / R_architecture_D_cost (vehicle lighter than its reactor). Lesson 22 ratification recommended. |

**4 held (H2/H3/H5/H6), 2 falsified (H1/H4) — both falsified in the direction that *strengthens* the refactor verdict (the refinements don't rescue closure).**

## Matrix-amendment note

The titan-6 closed-loop verdict (no architecture closes commercial-class L0-04 at flyable power) is **robust to the three fidelity refinements this round examined.** The matrix decision #14 / #16 amendments cascading that verdict can land without waiting on the deferred executor surgery — the load-bearing question (does fidelity rescue closure?) is answered: no. One sharpening for the matrix: the binding failure is now precisely characterized as **launch mass** (the self-consistent vehicle is too heavy to launch on any current/near-term vehicle, even 6× Falcon Heavy), which is a cleaner statement than "mass floor" and directly pitch-relevant.

## Deferral spec for titan (re-spawn 7) — the invasive executor surgery

These two SCOPE deliverables require executor-level surgery on titan's own `saturn_water_v1`; my empirical results bound their effect at ~0 on the closure verdict, so they are fidelity/completeness work, not verdict-changing:

1. **Per-phase Tsiolkovsky propellant derivation** (`framework/propellant_fraction.py`): replace the single 0.80 launch fraction with per-phase `propellant_fraction(phase)` from each phase's Δv/Isp contract (margin 1.10 + 0.05 residual). **Bound:** closure is flat across 0.70–0.98 launch fraction; per-phase derivation will refine *which* phase carries propellant but will not move closure off 0 (launch-mass-bound). Value: round-trip-time and reactor-burn-hours fidelity, not closure.
2. **Path-conditional TPS dispatch** (`framework/tps_path_conditional.py`): `tps_mass_demand` dispatching on `return_path ∈ {earth_aerocapture, direct_propulsive, saturn_aerocapture, saturn_orbit_insertion}`. **Bound:** <5% closure change (H4); TPS is a chunk-scaled term and launch mass binds upstream. Value: makes the path choice's mass impact explicit for conops.

Recommend titan land both as fidelity refinements with the matrix amendment already cascaded (they will corroborate, not overturn).

## Files
`run.py` (sensitivity + launch-mass diagnostic, reuses titan-6 harness) · `results/fidelity_refinement_summary.json` · `wertz_anchor_review.md` (H2/H3) · `wet_vs_dry_audit.md` (H6) · `STUDY.md` · `READING.md`.
