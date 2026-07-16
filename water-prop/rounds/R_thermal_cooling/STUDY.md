# R-thermal — Liquid Water as Reactor / Thruster Coolant + Propellant Preheat

**Status:** pre-result.

## Question

User-flagged architectural insight: instead of rejecting reactor and power-electronics waste heat through dedicated radiators (which sets the duty-cycle ceiling at 0.5-0.85 per Pale Blue / Dawn / BepiColombo heritage), route the chunk-fed water propellant through the cooling loop. The water absorbs waste heat, preheats from ~150 K (sublimating off the cold-wall bag) to several hundred Kelvin, then enters the ionizer hotter and more energetic.

**The question:** how much does propellant-as-coolant relax the duty cycle constraint, and what is the radiator mass savings? Does the audit's 0.7 duty cycle become realistic 0.85 or even 1.0 under this architecture?

## Pre-registered hypothesis (H-thermal)

**Aggregate (H-thermal-agg):** Propellant-as-coolant architecture relaxes the duty cycle ceiling from ~0.7-0.85 (radiator-limited) to approximately 0.95 (propellant-flow-limited) during cruise braking phase. The mass savings on radiators is 30-60% of nominal radiator mass. Ionization power requirement drops 5-10%. Combined improvement: per-ship deliverable chunk at 14-yr round trip rises another 15-25% beyond R-mid audit values.

**Pre-registered sub-claims:**

| Sub-claim | Predicted |
|---|---|
| H-thermal-a — Waste heat at Fission Surface Power 40 kilowatt-electric | 80-120 kilowatts thermal waste (25-33% conversion efficiency) plus 6-12 kilowatts electronics dissipation |
| H-thermal-b — Propellant mass flow at 40 kilowatt-electric water radio-frequency ion thrust | ~0.34 grams/second at 2000-second specific impulse + 0.65 efficiency (F = 2.65 N; m_dot = F/v_e ≈ 0.135 g/s wait this is wrong — let me recompute) |
| H-thermal-c — Heat capacity of water flow can absorb full waste heat | yes if mass flow × heat capacity × allowable ΔT >= waste heat power |
| H-thermal-d — Duty cycle improvement | 0.7 baseline → 0.9-0.95 under propellant-cooling architecture |
| H-thermal-e — Radiator mass savings | 30-60% of nominal radiator mass (estimated 2-5 t at Fission Surface Power class) |
| H-thermal-f — Cruise-braking time improvement at 14-yr ceiling | ~25-30% shorter due to higher duty + lower ionization power |

## Method

Use thermodynamics first-principles:

1. **Reactor waste heat at each power class** = (electrical output) × (1/conversion_efficiency − 1). For fission-electric at 25% efficiency (Kilopower / Fission Surface Power baseline), every 1 kilowatt-electric produces 3 kilowatts thermal waste.

2. **Propellant mass flow** at thrust F, exhaust velocity v_e: m_dot = F / v_e. For 40 kilowatt-electric water radio-frequency ion at 2000 s specific impulse and 0.65 efficiency: F = 2 × 0.65 × 40000 / 19620 = 2.65 N. m_dot = 2.65 / 19620 = 0.000135 kilograms per second = 0.135 grams per second.

3. **Heat absorption capacity of propellant flow.** Water heat capacity is 4.18 kilojoules per kilogram per Kelvin. At m_dot = 0.135 g/s and allowable ΔT = 200 K (heating from 150 K bag exit to 350 K ionizer input, well below water vapor pressure cliff at moderate ionization-chamber pressure): heat absorbed = 0.000135 × 4180 × 200 = 113 watts.

   **Wait — that is far less than the 120 kilowatt waste heat.** Propellant flow can absorb only ~0.1% of the waste heat. The architecture is fundamentally radiator-limited because mass flow is too small.

4. **Sanity-check via energy balance.** If the entire 40 kilowatt-electric reactor output went into accelerating water propellant at 2000-second specific impulse, the kinetic-power output is 0.5 × m_dot × v_e² = 0.5 × 0.000135 × 19620² = 26 kilowatts (thruster jet power, matches 2 × η × P = 52 kW input → 26 kW jet power if η=0.5 effective). The water carries kinetic energy 26 kilowatts, not thermal energy 120 kilowatts.

5. **Therefore: propellant-as-coolant doesn't work at electric-propulsion mass flow rates.** Mass flow is 3 orders of magnitude too small to absorb meaningful reactor waste heat.

