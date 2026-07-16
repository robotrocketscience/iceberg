# R-bus-mass-anchor-adjudication — STUDY

---

## HEADLINE RETRACTION (2026-05-19 same-day follow-on)

**Project-owner directive 2026-05-19:** "A 500 kilowatt reactor is not going to happen. Stop accounting for it, stop talking about it."

The "6 surviving commercial-strict cells at Europa-Clipper-bus + 10-kilometre-per-second aerocapture credit" headline this round produced (sub-procedure 1) presupposes a 500-kilowatt-electric reactor on the vehicle and is **retracted as fantasy** under the directive. Round artefacts preserved as data; headline cells do not exist in the project-owner's actual power envelope. See `results/closure_verdict.md` "HEADLINE RETRACTION" section for the full scope of what is retracted and what survives. Follow-on round `R-kilowatt-class-power-envelope` re-derives the analysis at 1–10 kilowatt-electric Kilopower-heritage power.

---



**Worker:** titan (re-spawn 3, branch `iceberg-titan-3`, 2026-05-19 latest+12+).
**SCOPE author:** Saturn (orchestrator), commit `c847d36` 2026-05-19.
**Round type:** synthesis / adjudication. No new physics; re-uses existing PRIMARY round artefacts plus closed-form sensitivity perturbations.
**Predecessors (PRIMARY):**
- enceladus-r5 `R-bus-mass-anchor-sweep` (commit `3700de7`, with shielding-sensitivity follow-up `95565cf`).
- phoebe `R-hybrid-aerocapture-aerobraking` (commit `1623cca`).
- phoebe `R-mission-architecture-pivot-survey` (commit `bb570d7`).

---

## Why this round, and why titan

Project-owner decision #14 surfaced at latest+12 integration pass: two PRIMARY findings agree on the bottom line (no realisation path under fully-conservative anchors) but disagree on the *attribution* (enceladus-r5 says bus mass is not the binding axis; phoebe says aerocapture is). Until the matrix carries decoupled axes, the orchestration debt around axis 02 remains, and any later cell-count statement is anchor-conditional in a way the matrix cannot represent cleanly.

This round produces three deliverables:

1. **A basis-of-record bus mass** — the value the matrix carries as default for cross-round comparison. Sensitivity sweeps continue to use brackets; the basis-of-record is what an architecture statement defaults to absent further qualification.
2. **A decoupling of the axis-02 verdict** into (a) bus-mass closure and (b) aerocapture closure, with a separate verdict per axis and an explicit "joint" cell for the intersection.
3. **A single-axis sensitivity sweep on phoebe's R-hybrid-aerocapture-aerobraking** that says, per failure mode, whether phoebe's 0/1920 result is robust by magnitude or has a single-axis flippable anchor. If a single-axis flip exists, the next critical-path round is a full re-run under the flippable anchor.

Titan is the natural worker because the synthesis is broad and rule-based, the prior titan-2 session merged 2026-05-18 cleared the residence-class engineering backlog, and a fresh titan-3 spawn off `c847d36` carries no held-finding entanglement that would bias the synthesis.

---

## Three load-bearing methodology choices (lesson-9 anchor audit)

Per methodology lesson 9 (anchor on PRIMARY-text aggregate verdict, not cherry-picked sub-findings), I name the choices this round inherits and the choices it must correct.

### Choice 1 — adopt enceladus-r5's own honest caveat as the basis-of-record bus mass.

enceladus-r5 §"Caveats — what my bus model omits" lists the components the Cassini-anchor 2 t excludes: radiation shadow shield (1–3 t at 500 kilowatt-electric), high-voltage power-conditioning unit (0.5–2 t), reactor-to-thruster cables and harness (0.5–1 t). enceladus-r5 then states "A more honest 'minimum' bus for a 500-kilowatt-electric ICEBERG vehicle... Total: ~5.5 t, close to Europa Clipper (5.9 t)."

The SCOPE adopts 5.5 t as the basis-of-record H1 anchor. This round does not over-rule the SCOPE; the question H1 tests is whether the value is defensible against an alternative project-owner-stated anchor. Absent project-owner override, 5.5 t stands.

