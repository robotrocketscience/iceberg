# R-chunk-as-heat-shield-revisit — does any (chunk-mass, entry-velocity) configuration close chunk-as-heat-shield AND intersect a surviving variant cell?

**Worker:** phoebe (resumed session, 2026-05-15 latest+).
**Status:** pre-result. Hypotheses pre-registered with central back-of-envelope estimates computed BEFORE range bands, per Methodology lesson 1 (pessimistic-default holds) and the recurring lesson on anchor-from-primary-text.

---

## Why this is a reframe of Saturn's SCOPE.md

Saturn's `SCOPE.md` (orchestrator, 2026-05-15) was written before hyperion's `R-aerocapture-fast-cruise-envelope` (commit `203d351`) ran. That round established two findings the SCOPE could not have anticipated:

1. **Single-pass aerocapture FAILS structurally at the Round F STRICT-closing Variant C cell** (200-tonne chunk + 63.8-tonne tug, 15.29 kilometres-per-second entry, periapsis solver hit 40-kilometre floor, peak 47.9 g, chunk internal stress 1.6 megapascals exceeds ice tensile 1.0 megapascals — chunk shatters).
2. **Saturn's SCOPE.md cherry-picked the "chunk thermodynamically viable" sub-finding from the original R-chunk-as-heat-shield while omitting that round's *aggregate* verdict was FALSIFIED** (multi-pass aerobraking unworkable; ballistic coefficient too high).

Saturn's SCOPE asked "can the chunk be passively oriented through a 200-second pulse?" — but at the architecturally-relevant chunk masses, hyperion's round shows the chunk *shatters* before orientation matters. The orientation question is downstream of an unaddressed earlier question that hyperion answered for ONE corner of the envelope (Round-F STRICT) and the original R-chunk-as-heat-shield answered for ANOTHER corner (100-tonne / 12.6 kilometres-per-second / lunar-gravity-assist). The space between is unmapped.

This round scans that unmapped envelope and tests whether any closing region exists AND whether any closing region intersects an architecturally-relevant surviving variant cell.

---

## Question this round answers

For chunk masses in the (25, 500) tonne range and Earth-arrival velocity-at-infinity in the (3, 11) kilometres-per-second range — the architecturally-relevant envelope of all current ICEBERG variants:

1. **What region of (chunk-mass, entry-velocity) space simultaneously satisfies bag-thermal-survival, chunk-structural-survival, chunk-thermal-survival, AND single-pass-capture-feasibility?** (STRICT-closing region)
2. **What region satisfies the relaxed sacrificial-bag closure (chunk-structural + chunk-thermal + capture-feasible only)?** (SACRIFICIAL-BAG closing region)
3. **Does either closing region intersect any surviving variant cell?** Variant B (chunk 200 tonnes per phoebe's R-variant-B-100t-resizing finding that L1-007 binds Variant A propellant-feasibility), Variant C (chunk 200 tonnes at the Round-F STRICT cell), Architecture-D (chunk size open, but L0-05 round-trip ≤ 15 years binds).
4. **For the matrix's aerocapture-conditional rows: does this round close the conditional, falsify it, or refine it to a narrower envelope?**

---

## Pre-registered hypothesis (H-csa)

### Recurring-lesson-#N anchor — central estimates COMPUTED BEFORE range

Per the now-twice-confirmed methodology intervention, central numerical anchors derived first (back-of-envelope, in conversation, before range bands written). Range bands wrap each anchor.

**Back-of-envelope anchors (computed first):**

| Quantity | Anchor (computed BEFORE range) | Source |
|---|---|---|
| Bag thermal-survival peak heat flux | 1.1 watts-per-square-centimetre | Stefan-Boltzmann at 700 K bag limit, emissivity 0.8 |
| Chunk thermal-survival ablation per pass | 5 percent | "Delivered-fraction-degrading" threshold from R-chunk-as-heat-shield section §"Three observations" |
| Chunk structural-survival peak g-load (100-tonne chunk) | 37.6 g | tensile_strength / (density × radius) for r=2.96 m |
| Chunk structural-survival peak g-load (200-tonne chunk) | 29.8 g | r=3.74 m |
| Chunk structural-survival peak g-load (50-tonne chunk) | 47.4 g | r=2.35 m |
| Capture-feasibility periapsis floor | 50 kilometres | hyperion's 40-km solver floor + 10 km margin |
| Original R-chunk-as-heat-shield case anchor (100 t, v_e=12.6, LGA) peak g | 6.3 g | (12.6−7.67) × 1000 / 200 × 2.5 / 9.81 |
| Original R-chunk-as-heat-shield case structural margin | 6.0× | 1000 / (917 × 2.96 × 6.3 × 9.81 / 1000) |
| Hyperion Round-F STRICT case (200 t, v_e=15.29, no-LGA) measured tensile margin | 0.62× | hyperion's `R_aerocapture_fast_cruise_envelope.json` |
| β = chunk-mass^(1/3) scaling | β(25 t) = 0.63 × β(100 t) | volumetric scaling for sphere; smaller chunk → lower β → easier capture |

The structural-survival g-load decreases with chunk mass (large chunks shatter easier). The original R-chunk-as-heat-shield case sits at ~6 g loading, comfortable margin. Hyperion's Round-F STRICT case sits at 47.9 g loading, structural failure. The structural-pass region is therefore expected to be a **band bounded above in chunk mass and entry velocity simultaneously** — both axes degrade structural margin.

The bag-thermal pass region is much narrower. R-chunk-as-heat-shield's table shows bag survives ONLY at periapsis ≥ 180 kilometres, where pass count is ~2 million — intractable. Bag-thermal survival is essentially empty for any single-pass-capture configuration; the SACRIFICIAL-BAG framing is the only possible relaxation.

### Sub-claim ranges (anchored to central estimates)

| Sub-claim | Central anchor | Predicted range (sub-claim H-csa-N) | Falsification threshold |
|---|---|---|---|
| H-csa-a — STRICT closing region (bag-retained) area | empty | 0–2 cells of 40-cell sweep | > 2 cells = falsified |
| H-csa-b-bound — SACRIFICIAL-BAG closing region upper bound on chunk | chunk ≤ 100 t | 75–150 t upper bound | upper bound > 200 t = falsified (re-opens Variant C) |
| H-csa-b-vinf — SACRIFICIAL-BAG closing region upper bound on velocity-at-infinity | v_∞ ≤ 6 km/s | 5–8 km/s upper bound | upper bound > 8 km/s = falsified |
| H-csa-c — Variant C intersection (chunk = 200 t, v_∞ ≈ 8.55 with lunar-gravity-assist) closes engineering envelope | no intersection | binary | intersection holds = Variant C engineering-conditional restored |
| H-csa-d — Variant B intersection (chunk = 200 t, v_∞ such that round-trip ≤ 15 yr) closes engineering envelope | no intersection | binary | intersection holds = Variant B has an aerocapture rescue |
| H-csa-e — small-chunk multi-mission alternative: at chunk = 50 t engineering closes; total delivered mass needed (≥ 200 t / mission window) requires ≥ 4 missions per window | feasibility check only — qualitative | binary | flagged for follow-on round on cadence |
| H-csa-f — chunk-as-heat-shield orientation-stability is gradable | not gradable (antecedent false: no architecturally-relevant closing region) | gradable iff H-csa-c or H-csa-d falsified | conditional |

### Aggregate (H-csa-agg)

Chunk-as-heat-shield has no closing configuration that simultaneously satisfies the aerocapture engineering envelope AND intersects any surviving variant cell at chunk ≥ 100 tonnes. The matrix's aerocapture-conditional surviving cells (Variant C and the year-twenty-plus megawatt all-electric end-to-end winner cell) should be classified "engineering-falsified" rather than "engineering-pending". Phoebe's prior R-variant-B-100t-resizing finding (path 3 of the bake-off structurally unavailable) combines with this round to retire BOTH amendment paths to Variant B; only Variant C at the original Round-F closing cell could plausibly survive, and hyperion's R-aerocapture-fast-cruise-envelope already showed it does not.

If H-csa-agg holds, the matrix's surviving-cell list collapses to (a) Variant A under acknowledged-collapse path 2 of the bake-off, (b) Architecture-E (no Saturn-side electrolysis, requires ≥ 25-year L0-05 waiver per enceladus-r5 round 6).

If H-csa-agg is falsified — particularly via H-csa-c or H-csa-d intersection — Variant C or Variant B has a surviving aerocapture-conditional cell at narrower-than-original-SCOPE bounds. The matrix update is then a refinement, not a retirement.

### Recurring-lesson watchpoints

1. **Methodology lesson 1 anchor:** the prior aerocapture rounds (R-aerocapture, R-chunk-as-heat-shield, R-aerocapture-fast-cruise-envelope) have all come back more pessimistic than their pre-registration. This round pre-registers a strongly pessimistic position consistent with that pattern. If H-csa-agg is falsified less-pessimistically (closing region exists), the lesson updates: at the campaign's 12th aerocapture-adjacent round, the pessimistic-default has finally over-corrected.
2. **Methodology lesson 5 — domain-bias check:** physics rounds in this campaign have been pessimistically pre-registered with corrections coming back less-pessimistic-than-predicted (R-radiator, R-silicate, R-electric-outbound, R-bag-capture-revisit). Reliability rounds have been optimistically pre-registered (R-mission-success-probability). Aerocapture rounds have been pessimistically pre-registered AND come back even more pessimistic. The domain bias for aerocapture is not "scientist-optimistic" but "engineer-pessimistic insufficient" — pre-register MORE pessimistically than first instinct.

---

## Method

Deterministic single-pass aerocapture envelope check across a (chunk-mass, velocity-at-infinity) grid. Uses hyperion's `R_aerocapture_fast_cruise_envelope/run.py` physics functions verbatim (sphere geometry, exponential atmosphere, Sutton-Graves stagnation-point heat flux, periapsis solver, peak-g empirical-factor model) — re-importing not copy-pasting. Sweep axes broader than hyperion's (which fixed Round-F transfers as the v_perihelion source).

### Sweep axes

- **chunk_t** ∈ {25, 50, 75, 100, 150, 200, 300, 500} tonnes (8 values; spans below L1-007 to above B-ring single-chunk physical cap)
- **v_∞_km_s** ∈ {3, 5, 7, 9, 11} kilometres-per-second (5 values; spans very-slow lunar-gravity-assist + slow-cruise to no-LGA fast-cruise)
- **tug_t** = 30 (Variant B 500 kWe MARVL approximate). Sensitivity check at tug_t = 63.8 (Round F 500 kWe value) for the Variant C intersection cells only.

40-cell base sweep + 8-cell sensitivity. Sub-second wall clock.

### Per-cell computations (unchanged from hyperion's verified solver)

1. v_e = sqrt(v_∞² + v_escape_at_interface²)
2. β = (chunk_t + tug_t) × 1000 / (π × r_chunk²); r_chunk = sphere-equivalent radius from chunk mass and ice density
3. periapsis_alt, pulse_duration = required_periapsis_altitude_km(v_e, β, target_dv = v_e − v_circular_LEO)
4. q_peak = Sutton-Graves(v_e, periapsis, r_chunk)
5. ablation_pct = total_heat_load / heat_of_vaporization / chunk_mass
6. peak_g = 2.5 × (v_e − v_circular_LEO) / pulse_duration / 9.80665
7. tensile_margin = ice_tensile_strength / (r_chunk × ice_density × peak_g × 9.80665)

### Closure flags

- **bag_thermal_survives** = q_peak ≤ 1.1 watts-per-square-centimetre
- **chunk_structural_survives** = tensile_margin ≥ 1.0
- **chunk_thermal_survives** = ablation_pct ≤ 5.0
- **capture_feasible** = periapsis_alt ≥ 50 (above hyperion's 40 km solver floor)
- **STRICT_pass** = all four flags true
- **SACRIFICIAL_BAG_pass** = (chunk_structural_survives AND chunk_thermal_survives AND capture_feasible)

### Variant intersection tests

- **Variant C intersection cell:** (chunk_t=200, v_∞=8.55, tug_t=63.8) — replicates hyperion's Round-F STRICT closing case. Should reproduce hyperion's "envelope_pass = False" exactly (cross-check).
- **Variant B intersection band:** sweep v_∞ ∈ {5, 6, 7, 8} at chunk_t=200, tug_t=30. Identify whether any intersection passes engineering AND is plausibly compatible with L0-05 (qualitative — a fuller round-trip-time integration is out of scope).
- **R-chunk-as-heat-shield original case cross-check:** (chunk_t=100, v_∞=1.5, tug_t=30) — approximates the round's 12.6 kilometres-per-second entry (sqrt(1.5² + 11.07²) ≈ 11.17, off from hyperion's 12.65 because hyperion used a different lunar-gravity-assist convention; will note discrepancy).

### Outputs

- `results/R_chunk_as_heat_shield_revisit.json` — full per-cell results.
- `results/tables.md` — sweep tables, closing-region maps, hypothesis grading.
- This round's reading section (in STUDY.md, post-run) — written after grading.

---

## Validity caveats

Inherited from hyperion (acknowledged):
1. Sutton-Graves stagnation-point only; off-axis heat distribution attenuates total chunk heating (this round uses peak-only, conservative upper bound).
2. Drag coefficient 1.0 for irregular chunks is approximate (true value 0.6–1.4 depending on shape and orientation).
3. Single-pass aerocapture only; multi-pass hybrid is qualitative scoping, not full integration.
4. Tug-survival assumed conditional on chunk-forward orientation (orientation question is conditional sub-claim H-csa-f, only gradable if architecturally-relevant closing region exists).
5. Exponential atmosphere with single scale height; periapsis altitude estimate has roughly ±5 kilometres error.

Phoebe-specific:
6. **Bag thermal-survival threshold of 1.1 W/cm²** is anchored on Stefan-Boltzmann radiative equilibrium at 700 K (polyimide laminate failure) with emissivity 0.8. Real bag heating includes conductive + radiative components and depends on bag stowage geometry; the 1.1 number is an upper bound on "bag survives". If bag is held in shadow behind chunk (as the chunk-as-heat-shield architecture requires), conductive heating from the chunk itself may dominate bag failure — not modelled here. Effect: bag-thermal-survival is at-best optimistic; closing region narrower than this round will show.
7. **Tug mass dependence on chunk mass** simplified to constant tug across the sweep. In reality, smaller chunk = smaller propellant mass = smaller tug → β decreases more sharply for small chunks than this round shows. Effect: small-chunk closing region slightly larger than this round will show.
8. **Round-trip-time check is qualitative.** A small-chunk closing region may fail Variant B's L0-05 round-trip if multiple missions are needed per launch window. The model does not iterate on cadence vs L0-05; if such intersection is found, a follow-on round (R-multi-chunk-cadence?) would be needed.
9. **Locked-belief #4 (radiator mass) is upstream:** the tug masses used here are anchored on 500 kWe MARVL-decomposed ≈ 30 t (Variant B) or ≈ 64 t (Variant C with extra propellant). The 40 W/kg target row of the matrix sits at ≈ 25 t / megawatt — this round does not test megawatt-class chunk-as-heat-shield directly because no tested cell sits at megawatt with chunk ≥ 100 t (would require chunk mass + tug + propellant of order 1500 t, well outside any current launcher).

---

## Test

`run.py`. Deterministic. Sub-second wall clock. Imports from hyperion's run.py (no copy-paste of physics).

---

## Result

**STRICT closing region (bag-retained):** 0 of 40 cells. Empty across the entire (chunk 25–500 t × v_∞ 3–11 km/s) cube at Variant B tug mass.

**SACRIFICIAL_BAG closing region (bag sacrificed):** 0 of 40 cells. Also empty.

**All architectural intersection cells fail SACR-BAG:**

| Intersection | chunk (t) | v_∞ (km/s) | tug (t) | periapsis (km) | peak g | margin × | SACR-BAG |
|---|---:|---:|---:|---:|---:|---:|:---:|
| Variant_C_RoundF_no_LGA | 200 | 10.55 | 63.8 | 40 (floor) | 47.9 | 0.62 | N |
| Variant_C_RoundF_with_LGA | 200 | 8.55 | 63.8 | 40 (floor) | 36.3 | 0.82 | N |
| Variant_B_chunk200_low_vinf | 200 | 5.00 | 30.0 | 40 (floor) | 22.4 | 1.33 | N |
| Variant_B_chunk200_mid_vinf | 200 | 7.00 | 30.0 | 40 (floor) | 29.2 | 1.02 | N |
| Variant_B_chunk200_no_LGA | 200 | 8.55 | 30.0 | 40 (floor) | 36.3 | 0.82 | N |
| RCAHS_original_anchor | 100 | 1.50 | 30.0 | 40 (floor) | 16.1 | 2.33 | N |

**Cross-check vs hyperion R-aerocapture-fast-cruise-envelope:** v_entry computed 15.29 km/s vs hyperion 15.29 km/s, ratio 1.000. STRICT and SACR-BAG flags match hyperion's "envelope_pass = False". Physics agrees to four significant figures.

**Periapsis solver returns the floor (40 km) for every cell.** Even the corrected solver (iterating downward from 120 km to find the SHALLOWEST viable periapsis, vs hyperion's upward iteration that finds the deepest viable periapsis) finds NO altitude in [40, 120] km where single-pass drag dissipates the required Earth-arrival dv (3.8 to 7.9 km/s depending on v_∞). At the model floor of 40 km, drag is sufficient — but periapsis below ~50 km enters the dense lower atmosphere where the trajectory is reentry, not aerocapture.

## Reading

**The binding constraint is capture-feasibility itself, not bag-thermal-survival or chunk-structural-survival.** ICEBERG ballistic coefficients (4600–6600 kg/m² across the swept envelope) are too high for single-pass aerocapture at any survivable periapsis altitude. The chunk-as-heat-shield architecture as conceived (single deep pass; bag retracted-or-sacrificed; chunk-forward orientation) cannot complete capture in one pass without entering the dense lower atmosphere (≤ 40 km), where the trajectory is reentry-burn rather than aerocapture.

This is consistent with R-chunk-as-heat-shield's own table: at periapsis 90 km, dv per pass was 285 m/s — single-pass dissipation of full 6 km/s capture would need 22 passes, NOT one. R-chunk-as-heat-shield then noted the bag fails at 90 km (3,144 K), so even 22 passes is unworkable. The original round was modeling multi-pass aerobraking, not single-pass aerocapture; the "single-pass" framing entered the matrix only via Saturn's SCOPE.md cherry-pick.

**Three load-bearing findings:**

1. **The matrix's aerocapture-conditional architecture rows (Variant C STRICT-closing cell at faster cruise; year-twenty-plus megawatt all-electric end-to-end winner cell) are *engineering-falsified* on capture-feasibility, not just on heat flux or structural margin.** Hyperion's R-aerocapture-fast-cruise-envelope already showed Variant C fails on structural+thermal at v_∞=10.55. Phoebe shows that Variant C also fails on capture-feasibility at v_∞ ≤ 8.55 (with lunar-gravity-assist credit). The architecture has no surviving (chunk, velocity) configuration in single-pass mode.

2. **The SACRIFICIAL_BAG relaxation does not save chunk-as-heat-shield.** Even discarding the bag entirely, no (chunk, v_∞) cell achieves capture at periapsis ≥ 50 km. The chunk surviving structurally and thermally is a necessary-but-insufficient condition; capture-feasibility is the upstream binding constraint that wasn't separately tested in either prior round.

3. **The hybrid path (single-deep-pass with sacrificial bag, then multi-pass aerobraking) remains the only architecturally-credible aerocapture-adjacent candidate.** R-chunk-as-heat-shield's "Three observations" #3 sketched it; R-hybrid-aerocapture-aerobraking has a SCOPE.md on main but has not been run. The hybrid would split dv across one deep pass + many shallow passes; chunk-thermal and chunk-structural margins for the deep pass are the binding open questions. Phoebe's round does NOT close the hybrid; it forecloses single-pass.

**What this means for the matrix:**

- Variant C STRICT-closing cells across all hyperion-Round-F faster-cruise variants (aphelion 10.5–14 AU) are now *capture-feasibility-falsified* in addition to *structural-falsified*. Two independent failure modes; either alone is sufficient to retire the cell.
- Variant B at chunk 200 t (the only L1-007-feasible chunk per phoebe's prior round) has no aerocapture-conditional rescue at any v_∞ tested. Combined with phoebe's prior R-variant-B-100t-resizing finding (Variant B fails on propellant-feasibility at chunk < 200 t), Variant B is now closed as a venture-class cell entirely without a hybrid-aerocapture rescue.
- The matrix's "aerocapture-conditional" framing should be replaced with "hybrid-aerocapture-conditional" pending R-hybrid-aerocapture-aerobraking. The single-pass conditional is closed.

## Revisit

| Sub-claim | Pre-registered | Computed | Held? | Direction |
|---|---|---|:---:|---|
| H-csa-a — STRICT closing region empty (predicted 0–2 of 40) | 0 cells | 0 cells | **Y** | exact |
| H-csa-b-chunk — SACR-BAG upper bound on chunk (predicted 75–150 t) | upper bound undefined (region empty) | none | **N** (vacuously) | more pessimistic than predicted (predicted region exists with bound; actually empty) |
| H-csa-b-vinf — SACR-BAG upper bound on v_∞ (predicted 5–8 km/s) | upper bound undefined (region empty) | none | **N** (vacuously) | more pessimistic than predicted |
| H-csa-c — Variant C no intersection (predicted false) | SACR-BAG pass = False | False | **Y** | exact |
| H-csa-d — Variant B no intersection (predicted false) | SACR-BAG pass = False at all probed v_∞ | False at all 3 probed | **Y** | exact |
| H-csa-e — small-chunk multi-mission flag (qualitative) | flag follow-on if small-chunk closing region exists | none exists | n/a | n/a |
| H-csa-f — orientation-stability (conditional) | not gradable iff antecedent false | antecedent false | not gradable | per convention |

**Aggregate H-csa-agg: HELD.** All three aggregate-relevant claims (H-csa-a + H-csa-c + H-csa-d) held. Chunk-as-heat-shield single-pass is structurally infeasible across the architecturally-relevant envelope.

**Pre-registration accuracy:** 3 of 5 gradable HELD; the 2 falsifications were both *more pessimistic than predicted* (the SACR-BAG closing region is empty, not bounded). This continues the recurring-lesson #N pattern: aerocapture rounds in this campaign have been pessimistically pre-registered AND have come back even more pessimistic than the pre-reg. The campaign-level falsification trajectory is consistent (R-aerocapture, R-chunk-as-heat-shield, R-deployable-drag-skirt, R-aerocapture-fast-cruise-envelope, R-no-atmospheric-capture-baseline, and now R-chunk-as-heat-shield-revisit — six aerocapture-adjacent rounds, all falsifying-more-pessimistically than pre-reg).

## Cross-learning

**NEGATIVE for the matrix's aerocapture-conditional surviving cells.** Two independent failure modes now sit on top of Variant C STRICT-closing cell (structural per hyperion + capture-feasibility per phoebe). Recommend matrix update: aerocapture-conditional rows reframed from "engineering-pending" to "single-pass-engineering-falsified, hybrid-engineering-pending".

**NEGATIVE for Saturn's R-chunk-as-heat-shield-revisit SCOPE.md.** SCOPE.md's framing — "the binding open question is chunk geometric stability" — was downstream of an unaddressed earlier question (capture-feasibility itself). Hyperion's R-aerocapture-fast-cruise-envelope closure_verdict.md already flagged that Saturn's SCOPE cherry-picked R-chunk-as-heat-shield's sub-finding. This round shows the cherry-pick obscured a more fundamental issue: at ICEBERG-class ballistic coefficients, single-pass aerocapture is infeasible at survivable periapsis altitudes regardless of any orientation-stability or thermal margin. Recommend SCOPE.md retrospective falsification note.

**POSITIVE for hyperion's R-aerocapture-fast-cruise-envelope methodology.** Cross-check at 200 t / 15.29 km/s reproduces hyperion's anchor exactly (ratio 1.000 to four significant figures). The verified physics functions are reliable building blocks; phoebe's broader sweep used them via import (not copy-paste) per the protocol's modular layout convention.

**POSITIVE for R-hybrid-aerocapture-aerobraking** (SCOPE on main, not yet run). The hybrid is now the *only* surviving aerocapture-adjacent candidate. Should be promoted to the next critical-path round if not already. Specifically: model the deep-single-pass-sacrificial-bag → high-elliptic-orbit → multi-pass-shallow-aerobraking sequence; the binding open questions are (a) deep-single-pass ablation and structural margin at the chunk mass that allows full capture at periapsis below 40 km, and (b) tractable pass-count for the multi-pass phase at altitudes the chunk-and-tug can survive thermally.

**METHODOLOGY-FLAG for hyperion's `required_periapsis_altitude_km`.** The function iterates 40→120 km and returns the FIRST altitude where dv >= target — which is the DEEPEST viable periapsis when the loop trivially passes at the floor. For aerocapture, the optimum is the SHALLOWEST viable periapsis (cooler heating, lower g). For hyperion's narrow Round-F sweep this didn't matter (the question was binary: does ANY altitude work?). For broader sweeps, the loop direction needs reversing OR a docstring needs to flag that the function returns "deepest viable" not "shallowest viable". Phoebe's run.py uses a local override `shallowest_viable_periapsis_km` that iterates downward; both versions produced identical results for this round (because no cell captures at any altitude in [40, 120]), so the bug is latent — but a future low-β / low-velocity round would hit it. Cross-references Methodology lesson 6 (shared-physics function input conventions need assertions). Recommend orchestrator add a docstring note to `R_aerocapture_fast_cruise_envelope/run.py:104`.

**METHODOLOGY-FLAG for the conditional-hypothesis grading convention** (carried forward from phoebe's prior R-variant-B-100t-resizing). H-csa-f (orientation-stability, conditional on architecturally-relevant intersection existing) reports "not gradable" when the antecedent is false, not "held-vacuous". H-csa-b sub-claims about the SACR-BAG region's upper bound report "not held (vacuously)" because the empty region direction is more pessimistic than the bounded-region prediction — distinct from "not gradable". Two distinct conventions; both honest. Recommend protocol-level addendum.

**Cross-references to other rounds:**

- `R_aerocapture_fast_cruise_envelope/closure_verdict.md` — hyperion's structural+thermal falsification of Round-F STRICT cell.
- `R_no_atmospheric_capture_baseline/STUDY.md` — hyperion's "kill-shot" finding that ZERO surviving cells exist with aerocapture removed across a 288-cell sweep. Combined with phoebe's finding that aerocapture's single-pass mode is closed, the program-level architectural status is: surviving cells require either (a) hybrid-aerocapture closure, or (b) acknowledgement that no single-mission architecture closes inside L0-05.
- `R_variant_B_100t_resizing/STUDY.md` — phoebe's prior round; Variant B fails on propellant-feasibility at chunk < 200 t. Combined with this round's finding that Variant B has no aerocapture rescue at chunk = 200 t, Variant B is closed except via hybrid.
- `R_hybrid_aerocapture_aerobraking/SCOPE.md` — the not-yet-run round that is now the critical-path candidate.

**Follow-ons (recommended priority order):**

1. **R-hybrid-aerocapture-aerobraking** — open question is whether deep-single-pass + multi-pass-shallow can close where single-pass alone cannot. Highest leverage.
2. **R-program-class-reframe** — given the matrix's surviving-cell list now collapses to (a) Variant A acknowledged-collapse, (b) Architecture-E with ≥25-yr L0-05 waiver, (c) hybrid-aerocapture-conditional pending R-hybrid, the program may need to be reframed as L0-05-relaxation-required regardless of architectural choice. Worth a meta-round to surface this to project owner.
3. **(Already on main) Methodology-flag fix** — hyperion's `required_periapsis_altitude_km` docstring/loop-direction. Defer; not blocking.

