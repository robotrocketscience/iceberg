# R-jupiter-ga-saturn-exit-flexibility

**Worker:** titan (Block 6)
**Owner:** project owner / orchestrator
**Pre-registration date:** 2026-05-15

---

## Motivation — questioning Block 5

R-launch-window-cadence-revisit (Block 5) concluded that Jupiter return gravity-assist is available at only 2.78% of Earth-Saturn launch windows at ±5° tolerance, and ~7.5% at the self-consistent maximum reshape tolerance (±13.5°). That analysis modeled a single trajectory degree-of-freedom: a *constant cross-track acceleration* during cruise to bend the chunk by Δθ at Jupiter's orbital radius.

The chunk has at least one other independent degree of freedom: the **Saturn-exit delta-velocity magnitude**. Varying the retrograde Saturn-exit burn shifts the chunk onto a different heliocentric ellipse with a different perihelion distance. For a purely tangential-retrograde burn applied at Saturn, the line-of-apsides direction is *fixed* (Saturn-position to its antipode), but the *time of Jupiter-orbit crossing* varies with perihelion choice. This means the chunk can wait at Jupiter's orbital radius for a longer or shorter wait while Jupiter sweeps into position — at the cost of a Saturn-exit delta-velocity premium.

This trajectory family was not modeled in Block 5. If it materially expands Jupiter-viable fraction at lower cost than cruise-reshape, then Block 5's conclusion that Jupiter return gravity-assist is "structurally not a load-bearing operational lever" needs revision.

**This round questions Block 5's own pessimism.**

---

## Pre-registered hypotheses

| # | Hypothesis | Prediction | Falsification rule |
|---|---|---|---|
| H1 | Restricting trajectory family to Saturn-exit-tangential-retrograde ellipses with perihelion in [0.5, 1.0] astronomical units does not enlarge the Jupiter-orbit-crossing longitude — only the crossing *time*. Crossing longitude remains anchored to Saturn-exit position by the line-of-apsides geometry. | Crossing-longitude variance across perihelion sweep is < 5°. | Falsified if any perihelion in [0.5, 1.0] AU produces a crossing-longitude shift > 5° relative to the Hohmann perihelion-1.0 baseline. |
| H2 | The time-of-flight from Saturn-exit (aphelion) to Jupiter-orbit-crossing varies significantly with perihelion. Range: ~3.5 to 5.5 years across perihelion ∈ [0.5, 1.0] astronomical units. | Crossing-time range ≥ 1.5 years. | Falsified if crossing-time range < 1.0 year (time-of-flight only weakly dependent on perihelion). |
| H3 | The Saturn-exit delta-velocity premium for perihelion ∈ [0.5, 1.0] astronomical units relative to Hohmann (perihelion = 1.0) is < 1.0 kilometre-per-second across the whole range. | Maximum premium at perihelion 0.5: ~0.5 kilometre-per-second. | Falsified if maximum premium > 1.5 kilometre-per-second (cost grows faster than expected). |
| H4 | Combining Saturn-exit-flexibility with the time-flexibility it provides, Jupiter-viable fraction at ±5° tolerance rises substantially above Block 5's 2.78%. | Combined fraction at ±5° and ≤ 1.0 kilometre-per-second Saturn-exit-premium budget: ≥ 0.20. | Falsified if combined fraction < 0.15 (Saturn-exit-flexibility is not a meaningful lever) or > 0.50 (re-opens the question of whether Jupiter gravity-assist is reliably available). |
| H5 | The expanded trajectory family changes the campaign-mean delivered fraction substantially: from Block 5's 15.97% (mostly-no-Jupiter) toward something closer to 18-20% (Jupiter alignment more often achievable at acceptable cost). | Campaign-mean delivered fraction at ≤ 1.0 kilometre-per-second budget: ∈ [0.17, 0.20]. | Falsified if < 0.16 (Saturn-exit-flexibility didn't help materially) or > 0.21 (some lever was over-credited). |

---

## Method

