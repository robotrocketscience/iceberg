---
axis: "Reactor power floor"
status: open
confidence: high
last_revised: 2026-05-22 (latest+18)
related:
  - "[[reactor-specific-power]]"
  - "[[saturn-side-process-power]]"
  - "[[program-class]]"
  - "[[surviving-cell]]"
  - "[[chunk-mass-cap]]"
---

# Reactor power floor

## Current

**2026-05-19 latest+13 RETRACTION under project-owner directive ("a 500 kilowatt reactor is not going to happen; stop accounting for it"):** the prior "500 kilowatt-electric optimum for Variant B / Architecture E" reading is RETIRED. New floor of record per titan-3 R-chunk-size-pareto closure cell: **20-30 kilowatt-electric Kilopower-extrapolation** (waiver closure at P=20-30 kilowatt-electric; strict closure at P=30 kilowatt-electric only). At pure-electric inbound with the 200-tonne commercial chunk anchor, 0 of 36 cells close at 1-30 kilowatt-electric (titan-3 R-kilowatt-class-power-envelope `5162735`). The closure path requires smaller chunk (40-80 tonnes) + 30 kilowatt-electric simultaneously. **Open project-owner question:** is 30 kilowatt-electric defensibly Kilopower-extrapolation, or does it quietly re-import the retired 500 kilowatt-electric fantasy? Kilopower's flown anchor is single-kilowatt; KRUSTY 2018 ground-test was 1-kilowatt-electric at 28-hour life; 30 kilowatt-electric requires either 30× scale-up of an under-developed program or 30 parallel single-kilowatt units. Variant B (500 kilowatt-electric / 200-tonne chunk) is retired across all matrix rows; every prior result anchored on it inherits implicit retraction.

**2026-05-21 latest+15 (framework-state note, Saturn worker `d8dd956`):** the `water-prop/sims/mission_graph/` framework now carries a **burn-time-vs-coast constraint** on low-thrust options that validates the framework against titan-3 R-chunk-size-pareto's verdict at heavy mass. Two remaining reactor-power-floor constraints are **NOT yet encoded** in the framework: (a) reactor lifetime versus cumulative full-power burn time (axis 20); (b) Modular Assembled Radiators for Very Large systems bundled radiator-mass formula. When the framework gains those constraints, expect the closure surface to shift further; the framework-versus-matrix closure-cell divergence is the load-bearing reading for `R-framework-matrix-parity` (punch-list item M-4 / S-1).

**2026-05-22 latest+18 — FRAMEWORK GAINS BOTH CONSTRAINTS (titan-4 `0eb11a7`):** R-framework-matrix-parity encoded all four matrix-carried constraints, including reactor lifetime versus cumulative burn and the Modular Assembled Radiators for Very Large systems bundled radiator-mass formula. The closure-surface shift is decisive: constraints-ON, the 200-tonne closure cell collapses to **0 surviving cells at conservative anchors** across the entire 1-55 kilowatt-electric flyable envelope. Two independent killers, each sufficient: (a) **a launch-feasible small vehicle cannot carry a flyable-class reactor** — at 30 kilowatt-electric / 2.4 watts-per-kilogram the powerplant is 22.8 tonnes; a 50-tonne launch vehicle has 10 tonnes of dry mass (constraints 2 + 3 binding jointly); (b) **a reactor cannot run long enough to move a multi-tonne chunk at the flyable power envelope** — cumulative full-power burn to move a 200-tonne chunk at 30 kilowatt-electric is 14-16 yr, over any plausible lifetime ceiling (KRUSTY heritage 28 hours; Brayton-flight-rated 5-yr floor; Kilopower design target 10 yr). H1 (lifetime) + H2 (specific power) both fall at every L ∈ {5, 10, 15, ∞} × specific power ∈ {2.4, 5, 10}. The framework now enforces the same two physics walls the campaign's locked findings already name (power finding 1: 40 watts-per-kilogram is aspirational; bet #3 audit) rather than by per-round assertion. Caveat from worker: `electric_burn_hours` uses thrust = 2P/v_e (more physical; ties burn time to power not to the framework's `electric_thrust_n` param; documented in `powerplant_constraints.py`). Hybrid power classes (e.g., kilopower + 20-kilowatt-solar) over-charged on powerplant mass — framework charges reactor+radiator on effective power, not split reactor/solar (conservative; flagged in code).

## Open question

