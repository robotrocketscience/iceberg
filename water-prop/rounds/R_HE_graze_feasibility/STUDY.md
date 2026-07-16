# R-HE-graze-feasibility — can a high-elliptical Saturn orbit grazing the B-ring actually capture chunks?

**Author:** Titan (re-spawn)
**Status:** pre-registered.
**Branch:** `iceberg-titan-2`.
**Date:** 2026-05-16.
**Protocol:** per `water-prop/PROTOCOL.md`.
**Predecessor this session:** R-multi-chunk-departure-orbit (commit `e8ca28b`).

---

## Motivation — the assumption being questioned

R-multi-chunk-departure-orbit bracketed two architectures for multi-chunk operations:

- **Case BR-direct:** capture in B-ring orbit, depart inbound from there. Δv = 40.2 km/s. N=10 chunks deliver 549 t (regulated-utility); N=23 for venture-class (infeasible).
- **Case HE-graze:** capture during a single periapsis pass through B-ring on a high-elliptical Saturn orbit, then depart inbound from high-elliptical. Δv = 24.4 km/s. N=10 chunks deliver 1291 t (venture-class).

The prior round noted that Case HE-graze "has its own un-litigated operational-feasibility burden" but did not test it. This round tests it.

**The specific question:** can the spacecraft actually capture chunks during a high-elliptical periapsis pass at the orbital relative velocities involved? The basic physics check is whether the relative velocity between a spacecraft on a high-elliptical Saturn orbit (periapsis inside B-ring) and the ring particles (in B-ring circular orbit) is compatible with soft-capture mechanisms.

If the relative velocity is high, the kinetic energy involved in capturing a 482-tonne chunk is enormous. Capture-by-collision becomes hypersonic-impact destruction; capture-by-bag becomes bag-vaporisation. The only way to soft-capture is to match orbital velocity — which requires being in B-ring orbit, not high-elliptical.

## Pre-registered hypotheses (H-hgf)

**Aggregate (H-hgf-agg):** Relative velocity between an HE-graze spacecraft and B-ring particles at periapsis is in the range 5 to 10 km/s — far above the soft-capture threshold for a deployable bag. Capture at this relative velocity is physically infeasible: the kinetic energy absorbed during impact exceeds the structural limits of any plausible capture mechanism. **Case HE-graze in the prior round is therefore not operationally realisable as a fast-flyby capture mode.** The only physically-realisable capture mode requires matching orbital velocity at B-ring radius (circular or near-circular B-ring orbit), which is operationally equivalent to Case BR-direct. **The R-multi-chunk-departure-orbit "HE-graze" case is best-case theoretical, not operationally accessible; BR-direct is the binding architecture for multi-chunk operations.**

| Sub-claim | Description | Predicted | Falsification |
|---|---|---|---|
| H-hgf-a | Relative velocity at periapsis between an HE-graze spacecraft (periapsis 105k km, apoapsis 1M km) and B-ring particles co-orbiting at 105k km circular | 7–8 km/s | outside [5, 10] km/s |
| H-hgf-b | Kinetic energy involved in capturing a 482-tonne chunk at HE-graze periapsis relative velocity | 10–15 terajoules | outside [5, 25] TJ |
| H-hgf-c | Maximum relative velocity at which a deployable bag can soft-capture a 482-tonne chunk, given typical aerospace bag-structure energy-absorption limits | < 100 m/s | falsified if a credible bag design tolerates > 1 km/s impact |
| H-hgf-d | Delta-velocity required to circularise at B-ring radius from the HE-graze high-elliptical orbit before capture | 6–8 km/s | outside [5, 10] km/s |
| H-hgf-e | Periapsis-pass duration in the upper B-ring radial extent (r ∈ [105, 117.5] thousand km, periapsis at 105k km) | 90–150 minutes | outside [60, 200] minutes |
| H-hgf-f | The HE-graze architecture as drawn in R-multi-chunk-departure-orbit is operationally realisable for multi-chunk soft-capture | falsified | "held" if a credible operational mode emerges at relative velocity < 1 km/s |

