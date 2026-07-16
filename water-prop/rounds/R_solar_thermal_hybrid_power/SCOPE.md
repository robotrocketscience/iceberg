# R-solar-thermal-hybrid-power — hybrid reactor + solar power architecture

**Status:** scope, pre-study. Authored by Saturn (worker), 2026-05-21 latest. Surfaced by user during the Phase 2 / Phase 1b expansion round.

**Context.** The mission_graph framework currently treats `power_available_kwe` as a constant scalar on `VehicleState`. The lightweight solar-thermal gating added in commit `89a1b82` rejects solar-thermal power as a sole power source for outer-system burns — at Saturn the solar flux is ~1 percent of Earth's, so a 20 kilowatt low-Earth-orbit solar array delivers only ~200 watts at Saturn. That gate is correct as far as it goes.

But the project owner surfaced a sharper architectural insight: **a vehicle carrying both a small reactor AND a large solar array is not dominated by either pure architecture.** The combination unlocks dial-up thrust on the inbound leg as the spacecraft approaches the sun.

Worked example with 10 kilowatt reactor + 20 kilowatt low-Earth-orbit-equivalent solar array, inbound from Saturn:

| Location | Distance (AU) | Solar contribution | Reactor | Total |
|---|---:|---:|---:|---:|
| Saturn (departure) | 9.5 | 0.22 kW | 10 kW | 10.2 kW |
| Jupiter (mid-cruise) | 5.2 | 0.74 kW | 10 kW | 10.7 kW |
| Asteroid belt | 2.7 | 2.7 kW | 10 kW | 12.7 kW |
| Mars vicinity | 1.5 | 8.9 kW | 10 kW | 18.9 kW |
| Earth (arrival) | 1.0 | 20 kW | 10 kW | 30 kW |

Inbound spacecraft has 3x more power on Earth approach than at Saturn departure. That power surplus on the final approach is exactly when the vehicle wants more thrust authority: trajectory refinement, lunar gravity assist setup, final spiral into low-Earth-orbit depot.

This round answers: **does a hybrid reactor + solar power architecture move ICEBERG closure thresholds enough to be worth the framework structural change required to model it, vs sticking with a constant-scalar power_available_kwe?**

## What needs to change in the framework

1. `VehicleState` gains two fields: `reactor_power_kwe` (constant), `solar_panel_leo_kwe` (sized at low-Earth-orbit equivalent). The current `power_available_kwe` becomes a *derived* function of location.
2. Each phase executor that ends up at a new location needs to recompute the effective `power_available_kwe` based on the heliocentric distance of that location. Phase 4 departure, Phase 5 cruise legs, Phase 6 arrival all need this.
3. Each phase precondition that gates on `power_available_kwe` needs to read the new derived value.
4. The sweep needs to gain axes for `reactor_power_kwe` and `solar_panel_leo_kwe` separately.

This is the same machinery as the deferred task #19 "reactor power class as phase-gating parameter" — the right time to do that work is alongside this round.

## Predecessor work

- `R_hybrid_solar_augmentation` (existing round) — explored adjacent hybrid ideas.
- `R_chemical_plus_small_reactor` (existing round) — the chemical-plus-small-reactor architectural variant, conceptually related.
- Commit `89a1b82` on iceberg-saturn — current lightweight solar-thermal gate that this round will supersede.

## Locked beliefs that constrain this work

- ICEBERG power finding 1 (0d5c882c): 40 watts-per-kilogram megawatt-class specific power is paper-study aspirational. A small reactor in this architecture is OK; megawatt is not the goal.
- ICEBERG power finding 2 (776575c0): 0-of-6 US fission programs reached orbit since 1965. Treat any reactor-dependent architecture as schedule-risk-heavy.
- ICEBERG power finding 3 (edcfe909): Fission Surface Power Phase 2 award not yet made as of May 2026. Small-reactor heritage path is uncertain.
- ICEBERG power finding 4 (0418e2c9): At megawatt scale, radiator mass dominates. A 10-kilowatt reactor is below that regime; radiator mass is sub-dominant.

The combination says: 10 kilowatt reactor + 20 kilowatt solar is in the **most program-friendly** corner of the reactor-program risk space (small enough to avoid the megawatt-radiator-mass problem, small enough that Kilopower-class flight heritage is plausible).

## Deliverables

1. Extended VehicleState with `reactor_power_kwe` + `solar_panel_leo_kwe`. Backward-compatible default: if only `power_available_kwe` is set, treat as constant reactor.
2. Heliocentric-distance-aware power function in framework.
3. New `R_hybrid_power_sensitivity` round (separate, follow-on) sweeping reactor 0-50 kW × solar 0-100 kW × chunk mass × vehicle mass.
4. Falsification or confirmation of the inbound dial-up-thrust hypothesis: does the inbound leg of the closure surface actually shift when hybrid power is modeled?

## Out of scope

- Power-conversion efficiency modeling (Brayton, Stirling).
- Solar array degradation over the 7-15 year mission timeline.
- Battery storage for off-sun-pointing operations.

## Priority

**High.** The user surfaced this as a real architectural insight, and the framework should be able to model it before the next round of pitch / matrix conversations. Implementation overlaps with deferred task #19 — picking this up means picking that up.
