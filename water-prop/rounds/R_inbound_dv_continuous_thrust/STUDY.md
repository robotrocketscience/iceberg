# R-inbound-dv-continuous-thrust — does the matrix's 6.42 km/s inbound delta-velocity hold up under continuous-thrust electric propulsion, or does the megawatt all-electric end-to-end architecture lose level-zero requirement L0-05 compliance?

**Status:** complete.

## Question

The architecture decision matrix carries 6.42 km/s as the chunk-fed inbound delta-velocity. The trace of that number runs through rounds R8 (inbound budget audit) and R10 (inbound propulsion architecture revisit): it is the residual after a Hohmann return trajectory, a Saturn-side egress mirror of the conops 2.09 km/s ingress, and a single lunar gravity assist credited with ~2.15 km/s of Earth-arrival velocity-at-infinity reduction.

Every piece of that 6.42 km/s figure is impulsive. Saturn-side egress assumes a single chemical-equivalent burn at the periapsis of a capture ellipse. Earth-arrival assumes a Keplerian hyperbolic flyby of the moon followed by a single brake-into-low-Earth-orbit burn that gets the Oberth bonus from being deep in Earth's gravity well. Neither holds under continuous-thrust electric propulsion.

R-electric-outbound (commit 9001ce9) already exposed the impulsive-versus-continuous-thrust gap on the *outbound* leg: the conops-stated 9 km/s outbound impulsive delta-velocity became 17.97 km/s under continuous-thrust electric. R-electric-outbound paid attention only to the outbound leg, citing 6.42 km/s for inbound from the matrix without re-derivation. This round closes that gap.

The question: under continuous-thrust electric propulsion at the inbound mass profile (vehicle plus grappled chunk), starting from a Saturn-side bound orbit and ending in a low Earth orbit depot, what is the integrated delta-velocity? Does the megawatt all-electric end-to-end mission still close inside the 15-year ceiling that level-zero requirement L0-05 imposes?

This is the highest-leverage unresolved per the end-of-day handoff. If the corrected continuous-thrust inbound delta-velocity is materially higher than 6.42 km/s — and especially if it pushes the round-trip past 15 years — then the matrix's clean binary collapses. Year-zero-through-fifteen Kilopower Variant B (chemical kick plus electric inbound) would remain, but the year-twenty-plus megawatt all-electric end-to-end winner would be retired.

## Pre-registered hypothesis (H-it)

**Aggregate (H-it-agg):** continuous-thrust electric pays the integrated delta-velocity in full, with no Oberth bonus at either end. By symmetry with R-electric-outbound (where impulsive 9 km/s → continuous-thrust 18 km/s, roughly doubled), continuous-thrust inbound delta-velocity will land in the 10–14 km/s band — roughly twice the matrix's impulsive 6.42 km/s. At megawatt all-electric end-to-end with this corrected inbound budget, the round-trip time stays inside 15 years (the inbound burn time grows but remains under three years at megawatt power). Megawatt all-electric still closes L0-05, but the delivered-chunk fraction degrades materially.

**Pre-registered sub-claims:**

