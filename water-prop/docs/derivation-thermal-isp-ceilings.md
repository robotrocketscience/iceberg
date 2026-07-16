# derivation — Thermal-class Isp ceilings (pre-R0)

**Status:** Pre-R0 exploration. Textbook derivation, not a sim run. Per protocol §0, this is the substrate that future rounds crystallize out of.

**Purpose:** Ground the candidate Isp ranges in `candidates.md` rows A, B, C, D (the four thermal-class architectures) in first-principles physics rather than open-literature proxies. Catch any numbers we got wrong *before* HYPOTHESES.md locks them as pre-registrations.

## The framework

For an ideal nozzle with full expansion (P_e → 0), the exhaust velocity is:

`v_e = √(2 · h_0)`

where `h_0` is the total enthalpy per unit mass available at chamber conditions. For a thermally-driven thruster:

`h_0 = c_p · T_0 + h_chem_release`

The two contributions:
- **Thermal:** `c_p · T_0` — the gas's specific heat times stagnation temperature
- **Chemical release:** energy from dissociation/recombination during expansion, recoverable only in equilibrium flow (frozen flow forfeits it)

For an ideal-gas equilibrium expansion, combining contributions in quadrature is a useful rough form (not strictly correct, but ballpark):

`v_e ≈ √(v_thermal² + v_chem_release²)`

`Isp = v_e / g_0` where `g_0 = 9.81 m/s²`.

## Water-specific numbers

Water vapor c_p (NIST/CRC, mass basis):

| T (K) | c_p (J/kg·K) | Notes |
|---|---|---|
| 300 | 1858 | reference |
| 1000 | 2290 | vibrational modes activating |
| 2000 | 2680 | vib fully on |
| 3000 | 2980 | dissociation onset |
| 4000 | dissociation regime — frozen vs equilibrium matters |
| 5000+ | atomic regime — c_p of monatomic mixture |

Water dissociation energy: H₂O → H₂ + ½O₂ requires **241 kJ/mol = 13.4 MJ/kg**. Recovered as kinetic energy on expansion *only if recombination is fast vs the expansion timescale*. For a high-area-ratio nozzle, equilibrium is closer to reality at the throat and frozen at the exit.

Velocity equivalent of recovered chemical energy:

`v_chem ≈ √(2 · 13.4e6) ≈ 5170 m/s ≈ 527 s Isp`

This is the upper bound for the chemical contribution. Realistic equilibrium-flow recovery is ~40-70% of this: 3000-4000 m/s.

## Per-architecture derivation

### C — Water resistojet

**T_0 limit:** resistive heater life. Refractory metals at 2000K survive limited hours; flight-qualified hardware sits at 1500-1800K to get 10⁴+ hour life. Pale Blue's resistojet undisclosed but Sony Star-Sphere-1 and EQUULEUS hardware suggest T_0 in the 500-1000K range (much lower than the materials ceiling).

**Calculation at T_0 = 1800K (high end, materials-limited):**
- v_thermal = √(2 · 2500 · 1800) = 3000 m/s
- Dissociation negligible at 1800K (need >2800K for material fraction)
- v_e ≈ 3000 m/s → **Isp ≈ 306 s**

**Calculation at T_0 = 700K (Pale Blue flight reality, conservative):**
- v_thermal = √(2 · 2100 · 700) = 1715 m/s
- v_e ≈ 1715 m/s → **Isp ≈ 175 s**

**EQUULEUS flight-validated: 91 s.** That's well below either calculation. The gap is frozen-flow loss + nozzle divergence + plume losses, typically 30-50% deduction from ideal. Realistic flight: 50-60% of ideal.

**Revised range: water resistojet 90-250 s realistic, 300s ideal ceiling.** Was 70-150 in candidates.md — bottom end is right (Pale Blue at 91s), top end is too low (materials-limited ceiling is ~300s).

### B — Water arcjet

**T_0 limit:** wall melts at ~3000K (tungsten). Arc plume center is 5000-10000K but chamber-averaged stagnation gets to ~3500-4500K with regen cooling.

**Calculation at T_0 = 4000K (high end):**
- Equilibrium: partial dissoc starts (~30% of H₂O dissociated), M_avg drops, c_p effective rises
- v_thermal = √(2 · 3500 · 4000) = 5292 m/s
- Partial chem recovery: ~30% of 5170 m/s = 1550 m/s
- v_e ≈ √(5292² + 1550²) = 5514 m/s → **Isp ≈ 562 s** (equilibrium, ideal)
- Frozen flow penalty 30%: **Isp ≈ 400 s** realistic

**Range: water arcjet 400-560 s realistic, 600s with optimal expansion.** Consistent with `candidates.md` row B at 400-600s. ✓

