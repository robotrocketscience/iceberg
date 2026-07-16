# R-assumption-audit-2026-05-21 — findings

**Status:** complete. Authored by Saturn (worker), 2026-05-21.

## Summary

Tested four of thirteen load-bearing assumptions catalogued in AUDIT.md. Two falsified hard, one falsified softly, one partially falsified, with very different implications for the framework's closure surface.

| Assumption | Verdict | Closure-surface impact |
|---|---|---|
| A1 water-electrothermal specific impulse = 800 s | **PARTIALLY FALSIFIED — sits at the cliff** | Drop to 700 s halves closure; drop to 600 s near-zero |
| A2 low-thrust spiral delta-velocity = 13 km/s | **FALSIFIED ON NUMBER, ROBUST IN VERDICT** | Real number is ~22 km/s but closure rate is flat from 13-28 km/s |
| A11 delivered-floor = 30 tonnes | **FALSIFIED AS ANCHOR, MAJOR LEVERAGE** | Floor is a cliff: 10 t → 52% close; 30 t → 8.5%; 50 t → 0% |
| A12 vehicle mass grid 50-200 tonnes | **FALSIFIED AS ANCHOR** | Smaller vehicles (10-50 t) close as well or better; multi-launch not required |

## A1 — water-electrothermal specific impulse

**Test:** swept water_met_isp_s across {400, 500, 600, 700, 800, 900} seconds in an audit sweep (288 cells).

**Result:**

| specific impulse (s) | closure rate |
|---:|---:|
| 400 | 0.0% |
| 500 | 0.0% |
| 600 | 0.5% |
| 700 | 2.9% |
| 800 (anchor) | 7.0% |
| 900 | 10.7% |

**Verdict:** the 800-second anchor sits exactly at the inflection point. Drop by 100 seconds and closure rate halves. Drop by 200 seconds and the matrix collapses.

**Action:** find a flight-rated water-electrothermal-thruster specific-impulse measurement. Until then, the matrix's closure verdict is conditional on a flight-scale 700-900 second specific impulse that hasn't been demonstrated.

## A2 — low-thrust spiral delta-velocity

**Test:** computed Edelbaum analytical bound for pure low-thrust LEO → Saturn approach (`test_a2_low_thrust_delta_v.py`). Compared to framework anchor of 13 km/s.

**Edelbaum bound:**
- Earth-bound spiral escape from low-Earth-orbit: 7.73 km/s
- Heliocentric Earth-orbit to Saturn-orbit spiral: 20.16 km/s
- **Total Phase 1 lower bound: 27.89 km/s**

**Discrepancy:** framework anchor is **53 percent below** the analytical lower bound. Published Glenn Research Center Hall-thruster mission designs land in the 18-25 km/s range — still significantly above 13 km/s.

**Sensitivity sweep:** ran the framework with low_thrust_total_dv_km_s as a parameter at {13, 18, 22, 25, 28} km/s. Closure rate was flat (8-10 percent) across the entire range.

**Why the closure surface is robust:** the dominant closing architecture uses 10-30-tonne vehicles. At small vehicle mass, even 28 km/s low-thrust delta-velocity costs only ~6 tonnes of propellant in absolute terms — well within budget. At larger vehicles (100+ tonnes) the burn-time-versus-coast-window constraint binds before the rocket equation does.

**Verdict:** the 13 km/s number is unrealistic — should be 22 km/s in the framework anchor — but the closure-surface verdict is robust to this correction.

**Action:** update LOW_THRUST_TOTAL_DV_KM_S default to 22.0. Keep the parameter override for sensitivity studies.

## A11 — delivered-floor at 30 tonnes

**Origin:** sticky shorthand from titan-3 R-chunk-size-pareto, NOT anchored in REQUIREMENTS.md. L0-04 commercial-class mass floor is currently OPEN / TBD. L0-09 (the requirement the floor language usually cites) is about service availability ratio, not per-mission mass.

