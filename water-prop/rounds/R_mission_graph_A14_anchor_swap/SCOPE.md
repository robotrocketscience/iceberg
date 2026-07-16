# R-mission-graph-A14-anchor-swap — does the mission_graph closure surface survive the velocity-conditional capture-efficiency reframe?

**Status:** scope, pre-study. Authored by Saturn (orchestrator), 2026-05-22 latest+17. Punch-list round from the latest+17 integration pass following R-A14-engineering-decomposition (`fd6fab0`).

---

## Why this round

R-A14-engineering-decomposition supersedes the mission_graph framework's single 0.85 single-pass-trawl capture-efficiency anchor with the velocity-conditional set: **0.53 mm/s undemonstrated, 0.41 realistic low-m/s, 0.69 demonstrator-confirmed.** The framework still carries 0.85 (and 0.65 / 0.85 / ~0.01 across the four Phase 3 capture options) per the canonical sweep `20260521T193329Z` configuration. The Saturn-worker audit ran the multiplier sweep parametrically (0.25 / 0.50 / 0.75 / 1.00) to surface the cliff, but the framework default remained at the desk anchor.

**The matrix decision-state section now carries the velocity-conditional set as operative reading.** The framework default still carries the desk anchor. Downstream artifacts that quote the closure surface (best-architecture report at L0-04 = 25 t, mining_view.py outputs, the 5,656 feasible paths / 322 unique architectures count) are anchored on the unswapped state. The framework-anchored numbers and the matrix-anchored numbers will diverge until the framework is reconciled with the velocity-conditional set.

This round does the reconciliation cleanly: replace the anchor, re-run the canonical sweep, report the closure-surface delta, and update derived artifacts. **The round is framework hygiene, not new science** — it propagates R-A14-engineering-decomposition's verdict into the framework's defaults so future workers don't re-import the superseded anchor by inertia.

---

## Out-of-scope guards

- Do NOT relitigate the R-A14-engineering-decomposition findings. The velocity-conditional set (0.53 / 0.41 / 0.69) is the operative input.
- Do NOT touch matrix `ARCHITECTURE-DECISION-MATRIX.md`, REQUIREMENTS.md, or design-axes/ files. Closure-surface changes are framework-side; orchestrator propagates to docs after worker completion.
- Do NOT touch `water-prop/rounds/R_assumption_audit_2026_05_21/BEST_ARCHITECTURES_25T.md` directly. Author a new sibling `BEST_ARCHITECTURES_25T_velocity_conditional.md` in the round's `results/` directory. Orchestrator decides whether to supersede the original or carry both.
- Bundle sequencing: this round should run AFTER R-framework-matrix-parity (titan-4 in-flight). R-framework-matrix-parity surfaces four constraints not yet in the framework (reactor lifetime, Modular Assembled Radiators bundled formula, bus-mass anchor, vis-viva delta-v anchors); landing those first avoids two-pass framework churn. If R-framework-matrix-parity is mid-flight when this round starts, coordinate via the orchestrator before touching shared framework files.

---

## The question this round answers

**Does the mission_graph framework's closure surface at L0-04 = 25 t survive the velocity-conditional reframe of single_pass_trawl capture efficiency?**

Three concrete sub-questions:

1. **Strict closure under velocity-conditional anchors:** with default Phase 3 capture options downgraded to 0.53 (mm/s undemonstrated baseline), does the framework still surface a non-empty closure set at L0-04 = 25 t? The 0.53 value sits between the 0.50 multiplier (matrix collapses) and the 0.75 multiplier (barely closes) in the Saturn-worker sensitivity sweep; the framework is at the cliff. Net direction is unclear from the sensitivity sweep alone — the actual cell-by-cell composition matters.
2. **Demonstrator-conditional closure:** with default Phase 3 capture options at 0.69 (demonstrator-confirmed), what does the closure surface look like? This is the architecturally-load-bearing case (matrix decision #13 carries the demonstrator-conditional gate); the framework should be able to compute its closure surface.
3. **Velocity-regime split:** the framework currently treats "single-pass trawl" as a single phase option with one efficiency anchor. Should the framework split into mm/s-trawl and low-m/s-trawl as two distinct Phase 3 options (analogous to how Phase 1 splits ballistic and Mars-Jupiter-GA)? That carries the velocity-conditioning into the architecture-search rather than hard-coding a single regime.

---

## Pre-registered hypotheses

| # | Hypothesis | Predicted range | Falsification band |
|---|---|---|---|
| H1 | Default-anchor velocity-conditional closure surface (0.53 mm/s) contracts substantially at strict L0-04 = 25 t versus the 0.85 desk-anchor baseline. Best single delivery drops from 39.5 t to <20 t; feasible-path count drops from 5,656 to <1,500. | Strict closure surface contracts by 50-80 percent on path count; best delivery drops below 25 t (no strict closure). | H1 falsified if the contraction is <30 percent — would suggest the 0.85 anchor was not load-bearing in the way the audit indicated. |
| H2 | Demonstrator-conditional closure surface (0.69) is intermediate — non-empty, smaller than 0.85 baseline, larger than 0.53 default. Best single delivery 25-35 t; feasible-path count 2,500-4,000. | Demonstrator-conditional closure surface non-empty; best delivery in the 25-35 t band. | H2 falsified if demonstrator-conditional closure is empty (would imply velocity-conditional set is not closure-rescuable even under demonstrator gating). |
| H3 | The dominant closing architecture at velocity-conditional anchors is the same as at the 0.85 baseline (single-launch + on-orbit assembly + low-thrust spiral + chunk-fed-spiral return + direct propulsive or hybrid aerocapture) — the architecture is robust to the anchor swap; the closure SURFACE shrinks but the TOP-RANKED PATHS don't change. | Top-ranked paths preserved; closure surface shrinks. | H3 falsified if a different architecture displaces the current top-ranked paths (would suggest the 0.85 anchor was hiding sensitivity to architecture choice). |
| H4 | Splitting Phase 3 single_pass_trawl into mm/s and low-m/s variants surfaces architectures that explicitly select mm/s capture as a load-bearing design choice; the framework's current implicit assumption (one capture option, velocity-agnostic) hides the conditioning structure. | After split, mm/s-trawl appears in top-ranked paths; low-m/s-trawl appears in feasible-but-not-top paths; some currently-feasible cells become low-m/s-only and drop. | H4 falsified if mm/s and low-m/s variants are indistinguishable in the closure surface (would suggest velocity-conditioning is not framework-actionable). |
| H5 | The velocity-conditional anchor set does NOT change the bet-#2 (water-electrothermal) and bet-#3 (reactor) closure surfaces independently of bet #1 — the three bets are decomposable in the closure-surface accounting, and bet #1's anchor change does not propagate to the other two. | Closure-surface delta from anchor swap is localized to capture-efficiency-sensitive cells; bets #2 and #3 closure surfaces unchanged. | H5 falsified if closure-surface deltas appear in cells that don't touch single_pass_trawl Phase 3 — would suggest the framework has cross-phase coupling not currently understood. |
| H6 (project-owner-facing) | The framework's closure surface at velocity-conditional anchors is **demonstrator-conditional in the same sense that the matrix verdict now is.** Without demonstrator gating, the strict-L0-04 closure surface is small or empty; with demonstrator gating, it is non-empty and architecturally credible. The framework anchor swap is hygiene that aligns the framework with the matrix's operative reading — not new closure-cell science. | Framework closure surface is hygiene-aligned with matrix; no closure cells survive un-demonstrated; demonstrator-conditional closure surface matches matrix's anticipated cells. | H6 falsified if the framework surfaces closure cells at velocity-conditional anchors that the matrix does not carry (would surface a framework-matrix-divergence beyond what R-framework-matrix-parity is currently scoped to find). |

If H6 holds, the framework is reconciled with the matrix at the velocity-conditional set; if H6 falsifies, framework-matrix-parity has a second divergence beyond the four constraints R-framework-matrix-parity scopes (reactor lifetime, MARVL, bus-mass, vis-viva).

---

## Deliverables

- `STUDY.md` — pre-registered hypotheses, methodology, framework-edit plan.
- `run.py` — re-runs the canonical sweep at velocity-conditional + demonstrator-conditional anchors.
- `inputs/anchor_swap_diff.json` — the literal framework-default changes (file paths + old / new values).
- `results/closure_surface_velocity_conditional.csv` — cell-by-cell closure at 0.53 default.
- `results/closure_surface_demonstrator_conditional.csv` — cell-by-cell closure at 0.69 default.
- `results/closure_surface_delta.md` — sub-questions 1 + 2 + 3 readings.
- `results/BEST_ARCHITECTURES_25T_velocity_conditional.md` — sibling to the original best-architecture report.
- `READING.md` — H6 verdict + recommended matrix-side propagation (which cells in BEST_ARCHITECTURES, mining_view, the 5,656 / 322 counts need updating).

---

## SCOPE guards (additional)

- The framework anchor swap is the load-bearing edit. Do NOT also swap other Phase 3 anchors (0.65 drift-through, 0.85 F-G gap, ~0.01 B-ring direct survival) unless R-A14-engineering-decomposition's findings extend cleanly to those (they do not in the current round; the round was scoped to single_pass_trawl).
- If the closure surface at velocity-conditional default is empty (H1 holds in the strong direction), do NOT falsify the architecture — the demonstrator-conditional case (0.69) is the operative one; the empty 0.53 case is the un-demonstrated baseline.
- Test that ALL existing pytest tests in `water-prop/sims/mission_graph/` still pass under the new defaults. If any test was anchored on the 0.85 number, surface the test as a finding (does the test encode an assumption that R-A14-engineering-decomposition now supersedes?).

---

## Suggested worker

mimas (recent framework-extension work; AST walker + canonical helper-pair experience in the codebase; demonstrated discipline on shared-doc-no-touch SCOPEs in R-shared-physics-audit). Saturn-worker re-spawn is the secondary fit (originally authored the framework; carries the most context on Phase 3 internals). titan-4 is mid-flight on R-framework-matrix-parity; do NOT route this round to titan-4 unless the parity round completes first — overlapping framework edits would conflict.

Sequencing recommendation: AFTER R-framework-matrix-parity lands, BEFORE R-near-earth-asteroid-mission-tree (which adds a second tree to the framework forest and would benefit from clean velocity-conditional defaults).
