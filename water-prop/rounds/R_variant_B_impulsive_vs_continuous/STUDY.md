# R-variant-B-impulsive-vs-continuous — does the 6.42 kilometers-per-second matrix-impulsive inbound assumption survive a first-principles continuous-thrust treatment?

**Status:** pre-result.

## Question

Round C left Variant B (chemical-kick + electric-inbound) standing as the matrix's single surviving architecture cell at 500 kilowatt-electric Modular-Assembled-Radiators-anchored mass, with delivered 127.8 t / round-trip 14.53 yr. **The entire surviving-cell finding rests on the matrix-impulsive 6.42 kilometers-per-second inbound delta-velocity figure.** Round C's STUDY.md flagged this as the dominant unmodeled risk; this round closes the gap.

The architectural fiction in the matrix's surviving cell is that an *electric* inbound burn achieves the *impulsive* delta-velocity figure 6.42 kilometers-per-second. Electric thrusters are low-thrust by definition; a megawatt-class water-ion thruster at specific impulse 2000 seconds produces ~66 newtons (vs the meganewton-class thrust an impulsive chemical burn provides). The inbound burn is fundamentally a continuous-thrust burn that takes weeks to months at megawatt-class, not a periapsis-localized impulsive maneuver.

Titan's R-inbound-dv-continuous-thrust round already established the continuous-thrust inbound delta-velocity for an all-electric end-to-end inbound: **24.67–40.17 kilometers-per-second** depending on Saturn departure orbit, with the most favorable case (Iapetus-distance departure, with Lunar Gravity Assist) at 24.67 kilometers-per-second. **That is 3.8× the matrix's 6.42 figure.** Variant B has no architectural reason to be different from titan's all-electric end-to-end inbound — both use electric inbound burns at the same specific impulse 2000 seconds at Saturn.

The plausible recoveries for the chemical-kick architecture:

1. **Chemical-kick Saturn-departure** (in addition to chemical-kick trans-Saturn-injection on the outbound side). Adds another chemical kick stage at Saturn, propellant from chunk water (electrolyzed). Saves the Saturn-side spiral-out cost (3.26–16.76 kilometers-per-second depending on departure orbit). Inbound delta-velocity reduces to titan's segments 2 + 4 + 5 (heliocentric retrograde + Earth heliocentric + LEO spiral) = 23.41 kilometers-per-second pre-LGA, 21.41 with LGA.
2. **Earth aerocapture.** Saves the LEO capture spiral cost (7.67 kilometers-per-second). Inbound delta-velocity reduces to titan's segments 1 + 2 + 4 (Saturn spiral + heliocentric retrograde + Earth heliocentric) = 21.89 kilometers-per-second at high-elliptical Saturn departure pre-LGA.
3. **Both 1 and 2.** Saves both. Inbound delta-velocity reduces to segments 2 + 4 = 15.74 kilometers-per-second pre-LGA.
4. **Smaller chunk.** Reduces inbound propellant requirement and burn time; doesn't change delta-velocity figure.

Even the most optimistic recovery (option 3, both Saturn-egress chemical kick AND Earth aerocapture, with Lunar Gravity Assist) gives inbound delta-velocity ≈ 13.74 kilometers-per-second — still 2.1× the matrix's 6.42 figure.

This round computes the corrected Variant B closure under each architectural recovery and asks whether the matrix's surviving cell survives.

## Pre-registered hypotheses

See `HYPOTHESES.md` for the full block (added in same commit). Summary:

- **H-vbic-a (Variant B continuous-thrust inbound, no architectural recovery):** at high-elliptical Saturn departure with Lunar Gravity Assist (matching rhea's Variant B configuration), continuous-thrust inbound delta-velocity ∈ **24–30 kilometers-per-second.** Pre-registered point 27 kilometers-per-second. (Should match titan's 27.56.)
- **H-vbic-b (Variant B + Saturn-egress chemical kick, with Lunar Gravity Assist):** continuous-thrust inbound electric delta-velocity (segments 2+4+5 of titan's decomposition) ∈ **20–24 kilometers-per-second.** Pre-registered point 21.4 kilometers-per-second. The Saturn-egress chemical kick provides ~2.09 kilometers-per-second impulsive Saturn escape (off the electric budget) plus its own propellant and stage cost.
- **H-vbic-c (Variant B + Earth aerocapture, with Lunar Gravity Assist):** continuous-thrust inbound electric delta-velocity (segments 1+2+4 of titan's decomposition) ∈ **18–22 kilometers-per-second.** Pre-registered point 19.9 kilometers-per-second.
- **H-vbic-d (Variant B + both recoveries, with Lunar Gravity Assist):** continuous-thrust inbound electric delta-velocity (segments 2+4) ∈ **12–16 kilometers-per-second.** Pre-registered point 13.7 kilometers-per-second.
- **H-vbic-e (Round C closure under H-vbic-a):** Variant B at 500 kilowatt-electric, Modular-Assembled-Radiators-anchored mass, chunk 200 t, specific impulse 2000 s, with corrected continuous-thrust inbound delta-velocity (no architectural recovery): **does NOT close inside ±1 yr soft margin.** Pre-registered: round-trip 16–18 yr (over the 16-yr soft ceiling), delivered 0–25 t (chunk barely fuels its own return), so cell is functionally falsified.
- **H-vbic-f (Round C closure under H-vbic-d, both recoveries):** Variant B at 500 kilowatt-electric with both Saturn-egress kick AND Earth aerocapture: **closes inside ±1 yr soft margin** with delivered 80–110 t. Pre-registered point: round-trip 14.5 yr, delivered 95 t. (This is the architecture that genuinely preserves Round C's headline.)

Aggregate prediction: **the matrix's surviving Variant B cell as currently presented (single chemical kick on outbound, electric inbound at impulsive-equivalent 6.42 kilometers-per-second) is architecturally incoherent.** The corrected delta-velocity makes the cell collapse to roughly the falsified megawatt all-electric end-to-end shape. The recoverable architecture is Variant C (chemical kick on BOTH ends + Earth aerocapture); without Earth aerocapture, no recovery closes Variant B at 500 kilowatt-electric.

## Method

Reuses titan's R-inbound-dv-continuous-thrust segment decomposition verbatim (results JSON at `water-prop/rounds/R_inbound_dv_continuous_thrust/results/inbound_dv.json`). For each architecture variant, sum the relevant segments:

| Variant | Saturn spiral (1) | Helio retrograde (2) | Earth helio (4) | LEO spiral (5) | Saturn-egress kick | Aerocapture |
|---|:--:|:--:|:--:|:--:|:--:|:--:|
| A — as-stated (no recovery) | included | included | included | included | no | no |
| B — Saturn-egress kick | replaced by 2.09 km/s impulsive | included | included | included | yes | no |
| C — Earth aerocapture | included | included | included | replaced by 0 | no | yes |
| D — both | replaced | included | included | replaced by 0 | yes | yes |

Lunar Gravity Assist credit (-2.0 kilometers-per-second on Earth side) applied to all four variants per titan's protocol.

Saturn departure orbit defaults to high-elliptical 1 million kilometers (matching Round C and rhea's surviving cell). Sensitivity rows for B-ring departure (worst-case continuous-thrust) and Iapetus-distance departure (best-case) included in the results table.

For each variant, recompute Round C's Variant B closure at 500 / 750 / 1000 kilowatt-electric Modular-Assembled-Radiators-anchored mass, chunk 200 t, specific impulse 2000 s, with the corrected inbound delta-velocity. Report round-trip time, delivered mass, delivered fraction, ±1 yr soft-margin closure verdict.

## Validity caveats

1. **Titan's continuous-thrust delta-velocity is an upper bound.** Per titan's STUDY.md: "the integrated delta-velocity is the 'vanilla' continuous-thrust upper bound, accurate to within 10–20% of optimal-control trajectories at the relevant power levels." So the corrected figures could be 10–20% lower under sophisticated optimal-control trajectory shaping. This does not change the qualitative finding (matrix's 6.42 is wrong by 2–4×) but could shift quantitative closure verdicts at the margin.

2. **Saturn-egress chemical kick at 2.09 kilometers-per-second is the matrix's stated impulsive Saturn-escape figure.** Round C's caveat that the conservative chemical-kick figure (9 kilometers-per-second) is the all-electric-outbound delta-velocity, not the actual chemical-kick impulsive figure (~5 kilometers-per-second), applies symmetrically here. The inbound chemical kick is genuinely a small impulsive maneuver at periapsis (~2 kilometers-per-second) plus the Hohmann mid-course alignment (~0.1 kilometers-per-second); 2.09 is defensible.

3. **Burn-time-comparable-to-cruise-time validity break.** At the corrected continuous-thrust delta-velocity of 24.7 kilometers-per-second, inbound burn at 500 kilowatt-electric / Isp 2000 s takes ~3.5 years — comparable to half the Hohmann cruise time. The continuous-thrust derivation assumes burns are short relative to orbital periods; this assumption breaks at megawatt-class for these delta-velocities. The actual round-trip time may be longer than the simple "cruise + burn" sum implies because the cruise itself becomes powered. This caveat applies to titan's original results too. Documenting; not modeling.

4. **Earth aerocapture for Variant B is the same engineering question R-chunk-as-heat-shield raised.** That round established that ICEBERG's ballistic coefficient (~4000 kilograms-per-square-meter) is 40× higher than Mars Global Surveyor's, and there is no altitude where both the bag survives AND aerobraking pass count is tractable. Variant C/D (with aerocapture) inherit this engineering risk; this round assumes the engineering is solvable but flags it as a separate dependency.

5. **Saturn-egress chemical-kick-stage mass not modeled here.** Round C's chemical-kick stage was the OUTBOUND kick (jettisoned at Saturn arrival). Variant B/D add an INBOUND kick at Saturn departure — another chemical stage, propellant from electrolyzed chunk water. This adds ~5–10 t of additional dry mass and consumes ~5–15 t of chunk water for the impulsive Saturn-egress. The modeling assumes ~10 t dry mass + ~10 t chunk-derived propellant; sensitivity not run.

6. **No correlation between variants.** This round treats each architecture variant independently. In practice, a real ICEBERG mission would likely combine elements (e.g., Earth aerocapture + smaller chunk for redundancy). The closure surface is more permissive than what this 4-variant table reports.

## Result

Ran four-variant analysis of corrected Variant B inbound delta-velocity under titan's continuous-thrust segment decomposition. Full table in `results/tables.md`; raw in `results/R_variant_B_impulsive_vs_continuous.json`.

**Inbound delta-velocity per variant (high-elliptical 1 megakilometer Saturn departure, with Lunar Gravity Assist credit):**

| Variant | Description | Electric inbound DV (km/s) | Ratio to matrix 6.42 |
|---|---|---:|---:|
| A — as-stated (no recovery) | matches Round C's assumption physically | **27.57** | **4.29×** |
| B — chemical Saturn egress | electric handles heliocentric + LEO-spiral only | 21.41 (+ 2.09 impulsive) | 3.33× |
| C — Earth aerocapture | electric handles Saturn-spiral + heliocentric only | 19.90 | 3.10× |
| D — both recoveries | electric handles heliocentric only | **13.74 (+ 2.09 impulsive)** | **2.14×** |

**The matrix's 6.42 kilometers-per-second figure is wrong by a factor of 2.1× even under the most optimistic architectural recovery.**

**Variant B closure at 500 kilowatt-electric MARVL-anchored mass, chunk 200 t, specific impulse 2000 s:**

| Variant | Egress prop (chem, t) | Inbound prop (electric, t) | Delivered (t) | Fraction | Round-trip (yr) | Closes ±1 yr soft margin (16 yr)? |
|---|---:|---:|---:|---:|---:|:--:|
| A — as-stated | 0 | 257.4 | **0.0** (chunk fully consumed) | 0.000 | 16.92 | **no** |
| B — Saturn-egress kick | 101.3 | INFEASIBLE (electric needs 104.4 t but only 98.7 t left) | INFEASIBLE | — | — | **no** |
| C — Earth aerocapture | 0 | 167.9 | **32.1** | 0.161 | 16.32 | **no** (0.32 yr over) |
| D — both | 101.3 | 79.1 | **20.0** | 0.100 | 14.67 | **yes** |

**Departure-orbit sensitivity, Variant A at 500 kilowatt-electric:** Iapetus-distance departure gives electric inbound 24.67 km/s (best continuous-thrust case, no recovery); B-ring departure gives 38.17 km/s. Even Iapetus-distance closure: round-trip > 16 yr, delivered ≤ 0 t. **No reasonable departure orbit gives Variant A a closure.**

**Pre-registration grading:**

| Sub-claim | Predicted | Measured | Held? |
|---|---|---|---|
| H-vbic-a — Variant A inbound DV | 24–30 km/s (point 27) | **27.57 km/s** | HELD |
| H-vbic-b — Variant B inbound DV | 20–24 km/s (point 21.4) | **21.41 km/s** | HELD |
| H-vbic-c — Variant C inbound DV | 18–22 km/s (point 19.9) | **19.90 km/s** | HELD |
| H-vbic-d — Variant D inbound DV | 12–16 km/s (point 13.7) | **13.74 km/s** | HELD |
| H-vbic-e — Variant A 500 kWe does not close (round-trip 16–18 yr, delivered 0–25 t) | does not close | round-trip 16.92 yr, delivered 0.0 t, closes_soft=False | **HELD** |
| H-vbic-f — Variant D 500 kWe closes with delivered 80–110 t, round-trip ~14.5 yr | closes with delivered 80–110 t | round-trip 14.67 yr (closes), delivered **20.0 t** (well below range) | **FALSIFIED-pessimistic by 4×** |

## Reading

**The matrix's surviving Variant B cell as currently presented has no L0-05-compliant configuration once the architectural fiction of impulsive-equivalent electric inbound is dropped.** Round C's headline (127.8 t delivered, 14.53 yr round-trip at 500 kilowatt-electric) is an artifact of the matrix's incorrectly-applied 6.42 kilometers-per-second figure. Substituting the physically-correct continuous-thrust inbound delta-velocity collapses the cell.

**Three sub-findings:**

1. **Variant A (as-stated, no architectural recovery) collapses cleanly.** Round-trip 16.92 yr at 500 kilowatt-electric (0.92 yr over even ±1 yr soft margin); delivered 0.0 t (chunk fully consumed by the inbound burn). At higher reactor powers the inbound burn time shortens but delivered mass goes more negative because tug mass grows. Variant A has no closing configuration.

2. **Variant B (Saturn-egress chemical kick added) is infeasible.** The Saturn-egress impulsive kick at 2.09 kilometers-per-second consumes ~101 t of chunk water (50% of the original 200 t) before the electric inbound even begins. The remaining ~99 t of chunk is insufficient to fuel the 21.41 kilometers-per-second electric inbound burn (which needs 104 t). **The chemical-kick-both-ends architecture starves the inbound burn.** This is a genuinely surprising finding — the architectural recovery makes things worse by destroying the inbound propellant supply.

3. **Variant C (Earth aerocapture, no Saturn-egress kick) is the actual best Variant B architecture.** Delivered 32.1 t, round-trip 16.32 yr — closer to closing than Variant D (which adds Saturn-egress kick on top). Under ±2 yr soft margin instead of ±1, Variant C closes at 16.32 yr with 32.1 t delivered. **The matrix's surviving cell, properly anchored, is "Variant C: chemical-kick outbound + electric heliocentric inbound + Earth aerocapture, no Saturn-egress chemical kick."**

4. **Variant D (both recoveries) closes inside ±1 yr soft margin but delivers only 20.0 t.** The Saturn-egress chemical kick saves the Saturn-spiral-out cost (~6.16 km/s electric) but costs 101.3 t of chunk water — a bad trade. The kick saves ~50 t of electric inbound propellant but consumes ~100 t of chemical egress propellant, leaving net 50 t less delivered.

**Implication for the matrix.** Round C's "Variant B at 500 kilowatt-electric closes with substantial headroom" finding does NOT survive Round D's interrogation. The matrix's options are now:

- **Option 1 (status quo, denial):** keep matrix-impulsive 6.42 kilometers-per-second figure as the inbound delta-velocity, document the architectural-fiction caveat, present the cell as a what-if. Round C's numbers stand conditional on someone else closing the impulsive-equivalent question.
- **Option 2 (acknowledge collapse):** retire Variant B from the matrix's surviving-cell list. The matrix has NO surviving cell at conservative continuous-thrust assumptions.
- **Option 3 (commit to recovery):** make Earth aerocapture for Variant B a hard architecture-decision-matrix dependency. Update Variant B row to "Variant C: chemical-kick outbound + electric heliocentric + Earth aerocapture." Acknowledge the engineering risk per R-chunk-as-heat-shield. Reduce delivered mass headline from 127.8 t to 32.1 t per mission. Round-trip from 14.53 yr to 16.32 yr (over ±1 yr soft margin; would need ±2 yr).
- **Option 4 (smaller chunk, less ambitious):** chunk-mass reduction is the alternative recovery. At chunk = 100 t, Variant A egress prop and inbound prop both halve; the cell may close even without Earth aerocapture. Round F (R-cruise-time-optimization) or a separate R-megawatt-chunk-100t round could test this.

**The matrix should pick option 3 with the smaller chunk caveat.** Option 1 is denial; option 2 is honest but loses the campaign's only surviving cell.

**Programmatic-risk overlay.** Even at Variant C's 32.1 t conditional delivered mass, expected delivered mass under uniform Round-A prior = **0.042 tonnes per mission** (down from 0.166 in Round C). Variant B's "lower-risk surviving cell" framing from Round C survives (still 4× higher than Round B megawatt-electric closure-threshold) but the absolute number is even smaller. **170 kg of water per mission at ~$1B per mission is in the wrong order of magnitude for any commercial reading.**

## Revisit

**Pre-registration accuracy: 5 of 6 held — best of any round in the hyperion-2 batch.** The four DV-derivation hypotheses (H-vbic-a/b/c/d) all held within their pre-registered ranges, validating the segment-decomposition approach. The closure-collapse hypothesis (H-vbic-e) held cleanly: Variant A at 500 kilowatt-electric does not close, with round-trip 16.92 yr and delivered 0.0 t, as anticipated.

**The one falsification (H-vbic-f) is the load-bearing finding.** I pre-registered Variant D at 500 kilowatt-electric closing with 80–110 t delivered. Actual: 20.0 t delivered. Falsified pessimistic by 4×. Why? **The Saturn-egress chemical kick consumes ~50% of the chunk water as hydrolox propellant.** I had implicitly assumed the impulsive Saturn-egress was "free" propellant-wise — it is not; at 2.09 kilometers-per-second impulsive against ~270 t wet mass at hydrolox specific impulse 450 s, the mass ratio is 1.6, costing 100+ t of propellant.

This is the same recurring lesson #N (back-of-envelope each headline metric): I ranged "delivered mass under both architectural recoveries" without computing the chunk-water consumed by the egress kick first. A 30-second computation would have flagged that 200-t chunk cannot support both a 100-t chemical egress kick AND a 100-t electric inbound burn. **Fourth instance of the recurring lesson in four rounds.**

**The infeasibility of Variant B (Saturn-egress kick alone) is genuinely informative.** The result that the chemical-kick-both-ends architecture *starves* the inbound burn is non-obvious from intuition: one would expect adding an architectural recovery to help, not hurt. The mechanism is that the Saturn-side spiral cost (6.16 km/s electric at the high-elliptical departure orbit) is small relative to the chemical-egress propellant cost (~100 t chunk water at 2.09 km/s impulsive), so the trade is unfavorable. This finding generalizes: **chemical-kick-from-chunk-water is very expensive in chunk-water units** because hydrolox specific impulse 450 s gives small mass ratio benefits. Future Variant B variants should consider non-chunk-derived chemical (i.e., bring the egress hydrolox propellant from Earth) — but that turns into a launch-mass multiplier discussion.

**Validity caveat 1 (titan's continuous-thrust DV is upper bound) is the dominant residual uncertainty.** Per titan, optimal-control trajectories could shave 10–20% off the integrated DV. Applying 80% to Variant C's 19.90 km/s gives 15.92 km/s, which would close cleanly at 500 kilowatt-electric. The qualitative finding ("matrix-impulsive 6.42 is wrong") is robust; the quantitative closure verdict for Variant C depends on whether the optimal-control trajectory shaping is real and bookable. A future round (R-optimal-control-inbound) could close this.

**Validity caveat 3 (burn time comparable to cruise time) is at its breaking point at Variant A.** A 3.5+ yr inbound burn at 500 kilowatt-electric / 27.57 km/s effectively means the spacecraft is thrusting throughout most of the inbound cruise; the "burn + cruise" decomposition becomes meaningless. The actual round-trip-time figure may be optimistic by 1–2 yr. This pushes the closure verdict for Variant A even further into infeasibility but has limited impact on Variant C/D.

## Cross-learning

- **NEGATIVE for `water-prop/docs/ARCHITECTURE-DECISION-MATRIX.md` "Year 0–15 deployment path" Variant B cell.** Round C's headline (127.8 t delivered, 14.53 yr round-trip at 500 kilowatt-electric) is wrong because it inherits the matrix-impulsive 6.42 kilometers-per-second fiction. Recommend orchestrator update Variant B row to one of the four options in the Reading section. **Recommended: Option 3 (Variant C with Earth aerocapture, 32.1 t delivered, 16.32 yr round-trip, ±2 yr soft margin required).** Under Option 3 the delivered-mass headline drops from 127.8 t to 32.1 t — a 75% reduction in the matrix's surviving-cell delivered figure.
- **NEGATIVE for Round C's headline finding.** The four optimistic-pessimistic falsifications in Round C (delivered, expected delivered, round-trip slope, etc.) were all relative to the matrix-impulsive baseline that Round D shows is incorrect. The closure-conditional headline of "127.8 t delivered" is replaced by "32.1 t delivered (with Earth aerocapture, ±2 yr soft margin)" or "0 t delivered (without aerocapture)." The matrix's surviving cell is materially worse than Round C reported.
- **POSITIVE for R-chunk-as-heat-shield-revisit (queued).** Earth aerocapture is the dominant architecture-recovery dependency for Variant B. R-chunk-as-heat-shield previously found 40× ballistic-coefficient mismatch vs Mars Global Surveyor heritage; R-chunk-as-heat-shield-revisit was the next named round on the matrix's queue. **This round elevates that round from "speculative aerocapture analysis" to "load-bearing dependency for the entire matrix's surviving cell."**
- **NEGATIVE for the matrix's cleanly-binary "Variant B closes / megawatt all-electric does not" framing.** Both cells now collapse under conservative continuous-thrust assumptions. The matrix has either (a) no surviving cell at conservative assumptions, or (b) a surviving cell conditional on Earth aerocapture engineering being solved. There is no architecture-pure path to L0-05 compliance.
- **POSITIVE for chunk-mass-reduction R-megawatt-chunk-100t round (queued).** At chunk = 100 t, all the propellant numbers halve; Variant A may close at 500 kilowatt-electric without architectural recovery. Trades delivered mass per mission for closure feasibility — but if the alternative is "no closing cell," halving chunk size is preferable to no mission.
- **POSITIVE for non-fission-baseline rounds.** With Variant B's expected delivered mass collapsing from 0.166 to 0.042 t per mission (uniform prior), a non-fission baseline (solar-electric at 200 kilowatt-electric class with 1 AU vs 9.5 AU power scaling) only needs to clear ~0.05 t per mission expected to be commercially competitive. Bar significantly lowered.
- **Recurring lesson #N elevated to fourth instance in four rounds.** Pre-registration must back-of-envelope each headline metric, especially when chained-multiplicative or cross-stage propellant accounting is involved. I am still failing this consistently. Strongly recommend the orchestrator surface this in the campaign-level lessons file.
- **Methodology validation: segment decomposition of inbound DV is robust and reusable.** Titan's segment decomposition (Saturn-spiral / heliocentric-retrograde / heliocentric-decelerate / LEO-spiral) gave clean, reproducible numbers for each architecture variant. This decomposition should become the campaign's canonical inbound-DV reference. Recommend orchestrator add a `water-prop/docs/CANONICAL-DELTA-VELOCITIES.md` documenting the segment table and its assumptions.