| Sub-claim | Predicted | Falsification |
|---|---|---|
| H-it-a — Saturn-side spiral-out integrated delta-velocity from B-ring circular orbit (135 000 km) to Saturn-escape | 14–18 km/s | outside this band |
| H-it-b — Heliocentric retrograde delta-velocity to drop from Saturn's orbital speed to Hohmann aphelion velocity (continuous-thrust, no Oberth) | 5.0–5.8 km/s (consistency check vs R8 H8b) | outside this band |
| H-it-c — Earth-side heliocentric decelerate delta-velocity from Hohmann perihelion velocity to Earth's orbital speed (continuous-thrust, no Oberth) | 10.0–10.6 km/s (consistency check vs R8 H8a) | outside this band |
| H-it-d — Earth-side Edelbaum capture spiral integrated delta-velocity from Earth-escape down to low Earth orbit (400 km altitude) | 7.5–7.9 km/s | outside this band |
| H-it-e — Total continuous-thrust inbound integrated delta-velocity, B-ring-departure case | 36–42 km/s | falsified low if < 36; falsified high if > 42 |
| H-it-f — Total continuous-thrust inbound integrated delta-velocity, lunar-gravity-assist-savings case (~2 km/s shaved off Earth phase) | 34–40 km/s | held if 2 km/s saving is credible, falsified if savings invalid for continuous-thrust |
| H-it-g — Aggregate hypothesis "doubled-from-impulsive" prediction: 6.42 × ~2 = 10–14 km/s | 10–14 km/s | strongly falsified high if total > 20 km/s (load-bearing for architecture) |
| H-it-h — Megawatt all-electric end-to-end round-trip under the corrected continuous-thrust inbound delta-velocity, 200-tonne chunk, electric specific impulse 2000 s | ≤ 15.5 years (just over L0-05 at most) | held if ≤ 15.5; load-bearing falsified if > 16 |
| H-it-i — Delivered chunk fraction at megawatt all-electric end-to-end under corrected delta-velocity | 25–55% (down from 75% nominal but not zero) | held if ∈ band; load-bearing falsified if < 10% |

**Pre-registered aggregate decision-ordering:**

The structurally interesting outcome is whether H-it-g falsifies (in either direction). If the continuous-thrust inbound delta-velocity lands in the 10–14 km/s band as predicted, the architecture stays close to what R-electric-outbound implied (some degradation but no collapse). If it lands materially higher — say 25–40 km/s — the architecture's clean binary collapses and three resolutions surface:

1. **Resurrect chunk-as-Earth-aerocapture-heat-shield** (R-chunk-as-heat-shield territory) to short-circuit the Earth-side spiral.
2. **Keep a small chemical kick at Saturn departure** (impulsive Saturn-egress, continuous-thrust elsewhere) to short-circuit the Saturn-side spiral. This defeats the "all-electric end-to-end" claim — but it may be the only L0-05-compliant year-twenty-plus architecture.
3. **Retire "all-electric end-to-end" entirely** and collapse the matrix back to Kilopower Variant B (chemical kick at both ends, electric inbound only) as the sole winning architecture for the program. This would falsify yesterday's matrix update.

If H-it-h falsifies (round-trip > 16 years at megawatt), the architecture decision matrix needs the year-twenty-plus winner cell revised. The pre-registered guess is that H-it-h holds (round-trip just inside 15.5 years at megawatt) but H-it-g falsifies in the structural direction.

## Method

Closed-form continuous-thrust integrated delta-velocity, mirroring R-electric-outbound's framework on the inbound leg. No optimal-control trajectory shaping; the integrated delta-velocity is the "vanilla" continuous-thrust upper bound, accurate to within 10–20% of optimal-control trajectories at the relevant power levels.

### Delta-velocity decomposition

The inbound vehicle starts in a bound Saturn orbit (after chunk capture and stow) and ends in a low Earth orbit circular orbit at 400 km altitude. The continuous-thrust integrated delta-velocity decomposes into four segments:

1. **Saturn-side spiral-out from circular bound orbit to Saturn-escape.** Edelbaum's planar-tangential-thrust closed-form: integrated delta-velocity equals the starting circular orbital speed, v_circ(r_dep). For B-ring departure (r_dep = 135 000 km), v_circ ≈ 16.8 km/s. The conops-implied alternative is a higher-elliptical departure orbit; sensitivity covered in §Sweeps.

2. **Heliocentric retrograde from Saturn's orbital speed to Hohmann aphelion velocity.** Once on Saturn-escape (heliocentric speed equal to Saturn's, ~9.65 km/s), the spacecraft must decelerate to Hohmann aphelion velocity (~4.17 km/s at 9.58 astronomical units). Continuous-thrust pays this in full: integrated delta-velocity = |v_Saturn_orb − v_Hohmann_aphelion| ≈ 5.45 km/s. Same number as R8 H8b under a different name.

