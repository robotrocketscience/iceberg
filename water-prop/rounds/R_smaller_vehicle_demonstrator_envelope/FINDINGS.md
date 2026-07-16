# R-smaller-vehicle-demonstrator-envelope — FINDINGS

**Round:** R-smaller-vehicle-demonstrator-envelope
**Date:** 2026-05-26
**Status:** baseline-only. Round superseded by methodology gap surfaced mid-execution.
**Author:** Saturn (orchestrator, in-session)
**Raw results:** `water-prop/sims/mission_graph/runs/audit_smaller_vehicle_water_met/20260526T191056Z/`

## HEADLINE — methodology gap, not closure verdict

**This round's closure tables ARE NOT a defensible engineering result.** They are a baseline record of what the current mission_graph framework returns when vehicle dry mass is treated as a free sweep parameter. Mid-execution, the project owner identified that the framework's treatment of vehicle dry mass is fundamentally wrong: vehicle dry mass should be a *derived* quantity computed from per-phase mass demands, not an *input* assumed by the sweep.

The sweep ran 288 cells with vehicle dry mass in {10, 20, 30, 50, 63, 100, 150, 200} tonnes, chunk mass in {5, 10, 25, 50, 100, 200} tonnes, water-electrothermal specific impulse in {400, 500, 600, 700, 800, 900} seconds (back-propagated to 58744 cells through architecture variations). 2724 cells (4.6 percent) close the 30-tonne delivered-floor.

**Headline that survives the gap:**

- All closing cells use chunk mass = 200 tonnes (the sweep maximum). Confirms the audit's prior finding: at the existing framework's fidelity, only the largest swept chunk size closes any delivered-floor threshold above ~10 tonnes.
- Closing cells span vehicle dry mass 10-63 tonnes. **At face value, this would say a 10-tonne vehicle closes a 30-tonne delivered mission. The methodology gap below explains why this is not credible.**
- Water-electrothermal specific impulse must be at least 600 seconds for any closure; closure rate climbs from 0.5 percent at 600 s, to 7.0 percent at 800 s, to 10.7 percent at 900 s.
- Power was held fixed at 100 kilowatts-electric in the sweep; the audit's prior finding that 30-kilowatt-electric closure cells exist at larger vehicle mass is not contradicted here.

**Headline that does NOT survive the gap:**

- The 10-tonne and 20-tonne vehicle closure cells (~821 and ~677 cells respectively, marginal closure 4.5 and 4.7 percent) **almost certainly do not represent self-consistent designs**. A 10-tonne vehicle carrying the capture mechanism (~10-15 tonnes for a 200-tonne chunk) plus reactor + shield (~3 tonnes) plus radiators (~6 tonnes at flown specific power) plus thermal protection for Earth aerocapture (~5-10 tonnes) plus structure (~10 tonnes) plus communications + guidance + computers (~2 tonnes) is internally inconsistent before considering propellant. The framework's "10-tonne vehicle closes" answer hides the fact that the phases would demand 30+ tonnes of subsystem mass for the choices the cell assumes.

## The methodology gap

Project-owner observation 2026-05-26 (paraphrased): vehicle sizing should be a function called at each phase node in the concept-of-operations graph, with mass demands propagating both upstream and downstream. Currently it is a boundary condition.

**Current framework data flow:**

```
sweep axes (including vehicle_mass_kg) -> walk phases -> delivered_mass
```

The framework's `VehicleState.mass_kg` is set from the sweep axis and walked forward. Per-phase operations consume propellant and adjust mass, but no phase reports back a *required* dry-mass contribution to the vehicle. So vehicle dry mass is never checked for self-consistency against the demands the phases impose.

**What the framework needs to become:**

```
sweep axes (NOT including vehicle_mass_kg) ->
  guess vehicle_mass_kg ->
    walk phases, accumulate per-phase dry-mass demands
    (capture_mechanism_mass, reactor_and_shield_mass, radiator_mass,
     power_conversion_mass, thermal_protection_mass, structure_mass,
     communications_and_GNC_mass, tankage_mass) ->
    sum demands + dry-margin ->
    new vehicle_mass_kg ->
  iterate until fixed point OR non-convergence flag ->
delivered_mass + self-consistent vehicle_mass_kg + convergence flag
```

Cells that fail to converge represent mutually inconsistent design choices and should NOT be counted as closures. The current framework happily includes them because it does not check.

## What this round preserves and what it retires

**Preserves:**

- Specific-impulse sensitivity (closure rate climbs steeply with water-electrothermal specific impulse from 600 to 900 seconds). This is a physics statement about Tsiolkovsky bookkeeping; it does not depend on vehicle-mass closure.
- The pattern that only 200-tonne chunks produce non-zero closure at any meaningful delivered-floor. This is consistent with the chunk-as-propellant-tank delta-velocity-leverage argument and does not depend on vehicle-mass closure.

**Retires:**

- The 10-tonne and 20-tonne vehicle closure cells are artifacts of the boundary-condition treatment of vehicle dry mass.
- The "vehicle mass floor for demonstrator class" question this round was meant to answer is NOT answered by this round. It will be answered by R-vehicle-mass-closure-refactor.

## Hypothesis verdicts (conditional)

All four pre-registered hypotheses (H1: sub-30-tonne vehicle closes; H2: vehicle-mass floor scales with chunk mass; H3: at least one (vehicle ≤ 20 t, chunk ≤ 50 t) cell closes with delivered ≥ 0.5 t; H4: specific impulse dominates at small scale) are **unverdictable on this evidence**. The framework's vehicle-mass treatment prevents any verdict from being defensible.

The hypotheses stay pre-registered; they will be re-tested by R-vehicle-mass-closure-refactor.

## Cascade

1. R-vehicle-mass-closure-refactor SCOPE'd (this commit).
2. Methodology lesson candidate appended for PROTOCOL.md ratification: vehicle mass is a derived quantity; sweep axes must not include design-closure outputs.
3. Prior rounds' absolute closure-mass numbers are conditionally preserved — their relative orderings and structural verdicts likely survive the refactor, but specific delivered-mass numbers at specific vehicle masses (e.g., "39.5 tonnes at vehicle 50 tonnes") need re-derivation. Catalog deferred to R-vehicle-mass-closure-refactor's audit phase.

## What I'd recommend reading next

`water-prop/rounds/R_vehicle_mass_closure_refactor/SCOPE.md` (this commit) for the full methodology fix.
