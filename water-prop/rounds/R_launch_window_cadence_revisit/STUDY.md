# R-launch-window-cadence-revisit

**Worker:** titan (Block 5)
**Owner:** project owner / orchestrator
**Pre-registration date:** 2026-05-15

---

## Motivation

R-residence-exit-maneuver (Block 4) closed the residence-class ram-scoop architecture at central 21.8% delivered fraction. That number depends on Jupiter return gravity-assist contributing ~2.5 kilometres-per-second of inbound velocity reduction. STUDY.md §285 noted that "roughly half of all Earth-Saturn return windows have a viable Jupiter swing-by" but did not actually compute the fraction.

The current concept-of-operations and demand documents assume launch cadence is set by the Earth-Saturn synodic period (~378 days). If Jupiter-return-gravity-assist alignment is load-bearing, the effective launch cadence is constrained by the Jupiter-Saturn synodic period (~19.86 years), not just Earth-Saturn. Whether this matters depends on:

1. Angular tolerance for a useful Jupiter flyby on the inbound trajectory.
2. Whether non-Jupiter-aligned launch windows are skipped, or flown with reduced delivered fraction (composite without Jupiter return-leg gravity-assist drops to ~14-17%).
3. Whether the inbound trajectory can be re-shaped (at modest velocity cost) to widen the Jupiter-encounter window.

This round quantifies the fraction and translates it into effective cadence for the demand model.

---

## Pre-registered hypotheses

| # | Hypothesis | Prediction | Falsification rule |
|---|---|---|---|
| H1 | Useful Jupiter return gravity-assist requires Jupiter to be within ±5 degrees of the chunk's Jupiter-orbit-crossing point on the inbound Hohmann-equivalent trajectory. | ±5° angular tolerance gives ~ 1 in 3 Earth-Saturn launches a Jupiter-viable return. | Falsified if a wider tolerance (±10°+) is needed for useful gravity-assist, or if the fraction is < 0.20 or > 0.50 at ±5°. |
| H2 | The "useful-Jupiter-aligned" fraction over a 60-year span clusters into 1-3 launch opportunities per 19.86-year Jupiter-Saturn cycle, separated by long droughts. | Bursts of 1-3 consecutive Jupiter-viable Earth-Saturn synodics, then 5-15 unaligned synodics. | Falsified if Jupiter-viable windows are approximately uniformly distributed (no clustering). |
| H3 | Under "skip unaligned windows" policy: effective cadence drops from 1 ship per 1.035 yr to 1 ship per (5-10 yr), throughput drops 4-10×. | Effective cadence ∈ [4.0, 10.0] years per Jupiter-viable launch. | Falsified if effective cadence < 3.0 yr or > 12.0 yr at ±5° tolerance. |
| H4 | Under "fly all windows, accept reduced delivered fraction on unaligned" policy: long-run throughput drops only modestly because most missions still close (just at lower delivered fraction). The campaign-level expected delivered fraction lands in [16%, 19%]. | Expected delivered fraction = 0.50 × 21.8% + 0.50 × 15.5% ≈ 18.6% under H1's central tolerance. | Falsified if expected delivered fraction < 15% or > 21% under H1's tolerance. |
| H5 | Modest inbound-trajectory reshaping (up to 0.5 kilometre-per-second additional velocity cost during cruise) widens the angular tolerance from ±5° to ±15°, raising Jupiter-viable fraction substantially. | At 0.5 kilometre-per-second cruise reshape budget, Jupiter-viable fraction rises to ≥ 0.70. | Falsified if reshape budget < 0.5 kilometre-per-second doesn't materially widen the Jupiter-viable fraction, or > 1.0 kilometre-per-second is needed to reach 0.70. |

---

## Method

**Orbital model.** Coplanar circular orbits for Earth (1.0 astronomical units, 1.0 year period), Jupiter (5.2 astronomical units, 11.862 year period), Saturn (9.55 astronomical units, 29.457 year period). Heliocentric longitudes propagated linearly. Initial conditions: all three planets at heliocentric longitude 0 at t = 0 (worst-case alignment baseline; final answer is rotation-invariant).

**Mission timeline per launch window.** Earth-Saturn launches at t_n = n × τ_ES (τ_ES = 1.0352 year) for n = 0...57 (60-year span). Outbound Hohmann transfer 6.04 year. Residence 0.5 year. Inbound Hohmann-equivalent transfer from Saturn (aphelion, 9.55 astronomical units) to Earth (perihelion, 1.0 astronomical units).

