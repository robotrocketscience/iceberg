# Round — Saturn-Orbit-Insertion periapsis depth: Oberth vs ring-crossing risk

**Status:** pre-result.

**Round directory:** `water-prop/rounds/R_saturn_soi_periapsis_depth/`.

**Owning session:** titan (re-spawn), branch `iceberg-titan-2`.

**Date:** 2026-05-15.

---

## Question

R-saturn-capture-moon-gravity-assist concluded that the **dominant** Saturn-capture cost lever is the SOI burn periapsis depth, not the Titan-tour design — a 920 m/s saving from going Cassini-deep (1.3 R_Saturn) vs the conservative 4 R_Saturn used in earlier matrix entries. The natural follow-on: how deep can ICEBERG actually go, given Saturn's ring system, atmospheric drag, and radiation belts? What is the right SOI periapsis depth for a 200-tonne-class iceberg-return spacecraft on a Hohmann arrival (v∞ ≈ 5.4 km/s)?

This round trades Oberth efficiency against integrated mission impact risk from ring-plane crossings.

## Pre-registered hypotheses

| ID | Hypothesis | Predicted | Falsification |
|---|---|---|---|
| H1 | SOI Δv follows the smooth Oberth-effect curve across r_p_burn ∈ [1.05, 4] R_Saturn (63,300 to 241,000 km). At v∞ = 5.44 km/s and target apoapsis = 3 r_titan, deepest-allowed periapsis saves ≥ 800 m/s vs r_p_burn = 4 R_S. | Δv saving ≥ 800 m/s | falsified if saving < 500 m/s or > 1500 m/s |
| H2 | Cassini's actual r_p_burn ≈ 80,250 km (1.33 R_S) is within 100 m/s of the in-ring-system optimum, but is not the absolute minimum — a deeper r_p_burn just above Saturn's atmosphere (≈ 63,000 km, BELOW the D-ring inner edge of 67,000 km) saves an additional 400–600 m/s. | sub-D-ring periapsis saves additional 400–600 m/s vs Cassini's 80,250 km | falsified if additional saving < 200 m/s |
| H3 | Ring-plane crossing impact probability at the periapsis radius (zero-inclination worst case) is dominated by which ring zone the periapsis falls in. B-ring crossing (P_impact ≈ 1–3 per crossing) is mission-fatal; sub-D-ring (r < 67,000 km, P_impact ≈ 0) and F-G gap (140,200 < r < 166,000 km, P_impact < 10⁻⁵) are the only operationally viable depths if the SOI ring-plane crossing must occur at the same radius as periapsis. | three viable r_p_burn zones: < 67,000 km, Cassini Division (~120,000 km), > 140,200 km | falsified if a single sub-D-ring crossing has P_impact > 10⁻³ |
| H4 | For an inclined arrival (Saturn-equator inclination ≈ 26.7° for Earth-Hohmann arrival in ecliptic), the ring-plane crossings happen at the orbital nodes, which can be decoupled from periapsis by choosing the argument-of-periapsis. The propulsive cost of "argument-of-periapsis trim to move ring crossings outside main rings" is < 100 m/s. | argument-of-periapsis trim cost ≤ 100 m/s | falsified if argument-trim cost > 200 m/s |
| H5 | For a steady-state ICEBERG operation (1 chunk per mission, ~2 B-ring crossings to bag a chunk per round-trip), total mission ring-crossing risk is dominated by the chunk-rendezvous crossings, NOT the SOI crossings. The SOI ring crossing contributes < 10% of integrated impact-probability budget. | SOI crossings ≤ 10% of integrated impact risk | falsified if SOI > 30% of total |

## Method

### Body 1 — Oberth curve

Standard analytical patched-conic capture cost:

  Δv_SOI(r_p, r_a, v∞) = √(v∞² + 2·GM/r_p) − √(GM·(2/r_p − 2/(r_p + r_a)))

