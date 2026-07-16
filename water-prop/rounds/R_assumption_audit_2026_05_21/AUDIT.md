# R-assumption-audit-2026-05-21 — load-bearing assumptions in the mission-graph framework

**Status:** audit, in progress. Authored by Saturn (worker), 2026-05-21.

## Premise

The framework has grown to 10 phases × ~36 options. The canonical sweep shows 2,808 of 53,704 paths close the 30-tonne delivered-floor predicate (5.2 percent). Before adding more options or running more sweeps, audit every load-bearing numerical and structural assumption and identify which would invert the closure verdict if wrong.

Method: for each assumption, state the hypothesis explicitly, predict the impact if wrong, design a test to falsify, give a preliminary verdict where evidence is already in hand.

## Tier 1 — load-bearing for closure verdict

### A1. Water-microwave-electrothermal (water-MET) specific impulse = 800 s

**Hypothesis:** chunk-fed water electrothermal thrust delivers 800 seconds of specific impulse at flight scale.

**Origin:** R0_microwave_electrothermal_frozen_flow round; upper-bound desk-study figure. Cited in `Phase4_chunk_fed_spiral_departure` and the new `Phase7_lunar_processing_and_leo_transfer`.

**Predicted impact if wrong:** chunk-fed spiral departure is the only Phase 4 option that's reachable at the canonical sweep. If specific impulse is actually 500 s (more realistic per R10b_thruster_per_power_class), the rocket-equation propellant cost for the same delta-v rises by ~30 percent. The 200-tonne chunk closure threshold likely moves to ~300 tonnes — possibly out of the sweep range.

**Test:** sensitivity sweep on `water_met_isp_s` parameter at values {400, 500, 600, 700, 800, 900}. Re-run closure surface. Find the specific-impulse threshold below which closure collapses.

**Falsifiability:** if closure rate at 500 s drops below 1 percent, the framework is anchored on an optimistic propulsion assumption that needs replacing with a more conservative number.

**Preliminary verdict:** UNTESTED. Highest priority test.

---

### A2. Low-thrust spiral total delta-v = 13 km/s for Saturn outbound

**Hypothesis:** an electric propulsion vehicle starting from low-Earth orbit at v_inf = 0 needs 13 km/s of accumulated delta-v to reach Saturn at v_inf ~0.5 km/s.

**Origin:** desk-study trajectory anchor from titan-3 R-chunk-size-pareto. Not a true low-thrust optimization output.

**Predicted impact if wrong:** if real delta-v is 17 km/s (cited in some Hall-thruster trajectory papers for slow spirals), propellant requirement at 3000 s specific impulse goes from `m * (1 - exp(-13/29.4)) = 35.8 percent` to `m * (1 - exp(-17/29.4)) = 43.7 percent`. Vehicle dry-mass fraction drops correspondingly. May invert closure at lower vehicle masses.

**Test:** run open-source low-thrust trajectory optimization (pyKEP, poliastro, or simple Edelbaum approximation) for LEO → Saturn at canonical electric thrust (5-25 N) and electric specific impulse (3000 s). Compare to 13 km/s anchor.

**Falsifiability:** if optimal trajectory gives 15 km/s or more, the framework's low-thrust spiral feasibility surface is over-optimistic.

**Preliminary verdict:** UNTESTED. Edelbaum analytical approximation gives ΔV ≈ v_circ_initial - v_circ_final * cos(plane change) for circle-to-circle transfers. LEO to Saturn orbital velocity: v_LEO ~7.7 km/s, v_Saturn_orbital ~9.7 km/s in heliocentric. Plus need ~12 km/s of heliocentric ΔV from Earth's orbit to Saturn's. Total spiral including LEO escape and Saturn capture is plausibly in the 15-20 km/s range — possibly higher than the 13 km/s anchor.

---

### A3. Aerocapture at Earth maximum payload = 30 tonnes

**Hypothesis:** aerocapture works for payloads up to 30 tonnes at Earth arrival; anything larger fails on thermal protection mass scaling.

**Origin:** titan-2 R-aerocapture rounds; structural argument about heat-shield areal density vs ballistic coefficient.

**Predicted impact if wrong:** if the limit is actually 100 tonnes (some more recent NASA studies argue this for inflatable / deployable aeroshells), aerocapture becomes viable for large-chunk missions, eliminating the propellant cost of direct propulsive capture. Closure rate likely 2-3x at canonical configuration.

**Test:** literature search on heat-shield scaling (NASA Hypersonic Inflatable Aerodynamic Decelerator program, etc.). Compute heat shield mass as a function of payload from first principles: thermal load ∝ ρ * v² * A_blunt, mass ∝ A * areal_density * heat_flux_integral.

**Falsifiability:** if NASA Hypersonic Inflatable Aerodynamic Decelerator has demonstrated 100-tonne payload aerocapture, the 30-tonne limit is conservative.

**Preliminary verdict:** UNTESTED. The Hypersonic Inflatable Aerodynamic Decelerator program has flown 3.7-m diameter aeroshells; scaling laws suggest 12-15 m diameter is feasible. 30 tonnes is plausibly too conservative.