### Choice 2 — re-check aerocapture-credit conditionality on enceladus-r5's 9-cell finding by FILTERING rather than re-running.

enceladus-r5's grid sweeps `aerocapture_credit_kms ∈ {0, 10}` already; the 9-cell headline is the `aero=10` subset. The SCOPE's H4 sub-test ("re-run at aero=0") is mechanically a filter on the existing 1920-cell results.json, not a new physics computation. I treat it as a filter and document the equivalence explicitly. (If the grid had not contained aero=0, this would be a new sweep; it does, so it isn't.)

### Choice 3 — single-axis sensitivity on phoebe is closed-form, not a re-run of phoebe's 1920-cell sweep.

phoebe's STUDY.md tables list the per-altitude pre-registered anchors with closed-form derivations (parabolic-velocity threshold, King-Hele drag impulse, Sutton-Graves heat flux, ε σ T⁴ equilibrium, sublimation rate). Single-axis perturbation can be applied analytically against those anchors. A full 1920-cell re-run would add no information at the same SCOPE per phoebe's own writeup.

### Surfaced for PROTOCOL update queue (candidate methodology lesson 17)

The SCOPE's naming of "ballistic-correction-factor" appears to conflate two distinct phoebe-STUDY parameters: (a) the dimensional ballistic coefficient β = m_total / (Cd × A) used in the King-Hele drag-pass formula, and (b) the boundary-layer-blocking factor (BLBF, value 0.4 in phoebe's sublimation calculation). These are different quantities affecting different failure modes. This round interprets the SCOPE's "ballistic-correction-factor 0.4 → 0.6" as BLBF (matching the numeric value 0.4 in phoebe's text), documents the naming ambiguity, and tests both possible interpretations. Naming-conflation across rounds is candidate methodology lesson 17 (per PROTOCOL update queue; lesson 10 was the atmosphere-model lesson surfaced by phoebe).

---

## Question this round answers (verbatim from SCOPE.md)

**Q1.** What single bus-mass anchor should the matrix carry as basis-of-record?

**Q2.** Of the matrix axes' prior verdicts, which were genuinely bus-mass-anchored and need updating, versus which were aerocapture-anchored and stand under conservative aerocapture?

**Q3.** If aerocapture closure is the binding constraint (not bus mass), what is the deepest possible aerocapture analysis still open? Is any of phoebe's three conservatism choices over-tight enough that a single-axis relaxation flips the 0/1920 verdict?

---

## Pre-registered hypotheses (central anchor computed BEFORE range, per methodology lesson 1)

Central numerical anchors derived first; ranges wrap each anchor. Each hypothesis carries a falsification band identical to SCOPE.md.

### Central anchors (computed before range bands)

**H1 anchor.** Adopt Europa-Clipper-with-shielding 5.5 t as basis-of-record bus mass. Derivation: enceladus-r5 caveat §99–104 sums 2 (base) + 2 (shadow shield at 500 kilowatt-electric × 4 kg/kilowatt-electric medium-conservatism) + 1 (power-conditioning unit) + 0.5 (cables/harness) = 5.5 t. Brackets: 2 t (Cassini, no shielding — upside) and 15 t (predecessor stale anchor — far-conservative). 5.9 t Europa-Clipper-flown is within the bracket.

**H2 anchor.** Heritage-bus + aerocapture = 9 cells (enceladus-r5 measured). At Europa-Clipper-with-shielding bus + linear bag + aerocapture credit 10 km/s, enceladus-r5's own shielding sensitivity §137–143 reports 6 of 9 surviving at medium shield. Anchor: 6 surviving cells at 5.5 t. Predicted range [5, 9] inherits SCOPE.md.

**H3 anchor.** Of phoebe's 31 candidates, bus-mass-anchored kill criteria are F1 (inbound Δv closure) and F3 (L0-05 round-trip). F2 (B-ring crossing) is geometric. F4/F7 are foundational-lever. F5 (Saturn-side process power) is independent. F6 (reactor program) is independent. F8 (capital class) is independent. Walking phoebe's per-candidate kill table at heritage bus: bus-mass reduction 15 t → 5.5 t reduces vehicle dry mass by ~9.5 t out of dry mass 70–150 t (reactor dominates dry mass at 500 kilowatt-electric / 5–10 watts-per-kilogram). Δv-budget effect is order 7–13%, far below the 4–6× overshoot F1 sees in continuous-thrust accounting. Predicted: **0 candidates re-classify** under heritage bus alone. SCOPE predicted 2–7; H3 anchor is more pessimistic.