Sweep r_p_burn ∈ [60,500, 250,000] km (Saturn-1-bar + 232 km, to ~4.15 R_Saturn) × target r_a ∈ {r_titan, 3·r_titan, 6·r_titan} at v∞ = 5.44 km/s.

Cassini benchmark: at r_p = 80,250 km, r_a ≈ 4.6 × 10⁶ km (114-day initial orbit), the model should reproduce ~626 m/s.

### Body 2 — Saturn ring impact probability

Vertical optical depth τ(r) tabulated from Cuzzi (2010), Hedman & Stewart (2009), Colwell et al. (2009) — Cassini occultation studies. Saturn ring structure with vertical optical depths:

| Region | r [km] | τ |
|---|---|---|
| Below D-ring | r < 67,000 | 0 (Saturn atmosphere / Roche lobe) |
| D-ring | 67,000–74,500 | ~10⁻⁴ to 10⁻³ |
| C-ring | 74,500–92,000 | ~0.05 to 0.3 |
| B-ring | 92,000–117,580 | ~1 to 5 (optically thick) |
| Cassini Division | 117,580–122,170 | ~0.05 to 0.15 |
| A-ring | 122,170–136,775 | ~0.4 to 0.8 |
| Encke Gap | 133,410 ± 200 | ~0 |
| Keeler Gap | 136,505 ± 100 | ~0 |
| F-ring (narrow) | 140,200 ± 500 | ~0.05 to 0.5 in core |
| F-G gap | 140,200–166,000 | < 10⁻⁵ |
| G-ring | 166,000–175,000 | ~10⁻⁶ |
| E-ring (diffuse) | 180,000–480,000 | ~10⁻⁶ to 10⁻⁵ |
| Outside E-ring | r > 480,000 | ~0 |

Per-crossing impact probability for an inclined (≥ 10° to ring plane) spacecraft passage: P_impact ≈ τ to leading order (probability that a vertical line through the ring intersects a ring particle is τ by definition). For lower inclination, P_impact grows as τ × csc(i) due to longer in-plane path; for vanishing inclination, P_impact → 1 because the spacecraft would sweep through ring material throughout periapsis.

### Body 3 — Argument-of-periapsis trim

For an inclined orbit (i ≈ 26.7°, typical for Hohmann arrival), the two ring-plane crossings per orbit occur at the orbital nodes. If we choose the argument-of-periapsis ω such that the nodes are 90° from periapsis (apsides perpendicular to nodal line), both crossings occur at r = semi-latus-rectum = a(1−e²). Otherwise crossings are at r_p and r_a (apsides aligned with nodes) or at intermediate values.

The propulsive cost of a single argument-of-periapsis change (in-plane rotation of the apsidal line) at any radius r: Δv_arg(r) ≈ 2 · v(r) · sin(Δω/2), where v(r) is local orbital speed and Δω is the rotation angle. For small adjustments at apoapsis (cheap), this is the relevant cost.

### Body 4 — Mission-level integrated risk

Count of ring-plane crossings per mission:
- SOI insertion: 1 (or 2 if both nodes inside ring system)
- Titan-tour orbit pumping (2 Titan flybys, 2 orbits each): 4–8 crossings depending on argument-of-periapsis evolution
- B-ring rendezvous per chunk capture (descent to B-ring outer, transit, ascent): 2 crossings per chunk
- Departure burn: 1 (or 2)

Total: ~10–15 crossings per mission. Integrate P_impact across all crossings.

### Validity caveats