### A — Water MET (microwave electrothermal)

**T_0 limit:** plasma is electrically driven, not contact-heated. Plasma-wall heat transfer is far lower than gas-wall for a magnetically/dielectrically confined plasma. Effective chamber-averaged T_0 can hit 5000-7000K with the wall held at materials-survival temperature.

**Calculation at T_0 = 6000K (high end, full dissoc to H+O atomic mix):**
- M_avg drops to ~6 g/mol (H₂O fully dissoc to 2H + O has M_avg = 6.0)
- R_s = 8314/6 = 1386 J/kg·K
- c_p of atomic mixture: (5/2)R = (5/2)·1386 = 3465 J/kg·K
- Wait — but you also need to add the energy of dissociation to enthalpy. Total h_0 = c_p·T_0 + (recovered dissociation)
- v_thermal_atomic = √(2 · 3465 · 6000) = 6450 m/s
- Full chem recovery (atomic regime → equilibrium expansion recombines at high area ratio): +5170 m/s in quadrature
- v_e ≈ √(6450² + 5170²) = 8265 m/s → **Isp ≈ 843 s** equilibrium ideal
- Frozen flow penalty ~20% (plasma flows tend to freeze at high recombination rates): **Isp ≈ 670 s** realistic

**Calculation at T_0 = 8000K (aggressive plasma, partial ionization):**
- v_thermal even higher, but ionization energy (1312 kJ/mol H, much larger than dissoc) is lost as radiation, not recovered
- v_e ≈ 9500 m/s → **Isp ≈ 970 s** equilibrium ideal
- Frozen penalty: **Isp ≈ 780 s** realistic

**Range: water MET 670-970 s ideal, 600-800s realistic.** `candidates.md` row A pre-registered 600-1000s. ✓ (top end is the theoretical ceiling, hardware reality lands in middle of range)

**The "Momentus approaches 1000s" claim is at the absolute theoretical ceiling with equilibrium expansion at T_0 ≈ 8000K. Our derivation suggests the flown 550W/750W Vigoride hardware delivers Isp in the 600-800s band rather than 1000s.** This is consistent with the Momentus research finding earlier today.

### D — Solar thermal on water (**THE BUG CATCH**)

**T_0 limit:** absorber/heat-exchanger materials. Tungsten mp 3695K, derated to 3000K for service. Rhenium-tungsten 3200K. Solar concentrator can deliver more power than the absorber can survive.

**Calculation at T_0 = 2800K (high end):**
- Partial water dissoc starts (~10% at 2800K)
- v_thermal = √(2 · 2900 · 2800) = 4031 m/s
- Partial chem recovery: ~15% of 5170 m/s = 775 m/s
- v_e ≈ √(4031² + 775²) = 4105 m/s → **Isp ≈ 418 s** equilibrium ideal
- Frozen penalty 20%: **Isp ≈ 334 s** realistic

**Range: solar thermal on water 330-420 s realistic.**

**`candidates.md` row D pre-registered 700-900 s. THIS IS WRONG.**

The 700-900s figure comes from solar thermal upper-stage proposals (STAR, ISUS, NASA SoTV) that all assumed **hydrogen propellant**, not water. For H₂:
- M=2, c_p ≈ 16000 J/kg·K at high T
- T_0 = 2800K
- v_e = √(2 · 16000 · 2800) = 9466 m/s → **Isp ≈ 965 s**

Hydrogen at the same chamber temperature beats water by ~2.5× on Isp because of molecular weight.

**Implication:** Solar-thermal-on-water is structurally limited to ~400s. It does NOT compete with MET on Saturn-cruise Isp. The candidate D entry in `candidates.md` was conflating "solar thermal" (the propulsion class) with "solar thermal upper stage" (the historically proposed hardware, which assumed hydrogen).

**To get high Isp out of solar power without electric conversion, you have to electrolyze water first and feed hydrogen to a solar-thermal heat exchanger.** That's now a hybrid architecture distinct from D — it's a sub-variant of G (chemical preprocessing).

### A + D hybrid (solar + electric MET, water-fed)

Worth noting because it's interesting and didn't make the original table:

If you concentrate sunlight on the MET cavity *and* drive plasma electrically, you raise effective T_0 via solar preheating. Lab work at AFRL studied this for combined-cycle thermal-electric thrusters. Theoretical Isp ceiling 850-1000s on water, but no flight heritage and significant integration complexity. Defer.

## Updated candidate table (revised Isp ranges)

