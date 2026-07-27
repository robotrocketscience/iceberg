# R-departure-anchor-resolution — STUDY (pre-registration)

**Worker:** worktree-172651, 2026-07-26 latest+29b. Project-owner-authorized
(ratification-pass decision 2): resolve the 9.0-vs-18 km/s chunk-fed Saturn
departure anchor that splits the closure-boundary map into Arms A/B, moving
every threshold by ~one technology generation. Method: Edelbaum analytic +
direct RK4 numerical integration from the B-ring residence orbit (numpy; the
project owner authorized the standard variant, not Basilisk-required).

## Question

`phase4_saturn_departure.py` books `CHUNK_FED_DV_KM_S = 9.0` for the
continuous-thrust chunk-fed departure. Methodology lesson 23 (ratified this
pass) already identified the error class: 9.0 km/s is an impulsive-Oberth-value
number under a "spiral" label. R-lowthrust-spiral-departure measured 21.9 km/s
by direct integration at one specific thrust-to-weight (2.68×10⁻⁴ m/s²). This
round derives **Δv(a)** — departure Δv as a function of thrust acceleration —
from the actual residence orbit, so the anchor question becomes "which regime is
the campaign actually in," not "which single number is right."

## Model

Planar two-body Saturn (GM = 3.7931×10⁷ km³/s²), circular start at the B-ring
residence radius r₀ = 100,000 km (campaign anchor; v_circ = 19.48 km/s),
tangential (velocity-aligned) constant thrust acceleration a, RK4 with
orbital-timescale-adaptive step (dt = period(r)/200, capped), integrated until
specific orbital energy reaches the hyperbolic target E = v∞²/2 at
v∞ = 5.44 km/s (titan-2 Saturn-side excess anchor). Δv ≡ a·t_thrust (constant-a
convention; mass-flow effects raise late-burn a and would lower Δv slightly —
noted, not modeled; per Deviation 8 this is a T1 integration, and it carries the
prior round's T1 result as its cross-check).

Acceleration sweep: a ∈ {10⁻⁵, 3×10⁻⁵, 10⁻⁴, 10⁻³, 10⁻², 10⁻¹} m/s², spanning
the campaign electric envelope (30 kWe / 300–600 t stack ≈ 1.3–2.5×10⁻⁵;
200 kWe ≈ 10⁻⁴) up to the near-impulsive chemical regime.

## Hypotheses

| # | Hypothesis | Gate | Prediction |
|---|---|---|---|
| H-D1 | At electric-class a (≤10⁻⁴ m/s²), Δv is within 15% of the Edelbaum escape term v_circ = 19.48 km/s (plus excess) and ≥1.9× the 9.0 anchor | Δv < 17.1 km/s at a = 10⁻⁴ falsifies | Holds — reproduces the spiral round's 18.8–21.9 band |
| H-D2 | The 9.0 km/s figure is recovered only at a ≥ ~10⁻² m/s², 2–3 orders above any campaign electric configuration | Δv ≤ 9.0 at a ≤ 10⁻³ falsifies | Holds — 9.0 is an impulsive-regime number |
| H-D3 | Δv(a) is monotone decreasing, asymptoting toward the impulsive Oberth value (7.7–8.5 km/s) | non-monotonicity or asymptote ≠ 7.7–8.5 falsifies | Holds |

## Pre-committed disposition

If H-D1/H-D2 hold: **Arm B (18 km/s-class) becomes the citable arm of the
closure-boundary map** for any electric chunk-fed departure at ≤200 kWe; the
framework's 9.0 default stays in code for baseline immutability but its option
notes are amended to carry the lesson-23 flag and the `chunk_fed_dv_km_s` param
is the sanctioned override. The Arm-A columns of the boundary map are re-labeled
"impulsive-regime bound (not reachable by electric propulsion)". If falsified:
the 9.0 anchor survives for whatever regime the integration licenses, and the
arms are re-derived.

Also shipped with this round (lesson-25 retro-compliance for latest+29's new
closure surfaces): single-path mass-ledger walks for (a) the Arm-A S5 closing
cell and (b) the v2 electrolysis-NTP 900-s corridor cell, as
`R_closure_boundary_inversion/ledger_walk.py` + committed output.