**Aggregate grading rule:**

- If H-hgf-a and H-hgf-c both hold, HE-graze is falsified as a soft-capture architecture. Multi-chunk operations must use BR-direct.
- If H-hgf-f is falsified, R-multi-chunk-per-mission's "venture-class reachable at N=5 with Starship launch" must be retracted; the binding multi-chunk envelope is the BR-direct case, where venture-class requires N=23 (operationally implausible).

## Method

### HE-graze orbit geometry

Spacecraft orbit:
- Periapsis r_p = 105,000 km (mid-B-ring; Saturn's B-ring extends from r=92,000 to r=117,500 km from Saturn's centre)
- Apoapsis r_a = 1,000,000 km (matches matrix's "high-elliptical" departure orbit)
- Semi-major axis a = (r_p + r_a)/2 = 552,500 km
- Eccentricity e = (r_a − r_p)/(r_a + r_p) = 0.810
- Period T = 2π × √(a³/GM_Saturn) ; GM_Saturn = 3.793 × 10⁷ km³/s²

### Velocities at periapsis

Spacecraft velocity at periapsis:

    v_p_spacecraft = √(GM_Saturn × (2/r_p − 1/a))

B-ring particle velocity (circular orbit at r_p):

    v_p_particle = √(GM_Saturn / r_p)

Relative velocity = v_p_spacecraft − v_p_particle (both prograde, in plane).

### Kinetic energy of impact

For a 482-tonne chunk at relative velocity v_rel:

    KE = 0.5 × m × v_rel²

Compare against typical aerospace bag-structure energy absorption (deployable inflatable structures, drag chutes, etc.): rough order ~10 MJ for a 100-square-metre bag rated for crushing loads in the 0.1-1 km/s range.

### Circularisation delta-velocity

To match orbital velocity at B-ring radius from the HE-graze orbit:

    Δv_circ = v_p_spacecraft − v_p_particle

(This is identical to the relative-velocity calculation — a circularisation burn at periapsis converts the velocity vector at r_p from the high-elliptical value to the circular value.)

### Periapsis-pass duration

Time spent in the B-ring radial range. For periapsis at r_p = 105k km (inside the B-ring), the spacecraft's radial range is [r_p, r_a]. The portion of the orbit at r ∈ [105k, 117.5k] (the part of the B-ring accessible without dipping below periapsis) corresponds to true anomaly θ ∈ [−θ_max, +θ_max] where:

    r(θ) = a(1−e²) / (1 + e cos θ)
    Solve for θ at r = 117.5k

Convert true anomaly to mean anomaly via eccentric anomaly:

    tan(E/2) = √((1−e)/(1+e)) × tan(θ/2)
    M = E − e sin(E)

Time = T × M_max / (2π)

### Bag-structure soft-capture limit

Pulled from published aerospace deployable-structure literature (rough order). Inflatable decelerators / supersonic-inflatable-aerodynamic-decelerators have demonstrated 5–10 g deceleration loads at relative velocities up to ~1.5 km/s in Earth-atmosphere entry; vacuum bag soft-capture for multi-tonne payloads has been demonstrated in the m/s range (rendezvous-and-docking). For 482-tonne chunks, the binding constraint is the bag's structural mass and the energy it can absorb without rupture. A rough order-of-magnitude for a 100-square-metre aerospace-grade bag: energy absorption capacity ~10–100 MJ, which corresponds to capturing a 482-tonne chunk at v_rel = 10–30 m/s. Anything above ~100 m/s is essentially structural failure of the bag.

### Validity caveats

1. The 100-MJ bag-energy-absorption number is a rough engineering estimate, not a calibrated number. R-bag-multichunk-mass (queued downstream) would refine it. For this round, an order-of-magnitude check is sufficient: even granting 10× the assumed limit, soft-capture at 7 km/s is infeasible by ~5 orders of magnitude.

2. The analysis assumes prograde-co-orbital relative velocity. A retrograde spacecraft orbit grazing the B-ring would have ~2× higher relative velocity (catastrophic). A polar spacecraft orbit would have orthogonal velocity (also catastrophic and outside the ring plane). The prograde case is the best-case for HE-graze.

3. Ring-particle eccentricities in B-ring are very small (Cassini observations show e < 0.0001 for most particles). Particles are nearly in circular orbit; HE-graze relative-velocity calculation against circular-orbit particles is accurate.

4. Bag-deployment time and chunk-acquisition time are not modelled. Even granting infinite-strength bag, the operational window during periapsis pass would constrain N captures. This round handles this in the duration calculation only.

5. The analysis ignores the option of using ring-particle aerodynamic-style braking before capture (deploying a drag skirt to slow the spacecraft via ring-particle impacts). R-deployable-drag-skirt may have addressed this; not investigated here.

### Revisit clause

Per-claim grading vs H-hgf-a..f. Cross-learning identifies whether the HE-graze finding falsifies R-multi-chunk-per-mission's venture-class claim and what operational alternatives (if any) remain.

## Result

**HE-graze reference orbit (periapsis 105k km, apoapsis 1 million km):**

| Quantity | Value |
|---|---:|
| Spacecraft velocity at periapsis | 25.57 km/s |
| B-ring particle velocity at periapsis (circular orbit) | 19.01 km/s |
| Relative velocity at periapsis | **6.56 km/s** |
| Orbital period | 4.85 days |
| Time in upper B-ring per periapsis pass | 104 minutes |

**Impact kinetic energy for a 482-tonne chunk at 6.56 km/s relative velocity:**

| Quantity | Value |
|---|---:|
| Kinetic energy | 10.38 terajoules |
| TNT equivalent | 2,482 tons |

**Maximum tolerable relative velocity for soft-capture of a 482-tonne chunk (bag-energy-absorption-limited):**

| Bag class | Energy limit | Max v_rel |
|---|---:|---:|
| Conservative aerospace bag | 10 MJ | 6.4 m/s |
| Moderate aerospace bag | 100 MJ | 20.4 m/s |
| Aspirational large bag | 1 GJ | 64.4 m/s |

**HE-graze relative velocity exceeds the aspirational soft-capture limit by 102×.** Even granting an order-of-magnitude improvement in bag energy absorption (10 GJ), the relative velocity is still 32× too high.

**Apoapsis sweep — can a less-eccentric orbit reduce relative velocity?**

| Apoapsis (km) | Relative velocity | Impact KE (TJ) | Period (days) | Time in upper B-ring per pass (min) |
|---:|---:|---:|---:|---:|
| 200,000 | 2.76 km/s | 1.84 | 0.70 | 171 |
| 500,000 | 5.43 km/s | 7.10 | 1.96 | 116 |
| 1,000,000 (reference) | 6.56 km/s | 10.38 | 4.85 | 104 |
| 2,000,000 | 7.19 km/s | 12.47 | 12.75 | 98 |
| 5,000,000 | 7.59 km/s | 13.90 | 48.15 | 95 |

Even at the lowest tested apoapsis (200,000 km), relative velocity is 2.76 km/s — still 43× above the aspirational soft-capture limit of 64 m/s. **There is no high-elliptical orbit with periapsis inside the B-ring at which soft-capture becomes feasible without circularising first.**

**Pre-registration grading:**

| Sub-claim | Predicted | Observed | Verdict |
|---|---|---|---|
| H-hgf-a (relative velocity at HE-graze periapsis ∈ [7, 8] km/s) | [7, 8] | 6.56 km/s | wrong-but-informative |
| H-hgf-b (kinetic energy ∈ [10, 15] TJ) | [10, 15] | 10.38 TJ | held |
| H-hgf-c (max v_rel for moderate bag < 100 m/s) | < 100 m/s | 20.4 m/s | held |
| H-hgf-d (circularisation delta-velocity ∈ [6, 8] km/s) | [6, 8] | 6.56 km/s | held |
| H-hgf-e (periapsis-pass duration ∈ [90, 150] min) | [90, 150] | 104 min | held |
| H-hgf-f (HE-graze falsified as soft-capture mode) | falsified | v_rel exceeds aspirational by 102× | **held — strong falsification** |

Five of six sub-hypotheses held; one wrong-but-informative (relative velocity slightly below the predicted range). Best calibration in the session.

## Reading

**The headline:** Case HE-graze from R-multi-chunk-departure-orbit is physically falsified as a soft-capture architecture. The relative velocity between a high-elliptical Saturn-orbit spacecraft and B-ring particles at periapsis (6.56 km/s for the reference orbit, never below 2.76 km/s for any apoapsis tested) exceeds the kinetic-energy-absorption capacity of any plausible deployable bag by 1-2 orders of magnitude. **The "ring-grazing capture" mode does not exist as an operational option for ICEBERG.**

**The only physically-realisable multi-chunk capture mode is to circularise at B-ring radius — i.e., Case BR-direct.** Circularising from the HE-graze orbit to B-ring circular costs 6.56 km/s of delta-velocity, identical to the relative velocity. Once circularised, the spacecraft is in B-ring orbit (BR-direct configuration); the HE-graze orbit no longer exists. Any "go back to high-elliptical between captures" strategy would burn 6.56 km/s × 2 = 13.12 km/s per inter-chunk transit — astronomically wasteful.

**This propagates back through the campaign:**

- R-multi-chunk-per-mission's headline ("venture-class reachable at N=5 with Starship launch") was specifically a Case HE-graze finding. **Retracted.** The HE-graze architecture is not operationally realisable.
- R-multi-chunk-departure-orbit's bracketed envelope collapses to the BR-direct case only. The HE-graze numbers in that round's tables are best-case theoretical and not operationally accessible.
- The binding multi-chunk architecture is Case BR-direct: capture in B-ring orbit, depart inbound at 40.2 km/s. Under this architecture, venture-class requires N=23 chunks (operationally implausible) and corporate-growth requires N=13 (still implausible at near-cap mass).

**The structural conclusion:** **ICEBERG is structurally a regulated-utility-class investment.** Venture-class returns are unreachable under any architecture the campaign has explored. The combined-leverage envelope:

| Best-case architecture | Hurdle class achievable | Required contingencies |
|---|---|---|
| Single-chunk + heat-shield + Starship + 2× reuse | regulated-utility (12-15%) | R-chunk-as-heat-shield-revisit closure |
| Multi-chunk BR-direct N=10 × 482 t + Starship | regulated-utility (15%) | bag scaling supports N=10; B-ring chunk availability at near-cap mass; per-capture reliability ≥ 0.95 |
| Multi-chunk BR-direct N=13 + Starship | corporate-growth (18%) | as above, but with N=13 (lower probability of full success) |
| Any architecture | venture-class (15%+) | **structurally unreachable** |

**Why no architecture reaches venture-class:** the rocket equation. At water-electric specific impulse (2000 s, exhaust velocity 19.62 km/s) and B-ring-departure integrated delta-velocity 40.2 km/s, asymptotic delivered fraction is 12.9 percent. Per-mission revenue at $10,000 per kilogram and 12.9 percent of N × 482 tonnes gives a fixed cashflow per mission; to reach 15 percent internal-rate-of-return, the cashflow must accumulate fast enough against the time-discounted 14.5-year round-trip. The math doesn't close at any N below ~20 with the current cost-and-revenue inputs.

**Honest pitch posture (final, after this round):**

> ICEBERG is a regulated-utility-class infrastructure investment with a structural moat. Marginal internal-rate-of-return under the demonstrated architecture (R-chunk-as-heat-shield-revisit closure plus Starship-class launch) is in the 12 to 18 percent range — sovereign-bond-plus to corporate-growth class. The program does *not* reach traditional-venture-capital-fund returns (≥20 percent) under any architecture explored to date. The capital-partner profile is sovereign + strategic-corporate + infrastructure-fund, not venture.

This is the correct framing for the anchor round and the Series-B-or-later pitch. The Suez-Canal-class moat metaphor remains apt for the regulated-utility framing; the venture-fund-returns claim was unsupportable across the campaign's analysis.

## Revisit

The methodology this session has produced seven rounds, with falsification grading evolving:

- R-conops-phase12-reuse: 2/7 held
- R-launch-cost-sensitivity: 2/7 held
- R-multi-chunk-per-mission: 2/8 held
- R-multi-chunk-departure-orbit: 5/8 held
- R-HE-graze-feasibility: 5/6 held

Hypothesis calibration improved monotonically across the session as each round's lesson refined the next round's anchor-discipline. The seventh-and-final round had its best calibration. **This is the protocol's value-add: not absence of errors, but compounding correction.**

The single load-bearing methodology lesson now formalised across seven rounds:

> **Compute the product of central estimates under the most pessimistic credible anchor first.** Range-around that, not around face-value or optimistic anchors. When an inherited number is ambiguous, run both endpoints rather than picking one.

This belongs in `water-prop/PROTOCOL.md` as a lesson number tied to this session's rounds.

## Cross-learning

**Three direct implications:**

1. **R-multi-chunk-per-mission's headline must be amended in shared docs.** The "venture-class reachable at N=5" finding is retracted; the round's published cross-learning carried HE-graze as the implicit architecture. Orchestrator (Saturn) action: ARCHITECTURE-DECISION-MATRIX should reflect that multi-chunk under BR-direct caps at regulated-utility-class, not venture-class.

2. **The ICEBERG-pitch rewrite is now load-bearing on the upcoming anchor round.** Current pitch carries venture-class language; current campaign evidence does not support it. Pitch posture should be retitled "regulated-utility-class infrastructure investment with structural moat." Sovereign + strategic-corporate + infrastructure capital, not venture.

3. **R-chunk-as-heat-shield-revisit is now confirmed as the *only* remaining high-leverage open round** (Iapetus running it). If it closes, single-chunk delivered jumps from ~150 t to ~482 t and the program reaches regulated-utility-class with margin. If it fails, the campaign's best architecture is multi-chunk-BR-direct at N=10, also regulated-utility but more operationally complex. Either way, regulated-utility is the realistic ceiling.

**Five rounds that no longer need to run** (downstream queue pruning):

- R-multi-chunk-per-mission follow-ons (bag-multichunk-mass, B-ring chunk-size, capture-reliability): all were predicated on HE-graze being viable. Under BR-direct, multi-chunk operations are constrained at N=10 by other factors (mission timeline, reliability compounding) that don't require physical-model refinement to bound. Queue de-prioritises these to "interesting if pursued but not load-bearing."

**One new question that this round opens:** what specifically would close R-chunk-as-heat-shield-revisit (delivery-uplift mechanism)? Aerocapture at Earth using the captured ice as ablator would relax phase 10 delta-velocity from 24.4 km/s (chunk-fed electric inbound including capture) to roughly 1 km/s (trim only after atmospheric deceleration). This propagates back into the chunk-fed Tsiolkovsky and could raise delivered fraction from 27 percent to ~75 percent — taking single-chunk 482 t delivered from ~150 t to ~360 t. That's not corporate-growth (still ~9% IRR per R-delivery-irr-curve) but it's a meaningful uplift. The orchestrator should weight Iapetus's R-chunk-as-heat-shield-revisit accordingly — it's the lever the campaign is now structurally counting on.

**Final session conclusion:**

The Titan re-spawn ran five R&D rounds (R-conops-phase12-reuse, R-launch-cost-sensitivity, R-multi-chunk-per-mission, R-multi-chunk-departure-orbit, R-HE-graze-feasibility) plus the meta-round R-conops-skeleton. The cumulative effect is to retire two previously-supported claims:

- **Reuse as a meaningful economic lever:** modest (1 pp uplift). Not load-bearing.
- **Venture-class returns:** structurally unreachable under any explored architecture. Pitch must retire this framing.

And to confirm two findings:

- **Regulated-utility class is achievable** under multiple architectures (single-chunk + heat-shield OR multi-chunk N=10 BR-direct). The program has a credible economic case at this hurdle.
- **The chunk-as-heat-shield rescue path is the sole remaining high-leverage lever.** Iapetus's round is the critical path.
