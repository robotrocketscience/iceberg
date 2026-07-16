# mission_graph — phase-option mission tree

> **Current state (2026-05-26 latest+25):** The framework has matured well past the "v0 schemas only" commitment described below. The walker, sweep harness, closure-verdict policies, ~30 phase options across 7 phases, and a 156-test suite are all live. Two mission specifiers ship: `saturn_water_v0` (open-loop, vehicle_mass_kg as sweep axis — preserved immutable as the campaign baseline) and `saturn_water_v1` (closed-loop, vehicle dry mass DERIVED via per-subsystem demand-functions and fixed-point iteration; see `framework/dry_mass.py` and `missions/saturn_mass_demands.py`). `v1` is the state-of-record for any new cell-level closure claim; `v0` is retained for reproducing prior round artifacts.
>
> The closed-loop refactor landed via R-vehicle-mass-closure-refactor (titan-6, merge `08fbef9`, 2026-05-26). The "v0 — schemas only" framing below predates the campaign's growth and is preserved as historical context.

## What this is

A framework for expressing ICEBERG mission concepts as a tree of phase nodes,
where each phase has multiple implementation options and complete mission
architectures are paths through the tree.

The intent is to absorb the campaign's parameter-grid rounds (R_*) into a
single replayable model so that changes to one parameter propagate downstream
through every affected phase, rather than requiring each round to be re-run
by hand against the new value.

## Scope of v0

Schemas only. No executor, no sweep harness, no closure-policy runner. The
four schema files in `framework/` define the data model. Concrete mission
definitions and the walker come later.

## Data model

Three records, plus the state object they pass between them.

- **`VehicleState`** — what flows between phase executors. Mass, propellant,
  payload, location tag, v_inf at the local reference body, time elapsed,
  available power, health flags. Frozen so it hashes for sweep memoization.

- **`Option`** — one way to execute a phase. Carries a `precondition`
  predicate (does the incoming state satisfy what this option needs?) and an
  `executor` function (given incoming state + params, produce outgoing
  state). The precondition is what gates feasibility when the walker
  enumerates `(parent_option, child_option)` pairs.

- **`Phase`** — a node in the mission timeline. Either carries an option set
  (leaf phase) or sub-phases (nested phase). Granularity is per-phase: cruise
  can stay flat, proximity-ops can nest.

- **`Mission`** — an ordered sequence of phases plus the closure predicates
  applied to the final state. One Mission per top-level objective
  (Saturn-water run, low-Earth-orbit debris demonstrator, cislunar
  pathfinder).

## What is intentionally not here yet

- The walker / executor that traverses a Mission across a parameter grid.
- Memoization layer (hash keys, cache backend).
- Closure-verdict policies (strict / waiver / commercial floor as separate
  predicate sets that can be swapped without re-running the sweep).
- Failure-mode layer (nominal / abort_salvage / abort_loss / contingency
  branches attached orthogonally to the option tree).
- Campaign-level timeline above the mission tree (flight cadence, depot
  refueling cycles).
- Concrete mission definitions (cislunar_demo, chunk_rendezvous, etc.).

Each of those is a deliberate v1+ item. The v0 commitment is the data model
only, so the schema can be falsified by porting one historical round onto
it before more code lands.

## Repo placement

Per project CLAUDE.md the framework lives under `water-prop/sims/` even
though it does not call Basilisk. Treat it as a sim framework that happens
to run all closed-form analytic for now; if a phase later needs Basilisk
fidelity it can opt in via `water-prop/.venv-bsk`.

## Open questions

- Does the precondition predicate need to return a verdict tag richer than
  `(bool, reason)` — for example "feasible_with_margin" vs "feasible_tight"?
- How should multi-option *combinations* within a single phase be handled
  (e.g., simultaneously running a chemical kick AND a low-thrust trim
  during the same phase)? Currently each phase picks one option; combinatoric
  options would need a different shape.
- Closure predicates currently return a single verdict tag per predicate.
  For Bayesian / probability-weighted closure verdicts the return type would
  need to widen.
