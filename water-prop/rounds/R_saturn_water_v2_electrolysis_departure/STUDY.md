# R-saturn-water-v2-electrolysis-departure — STUDY (pre-registration)

**Worker:** worktree-172651, 2026-07-26, immediately following
R-closure-boundary-inversion (`5d5f08d`). This encodes the latest+28 named
follow-on — "saturn_water_v2 with the H₂/O₂ departure stage" — that
R-electrolysis-departure-stage established analytically (reactor 1,248 →
146–437 kWe, delivery 6.1% → 12.7%) but which was never wired into the
mission-graph framework. The boundary round's Arm-B result motivates it
sharply: under honest spiral physics the 30-t floor needs Isp 3,000 s hardware
that does not exist; an impulsive Oberth departure burning ISRU-electrolyzed
H₂/O₂ at chemical Isp is the one architecture that sidesteps that requirement.

## Encoding (framework change, defaults inert)

1. **`missions/phase4_electrolysis.py`** — new Phase-4 option
   `electrolysis_kick_departure`: over a Saturn dwell the reactor electrolyzes
   chunk water into H₂/O₂, then a single impulsive periapsis burn
   (`electrolysis_tei_dv_km_s`, default **8.51 km/s** — Oberth-optimized anchor
   from R-eccentric-harvest-departure / R-electrolysis-departure-stage) at
   `electrolysis_isp_s` (default **450 s**, LH₂/LOX vacuum class). Propellant is
   drawn from the chunk (`payload_kg`). Gates: production time =
   propellant × `electrolysis_energy_kwh_per_kg` / power ≤
   `electrolysis_max_dwell_years` (defaults **6.7 kWh/kg** — 20 MJ/kg
   electrolysis at ~70% efficiency + ~1.1 kWh/kg liquefaction with mandatory
   ortho-para catalysis, per R-cryo-hydrogen-storage-saturn and the DOE
   liquefaction-cost literature — and **3 yr** dwell); reactor-lifetime hook
   charged with the full production hours; solar-thermal excluded at Saturn.
   Arrival v_inf 10 km/s (Hohmann return, same as chemical TEI), coast 6.5 yr
   plus the dwell.
2. **`saturn_mass_demands.py`** — `MassContext` gains `electrolysis_stage`
   (default False → byte-identical v1 behavior), `electrolysis_plant_kg_per_kwe`
   (**20 kg/kWe**, PEM stack + liquefier first-pass; vendor anchor deferred) and
   `electrolysis_cryo_tank_fraction` (**0.06** of the P4 propellant estimate,
   composite H₂+O₂ cryo tankage; R-electrolysis-departure-stage carried 5%
   jettisonable). The cryo-tank demand is dry-mass-dependent (propellant estimate
   = f_burn × (trial dry + chunk)) and joins the fixed-point like tankage.
3. **`missions/saturn_water_v2.py`** — mission clone of v1 with Phase 4 swapped
   for the extended phase (all three v0 options retained + the new one), same
   closure predicates, derived-mass transform setting `electrolysis_stage=True`.

**Not modeled (pre-registered exclusions):** tank jettison after the burn
(conservative — dry mass keeps the empty tanks; the analytic round jettisoned
34.5 t), boiloff during the return coast (R-cryo-hydrogen-storage found 0.35%/2 yr
passive at Saturn given the shadow-shield constraint — treated as met), the
reactor-shadow placement constraint itself (a design requirement, not a mass
term at this fidelity), and just-in-time electrolysis (killed analytically:
887–5,325 kWe).

## Hypotheses

| # | Hypothesis | Gate | Prediction |
|---|---|---|---|
| H-V1 | v2 restores ≥1 `arrived_at_depot` path under Arm-B honest physics at ≤200 kWe and ≤33 W/kg with launch elastic (multiplier ≤8) | 0 closures falsifies | Holds — the analytic round's 146–437 kWe band, now with the P0 wall bought off by the multiplier |
| H-V2 | At matched cells the electrolysis stage beats the electric spiral on delivered mass under Arm B | spiral ≥ electrolysis at all closing cells falsifies | Holds at ≤150 kWe (spiral is power-starved there) |
| H-V3 | The modal failure phase for v2 paths shifts from P4 to P6 (hot 10 km/s arrival: vis-viva capture needs ~7.3 km/s chemical, LGA tour trim ~4.2) | P4 still modal falsifies | Holds — R8's arrival wall re-emerges once departure is solved |
| H-V4 | Under Arm B + launcher ×5 + record specific power (2.4 W/kg), v2 closes the 30-t floor at chunk ≥200 t and power ≥100 kWe WITHOUT any Isp advance (450 s chemical) | no 30-t closure falsifies | **The load-bearing test: does ISRU chemistry substitute for the nonexistent 3,000-s thruster?** Prediction: holds at waiver ceiling, marginal at strict |
| H-V5 | At 30 kWe the 3-yr dwell gate binds (Kilopower cannot electrolyze fast enough) | 30-kWe closures with dwell ≤3 yr falsify | Holds — reproduces "not Kilopower" from the analytic round |

## Method

Sweep saturn_water_v2 with the boundary round's oracle harness: power
{30, 55, 100, 150, 200} kWe × chunk {50, 100, 200, 300, 500} t × thrust
{2.5, 10, 25} N; arms A/B as in the boundary round; launcher multiplier
{1, 5, 8}; delivered-floor predicates 10/30 t; v2-vs-v1 matched comparison at
identical parameters. Regression: v1 sweep and full test suite unchanged
(electrolysis_stage defaults False).
