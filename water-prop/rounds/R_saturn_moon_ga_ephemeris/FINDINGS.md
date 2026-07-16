# R-saturn-moon-ga-ephemeris — FINDINGS

**Worker:** phoebe (re-spawn, branch `iceberg-phoebe`)
**Date:** 2026-05-26
**Inputs:** `pull_horizons.py` → `results/horizons_moon_states.json`; `ga_leverage.py` →
`results/ephemeris_dv_table.json`. Pre-registration: `STUDY.md` (H1-H9).

> Terminology: "v_inf" = hyperbolic excess velocity (here, the spacecraft's
> Saturn-relative arrival speed at infinity); "Δv" = delta-velocity; "gravity assist"
> = unpowered flyby that rotates the spacecraft's velocity relative to the flyby body.

---

## Headline

The SCOPE asked: *replace the three constant-scalar Saturn-moon gravity-assist anchors
with epoch-dependent ephemeris-driven values.* The finding inverts the premise:

**The constant-anchor STRUCTURE is correct — gravity-assist leverage at Saturn's moons
is secularly epoch-invariant to better than 1% (H7). What is wrong is the VALUES and the
multi-moon framing.** No epoch-dependent lookup table is warranted; a set of constant
corrections is. Specifically:

1. The `*_VINF_REDUCTION_KM_S` constants (4.0 / 1.5 / 5.5 km/s) are **dead code** — they
   appear only in definitions and comments, never in any precondition or executor. The
   live model full-captures (`v_inf → 0`) for a small trim burn plus tour-time, for any
   arrival v_inf above the gate.
2. **Titan is the only moon that matters.** Its per-flyby Δv ceiling (~1.6 km/s) is
   4-17× every other moon's. The five small moons in the "Cassini-class multi-moon tour"
   are **leverage-inert** (H8): Dione 0.047, Tethys 0.025, Enceladus 0.007, Mimas
   0.003 km/s per flyby — they need 40-664 flybys to bleed 1 km/s. The multi-moon tour
   is, mechanically, a **Titan tour**; the small moons are phasing aids, not leverage.
3. `rhea_gravity_assist_capture` is **not a defensible standalone capture option**: Rhea
   capture from its own 4.0 km/s gate needs **34 flybys** of a 0.085-km/s-per-pass moon.
4. The `cassini_class_multi_moon_tour` **24-month anchor over-states capture time ~3×** —
   Titan alone captures from any arrival v_inf in 2-7 months.

None of this changes the campaign verdict — gravity-assist capture was never a binding
constraint (titan-4 R-framework-matrix-parity: binding constraints are reactor lifetime
and powerplant dry-mass, not Saturn capture). These are fidelity corrections to a
non-binding axis. No >2× error exists in a closure-flipping direction on a live binding
anchor, so no emergency surface per the work-order trip-wire. (Two >2× tour-TIME errors
exist — Cassini 24mo over, Rhea 12mo under at high v_inf — but tour time is coast time
feeding round-trip duration, not a closure-binding axis. Flagged below, not escalated.)

---

## Method recap

Patched-conic, upper-bound posture. A flyby conserves |v_inf relative to the moon| and
rotates it; the Saturn-relative Δv per pass is `2·v_inf,m·sin(δ/2)` with
`sin(δ/2)=1/(1+r_p·v_inf,m²/μ_moon)`, capped at `√(μ_moon/r_p)`. Best-case tangential
coplanar geometry every pass → these are optimistic ceilings; real tours derate. A
sequential same-moon pump-down counts flybys to rotate v_inf,m until the Saturn-relative
speed reaches capture, then converts flyby count → tour months via a 2× moon-period
resonant re-encounter spacing. Cross-checked against Cassini's flown Titan-flyby leverage
(~0.8-0.9 km/s/pass) — model realistic value 1.0-1.34 km/s/pass sits correctly above the
flown, non-optimal values.

---

## Per-hypothesis verdicts

