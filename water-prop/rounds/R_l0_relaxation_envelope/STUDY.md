# R-l0-relaxation-envelope — STUDY (pre-registration)

**Worker:** worktree-172651 (integration session, project-owner-directed "run the open rounds"), 2026-07-24 latest+28.
**SCOPE:** `SCOPE.md` (Saturn orchestrator, 2026-05-26 latest+25). Gated on R-vehicle-mass-fidelity-refinement.
**Gate status:** substantively discharged at latest+28 — the fidelity round landed twice
(hyperion + rhea-5) with H5 held net: closure is FLAT across launch propellant fraction
0.15–0.98 under corrected kick physics, the walker enumeration is honest (rhea-5
assembly-preconditions audit: NO BUG), and the kick-stage manifest bug is fixed with
regression tests. The specific deferred deliverable (per-phase Tsiolkovsky propellant
derivation, titan D5) did NOT land, but its effect is bounded at ~0 on closure by both
executions; deviation D-2 below records this honestly.

## Disclosure of priors (read before the verdict table)

This registration is written AFTER adjacent rounds produced strong priors on H1:
rhea-5's R-closing-path-self-consistency corrected-kick sweep found **0 arrivals at the
LEO depot across the full 150-cell grid at every propellant fraction (0.15–0.80) and
every capture multiplier**, and the latest+25 Tier-1 sanity sweep found 0 of 1744 paths
arrive. The prediction column is therefore informed, not blind (same disclosure class as
rhea-5's "code-read preceded registration"). The value of running the round anyway: the
SCOPE pre-registered the *reading* of each outcome, and the project-owner question
("which spirit-preserving L0 relaxations restore commercial closure?") deserves its
definitive, on-the-record answer computed under the corrected framework rather than
inferred from adjacent sweeps — plus the failure-taxonomy diagnostic (WHERE the 1744
paths die) that neither adjacent round reported on the corrected physics.

## Hypotheses (from SCOPE, operationalized)

| # | Hypothesis | Falsification gate | Prediction |
|---|---|---|---|
| H1 | ≥ 1 cell reaches LEO depot with payload > 0 under base parameters | 0 arrivals across all 150 cells | **FALSIFIED expected** (prior above). If any arrival appears, treat as a framework regression signal first, finding second |
| H2 | L0-04 → 5 t brings closure > 5 % at some L0-05 ceiling | closure rate at floor 5 t × ceiling 25 yr < 5 % | Falsified (vacuous if H1 falsifies) |
| H3 | L0-05 → 25 yr alone (floor 25 t) brings closure > 5 % | no cell closes 25 t within 25 yr | Falsified (vacuous if H1 falsifies) |
| H4 | Non-nuclear regime (1–11 kWe) admits ≥ 1 closure at floor 10 t, ceiling 25 yr | zero closures across 1/10/11 kWe rows | Falsified (vacuous if H1 falsifies) |
| H5 | Combined relaxation (floor 5 t, ceiling 25 yr, L0-24 vacated) gives closure > 20 % | below 20 % | Falsified (vacuous if H1 falsifies) |
| H6 | Delivered-water cost competitive at relaxed L0s | — | **DEFERRED** per SCOPE (financial model not operative) |

## Method

One closed-loop sweep (`saturn_water_v1_closure_sweep.run_closed_loop`, 150 cells,
corrected kick physics now on main), post-processed:

- **Floors/ceilings as post-processing** on `leaf_state.payload_kg` /
  `leaf_state.time_elapsed_s` of feasible leaves — mathematically identical to the
  framework's `delivered_floor_*` predicates (which gate on the same two fields), at
  arbitrary floor/ceiling values. Sweep 1: floors {0.5, 1, 2, 5, 10, 15, 20, 25} t at
  ceiling 25 yr. Sweep 2: ceilings {15, 18, 20, 22, 25, 28, 30, 35} yr at floor 10 t.
  Sweep 3: combined (floor 5 t × ceiling 25 yr), closure rate per power class.
- **L0-24 vacated** = restrict to the non-nuclear power rows (1/10/11 kWe) of the
  existing power axis; also reported unrestricted.
- **Failure taxonomy:** infeasible-path counts grouped by (phase_id, reason class)
  across all cells — where do the paths die under corrected physics.

## Deviations from SCOPE (pre-registered)

- **D-1:** SCOPE deliverable 3 (`framework/relaxed_predicates.py`) is implemented as
  post-processing in `sweep_combined.py`, not framework surgery. Equivalent output;
  zero framework risk; parameterized framework predicates are warranted only if a
  positive closure surface ever exists to sweep against.
- **D-2:** the per-phase propellant-fraction derivation (titan D5) has not landed;
  both fidelity executions bound its closure effect at ~0 (closure flat across
  f 0.15–0.98). The sweep runs at the frozen f = 0.80 baseline; an f = 0.20 guard-rail
  re-run confirms f-independence of whatever verdict lands.
- **D-3:** L0-07 (cadence) and L0-12 (cost-competitiveness) relaxations from the
  SCOPE's H5 wording are NOT testable in the framework (no cadence or cost predicates
  exist); H5 is operationalized as the (L0-04, L0-05, L0-24) triple. Both untestable
  relaxations are inert w.r.t. arrival/closure mechanics; they belong to the deferred
  H6 financial layer.

## Reading (pre-committed, from SCOPE)

- H5 holds → relaxation envelope supports a commercial program at relaxed L0s;
  project-owner decides ratify-vs-hold.
- H5 falsifies, H1 holds → commercial program structurally non-viable even at maximum
  spirit-preserving relaxation; demonstrator-class promotion is the only path.
- **H1 falsifies → "ICEBERG is not deliverable as currently conceived"** — the
  closed-loop framework is either over-pessimistic or the chunk-as-propellant-tank
  concept hits a structural wall. The failure taxonomy is then the round's load-bearing
  output: it names the wall.
