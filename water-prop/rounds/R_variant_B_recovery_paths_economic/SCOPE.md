# R-variant-B-recovery-paths-economic — bake-off pricing of the three Variant B amendment paths against R-delivery-irr-curve's hurdle table

**Status:** scope, pre-study. Authored by Saturn (orchestrator) on 2026-05-15 late evening after hyperion's R-variant-B-impulsive-vs-continuous (commit `daaf522`) falsified Option A as locked.

**Trigger and standing:** under first-principles continuous-thrust accounting, the matrix's 500-kilowatt-electric all-electric inbound cell at the 200-tonne chunk-mass cap (L1-007) delivers 0.0 tonnes — Variant A collapses. Three amendment paths surfaced by the worker; project owner has deferred the decision pending a bake-off that prices the three paths against R-delivery-irr-curve's marginal-internal-rate-of-return hurdle table.

## The three paths under test

| Path | Architecture | Delivered (t/mission) | Round-trip (yr) | L0-05 status | Notes |
|---|---|---:|---:|---|---|
| 1 — Earth aerocapture mandatory | Variant C (Earth aerocapture only, no Saturn-egress chemical kick) | 32.1 | 16.32 | over by 1.3 yr; needs soft margin | hyperion R-variant-B-impulsive-vs-continuous Variant C |
| 2 — No surviving cell | n/a — accept that under conservative assumptions there is no defensible matrix cell | 0 | n/a | n/a | program reframes as technology-demonstrator, not commercial |
| 3 — Chunk reduction to 100 t | 500-kilowatt-electric all-electric inbound at chunk ≤ 100 t (L1-007 relaxed downward, not upward) | TBD by this round | TBD | TBD | hyperion-queued; un-computed |

This round adds the economic axis (marginal internal-rate-of-return at the integrated cashflow level) to the propulsion-physics axis already established.

## Question this round answers

For each of the three paths (1, 2, 3) operating at the 500-kilowatt-electric Variant B architecture (no chemical trim at Earth capture, per rhea Round 3 / Option A):

