# R-closure-boundary-inversion — FINDINGS

**Worker:** worktree-172651, 2026-07-26. Pre-registration: `STUDY.md` (H-B1..H-B7,
arms A/B). Artifacts: `boundary_sweep.py`, `boundary_conditional.py`,
`boundary_isp_scan.py`; `results/boundary_results.json`,
`results/boundary_conditional.json`, `results/boundary_isp_scan.json`,
`results/boundary_bigchunk_probe.json`. Oracle: saturn_water_v1 closed-loop sweep
(~0.1 s/call; 185 calls stage 1-5 + conditional/scan passes). Baseline replicated
before every pass: 150 cells / 1,744 paths / 0 closures, taxonomy P0 660 / P1 445 /
P4 408 / P0b 180 / P2 36 / P1b 15.

## Headline

**No single performance parameter closes the mission — at any value, in either
posture (H-B1 HELD).** Launcher capacity ×16, reactor specific power to 400 W/kg,
water-MET Isp to 20,000 s, chemical Isp to 480 s, capture efficiency to 1.0,
power classes to 1,000 kWe: each alone leaves closure at exactly zero. The closure
boundary is inherently JOINT — minimum three simultaneous levers — and it sits in a
very different place depending on the departure-physics posture:

- **Arm A (record physics — 9.0 km/s chunk-fed departure anchor, legacy Earth-capture
  formula):** first closure at **water-Isp 2,000–4,000 s (a WINDOW, see below) +
  ≥100 kWe power class**, even at today's launchers and KRUSTY 2.4 W/kg — but it
  delivers only ~6.4 t. The 30-t commercial floor needs, in addition, launcher
  ×≥1.2 **or** specific power ≥2.8 W/kg; the full S5 scenario (Starship-refill ×5 +
  33 W/kg + Isp 2,000 s) closes 44/210 cells and delivers up to **60.6 t**, with
  both 15-yr-strict and 25-yr-waiver paths.
- **Arm B (honest physics — 18 km/s Edelbaum spiral departure, vis-viva Earth
  capture, 10-yr reactor lifetime):** every named-2030s-program scenario (S1–S5)
  collapses to ≤7 t. Reaching just the 10-t demonstrator floor requires
  **Isp 3,000 s + launcher ×8 + 60 W/kg + propellant fraction 0.40** (12.8 t).
  The 30-t commercial floor is reachable ONLY by adding a **300–500 t captured
  chunk** on top of all of that (2 cells close, max 56 t delivered). Below a
  ~300 t chunk, the commercial floor is unreachable at ANY probed technology
  (Isp ≤5,000 s, ×8, 100 W/kg, 500 kWe).

The A-vs-B split is the single most valuable number in the round: **the unresolved
9.0-vs-18 km/s chunk-fed departure anchor (Oberth-assisted vs pure spiral) moves
every threshold by roughly one full technology generation.** Resolving it (a
Basilisk/Edelbaum integration from the actual residence orbit) is now the
highest-leverage 0-cost desk item in the campaign.

## Verdicts

| # | Hypothesis | Verdict | Measured |
|---|---|---|---|
| H-B1 | No single-parameter closure | **HELD** | all six axes + power-grid extension: 0 closures at bracket extremes, both arms |
| H-B2 | Water-Isp threshold 1,200–4,000 s with launch elastic (Arm A) | **HELD (as a window)** | closure window 2,000–4,000 s at record launchers + 100 kWe; at ×5+33 W/kg the window opens down to 800 s (marginal 7 t) |
| H-B3 | Min power 50–200 kWe at threshold Isp | **HELD** | 100 kWe class is the first closing row at record mass tech; 30 kWe suffices only with ×5+33 W/kg mass relief; Arm B needs 150 kWe at Isp 3,000 |
| H-B4 | Specific power alone closes nothing | **HELD** | 2.4→400 W/kg alone: 0 |
| H-B5 | No propellant fraction alone closes | **HELD** | f scan 0.05–0.90 step 0.025: 0 everywhere, both arms |
| H-B6 | Demonstrator grid (0.5–5 t) fails at record tech at P4, closes with ≥30 kWe + Isp ≥1,000 | **HALF-FALSIFIED (informative)** | fails at record tech as predicted, but does NOT close even at Isp 1,500 + 10-kWe gate override: **a 0.5–5 t chunk cannot feed its own departure** — vehicle dry mass dominates the Tsiolkovsky ratio (P4 = 672 of 672+... deaths). Chunk-fed return has a MINIMUM viable chunk size (~10 t at Arm-A physics, ~100 t honest) |
| H-B7 | Some named-2030s scenario closes ≥10 t under waiver | **HELD for Arm A only** | Arm A S4 (900 s MET): 2 cells ≥10 t; S5 (2,000 s): 28 cells ≥10 t, 7 cells ≥30 t. **Arm B: every S1–S5 scenario ≤7 t — falsified under honest physics** |

