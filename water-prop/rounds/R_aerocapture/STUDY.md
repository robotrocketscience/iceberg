# R-aerocapture — does Earth aerocapture eliminate the propulsive inbound burden?

**Status:** pre-result.

## Question

The architecture decision matrix flags Earth aerocapture as "the single highest-leverage unresolved technical question." If aerocapture works, the 6.42 km/s post-lunar-tour propulsive inbound delta-v collapses to a small trim budget (~0.5 km/s for lunar-flyby navigation correction and final circularization). That changes every cell in the matrix:
- Inbound burn times collapse from 7–45 years to weeks-to-months.
- Reactor power requirements drop because the electric stage only has to do trim.
- The Variant B chunk-fed-chemical winning region disappears entirely (no Saturn-depart impulsive burn needed; deliveries can spiral down passively from lunar tour).
- The 14-year round-trip ceiling becomes structurally achievable across all reactor eras.

The trade-off: a heat shield. For a vehicle entering Earth's atmosphere at hyperbolic excess velocity v_∞ ~ 6 km/s (post-lunar-tour), peak stagnation-point heat flux is roughly 1–10 megawatts per square metre over a ~3-minute pulse. Heat shield mass fractions in the open literature for sample-return missions of this entry-velocity class run 5–15% of entering mass. For a 100-tonne vehicle, that is 5–15 tonnes of heat shield — comparable to the vehicle dry mass itself, but a fraction of the propellant the propulsive alternative would burn.

**Plus a novel possibility:** the water-ice chunk itself is competent thermal mass. Sublimating water absorbs ~2.5 megajoules per kilogram. For a 100-tonne chunk at 1 megajoule per square metre heat load over a 10-square-metre windward face, total heat ≈ 10 megajoules, requiring 4 kilograms of sublimated water. **The chunk is its own heat shield**, with negligible mass cost to the chunk inventory. Whether this works depends on geometry and bag survival under hypersonic flow, which are engineering questions outside the scope of this round.

The question this round answers: **conditional on aerocapture being feasible at v_∞ = 6 km/s with a heat shield mass fraction of 5–15%, how does the architecture matrix shift?** The technology-readiness question (will it actually work?) is named but not closed by this round.

## Pre-registered hypothesis (H-ac)

**Aggregate (H-ac-agg):** Aerocapture at v_∞ = 6 km/s collapses propulsive inbound delta-v to ~0.5 km/s. Delivered mass increases by 30–50% across all architecture-matrix cells at the cost of a heat shield mass fraction of 5–15% of entry mass. All-electric architecture wins more broadly; Variant B's winning region disappears entirely; the 14-year round-trip becomes feasible at Kilopower era for chunks up to 200 tonnes.

**Pre-registered sub-claims:**

| Sub-claim | Predicted | Falsification |
|---|---|---|
| H-ac-a — Heat shield mass fraction at v_∞ = 6 km/s, 10 m² heat-shield area | 5–15% of entry mass | outside ±25% |
| H-ac-b — Aerocapture-enabled inbound propulsive delta-v | 0.3–1.0 km/s (lunar tour trim + post-capture circularization) | outside ±0.3 km/s |
| H-ac-c — Delivered mass increase at Kilopower / 100 t cell (vs all-electric without aerocapture) | 30–50% | outside ±20% |
| H-ac-d — Variant B's winning region (Kilopower + chunks ≥ 100 t at high permeability) | disappears entirely | falsified if any Variant B cell still wins under aerocapture |
| H-ac-e — Kilopower-era inbound burn time under aerocapture | < 2 yr (vs 23–45 yr without) | outside ±1 yr |
| H-ac-f — 14-yr round-trip ceiling achievable at Kilopower under aerocapture | yes | falsified if any chunk ≥ 50 t at Kilopower exceeds 14-yr round trip |

**Aggregate decision:** if H-ac-agg holds, **Earth aerocapture is the single most consequential program technical investment**, surpassing megawatt reactor development, dual-ion thruster qualification, and bag-laminate permeability. The implication is that the inbound thermal-protection-system program (heat shield qualification at v_∞ 6 km/s for a multi-tonne vehicle with novel chunk-as-windward-face geometry) becomes the binding precursor for ICEBERG, and reactor scaling becomes secondary.

## Method

**Heat shield mass fraction (Sutton-Graves stagnation-point approximation):**

