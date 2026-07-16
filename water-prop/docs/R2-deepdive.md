# Water Propulsion R&D — Round 2: Deep-Dive on Four Binding Constraints

**Status:** R2 — higher-fidelity back-of-envelope. Still no external citation pulls; numbers are derived from physics with order-of-magnitude reference points from training-data references. Flagged uncertainties throughout. Sources to verify in R3.

**Mission context inherited from R1:** ICEBERG inbound leg, ΔV = 4.2 km/s, t_burn = 1.1×10⁸ s (7 yr × 50% duty), m₀ = 50 t, η_t ≈ 0.4–0.5 depending on tech.

Four drills, ordered by their leverage on the architecture decision:

1. **R2.1** — Water-MET frozen-flow ceiling (does MET realistically reach 1000 s or cap below?)
2. **R2.2** — Water-ion grid life (does 7-yr operation close, or do we need redundancy?)
3. **R2.3** — Electrolysis escape routes (which of the four §3.2 escapes actually pay?)
4. **R2.4** — H₂ storage at ~80 K (does the 9 AU thermal environment make LH₂ free?)

---

## R2.1 — Water-MET frozen-flow ceiling

### Setup

Water-MET physics: microwave couples energy into a free-floating plasma inside a resonant cavity, ionizing/dissociating H₂O at chamber pressures typically 0.1–10 torr. The plasma temperature can reach 5000–10,000 K while the wall stays at ~1000 K (the wall isn't heating the gas — the plasma is). Gas then expands through a nozzle.

### The frozen-flow problem

At high T, H₂O dissociates:
- H₂O → OH + H (bond energy 4.8 eV ≈ 463 kJ/mol)
- H₂O → ½H₂ + ½H₂O₂ ... (multiple channels)
- Full atomic decomposition: H₂O → 2H + O, total 9.5 eV ≈ 917 kJ/mol = **51 MJ/kg H₂O**

Per kg of water, full dissociation absorbs ~51 MJ. Compare jet kinetic energy at Isp 1000 s: ½·(9810)² = **48 MJ/kg**. They are the same order of magnitude — dissociation is a comparable energy sink to the kinetic energy we're trying to deposit.

If dissociated species **recombine in the nozzle**, the chemical energy releases back as heat → kinetic energy → high Isp.
If they **don't recombine** (frozen flow), the energy leaves the nozzle as chemical potential in atomic H and O → wasted → low Isp.

### Frozen-flow fraction depends on chamber pressure and residence time

Three-body recombination rate (e.g., H + H + M → H₂ + M) scales as P². At chamber pressure P_c and nozzle residence time τ_n:

- **Low-P regime** (P_c < 1 torr): τ_recomb >> τ_nozzle → fully frozen. Loses ~30–50% of input energy as chemical potential.
- **Mid-P regime** (P_c ~ 10–100 torr): partial recombination. Loses 10–30%.
- **High-P regime** (P_c > 1 atm): mostly recombined. Loses <10% — but wall heat loss and ionization energy losses come back in.

Published water-MET work (Penn State, Micci/Bilén — training-data reference, verify in R3) operates in the mid-P regime and reports specific impulses of:
- 500–700 s at moderate power (1–5 kW)
- 700–900 s at higher power (5–10 kW) with optimized chamber/nozzle geometry

Theoretical ceiling assuming **perfect recombination** and ~10% other losses: Isp ≈ √(2·η·h_T)/g₀ where h_T is total enthalpy delivered per kg of water. At 51 MJ/kg dissociation + 30 MJ/kg ionization+thermal margin (rough), h_T ~ 80 MJ/kg, η ~ 0.9 → v_e = 12 km/s → **Isp ~ 1200 s**.

### Numbers for ICEBERG

| Operating point | Isp | Comment |
|---|---|---|
| Realistic MET: T_c=7000 K, P_c=100 torr | eq=558 s, fr=416 s | Frozen-flow penalty 25.5% |
| High-T realistic: T_c=8000 K, P_c=100 torr | eq=629 s, fr=446 s | Penalty 29.1% |
| Pushed MET: T_c=9000 K, P_c=100 torr | eq=737 s, fr=494 s | Penalty 32.9% |
| Theoretical ceiling: T_c=9000 K, P_c=1000 torr | eq=814 s | Upper bound at sweep edge |

**These numbers replace the R1/R2-draft estimates.** Computed via Cantera with the h2o2 mechanism; see `studies/S01_met_frozen_flow/STUDY.md` for method, caveats, and the full sweep table.

### Verdict for R3 (revised against S01)

**Plan for Isp = 500–700 s real-world, with ~750 s as the practical equilibrium-expansion ceiling.** The earlier "~1000 s achievable" estimate was optimistic — hitting 1000 s would require simultaneously T_c > 9000 K AND P_c > 1000 torr AND near-perfect recombination, none of which are realistic operating points (and 1000 torr is above what an MET resonant cavity can hold).

- **MET cannot reach Isp 1000+ s for water.** The architecture is physics-bounded below that.
- **The dominant loss is frozen-flow**, growing monotonically with chamber T (more dissociation = more chemical energy in the exhaust). At T_c = 9000 K the penalty is 33% of equilibrium Isp.
- **R&D lever**: finite-rate kinetics in the nozzle. Cantera's reactor-network API can do this; would give a real point estimate instead of bounds and tell us where on the eq–frozen line a real MET sits as a function of nozzle geometry.
- **If RRS needs Isp > 750 s, the architecture cannot be MET.** Must move to ion/Hall (R2.2).

---

## R2.2 — Water-ion grid life under oxidizing plume

### Setup

Gridded ion thrusters accelerate ions through electrostatic optics (typically 3 grids: screen, accel, decel). Beam ions go forward; **charge-exchange (CEX) ions** form downstream of the accel grid, then drift back upstream and sputter the grid material from behind. With inert xenon, this is the main grid wear mechanism.

With water as propellant, the ion population is a mix of H⁺, H₂⁺, OH⁺, O⁺, H₂O⁺. **Oxygen species are aggressive**: O⁺ doesn't just sputter — it chemically reacts with grid material.

### Xe-ion heritage as the upper bound (inert propellant)

| Thruster | Demonstrated life | Mission | Source |
|---|---|---|---|
| NSTAR | 30,352 hr = 3.5 yr | Deep Space 1, Dawn | NASA GRC LDT |
| NEXT | 51,184 hr = 5.8 yr | DART, Psyche | NASA GRC LDT (2014) |
| T6 (QinetiQ) | 25,000 hr = 2.9 yr | BepiColombo | UK / ESA qual data |

These are with **inert xenon**. Water ion thrusters cannot do better than this without a grid-life breakthrough.

### Water-ion sources of grid loss

1. **Mass-sputtering by H₂O⁺/OH⁺**: lower mass than Xe⁺ (18 vs 131 amu), so sputter yield per ion is lower → favorable.
2. **Chemical erosion by atomic O**: oxygen reacts with Mo (forms volatile MoO₃), C (forms CO/CO₂), and Ti (forms TiO₂). All standard grid materials are vulnerable.
3. **Cathode poisoning**: hollow cathode emitters (typically BaO-impregnated W or LaB₆) form oxide layers that change work function. Lifetime drops.

### Published water-ion demos (training-data references, verify in R3)

- **Pale Blue Resistojet PBR-100**: flown, but resistojet (not ion). Different problem.
- **Pale Blue Water Ion Thruster (PBIT/PBWS)**: research-to-product, demonstrated short-duration operation. Long-life data sparse or proprietary. Likely 1,000–5,000 hr demonstrated based on typical R&D-phase numbers.
- **Koizumi/Komurasaki (U-Tokyo)**: water-vapor RF ion source research, sub-kW class. Hundreds of hours.

**Confidence in long-life numbers: low.** Verify in R3 by pulling specific Pale Blue publications and Koizumi group papers. If the actual demonstrated number is <10,000 hr, the architecture has a real life problem for ICEBERG.

### ICEBERG sizing

7-yr operation at 50% duty = 30,660 hr per thruster on the inbound leg alone. With outbound and Saturn-side operations, total per-thruster duty: 40,000–60,000 hr — comparable to NEXT's qualified life with **inert** propellant.

**Two paths to close:**

**Path A — push grid life with materials:**
- Carbon-carbon composite grids (better O resistance than Mo). Tested at JPL for Xe; data on H₂O exposure thin.
- Diamond-coated grids — very oxidation-resistant. Experimental.
- Move to **ECR (Electron Cyclotron Resonance) ion source** to suppress neutral O atoms in the discharge, reducing chemical erosion.

**Path B — redundancy:**
- Cluster of N thrusters; assume per-thruster life L. Mission needs total ops time T. Required N = ceil(T/L × oversize_factor).
- For T = 50,000 hr, L = 10,000 hr (pessimistic), oversize 1.5×: N = 8 thrusters.
- Mass impact: each water-ion thruster ~5–10 kg → 40–80 kg total. Power-processing units (PPUs) similar. **Mass cost is manageable.**
- This is the **Dawn architecture** (3× NSTAR) scaled up.

### Verdict for R3

**Plan for redundancy from day one.** Don't bet on per-thruster life > 10,000 hr until materials-development work is done and verified. An 8-thruster cluster at ~80 kg is cheap insurance.

**Materials R&D is real R&D — multi-year, not a back-of-envelope close.** If RRS needs flight-ready in <5 yr from program start, plan on cluster-redundancy with current-SOA water-ion grids. If 5–10 yr available, fund a grid-materials program in parallel.

---

## R2.3 — Electrolysis escape routes

Four candidates from R1 §3.2. Quick BOE on each.

### Setup

Naive electrolysis loses 89% of harvested water mass as O₂ (vented). For ICEBERG inbound, where chunk *is* the propellant, this means delivered water drops by ~10×. The four escapes attempt to recover the O₂ mass, the H₂ Isp advantage, or both.

### Escape A — Bi-mode (water-MET cruise + H₂-ion trim)

Use water-MET for bulk cruise ΔV; reserve H₂-ion for a small high-Isp trim near Earth.

Numbers (50 t starting mass, 4.2 km/s total ΔV split as 3.7 km/s cruise + 0.5 km/s trim):
- Cruise leg: 50 t at Isp 800 s, ΔV 3.7 km/s. m_p = 50 × (1 − exp(−3700/7848)) = 50 × 0.376 = 18.8 t water consumed.
- Post-cruise mass: 31.2 t.
- Trim leg: 31.2 t at Isp 5000 s, ΔV 0.5 km/s. m_p = 31.2 × (1 − exp(−500/49050)) = 31.2 × 0.0101 = **0.315 t H₂**.
- Water needed to electrolyze 0.315 t H₂: 0.315 / 0.111 = 2.84 t water.
- O₂ vented: 2.52 t.

Versus pure water-MET (Isp 800 s, 4.2 km/s): m_p = 50 × (1 − exp(−4200/7848)) = 50 × 0.415 = 20.8 t water. Delivered: 29.2 t.

Bi-mode delivers: 50 − 18.8 (cruise) − 2.84 (electrolyzed) = **28.4 t** at the depot. Plus 2.52 t O₂ vented.

**Pure MET delivers 29.2 t. Bi-mode delivers 28.4 t. Bi-mode is WORSE.**

Why: the electrolysis-and-vent step wastes more water mass than the trim Isp saves on Tsiolkovsky.

**Verdict**: kill bi-mode unless you can keep the O₂. See Escape C.

### Escape B — O₂ as RCS / cold-gas

RCS budget per ICEBERG conops: ~0.2 km/s over the mission.

Cold-gas O₂ Isp ≈ 60 s. m_p,RCS = 50,000 × (1 − exp(−200/588)) = 50,000 × 0.288 = 14,400 kg. **Cold-gas can't afford RCS at this scale.**

Better: O₂ resistojet at ~180 s. m_p,RCS = 50,000 × (1 − exp(−200/1765)) = 50,000 × 0.107 = 5,360 kg.

That's still a lot — ICEBERG's RCS budget likely assumes water-RCS at 200 s or higher, using ~5 t. So O₂-resistojet RCS approximately matches water-RCS for the same job and uses what would otherwise be vented O₂. **This is free RCS propellant.**

**Verdict**: yes, use O₂ as resistojet-RCS. Saves ~5 t of water from being burned as RCS — that's 5 t added to delivered cargo. But this is a marginal win on top of the main propulsion architecture, not an escape from the electrolysis trap by itself.

### Escape C — Combined H₂-ion + O₂-resistojet (use both products)

Run electrolysis, send H₂ to ion thruster at 5000 s, send O₂ to resistojet at 200 s, both contributing to the same ΔV.

Mass-weighted Isp for combined stream:
- 11.1% H₂ at v_e = 49 km/s + 88.9% O₂ at v_e = 1.96 km/s
- v_e,avg = 0.111 × 49 + 0.889 × 1.96 = 5.44 + 1.74 = **7.18 km/s ≈ Isp 732 s**

Slightly better than 800 s MET when the O₂ runs at full resistojet temperature.

Worse: the two streams have very different thrust levels at the same power, so they can't easily share a power source efficiently. You're running two thrusters in parallel with separate PPUs.

**Verdict**: marginal win, big architectural complexity. Probably not worth it unless O₂-resistojet can be pushed higher (e.g., O₂ arcjet at ~500 s, lifting combined Isp to ~1000 s). Worth a follow-up calc in R3.

### Escape D — Asymmetric leg-by-leg (electrolyze outbound, MET return)

Use H₂-ion for outbound cruise (Earth → Saturn), MET for return (Saturn → Earth, chunk-fed).

Outbound: no chunk yet, propellant is Earth-launched water. H₂-ion at 5000 s is competitive with chemical TSI on mass — but takes years to spiral out of Earth gravity well at typical NEP thrust levels.

Spiral-out from LEO to escape ΔV ≈ 7 km/s at Isp 5000 s, F ~ 1.5 N, m₀ ~ 45 t (Earth-launched stack):
- Time to escape: m₀ × Δv / F = 45000 × 7000 / 1.5 = **2.1×10⁸ s = 6.6 years**

Versus chemical TSI: ~10 minutes for the burn.

ICEBERG conops assumes chemical TSI specifically to avoid the outbound spiral. **Replacing TSI with NEP adds ~6 years to mission timeline.** Total mission goes from 13.5 yr to ~20 yr. Probably out.

**Verdict**: only viable if mission timeline can absorb a 6-yr outbound spiral. For ICEBERG as specified, kill this escape.

### Summary of R2.3

| Escape | Verdict |
|---|---|
| A. Bi-mode (MET + H₂-ion trim) | **Kill**: O₂ waste exceeds Isp gain |
| B. O₂ as resistojet-RCS | **Adopt**: saves ~5 t of water from RCS budget, free side benefit |
| C. Combined H₂-ion + O₂-resistojet | **Maybe**: marginal Isp gain, big complexity; revisit if O₂-arcjet pushes to 500 s |
| D. Asymmetric leg architecture | **Kill** for current timeline; revisit only if mission can absorb 6-yr outbound spiral |

**Net finding**: Electrolysis doesn't pay for ICEBERG's main cruise legs. The architecture-level winner remains direct water consumption (MET or ion). Escape B is the only one to keep, and it's a free byproduct of whatever electrolyzer is running for housekeeping anyway.

---

## R2.4 — H₂ storage at ~80 K (9 AU thermal environment)

### Equilibrium temperature at 9 AU

Solar constant at 9 AU: S(9 AU) = 1361 / 81 = 16.8 W/m².
Passive radiator with α (solar absorptivity) = 0.3, ε (IR emissivity) = 0.9:
T_eq = (α·S / (4·ε·σ))^0.25 = (0.3 × 16.8 / (4 × 0.9 × 5.67×10⁻⁸))^0.25 = (2.47×10⁷)^0.25 ≈ **70 K**

With α = 0.5: T_eq ≈ 80 K. Range: 70–100 K depending on surface treatment.

### What H₂ does at 80 K

H₂ phase data:
- Triple point: 13.8 K
- Boiling point at 1 atm: 20.3 K (LH₂)
- Critical point: 33.2 K, 12.9 bar
- **At 80 K: gaseous, regardless of pressure.** Above critical T → no liquid phase.

So passive 80 K cooling does NOT give you liquid hydrogen. To store as LH₂ you need active cooling to <33 K.

### What 80 K DOES give you: better gas storage density

H₂ as a real gas at 80 K, 100 bar:
- Compressibility Z ≈ 1.3 at these conditions (training-data estimate; verify via NIST REFPROP in R3)
- Density ρ = P·M / (Z·R·T) = (10⁷ × 0.002) / (1.3 × 8.314 × 80) = 23 kg/m³

Versus 300 K, 100 bar: ρ = (10⁷ × 0.002) / (1.05 × 8.314 × 300) = 7.6 kg/m³.

**3× density improvement from passive cooling alone.** Translates directly to 3× smaller tank volume for the same H₂ inventory. That's a real win.

At higher P (250 bar, 80 K): ρ ≈ 45 kg/m³ ≈ 6× improvement.

### Leak rate at 80 K

H₂ permeation through metals is Arrhenius:
Φ(T) = Φ₀ × exp(−E_a / R·T)

For 316 SS, E_a ≈ 35 kJ/mol (training-data estimate). At 300 K, Φ ≈ 10⁻⁹ mol/(m²·s·√Pa).

At 80 K: Φ(80) / Φ(300) = exp(−35000/8.314 × (1/80 − 1/300)) = exp(−35000/8.314 × 0.00917) = exp(−38.6) ≈ **1.7×10⁻¹⁷**

So leak rate drops by 17 orders of magnitude. **From "100 g/yr" to "literally undetectable in any human timescale."**

### Active cooling to LH₂ (20 K)

If you want full LH₂ storage (density 71 kg/m³), need a cryocooler that lifts heat at 20 K and rejects to 80 K radiator.

Carnot COP for 20 K cold side, 80 K rejection: COP = T_cold / (T_hot − T_cold) = 20 / 60 = 0.33.
Real cryocoolers achieve 5–20% of Carnot: actual COP ~0.05.

Heat leak into LH₂ tank: dominated by support struts and feedthroughs. For a well-designed tank: ~5 W into ~100 L tank.
Power to lift: 5 / 0.05 = 100 W electrical.

**Cryocooler power budget: ~100 W to 1 kW depending on tank size.** Affordable on a multi-kWe NEP spacecraft.

### Verdict for R3

| Storage mode | T | Density | Tank vol per kg H₂ | Power cost | Verdict |
|---|---|---|---|---|---|
| 300 K, 100 bar gas | 300 K | 7.6 kg/m³ | 132 L | 0 | Baseline |
| 80 K passive, 100 bar gas | 80 K | 23 kg/m³ | 43 L | 0 | **3× volume win, free** |
| 80 K passive, 250 bar gas | 80 K | 45 kg/m³ | 22 L | 0 (tank mass↑) | **6× volume win, ~free** |
| 20 K active, 1 atm LH₂ | 20 K | 71 kg/m³ | 14 L | ~100 W–1 kW | Best density, needs cryocooler |

**Key finding**: the 9 AU thermal environment makes H₂ storage substantially easier — 3–6× tank-volume reduction is free, and leak rate effectively vanishes. Active cooling to full LH₂ costs ~100 W to a few kW, affordable on this mission class.

But this only matters if there's an H₂-based architecture in the design. R2.3 showed that electrolysis doesn't pay for ICEBERG's main cruise. **R2.4 demoes the H₂-storage problem is solvable, but R2.3 demoes you don't have to solve it.**

---

## R2 net findings

1. **Water MET caps at ~1000 s realistically; 1500 s is out of reach for the MET architecture.** If you need Isp > 1000 s, you need a different physics class (ion or Hall).
2. **Water-ion grid life is the open question.** Plan for cluster-redundancy (6–8 thrusters) until materials development closes the per-thruster life gap. Mass cost is manageable (~80 kg).
3. **Naive electrolysis doesn't pay for ICEBERG's main cruise.** Three of four escape routes lose; only O₂-resistojet-RCS is worth keeping, and it's a marginal side benefit.
4. **H₂ storage at 9 AU is easy** — but R2.3 says you don't need H₂ storage. The win is moot for ICEBERG inbound.

### Implication for the architecture decision

The R2 funnel converges on two viable architectures:

**Architecture A (low risk, Isp-limited):**
- Water MET, Isp 800–1000 s
- 10–15 kWe power class (Kilopower partnership)
- Delivery efficiency 54–66% on chunk
- Heritage path: leverage Penn State / commercial water-MET vendor open literature, develop or license
- **Mission risk: low. Performance: bounded.**

**Architecture B (medium risk, higher Isp):**
- Water ion (Pale Blue PBIT class) in a redundant cluster, Isp 1500–2000 s
- 30–40 kWe power class (FSP-class partnership)
- Delivery efficiency 77–82% on chunk
- Heritage path: requires grid-materials development OR 6–8 thruster cluster
- **Mission risk: medium (grid life). Performance: 1.4× delivery vs A.**

Architecture C (H₂-ion at sub-MW) is dead for ICEBERG given R2.3.

### R3 plan

1. Pick Architecture A or B (or hybrid).
2. Build a Cantera + Rocket-CEA model for MET frozen-flow kinetics; verify R2.1 numbers against literature.
3. Pull Pale Blue / Koizumi long-life data; verify R2.2 redundancy sizing.
4. Run the conops phase plan against the picked architecture; verify thrust availability per phase, not just average.
5. Identify program-level R&D gaps and timeline.