**Jupiter-orbit-crossing computation.** On the inbound Hohmann trajectory, the chunk crosses Jupiter's orbital radius (5.2 astronomical units) at a specific true anomaly. From the Hohmann ellipse (semi-major-axis 5.275 astronomical units, eccentricity 0.81), this true anomaly is 216.8 degrees (descending leg from aphelion ν=180° to perihelion ν=360°/0°). The time from Saturn-exit (aphelion) to Jupiter-orbit-crossing is computed via Kepler's equation: convert true anomaly to eccentric anomaly to mean anomaly, then to time.

**Heliocentric longitude at crossing.** True anomaly is measured from perihelion (= Earth-arrival point) at the Sun. Heliocentric longitude of the chunk at Jupiter-orbit-crossing equals the heliocentric longitude of the line-of-apsides (Earth-arrival direction) plus 216.8°. The line of apsides is fixed in space: it connects the Saturn-exit point (aphelion) to the Earth-arrival point (perihelion). For each launch n, Saturn's heliocentric longitude at exit (and thus the line-of-apsides orientation) is computed from Saturn's orbital motion.

**Jupiter-viable test.** For each launch n, compute (a) chunk's heliocentric longitude at Jupiter-orbit-crossing time t_cross(n), and (b) Jupiter's heliocentric longitude at the same time. Angular separation modulo 360 degrees, signed within [-180°, +180°]. Window is Jupiter-viable if |separation| ≤ tolerance.

**Tolerance sweep.** Compute Jupiter-viable fraction at ±2°, ±5°, ±10°, ±15°, ±30°.

**Effective cadence.** Under "skip unaligned" policy, mean inter-launch interval = (total time span) / (number of Jupiter-viable launches). Under "fly all windows" policy, cadence stays 1.035 year but campaign-mean delivered fraction is weighted by Jupiter-viable fraction.

**Cruise-reshape sensitivity (H5).** Wider tolerance simulates trajectory reshape capability. Compute Jupiter-viable fraction across tolerance grid.

**Output.** Per-window CSV (launch index, launch year, Saturn-exit year, chunk Jupiter-crossing longitude, Jupiter longitude, separation, viable-at-each-tolerance flags). Summary JSON with fractions and effective cadences.

---

## Limitations of this model

- Coplanar circular orbits ignore Saturn (2.5°) and Jupiter (1.3°) inclinations and small eccentricities. Real-world tolerance is somewhat tighter than the planar model suggests.
- Hohmann inbound is a simplification of continuous-thrust inbound. Real continuous-thrust trajectories have different Jupiter-crossing geometry; the tolerance for "useful flyby" is the binding parameter and is set by patched-conic gravity-assist physics, not Hohmann-specific timing.
- "Useful flyby" is defined as Jupiter being within angular tolerance of the chunk's natural crossing point. This is a necessary but not sufficient condition: the flyby must also produce a bending angle that points the post-flyby velocity vector toward Earth at the correct arrival epoch. The tolerance sweep absorbs some of this; ±5° is a reasonable proxy for "useful at modest trajectory cost."
- Cruise-reshape budget (H5) is parameterized as widening the tolerance, not as an actual trajectory-optimization computation. A real reshape adds ΔV during cruise; the equivalence to angular tolerance is approximate.
- Triple-synodic constraint formally also requires Earth-Jupiter alignment at the Earth-arrival epoch, but the chunk's heliocentric trajectory is determined by Saturn-exit and the Jupiter swing-by, not by Earth-Jupiter geometry directly. Earth-Jupiter geometry is therefore a derived constraint, not a separate one.
- Saturn-exit ΔV vector has flexibility (chunk can leave Saturn at slightly different headings). This flexibility is not modeled; ±5° tolerance is a conservative proxy.

---

## Decision rule

After results land:

- **If Jupiter-viable fraction at ±5° tolerance ∈ [0.30, 0.60]:** the "roughly half" assumption from R-residence-exit-maneuver is corroborated. Update demand docs to reflect skip-or-reduced-fraction policy.
- **If fraction < 0.30:** Jupiter return gravity-assist is materially harder to schedule than assumed. The composite's 21.8% headline becomes a best-window number, not a steady-state number. Demand docs must be rewritten with reduced expected delivered fraction (closer to 15-17%, the no-Jupiter composite).
- **If fraction > 0.60:** the constraint is less binding than assumed. The composite's 21.8% is closer to steady state. Demand model is robust.
- **If cruise-reshape (H5) gets fraction to ≥ 0.70 at ≤ 0.5 kilometre-per-second cost:** reshape is the right operational answer. Document the velocity-budget hit and confirm composite delivered fraction is still ≥ 17%.

Findings propagate into:
- ICEBERG-demand.md: revenue cadence rows.
- ICEBERG-conops.md §"Launch cadence — when to send the next one": replace 13-month cadence with Jupiter-aware cadence.
- Architecture decision matrix: residence-class delivered-fraction row needs a footnote on Jupiter return gravity-assist availability.

---

## Results

### Geometric Jupiter-viable fraction (no cruise reshape)

The chunk's natural Hohmann inbound trajectory crosses Jupiter's orbital radius at true anomaly 216.4° (the descending leg from Saturn aphelion), 4.63 years after Saturn departure. The chunk's heliocentric longitude at that crossing is fixed relative to Saturn-at-exit. As successive Earth-Saturn launches step through Saturn's orbit, the chunk-Jupiter angular separation at the crossing point sweeps linearly through 360 degrees with period 19.85 years (the Jupiter-Saturn synodic period).

Phase-ensemble averaged over 360 Jupiter initial-phase samples — equivalently, the long-run uniform-distribution limit:

| Tolerance | Viable fraction (analytic = ensemble) |
|---|---|
| ±2° | 1.11% |
| ±5° | 2.78% |
| ±10° | 5.56% |
| ±15° | 8.33% |
| ±30° | 16.67% |

The viable fraction is exactly `(2 × tolerance) / 360°` — the angular separation between the chunk's natural crossing point and Jupiter is uniformly distributed over the Jupiter-Saturn synodic cycle. Block 4's "roughly half of all return windows" assumption was off by a factor of ~18 at ±5° tolerance. Source of the error: confusing "Jupiter is on the same side of the Sun as the chunk's trajectory" (~50%) with "Jupiter is close enough to the chunk's natural crossing point for a useful gravity-assist" (≤ 3% at ±5°).

### Cruise-delta-velocity cost of widening the tolerance

Active cruise reshape can bring the chunk to Jupiter even when the natural trajectory misses by Δθ. Under a constant-cross-track-acceleration model over the 4.63-year Saturn-to-Jupiter leg:

| Angular shift | Cross-track velocity cost | Jupiter-GA saving | Net |
|---|---|---|---|
| ±2°  | 0.37 km/s | 2.5 km/s | **+2.13 km/s** |
| ±5°  | 0.93 km/s | 2.5 km/s | **+1.57 km/s** |
| ±10° | 1.85 km/s | 2.5 km/s | **+0.65 km/s** |
| ±15° | 2.76 km/s | 2.5 km/s | -0.26 km/s |
| ±30° | 5.33 km/s | 2.5 km/s | -2.83 km/s |

Self-consistent maximum tolerance (where reshape stays net-positive against the 2.5-km/s Jupiter-GA benefit): **±13.5°**.

Phase-averaged Jupiter-viable fraction at ±13.5°: **7.50%**.

### Cadence policy implications

Under "skip unaligned, fly only Jupiter-viable windows":

| Tolerance | Viable fraction | Effective launch cadence |
|---|---|---|
| ±5°    | 2.78%  | 37.2 years per launch (1 ship every ~36 yr) |
| ±10°   | 5.56%  | 18.6 years per launch |
| ±13.5° (self-consistent) | 7.50% | 13.8 years per launch |
| ±15°   | 8.33%  | 12.4 years per launch |

Under "fly all Earth-Saturn synodic windows, accept reduced delivered fraction on the unaligned majority":

| Tolerance | Viable fraction | Campaign-mean delivered fraction per ship |
|---|---|---|
| ±5°    | 2.78%  | 0.0278 × 21.8% + 0.9722 × 15.5% = **15.68%** |
| ±10°   | 5.56%  | 15.85% |
| ±13.5° | 7.50%  | 15.97% |
| ±15°   | 8.33%  | 16.03% |