| # | Hypothesis | Verdict | Evidence |
|---|---|---|---|
| **H1** | Titan-only > 5 km/s at best-of-window | **HELD** | Titan captures fully from arrival v_inf 5.5-6.5 → 5.5-6.5 km/s reduction in 5-7 flybys / 5.2-7.3 months. |
| **H2** | Rhea-only > 2 km/s at best-of-window | **HELD in principle, FALSE operationally** | Rhea can pump to full capture, but 2 km/s alone needs ~25 flybys; gate-to-capture needs 34-78. Per-flyby 0.085 km/s — 34 consecutive near-perfect Rhea flybys is not a credible primary capture. |
| **H3** | Multi-moon > 5.5 km/s across most arrival epochs | **FALSIFIED** | Achievable reduction = arrival v_inf (full capture). Exceeds 5.5 only at arrival v_inf ≥ 5.5 (2 of 8 grid points). Leverage is epoch-invariant (H7), so the "epochs" axis does not vary the answer. |
| **H4** | ≥1 epoch with multi-moon Δv > 8.25 km/s (>50% over anchor) | **FALSIFIED** | Reduction is capped by arrival v_inf. The Phase-2 sweep ceiling is 6.5 km/s. You cannot bleed more v_inf than you arrived with. |
| **H5** | (load-bearing) Anchors within 30% of ephemeris-derived Δv across window | **FALSIFIED** | Reduction constants are dead/unused; Cassini 24-month tour-time over-states Titan capture (~7 mo) by ~240%; reduction anchors are fixed numbers while reality tracks arrival v_inf. |
| **H6** | Worst-case epoch: multi-moon Δv below titan-only 4.0 | **FALSIFIED** | Leverage epoch-invariant; multi-moon is Titan-driven and never underperforms titan-only. No epoch degrades it below 4.0. |
| **H7** | (phoebe, load-bearing) Leverage epoch-independent to < 1% | **HELD** | Per-flyby Titan Δv varies **0.74%** (1.2401→1.2488 km/s) across Titan's full perikrone-apokrone radius range; all moons < 1% except Mimas (3.9%, inert). Instantaneous speed swings (Titan 5.1%) are orbital eccentricity, not secular drift, and are absorbed by flyby-point selection. |
| **H8** | (phoebe) Small moons < 1 km/s combined; tour is a Titan tour | **HELD (strong)** | Per-flyby Δv: Rhea 0.085, Dione 0.047, Tethys 0.025, Enceladus 0.007, Mimas 0.003 km/s. To bleed 1 km/s each: 23 / 40 / 72 / 247 / 664 flybys. The five small moons are leverage-inert; useful only for phasing. |
| **H9** | (phoebe) ≥1 anchor wrong in a matrix-relevant way | **HELD** | (a) reduction constants dead; (b) Cassini 24-mo over-states ~3×; (c) Rhea 12-mo under-states (20-23 mo at arrival ≥6); (d) min-v_inf floor rationale inverts the physics. |

---

## Why the min-v_inf gate rationale is backwards