**H4 anchor.** Filter enceladus-r5 1920-cell results at (m_bus, bag_scaling, aerocapture_credit_kms) = (2, linear, 0). At parabolic-threshold-equivalent zero aerocapture, no cell closes commercial+strict because the residual Δv (25 km/s continuous-thrust mid-point) overshoots Tsiolkovsky propellant-fraction limit at 200-tonne chunk × 19.6 kilometre-per-second exhaust velocity. Anchor: **0 cells** at all bus masses ∈ {2, 5, 10, 15} t. Predicted range [0, 0]. SCOPE predicted 0 at Cassini only; my anchor extends to all bus masses.

**H5 anchor — three sub-claims.**

*H5-a (ice tensile 1.0 → 2.0 MPa).* phoebe's pass-1 chunk-shatter at chunk 200 tonnes, periapsis 40 km gives stress 1.3 megapascals vs tensile 1.0 megapascals (margin 0.77×). Relaxing tensile to 2.0 megapascals: margin = 2.0 / 1.3 = 1.54× ≥ 1.0 → structural leg flips. **Anchor: H5-a falsified at 2.0 megapascals**. SCOPE predicted leg robust; my anchor predicts it is the single flippable leg.

*H5-b (boundary-layer-blocking factor 0.4 → 0.6 — interpretation 1: sublimation rate).* phoebe sublimation at 130 km is 1505 t (chunk consumed 7.5× over for 200 t initial). Relaxation 0.4 → 0.6 reduces sublimation by factor (1 − 0.6) / (1 − 0.4) = 0.667. Reduced sublimation: 1003 t. Still ≥ 100 t threshold by an order of magnitude. **Leg does not flip.** *Interpretation 2 (King-Hele drag-coefficient correction 0.4 → 0.6 applied to aerobraking timescale).* Δv-per-pass × 1.5, pass count / 1.5, timescale at 130 km drops 69 yr → 46 yr. Still > 5 yr budget. **Leg does not flip.** Under either reading, H5-b held.

*H5-c (atmosphere density × {1, 2, 3} at aerobraking altitudes 130–200 km).* Density × 3 at 130 km: drag Δv-per-pass × 3 → pass count / 3 → timescale 69 yr / 3 = 23 yr. Still > 5 yr. Sublimation per pass × 3 (heat flux scales with ρ) and pass count / 3 → total sublimation unchanged in leading order (ρ × passes × per-pass-rate). Chunk temperature T_eq scales as ρ^0.25; density × 3 → T_eq × 1.32 = 928 K, worse not better. **Leg does not flip.** SCOPE predicted leg robust; anchor confirms.

**H5 aggregate anchor.** One of three legs single-axis flippable (structural at higher ice tensile). The architecture closure is *conjunctive* across the three legs (all must clear), so a single-leg flip does NOT close the architecture. Phoebe's 0/1920 verdict is robust-by-magnitude on legs (b) and (c); robust-by-cancellation on leg (a) only in the sense that the binding axes shift but the architecture-level verdict does not.

**H6 anchor.** Decoupled-axis basis-of-record:
- Bus-mass axis: 5.5 t basis-of-record; brackets [2, 15] t.
- Aerocapture axis: phoebe 0/1920 stands at conservative anchors; ice tensile single-axis-relaxable to 2.0 megapascals flips structural leg only; aggregate verdict (conjunctive) unchanged.
- Joint verdict at (5.5 t, closed aerocapture): 0 surviving cells.
- Joint verdict at (5.5 t, aerocapture credit 10 km/s): 6 surviving cells per enceladus-r5 shielding sensitivity.
- Joint verdict at (Cassini 2 t, closed aerocapture): 0 surviving cells (H4-extended).
- Joint verdict at (Cassini 2 t, aerocapture credit 10 km/s): 9 surviving cells (enceladus-r5 headline).

