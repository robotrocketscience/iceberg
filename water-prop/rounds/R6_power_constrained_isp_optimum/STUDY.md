# Round 6 — Power-Constrained Specific-Impulse Optimization

**Question.** Round 3i concluded that the dual-ion architecture at 1 kilovolt grid voltage delivers 97 percent of the chunk to low Earth orbit at 275 kilowatts of electrical power. But 275 kilowatts is not a realistic flight power level for the next 20+ years. Inverting the framing: given realistic available power (Kilopower 10 kWe, Fission Surface Power 40 kWe, sub-megawatt 100 kWe, megawatt-class roadmap 1000 kWe), what is the power-optimal specific impulse and the maximum achievable chunk-delivery fraction?

This is the classical NEP "power-optimal specific impulse" question (Stuhlinger 1964, Edelbaum 1961, Jahn 1968). The answer was the same in 1964 as it is now.

**Method.** Solve the joint energy-balance and Tsiolkovsky constraint:
- Energy: $\frac{1}{2} m_p v_e^2 = \eta \cdot P \cdot t \cdot \text{duty}$
- Tsiolkovsky: $m_p = m_0 (1 - e^{-\Delta v / v_e})$

Eliminating propellant mass: $m_0 (1 - e^{-\Delta v / v_e}) v_e^2 = 2 \eta P t \cdot \text{duty}$, a one-variable equation in $v_e$ for fixed mission parameters. Numerical root-find with `scipy.optimize.brentq`. See `src/waterprop/propulsion/nep_optimum.py`.

