# R-hybrid-solar-augmentation — reactor plus deployable solar array along the trajectory

**Status:** pre-result.

## Question

R-power-wonder treated solar as "dead at Saturn." That collapses two different questions into one. Standalone solar at 9.58 astronomical units delivers 1.09 percent of Earth flux and is indeed dead. But a hybrid that adds a deployable solar array to a reactor-class power bus passes through every heliocentric distance from 1 to 9.58 astronomical units along an inbound or outbound spiral; the solar contribution at the inner-system phase is large.

User raised this directly: "size an array that maybe in the beginning when it's inbound from Saturn it's relying on the nuclear power, but as it gets closer and closer to Earth, the solar panels can provide more and more power and therefore more and more thrust." This round tests the magnitude of that effect.

The interesting cross-question is whether the hybrid pays at Kilopower-class power (1–10 kilowatts-electric, the most defensible ICEBERG mission tier per R-power-base-rate) or only at higher power classes — and whether the array's mass cost is recoverable from chunk-mass gain.

## Pre-registered hypotheses

See `HYPOTHESES.md` § R-hybrid-solar-augmentation for the full block.

Summary:
- H-hsa-a: gain factor at 10 kilowatt-electric reactor plus 200 square-meter array ∈ [1.5, 2.2]
- H-hsa-b: gain factor at 100 kilowatt-electric reactor plus same array ∈ [1.05, 1.20]
- H-hsa-c: gain factor at 1000 kilowatt-electric reactor plus same array ∈ [1.00, 1.02] (negligible)
- H-hsa-d: reactor power class below which hybrid gain exceeds 1.5 ∈ [15, 40] kilowatts-electric
- H-hsa-e: net chunk-mass deliverable gain at 10 kilowatt-electric Kilopower plus 200 square-meter array, array dry-mass penalty subtracted ∈ [25, 55] percent
- H-hsa-f: areal density break-even ∈ [6, 15] kilograms per square meter (Roll-Out Solar Array is ~3)
- H-hsa-g: concentrated-burn-at-Earth-vicinity gain (single-point at 1.2 astronomical units) ∈ [4.0, 6.5]

Aggregate (H-hsa-agg): the hybrid is a Kilopower-class enabler, not a megawatt-class strategy. At Kilopower scale the harmonic-mean power gain is substantial; at megawatt scale it is negligible because the fixed array becomes proportionally insignificant.

## Method

**Trajectory model.** Continuous-thrust low-thrust spiral following Edelbaum's circular-to-circular approximation. At heliocentric distance r, the spacecraft is in a near-circular orbit with circular velocity v_c(r) = sqrt(mu_sun divided by r). Tangential thrust changes v_c at rate a(r) = 2 times P(r) times eta_thruster divided by (m times v_exhaust). The time spent traversing radial bin dr along the spiral is

  dt(r) = (one half) times sqrt(mu_sun) times r raised to negative one-and-a-half divided by a(r) times dr

Because a is proportional to P, dt scales as one-over-P times r-to-the-negative-one-and-a-half. The time-averaged power over the trajectory is therefore

  P_avg_time = integral of P(r) times dt(r) divided by integral of dt(r)
             = integral of r-to-the-negative-one-and-a-half divided by integral of (r-to-the-negative-one-and-a-half divided by P(r))

This is the harmonic mean of P weighted by r-to-the-negative-one-and-a-half. It is the quantity that determines mission burn duration at fixed propellant load: T_burn = m_prop times v_exhaust squared divided by (2 times P_avg_time times eta).

**Power model.**
- Reactor: P_reactor constant.
- Solar array: P_array(r) = P_array_at_1AU times (1 over r-squared) times eta_low_intensity_low_temperature(r), where eta_low_intensity_low_temperature drops linearly from 1.0 at 1 astronomical unit to 0.79 at 9.58 astronomical units per Juno mission data extrapolation.