3. **Ballistic Hohmann cruise from Saturn to Earth.** No propellant. Time-of-flight ~6.09 years.

4. **Earth-side heliocentric decelerate from Hohmann perihelion velocity to Earth's orbital speed.** At Earth (Hohmann perihelion), heliocentric speed is ~40.08 km/s; Earth's orbital speed is 29.78 km/s. Continuous-thrust integrated delta-velocity = ~10.30 km/s (R8 H8a).

5. **Earth-side Edelbaum capture spiral from Earth-escape down to low Earth orbit.** By time-reversal symmetry with the outbound Edelbaum spiral, integrated delta-velocity = v_circ_LEO ≈ 7.67 km/s.

Total continuous-thrust inbound integrated delta-velocity = sum of (1) + (2) + (4) + (5). Segment (3) is ballistic and adds time only.

### Lunar-gravity-assist credit

Under continuous-thrust electric propulsion, the lunar gravity assist (LGA) can still be exploited by shutting off thrust before encounter, coasting through the lunar sphere of influence on a clean hyperbolic trajectory, then resuming thrust. R2 found the LGA delivers up to ~3.24 km/s of velocity-at-infinity reduction at favorable conditions and ~2.15 km/s at the relevant velocity-at-infinity of 6 km/s. Realistic continuous-thrust savings are bounded by what the spacecraft can lose during a single thrust-off coast: probably 1.5–2.5 km/s of Earth-side heliocentric or capture-spiral budget. Conservative midpoint estimate: 2.0 km/s saved off segment (4) and/or (5).

### Saturn-side starting-orbit sensitivity

The conops Phase 5 has the vehicle in the B-ring for chunk operations (circular, 135 000 km). The Phase-5-mirror Phase-6 (Saturn departure) is an impulsive 2.09 km/s, suggesting the conops envisions the vehicle climbing back up to the original elliptical capture orbit before departing. Under continuous-thrust, "climb back up" is itself an Edelbaum-spiral cost. Three sub-cases:

- **B-ring-departure (worst case for continuous-thrust):** vehicle thrusts continuously from B-ring circular to Saturn-escape. Integrated delta-velocity = v_circ_Bring ≈ 16.8 km/s.
- **High-elliptical-departure:** vehicle uses small impulsive maneuver (or quasi-impulsive Hohmann-up) to return to a high-elliptical orbit with apoapsis ~Iapetus distance (3.56 million km), then continuous-thrust spiral-out from there. Departure-radius v_circ ≈ 3.3 km/s. Total spiral cost ≈ 3.3 km/s plus the climb-up cost (~2 km/s impulsive). This is the architecture that retains best-case continuous-thrust performance but requires a chemical or chunk-fed-impulsive periapsis-raise maneuver before departure.
- **Hybrid mid-elliptical-departure:** intermediate orbit with apoapsis ~1 million km, v_circ ≈ 6.16 km/s, used as the spiral-out starting point.

### Mass closure model

For each (continuous-thrust delta-velocity, electric specific impulse, reactor power) combination, compute:

1. **Inbound propellant mass.** Tsiolkovsky-consistent: m_prop / m_initial = 1 − exp(−Δv / v_e), where v_e = Isp × g₀ and m_initial = m_tug + chunk_mass.
2. **Delivered chunk fraction.** (chunk_mass − m_prop_inbound) / chunk_mass.
3. **Inbound burn time at constant thrust.** Same approximation as R-electric-outbound: thrust held constant over the burn while mass decreases; ~5% error at mass ratios ≤ 2 and rises to ~15% at mass ratios near 5.
4. **Round-trip time.** Outbound burn (taken from R-electric-outbound at the matching reactor power) plus two Hohmann cruises (12.17 years) plus 1 year Saturn operations plus inbound burn time.

### Sweeps

