# Round — Saturn capture using moon gravity assists

**Status:** pre-result.

**Round directory:** `water-prop/rounds/R_saturn_capture_moon_gravity_assist/`.

**Owning session:** titan (re-spawn), branch `iceberg-titan-2`.

**Date:** 2026-05-15.

---

## Question

The ICEBERG concept-of-operations puts a chemical Saturn-Orbit-Insertion burn at phase 4 and treats the target capture orbit as a free design variable. Two prior rounds (R2 and R12) have demonstrated that lunar gravity assists at Earth can shed kilometres-per-second of inbound velocity at zero propellant. Can the equivalent technique work at Saturn — using Titan and the inner moons to capture without paying the full hyperbolic-excess-velocity tax?

This is what Cassini actually did. Its 626 m/s Saturn-Orbit-Insertion burn put the spacecraft into a highly elliptical capture orbit; subsequent Titan flybys then pumped the tour over the prime-mission years at zero propellant cost. The question for ICEBERG is whether the same architecture closes for a 200–500-tonne-class iceberg-return vehicle on a tighter mission cadence than Cassini's open-ended tour.

The user prompt also asked whether capture off **all** of Saturn's moons is viable. Short answer surfaced by the literature and the moon-mass numbers: Titan dominates by a factor of roughly 5000 in GM over Rhea, the next-largest. The other moons are useful only for fine tuning, not for primary capture energy management. This round quantifies that.

## Pre-registered hypotheses

| ID | Hypothesis | Predicted range | Falsification |
|---|---|---|---|
| H1 | A single optimal Titan flyby reduces the Saturn-Orbit-Insertion propulsive burn by at least 500 metres per second at typical ICEBERG arrival hyperbolic-excess-velocity (4–7 kilometres per second). | 500 to 1500 m/s saved | falsified if < 200 or > 2500 m/s under the patched-conic model |
| H2 | A multi-Titan-flyby tour (Cassini analogue) shrinks the cumulative propulsive capture burn to no more than 200 m/s within a 36-month post-arrival pumping window. | total propulsive cost ≤ 200 m/s in ≤ 36 months | falsified if minimum propulsive cost > 400 m/s OR pumping window > 60 months |
| H3 | Inner moons (Rhea, Dione, Tethys, Mimas, Enceladus) provide a negligible additional contribution beyond Titan. Their per-flyby Saturn-frame velocity change is at most one-tenth that of Titan at comparable encounter geometry. | per-flyby delta-V ≤ 10% of Titan's | falsified if any inner moon delivers > 20% of Titan's per-flyby in Saturn-frame velocity change |
| H4 | Iapetus is occasionally useful as the outermost gravity assist for initial bound-orbit setup, but its long orbital period (79.3 days) makes it inefficient for pumping. Useful as a one-shot first-bound-orbit reducer; not useful for tour cadence. | Iapetus single-flyby delta-V ≤ 0.5 km/s; sequencing penalty > 4 months per flyby | falsified if Iapetus delivers > 1 km/s per flyby OR phasing penalty < 2 months |
| H5 | The choice of target capture-orbit apoapsis (range tested: 1.5 to 6 Titan orbital radii) affects the chemical-burn cost by less than 100 m/s. The dominant variable is the first Titan encounter geometry, not the apoapsis selection. | capture-burn cost spread across apoapsis sweep ≤ 100 m/s | falsified if apoapsis selection swings burn cost by > 200 m/s |
| H6 | (added in session: project-owner asked whether momentum exchange with a ring particle during the initial Saturn periapsis pass could brake the spacecraft.) The concept is physically real — inelastic coupling of a 200-tonne spacecraft to a 482-tonne B-ring chunk would slow the spacecraft from ~29 km/s to ~23 km/s by momentum conservation. But the relative velocity at the encounter is ~8.9 km/s, exceeding R-HE-graze-feasibility's aspirational soft-capture tolerance (64 m/s) by 139×, and the kinetic energy that must be absorbed by the bag structure (~5.6 TJ over ~1 ms encounter) destroys both the chunk and the spacecraft. | architecture-changing if feasible; falsified by the same physics that retired HE-graze | falsified if relative velocity at any ring-encounter altitude ≤ 100 m/s OR if absorbed kinetic energy ≤ 10 GJ per encounter |

## Method

### Body 1 — physics

Patched-conic two-body model. Each moon flyby is an instantaneous velocity rotation in the moon-centred frame; the Saturn-frame velocity change is computed by transforming back to the Saturn frame.

