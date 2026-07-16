# Water Propulsion R&D — Round 1: Landscape and ICEBERG-Constrained Isp Ceilings

**Status:** R1 — back-of-envelope. Numbers from training-data references; sources to be verified in R2.
**Mission context:** ICEBERG (Robot Rocket Science long-horizon thesis) — Earth ↔ Saturn B-ring, 50 t chunk return, ~13.5 yr round trip. See `ICEBERG-conops.md`, `ICEBERG-pitch.md` for the mission profile. **This R&D is greenfield**: RRS is not bound to any external company's heritage propulsion stack. Other companies' published water-prop work (Pale Blue, Penn State, Tethers Unlimited) is referenced only as open-literature data points for the tech landscape, not as procurement commitments or architectural constraints.

---

## 1. Reframe: "Highest Isp from water" is reactor-tiered, not a single number

The naive question "what's the highest Isp achievable with water?" has a misleading single-number answer (~10,000 s if you electrolyze and accelerate H⁺ through a high-voltage grid). For ICEBERG specifically, with a fixed cruise time and chunk mass, the binding constraint is electrical power, and the relationship between Isp and power for the inbound leg is **direct, not inverse**.

### The inbound-leg constraint

ICEBERG's inbound chunk-fed leg requires ΔV ≈ 4.2 km/s over ~7 years of cruise (per conops; LGA tour absorbs another 3 km/s at zero propellant cost). At 50% duty cycle over 7 years, available burn time t_burn ≈ 1.1×10⁸ s. Starting chunk mass m₀ ≈ 50 t.

For an electric thruster at total efficiency η ≈ 0.5:
- Required thrust ≈ m₀ × (ΔV/t_burn) × (1/Tsiolkovsky correction) ≈ 1.4–1.8 N (weak function of Isp)
- Jet power P_jet = ½ × F × v_e = ½ × F × g₀ × Isp
- Electrical power P_e = P_jet / η

This gives the **reactor-tier ↔ achievable-Isp mapping**:

| Reactor | P_e (kWe) | Implied Isp ceiling (this mission) | Delivery efficiency |
|---|---|---|---|
| Kilopower / KRUSTY | 1–10 | ~700–1000 s | 54–66% |
| Fission Surface Power | 40 | ~2000–2500 s | 81–85% |
| Sub-MW class | 100+ | ~5000 s | 92%+ |

**Higher Isp does not reduce power demand at the ICEBERG inbound leg — it raises it.** The often-cited "high Isp = low fuel = small spacecraft" framing applies when ΔV is fixed and trip time is unlimited. ICEBERG has the opposite constraint: trip time is fixed (mission timeline) and the question is how much chunk you can drag home.

---

## 2. Water propulsion technology landscape

### 2.1 Steam resistojet
- **Principle:** Heat liquid water → vapor through a resistive element → expand through nozzle.
- **Isp:** ~150–200 s demonstrated. Theoretical ceiling from Isp ≈ √(2·C_p·T₀)/g₀ with T_wall ≤ 1800 K → ~220 s.
- **Limit:** Wall temperature. Refractory metals fail above ~2000 K.
- **Status:** Flight heritage (HYDROS-M, AQUARIUS at lower Isp).
- **Verdict for ICEBERG:** Below MET-class options on Isp. Not competitive for the long cruise; possibly useful as RCS or contingency mode.

