# R-lowthrust-spiral-departure — R179's departure floor pairs an impulsive Δv with a low-thrust powerplant; the honest electric spiral is megawatt-class

**Status:** run + STUDY complete 2026-07-22. **4/4 HELD.** Result JSON `results/spiral_departure.json`; figure `results/spiral_departure.png`.
**Predecessor under test:** `R179 R_departure_anchor_reconciliation` (`79e5d7f`) / axis 05 — departure-physics reactor floor 155-175 kWe from a "2-year chunk-fed departure burn, direct 9.0 km/s spiral."

## Hypothesis (pre-registered; see SCOPE.md)

R179 computes the departure reactor power from a **continuous-thrust electric** powerplant (thrust = 2Pη/v_e, burn spread over 2 years) but uses a departure **Δv of 9.0 km/s** that is the **impulsive single-burn** value (`hyp_v(R_ring,v∞) − v_circ ≈ 8.5 km/s`). An impulsive burn from the circular B-ring is Oberth-efficient (fires at 18.8 km/s deep in the well). A low-thrust electric thruster cannot do that — it must spiral out, and a tangential spiral from a circular orbit to escape costs Δv ≈ v_circ ≈ 18.8 km/s (no Oberth). So R179's floor pairs an Oberth Δv with a non-Oberth propulsion system — the same impulsive-vs-continuous error axis 04 caught on the *inbound* leg, not yet applied to the departure.

## Test

Deterministic. (1) Reproduce R179's impulsive single-burn Δv and confirm 9.0 ≈ it. (2) Honest low-thrust spiral Δv: analytic escape = v_circ, **plus a direct RK4 integration of planar 2-body + constant tangential low thrust** from the circular B-ring to specific energy v∞²/2, at the *real* mission thrust-to-weight (thrust 2Pη/v_e at 175 kWe on 100 t → 2.68×10⁻⁴ m/s²) and two higher accels for the convergence trend. (3) Propagate each Δv through R179's own reactor-power formula (Isp 800 s, 2-yr burn); Isp sensitivity {800, 2000, 3000} s; the fixed-power burn-time alternative; the chemical-kick mass. Anchors identical to R179.

## Result

| Sub-claim | Predicted | Measured | Held? |
|---|---|---|---|
| H-C1 R179's 9.0 is the impulsive value | within 30 % of impulsive | impulsive **8513 m/s**, R179 9000 → **6 %** diff | ✅ |
| H-C2 honest spiral Δv ≥ 15 km/s (≥2× 9.0) | [18.8, 25.0], ≥2× | **21.9 km/s** (numerical, mission a, 2294 revs); analytic v_circ 18.8 → **2.44×** | ✅ |
| H-C3 spiral floor ≥ 500 kWe | ~810–1900 kWe | **1248 kWe** (7.13× R179's 175); or **14.3-yr** burn at 175 kWe | ✅ |
| H-C4 no Isp escape (≥1.3×) | ≥2× at all flyable Isp | ratios 7.15 / 3.54 / 3.09 at Isp 800/2000/3000 s; **min 3.09** | ✅ |

Chemical-kick escape: recovering the Oberth 8.5 km/s with a high-thrust chemical stage (Isp 350 s) needs **~1095 t of propellant** for a 100-t payload — a departure stage larger than the whole vehicle.

## Reading

**R179's 155-175 kWe departure floor is valid only if the departure is an impulsive (high-thrust/chemical) burn. Under the electric low-thrust "chunk-fed-spiral departure" the matrix actually specifies, the honest departure floor is ~1250 kWe — megawatt-class, squarely inside the retired-as-fantasy band — because a low-thrust engine cannot exploit the Oberth effect that makes the 8.5 km/s impulsive burn efficient.** The numerical spiral, run at the real mission thrust-to-weight, climbs out of Saturn's well over **2294 revolutions** and costs **21.9 km/s** — 2.44× the booked 9.0, and above even the analytic v_circ because reaching the hyperbolic v∞ (not merely parabolic) adds ~3 km/s of finite-thrust spiral. Through R179's own rocket-equation formula that is **1248 kWe**, and no flyable Isp escapes it (the power formula's v_e² cancels the propellant-mass savings — the floor is ~1050-1260 kWe across Isp 800-3000 s).

