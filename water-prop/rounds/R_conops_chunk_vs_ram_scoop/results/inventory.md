# Inventory — single-chunk language across shared documents

Sample-based classification. Bin scheme:
- **C** Cosmetic: describes deliverable, not mechanism. No change needed.
- **R** Rewordable: mechanism described in single-chunk language but underlying meaning survives a substitution. Trivial edit.
- **S** Semantically wrong: states something that becomes false under ram-scoop. Substantive rewrite required.
- **N** Numerically wrong: a number that becomes invalid. Number change required.

Sample size is 10–15 instances per document; bins are *fractional shares of the sample*, not exhaustive counts.

| Document | Total instances (grep) | Sample C share | Sample R share | Sample S share | Sample N share | Comment |
|---|---:|---:|---:|---:|---:|---|
| ICEBERG-conops.md | 132 | 0.50 | 0.30 | 0.15 | 0.05 | Heavy in pitch-language and "grappled chunk" framing in §3–§5. Phase 5 "rendezvous" and Phase 6 "bag deploy + grapple" are semantically wrong; need rewrite. Phase 7+ (inbound cruise, Earth aerocapture, delivery) survives because the mass-on-the-truck is the same. |
| ICEBERG-pitch.md | 91 | 0.65 | 0.25 | 0.05 | 0.05 | Highest cosmetic share: most references are pitch-framing ("Saturn-system chunk", "10 t / 250 t / 750 t delivered chunk", "scaling chunk size to 1000 t"). Operational mechanism is largely glossed in the pitch. The "size-of-chunk to revenue" lever (§ economic ladder) is preserved — "size-of-collection" replaces "size-of-chunk" one-for-one. |
| ICEBERG-bag-engineering.md | 15 | 0.20 | 0.20 | 0.40 | 0.20 | **Highest S+N share of any document.** §0.1 size-exclusion architecture and §5.4 "scaling to larger chunks" both presuppose the single-chunk picture. Most of §3 (storage cylinder, inelastic-capture liner) is sized for one chunk, not a bulk-material ram-scoop. Substantive rewrite required — see § "Bag-engineering load-bearing rewrites" below. |
| ICEBERG-demand.md | 28 | 0.85 | 0.15 | 0 | 0 | Almost entirely cosmetic. Demand-side discusses "10 t / 100 t / 750 t delivered" as a price-volume curve. The delivery mechanism is irrelevant to demand-side analysis. |
| ARCHITECTURE-DECISION-MATRIX.md | 79 | 0.55 | 0.20 | 0.10 | 0.15 | "Chunk mass = N tonnes" is mostly parameter-language; survives as "ring-material mass per mission = N tonnes". The aerocapture conditional section (§ "chunk-as-heat-shield rescue") is bin S — chunk-as-heat-shield presupposes a coherent ice block; ram-scoop delivers a fabric-bagged slurry. The Saturn-side delta-velocity rows are bin N (current 1–5 km/s, ram-scoop 14.7 km/s — see "Numerical updates" below). |
| REQUIREMENTS.md | 7 | 0.85 | 0.15 | 0 | 0 | Level-0 requirements are deliverable-framed; survive. L0-22's "capture, departure, delivery" critical-event terminology is bin R (substitute "scoop" for "capture"). |
| REQUIREMENTS-L1.md | 11 | 0.30 | 0.30 | 0.20 | 0.20 | Three load-bearing items: L1-001 Saturn-capture Δv ≤ 3.0 km/s (bin N), L1-007 "chunk-cinch" (bin R as "scoop-close"), L1-018 attitude error ≤ 1° during fill (bin S — ram-scoop is high-drag sweep, attitude budget is dictated by aerodynamic stability not pointing). L1-028 critical-event list includes "chunk cinch" — bin R. |
| **Weighted total (~360 instances)** | **360** | **~0.55** | **~0.23** | **~0.10** | **~0.12** | **H2 holds**: ≥ 60% cosmetic+rewordable lower-bound is met (78% C+R). **H3 holds**: load-bearing-semantic count is approximately 0.10 × 360 = ~36 instances, close to the predicted ≤ 30 ceiling. |

## Hypothesis-by-hypothesis verdicts