## Prediction-error notes

1. **The Isp axis is non-monotone (declared post-hoc as deviation D-6).** Propellant
   need falls with Isp but power-limited burn time grows ~linearly with exhaust
   velocity; the two constraints cross and leave a finite closure window
   (2,000–4,000 s at record mass tech; wider with mass relief). Stage-1 bisections
   on Isp are therefore invalid and were replaced by explicit scans
   (`boundary_isp_scan.py`); the pre-registered 3-point monotonicity spot-check was
   insufficient to catch a window narrower than the bracket midpoints. Protocol
   lesson candidate: monotonicity checks for bisection must bracket the *physics
   crossover*, not just sample endpoints. **Project-owner ruling 2026-07-26
   (latest+29b): NOTE-ONLY — recorded here, not promoted to PROTOCOL.md.**
2. **The demonstrator-scale result inverts the intuition that smaller is easier.**
   Below ~10 t chunk, the chunk-as-propellant architecture starves: the departure
   burn needs more water than the chunk contains once vehicle dry mass (16–18 t
   derived at 1–30 kWe) enters the mass ratio. A Saturn-return demonstrator must
   either carry its own return propellant (different architecture) or capture
   ≥10 t (Arm A) — the 0.5–5 t "cheap demonstrator grid" the relaxation round
   asked for is structurally void, not merely unfunded.
3. **λ-bisection returned no threshold in either arm** because the aspirational
   direction included f→0.36, which starves the chemical/kick outbound legs
   (need f ≥ 0.76 at 340 s) while the electric outbound is burn-time-capped at the
   record thrust axis — the aspirational VECTOR is infeasible even though nearby
   scenario combinations close. Straight-line interpolation through a non-convex
   feasible set is the wrong scalarization; the named-scenario table replaces it.

## The closure boundary (the three lists the project owner asked for)

### List 1 — why it does not close today (binding walls, in order)

1. **P0 launch mass:** smallest self-consistent wet vehicle 138 t vs largest
   encoded capacity 300 t (6×FH raw) — 660/1,744 paths; heaviest useful cells
   (30 kWe, ≥50 t chunk) need 331–604 t.
2. **P1 outbound:** chemical TSI needs propellant fraction 0.888 > the 0.80
   convention (infeasible-by-construction); electric outbound gated ≥20 kWe and
   burn-time-capped — 445 paths.
3. **P4 Saturn departure:** at 800 s the ENTIRE 200-t chunk buys 7.66 km/s < the
   9.0 km/s (optimistic) anchor, and the honest anchor is 18 km/s; power gate
   30 kWe — 408 paths.
4. **Delivered-mass floor:** even where arrival closes (Arm A + 100 kWe + Isp
   2,000–4,000 s), delivery is ~6 t vs the 25-t provisional commercial floor.
5. **Round-trip ceiling:** most closures are 16+ yr (25-yr-waiver class); 15-yr
   strict paths exist only at ≥100 kWe with high Isp.

### List 2 — performance parameters that flip closure (with thresholds)

| Parameter | Record value | Threshold (Arm A, optimistic) | Threshold (Arm B, honest) |
|---|---|---|---|
| Water-compatible Isp (continuous, flight-scale) | 800 s (lab, pulsed) | **2,000–4,000 s window** (with ≥100 kWe); ≥900 s if launch+specific-power also move | **3,000 s** (with ×8 launcher + 60 W/kg + f 0.40) |
| Electric power class at Saturn | 1–55 kWe grid | **≥100 kWe** (or 30 kWe with ×5 launcher + 33 W/kg) | **≥150 kWe** |
| Reactor specific power | 2.4 W/kg (KRUSTY) | 2.8–33 W/kg (trade vs launcher) | **≥40 W/kg** (arrival) / **≥60 W/kg** (10-t floor) — the exact TRL-2 "aspirational" band the campaign retired |
| Launcher capacity (effective, incl. refill/assembly) | 63.8–300 t | ×1.2 (with 33 W/kg + Isp 2 ks) to ×5 | **×8 (≈800 t single-manifest equivalent)** |
| Captured chunk mass | 10–200 t grid | ≥10 t (minimum viable); 200 t for 60-t delivery | **300–500 t for the 30-t floor** (B-ring single-chunk cap is 482 t — the requirement sits inside the cap by 0–38%) |
| Propellant-fraction posture | 0.80 frozen | insensitive (closure exists at 0.80) | **~0.40** (per-phase-Tsiolkovsky-like) |
| Capture efficiency | 0.85 anchor | not binding (multiplier 0.25–1.0 moves delivered mass, not closure) | same |
| Chemical Isp | 340 s | not binding ≤480 s | not binding |

