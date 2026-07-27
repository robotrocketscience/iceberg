# R-closure-boundary-inversion — STUDY (pre-registration)

**Worker:** worktree-172651 (project-owner-directed "full audit … run r&d rounds and
lets try to close this realistically and economically … make a list of the
performance parameters that would need to be improved"), 2026-07-26, latest+28
baseline (`b9cb6d6`). No SCOPE predecessor — this round was born directly from the
project-owner directive; the audit pass that seeded it (six-reader sweep + wonder
dispatch, this session) stands in for the SCOPE survey.

## Question

The closed-loop framework returns **0 closures out of 1,744 enumerated paths**
(R-l0-relaxation-envelope, latest+28) at the record technology baseline. This round
INVERTS the question: instead of asking "does the mission close at parameter set X,"
ask **"what is the minimum value of each performance parameter — and the minimum
joint scenario — at which at least one path closes?"** The output is the
closure-boundary map the project owner asked for: required specific impulse,
power class, specific power, launcher capacity, capture scale, propellant-fraction
posture — each stated as a threshold with the wall it moves.

## Method

Oracle: `run_grid(power_values, chunk_values, thrust_values, extra_params)` — the
saturn_water_v1 closed-loop sweep (derived dry mass, Picard fixed point, launch
wet = dry/(1−f)). One oracle call = one full grid walk (~0.1 s measured; bisection
budget is unconstrained). Closure metrics per call: `arrived_at_depot`,
`delivered_floor_10t` (demonstrator floor), `delivered_floor` (30 t commercial
shorthand), plus max delivered payload and per-phase failure taxonomy.

**Framework change (pre-registered):** the hardcoded walls are converted to
`params.get(name, DEFAULT)` hooks with DEFAULTS BYTE-IDENTICAL to the record —
launcher caps (`launcher_cap_multiplier`, scales Falcon Heavy 63.8 t / Starship
100 t / multi-FH 50 t-per-launch / 300 t kick manifest together), Saturn-departure
delta-v anchors (`chemical_tei_dv_km_s` 7.7, `chunk_fed_dv_km_s` 9.0), minimum-power
gates (`low_thrust_min_power_kwe` 20, `chunk_fed_min_power_kwe` 30,
`lt_capture_min_power_kwe` 30 at P6), and the phase-7 water-MET Isp propagation leak
(hardcoded 800 s → reads `water_met_isp_s`). Kick-stage residual burns honor
`tsi_hohmann_dv_km_s`. Regression gate: full test suite green AND the record
150-cell/1,744-path/0-closure baseline reproduces exactly with no extra params.

**Postures (both reported for every threshold):**
- **Arm A (record):** constraint toggles as in the 0/1,744 record — legacy
  Earth-capture dv formula, no reactor-lifetime cap, chunk-fed departure at the
  optimistic 9.0 km/s anchor. Thresholds under Arm A are LOWER BOUNDS on required
  performance.
- **Arm B (honest):** `visviva_capture=True` (physically correct Earth-capture
  burn), `chunk_fed_dv_km_s=18.0` (Edelbaum spiral band per
  R-spiral-out-exit-architecture; the 9.0 anchor books Oberth benefit a
  continuous-thrust spiral does not get), `reactor_lifetime_years=10` (Kilopower
  design target). Arm B is the defensible headline; the A→B delta is itself a
  finding.

**Stages:**
1. Monotonicity spot-check (3 points per axis), then per-axis bisection to ~2%
   with all other axes at record baseline. Axes: `water_met_isp_s` [800, 20,000 s],
   `electric_isp_s` [3,000, 20,000 s], `chemical_isp_s` [340, 480 s],
   `launcher_cap_multiplier` [1, 16], `reactor_specific_power_w_per_kg`
   [2.4, 400 W/kg], `capture_efficiency_multiplier` [0.25, 1.0], power grid
   extension [1, 1,000 kWe].
2. Dense scans on the declared-non-monotone axes: `propellant_fraction`
   [0.05, 0.90] step 0.025; chunk mass [0.5 t, 500 t] (includes the never-computed
   demonstrator-scale 0.5–5 t grid).
3. Pairwise 2-D boundary maps around any thresholds found: (water-MET Isp × power),
   (specific power × launcher multiplier), (propellant fraction × launcher
   multiplier).
4. Named joint scenarios (the owner-legible deliverable): S1 Starship-refill launch
   elasticity alone; S2 +propellant-fraction optimum; S3 +NSTM-3-class reactor
   (100 kWe, 33 W/kg); S4 +water-MET at measured ceiling (900 s); S5 +RF-ion-class
   2,000 s on filtered water; S6 honest-arm replays of S1–S5; S7 demonstrator grid
   (0.5–5 t chunk, 1–20 kWe, single launcher).
5. Scalar λ-bisection along the baseline→aspirational-2035 direction (launcher ×5,
   specific power 2.4→40 W/kg, water-MET 800→3,000 s, f 0.80→0.36): smallest λ
   that closes = "fraction of the way to aspirational tech."

## Hypotheses

| # | Hypothesis | Gate | Prediction |
|---|---|---|---|
| H-B1 | No SINGLE parameter within its bracket restores ≥1 `arrived_at_depot` path (others at record) | any single-axis threshold found falsifies | **Holds** — the walls are joint (P0 launch mass, P1 power/burn-time, P4 departure); e.g. launcher multiplier alone leaves P4 propellant-starved at 800 s |
| H-B2 | With launch elastic (multiplier ≤ 8), the water-MET Isp threshold for chunk-fed departure closure sits at 1,200–4,000 s (Arm A) | threshold outside band, or none ≤ 20,000 s, falsifies | Tsiolkovsky prior: deliver ≥30 t from a 200 t chunk at 9 km/s from m0 = dry+chunk needs ≈1,200 s; keep-50% needs 2,500–3,800 s; Arm B roughly doubles it |
| H-B3 | At the H-B2 threshold, minimum power sits at 50–200 kWe (burn-time gate), i.e. above every flyable class and below the megawatt band | threshold < 50 or > 200 kWe falsifies | burn energy m·ve²/2 against the 90%-of-transit window |
| H-B4 | Raising reactor specific power ALONE (2.4 → 400 W/kg) does not close anything | closure falsifies | it shrinks dry mass but no gate on Isp/power class moves |
| H-B5 | No single `propellant_fraction` value closes (chemical legs want f ≥ 0.85, electric legs want f ≤ 0.4) | closure at any f falsifies | the scan should show the two regimes never overlap at record Isp |
| H-B6 | The demonstrator-scale grid (0.5–5 t) does NOT close at record technology (fails at P4), but closes at ≥30 kWe + water-MET ≥ ~1,000 s with single-Starship launch | no-closure everywhere, or closure at record tech, falsifies | small chunks fit the launcher (wet ~80–90 t) and fail only the departure |
| H-B7 | At least one named joint scenario (S1–S6) built ONLY from named-program 2030s levers (Starship refill, NSTM-3 100 kWe/33 W/kg, ≤2,000 s water-compatible Isp) closes ≥10 t delivered under the 25-yr waiver | all scenarios 0 falsifies | this is the "what it would take" list; prediction: S5-class (RF-ion Isp) required, S4 (900 s MET) insufficient |

## Deviations (pre-registered)

- **D-1:** Arm A inherits the record's optimistic toggles (legacy Earth-capture
  formula, lifetime off) — published Arm-A thresholds are lower bounds, stated as
  such. Arm B carries the honest posture.
