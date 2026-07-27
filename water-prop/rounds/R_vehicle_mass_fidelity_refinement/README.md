# R-vehicle-mass-fidelity-refinement — two independent executions

This round was executed **twice, independently, by two workers who could not see each
other's branches** (discovered at the 2026-07-24 integration pass). Both executions are
preserved verbatim, one subdirectory each; neither supersedes the other's artifacts.
`SCOPE.md` (top level) is the shared pre-registration lineage (titan-6 D5 successor,
SCOPE'd latest+24).

## Executions

- **`hyperion-execution-2026-05-26/`** — hyperion (re-spawn 2), branch `iceberg-hyperion`.
  Partial scope (load-bearing H1/H5 + Wertz review + wet-vs-dry audit; per-phase
  Tsiolkovsky and path-conditional TPS deferred). **H5 HELD:** closure flat 0/150 across
  propellant fraction 0.70–0.98; binding failure restated as **launch mass** (the
  self-consistent wet vehicle exceeds 6× Falcon Heavy).
- **`rhea5-execution-2026-06-12/`** — rhea-5, branch `iceberg-rhea-5`, executing the
  titan-7 scope at project-owner direction. Swept the full propellant-fraction axis
  (0.12–0.92) and initially reported **"H5 FALSIFIED as stated"** via an
  f ≈ 0.18–0.22 chemical-kick closure window (10/150 cells at the 30 t floor).

## Adjudication (final state of record)

The rhea-5 closure window was **reversed the same day by rhea-5's own adversarial
follow-on, `R_closing_path_self_consistency/`**: the window was manufactured by v0-era
kick-stage manifest semantics surviving into the closed-loop framework (a 9.2 t "ghost
vehicle" — against 93.2 t of derived hardware — flew the closing path). With
self-consistent kick physics, closure is **0 of 150 cells at every propellant fraction
(0.15–0.80) and every capture multiplier**. The fidelity round's H5-falsification
headline is RETRACTED (see the correction notices in `water-prop/RUNNING_DOC.md`).

**Net verdict, corroborated by both executions: H5 HELD — no fidelity refinement rescues
closure; titan-6's 0/150 collapse verdict stands, strengthened (now propellant-fraction-
independent, and precisely characterized as launch-mass-bound).** The capture-physics
findings of rhea-5's companion round `R_chunk_capture_tier15_reduced_order/` stand;
only its closure-coupling numbers are void.

Framework fix + regression tests shipped on `iceberg-rhea-5`
(`mission_graph/missions/phase1_leo_to_saturn.py`, `tests/test_kick_stage_manifest.py`).
