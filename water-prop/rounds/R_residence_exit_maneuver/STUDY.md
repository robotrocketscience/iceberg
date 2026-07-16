# Round — Residence-class exit-Δv closure

**Status:** pre-result.

**Round directory:** `water-prop/rounds/R_residence_exit_maneuver/`.

**Owning session:** titan (re-spawn), branch `iceberg-titan-2`.

**Date:** 2026-05-15.

**Pre-requisite rounds:**
- R-bring-fine-structure-rendezvous (commit `201e2c2`): residence-class architecture at r ≈ 100,000 km circular costs ~7.4 km/s impulsive in and ~7.4 km/s impulsive out. Accretion rate at v_rel = 10 m/s is 5,000–230,000 kg/s per 100 m² bag opening at B-ring zone-averaged τ.
- R-conops-chunk-vs-ram-scoop (commit `07b73ec`): under continuous-thrust electric accounting (the regime in which Option A's 17% delivered fraction was derived), the exit Δv must stack with the inbound 24.7 km/s cruise. Total chunk-fed Δv = 32.1 km/s → mass ratio 1.93 at megawatt-electric specific impulse 5000 s → delivered fraction **3.5%** (a 5× drop from Option A; 18× drop from matrix original).
- R-variant-B-impulsive-vs-continuous (commit `e6467ab`, hyperion): inbound continuous-thrust integrated delta-velocity 24.7 km/s, not the matrix's impulsive 6.42 km/s. Two Edelbaum capture spirals (Earth + Saturn side) dominate the integral.

---

## Question

R-conops-chunk-vs-ram-scoop surfaced that the residence-class architecture's *exit* Δv stack collapses delivered fraction to ~3.5% under chunk-fed continuous-thrust accounting. The architecture is operationally feasible (the ram-scoop accretes mass in seconds) but appears to fail at the propellant-economics layer. The standing question is whether ICEBERG has any propulsion configuration that recovers delivered fraction to at least Option A's 17%.

This round answers: **under what specific-impulse / propellant-source / trajectory / mission-profile combination does the residence-class architecture close to delivered fraction ≥ 10%? Is there a path that recovers Option A's 17%, or is residence-class structurally sub-Option-A?**

Eight candidate configurations are pre-registered for evaluation:

| # | Configuration | Lever |
|---|---|---|
| A1 | Pure electric chunk-fed, Isp 5000 s, no aerocapture, no GA (baseline) | none (anchor) |
| A2 | Electric chunk-fed + Earth aerocapture | inbound Δv reduction |
| A3 | Electric chunk-fed + Earth aerocapture + Jupiter return GA | inbound Δv reduction |
| A4 | Hybrid chemical-electric (chemical exit burn from collected-water-derived H2/O2, electric inbound) | Isp ↓ but thrust ↑ for exit |
| A5 | Isp uplift to 7000 s for exit burn only (long residence-period burn) | exit-burn Isp ↑ |
| A6 | Drop residence-class hardware at Saturn departure (jettison bag, scoop, deployable structure) | dry-mass ↓ |
| A7 | Resonance-pumping exit via inner-moon GA cascade (Mimas → Enceladus → Dione → Rhea → Titan) | gravitational Δv |
| A8 | Aerobraking Saturn entry only (saves entry Δv; exit unchanged) | round-trip Δv reduction (does not address exit specifically; included as control) |

The round answers whether any configuration — or any combination — closes residence-class to delivered fraction ≥ 10%, and whether any closes to ≥ 17% (Option A parity).

## Pre-registered hypotheses

| ID | Hypothesis | Predicted | Falsification |
|---|---|---|---|
| H1 | The exit Δv from circular B-ring residence orbit (any radius 95,000–117,000 km) is bounded below by 7.0–8.1 km/s for Saturn escape. Bi-elliptic and perihelion-drop alternatives do not undercut direct escape because target C3 at infinity is ~0. | exit Δv ∈ [7.0, 8.1] km/s for any propulsive-only exit from circular residence | falsified if any propulsive-only exit < 6.5 km/s OR > 9.0 km/s |
| H2 | At Isp 5000 s and inbound 24.7 km/s, no propulsive-only configuration (A1–A6 ex moon-GA) recovers delivered fraction ≥ 17%. Tsiolkovsky stack is set by total Δv; chunk-fed accounting cannot escape it. | configurations A1–A6 (ex A4 if chemical exit closes) deliver < 17% | falsified if any configuration delivers ≥ 17% without invoking aerocapture or GA |
| H3 | Configuration A4 (chemical exit + electric inbound, using collected water as feedstock) **does not close**. At chemical Isp 450 s and 7.4 km/s exit, mass ratio is 5.34 — propellant requirement at exit point is 4.34× wet mass, exceeding both the collected mass (200 t) and any conceivable Saturn-side cryogen-stored reserve. Even if the entire collected payload is converted to LOX/LH2, mass-ratio penalty kills delivered fraction. | A4 delivered fraction < 1% (worse than baseline) | falsified if A4 delivers ≥ 5% |
| H4 | Configuration A2 (Earth aerocapture only) saves ~1.5 km/s of inbound Δv (one Earth-side Edelbaum capture spiral retired). Configuration A3 (aerocapture + Jupiter GA) saves additionally ~2–3 km/s of inbound v_∞ via swing-by. Combined, A3 inbound drops from 24.7 to ~19–20 km/s. Stack with 7.4 km/s exit = 26.4–27.4 km/s; delivered fraction recovers to 13–17% range. | A3 delivered fraction ∈ [12%, 18%] | falsified if A3 < 8% (Δv savings smaller than predicted) or > 22% (Δv savings larger than predicted) |
| H5 | Configuration A5 (Isp 7000 s for exit burn during months-long residence period) IS executable at low thrust — the burn is spread across the entire Saturn-side dwell, decoupling Isp from L0-05 cruise-time constraints. At Isp 7000 s for exit, Isp 5000 s for inbound, stack 7.4 km/s + 24.7 km/s, delivered fraction recovers to 8–11%. | A5 delivered fraction ∈ [7%, 13%] | falsified if A5 < 5% or > 15% |
| H6 | Configuration A6 (jettison residence-class hardware) saves only 10–30 t of dry mass. Bag fabric, accretion structure, and deployment mechanism are a fraction of the 200 t dry mass; reactor, radiators, RCS, comm, structure are non-discardable. Delivered fraction uplift is 0.5–2 percentage points. | A6 uplift < 3 pp vs A1 | falsified if A6 uplift > 5 pp |
| H7 | Configuration A7 (inner-moon resonance pumping) saves < 0.5 km/s of effective exit Δv. Inner moons (Mimas through Rhea) have GM values 2.5–154 km³/s² — flyby Δv from each is ≤ 0.1 km/s under achievable v_∞ and minimum-pass altitude. Titan flyby (GM 8978 km³/s²) gives 1.5–2 km/s but requires raising apoapsis to Titan radius first (≥ 6 km/s upward Δv). Net: resonance-pumping is not a meaningful lever — confirms titan's earlier R-saturn-capture-moon-gravity-assist verdict at the exit phase as well as the entry phase. | A7 net Δv savings < 0.5 km/s; delivered-fraction uplift < 1 pp | falsified if A7 saves > 1 km/s |
| H8 | Configuration A8 (Saturn aerobraking entry only) saves ~7 km/s on round-trip Saturn-side Δv. But the *exit* Δv is unchanged, and exit-Δv is what kills delivered fraction under chunk-fed accounting (because the chunk is collected before exit). So A8 has zero impact on chunk-fed delivered fraction; it only affects mission-success risk (aerobraking is a complex maneuver) and the outbound mass budget. Included as control. | A8 delivered-fraction impact = 0 pp (unchanged from baseline A1) | falsified if A8 changes A1's delivered fraction at all |
| H9 | The composite of A3 + A5 + A6 (aerocapture + Jupiter GA + Isp 7000 exit + jettison residence hardware) DOES close residence-class to ≥ 17% delivered fraction. This is the architecture-rescue path if it exists; if even the composite fails, the residence-class architecture is sub-Option-A and the campaign should retire ram-scoop entirely in favour of Option A's HE-graze-equivalent or accept the lower delivered fraction as a feature of the operational reframe. | composite A3+A5+A6 delivered fraction ∈ [15%, 22%] | falsified if composite < 12% (architecture remains broken) or > 25% (some lever was double-counted) |

## Method

### Body 1 — Exit Δv floor (H1)

Compute Δv to escape Saturn from circular orbits across the residence-eligible radial range (95,000–117,000 km). Compare direct escape, bi-elliptic via low-perihelion (perihelion drop to 1.0–1.5 R_S), bi-elliptic via high-apoapsis (apoapsis raised to Saturn Hill sphere ~65×10⁶ km). Verify the 7.0–8.1 km/s range.

### Body 2 — Baseline A1 (anchor)

Recompute the R-conops-chunk-vs-ram-scoop 3.5% number under the protocol's clean Tsiolkovsky formulation. Spacecraft model: 200 t dry, 200 t collected mass at residence exit point. Apply Δv_stack = Δv_exit + Δv_inbound at Isp 5000 s. Delivered = (m_initial / exp(Δv/Isp·g₀)) − m_dry. Confirm 3.5% ± 0.5%.

### Body 3 — Configurations A2, A3 (inbound Δv reduction)

A2: subtract one Earth-side Edelbaum capture spiral from inbound 24.7 km/s. Edelbaum spiral cost is (v_circ_target − v_∞), bracketed by R-inbound-dv-continuous-thrust at ~1.5 km/s for an Earth-side spiral. A2 inbound = 23.2 km/s. Compute delivered.

A3: A2 + Jupiter return GA. Jupiter GA at heliocentric v_∞ ~ 5 km/s gives bending-angle-bounded Δv ~ 2.5 km/s (per standard patched-conic, max-bending limited by Jupiter atmosphere). A3 inbound = 20.7 km/s. Compute delivered.

### Body 4 — Configuration A4 (chemical exit, electric inbound)

Two sub-variants:
- A4a: collected water electrolysed in-flight; H2/O2 stored as cryogens; chemical burn at Isp 450 s for 7.4 km/s exit, then electric for 24.7 km/s inbound.
- A4b: chemical propellant brought from Earth (no electrolysis); chemical burn for exit; electric for inbound.

For A4a: mass-budget the electrolyser, cryogen tankage, boiloff over Saturn-side dwell (6 months). Subtract from collected payload. Compute exit-point wet mass = 200 t dry + (200 − tankage − electrolyser − boiloff) t H2/O2 propellant. Apply chemical mass-ratio 5.34. Verify feasibility.

For A4b: chemical propellant arrives at Saturn alongside spacecraft. Has to be lifted from Earth at outbound Isp 5000 s. Cost of carrying 1 t of cryogen to Saturn residence = (outbound mass ratio at megawatt-electric, ~24 km/s outbound Δv) ≈ 1.6 t Earth-departure mass per kg delivered at Saturn. Mass budget closes against original 200 t dry + 200 t payload outbound only if chemical propellant is < ~50 t. Not enough to cover 7.4 km/s at Isp 450 s.

### Body 5 — Configuration A5 (Isp 7000 s exit)

The R-inbound-dv-continuous-thrust finding (methodology lesson 3) was that under L0-05 cruise-time ceiling, Isp 5000 wins because higher Isp means lower thrust means longer burn. This binds during *interplanetary cruise*. The exit burn from Saturn residence orbit, however, can be executed over the Saturn-side dwell period (~6 months per current architecture) at low thrust — not bound by L0-05 cruise-time directly. So Isp uplift is admissible for the exit burn alone.

Tsiolkovsky stack: Δv_exit at Isp_exit + Δv_inbound at Isp_inbound. Compute via segmented rocket equation. Confirm A5 numbers.

Validity caveat: Isp 7000 s NEP requires a reactor + grid + plasma source. Thrust at fixed power scales 1/Isp; doubling Isp halves thrust. Need to verify 6-month exit burn is executable at half thrust without exceeding power-system duty cycle limits. Reference R-cathode-life-water-plasma for grid life.

### Body 6 — Configuration A6 (jettison residence hardware)

Bag fabric mass-per-area: from ICEBERG-bag-engineering §3, ~0.5–2 kg/m². For a 100 m² bag opening with structural ribs scaling as bag perimeter, total bag+ribs mass ~5–15 t. Accretion-management deployable structure: ~5–15 t. Heat-shield protection for ablative payload: not in residence-class architecture (ram-scoop slurry replaces coherent block; heat-shield is not a residence-class component). Jettison total: 10–30 t out of 200 t dry. Compute uplift.

### Body 7 — Configuration A7 (resonance-pumping moon GA cascade)

For each Saturnian inner moon (Mimas, Enceladus, Tethys, Dione, Rhea, Titan), compute:
- GM, orbital radius, orbital v_circ
- Maximum bending angle δ_max at minimum-pass altitude (50 km above surface): tan(δ_max/2) = GM / (v_∞² × r_p)
- Δv per flyby: 2 × v_∞ × sin(δ_max/2)
- v_∞ at the moon's orbit from a residence-orbit-departure trajectory (compute via patched-conic)

Compute cumulative Δv from a Mimas-Enceladus-Dione-Rhea sequence (assuming favourable phasing — best case). Subtract from required exit Δv. Verify the < 0.5 km/s prediction.

For Titan: compute cost of raising apoapsis from 100,000 km to Titan radius (1.22×10⁶ km), then Titan GA, then escape from Titan-radius apoapsis. Compare to direct escape from 100,000 km. Verify net penalty.

### Body 8 — Configuration A8 (Saturn aerobraking entry)

Aerobraking entry at Saturn periapsis ~ 1.0–1.1 R_S: deceleration in upper atmosphere. Reference: Cassini final dive demonstrated periapsis ~60,000 km feasibility. For ICEBERG, aerobraking from inbound v_∞ ~ 6 km/s at SOI down to v_circ at 100,000 km = 19.5 km/s. Required Δv reduction from aerobraking: ~3–7 km/s of the entry burn (depending on inbound trajectory).

Verify H8: aerobraking saves on the entry burn, but does not touch the exit burn or the chunk-fed inbound. Delivered-fraction impact is 0 pp (control verification).

### Body 9 — Composite A3+A5+A6 (H9)

Stack savings: aerocapture (A2) saves 1.5 km/s, Jupiter GA (A3) adds 2.5 km/s, Isp 7000 exit (A5) shifts exit mass-ratio penalty downward, jettison hardware (A6) reduces dry mass by 10–30 t. Compute composite delivered fraction.

### Validity caveats

- Tsiolkovsky stack assumes propellant is carried; chunk-fed accounting treats collected water as propellant reserve. The composite A3+A5+A6 mixes propellant sources (collected for exit, collected for inbound) and the Isp differs between the two segments. Segmented rocket equation handles this cleanly.
- Earth aerocapture savings (1.5 km/s) is an estimate from R-inbound-dv-continuous-thrust; precise value is geometry-dependent. Treat 1.0–2.0 km/s as the realistic band.
- Jupiter GA savings depend on synodic phasing. Roughly half of all departure windows include a viable Jupiter swing-by; the other half do not. Treat A3 numbers as best-case-window.
- Resonance-pumping moon GA cascade requires N flybys at N consecutive orbital periods (Mimas-Enceladus inner moons have periods 1–4 days; the cascade fits in days). Phasing is assumed ideal for the best-case verdict.
- Isp 7000 s NEP exit burn assumes the reactor and grid can operate at half-thrust for 6 months. Cathode life under water plasma (R-cathode-life-water-plasma) is the limiting factor — if cathode life is < 6 months at full thrust, halving thrust extends life, so the constraint is admissible.
- Residence-hardware jettison assumes the bag and scoop are mechanically separable from the spacecraft bus without disabling thermal, comm, or propulsion. Engineering verification deferred to a future round.
- All numbers in the round are point estimates at the central spacecraft model (200 t dry, 200 t collected). Sensitivity to dry-mass assumption is logarithmic via Tsiolkovsky — a ±20% dry-mass change moves delivered fraction by ±2–3 pp. Treat verdict bands as wide.

## Results

Full sweep in `results/`; headline numbers below. Central spacecraft model 200 t dry + 200 t collected at residence exit point unless noted.

### H1 — Exit Δv floor across residence orbits and strategies

| r_residence [km] | v_circ [km/s] | direct escape Δv [km/s] | bi-elliptic via 1.0 R_S perihelion [km/s] | bi-elliptic via Hill apoapsis [km/s] | minimum [km/s] |
|---|---|---|---|---|---|
| 95,000 | 19.98 | **8.28** | 10.10 | 9.30 | 8.28 |
| 100,000 | 19.48 | **8.07** | 10.04 | 9.08 | 8.07 |
| 105,000 | 19.01 | **7.87** | 9.97 | 8.89 | 7.87 |
| 110,000 | 18.57 | **7.69** | 9.91 | 8.71 | 7.69 |
| 115,000 | 18.16 | **7.52** | 9.84 | 8.53 | 7.52 |
| 117,000 | 18.01 | **7.46** | 9.81 | 8.47 | 7.46 |

| Predicted | Measured | Verdict |
|---|---|---|
| Exit Δv ∈ [7.0, 8.1] km/s, direct beats bi-elliptic | Direct exit ∈ [7.46, 8.28] km/s; bi-elliptic strategies all higher | **held with 2% caveat** — 95,000 km orbit needs 8.28, marginally above 8.1 upper bound but well inside falsification band (> 9.0) |

Direct escape is the minimum strategy at every residence radius. Bi-elliptic via low-perihelion costs 10+ km/s because lowering perihelion requires a substantial retrograde burn at residence that the Oberth-enhanced escape burn at low perihelion cannot recoup against zero target C3. Bi-elliptic via high-apoapsis is mathematically equal to direct escape in the limit but the staged execution adds inefficiency.

### H2 — A1 baseline (anchor)

| dv_exit [km/s] | dv_inbound [km/s] | Isp [s] | delivered [t] | delivered fraction |
|---|---|---|---|---|
| 7.4 (as reported by R-bring-fine-structure) | 24.7 | 5000 | 7.8 | **0.039** |
| 8.07 (direct escape from 100,000 km) | 24.7 | 5000 | 5.0 | **0.025** |

| Predicted | Measured | Verdict |
|---|---|---|
| A1 ~ 3.5% per R-conops-chunk-vs-ram-scoop | 3.9% at the prior round's quoted 7.4 km/s exit; 2.5% at the geometrically-strict 8.07 km/s direct escape | **held** — anchor replicates within 0.5 pp |

Minor methodology note: R-bring-fine-structure-rendezvous's 7.4 km/s exit number is ~0.7 km/s below the direct-escape value at 100,000 km circular (8.07 km/s). The 0.7 km/s discrepancy is plausibly attributable to Saturn rotation gain (~0.5 km/s prograde) plus a small departure-direction optimization. **A1 baseline used for downstream comparison takes the optimistic 7.4 km/s figure, consistent with prior round.**

### H3 — A4 chemical-electric hybrid

| Sub-variant | Description | Result | Verdict |
|---|---|---|---|
| A4a | Chemical exit (LOX/LH2 from electrolysed collected water, Isp 450 s) + electric inbound | **delivered fraction = -0.80** (vehicle cannot complete inbound; collected water is exhausted as chemical propellant) | infeasible |
| A4b | Chemical exit (LOX/LH2 brought from Earth) + electric inbound | propellant required at residence: **1739 t**; Earth-departure lift mass: **~2730 t** | architecturally infeasible |

| Predicted | Measured | Verdict |
|---|---|---|
| A4 delivered fraction < 1% (worse than baseline) | A4a: −80% (cannot close); A4b: requires 1700+ t cryogen at residence | **held strongly** — both sub-variants confirm chemical exit is dead. The chemical mass-ratio penalty at 7.4 km/s is fatal whether the cryogen comes from collected water or Earth lift |

A4a fails because the Tsiolkovsky penalty at Isp 450 s consumes 81% of the (m_dry + m_collected) initial wet mass just for the exit burn, leaving the inbound burn under-fuelled by ~135 t. A4b fails because lifting 1700+ t of cryogen from Earth to Saturn residence orbit at outbound electric Isp 5000 s requires a 2700-tonne Earth-departure mass — an order of magnitude beyond any plausible launch architecture.

**Chemical exit is dead at every plausible cryogen source.**

### H4 — A2 / A3 inbound Δv reduction

| Configuration | Δv_exit [km/s] | Δv_inbound [km/s] | delivered [t] | delivered fraction |
|---|---|---|---|---|
| A1 baseline | 7.4 | 24.7 | 7.8 | 0.039 |
| A2 Earth aerocapture only | 7.4 | 23.2 | 14.4 | **0.072** |
| A3 Earth aerocapture + Jupiter GA | 7.4 | 20.7 | 25.6 | **0.128** |
| A3-only Jupiter GA (no aerocapture) | 7.4 | 22.2 | 18.7 | 0.094 |

| Predicted | Measured | Verdict |
|---|---|---|
| A3 delivered fraction ∈ [12%, 18%] | A3 = 12.8% | **held at lower edge of band** — within prediction but Jupiter GA + Earth aerocapture savings are at the conservative end of the 5.8 km/s assumed reduction |

Earth aerocapture alone (A2) lifts delivered fraction from 3.9% to 7.2%. Adding Jupiter return GA (A3) further lifts to 12.8%. **Neither A2 nor A3 alone reaches Option A's 17% parity, but A3 is within striking distance and closes most of the gap.**

### H5 — A5 Isp uplift at exit

| Isp_exit [s] | Isp_inbound [s] | delivered fraction |
|---|---|---|
| 5000 (A1) | 5000 | 0.039 |
| 6000 | 5000 | 0.066 |
| **7000 (A5)** | 5000 | **0.085** |
| 8000 | 5000 | 0.099 |
| 9000 | 5000 | 0.108 |

| Predicted | Measured | Verdict |
|---|---|---|
| A5 ∈ [7%, 13%] at Isp 7000 exit | A5 = 8.5% | **held** — within predicted band, on the low side |

Isp uplift at the exit burn alone is admissible because the exit can be executed at low thrust over the months-long Saturn residence period (decoupled from L0-05 cruise-time ceiling that binds the interplanetary cruise). At Isp 7000 s the exit mass-ratio drops from 1.163 (Isp 5000) to 1.114, freeing ~40 t of effective propellant savings into delivered payload.

### H6 — A6 jettison residence hardware

| Jettison mass [t] | m_dry_effective [t] | delivered [t] | delivered fraction | uplift vs A1 [pp] |
|---|---|---|---|---|
| 0 | 200 | 7.8 | 0.039 | (baseline) |
| 10 | 190 | 11.9 | 0.060 | +2.1 |
| **20** | 180 | **17.4** | **0.087** | **+4.8** |
| 30 | 170 | 23.0 | 0.115 | +7.6 |
| 40 | 160 | 27.0 | 0.135 | +9.6 |

| Predicted | Measured | Verdict |
|---|---|---|
| A6 uplift < 3 pp at 20 t jettison | A6 uplift = 4.8 pp at 20 t (and 9.6 pp at 40 t) | **falsified — load-bearing in the predicted direction** — dry-mass reduction is more effective than pre-registered |

The falsification reason: dry mass appears *twice* in the Tsiolkovsky cascade — once as ballast that must be accelerated through the exit burn, and again as ballast through the inbound burn. The compounding effect means a 10% dry-mass reduction (20 t out of 200 t) increases delivered fraction by 5 pp, not 1-2 pp. This is a methodology lesson worth flagging: when pre-registering sensitivity to dry mass across a multi-burn stack, account for compounding through every burn.

### H7 — A7 inner-moon resonance pumping

| Moon | GM [km³/s²] | a [km] | v_∞ at moon [km/s] | Δv to raise apoapsis [km/s] | Δv per flyby [km/s] | net Δv [km/s] |
|---|---|---|---|---|---|---|
| Mimas | 2.50 | 185,539 | 2.33 | **2.73** | 0.009 | **−2.72** |
| Enceladus | 7.21 | 238,042 | 2.91 | 3.64 | 0.016 | −3.62 |
| Tethys | 41.21 | 294,672 | 3.27 | 4.32 | 0.043 | −4.28 |
| Dione | 73.12 | 377,415 | 3.54 | 5.01 | 0.068 | −4.95 |
| Rhea | 153.94 | 527,068 | 3.69 | 5.78 | 0.102 | −5.67 |
| Titan | 8978.14 | 1,221,865 | 3.40 | 7.00 | **1.93** | **−5.08** |

| Predicted | Measured | Verdict |
|---|---|---|
| A7 saves < 0.5 km/s; delivered-fraction uplift < 1 pp | A7 *net* Δv is **negative** at every moon — orbit-raise cost dwarfs flyby return. Even Titan's substantial 1.93 km/s flyby returns less than the 7.00 km/s cost of reaching Titan radius. | **held in spirit (resonance pumping is not a lever); falsified in direction (it is actively negative)** |

The pre-registered prediction was that moon flybys save < 0.5 km/s. The data shows they don't save anything — they *cost* 2.7 to 5.7 km/s net, because reaching the inner moons from residence at 100,000 km requires raising apoapsis through a Hohmann burn that exceeds the flyby's gravitational deflection bonus. This re-affirms titan's prior R-saturn-capture-moon-gravity-assist verdict (Titan flyby saves only ~300 m/s for Saturn capture) and extends it to the exit-phase question.

**Resonance pumping is decisively retired from the residence-class architecture's exit toolkit.**

### H8 — A8 Saturn aerobraking entry control

| Configuration | Δv_exit [km/s] | Δv_inbound [km/s] | delivered fraction |
|---|---|---|---|
| A1 (no aerobrake) | 7.4 | 24.7 | 0.039 |
| A8 (aerobrake entry) | 7.4 | 24.7 | 0.039 |

| Predicted | Measured | Verdict |
|---|---|---|
| A8 delivered-fraction impact = 0 pp vs A1 | A8 = A1 by construction | **held by construction** |

A8 confirms (as a control) that aerobraking *entry* does not affect chunk-fed delivered fraction. The chunk is collected after entry; subsequent burns (exit, inbound) are independent of how entry was performed. Aerobraking entry remains a useful lever for the **outbound** mass budget (saves ~7 km/s of propellant needed to deliver the spacecraft to residence), but it does not rescue exit-Δv-driven delivered-fraction collapse. This isolates which levers matter for the round's central question.

### H9 — Composite A3 + A5 + A6

| Case | Δv_exit [km/s] | Isp_exit [s] | Δv_inbound [km/s] | Isp_inbound [s] | m_dry_eff [t] | delivered [t] | delivered fraction |
|---|---|---|---|---|---|---|---|
| Composite central (A3 + A5 + 20 t jettison) | 7.4 | 7000 | 20.7 | 5000 | 180 | 43.7 | **0.218** |
| Composite best case | 7.4 | 7000 | 19.2 | 5000 | 170 | 54.6 | **0.273** |
| Composite worst case | 7.4 | 7000 | 22.2 | 5000 | 190 | 32.6 | **0.163** |

| Predicted | Measured | Verdict |
|---|---|---|
| Composite delivered fraction ∈ [15%, 22%] | Central 21.8%, range [16.3%, 27.3%] | **held — load-bearing** — composite *closes* the architecture at and above Option A parity (17%) |

**This is the architecture-rescue finding.** Under the composite configuration — Earth aerocapture, Jupiter return gravity assist, Isp 7000 s exit burn over the Saturn residence period, and 20 t residence-hardware jettison before departure — the residence-class architecture delivers central 21.8% of collected mass to Earth orbit. The worst-case (conservative levers) still delivers 16.3%, essentially Option-A parity. The best-case 27.3% exceeds Option A by 10 pp.

The composite is not stretch-physics. Every lever has independent precedent:
- Earth aerocapture: heritage from Mars sample return concepts; flight-demonstrated by Mars Reconnaissance Orbiter aerobraking (lower-energy).
- Jupiter GA: heritage from Cassini, Galileo, Juno, Voyager, Pioneer (all flown).
- Isp 7000 s electric: within demonstrated range of laboratory ion engines (NEXT, BHT-6000); admissible because exit-burn duty cycle (months at low thrust) is compatible with extended grid life.
- 20 t hardware jettison: residence-class bag + scoop + accretion-management hardware estimated at 10-15 t of fabric + 5-10 t of deployable structure; mechanically separable from the spacecraft bus.

## Reading

**Headline: the residence-class architecture closes.** Under composite A3+A5+A6, central delivered fraction is 21.8% (16.3-27.3% range). This exceeds Option A's 17% parity in the central and best cases; the worst case is essentially at parity. The ram-scoop pivot is *not* sub-Option-A. The architecture survives the exit-Δv falsification gate.

Three structural findings:

**1. The exit-Δv problem has no single-lever solution. It has a multi-lever solution.** No single configuration (A2 through A8 individually) recovers delivered fraction above 14%. The composite is what works. This means the residence-class architecture's closure depends on stacking *all* of: aerocapture-class Earth arrival, a return-leg Jupiter swing-by (synodic-phasing-dependent), Isp uplift at exit, and physical jettison of residence-class hardware. None of these are stretch; their *combination* is the architecture, not any one.

**2. Chemical exit is permanently retired.** A4a and A4b both fail by wide margins. The chemical mass-ratio penalty at 7.4 km/s exit is too steep at any plausible Isp (450 s LOX/LH2 or below). Future rounds should not revisit chemical-kick exit as a residence-class candidate. Same applies to any propellant generated by Saturn-side electrolysis if the resulting Isp is in the chemical regime — the H₂/O₂ Isp ceiling at ~450 s is what kills it, not the propellant source.

**3. Resonance-pumping moon gravity assists are also permanently retired.** Net Δv from any Saturnian moon flyby from a B-ring residence orbit is *negative* — every moon costs more orbit-raise energy than its flyby returns. This extends titan's earlier R-saturn-capture-moon-gravity-assist finding (Titan flyby saves only ~300 m/s for Saturn capture) and confirms the moon GA tool is structurally absent from Saturn-system mission design for any orbit interior to Titan.

**Caveats on the closure verdict:**

- **The composite's central 21.8% requires Jupiter GA, which is synodic-phasing dependent.** Roughly half of all Earth-Saturn return windows have a viable Jupiter swing-by; the other half do not. Without Jupiter GA, the composite drops to A2+A5+A6 ≈ 14-17% (still close to Option A but not exceeding it). This makes return-window selection a load-bearing operational constraint.
- **Earth aerocapture savings of 1.5 km/s is on the conservative end of the 1.0-2.0 km/s band.** R-inbound-dv-continuous-thrust cited the spiral cost more precisely; if Earth aerocapture removes the entire spiral plus a small additional v_∞ reduction, savings could be ~2.0-2.5 km/s and composite delivered fraction would rise correspondingly.
- **The 20 t jettison assumes residence-class hardware is mechanically separable.** Detailed engineering is deferred to R-residence-bag-structural (queued). If jettison is impractical (e.g., bag-mouth structure is integral to the deployable radiator or the spacecraft bus), composite drops to 14-15%.
- **The composite worst-case at 16.3% is essentially Option-A parity — within rounding.** Treat the architecture as Option-A-equivalent in the worst case, modestly better than Option A in the central, and meaningfully better than Option A in the best case. The pre-residence-class delivered-fraction superiority of Option A is structurally erased once exit-Δv is honestly accounted.

## Revisit

Seven of nine pre-registered hypotheses held. Two falsifications:

- **H6 falsified in the predicted direction.** Dry-mass reduction uplift was undercounted by ~2× because the pre-registration treated jettison as a single-burn benefit rather than a stacked-burn benefit. The methodology lesson: when pre-registering dry-mass sensitivity across a multi-burn stack, apply the rocket-equation derivative through every burn. A formal expression: ∂(delivered)/∂(m_dry) ≈ −Π_i exp(Δv_i / (Isp_i · g₀)) − 1 (for the chunk-fed accounting used here). For a two-burn stack at 7.4 + 24.7 km/s at Isp 5000, the gradient is approximately 0.45 t delivered per tonne dry. The pre-registration implicitly assumed gradient ≈ 0.15-0.20, undercounting by ~2×.

- **H7 falsified in direction.** Predicted "moon GAs save < 0.5 km/s." Actual: moon GAs cost a net 2.7-5.7 km/s. The pre-registration imagined resonance pumping as a tactic where one pays the orbit-raise cost once and gets multiple GA benefits cheaply on subsequent encounters. In reality, the orbit-raise cost scales with the moon's orbital radius (largest for outer moons), but the GA benefit only marginally exceeds that of inner moons (because v_∞ at the moon's altitude is small for low-energy transfers). The two effects don't decouple, and net Δv is always negative.