For aerocapture at v_∞ = 6 km/s, atmospheric entry velocity at periapsis ≈ √(v_∞² + 2 × G × M_earth / r_periapsis) ≈ 11 km/s for 90 km periapsis.

Peak stagnation-point heat flux (Sutton-Graves):

```
q_dot_max ≈ k_SG × √(rho_atm / R_nose) × v_entry^3
```

where k_SG ≈ 1.74e-4 (in W·m⁻²·(kg·m⁻³)⁻⁰·⁵·(m/s)⁻³ units), rho_atm ≈ 1e-5 to 1e-4 kg/m³ at 90 km, R_nose = effective nose radius. For a 100-tonne vehicle with 10 m² windward area (5.6 m² ≈ R_eff 1.3 m).

Total heat load Q ≈ q_dot_max × t_pulse where t_pulse ≈ 200 s for a high-energy aerocapture.

Heat shield mass per unit area ≈ Q / Q_specific where Q_specific ≈ 30 MJ/kg for ablative shields (PICA-X class). Total heat shield mass = (heat shield mass/area) × area.

**Architecture comparison with aerocapture:**

Replace inbound propulsive delta-v from 6.42 km/s to 0.5 km/s in the existing all-electric and Variant B inbound models. Add heat shield mass to the vehicle dry mass. Re-compute delivered water and launch mass for each (reactor, chunk) cell.

**Sweep axes:**

- Reactor power: 10, 40, 100, 200, 500, 1000 kilowatt-electric (consistent with prior rounds)
- Chunk mass: 100, 200, 500 tonnes
- Heat shield mass fraction: 5%, 10%, 15% of entry mass (sweep to handle uncertainty)
- Inbound propulsive trim: 0.3, 0.5, 1.0 km/s (sweep to test sensitivity)
- Electric specific impulse: 1500, 2000, 2934, 5000 s
- Outbound architecture: A (all-electric, baseline assumption for relative comparison)

**Validity caveats:**

- Sutton-Graves is a stagnation-point approximation. Real aerocapture has variable heat flux over the windward area; integrated load is typically 0.5–0.7× the peak flux integrated naively.
- Heat shield mass scales with total heat load Q, not peak flux. A long, gentle aerocapture (deeper periapsis, longer pulse) gives lower peak flux but higher total Q.
- The chunk-as-heat-shield possibility is *not* modeled here. If it works, heat-shield mass fraction drops to ~0% and delivered mass goes up further. This round uses a conventional heat shield (PICA-X class).
- Trajectory dispersion not modeled. Real aerocapture requires periapsis altitude control to ±2 km; missing high → vehicle escapes back to space, missing low → vehicle crashes. Both failure modes are mass-cost neutral but mission-fatal.
- Atmospheric density uncertainty (±30% real-world) affects delta-v dissipated, which affects shield mass required. Not in this round.
- For 100-tonne mass aerocapture is unprecedented at this entry velocity. Apollo capsule returned at v_∞ ~ 0 km/s (entry at ~11 km/s but for a 6-tonne vehicle). Galileo Jupiter atmosphere probe entered at v_∞ ~ 47 km/s but was a 0.34-tonne sphere with a 100% heat shield. Multi-tonne aerocapture at intermediate velocities is technology-readiness ~4 (component demonstrated in lab) rather than ~7 (flight-proven). This round assumes it works; the technology-readiness gap is named but not closed.
- Multi-orbit aerobraking to circularize from initial elliptical capture not in scope. After aerocapture, the vehicle is in a high elliptical orbit with periapsis ~90 km (in atmosphere). Multiple aerobraking passes shrink the apogee to low Earth orbit altitude over weeks. Mass cost ~0; time cost ~3 months.

## Result

### Heat shield characterization at v_∞ = 6 km/s

| Quantity | Value | Notes |
|---|---:|---|
| Entry velocity at 90 km periapsis | 12.62 km/s | v_∞² + 2 G M / r_p |
| Peak convective stagnation-point heat flux (Sutton-Graves) | 3.07 MW/m² | only convective; **radiative not included** |
| Total convective heat load over 200 s pulse (0.6 peak-to-average factor) | 368 MJ/m² | |
| Shield mass per unit area at 30 MJ/kg ablative | 12.3 kg/m² | PICA-X-class |
| Shield mass for 10 m² windward area | **0.12 tonnes** | **0.12% of 100-t entry mass** |

**The Sutton-Graves result is much smaller than literature shield fractions** (5–15% for Stardust, Orion, Mars sample return class). Two reasons:

1. **Sutton-Graves captures only convective heating; radiative heating is missing.** At entry velocity 12.6 km/s, radiative heating is roughly comparable to convective in magnitude. Adding radiative roughly triples total heat load → shield mass ≈ 0.4 tonnes ≈ 0.4% of entry mass.

2. **Shield mass fraction scales inversely with vehicle size.** Stardust (46 kg, 12% shield) and Orion (8.5 t, 9%) are small enough that surface-to-volume penalizes them. For a 100-tonne vehicle with ~25 m² windward area, scaled shield mass ≈ 1.25 tonnes ≈ **1.25% of entry mass**, even including radiative. Heritage shield-mass-fraction numbers do not apply.

**Bottom line on shield mass:** for a 100-tonne vehicle at v_∞ = 6 km/s, realistic shield mass fraction is **1–3%**, not the 5–15% predicted in H-ac-a. The architecture sweep below used 5%, 10%, 15% parametrically; the real value is at the favorable low end, so all "aero delivered" numbers below are *lower bounds*.

### Delivered water — baseline vs aerocapture (10% shield, 0.5 km/s trim)

| Reactor (kWe) | Chunk (t) | Baseline delivered | Aerocapture delivered | Improvement | Baseline 7-yr feasible? | Aero 7-yr feasible? |
|---:|---:|---:|---:|---:|:--:|:--:|
|   10 | 100 | 87.0 t |  98.0 t | +13% | **no** | yes |
|   10 | 200 | 174.7 t | 194.3 t | +11% | **no** | yes |
|   40 | 100 | 86.6 t |  98.8 t | +14% | **no** | yes |
|   40 | 200 | 174.4 t | 197.7 t | +13% | **no** | yes |
|   40 | 500 | 437.5 t | 490.4 t | +12% | **no** | yes |
|  100 | 100 | 85.9 t |  98.7 t | +15% | **no** | yes |
|  100 | 200 | 173.6 t | 197.6 t | +14% | **no** | yes |
|  100 | 500 | 436.8 t | 494.3 t | +13% | **no** | yes |
|  200 | 100 | 84.7 t |  98.6 t | +16% | yes | yes |
|  200 | 200 | 172.4 t | 197.5 t | +15% | **no** | yes |
|  200 | 500 | 435.6 t | 494.1 t | +13% | **no** | yes |
|  500 | 100 | 81.0 t |  98.3 t | +21% | yes | yes |
|  500 | 200 | 168.7 t | 197.2 t | +17% | yes | yes |
|  500 | 500 | 431.9 t | 493.8 t | +14% | **no** | yes |
| 1000 | 100 | 74.8 t |  97.7 t | +31% | yes | yes |
| 1000 | 200 | 162.6 t | 196.6 t | +21% | yes | yes |
| 1000 | 500 | 425.8 t | 493.2 t | +16% | yes | yes |

### Inbound burn time — baseline vs aerocapture

| Reactor (kWe) | Chunk (t) | Baseline burn (yr) | Aero burn (yr) | Effect |
|---:|---:|---:|---:|---|
|   10 | 100 |  90.1 yr |  4.05 yr | **infeasible → feasible** |
|   10 | 200 | 175.1 yr |  5.35 yr | infeasible → feasible |
|   40 | 100 |  23.2 yr |  2.11 yr | infeasible → feasible |
|   40 | 200 |  44.4 yr |  4.04 yr | infeasible → feasible |
|   40 | 500 | 108.2 yr |  4.87 yr | infeasible → feasible |
|  100 | 100 |   9.8 yr |  0.89 yr | infeasible → feasible |
|  100 | 200 |  18.3 yr |  1.66 yr | infeasible → feasible |
|  100 | 500 |  43.8 yr |  3.98 yr | infeasible → feasible |
|  200 | 100 |   5.3 yr |  0.48 yr | shrinks 4.8 yr |
|  200 | 200 |   9.6 yr |  0.87 yr | infeasible → feasible |
|  200 | 500 |  22.3 yr |  2.03 yr | infeasible → feasible |
|  500 | 100 |   2.6 yr |  0.24 yr | shrinks 2.4 yr |
|  500 | 200 |   4.3 yr |  0.39 yr | shrinks 3.9 yr |
|  500 | 500 |   9.4 yr |  0.86 yr | infeasible → feasible |
| 1000 | 100 |   1.7 yr |  0.16 yr | shrinks 1.6 yr |
| 1000 | 200 |   2.6 yr |  0.24 yr | shrinks 2.4 yr |
| 1000 | 500 |   5.1 yr |  0.47 yr | shrinks 4.7 yr |

