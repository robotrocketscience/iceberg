# R-vehicle-mass-closure-refactor — vehicle dry mass is a derived quantity, not a sweep axis

**Status:** scope, pre-study. Authored by Saturn (orchestrator) 2026-05-26.
**Predecessor:** project-owner methodology observation 2026-05-26 (mid-execution of R-smaller-vehicle-demonstrator-envelope). The current `mission_graph` framework treats `vehicle_mass_kg` as a boundary condition rather than a derived quantity, which makes any per-cell vehicle-mass answer non-self-consistent.

## Premise — the methodology bug

Every prior round in the campaign that sweeps `vehicle_mass_kg` is open-loop: the sweep picks a vehicle dry mass, walks the mission graph forward, returns delivered mass. The framework does not check whether the assumed vehicle dry mass is self-consistent with the dry-mass demands the chosen phases impose. So:

- R-chunk-size-pareto cells that close at vehicle 50 t / chunk 40-80 t do not check whether 50 t is enough to carry the capture mechanism for an 80 t chunk.
- R-megawatt-architecture-viability cells that close at vehicle 100 t / reactor 1 megawatt-electric do not check whether the 1 megawatt-electric reactor's MARVL-anchored radiator and shield mass fit inside the 100 t dry budget.
- R-smaller-vehicle-demonstrator-envelope (2026-05-26) cells that close at vehicle 10-20 t are almost certainly internally inconsistent and the framework reports them as closures anyway.

Standard space-systems-engineering methodology (JPL Team-X, NASA COMPASS, Aerospace Corporation Concept Design Center) treats vehicle dry mass as a derived quantity computed iteratively from per-subsystem mass demands. The campaign's framework needs to adopt this pattern.

## Pre-registered hypotheses

H1: **A closed-loop vehicle-mass-derivation framework converges (returns a self-consistent dry mass) for at least 50 percent of the cells the open-loop framework currently counts as closures.** Falsified if more than 50 percent of currently-counted closures fail to converge — would mean the campaign's current closure inventory is severely contaminated.

H2: **The relative ordering of architectures (which cells close vs which do not) is preserved across the refactor, even though absolute closure-mass numbers shift.** Falsified if at least one architecture that was previously a closer becomes a non-closer AND a different architecture moves from non-closer to closer (i.e., the leaderboard inverts at any pair). Reading-if-held: the campaign's structural verdicts (ram-scoop vs harpoon, chunk-size monotonicity, specific-impulse cliff) survive.

H3: **The 50-tonne vehicle-dry-mass floor in the prior audit's BEST_ARCHITECTURES_25T sweep is approximately right — within 30 percent of the closed-loop derivation at the audit's chosen (200 t chunk, 30 kilowatt-electric reactor, single-pass trawl, hybrid aerocapture) cell.** Falsified if the closed-loop derivation gives a dry mass outside [35, 65] t at that cell.

H4 (load-bearing): **The "thousands of closing cells" headline collapses substantially under closed-loop derivation.** Specifically: cells closing under closed-loop are less than 30 percent of cells closing under open-loop, because most of the open-loop closures hide subsystem-mass inconsistencies. Falsified if closed-loop closure count is greater than 70 percent of open-loop closure count.

H5: **The demonstrator-class minimum vehicle dry mass is in [12, 25] t.** Below 12 t the communications + guidance + computer floor + minimum reactor + minimum thermal protection cannot fit; above 25 t the configuration becomes commercial-class rather than demonstrator-class. Falsified if the closed-loop derivation produces a self-consistent demonstrator with dry mass outside that bracket.

## Methodology

### Architecture of the refactored framework