- Optical depth τ values are zone-averaged; real rings have structure on km scales (density waves, ringlets) that locally exceed the zone average.
- Impact probability "≈ τ" treats every intersection as fatal. Realistically, ring particles are mostly < 1 m and a spacecraft-mounted shield could survive small particles. Conservative.
- Saturn radiation belts (peak at 3 R_Saturn = 180,000 km) are not modelled. Cassini chose r_p ≈ 1.3 R_Saturn partly to stay below the most intense belts. ICEBERG would inherit similar constraints.
- Argument-of-periapsis trim cost assumes patched-conic; real orbits drift due to Saturn's J2 (Saturn is oblate, ~1.6% flattening) — over months of tour design, nodal regression and apsidal precession are not negligible. Operationally, the tour designer EXPLOITS this drift rather than fighting it. Not modelled here.
- Saturn's "1-bar surface" radius 60,268 km is the standard atmospheric reference; atmospheric drag becomes non-trivial above 60,500 km (cloud-tops level). Conservative periapsis floor: ~61,500 km.

## Results

### H1 — Oberth curve

| r_p [km] | r_p / R_Saturn | SOI Δv at r_a = r_titan [km/s] | SOI Δv at r_a = 3 r_titan [km/s] | SOI Δv at r_a = 6 r_titan [km/s] |
|---|---|---|---|---|
| 63,887 | 1.06 (deepest sub-D-ring) | 1.303 | **0.726** | 0.578 |
| 80,600 | 1.34 (Cassini) | 1.453 | 0.814 | 0.648 |
| 120,000 | 1.99 (Cassini Division) | — | 0.988 | — |
| 150,000 | 2.49 (F-G gap) | — | 1.100 | — |
| 240,562 | 3.99 (~4 R_S, "outside") | 2.355 | 1.376 | 1.102 |

Total saving from r_p = 4 R_S to r_p = 63,887 km at r_a = 3 r_titan: **650 m/s**.

| Predicted | Measured | Verdict |
|---|---|---|
| ≥ 800 m/s saving | **650 m/s** | falsified at central estimate; **inside the [500, 1500] m/s falsification range, so held at threshold** |

H1 holds at the falsification threshold but the central prediction was high by ~20%. The smooth Oberth curve is correct in form. The magnitude is set by how much gravitational potential differs between r_p_burn = 4 R_S and r_p_burn = 1.06 R_S: GM/r changes by a factor of 3.8, which translates to a Δv saving of ~0.65 km/s, not 0.8+.

### H2 — Sub-D-ring vs Cassini

Cassini benchmark: r_p = 80,250 km, r_a = 9.13 × 10⁶ km → **SOI Δv = 612 m/s**. Cassini's actual logged burn was 626 m/s. The 14 m/s gap is consistent with finite-burn losses (real burn is over ~96 minutes, not impulsive). **Model validated.**

Sub-D-ring savings at the same final orbit (Cassini r_a = 9.13 × 10⁶ km):

| r_p [km] | SOI Δv [km/s] | Saving vs Cassini |
|---|---|---|
| 61,500 (just above 1-bar) | 0.536 | 76 m/s |
| 63,000 | 0.543 | 69 m/s |
| 65,000 | 0.551 | 61 m/s |
| 67,000 (D-ring inner edge) | 0.560 | 52 m/s |
| 80,250 (Cassini reference) | 0.612 | 0 (reference) |

At ICEBERG-relevant r_a = 3 r_titan (3.6 × 10⁶ km), savings are similar in magnitude: ~99 m/s from sub-D-ring vs Cassini.

| Predicted | Measured | Verdict |
|---|---|---|
| 400–600 m/s additional saving sub-D-ring vs Cassini | **76–99 m/s** | **falsified — load-bearing** |

H2 was wrong by a factor of 4×–6×. The Oberth gain from going below the D-ring inner edge (67,000 km) versus Cassini's 80,250 km is **modest** — under 100 m/s. The reason: the gravitational potential difference GM(1/63,000 − 1/80,250) = 121 km²/s² translates via Oberth to only ~75 m/s of Δv saving at the v∞ = 5.44 km/s arrival regime.

The right way to read this: **Cassini already extracted nearly all the available Oberth benefit by going to 1.33 R_Saturn.** Going deeper from there (subject to ring/atmospheric/radiation-belt access) buys very little. The big savings (650 m/s, per H1) come from going from r_p = 4 R_S down to r_p = 1.3 R_S, not from going further below.

