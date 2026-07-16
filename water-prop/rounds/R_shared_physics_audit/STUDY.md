# R-shared-physics-audit — campaign-wide contamination matrix for shared-physics-function input-convention bugs

**Round:** R-shared-physics-audit
**Started:** 2026-05-20
**Worker:** mimas
**Branch:** iceberg-mimas
**Orchestrator:** Saturn (worktree-092320)
**Status:** in progress

---

## Phase question

Project-owner challenge (2026-05-20 latest+14): "every test is contaminated and needs to be re-run with this new reality."

How big is the function-convention contamination across the 146 round-directories under `water-prop/rounds/`, where is it concentrated, and which of those rounds anchor a still-live design-axis or matrix-cell verdict?

Secondary: what enforcement mechanism (assertion-at-entry plus tree-walking audit script) prevents this bug class from recurring round-to-round.

## Context

Three independent rounds caught function-convention bugs in the prior two weeks:

1. **Hyperion R-bag-capture-efficiency-revisit** (`00cbfc1`, 2026-05-15) — `R_electric_outbound/run.py:223` passed dry-tug mass to `constant_thrust_burn`, whose Tsiolkovsky math expects wet-mass-at-start-of-burn. Burn-time understated by mass-ratio factor (~2.5× at megawatt era).
2. **Titan-2 R-exit-burn-power-audit** (`95ca4d3`, latest+12) — same bug class. 17.8× burn-time discrepancy at 500 kilowatt-electric in composite chunk-rendezvous closure. Propagated through `R_composite_burn_time_closure`, `R_spiral_out_exit_architecture`, `R_megawatt_composite_with_mass_scaling`.
3. **Enceladus-r5 R-variant-B-{burn-consistency,propellant-accounting,matrix-dv-regime-consistency}** (`228adb8`, `ba42898`, `b91c6db`, latest+12) — **different bug class** (matrix-anchor numbers not reproducing from first principles). Read for pattern recognition; out-of-scope for this round's audit method (per SCOPE §"Out-of-scope" — needs per-cell re-derivation, not call-graph walking).

The diagnosis from PROTOCOL methodology lesson 6 — "shared-physics function input conventions need assertions" — assumes the contaminated functions live in the shared `waterprop/` package and that adding entry assertions is a single edit per function. Pre-audit static survey (worktree-092320) showed 9 rounds called the named functions, suggesting a bounded blast radius.

**Mimas pre-audit cross-check (this STUDY-authoring pass):** the three named seed-list functions (`constant_thrust_burn`, `edelbaum_spiral`, `spiral_burn`) are **NOT defined in `waterprop/src/`**. They are redefined locally in 6 round-level `run.py` files. The shared library has its own convention-bearing functions (`power_optimal_isp`, `energy_balance_residual`, `delivery_fraction_chunk_fed`), but those are NOT the source of the three known catches. This reshapes the audit: the actual contagion pattern is copy-pasted-physics with per-round convention drift, not single-library-function-with-many-callers. The library hardening patch can add assertions in `waterprop/`, but the round-level redefinitions need their own treatment.

## Pre-registered hypotheses

Lifted from SCOPE.md §"Pre-registered hypotheses" with predictions sharpened by the mimas pre-audit cross-check. All numeric thresholds remain SCOPE-stated.

### H1 — Convention-incorrect round count

**Predicted range:** 3 ≤ N ≤ 12 convention-incorrect rounds out of 146.

**Mimas point prediction:** N ≈ 5–7. The known catches (hyperion's call site in `R_electric_outbound`, titan-2's chain) account for ≥ 3. The 6 round-local redefinitions of `constant_thrust_burn` (the seed-list function) bound the function-convention contamination upward — only those 6 rounds can carry the convention bug for that specific function. Spiral / Edelbaum functions add a small additional set (1-2 rounds).

**Falsification:**
- **High (N > 12):** campaign contamination is wider than reactive triage suggested; audit trail substantially less load-bearing than the matrix HISTORY presumes.
- **Low (N < 3):** known catches double-counted in headline framing.

### H2 — Tier-A re-run count

**Predicted range:** 4 ≤ Tier-A ≤ 10 (convention-incorrect AND supporting a still-live decision).

**Mimas point prediction:** Tier-A ≈ 2–4. The 2026-05-19 latest+13 directive retiring 500 kilowatt-electric and the closure of axes 03, 04, 06, 07, 15, 18 leave fewer live axes than the SCOPE-authoring-time matrix carried. Several contaminated rounds (notably `R_inbound_dv_continuous_thrust`, `R_megawatt_architecture_viability`) anchor cells that are now closed-by-directive or closed-on-physics, making them Tier-B at best.

**Falsification:**
- **High (Tier-A > 10):** matrix is more load-bearing on contaminated rounds than the matrix HISTORY suggests.
- **Low (Tier-A < 4):** most contamination is in already-falsified cells. (Note: mimas point prediction is on the low edge of the SCOPE band; if Tier-A < 4 holds, that is mimas-predicted, not SCOPE-predicted.)

### H3 — Tier-A verdict-flip