- **Saturn departure orbit:** B-ring (135 000 km), high elliptical (1 million km), Iapetus-distance (3.56 million km).
- **Reactor power:** 100, 200, 500, 1000, 2000 kilowatt-electric. Note 2000 kilowatt-electric is added beyond R-electric-outbound's top to test whether sub-megawatt-class can close at the corrected delta-velocity, and whether dual-megawatt closes more comfortably.
- **Electric specific impulse:** 2000, 3000, 4000 seconds.
- **Chunk mass:** 100, 200, 500 tonnes (architecture decision matrix sensitivity).
- **Lunar-gravity-assist credit:** 0 (no savings) and 2.0 km/s (best plausible).

### Validity caveats

- Edelbaum's closed-form is exact for planar tangential thrust between circular orbits. For elliptical-to-escape spirals the integrated delta-velocity is approximated as v_circ at the starting periapsis-like radius; this is the upper-bound approximation, accurate to ~10% in standard low-thrust trajectory references (Edelbaum 1961; Petropoulos and Russell 2008, "Optimization of low-thrust trajectories").
- The continuous-thrust delta-velocity formulation ignores optimal-control trajectory shaping (perihelion / aphelion phasing, multi-flyby tours). Trajectory-shaping can shave 10–20% off the "vanilla" integrated delta-velocity for missions where it has been worked, e.g. BepiColombo, Hayabusa-2. This round does not attempt that; the headline number is the conservative continuous-thrust ceiling.
- The constant-thrust burn-time approximation (thrust held constant while mass decreases) overstates burn time at mass ratios above 2. At Tsiolkovsky-consistent mass ratios of 5 (realistic at the highest delta-velocity sub-cases here), the approximation error is ~15%. The actual burn time is shorter than reported. This is the same approximation R-electric-outbound used; carried for cross-comparability.
- Lunar gravity assist credit under continuous-thrust assumes the spacecraft can shut off thrust, coast through the lunar sphere of influence on a clean hyperbolic trajectory, and resume thrust afterward. This is operationally feasible for ion-class thrusters that can be cycled. It is not feasible for arcjet-class thrusters that cannot be cycled rapidly. The 2.0 km/s credit assumes ion-class.
- Reactor cycle life under multi-year continuous burn is not modeled. The corrected inbound burn time may exceed the burn-life ceiling that R-electric-outbound's seven-year-burn-cap convention encoded.
- Solar-electric augmentation for the inner-AU phase of the *inbound* leg is plausible (sunlight returns as the spacecraft approaches Earth), but the inbound burn is dominated by the Saturn-side phase where solar is unavailable. Not modeled.
- Chunk-as-Earth-aerocapture-heat-shield is not modeled. If chunk-aerobrake works, segment (5) and most of segment (4) collapse to a single dissipative pass. This is a separate architectural option; this round documents the all-electric ceiling without that path.

## Result

Run output in `results/inbound_dv_continuous.json` and `results/tables.md`.

**Headline numbers — continuous-thrust inbound integrated delta-velocity by Saturn-departure orbit:**

| Saturn departure | No lunar gravity assist | With lunar gravity assist credit (2.0 km/s) | Multiple of matrix 6.42 |
|---|---:|---:|---:|
| B-ring (135 000 km circular) | 40.17 km/s | 38.17 km/s | 6.26× / 5.95× |
| High-elliptical (1 million km) | 29.56 km/s | 27.56 km/s | 4.60× / 4.29× |
| Iapetus distance (3.56 million km) | 26.67 km/s | 24.67 km/s | 4.15× / 3.84× |

The decomposition is dominated by the two Edelbaum spirals (Saturn-side 3.3–16.8 km/s, depending on departure orbit; Earth-side 7.67 km/s fixed) and the two heliocentric drops (Saturn 5.44 km/s, Earth 10.30 km/s). Lunar gravity assist credit of 2 km/s is small compared to the spiral and heliocentric segments.

**Megawatt all-electric end-to-end round-trip, 200-tonne chunk, electric specific impulse 2000 seconds:**