### 2.2 Water arcjet
- **Principle:** Arc discharge heats water directly, decoupling gas T from wall T.
- **Isp:** 250–350 s demonstrated for various propellants; water specifically harder due to electrode oxidation.
- **Limit:** Electrode erosion from oxidizing plume. Frozen-flow losses (dissociated species don't recombine in the nozzle).
- **Status:** Hydrazine arcjets have flight heritage; water arcjet is research-phase.
- **Verdict:** Marginal improvement over resistojet, big erosion problem. Skip.

### 2.3 Microwave Electrothermal Thruster (MET)
- **Principle:** Microwave couples energy into a free-floating plasma in water vapor. Plasma T can reach ~5000–10,000 K while wall T stays moderate.
- **Isp:** Open-literature water-MET reports **500–800 s**; theoretical with full dissociation and minimal frozen flow ~1000 s.
- **Limit:** Frozen-flow recombination in the nozzle. H/O/OH species don't fully recombine before exiting → energy lost.
- **Status:** Penn State (Micci, Bilén) demonstrated in research; some commercial water-MET stacks use it.
- **Verdict for ICEBERG:** Strong architectural fit (cargo can double as propellant tank — no electrolyzers or intermediate phase changes), with Isp caps at ~1000 s. Sufficient if power is limited to ~10 kWe; leaves performance on the table at higher power. RRS would need to either license/clone the architecture or develop in-house — both real options to evaluate.

### 2.4 Water ion thruster (Pale Blue PBIT-class)
- **Principle:** Electron-impact ionization of water vapor, electrostatic acceleration through gridded optics.
- **Isp:** Pale Blue / U-Tokyo (Koizumi) demo ~800–1500 s; theoretical ~3000 s.
- **Limit:** Grid sputter erosion from O⁺ (oxidizing plasma, hard problem). Cathode life from oxide layer formation on emitters.
- **Status:** Pale Blue Inc has flown water-resistojet versions; water-ion is research-to-early-product phase. Confidence on quoted Isp numbers is moderate — need to verify in R2 against actual published performance maps, not marketing.
- **Verdict for ICEBERG:** Top candidate for FSP-class era. ~2x delivery efficiency over MET if grid life closes.

### 2.5 Water Hall thruster
- **Principle:** Hall-effect crossed E×B acceleration of ionized water plasma.
- **Isp:** Water Hall research at Busek, MIT (Lozano group) reports 1000–1500 s; theoretical 2000+ s.
- **Limit:** Same oxidation problem as ion thruster, plus channel wall erosion from H/O/OH ion bombardment.
- **Status:** Active research. No flight heritage with water specifically.
- **Verdict:** Parallel candidate to water-ion at FSP power. Similar Isp ceiling, different failure modes.

### 2.6 Electrolyze → H₂/O₂ chemical thruster (Tethers HYDROS class)
- **Principle:** Electrolyze water on-board, store H₂ and O₂, burn in a small chemical thruster.
- **Isp:** ~310 s (HYDROS-C demonstrated); theoretical chemical ceiling ~450 s.
- **Limit:** Chemistry. This is a chemical rocket — Isp can't exceed H₂/O₂ combustion enthalpy.
- **Verdict for ICEBERG:** **Wrong tool entirely.** Chemical Isp ceiling is below water-MET. Only interesting where chemical thrust is needed (high-thrust burns, contingency). Not for cruise.

### 2.7 Electrolyze → H₂-fed electric (ion / Hall / MPD)
- **Principle:** Electrolyze water, dump O₂, accelerate H₂ in an electric thruster.
- **Isp:** H₂ is the highest-Isp propellant available to electric propulsion. Ion thrusters with H₂ have demonstrated 5000–10,000 s. MPD with H₂ has run 5000+ s.
- **Limit:**
  - H₂ storage (leak, tank mass) — see §3 below.
  - O₂ disposal — venting wastes 89% of harvested water mass.
  - Electrolyzer mass + power overhead (5–10 kWh per kg H₂ for PEM).
- **Status:** No flight precedent for water→electrolyze→H₂ ion thrust as an integrated system. Each component has heritage; integration doesn't.
- **Verdict:** **Highest practical Isp from water input.** But it inverts ICEBERG's architectural fit (cargo-as-tank no longer works; you need separate H₂ tankage that doesn't double as cargo).

### 2.8 Water MPD thruster
- **Principle:** Magnetoplasmadynamic acceleration of fully-ionized water plasma.
- **Isp:** MPD with H₂ or Li: 3000–5000 s. With water: limited research; ~2000–3000 s plausible.
- **Limit:** MW-class power required for efficient operation. Cathode life at high power.
- **Status:** Research only. Princeton EPPDyL, JPL legacy programs.
- **Verdict:** Only viable at sub-MW reactor class. Then competes with H₂-ion. Probably loses on η.

---

## 3. The electrolysis question, properly bounded

The user's specific question: *"if we electrolyze it there's a problem with hydrogen gas leaking, but what is the leak rate and can we electrolysize enough to make it worth it?"*

### 3.1 Leak rate (back-of-envelope)

H₂ permeation through 316 stainless steel at 300 K, with permeability Φ ≈ 10⁻⁹ mol/(m²·s·√Pa) (Sandia/Aceves data; needs verification in R2):

For a representative storage tank:
- 100 L volume, 0.5 m² wall area, 100 bar H₂ (10⁷ Pa internal)
- Flux = Φ × A × √P = 10⁻⁹ × 0.5 × √(10⁷) = 1.6 × 10⁻⁶ mol/s
- = 50 mol H₂/yr = **100 g H₂/yr**

Over a 13-year mission: ~1.3 kg lost. Inventory of H₂ on a sub-MW H₂-ion ICEBERG variant would be tens to hundreds of kg. **Loss fraction is <1% over the mission. Not the killer.**

A composite (Al-liner + CFRP) tank cuts permeation 10–100× further. Confidently below the noise floor.

### 3.2 The actual electrolysis killer: tank dry mass + O₂ waste