**Project-owner resolution 2026-05-22 latest+16:** require the explicit KRUSTY-scale-up-credibility audit before committing to soften-or-hold of the locked-memory directive (matrix decision point #14 option (iii)). R-kilopower-scale-up-credibility (SCOPE'd 2026-05-19 latest+13; highest-priority in Open SCOPEs queue) is the load-bearing audit input; until it ships, the matrix does NOT carry titan-3's closure cell as state-of-record. The locked-memory directive ("Kilopower-class single-kilowatt fission at best") stands as the operating envelope; titan-3's 40-80 tonne / 30 kilowatt-electric closure cell is held in abeyance pending the audit's H6 reading. Soft-or-hold call deferred until then.

**Audit verdict 2026-05-22 latest+17 (hyperion re-spawn `3529984`): H6 HELD.** Hyperion recommendation: hold the no-large-fission directive (option b); option (a) accept-30-kilowatt-electric is structurally indefensible. The 30 kilowatt-electric cell is MASS-ROBUST at KRUSTY-measured 2.4 watts-per-kilogram (H2/H3 falsified — parallel modules preserve per-unit 2.4 → ~1.8-2.4 effective; strict cell collapses only below 1.1-1.6). It FAILS on programmatic + lifetime: Path A (single 30 kilowatt-electric core) is Fission-Surface-Power-class, joint posterior 1.5 → 0.5 percent skeptical; Path B (30× parallel 1-kilowatt-electric Kilopower modules) is honestly Kilopower-extrapolation but 0.15 → 0.05 percent; Path C 0.43 → 0.14 percent. None reach the 5 percent falsify band. Lifetime corroborates: KRUSTY 28-hour heritage versus ~6-8 year cumulative full-power burn required is 3-4 orders of magnitude short (independent of Path A/B/C). **Operating envelope of record:** locked-memory directive at single-kilowatt Kilopower-class; titan-3's 30 kilowatt-electric closure cell is annotated as mass-robust but retired-as-state-of-record on programmatic + lifetime grounds. Project-owner ratification on option (b) hold-directive is the substantive remaining call.

## Last touched by

- hyperion R-variant-B-500kWe-sizing — `5c2b294` [RETRACTED]
- hyperion R-power-bayesian-update — `67e08a6`
- titan-3 R-kilowatt-class-power-envelope — `5162735` + `10b77b7`
- titan-3 R-chunk-size-pareto — `1997a51`
- Saturn worker mission-graph burn-time-vs-coast validation — `d8dd956`
- titan-4 R-framework-matrix-parity — `0eb11a7` (mass-floor + reactor-lifetime now framework-enforced; 200-t cell collapses to 0 surviving cells at conservative anchors)

## HISTORY

### 2026-05-15 — Initial scaffold from `ARCHITECTURE-DECISION-MATRIX.md` current-decision-state table

Status: open. Confidence: high.

Current state and open question captured from the matrix's top section as of commit `9704700`. Full audit trail of how this axis arrived at its current state is in the matrix HISTORY section (`water-prop/docs/ARCHITECTURE-DECISION-MATRIX.md`).

---

<!-- Append-only HISTORY entries go below this line. Each entry: ### YYYY-MM-DD — round-name or commit-hash — one-line summary -->

### 2026-05-19 latest+13 — titan-3 batch (merge `3be9ce0`) — 500 kilowatt-electric retired; 20-30 kilowatt-electric Kilopower-extrapolation surfaces as new floor

Project-owner directive 2026-05-19 retired 500 kilowatt-electric as fantasy-conditioned: "a 500 kilowatt reactor is not going to happen; stop accounting for it." Locked as feedback memory (`feedback_no_large_fission.md`). titan-3 R-kilowatt-class-power-envelope (`5162735`) tested pure-electric inbound at 1-30 kilowatt-electric + 200-tonne commercial chunk: 0 of 36 cells close. titan-3 R-chunk-size-pareto (`1997a51`) then swept chunk-mass × power × specific-power at corrected vis-viva delta-velocity anchors + R12 lunar-gravity-assist Earth-arrival: closure surfaces at 40-80 tonne chunks + 20-30 kilowatt-electric Kilopower-extrapolation (strict closures at P=30 kilowatt-electric only).

Tension: 30 kilowatt-electric is outside titan-3's own 1-10 kilowatt-electric "flyable" envelope from the predecessor round, and outside the locked-memory "Kilopower-class single-kilowatt at best" envelope. Project-owner-only decision whether to soften directive to admit 30 kilowatt-electric, hold strict, or require KRUSTY-scale-up-credibility audit. Status held at open / high.

### 2026-05-21 latest+15 — Saturn worker mission-graph framework (`d8dd956`) — burn-time-vs-coast constraint encoded; reactor-lifetime + Modular Assembled Radiators for Very Large systems flagged as not-yet-encoded

Mission-graph framework now validates against titan-3 R-chunk-size-pareto via a burn-time-vs-coast constraint on low-thrust options (heavier chunk requires more reactor power to fit burn into the 6-year Hohmann coast budget). This is the first framework-encoded reactor-power-floor constraint. Two reactor-power-floor constraints remain NOT-YET-ENCODED in the framework and are flagged as `R-framework-matrix-parity` open-round inputs (punch-list items M-4 / S-1): reactor lifetime versus cumulative full-power burn time (per enceladus-r5 R-reactor-lifetime-vs-burn-time finding) and the MARVL bundled radiator-mass formula (per locked belief `0418e2c9` finding that at megawatt-electric scale the bundled formula 5 t + reactor_kilowatt-electric × 0.1 t is closer to correct than the decomposed model). When the framework gains those constraints, expect the closure surface to shift further. Status held at open / high; the addition is framework-state context, not a new decision.

### 2026-05-22 latest+17 — hyperion R-kilopower-scale-up-credibility (`3529984`) — H6 HELD; option (a) indefensible

Audit verdict on matrix decision point #14: the 30 kilowatt-electric closure cell is mass-robust at flown 2.4 watts-per-kilogram but programmatically near-zero (≤1.5 percent under uniform prior on the most-charitable single-core path; 0.05-0.43 percent on the genuinely-Kilopower parallel-module and intermediate paths) and lifetime-falsified (KRUSTY 28-hour heritage versus ~6-8 year cumulative full-power burn). H2/H3 (mass-axis falsification by analogy to 500-kilowatt-electric blowout) FALSIFIED — reactor mass scales linearly with power and 30 kilowatt-electric is 17× smaller, so the analogy did not transport. H1/H4/H5/H6 HELD: only the most-charitable single-core path (Path A, FSP-class, NOT Kilopower) reaches deliverable-looking posterior 1.5 percent, and that path is gated on a Fission-Surface-Power Phase 2 award that has not happened (locked finding `edcfe909`); the genuinely-Kilopower Path B is 0.05-0.15 percent. Decision #14 recommendation: option (b) hold the no-large-fission directive. Annotation reason for the retired-from-state-of-record titan-3 cell differs from the prior 500-kilowatt-electric cells (mass-died) — kept as a note in matrix Current section to avoid conflating failure modes. Status remains open / high; the resolution is a recommendation to the project owner, not a numerical change to the floor (the floor stays at locked-memory single-kilowatt-class until project owner ratifies hold-directive or overrides). Methodology-lesson candidate: do not import a failure mode across power classes without re-checking the scaling.

### 2026-05-22 latest+18 — titan-4 R-framework-matrix-parity (`0eb11a7`) — framework structurally enforces flyable-power constraint via mass-floor + reactor-lifetime

Worker encoded the four matrix-carried constraints into `water-prop/sims/mission_graph/`. The mass-floor + reactor-lifetime constraints flagged as not-yet-encoded at latest+15 are both now first-class, param-gated, and tested. Constraints-OFF reproduces the pre-encoding baseline exactly (16 cells, 200-tonne chunk only). Constraints-ON the 200-tonne closure cell collapses to 0 surviving cells at conservative anchors across the 1-55 kilowatt-electric flyable envelope. Two independent killers: powerplant dry-mass floor (50-tonne small vehicle / 10-tonne dry cannot carry 22.8-tonne reactor at 30 kilowatt-electric / 2.4 watts-per-kilogram; bigger vehicles ≥150 t don't deliver ≥30 t even baseline); reactor lifetime (200-tonne chunk at 30 kilowatt-electric needs 14-16 yr cumulative burn, over any plausible ceiling). H1 + H2 both fall at every L ∈ {5, 10, 15, ∞} × specific power ∈ {2.4, 5, 10}. Framework now enforces the same physics walls the locked findings name (power finding 1: 40 watts-per-kilogram aspirational; bet #3 audit) rather than by per-round assertion.

Status held at open / high. Substantive verdict from the framework: the locked-memory single-kilowatt-class envelope is now structurally enforced at the architecture level — there is no flyable-power cell to soften the directive into. Aligns with hyperion latest+17 H6-holds verdict; matrix decision #14 option (b) hold-directive is the recommended ratification on both audit (latest+17) and framework (latest+18) grounds.

### 2026-05-22 latest+16 — project-owner resolution on matrix decision point #14: audit-required

Soften-or-hold of the locked-memory directive on 30 kilowatt-electric Kilopower-extrapolation is deferred pending the explicit reactor-program-credibility audit (R-kilopower-scale-up-credibility, SCOPE'd 2026-05-19 latest+13). Project-owner chose option (iii) — neither accept 30 kilowatt-electric as flyable (option i) nor hold strict single-kilowatt (option ii) — until the audit's H6 verdict lands. Operating envelope for matrix and design-axis purposes stays at the locked-memory directive ("Kilopower-class single-kilowatt fission at best"); titan-3's 40-80 tonne / 30 kilowatt-electric closure cell is held in abeyance, not state-of-record. R-mission-1-demonstrator-then-scale-up remains CONDITIONAL on the audit. Status held at open / high; the resolution is a decision-frame commitment (use the audit), not a numerical change to the axis.
