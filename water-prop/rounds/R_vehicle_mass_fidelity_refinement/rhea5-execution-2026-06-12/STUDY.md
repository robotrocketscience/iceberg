# R-vehicle-mass-fidelity-refinement — STUDY (pre-registration)

**Worker:** rhea-5 (`iceberg-rhea-5`) executing the titan-7-scoped round at project-owner
direction 2026-06-12 (titan-7 dispatch of 2026-05-26 never started; registry row was
pre-staged but no branch exists). Identity mismatch vs SCOPE's "suggested worker" noted.
**Date pre-registered:** 2026-06-12, BEFORE any sweep in this round was run.
**Predecessors:** titan-6 R-vehicle-mass-closure-refactor (`08fbef9`); rhea-5
assembly-precondition audit (`7f9b910`, NO BUG — 0 of 904 walked designs complete the
phase graph at f = 0.80).

## Declared deviations from SCOPE (up front, per lesson 18: pre-register the conditioning structure)

- **D-A (H1 tested as best-f-per-cell, not per-phase derivation).** SCOPE slice 1 wants
  `propellant_fraction(phase)` derived per phase via Tsiolkovsky. This execution instead
  sweeps fixed launch propellant fraction f over a grid {0.10..0.92} and evaluates each
  cell at its BEST f (union over the grid). Rationale: launch propellant only serves the
  outbound legs (the return leg is chunk-water-fed), so a per-cell optimal fixed f is an
  UPPER BOUND on what any single-tank per-phase derivation can achieve; if no f on the
  grid opens a closure for a cell, no Tsiolkovsky-derived fraction would either.
  Within-path staging (different tanks per leg) remains out of scope — residual for
  titan-7 proper.
- **D-B (H4 tested as a bracket, not a dispatch).** Path-conditional thermal protection is
  tested by running the full f-grid at `plans_aerocapture=True` (every vehicle carries
  Earth-aerocapture thermal protection, the v1 default) vs `False` (direct-propulsive
  return, zero thermal-protection mass). The True/False pair BOUNDS the path-conditional
  dispatch the SCOPE describes; per-path charging lands with titan-7 proper.
- **D-C (H2 deferred).** The Wertz Space Mission Engineering anchor review requires the
  reference text; not executed in this session. H2 carries no verdict here.
- **D-D (H3 via hand-rolled Jansen estimator).** total-order sensitivity indices computed by a
  numpy Jansen estimator over pre-registered parameter ranges (below), n = 2^12 base
  samples, on the derived dry mass at the canonical cell (30 kWe, 200 t chunk). SALib is
  not in the environment; the estimator is ~40 lines and tested against an additive toy.

## Hypotheses under test (SCOPE numbering) and THIS WORKER'S quantitative predictions

**H1** (SCOPE: per-phase propellant derivation moves closure from 0 to non-zero at ≥ 1
architecture).
**Prediction: HELD via the electric-outbound channel.** Mechanism: at f = 0.80 the
derived 100–130 t dry vehicles wet out at 500–650 t, over every launch manifest; at
f ≈ 0.30 the same vehicles wet out at ~145–185 t, under the 300 t six-Falcon manifest,
and electric outbound at specific impulse 3000 s only needs f ≈ 0.25 × 1.10 margin.
Quantitative: **5–25 of 150 cells gain `arrived_at_depot` ≥ 1 path at best-f**,
concentrated at power ∈ {30, 55} kWe (the only classes passing both the ≥ 20 kWe Phase-1
and ≥ 30 kWe Phase-4 gates) and chunk ∈ {100, 200} t (the Phase-4 chunk-water wall —
median 5.2× shortfall at small chunks — should persist).
**Where this could be wrong:** phases 5–7 (inbound, Earth arrival, depot delivery) have
not been read by this worker and may carry their own gates that hold arrivals at 0 even
at optimal f. If the result is 0 arrivals at every f, that is H1 FALSIFIED and the
finding is that the frozen 0.80 was NOT what was hiding closure — a direct contradiction
of titan-6's D5 worry and of my own mechanism story above.

