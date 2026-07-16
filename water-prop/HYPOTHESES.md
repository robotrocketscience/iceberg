# Pre-Registered Hypotheses — water-prop campaign

Per protocol section 4. Each round's numeric prediction is written **before** the run. The Revisit clause in each round's STUDY.md grades whether the prediction held.

## Aggregate prediction (mission-level)

I predict the campaign concludes that **the highest-delivered-mass propulsion technology depends on chunk mass**:

- For small chunks (5–50 tons), high-specific-impulse low-thrust technologies (water radio-frequency ion, water Hall, or hydrogen ion via electrolysis) win because thruster mass and Tsiolkovsky losses are small relative to chunk mass.
- For medium chunks (50–200 tons), the Pareto frontier is mixed — microwave electrothermal at lower specific impulse and lower power, vs water ion at higher specific impulse and higher power.
- For large chunks (200–500+ tons), the binding constraint shifts to available power, which gates specific impulse from above (per the round 0 / round 1 finding). Microwave electrothermal at low specific impulse may win because it produces useful thrust at lower power than ion or Hall.

I predict the campaign does **not** produce a single-winner architecture — it produces a Pareto surface in (chunk mass × propulsion technology × power class) with explicit selection criteria per regime.

I predict that electrolysis-to-hydrogen-ion is **not** competitive for the ICEBERG return leg unless the oxygen byproduct can be productively consumed (oxygen-resistojet for reaction control or other secondary thrust). Naively venting the oxygen loses 89% of the harvested water mass and dominates any specific-impulse advantage.

I predict at least one of my baked-in assumptions will be wrong by a factor of 2 or more — most likely the total electrical-to-jet efficiency for water ion or water Hall thrusters. Round 4 is sized to surface this.

---

## Round 0 — microwave electrothermal thruster frozen-flow ceiling (already run)

Round 0 was run before this protocol was adopted. Its hypothesis is being reconstructed retrospectively from the round 1 / round 2 stage docs for audit-trail completeness. **Not a fresh pre-registration.**

**Reconstructed hypothesis:** real-world water-microwave-electrothermal specific impulse sits in the 700–1000 second band per training-data references.

**Reading after the fact:** falsified in the conservative direction. The Cantera shifting-equilibrium upper bound at realistic operating conditions (chamber temperature 7000 K, chamber pressure 100 torr) is 558 seconds; frozen-flow lower bound is 416 seconds. Realistic real-world value sits in 480–520 seconds, well below the original 700–1000 estimate. Round 1 / round 2 stage docs updated to reflect this.

---

## Round 1 — citation verification (not yet run)

**Hypothesis (H1):** Across the citations I have used in round 1 / round 2 stage docs without verification, I predict:

| Claim | My current value | Predicted real value (range) | Source to verify |
|---|---|---|---|
| Penn State water-microwave-electrothermal published specific impulse | 500–800 seconds | 400–800 seconds | Micci / Bilén papers |
| Tethers Unlimited HYDROS-C demonstrated specific impulse | 310 seconds | 250–350 seconds | Tethers Unlimited published data |
| Pale Blue water ion thruster specific impulse | 800–1500 seconds | 500–1500 seconds | Koizumi / Komurasaki publications |
| Hydrogen permeation through 316 stainless steel at room temperature | 10⁻⁹ mol/(m²·s·√Pa) | 10⁻¹⁰ to 10⁻⁸ mol/(m²·s·√Pa) | Aceves / Sandia data |
| NASA Kilopower / KRUSTY specific power | 1–10 kilowatts electrical | 1–10 kilowatts electrical (per design class) | NASA Glenn reports |
| B-ring water-ice fraction | 92–98% | 92–98% | Cassini / Hedman publications |
| B-ring max particle diameter | ~10 meters | 5–20 meters | Cuzzi 2010 / Tiscareno |

**Prediction grading:** held if the real value falls inside the predicted range; wrong-but-informative if outside by less than 2×; wrong-and-load-bearing if outside by 2× or more (triggers a follow-up round on whatever model used the wrong number).

**Predicted aggregate:** I predict 1–3 of the 7 claims above will be falsified beyond the predicted range. Most likely candidates: water ion specific impulse (could be lower than the open-literature suggests for real long-duration operation), Aceves hydrogen permeation (might be off by an order of magnitude either way).

**Test:** WebSearch + WebFetch for each citation. No code; results captured in `rounds/R1_citation_verification/results/citations.md` as a table of (claim, predicted, found, source, held?).

---

## Round 2 — lunar gravity assist trajectory analysis (not yet run)

**Hypothesis (H2):** For an ICEBERG inbound spacecraft arriving from Saturn at v-infinity 6 kilometers per second relative to the Moon, a 3-flyby lunar gravity assist tour:

| Metric | Predicted value (range) | Reasoning |
|---|---|---|
| Maximum delta-v per flyby at v-infinity = 6 km/s, 100 km flyby altitude | 1.5–2.0 km/s | Closed-form: 2 × v_inf × v_moon / (v_inf + v_moon), with degradation for finite turn angle |
| 3-flyby total delta-v at favorable lunar geometry (small relative inclination) | 2.5–4.0 km/s | Conops claims 3 km/s; predicted as held but uncertain |
| 3-flyby total delta-v at worst lunar geometry (max inclination, opposite nodes) | 1.0–2.0 km/s | Below the conops claim of 3 km/s — would shift propulsion budget |
| Mid-course correction budget at worst geometry | 50–300 m/s | To bend the trajectory into the lunar orbital plane |
| Fraction of arrival epochs that meet the 3-km-per-second target | 60–85% | Driven by 18.6-year lunar nodal regression cycle |

**Predicted aggregate:** I predict the conops claim "3 km/s at zero propellant cost" is held at favorable arrival epochs but falsified at unfavorable arrival epochs, with the worst case requiring 100–300 m/s of additional propulsive trim. **This would not kill the architecture**, but it would tighten the propulsion budget by ~5% during unfavorable years.

If maximum per-flyby delta-v falls below 1 km/s at v-infinity = 6 km/s — falsified hypothesis, **architecture revisit required.** Would mean the conops claim is structurally unachievable, not just geometry-sensitive.

**Test:** scipy-based patched-conic two-body integration. Vary arrival v-infinity (4 to 8 km/s), flyby altitude (100 to 5000 km), lunar nodal phase (full 18.6-year cycle). Output: distribution of delivered delta-v across the parameter space.

---

## Revisit log

