# R-shared-physics-audit — how many rounds are contaminated by shared-physics-function input-convention bugs, and which still-live decisions depend on them?

**Status:** scope, pre-study. Authored by Saturn (orchestrator), 2026-05-20. Triggered by project-owner challenge during status review: "it seems like every test is contaminated and needs to be re-run with this new reality."

**Worker assignment:** open to any moon. Static-analysis round, not a physics round. Touches the shared `waterprop` Python package, the rounds tree, the architecture matrix, and the design-axes index.

---

## Context

Three independent rounds in the last two weeks found that load-bearing matrix verdicts were computed from shared physics functions called with the wrong input convention:

1. **hyperion R-bag-capture-efficiency-revisit** (commit `00cbfc1`, May 15 evening) — `water-prop/rounds/R_electric_outbound/run.py:223` understated outbound burn time by a factor of mass-ratio (~2.5× at megawatt era). Root cause: `constant_thrust_burn` in the shared library interpreted its `m_initial_t` argument as wet-mass-at-start-of-burn; the call site passed dry-mass-at-end-of-burn. No assertion on entry to catch the convention mismatch.
2. **titan-2 R-exit-burn-power-audit** (commit `95ca4d3`, latest+12) — same function class, 17.8× burn-time discrepancy at 500 kilowatt-electric in the composite chunk-rendezvous closure. Propagated through R-composite-burn-time-closure (`ea49a93`), R-spiral-out-exit-architecture (`8d6c3cb`), R-megawatt-composite-with-mass-scaling (`c2136e9`) — together these retracted the latest+11 "21.8% composite-close" headline for axis 19.
3. **enceladus-r5 R-variant-B-burn-consistency / R-variant-B-propellant-accounting / R-matrix-dv-regime-consistency** (commits `228adb8`, `ba42898`, `b91c6db`, latest+12) — different bug class: matrix-stated Variant B numbers don't reproduce from first principles. Not a function-call bug, but a matrix-anchor bug.