**Test:** added 5 floor closure predicates (10 t, 20 t, 30 t, 50 t, 100 t) and aggregated the latest audit sweep across all of them.

**Result:**

| floor | closure rate |
|---:|---:|
| 10 t (demonstrator-class threshold) | **52.1%** |
| 20 t (pre-commercial-class) | **25.0%** |
| 30 t (current anchor) | 8.5% |
| 50 t | **0.0%** |
| 100 t | **0.0%** |

**Verdict:** the framework's closure verdict is almost entirely determined by where the floor sits, not by the physics. The 30-tonne current anchor is right at the cliff edge. Demonstrator-class missions (10-tonne floor, "any non-zero" per REQUIREMENTS §7) close handily; commercial-class missions at 50-tonne floor are infeasible at all canonical architectures.

**Action:** L0-04 commercial-class floor must be derived before any further matrix-verdict claims are credible. The closure surface is a function of this number more than of any physics axis.

## A12 — vehicle mass grid 50-200 tonnes

**Test:** ran audit sweep with vehicle mass extended downward to 10 / 20 / 30 tonnes alongside the canonical 50 / 63 / 100 / 150 / 200.

**Result:**

| vehicle mass (tonnes) | closure rate |
|---:|---:|
| 10 | 4.5% |
| 20 | 4.7% |
| 30 | 4.6% |
| 50 | **5.1%** (peak) |
| 63 | 4.4% |
| 100 | **0.0%** |
| 150 | 0.0% |
| 200 | 0.0% |

**Verdict:** closure rate is roughly flat from 10 to 63 tonnes; collapses at 100+ tonnes due to burn-time-versus-coast constraint. The "multi-launch + in-orbit-assembly" architecture has been carried in the matrix on pitch optics, not physics — single-launch Falcon 9 or Falcon Heavy partial-reuse architectures close as well or better.

**Action:** revise the matrix to recognize single-launch demonstrator architecture as the preferred path. Multi-launch assembly is an architectural option but not a closure requirement.

## Combined finding: the framework was anchored on cliff-edges

Two of the four tested assumptions (A1 water-electrothermal specific impulse, A11 delivered-floor) sit EXACTLY at cliff edges in the closure surface. Tiny errors in either produce huge swings in matrix verdict. This is not a coincidence — the framework's "5 percent close" headline implicitly required these anchors to be calibrated to that exact value.

If a more rigorous derivation of EITHER assumption moves it by 20 percent in the wrong direction, the matrix collapses to zero. If it moves 20 percent in the right direction, closure rate triples.

**The matrix verdict is therefore CONDITIONAL ON these assumption values, not robust to them.** Anyone reading the matrix should know which assumptions are load-bearing in this sense.

## A4 update — Cassini-data validation (2026-05-21 evening)

The earlier audit sweep at chunk_water_fraction (0.6, 0.8, 1.0) flagged A4 as a high-leverage falsification risk (closure rate drops by 4x going from 100% to 80% water). Cassini-data validation finds the 100% water assumption is well-supported for ICEBERG's target rings:

- **B-ring (ICEBERG primary target):** 99.7-99.8% water by volume per Cassini microwave radiometry
- **Main rings overall (A, B, Cassini Division):** >99% (some sources cite 99.9%)
- **C-ring middle:** up to 11% non-icy material (worth avoiding)
- **D-ring:** organic and silicate rich, water-poor (not a target)
- **Ring rain falling into Saturn's atmosphere:** ~95% water (enriched in non-water because lighter water sublimates; NOT the ring-particle composition)

The Cassini "ring rain" 95% water number that motivated the 0.6-1.0 sweep range applies to the wrong material. Ring particles themselves (what ICEBERG would harvest) are >99% water at all ICEBERG-targeted zones.

**Verdict revised: A4 CONFIRMED, not falsified.** The framework's 100% water assumption is supported by Cassini data. Closure rate at realistic 0.99 fraction is ~10% at 30-tonne floor, essentially identical to 10.1% at 1.0. Default unchanged.