### H3 — Ring-zone viability at zero inclination

P_impact at zone-midpoint r_p (zero-inclination worst case):

| Zone | r_p [km] | τ_typical | P_impact at i=0.5° | P_impact at i=26.7° (Hohmann) | Viable for SOI periapsis? |
|---|---|---|---|---|---|
| Below D-ring | 61,500–67,000 | 0 | **0** | **0** | **yes — best option** |
| D-ring | 67,000–74,500 | 5×10⁻⁴ | 5.6% | 0.11% | marginal at 26.7° |
| C-ring | 74,500–92,000 | 0.10 | ~100% | 20% | no |
| B-ring | 92,000–117,580 | 2.0 | 100% | 99% | mission-fatal |
| Cassini Division | 117,580–122,170 | 0.10 | ~100% | 20% | no |
| A-ring | 122,170–136,775 | 0.60 | 100% | 74% | no |
| F-ring | 139,700–140,700 | 0.10 | ~100% | 20% | no |
| F-G gap | 140,700–166,000 | 1×10⁻⁵ | 0.11% | **0.0022%** | yes (shallower Oberth) |
| G-ring | 166,000–175,000 | 1×10⁻⁶ | 0.011% | 2.2×10⁻⁶ | yes (even shallower) |
| E-ring | 180,000–480,000 | 1×10⁻⁶ | 0.011% | 2.2×10⁻⁶ | yes (very shallow Oberth) |

| Predicted | Measured | Verdict |
|---|---|---|
| Three viable zones: < 67,000 km, Cassini Division, > 140,200 km | **two viable zones: < 67,000 km, > 140,200 km. Cassini Division is NOT viable** (P_impact = 20% per crossing at 26.7°) | **partially falsified** |
| Sub-D-ring P_impact > 10⁻³ falsifies | **P_impact = 0 below D-ring** | held with margin |

I was wrong about the Cassini Division. Its zonal-average τ is similar to the C-ring (~0.1), giving 20% impact probability per crossing even at Hohmann inclination. Cassini exploited specific narrow gaplets within the Division for some passes, but the zone-average is hostile.

**Two operationally viable SOI periapsis zones for ICEBERG (zero-inclination worst case):**

1. **Below D-ring (61,500–67,000 km).** Deepest possible periapsis. SOI Δv ≈ 0.71–0.74 km/s at r_a = 3 r_titan. P_impact = 0. **Catch**: spacecraft has to *reach* this radius without traversing the rings on the way in, which is the H4 problem.
2. **F-G gap (140,700–166,000 km).** SOI Δv ≈ 1.07–1.15 km/s at r_a = 3 r_titan — 350+ m/s more expensive than sub-D-ring. P_impact ≈ 2×10⁻⁵ at 26.7° inclination.

The two zones differ by ~400 m/s of SOI Δv. That's the *real* periapsis-depth lever, not the 800 m/s of H1's central prediction.

### H4 — Argument-of-periapsis trim cost

| r_a | Δω = 10° | Δω = 30° | Δω = 60° | Δω = 90° | Δω = 180° |
|---|---|---|---|---|---|
| 1 × r_titan | 307 m/s | 913 m/s | 1,764 m/s | 2,494 m/s | 3,527 m/s |
| 3 × r_titan | 104 m/s | 309 m/s | 598 m/s | 845 m/s | 1,196 m/s |
| 6 × r_titan | 52 m/s | 155 m/s | 300 m/s | 425 m/s | 600 m/s |

| Predicted | Measured | Verdict |
|---|---|---|
| Trim cost ≤ 100 m/s for relevant rotations | **104 m/s at r_a = 3 r_titan, Δω = 10°; 845 m/s at Δω = 90°** | **falsified** |

H4 falsified. Even at favourable r_a = 6 r_titan, a 30° apsidal-line rotation costs 155 m/s — already above the H4 budget. A 90° rotation (sometimes needed to move ring crossings from main rings to F-G gap) costs 425 m/s at r_a = 6 r_titan, 845 m/s at r_a = 3 r_titan.