For a hyperbolic flyby of a moon with gravitational parameter mu_m at periapsis radius r_p, with relative speed v_inf at infinity:

  e = 1 + r_p · v_inf² / mu_m
  sin(theta/2) = 1 / e  (turning angle theta)
  delta-V_inf in moon frame = 2 · v_inf · sin(theta/2)  (magnitude of velocity change in moon frame)

In the Saturn frame, the spacecraft velocity vector is:

  v_sc_in (Saturn frame) = v_moon + v_inf_in  (vector sum)
  v_sc_out = v_moon + R(theta, phi) · v_inf_in

where R(theta, phi) is the rotation in the flyby plane. The Saturn-frame kinetic energy change is the difference of squared magnitudes. The largest energy loss for capture occurs when the flyby rotates v_inf_in toward anti-parallel with v_moon (purely retrograde flyby behind the moon).

For the multi-flyby tour, each subsequent encounter changes v_inf relative to the moon (because the post-flyby Saturn-frame velocity, recomputed at the next encounter, differs from the pre-flyby value). The tour effect of compounding flybys is captured by iterating the model with the spacecraft state propagated between encounters under Saturn's gravity to the next moon-encounter epoch.

### Body 2 — ephemerides

JPL Horizons API (https://ssd.jpl.nasa.gov/api/horizons.api), pulled via stdlib urllib. For each Saturnian moon of interest (Mimas, Enceladus, Tethys, Dione, Rhea, Titan, Hyperion, Iapetus, Phoebe), retrieve:

- Cartesian state vector relative to Saturn barycentre (J2000) at the nominal ICEBERG Saturn-arrival epoch of 2045-01-01 (placeholder; can be re-run for any ICEBERG arrival date).
- Osculating orbital elements (semi-major axis, eccentricity, inclination relative to Saturn equatorial plane).

These confirm the nominal orbital parameters used in the analytic model and provide the actual encounter geometry that the trajectory designer would use for tour planning. Results cached in `results/horizons/` so the round is reproducible without re-pulling.

### Body 3 — sweeps

1. Single-Titan-flyby sweep: v∞ at Saturn ∈ {4, 5, 5.44 (Hohmann), 6, 7, 8} km/s × Titan flyby altitude ∈ {500, 1000, 2000, 5000, 10000} km. Output: capture-burn saving in Saturn frame.

2. All-moons single-flyby comparison: at fixed v∞ at Saturn = 5.44 km/s, evaluate each moon's best-case Saturn-frame delta-V. Output: per-moon ranking.

3. Multi-Titan tour: starting from a post-Saturn-Orbit-Insertion ellipse with apoapsis at 2 Titan radii (Saturn-frame), simulate N = 1 to 8 sequential Titan flybys with optimal phasing. Output: cumulative capture-burn savings and pumping-window duration.

4. Apoapsis sweep: target capture orbit apoapsis ∈ {1.5, 2, 3, 4, 6} Titan radii. Output: total chemical-burn cost.

5. Iapetus-as-initial-reducer: single Iapetus flyby pre-Titan-tour. Output: whether it makes the subsequent tour cheaper.

### Validity caveats

- Patched-conic ignores Saturn's gravity perturbation during the flyby itself (it is added back in the trajectory between flybys). Standard approximation for flyby distances small compared to the moon's sphere of influence. Titan sphere-of-influence radius is about 53,000 km, so flyby altitudes below ~25,000 km are well-bounded.
- Two-body inter-flyby propagation. Real tour design uses Saturnian J2 effects and other-moon perturbations; for a leading-order capture analysis these are second-order.
- Optimal geometry assumed (the trajectory designer can phase to the right encounter direction). Real-mission availability of optimal-geometry flybys is constrained by launch-date and arrival-date phasing — covered in validity caveat, not modelled here.
- "Cumulative capture burn" includes only the propulsive component. Phasing time between flybys (operational duration in Saturn orbit) is reported separately.
- This round addresses **capture only**. It does not address (a) departure-from-Saturn delta-V (which would use the same gravity-assist mechanism in reverse), (b) chunk-rendezvous after capture (a separate problem covered by R-multi-chunk-departure-orbit), or (c) any aerodynamic capture via Titan's atmosphere (deferred to a follow-on round if H1 falsifies).

## Results

### H1 — Single Titan flyby on hyperbolic Saturn approach

| Metric | Predicted | Measured | Verdict |
|---|---|---|---|
| Capture-burn saving at v∞ = 5.44 km/s, 500 km Titan-flyby altitude | 0.5 to 1.5 km/s | **0.059 km/s** | **falsified — load-bearing** |
| Capture-burn saving at v∞ = 4.0 km/s, 500 km altitude | 0.5 to 1.5 km/s | **0.075 km/s** | **falsified — load-bearing** |
| Capture-burn saving at v∞ = 8.0 km/s, 500 km altitude | 0.5 to 1.5 km/s | **0.045 km/s** | **falsified — load-bearing** |
| Turning angle at 500 km altitude, v∞ = 5.44 km/s | n/a (diagnostic) | **17.9°** | — |

A single Titan flyby on hyperbolic Saturn approach delivers only 40–80 m/s of Saturn-frame energy reduction. The Titan turning angle is small (~18°) because the relative velocity between the spacecraft and Titan at the encounter (v_inf_moon ≈ 4 km/s) is high enough that the moon's gravity cannot deflect the velocity vector much.

H1 was wrong in the load-bearing direction — by an order of magnitude. The conventional intuition that "a Titan flyby is worth km/s" comes from Cassini's *later* tour, when its post-SOI orbit had been pumped down so that v_inf_moon was lower, giving larger turning angles.

### H2 — Multi-Titan tour (Cassini-style) for Saturn capture

| Metric | Predicted | Measured | Verdict |
|---|---|---|---|
| Cumulative propulsive cost at initial r_a = 4 × r_titan, 2 flybys | ≤ 0.2 km/s in ≤ 36 months | **1.24 km/s in ~43 days** | **falsified on propulsive cost; held on pumping window** |
| Cumulative propulsive cost at initial r_a = 3 × r_titan, 2 flybys | ≤ 0.2 km/s | **1.38 km/s** | **falsified on propulsive cost** |
| Cumulative propulsive cost at initial r_a = 2 × r_titan, 2 flybys | ≤ 0.2 km/s | **1.64 km/s** | **falsified on propulsive cost** |
| Pumping window for 2 flybys | ≤ 36 months | **~21 to 43 days depending on r_a** | **held — much faster than expected** |
| Comparison: best direct-chemical capture to (r_p = 92,000 km, r_a = r_titan) | n/a (baseline) | **1.55 km/s** | — |
| Net tour-vs-chemical savings (r_a = 4 case) | ≥ 1.0 km/s | **0.31 km/s** | **falsified — load-bearing** |

H2 was wrong about the magnitude. The Titan tour is **modestly cheaper than direct chemical capture (≈ 300 m/s saved)**, not order-of-magnitude cheaper. The dominant cost is the Saturn-Orbit-Insertion burn itself (1.2–1.6 km/s); subsequent Titan flybys further reshape the orbit but cannot eliminate the initial periapsis-lowering burn.

A subtle related finding: the multi-flyby tour, optimally tuned, drops periapsis below B-ring outer (76,000 km after 2 flybys at r_a = 2 × r_titan) and eventually inside Saturn's surface after 5–6 flybys. The operationally useful number of flybys is **2 to 3**, after which the orbit naturally lands at B-ring rendezvous geometry. More flybys add nothing.

Sanity check against Cassini's actual SOI burn (626 m/s): the model reproduces this when r_p_burn is set to 1.3 R_Saturn ≈ 80,000 km (Cassini's actual SOI periapsis between F and G rings) instead of 4 R_Saturn — Cassini paid 626 m/s by going deep, not by gravity assists.