**Sweeps.**
- Reactor power class: 1, 3, 10, 30, 100, 300, 1000 kilowatts-electric.
- Array size: 50, 100, 200, 400, 800 square-meters.
- Array areal density: 1, 3, 6, 10, 15, 20 kilograms per square meter (current Roll-Out Solar Array is ~3).
- Trajectory direction: inbound (9.58 to 1 astronomical unit) and outbound (1 to 9.58); these are symmetric for the harmonic-mean calculation.

**Chunk-mass-deliverable model.** Use the conops heuristic (1 kilowatt-electric supports ~25 tonnes of delivered chunk over the 7-year inbound coast) as the first-order chunk-vs-power relationship. Scale chunk linearly with P_avg_time. Subtract array dry mass from the deliverable budget. This is a deliberately simple chunk model; a more honest treatment would solve Tsiolkovsky directly per mission tier (deferred to a future round).

**Concentrated-burn case (sub-claim g).** Some inbound trajectories are not continuous spirals — they Hohmann-coast for most of the trip and concentrate the burn at one location, typically near Earth arrival where the velocity change is most efficient. Sub-claim g evaluates the hybrid gain at a single radial distance of 1.2 astronomical units (representative of an Earth-vicinity boost burn). At that distance the solar contribution dominates the reactor contribution, so the gain factor is much larger than the trajectory-averaged value.

## Validity caveats

1. **Edelbaum is a circular-to-circular approximation.** Real ICEBERG inbound is from Saturn-bound elliptical orbit with significant impulsive components. The continuous-thrust spiral over-represents the burn duration; the harmonic-mean derivation is an upper bound on the trajectory-time-averaging effect. A bunched-burn architecture would have different gain dynamics, captured separately in sub-claim g.

2. **Linear low-intensity low-temperature derate is an approximation.** Real photovoltaic cell behavior at outer-system temperatures and irradiances is non-linear and cell-chemistry-specific. Juno data at 5.2 astronomical units is the deepest-space anchor; beyond that the derate is extrapolation. A more conservative derate (e.g., a 0.6 floor) would reduce outer-system solar contribution but barely affect the harmonic-mean result, because the harmonic mean is dominated by where power is smallest, which is the outer system regardless.

3. **Array dry-mass attribution is per-array-mass only.** Does not include attitude-control penalty, deployment mechanism, thermal management, or end-of-life degradation. Real total dry-mass cost is likely 30–50 percent higher than the cell-and-substrate mass alone.

4. **Chunk-mass linear-scaling-with-power heuristic is unsourced internally.** Per the gap analysis from R-power-wonder block-2 finding, the "1 kilowatt-electric per 25 tonnes of delivered chunk" figure in `startup/ICEBERG-pitch.md` is not derived from any specific round. A more rigorous chunk-mass model solves Tsiolkovsky directly given specific impulse, propellant fraction, and time budget. Deferred.

5. **200-square-meter array size matches state-of-the-art deep-space arrays.** Lucy mission is ~84 square meters; Europa Clipper ~102 square meters. A 200-square-meter array at Saturn would be the largest deep-space array ever flown by a factor of two. Sensitivity to size is reported.