**Inputs:**
- Delta-V = 5.2 kilometers per second (revised from 4.2 after round 2's lunar gravity assist finding)
- Cruise time = 7 years at 50 percent duty cycle
- Total electrical-to-jet efficiency = 0.4
- Initial chunk mass = 5, 50, 200, 500 tons (covers the trade range from `docs/CHUNK-MASS-RANGE.md`)
- Available power = 5, 10, 20, 40, 70, 100, 200, 500, 1000 kilowatts electrical

**Validity caveats.**
- The model assumes the chosen propulsion technology can actually operate at the power-optimal specific impulse without efficiency falloff. Real thrusters have a sweet spot in their operating range; running well off-design degrades total efficiency. The constant 0.4 efficiency assumption is approximate.
- Reactor mass (round 1 finding: 2.5–6.5 watts per kilogram of dry mass) is NOT in this round's model. For a 100-kilowatt reactor weighing 20–40 tons, the chunk-fed initial mass is the chunk plus the reactor — significantly changing the Tsiolkovsky math for small chunks. See cross-learning.
- The model implicitly assumes the thruster can deliver the required thrust ($F = 2 \eta P / v_e$) — for very high specific impulse the thrust may be too low to make the cruise time, but the model doesn't enforce that. In practice for the operating points here, thrust ranges from ~30 mN at megawatt power, 1 kV operation down to ~3 N at Kilopower / low-Isp; all feasible.
- The user's note (correct) that grid voltage and power are independent: a 1 kilovolt thruster can operate at any power level, but at low power the mass flow rate and therefore the thrust drop proportionally. At 10 kilowatts / 1 kilovolt grid voltage / dual-ion architecture, the total propellant burned over a 7-year cruise is only 40 kilograms, delivering ~117 meters per second of delta-V — three orders of magnitude short of the mission's 5.2 km/s requirement. The "power-optimal specific impulse" is not a hard upper bound on what you CAN run, only on what you should run for this mission and time budget.

**Result.** See `results/power_constrained_optimum.png` and `results/power_constrained_optimum_sweep.csv`.

For a 50-ton chunk at 5.2 km/s delta-V over a 7-year cruise at 50% duty:

| Available power | Power-optimal Isp | Propellant | Delivered chunk | Delivery fraction |
|---|---|---|---|---|
| 5 kWe | 341 s | 39.4 t | 10.6 t | 21.2% |
| **10 kWe (Kilopower)** | **543 s** | **31.2 t** | **18.8 t** | **37.7%** |
| 20 kWe | 914 s | 22.0 t | 28.0 t | 56.0% |
| **40 kWe (Fission Surface Power)** | **1,625 s** | **13.9 t** | **36.1 t** | **72.2%** |
| 70 kWe | 2,674 s | 9.0 t | 41.0 t | 82.0% |
| 100 kWe (sub-megawatt) | 3,718 s | 6.6 t | 43.4 t | 86.7% |
| 200 kWe | 7,190 s | 3.6 t | 46.5 t | 92.9% |
| 500 kWe | 17,590 s | 1.5 t | 48.5 t | 97.0% |
| 1,000 kWe (megawatt) | 34,919 s | 0.8 t | 49.3 t | 98.5% |

Across chunk masses (5, 50, 200, 500 tons), the qualitative pattern is the same; absolute numbers differ:
- Smaller chunks need less impulse, so at any power level they reach higher delivery fractions and higher specific impulses.
- 5-ton chunk at 10 kWe: 87% delivery at 3,700 s specific impulse — Kilopower is plenty.
- 500-ton chunk at 10 kWe: 2% delivery at 137 s specific impulse — Kilopower is hopelessly underpowered for big chunks.

**Reading.**

This is the load-bearing analysis for the whole campaign. Several findings collapse together:

1. **At Kilopower (the only ground-tested reactor), the optimum specific impulse is 543 seconds — exactly microwave-electrothermal-class.** Higher-Isp technology cannot win at this power level because the energy budget doesn't support it. The conops' choice of microwave electrothermal at ~600 seconds (now believed to be more like 500–650 s per round 0) is **the correct architectural decision for a Kilopower-era mission**, not a compromise made for heritage reasons.
2. **At Fission Surface Power (40 kWe, paper-study only), the optimum jumps to 1,625 seconds — water radio-frequency ion territory.** Pale Blue's demonstrated 2,000 seconds is slightly above optimum but close enough that the heritage-competitive option (Pale Blue) is also the near-optimal one.
3. **The dual-ion architecture's 97 percent delivery requires 500 kWe at power-optimal operation**, or 275 kWe at 1 kilovolt grid voltage (sub-optimal for power efficiency but achievable in slightly more time). **Either way, sub-megawatt-to-megawatt reactor.** This is megawatt-class roadmap territory (2040s+). Not viable for the near-term ICEBERG concept.
4. **Higher specific impulse is not "always better."** It is only better when you have the power budget to use it. The Stuhlinger / Edelbaum classic result: optimum specific impulse scales as $\sqrt{P \cdot t / m_0}$. For ICEBERG-class inputs (50-ton chunk, 7-year cruise), the available power directly sets the optimum.
5. **For smaller chunks, the picture flips.** A 5-ton chunk at Kilopower delivers 87% at 3,718 seconds Isp. Small chunks plus Kilopower plus a high-Isp thruster like Pale Blue is a viable architecture. The conops' choice of microwave electrothermal is optimal for 50-ton chunks; it is sub-optimal for 5-ton chunks.

**Revisit.**

Hypothesis was not pre-registered for this round (exploratory). The result is the canonical NEP curve. The most important implication is the validation of the conops choice at Kilopower power class: microwave electrothermal at ~550 seconds is power-optimal for the stated mission. The dual-ion architecture, while exciting on a chunk-fraction basis, requires power levels that don't exist as flight programs.

**Cross-learning.**

- **Validates round 0**: microwave electrothermal at 500–650 seconds is the power-optimal choice at Kilopower power class for a 50-ton chunk. Not a compromise — the energy budget caps the optimum here.
- **Validates round 1's Pale Blue finding** as the Fission Surface Power-era candidate: 2,000 seconds is just above the 1,625-second power-optimum at 40 kWe.
- **Reframes round 3i**: dual-ion is interesting only at megawatt-class power, which is roadmap-only. At realistic power levels, it offers no specific-impulse advantage over Pale Blue. The advantage of the dual-ion architecture is mass utilization (100% vs 11% for hydrogen ion alone with oxygen vented); but in the power-optimal regime, the relevant comparison is against Pale Blue water radio-frequency ion at TRL 7–8.
- **Confirms risk E08** (reactor dry mass overhead) is load-bearing: at 100 kWe / 20–40 ton reactor, the reactor-plus-thruster mass approaches the chunk size for 50-ton chunks. Round 5 (mass margin) needs to include this explicitly.
- **Surfaces a new round**: **R6b — chunk-mass / power Pareto map**. Build a 2D heatmap showing optimal Isp and delivered mass across (power × chunk mass), with technology readiness overlays. This is the headline figure for the campaign verdict.
- **Methodology issue flagged**: this analysis ignored reactor dry mass. The reactor adds to the initial mass that has to be moved, so the Tsiolkovsky math is actually worse than this round's table suggests. Round 5 should fold this in.
- **Architecture implication**: **for a Kilopower-era flight, the conops' microwave-electrothermal choice is correct.** Higher-Isp candidates (water radio-frequency ion, dual-ion) only beat microwave-electrothermal once Fission Surface Power-class reactors become available. The R&D timeline is gated by the reactor program, not the propulsion program.