**Caveats logged:**
1. Composition is not strength: ring-particle aggregate fragmentation during capture is a separate concern captured by Phase 3 capture-efficiency constants (0.65-0.85).
2. B-ring direct rendezvous architecture has been separately falsified by phoebe rounds — high water content but engineering-zero survivability.
3. Pollution age (30-150 Myr) means ring composition is stable on mission timescales.

Sources: Cassini microwave radiometry; Cassini infrared spectroscopy; Cassini Ion and Neutral Mass Spectrometer ring-rain analysis.

## A1 update — water-electrothermal specific impulse ground-test validation (2026-05-21 evening)

The 800-second water-MET specific impulse anchor is **supported by ground-test data** but not yet flight-validated at the operation profile ICEBERG needs.

Sources:
- AMET (NASA Small Business Innovation Research): >800 s with water vapor
- MET (academic literature): ~900 s peak for 50+ second pulses
- Multiple academic publications: 700-900 s range
- Lower-performance flight heritage alternatives: water resistojet ~180-200 s; water arcjet ~300-400 s
- Momentus Vigoride-3/5 (in-flight demonstration of water-plasma propulsion; specific in-flight specific-impulse not publicly detailed)

Three caveats the framework hasn't been carrying explicitly:

1. Ground-test ≠ flight-demonstrated. Momentus Vigoride is the closest ICEBERG has to flight validation; specific numbers not public.
2. Pulse ≠ continuous. The 900 s figure is for 50-second pulses. ICEBERG needs continuous operation for months (Phase 4 chunk-fed spiral, Phase 7 lunar-to-LEO shuttle). Steady-state specific impulse may be lower.
3. Lab-clean propellant ≠ Saturn-ring water. Real ring water has ~0.3 percent non-icy content. Trace silicates could erode the thruster's resonant cavity over months of operation.

Verdict: A1 is PLAUSIBLE-PROVISIONAL. The lab-demonstrated specific impulse is in the right band, but the duration-and-continuity requirement is unvalidated.

Architectural fallback paths if A1 underperforms:
- Water arcjet 300-400 s (flown heritage; matrix would not close at the 25-tonne L0-04 floor)
- Chemical-electric leapfrog (water electrolysis + chemical): ~450 s effective; same problem
- Pure chemical with water feedstock: ~450 s; same problem

**Recommendation:** the demonstrator mission's highest-leverage technical objective is to demonstrate a water-MET running CONTINUOUSLY for MONTHS on chunk-class-purity water in deep space. That's the single experiment that confirms or falsifies A1 conclusively. More leverage than the chunk-acquisition demonstration because chunk acquisition can fall back to alternative architectures; A1 cannot.

Sources: AMET Small Business Innovation Research; MET academic literature 2005-2024; Momentus Vigoride mission reports.

## A14 — chunk-capture efficiency is the most load-bearing assumption

Added to the audit list this round. Tests the 0.65-0.85 capture-efficiency anchors hardcoded in Phase 3 single_pass_trawl, drift_through_trawl, fg_gap_rendezvous_trawl, and b_ring_direct_rendezvous.

**Verdict: PARAMETRICALLY FALSIFIED. The matrix verdict is determined by this single assumption more than by any other.**

Test: capture_efficiency_multiplier sweep at (0.25, 0.50, 0.75, 1.00):

| Multiplier | Best delivered (t) | Closure at 30-t floor |
|---:|---:|---:|
| 0.25 | 4.3 | 0.0% |
| 0.50 | 19.7 | 0.0% |
| 0.75 | 33.1 | 1.1% |
| 1.00 | 47.1 | 7.2% |

Engineering decomposition: rendezvous 90 percent × deployment 95 percent × catch 80 percent × containment 70 percent × survival 95 percent = ~46 percent joint success. That's the 0.50 multiplier, where the matrix collapses to zero closure at the L0-04 = 25-tonne provisional floor.

