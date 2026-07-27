# Wet-vs-dry anchor audit (H6)

**Worker:** hyperion (re-spawn 2). **Date:** 2026-05-26. Catalog only — does NOT re-derive prior verdicts (per titan-6: structural readings survive). Grep across prior rounds' STUDY/FINDINGS/RESULTS/READING.

## Verdict — H6 HELD

The wet-vs-dry confusion titan-6 surfaced ("the audit's swept 50 t was WET = 10 t dry, read as if dry → 12× error") is **NOT unique to the audit baseline.** The same error class — a vehicle-mass number whose wet/dry status is ambiguous, or a small vehicle implicitly carrying a powerplant heavier than itself — recurs across several prior rounds. Lesson 22 candidate ("confirm wet-vs-dry before comparing a derived number to a prior anchor") is confirmed and should be ratified.

## Catalog

| Round | Anchor as written | Issue | Status |
|---|---|---|---|
| R_assumption_audit_2026_05_21 | "50 t vehicle" swept floor | **WET (= 10 t dry at 0.80)**, read as dry. 5–12× error. | **Caught by titan-6** (`08fbef9`); origin of the finding. |
| R_framework_matrix_parity (titan-4) | "50–63 t vehicle that is already 80% propellant" | Correctly identifies 50–63 t as WET (→ 10–12.6 t dry). | **Already flagged** by titan-4; no error, good practice. |
| R_bottoms_up_vehicle_cost (R13) | "implicit assumption that dry mass ~ 50 t" | Dry-mass anchor too LOW: true closed-loop dry at flown specific power is 67–117 t (per R_bus_mass_anchor_sweep). Not wet/dry per se, but an unanchored dry-mass assumption ~2× optimistic. | **Flagged** (corroborates titan-6 via a different round). |
| R_chemical_plus_small_reactor | "10-tonne vehicle" cells delivering 19.89–27.55 t | A 10 t vehicle carrying a 20 t reactor is **lighter than its own powerplant** — the closed-loop mass-floor violation. "Best closing cells" are open-loop artifacts. | **Flagged** — same class titan-6 closed-loop discredits (0/150). |
| R_non_fission_baseline | "10-tonne vehicle" + "30-tonne RTG" cells | Same: a 10 t vehicle cannot contain a 30 t RTG. Open-loop closure artifact. | **Flagged.** |
| R_architecture_D_cost | "10-tonne vehicle dry; 20-tonne reactor" | Stated dry 10 t with a 20 t reactor — explicitly vehicle-lighter-than-powerplant. | **Flagged** (here the wet/dry IS labeled, but the consistency violation remains). |
| R_chemical_plus_small_reactor | "10-tonne reactor at 40 W/kg ... 10-tonne vehicle, delivered 27.55 t" | 40 W/kg is TRL-2 aspirational (locked belief 1); this is the upside-only cell, already self-flagged. | **Already self-flagged** in-round. |

## Reading

- **Two distinct sub-classes** surfaced: (1) literal wet/dry mislabeling (audit baseline 50 t); (2) the deeper structural error it is a symptom of — **small-vehicle cells implicitly carrying a powerplant heavier than the vehicle** (the 10-t-vehicle cells across three rounds). titan-6's closed-loop refactor *structurally prevents* sub-class (2) going forward by deriving dry mass; this audit catalogs where it lived in the open-loop corpus.
- **No prior verdict needs re-deriving** (titan-6 verdict: structural readings survive; these rounds' qualitative conclusions — chemical-plus-small-reactor is upside-only, non-fission-baseline hidden-fails — were correct *despite* the anchor issue, because they all concluded "infeasible / upside-only" anyway). The catalog is methodology hygiene, not a verdict change.
- **Lesson 22 ratification recommended:** "confirm wet-vs-dry (and vehicle-vs-powerplant mass consistency) before comparing a derived number to a prior anchor." The closed-loop framework now enforces the consistency; the lesson protects the *reading* of legacy numbers.