(Each round's Revisit clause feeds back here when the round closes. Empty until round 1 completes.)

| Round | Hypothesis ID | Held? | Wrong direction / magnitude | Round-level lesson |
|---|---|---|---|---|
| R0 | reconstructed | falsified-conservative | overestimated specific impulse by ~30% | training-data references for microwave electrothermal were optimistic |
| R1 | H1 aggregate | held | 2 of 7 falsified-informative, both with under-spread uncertainty bands | training-data Isp references show systematic optimistic bias; widen ranges in future hypotheses |
| R2 | H2 aggregate | **falsified** | conops 3 km/s lunar gravity assist claim is ~30% optimistic at v_∞=6 km/s; real model gives 2.0–2.3 km/s | inbound chunk-fed delta-V revises from 4.2 km/s to ~5.2 km/s; propagates back into every candidate's delivery numbers |
| R3i | (exploratory, no pre-registration) | n/a | dual-ion at 1 kV delivers 97% chunk fraction at 275 kWe; reactor mass overhead dominates trade for chunks <100 t | high-Isp wins are real but reactor mass at 5 W/kg is load-bearing — should be added to all future round delivery-fraction calcs |
| R8 | H8 aggregate; H8c specifically | held in predicted direction; **H8c load-bearing falsified** | conops 1.6 km/s implicit chunk-fed allocation vs first-principles 2.85–10.5 km/s; gap is 1.2–8.9 km/s, well above the 2 km/s load-bearing threshold | single-number budgets in concept-paper documents are systematically optimistic against first-principles physics; this is the third such finding in the campaign (R0, R2, R8); pre-emptively widen prediction bands for any single-number claim from any single source |
| R10 | H10 ranking + H10b + H10f | partial — H10a/c/d/e held; **H10b and H10f falsified** | C2 (microwave electrothermal) delivers 0% chunk (not 0.5–5%) once reactor mass is included; C6 (split-prop) delivers 40% (not 70–90%) because Saturn egress at 500 s consumes ~60% of the chunk before inbound braking starts | recurring lesson #4: every Tsiolkovsky delivery-fraction calculation in this campaign must include reactor + dry + payload mass as Tsiolkovsky initial mass — R6 silently omitted this and the omission propagated through R8 |
| R-NPV | H-NPV-agg + sub-claims a..g | aggregate **held**; H-NPV-a/d/e held; H-NPV-b/c/f/g held with terminal value but under-spread without it | best-case audited cell IRR is 3.63% (no TV) / 6.97% (with perpetuity TV) — sovereign-bond territory, never commercial-equity territory; 0 of 90 cells NPV-positive at 10% commercial discount | recurring lesson #5: every cashflow round must report NPV at multiple discount rates, IRR, and terminal-value sensitivity — undiscounted "year 40 break-even" is operationally misleading |
| R-cadence | H-cad-agg + sub-claims a..h | aggregate **held** (cadence not commercial-equity-promoting), but H-cad-d/e/f load-bearing **falsified — wrong direction** | maximum IRR lift from cadence alone is +0.55pp at N=2 compressed; higher cadences anti-optimal because schedule compression denies late-launching ships access to late-era megawatt-class reactor | lessons #6 (sweep before promoting a "largest lever" claim from first-principles intuition) and #7 (reactor-era must be a free axis, not a function of launch year — R15-rerun's `reactor_era_for_launch_year()` conceals a load-bearing coupling) |

---

## Round 10 — Inbound propulsion architecture revisit (post-result)

**Pre-registered claims** (Kilopower 10 kWe / Case B 5.94 km/s chunk-fed):

| Sub-claim | Predicted | Falsification threshold |
|---|---|---|
| H10a — C1 water resistojet (200 s) | 0% delivery (≤ 0.1 t) | held if ≤ 0.1 t |
| H10b — C2 water microwave electrothermal (500 s) | 0.5–5% delivery | held if ∈ [0.014, 0.7 t] |
| H10c — C3 water Hall (1500 s) | 40–65% delivery | held if ∈ range |
| H10d — C4 water radio-frequency ion (2000 s) | 60–80% delivery | held if ∈ range |
| H10e — C5 water dual-ion (5000 s) | 80–95% delivery | held if ∈ range |
| H10f — C6 split-prop (water egress + Hall-xenon inbound) | 70–90% delivery | held if ∈ range |

**Ranking pre-registration:** C5 > C4 ≈ C6 > C3 > C2 > C1.

**Test:** closed-form Tsiolkovsky + R6 power-optimal framework + R1 reactor mass overhead. See `rounds/R10_inbound_propulsion_revisit/run.py`.

**Measured (Kilopower / Case B):** H10a 0.0% (held); **H10b 0.0% (falsified — reactor mass closes the window)**; H10c 50.2% (held); H10d 60.8% (held); H10e 82.9% (held); **H10f 40.0% (falsified — Saturn egress at 500 s consumes 60% of chunk before inbound)**. Actual ranking C5 > C4 > C3 > C6 > C2 = C1. **Architectural decision: replace microwave electrothermal with water radio-frequency ion (Pale Blue class) for both Saturn egress and inbound braking.**

---

## Round 8 — inbound delta-velocity budget audit (post-result)

**Pre-registered claims:**

| Sub-claim | Predicted range | Falsification threshold |
|---|---|---|
| H8a — Hohmann velocity-at-infinity at Earth | 9.0–11.0 km/s | outside ±1 km/s |
| H8b — Hohmann velocity-at-infinity at Saturn | 5.0–5.8 km/s | outside ±0.3 km/s; consistency check vs conops 5.4 |
| H8c — conops total vs first-principles gap | ≤0.5 km/s held | 0.5–2 km/s falsified; >2 km/s load-bearing |
| H8d — inbound chunk-fed delta-velocity case B | 5.5–7.5 km/s | outside ±1 km/s |
| H8e — mass closure case B at 500 s specific impulse | <25% delivered | held if >50% delivered; load-bearing if 0% delivered |

**Test:** closed-form patched conic + Tsiolkovsky. See `rounds/R8_inbound_dv_budget/run.py` and `STUDY.md`.

**Measured:** H8a 10.30 km/s (held), H8b 5.44 km/s (held; matches conops 5.4), H8c 1.24–8.92 km/s gap (load-bearing falsified), H8d 5.94 km/s (held), H8e 4.7% delivered (held). Aggregate held in the predicted direction with magnitude in the upper half of the predicted range.

---

## Round R-power-base-rate — Bayesian prior on space-fission reactor arrival year (pre-result)

**Motivation.** R-power-wonder (May 2026) surfaced a hard base-rate: zero US space-fission programs have reached orbit within their originally-stated decade since 1965. Six programs (SP-100, Project Timberwind, Prometheus/JIMO, Kilopower flight, DARPA DRACO, NASA Fission Surface Power) consumed ~$1.7 billion post-SNAP-10A with zero orbital outcomes. The architecture decision matrix's R15-rerun baseline pins megawatt arrival at year 20 and R-reactor-roadmap's H-rxr-agg parameterizes the IRR curve assuming megawatt arrival is *certain* at each swept year. This round computes the actual probability distribution over reactor-arrival year given the base rate and current Fission-Surface-Power (FSP) program state.

**Pre-registered hypotheses (H-pbr).** Years are measured forward from January 2026.

| Sub-claim | Predicted range | Falsification threshold |
|---|---|---|
| H-pbr-a — P(any US space-fission system in orbit by end of 2032) | 5–20% | outside range |
| H-pbr-b — P(any US space-fission system in orbit by end of 2035) | 15–40% | outside range |
| H-pbr-c — P(40+ kilowatt-electric system in orbit by end of 2035) | 5–25% | outside range |
| H-pbr-d — P(megawatt-class system in orbit by end of 2040) | 2–10% | outside range |
| H-pbr-e — P(megawatt-class system in orbit by end of 2045) | 5–20% | outside range |
| H-pbr-f — Median (P=0.5) megawatt-arrival year, measured from 2026 | 22–35 years (i.e. 2048–2061) | outside range |
| H-pbr-g — P(megawatt-class system by year 20, R15-rerun baseline assumption) | 1–8% | outside range |

**Aggregate (H-pbr-agg).** The R15-rerun assumption that megawatt is available at year 20 with certainty has actual posterior probability under 10%. Median megawatt arrival lies more than a decade later than R15-rerun assumes. Any IRR result conditional on year-20 megawatt access is therefore an upper bound on a Bayesian-marginal IRR distribution, not a baseline; the marginal IRR (integrating over P(megawatt-arrival-year)) is at least 2 percentage points below the point estimate at year-20-certain.

**Method.** Beta(α=1, β=7) prior on per-decade-program success rate (0-of-6 base rate, plus 1 prior pseudo-count to keep the distribution non-degenerate). Convert to annual hazard. Update with FSP-specific likelihood: Phase 1 awarded 2022, extended 2024, Duffy directive Aug 2025, Draft AFPP Aug 2025, no Phase 2 contract as of May 2026. Forward Monte Carlo: 10,000 trajectories. For each, sample (a) whether the next program-attempt succeeds, (b) time-to-next-attempt given current attempt outcome, (c) megawatt-arrival year given prior reactor-class flights. Output: cumulative distribution function over arrival-year per reactor class.

**Validity caveats.** Base rate is small-N (6 programs). Two structural changes since the base rate was set could push the posterior in either direction: (a) commercial small-modular-reactor industry maturation provides more vendor capacity than the SP-100 era; (b) FY2026 budget request zeroed NEP/NTP lines, removing a procurement vehicle Prometheus/JIMO had. Round documents both biases and treats the central estimate as the geometric mean.

**Test.** `rounds/R_power_base_rate/run.py`. Deterministic with `seed=0` for the Monte Carlo. Sub-minute wall clock. Outputs cumulative-distribution tables in `results/`.

---

## Round R-power-bayesian-update — three-prior sensitivity bracket on the same posterior, plus matrix programmatic-risk overlay (pre-result; hyperion-2 batch)

**Motivation.** R-power-base-rate's headline (9.1% P(any United States fission orbit by 2035)) is a single-prior result against Beta(1, 7). This round (a) sweeps three priors against the same 0-of-6 likelihood and same Fission-Surface-Power-specific multiplier set to bracket how much the headline depends on prior choice, and (b) produces a matrix programmatic-risk overlay (`results/matrix_overlay.json`) that the orchestrator can drop into the architecture decision matrix as an "expected delivered mass per mission integrated over reactor-availability uncertainty" column.

**Pre-registered hypotheses (H-pbu).** All probabilities measured at base year 2026. Demonstrator window 2032–2035 per matrix's stated horizon.

| Sub-claim | Predicted range | Point estimate | Falsification threshold |
|---|---|---|---|
| H-pbu-a — uniform Beta(1, 1) posterior P(any United States fission orbit by 2035) | 7–14% | 10% | outside range |
| H-pbu-b — Jeffreys Beta(0.5, 0.5) posterior P(any United States fission orbit by 2035) | 4–9% | 6% | outside range |
| H-pbu-c — skeptical Beta(0.5, 5) posterior P(any United States fission orbit by 2035) | 2–6% | 3.5% | outside range |
| H-pbu-d — bracket ratio (uniform / skeptical) at 2035 horizon | 2.0–4.5 | 2.9 | outside range |
| H-pbu-e — Variant B 500-kilowatt-electric chemical-kick + electric-inbound expected delivered mass under uniform prior (programmatic-risk-adjusted) | 10–35 t per mission | 18 t | outside range |

**Aggregate (H-pbu-agg).** Prior choice moves headline 2–4×; uniform prior is the most defensible-to-skeptics single number per the user's prior-choice response; the matrix's surviving Variant B cell delivers programmatic-risk-adjusted mass under 25 t per mission across all three priors. The matrix's current "90 t conditional on reactor available" presentation overstates expected delivered mass by 4–10× when the reactor-availability conditioning weight is propagated.

**Method.** Reuses upstream R-power-base-rate Monte Carlo machinery verbatim (10,000 trajectories per prior, seed = 0). Three priors swept: Beta(1, 1) → Beta(1, 7); Beta(0.5, 0.5) → Beta(0.5, 6.5); Beta(0.5, 5) → Beta(0.5, 11.5), all updated against the 0-of-6 likelihood. Identical Fission-Surface-Power-specific likelihood multipliers and identical megawatt-conditional-on-Fission-Surface-Power machinery to the upstream round; new 500-kilowatt-electric-class chain (P(funded | Fission-Surface-Power) = 0.6, gap mean 4 years) for the Variant B overlay.

**Validity caveats.** Inherits all upstream R-power-base-rate caveats (small-N base rate, structural-change biases, independence assumption, no upside from non-United-States programs, R-reactor-roadmap pre-result). Skeptical prior could be argued harder either way (Beta(0.5, 10) twice as skeptical, Beta(2, 6) treats SNAP-10A as worth two pseudo-successes); bracket width is itself a defensibility question this round does not close. Matrix overlay uses central-estimate multiplication, not full convolution, so understates total uncertainty.

**Test.** `rounds/R_power_bayesian_update/run.py`. Deterministic with `seed=0` (per-prior sub-seed derived deterministically from prior name). Sub-minute wall clock. Outputs `results/R_power_bayesian_update_summary.json` and `results/matrix_overlay.json`.

---

## Round R-megawatt-relaxed-specific-power — bracket how far above paper aspiration the megawatt all-electric end-to-end cell sits (pre-result; hyperion-2 batch)

**Motivation.** Locked finding 1 records 40 watts-per-kilogram as paper-aspirational megawatt-class specific power, Technology Readiness Level 2. Rhea's R-megawatt-marvl-radiator falsified the cell at 10 watts-per-kilogram bundled. This round sweeps specific power continuously from 10 to 300 watts-per-kilogram (with headline 60 and 80 per the user's brief) at 1 megawatt-electric / chunk 200 tonnes / specific impulse 2000 seconds and identifies the closure threshold for round-trip ≤ 15 years AND delivered mass > 0. Result feeds the matrix's "upside-only path" line.