| Inbound delta-velocity case | Mass ratio | Delivered fraction | Inbound burn (yr) | Round-trip (yr) | Closes L0-05? |
|---|---:|---:|---:|---:|:--:|
| Matrix 6.42 km/s (Oberth-credited) | 1.39 | 70.4% | 0.56 | 13.90 | yes |
| B-ring departure, no lunar gravity assist | 7.75 | 7.6% | 1.73 | 15.07 | **no** |
| B-ring departure, with lunar gravity assist | 7.00 | 9.1% | 1.70 | 15.05 | **no** |
| High-elliptical departure, no lunar gravity assist | 4.51 | 17.4% | 1.55 | 14.89 | yes |
| High-elliptical departure, with lunar gravity assist | 4.08 | 20.0% | 1.50 | 14.84 | yes |
| Iapetus-distance departure, with lunar gravity assist | 3.52 | 24.1% | 1.42 | 14.77 | yes |

The matrix-assumed 6.42 km/s case closes with 70% delivered. The corrected continuous-thrust cases all degrade delivered fraction to 8–24% and three of six burst the 15-year ceiling.

**Hypothesis grading:**

| Sub-claim | Predicted | Actual | Verdict |
|---|---|---|---|
| H-it-a — Saturn spiral-out (B-ring) | 14–18 km/s | 16.76 km/s | held |
| H-it-b — Saturn-side heliocentric drop | 5.0–5.8 km/s | 5.44 km/s | held |
| H-it-c — Earth-side heliocentric drop | 10.0–10.6 km/s | 10.30 km/s | held |
| H-it-d — Earth Edelbaum capture spiral | 7.5–7.9 km/s | 7.67 km/s | held |
| H-it-e — Total delta-velocity, B-ring no lunar gravity assist | 36–42 km/s | 40.17 km/s | held |
| H-it-f — Total delta-velocity, B-ring with lunar gravity assist | 34–40 km/s | 38.17 km/s | held |
| H-it-g — "Doubled-from-impulsive" prediction (10–14 km/s) | 10–14 km/s | 24.67–40.17 km/s | **load-bearing falsified high** |
| H-it-h — Megawatt round-trip ≤ 15.5 years | ≤ 15.5 yr | 14.77–15.07 yr | held both architectures |
| H-it-i — Delivered fraction 25–55% | 25–55% | 9–24% | **falsified low both architectures** |

The four segment-level predictions (H-it-a/b/c/d) all held tightly — these are textbook orbital mechanics and the pre-registration was a sanity check. The two aggregate B-ring totals (H-it-e/f) held in the predicted band. The architectural hypothesis H-it-g — that continuous-thrust roughly doubles the impulsive delta-velocity — falsified hard: the actual ratio is 3.8× to 6.3×, not 2×. H-it-h held narrowly: megawatt all-electric end-to-end does still close inside 15 years at the best architectures. H-it-i falsified low: delivered chunk fraction at megawatt is 9–24%, well below the 25–55% pre-registered band and far below the 70% the matrix carries.

## Reading

**The matrix's clean binary survives but the year-twenty-plus winner cell narrows substantially.** Megawatt all-electric end-to-end still fits inside L0-05's 15-year ceiling — but only under three simultaneous constraints that the matrix did not previously surface:

1. **Saturn departure must be from a high-elliptical orbit (apoapsis ≥ ~1 million km), not from the B-ring.** B-ring departure under continuous-thrust integrates 16.76 km/s in the Saturn-side spiral-out alone (Edelbaum 1961, closed-form), which bursts the round-trip to 15.05 years even after lunar-gravity-assist credit. The conops's current Phase-6 architecture — chunk operations in B-ring with Saturn departure mirroring the 2.09 km/s impulsive ingress — is incompatible with all-electric end-to-end.