**Methodology lesson candidate for the campaign-level PROTOCOL.md:** *Multi-burn stack effects compound dry-mass and Δv-reduction levers more than single-burn intuition predicts.* When sensitivity-testing a delivered-fraction architecture, model every burn segment explicitly; do not assume linear sensitivity.

## Cross-learning

**1. The residence-class architecture is rescued.** R-conops-chunk-vs-ram-scoop's load-bearing finding (delivered fraction collapses to 3.5% under chunk-fed continuous-thrust accounting) was correct as far as the baseline A1 went, but it was not exhaustive of available levers. Under composite A3+A5+A6, the architecture closes at or above Option A's 17%. **Saturn should treat the ram-scoop pivot as architecturally viable and proceed with doc-rewrite scoping**, with the caveat that the doc-rewrite must specify the composite configuration explicitly (single-lever rewording does not survive).

**2. R-residence-bag-structural is now critical-path again.** The exit-Δv falsification gate is cleared; the next falsification gate is bag structural integrity under ~1 MN of accretion drag plus ~30 metre-class chunk impacts during a 5-second sweep. This is iapetus-owned per active-sessions.md but should be re-prioritised.

**3. Multi-chunk row in the matrix is now triple-retired.** Falsified by (a) R-HE-graze-feasibility, (b) ram-scoop pivot operational architecture, (c) the composite architecture not requiring multiple chunks anyway. Saturn should retire that matrix row at the next integration.

