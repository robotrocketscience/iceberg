# R-aerocapture-fast-cruise-envelope — does Round F's STRICT-closing Variant C cell survive Earth aerocapture engineering envelope?

**Author:** hyperion (post-STOP override session, 2026-05-15).
**Status:** pre-result (hypothesis pre-registered with central estimates computed BEFORE range, per recurring-lesson #N intervention).

---

## Motivation

Round F (`R_cruise_time_optimization`) reported that Variant C at faster-than-Hohmann cruise (aphelion radius 10.5–11 astronomical units, cruise 4.2–4.4 years each leg) closes the strict 15-year level-zero requirement L0-05 with delivered mass 23.5–26 tonnes per mission and round-trip 12.7–13.1 years. Every closure verdict in batches 2 and 3 of this hyperion session folds into "Variant C closes IF Earth aerocapture works for the chunk + tug stack."

The aerocapture assumption was previously analysed in `R_chunk_as_heat_shield` at entry velocity 12.6 kilometres-per-second and entry mass ~100 tonnes, giving 0.5 percent chunk ablation and a closure verdict. Two architectural shifts since then make that envelope no longer applicable:

1. The current closing cell uses 200-tonne chunks (versus the 100-tonne assumption in R-chunk-as-heat-shield).
2. Round F's faster cruise pushes Earth-arrival velocity-at-infinity higher than Hohmann, raising the entry velocity by 10–25 percent over the prior assumption.

This round computes whether the entry-velocity-and-mass envelope of the Round F STRICT-closing cell sits inside or outside the chunk-as-heat-shield engineering envelope established by R-chunk-as-heat-shield. If outside, Round F's STRICT closure verdict has been falsified at the engineering level even though it closes at the trajectory level.

---

## Pre-registered hypothesis (H-afce)

### Recurring-lesson-#N anchor: central estimates COMPUTED BEFORE range

Per the batch-3 handoff recommendation, central numerical estimates were derived first (back-of-envelope, in conversation, before this hypothesis was named). Range bands wrap each anchor.

**Back-of-envelope anchors (computed first):**

| Quantity | Anchor (computed BEFORE range) | Source of anchor |
|---|---|---|
| Entry velocity at aphelion 11 astronomical units, no lunar-gravity-assist credit | 15.4 kilometres-per-second | sqrt(v_∞² + v_escape²), v_∞ = 40.33 − 29.78 = 10.55 |
| Entry velocity at same, with 2 kilometres-per-second lunar-gravity-assist credit | 14.1 kilometres-per-second | sqrt(8.55² + 11.18²) |
| Entry mass | 263.8 tonnes | 200 chunk + 63.8 tug from Round F output |
| Ballistic coefficient | 5500 kilograms-per-square-metre | mass / (drag-coefficient × frontal-area), water-ice sphere geometry, drag-coefficient 1.0 |
| Sutton-Graves peak heat flux ratio versus R-chunk-as-heat-shield 12.6 kilometres-per-second case | 1.83× | (15.4 / 12.6)³ |
| Predicted peak heat flux | 330 watts-per-square-centimetre | R-chunk-as-heat-shield 180 watts-per-square-centimetre × 1.83 |
| Predicted ablation per pass | 0.9 percent | R-chunk-as-heat-shield 0.5 percent × (15.4/12.6)² for total heat load |
| Average deceleration over 200-second pulse | 3.9 g | (15.4 − 7.7) / 200 / 9.81 |
| Peak g-load (estimated 2.5× average) | 10 g | empirical ratio for hypersonic atmospheric capture pulses |
| Chunk internal stress at peak g | 343 kilopascals | chunk-radius × density-ice × peak-g |
| Ice tensile strength (literature) | 1000 kilopascals | textbook value for cold polycrystalline ice |
| Margin against tensile failure | 2.9× | 1000 / 343 |

### Sub-claim ranges (anchored to central estimates)

| Sub-claim | Central estimate | Predicted range (sub-claim H-afce-N) | Falsification threshold |
|---|---|---|---|
| H-afce-a — entry velocity at aphelion 11 astronomical units, no lunar-gravity-assist | 15.4 kilometres-per-second | 14.5–16.5 | outside range |
| H-afce-b — peak heat flux at H-afce-a entry velocity, chunk geometry | 330 watts-per-square-centimetre | 200–500 | outside range |
| H-afce-c — chunk ablation per single-pass aerocapture | 0.9 percent | 0.4–2.5 | outside range |
| H-afce-d — peak deceleration during pulse | 10 g | 5–18 | outside range |
| H-afce-e — chunk internal stress versus ice tensile strength | margin 2.9× | margin 1.5–6 | margin outside range |
| H-afce-f — Round F STRICT closure delivered-mass adjustment after aerocapture losses | minus 1.0 percent | minus 0.5 to minus 4.0 percent | outside range OR architecture infeasible |
| H-afce-g — periapsis altitude needed for full capture from velocity-at-infinity 10.55 kilometres-per-second at ballistic coefficient 5500 kilograms-per-square-metre | 60 kilometres | 50–75 | outside range |

### Aggregate (H-afce-agg)

Round F's STRICT-closing cell at aphelion 11 astronomical units survives the aerocapture engineering envelope. Ablation under 1 percent. Chunk structural integrity holds with about 3× margin over ice tensile failure. Periapsis altitude required is in the standard low-Earth-orbit-aerobraking band (50–75 kilometres). Delivered mass adjusts by less than 3 percent.

If H-afce-agg holds, Round F's closure verdict is robust and the matrix can quote 23–26 tonnes delivered per mission for Variant C at faster cruise.

If H-afce-agg is falsified — particularly in sub-claims b, c, d, or e — the matrix's surviving cell has been falsified at the engineering level and a slower cruise (Hohmann or near-Hohmann) is the only candidate that survives both the trajectory closure AND the aerocapture envelope. Slower cruise costs round-trip time and may push the cell outside L0-05 strict, returning it to the soft-margin regime.

### Recurring-lesson watchpoint

Hyperion's pre-registration intuition has been falsified in the same direction (architectures fail to close) six times this session. This round pre-registers a closure-supporting prediction (Round F survives envelope). If this is wrong, the recurring lesson updates: hyperion's intuition is biased toward closure being marginal; reality is "closes cleanly" or "fails completely" with no marginal middle.

---

## Method

Deterministic single-pass aerocapture envelope check across the Round F transfer-time grid (aphelion radius 9.58, 10.5, 11.0, 12.0, 14.0 astronomical units), at entry mass {100, 200, 263.8, 350} tonnes, with and without 2 kilometre-per-second lunar gravity assist credit.

### Computations per (aphelion, mass, lunar-gravity-assist-state) tuple

1. **Heliocentric perihelion velocity** at Earth orbit from Round F config (vis-viva).
2. **Velocity-at-infinity** at Earth: v_∞ = v_perihelion − v_Earth − optional 2 kilometres-per-second lunar-gravity-assist credit.
3. **Entry velocity** at atmospheric interface (125 kilometres altitude): v_e = sqrt(v_∞² + v_escape²), v_escape at Earth interface = 11.18 kilometres-per-second.
4. **Frontal area** assuming spherical chunk of liquid-water-equivalent density (917 kilograms-per-cubic-metre). Tug shielded behind chunk; tug area not added.
5. **Ballistic coefficient** β = mass / (drag-coefficient × frontal-area). Drag-coefficient = 1.0 for blunt body in hypersonic flow.
6. **Required periapsis altitude** for capture: solve density-altitude such that integrated drag delta-velocity equals (v_e − v_circular-at-low-Earth-orbit). Use exponential atmosphere with scale height 7.5 kilometres above 80 kilometres, density-at-100-kilometres = 5.6 × 10⁻⁷ kilograms-per-cubic-metre, Earth radius 6378 kilometres. Approximate pulse duration as 2 × periapsis-radius / horizontal-velocity-at-periapsis.
7. **Sutton-Graves stagnation-point heat flux**: q_peak = K × sqrt(rho_periapsis / nose-radius) × v_e³, K = 1.7415 × 10⁻⁴ in international-standard units, nose radius = chunk radius.
8. **Total heat load per pass**: integrate q over pulse duration.
9. **Chunk ablation**: total heat load divided by water heat-of-vaporization 2.26 megajoules-per-kilogram, assuming all peak heat conducts into the surface ablation layer. Conservative upper bound on ablation; actual would be lower due to radiative re-emission.
10. **Peak deceleration**: (v_e − v_circular) / pulse-duration × empirical-peak-factor 2.5.
11. **Chunk internal stress** at peak g: chunk-radius × density × peak-g-acceleration.

### Cross-check against R-chunk-as-heat-shield

For the (aphelion 9.58, mass 100, with-lunar-gravity-assist) case the entry velocity should match R-chunk-as-heat-shield's 12.6 kilometres-per-second within rounding. If the cross-check matches, the new computations at higher mass and velocity are anchored to a known-validated point. If not, the model is broken and the round must regress to find the discrepancy.

### Outputs

- `results/R_aerocapture_fast_cruise_envelope.json` — full per-tuple results.
- `results/tables.md` — human-readable tables for each sub-claim.
- `results/closure_verdict.md` — does Round F's aphelion-11 closing cell survive the envelope? Single-paragraph verdict.

---

## Validity caveats

1. **Sutton-Graves is stagnation-point only.** Real heat flux distribution over a 3.74-metre-radius blunt body has off-axis attenuation; integrating q × area gives lower total than peak × area. The round uses peak-only as conservative upper bound.
2. **Drag coefficient 1.0 for irregular chunk is approximate.** Real B-ring chunks are rubble piles; drag coefficient could be 0.6–1.4 depending on shape orientation. Dial chosen as central blunt-body value.
3. **Tug-survival assumed conditional on chunk-forward orientation.** This round does NOT close the orientation-stability question (R-chunk-as-heat-shield-revisit's binding open question). If chunk tumbles, tug burns up and "delivered-mass" goes to zero. This round assumes the orientation question closes.
4. **Single-pass aerocapture only.** Multi-pass aerobraking would split delta-velocity and reduce per-pass heat flux but extends mission duration by months. Out of scope.
5. **Lunar gravity assist credit** at 2 kilometres-per-second is the matrix's standing value; depends on lunar-Earth-Saturn geometry at arrival. Some arrival epochs give 0 credit (worst case examined as no-lunar-gravity-assist branch).
6. **Exponential atmosphere with single scale height** is approximate above 100 kilometres; real density profile has two-scale behaviour. Periapsis altitude estimate has roughly ±5 kilometres error.
7. **Water heat-of-vaporization** is the conservative ablation enthalpy. Real ice may sublime at the lower 2.83 megajoules-per-kilogram heat-of-fusion-plus-vaporization in vacuum (slightly more conservative). Difference is within model uncertainty.
8. **Variant C tug mass at 500 kilowatt-electric** taken as 63.8 tonnes from Round F output, which uses MARVL-anchored mass. If MARVL parameters shift (locked-finding-4 envelope), tug mass varies ±15 tonnes which changes ballistic coefficient by ±5 percent.

---

## Test

`run.py`. Deterministic. Sub-second wall clock. No randomness.

---

## Revisit clause (to be filled after run)

To be completed in the Reading section of `run.py` output / `results/closure_verdict.md`. Will grade each sub-claim against the predicted range, name the recurring-lesson update if any, and list follow-on rounds if engineering envelope is breached.