```
Inputs (sweep axes):
  chunk_mass_kg
  capture_architecture       (harpoon | ram_scoop | everting_sleeve)
  reactor_class              (single_kilowatt | 30_kilowatt | 100_kilowatt | 1_megawatt)
  water_met_isp_s
  trajectory_choices         (outbound, inbound, capture-orbit, etc.)
  launch_class               (falcon_heavy_expended | starship | multi_falcon_assembly)

Per-phase mass-demand functions (new framework primitive):
  phase.dry_mass_demand(context) -> {
      "subsystem_name": mass_kg,
      ...
  }

  Implementations per phase:
    capture_phase:   bag/grapple/structural mass = f(chunk_mass, capture_arch)
    propulsion_phase: reactor mass = f(power_kwe), radiator mass = f(power_kwe, specific_power),
                      thruster mass = f(thrust_n, isp), tankage mass = f(propellant_mass)
    aerocapture_phase: TPS mass = f(entry_velocity, ballistic_coefficient, chunk_mass)
    rendezvous_phase: sensor mass = f(navigation_precision_required)
    structural_phase: backbone mass = f(max_load_event in mission)
    communications_phase: comm mass = floor(2 t) + scaling(distance, data_rate)

Closure loop:
  vehicle_mass_kg := initial_guess (e.g., 50_000.0)
  for iter in range(MAX_ITER):
      total_demand = sum(phase.dry_mass_demand(context) for phase in mission)
      total_demand += dry_margin (e.g., 0.20)
      new_vehicle_mass = total_demand
      if abs(new_vehicle_mass - vehicle_mass_kg) / vehicle_mass_kg < CONVERGENCE_TOL:
          break
      vehicle_mass_kg = new_vehicle_mass
  else:
      cell.converged = False
      return non-convergence

  cell.vehicle_mass_kg = vehicle_mass_kg
  cell.converged = True
  walk forward as before, compute delivered_mass
```

### Per-phase mass-demand functions — first-pass forms

Initial implementations should be **simple and bounded**, anchored to flown-system mass fractions where possible. Refinement in later rounds.

| Subsystem | Mass-demand function | Anchor |
|---|---|---|
| Reactor + shield | `f(power_kwe) = 5_000 + 0.2 * power_kwe` kg | Kilopower 1 kWe = 1500 kg; FSP 40 kWe = 13000 kg; MARVL extrapolation |
| Radiators | `f(power_kwe, specific_power) = power_kwe * 1000 / specific_power` kg | Flown 5 W/kg → 200 kg/kWe; MARVL aspirational 40 W/kg → 25 kg/kWe |
| Power conversion | `f(power_kwe) = 0.1 * power_kwe + 500` kg | Brayton converters at ~10 kg/kWe + minimum tooling |
| Thrusters + tankage | `f(thrust_n, prop_mass) = 50 * thrust_n + 0.05 * prop_mass` kg | water-MET head ~50 kg/N; tankage 5% of propellant |
| Capture mechanism (harpoon) | `f(chunk_mass) = 500 + 0.05 * chunk_mass` kg | minimum harpoon + tether scales mildly with chunk |
| Capture mechanism (ram-scoop bag) | `f(chunk_mass, aperture_area) = 1000 + 0.08 * chunk_mass + 50 * aperture_area_m2` kg | bag + frame scales with chunk and aperture |
| Capture mechanism (everting sleeve) | `f(chunk_mass) = 2000 + 0.10 * chunk_mass + 5 * sleeve_length_m^2` kg | extra mass for eversion mechanism at scale |
| Earth-aerocapture TPS | `f(entry_v_km_s, beta_kg_m2) = 0.10 * chunk_mass + 200 * entry_v_km_s` kg | scales with chunk and entry velocity |
| Primary structure | `f(max_thrust_load_kN, chunk_mass) = 0.05 * chunk_mass + 100 * max_load_kN` kg | backbone scales with chunk and max load |
| Communications + guidance + comp | `2000 kg` (floor) | invariant minimum for deep-space mission |
| Dry margin | `0.20 * subtotal` | NASA Class B mission design margin |

The numbers are first-pass anchors. They should be reviewed against a published spacecraft mass-fraction reference (e.g., Wertz "Space Mission Engineering" chapter on subsystem mass models) before the refactored framework is treated as authoritative.

### Convergence behavior

Expected behavior at canonical audit cell (200 t chunk, ram-scoop, 30 kWe, water-MET 800 s, hybrid aerocapture):

- Initial guess 50 t → first iteration sum: 5 t reactor + 6 t radiator (at 5 W/kg) + 3.5 t power conversion + ~3 t thrusters + ~17 t bag + ~25 t TPS + ~12 t structure + 2 t comms + margin = ~73 t × 1.2 = ~88 t.
- Second iteration with 88 t base: TPS scales up, structure scales up → ~95 t.
- Third iteration: ~98 t. Converges.
- Final self-consistent dry mass: ~95-100 t at canonical audit cell.