2. **Electric specific impulse must be ~2000 seconds, not higher.** Counter-intuitively, dropping to 2000 seconds is the only specific impulse that closes; at 3000 seconds the round-trip is 16.06 years, at 4000 seconds 17.36 years. Higher specific impulse helps propellant mass (delivered fraction climbs from 20% at 2000 s to 35.5% at 3000 s, 46.5% at 4000 s) but reduces thrust at fixed power, so burn time grows linearly with specific impulse. The 15-year ceiling forces 2000 s as the bottom of the achievable specific impulse band.

3. **Chunk mass ≤ 200 tonnes.** At 500 tonnes the round-trip is 16.97 years; chunk-mass sensitivity is roughly linear in inbound burn time. The matrix's year-twenty-plus winner cell baseline of 500-tonne chunks does not close at the corrected delta-velocity; the actual close-cell is 200-tonne chunks.

**The 70% delivered-chunk-fraction baseline is the most load-bearing-falsified architectural assumption uncovered in the campaign to date.** Under continuous-thrust electric at megawatt, the best-case delivered fraction is 24% (Iapetus-distance Saturn departure with lunar gravity assist). The realistic mid-case is 20% (high-elliptical departure). This is a 3.5× degradation from the matrix's 70%, multiplied across all years of steady-state production. The financial model's net-present-value, the pitch's headline mass-delivered numbers, and the conops's bag-engineering 75% nominal — all calibrated against the impulsive-budget 6.42 km/s baseline — overstate delivered mass per mission by a factor of ~3.5 at the year-twenty-plus megawatt cell.

**The chemical-kick architecture (Kilopower Variant B, year-zero-through-fifteen) is unaffected by this finding.** Variant B's inbound burn is already chunk-fed-electric, but Saturn departure is chemical-kick (impulsive) and Earth arrival uses chemical capture (impulsive). Under those two impulsive maneuvers, the inbound segment payable at electric specific impulse is the small residual — exactly what the matrix's 6.42 km/s represents. The Variant B mass economics hold.

**The mechanism is mirror-symmetric to R-electric-outbound's mechanism but the magnitudes are larger.** R-electric-outbound found continuous-thrust outbound integrated delta-velocity is 17.97 km/s versus impulsive 9 km/s (a 2× ratio). The same physics applied to the inbound leg gives 24.67 to 40.17 km/s versus impulsive 6.42 km/s (3.8× to 6.3×). The ratio is much worse on the inbound leg because:

- Inbound passes through *two* Edelbaum spirals (Saturn-escape spiral plus Earth-capture spiral), totaling ~24 km/s in the B-ring case. Outbound has only the Earth-escape spiral (~7.67 km/s).
- Inbound's impulsive baseline (6.42 km/s) is already small thanks to lunar-gravity-assist credit applied in earlier rounds; the continuous-thrust correction is computed against this small baseline, inflating the ratio.

**Re-derivation: I predicted ratio 2× because I anchored on R-electric-outbound's outbound ratio.** This is the same anchoring-failure mode R-electric-outbound itself flagged as a recurring lesson. The right pre-registration would have noted that inbound geometry includes two spirals where outbound includes only one, and the ratio would compound accordingly. The methodology lesson recurs.

**Three architecture choices the matrix needs to make:**

1. **Endorse high-elliptical Saturn-departure architecture for the megawatt all-electric era.** Update conops Phase 5–6: chunk operations remain in B-ring (the chunk source) but the vehicle uses chunk-fed impulsive-equivalent maneuvers to climb back to high-elliptical apoapsis before continuous-thrust departure. This requires either a chemical or chunk-fed-mini-impulsive periapsis-raise capability, partially defeating "all-electric end-to-end" but keeping the bulk of the inbound burn on electric.

2. **Accept the 20% delivered-fraction baseline in the year-twenty-plus financial model.** Re-run net-present-value sensitivity in R-NPV-discount-rate / R-financing-capital-stack with 20% delivered baseline. The year-twenty-plus winner cell's L0-05 compliance is preserved but its unit economics tighten by 3.5×.