Steady-state campaign-mean delivered fraction is ~15.7-16.0% across the Δv-positive tolerance range. **The composite's 21.8% is a 7.5%-of-windows number, not a steady-state number.** The 92.5% of launches without Jupiter alignment deliver at the no-Jupiter composite (A2+A5+A6 only) of ~15.5%.

---

## Hypothesis adjudication

| # | Prediction | Realized | Status |
|---|---|---|---|
| H1 | ±5° tolerance gives ~ 1-in-3 viable; fraction ∈ [0.20, 0.50] | Phase-ensemble = 2.78% | **falsified low** |
| H2 | Viable windows cluster in bursts of 1-3 per Jupiter-Saturn cycle separated by long droughts | Viable windows are uniformly distributed, ~one per (360/18.77°)/synodic = 19.18 synodics, no clustering | **falsified** — the structure is uniform, not clustered |
| H3 | Skip-unaligned effective cadence ∈ [4, 10] yr | At ±5°: 37 yr; at ±13.5° self-consistent: 13.8 yr | **falsified high** |
| H4 | Fly-all campaign-mean delivered fraction ∈ [0.16, 0.19] at ±5° | 15.68% (just below the band) | **falsified low** (barely) |
| H5 | At ±15° proxy (≤ 0.5 km/s reshape budget), viable fraction ≥ 0.70 | At ±15°: 8.33%, and the reshape budget for ±15° is 2.76 km/s, not 0.5 km/s | **falsified** |

**Every pre-registered hypothesis was wrong in the same direction:** the Jupiter return gravity-assist is much harder to schedule than expected, by roughly an order of magnitude.

---

## Findings

**Finding 11 — Jupiter return gravity-assist is structurally not a load-bearing operational lever.** Even with cruise reshape spending the maximum Δv that still yields net Jupiter-GA benefit (±13.5° tolerance, 2.76 km/s reshape ≈ 2.5 km/s saving — actually marginally negative), only 7.5% of Earth-Saturn launch windows admit a useful Jupiter swing-by. At the strict net-positive boundary (~±10°, 1.85 km/s reshape), viability is 5.6%.

**Finding 12 — The composite architecture's steady-state delivered fraction is ~16%, not 21.8%.** The 21.8% headline from R-residence-exit-maneuver applies only to the ~7.5% of windows where Jupiter alignment is achievable at acceptable cost. The other 92.5% of windows operate at A2+A5+A6 (aerocapture + Isp uplift + jettison, no Jupiter GA), delivering ~15.5%. The expected-value campaign-mean is 0.075 × 0.218 + 0.925 × 0.155 = 0.1597.