### H3 — Inner moons negligible vs Titan

| Moon | v_orbit [km/s] | Turning angle at 200 km altitude [deg] | Saturn-frame Δv [m/s] | Fraction of Titan |
|---|---|---|---|---|
| Mimas | 14.58 | 0.027 | 5.7×10⁻⁴ | 8×10⁻⁶ |
| Enceladus | 12.67 | 0.050 | 1.6×10⁻³ | 2×10⁻⁵ |
| Tethys | 11.35 | 0.21 | 2.2×10⁻² | 3×10⁻⁴ |
| Dione | 10.00 | 0.41 | 7.2×10⁻² | 1×10⁻³ |
| Rhea | 8.49 | 0.83 | 0.22 | 3×10⁻³ |
| **Titan** | **5.63** | **19.5** | **69.6** | **1.0 (reference)** |
| Hyperion | 5.54 | 0.0091 | 1.4×10⁻⁵ | 2×10⁻⁷ |
| Iapetus | 3.26 | 0.98 | 0.099 | 1×10⁻³ |
| Phoebe | 1.99 | 0.013 | 1.1×10⁻⁵ | 2×10⁻⁷ |

H3 **holds**. No moon other than Titan delivers more than 0.3 % of Titan's Saturn-frame Δv on a single optimal flyby. The inner moons fail not because their orbital velocity is low (they are *faster* than Titan, which is favourable per the theoretical max 2·v_moon·sin(θ/2)) but because their masses are tiny — Rhea is the next-largest moon and has GM = 154 km³/s², 58× lighter than Titan. The turning angle that Rhea can impart to a 5+ km/s incoming spacecraft is under 1°.

