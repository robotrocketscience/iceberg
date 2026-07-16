# ICEBERG — Trawl bag, deeper engineering

> **Reader's note, post-evening 2026-05-15 — η_c convention now integrated; year-twenty-plus delivered-fraction question moot under current architecture state.** Four worker handoffs integrated (titan, hyperion, enceladus, rhea — twelve rounds combined) plus four user-locked R-power-wonder findings. Hyperion's R-bag-capture-efficiency-revisit confirmed that this document's effective-specific-impulse single-number convention understates delivered-mass reduction by 3–5× when decomposed into mass-loss-before-burn (η_bag · η_feed) versus specific-impulse-degradation-during-burn (η_thr); for the (now-falsified) year-twenty-plus megawatt all-electric architecture, composite η_c falls to ~0.65 (radio-frequency-ion thrusters) rather than the 0.80 design point this document targets. **The year-twenty-plus megawatt all-electric end-to-end architecture is structurally falsified** by rhea's three rounds (R-electric-outbound-rerun, R-outbound-dv-continuous-thrust, R-megawatt-marvl-radiator) under MARVL-anchored mass + continuous-thrust delta-velocity; closest miss at 1 megawatt-electric: round-trip 19.56 yr, delivered −34.4 tonnes. **The η_c question for the surviving 500-kilowatt-electric chemical-kick + electric-inbound architecture (year zero through fifteen, retitled from "Kilopower Variant B") is the load-bearing one going forward** — at chemical-kick architecture, the chunk-fed inbound is the only leg where η_c bookkeeping matters and the chunk-mass cap is ≤ 200 tonnes per L0-05 compliance under continuous-thrust electric inbound. The bag mechanical, material, and trawl-architecture content below is unaffected. The η_c sensitivity table in §5 should be re-read with composite-η_c convention (hyperion's decomposition) rather than the single-number η_c, and at the surviving chemical-kick architecture's chunk size cap. See `water-prop/docs/ARCHITECTURE-DECISION-MATRIX.md` (post-evening section), `REQUIREMENTS.md` v0.5, and `REQUIREMENTS-L1.md` v0.2 for the integrated state.

**Companion to `ICEBERG-conops.md` §"The trawl bag — engineering treatment" (lines 605–795) and `ICEBERG-pitch.md` §9 #1–#3.** The conops establishes the trawl architecture, materials, and TRL roadmap. This document closes four bench-test-grade items that the pitch's §9 explicitly calls out as open: particle cull + lidar reject sizing, permeability **aging** (not just static WVTR), stationkeeping ΔV during fill **derived from Hill equations**, and the η_c sensitivity table with a re-framing of where the η_c bottleneck actually sits.

It also corrects two arithmetic errors in the existing conops bag treatment that I caught while doing the derivation. Both are flagged below rather than silently patched, so reviewers can audit the conops vs. this document.

---

## 0. Conops corrections (audit trail)

### 0.1 Conops line 63 (pitch §1, "Three bag-physics questions") — kinetic energy off by 10³

Conops/pitch text:

> "At 1 mm/s closing rate, a 1 m, ~500 kg ice boulder still carries ~0.25 J of impact energy distributed over the bag aperture wall"

Correct value:

`KE = ½ × m × v² = ½ × 500 kg × (10⁻³ m/s)² = 2.5 × 10⁻⁴ J = 0.25 mJ`

Off by a factor of 1000. **The corrected value strengthens the conclusion**: at the design closing rate, even a 1 m boulder carries sub-millijoule impact energy — trivially below any ballistic-fabric energy budget. The cull problem is therefore **geometry-driven (does it fit?), not energy-driven (does it puncture?)**, which changes how we size the mesh and lidar (§3 below).

For a 10 m boulder (mass ~470 t at 900 kg/m³): KE at 1 mm/s = 0.235 J. Still well within Vectran budget on energy alone. The pitch's claim that "a 10 m boulder is not [in the energy budget]" is wrong; it should read "a 10 m boulder doesn't fit through the intake." Recommend that line be reworded in the next pitch revision.

### 0.2 Conops line 673 (trawl architecture, "drift velocity") — Keplerian shear off by ~400×

Conops text:

> "a 1 km radial offset from the local ring orbit produces ~0.3 mm/s relative velocity to nearby particles"

From the Hill-Clohessy-Wiltshire equations, the differential circular-orbit velocity for radial offset Δr at orbital radius r is:

`Δv = (1/2) × n × Δr,   where n = √(GM/r³) = mean motion`

At the B-ring inner edge (r ≈ 92,000 km from Saturn center, GM_Saturn = 3.79 × 10¹⁶ m³/s²):

`v_orb = √(GM/r) = 20,300 m/s`
`n = v_orb / r = 2.21 × 10⁻⁴ rad/s`
`T_orb = 2π/n = 28,400 s ≈ 7.9 hr`

For Δr = 1 km: `Δv = ½ × 2.21 × 10⁻⁴ × 1000 = 0.11 m/s = 110 mm/s`.

Off by a factor of ~360. **This actually changes the operational sequence in a meaningful way**: to achieve the conops's design closing rates, the radial offset is much smaller than the conops implies.

| Desired closing rate | Required Δr |
|---|---|
| 1 mm/s | 9 m |
| 1 cm/s | 90 m |
| 10 cm/s | 900 m |

Holding a 9 m or 90 m radial offset against Hill secular drift is a tight stationkeeping problem (§5 below) that the conops's "1 km offset" frame did not surface. **The fix is not to back off the closing rate — it's to acknowledge the stationkeeping is non-trivial and budget for it.**

Both corrections fold into the operational implications below.

---

## 1. Scope and what this document closes

| Pitch §9 item | Status before | Closed by section |
|---|---|---|
| #1 — particle cull mesh + lidar reject loop | "bench prototype" | §3 — mesh aperture, lidar SWaP, reject corridor sizing |
| #2 — bag permeability over 7 years | static WVTR analysis only | §4 — MMOD pinhole-accumulation model + thermal-cycle fatigue |
| #3 — stationkeeping ΔV during fill | "O(10 m/s); not in §2 ΔV table" | §5 — Hill-equation derivation, fill-mass-dependent integration |
| η_c sensitivity (referenced throughout) | spot points (η_c=0.8, η_c=0.5) | §6 — full table 0.3–1.0, design-point recommendation |

What this document does **not** close: ground-test calibration (HVIT campaign at JSC/MSFC), candidate-laminate downselect (multi-vendor procurement question), and Gate D long-soak test design. Those are program activities, not paper exercises.

---

## 2. Reference values used throughout

Centralized so any single mistake is fixable in one place.

| Quantity | Symbol | Value | Source |
|---|---|---|---|
| Saturn GM | GM_S | 3.79 × 10¹⁶ m³/s² | NASA planetary fact sheet |
| B-ring inner edge | r_B | 92,000 km | Cuzzi 2010 (`pitch.md` ref 7) |
| Orbital velocity at r_B | v_orb | 20,300 m/s | √(GM/r) |
| Mean motion at r_B | n | 2.21 × 10⁻⁴ s⁻¹ | v_orb / r |
| Orbital period at r_B | T_orb | 28,400 s (7.9 hr) | 2π/n |
| Ring volume mass density | ρ_ring | ~10 kg/m³ | conops §sizing (Hedman & Nicholson 2016) |
| Ice density | ρ_ice | 920 kg/m³ | standard |
| Spacecraft dry mass (demonstrator) | m_dry | 1,000 kg | pitch §2c |
| Spacecraft wet mass at fill start | m_0 | 5,000 kg (incl. residual outbound water) | derived |
| Design closing rate (collection phase) | v_rel | 1 cm/s | conops §collection-rate (now via Δr ≈ 90 m, not 1 km) |
| Inbound chunk-fed ΔV requirement | ΔV_in | 4,200 m/s | pitch §2 ΔV table |
| Open-literature water-MET Isp proxy | Isp | 700 s | pitch ref [^isp] |
| Exhaust velocity | v_e | 6,870 m/s | g × Isp |
| Micrometeoroid flux integrand at 1 AU | F(>m) | Grün 1985 model | NASA SSP-30425 |

---

## 3. Particle cull — mesh aperture and forward lidar

### 3.1 The cull problem, restated

Per §0.1, the cull is **size-exclusion**, not energy-exclusion. A particle that fits inside the storage cylinder and decelerates within the inelastic-capture liner is acceptable; one that doesn't fit jams the bag and ends the mission.

For the 14 t demonstrator (storage cylinder ≈ 3.4 m diameter × 3.4 m long, conops table line 646), the maximum acceptable single-particle dimension is roughly **half the cylinder diameter** — i.e. 1.7 m maximum chord, with realistic safety margin → **1 m mesh aperture**.

### 3.2 Mesh sizing

Inlet mesh is a coarse pre-screen, not a high-pressure-drop filter. Requirements:

- Aperture ≤ 1 m (geometric exclusion)
- Open area fraction ≥ 80% (don't choke the volumetric flow rate that drives the conops collection-rate table)
- Mass: <50 kg for a 100 m² intake
- Heritage: deployable mesh antennas (Harris AstroMesh family — 15+ flight units, decades of heritage on commercial GEO; Northrop's mesh reflectors on MUOS, SkyTerra; JWST is rigid not relevant here)

**Construction:** gold-plated molybdenum wire (AstroMesh heritage) or Vectran cordage. Either supports the 1 m aperture with ~10 mm cord diameter at the spans involved. Deployment is the same hoop-and-radial-spoke geometry as a deployable antenna, sized for ~10 m diameter — well inside heritage envelope.

### 3.3 Forward lidar — what's it actually for

**Closing rate (cm/s class) does not need lidar to react to** — at 1 cm/s, even a 100 m detection range gives 10⁴ s = 2.8 hr to react. Trivially within any onboard control loop.

The actual lidar job is to detect **bulk-motion outliers**: bodies moving faster than local Keplerian shear. Two source classes:

1. **"Propeller" moonlets** (Tiscareno 2010) — embedded 100+ m bodies orbiting on near-Keplerian trajectories. Detectable by orbital wake (a propeller-shaped clearing in the surrounding ring). Predictable from imagery, not surprises.
2. **B-ring velocity-dispersion outliers** — the local velocity distribution has a tail of ~cm/s residuals. Most ring particles have small dispersion (mm/s); occasional particles arrive at 5–10 cm/s. These are the lidar's actual targets.

| Lidar requirement | Value | Heritage |
|---|---|---|
| Range | 1 km | OSIRIS-REx GoldenEye TAG sensor (Lockheed) |
| FOV | ~30° conical | Standard nav-lidar |
| Range resolution | 10 cm | OSIRIS-REx, Hayabusa2 |
| Update rate | 10 Hz | Standard |
| Mass | ~8 kg | Leonardo / Ball flight units |
| Power | ~25 W active | Standard |

**Reject corridor:** at 1 km detection range and 10 cm/s closing-outlier velocity, time-to-contact = 10⁴ s. With a 50 mN water-MET thrust on a 5 t spacecraft (a = 10⁻⁵ m/s²), avoidance ΔV of 1 m/s requires ~10⁵ s. **The lidar warning time is too short for thrust avoidance against fast outliers.**

The realistic reject is **rotational dodge of the intake aperture**, not translational dodge of the spacecraft. Spinning the bag away from an incoming outlier on RCS torque takes ~10–60 s for a few-degree rotation; well within the 10⁴ s warning. Cost: ~10⁻³ N·m·s of momentum per dodge; ~10–100 dodges per fill — negligible RCS budget.

If outlier flux is high enough that the dodge cadence interrupts collection too often, the operational answer is **decrease aperture** (reduce sky exposure to outliers) and **trade against fill duration**, not avoidance ΔV.

### 3.4 What's still open

- **Outlier flux at the B-ring radius** is not directly observed at the cm/s scale — Cassini imagery resolution and frame rate weren't built for it. Needs Gate-A bench-test calibration against published velocity-dispersion models, and ideally a cubesat-scale ride-along on a future Saturn mission to measure directly. **Not a no-go; worst case the dodge cadence doubles fill duration, which is well within the 6-month Saturn-system loiter budget.**
- **Mesh fouling by sub-aperture particles** (the ones we *want*) — repeated mm-scale impacts could plate the mesh wires with ice over the fill. Order of magnitude: at ρ_ring = 10 kg/m³ and 1 cm/s through a 100 m² aperture, mass through aperture is 1 kg/s. Mesh wire surface area ~10 m². Sub-aperture pass-through fraction is the design variable. Bench-test answer.

---

## 4. Permeability **aging** over 7 years

### 4.1 Why static WVTR isn't the answer

Conops §permeability shows the candidate barrier films are 4–5 orders of magnitude over budget at standard test conditions. That's correct and load-bearing — at t=0. **The unaddressed question is what those numbers look like after 7 years of cruise.**

Three aging mechanisms matter; one dominates.

### 4.2 Mechanism A — micrometeoroid pinhole accumulation (dominant)

**Flux model.** Grün et al. 1985 (canonical reference, NASA SSP-30425 derives the engineering model from it) gives interplanetary micrometeoroid mass flux at 1 AU:

| Particle mass threshold | Cumulative flux (m⁻² s⁻¹) |
|---|---|
| > 10⁻¹² g (sub-micron) | ~10⁻⁵ |
| > 10⁻⁹ g (~10 μm) | ~10⁻⁷ |
| > 10⁻⁶ g (~100 μm) | ~10⁻¹⁰ |
| > 10⁻³ g (~1 mm) | ~10⁻¹² |

**At Saturn distance the flux drops** — interplanetary dust population thins with heliocentric distance roughly as r⁻¹ to r⁻¹·⁵. Use 10× reduction at 9.5 AU as a planning value (Divine 1993 interplanetary meteoroid model).

**Outbound + inbound integrated exposure** for a 200 m² bag system over 14 years (combining 1 AU at endpoints and dropping flux through cruise): ~6 × 10¹⁴ m²·s of integrated exposure-time. Dominant contributor by *count* is the sub-micron flux; dominant by *pinhole area* is the 10–100 μm flux.

**Pinhole conversion.** Hypervelocity impact on multilayer films creates a hole roughly 5–10× the particle diameter (Whipple shielding theory; Cour-Palais 1979; ESA MASTER model calibration). For the engineering bound, assume:

- 10 μm particles → 80 μm pinholes → ~5 × 10⁻⁹ m² each
- 100 μm particles → 800 μm pinholes → ~5 × 10⁻⁷ m² each

Integrated over 14-year exposure on 200 m²:

| Particle size | Impacts (14 yr, 200 m², heliocentric-averaged) | Pinhole area added |
|---|---|---|
| 10 μm | ~6,000 | ~3 × 10⁻⁵ m² |
| 100 μm | ~6 | ~3 × 10⁻⁶ m² |
| 1 mm | ~0.06 | negligible (probabilistic — may not occur) |

**Total pinhole area accumulated: ~3 × 10⁻⁵ m² out of 200 m² = 1.5 × 10⁻⁷ open-area fraction.**

**Flow through pinholes** for water vapor at 200 K bag interior, ~100 Pa partial pressure, into vacuum: molecular-effusion regime (Knudsen number >> 1 for sub-mm pinholes). Hertz-Knudsen flux:

`ṁ = P × √(M / (2π R T))`

For H₂O at 100 Pa, 200 K, M = 0.018 kg/mol, R = 8.314 J/(mol·K):

`ṁ = 100 × √(0.018 / (2π × 8.314 × 200)) = 100 × √(1.72 × 10⁻⁵) = 0.42 kg/(m²·s)`

Through 3 × 10⁻⁵ m² of pinhole area: **1.3 × 10⁻⁵ kg/s = 1.1 kg/day.**

**Compare to conops permeability budget**: 22 kg/day total acceptable leak. Pinhole leak by mission end is **5% of budget**. The Whipple bumper outer layer reduces the pinhole accumulation rate by another order of magnitude through MMOD pre-shattering. **Net: MMOD pinhole accumulation is 4×–10× under budget across the mission.**

### 4.3 Mechanism B — thermal-cycle fatigue (small)

Hot-side / cold-side delta is roughly 200 K → <150 K = 50 K across the bag wall in steady state. Spacecraft body rotation (if any) cycles each surface element through this delta. Even at 1 RPM, that's 5 × 10⁸ cycles over 14 years — well into fatigue regimes.

Heritage: Voyager MLI has survived 47+ years with much harsher thermal cycling on antenna boom segments. JWST sunshield holds sub-Kelvin temperature stability across deployed film layers. Failure mode is delamination at panel seams, not bulk film cracking.

**Mitigation:** seam quality on multi-vendor laminate is the manufacturing-craftsmanship constraint. Existing aerospace MLI vendors (Stress Engineering Services, NeXolve, Energy Sciences) routinely deliver seam quality good for decade-class missions. Not a paper-grade open question.

### 4.4 Mechanism C — UV / GCR polymer crosslinking (negligible at this duty)

Polyimide (Kapton) and polyester films crosslink slowly under deep-space UV and GCR. Mass-loss rates on Kapton at 1 AU are ~10⁻¹⁵ kg/(m²·s) for unprotected film; metallized films cut this by ~10⁴ (Voyager MLI flight data, NASA TM-2002-211727).

For a 200 m² bag over 14 years on metallized Kapton: ~9 × 10⁻¹⁰ kg total mass loss. Mechanism is irrelevant at this timescale.

### 4.5 Net permeability aging conclusion

| Source | Leak rate at end of mission | % of 22 kg/day budget |
|---|---|---|
| MMOD pinhole accumulation | ~1.1 kg/day | 5% |
| Thermal-cycle seam fatigue | <0.1 kg/day (heritage estimate) | <0.5% |
| UV/GCR polymer breakdown | negligible | ~0% |
| **Total aging contribution** | **~1.2 kg/day** | **~5%** |
| Static WVTR baseline | <0.001 kg/day | <0.005% |
| **End-of-mission total leak** | **~1.2 kg/day** | **~5%** |

**Bag permeability over 7 years closes with ~20× margin to budget.** §9 #2 ("if more than ~5% of cargo mass is lost to leak across the inbound coast, chunk-fed ΔV no longer closes Tsiolkovsky") is satisfied: end-of-mission cumulative leak is ~6 t against a 67 t collected mass = ~9% across the full 14 years, of which the fill-to-Earth-arrival inbound 7-year leg is roughly half. Inbound leg leak ≈ 4–5% of cargo. **Within budget; not the binding constraint.**

### 4.6 What still needs ground-test calibration

- **HVIT campaign at JSC or MSFC.** Light-gas-gun shots of sub-mm particles at 5–10 km/s into candidate laminates; measure pinhole geometry vs. particle mass. Maps the Cour-Palais bound from theory to as-built. **Cost: $5–10M, 18 months.** Standard MMOD qualification.
- **Long-duration thermal-vacuum chamber test.** Candidate laminate at 200–280 K with mass-loss telemetry across 10⁴-cycle equivalent. **Cost: $2–4M, 12 months.** Existing vendor capability.
- **Multi-vendor procurement.** Three candidate stack designs (NeXolve, NASA Glenn cryogenic-thermal-protection-system heritage, IRVE-3 inflatable heritage) bench-tested in parallel. Downselect at Gate A. **Cost: $8–15M, parallel with above.**

---

## 5. Stationkeeping ΔV during fill — Hill-equation derivation

### 5.1 The setup

Per §0.2: to achieve 1 cm/s closing rate, spacecraft sits at Δr ≈ 90 m radial offset from local Keplerian. **This offset is unstable in Hill dynamics** — a free particle at Δr drifts in-track at rate -3/2 × n × Δr × t (linear secular drift) and oscillates radially with amplitude ∝ initial radial velocity. Maintaining the offset requires continuous thrust.

### 5.2 Required acceleration

For station-keeping at fixed Δr in the rotating local frame, the required radial acceleration to cancel the Hill secular term is:

`a_radial = 3 × n² × Δr`

At r_B with n = 2.21 × 10⁻⁴ s⁻¹ and Δr = 90 m:

`a_radial = 3 × (2.21 × 10⁻⁴)² × 90 = 1.32 × 10⁻⁵ m/s²`

For a 5,000 kg spacecraft at fill start: thrust required = 66 mN. **This is well within the water-MET continuous-thrust capability** (open-literature water-MET thrust is in the 10–500 mN class for the 1–10 kWe input range).

### 5.3 Integrated ΔV over fill duration

For a 14 t collection at 1 cm/s closing rate and 100 m² aperture, conops §collection-rate gives **fill duration ≈ 10 hr**. Over that interval, the spacecraft mass grows from m_0 = 5 t to m_f ≈ 19 t (pre-existing dry + outbound residual + collected). Required thrust grows in proportion.

Integrated ΔV over a 10 hr fill, treating mass as linearly increasing:

`ΔV_fill ≈ a × t × (m_avg / m_0_correction) ≈ 1.32 × 10⁻⁵ × 36000 × (1 + correction) ≈ 0.5–0.8 m/s`

Plus radial-offset cancellation at end-of-fill: ~0.1 m/s impulsive.

**Total fill-phase ΔV: ~1 m/s for a 14 t collection at the design point.**

### 5.4 Scaling to larger chunks

| Delivered chunk | Collected | Aperture | Fill duration | Stationkeeping ΔV |
|---|---|---|---|---|
| 10 t | 14 t | 100 m² | 10 hr | ~1 m/s |
| 50 t | 67 t | 100 m² | 50 hr | ~5 m/s |
| 50 t (alt) | 67 t | 200 m² | 25 hr | ~3 m/s |
| 200 t | 270 t | 200 m² | 100 hr | ~12 m/s |
| 1000 t | 1340 t | 400 m² | 250 hr | ~30 m/s |

**Per-flight stationkeeping ΔV ranges from 1 m/s (demonstrator) to 30 m/s (steady-state-era max-chunk).** Conops's "O(10 m/s)" estimate was the right order of magnitude for the mid-program FSP era; off by ~3× low for the steady-state MW-class era.

### 5.5 Where this lives in the §2 ΔV table

Add as a line item in `pitch.md` §2:

```
| Stationkeeping during fill (chunk-size dependent) | 1–30 m/s | Water-MET | Earth-launched water (small) |
```

Negligible against the 13,000 m/s round-trip total. Worth surfacing for completeness, not for budget impact.

### 5.6 What's still open

- **Position knowledge requirement.** Holding 90 m radial offset at Saturn distance with 80-min light-time means the spacecraft's local-frame nav must be onboard, vision-based against ring-particle features. Delta from Phase 5b autonomy stack: small — same sensor, same compute.
- **Coupling to CoM walk.** As the bag fills, c.o.m. moves rearward into the cylinder. Stationkeeping thrust line must be re-trimmed continuously. Bench-test/sim-grade work.
- **Differential drag / non-Keplerian forcing in B-ring.** Saturn's gravitational harmonics (J₂, J₄) and ring self-gravity perturb the local frame slightly. Magnitude is well within budget, but adds ~10% sim-validation work for trajectory design.

---

## 6. η_c sensitivity — and a re-framing

### 6.1 The bag is **not** the η_c bottleneck

The pitch and conops both treat η_c as a bag property — "shroud capture efficiency" is the language. **That framing is misleading.** η_c is the product of three serial efficiencies:

`η_c = η_bag × η_feed × η_MET`

| Term | Definition | Realistic range | Driver |
|---|---|---|---|
| η_bag | Fraction of sublimated water captured by cold-wall before escaping | 0.95–0.99 | §4 permeability + cold-wall sticking coefficient |
| η_feed | Fraction of cold-wall frost successfully re-sublimated and routed to MET | 0.95–0.99 | Harvest-port heater design + plumbing |
| η_MET | MET propellant utilization × mass utilization | 0.75–0.92 | Propulsion engineering — the MET itself |

**Net: η_c = 0.68–0.90, with the MET being the dominant uncertainty, not the bag.** η_bag is well-bounded by §4. η_feed is essentially a heated-line problem. η_MET is the open-literature number that's in the 75–95% range depending on operating mode and is what vendor-actual hardware data would settle.

### 6.2 Sensitivity table

For inbound chunk-fed ΔV = 4,200 m/s (pitch §2), Isp = 700 s, v_e = 6,870 m/s:

`m_0 / m_f = exp(ΔV / (η_c × v_e))`
`Delivered fraction = m_f / m_0`

| η_c | Effective Isp (s) | Mass ratio | Delivered fraction of collected |
|---|---|---|---|
| 1.00 | 700 | 1.85 | 54% |
| 0.95 | 665 | 1.92 | 52% |
| 0.90 | 630 | 1.98 | 50% |
| 0.85 | 595 | 2.07 | 48% |
| **0.80** (design point) | **560** | **2.16** | **46%** |
| 0.75 | 525 | 2.27 | 44% |
| 0.70 | 490 | 2.40 | 42% |
| 0.60 | 420 | 2.72 | 37% |
| 0.50 | 350 | 3.30 | 30% |
| 0.40 | 280 | 4.34 | 23% |
| **0.30** (cliff) | **210** | **6.42** | **16%** |

### 6.3 Design-point recommendation

**Design η_c = 0.80** with the following budget allocation:

- η_bag ≥ 0.97 (achievable per §4)
- η_feed ≥ 0.95 (heated-line heritage)
- η_MET ≥ 0.87 (mid-band of open-literature range; calibrate against vendor-actual data)
- **Margin to cliff (η_c < 0.5): 0.30 of system efficiency** before architecture stops closing. Comfortable reserve.

The pitch §2 currently quotes 54% delivered chunk efficiency at "Isp = 700 s" without qualifying that this implicitly assumes η_c = 1.0. **The honest planning number is 46% delivered at η_c = 0.80.** This revises the pitch §4 era table downward by a relative ~15% across the board — small enough not to threaten the thesis, large enough to be worth a footnote.

| Era | Pitch §4 chunk delivery (η_c=1) | Honest delivery (η_c=0.80) |
|---|---|---|
| Floor (Kilopower) | 50 t | ~42 t |
| FSP-era | 100–200 t | ~85–170 t |
| Sub-MW–MW era | 500–1000 t | ~425–850 t |

Recommend the next pitch revision either (a) carry the η_c = 0.80 numbers as headline and footnote the η_c = 1.0 idealized case, or (b) raise the headline collected-mass targets so that delivered tonnages match the existing era table at η_c = 0.80. Either is honest; (b) is narratively stronger because it preserves the era-table headline numbers.

### 6.4 What changes if the MET disclosed Isp differs

The whole sensitivity scales with v_e = g × Isp. If the actual MET Isp is in the 500–800 s range (open-literature water-MET envelope), the table shifts:

| MET Isp | η_c=0.80 effective Isp | Delivered fraction |
|---|---|---|
| 500 s | 400 s | 35% |
| 600 s | 480 s | 41% |
| **700 s** (proxy) | **560 s** | **46%** |
| 800 s | 640 s | 51% |
| 900 s (optimistic) | 720 s | 56% |

**The thesis closes across the entire plausible Isp range.** The vendor-actual number sets the chunk-mass-target sizing, not the closure question.

---

## 7. Updated open-questions (delta to pitch §9)

| § | Item | Status before this doc | Status after |
|---|---|---|---|
| #1 | Particle cull mesh + lidar | "bench prototype the mesh" | **Sized**: 1 m mesh aperture, 1 km lidar, rotational-dodge reject. Bench-test still needed for outlier-flux calibration and mesh-fouling rate. |
| #2 | Permeability over 7 years | "long-duration thermal-vacuum chamber test of candidate laminates" | **Closed on paper** at ~5% of budget. HVIT and multi-vendor procurement still open as $15–30M Gate-A program. |
| #3 | Stationkeeping ΔV during fill | "O(10 m/s); not in §2 ΔV table" | **Derived**: 1–30 m/s scaling with chunk size. Add to §2 table at next pitch revision. |
| (new) | η_c reframing — MET dominates, not bag | implicit; pitch quoted η_c-blended numbers ambiguously | **Reframed**: η_c = η_bag × η_feed × η_MET; design 0.80; revise pitch §4 chunk targets accordingly. |
| (closed 2026-05-15) | Conops 0.25 J / 1 km offset arithmetic errors | not flagged | **Patched in pitch line 58 and conops lines 672 + 738.** §0.1 and §0.2 here remain the canonical derivation. |

---

## 8. Cost and schedule for closing the residuals

**Bench-grade closure of the bag-engineering residuals before Gate A funds a flight unit:**

| Activity | Cost | Duration | Notes |
|---|---|---|---|
| HVIT MMOD characterization on candidate laminates | $5–10M | 18 mo | JSC/MSFC light-gas gun |
| Multi-vendor laminate procurement and parallel TVAC qual | $8–15M | 12 mo | NeXolve / Glenn-CTPS / IRVE-3 vendors |
| Mesh + intake aperture prototype + vacuum-chamber simulant testing | $3–6M | 12 mo | ground rig with water-ice pellet dispenser |
| Forward-lidar SWaP & FOV trade vs. heritage units | $1–2M | 6 mo | trade study, no hardware |
| Outlier-flux model refinement (Cassini archive re-analysis) | $0.5–1M | 6 mo | university subcontract; PSI / SwRI candidates |
| **Total bag-engineering residual closure** | **$18–34M** | **~18 mo** | All parallelizable; sets Gate A go/no-go |

This figure rolls up under the conops §TRL-roadmap Phase TRL 3–4 cost line ($20–42M combined), so the deeper engineering work above doesn't blow the existing budget — it spends the same money against sharper acceptance criteria.

---

## 9. What this document does **not** address (deferred)

- **Cinch/seal mechanism detailed design.** Conops names "drawstring or iris"; a real downselect needs prototyping.
- **Center-of-mass walk model for GNC.** Conops names the problem; quantitative GNC sim is its own document.
- **Gate D long-soak orbital testbed scope.** Pitch §9 #4 calls it the largest residual; deserves its own design exercise (~similar length to this document).
- **Phase 5b autonomy architecture.** Mentioned in pitch §9 #5; deferred to a separate companion doc if pursued.
- **Crewed variant — cargo as GCR shield.** Conops §810 raises it as upside; not engineered here.

Each is a similar-scope deliverable. Prioritization is an operator-internal decision.

---

*Methodology: Hill-Clohessy-Wiltshire equations from Vallado, *Fundamentals of Astrodynamics and Applications*, 4th ed. Hertz-Knudsen flux for free-molecular regime. Cour-Palais hypervelocity-impact bound from NASA SSP-30425. Grün 1985 micrometeoroid flux model. Divine 1993 interplanetary meteoroid model for heliocentric scaling. All numerical derivations spot-checked but not formally simulated; values are paper-grade and to be calibrated against vendor-internal data plus Gate-A bench tests.*