H₂ density at 100 bar, 300 K ≈ 8 kg/m³. Equivalent of 1 t H₂ requires 125 m³ tank at 100 bar. Composite tank mass at 0.1 tank-mass-fraction-per-kg-H₂ → 100 kg tank for 1 t H₂. Workable but not free.

**Bigger problem: O₂ disposal.** Water is 11% H by mass. Electrolyzing 1 t of water yields 110 kg H₂ and 890 kg O₂. **The O₂ either gets vented (89% of harvested water mass wasted), stored (large tank), or used (lower-Isp O₂-augmented thrust mode).**

For ICEBERG specifically, where cargo *is* the propellant on the return leg, naively venting O₂ is a deal-breaker: harvest 50 t of chunk, throw away 89% as O₂ for high-Isp H₂ thrust, delivered water drops by ~10×. Delivered cargo collapses.

**Possible escapes:**
- **Bi-mode propulsion:** water-MET for bulk cruise (consumes water directly, no waste); reserve H₂-electric for specific high-Isp maneuvers (Earth-arrival fine-trim).
- **O₂ as RCS or cold-gas thrust:** use the O₂ stream at low Isp for attitude/RCS, recovering some of the 89%.
- **O₂ as a secondary resistojet stream:** heat O₂ in a resistojet to recover ~200 s Isp from the O₂ mass fraction; combined mass-weighted Isp is somewhere between H₂-ion and the O₂-resistojet number.
- **Don't electrolyze on the return leg:** electrolyze only the small inventory used for outbound cruise; return leg uses MET on raw water. Lets H₂-ion be the outbound prop, water-MET be the return prop. Asymmetric architecture.

All four warrant their own back-of-envelope in R2.

### 3.3 Electrolysis power overhead

PEM electrolyzer specific energy: ~5–10 kWh/kg H₂ = 18–36 MJ/kg.
At Isp 5000 s for H₂-ion thruster with η = 0.7, jet energy per kg of H₂ = ½ × (5000 × 9.81)² = 1.2 GJ/kg. Electrical input ≈ 1.7 GJ/kg.
Electrolyzer overhead = 36 MJ / 1700 MJ = **2%** of total electric power. Negligible.

---

## 4. Output: required electrical power for each Isp choice

Power source treated as a free variable here. Output the **electrical power required at the thruster** to deliver ΔV = 4.2 km/s in t_burn = 1.1×10⁸ s (7 yr cruise × 50% duty), starting from m₀ = 50 t chunk-fed initial mass (ICEBERG inbound-leg parameters from the conops). The power-source decision falls out of the resulting P_e.

**Derivation (back-of-envelope):**
- Tsiolkovsky: m_p = m₀ · (1 − e^(−ΔV/v_e))
- Mass flow: ṁ = m_p / t_burn
- Thrust: F = ṁ · v_e
- Jet power: P_jet = ½ · F · v_e = ½ · ṁ · v_e²
- Electrical power: **P_e = P_jet / η_t**

Total efficiency η_t assumptions (electrical → jet, includes ionization, beam, divergence losses):
- η_t = 0.5 for MET / electrothermal
- η_t = 0.6 for mature ion/Hall (xenon-class)
- η_t = 0.4 for water-ion / water-Hall (oxidation, grid losses)
- η_t = 0.5 for electrolyze + H₂-ion chain (electrolyzer + thruster combined)

| Isp (s) | v_e (km/s) | m_p (kg) | Delivery eff. | F (N) | P_jet (kW) | η_t | **P_e (kWe)** | Tech candidate |
|---|---|---|---|---|---|---|---|---|
| 300 | 2.94 | 38,200 | 24% | 1.02 | 1.5 | 0.5 | **3.0** | Steam resistojet, water arcjet |
| 500 | 4.91 | 28,600 | 43% | 1.28 | 3.1 | 0.5 | **6.3** | Low-end water MET |
| 700 | 6.87 | 22,800 | 54% | 1.42 | 4.9 | 0.5 | **9.7** | Water MET (open-literature Isp) |
| 1000 | 9.81 | 17,000 | 66% | 1.52 | 7.4 | 0.5 | **14.9** | High-end water MET / low-power water ion |
| 1500 | 14.7 | 11,500 | 77% | 1.54 | 11.3 | 0.4 | **28.3** | Water ion (Pale Blue class) |
| 2000 | 19.6 | 8,830 | 82% | 1.57 | 15.4 | 0.4 | **38.6** | Water ion / water Hall |
| 3000 | 29.4 | 5,650 | 89% | 1.51 | 22.2 | 0.4 | **55.5** | Water ion at high V (erosion-limited) |
| 5000 | 49.1 | 3,400 | 93% | 1.52 | 37.2 | 0.5 | **74.4** | Electrolyze → H₂-ion |
| 10000 | 98.1 | 1,700 | 97% | 1.52 | 74.3 | 0.5 | **148.6** | H₂-ion at high voltage |

