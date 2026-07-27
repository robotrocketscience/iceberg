# R-hohmann-vinf-reconciliation — the campaign's 6.21 km/s Saturn-departure v∞ vs the two-body minimum, and whether it matters

**Status:** SCOPE pre-registered 2026-07-21, before `run.py`. Bounds from `scope_bounds.py`, committed alongside.
**Worker:** worktree-115637 session. Closes the corrections-live-forward item flagged in `design-axes/04-inbound-dv-accounting.md` (latest+25): the campaign carries **VINF_DEP = 6.21 km/s** as "the Hohmann-return hyperbolic excess" at Saturn (R179 `R_departure_anchor_reconciliation` scope_bounds line 31; reused by R186 `R_titan_tour_ephemeris`), but a clean two-body Saturn→Earth Hohmann gives **~5.44 km/s**. This round reconciles the 0.77 km/s (14 %) gap from first principles and propagates it through the two things that depend on it — the reactor-power floor and R186's Titan bound-chain cap.

## The discrepancy

`R_departure_anchor_reconciliation` (R179) fixed the departure-Δv accounting and set the 155-175 kWe reactor floor, anchoring on VINF_DEP = 6210 m/s labeled "Hohmann-return hyperbolic excess (audit)." A minimum-energy heliocentric Hohmann from Saturn's orbit to Earth's orbit gives v∞ = v_Saturn − v_transfer-aphelion = 9.64 − 4.20 = **5.44 km/s**. The campaign value is 14 % high. The question is not only *which is right* but *does the reactor floor or the Titan-lever revocation move if we use 5.44*.

## Pre-registered hypotheses (bounds scripted)

**H1 [S] (the two-body minimum).** The minimum-energy Hohmann Saturn→Earth departure excess is **5.44 km/s**, robust to the Saturn semi-major-axis convention (9.537 / 9.5388 / 9.582 AU all give 5.44 to 3 sig figs). SCOPE band **[5.3, 5.6] km/s**. Falsified outside band.

**H2 [S] (what 6.21 actually is).** 6.21 km/s is **not** the tangent-Hohmann minimum; it corresponds to a **faster transfer** whose perihelion dips to **~0.65 AU** (inside Venus's orbit) while keeping aphelion at Saturn — a legitimate faster Saturn→Earth trajectory, but **conservative by 14 %**, not the minimum-energy value it was labeled. SCOPE: perihelion q ∈ **[0.55, 0.75] AU**. Falsified if q ≥ 0.95 AU (i.e. 6.21 is in fact ~tangent).

**H3 [S] (departure Δv barely moves — Oberth quadrature).** From the co-orbital B-ring (v_circ 18.83, v_esc 26.63 km/s), the single-burn escape to v∞ is `sqrt(v∞² + 2μ/R) − v_circ`: **8.51 km/s at 6.21** (reproduces R179 exactly) vs **8.35 km/s at 5.44** — a change of **0.16 km/s (1.9 %)**. The well depth dominates; v∞ enters in quadrature, so d(Δv)/d(v∞) ≈ 0.23. SCOPE band on the change **[0.10, 0.25] km/s**. Falsified if the departure-Δv change exceeds 0.4 km/s.

**H4 [S] (reactor floor and Titan cap both unmoved).** Recomputing R179's reactor model (2-yr chunk-fed MET burn, 100 t final, 800 s, η 0.6) at the impulsive departure Δv: **159 kWe at 6.21 → 154 kWe at 5.44**, a **~5 kWe (3 %)** change, **inside the existing 155-175 kWe band** (R179's 175 headline uses the 9.0 km/s chunk-fed *spiral* Δv, whose v∞-sensitivity is even weaker — impulsive is the upper bound on the fractional effect). R186's Titan bound-chain cap (**~3.2 km/s**) remains far below even 5.44, so the Titan pump-up lever stays revoked. SCOPE: floor ∈ [150, 175] kWe at 5.44; |change| < 10 kWe; Titan cap < 5.44. Falsified if the floor drops below 120 kWe or the Titan cap reaches v∞.

## Sweep (run.py)

v∞ over {5.44, 6.21} × a_Saturn {9.537, 9.5388, 9.582} AU; perihelion solve for 6.21; single-burn departure Δv and reactor power at both v∞; Titan-cap comparison; a v∞→Δv→reactor sensitivity curve across v∞ ∈ [5.0, 6.5]. Deterministic. Grids span the pre-script's.

## What this round does NOT do

- Does not re-derive the 9.0 km/s chunk-fed *spiral* Δv or the low-thrust departure model (R179 / mission_graph state-of-record) — it bounds the v∞-sensitivity of the reactor floor, using the impulsive chain as the conservative upper bound.
- Does not change any frozen STUDY (R179 / R186); corrections live forward as a footnote and a design-axes amendment.
- Does not re-open the Titan-lever verdict (R186) — it confirms the revocation is robust to the v∞ correction.

## Deliverables

`scope_bounds.py`, `run.py` (+ `results/vinf_reconciliation.png`), `results/findings.json`, `STUDY.md` with Revisit + bug-catch. Orchestrator notes: the campaign's 6.21 km/s is a faster-transfer (conservative) value, not the minimum-energy Hohmann (5.44); the correction is **immaterial** downstream (≤ 5 kWe of a 155-175 kWe floor; Titan revocation intact); the design-axes/04 corrections-live-forward footnote is discharged.