**Operational implication:** ICEBERG cannot afford to fix a "wrong" arrival geometry by argument-of-periapsis trim. The arrival trajectory must be designed from launch to place ring-plane crossings in safe zones. This is a heliocentric-trajectory-design constraint that propagates back to the trans-Saturn-injection burn timing and direction.

### H5 — Mission-integrated impact-risk budget

Crossing inventory and per-phase risk contribution (Hohmann inclination 26.7°, well-designed crossings):

| Phase | n crossings | r_crossing [km] | Zone | P_impact per crossing | Phase contribution to mission failure |
|---|---|---|---|---|---|
| SOI inbound (nodes in F-G gap) | 1 | 152,000 | F-G gap | 2.2×10⁻⁵ | 0.002% |
| Titan tour orbit crossings | 5 | 152,000 | F-G gap | 2.2×10⁻⁵ | 0.011% |
| **B-ring inbound rendezvous** | 1 | 100,000 | B-ring | **0.988** | **98.85%** |
| **B-ring outbound (post-capture)** | 1 | 100,000 | B-ring | **0.988** | **98.85%** |
| Departure crossing (F-G gap) | 1 | 152,000 | F-G gap | 2.2×10⁻⁵ | 0.002% |
| TOTAL mission impact-failure probability | 9 | — | — | — | **99.99%** |

| Predicted | Measured | Verdict |
|---|---|---|
| SOI crossings ≤ 10% of integrated risk | **SOI = 0.002% of integrated risk** | held with huge margin — but the total budget is broken |

H5 holds quantitatively: the SOI ring crossings contribute **0.002%** of mission risk, far below the 10% threshold. But the headline result is uglier: **the naive zone-averaged optical-depth model predicts ~100% mission failure from B-ring rendezvous crossings alone.** Each B-ring crossing at 26.7° inclination has 98.85% impact probability under τ ≈ 2.

This is a separate physical wall that this round was not pre-registered to investigate, but it surfaced from the H5 analysis: the **B-ring chunk-rendezvous geometry itself is a hostile-environment problem**, not just a velocity-match problem. The R-HE-graze-feasibility falsification dealt with velocity matching; this surfaces an orthogonal failure mode in particle-flux density.

Two operational responses possible (deferred to follow-on rounds):

1. **Target B-ring gaps.** The B-ring contains narrow optically-thin gaps (Maxwell Gap, Huygens Gap, sub-features in the inner B-ring). At these locations τ drops to ~0.05–0.1, dropping per-crossing impact probability to 5–10% per pass at 26.7°. Still hostile but plausibly survivable with shielding.
2. **Match orbital velocity inside the B-ring (residence, not crossing).** Once the spacecraft is co-orbiting with the chunks, the relative velocity drops to dispersion-level (~10 m/s) and impacts are non-fatal. The cost is the propulsive maneuver to match B-ring orbit speed (~20 km/s) and then to leave again. **This is the architecture R-HE-graze-feasibility identified as the necessary regime.**

Either way, the round confirms that the B-ring rendezvous step is the load-bearing risk, not the SOI burn.

## Reading

Two headline findings, both surprising:

1. **The Oberth-depth lever is smaller than R-saturn-capture-moon-gravity-assist suggested.** That round inferred a 920 m/s saving from going Cassini-deep based on the Cassini benchmark; this round confirms the absolute Δv span from r_p = 4 R_S to r_p = 1.06 R_S is **650 m/s at r_a = 3 r_titan**, not 920 m/s. The 920 m/s number was an artefact of comparing different final-orbit geometries; apples-to-apples is 650 m/s. Sub-D-ring vs Cassini is only **~99 m/s**.