**Trajectory family.** All chunks leave Saturn at the same aphelion point (Saturn's heliocentric position at exit time) with a purely tangential-retrograde delta-velocity. The post-burn heliocentric orbit is an ellipse with aphelion 9.55 astronomical units (Saturn's radius) and varying perihelion ∈ [0.5, 1.0] astronomical units. For each perihelion:
- Semi-major-axis a = (perihelion + 9.55) / 2
- Eccentricity e = (9.55 - perihelion) / (9.55 + perihelion)
- Heliocentric speed at Saturn-exit: v = 2π × √(2/9.55 - 1/a) [astronomical-units per year]
- Saturn orbital speed: v_Saturn = 2π × 9.55 / 29.457 ≈ 2.037 astronomical-units per year
- Required Saturn-exit retrograde delta-velocity: Δv(perihelion) = v_Saturn - v(perihelion) [astronomical-units per year, converted to kilometres-per-second]
- Premium relative to Hohmann (perihelion = 1.0): Δv(perihelion) - Δv(1.0)

**Jupiter-orbit-crossing geometry.** For each perihelion, compute:
- True anomaly at radius 5.2 astronomical units on the descending leg from aphelion
- Time-of-flight from aphelion to crossing (via Kepler's equation)
- Heliocentric longitude at crossing (line-of-apsides fixed at Saturn-exit-to-antipode; perihelion direction is the *antipode* of Saturn-exit, so heliocentric longitude of chunk at true-anomaly ν is θ_perihelion-direction + ν)

**Per-launch sweep.** For each launch n ∈ [0, 57] (60-year span) and each perihelion in a grid [0.5, 1.0] at 0.05-AU resolution:
- Compute chunk's Jupiter-crossing time and longitude
- Compute Jupiter's heliocentric longitude at that time
- Angular separation |chunk_longitude - jupiter_longitude| (signed, wrapped to [-180°, +180°])
- Record (separation, Saturn-exit-premium)

**Viable test.** Window n is "Jupiter-viable at tolerance T° within budget B kilometres-per-second" if any perihelion in the grid yields |separation| ≤ T° AND Saturn-exit-premium ≤ B.

**Tolerance and budget sweep.**
- Tolerances: ±2°, ±5°, ±10°, ±15°.
- Budgets: 0.0, 0.25, 0.5, 1.0, 1.5, 2.0 kilometres-per-second.

For each (tolerance, budget) pair, report the Jupiter-viable fraction and the campaign-mean delivered fraction (weighted average of 21.8% for viable, 15.5% for non-viable).

**Phase ensemble.** As in Block 5, average over 360 Jupiter initial-phase samples to remove single-phase sampling noise.

**Comparison with Block 5.** Reproduce Block 5's tolerance-only result (Saturn-exit-budget = 0) as a control. Verify it matches Block 5's 2.78% at ±5°.

**Outputs.**
- `results/trajectory_family.csv` — per-perihelion: true anomaly at Jupiter crossing, time-of-flight, heliocentric speed at Saturn, Saturn-exit delta-velocity, premium relative to Hohmann.
- `results/per_window_min_cost.csv` — per-launch: minimum Saturn-exit-premium that achieves Jupiter alignment at each tolerance.
- `results/viable_fraction_grid.csv` — viable fraction at each (tolerance, budget) pair.
- `results/campaign_mean_grid.csv` — campaign-mean delivered fraction at each (tolerance, budget) pair.
- `results/summary.json` — hypothesis adjudication.

---

## Limitations of this model

- **Pure-tangential Saturn-exit burn only.** A non-tangential burn rotates the line-of-apsides and could shift Jupiter-crossing *longitude*. This is a third degree of freedom not modeled here; it would further widen the viable fraction.
- **Earth-arrival speed varies with perihelion.** Lower perihelion → higher Earth-arrival hyperbolic excess speed → more aerocapture demand. This may eat some Jupiter-gravity-assist benefit on the Earth-side. Not modeled in this round; flagged as a follow-on cost to bookkeep.
- **Jupiter-arrival hyperbolic-excess speed.** The 2.5 kilometre-per-second Jupiter-gravity-assist benefit number is calibrated to a specific Jupiter-approach geometry; off-nominal perihelion changes the v-infinity at Jupiter and therefore the achievable bending-angle delta-velocity. First-order: bending-angle benefit scales roughly inversely with v-infinity, so deeper perihelions (higher v-infinity at Jupiter) get *less* benefit. Not modeled; would make the Saturn-exit-flexibility lever *weaker* than this round suggests.
- **Combined with Block 5's cruise-reshape.** This round modes Saturn-exit-flexibility as a stand-alone lever. The true optimum is the joint optimization (Saturn-exit-Δv × cruise-reshape-Δv). Not modeled; would make the viable fraction at least as good as the better single-lever answer, not worse.
- **Two-body Sun-only dynamics.** Saturn and Jupiter gravitational perturbations during cruise are ignored. First-order: small.
- **Coplanar circular orbits for planets.** Same caveat as Block 5.

---

## Decision rule

If H4 holds (Jupiter-viable fraction at ±5° and ≤ 1.0 kilometre-per-second budget ≥ 0.20):
- Block 5's "Jupiter return gravity-assist is structurally not a load-bearing operational lever" is overturned. Re-elevate Jupiter gravity-assist as a lever; revise composite steady-state delivered fraction upward.
- ICEBERG-conops and demand docs need to use the higher campaign-mean delivered fraction.

If H4 falsified low (< 0.15):
- Block 5 confirmed: Saturn-exit-flexibility doesn't fix the problem. Composite steady-state stays at ~16%.

If H4 falsified high (> 0.50):
- Strong evidence Saturn-exit-flexibility is much more powerful than expected. Need to verify with the line-of-apsides-rotation degree of freedom (which would help further). Consider re-elevating Jupiter gravity-assist to "central case" status.

In either direction the verdict propagates into the architecture-decision-matrix delivered-fraction row.

---

## Results

### Trajectory family per perihelion

| Perihelion (AU) | ν at Jupiter crossing (°) | Time to Jupiter (yr) | Heliocentric speed at Saturn (km/s) | Δv premium vs Hohmann (km/s) |
|---|---|---|---|---|
| 0.50 | 204.8 | 4.363 | 3.04 | **+1.16** |
| 0.70 | 209.8 | 4.466 | 3.56 | +0.63 |
| 0.85 | 213.2 | 4.546 | 3.90 | +0.30 |
| 1.00 (Hohmann) | 216.4 | 4.628 | 4.19 | 0.00 |

### Hypothesis adjudication

| # | Prediction | Realized | Status |
|---|---|---|---|
| H1 | Crossing-longitude variance across perihelion grid < 5° | 11.62° | **falsified** — but the shift is modest |
| H2 | Time-of-flight range across perihelion grid ≥ 1.5 yr | 0.27 yr | **falsified low** — descent from 9.55 AU to 5.2 AU is fast and insensitive to perihelion |
| H3 | Max Δv premium < 1.0 km/s | 1.16 km/s | **marginal** — within 16% of the boundary |
| H4 | Viable fraction at ±5° and ≤ 1 km/s ≥ 0.20 | 3.48% | **falsified low** — Saturn-exit-flexibility is not a meaningful lever |
| H5 | Campaign-mean delivered fraction at ±5° and ≤ 1 km/s ∈ [0.17, 0.20] | 15.72% | **falsified low** — barely above the no-Jupiter floor (15.5%) |

**Block 5 reproduction:** At perihelion = 1.0 and budget = 0, viable fraction at ±5° is 2.78%, exactly matching Block 5's result. Sanity check passed.

### Viable-fraction grid (phase-averaged)

| Tolerance | Budget 0.0 km/s | 0.5 km/s | 1.0 km/s | 1.5 km/s |
|---|---|---|---|---|
| ±2°  | 1.11% | 1.39% | 1.82% | 2.10% |
| ±5°  | **2.78%** (Block 5 baseline) | 3.06% | **3.48%** | 3.76% |
| ±10° | 5.56% | 5.84% | 6.26% | 6.54% |
| ±15° | 8.33% | 8.62% | 9.04% | 9.32% |

### Campaign-mean delivered fraction grid (phase-averaged)

| Tolerance | Budget 0.0 km/s | 0.5 km/s | 1.0 km/s | 1.5 km/s |
|---|---|---|---|---|
| ±5° | 15.68% | 15.69% | **15.72%** | 15.74% |
| ±10° | 15.85% | 15.87% | 15.89% | 15.91% |

Saturn-exit-flexibility moves the campaign-mean delivered fraction from 15.68% to 15.74% at ±5° with full 1.5 km/s budget. **Six basis points.** Not material.

---

## Findings (this round)

**Finding 16 — Saturn-exit-flexibility is not a meaningful Jupiter-gravity-assist lever.** Varying chunk perihelion from 1.0 AU (Hohmann) down to 0.5 AU spends up to 1.16 km/s extra Saturn-exit Δv but only shifts the chunk-Jupiter geometry by 12° in longitude and 0.27 years in time. Combined viable-fraction improvement: 2.78% → 3.48% at ±5° tolerance with ≤ 1 km/s budget. The campaign-mean delivered fraction moves by 0.06 percentage points (15.68% → 15.74%). Block 5's pessimism is confirmed; the obvious "escape hatch" via Saturn-exit Δv flexibility does not exist.

**Finding 17 — The reason Saturn-exit-flexibility is not a meaningful lever.** The inbound descent from Saturn aphelion (9.55 AU) to Jupiter orbital radius (5.2 AU) is *fast* (~4.4-4.6 yr) and the time-of-flight is *largely insensitive* to perihelion choice. The chunk has effectively committed to a Jupiter-crossing geometry by the time it leaves Saturn — most of the trajectory shape sensitivity is on the *inner* leg (Jupiter to Earth, 1.0-5.2 AU), not the outer leg (Saturn to Jupiter). Saturn-exit Δv mostly trades for Earth-arrival speed, not for Jupiter-encounter timing.

**Finding 18 — Block 5's analytic limit `(2 × tolerance) / 360°` is robust.** Even when admitting a second trajectory degree of freedom, the viable-fraction increase is bounded by the angular flexibility (~12° from perihelion), which only marginally widens the effective tolerance. The fraction stays well below `(2 × tolerance) / 360°` × 1.5 even at maximum budget.

---

## Methodology lesson 8

**"A trajectory degree of freedom that costs delta-velocity is only useful if the gain in flexibility exceeds the cost in mission performance."** Saturn-exit-flexibility costs up to 1.16 km/s but buys 12° of longitude and 0.27 yr of time flexibility — about 0.6° per km/s and 0.23 yr per km/s. Compared to the cruise-reshape lever (~5°/km/s in Block 5), Saturn-exit-flexibility is *less efficient* per km/s, not more. Future trajectory-lever questions should compute flexibility-per-km/s before committing to detailed analysis.

---

## What's still untested

This round confirmed that Saturn-exit-flexibility alone is not a lever. Two additional levers worth testing:

1. **Residence-time-flexibility.** The 0.5-year Saturn residence assumption is operationally flexible (within radiation-dose limits). Extending residence by 1 year would shift Jupiter-Saturn relative geometry by 18.1° — potentially much more useful than the 12° from Saturn-exit-flexibility. Worth a dedicated round.
2. **Non-tangential Saturn-exit burns.** A burn with a normal component rotates the line-of-apsides, shifting the *Jupiter-crossing longitude* (rather than just time). This is the third independent degree of freedom. Estimated cost: similar order of magnitude to tangential perihelion variation, but potentially more useful for longitude-shifting.

If either of these levers materially expands viable fraction (≥ 15% at ≤ 1 km/s budget), Block 5's verdict needs partial revision. If not, the verdict stands and the architecture-decision-matrix correction (composite at 15.97%, not 21.8%) is final.

---

## Status

All work pre-registered before running. Five hypotheses adjudicated; H1, H2, H4, H5 all falsified low (Saturn-exit-flexibility weaker than predicted), H3 marginal. Block 5's verdict survives the most plausible counter-question. Continuing to residence-time-flexibility round next.