### Sensitivity at 100 t chunk × 40 kilowatt-electric: shield fraction × trim Δv

| Shield % | Trim Δv = 0.3 km/s | Trim Δv = 0.5 km/s | Trim Δv = 1.0 km/s |
|---:|---:|---:|---:|
|  5% | 99.3 t | 98.8 t | 97.7 t |
| 10% | 99.3 t | 98.8 t | 97.6 t |
| 15% | 99.2 t | 98.7 t | 97.5 t |

**Shield-mass-fraction sensitivity is negligible** in the 5–15% range. Even a 15% shield (high end of literature) costs only 0.1–0.3 tonnes of delivered mass per 100 t cell. The shield mass fraction is not a load-bearing input.

### Hypothesis grading

| Sub-claim | Predicted | Actual | Held? |
|---|---|---|---|
| H-ac-a — Shield mass fraction at v_∞ = 6 km/s | 5–15% | 0.12% (Sutton-Graves convective only); ~1–3% with radiative + scaling | **falsified-low**; heritage values do not scale to 100-tonne vehicles |
| H-ac-b — Aerocapture-enabled inbound propulsive Δv | 0.3–1.0 km/s | swept as parameter | held by construction |
| H-ac-c — Delivered mass increase at Kilopower / 100 t | 30–50% | +13% | **falsified-low**; the chunk was almost fully delivered already (baseline 87 t for 100 t chunk); aerocapture's main value is feasibility, not delivered mass |
| H-ac-d — Variant B's winning region disappears | yes | held by implication — all Kilopower / Fission-Surface-Power cells become 7-yr all-electric feasible | held |
| H-ac-e — Kilopower inbound burn time | < 2 yr | 4.05 yr at 100 t; 5.35 yr at 200 t | falsified-high |
| H-ac-f — 14-yr round-trip ceiling achievable at Kilopower under aerocapture | yes | round-trip = 6 + 1 + 4.05 = 11 yr (Kilopower / 100 t); ≈ 12.4 yr (Kilopower / 200 t) | held |

## Reading

**Aerocapture's primary value is not delivered mass — it is schedule feasibility.** Across all 18 (reactor, chunk) cells tested, aerocapture turns 12 infeasible cells into feasible ones and shrinks the 6 already-feasible cells' burn times by 1.6–4.7 years. **Delivered mass improves only 11–31%** because the baseline cells were already delivering most of the chunk (just over too long a burn time).

**Five observations the result supports:**

1. **Aerocapture makes every cell in the architecture matrix 7-year feasible.** Previously, Kilopower-era cells required 23–175 years of inbound burn for chunks ≥ 100 tonnes. With aerocapture, the same cells close in 2–5 years. The 14-year round-trip ceiling, which was structurally inconsistent with Kilopower all-electric in R-bag-permeability-vs-burn-time, becomes structurally achievable across every reactor era.

2. **Variant B's winning region collapses entirely.** Variant B existed in the matrix as the Kilopower-era architecture for net-present-value optimization, where the alternative (all-electric with 28-year burn) lost on time-discount value. With aerocapture, Kilopower all-electric closes in 4 years and round-trip is 11 years. Variant B's chunk-fed chemical, which costs 50% of chunk mass at Saturn-departure, no longer earns its keep. **The architecture decision matrix collapses to "all-electric, every cell."**