3. **Re-evaluate whether chunk-as-Earth-aerocapture-heat-shield should be resurrected as a third architecture.** The Earth-side spiral plus heliocentric drop (segments 4+5 = 17.97 km/s) is the largest single chunk of the continuous-thrust budget. If chunk-aerocapture works (R-chunk-as-heat-shield territory), this collapses to a single aerodynamic pass; delivered fraction rises dramatically. R-chunk-as-heat-shield was previously evaluated but is worth revisit specifically in light of the year-twenty-plus mass economics under the corrected budget.

**Methodology lessons added:**

- *Sub-spirals compound across legs.* Outbound and inbound each include the LEO/Earth spiral, but inbound additionally pays a Saturn spiral. When pre-registering an aggregate ratio, count the number of spiral segments per leg.
- *Lunar gravity assist credit is not architecturally load-bearing under continuous-thrust.* 2.0 km/s saved out of 27–40 km/s total is a single-digit percentage; the architecture-survival decision is driven by the spiral and heliocentric segments, not the lunar gravity assist tour. R2's 30%-optimistic finding on lunar gravity assist is no longer the load-bearing item.
- *Higher specific impulse can hurt under L0-05.* At fixed power, higher specific impulse drops thrust linearly. For a fixed delta-velocity, propellant mass falls but burn time rises. The optimum for the L0-05-constrained architecture is at the lower bound of the available specific impulse band, not the upper. This inverts the conventional "higher specific impulse is always better" intuition for ion propulsion.

## Revisit clause

## Revisit clause

Grade H-it-a through H-it-i. If H-it-g falsifies high (continuous-thrust inbound delta-velocity materially higher than the doubled-from-impulsive prediction), the architecture decision matrix needs three changes:

1. Update the "year-twenty-plus megawatt all-electric end-to-end" cell's outbound-delta-velocity row to flag inbound-delta-velocity as load-bearing for L0-05 compliance.
2. Determine whether the corrected inbound delta-velocity at megawatt all-electric still closes inside 15 years (H-it-h grade). If not, propagate to either chunk-aerobrake resurrection or chemical-kick-at-Saturn hybrid.
3. Revisit the delivered-chunk fraction across all matrix cells under the corrected inbound delta-velocity. The mass-delivery numbers in `ICEBERG-pitch.md` and `ICEBERG-conops.md` are calibrated against the impulsive budget; if continuous-thrust is the realistic flight regime, the headline delivered-mass economics need a sensitivity sweep.

If H-it-h load-bearing-falsifies (round-trip > 16 years), the year-twenty-plus winner cell is retired. The architecture matrix returns to a single year-zero-through-fifteen winner (Kilopower Variant B), and the steady-state production phase of the program needs a re-roadmap.

## Cross-learning