- **D-2:** Delta-v anchors are parameterized, not re-derived; the 9.0-vs-18 km/s
  chunk-fed discrepancy is carried as the A/B split, not resolved here (named
  follow-on: Basilisk/Edelbaum check from the actual residence orbit).
- **D-3:** No ISRU processing-rate axis — it does not exist in the framework; the
  electrolysis departure stage (which forces it) is the companion round
  R-saturn-water-v2-electrolysis-departure, executed after this one.
- **D-4:** Thrust axis retained at the record grid values; power-thrust consistency
  (F ≤ 2P/ve) is NOT enforced by the framework in P1 — inherited limitation,
  flagged where it flatters a threshold.
- **D-5:** Aerocapture payload caps (30 t / 100 t hybrid) stay fixed — they are
  falsification-anchored (phoebe rounds), not tunable performance parameters. The
  drag-skirt lever stays project-owner-gated.

## Priors disclosed

Walls arithmetic (audit pass, this session): smallest self-consistent wet vehicle
138 t vs largest encoded launch option 300 t raw (six-Falcon-Heavy; the FINDINGS'
382 t figure was a wrong per-launch cap — corrected in this round's record);
burning the ENTIRE 200 t chunk at 800 s yields 7.66 km/s < the 9.0 km/s anchor;
chemical TEI needs propellant fraction 0.90 of the chunk-laden stack. Single-lever
fixes should therefore all fail; the interesting output is the joint minimum.