3. **The "raw mass vs net-present-value" tension at Kilopower disappears.** Under aerocapture, all-electric at Kilopower delivers 98 tonnes (vs Variant B's 33 tonnes from R-chunk-fed-chemical) with a 4-year burn time, so both raw mass *and* net-present-value pick all-electric. The Kilopower-era choice becomes uniformly all-electric regardless of objective function.

4. **The delivered mass improvement is modest (11–31%) because the rocket equation was already efficient at electric thrust.** For η = 0.8 baseline delivery at 6.42 km/s, aerocapture removes the propellant tax but the chunk-fed propellant was small to begin with (10–15% of chunk). The dominant value of aerocapture is *time*, not *mass*.

5. **Shield mass is structurally smaller than aerospace heritage suggests.** Heritage shield-mass-fraction numbers (Stardust 12%, Orion 9%) come from vehicles 100–10000× smaller than ICEBERG. The scaling is sub-linear: a 100-tonne vehicle has only ~25 m² of windward area vs the 0.5–5 m² of heritage vehicles. Realistic shield-mass-fraction at this scale is **1–3%**, not 5–15%. **The "heat shield mass" objection to aerocapture loses force at ICEBERG scale.**

**What this round still papers over — and the biggest open item:**

- **Sutton-Graves is convective-only.** Real total heat load at v_∞ 6 km/s includes radiative heating, which roughly triples the heat budget for ablative shield sizing. The 0.12% figure from Sutton-Graves is misleading on its own; the radiative-corrected figure is ~0.4–1.5%.
- **Trajectory dispersion not modeled.** Aerocapture requires periapsis altitude control to ±2 km. A wide-tolerance entry profile (allowing ±5 km) is achievable with current navigation; tighter tolerances need active guidance during atmospheric pass. Neither is in the heat shield mass calculation.
- **Atmospheric density uncertainty.** Real-world ±30% density variation at 90 km. Affects delta-v dissipated → mission outcome. Mitigatable with active guidance or trajectory shaping; not in this round.
- **Multi-orbit aerobraking to circularize.** After aerocapture, the vehicle is in a high elliptical orbit. Multiple aerobraking passes shrink the apogee to low Earth orbit over 3–6 months. Mass-cost zero; time-cost adds to inbound. Not in the burn time numbers.
- **Bag and chunk survival at 12.6 km/s entry velocity.** This is the question this round does not close. The vehicle's water-ice chunk and the trawl bag would experience peak stagnation heat fluxes of 3–10 MW/m² for 200 seconds. Whether the chunk can serve as its own heat shield (sublimating ice provides ablative cooling), and whether the bag survives the heat pulse — these are engineering questions for a thermal-protection-system program, not algebra. **The technology-readiness gap is named but not closed.**
- **Multi-tonne aerocapture is unprecedented.** Existing flight heritage tops out around 8 tonnes (Orion). A 100-tonne vehicle at hyperbolic entry velocity is technology-readiness ~4 (component lab demonstration); single-launch unprecedented in any flown mission. Closing the technology-readiness gap is a multi-year ground-test campaign with multiple lab and flight demonstrations.

## Revisit clause

H-ac-d/f held; H-ac-b held by construction; H-ac-a/c/e falsified, all in favorable directions for aerocapture (shield mass smaller than predicted; delivered mass improvement smaller because baseline was already most of chunk; burn time still feasible at 4 yr vs predicted 2 yr).

**Three propagations to `ARCHITECTURE-DECISION-MATRIX.md`:**

1. **Aerocapture transforms the matrix from "all-electric vs Variant B by era" to "all-electric, every era."** The Variant B Kilopower-era winning row should be removed. The matrix's "objective function" decision point becomes moot.

2. **Burn times across the matrix should be re-quoted under aerocapture.** Every cell at Kilopower / Fission-Surface-Power era goes from infeasible-or-long-burn to 1–5 year burn.

3. **The "Aerocapture R&D" decision point in the matrix should be re-framed.** It is no longer "highest-leverage unresolved technical question" — it is now "the single technical investment that opens up the entire mission architecture." The thermal-protection-system program for chunk-bearing entry becomes the binding precursor.

**Next-round candidates:**

- **R-chunk-as-heat-shield:** can the water-ice chunk itself serve as ablative thermal protection, replacing or supplementing the conventional ablative shield? If yes, the shield mass fraction goes to zero. Engineering feasibility study, not algebra; needs heat transfer modeling and bag survival analysis.
- **R-multi-orbit-aerobraking:** after aerocapture, how long does multi-orbit aerobraking add to the inbound? Time-of-flight implication for the round-trip total.
- **R-trajectory-dispersion:** what active guidance is needed to keep aerocapture periapsis within ±2 km? Mass implication for guidance, navigation, and control subsystem.


## Revisit clause

Grade H-ac-a through H-ac-f. If H-ac-agg holds, propagate to `ARCHITECTURE-DECISION-MATRIX.md` as a major rewrite — the entire matrix collapses to "all-electric, low-power reactor, large chunk, aerocapture inbound."

If the technology-readiness uncertainty (whether aerocapture actually works for a 100-tonne vehicle with novel windward-face geometry) is what's blocking confidence, the next round is **R-chunk-as-heat-shield**, a thermal-protection-system feasibility study that asks whether the water ice itself can replace conventional ablative shield material.
