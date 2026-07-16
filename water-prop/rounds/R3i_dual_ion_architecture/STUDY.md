# Round 3i — Dual-Ion Architecture (Hydrogen-Ion plus Oxygen-Ion from Electrolyzed Water)

**Question.** A dual-ion electric thruster fed by on-board water electrolysis — one ion engine for the hydrogen stream, one for the oxygen stream, both at the same grid voltage — uses 100 percent of the chunk mass as propellant (no oxygen waste). What is the mass-weighted specific impulse, the electrical power required for ICEBERG-class thrust, and the chunk-delivery fraction at the ICEBERG inbound delta-V? How does it compare to single-technology water options?

**Method.**
- Closed-form ion kinematics in `src/waterprop/propulsion/dual_ion.py`. For each ion species at grid voltage V: exhaust velocity v_e = sqrt(2 q V / m). Mass-weighted specific impulse Isp_avg = (f_H × v_H + f_O × v_O) / g_0, where f_H = 11.19% and f_O = 88.81% are the mass fractions of hydrogen and oxygen in water.
- Sweep grid voltage 100 to 10,000 volts. Compute thrust per kilowatt of electrical power assuming a single combined total electrical-to-jet efficiency of 0.4. Compute chunk-fed delivery fraction at the ICEBERG inbound delta-V of 4.2 km/s (recognizing this number is being revised upward by round 2's finding — see cross-learning).
- Two flavors: atomic hydrogen ion (H+) as the maximum-Isp case, and diatomic hydrogen ion (H2+) as the realistic case where the plasma source doesn't fully dissociate hydrogen.

**Validity caveats.**

This round is a **physics ceiling analysis only**, not a flight-design study. Major omissions:

1. **Grid life under pure oxygen-ion erosion**. Pure O+ at 1 kV beam velocity is the most chemically aggressive ion-thruster propellant in common use. Standard grid materials are vulnerable: molybdenum forms volatile molybdenum trioxide; carbon forms carbon dioxide; titanium forms titanium dioxide. **No flight-qualified material is known to survive long-duration pure O+ ion thruster operation.** This is the dominant risk for the architecture and is not modeled here.
2. **Flight heritage / Technology Readiness Level**. As an integrated system: TRL 2–3, no flight heritage. Component-level: water electrolysis in space at TRL 7–8 (HYDROS); hydrogen-ion gridded thrusters at TRL 3–4; oxygen-ion gridded thrusters at TRL 3. **Pale Blue's water radio-frequency ion thruster (round 1 finding) is at TRL 7–8 with in-orbit demonstration** — the heritage-competitive option for high-specific-impulse water propulsion today.
3. **Silicate dust in B-ring water**. The ~99% water-ice composition still leaves 0.1–0.5% non-icy material, mostly submicron silicate dust per Cassini Cosmic Dust Analyzer data. Dust contamination of an ion thruster grid or electrolyzer membrane is fatal over a 7-year mission. **Filtration is a hard requirement** that adds mass and complexity not in this model.
4. **Electrolyzer mass and power overhead**. Polymer-electrolyte-membrane electrolyzers run at 5–10 kilowatt-hours per kilogram of hydrogen produced (~0.5–1 kilowatt-hour per kilogram of water). At the kilogram-per-day water flow this model implies, electrolyzer electrical overhead is 50–100 watts — negligible against the 100–300 kilowatt thrust budget. Electrolyzer dry mass is non-trivial but not included in this delivery-fraction model.
5. **Beam neutralization, ionization energy, and other small efficiency factors** are folded into the scalar `efficiency_total = 0.4` parameter. Real total efficiency may be 0.3–0.5 depending on the operating point and could be a meaningful sensitivity.
6. **Reactor dry mass overhead** (risk E08 from round 1). At Kilopower-class specific power of 2.5–6.5 watts per kilogram, a 100-kilowatt-electrical reactor weighs 15–40 tons. At 275 kilowatts (the 1 kilovolt operating point for this round): 42–110 tons — comparable to or larger than the chunk itself. **This is the load-bearing constraint for whether the architecture closes at all for a 50-ton chunk.**

**Result.** See `results/dual_ion_comparison.png`, `results/dual_ion_sweep_h_plus.csv`, `results/dual_ion_sweep_h2_plus.csv`.

| Grid voltage (V) | Isp_avg (s) | Thrust per kilowatt electrical (mN/kW) | Electrical kilowatts for 1.5 N thrust | Chunk delivery at 4.2 km/s (atomic hydrogen ion case) |
|---|---|---|---|---|
| 100 | 4,724 | 17.3 | 87 | 91.3% |
| 300 | 8,182 | 10.0 | 150 | 94.9% |
| 1,000 | 14,938 | 5.5 | **275** | **97.2%** |
| 3,000 | 25,873 | 3.2 | 476 | 98.4% |
| 10,000 | 47,238 | 1.7 | 869 | 99.1% |

For the diatomic hydrogen ion case the specific impulse drops by sqrt(2) for the hydrogen stream; mass-weighted Isp values are 5–10% lower. Chunk delivery is essentially unchanged (high-Isp regime is asymptotic).

**Comparison against single-technology baselines:**

| Architecture | Isp (s) | Chunk delivery at 4.2 km/s | Power (kWe) | Technology Readiness Level | Reactor mass at 5 W/kg (tons) |
|---|---|---|---|---|---|
| Microwave electrothermal (round 0) | 600 | 49% | 10 | 4–5 (Penn State research) | 2 |
| Pale Blue water radio-frequency ion (round 1) | 2,000 | 81% | 37 | 7–8 (flight) | 7 |
| Dual-ion 100 V | 4,724 | 91% | 87 | 2–3 (concept) | 17 |
| Dual-ion 1 kV | 14,938 | 97% | 275 | 2–3 (concept) | 55 |
| Dual-ion 10 kV | 47,238 | 99% | 869 | 2 (research) | 174 |

**Reading.**

The mass-weighted specific impulse advantage of dual-ion is real and substantial — the user's intuition was correct. At 1 kV grid voltage, the architecture delivers 97% of the chunk to low Earth orbit compared to 49% for microwave electrothermal: a **1.98× improvement in delivered cargo**. Even at the much lower 100 V operating point, dual-ion delivers 91% vs Pale Blue's 81% (a 1.12× improvement).

**But the architecture is power-hungry and technology-immature:**

- At 1 kV, the reactor required (275 kilowatts electrical, ~55 tons dry mass) is bigger than a 50-ton chunk. **For chunks below ~100 tons, the reactor mass overhead dominates the trade and the architecture loses on a delivered-mass basis** — even though it wins on chunk-delivery percentage.
- At 100 V, the reactor (87 kilowatts, ~17 tons) is a meaningful but tolerable fraction of a 50-ton chunk. **This operating point is the dual-ion sweet spot for ICEBERG-Kilopower-era missions.** It still requires a Fission Surface Power-class reactor (40 kWe ground-tested only as Phase 1 study) at minimum, not Kilopower.
- Pure oxygen-ion grid life is the dominant risk. No flight-qualified material is known to survive 7-year operation under pure O+ erosion. A cluster-redundancy architecture (multiple thrusters, swap-out as they fail) might close the mission life requirement, but at additional mass cost.
- TRL 2–3 means a multi-year development program to reach flight qualification. **Not viable for a near-term mission.** Pale Blue's water radio-frequency ion at TRL 7–8 is the heritage-competitive option today.

**The architecture is not dominated, but it's only competitive in two regimes:**
1. **Megawatt-class power era** (sub-MW reactors or larger). At 1 kV grid voltage with cheap power, dual-ion wins on every metric except heritage.
2. **Large chunks (above 200 tons)** where the reactor mass overhead is small relative to the chunk. The dual-ion power-overhead penalty disappears.

For the Kilopower era and chunks in the 50-ton range, **Pale Blue's water radio-frequency ion (round 1) likely beats dual-ion** on a delivered-mass basis despite the lower specific impulse, because the reactor mass overhead and the technology-readiness premium dominate.

**Revisit.**

This was a fresh pre-registration round, not a Revisit of an existing hypothesis. But the user's framing intuition ("oxygen is heavier than hydrogen; ionize and throw it out") is precisely what the mass-weighted specific impulse math says: at the same grid voltage, you trade peak specific impulse for mass utilization, and the trade pays for chunk-fed propulsion where every kilogram of cargo not consumed as propellant is delivered cargo.

The numbers exceed what I would have estimated by hand without the model. Specifically the 97% chunk-delivery figure at 1 kV is striking — but the corresponding 275 kilowatts of electrical power is megawatt-class reactor territory, far beyond any current program.

**Cross-learning.**

- **Positive for round R-synthesis** (final architecture ranking): dual-ion enters the candidate set as a high-power, high-Isp option that wins on delivered-cargo for chunks above ~200 tons or in eras with megawatt-class reactors. Below those thresholds it loses to Pale Blue-class water ion on a heritage and reactor-mass basis.
- **Positive for round R6 (power vs Isp trade across reactor classes)**: dual-ion shifts the Pareto frontier at sub-megawatt and megawatt power levels significantly. Update the trade table.
- **Negative for the original "highest specific impulse always wins" framing**. The reactor mass at high specific impulse can dominate the trade for small chunks. This is risk E08 (uncharacterized reactor mass overhead) coming into the math.
- **Methodology issue flagged for the next round on this candidate**: grid life under pure O+ erosion needs a sputter-yield and chemical-erosion model. Without that number, the 97% delivery figure is upper-bound only.
- **Methodology issue flagged for R-mid (mid-cycle audit)**: should add a "salt-doped water field-emission electric propulsion" candidate to the trade study. B-ring water is not pure distilled water — it has trace salts (from analogy to Enceladus's plumes per Hsu et al. 2015), so a field-emission/colloid thruster architecture may be physically viable. Predicted specific impulse range 1500–5000 seconds for ionic-liquid colloid analogs; needs its own round.
- **Cross-link to round 2**: the inbound delta-V baseline used here (4.2 km/s) is being revised upward by round 2's finding (lunar gravity assist only delivers ~2 km/s of braking at v∞ = 6 km/s, not the 3 km/s claimed). Real inbound delta-V is more like 5.2 km/s. Re-run all delivery numbers with the revised value in a later pass; the qualitative conclusions hold but the absolute numbers shift by a few percentage points.