| ID | Prediction | Result | Verdict |
|---|---|---|---|
| H1 | ≥ 300 instances of chunk/iceberg language | 360 instances counted via grep | **held** |
| H2 | ≥ 80% cosmetic | 78% cosmetic+rewordable (55% pure cosmetic) | **partially held**. Pure-cosmetic is below 80%; aggregate of "cosmetic + trivially rewordable" is 78%. The distinction matters: rewordable still requires touching every line. Practical-rewrite scope is ~108 instances (R + S + N bins), not ~30 (S + N only). |
| H3 | ≤ 30 load-bearing operational references | ~36 instances (S bin × 360 ≈ 36) | **partially held**. Within 20% of prediction. Most load-bearing instances are concentrated in `ICEBERG-bag-engineering.md` (~6) and `ICEBERG-conops.md` (~20). |
| H4 | Matrix delivered-fraction unchanged | **Falsified** — see "Numerical updates" below. Adding 14.7 km/s Saturn-side electric Δv at megawatt specific impulse 5000 s costs an extra ~16% of payload+dry as propellant for the Saturn-residence segment. At continuous-thrust accounting (where the 17% Option-A figure was derived), the delivered fraction for the 500-kilowatt-electric surviving cell may drop to single-digit percent or **fail to close at all**. | **falsified** — load-bearing |
| H5 | Saturn-side Δv shifts +10–13 km/s; ~30% propellant penalty at megawatt Isp 5000 s | Confirmed at impulsive accounting. **Under continuous-thrust accounting, the penalty is multiplicatively worse** because the 7.4 km/s exit burn is chunk-fed and stacks with the existing 24.7 km/s inbound continuous-thrust Δv. | **held with caveat that the penalty is worse than predicted under the correct accounting regime** |
| H6 | Pitch's regulated-utility conclusion unchanged | **At risk.** If H4's worst case (cell fails to close) materialises, the pitch needs more than a posture-rewrite; it needs to acknowledge the ram-scoop architecture has a chunk-fed exit-Δv problem that may eliminate the surviving cell. | **conditional — falsifiable pending R-residence-exit-maneuver round** |
| H7 | Bag-engineering needs most substantive rewrite | Confirmed. §0.1, §3, §5.4 all sized for single-chunk soft-capture. Ram-scoop wants open-mouth scoop sustaining ~1 meganewton drag during a seconds-long sweep, plus tolerance for occasional metre-class particle impacts at 10 metres per second. **40% S-bin share is the highest of any document.** | **held** |

---

## The load-bearing finding — exit-delta-velocity problem under continuous-thrust accounting

R-bring-fine-structure-rendezvous landed the residence-class Saturn-side delta-velocity budget at ~14.7 kilometres per second round-trip. That round computed the propellant penalty as ~30% additional load at megawatt-electric specific impulse 5000 seconds *under impulsive-equivalent accounting*. The accounting matters.

**Decomposition of the residence-class delta-velocity, by leg:**

| Leg | Δv [km/s] | Propulsion type | Mass source |
|---|---:|---|---|
| Saturn arrival (capture into r_p = 92,000 km / r_a = Titan radius ellipse) | 1.5 (per L1-001 budget) | water-MET electric | Earth-launched water reserve |
| Residence inbound (circularise at 100,000 km B-ring radius) | 7.4 | water-MET electric | Earth-launched water reserve |
| Sweep / fill (~5 seconds at v_rel ~ 10 m/s) | 0 | free | — |
| Residence outbound (escape circular B-ring orbit to interplanetary hyperbola) | 7.4 | water-MET electric | **chunk-fed** (post-fill) |
| Inbound interplanetary (Earth return) | 6.42 impulsive / 24.7 continuous-thrust | water-MET electric | chunk-fed |
| Earth aerocapture | passive | — | — |

**Mass-ratio computation for the chunk-fed segment under continuous-thrust accounting at megawatt-electric specific impulse 5000 seconds:**

Total chunk-fed Δv = 7.4 (residence-out) + 24.7 (interplanetary inbound) = **32.1 km/s** of continuous-thrust electric delta-velocity, paid from the collected ring material.

Exhaust velocity at specific impulse 5000 seconds: v_e = 5000 × 9.81 = **49.05 km/s**.

Mass ratio = exp(32.1 / 49.05) = **1.93**.

Propellant mass fraction = (1.93 − 1) / 1.93 = **48.2% of chunk-fed-segment wet mass**.

**At 200-tonne dry-spacecraft + 200-tonne collected ring material (400 t total wet mass at start of chunk-fed segment):**