1. **Marginal internal-rate-of-return at the worker's delivered-mass figure**, computed against R-delivery-irr-curve's cashflow model (R-reactor-roadmap's MARVL-anchored mass + R-power-base-rate reactor cumulative-distribution-function). For path 3, compute delivered-mass first under hyperion's Variant-A-equivalent at chunk 100 t before computing marginal internal-rate-of-return.
2. **Where each path falls against R-delivery-irr-curve's hurdle table** (sovereign-bond ~4 percent at 209 tonnes-per-ship; regulated-utility ~8 percent at 461 tonnes-per-ship; corporate-growth ~10 percent at 691 tonnes-per-ship).
3. **Programmatic-risk-adjusted expected delivered-mass per mission** for each path, propagating hyperion's three-prior bracket on US fission orbit by 2035 (uniform 8.9 percent / Jeffreys 4.9 percent / skeptical 2.9 percent).
4. **L0-05 status under each path.** Path 1 is over by 1.3 yr at the 200-tonne cap. Path 3 may be under or over depending on resized delta-velocity. Path 2 sidesteps the requirement.
5. **Sensitivity to L1-007 relaxation upward.** For paths 1 and 3, if the chunk-mass cap is relaxed to the B-ring single-chunk physical cap (482 tonnes-per-ship) instead of held at 200 t (path 1) or further reduced to 100 t (path 3), where does the marginal internal-rate-of-return move?

## Pre-registered prediction (sketch — full hypothesis grading in STUDY.md when round runs)

**Aggregate:** none of the three paths clears the regulated-utility hurdle (~8 percent marginal internal-rate-of-return) without simultaneously closing aerocapture AND relaxing L1-007 upward. Path 1 + aerocapture closure + L1-007 → 482 tonnes-per-ship is the only configuration that approaches ~6-8 percent. Path 3 (chunk reduction) reduces per-mission revenue more than it reduces costs and is a net negative on marginal-internal-rate-of-return. Path 2 is the most honest reading: at conservative assumptions, the program is a technology demonstrator, not a return-seeking-capital play.

**Falsification bands and sub-claims to refine in STUDY.md:**

- Path 1 (aerocapture mandatory) at 32.1 tonnes-per-ship, L1-007 unchanged: marginal internal-rate-of-return is 0.5–2.5 percent. Falsified if > 3 percent (in which case path 1 alone clears sovereign-bond floor without further changes).
- Path 1 + aerocapture + L1-007 → 482 tonnes-per-ship: marginal internal-rate-of-return is 5–8 percent (just below or at regulated-utility hurdle). Falsified if > 10 percent (corporate-growth reachable) or < 3 percent (aerocapture alone is insufficient even with chunk-cap relaxation).
- Path 3 (chunk reduction to 100 t) delivered-mass: at hyperion's Variant-A architecture under chunk 100 t, expect ~30–50 tonnes per mission (the lower chunk relaxes inbound delta-velocity disproportionately). Falsified if < 15 t or > 80 t.
- Path 3 marginal internal-rate-of-return: 1–3 percent. Falsified if > 5 percent (chunk reduction beats path 1) or < 0 percent (chunk reduction makes economics worse than the falsified Variant A baseline).
- Programmatic-risk-adjusted delivered mass per path under uniform prior: path 1 ≈ 0.04 tonnes-per-mission; path 3 ≈ 0.03 tonnes-per-mission. Falsified if either is > 0.5 tonnes-per-mission (which would re-enable a commercial reading).

## Method sketch

Approximate methodology — detailed in STUDY.md when the round runs.

1. **Cashflow model reuse.** Use R-delivery-irr-curve's cashflow model directly (in `water-prop/rounds/R_delivery_irr_curve/run.py`); do not re-derive the discount-rate or per-ship-revenue assumptions. Cross-reference R-reactor-roadmap's mass model.
2. **Path 1 input:** hyperion R-variant-B-impulsive-vs-continuous Variant C delivered-mass (32.1 tonnes-per-ship at chunk 200 t) and round-trip (16.32 yr).
3. **Path 3 input:** re-run hyperion's R-variant-B-impulsive-vs-continuous run.py with chunk 100 t and no recovery (Variant A under reduced chunk). Output: delivered-mass and round-trip at the smaller chunk.
4. **Path 2 input:** no propulsion-side number; path 2 is the explicit acknowledgement that the cashflow model returns marginal internal-rate-of-return < 0 under conservative assumptions. Compute the gap-to-sovereign-bond to quantify "how much wrong" the program is.
5. **Marginal-internal-rate-of-return computation per path.** R-delivery-irr-curve's run.py takes delivered-mass-per-ship as an input. For each path, sweep the L1-007 chunk-mass cap from the path's natural value (200 t for path 1, 100 t for path 3) up to the B-ring single-chunk physical cap (482 tonnes-per-ship).
6. **Programmatic-risk overlay.** Apply hyperion R-power-bayesian-update's three-prior bracket (uniform 8.9 percent / Jeffreys 4.9 percent / skeptical 2.9 percent) to convert "delivered mass conditional on reactor available" to "expected delivered mass." Report unconditional expected marginal internal-rate-of-return for each path.
7. **Hurdle-table comparison.** Tabulate where each path falls relative to R-delivery-irr-curve's hurdle crossovers (sovereign-bond 209 t/ship, regulated-utility 461 t/ship, corporate-growth 691 t/ship). Path-vs-hurdle is the single deliverable that drives the project-owner's matrix-amendment decision.
8. **Deterministic run.py per project convention.** No randomness; results reproducible from inputs.

## What this round does NOT cover (deferred to follow-on rounds)

- Engineering closure of aerocapture itself. R-chunk-as-heat-shield-revisit (separate round; SCOPE.md at `water-prop/rounds/R_chunk_as_heat_shield_revisit/SCOPE.md`) owns that. This round prices the architectural choice assuming aerocapture closes; if it does not, path 1 is unavailable.
- Cryogenic hydrolox storage technology-readiness assessment (the "preserve 27.6 percent delivered but admit Technology-Readiness-Level-3 cryogenic dependency" path rhea named as Option B in Round 3, not under test here). Option B was not picked up by the project owner as a candidate path; if it returns to the table, this round should be extended.
- Architecture D (D-fission / D-solar-thermal) costing. Owned by R-architecture-D-cost (not yet pre-registered).
- L0-05 round-trip ceiling relaxation. If path 1 wins this round, the next conversation is whether L0-05 admits a 16.32-yr round-trip under soft-margin. That is a REQUIREMENTS.md amendment, not a propulsion round.

## Cross-references (read before authoring STUDY.md)

- `water-prop/rounds/R_variant_B_impulsive_vs_continuous/STUDY.md` — hyperion's just-shipped round establishing the three paths.
- `water-prop/rounds/R_delivery_irr_curve/STUDY.md` + `run.py` — the cashflow model this round uses.
- `water-prop/rounds/R_reactor_roadmap/STUDY.md` — the MARVL-anchored mass + R-power-base-rate reactor distribution.
- `water-prop/rounds/R_power_bayesian_update/STUDY.md` — the three-prior bracket for the programmatic-risk overlay.
- `water-prop/rounds/R_chemical_trim_vs_all_electric_earth_arrival/STUDY.md` — rhea Round 3's chemical-trim falsification, which is the precondition for the Option-A → bake-off chain.
- `water-prop/docs/ARCHITECTURE-DECISION-MATRIX.md` — late-evening PAUSE block at the top of the document. The matrix is paused awaiting this round's output.
- `water-prop/rounds/R_variant_B_500kWe_sizing/STUDY.md` — hyperion's 500-kilowatt-electric optimum finding (independent of which path wins).

## Deliverables

- `water-prop/rounds/R_variant_B_recovery_paths_economic/STUDY.md` — pre-registration + Result + Reading + Revisit + Cross-learning per project template.
- `water-prop/rounds/R_variant_B_recovery_paths_economic/run.py` — deterministic, wraps R-delivery-irr-curve's run.py and hyperion R-variant-B-impulsive-vs-continuous's run.py.
- `water-prop/rounds/R_variant_B_recovery_paths_economic/results/` — JSON outputs + tables.md with the path-vs-hurdle comparison table.
- `water-prop/RUNNING_DOC.md` — append round-status entry + narrative section.
- Handoff at `~/.claude/handoffs/iceberg-WORKER-NAME-YYYYMMDD.md` whose headline is the project-owner-facing recommendation among paths 1/2/3.

## Pre-registration discipline

Per the recurring methodology lesson surfaced in R-reactor-roadmap and R-delivery-irr-curve: compute the back-of-envelope answer for each sub-claim with central inputs BEFORE freezing the ±band in pre-registration. R-delivery-irr-curve was the first all-seven-hypotheses-held round of the campaign by following this discipline. Adopt it here.