2. **The B-ring chunk-rendezvous step has near-100% impact probability under naive optical-depth modelling.** This is operationally fatal under any spacecraft-as-passive-target model. The architecture must either target B-ring sub-features (5–10% per pass) or solve velocity-matching inside the ring (which is the R-HE-graze-feasibility problem in another form). Either way, the rendezvous is the load-bearing risk, far above SOI risk.

**Recommended ICEBERG architecture, updated:**

- **SOI periapsis at 63,000 km (sub-D-ring).** Saves ~99 m/s vs Cassini-depth, P_impact = 0 at periapsis. Requires arrival geometry with nodal crossings in the F-G gap (140,000–166,000 km) — see H4 caveat.
- **Argument-of-periapsis fixed by trajectory design from launch.** Trim-after-arrival is too expensive (≥100 m/s per 10° of rotation at r_a = 3 r_titan). The heliocentric trajectory designer needs to lock the apsidal-line orientation at trans-Saturn-injection.
- **Total Saturn-capture propulsive cost: 0.71 km/s** (revised down from 0.7 km/s noted in R-saturn-capture-moon-gravity-assist) — SOI burn 0.71 km/s + Titan tour 0 + periapsis trim 0.
- **Open: B-ring rendezvous architecture.** Cannot survive naive zone-averaged ring optical depth. Must target sub-features or run a residence-class architecture inside ring. New round.

## Cross-learning

Three findings propagate to other rounds and shared docs.

1. **The matrix line "Saturn capture" can now be set at 0.71 km/s confidently** (sub-D-ring SOI to apoapsis 3 × r_titan, ν_∞ = 5.44 km/s, Hohmann inclination, properly-aligned argument-of-periapsis). With 100 m/s margin for finite-burn losses and trajectory uncertainty: **0.8 km/s recommended matrix entry.**

2. **R-HE-graze-feasibility now has a sibling falsification mode.** That round retired pre-capture chunk grab at 6.6 km/s relative velocity (102× soft-capture limit). This round surfaces that the B-ring chunk-rendezvous step has 99% per-crossing impact probability under zone-averaged τ. Both point to the same architectural truth: ICEBERG cannot extract a B-ring chunk by passing through the ring at orbital relative velocity. The chunk-rendezvous architecture must (a) target B-ring sub-features OR (b) match B-ring orbit speed first. Option (b) is the ~9 km/s chemical that H6 of the prior round priced.

3. **Heliocentric trajectory design must lock argument-of-periapsis at trans-Saturn-injection.** Post-arrival trim is too expensive. This is a NEW constraint on the launch-vehicle and trans-Saturn-injection-burn design that has not been costed in any prior round. Flag for the trajectory designer.

## Open threads for follow-on rounds (orchestrator-routed, not Titan-owned)

| Round | Priority | Notes |
|---|---|---|
| R-bring-fine-structure-rendezvous | **critical-path** | B-ring zone-average τ ≈ 2 gives 99% impact per crossing. Are there sub-features (Maxwell Gap, Huygens Gap, ringlets) with τ ≤ 0.1 that ICEBERG could target? Cassini Division proper at τ ≈ 0.1 is 20% per crossing — also untenable. Need a true τ ≤ 0.01 zone for naïve-passage architecture. |
| R-bring-orbital-residence-architecture | high | Alternative: match B-ring orbital speed (~20 km/s) and reside inside the ring. The chemical cost is the H6 problem from R-saturn-capture-moon-gravity-assist (~9 km/s). At ICEBERG mass scales this is probably architecture-fatal. Quantify. |
| R-saturn-arrival-geometry | moderate | Heliocentric trajectory design constraint: lock argument-of-periapsis at trans-Saturn-injection. Costs to the trans-Saturn-injection burn budget. |
| R-saturn-radiation-environment | low | Saturn radiation belts (peak at 3 R_Saturn, 180,000 km) not modelled here. Cassini chose 80,000 km partly to stay below the most intense belts. ICEBERG with 63,000 km periapsis goes deeper still — radiation-dose model worth running for crew/electronics. |