**Pre-registered hypotheses (H-mrsp).**

| Sub-claim | Predicted range | Point estimate | Falsification threshold |
|---|---|---|---|
| H-mrsp-a — 60 W/kg cell closes inside L0-05 | round-trip 11–14 yr, delivered 5–40 t | closes | round-trip outside range OR delivered outside range OR cell does not close |
| H-mrsp-b — 80 W/kg cell closes inside L0-05 | round-trip 9–13 yr, delivered 30–80 t | closes | round-trip outside range OR delivered outside range OR cell does not close |
| H-mrsp-c — closure threshold (smallest swept specific power that closes) | 40–60 W/kg | 50 W/kg | outside range |
| H-mrsp-d — delivered fraction at 80 W/kg | 0.15–0.40 | 0.25 | outside range |
| H-mrsp-e — programmatic-risk-adjusted delivered mass at 60 W/kg, uniform prior from Round A | 0.005–0.05 t/mission | 0.02 t/mission | outside range |

**Aggregate (H-mrsp-agg).** 60 watts-per-kilogram is at or near the closure threshold; the threshold sits 4–6× above current Kilowatt-Reactor-Using-Stirling-Technology system-level specific power. Even at closure, programmatic-risk-adjusted expected delivered mass is sub-tonne under the 0-of-6 prior — recapitulating Round A's lesson that closure-conditional thinking is misleading without conditioning weights.

**Method.** Reuses rhea's R-megawatt-marvl-radiator round-trip closure machinery (self-consistent tug-mass iteration, corrected delta-velocities 29.56 / 24.7 kilometers-per-second, chunk-fed wet-at-start inbound, Hohmann cruise + 1-year Saturn ops, throttle-jet efficiency 0.65). Mass model is bundled with parameterized specific power (10, 20, 30, 40, 50, 60, 80, 100, 150, 200, 300 watts-per-kilogram). Reactor power held at 1 megawatt-electric. Programmatic-risk overlay multiplies closure-conditional delivered mass by Round A's `p_megawatt_orbit_by_2040` per prior (uniform 0.0013, Jeffreys 0.0004, skeptical 0.0001).

**Validity caveats.** Bundled formula hides component breakdown (radiator-share dial not separately tested); 5-tonne fixed mass is rhea's number not re-derived; no radiator-areal-density realism check (200 W/kg implies sub-1-kilogram-per-square-meter areal density vs ~3 standard); single chunk mass (200 t); programmatic-risk overlay uses 2040 horizon (generous vs matrix's 2032–2035 demonstrator window).

**Test.** `rounds/R_megawatt_relaxed_specific_power/run.py`. Deterministic. Sub-second wall clock. Outputs `results/R_megawatt_relaxed_specific_power.json` and `results/tables.md`.

---

## Round R-variant-B-500kWe-sizing — clean closure on the chemical-kick + electric-inbound surviving cell at 500, 750, 1000 kilowatt-electric (pre-result; hyperion-2 batch)