### Key reads from the table

1. **Water MET (~700 s) lands at ~10 kWe.** Kilopower-class.
2. **Doubling Isp 700 → 1500 s ≈ 3× the power bill** (10 → 30 kWe). Buys 14 percentage points more delivered chunk (54 → 77%).
3. **5× Isp (700 → 3500 s) ≈ 6× the power.** Delivers 89% vs 54%.
4. **H₂-ion at 5000 s ≈ 75 kWe.** Sub-MW class. Plus electrolyzer mass and the O₂-disposition problem (§3.2).
5. **Thrust is flat at ~1.5 N across the whole Isp range.** For fixed ΔV and fixed cruise time, F is approximately constant; what changes is v_e and m_p. P_e scales roughly linearly with Isp because P_e = ½·F·v_e/η_t.
6. **All numbers exclude housekeeping load** (avionics, comms, thermal, electrolyzer power). Add ~1–3 kWe overhead to anything below.

### How to use this table for the power-source conversation

Pick an Isp band → read off P_e → that defines the power source you need to procure.

| If procurable P_e is… | …Isp ceiling is | Implied power source |
|---|---|---|
| ~5 kWe | ~500 s | Multiple ASRGs/eMMRTGs (radioisotope), or small reactor |
| ~10 kWe | ~700–1000 s | Kilopower-class fission reactor (NASA/DOE partnership host) |
| ~30–40 kWe | ~1500–2000 s | FSP-class fission reactor (LM/Westinghouse/IX/BWXT designs) |
| ~75 kWe | ~5000 s | Sub-MW fission unit (no current program) |
| ~150 kWe | ~10,000 s | Approaches MW-class (DOE roadmap, 2040s) |
| Solar | n/a at Saturn | Solar dies past Mars (~1% Earth flux at 9 AU). Inner-system missions only. |

**Procurement reality check** (separate from physics): the US has no fission reactor flight heritage since SNAP-10A in 1965 (43 days, 500 W). Soviet RORSAT BES-5/TOPAZ flew ~30 times in the 60s–80s at 3–6 kWe, none operational today. Kilopower ground-tested 2018, never flown. FSP is Phase-1 paper-study (2022 awards to LM, Westinghouse, IX, BWXT). For RRS, the power-source line is a partnership with NASA STMD / DOE INL where they own the reactor and RRS owns the spacecraft — *not* a procurement. Treat as top-level program risk in R3.

### Caveats

- Thrust is back-of-envelope; real mission design with multi-arc trajectories gives a different number. Re-derive against the conops phase plan in R3.
- η_t values are estimates from training data, not measured. Water-ion η at ICEBERG-class operating points is poorly constrained.
- Duty cycle 50% is a guess; thermal management and autonomy may push it lower. Re-derive with verified duty-cycle in R2.

---

## 5. Open questions for R2 (higher fidelity)

1. **Water-MET Isp vs. power**: real performance map. Is 1000 s achievable at Kilopower (10 kWe) or does it need more? Get Micci/Bilén papers; check what η drops to at high Isp.
2. **Water-ion grid life with oxidizing plume**: actual lifetime numbers from Pale Blue / Koizumi. Is 7-year operation feasible or do we need redundant thrusters?
3. **Frozen-flow loss model for water MET**: what's the recombination efficiency in the nozzle? Sets the practical Isp ceiling.
4. **Two-mode architecture trade**: does adding a small H₂-ion / H₂-Hall mode for Earth-arrival trim pay off, or does the complexity wipe out the gain?
5. **Hydrogen storage at outer-planet thermal environment**: at 9 AU, ambient T is ~80 K — H₂ may be easier to store than at room temperature. Re-do leak calc at low T.
6. **O₂ disposition for electrolysis variants**: can O₂ be used at all? Cold-gas RCS? Resistojet-RCS? Sets whether electrolysis is 11% efficient or higher.

---

## 6. Source list (to verify in R2)

These are training-data references, not freshly cited:
- Micci & Bilén — water MET performance, Penn State.
- Tethers Unlimited — HYDROS-C / HYDROS-M flight data.
- Koizumi et al., U Tokyo — water ion thruster heritage (Pale Blue founders).
- Pale Blue Inc — published thruster performance.
- Aceves et al., Sandia — H₂ permeation through metals.
- Risha et al., Penn State — metal-water combustion (relevant if Mg/Al hybrid revisited).
- Jahn, *Physics of Electric Propulsion* — first-principles Isp ceilings.
- NASA Kilopower / KRUSTY 2018 ground test reports.
- NASA Fission Surface Power 2022 Phase 1 awards (LM, Westinghouse, IX, BWXT).
