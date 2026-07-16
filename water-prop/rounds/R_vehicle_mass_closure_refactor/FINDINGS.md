# FINDINGS — R-vehicle-mass-closure-refactor

**Worker:** titan (re-spawn, branch `iceberg-titan-6`). **Date:** 2026-05-26.
**Status:** complete; awaiting orchestrator integration.
**Deliverables:** `framework/dry_mass.py`, `missions/saturn_mass_demands.py`,
`missions/saturn_water_v1.py`, `missions/sweeps/saturn_water_v1_closure_sweep.py`,
`tests/test_dry_mass.py` (13 tests; 156 total pass), STUDY.md, BACK_TEST.md, this file.

---

## Verdict in one line

Vehicle dry mass is now a **derived** quantity (per-subsystem demand → fixed-point iteration), not a
sweep boundary condition. Under self-consistent mass the campaign's open-loop closure inventory
**collapses to zero** on the canonical grid (0 of 150 closed-loop vs 16 open-loop), because every
open-loop closer was a vehicle lighter than its own powerplant. **H1 held, H4 (load-bearing) held,
H2 held (vacuously/consistently), H3 falsified, H5 falsified.** No structural verdict is overturned;
absolute delivered-mass numbers tied to specific vehicle masses must be re-derived.

---

## Hypothesis verdicts

**H1 — Convergence (≥50% of open-loop closers converge): HELD, trivially.**
Every cell on the closed-loop grid converges (typically 6 Picard iterations). With the 0.80 propellant
convention the only dry→propellant→dry coupling is tankage = 0.05·(f/(1−f))·dry = 0.2·dry, giving a
contraction factor (1+margin)·0.2 = 0.24 < 1. Non-convergence is reachable and tested (it appears
above ~0.95 propellant fraction, where tankage growth outruns the dry mass it is added to), but does
not occur on the flyable grid. The closure inventory is numerically well-posed; the collapse is from
self-consistent mass being **large**, not from pathology.

**H2 — Ordering preserved (no leaderboard inversion): HELD (consistently; partly vacuous).**
Closed-loop produces zero closers, so no architecture moves non-closer→closer; therefore no inversion
is possible and H2 is not falsified. Architectures that were open-loop closers (audit canonical cell,
titan-3 chunk-size-pareto cells, smaller-vehicle cells) all become non-closers — uniformly, in the
same direction the campaign's structural verdicts already point (200-t cell collapse, demonstrator
re-gating). The refactor restates absolute numbers without inverting the leaderboard.

**H3 — Audit canonical-cell derived dry mass ∈ [35, 65] t: FALSIFIED.**
Derived dry mass at (200 t chunk, 30 kWe, single-pass, hybrid aerocapture) = **120.8 t**, far above the
bracket. Breakdown (t): tankage 24.2, aerocapture-TPS 22.2, powerplant 20.8, capture 19.5, structure
10.0, bus 2.0, comms 2.0; ×1.20 margin → 120.8. The audit's swept 50 t **wet** = 10 t dry was ~12×
too light. The SCOPE's ~95–100 t convergence estimate was directionally correct but understated because
it used the SCOPE first-pass reactor anchor (~5 t) rather than the locked KRUSTY anchor (12.5 t, decision
D1). **The terminology resolution (STUDY §2) is the durable output here:** the audit's "50 t vehicle"
is a wet number; read as dry it is 10 t; the self-consistent dry is 121 t.

**H4 (load-bearing) — Closed-loop closers < 30% of open-loop: HELD, emphatically.**
0 of 150 closed-loop cells close `delivered_floor` (and 0 reach `LEO_depot` at all) vs 16 open-loop
closers → **0%**, far below the 30% threshold. The "thousands of closing cells" headline the SCOPE
referenced collapses because the open-loop closers were the precise cells the open-loop framework could
not police: 10–20 t dry vehicles at 30–55 kWe (powerplant ≥ 20.8 t) and 200 t chunk. **Caveat
(honest):** the *completeness* of the collapse (literally zero arrive) is partly a consequence of the
frozen 0.80 propellant convention (D5) — see "Two mechanisms" in BACK_TEST. The collapse *direction*
and the < 30% verdict are robust to that convention; "0% arrive as a convention-independent fact"
requires the fidelity follow-on.