**Finding 13 — The residence-class architecture remains net-positive vs the no-aerocapture baseline (3.5%), but no longer exceeds Option A's 17%.** Block 4's "ram-scoop pivot beats Option A by ≥ 5 percentage points" verdict is overturned. The residence-class composite is *Option-A-equivalent* (~16% vs 17%), not Option-A-superior. The architecture is still preferable on grounds of physical feasibility (Option A's HE-graze was independently falsified), but the delivered-fraction headline that argued for the pivot is closer to a wash.

**Finding 14 — Earth-Saturn launch cadence is *not* materially constrained by Jupiter alignment if the campaign accepts the lower delivered fraction.** Under fly-all-windows policy, cadence stays at one ship per 1.035 yr (the Earth-Saturn synodic). The Jupiter constraint shows up as a per-ship delivered-fraction discount, not a cadence slowdown. Demand-model implication: cadence assumption (13 months) stays valid; per-ship delivered tonnage discount is the operative correction.

**Finding 15 — A campaign that requires Jupiter GA on every flight is fatally cadence-limited.** Skip-unaligned policy at the geometric net-positive tolerance (±10°) gives 1 launch per ~18.6 years. At ICEBERG's mission timescale and operating costs, this is roughly a hundred-million-dollar-per-year program with a single delivery every ~32 years (18.6 yr cadence + 13.5 yr round-trip). Not commercially viable. The fly-all-windows policy is the only operable choice; Jupiter GA must be treated as an occasional bonus, not a design lever.

---

## Methodology lesson 7

**"Synodic-style alignments between three or more bodies scale as the product of the constraint tolerances divided by 360°, not as the looser pairwise alignment intuition suggests."** Block 4's "roughly half" assumed Earth-Saturn synodic windows have roughly even odds of hitting Jupiter alignment. They do not — the Jupiter-Saturn synodic cycle makes Jupiter alignment a separate, near-independent constraint that scales as (2 × tolerance) / 360° in the long run. Multi-body alignment availability collapses much faster than two-body intuition predicts.

---

## Limitations and what would change the answer

- **Coplanar circular orbits.** Real Saturn and Jupiter have 2.5° and 1.3° inclinations and small eccentricities; tolerances are slightly tighter in 3D. First-order effect on viable fraction: ~10-30% relative reduction (i.e. 2.78% → 2.0-2.5% at ±5°). Does not change the order-of-magnitude conclusion.
- **Hohmann inbound is a simplification of continuous-thrust.** A continuous-thrust trajectory has flexibility to time the Jupiter encounter independently of the Saturn-exit-time-determined "natural" crossing. This flexibility is partially captured by the cruise-reshape tolerance sweep. The full continuous-thrust solution is a trajectory-optimization problem; first-order effect on Jupiter-viable fraction at a fixed Δv budget is bounded by the reshape-cost calculation (no free lunch on geometry).
- **Saturn-exit direction is fixed.** A real mission has some freedom in exit-burn direction. This translates to additional "inbound-trajectory family" freedom that could marginally widen Jupiter-encounter accessibility, but the Saturn-exit Δv is large (~7.4 km/s) and most of it is spent fighting Saturn's gravity, leaving little tangential-direction freedom.
- **Jupiter-GA effective Δv saving is anchored at 2.5 km/s.** This is the Block-4 round's central estimate. Higher savings (3-4 km/s) shift the self-consistent tolerance to ±20° and viable fraction to ~11-12%, but the cruise-Δv cost growth is super-linear in tolerance (sin-related), so even doubling the GA benefit only modestly widens the self-consistent window.
- **Did not model "Jupiter-targeted launches."** A campaign could schedule launches specifically at Jupiter-Saturn-aligned synodic windows (the ~7.5% subset) and skip the unaligned majority. This is the skip-unaligned policy; its 14-37 yr effective cadence is the killer.

A real campaign-planning round would build a Lambert-arc trajectory optimizer with cruise Δv as the cost function, an actual Jupiter-flyby model with close-approach altitude, and 3D ephemerides for Saturn / Jupiter / Earth. This round's coplanar-Hohmann analysis is sufficient to retire the Jupiter-GA-as-load-bearing-lever assumption; refinement would change the headline numbers within ~30% but not the structural conclusion.

---

## Propagation to shared documents (orchestrator-owned)

1. **Architecture decision matrix.** The residence-class composite row's delivered-fraction entry should read "**15.7-16.0% steady state** (21.8% at the ~7.5% of windows with Jupiter alignment available)" with a footnote pointing to this round. The previous "21.8% delivered, near Option-A-parity-or-better" claim is no longer supported as a steady-state number.

2. **ICEBERG-conops.md §"Launch cadence."** Add a Jupiter-alignment paragraph: cadence stays at 1.035 yr under fly-all-windows policy; per-ship delivered fraction averages 15.97%; ~7.5% of launches realize the full composite 21.8%.

3. **ICEBERG-demand.md.** Revenue cadence is unchanged (1.035 yr per ship), but per-ship delivered tonnage should be discounted from the 21.8% composite to 15.97% campaign-mean. At a 482-tonne accretion fill, expected delivered chunk is 77 tonnes per ship rather than 105 tonnes per ship. ~25% revenue-tonnage reduction.

4. **R-residence-exit-maneuver STUDY.md.** No edit (worker-owned), but its §285 "roughly half of all return windows" remark is superseded by this round's 2.78% finding; the Block-4 summary statement that the composite "exceeds Option A by 10pp in best case" should be footnoted: best-case ~22% but campaign-mean ~16%.

5. **PROTOCOL.md (methodology lessons).** Add lesson 7 (multi-body alignment scaling).

---

## Status

All work pre-registered before running. Hypotheses adjudicated against pre-registered falsification rules. Every hypothesis falsified in the same direction (more pessimistic than expected). Block 4's architecture-rescue verdict survives but with a substantially reduced delivered-fraction headline. Architecture remains operationally feasible and net-positive vs no-aerocapture baseline, but no longer Option-A-superior.

Round commits: see SESSION-LOG or the worker handoff at `~/.claude/handoffs/iceberg-titan-20260515-launch-window-cadence.md`.