That is roughly 2× the audit's assumed 50 t, which would explain why the audit's "39.5 tonnes delivered" might over-state by a similar factor. Refactor confirms or refutes.

### Migration plan

The refactored framework must coexist with the existing one during the transition:

1. New module `mission_graph/framework/dry_mass.py` carrying per-phase mass-demand registrations and the fixed-point iterator.
2. New mission specifier `saturn_water_v1` that uses the new framework. Keep `saturn_water_v0` immutable as the open-loop baseline.
3. New `VehicleState.derived_mass_kg` field alongside the existing `mass_kg`; sweep grid no longer includes `vehicle_mass_kg` as a sweep axis.
4. Audit script that runs every prior round's sweep through the new framework, flags non-convergent cells, and emits a "% of original closures that survive" table.
5. Methodology lesson candidate ratification (see below).

### Audit phase — back-test against prior rounds

After the framework refactor lands:

1. Re-run R-chunk-size-pareto with the new framework. Verify (H2) that titan-3's 40-80 tonne chunk closure cells either converge to a new self-consistent dry mass or are flagged non-convergent.
2. Re-run R-assumption-audit-2026-05-21's BEST_ARCHITECTURES_25T sweep. Verify (H3) the 50 t floor lands inside [35, 65] t in the closed-loop derivation.
3. Re-run R-smaller-vehicle-demonstrator-envelope. Verify (H5) the demonstrator-class minimum dry mass is in [12, 25] t.
4. Compile an audit report: which prior rounds' headline numbers survive, which need re-stated, which need re-run.

## Deliverables

1. This SCOPE.md.
2. STUDY.md with H1-H5 pre-registered.
3. `mission_graph/framework/dry_mass.py` — per-phase mass-demand primitive + fixed-point iterator.
4. `mission_graph/missions/saturn_water_v1.py` — new mission specifier using the closed-loop framework.
5. Per-phase mass-demand implementations across all existing phases (a non-trivial wiring exercise — every phase gets a new method).
6. Sweep harness updated to drop `vehicle_mass_kg` from `VEHICLE_AXES` and add a derived-mass column to outputs.
7. Audit report `BACK_TEST.md` running prior rounds' sweeps through the new framework with per-round verdict on survivors-vs-retirees.
8. FINDINGS.md — verdict on H1-H5 + methodology lesson candidate text for PROTOCOL.md ratification.

## Out of scope

- Improving the mass-demand functions' fidelity beyond the first-pass anchors. That is a follow-on (R-vehicle-mass-fidelity-refinement).
- Re-running every prior round in full. The audit phase flags survivors and retirees; full re-runs are a follow-on per affected round.
- Changing the chunk-as-propellant-tank physics. The refactor is about *bookkeeping*, not about the architecture itself.

## Predecessor work

- R-smaller-vehicle-demonstrator-envelope (commit `<this pass>`) — surfaced the methodology gap mid-execution. Its FINDINGS document is the public record of "what the broken framework says" as a baseline.
- R-assumption-audit-2026-05-21 A12 — already-noted question "could we go with a much smaller spacecraft?". The audit script existed but had not been run; running it exposed the gap.
- Project-owner observation 2026-05-26 — diagnosis that vehicle mass should be derived per-phase, not assumed.

## Priority

**CRITICAL.** This is a foundational methodology fix. Every architecture-comparison round downstream — including R-chunk-capture-monte-carlo's contact-fidelity follow-on, R-ramscoop-foundational-premise-revisit, R-mission-1-demonstrator-then-scale-up, the demonstrator-class promotion's commercial-class readiness check — needs a framework that returns self-consistent vehicle dry mass. Without this, the campaign's absolute numbers are not defensible.

The refactor is **multi-day work**. It should be a dedicated worker session, not in-session.

## Suggested worker

Any moon worker comfortable with framework-level Python refactoring + space-systems mass-fraction modeling. Best fit: titan (multiple prior delta-velocity rounds + framework familiarity) or hyperion (mass-anchor audit experience).
