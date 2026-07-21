# R-com-offset-thrust-alignment — STUDY

**Round:** R-com-offset-thrust-alignment. SCOPE pre-registered 2026-07-20 (commit `406446b`) before `run.py` existed.
**Worker:** worktree-115637 session. Follow-on demanded by R-chunk-despin-budget's Revisit.

## Hypotheses, tests, results

All computations in `run.py` (closed form, deterministic); numbers in `results/findings.json`; figures in `results/`.

### H1 — RCS-fought offset is architecturally dead — **HELD**

| metric | predicted | measured | held? |
| --- | --- | --- | --- |
| every grid point, chunk ≥ 25 t, ε ≥ 0.5 m | > 5 t propellant | minimum 7.4 t | yes |
| worst corner (200 t, ε = 1.0 m, 10 kWe) | > 50 t | **496 t** | yes |

**Reading.** Fighting a decimeter-class thrust-line offset with corner reaction-control thrusters over a 4.2 km/s low-thrust burn costs between "several times the delivery floor" and "ten times the wet stack." The number is insensitive to power (slower burn at low power exactly cancels lower thrust — the angular impulse is delta-v-fixed: τ·t = T·ε·t and T·t ≈ m̄·Δv, so angular impulse ≈ m̄·Δv·ε regardless of thrust level). No propellant-based attitude strategy survives an uncorrected offset.

### H2 — steer-through-center-of-mass is cheap — **HELD**

| metric | predicted | measured | held? |
| --- | --- | --- | --- |
| worst steer authority (ε = 1.0 m, l = 5 m) | ≤ 11.4° | 11.31° | yes |
| worst cosine tax | ≤ 2% of inbound propellant | 1.98% (1.81 t on the 200 t case; 492 kg on 40 t) | yes |

**Reading.** Steering the thrust vector through the actual center of mass — main-engine gimbal, or differential throttle across the thruster array — converts a mission-killing torque fight into a cosine tax bounded at 2 percent of inbound propellant. At the canonical 40 t chunk and a well-managed offset (ε = 0.5 m, l = 10 m) the tax is **31 kg**. This held with 0.09° and 0.02-percentage-point margins — the bound was set at the worst corner per the R-chunk-despin-budget lesson, and it nearly bit anyway.

### H3 — the walk makes ε ≥ 0.5 m the operating point — **HELD**

| chunk | walk, solid 900 kg/m³ | walk, porous 500 kg/m³ |
| --- | --- | --- |
| 40 t | **1.35 m** | **1.65 m** |
| 200 t | 1.18 m | 1.44 m |

**Reading.** The inbound burn drinks roughly 40 percent of the cargo. Drawn from one side (a fixed harvest port), that walks the cargo center of mass 1.2–1.7 m — two to three times past the 0.5 m regime where H1's verdict applies. Offset is not an off-nominal condition of this architecture; it is the *default trajectory of the center of mass* unless the harvest draw is actively symmetrized or the steering tracks the walk.

### H4 — closure discriminates the strategies — **HELD**

On the audit sweep's 5 closing cells at the 25 t floor: steer-through cosine tax (worst case) flips **0**; RCS-fought flips **all 5**. The strategy choice is worth the entire commercial case.

## Revisit (mandatory)

All four held — but H2 by margins (0.09°, 0.02 pp) thin enough that a modestly different lever assumption would have falsified it; worst-corner bound-setting worked and is confirmed as the standing convention. One modeling honesty note: the walk model (uniform one-hemisphere draw, centroid at 3r/8) is a geometry bound, not a thermal simulation — an actual sublimation front follows insolation and port placement, and could be better or worse; H3's margin (2–3×) is wide enough that the qualitative verdict survives any plausible front geometry. The closure reprocess reuses the corrected `leaf_state.payload_kg` field from R-chunk-despin-budget's bug catch.

## Cross-learning

- **Adopt (two-round arc verdict, for the owner's original question):** the de-spin fuel tax is real but lives at gram-to-kilogram scale; the spin-adjacent cost that actually moves delivered water is thrust-phase center-of-mass management — bounded at ~0.1–2 percent of inbound propellant (31–492 kg on the canonical 40 t chunk) *if and only if* the vehicle can steer thrust through a center of mass that walks more than a meter during the burn.
- **Proposed L1 requirement (orchestrator to adjudicate and place):** thrust-vector authority (gimbal or differential throttle) ≥ 12° about both transverse axes, tracking a cargo center-of-mass walk envelope of ±1.7 m; OR an actively symmetrized harvest draw holding ε below 0.2 m, in which case 3° suffices. SATURN-SHIP-SPEC.md currently specifies neither.
- **Negative for** any architecture variant that fixes the main thruster rigidly on the stack axis.
- **Follow-on candidates:** thermal-front model of the sublimation draw (does port rotation symmetrize passively?); coupled wobble/slosh of chunk-in-bag under gimbal transients (Basilisk sim material, `water-prop/sims/`).