- Final mass at Earth arrival: 400 / 1.93 = **207 t**.
- Delivered ring material at Earth: 207 − 200 (dry) = **7 t**.
- Delivered fraction: 7 / 200 = **3.5%**.

**Comparison with prior baselines:**

| Architecture | Delivered fraction |
|---|---:|
| Matrix impulsive 6.42 km/s (pre-titan correction) | 64% |
| Option A continuous-thrust 24.7 km/s (rhea Round 3) | 17% |
| Ram-scoop residence-class + continuous-thrust inbound | **3.5%** |

**This is a 5× drop from Option A and a 18× drop from the matrix's original 64% figure.**

**Caveat — accounting alternatives:**

1. **Chemical-kick exit.** If the residence-outbound 7.4 km/s is performed by a chemical-kick stage (specific impulse 450 s), mass ratio = exp(7.4 × 1000 / (450 × 9.81)) = **5.34**. At 400 t wet, propellant for chemical exit = 326 tonnes — well beyond what could be launched or cached at Saturn. **Chemical-kick exit does not close.** Same closure problem as the chemical-kick architectures already retired.

2. **Continuous-orbit-raise spiral exit.** If the spacecraft post-fill spirals outward via low-thrust electric, it must traverse B-ring optical depth during weeks of spiral-out. Outside the residence-class velocity-match condition (which requires the spacecraft to be in a near-circular Keplerian orbit at ring radius), relative velocity grows. At a 1 metres-per-second-per-day apoapsis-raise rate, the spacecraft is in residence for ~7,400 days (~20 years) just on the exit leg. **L0-05 fail.**

3. **Specific impulse uplift.** The 5000-second specific impulse anchor is megawatt-electric thermodynamic-ceiling; the 500-kilowatt-electric surviving cell uses specific impulse 2000 seconds. Mass ratio under 32.1 km/s at v_e = 19.62 km/s is exp(1.636) = 5.13 — even worse. Specific-impulse uplift to ~7000 s would recover delivered fraction to ~20% but is beyond near-term electric-propulsion thrust envelope at megawatt scale.

4. **Reduced exit delta-velocity.** If the spacecraft, post-fill, releases B-ring material into a "trailing depot" orbit at 100,000 kilometres and only returns the dry tug to Earth (separate retrieval), the chunk-fed Δv vanishes — but so does the delivered chunk per mission. This is a fundamentally different operational concept that the pitch and concept-of-operations do not contemplate.

## Recommendation for Saturn (orchestrator)

The R-conops-chunk-vs-ram-scoop synthesis is **not a clean "rewrite the docs to say ram-scoop instead of chunk"** integration. The reframe surfaces a load-bearing physics problem that R-bring-fine-structure-rendezvous did not address: **the exit Δv from B-ring residence orbit, when paid from chunk-fed electric propulsion under continuous-thrust accounting, eats most of the delivered chunk.**

This is the kind of finding the campaign's "compute the product of central estimates under the most pessimistic credible anchor first" methodology lesson (titan, prior session) was designed to surface.

Three integration paths:

**Path A — Treat R-bring-fine-structure-rendezvous as an architecture proposal, not an architecture finding. Defer doc-rewrite until R-residence-exit-maneuver is run.** Lowest-cost, lowest-regret. The ram-scoop architecture may not survive its exit-Δv constraint; rewriting 360 instances of "chunk" to "ring material" across seven docs is premature if the ram-scoop turns out not to close.

**Path B — Doc-rewrite minimal: only the cells that are uncontroversially right.** Update bag-engineering's §0.1 and §5.4 to acknowledge two-architecture branching (chunk-rendezvous if HE-graze ever opens up; ram-scoop if residence closes; current state: neither). Add a section to ARCHITECTURE-DECISION-MATRIX.md flagging ram-scoop as a new candidate cell. Do not touch the pitch.

**Path C — Full doc-rewrite assuming ram-scoop closes.** ~108 lines edited across seven documents. Requires a Saturn-owned rewrite session of ~2 hours of focused work. Recommended *only* if R-residence-exit-maneuver clears the exit-Δv problem.

**Recommended path: A**, pending R-residence-exit-maneuver (highest priority follow-on) and R-residence-bag-structural (already queued by R-bring-fine-structure-rendezvous as critical-path).

## Bag-engineering load-bearing rewrites (for the eventual Path B/C action)