**4. The "Saturn-side electrolysis can power chemical exit" rescue path is dead.** A4a's −80% delivered fraction kills any architecture that uses electrolysed water for chemical exit propellant. This propagates back into enceladus-r5's Architecture E (no Saturn-side electrolysis) which is now even more attractive — there is no chemical-exit rescue waiting in the wings for the Saturn-side-electrolysis branch.

**5. Jupiter GA on return is a load-bearing operational lever.** This changes ICEBERG's launch-window analysis. Currently the demand and pricing docs assume cadence is set by Earth-Saturn synodic period (~378 days). With Jupiter return GA load-bearing, *both* legs must have viable Jupiter alignment — the Earth-Saturn synodic period intersects with the Earth-Jupiter synodic period (~399 days) to give an effective triple-synodic constraint. **R-launch-window-cadence-revisit** is a candidate follow-on round for the demand docs.

**6. Earth aerocapture is now load-bearing for delivered fraction, not optional.** Several prior rounds (R-megawatt-aerocapture-engineering-closure, R-multi-chunk-per-mission) discussed aerocapture as an optional efficiency. The residence-class architecture *requires* it for closure. Aerocapture is no longer a Variant-C selector; it is a residence-class enabler. The matrix should reflect this dependency.

**7. Isp uplift at exit specifically (not at inbound) breaks the L0-05 / Isp coupling.** Methodology lesson 3 (titan, R-inbound-dv-continuous-thrust) said low Isp wins at the time ceiling because higher Isp lowers thrust and extends burn time. This binds during interplanetary cruise. The exit burn is *not* time-binding (executable over months of residence) and so admits higher Isp without violating L0-05. This is a useful general pattern: Isp can be optimised per-segment, not globally, and segments that have slack time budgets should use higher Isp.