| # | Architecture | Pre-registered Isp (was) | Derived Isp (now) | Change |
|---|---|---|---|---|
| A | Water MET | 600-1000 | 670-970 ideal, 600-800 realistic | ~confirmed |
| B | Water arcjet | 400-600 | 400-560 realistic | confirmed |
| C | Water resistojet | 70-150 | 90-250 realistic, 300 ideal ceiling | range widened — top end was too low |
| D | Solar thermal **on water** | 700-900 | **330-420 realistic** | **WRONG — corrected 2× downward** |
| D' | Solar thermal **on H₂** (needs electrolysis pre-stage) | (not in table) | 800-960 realistic | NEW — hybrid sub-variant of G |
| E | Electrolysis → H₂/O₂ chemical | 300-380 | 300-450 (HYDROS-C 310 flown, theoretical 480 vacuum-ideal) | range widened |
| F | Water vapor gridded ion | 500-1500 | 500-2000 lab; 7000 N·s life-limited (Pale Blue PBI) | unchanged |
| G | Hybrid: electrolysis → H₂-fed MET | 800-1500 | 900-1500 ideal, 800-1200 realistic | confirmed |
| H | Water PPT | 500-1500 | 500-1500 (highly op-point-dependent) | unchanged |

## What this changes for the campaign

**1. Solar-thermal-on-water (D) is functionally dead** for ICEBERG. It can't compete with MET on Saturn-cruise Isp, can't compete with arcjet on cost, doesn't have a unique angle. Drop or de-prioritize.

**2. Solar-thermal-on-hydrogen (D') emerges as a new architecture.** Requires electrolysis preprocessing. Eliminates the electric power conversion losses on the outbound leg (where solar is plentiful). H₂ cryo storage in deep space is hard (boil-off problem) — but for outbound-only operation on a multi-month timescale, plausible. **For Saturn cruise inbound, the multi-year H₂ storage problem kills it.**

**3. The MET ceiling really is at ~800-970s realistic, not 1000s.** Momentus's marketing claim "approaches 1000s" assumes the theoretical limit. Real flight hardware is more likely in the 650-850s band. Our pre-registration P1 (Bet 1 beats Bet 2) might be wrong if we counted Momentus marketing numbers.

**4. The arcjet/MET gap is smaller than expected.** Arcjet ~500s realistic; MET ~700s realistic. The 40% Isp improvement of MET over arcjet matters for Saturn (delivered-mass-per-flight scales steeply with Isp at 4.2 km/s ΔV target) but the difference between "viable" and "non-viable" is between resistojet and arcjet, not between arcjet and MET.

**5. We have a new architecture branch to add to the trade study:** **G + D' combined** — electrolyze water on the outbound leg, run solar-thermal on H₂ for the outbound cruise, recombine to water at Saturn for capture, then run water-MET on the inbound cruise. Multi-mode propulsion. Interesting; probably too complex for ICEBERG-co; worth a single-paragraph rejection in the verdict.

## Open questions surfaced

- **Frozen vs equilibrium expansion fraction** for water MET at flight scale. Theoretical bound says equilibrium recovers ~30% more Isp than frozen. Real Momentus hardware fraction is unknown. This is the difference between 700s and 950s.
- **Chamber temperature scaling with input power** for a water MET. Closed-form `P = ṁ · c_p · T_0` says higher power → higher T_0 → higher Isp at fixed ṁ. But real MET hardware hits efficiency rolloff above some optimal T_0. Where?
- **Pale Blue's actual resistojet T_0.** Their disclosed Isp (91s on EQUULEUS) implies T_0 ≈ 500-700K, which is much lower than the materials limit. Why? Probably power-limited at the spacecraft level — they don't have the budget to push T_0 higher. For ICEBERG with 5-10 kW of power available, the resistojet ceiling at 1800K (~300s Isp) is reachable, not just 91s.
- **The water-PPT case is undeveloped.** Need Jahn Ch. 9 to ground it properly. Defer.

## What this means for next steps

The textbook derivation pass produced one solid bug catch (solar-thermal-water Isp was 2× too high), confirmed three rows (A, B, E), and surfaced a new hybrid architecture (D'). Before R0, we should:

1. **Update `candidates.md`** to reflect the corrected row D and added row D'.
2. **Drop or de-prioritize candidate D** in the R0 trade study (it's a known dead-end on water).
3. **Pre-register MET Isp at the realistic 650-850s band**, not 1000s, in HYPOTHESES.md. This makes the "MET wins on Saturn-leg" aggregate prediction harder to confirm — which is the point.
4. **Add a sub-question** to the campaign: does any hybrid (solar-thermal-on-electrolyzed-H₂ + water-MET) beat the pure-MET architecture, when the chemical preprocessing cost is honestly accounted? This is an R1+ question, not R0.

No conclusions are locked. This is one textbook pass, not the answer.