**Predicted:** ≥ 1 Tier-A re-run flips a verdict currently being relied on for project-owner decision-making (design-axes/INDEX.md decisions #1–#7 + #14).

**Mimas point prediction:** H3 falsified. The titan-3 closure cell at 40-80 tonne / 30 kilowatt-electric is the only still-live closure cell, and it is anchored on titan-3's own clean rounds (not on contaminated rounds). The audit is most likely to clean up audit trail for retired cells, not flip a live decision.

**Falsification:** any Tier-A re-run, when actually re-run with the corrected convention, reproduces its prior verdict within ±15% on the load-bearing number. (Note: H3 is the SCOPE's null hypothesis; "falsified" by SCOPE language = "audit produces no live-decision flip" = mimas's predicted outcome.)

### H4 — Assertion-at-entry catches all three known bugs

**Predicted:** all three known catches (hyperion, titan-2, titan-2 propagations) would have been caught by assertion-at-entry on the relevant function.

**Mimas point prediction:** H4 partial. Of the three known catches, only one (hyperion `R_electric_outbound:223`) is the canonical function-convention bug class addressable by `assert m_initial == m_dry + m_prop` at function entry. The titan-2 17.8× burn-time discrepancy needs a closer reading to confirm class; the enceladus-r5 catches are matrix-anchor, not function-convention, and the SCOPE explicitly excludes them. Expect 1-of-1 known catches in scope to be assertion-catchable.

**Falsification:** any in-scope known catch slips past a reasonable entry-assertion. Would indicate the convention is value-dependent (not signature-typeable), and a different mechanism (typed wrapper class, named-helper-pair like `burn_from_wet` / `burn_from_dry_end`) is required.

### H5 — Audit script size and runtime

**Predicted:** ≤ 200 lines Python, ≤ 30 seconds wall-clock across the 146-round tree.

**Mimas point prediction:** H5 held with margin. Plain-text grep + AST-walking the local definitions is cheap; the dominant cost is reading every `run.py` once, which is bounded.

**Falsification:** script exceeds 500 lines or 2 minutes — would mean convention enforcement is too expensive to gate every commit on.

### H6 — Load-bearing reading (binding-constraint test)

**Predicted:** function-convention contamination, fully audited and (hypothetically) re-run, does NOT change the binding constraints surfaced as decision points #5 (pricing anchor), #14 (reactor power class for closure cell, R-kilopower-scale-up-credibility-blocked), and #15 (L0-04 strict deliver-to-Earth-orbit vs Saturn-system depot waiver). The contamination is real, parallel cleanup; not architecturally rescuing.

**Mimas point prediction:** H6 held. Falsification would require a Tier-A re-run that on its own flips a still-open architectural verdict. The closure cell that matters (titan-3 40-80 tonne / 30 kilowatt-electric) does NOT depend on any of the 6 round-local-redefinition rounds — it is anchored on titan-3's own clean computations. Cleanup of the contaminated rounds therefore cannot rescue or destroy the closure cell on its own.

**Falsification:** ≥ 1 Tier-A re-run produces a corrected number that, on its own, flips a still-open architectural verdict independent of the three anchor decisions.

H6 is the load-bearing reading. H1–H5 build the evidence; H6 says whether the cleanup changes the project-owner decision space or just cleans up the audit trail.

## Method

Static-analysis round. Six steps in `run.py`:

1. **Catalogue shared-library functions.** AST-walk `water-prop/src/waterprop/`. For each function definition, classify whether any argument has a convention that, if violated, returns a silently-wrong physical answer. Document signature + convention specification + wrong-convention failure mode. (Result: library is small — 11 .py files, 747 lines total — so the catalogue is exhaustive.)
2. **Catalogue round-local convention-bearing functions.** AST-walk `water-prop/rounds/*/run.py`. Identify any local function definition matching the seed-list names or carrying similar signatures (mass + delta-velocity + power + specific-impulse → propellant + burn-time). Record per-round formula variant.
3. **Build the call graph.** For every importer of a flagged shared-library function (`grep` for `from waterprop` + `import waterprop`), record the call site + the literal argument expression. For every round-local redefinition, record the call sites within that round.
4. **Convention-correctness verdict per call site.** For each call site: extract the variable being passed; trace its assignment within the same `run.py`; check whether the variable's semantic content (e.g., wet-mass-at-start vs dry-mass-at-end) matches the function's documented convention. Three verdicts: correct / incorrect / ambiguous-needs-manual-review.
5. **Tier the rounds.** For each convention-incorrect round, grep `design-axes/*.md` and `water-prop/docs/ARCHITECTURE-DECISION-MATRIX.md` HISTORY for the round name. Tag the supported axis/cell + read its status (open / closed / falsified) from `design-axes/INDEX.md`. Assign Tier A / B / C.
6. **Tier-A dispatch.** For each Tier-A round, write a one-paragraph re-run scope (call site identified, corrected call signature, current asserted verdict, predicted re-verdict band under correction). Output to READING.md "Next-round candidates" section.

Deliverables in commit order: STUDY (this file) → run.py (steps 1-6 logic) → contamination_matrix.csv (output of steps 2-5) → results/H1..H6.md (per-hypothesis verdict) → library hardening patch (assertions on `power_optimal_isp` and `energy_balance_residual`; canonical `burn_from_wet` / `burn_from_dry_end` helpers added to `propulsion/`) → audit-call-conventions.py enforcement script → READING.md.

## Out-of-scope

Per SCOPE.md and ASSIGNMENT.md:

- Matrix-anchor contamination (enceladus-r5 bug class). Mentioned in READING.md as follow-on round candidate.
- Anchor-conditional verdicts (bus-mass, pricing, reactor-program-availability, 30-kilowatt-electric closure cell). Project-owner adjudication items.
- Running any Tier-A re-run. This round produces the list; the re-runs are separate rounds.
- Editing shared docs (REQUIREMENTS, design-axes, matrix, RISKS, SESSION-LOG, pitch docs). Findings go in this round's READING.md; Saturn integrates.
- Picking up R-kilopower-scale-up-credibility. Separate Open SCOPE assigned to iapetus/hyperion.

## Reading template (filled in after run)

5-section round template per SCOPE.md §"Reading template": Hypotheses adjudicated, Headline, Reading, Cross-learning, Next-round candidates.