The 9-cell vs 0-cell delta is entirely on the aerocapture axis. Bus mass moves the count by ~3 cells at fixed aerocapture; aerocapture moves the count by 9 cells at fixed bus.

### Hypothesis verdict ranges (inheriting SCOPE.md)

| # | Hypothesis | Predicted (anchor) | Predicted (range) | Falsification |
|---|---|---|---|---|
| **H1** | Europa-Clipper-with-shielding 5.5 t is basis-of-record bus mass | adopt 5.5 t | (binary) | project-owner override OR shielding sensitivity over-tight |
| **H2** | At 5.5 t bus + aerocapture 10 km/s, 5–9 commercial-strict cells | 6 cells | [5, 9] | < 5 (shielding more conservative) OR > 9 (sensitivity over-tight) |
| **H3** | 2–7 phoebe-pivot-survey candidates re-classify DEAD→DEEP-DIVE at heritage bus | **0** (more pessimistic) | [0, 1] | > 1 candidate re-classifies (bus mass more load-bearing on phoebe's criteria than I think) |
| **H4** | 0 commercial-strict cells at aero=0 (Cassini bus) | 0 (at all bus masses) | [0, 0] | ≥ 1 cell closes commercial+strict at any (bus, aero=0) corner |
| **H5-a** | Ice tensile 1.0 → 2.0 MPa: structural leg flips | margin 1.54× | flips | does not flip (anchor mis-computed) |
| **H5-b** | BLBF 0.4 → 0.6: no leg flips | sublimation 1003 t; timescale 46 yr | no flip | any leg flips |
| **H5-c** | Atmosphere density × 3: no leg flips | timescale 23 yr; T_eq 928 K | no flip | any leg flips |
| **H5-agg** | One single-axis flippable leg, aggregate verdict unchanged | 1 leg flips of 3; architecture conjunctive | 0–1 legs flip | ≥ 2 legs flip (architecture closure plausibly recoverable) |
| **H6** | Bus and aerocapture axes are separately load-bearing; matrix carries both | bus moves count by ~3 cells; aerocapture by 9 cells at heritage bus | decoupled | strongly coupled (e.g., shielding mass scales with aerocapture peak-q) |

---

## Method

`run.py` implements three sub-procedures, each operating on existing PRIMARY-round artefacts:

### Sub-procedure 1 — bus-mass × aerocapture filter on enceladus-r5

Load `water-prop/rounds/R_bus_mass_anchor_sweep/results/results.json`. Construct a 4-bus × 2-aerocapture closure table (commercial+strict pass count under linear bag scaling, marginalising over the remaining axes). Tests H1, H2, H4. Produces `results/bus_aero_table.md`.

### Sub-procedure 2 — phoebe pivot-survey re-classification at heritage bus

Load `water-prop/rounds/R_mission_architecture_pivot_survey/results/R_mission_architecture_pivot_survey.json`. For each of the 31 candidates, identify which kill criteria were bus-mass-anchored (F1, F3) versus bus-mass-independent (F2, F4, F5, F6, F7, F8). For each candidate, apply heritage-bus reduction (15 t → 5.5 t = −9.5 t out of dry mass 70–150 t = 7–13% lighter): if bus-mass-anchored criteria are the ONLY physics kills AND the kill margin is ≤ 13%, mark "would re-classify"; else "still DEAD". Tests H3. Produces `results/pivot_survey_reclassification.md`.

The 13% margin threshold is generous to the H3 hypothesis: F1 kills phoebe-flagged candidates by 4–6× (continuous-thrust 24.7–40.2 km/s vs impulsive-equivalent threshold 6.42 km/s), which is far beyond 13% recovery. F3 kills are typically driven by cruise-time physics (R9_slow_trajectory_tof, R_cruise_time_optimization), not by bus mass. Pre-registration is the more pessimistic side.

### Sub-procedure 3 — single-axis sensitivity on phoebe's aerocapture-aerobraking

Three closed-form perturbations of phoebe's STUDY.md anchors:

(a) **Ice tensile 1.0 → 1.5 → 2.0 MPa.** Phoebe's anchor at chunk 200 t / periapsis 40 km: peak g ~40, chunk radius 3.73 m, ρ_ice 917 kg/m³, stress = r × ρ_ice × g_peak × g_earth = 1.34 MPa. Margin = tensile / stress. Test: margin ≥ 1.0 → leg flips.

(b) **Boundary-layer-blocking factor 0.4 → 0.5 → 0.6** under interpretation 1 (sublimation rate). Sublimation scales as (1 − BLBF). 130-km anchor 1505 t × (1 − BLBF) / (1 − 0.4). Test: total sublimation ≤ 100 t → leg flips.

(c) **Atmosphere density × {1, 2, 3}.** Three regimes:
   - Aerobraking timescale at 130 km. Phoebe anchor: 303k passes × 2 hr / pass = 69 yr at density × 1. ρ × n → drag-pass-Δv × n → pass count / n → timescale / n. Test: timescale ≤ 5 yr → leg flips.
   - Sublimation total at 130 km. Heat-per-pass × ρ; pass count / ρ; total sublimation invariant in leading order (constant at 1505 t under proportional heat flux). Refined: per-pass T_eq × ρ^0.25 raises sublimation rate as exp(−ΔH/RT), super-linear in T → density × 3 produces *worse* sublimation. Test directional only.
   - Chunk equilibrium temperature at 130 km. T_eq = (q / (ε σ))^0.25; q ∝ ρ × v³. T_eq × ρ^0.25. Phoebe anchor 702 K at density × 1 → 925 K at density × 3.

Aggregate H5 verdict.

### Cross-check audit

Hand-recompute phoebe's anchor at chunk 200 t / periapsis 40 km using the closed-form formulas, confirm agreement with phoebe's STUDY tables within ±10%. Hand-recompute enceladus-r5's best-cell (500 kilowatt-electric / 200 t / sp=10 / aero=10 / Isp=2934 / Cassini bus) to confirm 91.5 t delivered (already audited at the bottom of enceladus-r5's STUDY.md but worth re-verifying as fresh-eyes lesson 9).