**The architecture faces four options, each of which fails a specific axis:**
1. **Accept megawatt power** (~1250 kWe): retired as fantasy (500 kWe retirement; power findings 1-4; bet #3 already ≤1.5 % programmatic). This is the direct reading and it *sharpens bet #3 by ~7× on the departure leg alone.*
2. **Hold 175 kWe, accept a ~14-year departure burn:** blows the 15-yr round-trip ceiling ([[10-round-trip-ceiling]]) by itself (before the inbound leg) and demands ~14 full-power-years of reactor life against an unmeasured Kilopower target ([[20-reactor-lifetime]]).
3. **Add a chemical departure kick stage** to legitimately claim the Oberth 8.5 km/s: ~1095 t of chemical propellant (Isp 350) for a 100-t payload — a stage larger than the vehicle, and the architecture is explicitly electric.
4. **Re-architect to an eccentric harvest orbit** (periapsis at the ring, apoapsis high) so the vehicle departs from near-escape energy: this is the honest open escape R179 did not consider — but it trades departure Δv for harvest dwell time (the bag harvests only during brief periapsis passes each multi-day orbit), and a low-thrust engine still cannot concentrate its burn at periapsis, so the recovered Δv sits between the circular-spiral (21.9) and impulsive (8.5), not at 8.5. **Named, not quantified here.**

**Honest scope (methodology lesson 9/19):** this does *not* claim R179's number is a bug — R179's *impulsive* single-burn Δv is correct, and its 175 kWe is right *for an impulsive departure*. The finding is that R179 fed that impulsive Δv through a continuous-thrust powerplant model, and the matrix's "chunk-fed-**spiral** departure" is the electric case where that pairing is invalid. The reactor-floor *number* (175 kWe) is unchanged for the chemical-departure architecture; what changes is that the **electric-spiral departure the campaign actually names cannot use it**, and its honest floor is megawatt-class.

## Revisit

Pre-registration held and the measured number (1248 kWe) came in *above* the pre-registered ~810 kWe (the v_circ-only estimate), because the numerical spiral to the hyperbolic v∞ costs 21.9 km/s, more than the v_circ escape term alone — the finite-thrust completion to v∞ adds real Δv the analytic escape bound omitted. Consistent with methodology lesson 1 (pessimistic prediction; the reality was worse than predicted) and lesson 7 (I computed the conservative v_circ anchor first in scope_bounds, then the numerical integration confirmed it is a *lower* bound). The one honest soft spot is option 4 (eccentric harvest orbit) — I name it rather than dismiss it, because a defender would push there; quantifying the harvest-dwell-vs-departure-Δv trade is the natural next round. The mission thrust-to-weight (2.68×10⁻⁴ m/s²) was derived from R179's own 175 kWe / 100 t / Isp 800, so the low-thrust regime is not an assumption — it is what R179's own numbers imply.

**Deferred (retest spec):** (a) **eccentric-harvest-orbit departure** — quantify the low-thrust departure Δv from a periapsis-at-ring / apoapsis-high harvest orbit vs the harvest-dwell penalty (the option-4 trade); (b) cross-check the spiral Δv against trajectory-bot's `edelbaum_sim` re-hosted at Saturn (an independent low-thrust integrator); (c) promote the Isp/mass spiral layer built here to `water-prop/src/waterprop/trajectory/` if reused (the STATE follow-on's original intent).

## Cross-learning

- **Forward to axis 05 (reactor-power-floor) + axis 04 (inbound-dv-accounting):** the impulsive-vs-continuous correction axis 04 applied to the *inbound* leg (2.1-4.3×) now applies to the *departure* leg too — R179's departure floor is impulsive-anchored and the electric-spiral reality is ~2.4× the Δv / ~7× the power. Integration folds this into axis 05 as a sharpening of bet #3 (with the four-options framing and the option-4 open question).
- **Backward to R179/R186:** R186 revoked the Titan *tour* lever (can't pump v∞ *up*); this round shows the *direct* departure is also far more expensive than booked when done with the electric engine the architecture specifies. The two are orthogonal and compounding: no Titan help, and the direct electric spiral is megawatt-class.
- **To the project-owner USER-NOTE on axis 05** ("skeptical we'd ever get to this power level... need to think outside the box"): this round makes that skepticism quantitatively sharper — the honest electric-departure power is not 175 kWe but ~1250 kWe. "Outside the box" options that actually attack this are: a chemical departure kick (accept a non-electric stage), an eccentric harvest architecture (option 4), or abandoning chunk-return-to-Earth for a Saturn-system depot (axis 02 waiver) where no deep-well departure is paid.
- **Methodology:** a Δv anchor is only valid paired with a propulsion mode. "9.0 km/s spiral" carried an impulsive *value* under a spiral *label*; the label and the number must agree on the thrust regime. Companion to axis-04's lesson-20 (re-derive from inputs) — here the input error is a thrust-regime mismatch, not an unverified magnitude.