---

### A4. Chunk mass = 100 percent water, structurally intact for trawl + departure + return

**Hypothesis:** the captured Saturn ring particle is pure water ice, structurally intact through capture maneuvers, and remains usable as both payload and propellant feedstock.

**Origin:** desk-study simplification. Real ring particles are heterogeneous: water ice is dominant by mass but there are silicate inclusions, micron-scale dust, and accreted material.

**Predicted impact if wrong:** if useable water fraction is 80 percent (rather than 100 percent), and structural breakup loses another 10 percent during capture maneuver, then a 200-tonne nominal chunk delivers ~144 tonnes of useable water. Closure threshold moves from 200 tonnes nominal chunk to ~280 tonnes nominal chunk.

**Test:** survey of Cassini ring-particle composition data. Estimate breakup probability from R_bring_rendezvous_survivability and R_bag_capture_efficiency_revisit prior rounds.

**Falsifiability:** if Cassini data shows water fraction below 70 percent in any ring band ICEBERG would target, the framework's 100-percent-water-yield assumption breaks closure at canonical chunk masses.

**Preliminary verdict:** R_bring_rendezvous_survivability and R_bag_capture_efficiency_revisit are prior rounds that touch this. Need to re-read their conclusions.

---

### A5. Reactor power class as constant scalar (no distance-from-sun dependence)

**Hypothesis:** `power_available_kwe` on VehicleState is constant across the mission, regardless of location.

**Origin:** v0 framework simplification.

**Predicted impact if wrong:** if vehicle uses any solar augmentation, available power changes by ~100x between low-Earth orbit and Saturn. The hybrid reactor + solar architecture (per project owner) requires distance-aware power. This was captured in `R_solar_thermal_hybrid_power/SCOPE.md` as a high-priority follow-on.

**Test:** add solar-flux-vs-distance function to VehicleState power lookup. Re-run sweep. Verify hybrid architectures with significant solar component now show different reachability.

**Falsifiability:** if the hybrid architecture closure surface is materially different from the pure-reactor closure surface, the current scalar-power model has been hiding a real architectural option.

**Preliminary verdict:** UNTESTED but ARCHITECTURALLY VALID per the prior conversation. Captured in `R_solar_thermal_hybrid_power/SCOPE.md`.

---

### A6. Kick-stage delta-v decomposition (after the fix)

**Hypothesis:** the corrected kick-stage model (286 s specific impulse for Star-class, 330 s for Helios-class) accurately reflects real solid-motor and liquid-bipropellant kick performance.

**Origin:** corrected in commit `cce2810`. Star 48B real specific impulse: 286 s vacuum. Helios speculative anchor: 330 s for hydrocarbon/oxygen liquid kick.

**Predicted impact if wrong:** if real kick performance is closer to 290 s (Star) and 340 s (Helios), the kick-wet-mass calculations are within ~3 percent. Already-tight feasibility surface for kick stages remains tight; conclusions unchanged.

**Test:** cross-reference Star 48B Boeing data sheet and any Impulse Space Helios technical specs.

**Falsifiability:** if Helios real specific impulse is below 300 s, the Helios option may not be feasible even at the configurations we tested.

**Preliminary verdict:** Star 48B is well-known (286 s vacuum from Thiokol data). Helios is unflown; 330 s is plausible but not validated.

## Tier 2 — significant but not load-bearing

### A7. Hohmann trans-Saturn injection delta-v = 7.3 km/s

**Hypothesis:** chemical Hohmann from low-Earth orbit to Saturn arrival needs 7.3 km/s of delta-v.

**Origin:** desk-study figure; the real number depends on Earth-Saturn alignment.

**Predicted impact if wrong:** ±0.3 km/s based on launch window. Translates to ±10 percent in propellant requirement at 340 s specific impulse. Already within the noise of the propellant-fraction sweep.

**Test:** open-source ephemeris-based Hohmann calculation for 2032-2050 demonstrator window.

**Preliminary verdict:** UNTESTED; low priority — bracketed by the propellant-fraction sweep.

---

### A8. Gravity-assist delta-v reductions are constant anchors

**Hypothesis:** Jupiter GA reduces v_inf by 2.5 km/s, Mars+Jupiter by 4.0 km/s, Venus-Earth by 2.0 km/s, lunar by 5.83 km/s, Titan by 4.0 km/s, Rhea by 1.5 km/s, Cassini-class multi-moon by 5.5 km/s, Earth-GA-slowdown by 3.0 km/s.

**Origin:** desk-study constants based on first-principles flyby geometry. Captured in `R_saturn_moon_ga_ephemeris/SCOPE.md` as a deferred ephemeris study.

**Predicted impact if wrong:** ±20 percent on any single GA value moves closure surface by similar amount. Aggregate effect across multiple stacked GAs could compound.

**Test:** the ephemeris-driven SCOPE handles this.

**Preliminary verdict:** UNTESTED. Tier 2 because errors are bounded and the framework can be retuned post-ephemeris.

---