**H1-corollary (chemical channel).** Chemical trans-Saturn injection at specific impulse
340 s and 7.3 km/s needs f ≈ 0.89 before margin; **prediction: f = 0.92 grid point opens
zero additional arrivals** (chemical paths stay dead — wet mass at f = 0.92 is
~13× dry, far over every manifest).

**H3** (capture-mechanism mass is the largest single dry-mass uncertainty; falsified if
total-order sensitivity < 0.15).
**Prediction: HELD, narrowly — capture total-order index 0.15–0.35 at the canonical
cell,** but TPS comparable (0.15–0.40); powerplant variance-small because its anchors are
locked (narrow ranges), even though its mean contribution is largest. Pre-registered
ranges (uniform): capture coefficient 0.04–0.16 of chunk (first-pass ±2×), capture base
500–2000 kg, aperture term 25–100 kg/m²; TPS chunk-coefficient 0.05–0.20, TPS velocity
term 100–400 kg/(km/s); structure coefficient 0.025–0.10; comms floor 1000–4000 kg; bus
1000–3000 kg; reactor specific power 2.2–2.6 W/kg (locked, narrow); radiator base
4500–5500 kg and slope 90–110 kg/kWe (locked, narrow); tankage coefficient 0.03–0.08;
dry margin 0.15–0.25.

**H4** (path-conditional thermal protection changes closure count by ≥ 5 % of cells).
**Prediction: HELD at the bracket level** — `plans_aerocapture=False` removes
0.10 × chunk + 2.2 t of dry mass (22 t at the 200 t chunk), and **adds ≥ 8 of 150 cells
with ≥ 1 `arrived_at_depot` path at best-f vs the True case.** Direction: False > True.

**H5 (load-bearing)** (no combination produces > 5 % closure at L0-04 = 25 t).
**Prediction: HELD.** The v1 predicate grid brackets 25 t with `delivered_floor_20t` and
`delivered_floor` (30 t). Quantitative: **delivered_floor_20t closures ≤ 7 cells (≈ 5 %)
and delivered_floor (30 t) closures ≤ 3 cells at the most favorable (f, aerocapture)
combination.** Mechanism: even when paths arrive, delivered mass is bounded by the
capture/water bookkeeping that the ramscoop round showed tops out near ~21 t optimistic;
the assembly audit's 2–275× water-shortfall distribution says most arriving paths arrive
nearly empty. **If H5 falsifies, the titan-6 matrix-amendment cascade must pause** — that
is the SCOPE's stated reading and the reason this round gates everything.

**H6** (≥ 1 other wet-vs-dry confusion exists in prior rounds' anchors).
**Prediction: HELD; expect 2–5 ambiguous anchors** in a grep-driven catalog of
STUDY/SCOPE/FINDINGS/READING files (executed as catalog only, no re-derivation).

## Method

1. `run.py` sweeps f ∈ {0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.88, 0.92}
   × plans_aerocapture ∈ {True, False} over the standard 150-cell closed-loop grid
   (`run_closed_loop(extra_params=...)`), recording per cell: convergence, derived dry,
   wet, and per-predicate best verdicts. f = 0.80/True reproduces the titan-6 baseline
   (regression check — must show 0 arrivals or this harness is wrong).
2. Jansen total-order total-order sensitivity on derived dry mass at canonical cell over the H3 ranges.
3. Wet-vs-dry grep catalog across `water-prop/rounds/*/{STUDY,SCOPE,FINDINGS,READING}*.md`.
4. FINDINGS.md: verdicts H1/H3/H4/H5/H6 with prediction-vs-outcome analysis, especially
   wherever the outcome contradicts the predictions above.

Expected runtime: 20 sweeps × ~10 s ≈ 3–4 min (slow step: 150 fixed-point derivations +
walks per sweep). No randomness except the quasi-random sampler (seeded, numpy default_rng(42)).