Iapetus's per-flyby contribution (0.099 m/s) is interesting only insofar as it shows that even a 120-km³/s² moon at a less-favourable orbital velocity ranks above Rhea on this metric.

### H4 — Iapetus as initial reducer

| Metric | Predicted | Measured | Verdict |
|---|---|---|---|
| Iapetus single-flyby Saturn-frame Δv at v∞ = 5.44 km/s, 1000 km altitude | ≤ 500 m/s | **0.029 m/s** | held — well under the upper bound, but for the *opposite reason* I had in mind |
| Iapetus phasing penalty (orbital period) | > 2 months | **2.64 months (79.3 days)** | held |

H4 holds quantitatively but the reasoning was wrong. I had assumed Iapetus would be a useful initial energy reducer; in fact Iapetus is *too small* to be useful at all on a hyperbolic-Saturn-arrival geometry — its turning angle is only 0.98°, identical to Rhea's, and at 3.56 × 10⁶ km from Saturn the encounter happens with a fast-moving spacecraft (7.13 km/s at Iapetus's distance) that Iapetus cannot meaningfully bend.

**Iapetus is not useful as a Saturn-capture gravity assist.** It is useful for inclination changes (Cassini used Iapetus to reach high-inclination ring observations), but inclination management is outside this round's scope.

### H5 — Capture-orbit apoapsis selection

| Initial apoapsis | Pre-flyby SOI burn cost | Direct-chemical alternative (no tour) |
|---|---|---|
| 1.5 × r_titan | 1.89 km/s | n/a |
| 2.0 × r_titan | 1.64 km/s | 1.55 km/s (to apoapsis = r_titan, r_p = B-ring) |
| 3.0 × r_titan | 1.38 km/s | — |
| 4.0 × r_titan | 1.24 km/s | — |
| 6.0 × r_titan | 1.10 km/s | — |

H5 **falsified**. Apoapsis choice swings SOI burn cost by **790 m/s** across the range tested, far exceeding the predicted ≤ 100 m/s. This is a real design lever: pushing apoapsis from 2 × r_titan to 6 × r_titan saves 540 m/s of propellant. The tradeoff is the first-Titan-encounter phasing — at r_a = 6 × r_titan the spacecraft period is ~140 days and a poorly-phased arrival could cost an extra 70 days of tour design before the first encounter.

The true dominant variable is **periapsis depth at the SOI burn**, not apoapsis. The basic chemical-rocket gravity-well leverage says: burn as deep as you can. Cassini's 1.3 R_Saturn SOI periapsis is the canonical example. For ICEBERG, B-ring outer (≈1.53 R_Saturn) gives most of the benefit at acceptable ring-crossing risk.

### H6 — Chunk-capture-as-brake during SOI

| Geometric input | Value |
|---|---|
| Spacecraft speed at B-ring outer on hyperbolic approach (v∞ = 5.44 km/s) | 29.2 km/s |
| B-ring particle circular-orbit speed at 92,000 km | 20.3 km/s |
| Relative velocity at encounter | **8.9 km/s** |
| Aspirational bag soft-capture tolerance (per R-HE-graze-feasibility) | 64 m/s |
| Excess factor | **139×** |
| Combined-system velocity if inelastic coupling worked (m_sc = 200 t, m_chunk = 482 t) | 22.9 km/s |
| Net spacecraft Δv if coupling worked | 6.3 km/s |
| Kinetic energy in the reduced-mass frame | 5.6 TJ |
| Encounter duration at chunk diameter ~4 m / v_rel | ~0.5 ms |
| Vaporization-enthalpy budget for the chunk (water) | 1.1 TJ |
| Energy remaining post-vaporization | 4.5 TJ (destroys the spacecraft) |