### List 3 — TRL gaps implied (each threshold vs 2026 state of the art)

- **2,000–3,000 s continuous on water-derived propellant:** no hardware >900 s on
  raw water exists (water-Hall record 2,039 s at 1.6 kW, 12.5% anode efficiency —
  single lab point); RF-ion at 2,000 s requires the un-flown
  purity/filtration conjunction. TRL 3–4. THE gating technology in both arms.
- **100–200 kWe space reactor at 33–60 W/kg:** flight-credible 2030s hardware is
  6–20 kWe at 3–10 W/kg (JETSON PDR); 100 kWe directed by NSTM-3 but Phase 2
  unawarded; 40+ W/kg is TRL 2 paper. Second gating technology.
- **Starship-refill-class effective lift (×5–×8 = 500–800 t):** the only lever
  already moving — refilling demo scheduled late 2026; TRL 5→6-7 within ~18 months.
  Treat as cost, not physics.
- **300–500 t single-chunk capture (honest arm):** 2.5× beyond the 200-t
  containment/GNC envelope studied in Round J (ceilings scale m^(−1/6): 24.6→9.2
  m/s whole-bag at 500 t — still 4 orders above residence velocities, so
  containment physics scales; mechanism reliability and despin at 500 t are
  unstudied). TRL 2.
- **ISRU processing rate:** absent from the framework entirely; becomes binding the
  moment any closure exists (a 200-t chunk melt at 55 kWe is ~1 month — tolerable;
  electrolysis at scale is the v2 round's subject).

## Matrix / axis amendment specification

- Decision #16 table: add the boundary map above as the parametric answer to
  "what would it take" — supersedes the empty-set framing as the final word
  (the set is empty at record tech; non-empty at named joint thresholds).
- Axis 03 (inbound propulsion): the 2,000–4,000 s Arm-A window and 3,000 s Arm-B
  point land exactly on the RF-ion-class regime — strengthens the axis-03 position
  that water-MET at 500–800 s is an architecture trap for the RETURN leg.
- Axis 05/06/20 (power): honest-arm thresholds (150 kWe, 40–60 W/kg) restate the
  falsified megawatt wall one generation lower — update the restoration bound.
- Axis 09 (chunk-mass cap): NEW lower bound — minimum viable chunk ~10 t (Arm A)
  / ~100 t (Arm B); commercial floor needs 300–500 t honest, inside the 482 t cap.
- Axis 13 (launch): ×5–×8 effective-lift requirement; New Glenn/SLS still
  un-encoded (immaterial — both below Starship-refill class).

## Residuals (open)

1. **9.0-vs-18 km/s chunk-fed departure anchor** — highest-leverage desk item;
   every Arm-A number is conditional on partial Oberth credit that
   R-lowthrust-spiral-departure says a continuous spiral does not get.
2. Power-thrust consistency (D-4): closing cells at the 100-kWe row use thrust
   1–2.5 N (consistent: F_max = 2P/ve ≈ 6.8 N at 100 kWe/3,000 s); spot-checked
   `power_thrust_consistent=True` on the top cells, but P1's thrust axis is still
   not power-derived framework-wide.
3. The 180 P0b assembly deaths: confirmed mostly by-design enumeration stubs +
   the never-exercised depot-relay branch (`existing_leo_depot` unset) — cheap
   framework cleanup, not physics.
4. Transit-time is NOT scaled with departure delta-v in Arm B (18 km/s spiral
   still books 8-yr transit) — honest-arm round-trip times are optimistic; a
   spiral-time model would push more closures from strict to waiver to miss.
5. The v2 electrolysis departure stage (impulsive Oberth 8.51 km/s from ISRU
   H₂/O₂) is the one architecture that dodges the Arm-B spiral penalty entirely —
   companion round, executed next.