**H5 — Demonstrator minimum self-consistent dry mass ∈ [12, 25] t: FALSIFIED (high).**
Smallest closed-loop demonstrator (10 t chunk, 1 kWe) derives **27.7 t dry**, just above the bracket;
TPS-sensitive (drops ~3 t toward the bracket if aerocapture intent is removed). It is 7–14× larger than
the 2–4 t dry implied by the smaller-vehicle round's "10–20 t vehicle" closers. A real demonstrator
floor is set by the invariant comms+bus (4 t) + minimum powerplant + capture + (optional) TPS, and
lands just above 25 t under conservative TPS — a tighter, defensible number than the bracket, and one
that says the "sub-20-tonne demonstrator" framing is not self-consistent.

---

## What this changes / does not change

- **State-of-record:** `saturn_water_v1` (closed-loop) is now the framework for any cell-level closure
  claim. `saturn_water_v0` is retained, immutable, as the open-loop baseline (reproduces all 143 prior
  tests + the pre-refactor sweep).
- **Survives:** every structural verdict — ram-scoop vs harpoon ordering, chunk-size monotonicity, the
  specific-impulse cliff, the 200-t-cell collapse, the three-bets framing, the demonstrator re-gating.
- **Must be re-derived:** absolute delivered-mass numbers tied to a specific (too-light) vehicle mass
  (audit "39.5 t delivered", titan-3 "30–60 t delivered", smaller-vehicle closures). BACK_TEST §
  "Survivors / retirees" catalogs them. Full per-round re-runs are per-round follow-ons (SCOPE
  out-of-scope).

## Coordination items for the orchestrator (handoff-back triggers)

1. **D1 anchor deviation — surfaced, not blocking.** Powerplant reuses the locked KRUSTY 2.4 W/kg +
   MARVL anchors over the SCOPE first-pass reactor form (~2.5× lighter at 30 kWe). This is the
   consistency-preserving choice and does not exceed the SCOPE's >2× handoff-back trigger as a *class
   of error*; the specific SCOPE reactor line is superseded by the locked belief. No re-SCOPE needed
   unless the project owner wants the lighter anchor carried as a sensitivity.
2. **D5 propellant convention — flagged.** The "0 arrive" completeness is convention-sensitive.
   Recommend a follow-on **R-vehicle-mass-fidelity-refinement** that (a) derives propellant from the Δv
   schedule rather than a fixed fraction, (b) reviews the first-pass subsystem anchors against Wertz
   SMAD, (c) makes TPS path-conditional (D3). This is the natural successor and is where the H4
   completeness claim gets hardened.
3. **Capture-archetype mismatch (D2).** The SCOPE's harpoon/ram-scoop/everting archetypes belong to
   `R_chunk_capture_monte_carlo`, not `saturn_water_v0` Phase 3. v1 uses the ram-scoop-bag form as the
   trawl default and exposes `capture_arch` for the monte-carlo round to reuse the same demand machinery.

## Methodology-lesson candidate (for PROTOCOL.md ratification)

**Candidate lesson — "A derived quantity must not be a free sweep axis."**
When a quantity is *determined* by other modeled quantities (vehicle dry mass is determined by the
subsystems the architecture selects), sweeping it as an independent boundary condition manufactures
cells that violate the model's own internal accounting and reports them as results. The fix is to make
it derived (fixed-point over the demands) and to treat non-convergence as a finding, not an error to
clip. Corollary, surfaced sharply by H3: **before comparing a derived number to a prior anchor, confirm
the two are the same quantity** — the campaign's "50 t vehicle" was a *wet* axis value repeatedly read
as a *dry* mass, a 5× error hiding in a label. (Compounds with mimas lesson-17 "round-local
redefinition invites convention drift" and the latest+20 lesson "re-derive from inputs".)