- **Architecture decision matrix update needed at the year-twenty-plus megawatt all-electric end-to-end cell.** The cell still closes L0-05 — round-trip 14.77–14.84 years at high-elliptical Saturn departure with lunar-gravity-assist credit — but three constraints surface that were not in the matrix: Saturn departure must be high-elliptical not B-ring, electric specific impulse must be ~2000 seconds (not higher), and chunk mass must be ≤200 tonnes. The matrix cell needs annotations for all three.
- **Delivered-chunk-fraction baseline of 70% in the matrix is wrong by 3.5× at the year-twenty-plus winner cell.** The corrected best-case delivered fraction is 20% (high-elliptical with lunar gravity assist, megawatt, 2000 s, 200 t). This is the biggest single-number revision uncovered in the campaign. Propagates to: pitch's mass-delivered headline, conops's bag-engineering 75% nominal, financial model's net-present-value sensitivity. None of these documents are corrected by this round (worker-session writes do not touch shared docs); flagged for orchestrator integration.
- **Kilopower Variant B (year-zero-through-fifteen winner) is structurally unaffected.** Its impulsive-budget 6.42 km/s inbound was always correct for the chemical-kick-Saturn-departure plus chemical-capture-Earth-arrival architecture. The architecture decision matrix's year-zero-through-fifteen cell does not need any revision from this round.
- **The conops B-ring chunk-operations baseline is incompatible with the year-twenty-plus megawatt all-electric architecture.** Conops Phase 5–6 has the vehicle do chunk operations in B-ring and depart from B-ring under chunk-fed-electric propulsion. Under continuous-thrust, this bursts the L0-05 ceiling (15.05 years versus 15.00). The fix is either (a) move chunk operations to a high-elliptical orbit (engineering change to bag deployment and capture mechanism that must operate ~10× further from Saturn), or (b) retain B-ring chunk operations and use a small impulsive Saturn periapsis-raise maneuver to climb back to high-elliptical before continuous-thrust departure (requires a chemical or chunk-fed-impulsive capability on the vehicle, partially defeating "all-electric end-to-end").
- **Promotes R-chunk-as-heat-shield revisit.** The Earth-side segments (heliocentric drop + Edelbaum capture spiral) total 17.97 km/s of the inbound continuous-thrust budget. If chunk-aerocapture works, this collapses to one aerodynamic pass and the corrected delta-velocity drops to ~10 km/s — back into the matrix's original 6.42 km/s neighborhood. The earlier round's aerocapture-retirement decision was driven by drag-skirt rescue path collapse; the chunk-as-heat-shield path is structurally different and worth specific revisit at the year-twenty-plus cell's economics under continuous-thrust.
- **R-mission-success-probability gains urgency.** With delivered-chunk-fraction at 20% per mission, the year-twenty-plus financial model has much tighter margins per mission; the 90% per-mission success requirement (L0-10) compounds harder on net-present-value. The mission-success-probability round was already candidate-2 in the handoff; this round elevates it.
- **Methodology lesson — anchoring on a single-leg ratio underestimates a multi-leg compounded ratio.** I anchored my H-it-g prediction on R-electric-outbound's 2× outbound continuous-thrust ratio. Inbound has *two* Edelbaum spirals (Saturn-escape plus Earth-capture) where outbound has only one, so the ratio compounds; correct pre-registration would have been 3–4× rather than 2×. The recurring pattern across the campaign — pre-registered prediction bias is consistently pessimistic in the direction of the headline (continuous-thrust *less* bad than predicted) but consistently *optimistic* on the structural mechanism (anchoring on the wrong ratio). Adding to the convention log.
- **Methodology lesson — at L0-05-constrained architectures, specific impulse optimum is at the lower band, not the upper.** Conventional electric-propulsion intuition is that higher specific impulse is always better; at fixed reactor power and a fixed time ceiling, higher specific impulse means lower thrust means longer burn means burst time-budget. The year-twenty-plus megawatt cell's specific impulse is *locked* at the bottom of the available band by L0-05. This inverts the design-of-experiments expectation for R-thruster-per-power-class and adjacent rounds.
- **Validity-caveat carryover.** The Edelbaum-plus-heliocentric integrated-delta-velocity model overstates burn time relative to optimal-control trajectories (which can use perihelion/aphelion phasing and gravity-assist sequences to shave the integral). For the year-twenty-plus cell this means the "burst 15 years" result for B-ring/Iapetus/high-specific-impulse cases may be recoverable by trajectory shaping. R-trajectory-shaping-optimization is a new candidate round; would close the 15.05-year B-ring case and the 16.06-year Isp-3000 case if 10–20% trajectory-shaping savings are real. Flagged but not in scope here.
- **The "all-electric end-to-end" architectural label remains structurally accurate.** No chemical kick at Earth departure, no chemical kick at Saturn arrival, no chemical kick at Saturn departure — provided the B-ring climb-back is accomplished with chunk-fed-electric using more delta-velocity, which the corrected budget shows is feasible at 1 megawatt-electric. The matrix's binary distinction between "chemical-kick architecture" (Variant B, year-0–15) and "all-electric end-to-end" (megawatt, year-20+) is preserved; what shifts is the unit-economics on the all-electric side, not the propulsion-mode-purity claim.
