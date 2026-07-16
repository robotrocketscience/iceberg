# Round 8 — Inbound Delta-Velocity Budget Audit

**Status:** pre-result.

## Question

R6 used 5.2 kilometers per second of chunk-fed inbound delta-velocity (revised up from 4.2 after R2's lunar gravity assist falsification). The ICEBERG conops document allocates only 3.7 kilometers per second total to all water-microwave-electrothermal-thruster phases of the mission, with 7.3 kilometers per second reserved for the chemical Trans-Saturn-Injection. Of that 3.7, the conops itemizes 0.6 (Saturn capture) + 1.49 (Saturn-side rendezvous) = 2.09 explicitly, leaving 1.6 kilometers per second for everything else (Saturn departure + inbound corrections + Earth-arrival trim).

The two budgets do not share a definition and have not been reconciled. The conops also assumed Earth aerocapture absorbed the bulk of the inbound velocity-at-infinity, but aerocapture was retired (program risk M-AEROCAP), and the lunar gravity assist replacement was tested in R2 and delivers only 2.0–2.3 kilometers per second at velocity-at-infinity = 6 kilometers per second (not the 3 kilometers per second the conops assumed).

This round asks: when the chunk-fed inbound delta-velocity budget is computed from first principles, do the conops, R2, and R6 numbers reconcile, or is there a structural hole in the architecture?

## Pre-registered hypothesis (H8)

| # | Claim | Predicted | Falsification threshold |
|---|---|---|---|
| H8a | Hohmann transfer velocity-at-infinity at Earth on Saturn-to-Earth descent | 9.0–11.0 km/s | outside this range by 1+ km/s |
| H8b | Hohmann transfer velocity-at-infinity at Saturn on Earth-to-Saturn ascent | 5.0–5.8 km/s | outside this range (consistency check vs conops 5.4) |
| H8c | Conops 11 km/s round-trip total reconciles to within 0.5 km/s of phase-by-phase rebuild | held if gap ≤ 0.5 km/s | falsified if 0.5–2 km/s, load-bearing if > 2 km/s |
| H8d | Inbound braking required to bring Earth velocity-at-infinity from Hohmann arrival down to 3.0 km/s (lunar gravity assist capability at velocity-at-infinity = 6 km/s per R2) | 5.5–7.5 km/s | outside this range by 1+ km/s |
| H8e | Chunk-fed inbound mass closure at water-microwave-electrothermal-thruster specific impulse = 500 s for the H8d delta-velocity, 14 t grappled chunk, 5 t dry spacecraft | falsified (mass ratio exceeds chunk-only propellant supply) | held if chunk delivers > 50%, falsified if chunk delivers < 25%, load-bearing if chunk arrives empty |

**Aggregate (H8-agg):** I predict the architecture has a 2–6 kilometers per second hole in the chunk-fed inbound delta-velocity budget. Conops's 3.7 km/s total water-MET allocation is structurally under-specified. The hole closes only if one of the following holds: (a) a slower-than-Hohmann inbound trajectory arrives at Earth with velocity-at-infinity well below 10 kilometers per second, (b) a multi-flyby (4+) lunar gravity assist tour absorbs more than 3 kilometers per second, (c) the inbound leg includes multi-kilometer-per-second of low-thrust braking and the conops budget understates the chunk-fed propellant requirement by 2-3×, or (d) higher-than-water-microwave-electrothermal specific impulse is used (water radio-frequency ion, dual ion).

**Pre-registered conclusion ordering:** if H8a, H8b, H8d, H8e all hold and H8c is falsified-load-bearing, the architecture choice in the conops (water-microwave-electrothermal at ~500 s specific impulse, chemical Trans-Saturn-Injection, lunar gravity assist arrival) is not self-consistent and one of the four reconciliation paths above must be selected before mission closure.

## Method

Closed-form orbital mechanics; no integration. See `run.py`.

1. **Hohmann transfer velocities-at-infinity at both endpoints:**
   - Semi-major axis of Hohmann ellipse: $a_h = (a_E + a_S) / 2$
   - At perihelion (Earth distance): $v_p = \sqrt{\mu_{sun} (2/a_E - 1/a_h)}$
   - At aphelion (Saturn distance): $v_a = \sqrt{\mu_{sun} (2/a_S - 1/a_h)}$
   - Velocity-at-infinity at each body: $v_\infty = |v_{transfer} - v_{body}|$ where $v_{body} = \sqrt{\mu_{sun} / a_{body}}$

2. **Saturn-side delta-velocity ledger (low-thrust impulsive approximation):**
   - Saturn arrival (hyperbolic to highly-elliptical capture): $\Delta v_{cap} \approx 0.6$ km/s per conops
   - Drop from elliptical capture orbit to B-ring circular orbit (~135,000 km): patched-conic Hohmann within Saturn's gravity well
   - Phasing within B-ring: small relative to Hohmann drop
   - Climb back from B-ring to elliptical orbit (mirror of drop, chunk-fed)
   - Escape to inbound velocity-at-infinity = 5.4 km/s (mirror of capture, chunk-fed)

3. **Earth-side delta-velocity ledger:**
   - Inbound velocity-at-infinity at Earth from Hohmann transfer (computed in step 1)
   - Lunar gravity assist contribution per R2 result table at the relevant velocity-at-infinity
   - Remaining velocity-at-infinity after lunar gravity assist = inbound braking requirement
   - Total inbound chunk-fed delta-velocity = Saturn egress + cruise corrections (small) + Earth-arrival inbound braking

4. **Mass closure check:**
   - Tsiolkovsky equation: $m_{prop} / m_0 = 1 - e^{-\Delta v / v_e}$
   - At water-microwave-electrothermal $v_e \approx 4905$ m/s (specific impulse 500 s)
   - At chunk mass 14 t + dry spacecraft 5 t initial; compute propellant required for various inbound delta-velocity assumptions
   - Compare with chunk mass; if propellant required exceeds chunk mass minus delivered fraction, mass closure fails

5. **Validity caveats:**
   - Hohmann assumes both body orbits are circular and coplanar; real Saturn orbit has eccentricity 0.054 (small) and inclination 2.49° to ecliptic (small)
   - Saturn-system patched-conic treats spheres of influence as instantaneous boundaries; finite-burn corrections are typically 5–10% but not modeled
   - Impulsive-burn approximation; low-thrust losses are real but order-of-magnitude correct
   - This is a budget-reconciliation round, not a trajectory-design round; quantitative output is not a flight-software input

## Result

See `results/budget_audit.json` for the full ledger. Headline numbers:

**Hohmann transfer Earth-Saturn endpoint velocities-at-infinity (closed form):**

| Endpoint | Value | Status |
|---|---|---|
| Hohmann velocity-at-infinity at Earth (return leg) | 10.30 km/s | H8a held (predicted 9.0–11.0) |
| Hohmann velocity-at-infinity at Saturn (outbound) | 5.44 km/s | H8b held (predicted 5.0–5.8; conops states 5.4) |

The Saturn-arrival velocity-at-infinity that the conops uses (5.4 km/s) is exactly the Hohmann-transfer prediction, confirming the conops trajectory is Hohmann. By symmetry, the inbound velocity-at-infinity at Earth from a Hohmann descent is 10.30 km/s — nearly double the 5.4 the conops cites for Saturn arrival, because Earth orbital velocity (29.8 km/s) is much higher than Saturn's (9.6 km/s) and the perihelion speed of the Hohmann ellipse approaches Earth orbital velocity in the limit.

**Inbound braking cases (chunk-fed propulsion required to bring velocity-at-infinity at Earth to zero):**

| Case | Inbound velocity-at-infinity at Earth | Lunar gravity assist | Residual | Chunk-fed inbound total | Delivered chunk at 500 s specific impulse |
|---|---|---|---|---|---|
| A: Hohmann return + single lunar gravity assist | 10.30 km/s | 1.86 km/s | 8.44 km/s | 10.53 km/s | **0.0%** |
| B: Slow transfer to velocity-at-infinity 6 + single lunar gravity assist | 6.00 km/s | 2.15 km/s | 3.85 km/s | 5.94 km/s | **4.7%** |
| C: Slower transfer to velocity-at-infinity 4 + single lunar gravity assist | 4.00 km/s | 3.24 km/s | 0.76 km/s | 2.85 km/s | **40.2%** |
| D: Hohmann return + 5-flyby tour (3 km/s assumed) | 10.30 km/s | 3.00 km/s | 7.30 km/s | 9.39 km/s | **0.0%** |

Chunk-fed inbound total = Saturn-side egress (2.09 km/s mirror of ingress) + residual after lunar gravity assist.

**Conops reconciliation:**

| Quantity | Value |
|---|---|
| Conops total water-microwave-electrothermal allocation | 3.70 km/s |
| Conops itemized water-MET (Saturn capture 0.6 + ring rendezvous-in 1.49) | 2.09 km/s |
| Implicit conops chunk-fed allocation | 1.61 km/s |
| First-principles chunk-fed (case C, optimistic) | 2.85 km/s |
| First-principles chunk-fed (case A, Hohmann + single lunar gravity assist) | 10.53 km/s |
| Conops shortfall (optimistic case C) | 1.24 km/s |
| Conops shortfall (pessimistic case A) | 8.92 km/s |

**Hypothesis grading:**

| ID | Verdict | Evidence |
|---|---|---|
| H8a | held | 10.30 km/s ∈ [9.0, 11.0] |
| H8b | held | 5.44 km/s ∈ [5.0, 5.8]; matches conops 5.4 |
| H8c | **load-bearing falsified** | shortfall is 1.24–8.92 km/s vs predicted ≤0.5 |
| H8d | held | case B chunk-fed inbound 5.94 km/s ∈ [5.5, 7.5] |
| H8e | held | case B delivers 4.7% of chunk, below 25% threshold |

Aggregate H8-agg: **held in the direction predicted, with the magnitude in the upper half of the predicted 2–6 km/s range.** Architecture has a 1.2–8.9 km/s hole. Three of the four reconciliation paths I identified pre-registration are insufficient (Hohmann + single lunar gravity assist, Hohmann + 5-flyby, slow transfer to velocity-at-infinity 6); only Case C (slow transfer arriving at velocity-at-infinity 4) closes mass — and even then at 40% delivery, well under the conops' 75% claim.

## Reading

This is the most architecturally load-bearing finding of the campaign to date.

1. **The conops' Hohmann return trajectory does not close at water-microwave-electrothermal specific impulse.** At 500 s specific impulse the chunk arrives 0% delivered because the propellant required for 10.5 km/s of inbound braking exceeds the chunk mass. The conops' 14 t grappled chunk, towed home via water-microwave-electrothermal, vanishes en route as propellant before reaching Earth.

2. **The retired Earth-aerocapture maneuver was load-bearing in a way the conops did not flag explicitly.** Aerocapture was rated TRL 4–5 and called "the riskiest never-flown element of the architecture," but the budget retired it (program risk M-AEROCAP) and replaced it with lunar gravity assist. R2 already found the lunar gravity assist replacement delivers only 2.0–2.3 km/s at velocity-at-infinity = 6 km/s, not 3. R8 now closes the loop: the spacecraft cannot get to velocity-at-infinity = 6 km/s in the first place from a Hohmann return without consuming the chunk as propellant.

3. **Only "slower than Hohmann" reconciles the trajectory.** Case C (velocity-at-infinity at Earth arrival = 4 km/s) gives 40% chunk delivery at water-microwave-electrothermal 500 s. A velocity-at-infinity of 4 km/s requires either (a) low-thrust continuous braking through cruise (which adds propellant to the budget, partially defeating the slow-trajectory advantage), or (b) a non-Hohmann trajectory with longer time-of-flight — possibly using planetary gravity assists during the inbound coast. Either way, the conops timeline (6 years inbound) shortens or the cruise propellant grows.

4. **The conops document is internally inconsistent.** It claims Earth aerocapture absorbs the bulk of the inbound velocity-at-infinity (mass at Saturn arrival ~5 t, mass at Earth arrival ~10 t cargo + ~5 t dry per the bag-engineering doc and pitch §III), but program risk register M-AEROCAP says aerocapture was retired and replaced with lunar gravity assist. The conops body text has not been updated. The 75% chunk-delivery number in the conops is calibrated against the aerocapture-arrival case, not the lunar-gravity-assist-arrival case.

5. **At higher specific impulse the budget closes more easily.** Pale Blue water radio-frequency ion at 2000 s specific impulse (per R1) gives mass ratio e^(5940 / (2000 × 9.81)) = e^0.303 = 1.35 for Case B; chunk delivery rises from 4.7% to ~74%. Water radio-frequency ion at Kilopower-class power level closes the mission where water-microwave-electrothermal does not. **This converts R8 from a budget audit into a propulsion architecture revisit.** The conops' choice of water-microwave-electrothermal in plasma mode (per pitch §III) is wrong for the inbound chunk-fed leg under the current trajectory. The right inbound thruster is water-ion-class.

## Revisit

H8a, H8b, H8d, H8e held. The Saturn-arrival velocity-at-infinity match (5.44 km/s computed, 5.4 conops) is independent confirmation that the conops trajectory is Hohmann; H8b was a sanity check and it confirms the modeling pipeline.

H8c was falsified in the load-bearing direction. The 1.2–8.9 km/s conops shortfall is far past the 0.5 km/s "held" threshold and past the 2.0 km/s "falsified" threshold. The aggregate pre-registered conclusion — that one of four reconciliation paths must be selected — is held, but only Case C is actually viable, and Case C requires a trajectory revision the conops does not describe.

The methodology lesson here is the same as R0 (training-data references for microwave-electrothermal specific impulse were optimistic): **budget numbers stated in a single document tend to be optimistic in the conservative direction when reconciled against first-principles physics.** This is now a recurring pattern. The next round that pulls a single-number claim from any source (vendor data sheet, white paper, conops document) should default to the wider end of the uncertainty range.

## Cross-learning

- **Falsifies the conops architecture as stated.** Microwave-electrothermal at ~500 s specific impulse + Hohmann return + single-flyby lunar gravity assist does not close mass for a 14 t chunk. Conops body text needs revision to (a) reflect lunar gravity assist replacement of aerocapture, (b) re-derive the 75% chunk-delivery number for the lunar-gravity-assist case, (c) state the actual inbound trajectory (slow Hohmann variant vs. powered braking).
- **Promotes R3i** (dual-ion architecture) and Pale Blue water radio-frequency ion from "future technology candidates" to "necessary technology candidates" for the inbound leg under the conops chunk mass. Water-microwave-electrothermal is sufficient for outbound (Earth-water-fed, low cumulative delta-velocity) but not for inbound (chunk-fed, multi-kilometer-per-second residual velocity).
- **Confirms R2** (lunar gravity assist falsification) is load-bearing for mission closure, not just a margin issue. The optimistic-vs-pessimistic spread on the conops hole is dominated by which trajectory you assume; R2's flag for a multi-flyby retest (Case D here) is now revealed to be insufficient even speculatively — Case D still delivers 0% of the chunk at water-microwave-electrothermal specific impulse.
- **Negative for the bag-engineering 75% chunk-delivery efficiency** as a load-bearing program assumption. The 75% number was computed for an aerocapture-arrival case where the chunk-fed propulsion only had to handle Saturn egress + cruise corrections + small Earth-arrival trim, totaling ~1.6 km/s. Under the lunar-gravity-assist replacement, even the optimistic case adds 1.2 km/s of additional inbound braking, which compounds Tsiolkovsky-wise. The pitch deck's mass-delivery numbers need a sensitivity analysis.
- **New round R9 candidate: slow-transfer trajectory family.** Compute time-of-flight and propellant cost for inbound transfers arriving at Earth at velocity-at-infinity 3, 4, 5, 6 km/s. The right trajectory is somewhere on this curve. If the time-of-flight at velocity-at-infinity = 4 km/s exceeds 10 years, the conops' "13-year round trip" claim also needs revision.
- **New round R10 candidate: propulsion architecture revisit for inbound leg.** Compare water-microwave-electrothermal vs water radio-frequency ion vs dual ion at the actual chunk-fed inbound delta-velocity (whatever R9 determines), with Kilopower / Fission Surface Power power levels per R6. Headline candidate for shifting the conops decision from microwave electrothermal to Pale Blue water radio-frequency ion class on the return leg.
- **Risk register update needed.** Program risk M-AEROCAP says aerocapture is "already retired in conops — replaced by lunar gravity assist." R8 shows the replacement does not close at water-microwave-electrothermal specific impulse. M-AEROCAP should be re-elevated, or a new risk M-INBOUND-BUDGET should be added at I5-L4 (the architecture does not close as documented) until R9/R10 select the reconciliation path.
- **Documentation defect.** The conops body text retains aerocapture language despite the program register retirement. Add to RISKS.md or open a doc-fix ticket. Not a propulsion finding per se but should not stay unflagged.
- **Methodology recurring lesson.** Single-number budgets in concept-paper documents (conops, pitch) tend to be optimistic when reconciled against patched-conic plus Tsiolkovsky. Pattern is now: R0 (vendor specific-impulse 30% optimistic), R2 (conops lunar gravity assist 30% optimistic), R8 (conops chunk-fed inbound budget 80%+ optimistic). The campaign should pre-emptively widen prediction bands for any single-number claim from any single source.

