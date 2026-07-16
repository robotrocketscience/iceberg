# R-vehicle-mass-closure-refactor — STUDY

**Status:** pre-study FROZEN. Hypotheses H1–H5 registered before any framework code lands.
**Worker:** titan (re-spawn, branch `iceberg-titan-6`), 2026-05-26.
**Base:** `main` HEAD `3e0ad81` (constraint-encoded framework, state-of-record). SCOPE + two
back-test-input rounds imported from `worktree-092320` per project-owner base decision 2026-05-26.
**SCOPE:** `SCOPE.md` (this directory), authored by Saturn (orchestrator).

---

## 1. Problem statement (restated from SCOPE)

`mission_graph` treats vehicle mass as a sweep **boundary condition**: the canonical sweep's
`vehicle_mass_kg` VehicleAxis sets `VehicleState.mass_kg` at launch and walks forward. The framework
never checks that the assumed vehicle mass is consistent with the dry-mass *demands* the chosen phases
impose. Open-loop cells can therefore report closure for a vehicle physically too small to contain its
own subsystems. R-smaller-vehicle-demonstrator-envelope surfaced this by sweeping down to 10 t vehicles
and reporting closures.

The fix: vehicle **dry mass** becomes a *derived* quantity computed by per-subsystem mass-demand
functions iterated to a self-consistent fixed point. Cells that fail to converge are flagged as
mutually inconsistent — and **non-convergence is a valid result, not a bug to be clipped** (per SCOPE
open-coordination note).

---

## 2. Terminology resolution (load-bearing; decided before coding)

The framework's mass bookkeeping (verified by reading `state.py`, `phase1`, `phase3`, `phase6`):

```
mass_kg      = total current vehicle mass (dry structure + propellant + captured payload)
propellant_kg= propellant remaining
payload_kg   = captured water (0 at launch, grows at Phase 3, consumed by water-MET / delivered)
DRY MASS     := mass_kg - propellant_kg - payload_kg    (structure + subsystems)
```

DRY MASS is ~invariant across burns (a burn drops `mass_kg` and `propellant_kg` equally) and across
capture (capture raises `mass_kg` and `payload_kg` equally). It changes only at staging/jettison events
(kick-stage drop, hardware jettison). This is exactly the quantity `mass_floor_ok()` already computes.

**The closed-loop derivation targets DRY MASS.** This matters because the canonical sweep's
`vehicle_mass_kg` axis is **wet** mass with `propellant_kg = 0.80 · mass_kg` (`_scale_propellant`), so a
swept "50 t vehicle" carries only **10 t of dry structure+subsystems**. The SCOPE's narrative ("50 t
dry", convergence example "~95–100 t dry") reasons in DRY-mass terms. **The audit's swept 50 t wet
floor and the SCOPE's intended 50 t dry floor are different numbers by 5×.** H3 below is evaluated in
DRY-mass terms and reports the comparison against both readings explicitly, because resolving this
confusion is itself a deliverable.

---

## 3. Design decisions (frozen before coding)

- **D1 — Reuse existing powerplant anchors, not the SCOPE first-pass.** `powerplant_constraints.py`
  already encodes reactor = `power_kWe·1000/specific_power` (KRUSTY 2.4 W/kg default, locked beliefs
  `0d5c8822` / power finding 1), MARVL bundled radiator = `5 t + 0.1 t/kWe` (locked `0418e2c9`),
  thrusters = `10 kg/kWe`, bus = 2000 kg conservative. The SCOPE's first-pass reactor anchor
  (`5000 + 0.2·kWe` ≈ 5 t at 30 kWe) contradicts the locked KRUSTY figure (12.5 t reactor at 30 kWe,
  2.4 W/kg) by ~2.5×. The closed-loop module **reuses `required_powerplant_mass_kg()` verbatim** for
  the powerplant subsystems and adds the SCOPE's other subsystems (capture, TPS, structure, comms,
  tankage) on top. Deviation logged for FINDINGS / orchestrator surfacing per SCOPE §"Open coordination
  questions" (>2× anchor disagreement).
- **D2 — Capture-mechanism demand keyed to the trawl options actually in `saturn_water_v0`.**
  The SCOPE's capture archetypes (harpoon / ram-scoop / everting-sleeve) belong to
  `R_chunk_capture_monte_carlo`, not Phase 3 of `saturn_water_v0` (single-pass / drift / F-G / B-ring
  trawls). The first-pass capture demand uses the SCOPE's ram-scoop-bag form
  (`1000 + 0.08·chunk + 50·aperture`) as the default trawl bag/frame, with a `capture_arch` context
  hook for the monte-carlo archetypes. Mismatch noted for FINDINGS.
- **D3 — Derivation granularity is the sweep coordinate, not the per-path option.** Subsystem demands
  depend on `chunk_mass`, `power_kWe`, `thrust_n`, `propellant` (sweep-coordinate-fixed), so dry mass is
  derived once per coordinate, the derived value sets the launch `VehicleState.mass_kg`, and the
  existing walker then enumerates all paths. The one path-dependent subsystem is aerocapture TPS (only
  some Phase-6 options use it). v1 charges TPS conservatively via a `plans_aerocapture` context flag
  (default on) and flags path-conditional TPS as a fidelity follow-on. This keeps the iterator
  well-posed and convergent.