The Titan option gates on arrival v_inf ≥ 3.5 km/s, with the comment *"Below that, the
geometry of close passes does not have enough leverage."* The physics is the opposite:
**lower arrival v_inf is easier to capture**, not harder — at v_inf 3.0 Titan captures in
2 flybys / 2.1 months; at 6.5 it needs 7 flybys / 7.3 months. The floor is a sensible
*operational selection heuristic* ("below ~3 km/s you are nearly captured already; use a
small direct chemical burn instead of a months-long tour"), but its stated *leverage*
justification is false and should be corrected so no downstream reasoning treats GA
capture as leverage-limited at low v_inf.

---

## Matrix / framework amendment specification

These are recommendations for the orchestrator; workers do not edit shared docs. None is
verdict-changing. Target file: `water-prop/sims/mission_graph/missions/phase2_saturn_capture.py`
(and the matrix axis that references the Saturn-capture options).

1. **Retire or relabel `rhea_gravity_assist_capture`.** Not a credible standalone
   capture (34+ flybys at 0.085 km/s/pass). Either delete, or relabel as a *Rhea phasing
   assist* that is never the primary capture mechanism. The 1.5 km/s / 12-month anchor is
   not defensible as standalone capture.

2. **Relabel `cassini_class_multi_moon_tour` as a Titan-led tour and cut its time.** The
   five small moons add negligible leverage (H8). Either (a) drop it as *dominated by*
   `titan_gravity_assist_capture` (same capture, ~1/3 the time, comparable trim), or
   (b) keep it but correct the rationale (small moons = phasing aids) and reduce
   `CASSINI_TOUR_MONTHS` from 24 to ~10-14 if it is meant to be a realistic capture tour.

3. **Remove or correct the dead `*_VINF_REDUCTION_KM_S` constants.** They are unused. If
   retained for documentation, restate them correctly: *achievable reduction = arrival
   v_inf (full capture); per-Titan-flyby Δv ~1.0-1.34 km/s realistic, ceiling 1.585.*
   Nobody downstream should treat 5.5 as a capability — it is only reachable when arrival
   v_inf ≥ 5.5.

4. **Fix the Titan min-v_inf gate comment** (and consider allowing GA capture below the
   gate). The floor is an operational heuristic, not a physics limit.

5. **Titan tour-time (8 months) is well-calibrated / mildly conservative.** Keep. If the
   matrix needs capture *duration* (it feeds round-trip time and reactor *calendar* life,
   not burn time — GA is coast), make Titan months arrival-v_inf-dependent:
   ~2 months (v_inf 3) → ~7 months (v_inf 6.5). The chemical trim anchors (0.3 km/s
   Titan) are physically plausible for the final park burn.

6. **No epoch-dependent lookup table.** H7: leverage is epoch-invariant. The SCOPE's
   epoch-dependent-value premise is itself falsified. Epoch matters only for phasing the
   first Titan encounter (always reachable within ~1 Titan period ≈ 16 days) and for the
   now-moot multi-moon sequencing.

---

## Limits & threats to validity

- **Patched-conic, coplanar, optimal-geometry-every-pass.** All numbers are optimistic
  upper bounds; real tours derate per-flyby Δv and need more flybys / longer tours. This
  strengthens the falsifications (H2/H3/H4/H8 only get worse for the anchors under
  realistic geometry) and weakens H1 (Titan >5 km/s is at the optimistic edge — ~7 ideal
  flybys; a real tour might need 10-12 and run closer to the 8-month anchor).
- **Resonance spacing fixed at 2× moon period.** Tour-month estimates scale linearly with
  this assumption; the *flyby counts* and *Δv* numbers do not depend on it. A real tour's
  spacing varies pass-to-pass; the Cassini-class tour spacing was weeks-to-months. The
  qualitative conclusions (Titan dominant, small moons inert, leverage epoch-invariant)
  are robust to this assumption.
- **Single-moon pump-down.** Real captures interleave moons for phasing; modeled here as
  Titan-only because the small moons contribute no leverage. A genuine multi-moon
  *phasing-optimised* tour was not constructed (out of SCOPE; would need a Lambert/MALTO
  phase search). It would not change the leverage conclusions.
- **Atmosphere/altitude.** Titan flyby altitude fixed at 1000 km (Cassini went to ~880).
  Lower altitude raises the per-flyby ceiling slightly; does not change conclusions.

## Reproduce

```bash
cd water-prop
uv venv .venv-ephem --python 3.11 && uv pip install --python .venv-ephem/bin/python numpy scipy requests
.venv-ephem/bin/python rounds/R_saturn_moon_ga_ephemeris/pull_horizons.py    # ~30 s, needs internet
.venv-ephem/bin/python rounds/R_saturn_moon_ga_ephemeris/ga_leverage.py
```