Cassini sampled ring particles passively. No spacecraft has ever attempted active capture of a multi-tonne ring particle. The 0.85 anchor is pure desk-study optimism.

**Demonstrator-mission implication:** A14 is the most load-bearing assumption. A small-scale active-chunk-capture demonstration (10-tonne chunk in Saturn or even simulated in low-Earth orbit using deployable target masses) is the second critical-path demonstrator objective after water-electrothermal specific impulse (A1).

## A3 — aerocapture payload limit (Hypersonic Inflatable Aerodynamic Decelerator scaling)

Verdict: 30-tonne cap is REASONABLY CONSERVATIVE.

Hypersonic Inflatable Aerodynamic Decelerator scaling per NASA Technical Reports Server 2024:
- 6 m diameter (LOFTID, flown 2022): ~2.5 t payload
- 8.5 m: ~3.5 t payload
- 20 m: ~20 t payload

Roughly scales as diameter squared. 30-tonne cap at ~24 m aeroshell is a modest extension of demonstrated technology. Not optimistic, if anything slightly aspirational.

Architecturally important: ICEBERG's 200-tonne chunk cannot directly aerocapture. The closing matrix path works because chunk-fed-spiral departure consumes most of the chunk during return, leaving ~40-tonne-class payload at Earth approach.

**A1 (water-electrothermal specific impulse) and A3 (aerocapture mass limit) are coupled:** if A1 underperforms, the residual chunk at Earth approach exceeds the aerocapture cap, forcing direct propulsive or lunar staging. The framework doesn't currently capture this coupling explicitly.

## A15 — lunar gravity assist tour 5.83 km/s

Verdict: PLAUSIBLE-PROVISIONAL at the upper end of published estimates.

Locked belief `1a564ee4` cites "10 flybys, 4.5 months, 5.83 km/s reduction." Arithmetic works: 10 × ~0.58 km/s per pass = 5.8 km/s. But:
- 10 flybys in 4.5 months = ~13-day spacing, tight against ~27-day lunar period
- Each pass needs trajectory replanning
- No flight precedent for 10-pass lunar capture tour (Cassini's Saturn-moon tour has 155 flybys but over 13 years)

Single lunar gravity assist can capture arrival v_inf up to ~1.5 km/s per NASA Technical Reports Server material capture analysis. Reaching the 5.83 km/s total reduction requires the aggressive multi-pass tour.

Not load-bearing for the current matrix verdict because lunar gravity assist capture doesn't dominate the closing architecture — direct propulsive and hybrid aerocapture options do.

## Open audit work

A5 distance-dependent power (deferred SCOPE per R_solar_thermal_hybrid_power).

A8 Tier 2 GA delta-v anchor sensitivity — Titan/Rhea/Cassini delta-v constants not yet swept; lower priority because GA options aren't in closing architecture.

A13 vehicle reliability over 7-15 years — out of scope for current framework iteration.

A5 distance-dependent power (constant scalar) — captured in `R_solar_thermal_hybrid_power/SCOPE.md`.

A6 kick-stage specific impulses — already corrected in commit `cce2810`; not high priority for re-test.

A7-A10 — Tier 2 sensitivities not yet tested.

A13 vehicle reliability over 7-15 years — out of scope for current framework iteration.

## Recommendations

1. **Set L0-04 commercial-class floor** in REQUIREMENTS.md. This is the single highest-leverage open decision.
2. **Find or measure flight-scale water-electrothermal specific impulse**. Confirm 700-900 s anchor or revise.
3. **Update LOW_THRUST_TOTAL_DV_KM_S to 22 km/s** as default. The 13 km/s anchor is unrealistic, even if the closure surface is robust to the correction.
4. **Revise the vehicle-mass anchor** in matrix/pitch documents to favor 10-50-tonne single-launch architectures.
5. **Open the assumption audit document as a living document** — keep adding tested assumptions and verdicts to it.