---

## Out-of-scope (per SCOPE.md, restated for clarity)

- New physics on Architecture E surviving cells (this round determines bus-mass attribution, not validates cells).
- Full re-run of phoebe's hybrid round under joint-axis relaxation (single-axis only here; if H5 surfaces a flippable axis, that's the next SCOPE).
- L0-24 reactor-program-availability gate (iapetus settled).
- Pricing-anchor (R-pricing-anchor-revisit covers).
- Joint-axis relaxation of all three of (ice tensile + BLBF + atmosphere). Flagged for follow-on if H5 single-axis flip is itself bound only by the joint.

---

## Methodology lesson dependencies

- **Lesson 1** (pessimistic-prediction default): H1 picks 5.5 t basis-of-record (mid-conservatism) not 2 t; H3 anchor 0 candidates is more pessimistic than SCOPE's 2–7.
- **Lesson 7** (compute under most pessimistic credible anchor first): 5.5 t + closed aerocapture is the matrix's pessimistic anchor reading; heritage-bus + open-aerocapture is the upside-only reading.
- **Lesson 9** (anchor on PRIMARY-text aggregate verdict): three PRIMARY rounds cited verbatim above; per-round verdicts identified before this round's own predictions written.
- **Lesson 11** (robustness-by-magnitude vs robustness-by-cancellation): H5 explicitly tests both modes. Anchor: legs (b) and (c) robust-by-magnitude; leg (a) is single-axis flippable but architecture-level verdict robust-by-conjunction.
- **Lesson 13** (robust-to-single-axis vs robust-to-joint-axis): H5 is single-axis only. Flagged in out-of-scope.
- **Candidate lesson 14** (conditional-axis stripping discipline): enceladus-r5's 9-cells inherit the 10 km/s aerocapture credit as a charitable conditional. H4-extended (all bus masses at aero=0) strips that conditional cleanly.
- **Candidate lesson 17** (naming-conflation across rounds): SCOPE's "ballistic-correction-factor" vs phoebe's BLBF / β. Documented in Choice-3 above. PROTOCOL update flagged.

---

## Files of record