H6 **falsified by the same physics that retired HE-graze**. The momentum-exchange concept is real — if you could couple the masses, you would brake the spacecraft by 6.3 km/s — but the relative velocity required to MAKE the encounter happen (8.9 km/s) is in the bulk-vaporization regime for any plausible bag material. The spacecraft and chunk both come apart, and there is no water gain. Closing the trap: the only place ring particles exist is between r = 67,000 km and r = 140,000 km, where their orbital velocities (16.5 to 25.2 km/s) are always significantly slower than any spacecraft arriving from a hyperbolic Saturn approach, regardless of approach geometry.

The only escape route is a chemical pre-match of velocities — i.e., a full SOI burn that drops the spacecraft into a near-circular orbit at B-ring radius before approaching the chunk. That burn costs ~9 km/s of chemical, dramatically more than capturing into a normal Cassini-style orbit and rendezvousing with chunks later from the bound orbit.

## Reading

This round confirms what R-HE-graze-feasibility surfaced and extends it: **Saturn-system geometry is hostile to "free" capture mechanisms that depend on relative velocities below the bag soft-capture tolerance**. The two relevant cases now resolved:

1. *Pre-capture chunk grab on the hyperbolic approach* (R-HE-graze): 6.6 km/s relative velocity at periapsis — 102× the soft-capture limit.
2. *Capture-as-brake using a B-ring chunk during SOI* (this round, H6): 8.9 km/s relative velocity — 139× the limit.

Both fail for the same reason. The escape route in both cases is a substantial chemical burn first, after which the rendezvous looks like a normal post-capture operation.

What this round *does* establish positively:

- **The Cassini-style Saturn capture works for ICEBERG, with modest gravity-assist savings.** Best total propulsive cost is ~1.24 km/s using a Titan tour starting from initial apoapsis ≈ 4 × r_titan, vs ~1.55 km/s for the cheapest direct chemical capture. Savings ≈ 310 m/s.
- **The dominant lever for cheap capture is the SOI periapsis depth, not the tour design.** Going from r_p_burn = 4 R_Saturn to r_p_burn = 1.3 R_Saturn (Cassini's actual periapsis) drops the SOI cost from ~1.55 km/s to ~626 m/s — a 920 m/s saving, 3× larger than the Titan-tour benefit.
- **The right operational sequence for ICEBERG**: small SOI burn at low periapsis (just outside the F-ring at ~80,000 km, similar to Cassini) into an ellipse with apoapsis at 3–4 × r_titan, then 2 Titan flybys over ~30–50 days to pump periapsis down to B-ring outer (~92,000 km). Total propulsive ~0.7 km/s SOI + ~0 trim = ~0.7 km/s.

## Cross-learning

Three findings propagate to other rounds:

1. **R-HE-graze-feasibility generalises.** The "no soft capture above ~100 m/s relative velocity" wall is now established for both the inbound-chunk-grab geometry AND the SOI-chunk-grab geometry. Any future architecture proposal that depends on capture relative-velocities above the bag tolerance is automatically suspect and needs an explicit propulsion budget for the velocity match.

2. **The ARCHITECTURE-DECISION-MATRIX should treat Saturn-side capture as a ~0.7 km/s line item, not a free placeholder.** Prior matrix variants had the SOI burn implicit (rolled into "Saturn capture") or omitted; this round bounds it at 0.6 to 1.6 km/s depending on periapsis-depth choice. The 0.7 km/s recommended-baseline is a meaningful chunk of the overall propulsive budget.

3. **The conops phase-4 "Saturn capture" should be reframed.** Currently the conops treats this as a single chemical maneuver. The recommended architecture is *Cassini-pattern*: small SOI burn at deep periapsis, 2–3 Titan flybys over 1–2 months to lower periapsis to B-ring outer. This is a multi-month operational phase, not a single burn — has implications for phase-4 mission timing and for the R-mission-success-probability redundancy budget (multiple Titan encounters = more failure opportunities).

## Open threads for follow-on rounds (orchestrator-routed, not Titan-owned)

| Round | Priority | Notes |
|---|---|---|
| R-saturn-soi-periapsis-depth | high | Sweep r_p_burn ∈ [1.3, 4] R_Saturn × ring-crossing collision probability. Cassini did 1.3 R_S; can ICEBERG? Trade is SOI-cost vs ring-crossing risk. |
| R-inclination-management-iapetus | low | Iapetus failed as a capture tool but is the only useful Saturn moon for inclination changes. Likely de-prioritised — ICEBERG doesn't need high-inclination ops. |
| R-multi-moon-tour-design | de-prioritised | Per H3, no inner moon is useful. Tour design = Titan-only. |

