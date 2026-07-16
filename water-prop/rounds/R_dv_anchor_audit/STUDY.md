# R-dv-anchor-audit — re-derive Saturn-departure and Earth-arrival delta-velocity anchors from vis-viva; recompute leapfrog cell

**Worker:** titan (re-spawn 3, branch `iceberg-titan-3`, 2026-05-19 same-day follow-on).
**Round type:** anchor audit + recomputation. Closed-form vis-viva, no parameter sweep beyond a small grid.
**Predecessors:** R-chemical-electric-leapfrog (this branch, commit `3a97067`); R12_lunar_GA_both_legs (main, commit pre-titan-3); R-bus-mass-anchor-adjudication (this branch).

---

## Why this round exists

User direction 2026-05-19: "question your assumptions." Audit of R-chemical-electric-leapfrog's load-bearing delta-velocity anchors reveals two anchors that were inherited from informal sketch rather than derived from vis-viva. They are likely wrong by a factor of 1.4–2.

The two suspect anchors:

1. **Saturn-departure delta-velocity = 5.5 kilometres-per-second impulsive.** Used as the leapfrog round's chemical Saturn-departure burn requirement. Source: informal sketch in conversation, not from any prior round's primary text.

2. **Earth-arrival chemical capture delta-velocity = 3.5 kilometres-per-second impulsive.** Used as the aerocapture-no scenario's capture burn requirement. Source: same.

The other anchors used in the leapfrog round (trans-Earth coast 0.3 km/s electric trim, vehicle dry mass 22.8 t from R-bus-mass-anchor-adjudication, chunk 200 t from matrix) have defensible sources.

This round derives the Saturn-departure and Earth-arrival anchors from vis-viva at the relevant orbital geometries, and re-runs the leapfrog Pareto sweep with the corrected anchors.

---

## Derivation

### Saturn-departure delta-velocity from B-ring parking orbit

Hohmann Saturn-Earth return trajectory: aphelion at Saturn (9.58 astronomical units), perihelion at Earth (1.0 astronomical units). Semi-major axis 5.29 astronomical units. Heliocentric velocity at Saturn (aphelion of return trajectory):

```
v_aphelion_helio = sqrt(GM_sun × (2/r_sat - 1/a)) = 3.42 km/s
```

Saturn's heliocentric orbital velocity = 9.63 km/s. The spacecraft must depart with a heliocentric velocity of 3.42 km/s in the retrograde direction relative to Saturn's heliocentric motion. Hyperbolic excess velocity at Saturn departure:

```
v_inf_at_saturn = v_sat_helio - v_aphelion_helio = 9.63 - 3.42 = 6.21 km/s
```

Vehicle parking orbit at Saturn: chunk is collected at the B-ring (mid-B-ring radius ~107,000 km from Saturn centre). Most efficient Saturn-departure strategy is Oberth-optimised periapsis burn: drop periapsis to just above Saturn's cloud tops (~60,000 km), retain apoapsis at B-ring (107,000 km). Elliptical parking orbit:

- Semi-major axis a = (60,000 + 107,000) / 2 = 83,500 km
- Eccentricity e = (107,000 - 60,000) / (107,000 + 60,000) = 0.281
- Velocity at periapsis (60,000 km): sqrt(GM_Saturn × (2/r_p − 1/a)) = sqrt(3.793 × 10¹⁶ × (3.33 × 10⁻⁸ − 1.20 × 10⁻⁸)) = **28.4 km/s**

For escape with v_∞ = 6.21 km/s at the same periapsis (vis-viva for hyperbolic trajectory):

```
v_periapsis_hyperbolic = sqrt(v_inf² + 2 × GM_Saturn / r_p)
                       = sqrt(6210² + 2 × 3.793 × 10¹⁶ / 6.0 × 10⁷)
                       = sqrt(3.86 × 10⁷ + 1.264 × 10⁹)
                       = 36.1 km/s
```

Departure burn delta-velocity at periapsis:

```
Δv_saturn_departure = v_periapsis_hyperbolic - v_periapsis_elliptical
                    = 36.1 - 28.4 = 7.7 km/s
```

**Corrected anchor: Saturn departure = 7.7 km/s impulsive, not 5.5 km/s.** Error in prior round: −40%.

### Earth-arrival delta-velocity from Hohmann return

Heliocentric velocity at Earth arrival (perihelion of return trajectory):

```
v_perihelion_helio = sqrt(GM_sun × (2/r_earth - 1/a)) = 40.1 km/s
```

Earth's heliocentric orbital velocity = 29.78 km/s. Hyperbolic excess velocity at Earth arrival:

```
v_inf_at_earth = v_perihelion_helio - v_earth_helio = 40.1 - 29.78 = 10.3 km/s
```

Three Earth-arrival options to evaluate:

**(a) Low Earth orbit capture impulsively (perigee 6578 km, 200 km altitude, circular).** Circular velocity at 200-km low Earth orbit = sqrt(GM_Earth / r) = 7.78 km/s. Velocity at same perigee on hyperbolic arrival:

```
v_perigee_hyperbolic = sqrt(v_inf² + 2 × GM_Earth / r) = sqrt(10300² + 2 × 3.986 × 10¹⁴ / 6.578 × 10⁶) = 15.1 km/s
```

Capture burn: 15.1 − 7.78 = **7.3 km/s impulsive** to low Earth orbit.

**(b) Highly elliptical Earth orbit capture (perigee 6700 km, apogee 384,000 km — lunar distance).** Velocity at perigee on this elliptical orbit:

```
v_perigee_elliptical = sqrt(GM_Earth × (2/r_p - 1/a)) where a = (6700 + 384,000)/2 = 195,350 km
                     = sqrt(3.986 × 10¹⁴ × (2.99 × 10⁻⁷ - 5.12 × 10⁻⁹))
                     = 10.82 km/s
```

Capture burn: 15.1 − 10.82 = **4.3 km/s impulsive** to highly elliptical Earth orbit.

**(c) Lunar gravity assist tour, then Earth orbit capture.** R12 measured: 10 inbound flybys shed 5.83 km/s of v_∞. Residual v_∞ after tour = 10.3 − 5.83 = **4.47 km/s** (matches R12's verbatim residual). To capture into low Earth orbit from v_∞ = 4.47 km/s:

```
v_perigee_hyperbolic = sqrt(4470² + 2 × GM_Earth / 6.578 × 10⁶) = 12.0 km/s
```

Capture burn: 12.0 − 7.78 = **4.2 km/s impulsive** to low Earth orbit after lunar gravity assist tour.

### Comparison table

| Earth-arrival option | Δv impulsive | Notes |
|---|---|---|
| (a) Direct chemical capture to low Earth orbit | 7.3 km/s | what no-aerocapture really costs |
| (b) Direct chemical capture to highly elliptical Earth orbit | 4.3 km/s | accept higher orbit, lower Δv |
| (c) Lunar gravity assist tour + chemical capture to low Earth orbit | 4.2 km/s | R12's architecture |
| (d) Earth aerocapture | ~0 propulsive | phoebe-falsified at conservative anchors |

The 3.5-km/s anchor in the leapfrog round was understated by ~1× to ~2×. The closest defensible value to my 3.5 was (b) at 4.3 km/s or (c) at 4.2 km/s, both ~20% higher than I used.

---

## Pre-registered hypotheses

### H-anchor-1 — Saturn-departure anchor correction

**Anchor.** 7.7 km/s impulsive from elliptical B-ring parking orbit with periapsis at 60,000 km, per vis-viva derivation above.

**Prediction.** Recompute the leapfrog round at the corrected Saturn-departure anchor:
- Propellant for 7.7 km/s on 220 t vehicle at chemical specific impulse 450 s: 220 × (1 − exp(−7700/4413)) = 220 × 0.827 = 182 tonnes water.
- Delivered with Earth aerocapture: 220 − 182 − 0.96 (trim) − 22.8 (dry) = **14.2 tonnes**. BELOW L0-09 30-t commercial floor.
- Reactor electrolysis time at 10 kilowatt-electric: 182 × 13.4 / 0.75 / 10 = 325 megajoule-years = 10.3 years.
- Round-trip (15 kilowatt-electric, 10-tonne tank, with aerocapture): 6 + 1 + (182 − 10) / 26.4 + 6 = 19.5 years.

Prediction: NO cell closes commercial-strict (L0-05 strict + L0-09 floor) at flyable power. Most flyable cells lose ~20 tonnes of delivered mass relative to my prior leapfrog round.

Falsified if any cell delivers ≥ 30 t at flyable power.

### H-anchor-2 — Earth-arrival anchor correction (no aerocapture)

**Anchor.** Chemical Earth-arrival capture is at least 4.2 km/s impulsive (with lunar gravity assist tour) or 7.3 km/s impulsive (direct from Hohmann v_∞ = 10.3 km/s).

**Prediction.** The aerocapture-no leapfrog cells deliver even less than I previously reported. At 7.3 km/s chemical capture on a 62-tonne post-trans-Earth vehicle: propellant = 62 × (1 − exp(−7300/4413)) = 62 × 0.808 = 50 tonnes. Vehicle after capture: 12 t. Delivered: 12 − 22.8 = **NEGATIVE** (vehicle can't close mass).

Falsified if any aerocapture-no cell delivers > 0 t at flyable power.

### H-anchor-3 — Lunar gravity assist + leapfrog combined verdict

**Anchor.** Combine R12's 10-flyby tour (5.83 km/s v_∞ shed at 8.7-month phasing penalty) with leapfrog chemical Saturn-departure. Inbound capture becomes 4.2 km/s chemical (or 0 with aerocapture). This is the architecturally most-defensible cell because it doesn't bet on aerocapture closing.

**Prediction.** At reactor power 15 kilowatt-electric, tank capacity 10 tonnes, lunar gravity assist tour active, the corrected anchors give:
- Saturn departure 7.7 km/s chemical: 182 t propellant.
- Earth capture 4.2 km/s chemical: 13 t propellant on a 38-t mid-cruise vehicle.
- Round-trip: 6 + 1 + spiral_yr + 6 + lunar_phasing 8.7/12 = 13.73 + spiral_yr.
- Spiral electrolysis at 15 kilowatt-electric: (182 − 10) / 26.4 = 6.5 years.
- Round-trip: 13.73 + 6.5 = 20.2 years.
- Delivered: 220 − 182 − 13 − 22.8 = **2.2 tonnes**. BELOW floor.

Prediction: even with the lunar gravity assist substituting for aerocapture, the corrected anchors put delivered mass below L0-09 floor at flyable power.

Falsified if any cell delivers ≥ 30 t under corrected anchors.

### H-anchor-4 (aggregate)

**ICEBERG at commercial chunk scale (200 tonnes) and flyable reactor power (≤ 30 kilowatt-electric Kilopower-extrapolation) does NOT close commercial-floor delivery under any architectural variant tested in this session — including the chemical-electric leapfrog and the lunar gravity assist tour — once the Saturn-departure and Earth-arrival delta-velocity anchors are corrected to vis-viva-derived values.**

Implications:
- The prior leapfrog round's "33-42 tonnes delivered at flyable power" headline was an artefact of the 5.5-km/s Saturn-departure anchor. Under the corrected 7.7-km/s anchor, that headline is retracted.
- The R12 lunar-gravity-assist verdict (13.91-year round-trip / 70% delivery at demonstrator scale) survives because R12 was sized for a 14-tonne chunk, not 200 tonnes. Demonstrator-scale architecture is unaffected.
- Commercial-scale ICEBERG inbound delivery requires either (a) chunk mass much smaller than 200 t (demonstrator-class), (b) reactor power well above flyable Kilopower-extrapolation (Fission Surface Power class, which the directive retired), or (c) a propulsion architecture not yet considered.

Falsified if any flyable cell delivers ≥ 30 t commercial floor under corrected anchors.

---

## Method

`run.py` re-runs the leapfrog sweep from `R_chemical_electric_leapfrog/run.py` with three corrections:

1. `DV_SATURN_DEPARTURE_MPS = 7700.0` (was 5500.0).
2. `DV_EARTH_CAPTURE_MPS = 7300.0` (was 3500.0) for aerocapture-no scenario.
3. Adds a new scenario: lunar gravity assist tour + chemical Earth capture at 4200 m/s residual (R12-anchored), with 0.725 year (8.7 month) phasing penalty added to round-trip.

Output: corrected Pareto envelope, comparison vs prior leapfrog round, identification of any cells that still close commercial floor.

Also runs a sensitivity: what reactor power would be needed to close commercial floor at corrected anchors with the lunar-gravity-assist scenario? Bisection on reactor power, holding tank at 10 t.

---

## Out-of-scope

- Saturn arrival capture delta-velocity. Assumed aerocapture-at-Saturn works (Saturn atmosphere is thick; Cassini-Huygens entry probe demonstrated entry physics). Separate validation round flagged.
- Variation in chunk mass. Held at 200 t commercial anchor; separate R-chunk-size-pareto round flagged.
- Variation in cruise time. Held at Hohmann 6 yr each leg; separate R-cruise-time-vs-trans-Saturn-injection-pareto round flagged.
- Non-Hohmann return trajectories (could reduce inbound time at higher Earth-arrival v_∞).
- Lunar gravity assist phasing realism beyond R12's 29.5-days-per-pass anchor.
- Reactor lifetime over the extended mission duration.

Each is its own round.

---

## Methodology lesson dependencies

- **Lesson 1** (pessimistic-default holds): H-anchor-4 is the more-pessimistic reading of the leapfrog round; prediction tested against measurement.
- **Lesson 9** (anchor-on-PRIMARY-text): the 5.5-km/s Saturn-departure anchor failed lesson 9 — it was an informal-sketch value, not anchored on any prior round's primary text. Corrected via vis-viva from first principles.
- **Lesson 19 candidate** (parameter-cascade): when a swept parameter (Saturn-departure delta-velocity) is also an unaudited anchor, the round's verdict propagates the error. Audit anchors before sweeping them.
- **Candidate lesson 20** (vis-viva-default): when a delta-velocity value is used without a primary-text citation, default to deriving it from vis-viva at the relevant orbital geometry. Hand-derivation takes 5 minutes and catches 40% errors.

---

## Files of record

```
water-prop/rounds/R_dv_anchor_audit/STUDY.md   (this file)
water-prop/rounds/R_dv_anchor_audit/run.py     (corrected leapfrog rerun)
water-prop/rounds/R_dv_anchor_audit/results/corrected_pareto.md
water-prop/rounds/R_dv_anchor_audit/results/closure_verdict.md
water-prop/rounds/R_dv_anchor_audit/results/results.json
```

Results appended after run.py executes.