6. **No eclipse modeling.** During Earth-vicinity spiral phases the spacecraft can spend significant time in Earth shadow, reducing effective solar power. This penalty does not exist on the cruise leg (outside Earth's hill sphere) but does affect the boost-burn case.

## Result

Ran the closed-form trajectory integration over a 1000-point radial grid from 1 to 9.58 astronomical units. Full summary: `results/R_hybrid_solar_augmentation_summary.json`.

**Reactor-power sweep** (200-square-meter array, 60-kilowatts-electric at 1 astronomical unit):

| Reactor (kilowatts-electric) | Reactor-only P-avg | Hybrid P-avg-time | Gain factor |
|---|---|---|---|
| 1 | 1.00 | 6.22 | 6.22 |
| 3 | 3.00 | 9.89 | 3.30 |
| 10 | 10.00 | 19.71 | 1.97 |
| 30 | 30.00 | 42.71 | 1.42 |
| 100 | 100.00 | 115.36 | 1.15 |
| 300 | 300.00 | 316.67 | 1.06 |
| 1000 | 1000.00 | 1017.25 | 1.02 |

**Pre-registration grading:**

| Sub-claim | Predicted range | Measured | Held? |
|---|---|---|---|
| H-hsa-a — gain at 10 kilowatts-electric | 1.5–2.2 | 1.97 | HELD |
| H-hsa-b — gain at 100 kilowatts-electric | 1.05–1.20 | 1.15 | HELD |
| H-hsa-c — gain at 1000 kilowatts-electric | 1.00–1.02 | 1.02 | HELD |
| H-hsa-d — reactor class at gain-equals-1.5 | 15–40 kilowatts-electric | 24.4 | HELD |
| H-hsa-e — net chunk-mass deliverable gain at Kilopower | 25–55 % | 96.8 % | FALSIFIED-optimistic |
| H-hsa-f — array areal density break-even | 6–15 kilograms per square meter | 9.7 | HELD |
| H-hsa-g — concentrated-burn-at-1.2-astronomical-units gain | 4.0–6.5 | 5.15 | HELD |

Aggregate (H-hsa-agg) held strongly: the hybrid is a Kilopower-class enabler. Gain factor of nearly 2 at 10 kilowatts-electric reactor, dropping to negligible at megawatt class. The 1.5-gain threshold sits at 24.4 kilowatts-electric reactor power.

## Reading

The harmonic-mean trajectory averaging is more favorable to the hybrid than my pre-registration anticipated. At 10 kilowatts-electric Kilopower plus a 200-square-meter array (60-kilowatts-electric at 1 astronomical unit), the trajectory-time-averaged effective power is 19.7 kilowatts-electric — essentially doubling the reactor's standalone contribution. The mechanism is that the inner-system phase of the trajectory carries a 7-times-larger power, and the trajectory weighting (r raised to negative one-and-a-half from Edelbaum spiral dynamics) does not heavily discount that region.

The architectural pattern is clean: for any reactor class below ~25 kilowatts-electric, adding a state-of-the-art Roll-Out Solar Array delivers more than 50 percent gain in effective trajectory power. For reactor classes above ~100 kilowatts-electric, the fixed array contribution is dilute and the gain falls below 15 percent. The crossover is exactly the boundary between the Kilopower era (per the architecture matrix, year 0 to year 7) and the Fission Surface Power era (year 7 to year 13). The hybrid maps onto the Kilopower mission tier.

The chunk-mass-deliverable gain at Kilopower (sub-claim e) measured 96.8 percent — the array nearly doubles deliverable chunk. This is because the 600-kilogram array dry-mass penalty is small compared with the 250-tonne reactor-only chunk that the conops heuristic projects. Subtracting 0.6 tonnes from 493 tonnes barely registers. My pre-registered 25–55 percent range was conservative because I implicitly weighted the array mass penalty too heavily relative to the chunk-power scaling factor.

The break-even array areal density of 9.7 kilograms per square meter (sub-claim f) is comfortably above current Roll-Out Solar Array technology (~3 kilograms per square meter). The hybrid wins by a 3-times margin against a same-mass larger pure reactor at Kilopower scale.

The concentrated-burn case (sub-claim g, gain 5.15 at 1.2 astronomical units) is a useful upper bound for architectures that bunch the inbound burn near Earth rather than spiraling continuously. If ICEBERG inbound is more bunched than continuous, the hybrid gain is even larger than the spiral-averaged value.

## Revisit

**Pre-registration bias direction: pessimistic on chunk-mass gain (H-hsa-e), correct elsewhere.** Six of seven sub-claims held. The one falsification was on the bullish side — chunk gain was nearly twice my upper bound. This is the opposite direction from R-power-base-rate's pre-registration bias (which was uniformly too optimistic on program-completion probabilities). The pattern: when ranging chained-multiplicative chains (R-power-base-rate), I am over-bullish; when ranging single-physical-mechanism scaling (R-hybrid-solar-augmentation chunk-from-power), I am over-bearish.

**Validity caveat 4 is load-bearing for sub-claim e.** The "1 kilowatt-electric per 25 tonnes of delivered chunk" heuristic from the conops is unsourced internally and is what carries the chunk-gain prediction. If the heuristic over-states the chunk-per-power ratio by a factor of 2, then the chunk gain falls to ~50 percent, which is still architecturally significant but no longer near-doubling. A future round should derive chunk-mass directly from Tsiolkovsky for the Kilopower-era mission tier with measured specific impulse and time budget, and revisit this sub-claim against that derivation.

**Validity caveat 1 (Edelbaum approximation) is the second-largest sensitivity.** The continuous-thrust spiral over-represents burn duration compared with bunched-burn architectures. If the real ICEBERG inbound concentrates burn near Earth, sub-claim g's gain factor (5.15) is the relevant number rather than the spiral-averaged sub-claim a (1.97). Both favor the hybrid, but the magnitude differs substantially. Cross-reference to R10b-thruster-per-power-class and R8-inbound-dv-budget for the burn architecture they assume.

**Validity caveat 3 (incomplete array mass attribution) likely shifts sub-claim e downward by 30–50 percent.** Including attitude-control margin, deployment mechanism, thermal management, and end-of-life degradation pushes effective array mass toward 1.0–1.5 tonnes rather than 0.6. Even at 1.5 tonnes, the chunk gain remains around 90 percent — still well above my pre-registered upper bound. The qualitative finding holds; the quantitative number softens by a few percent.

## Cross-learning

- **Positive for ICEBERG-pitch.md Kilopower-only floor case.** The pitch's "single-ship-per-window: 50 tonnes times $1,400 per kilogram equals $370 million per year" line could become "single-ship-per-window with solar augmentation: 100 tonnes per ship at the same launch cost" — a doubling of the floor-case revenue. Architecture impact: the Kilopower-only floor case shifts from $370 million per year to approximately $700 million per year per ship; the multi-ship cadence floor of $1.0–1.2 billion per year shifts to approximately $2 billion per year. The Kilopower-only floor case becomes competitive with the original Fission Surface Power scenario.
- **Negative for matrix megawatt-era rows.** Hybrid augmentation does not help the megawatt-class architecture. Combined with R-power-base-rate's finding that megawatt arrival by year 20 has 0.5 percent probability, the megawatt rows lose their primary justification (they were the high-throughput tier) without a fallback strategy. The hybrid promotes the Kilopower tier to handle the high-throughput case.
- **Methodology lesson candidate (campaign-level).** Asymmetric pre-registration bias: I am over-bullish on chained-multiplicative chains (R-power-base-rate) and over-bearish on single-physical-mechanism scaling (this round's H-hsa-e). Both are correctable by computing the product or scaling of central estimates first and then ranging around it, but the *direction* of error is opposite. Adding this to the cross-campaign lesson log per CONVENTIONS section 9.5.
- **Negative for `startup/ICEBERG-pitch.md` Section 1 framing.** The current pitch text leans on the architectural primacy of progressively-larger reactors. The cross-round finding from R-hybrid-solar-augmentation plus R-power-base-rate is that ICEBERG can do its work at Kilopower-class with a solar augment, without ever needing Fission Surface Power or megawatt. The pitch could be reframed as "Kilopower is sufficient; everything above is upside" — a much more defensible posture against an investor who has done their own homework on space-fission program history.
- **Positive for queued R-radiator-mass-recheck.** That round will re-anchor the radiator mass formula to Modular Assembled Radiators for Very Large systems data. The hybrid finding here makes the radiator question less urgent because the architectural baseline is Kilopower (where radiator mass is small) rather than megawatt (where it dominates). Suggest re-scoping R-radiator-mass-recheck to focus on Fission Surface Power class (40–100 kilowatts-electric) rather than megawatt.
- **Cross-reference to R-hybrid-impulsive-insertion (deferred).** The concentrated-burn case (sub-claim g) found 5.15-times gain at 1.2 astronomical units. If the impulsive-insertion architecture bunches the burn near Earth, hybrid augmentation amplifies the gain at exactly that point. The two rounds together would surface a unified architecture: chemical or water-prop impulsive Saturn-orbit insertion, nuclear-electric-propulsion cruise, hybrid-augmented near-Earth boost.
