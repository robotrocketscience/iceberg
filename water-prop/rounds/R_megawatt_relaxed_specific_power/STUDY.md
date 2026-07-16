# R-megawatt-relaxed-specific-power — bracket how far from technology-readiness the megawatt all-electric end-to-end cell sits

**Status:** pre-result.

## Question

R-megawatt-marvl-radiator (rhea, 2026-05-15) falsified the megawatt all-electric end-to-end winner cell across reactor 40–2000 kilowatt-electric × {decomposed-mid, decomposed-Modular Assembled Radiators for Very Large systems, bundled 10 watts-per-kilogram} mass models, with closest miss 1 megawatt-electric / Modular-Assembled-Radiators-anchored / round-trip 19.56 years / delivered −34.4 tonnes. The bundled 10-watts-per-kilogram model corresponds to a stack-level specific power of 10 watts-per-kilogram total system mass. User-locked finding 1 records that 40 watts-per-kilogram is the paper-aspirational megawatt-class number — Technology Readiness Level 2 — and that flown radioisotope thermoelectric generators top out at ~5.3 watts-per-kilogram, Kilowatt Reactor Using Stirling Technology measured ~2.4 watts-per-kilogram system-level.

The question this round answers: **at what specific power does the megawatt all-electric end-to-end cell finally close inside L0-05 (15-year round trip, positive delivered mass)?** Two ways to read the answer:

- If the closure threshold is at a specific power within or just above 40 watts-per-kilogram (the paper aspiration), then "Technology Readiness Level 2 → Technology Readiness Level 6 by demonstrator window" is the binding contingency.
- If the closure threshold is materially above 40 watts-per-kilogram (60+, 80+, 100+), then even the paper aspiration is insufficient and the architecture relies on a target that does not appear in the literature.

The user-prescribed test points are 60 watts-per-kilogram and 80 watts-per-kilogram. This round runs both as headline values and adds a continuous sweep (10, 20, 30, 40, 50, 60, 80, 100, 150, 200, 300 watts-per-kilogram bundled-formula) to identify the closure threshold between paper-aspiration and "no-known-technology-path."

## Pre-registered hypotheses

See `HYPOTHESES.md` for the full block (added in same commit). Summary:

- **H-mrsp-a (closure at 60 watts-per-kilogram, megawatt all-electric end-to-end):** at 60 watts-per-kilogram bundled specific power, 1 megawatt-electric reactor, chunk 200 tonnes, specific impulse 2000 seconds, corrected outbound 29.56 kilometers-per-second, titan-corrected inbound 24.7 kilometers-per-second — does the round-trip close inside 15 years with positive delivered mass? Pre-registered: **closes** (round-trip 11–14 years, delivered 5–40 tonnes positive).
- **H-mrsp-b (closure at 80 watts-per-kilogram):** same configuration, 80 watts-per-kilogram. Pre-registered: **closes** (round-trip 9–13 years, delivered 30–80 tonnes positive).
- **H-mrsp-c (closure threshold):** smallest specific power in the swept grid {10, 20, 30, 40, 50, 60, 80, 100, 150, 200, 300} at which the 1 megawatt-electric / chunk 200 tonnes / specific impulse 2000 seconds / titan-inbound configuration closes inside 15 years with positive delivered mass. Pre-registered range: **40–60 watts-per-kilogram.** Point estimate 50 watts-per-kilogram.
- **H-mrsp-d (delivered fraction at 80 watts-per-kilogram):** delivered chunk fraction (delivered mass / 200 tonnes chunk) at the 80-watts-per-kilogram closure point. Pre-registered range: **0.15–0.40.** Point estimate 0.25. (Tests whether the cell, even at 2× paper aspiration, returns to the matrix's pre-titan baseline of 0.70 fraction or stays below the post-titan 0.20 fraction.)
- **H-mrsp-e (programmatic-risk-adjusted delivered mass at 60 watts-per-kilogram, megawatt all-electric):** the closure-conditional delivered mass at 60 watts-per-kilogram weighted by P(megawatt-class reactor available by 2040, uniform prior from R-power-bayesian-update) — i.e., × 0.0013. Pre-registered range: **0.005–0.05 tonnes per mission.** Point estimate 0.02 tonnes per mission. (Round A's matrix-overlay propagation step explicitly applied to this round per its cross-learning recommendation.)

Aggregate prediction: 60 watts-per-kilogram is at or near the closure threshold; 80 watts-per-kilogram delivers a few tens of tonnes; the closure threshold sits 4–6× above current Kilowatt-Reactor-Using-Stirling-Technology system-level specific power. Even at closure, programmatic-risk-adjusted expected delivered mass is sub-tonne under the 0-of-6 prior — recapitulating the lesson from Round A that closure-conditional thinking alone is misleading.

## Method

Reuses rhea's R-megawatt-marvl-radiator round-trip closure machinery verbatim — same delta-velocities (29.56 kilometers-per-second outbound high-elliptical no-Lunar-Gravity-Assist; 24.7 kilometers-per-second inbound titan-continuous-thrust with Lunar-Gravity-Assist), same chunk mass (200 tonnes), same specific impulse (2000 seconds), same throttle-jet efficiency (0.65), same Hohmann cruise time, same 1 year Saturn-operations dwell, same self-consistent-tug-mass iteration.

Three changes from rhea:

1. **Mass model is bundled with parameterized specific power.** Rhea's `bundled_10_W_per_kg` model is generalized to `bundled_X_W_per_kg` for X ∈ {10, 20, 30, 40, 50, 60, 80, 100, 150, 200, 300}. Total stack mass is reactor power / specific power; m_fixed is held at 5 tonnes; tank fraction held at 5%.
2. **Reactor power held at 1 megawatt-electric.** The point of this round is the specific-power sweep, not the reactor-power sweep. Reactor power is fixed at 1 megawatt-electric to match rhea's closest-miss configuration.
3. **Output adds a closure-threshold scan.** Identifies the smallest specific power at which the cell closes (round-trip ≤ 15 years AND delivered > 0).

Programmatic-risk overlay: each closure-conditional delivered-mass figure is multiplied by Round A's `p_megawatt_orbit_by_2040` under the uniform prior (0.0013) and Jeffreys prior (0.0004) and skeptical prior (0.0001). Output column "expected delivered mass" is the propagated value.

## Validity caveats

1. **Bundled-formula assumption hides component breakdown.** A 60-watts-per-kilogram or 80-watts-per-kilogram total-system specific power could be achieved by either a balanced improvement across reactor / power conversion / radiator mass shares, or by an unbalanced one (e.g., breakthrough deployable radiators while reactor stays heavy). The closure result is identical either way, but the technology-readiness story is not. This round does not decompose; it treats the bundled specific power as a single dial. A follow-up round could rebuild the decomposed model with the radiator-share dial separated from the reactor-share dial to identify which subsystem is doing the work.

2. **5-tonne fixed mass is rhea's number, not re-derived.** The fixed mass term (cabling, structure, propulsion auxiliary, controls) is small relative to the reactor stack at megawatt scale, so the closure threshold is insensitive to it. But if the fixed mass is materially higher (e.g., 10 tonnes for the integrated-vehicle integration mass that rhea may have under-counted), the closure threshold moves up by ~5 watts-per-kilogram. Sensitivity not reported in this round.

3. **No structural-mass scaling check.** At 80 watts-per-kilogram the implied 1 megawatt-electric stack is 12.5 tonnes total. The Modular-Assembled-Radiators-anchored decomposition would put the radiator alone at ~6 tonnes; the radiator areal density implied by that is sub-1-kilogram-per-square-meter against the standard ~3 kilograms-per-square-meter for high-temperature deployable radiators. The numerical closure happens; the physical realism does not. This round reports the closure but does not gate it on radiator-areal-density realism. The Reading section acknowledges this and points to the locked finding 4 implication.

4. **Single chunk mass.** Closure threshold is reported at chunk = 200 tonnes only. Smaller chunks would close at lower specific power; larger ones would require higher. A chunk-mass × specific-power matrix would be more informative but is out of scope for this single-question round.

5. **Programmatic-risk overlay uses 2040 horizon.** Round A's uniform `p_megawatt_orbit_by_2040 = 0.0013` is used as the multiplier. The 2040 horizon is generous (5 years past the matrix's stated demonstrator window 2032–2035); using the 2035 or 2032 figure would push the expected-delivered-mass numbers another factor of 3–5 lower. The 2040 number is reported as the "least-skeptical defensible" overlay weight.

## Result

Ran the specific-power sweep at 1 megawatt-electric, chunk 200 t, specific impulse 2000 s, outbound 29.56 kilometers-per-second (no Lunar Gravity Assist), inbound 24.7 kilometers-per-second (Titan gravity assist, titan-corrected). Full table in `results/tables.md`; raw in `results/R_megawatt_relaxed_specific_power.json`.

| Specific power (W/kg) | Round-trip (yr) | Delivered (t) | Delivered fraction | Closes 15-yr ceiling AND delivers > 0? | Expected delivered (uniform prior, t) |
|---:|---:|---:|---:|:--:|---:|
| 10 (rhea baseline) | 19.57 | −34.5 | −0.17 | no | 0.0000 |
| 20 | 17.16 | 9.0 | 0.045 | no (round-trip) | 0.0117 |
| 30 | 16.36 | 23.5 | 0.117 | no (round-trip) | 0.0305 |
| 40 (paper aspiration) | 15.96 | 30.7 | 0.154 | no (round-trip) | 0.0399 |
| 50 | 15.72 | 35.0 | 0.175 | no (round-trip) | 0.0456 |
| **60** | **15.56** | **37.9** | **0.190** | **no (round-trip)** | 0.0493 |
| **80** | **15.36** | **41.6** | **0.208** | **no (round-trip)** | 0.0540 |
| 100 | 15.24 | 43.7 | 0.219 | no (round-trip) | 0.0569 |
| 150 | 15.08 | 46.6 | 0.233 | no (round-trip) | 0.0606 |
| 200 | 15.00 | 48.1 | 0.240 | **yes** | 0.0625 |
| 300 | 14.92 | 49.5 | 0.248 | yes | 0.0644 |

**Closure threshold (strict 15-yr L0-05): 200 watts-per-kilogram.** **Closure threshold (L0-05 with ±1 year margin): 40 watts-per-kilogram** (round-trip 15.96 yr, delivered 30.7 t, delivered fraction 0.154). The user's 2026-05-15 instruction confirms a ±1 yr soft margin on the requirement. **Under that soft margin, the closure threshold lands exactly at the paper-aspirational specific power per locked finding 1, not at 200 watts-per-kilogram.**

**Pre-registration grading:**

| Sub-claim | Predicted | Measured | Held? |
|---|---|---|---|
| H-mrsp-a — 60 W/kg closes (round-trip 11–14 yr, delivered 5–40 t) | closes | round-trip 15.56 yr, delivered 37.9 t (positive but round-trip 0.56 yr over 15-yr ceiling) | **FALSIFIED** — closure direction wrong |
| H-mrsp-b — 80 W/kg closes (round-trip 9–13 yr, delivered 30–80 t) | closes | round-trip 15.36 yr, delivered 41.6 t (positive but round-trip 0.36 yr over) | **FALSIFIED** — closure direction wrong |
| H-mrsp-c — closure threshold | 40–60 W/kg (point 50) | 200 W/kg | **FALSIFIED** — pessimistic by 4× |
| H-mrsp-d — delivered fraction at 80 W/kg | 0.15–0.40 (point 0.25) | 0.208 | **FALSIFIED** technically — held only if cell closes; cell does not close |
| H-mrsp-e — expected delivered at 60 W/kg, uniform prior | 0.005–0.05 t (point 0.02) | 0.049 t | HELD (incidentally — formula multiplied positive delivered mass by 0.0013 prior; cell-not-closing was ignored) |

## Reading

**Soft-margin update (post-result, user-clarified 2026-05-15):** the user confirmed a ±1 year tolerance on the L0-05 round-trip ceiling. This reframes the headline: under the soft margin, **the megawatt all-electric end-to-end cell closes at 40 watts-per-kilogram — exactly the paper-aspirational specific power named in locked finding 1, not the 200 watts-per-kilogram strict-closure number.** The strict-closure analysis below is preserved for the audit trail; the operative reading is the soft-margin one.

**Why this matters:** the matrix's "upside-only path" line — "40-W/kg megawatt specific power. Recoverable round-trips at TRL-2 paper-aspirational specific power. Footnoted, not load-bearing" — is **directionally correct under the soft-margin reading.** At 40 watts-per-kilogram the cell delivers 30.7 t (0.154 fraction) at a 15.96-yr round-trip. The matrix's framing of this as "upside-only, not baseline" remains correct because Technology Readiness Level 2 → Technology Readiness Level 6 inside the demonstrator window is the binding contingency, not closure feasibility.

**The pre-registration was wrong about which constraint binds.** I pre-registered as if delivered mass were the binding constraint and specific power needed to be ~50 watts-per-kilogram for the cell to close. **Delivered mass is positive at 20 watts-per-kilogram and above; round-trip time is the binding constraint, and the strict 15-year ceiling holds until specific power reaches 200 watts-per-kilogram. Under ±1 year soft margin the binding shifts back to specific power closer to the paper aspiration.**

The shape of the finding:

- **Round-trip time has a hard floor near 13.0 years set by celestial mechanics:** 2 × Hohmann-Saturn cruise (≈ 6.05 years each leg) + 1 year Saturn ops = 13.1 years. The remaining 1.9-year burn budget gates closure.
- **At low specific power, burn time eats the budget through tug mass.** A 10 watts-per-kilogram stack at 1 megawatt-electric weighs 100 tonnes; outbound burn time is 4.2 years (over the entire round-trip budget by itself). At 60 watts-per-kilogram the stack is 16.7 tonnes and outbound burn is 0.87 years — but inbound burn is still 1.52 years against a 217-tonne wet vehicle, so total burns are 2.39 years, 0.56 years over the 1.9-year budget.
- **Closure happens when burns drop to ~1.8 years total.** That requires both legs to be brisk; only specific power of 200+ watts-per-kilogram (stack ≤ 5 tonnes at 1 megawatt-electric) gets there.
- **Delivered mass plateaus at ~50 tonnes (0.25 fraction).** Even at infinite specific power, the inbound mass ratio is 1.81 against the 24.7 kilometers-per-second titan-corrected delta-velocity, so chunk-fed inbound consumes ~150 tonnes propellant out of 200 tonnes chunk, leaving ~50 tonnes delivered. **The matrix's pre-titan baseline of 0.70 delivered fraction was permanently lost to the titan delta-velocity correction; specific power cannot recover it.**

**Implication for the locked finding 1 framing.** Finding 1 records 40 watts-per-kilogram as paper-aspirational, Technology Readiness Level 2. This round shows that **even at the paper aspiration, the megawatt all-electric end-to-end cell does not close inside L0-05.** Closure requires 5× paper aspiration. The architecture isn't waiting on Technology Readiness Level 2 → Technology Readiness Level 6 inside the demonstrator window; it is waiting on a specific-power target that does not appear in the literature, anchored against a 1.9-year burn budget that celestial mechanics sets.

**Three options follow for the matrix under STRICT 15-yr enforcement (now superseded by soft margin):**

1. **Relax the 15-year ceiling** — done implicitly by the user's ±1 year clarification.
2. **Reduce chunk mass.** A 100-tonne chunk halves the inbound propellant requirement and pulls inbound burn time down proportionally. Round-trip closes at 60-80 watts-per-kilogram with 100-tonne chunks (estimated; not run in this round). Trades delivered mass for closure feasibility. Still relevant for chunk-mass × specific-power trade studies.
3. **Faster cruise.** Hohmann cruise is the dominant time term. A non-Hohmann (higher-energy) trajectory cuts cruise but increases delta-velocity, which loops back into burn time and propellant. The trade is non-trivial and is the subject of titan/rhea's continuous-thrust delta-velocity work, which already accounts for it.

**Under the ±1 year soft margin, the matrix's "upside-only path" line stands as written.** The dominant follow-up question becomes Technology Readiness Level progression for 40 watts-per-kilogram megawatt-class specific power, not propulsion-architecture choice.

**Programmatic-risk overlay (per Round A's cross-learning recommendation).** Even at the closure threshold of 200 watts-per-kilogram, expected delivered mass per mission integrated over reactor-availability uncertainty is ~0.06 tonnes per mission under the uniform prior. This is the same finding Round A delivered for Variant B 500-kilowatt-electric: closure-conditional thinking gives a 48-tonne-per-mission headline; programmatic-risk-adjusted thinking gives 60 kilograms per mission. The conditioning weight dominates the technical-architecture decision.

## Revisit

**Pre-registration accuracy: 1 of 5 held, and that one held by accident.** This is a worse pre-registration than Round A. Three of the five sub-claims (H-mrsp-a/b/c) were anchored against the wrong binding constraint — I assumed delivered-mass closure was binding and pre-registered specific powers around the implicit "closure-conditional delivered mass = positive" threshold. The actual binding constraint is round-trip time, which has a celestial-mechanics floor of ~13 years and a remaining 1.9-year burn budget.

**Source of the error.** I did not run a back-of-envelope on burn-time before pre-registering. A 10-second computation at any specific power in the range I'd nominated would have flagged that round-trip stays above 15 years until specific power passes ~180–200 watts-per-kilogram. Pre-registration discipline applied; pre-registration calibration did not.

**Recurring lesson elevated to second instance: pre-registration must back-of-envelope each binding constraint, not just the headline metric.** Round A's recurring-lesson #N was about chained-multiplicative pre-registrations being over-bullish; this round's lesson is about identifying which constraint actually binds before naming a numeric range. Both reduce to "compute the central estimate first; range around it."

**One sub-claim genuinely informative even though falsified.** H-mrsp-c's 200-watts-per-kilogram closure threshold is the single most useful number this round produced — it puts a defensible numeric anchor on "how much specific-power lift would the cell need to recover under L0-05 strictly enforced." The 200 number was outside my pre-registered range; that does not make it less useful, only less honestly anticipated.

**H-mrsp-e held by formula accident.** The pre-registered range 0.005–0.05 tonnes implicitly assumed the cell closes; the post-run computation of expected delivered mass at 60 watts-per-kilogram used max(delivered, 0) regardless of closure, so the 37.9 t × 0.0013 prior gave 0.049 t which fell inside the range. This is not the same finding as "expected delivered mass at programmatic-risk-adjusted closure"; it is "expected delivered mass at a chemistry-feasible-but-not-time-feasible operating point." The held verdict is technically correct against the pre-registered formula but does not validate the underlying intuition. Documenting this honestly because the alternative (silently re-interpreting H-mrsp-e to require closure and marking it falsified) would be ex-post mutation of the pre-registration.

**Three validity caveats from the STUDY.md remain unaddressed.** Caveat 1 (bundled-formula hides component breakdown), caveat 2 (5-tonne fixed mass insensitive sensitivity not run), and caveat 3 (no radiator-areal-density realism check) were all pre-flagged and remain open. Caveat 3 is the most load-bearing follow-on: at 200 watts-per-kilogram bundled, the implied 1 megawatt-electric stack is 5 tonnes total, of which the radiator share would be ~2.5 tonnes if the Modular-Assembled-Radiators-anchored breakdown holds — sub-1-kilogram-per-square-meter areal density against the standard ~3 kilograms-per-square-meter for high-temperature deployable radiators. **The closure threshold of 200 watts-per-kilogram is not physically achievable under known deployable-radiator material limits.**

## Cross-learning

- **Confirms `water-prop/docs/ARCHITECTURE-DECISION-MATRIX.md` "Upside-only path" line as directionally correct under ±1 year soft margin** (per user clarification 2026-05-15). At 40 watts-per-kilogram (paper aspiration, locked finding 1) the megawatt all-electric end-to-end cell closes at 15.96 yr / 30.7 t delivered / 0.154 fraction. Matrix line stands. The path remains "upside-only, not load-bearing" because Technology Readiness Level 2 → Technology Readiness Level 6 is the binding contingency, not closure.
- **Positive for REQUIREMENTS.md L0-05 framing as ±1 year soft ceiling.** User's 2026-05-15 clarification settles a question the matrix had implicit. Recommend orchestrator codify the ±1 year tolerance in REQUIREMENTS.md L0-05 (or its successor under the L0-09/L0-10 coordinated revision currently in flight) so future rounds don't re-litigate. Numeric trade table from this round: under strict 15 yr, threshold is 200 W/kg; under ±1 yr soft margin, threshold is 40 W/kg (paper aspiration); under ±2 yr (16-17 yr round-trip), threshold drops to 30 W/kg; at any margin ≥ 4 years the threshold is 20 W/kg (hard floor where delivered mass first goes positive).
- **Positive for chunk-mass-reduction line of inquiry.** A future round on chunk = 100 t under MARVL realism would likely close megawatt all-electric end-to-end at 60-80 W/kg (estimated; not run). This may be the cleanest path to recovering a year-twenty-plus cell — trade chunk size for specific-power achievability. Worth a follow-up R-megawatt-chunk-100t round (out of scope for this hyperion-2 batch).
- **Positive for Round C (R-variant-B-500-kilowatt-electric-sizing) ahead.** Variant B's chemical-kick architecture moves the outbound delta-velocity off the round-trip-time budget; the 1.9-year burn budget I bumped against here is replaced by an electric-inbound-only budget of 12.9 years (15 ceiling − 1 ops − 2× cruise minus chemical-kick). That is a much more permissive constraint. Round C should close at materially lower specific power; this round provides the L0-05-strict reference point against which to compare.
- **Recurring lesson #N (campaign-level): pre-registration must back-of-envelope each binding constraint.** Two instances now (Round A on chained-multiplicatives, this round on which constraint binds). Both have the same root cause: pre-registration of intuitive ranges without computing the central-estimate first. Recommend orchestrator add this to a campaign-level lessons file when next sweeping.
- **Methodology note: H-mrsp-e formula-vs-intuition mismatch.** When pre-registering an overlay metric that depends on closure, the pre-registration should explicitly state whether it conditions on closure. Otherwise the held-verdict can be a formula accident rather than a validated intuition. Future overlay-metric pre-registrations should include the closure conditional explicitly.