- **D4 — `saturn_water_v1` reuses `saturn_water_v0`'s phase sequence.** The mission tree does not
  change; only the launch-state mass derivation changes (swept axis → derived fixed point). `v0` stays
  immutable as the open-loop baseline. This isolates the refactor to bookkeeping (SCOPE out-of-scope:
  "not changing the chunk-as-propellant-tank physics").
- **D5 — Propellant load convention preserved.** Launch wet mass = derived dry `D` + propellant, with
  propellant following the existing `PROPELLANT_FRACTION = 0.80` convention (`wet = D / (1 − f)`,
  `propellant = f·wet`). Re-deriving propellant from the Δv schedule is explicitly out of scope
  (follow-on). Tankage demand = `0.05·propellant` is the only D→propellant→D coupling and is what makes
  the fixed point non-trivial.

---

## 4. Pre-registered hypotheses (FROZEN)

Carried verbatim in intent from SCOPE §"Pre-registered hypotheses"; falsifiers made operational.

**H1 — Convergence.** A closed-loop derivation converges (returns a self-consistent dry mass within
`CONVERGENCE_TOL = 1e-3` relative, `MAX_ITER = 50`) for **≥ 50%** of the cells the open-loop framework
counts as `delivered_floor` closures.
- *Falsified if* > 50% of currently-counted closures fail to converge.
- *Reading if held:* the closure inventory is iterable, not numerically pathological.
- *Prior expectation:* with the D5 coupling (tankage ∝ propellant ∝ dry), the only D-on-RHS term is
  tankage ≈ `0.05·4D = 0.2D`, so the map is a contraction and convergence is near-universal. H1 is
  expected to hold easily; the informative hypothesis is H4.

**H2 — Ordering preserved.** The relative ordering of architectures (which cells close vs which do not)
is preserved across the refactor, even though absolute closure-mass numbers shift.
- *Falsified if* at least one architecture flips closer→non-closer **and** a different one flips
  non-closer→closer (a leaderboard inversion at any pair).
- *Reading if held:* the campaign's structural verdicts (ram-scoop vs harpoon, chunk-size monotonicity,
  specific-impulse cliff, the 200-t-cell collapse) survive; only absolute mass numbers restate.

**H3 — Audit floor ≈ right (DRY-mass terms).** At the audit's canonical cell (200 t chunk, single-pass
trawl, 30 kWe, water-MET 800 s, hybrid aerocapture), the closed-loop derived **dry** mass lands in
**[35, 65] t**.
- *Falsified if* derived dry mass is outside [35, 65] t at that cell.
- *Explicit dual report:* compare against (a) the audit's swept 50 t **wet** = 10 t dry, and (b) the
  SCOPE's intended 50 t **dry**. The terminology resolution (§2) is reported regardless of verdict.

**H4 (load-bearing) — Closure headline collapses.** Cells closing under closed-loop derivation are
**< 30%** of cells closing under open-loop, because most open-loop closures hide subsystem-mass
inconsistencies (vehicles too light to contain their powerplant + capture gear).
- *Falsified if* closed-loop closure count is **> 70%** of open-loop closure count.
- (30–70% is the indeterminate band: neither held nor falsified; report the number.)

**H5 — Demonstrator dry-mass bracket.** The demonstrator-class minimum self-consistent **dry** mass is
in **[12, 25] t**.
- *Falsified if* the closed-loop derivation produces a self-consistent demonstrator (smallest chunk,
  smallest flyable power class) with dry mass outside [12, 25] t.
- *Note:* evaluated at the smallest-chunk / lowest-power coordinate; reported alongside what
  R-smaller-vehicle-demonstrator-envelope's open-loop sweep claimed (10–20 t **wet**).

---

## 5. Deliverables (tracked)

1. This STUDY.md (frozen before code). ✓ on commit.
2. `framework/dry_mass.py` — `MassContext`, per-subsystem demand functions, `derive_vehicle_dry_mass()`
   fixed-point iterator returning `(dry_mass_kg, converged, iterations, breakdown)`.
3. `missions/saturn_water_v1.py` — closed-loop mission specifier reusing v0's phase sequence; v0 immutable.
4. Per-phase / per-subsystem mass-demand implementations (capture, propulsion, aerocapture-TPS,
   structure, comms, tankage), reusing `powerplant_constraints` for powerplant.
5. Sweep harness `missions/sweeps/saturn_water_v1_closure_sweep.py` — drops `vehicle_mass_kg` from
   `VEHICLE_AXES`; adds `derived_dry_mass_kg` + `converged` columns.
6. `BACK_TEST.md` — back-test BEST_ARCHITECTURES_25T (audit), chunk-size-pareto (titan-3),
   smaller-vehicle-demonstrator-envelope; flag non-convergent cells; "% of original closures that
   survive" table.
7. `FINDINGS.md` — verdict on H1–H5 + methodology-lesson candidate text + anchor-deviation surfacing.
8. New tests under `tests/` for `dry_mass.py` (convergence, contraction, breakdown invariants,
   non-convergence path).

---

## 6. Out of scope (from SCOPE; reaffirmed)

- Improving mass-demand fidelity beyond first-pass anchors (→ R-vehicle-mass-fidelity-refinement).
- Re-running every prior round in full (BACK_TEST flags survivors/retirees; full re-runs are per-round
  follow-ons).
- Re-deriving propellant load from the Δv schedule (D5 keeps the 0.80 fraction convention).
- Changing chunk-as-propellant-tank physics.
- Path-conditional TPS (v1 charges conservatively via flag; fidelity follow-on).