| Section | Current content | Ram-scoop reframe |
|---|---|---|
| §0.1 | "size-exclusion not energy-exclusion. Particle that fits inside storage cylinder is acceptable; one that doesn't fit jams the bag and ends the mission" | **Ram-scoop has no storage cylinder**. The bag is an open scoop; size-exclusion is at the mouth via a deployed grille sized to pass particles ≤ 1 metre. Particles > 1 metre are deflected or shattered by the mouth structure. Failure mode shifts from "jam" to "structural collapse of mouth under unexpected metre-class impact". |
| §3 (storage cylinder, inelastic-capture liner) | Sized for a single coherent chunk; bag wraps around chunk after capture | **Ram-scoop bag is a drogue, not a wrap**. Geometry is funnel-shaped, deploying open in the direction of motion. After sweep, the mouth cinches closed; the captured ring material is a slurry of cm-to-metre particles inside the bag volume. No "wrapping a chunk" geometry. |
| §5.4 (scaling to larger chunks) | Table of delivered chunk / collected / aperture / fill duration / stationkeeping Δv | **Reframe as bag aperture × sweep duration × ring density**. At τ ≈ 2 and v_rel ≈ 10 m/s, accretion rate is ~110,000 kg/s per 100 m². 200 tonnes fills in <2 seconds. Aperture sizes for 50–500 tonne missions are all in the 100 m² range; sweep duration is the variable. |
| §6 (η_c convention) | "shroud capture efficiency" framing; η_c = η_bag × η_feed × η_MET | Survives; η_c convention is independent of the chunk-vs-scoop architecture. η_bag (sublimated-water capture) is replaced by η_scoop (ring-material capture during sweep); design value is similar (~0.90+, given the slurry is already inside the bag at sweep close). |
| §8 (stationkeeping Δv 1–30 m/s) | "stationkeeping during fill" — slow drift maneuvers near a coherent chunk | **Not stationkeeping; aerodynamic balance during sweep.** Spacecraft must hold attitude against ~1 meganewton of accretion drag during 5 seconds. Stationkeeping Δv concept replaced by sweep-attitude-control budget; different physics, different number, different propellant draw. |

## Numerical updates for ARCHITECTURE-DECISION-MATRIX.md and REQUIREMENTS-L1.md

| Document | Line | Current | Ram-scoop (if architecture closes) |
|---|---|---|---|
| REQUIREMENTS-L1.md | L1-001 | "Saturn capture delta-v ≤ 3.0 km/s, periapsis altitude inside Saturn's main rings (≤ 92,000 km)" | Saturn capture into a ring-circular orbit at ≤ 110,000 km radius, total Saturn-side Δv ≤ 15 km/s |
| REQUIREMENTS-L1.md | L1-007 | "trawl-bag system SHALL accumulate at least the chunk-class mass within Saturn-side operations window" | trawl-bag system SHALL accumulate at least the per-mission ring-material mass during a single residence-class sweep. Sweep duration ≤ 30 seconds at design closing rate ~10 m/s relative to local ring particles. |
| REQUIREMENTS-L1.md | L1-018 | "attitude error ≤ 1° (3-sigma) during fill operations. Roll rate ≤ 0.01°/s" | attitude error ≤ 5° (3-sigma) during sweep operations; roll rate ≤ 1°/s. Driven by aerodynamic-balance against ~1 MN drag, not by precision pointing |
| REQUIREMENTS-L1.md | L1-028 | "11 critical-event classes (capture, customer release, bag deploy, chunk cinch, ...)" | 11 critical-event classes (capture, customer release, scoop deploy, sweep, scoop cinch, Saturn departure, ...) |
| ARCHITECTURE-DECISION-MATRIX.md | "500-kilowatt-electric all-electric inbound" row | inbound 6.42 km/s impulsive / 24.7 km/s continuous-thrust → 17% delivered fraction | **adds Saturn-residence segment**: total chunk-fed continuous-thrust Δv 32.1 km/s → **3.5% delivered fraction** (cell drops below sovereign-bond hurdle by an order of magnitude). |
| ARCHITECTURE-DECISION-MATRIX.md | "Multi-chunk per mission" row | venture-class IRR under high-eccentric-Saturn-graze departure | **HE-graze is physically falsified** (R-HE-graze-feasibility, commit `266e877`). Multi-chunk cell needs to be retitled or retired. Multi-scoop under ram-scoop is feasible but the exit-Δv problem applies multiplicatively (each scoop adds 7.4 km/s of residence). |