```
water-prop/rounds/R_bus_mass_anchor_adjudication/STUDY.md                  (this file — pre-registration)
water-prop/rounds/R_bus_mass_anchor_adjudication/run.py                    (three sub-procedures)
water-prop/rounds/R_bus_mass_anchor_adjudication/results/bus_aero_table.md
water-prop/rounds/R_bus_mass_anchor_adjudication/results/pivot_survey_reclassification.md
water-prop/rounds/R_bus_mass_anchor_adjudication/results/aerocapture_sensitivity.md
water-prop/rounds/R_bus_mass_anchor_adjudication/results/closure_verdict.md
water-prop/rounds/R_bus_mass_anchor_adjudication/results/results.json
```

Results section appended after run.py executes.

---

## Result

`run.py` executes in <1 second. Audit cross-check passes (phoebe stress recompute 1.342 MPa vs published 1.340 MPa, 0.15% error; enceladus-r5 best-cell delivered recompute 91.53 t vs published 91.5 t, 0.03% error).

| metric | predicted (anchor) | predicted (range) | measured | held? |
|---|---|---|---|---|
| H1 — basis-of-record bus mass | 5.5 t | (binary) | 5.5 t adopted; brackets [2, 15] | **ADOPTED** |
| H2 — commercial-strict cells at 5.5-t-proxy + aero=10 | 6 | [5, 9] | 6 (at m_bus = 5 t grid-nearest); 6 also at m_bus = 10 t; 4 at m_bus = 15 t | **HELD** (exact anchor) |
| H3 — pivot-survey re-classifications at heritage bus | 0 (vs SCOPE 2–7) | [0, 1] | 0 of 31 | **HELD-strong**; SCOPE FALSIFIED-low |
| H4 — commercial-strict at aero=0, any bus | 0 (all four) | [0, 0] | 0 at {2, 5, 10, 15} t | **HELD-strong** (extends SCOPE Cassini-only prediction) |
| H5-a — ice tensile 1.0 → 2.0 MPa flips structural | flips | flips | flips at 1.5 MPa (margin 1.12×); definitively at 2.0 MPa (margin 1.49×) | **FALSIFIED at 1.5 MPa+** (single-axis flippable as anchor predicted) |
| H5-b — BLBF / drag K-factor 0.4 → 0.6 flips no leg | no flip | no flip | sublimation 1003 t > 100 t; timescale 46 yr > 5 yr | **HELD** |
| H5-c — atmosphere density × 3 flips no leg | no flip | no flip | timescale 23 yr > 5 yr; T_eq 925 K (worse) | **HELD** |
| H5-agg — single-axis-flippable legs: 0–1; architecture robust-by-conjunction | 1 of 3 flips; closure conjunctive | [0, 1] | 1 of 3 flips; architecture closure unchanged | **HELD** |
| H6 — bus and aerocapture separately load-bearing | decoupled; bus 0–9, aerocapture 0–9 | decoupled | bus axis contributes 0–9 cells at fixed aerocapture; aerocapture axis contributes 0–9 at fixed bus | **HELD** |

**Score: 8 of 9 hypotheses HELD; H5-a FALSIFIED as anchor predicted (single-axis flippable, useful information).**

Detailed sub-procedure tables in:
- `results/bus_aero_table.md` (H1, H2, H4)
- `results/pivot_survey_reclassification.md` (H3)
- `results/aerocapture_sensitivity.md` (H5-a, H5-b, H5-c)
- `results/closure_verdict.md` (aggregate + matrix amendments)
- `results/results.json` (machine-readable)

---

## Reading

**The matrix's basis-of-record bus mass is 5.5 t (Europa-Clipper-with-medium-shielding), with brackets [2 t Cassini, 15 t predecessor-stale] retained for sensitivity sweeps.** enceladus-r5's own honest caveat is adopted verbatim; no project-owner direction has overridden. Cell statements at Cassini 2 t are upside-only readings; cell statements at 15 t are far-conservative readings of a stale anchor.

**The axis-02 'architectural search space exhausted at worker-round level' reading from latest+11 is bus-mass-independent and stands.** Phoebe's 31-of-31 DEAD pivot-survey carries through cleanly to heritage bus because phoebe's kill criteria (F2 ring crossing, F4/F7 foundational lever, F5 Saturn-side process power, F6 reactor program, F8 capital class) are bus-mass-independent, and the two bus-anchored criteria (F1 continuous-thrust inbound Δv, F3 round-trip closure) bind by 4–6× and ~50% respectively — far beyond the ~13% recovery from a 15 t → 5.5 t bus reduction.