## Result (sketched pre-run)

**H-thermal aggregate: FALSIFIED before running.** Quick energy-balance check shows propellant mass flow at electric-propulsion specific impulse is 1000x too small to absorb reactor waste heat. The architecture would only work for nuclear thermal propulsion (NTP), where mass flow is high enough.

For reference:
- Electric propulsion (water radio-frequency ion at 40 kilowatt-electric): m_dot = 0.135 g/s, can absorb ~113 W. Reactor waste heat: 120 kW. **Coolant capacity is 0.1% of waste heat.**
- Nuclear thermal water propulsion (NTP-water, conceptual): m_dot at 800-second specific impulse and 100 newtons thrust = 100 / 7848 = 0.0127 kilograms per second = 12.7 g/s. Heat absorption at ΔT = 1500 K (water → steam at 1700 K typical NTP outlet): 0.0127 × 4180 × 1500 + heat of vaporization 2257 × 0.0127 × 1000 = 80 kilowatts + 29 kilowatts = 109 kilowatts. **Coolant capacity matches reactor scale for NTP.**

**The architectural insight points to nuclear thermal propulsion, not electric propulsion as currently baselined.** This is a meaningful finding — it suggests a fundamentally different propulsion architecture (NTP-water) where the conversion efficiency problem dissolves because the reactor IS the thruster.

## Reading (sketched)

**Propellant-as-coolant doesn't help the current water radio-frequency ion architecture.** Electric propulsion mass flow is too low by ~3 orders of magnitude to absorb the reactor's thermal waste. The duty cycle constraint remains radiator-limited.

**But the architectural insight points somewhere useful:** for nuclear thermal water propulsion (NTP-water, conceptual), the propellant IS the working fluid that absorbs reactor heat directly. There's no electrical conversion step, no waste-heat-rejection problem, and no duty cycle constraint set by radiators. NTP characteristics:
- Specific impulse: 600-1000 seconds (water-cooled NTP; lower than electric)
- Thrust: 1000-100,000 newtons (much higher than electric)
- Mass flow: 1-100 grams/second (orders of magnitude higher than electric)
- Duty cycle: limited by reactor thermal cycling, but ~1.0 during continuous burn

NTP-water would be a different mission architecture entirely:
- Specific impulse 700-800 seconds means more propellant burn for the same delta-velocity (similar to water-MET)
- High thrust means impulsive-class burns: minutes to hours for trans-Saturn-injection or capture, not years of low-thrust spiral
- Could potentially eliminate the chemical trans-Saturn-injection kick stage (NTP does it directly)
- Saves the $140 million per ship trans-Saturn-injection cost
- Saves the 10+ year low-thrust spiral inbound — replaced by short impulsive maneuvers
- Round trip could be Hohmann ballistic (6 yr each way) + brief impulsive maneuvers = ~13.5 years (back to conops headline)

**NTP-water is a different propulsion architecture worth a dedicated round.** R-thermal as a question (propellant cooling) was the wrong frame; the right frame is "use the reactor as a thruster directly."

## Revisit

The user's prompt was insightful but pointed at a different architectural regime than I initially recognized. Electric propulsion with chunk-water has fundamentally low mass flow rates that don't carry meaningful thermal capacity. NTP-water, by contrast, has 100x+ higher mass flow rates and the propellant naturally absorbs reactor heat (because that's literally how nuclear thermal propulsion works).

**Promote R-NTP-water (nuclear thermal water propulsion) to the queue as a load-bearing alternative architecture round.** This is the answer to the user's "different propulsion systems" earlier prompt.

## Cross-learning

- **The water-cooling insight points to a different propulsion class entirely.** Electric propulsion (radio-frequency ion, Hall, dual-ion) has low mass flow and electrical-conversion-losses → big radiator problem. Nuclear thermal propulsion has high mass flow and no electrical conversion → propellant is the natural coolant. The conops baselines electric; NTP is a fundamentally different architecture.
- **Energy-balance sanity checks should be the first thing checked when proposing thermal architectures.** Mass flow × heat capacity × allowable ΔT vs available waste heat is a 30-second calculation that immediately distinguishes electric-class (radiator-limited) from thermal-class (mass-flow-limited).
- **R-thermal sub-claims H-thermal-a through H-thermal-f are all moot** because the load-bearing prediction (propellant flow can absorb meaningful waste heat) fails the first-principles check. This is the cleanest "round falsified before running" example in the campaign.