Methodology lesson 9 in `water-prop/PROTOCOL.md` (added after hyperion's catch) prescribed input-convention assertions on shared physics functions. The assertions have not been added to the library. The pattern has been reactive, round-by-round catches rather than a systematic sweep.

**Blast-radius reality check (static grep, this scope authoring pass):**

- 139 round directories under `water-prop/rounds/`.
- 37 rounds import the shared `waterprop` package (`grep -rln "from waterprop\|import waterprop" water-prop/rounds/`).
- 9 rounds call the specific functions known to have convention conventions (`constant_thrust_burn`, `edelbaum_spiral`, `spiral_burn` — verify exact function names during audit; some may be in different modules).
- 14 rounds already have `_audit` / `_revisit` / `_rerun` / `_consistency` suffixes — the reactive triage is already underway, ~10% of the tree.

Most rounds (~100 of 139) are pure desk-study Monte Carlo / closed-form / economics / base-rate sensitivity rounds that do not touch the shared physics functions and are not contaminated by this specific bug class. They may have other problems (anchor-conditional verdicts, stale matrix references) but not the convention bug.

The project-owner challenge therefore needs two answers, not one:

- **Function-convention contamination:** which rounds called a flagged function with wrong inputs, and how many of those rounds anchor a still-live design-axis or matrix-cell verdict?
- **Matrix-anchor contamination** (enceladus-r5 bug class): which load-bearing matrix cells have stated numbers that have not been re-derived from first principles since the round that authored them?

This SCOPE covers both. The function-convention half is mechanical and the audit can complete it. The matrix-anchor half is harder and may need to be deferred to a follow-on round per cell.

---

## What this round answers

**Primary question:** how big is the function-convention contamination, where is it concentrated, and what is the prioritized re-run list?

**Secondary question:** what mechanism gets added to the campaign so this class of bug stops slipping past round-completion?

Deliverables (in order):

1. **Contamination matrix.** Rows: every function in `water-prop/src/waterprop/` that has a mass-or-Δv interpretation convention (or any other input convention where a wrong-convention call would silently return a numerically plausible but physically wrong result). Columns: every round that imports the function. Cell: convention-correct / convention-incorrect / uncalled.
2. **Tiered re-run list.** Tier A (rounds whose verdict supports a still-open design axis or non-falsified matrix cell — re-run now). Tier B (rounds whose verdict supports a falsified cell or closed axis — verdict is structurally moot unless the finding would also flip an open axis). Tier C (isolated rounds whose verdict doesn't propagate — skip).
3. **Library hardening patch.** Pull-request-ready edits to `water-prop/src/waterprop/**/*.py` adding `assert` statements at function entry for every convention. Designed to fail loudly on wrong-convention calls instead of returning silently-wrong numbers.
4. **Audit script.** A short `water-prop/scripts/audit-call-conventions.py` that runs across the rounds tree, checks every caller of a flagged function against the convention specification, and exits non-zero if any caller is convention-incorrect. Wired into the round-completion checklist so future rounds can't merge without passing.
5. **Tier-A re-run dispatch.** Pre-registered hypotheses for each Tier-A re-run (does the corrected number flip the round's verdict?). Worker assignments suggested per re-run.

Out-of-scope for this round:

- Matrix-anchor contamination (enceladus-r5 bug class). Mentioned in §Reading template but the audit method differs (per-cell re-derivation) and that is best as a follow-on round per still-live cell.
- Anchor-conditional verdicts (bus-mass anchor, pricing anchor, reactor-program-availability anchor). These are project-owner adjudication items, not audit items.
- Re-running the Tier-A rounds themselves. This SCOPE produces the list and the dispatch. The re-runs are separate rounds.

---

## Pre-registered hypotheses (numeric ranges + falsification bands)

| # | Hypothesis | Predicted range | Falsification band |
|---|---|---|---|
| H1 | The number of rounds that call a flagged function with a convention-incorrect signature is between 3 and 12 (inclusive of the three already known: hyperion's catch + titan-2's catch + the propagated rounds those triggered). | 3 ≤ N ≤ 12 convention-incorrect rounds | H1 falsified high if N > 12 (campaign contamination is wider than reactive triage suggested); H1 falsified low if N < 3 (the known catches double-counted) |
| H2 | The number of Tier-A re-runs (convention-incorrect AND supporting a still-live decision) is between 4 and 10. The reason it's not zero: the campaign is still anchoring on the year-zero-through-fifteen Kilopower Variant B cell and the year-twenty-plus megawatt cell, both of which have outbound / inbound burn-time inputs that touch the flagged functions. | 4 ≤ Tier-A ≤ 10 | H2 falsified high if Tier-A > 10 (the audit reveals the matrix is more load-bearing on contaminated rounds than the matrix HISTORY suggests); H2 falsified low if Tier-A < 4 (most contamination is in already-falsified cells) |
| H3 | At least one Tier-A re-run, when actually re-run with the corrected convention, will flip a verdict that is currently being relied on for project-owner decision-making (decisions #1–#7 in `design-axes/INDEX.md`). | ≥ 1 Tier-A verdict flips | H3 falsified if every Tier-A re-run reproduces its prior verdict within ±15% on the load-bearing number |
| H4 | Adding `assert` statements at function entry would have caught all three already-known convention bugs (hyperion, titan-2, the propagated burn-time bugs) before they were committed. This is the trivial check; the hypothesis is here so the worker reports the counter-example if assertion-at-entry is insufficient for any of the three. | all 3 known bugs caught by assertions | H4 falsified if any of the 3 known bugs would have passed an entry assertion (would indicate the convention is value-domain-dependent, not signature-typeable, and a different mechanism is needed) |
| H5 | The `audit-call-conventions.py` script can be implemented in ≤ 200 lines of Python and runs in ≤ 30 seconds across the whole rounds tree. Cheap enough to put in a pre-commit hook. | ≤ 200 lines, ≤ 30 s wall-clock | H5 falsified if the script needs > 500 lines or > 2 minutes (would mean convention enforcement is too expensive to gate every commit on — needs a different mechanism, possibly a typed wrapper class) |
| H6 | (Reading-level — load-bearing for project owner.) The function-convention contamination, once fully audited and re-run, does NOT change the architecturally-binding constraints surfaced in latest+12: reactor-program-availability (L0-24), bus-mass anchor decision (#6), and pricing anchor decision (#5). The contamination is real and worth cleaning up, but it is NOT the load-bearing constraint on whether ICEBERG closes. | H6 held: function-convention bugs ≠ binding constraint | H6 falsified if any Tier-A re-run produces a corrected number that, on its own, flips a still-open architectural verdict independent of the three anchor decisions |

H6 is the load-bearing reading. H1–H5 build the evidence; H6 says whether the cleanup changes the project-owner decision space or just cleans up the audit trail.

---

## Method sketch (worker drafts the actual code in `run.py`)

This is a static-analysis + light-instrumentation round, not a Monte Carlo. Expected ~40% Python AST work, ~30% library reading, ~20% spreadsheet (tiered contamination matrix), ~10% manual round-result re-verification.

1. **Enumerate flagged functions.** Walk `water-prop/src/waterprop/` AST. For every function definition, classify whether any argument has an interpretation convention that, if violated, would return a silently-wrong physical answer (mass-at-start vs mass-at-end, Δv-impulsive vs Δv-integrated, wet vs dry, total-system vs reactor-only, etc.). The seed list is at minimum: `constant_thrust_burn`, `edelbaum_spiral`, `spiral_burn` — but the audit should not assume the seed list is complete. Document each flagged function with: file:line, signature, convention specification (one short sentence per argument), what a wrong-convention call would return (numerical direction + magnitude).
2. **Build the call graph.** For every round under `water-prop/rounds/`, grep `run.py` for callers of every flagged function. For each call site: extract the actual argument values being passed (often via reading the call-site context), and check whether the values satisfy the convention specification from step 1. Record: round name, call site (file:line), arguments passed, convention-correct / convention-incorrect / inconclusive (e.g., argument is computed from a variable whose convention is not obvious from local context).
3. **Tier the contaminated rounds.** For each convention-incorrect round, look up: (a) which design-axis state it currently supports (via grep of `design-axes/*.md` for the round name); (b) which matrix cell verdict it anchors (via grep of `water-prop/docs/ARCHITECTURE-DECISION-MATRIX.md` HISTORY entries); (c) whether the supported axis / cell is still live (open or non-falsified) or already retired (falsified or closed). Assign Tier A / B / C accordingly.
4. **Write the library hardening patch.** Add `assert` statements at the entry of each flagged function checking the convention. Statements should fail loudly with a one-line message naming the convention violated and the expected vs received argument shape. Patch should not change any function's return semantics — pure defensive instrumentation. Verify no currently-correct call site breaks by running the existing test suite (if any) and at least one known-correct round.
5. **Write the audit script.** `water-prop/scripts/audit-call-conventions.py`. Walks the rounds tree, identifies callers of flagged functions, checks convention-correctness via the same logic as step 2. Exits 0 if all callers correct, exits 1 with a per-violation report if any are incorrect. Add a `--strict` flag for the pre-commit-hook use case and a `--report` flag for human-readable output. Target ≤ 200 lines.
6. **Tier-A re-run dispatch.** For each Tier-A round, write a one-paragraph re-run scope: which call site is wrong, what the corrected call signature should be, the round's currently-asserted verdict, the predicted re-verdict band under correction. Each scope becomes the seed for a follow-on round assignment.
7. **Matrix-anchor contamination — separate accounting.** This round does NOT re-derive matrix cells from first principles (that's the enceladus-r5 bug class, which needs per-cell work). But the audit should produce a list of matrix cells whose stated numbers have not been re-derived since the round that authored them — pre-registered as a follow-on round candidate.

---

## Reading template (5-section round template, worker fills in after run)

- **Hypotheses adjudicated.** Verdict per H1..H6 (held / falsified / held-with-margin / falsified-at-magnitude). Predicted vs measured numeric range for each.
- **Headline.** One-line summary: how many rounds are contaminated, how many of those are Tier A, and does H6 hold (i.e., is function-convention contamination the binding constraint or not).
- **Reading.** Reading-level decision the project-owner needs. Options:
  - **H6 held:** function-convention cleanup proceeds in parallel with anchor decisions, doesn't gate them. Tier-A re-runs queue as separate rounds.
  - **H6 falsified:** at least one Tier-A re-run flips an architectural verdict on its own. Surface the specific flip; project-owner re-reads the affected design axis before the next anchor decision.
- **Cross-learning.** What this round teaches about shared-library discipline in a Monte-Carlo-heavy campaign. Relationship to PROTOCOL methodology lessons 9 (input-convention assertions) and 10 (multi-burn-stack mass propagation). Specifically: lesson 9 was the right diagnosis but the wrong enforcement mechanism — assertions live in the library, but the audit needs a tree-walking gate that can't be skipped on a round-by-round basis.
- **Next-round candidates.**
  - Tier-A re-runs (each its own round, scoped per step 6).
  - Matrix-anchor contamination audit (the enceladus-r5 bug class) — per-cell re-derivation rounds for the still-live cells. The cells most worth checking first: year-zero-through-fifteen Kilopower Variant B numerics (already partially audited by enceladus-r5's three rounds), year-twenty-plus megawatt cell numerics at heritage and conservative bus anchors.

---

## Worker assignment notes

- **Round priority:** **high.** Project-owner-triggered. Lands as a prerequisite to any further architectural rounds — the campaign needs the contamination matrix before deciding which other rounds are worth re-running.
- **Worker fit:** any moon. Light on physics, heavy on Python AST walking, grep-discipline, and disciplined per-round verdict-vs-axis-vs-cell traceability. Worker should be comfortable reading other workers' `run.py` files and recognizing convention violations.
- **Inputs the worker needs:**
  - `water-prop/PROTOCOL.md` methodology lessons 9 and 10 (the bug class definition).
  - `water-prop/src/waterprop/` — the shared library to audit.
  - `water-prop/rounds/` — every round directory; specifically `R_electric_outbound/run.py`, `R_bag_capture_efficiency_revisit/`, `R_exit_burn_power_audit/`, `R_composite_burn_time_closure/`, `R_spiral_out_exit_architecture/`, `R_megawatt_composite_with_mass_scaling/`, `R_variant_B_burn_consistency/`, `R_variant_B_propellant_accounting/`, `R_matrix_dv_regime_consistency/` (the known catches and propagations — start by understanding what's already been found).
  - `design-axes/INDEX.md` — the still-live decision space; the tier-A filter.
  - `water-prop/docs/ARCHITECTURE-DECISION-MATRIX.md` — HISTORY entries to trace which round supported which cell verdict.
  - `SESSION-LOG.md` latest+11 and latest+12 entries — the retraction trail.
- **Out-of-scope for this round:** any actual Tier-A re-run (those are follow-on rounds). Any anchor-decision adjudication. Any new physics. Any change to round-result files for past rounds (the audit produces verdicts about which rounds need re-running, but does not modify their result files).
- **Authorial note from Saturn:** the project-owner challenge was specifically "every test is contaminated and needs to be re-run." Pre-registered hypotheses bracket the realistic answer at 3 to 12 contaminated rounds out of 139, with 4 to 10 of those being Tier A. If the audit comes back with > 12 contaminated rounds, that is the unhappy outcome and the project-owner needs to know quickly because the campaign's audit trail becomes substantially less load-bearing. If the audit comes back with the predicted range, the cleanup is finite and the architectural binding constraints (reactor-program-availability, bus-mass anchor, pricing anchor) remain where latest+12 left them.