**Motivation.** Rhea's R-megawatt-marvl-radiator left Variant B (chemical-kick + electric-inbound) standing as the single surviving architecture cell at ≥ 500 kilowatt-electric under MARVL-anchored mass, but reported only "closes" without the numeric headlines. This round produces round-trip time, delivered mass, propellant split, and stage masses at 500 / 750 / 1000 kilowatt-electric, plus low-Earth-orbit launch-mass under conservative (9 kilometers-per-second) and realistic (5 kilometers-per-second) chemical-kick delta-velocity scenarios. Programmatic-risk overlay propagated per Round A.

**Pre-registered hypotheses (H-vbs).** All against conservative 9 kilometers-per-second chemical-kick scenario.

| Sub-claim | Predicted range | Point estimate | Falsification threshold |
|---|---|---|---|
| H-vbs-a — 500 kilowatt-electric round-trip time | 12.5–14.5 yr | 13.5 yr | outside range |
| H-vbs-b — 500 kilowatt-electric delivered mass | 80–110 t | 95 t | outside range |
| H-vbs-c — 1000 kilowatt-electric slope (round-trip 12.0–13.5 yr AND delivered 100–125 t) | both ranges | round-trip 12.7 yr / delivered 110 t | either range outside |
| H-vbs-d — 500 kilowatt-electric LEO mission-1 launch mass (conservative kick) | 350–550 t | 450 t | outside range |
| H-vbs-e — 500 kilowatt-electric expected delivered mass, uniform prior from Round A | 0.10–0.15 t/mission | 0.12 t/mission | outside range |

**Aggregate (H-vbs-agg).** Variant B at 500 kilowatt-electric closes with ~13–14 yr round-trip and ~95 t delivered, giving a clean technical-conditional headline that the matrix can quote alongside its programmatic-risk-adjusted ~0.12 t / mission expected value. Slope to 1000 kilowatt-electric is shallow.