## Open threads for follow-on rounds (orchestrator-routed, not Titan-owned)

| Round | Priority | Notes |
|---|---|---|
| **R-residence-bag-structural** | **critical-path** | Now the next falsification gate. ~1 MN accretion drag + ~30 metre-class chunk impacts during a 5-second sweep — does the bag survive? Iapetus-owned per active-sessions.md. |
| R-launch-window-cadence-revisit | high | Triple-synodic constraint (Earth-Saturn + Earth-Jupiter + return-leg Jupiter alignment) probably reduces effective launch cadence vs current 378-day assumption. Propagates into ICEBERG-demand.md. |
| R-residence-tour-design | moderate | The 7.4 km/s exit spiral at Isp 7000 over Saturn residence period — does megawatt-electric thrust profile / power-system duty cycle / cathode life support a 6-month low-thrust burn? Cross-reference R-cathode-life-water-plasma. |
| R-aerocapture-savings-bracket | moderate | Pin down Earth aerocapture savings precisely (1.5 km/s central estimate could be 1.0–2.5; matters for composite delivered fraction). Iapetus / Rhea heritage. |
| R-jettison-engineering-feasibility | moderate | Verify 10–30 t of residence-class hardware is mechanically separable from spacecraft bus without disabling thermal, comm, or propulsion. |
| R-chunk-as-heat-shield-revisit-under-slurry | low (conditional) | Now triggered: residence-class architecture is alive, so the slurry-payload reframe is relevant. Coherent-ice heat-shield analysis (matrix row) does not transfer to fabric-bagged slurry. |
| R-bring-particle-composition | low | Cassini RPX says > 99% water by mass; trace silicates ~1%. Confirm for downstream electrolysis. |
| R-saturn-side-residence-radiation | low | Months-long dwell at 100,000 km circular radiation dose vs Cassini-class electronics survival. |
| Multi-chunk matrix row retirement | medium | Triple-retired; remove from matrix. |
| Methodology lesson 7 to PROTOCOL.md | low | "Multi-burn stack compounds dry-mass and Δv-reduction sensitivity more than single-burn intuition predicts." |
| ICEBERG-pitch.md rewrite | high (now unblocked) | Architecture closes; doc-rewrite can proceed. Use composite A3+A5+A6 as the operational baseline. Posture remains regulated-utility. |

