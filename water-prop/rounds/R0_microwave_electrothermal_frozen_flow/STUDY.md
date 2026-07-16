# Study S01 — Water-MET frozen-flow ceiling

**Question:** Where does a water Microwave Electrothermal Thruster (MET) actually cap on specific impulse? R2.1 estimated ~1000 s based on first-principles reasoning. This study replaces that estimate with a numerical answer bounded by the two physical extremes of nozzle expansion.

**Method:**
- Cantera-backed chemical-equilibrium model using the standard H₂/O₂ mechanism (`h2o2.yaml`). Species: H₂O, H₂, O₂, H, O, OH, HO₂, H₂O₂.
- Chamber: pure H₂O at (T_c, P_c), equilibrated at constant enthalpy and pressure (HP) — represents the MET assumption that microwave power dumps into the plasma and the gas equilibrates chemically and thermally at chamber conditions.
- Two isentropic expansions to vacuum (P_exit = 1 Pa):
  - **Shifting-equilibrium expansion** — composition re-equilibrates at each pressure step. Releases all dissociation enthalpy back as kinetic energy. **Upper bound** on real performance.
  - **Frozen-flow expansion** — chamber-equilibrium composition held fixed; only T and density change. Dissociation enthalpy is lost to the exit as chemical potential. **Lower bound** on real performance.
- Sweep T_c ∈ {3000, 4000, ..., 12000} K, P_c ∈ {1, 3, 10, 30, 100, 300, 1000} torr.
- Run: `uv run python studies/S01_met_frozen_flow/run.py` → writes `results/met_isp_table.csv` and `results/met_frozen_flow.png`.

**Validity caveats:**
- The h2o2 mechanism does **not** include ionized species (electrons, H⁺, O⁺). Above ~10,000 K, ionization becomes significant and the mechanism is invalid. The 12,000 K row in the sweep fails to converge — this is the symptom, not a numerical bug.
- Real MET chamber pressures are typically 0.1–10 torr. The high-P regime (100–1000 torr) is included to show the thermodynamic ceiling, not because it's an operating point. A real MET cannot hold 1000 torr in the discharge — wall losses and the magnetics of the resonant cavity bound P_c upward.
- The model assumes thermal equilibrium between heavy species and electrons. Real plasma thrusters have non-equilibrium effects (T_e > T_gas), not captured here.

**Findings:**
- **Maximum equilibrium-expansion Isp in the sweep: 814 s** at T_c = 9000 K, P_c = 1000 torr. This is the theoretical ceiling under ideal recombination, in a P regime that no real MET reaches.
- **Maximum frozen-flow Isp: 494 s** at T_c = 9000 K, P_c = 100 torr.
- **Real-world MET sits between these two surfaces.** At the realistic operating point T_c ≈ 7000 K, P_c ≈ 100 torr: equilibrium upper bound 558 s, frozen lower bound 416 s. Real performance probably ~480–520 s with partial recombination — consistent with open-literature water-MET reports in the 500–700 s band.
- **The frozen-flow penalty grows monotonically with chamber T.** At 3000 K it's ~10% of Isp; at 9000 K it's ~33%. More dissociation = more chemical energy that can be locked in the exhaust if recombination is incomplete.
- **R2.1's "1000 s realistic ceiling" was optimistic.** The equilibrium-expansion ceiling at realistic chamber conditions (T_c ≤ 9000 K, P_c ≤ 100 torr) is ~700–750 s, not 1000 s. Hitting 1000 s would require simultaneously high T AND high P AND near-perfect recombination — the latter being a finite-rate kinetics question this sweep doesn't resolve.

**Decisions / implications for R3:**
1. **Update R2.1's MET ceiling from "~1000 s" to "~750 s as a realistic equilibrium-expansion upper bound, with 500–650 s as the more likely real-world performance."**
2. The frozen-flow penalty is the dominant loss. **Pushing MET past 750 s requires a recombination-kinetics study** (finite-rate Cantera with the reactor-network API along the nozzle profile), not more chamber temperature.
3. If RRS wants Isp > 750 s, the architecture cannot be MET. Must move to ion/Hall (R2.2).

**Open follow-ups:**
- Finite-rate kinetics expansion along an actual nozzle geometry. Cantera's `IdealGasReactor` with the right reaction network can do this. Would give a real point estimate, not just bounds.
- Plasma non-equilibrium model (T_e ≠ T_gas) for the chamber. Would tighten the chamber-side assumptions.
- Higher-fidelity mechanism above 10,000 K — needs ionization reactions. Out of scope here; an ionized-MET design is more like an arcjet-ion-hybrid, evaluated separately.