### A9. Launch window stub windows (Earth-Saturn 21-day, Earth-Jupiter 30-day, Cassini-class 60-day, Venus-Earth 20-day)

**Hypothesis:** these synodic-period-based stub windows are adequate go/no-go gates for sizing.

**Origin:** ephemeris_stubs.py first-order approximation.

**Predicted impact if wrong:** the real launch window is wider in some cases and narrower in others. Critically, the alignment between simultaneous Mars+Jupiter+Saturn (Cassini-class) is exquisitely sensitive — the real 1997 Cassini window was a 30-day opportunity, not 60.

**Test:** integrate JPL Horizons ephemeris data via existing robotrocketscience website integration. Replace stub windows with real synodic alignment calculations.

**Preliminary verdict:** UNTESTED. Tier 2 because misaligned windows just delay missions, they don't invalidate them.

---

### A10. Phase 7 lunar-to-LEO transfer uses water-MET at 800 s

**Hypothesis:** the lunar-to-LEO water shuttle uses water-electric thrust at the same 800 s specific impulse as the outbound chunk-fed leg.

**Origin:** Phase 7 model.

**Predicted impact if wrong:** if specific impulse is 500 s (more conservative water-electric performance), the mass ratio for the 3 km/s lunar-to-LEO transfer is exp(3 / 4.9) = 1.85 instead of 1.47. Arriving water at low-Earth orbit drops from 68 percent to 54 percent of chunk mass. Sub-mission margin shrinks but does not break closure.

**Test:** same sensitivity sweep as A1.

**Preliminary verdict:** UNTESTED but coupled to A1.

## Tier 3 — structural / methodological

### A11. Closure predicate `delivered_floor` is set at 30 tonnes

**Hypothesis:** 30 tonnes delivered water is the L0-09 commercial floor below which the mission is not commercially viable.

**Origin:** L0-09 requirement document.

**Predicted impact if wrong:** if the real floor is 100 tonnes (some demand-modeling rounds suggest higher numbers for a 7-year mission timeline), most of the current "closing" paths are below the floor.

**Test:** re-read L0-09 derivation. Re-read R_market_demand_floor_sensitivity if it exists.

**Preliminary verdict:** UNTESTED. Methodological; affects how we interpret closure verdicts but not whether the physics works.

---

### A12. Vehicle mass sweep grid is anchored to launcher capacities

**Hypothesis:** the (50, 63, 100, 150, 200) tonne vehicle-mass grid covers the realistic launcher capacity space.

**Origin:** explicit anchor to Falcon Heavy partial-reuse, Falcon Heavy expended, Starship lower, Starship upper, multi-Falcon-partial.

**Predicted impact if wrong:** if New Glenn or Starship-V3 ends up with significantly different capacity, the grid misses real architectures.

**Test:** sensitivity sweep on vehicle mass at finer grid resolution (e.g., every 10 tonnes from 30 to 250).

**Preliminary verdict:** Grid is anchored to current published numbers but could miss future launcher updates.

---

### A13. No vehicle reliability / degradation modeling

**Hypothesis:** vehicle hardware works perfectly for 7-15 year mission duration.

**Origin:** v0 framework simplification.

**Predicted impact if wrong:** at 0.5 percent per year hardware-failure rate, a 10-year mission has ~5 percent attrition. Mission risk-adjusted closure rate drops correspondingly.

**Test:** add stochastic reliability layer (out of scope for sizing-level framework; should be a follow-on R-round).

**Preliminary verdict:** Out of scope for current framework iteration.

## Ranked priority for testing

1. **A1 water-MET specific impulse sensitivity** — single most load-bearing assumption. Run a sweep over {400, 500, 600, 700, 800, 900} s.
2. **A2 low-thrust spiral delta-v** — second-most load-bearing. Run open-source low-thrust optimization or Edelbaum approximation.
3. **A3 aerocapture payload limit** — literature search on Hypersonic Inflatable Aerodynamic Decelerator scaling.
4. **A4 chunk yield** — re-read prior rounds + add a useable-water-fraction parameter to the sweep.
5. **A5 distance-dependent power** — implement per `R_solar_thermal_hybrid_power/SCOPE.md`.

## What test 1 would look like in detail

`water_met_isp_s` sensitivity sweep:
- Add `water_met_isp_s` as a fifth axis in `saturn_water_canonical_sweep.py` with values {400, 500, 600, 700, 800, 900}.
- Total cells: 5^5 = 3,125 (~30 minutes wall-clock).
- Aggregate: closure rate vs water-MET specific impulse, marginal closure breakdown.
- Expected falsification surface: closure rate drops sharply below ~600 s.
- If true, document the threshold and update the framework default to a more conservative anchor.

## Next steps

1. Run A1 test now (single sweep, ~30 minutes).
2. Build A2 test (Edelbaum approximation for low-thrust spiral) — small Python script outside the framework.
3. Aggregate results into a `FINDINGS.md` document parallel to this AUDIT.
4. Update framework defaults where assumptions falsified.
5. Open A3, A4, A5 as follow-on rounds.