**The 9-cell vs 0-cell delta in enceladus-r5's bus-mass sweep is entirely aerocapture-driven, not bus-mass-driven.** At fixed aerocapture credit = 0, every bus mass gives 0 cells. At fixed aerocapture credit = 10 km/s, bus mass moves the count 0 → 9. The 'no engineering-closed cell' verdict was right on the bottom line and wrong on attribution; the binding axis is aerocapture, not bus mass.

**Phoebe's R-hybrid-aerocapture-aerobraking 0/1920 verdict is robust by conjunction.** Single-axis relaxation of ice tensile from 1.0 MPa to 2.0 MPa (within phoebe's own 'laboratory-ice envelope') flips the pass-1 chunk-shatter structural leg, but the aerobraking-timescale and sublimation legs both remain bound by orders of magnitude under any single-axis relaxation tested (BLBF 0.4 → 0.7, K-factor 1.0 → 1.5, atmosphere density × 3). The architecture closure is conjunctive: all three legs must clear. A joint-axis relaxation across all three is the deeper-question follow-on, not addressed here.

---

## Revisit (mandatory)

All nine hypotheses graded against measured outputs above. Aggregate: 8 HELD, 1 FALSIFIED as anchor predicted (H5-a single-axis flippable). The one falsification is informative, not surprising: my pre-registered central anchor predicted H5-a would flip, and it did. The SCOPE's broader H5 prediction ('phoebe's 0/1920 verdict is robust to the three most conservative anchors phoebe used') is HELD at the *architecture-closure* level (conjunctive across legs) but FALSIFIED at the *individual-leg* level (structural leg flippable). The distinction matters because a follow-on round targeting only H5-a would not reopen the architecture.

The SCOPE's H3 prediction (2–7 candidates re-classify at heritage bus) was wrong on direction. My pre-registered anchor 0 (more pessimistic) was correct. This is the 13th aerocapture-adjacent / matrix-adjudication round where methodology lesson 1 (pessimistic-default holds) was the right call relative to the SCOPE-author's more-optimistic anchor; lesson 1 base rate continues to reinforce.

---

## Cross-learning

**Positive for the matrix (axis 02 amendment):** decouple into 02-bus-mass and 02-aerocapture-closure; carry the basis-of-record bus mass (5.5 t) as a top-line parameter; flag aerocapture as the binding axis. The 'no engineering-closed cell' verdict survives at conservative anchors; cell-count statements at heritage anchors should specify both axes explicitly.

**Negative for any follow-on round targeting only H5-a:** structural-leg single-axis flippability does NOT reopen the architecture by itself. A round that just relaxes ice tensile would discover the timescale leg becomes the new binding constraint at 130 km (69 yr) and the sublimation leg becomes binding at 110 km (445 t total loss). The architectural recovery requires a joint-axis relaxation across all three legs simultaneously, which exceeds any single-leg refinement.

**Methodology lesson surfaced for PROTOCOL update queue:** candidate methodology lesson 17 — naming-conflation across rounds. SCOPE's 'ballistic-correction-factor' conflated phoebe's 'boundary-layer-blocking factor' (sublimation-rate factor 0.4) with 'ballistic coefficient' β (6022 kg/m² drag coefficient). This round tested both interpretations; verdict robust under either. The naming-conflation pattern likely recurs across rounds; PROTOCOL should flag a candidate convention: "any parameter referenced across rounds must cite the source round's STUDY.md variable name and units verbatim, not a paraphrase."

**Reference for next round candidates (project-owner direction required):**
- R-hybrid-aerocapture-joint-axis-sensitivity (highest-priority follow-on if H5-a flippability is read as actionable; joint relaxation of {ice tensile, BLBF, atmosphere density} at the credible-upper-bound).
- R-pricing-anchor-revisit (separate Open SCOPE; cross-orthogonal to this round).
- Pivot-survey probabilistic-F6 re-run (separate axis; iapetus settlement is the load-bearing programme-level reading).