**Method.** MARVL-anchored mass model (rhea, decomposed-MARVL parameters). Three-stage Variant B: chemical kick (hydrolox, specific impulse 450 s, jettisoned at Saturn arrival), tug dry mass, chunk-fed electric inbound at the matrix-impulsive 6.42 kilometers-per-second (preserved by chemical-kick architecture per rhea's footnote). Round-trip = 2 × Hohmann cruise + 1-yr Saturn ops + electric inbound burn (chemical kick is impulsive, off-budget). Closure interpreted with ±1 year soft margin per user clarification 2026-05-15.

**Validity caveats.** Conservative chemical-kick 9 kilometers-per-second is upper bound (realistic 5 kilometers-per-second reported separately); matrix-impulsive 6.42 kilometers-per-second inbound is architectural-aspirational (caveat 2 — dominant unmodeled risk); chemical-stage dry mass 10 t inherited from R_chunk_fed_chemical, not re-derived; no Lunar Gravity Assist credit (would double-count Saturn-system Oberth bonus already in 6.42 figure); Round A 500-kilowatt-electric scale-up parameters (P=0.6, 4-yr gap) author-asserted.

**Test.** `rounds/R_variant_B_500kWe_sizing/run.py`. Deterministic. Sub-second wall clock. Outputs `results/R_variant_B_500kWe_sizing.json` and `results/tables.md`.

---

## Round R-variant-B-impulsive-vs-continuous — does the matrix-impulsive 6.42 km/s inbound delta-velocity assumption survive a first-principles continuous-thrust treatment? (pre-result; hyperion-2 batch)

**Motivation.** Round C left Variant B (chemical-kick + electric-inbound) standing as the matrix's surviving cell with delivered 127.8 t / round-trip 14.53 yr at 500 kilowatt-electric. The entire result rests on the matrix-impulsive 6.42 kilometers-per-second inbound delta-velocity figure. Electric thrusters are low-thrust; an electric inbound burn cannot be impulsive. Titan's R-inbound-dv-continuous-thrust already showed continuous-thrust electric inbound is 24.7–40.2 kilometers-per-second (3.8–6.3× the impulsive figure) for all-electric end-to-end. This round substitutes the corrected delta-velocity into Round C's closure across four architectural recovery variants and asks whether the matrix's surviving cell survives.

**Pre-registered hypotheses (H-vbic).** All against high-elliptical 1 megakilometer Saturn departure with Lunar Gravity Assist credit.

| Sub-claim | Predicted range | Point estimate | Falsification threshold |
|---|---|---|---|
| H-vbic-a — Variant A (as-stated, no recovery) electric inbound DV | 24–30 km/s | 27 km/s | outside range |
| H-vbic-b — Variant B (chemical Saturn-egress kick) electric inbound DV | 20–24 km/s | 21.4 km/s | outside range |
| H-vbic-c — Variant C (Earth aerocapture) electric inbound DV | 18–22 km/s | 19.9 km/s | outside range |
| H-vbic-d — Variant D (both recoveries) electric inbound DV | 12–16 km/s | 13.7 km/s | outside range |
| H-vbic-e — Variant A 500 kilowatt-electric does NOT close inside ±1 yr soft margin | round-trip 16–18 yr, delivered 0–25 t | round-trip 17 yr, delivered 10 t | cell closes OR delivered > 25 t |
| H-vbic-f — Variant D 500 kilowatt-electric closes inside ±1 yr soft margin with delivered 80–110 t | closes with delivered 80–110 t | round-trip 14.5 yr, delivered 95 t | does not close OR delivered outside range |

**Aggregate (H-vbic-agg).** Matrix's surviving Variant B cell as currently presented is architecturally incoherent (electric inbound at impulsive-equivalent DV). Corrected DV makes the cell collapse to roughly the falsified megawatt all-electric end-to-end shape. Recoverable architecture is Variant D (both recoveries). Without architectural recovery, no Variant B configuration closes at 500 kilowatt-electric.

**Method.** Reuses titan's R-inbound-dv-continuous-thrust segment decomposition: Saturn spiral-out + heliocentric retrograde + Earth heliocentric decelerate + LEO capture spiral, minus Lunar Gravity Assist credit, plus optional impulsive Saturn-egress chemical kick (2.09 km/s). For each of four architecture variants, sum applicable segments and substitute into Round C's closure machinery (MARVL-anchored mass, chunk 200 t, specific impulse 2000 s, reactor sweep 500/750/1000 kilowatt-electric).

**Validity caveats.** Titan's continuous-thrust DV is upper bound (10–20% headroom under optimal-control); Saturn-egress chemical kick at 2.09 km/s is matrix's stated impulsive figure; burn-time-comparable-to-cruise-time validity break at 500 kilowatt-electric / 27 km/s; Earth aerocapture inherits R-chunk-as-heat-shield engineering risk; Saturn-egress kick stage dry mass 10 t author-asserted; no inter-variant correlation (real mission would combine elements).

**Test.** `rounds/R_variant_B_impulsive_vs_continuous/run.py`. Deterministic. Sub-second wall clock. Outputs `results/R_variant_B_impulsive_vs_continuous.json` and `results/tables.md`.

---

## Round R-marvl-mass-anchor-validation — does Variant C's surviving cell verdict survive a sweep of plausible MARVL-anchored mass parameterizations? (pre-result; hyperion-2 batch)

**Motivation.** Round D's surviving cell (Variant C: chemical-kick outbound + electric heliocentric inbound + Earth aerocapture, 500 kilowatt-electric, 32.1 t delivered, round-trip 16.32 yr) sits on top of rhea's specific MARVL-anchored mass parameters. Locked finding 4 specifies subsystem-fraction ranges: reactor + shield 25-35%, PC 15-25%, radiator 40-55%. Rhea picked midpoints. This round sweeps pessimistic and optimistic ends of the locked-finding-4 ranges plus a radiator areal-density check.

**Pre-registered hypotheses (H-mmav).**

| Sub-claim | Predicted range | Point estimate | Falsification threshold |
|---|---|---|---|
| H-mmav-a — pessimistic 1 megawatt-electric stack mass | 130-160 t | 145 t | outside range |
| H-mmav-b — optimistic 1 megawatt-electric stack mass | 70-95 t | 80 t | outside range |
| H-mmav-c — pessimistic Variant C @ 500 kilowatt-electric closes ±2 yr soft margin | closes / delivered 10-30 t / round-trip 16.5-17.0 yr | closes / 18 t / 16.7 yr | does not close OR outside ranges |
| H-mmav-d — optimistic Variant C @ 500 kilowatt-electric closes ±1 yr soft margin | closes / delivered 40-55 t / round-trip 16.0-16.3 yr | closes / 47 t / 16.15 yr | does not close OR outside ranges |
| H-mmav-e — rhea-baseline radiator areal density at 500 kilowatt-electric | 2.5-3.5 kg/m² | 3.0 kg/m² | outside range |

**Aggregate (H-mmav-agg).** Variant C's closure verdict is robust under pessimistic MARVL parameterization (cell still closes with delivered 10-30 t at ±2 yr soft margin); optimistic gives modest improvement. Radiator areal density at rhea's parameters is at the edge of physical feasibility.

**Method.** Three parameterizations spanning locked-finding-4 ranges: pessimistic (31/21/45/eta=0.27), rhea baseline, optimistic (28/18/46/eta=0.32). m_fixed 5 t. Back-solve alphas to reproduce target percentages at 1 megawatt-electric. Run Variant C closure (Round D parameters: inbound DV 19.90 km/s, outbound chemical kick 5 km/s, chunk 200 t, Isp 2000 s, Earth aerocapture).

**Validity caveats.** Locked-finding ranges are individual subsystem ranges, not constrained to sum to 100% — pessimistic/optimistic picks must be internally consistent; back-solve from percentages is hyper-sensitive when sum approaches 1.0; Brayton conversion efficiency couples to radiator sizing; areal-density check uses single 700 W_th/m² surface conductance; Round D's matrix-impulsive 6.42 fiction remains the dominant unmodeled risk.

**Test.** `rounds/R_marvl_mass_anchor_validation/run.py`. Deterministic. Sub-second wall clock. Outputs `results/R_marvl_mass_anchor_validation.json` and `results/tables.md`.

---

## Round R-cruise-time-optimization — does Hohmann minimize round-trip time, or does a faster non-Hohmann transfer close more cells? (pre-result; hyperion-2 batch)

**Motivation.** Every closure verdict in this batch sits on top of 12.1 yr of Hohmann cruise (6.05 yr each leg). Hohmann minimizes delta-velocity, not round-trip time. For continuous-thrust electric architectures, faster cruise costs more delta-velocity → more burn time. This round sweeps cruise time from ~3 yr to Hohmann ~6 yr at Variant C 500 kilowatt-electric and asks: does a faster trajectory close more cells, or does the additional delta-velocity eat the time savings?

**Pre-registered hypotheses (H-cto).**

| Sub-claim | Predicted range | Point estimate | Falsification threshold |
|---|---|---|---|
| H-cto-a — heliocentric DV sum at 4-yr cruise | 24-32 km/s | 28 km/s | outside range |
| H-cto-b — round-trip at 4-yr cruise (Variant C 500 kWe) | 15-18 yr | 16.5 yr | outside range |
| H-cto-c — optimal cruise time for Variant C round-trip minimization | 5.5-6.5 yr | 6.0 yr | outside range |
| H-cto-d — round-trip improvement at optimum vs Hohmann | 0.0-0.7 yr | 0.3 yr | outside range |
| H-cto-e — chemical-kick prop at 4-yr cruise (outbound) | > 200 t | 280 t | < 200 t |

**Aggregate (H-cto-agg).** Hohmann is approximately optimal for Variant C at megawatt-class power; round-trip-time savings from non-Hohmann are < 1 yr. Matrix should not invest optimization effort in cruise-time selection.

**Method.** Type-I half-orbit elliptical transfer parameterized by aphelion radius r_apo ≥ r_Saturn. For each r_apo: vis-viva for v at perihelion and r_Saturn; vector dV (tangential against v_Saturn_orbit + radial cancellation); cruise time via Kepler's equation. Symmetric outbound/inbound. Variant C closure (chemical-kick out + electric inbound + Earth aerocapture) at MARVL-anchored mass, chunk 200 t, Isp 2000 s.

**Validity caveats.** Type-I half-orbit only; symmetric outbound/inbound; continuous-thrust = full heliocentric dV (no Oberth bonus on heliocentric segments); Earth-departure / Saturn-arrival in heliocentric frame (LEO escape implicit in chemical-kick stage); chemical-kick prop scales with Tsiolkovsky; Saturn-spiral cost (segment 1) doesn't depend on cruise time; Round D matrix-impulsive-fiction caveat is dominant unmodeled risk.

**Test.** `rounds/R_cruise_time_optimization/run.py`. Deterministic. Sub-second wall clock. Outputs `results/R_cruise_time_optimization.json` and `results/tables.md`.

---

## Round R-hybrid-solar-augmentation — reactor plus deployable solar array along the trajectory (pre-result; prior hyperion session)

**Motivation.** The R-power-wonder pass treated solar as "dead at Saturn." That phrase conflates two questions. Standalone solar at 9.58 astronomical units delivers 1.09 percent of Earth flux and is indeed dead. But a hybrid that adds a deployable solar array to a reactor-class power bus is a different question: along an inbound or outbound spiral trajectory, the spacecraft passes through every heliocentric distance from 1 to 9.58 astronomical units, and the solar contribution at the inner-system phase of the trajectory is large. The user surfaced this idea during the wonder discussion; pre-registering it here.

**Pre-registered hypotheses (H-hsa).** All ranges assume a 200-square-meter Roll-Out Solar Array delivering 300 watts per square meter at 1 astronomical unit (60 kilowatts-electric at 1 astronomical unit), with a linearly-falling low-intensity low-temperature efficiency derate from 1.0 at 1 astronomical unit to 0.79 at Saturn distance per Juno mission data. Trajectory model is continuous-thrust circular-to-circular spiral following Edelbaum, with time-spent-per-radial-bin proportional to r raised to negative one-and-a-half divided by local power.

| Sub-claim | Predicted range | Falsification threshold |
|---|---|---|
| H-hsa-a — Time-averaged effective power gain factor at 10 kilowatt-electric reactor plus 200 square-meter array (continuous-thrust inbound spiral) | 1.5–2.2 | outside range |
| H-hsa-b — Same gain factor at 100 kilowatt-electric reactor plus same array | 1.05–1.20 | outside range |
| H-hsa-c — Same gain factor at 1000 kilowatt-electric reactor plus same array | 1.00–1.02 (negligible) | outside range |
| H-hsa-d — Reactor power class below which hybrid gain factor exceeds 1.5 | 15–40 kilowatts-electric | outside range |
| H-hsa-e — Net chunk-mass deliverable gain at 10 kilowatt-electric Kilopower plus 200 square-meter array, after subtracting the 600 kilogram array dry-mass penalty from the chunk budget | 25–55 percent | outside range |
| H-hsa-f — Areal density break-even (kilograms per square meter at which hybrid loses to a larger pure reactor at fixed power-subsystem mass) | 6–15 | outside range |
| H-hsa-g — Concentrated-burn-at-Earth-vicinity gain factor (single-point evaluation of solar contribution at 1.2 astronomical units, if the inbound burn is bunched there rather than spiraled) | 4.0–6.5 | outside range |

**Aggregate (H-hsa-agg).** The hybrid is a Kilopower-class enabler, not a megawatt-class strategy. At Kilopower scale (1–10 kilowatts-electric) the harmonic-mean power gain over the trajectory is substantial (sub-claims a, d). At megawatt scale (sub-claim c) it is negligible because the fixed array becomes proportionally insignificant. The chunk-mass-deliverable gain at Kilopower (sub-claim e) is large enough to make the array architecturally worthwhile if the relevant ICEBERG mission tier is the Kilopower-only floor case (which, per R-power-base-rate, is the most defensible tier).

**Method.** Closed-form trajectory time-weighting plus harmonic-mean power. For each reactor power class swept (1, 3, 10, 30, 100, 300, 1000 kilowatts-electric):
- Sample P(r) at radii r ∈ [1, 9.58] astronomical units on a 100-point grid.
- Apply array power P_array(r) = P_array_1AU divided by r-squared, times the low-intensity low-temperature derate (linear from 1.0 at 1 astronomical unit to 0.79 at Saturn).
- Compute the harmonic mean of P_reactor + P_array(r), weighted by r raised to negative one-and-a-half. This is the time-averaged effective power for the spiral trajectory.
- Report the gain factor versus reactor-only.
- Compute chunk-mass gain by scaling chunk linearly with effective power (per the conops heuristic of 1 kilowatt-electric per 25 tonnes of delivered chunk), then subtracting the array's 600 kilogram dry mass from the chunk-mass budget.
- Sensitivity sweep: areal density 1, 3, 6, 10, 15, 20 kilograms per square meter (Roll-Out Solar Array is currently ~3); locate the break-even where hybrid loses to a larger pure reactor.

Also computes a separate concentrated-burn case (sub-claim g) where the inbound burn happens at one radial distance rather than spiraled, evaluating the hybrid gain at that fixed r.

**Validity caveats.**
1. Edelbaum is a circular-to-circular approximation. Real ICEBERG inbound is from Saturn-bound elliptical orbit, with significant impulsive components and Hohmann-coast phases between burns. The continuous-thrust spiral over-represents the burn duration, so the harmonic-mean derivation is an upper bound on the time-averaging effect.
2. Low-intensity low-temperature derate is modeled linearly. Real photovoltaic cell behavior at outer-system temperatures and irradiances is non-linear and cell-chemistry-specific. Juno data (5.2 astronomical units) is the deepest-space anchor; beyond that the derate is extrapolation.
3. Array dry-mass attribution is per-array-mass only. Does not include attitude-control penalty, deployment mechanism, thermal management, or end-of-life degradation. Real cost is likely 30–50 percent higher in mass-equivalent.
4. The chunk-mass linear-scaling-with-power heuristic from the conops is itself unsourced internally (per the gap analysis from R-power-wonder block-2 finding). A more honest chunk-mass model would solve Tsiolkovsky directly for the specific mission tier; deferred to a future round.
5. The 200-square-meter array size is one design point chosen for matching the largest deep-space arrays flown to date (Lucy is ~84 square meters; Europa Clipper ~102 square meters). Sensitivity to array size is reported via gain-vs-reactor-power-class curves.

**Test.** `rounds/R_hybrid_solar_augmentation/run.py`. Deterministic (no Monte Carlo needed; closed-form integration on a fine grid). Sub-second wall clock. Outputs tables in `results/`.

---

## Round R-aerocapture-fast-cruise-envelope — does Round F's STRICT-closing Variant C cell survive Earth aerocapture engineering envelope? (post-result; hyperion-3 batch, recurring-lesson-#N intervention)

**Motivation.** Round F reported Variant C at faster-than-Hohmann cruise (aphelion 10.5–11 astronomical units) closes strict L0-05 with delivered 23.5–26 tonnes per mission and round-trip 12.7–13.1 years. Every closure verdict in batches 2 and 3 of this hyperion session folds into "Variant C closes IF Earth aerocapture works for the chunk + tug stack." Aerocapture was previously analysed in `R_chunk_as_heat_shield` at 12.6 km/s entry and ~100 t entry mass; current closing cell is 15.3 km/s entry at 263.8 t. This round computes whether the entry-velocity-and-mass envelope sits inside or outside the prior aerocapture envelope.

**Recurring-lesson-#N intervention.** Per batch-3 handoff recommendation, central numerical estimates were derived first (back-of-envelope, in conversation, before this hypothesis was named). Range bands wrap each anchor.

**Pre-registered hypotheses (H-afce).**

| Sub-claim | Central anchor (computed FIRST) | Predicted range | Falsification threshold |
|---|---:|---|---|
| H-afce-a — entry velocity at aphelion 11 AU, no LGA | 15.4 km/s | 14.5–16.5 | outside range |
| H-afce-b — peak heat flux at H-afce-a entry, chunk geometry | 330 W/cm² | 200–500 | outside range |
| H-afce-c — chunk ablation per single-pass aerocapture | 0.9 percent | 0.4–2.5 | outside range |
| H-afce-d — peak deceleration during pulse | 10 g | 5–18 | outside range |
| H-afce-e — chunk internal stress vs ice tensile strength | margin 2.9× | margin 1.5–6 | outside range |
| H-afce-f — Round F STRICT closure delivered-mass adjustment after aerocapture losses | minus 1.0 percent | minus 0.5 to minus 4.0 percent | outside range OR architecture infeasible |
| H-afce-g — periapsis altitude needed for full capture | 60 km | 50–75 | outside range |

**Aggregate (H-afce-agg).** Round F's STRICT-closing cell at aphelion 11 AU survives aerocapture engineering envelope. Ablation under 1 percent. Chunk structural integrity holds with about 3× margin over ice tensile failure. Periapsis altitude in standard 50–75 km band. Delivered mass adjusts by less than 3 percent.

**Method.** Deterministic single-pass aerocapture envelope check across the Round F transfer-time grid (aphelion 9.58, 10.5, 11.0, 12.0, 14.0 astronomical units) at entry mass {100, 200, 263.8, 350} t with and without 2 km/s lunar gravity assist credit. Heliocentric perihelion velocity from Round F config. Velocity-at-infinity at Earth = v_perihelion − v_Earth − optional lunar-gravity-assist credit. Entry velocity = sqrt(v_∞² + v_escape²). Frontal area from spherical chunk geometry at water-ice density 917 kg/m³. Ballistic coefficient = mass / (Cd × A_chunk), Cd = 1.0. Required periapsis altitude found by inverting drag-impulse-equals-target-Δv on exponential-atmosphere profile (scale height 7.5 km, ρ at 100 km = 5.6e-7 kg/m³). Sutton-Graves stagnation-point heat flux at periapsis density. Total heat load per pass = 0.5 × q_peak × pulse_duration. Chunk ablation = total energy / heat-of-vaporization 2.26 MJ/kg. Peak g = 2.5 × average deceleration. Internal stress = chunk_radius × ρ_ice × peak_g.

**Validity caveats.**
1. Sutton-Graves is stagnation-point only; integrated heat over off-axis area lower than peak × area. Conservative upper bound.
2. Drag coefficient 1.0 for irregular chunk is approximate; real B-ring chunks 0.6–1.4 depending on orientation.
3. Tug-survival assumed conditional on chunk-forward orientation. This round does NOT close R-chunk-as-heat-shield-revisit's binding open question.
4. Single-pass aerocapture only; multi-pass aerobraking deferred.
5. Lunar gravity assist credit at 2 km/s depends on arrival epoch geometry; some epochs give 0.
6. Exponential atmosphere with single scale height is approximate above 100 km; periapsis estimate ±5 km error.
7. Variant C tug mass 63.8 t at 500 kWe from Round F output; MARVL parameter shift gives ±15 t.

**Test.** `rounds/R_aerocapture_fast_cruise_envelope/run.py`. Deterministic. Sub-second wall clock.

**Reading (post-result).** **6 of 7 sub-claims FALSIFIED.** Only H-afce-a (entry velocity) held. The 6 falsifications cascade from a single underlying error: the central anchors were taken from Saturn's `R_chunk_as_heat_shield_revisit/SCOPE.md` summary of R-chunk-as-heat-shield, which **misrepresented** the prior round's findings. The actual R-chunk-as-heat-shield aggregate verdict was "falsified — multi-pass aerobraking is not the right architectural choice for ICEBERG, the ballistic coefficient is too high," and the round explicitly listed three required (unresolved) engineering programmes. Saturn's SCOPE.md cherry-picked the favourable sub-finding ("0.5% chunk ablation") while burying the falsified aggregate.

**Architecture-level consequence.** Variant C closure at faster cruise (Round F), at Hohmann (Round D Variant C), and at Variant D both-recoveries (Round D), all rest on the falsified aerocapture conditional. Combined with R-deployable-drag-skirt killed at orchestrator commit `34a473b`, ICEBERG has no surviving Earth-side capture mechanism that closes engineering-side. The "no atmospheric capture baseline" round R-chunk-as-heat-shield named as a next-round candidate was never run; it is now the load-bearing question.

**Recurring lesson #N updated.** Seven hyperion-2 (now hyperion-3) rounds, seven aggregate falsifications. Pre-registration intuition was within 0.7 percent of the entry-velocity computed value — the back-of-envelope-first intervention worked at the *intuition* level. What was wrong was the *anchor* I scaled from. Updated lesson: when anchoring to a prior round's findings, re-read the prior round's `STUDY.md` Reading and Revisit sections directly, not the orchestrator's downstream SCOPE summary. SCOPE documents are framing devices, not authoritative summaries.

**Revisit clause.** If R-no-atmospheric-capture-baseline closes (yields any surviving cell with aerocapture entirely removed), this round's matrix-level conclusion softens to "aerocapture-conditional cells are upside-only, not baseline." If R-no-atmospheric-capture-baseline also collapses to zero delivered mass, this round's finding combined with that one is the matrix's actual kill-shot for Variant C and the matrix needs to escalate to "the surviving cell is empty" before any further architectural rounds.

---

## Round R-no-atmospheric-capture-baseline — does ANY surviving cell exist with Earth aerocapture entirely removed? (post-result; hyperion-3 batch, FIRST HELD AGGREGATE)

**Motivation.** R-chunk-as-heat-shield closed (8 rounds ago) with aggregate falsified and named three follow-on candidates. R-deployable-drag-skirt was killed at orchestrator commit `34a473b`. R-hybrid-aerocapture-aerobraking was never run. R-no-atmospheric-capture-baseline was never run. R-aerocapture-fast-cruise-envelope (this session, prior round) showed the chunk-as-heat-shield mitigation also collapses under Round F's higher entry velocity. This round runs the conservative-architecture confirmation R-chunk-as-heat-shield asked for: with Earth aerocapture entirely removed, is ANY combination a surviving cell?

**Recurring-lesson-#N intervention (stacked).** Per the updated lesson from R-aerocapture-fast-cruise-envelope: anchors must come from PRIMARY texts (titan's STUDY.md, rhea's STUDY.md, R-chunk-as-heat-shield's STUDY.md, Round F's JSON), not from orchestrator SCOPE summaries. Back-of-envelope computed FIRST.

**Pre-registered hypotheses (H-nacb).**

| Sub-claim | Central anchor (PRIMARY-text source) | Predicted range | Falsification threshold |
|---|---:|---|---|
| H-nacb-a — chemical-Earth-capture propellant for Round F closing-case mass | 1219 t | 1000–1500 | outside range |
| H-nacb-b — Saturn-departure mass if chemical propellant carried | 2025 t | 1700–2400 | outside range |
| H-nacb-c — chunk-water fraction of Saturn-departure propellant (chemical branch) | 9.9 percent | 7–13 | outside range |
| H-nacb-d — electric-only inbound mass-ratio at full-titan Δv 24.13 km/s, Isp 2000 s | 3.50 | 3.0–4.2 | outside range |
| H-nacb-e — chunk water remaining after electric-only inbound | 57 t | 45–80 | outside range |
| H-nacb-f — number of strict-closing cells (any combination) at L0-05 strict 15 yr round-trip with aerocapture removed | 0 | 0–2 | outside range |
| H-nacb-g — number of soft-closing cells at L0-05 soft-margin 17 yr round-trip with aerocapture removed | 0 | 0–4 | outside range |

**Aggregate (H-nacb-agg).** With Earth aerocapture entirely removed, ZERO surviving cells in the matrix at strict L0-05 15-year ceiling AND ZERO at soft-margin 17-year ceiling. Both candidate Earth-arrival mechanisms (chemical impulsive at periapsis, electric continuous-thrust spiral) collapse: chemical demands 1200+ tonnes propellant at Earth (Earth-launch tankering at ~12 Starship launches per mission) back-propagating to a 2000+ tonne Saturn-departure mass; electric is the falsified all-electric end-to-end architecture from rhea's R-megawatt-marvl-radiator. The matrix's surviving cell, with aerocapture removed, is EMPTY.

**Method.** Deterministic 288-cell sweep across (transfer-time aphelion × reactor power kWe × chunk size × Earth-arrival mechanism × Saturn-egress mode × lunar-gravity-assist credit). For each tuple: compute Earth-arrival propellant under each mechanism, back-propagate through inbound electric burn (Saturn-egress 6.16 km/s at Isp 2000 s) to find Saturn-departure mass, back-propagate through outbound chemical-kick to find LEO mission-1 launch mass, check round-trip time against L0-05 ceilings. Sweep axes: aphelion {9.58, 10.5, 11.0, 12.0} AU; reactor {500, 1000, 2000} kWe; chunk {100, 200, 350} t; arrival {chemical, electric}; egress {chemical_kick, electric_only}; LGA {with, without}.

**Validity caveats.**
1. Heliocentric Δv approximations from Round F vector-Lambert machinery (Type-I half-orbit symmetric).
2. Chemical-capture single-impulse assumption is best-case for chemical.
3. Electric-capture mass-ratio assumes chunk-fed.
4. R-hybrid-solar-augmentation orphan-branch finding showed solar gain negligible at megawatt-class.
5. Tug dry mass scales linearly with reactor kWe per MARVL bundled approximation.
6. Lunar-gravity-assist credit at 2 km/s is matrix standing value; favorable epochs only.
7. Saturn-egress chemical kick still allowed (Variant B configuration).
8. Outbound chemical kick at 5 km/s realistic (Round F config).
9. Tug survival on entry not modeled because there is no aerocapture; tug arrives at LEO via propulsive capture or fails entirely.

**Test.** `rounds/R_no_atmospheric_capture_baseline/run.py`. Deterministic. Sub-second wall clock.

**Reading (post-result).** **HYPOTHESIS HELD. First held aggregate in 8 hyperion rounds.**

5 of 7 sub-claims held. The 2 that missed (H-nacb-b, H-nacb-c) underestimated chain back-propagation through the outbound chemical-kick stage — my anchor stopped at 2025 t at Saturn departure, but the outbound stage Tsiolkovsky-multiplies that to 31,934 t at LEO for the chemical-Earth-arrival branch. The kill-shot sub-claims (H-nacb-f, H-nacb-g) held with margin: zero strict-closing cells, zero soft-closing cells out of 288 swept.

**Architecture-level consequence (combined with R-aerocapture-fast-cruise-envelope).** The matrix as currently shaped has no surviving cell at any L0-05 ceiling. Variant C closure verdicts (Rounds D, E, F) rest on a falsified aerocapture-conditional; with aerocapture removed entirely, no other combination closes either. Path forward requires architectural escape: smaller chunks (R-megawatt-chunk-100t), hybrid aerocapture-then-aerobraking with bag-sacrificed pass-1, sacrificial-bag as first-class cost line, mission-architecture pivot (lunar-orbit catcher, cislunar processing depot), or relax L0-05 ceiling.

**Recurring lesson #N — first success.** The pattern (six straight falsifications) broke. The interventions stacked: (a) compute back-of-envelope FIRST, (b) anchor on PRIMARY texts not SCOPE summaries. Both are required. SCOPE summaries are framing devices, not authoritative. This generalises beyond hyperion: the SCOPE-misread vector is general — any worker may benefit from the same discipline.

**Revisit clause.** This round, combined with R-aerocapture-fast-cruise-envelope, is the matrix kill-shot for Variant C and the entire aerocapture-conditional chain. Orchestrator-decision required: which architectural escape path to scope next, or whether to relax L0-05 ceilings.

---

## Round R-outbound-chemical-kick-economics — does outbound chemical-kick economics independently kill the surviving 500-kWe cell, and if so under what launch market? (post-result; hyperion batch-5, SECOND HELD AGGREGATE + first round to retract a prior-round verdict-text claim)

**Motivation.** Batch-3 and batch-4 handoffs flagged an unrun "sleeper falsifier" — claim from `R_aerocapture_fast_cruise_envelope/results/closure_verdict.md`: "Round F uses 715 t of hydrolox per outbound mission. At Earth-launch costs of $500–1000/kg this is $358–715 million in propellant per mission, dwarfing the matrix-implied per-mission revenue. May be the second sleeper falsifier of Variant C closure." Per recurring-lesson-#N stacked intervention (compute back-of-envelope FIRST, anchor on PRIMARY texts), this round retests the claim against `variant_b_closure` directly.

**Recurring-lesson-#N intervention (stacked, third instance).** Anchors taken from PRIMARY texts (`variant_b_closure` source, R-reactor-roadmap `LAUNCH_PLUS_TSI`, rhea bake-off `STUDY.md`, SpaceX-published launcher specs) — not from verdict-text claims of prior rounds.

**Pre-registered hypotheses (H-ock).**

| Sub-claim | Central anchor (computed FIRST) | Predicted range | Falsification threshold |
|---|---:|---|---|
| H-ock-a — outbound prop per mission for surviving cells | 150 t | < 200 t (715 claim overstated by ≥ 4×) | exceeds 200 t |
| H-ock-b — implied launch cost at $290M/ship anchor and central LEO mass 224 t | $1,295/kg | [$1,200, $1,400]/kg | outside |
| H-ock-c — central LEO mass / Falcon Heavy expendable capacity 63.8 t | 3.51× | ≥ 2.5× | < 2.5× |
| H-ock-d — marginal IRR under realistic Falcon Heavy ($665M/ship) | 0% | ≤ 0% (matches rhea floor) | > 0% |
| H-ock-e — Starship-target ($200/kg) + best path + $10k water + sovereign crosses sov-bond | no pass | no pass at L0-05 hard | any pass |
| H-ock-f — full sweep (96 rows) crosses sov-bond at L0-05 hard | 0 rows | 0 rows | ≥ 1 row passes |
| H-ock-g — at L0-05 soft, ≤ 1 row passes; if so, Starship-class only | 0 rows | ≤ 1 Starship-class row | > 1 row OR non-Starship |
| H-ock-h — rhea LAUNCH_PLUS_TSI internally inconsistent with MARVL ship LEO mass | INCONSISTENT | INCONSISTENT (held a priori on H-ock-c) | n/a |
| H-ock-i — sleeper-falsifier framing retirement | retire | calibration finding NOT independent kill-shot | round produces kill-shot |

**Aggregate (H-ock-agg).** All 9 sub-claims hold. The batch-3/4 sleeper-falsifier claim of "715 t hydrolox per outbound mission" is overstated by ~5×. The actual variant_b_closure-anchored figure is 145–174 t per mission for surviving cells. The bake-off's $290M/ship anchor implies $1,273/kg launch cost — internally inconsistent with the source comment "Falcon Heavy expendable + Vulcan-Centaur kick" because Falcon Heavy expendable cannot launch the surviving cell's 228 t LEO mass in one shot. Updating LAUNCH_PLUS_TSI to realistic Falcon-Heavy ($590M/ship) or SLS-class ($1,565M/ship) does not change the bake-off's marginal IRR verdict — every conditional NPV is already negative across MW_YEARS. Outbound chemical-kick economics is NOT an independent matrix-killer; the cell is killed by reactor program risk + L0-05 ceiling, both already established.

**Method.** Deterministic 96-row sweep (4 path-and-chunk × 6 launch markets × 2 water prices × 2 sovereign options). For each path-and-chunk: call `variant_b_closure` with `variant_inbound_dv` from R_variant_B_impulsive_vs_continuous to extract delivered_t, RT_yr, m_LEO_mission1_t. For each (path-and-chunk, launch_market): compute realistic launch+TSI as `ceil(LEO_mass / launcher_capacity) × per_launch_cost + $140M kick stage`. Override R-reactor-roadmap's LAUNCH_PLUS_TSI / MARVL_CHUNK_DELIVERED_T / ROUND_TRIP_YR_MARVL per cell, recompute conditional IRR curve over MW_YEARS, take marginal IRR averaged over R-power-base-rate CDF.

**Validity caveats.**
1. Mission-1 only (no depot); mission-2+ depot-amortization scenario deferred to follow-on round.
2. Ship-cost / NRE / ground-ops inherited from R15-rerun; not under test.
3. Launcher capacities and prices anchored to SpaceX-published / SpaceX-stated values; Starship targets NOT YET ACHIEVED.
4. Marginal IRR averaging via `rr.marginal_irr` floors None values at 0; does not reflect "deeply negative" properly.
5. Saturn-departure orbit fixed at high-elliptical 1-million-km (rhea-bakeoff DEFAULT_DEPARTURE).
6. Lunar-Gravity-Assist credit 2 km/s on Earth-side; favorable epochs only.
7. Reactor program risk priors absorbed via R-power-base-rate CDF; this round inherits, does not modify.

**Test.** `rounds/R_outbound_chemical_kick_economics/run.py`. Deterministic. Sub-second wall clock. PYTHONPATH=src.

**Reading (post-result).** **HYPOTHESIS HELD. Second held aggregate in 9 hyperion rounds. First round to catch a prior-round verdict-text error.**

All 9 sub-claims held with margin: max outbound prop 174 t (vs band [145, 200]); implied cost $1,273/kg (vs [1200, 1400]); FH ratio 3.57× (vs ≥ 2.5×); 0/96 sov-bond passes at any L0-05 ceiling. The kill-shot framing is RETIRED — outbound chemical-kick economics is a calibration item, not an independent matrix-killer.

**Architecture-level consequence.** Three reconciliation findings for the orchestrator:

1. **Retire the "outbound chemical-kick economics sleeper falsifier" item from the matrix open-items list.** Source claim was a back-of-envelope error in `R_aerocapture_fast_cruise_envelope/results/closure_verdict.md`.
2. **Flag the rhea bake-off's $290M/ship LAUNCH_PLUS_TSI as internally inconsistent with the surviving cell's MARVL LEO launch mass.** Implies Starship-pessimistic launch economics (NOT YET ACHIEVED) without flagging it. Queue R-launch-cost-anchor-revision to settle.
3. **The bake-off's headline ("no surviving cell at conservative assumptions") is robust to launch-cost revision** across the full sweep — even at SLS-class costs, the cell does not return capital. The headline strengthens, not softens.

**Recurring lesson #N — third instance, generalized vector.** The verdict-text-misclaim vector is a generalization of the SCOPE-misread vector caught in batch 4. The pattern: any unsourced numerical claim in any round's verdict text or SCOPE summary is a candidate falsifier worth one back-of-envelope verification pass before being adopted as load-bearing. Recommend orchestrator-level discipline: round closure verdicts should not introduce numerical claims that aren't either in the round's run.py output or anchored to a named PRIMARY-text source.

**Revisit clause.** This round closes the outbound-chemical-kick sleeper-falsifier item. If R-launch-cost-anchor-revision reveals that the rhea bake-off was correct after all (i.e., the $290M/ship anchor IS defensible under some launcher assumption I haven't considered), then this round's H-ock-h would soften — but H-ock-i (sleeper-falsifier retirement) remains held independently because H-ock-a is verdict-binding. No Revisit triggered this round.
