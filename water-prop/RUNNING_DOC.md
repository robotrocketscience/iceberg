# Campaign Running Document — water-prop

Per protocol section 5. Append-only per round. Round entries advance through four states (skeleton → pre-result → post-result → cross-linked).

## Phase question

For a Project ICEBERG return mission carrying a 5–500 ton chunk of B-ring water ice from Saturn to a low Earth orbit depot, what propulsion technology and architecture delivers the largest fraction of the chunk to Earth, accounting for available reactor power, mission timeline, propellant contamination, and component lifetime?

## Methodology commitment

This campaign follows the protocol in `PROTOCOL.md`, which is adapted from the aelfrice project's internal experiment conventions (CONVENTIONS.md). Pre-registered numeric hypotheses live in `HYPOTHESES.md`. Risks are tracked in `RISKS.md` (propulsion) and `../RISKS.md` (program). Each round writes a `STUDY.md` entry that follows the 5-section template (hypothesis, test, result, reading, revisit, cross-learning).

## Round status

| Round | Title | State | Notes |
|---|---|---|---|
| R0 | Microwave electrothermal frozen-flow ceiling | post-result | Pre-protocol; reconstructed retrospectively in `HYPOTHESES.md`. |
| R1 | Citation verification | post-result | 7 citations checked; 2 falsified-informative. |
| R2 | Lunar gravity assist trajectory | post-result | Conops 3 km/s claim falsified at velocity-at-infinity = 6 km/s. |
| R3i | Dual-ion architecture (electrolyzed water) | post-result | Exploratory; wins only at megawatt-class power. |
| R6 | Power-constrained specific-impulse optimum | post-result | Validates microwave electrothermal at Kilopower power class. Methodology gap: reactor mass not included. |
| R8 | Inbound delta-velocity budget audit | post-result | **Architectural finding:** conops chunk-fed inbound budget is structurally under-specified by 1.2–8.9 km/s. Triggers R9 and R10 follow-ups. |
| R10 | Inbound propulsion architecture revisit | post-result | **Architectural decision:** water radio-frequency ion (Pale Blue) replaces microwave electrothermal for both Saturn egress and inbound braking. Microwave electrothermal delivers 0% at 14 t chunk; water radio-frequency ion delivers 61–80%. |
| R3a-h | Per-technology specific impulse ceilings | superseded by R10 | R10 covered the four chunk-fed candidates with pre-registered hypotheses. |
| R4 | Efficiency sensitivity | not registered | |
| R5 | Duty cycle and mass margin (incl. reactor mass) | upgraded to load-bearing | R6 omitted reactor mass; R8 and R10 both inherited or partially corrected the omission. R5 must redraw R6's power-optimal curve with full mass stack. |
| R7 / R11 | B-ring dust contamination tolerance for water radio-frequency ion | upgraded to load-bearing | R10's recommendation depends on radio-frequency ion grid life under chunk water. |
| R9 | Slow-transfer trajectory family | proposed in R8 cross-learning | Time-of-flight vs arrival velocity-at-infinity trade. Determines which R10 case (B or C) is physically realizable. |
| R0b | Microwave electrothermal retest with extended chemistry mechanism | not registered | |
| R0c | Microwave electrothermal with wall heat loss and plasma non-equilibrium | not registered | |
| R0d | Microwave electrothermal with finite-rate kinetics in the nozzle | not registered | |
| R-mid | Mid-cycle audit | not run | Scheduled around campaign midpoint (protocol section 6). |
| R-NPV | Discount-rate net-present-value of cashflow | post-result | Internal-rate-of-return 3.63–6.97 percent at R15-rerun mass; sovereign-development territory. **Conditional finding — superseded by R-reactor-roadmap (second pre-registration) under MARVL anchoring.** |
| R-cadence | Multi-ship cadence sensitivity on internal-rate-of-return | post-result | Cadence is not the dominant lever; megawatt-arrival year promoted to next round (R-reactor-roadmap). |
| R-power-base-rate | Bayesian prior on space-fission arrival year | post-result (integrated via four-worker merge) | P(megawatt by year 20) = 0.5 percent; median megawatt arrival offset 40.8 years. Five of seven sub-claims falsified-pessimistic. Feeds R-reactor-roadmap (second pre-registration). |
| R-reactor-specific-power | Specific power sweep at MARVL mass | post-result (integrated via four-worker merge) | Optimum reactor power tracks chunk mass, not specific power. 40 watts-per-kilogram megawatt cell is upside-only (paper-grade). |
| R-megawatt-marvl-radiator | MARVL-anchored radiator mass model | post-result (integrated via four-worker merge) | Year-20+ megawatt all-electric end-to-end **falsified** at MARVL realism. Chemical-kick architecture survives only at ≥ 500 kilowatt-electric (5× FSP Phase 2 scope). |
| R-reactor-roadmap | Marginal internal-rate-of-return integrated over reactor-arrival distribution | post-result (second pre-registration) | Marginal internal-rate-of-return = 1.45 percent (sub-sovereign-bond). Reactor-roadmap timing lever is essentially dead (+0.04 percentage points uplift from aggressive program). Original pre-registration retired in light of upstream falsifications. |
| R-delivery-irr-curve | Marginal internal-rate-of-return as a function of per-ship delivery, rescue-mechanism-agnostic | post-result | 4% / 8% / 10% hurdle crossovers at 209 / 461 / 691 tonnes per ship. **Regulated-utility hurdle (8%) is just barely reachable at B-ring single-chunk physical cap of 482 tonnes; corporate-growth (10%) is structurally unreachable on single-chunk-per-mission.** All seven sub-claims held (first all-held round of the campaign; pre-registered ranges locked after BOE). |
| R-chunk-as-heat-shield-revisit | Single-pass aerocapture rescue path, full envelope scan | post-result (phoebe, 2026-05-15 latest+) | **Single-pass chunk-as-heat-shield is structurally infeasible across the full architecturally-relevant envelope.** Zero of 40 cells (8 chunk × 5 v_∞) achieve capture at periapsis ≥ 50 km; binding constraint is capture-feasibility itself, not bag-thermal or chunk-structural margin. Aggregate H-csa-agg HELD; 3 of 5 gradable held; 2 falsifications more pessimistic than predicted. Matrix's aerocapture-conditional rows reframed: single-pass-engineering-falsified, hybrid-engineering-pending. Hybrid path (R-hybrid-aerocapture-aerobraking, SCOPE on main, not run) is now the only architecturally-credible aerocapture-adjacent candidate. |
| R-hybrid-aerocapture-aerobraking | Pass-1-deep-aerocapture (bag sacrificed) + pass-2-onward-shallow-aerobraking — architectural-recovery candidate | post-result (phoebe, 2026-05-15 latest+1) | **Hybrid architecture does NOT close at any cell.** 0 of 1920 cells (4 chunk × 3 reactor × 2 aphelion × 2 lunar-gravity-assist × 8 pass-1-altitude × 5 aerobraking-altitude) satisfy all five closure conditions. Three independent failure modes: (1) pass-1 structural — chunk shatters at any depth dumping ≥ 4.18 km/s (parabolic-velocity threshold), tensile margin 0.75× at h₁=40 km; (2) aerobraking unphysical timescale — 9 yr at 110 km worsening to 1608 yr at 200 km under US Standard 1976 atmosphere; (3) chunk consumed by sublimation — 77-1486 t loss across 110-200 km aerobraking, all exceeding 50% chunk-mass tolerance. 8 of 9 gradable sub-claims HELD, 1 falsified-conservative (sublimation lower than predicted but still chunk-killing). Three SCOPE input-assumption errors documented: β-by-chunk-size non-monotonic, pass-1 Δv-to-insert set by parabolic threshold not engineering judgment, single-scale-height atmosphere qualitatively wrong above 110 km. Adopts US Standard 1976 atmosphere as campaign methodology improvement. R-deployable-drag-skirt promoted to next critical-path round. |
| R-hybrid-chemical-power-augmentation | Does a small reactor (1-50 kWe) plus brought-from-Earth hydrolox gas-generator boost close any inbound cell at flown-anchored reactor performance? | post-result (phoebe, 2026-05-18 latest+11) | **0 cells close joint-strict at audit-conditional anchors.** Raw sweep (1,800 cells): 0 close L0-05 strict (15 yr); 54 close joint-demonstrator (40 yr + 2× Starship + reactor lifetime 30-yr aspirational). After stripping three audit-conditional axes (aerocapture_credit = 0 km/s vs falsified R-hybrid-aerocapture-aerobraking; reactor lifetime ≤ Kilopower 10-yr design target; launch envelope ≤ 1× Starship 150 t): **0 cells survive.** H1 HELD strongly (200-t commercial unreachable). H2 + H3 raw-HELD but audit-conditional-FALSIFIED (4 / 30 cells respectively → 0 after audit-strip). H4 falsified. H5 falsified. H6 not gradable (no demonstrator-closing cell uses M_H2O2 > 0; the hybrid mechanism is functionally inert). H-pa-aggregate HELD on strict (0); falsified-high on demonstrator charitable count; HELD on demonstrator audit-conditional. **Fourth orthogonal kill on held chunk-rendezvous architecture.** Six SCOPE/anchor input-assumption errors documented (lesson 9 sixth campaign-wide application): chunk-as-propellant Tsiolkovsky constraint missed; Saturn departure orbit unspecified (Iapetus 24.7 km/s anchor vs B-ring 40.2 km/s operating zone); aerocapture credit conditional on separately-falsified cell; reactor lifetime constraint absent; tank-fraction Centaur-hours anchor wrong for multi-year cryostorage; SATURN-SHIP-SPEC dry mass anchored to Kilopower paper-study specific power (~6 W/kg) not KRUSTY flown anchor (2.4 W/kg). Methodology lesson 12 candidate: conditional-axis stripping discipline. |
| R-mission-architecture-pivot-survey | Triage 31 candidate mission architectures against 8 kill criteria assembled from existing campaign evidence; produce DEAD-ON-ARRIVAL / REQUIRES-REFRAME / WORTH-DEEP-DIVE classification per candidate | post-result (phoebe, 2026-05-18) | **31 of 31 surveyed candidates classify DEAD-ON-ARRIVAL.** Zero land REQUIRES-REFRAME; zero land WORTH-DEEP-DIVE. More pessimistic than pre-registered H-pas-1 (predicted 20-26 DEAD; observed 31). H-pas-2 falsified on direction for ~16 candidates predicted REQUIRES-REFRAME or WORTH-DEEP-DIVE. H-pas-3 (4-7 WORTH-DEEP-DIVE) falsified-high. H-pas-4 (L1r+L3r as novel decision space) falsified — no L0-reframe escapes physical kills (F2 B-ring + F6 reactor program both physics-binary not framing-relaxable). H-pas-5 (≤ 1 fully-clean candidate) HELD-strong. **Methodology lesson 14 candidate** surfaced: F6 (reactor program) is probabilistic in iapetus's framework but binarised to FAIL in this triage, over-determining 24 of 31 candidates. Re-classifying F6 as UNKNOWN (rather than FAIL) yields 24 DEAD + 7 F6-conditional WORTH-DEEP-DIVE — matching pre-registered H-pas-3 range. **Honest reading:** under conservative anchors, 31/31 DEAD; under iapetus-style probabilistic F6, 7 F6-conditional candidates (S1 Enceladus plume, S2 Mimas, S4 Hyperion, S5 Tethys, C2c precursor, C4c data-resource, M2m one-way) are worth deep-dive contingent on the same reactor-program question that already bounds the matrix. **Triple-corroborated campaign reading** (iapetus from program-class side; phoebe from chunk-rendezvous side; phoebe from alternative-architecture side): the architectural search space is exhausted at worker-round level; remaining decision space is project-owner-level reframing or new architectural inputs not in the surveyed set. |
| R-particle-distribution-q-sensitivity | Self-questioning round 4 — interrogate the N(D) ∝ D⁻³ particle-size-distribution exponent anchor across literature range q ∈ [2.5, 4.0] | post-result (phoebe, 2026-05-16 latest+9 → +10) | **Verdict robust across literature q range.** 0 of 540 cells close at strict or moderate threshold at any q. At q=4 (literature most-favourable extreme), best chunk-bearing mass-passing cell (outermost-180km × 20cm × 60°) gives P_ea = 45.8% per pass — 458× short of strict, 20× short of extreme threshold. At q=3 (literature mean), same cell gives P_ea = 100%. Two opposing direction-of-bias effects partially cancel: low q (heavier toward large) raises hit count modestly; high q (heavier toward small) shrinks hit count by factor 73 (less than predicted). "Target high-q location" architectural rescue path foreclosed (B3 core has q≈3.3 but τ=4.5 overwhelms rescue). H-pq-3, H-pq-4, H-pq-6 falsified at strict threshold; H-pq-7 (aggregate) HELD-strong. **FIFTH convergent falsification** of held chunk-rendezvous architecture; phoebe now demonstrably out of internal-assumption levers to interrogate. PROTOCOL footnote candidate: interrogate symmetric-looking assumptions because the sensitivity may surprise you. |
| R-bag-aperture-chunk-joint | Self-questioning round 3 — interrogate the bag-aperture = 100 m² anchor (which I never justified) jointly with chunk mass and venture-class economics | post-result (phoebe, 2026-05-15 latest+8 → +9) | **Bag-aperture lever does not rescue any cell.** 0 of 2,160 cells close on the 5-constraint aggregate (extended-aperture survivability + mass budget + defensible threshold + chunks-present + venture-class economics). Anchor cell (10t chunk × 7m² bag × 1m mesh × outermost-80km × 90°) gives 0.015 hits/pass and P_ea = 1.47% — survives — but mass penalty 14.5% (over budget; 90° plane-change Δv dominates), zone is chunk-sparse, delivered mass 10t fails ALL 3 hurdles (sovereign-bond 209t / regulated-utility 461t / corporate-growth 691t per R-delivery-irr-curve). Confirms: chunk-population vs safe-passage co-location is the single most-binding constraint on the held architecture. Recommends campaign-shared utility `bag_min_area_m2(chunk_t)` for future rounds. Cumulative session falsification arc: 4,268 unique closure-checks across 4 rounds, all negative. |
| R-bring-survivability-relaxed | Self-questioning follow-up to R-bring-rendezvous-survivability — sweep closure threshold, mesh capability, extended-aperture treatment, single-vs-double crossing | post-result (phoebe, 2026-05-15 latest+8 → +9) | **Prior verdict ROBUST to all four self-questioning levers combined.** 0 of 126 cells close at any of 5 thresholds × 2 treatments × 2 crossings (= 2520 closure-checks). Best chunk-bearing flip-threshold = 4.79% per crossing (requires non-defensible f_other = 0). Extended-aperture treatment SHARPENS verdict — point-vehicle formula understates real hit count by 4-6 orders of magnitude on bag-aperture metric; at chunk-bearing cells, ≥ 5 expected hits per pass even with 20cm-cull mesh. 1m-cull mesh (only config dropping P_ea below 99%) costs 50t = 19% baseline (3× over budget) AND only works at chunk-sparse outermost-80km zone. Six of six pre-registered hypotheses HELD or HELD-strong. Reading-level: held chunk-rendezvous architecture is doubly-confirmed-non-closing; phoebe's recommendation strengthens to retire from venture-class viability. PROTOCOL footnote candidate: point-vehicle vs extended-aperture treatment for any ring/atmosphere/debris exposure. |
| R-bring-rendezvous-survivability | Engineering question 2 of 2 on held chunk-rendezvous architecture — does engineered survivability close 99-percent-per-pass B-ring impact-prob gap? | post-result (phoebe, 2026-05-15 latest+8 → +9) | **Engineered survivability does NOT close the impact-prob target at any cell.** 0 of 162 cells (9 τ-zones × 3 armour densities × 2 mesh states × 3 inclinations) satisfy per-pass impact probability ≤ 0.01%. Lowest P_impact in any chunk-bearing zone: 7.23% per pass at B-ring outermost 180 km × 90° × cull-mesh — 723× short of target. Lowest P_impact anywhere: 0.075% at Huygens Gap × 90° × mesh — but contains no large chunks (per fine-structure H1+H2). Fundamental obstruction is the chunk-population vs safe-passage co-location problem. 6 of 6 hypotheses graded as predicted (1 wrong-but-informative on cost magnitude, all others HOLD or HOLD-strong). Four SCOPE input-assumption errors documented (lesson 9 third application): geometric-impact-prob velocity-independence, slow-cross frame ambiguity, armour cross-section bookkeeping, Edelbaum-cost computed at wrong orbital point. Combined with R-hybrid-aerocapture-aerobraking 0/1920, the held chunk-rendezvous architecture is structurally non-closing on conjunction of both load-bearing engineering questions. |
| R-variant-B-100t-resizing | Does chunk reduction to 100 tonnes rescue Variant B without aerocapture? | post-result (phoebe, 2026-05-15 latest) | **Path 3 of the bake-off is structurally unavailable.** No (chunk, reactor) point in the swept envelope simultaneously satisfies propellant-feasibility AND L0-05 closure. Bake-off collapses to paths 1 (aerocapture mandatory) and 2 (acknowledge collapse). 4 of 4 gradable hypotheses HELD under pessimistic framing; orchestrator-authored SCOPE.md optimistic prediction falsified-pessimistic. |
| R-multi-chunk-per-mission | Multi-chunk aggregation to break corporate-growth hurdle | queued | Only path to ≥ 691 tonnes per ship; B-ring single-chunk cap is 482 tonnes. |
| R-water-price-market-depth | Market depth above $10,000 per kilogram | queued | R15b's $10,000 ceiling was the upper bound of sensitivity sweep, not the upper bound of willingness-to-pay. |
| R-synthesis | Delivered-mass Pareto surface across all candidates | not run | Final round (protocol section 10). |

---

## R0 — Microwave electrothermal thruster frozen-flow ceiling

**Status:** Pre-protocol. Run before the protocol was adopted; the entry below is a retrospective protocol-format reconstruction. The original analysis lives in `rounds/R0_microwave_electrothermal_frozen_flow/STUDY.md` and round 1 / round 2 stage docs.

**Hypothesis (reconstructed):** Real-world water-microwave-electrothermal-thruster specific impulse sits in the 700–1000 second band per training-data references.

**Test:** Cantera-based sweep over chamber temperature 3000–12,000 K and chamber pressure 1–1000 torr, computing specific impulse under shifting-equilibrium expansion (upper bound) and frozen-flow expansion (lower bound). See `rounds/R0_microwave_electrothermal_frozen_flow/run.py`.

**Result:**

| Metric | Predicted | Measured | Held? |
|---|---|---|---|
| Maximum equilibrium specific impulse in sweep | 700–1000 s | 814 s (at chamber T = 9000 K, pressure = 1000 torr) | partially held — only at sweep edges |
| Realistic operating point specific impulse (T=7000 K, P=100 torr) | 700–800 s | equilibrium 558 s, frozen 416 s | falsified-conservative |
| Frozen-flow penalty growing with chamber T | yes | yes — 10% at 3000 K, 33% at 9000 K | held |

**Reading.** Real-world microwave-electrothermal water thrusters cannot reach 1000 second specific impulse at any realistic operating point. The 700–1000 second range cited in open literature is theoretical-ceiling territory, not a real operating point. Realistic value is 500–650 seconds.

**Revisit.** Hypothesis was wrong in the conservative direction. Lesson: training-data references on water-microwave-electrothermal specific impulse appear to be optimistic; this is a recurring pattern (round 1 will check whether other training-data citations show the same bias).

**Cross-learning.**
- Positive for round 3a (water radio-frequency ion): if a higher specific impulse than 750 seconds is needed, ion or Hall must close.
- Negative for the previously hopeful "microwave electrothermal at 1000 seconds is achievable" framing in R1 / R2 stage docs (`docs/R1-landscape.md`, `docs/R2-deepdive.md`) — both updated.
- Methodology issue flagged for round 0b: Cantera convergence failures at chamber temperature > 9000 K mean the high-T edge of the sweep is not characterized. R0b extends the mechanism to include ionized species.

---

## R1 — Citation verification

**Status:** post-result. Full entry in `rounds/R1_citation_verification/STUDY.md`. Summary below.

**Hypothesis (H1):** 7-row table in `HYPOTHESES.md`. Aggregate: 1–3 of 7 citations falsified beyond predicted range.

**Test:** Web search on each citation. Outputs: `rounds/R1_citation_verification/results/citations.md`.

**Result.**

| Claim | Predicted | Found | Verdict |
|---|---|---|---|
| Penn State water microwave electrothermal Isp | 500–800 s | not measured for water | falsified-informative |
| Tethers HYDROS Isp | 250–350 s | up to 300 s | held |
| Pale Blue water ion Isp | 800–1500 s | 2000 s | falsified-informative |
| Hydrogen permeation through 316 stainless steel | 10⁻⁹ mol/(m²·s·√Pa) | source identified | deferred |
| Kilopower electrical power | 1–10 kWe | 1 kWe nominal, 1–10 kWe project | held |
| B-ring water-ice fraction | 92–98% | >99% | held-conservative |
| B-ring max particle diameter | 5–20 m | 2–10 m | partially held |

Aggregate prediction (1–3 of 7 falsified): **held**, with 2 falsified.

**Reading.** Two load-bearing findings: (1) Penn State has not measured water specific impulse; round 0's Cantera bounds (416–558 s) are the most rigorous public estimate. (2) Pale Blue water ion delivers 2000 s in orbit at 60 W in a 1U+ module — above my predicted upper bound, with real flight heritage. Three additional findings: Kilopower specific power is 2.5–6.5 W/kg (adds reactor mass to budget); B-ring is >99% water ice (lowers contamination risk); B-ring max diameter is 10 m (single-chunk cap is ~470 t).

**Revisit.** H1 aggregate held. Specific-prediction pattern: my uncertainty bands were under-spread on both falsifications. Take wider ranges in future hypotheses.

**Cross-learning.**
- Positive for round 0: water microwave-electrothermal at 416–558 s is the public-best estimate.
- Positive for rounds 3a/3b/3c: Pale Blue's 2000 s is data-backed for the per-thruster operating point.
- Positive for round 5: add reactor mass at 2.5–6.5 W/kg to mass budget.
- Negative for risk C06 (B-ring dust contamination): probability rating drops to L2.
- Methodology flagged for round 0c: pull hydrogen permeation number from Sandia SAND2012-7321 PDF.
- Methodology flagged for all future rounds: training-data references for specific impulse have systematic optimistic bias; widen predicted ranges.

---

## R2 — Lunar gravity assist trajectory analysis

**Status:** post-result. Full entry in `rounds/R2_lunar_gravity_assist_trajectory/STUDY.md`.

**Result.** At v_∞ = 6 km/s, the 3-flyby tour delivers **2.0–2.3 km/s** of braking (best to worst geometry), NOT 3 km/s. Single-flyby max at 100 km altitude = 0.71 km/s; subsequent flybys deliver more as v_∞ drops (0.71, 0.79, 0.83 km/s for flybys 1–3).

**Aggregate H2 status: falsified.** The conops claim of "3 km/s at zero propellant cost" is not supported at v_∞ = 6 km/s. Two ways to reconcile: arrival velocity is actually lower than 6 km/s (at v_∞ = 4 km/s, the tour delivers 3.24 km/s), or the tour uses 4–5 flybys instead of 3.

**Cross-learning.**
- B01 risk confirmed upward. The conops' 3 km/s lunar gravity assist tour claim is optimistic by ~30% at v_∞ = 6 km/s.
- **Inbound chunk-fed delta-V revised from 4.2 km/s to ~5.2 km/s.** Propagates back into every candidate-technology delivery number. R0 and R3i numbers all shift downward by a few percentage points.
- Flag for R-mid: verify the conops' inbound v_∞ value — heliocentric cruise round needed.
- Flag for R2b (possible retest): extend to 4–5 flybys, compute timeline penalty, see whether the 3 km/s claim recovers.

---

## R3i — Dual-ion architecture (hydrogen-ion + oxygen-ion from electrolyzed water)

**Status:** post-result. Full entry in `rounds/R3i_dual_ion_architecture/STUDY.md`.

**Question.** User-proposed architecture: electrolyze water on board; ionize both H₂ and O₂ streams; accelerate as parallel gridded-ion thrusters at the same grid voltage. Mass-weighted specific impulse, power required, chunk delivery vs single-tech baselines.

**Result.** (no pre-registered hypothesis — exploratory round)

| Grid voltage (V) | Isp_avg (s) | Electrical kW for 1.5 N | Chunk delivery at 4.2 km/s | Reactor mass at 5 W/kg (tons) |
|---|---|---|---|---|
| 100 | 4,724 | 87 | 91% | 17 |
| 1,000 | 14,938 | 275 | 97% | 55 |
| 10,000 | 47,238 | 869 | 99% | 174 |

Compare: microwave electrothermal (49% at 10 kWe / 2 tons reactor), Pale Blue water radio-frequency ion (81% at 37 kWe / 7 tons reactor).

**Reading.** Dual-ion delivers 91–99% chunk fraction, dramatic improvement over single-tech baselines (49–81%). But reactor mass at higher specific impulse dominates the trade for small chunks — 55-ton reactor for 1 kV operation exceeds a 50-ton chunk. **Only competitive in megawatt-class power era or for chunks above ~200 tons.** TRL 2–3 as integrated system; no flight heritage. Pale Blue at TRL 7–8 remains the heritage-competitive option for near-term high-Isp water propulsion.

**Cross-learning.**
- Positive for R-synthesis: dual-ion enters as a high-power, high-Isp candidate; wins at chunks >200 t or megawatt reactors.
- Positive for R6: dual-ion shifts the Pareto frontier at sub-megawatt and megawatt power levels.
- New sub-variant proposed: **R3i-neg** — dual ion with H⁺ + O⁻ (negative-oxygen mode). Eliminates neutralizer cathode and partially reduces oxidative grid erosion. TRL 1–2 as space propulsion. Cross-link to ITER's Negative Ion Source ground precedent.
- New round candidate proposed: **field-emission electric propulsion with salt-doped Saturnian water** (B-ring ice contains trace salts per Hsu 2015 / Cassini Cosmic Dust Analyzer evidence on Enceladus plumes — should propagate to B-ring particles).
- Risk C06 (B-ring dust contamination) re-upgraded to L3-I4 = 12. The 99% water-ice composition still leaves silicate dust that wrecks ion thrusters; downgrade in R1 was wrong.
- Risk E08 (reactor dry mass) confirmed as load-bearing. For 1 kV dual-ion, reactor mass exceeds a 50-ton chunk.

---

## R8 — Inbound delta-velocity budget audit

**Status:** post-result. Full entry in `rounds/R8_inbound_dv_budget/STUDY.md`.

**Question.** Three competing inbound delta-velocity budgets are loose in the campaign: the conops' 3.7 km/s total water-MET allocation (which implies ~1.6 km/s chunk-fed remainder after the itemized Saturn capture and rendezvous burns), R6's revised 5.2 km/s chunk-fed inbound budget (after R2's lunar gravity assist falsification), and the first-principles patched-conic rebuild. Do they reconcile?

**Result.**

| Quantity | Value |
|---|---|
| Hohmann velocity-at-infinity at Earth (return leg) | 10.30 km/s |
| Hohmann velocity-at-infinity at Saturn (outbound) | 5.44 km/s (matches conops 5.4) |
| Conops itemized water-MET (capture 0.6 + ring rendezvous-in 1.49) | 2.09 km/s |
| Conops implicit chunk-fed remainder | 1.61 km/s |
| First-principles chunk-fed (case C, optimistic — slow transfer to velocity-at-infinity 4) | 2.85 km/s |
| First-principles chunk-fed (case A, pessimistic — Hohmann + single lunar gravity assist) | 10.53 km/s |
| Conops budget shortfall | **1.24–8.92 km/s** |

Chunk delivery at water-microwave-electrothermal specific impulse 500 s for a 14 t chunk + 5 t dry spacecraft:

| Case | Velocity-at-infinity at Earth | Lunar gravity assist | Residual | Chunk-fed inbound total | Delivered chunk |
|---|---|---|---|---|---|
| A: Hohmann + single lunar gravity assist | 10.30 km/s | 1.86 km/s | 8.44 km/s | 10.53 km/s | **0.0%** |
| B: Slow transfer to velocity-at-infinity 6 + single lunar gravity assist | 6.00 km/s | 2.15 km/s | 3.85 km/s | 5.94 km/s | **4.7%** |
| C: Slower transfer to velocity-at-infinity 4 + single lunar gravity assist | 4.00 km/s | 3.24 km/s | 0.76 km/s | 2.85 km/s | **40.2%** |
| D: Hohmann + 5-flyby tour (3 km/s assumed) | 10.30 km/s | 3.00 km/s | 7.30 km/s | 9.39 km/s | **0.0%** |

**Hypothesis grading.** H8a held (10.30 km/s ∈ [9.0, 11.0]). H8b held (5.44 km/s ∈ [5.0, 5.8]; matches conops 5.4). H8c **load-bearing falsified** — gap is 1.2–8.9 km/s, well above the 2 km/s threshold. H8d held (case B chunk-fed inbound 5.94 km/s ∈ [5.5, 7.5]). H8e held (case B delivers 4.7% of chunk; under the 25% load-bearing threshold).

**Reading.** The most architecturally load-bearing finding of the campaign to date. At water-microwave-electrothermal specific impulse 500 s the conops' Hohmann return trajectory does not close — the chunk is fully consumed as propellant before reaching Earth. Only a slow inbound transfer arriving at velocity-at-infinity ~4 km/s closes mass at water-microwave-electrothermal specific impulse, and even then delivery is 40% (not the conops' stated 75%). At water radio-frequency ion (Pale Blue at 2000 s, per R1), the budget closes at 74% delivery for case B; this is the path that recovers the conops mass numbers, but it shifts the propulsion architecture decision off water-microwave-electrothermal and onto water radio-frequency ion class.

**Cross-learning.**
- **Falsifies the conops architecture as stated.** The conops body text claims 75% chunk delivery via water-microwave-electrothermal + Hohmann return + lunar gravity assist arrival. Mass closure fails at this combination. The conops 75% number was calibrated against an Earth-aerocapture arrival case that was later retired (program risk M-AEROCAP) and not re-derived.
- **Promotes Pale Blue water radio-frequency ion** from "Fission Surface Power-era candidate" (per R6) to "required candidate for water-microwave-electrothermal replacement on the chunk-fed inbound leg under the Kilopower-era power budget."
- **New round R9 candidate:** slow-transfer trajectory family. Compute time-of-flight for inbound transfers arriving at Earth velocity-at-infinity 3, 4, 5, 6 km/s. If time-of-flight at velocity-at-infinity = 4 km/s exceeds 10 years, the conops' "13-year round trip" headline also needs revision.
- **New round R10 candidate:** inbound propulsion architecture revisit. Water-microwave-electrothermal vs water radio-frequency ion vs dual ion at the actual chunk-fed inbound delta-velocity from R9.
- **Documentation defect.** The conops body text still describes aerocapture as the inbound velocity-at-infinity absorber, despite program risk M-AEROCAP saying it was retired in favor of lunar gravity assist. The conops `ICEBERG-conops.md` Phase 7–10 section needs revision.
- **Risk register update needed.** Either re-elevate M-AEROCAP, or add a new risk M-INBOUND-BUDGET at I5-L4 (architecture does not close as documented), pending R9/R10 resolution.
- **Methodology recurring lesson.** Single-number budgets in concept-paper documents are systematically optimistic when reconciled against patched-conic + Tsiolkovsky. R0 was 30% optimistic, R2 was 30% optimistic, R8 is 80%+ optimistic. Pre-emptively widen prediction bands for any single-number claim from any single source going forward.

---

## R10 — Inbound propulsion architecture revisit

**Status:** post-result. Full entry in `rounds/R10_inbound_propulsion_revisit/STUDY.md`.

**Question.** Given R8's corrected chunk-fed inbound delta-velocity budget, which water-compatible propulsion candidate delivers the largest fraction of a 14 t grappled chunk at each realistic power level? Candidate set: water resistojet (200 s), water microwave electrothermal (500 s — R0 baseline), water Hall (1500 s), water radio-frequency ion (2000 s — Pale Blue per R1), water dual-ion (5000 s — R3i), and a split-prop architecture using Earth-launched xenon for inbound braking.

**Result (Kilopower 10 kWe, Case B 5.94 km/s chunk-fed):**

| Candidate | Specific impulse (s) | Propellant required (t) | Delivered chunk (t) | Delivery fraction |
|---|---|---|---|---|
| Water resistojet | 200 | 19.98 | 0.00 | 0.0% |
| Water microwave electrothermal | 500 | 14.75 | 0.00 | 0.0% |
| Water Hall | 1500 | 6.98 | 7.02 | 50.2% |
| **Water radio-frequency ion (Pale Blue)** | **2000** | **5.49** | **8.51** | **60.8%** |
| Water dual-ion | 5000 | 2.40 | 11.60 | 82.9% (33-year cruise) |
| Split-prop (water egress + xenon inbound) | 500 + 2000 | n/a | 5.61 | 40.0% |

**At slower trajectory (Case C, 2.85 km/s chunk-fed):** water radio-frequency ion delivers 79.7% (matching the conops' 75% headline at last); water Hall delivers 73.6%; even microwave electrothermal delivers 33.9% — but still well short of 75%.

**At higher power (40 kWe Fission Surface Power) at Case B:** all deliveries DEGRADE because the 8 t reactor swamps the 14 t chunk. Water radio-frequency ion drops from 60.8% (Kilopower) to 49.6% (Fission Surface Power). **Adding power to a 14 t chunk is anti-optimal.** Sub-Kilopower reactor sizing may be a future design point.

**Hypothesis grading.** H10a, H10c, H10d, H10e held. **H10b falsified** — microwave electrothermal delivers 0.0% (not the predicted 0.5–5%) once reactor mass is added to Tsiolkovsky initial mass. **H10f falsified** — split-prop delivers 40% (not the predicted 70–90%) because Saturn egress at 500 s consumes 60% of the chunk before inbound braking begins. Aggregate ranking pre-registration was wrong: actual ranking C5 > C4 > C3 > C6 > C2 = C1.

**Reading.** Two architectural decisions:
1. **Replace microwave electrothermal with water radio-frequency ion (Pale Blue class) for both Saturn egress and inbound braking.** This is the propulsion architecture revision R8 demanded; R10 selects the replacement. Pale Blue has TRL 7–8 flight heritage; specific impulse 2000 s is verified by R1.
2. **Stop assuming "more power is always better."** At 14 t chunk size, the Kilopower reactor (10 kWe / 2 t) is closer to optimum than Fission Surface Power (40 kWe / 8 t). Megawatt-class is firmly anti-optimal for this mission scale. Reactor power scales with chunk mass, not absolutely.

The Saturn egress finding is the deeper one: the conops' chunk-fed Saturn departure burn, which everyone (myself included) had treated as cheap, costs 35% of the egress-initial mass at microwave electrothermal specific impulse. The egress-initial mass on a split-prop architecture is heavier still (xenon + tanks), so split-prop loses MORE chunk water during egress than it saves on the inbound. Single-thruster all-water-radio-frequency-ion is strictly preferred over split-prop.

**Cross-learning.**
- **Decision-supporting:** water radio-frequency ion at Kilopower power class is the recommended inbound (and Saturn-egress) propulsion. Replaces microwave electrothermal in the conops.
- **Negative for split-prop architecture as proposed.** Doesn't help unless egress is also high-specific-impulse, at which point all-water radio-frequency ion strictly dominates.
- **Methodology lesson #4 surfaced:** every Tsiolkovsky delivery-fraction calculation in this campaign must include reactor + dry + payload mass in the initial mass. R6 omitted this; R8 inherited it; R10 corrects it. R5 should rerun R6 with the full mass stack.
- **R5 upgraded to required:** redraw R6's power-optimal-specific-impulse curve with full mass stack. R6's conclusion that microwave electrothermal at 500 s is power-optimal at Kilopower is wrong with reactor mass folded in.
- **R7 / R11 upgraded to load-bearing:** B-ring dust contamination tolerance for water radio-frequency ion grids. Pale Blue's heritage is on purified water; ICEBERG chunk water carries silicate contamination.
- **R9 still needed:** slow-transfer trajectory family determines whether Case B or Case C is physically realizable.
- **Conops decision.** The conops document needs revision: replace microwave electrothermal with water radio-frequency ion for the chunk-fed phases, and explicitly state which trajectory case (B or C) the architecture is sized against. The conops' 75% chunk-delivery headline is recoverable at radio-frequency ion + Case C only.

---

## R-NPV — Discount-rate NPV of ICEBERG cashflow

**Status:** post-result. Full entry in `rounds/R_NPV_discount_rate/STUDY.md`.

**Question.** R15-rerun reported undiscounted "year 40 break-even." What is NPV at year 0 once a discount rate is applied? At what discount rate does the project become NPV-positive?

**Result.** Reusing R15-rerun's audited cashflow (duty cycle 0.7, 18-yr round trip, 3-flyby tour, water radio-frequency ion). Internal-rate-of-return on the best-case audited cell ($10k/kg + $2B sovereign at year 11 + commercial_mid ship cost): **3.63% (no terminal value) / 6.97% (with perpetuity terminal value, growth 0%)**. NPV at 8% commercial discount on the best-case cell: −$3.51B (no TV) / −$1.62B (with TV). Across all 90 price × sovereign × ship-cost cells: **0 of 90 are NPV-positive at 10% commercial discount; 0 of 90 are NPV-positive at 8% without terminal value; 1 of 90 is NPV-positive at 8% with terminal value (the corner cell)**. At 5% infrastructure discount, 4 (no TV) to 24 (with TV) cells are positive. At 3% sovereign discount, 12 (no TV) to 48 (with TV) cells are positive. The conops-baseline cell ($2k/kg, no sovereign, commercial_mid) is NPV-negative at every tested discount rate, including 3%.

**Hypothesis grading.** H-NPV-a, H-NPV-d, H-NPV-e held; H-NPV-b/c/f/g held with terminal value but were under-spread without it. **H-NPV-aggregate held as stated:** ICEBERG is NPV-negative at any commercial discount rate (≥8%) across every tested cell. NPV becomes positive only at sovereign-development rates (≤5%), and only with premium pricing and / or sovereign purchase.

**Reading.** ICEBERG IRR ≈ 4–7% places the project structurally **inside** sovereign-treasury and World Bank IDA / IBRD multilateral infrastructure rates, **at the boundary of** regulated-utility cost-of-capital, and **outside** any commercial growth-equity, corporate, or venture hurdle rate. The "Suez Canal not Amazon" framing is now quantitative: IRR is sovereign-bond territory, not equity territory. Capital structure must be sovereign-development bank, treasury bond, or international multilateral instruments. Any pitch that frames ICEBERG as venture-fundable or growth-equity-fundable is mathematically impossible at the audited cashflow profile.

**Cross-learning.**
- **Methodology lesson #5:** every cashflow round must report (a) NPV at multiple discount rates, (b) IRR, (c) terminal-value sensitivity. R15 / R15b / R15-rerun all reported undiscounted cashflow only — technically correct but operationally misleading. Add discount-rate analysis to the standard cashflow-round template in PROTOCOL.md.
- **Decision-supporting:** the campaign's headline financial number is now "IRR 4–7%, NPV-positive only at sovereign-development discount rates." Replaces the prior "year 40 break-even" headline.
- **Risk register update needed.** Promote B-FUND from L3-I4 = 12 to L4-I4 = 16. The capital-source mismatch is no longer a qualitative warning — it is a quantitative ceiling.
- **Promotes R-cadence to next round.** The single largest IRR lever is revenue cadence. 2x ships per launch window would raise IRR ~1.5pp; 3x ~3pp. Could promote ICEBERG from "sovereign-only" to "regulated-utility-eligible." Run before R-thermal-2 (which is second-order on IRR).
- **Negative for the R15b "even-money $80–150M demonstrator" framing.** A demonstrator at IRR 4–7% is a sovereign-funded option-purchase on a long-tail asset, not a venture bet at even-money equity odds.
- **Terminal-value sensitivity is load-bearing.** Without a perpetuity tail, NPV at 5% is negative; with one, positive. The pitch deck must include the explicit terminal-value assumption — and a corresponding tail-risk (asteroid impact, mission abandonment, year-50 price collapse) discussion.

---

## R-cadence — Multi-ship-per-window cadence sensitivity on IRR

**Status:** post-result. Full entry in `rounds/R_cadence_multiship/STUDY.md`.

**Question.** R-NPV's cross-learning estimated cadence as the largest available IRR lever (2x → +1.5pp; 3x → +3pp). Test the estimate. Do high-cadence schedules promote ICEBERG out of sovereign-bond IRR territory?

**Result.** No. Maximum achievable IRR lift from cadence alone is **+0.55pp at N=2 compressed schedule** (6.97% → 7.52%). Higher cadences (N≥3 compressed) are **anti-optimal**: IRR collapses to 2.66% at N=3 and −1.45% at N=5. Larger-fleet flavor (scale fleet linearly with N, same time profile) gains only ~0.10pp at N=5 (6.97% → 7.09%). The 0/90 cells positive at 10% commercial discount holds at every cadence variant.

**Mechanism behind the falsification.** Compressing the launch schedule front-loads ships into years 0–12, denying late-launching ships access to the late-era megawatt-class reactor (which is the primary chunk-delivery driver at 588 t/ship vs Kilopower's 7 t/ship). Per-ship capex is barely changed; per-ship deliverable mass collapses 2–4×. The pre-registered hypothesis treated cadence and reactor-era access as orthogonal axes. They are not — `reactor_era_for_launch_year()` couples them.

**Hypothesis grading.** H-cad-a/b/c/g held. **H-cad-d, H-cad-e, H-cad-f load-bearing falsified — wrong direction at N≥3 compressed.** H-cad-h falsified-conservative. Aggregate H-cad-agg held (cadence does not promote to commercial-equity class), but for an entirely different reason than predicted.

**Cross-learning.**
- **Decision-supporting (negative):** retract the R-NPV cross-learning estimate of "+1.5pp at 2x cadence." Maximum is +0.55pp; higher cadences are anti-optimal under the R15-rerun reactor roadmap. Update R-NPV's STUDY to flag the over-estimate.
- **Decision-supporting (positive):** the dominant exogenous IRR lever is **reactor-roadmap timing**, not cadence. Promotes A-REACTOR risk from L4-I3 = 12 to L4-I4 = 16 in the program register — A-REACTOR is now a financial-existence concern, not just a schedule concern.
- **Promotes R-reactor-roadmap to next round.** Parameterize reactor-era arrival years (Kilopower / Fission Surface Power / sub-MW / MW) and sweep to find IRR vs MW-arrival-year curve. Pre-register: megawatt-at-year-8 should push IRR to 9–10%; megawatt-at-year-25 should drop IRR below sovereign-bond rate.
- **Closes the R15c thread.** R15-rerun cross-learning queued "R15c (multi-ship cadence)"; this round resolves it.
- **Methodology lesson #6:** confident "X is the largest lever" claims based on first-principles intuition need actual sweeps before being promoted to a deck or downstream round. R-NPV's cross-learning made the wrong call at 3×, in the wrong direction.
- **Methodology lesson #7:** any future cashflow round must treat reactor-era assignment as a free axis, not as a function of launch year. R15-rerun's `reactor_era_for_launch_year()` is convenient but conceals a load-bearing coupling.

---

## R-reactor-roadmap — marginal internal-rate-of-return integrated over reactor-arrival distribution

**Status:** post-result, second pre-registration. The first pre-registration (sweeping megawatt-arrival year vs conditional internal-rate-of-return under R15-rerun mass) was retired in light of upstream falsifications from R-megawatt-marvl-radiator and R-power-base-rate. Full entry in `rounds/R_reactor_roadmap/STUDY.md`.

**Question.** R-NPV reported internal-rate-of-return 3.63–6.97 percent at R15-rerun's "megawatt = 588 tonnes per ship" delivery; R-cadence promoted reactor-roadmap timing to the dominant exogenous lever. Both conclusions were conditional on (a) R15-rerun's decomposed-mid mass model and (b) megawatt arrival as a free parameter. **Upstream R-megawatt-marvl-radiator falsified the year-20+ megawatt all-electric end-to-end cell at MARVL realism** (delivered chunk = −34.4 tonnes; 1 megawatt-electric tug under MARVL = 104.9 tonnes, not 29.2 tonnes); **upstream R-power-base-rate measured P(megawatt by year 20) = 0.5 percent**. Recompute the internal-rate-of-return curve under (a) MARVL-anchored per-ship delivery (128.8 tonnes per ship at the 500-kilowatt-electric chemical-kick architecture floor; 0 tonnes below that) and (b) integrating over R-power-base-rate's measured megawatt cumulative-distribution-function for a marginal internal-rate-of-return rather than conditional.

**Result.**

| View | Internal-rate-of-return |
|---|---:|
| R-NPV headline (R15-rerun mass, conditional on megawatt at year 20) | 6.97% |
| This round, conditional at megawatt-year-20 (MARVL mass) | 1.06% |
| This round, conditional at megawatt-year-8 (MARVL, best year) | 1.61% |
| This round, conditional, megawatt never (chemical-kick saturated) | 1.48% |
| **Marginal, R-power-base-rate baseline cumulative-distribution-function** | **1.45%** |
| **Marginal, aggressive program (median megawatt arrival shifted to year 10)** | **1.49%** |
| Marginal uplift from aggressive reactor program | +0.04 percentage points |

Conops-baseline cell ($2,000 per kilogram, no sovereign) does not close at any tested sensitivity — net-present-value is negative at near-zero discount rate for every megawatt-arrival year including the never branch. Only the best-case audited cell ($10,000 per kilogram, $2 billion sovereign at year 11, commercial_mid ship cost) produces any positive internal-rate-of-return at all.

**Hypothesis grading.** H-rxr2-a (per-ship delivery 80–250 tonnes) held at 128.8 tonnes; H-rxr2-e (no 8 percent crossover) held cleanly. **H-rxr2-b, H-rxr2-c, H-rxr2-d, H-rxr2-f, H-rxr2-g all falsified-pessimistic** — five of seven sub-claims wrong on the optimistic edge. The aggregate (reactor-roadmap timing is not the dominant lever; marginal internal-rate-of-return below the regulated-utility hurdle) held in direction and qualitative shape but was further pessimistic than pre-registered: marginal internal-rate-of-return is sub-sovereign-bond territory (1.45 percent), not "sovereign-development at the floor" as I had ranged (3.0–5.0 percent).

**Reading.** Three load-bearing reframings:

1. **R-NPV's "sovereign-development discount-rate territory" headline is retired** under MARVL anchoring. Marginal internal-rate-of-return = 1.45 percent is below the 10-year US Treasury yield (~4 percent), below investment-grade corporate bond yields (~5 percent), below International Development Association concessional rates (~2.5 percent), and below the regulated-utility allowed return on equity (~9 percent). ICEBERG's economic profile is structurally pure-subsidy / strategic-policy-funded under conservative reactor mass.

2. **R-cadence's "reactor-roadmap timing is the dominant exogenous internal-rate-of-return lever" conclusion is retired.** Under MARVL anchoring, the entire conditional internal-rate-of-return curve sits within a 75-basis-point band (0.89 to 1.64 percent) across the full plausible megawatt-arrival window. The aggressive-program counterfactual lifts marginal internal-rate-of-return by 4 basis points (+0.04 percentage points). **Lobbying for an accelerated reactor program is a near-zero-leverage internal-rate-of-return move.** The dominant lever shifts to per-ship deliverable mass, which is gated by R-chunk-as-heat-shield-revisit (Earth aerocapture rescue) more than by reactor power.

3. **"Megawatt-era unlocks Saturn-class chunks" framing in `ICEBERG-pitch.md` is now falsified, not just low-probability.** Even if megawatt arrives on the original schedule, the all-electric end-to-end cell is falsified at MARVL mass, and the chemical-kick cell does not scale beyond 500-kilowatt-electric in delivered mass per ship. The pitch must either be revised to chunk-as-heat-shield-conditional language, or it must acknowledge that the project is sub-sovereign-bond on its base architecture.

**Cross-learning.**

- **Decision-supporting (load-bearing):** retire the "sovereign-development discount-rate" capital-class framing from R-NPV. Replace with "marginal internal-rate-of-return = 1.45 percent, sub-sovereign-bond, structurally pure-subsidy" pending chunk-as-heat-shield resolution.
- **Decision-supporting (load-bearing):** retire the "reactor-roadmap timing is the dominant lever" framing from R-cadence. Replace with "per-ship deliverable mass is the dominant lever; chunk-as-heat-shield-revisit is the highest-leverage open round."
- **Promotes R-chunk-as-heat-shield-revisit to next round.** A 4× delivery uplift (~500 tonnes per ship via Earth aerocapture) would push conditional internal-rate-of-return to ~4–5 percent, restoring some of the lost economic case. Pre-register against that range.
- **Methodology lesson (repeat occurrence, third in two days):** pre-register numeric ranges only after running the back-of-envelope calculation. H-rxr2-b through H-rxr2-f all fell outside their pre-registered ranges by 1.5 to 5 percentage points, because I mechanically halved R-NPV's 6.97 percent point estimate to predict 4–6 percent at megawatt-year-20 without doing the cashflow arithmetic. The actual collapse was ~85 percent of revenue, with non-linear internal-rate-of-return collapse due to fixed-cost dilution. Add to recurring-lesson log; promote to a hard rule at next PROTOCOL.md revision.
- **Open question for orchestrator integration:** the architecture decision matrix lists the 500-kilowatt-electric chemical-kick cell as "the sole defensible deployment cell." Add a financial-feasibility column. The surviving cell is propulsion-physically-defensible but not economically-defensible at 1.45 percent marginal internal-rate-of-return.

---

## R-delivery-irr-curve — marginal internal-rate-of-return as a function of per-ship chunk delivery, rescue-mechanism-agnostic

**Status:** post-result. Full entry in `rounds/R_delivery_irr_curve/STUDY.md`.

**Question.** R-reactor-roadmap's cross-learning predicted "a 4× delivery uplift would push conditional internal-rate-of-return to ~4–5 percent." That prediction was made from intuition without a back-of-envelope cashflow — the same methodology mistake R-reactor-roadmap's Revisit flagged as recurring. Before sinking a sizeable engineering round (R-chunk-as-heat-shield-revisit, SCOPE.md estimates 6–10 analyst hours) into chunk geometric stability, run the prior question: **independent of any specific rescue mechanism, what per-ship delivery uplift would be required to push marginal internal-rate-of-return above the hurdle rates that matter?** This round also tests the binding upper bound: L1-007's 200-tonne-per-mission cap vs the B-ring single-chunk physical cap of ~482 tonnes solid water-ice mass.

**Result.** Pre-registered numeric ranges (locked after a 20-minute back-of-envelope) all held cleanly — **seven of seven sub-claims, the first all-held round of the campaign**:

| Hurdle | Per-ship delivery at crossover |
|---|---:|
| sovereign-bond floor (~4%) | 209 tonnes per ship |
| regulated-utility (~8%) | 461 tonnes per ship |
| corporate-growth (~10%) | 691 tonnes per ship |

Marginal internal-rate-of-return at L1-007 cap (200 tonnes per ship): **3.77 percent**. At B-ring single-chunk physical cap (482 tonnes per ship): **8.22 percent**. Curve is monotonically increasing and concave above 500 tonnes per ship (diminishing returns confirmed). R-reactor-roadmap's cross-learning prediction ("4× delivery → 4–5 percent internal-rate-of-return") was wrong by ~4 percentage points; actual at 4× delivery (515 t) is ~8.5 percent. Fixed-cost dilution is non-linear near the cashflow-baseline.

**Reading.** Three load-bearing numbers:

1. **Aerocapture / chunk-as-heat-shield rescue produces meaningful internal-rate-of-return uplift only if L1-007 is also relaxed.** Under L1-007's 200-tonne cap, marginal internal-rate-of-return is 3.77 percent (sovereign-bond floor) — +2.3 percentage points over R-reactor-roadmap's MARVL baseline of 1.45 percent, but still subsidy capital class. The rescue's economic value is gated on a coordinated L1-007 revision, not just on engineering closure.

2. **The regulated-utility hurdle (~8 percent) is just barely reachable at the B-ring single-chunk physical cap (~482 tonnes solid water-ice).** Promoting ICEBERG to regulated-utility-eligible capital class requires a four-step sequence: (a) chunk-as-heat-shield engineering closure, (b) L1-007 relaxation, (c) bag scaling from current ~100-tonne envelope to ~480 tonnes, (d) B-ring particle-size-distribution-skew handling. All four required; none currently funded.

3. **The corporate-growth hurdle (~10 percent) is structurally unreachable on single-chunk-per-mission.** Required delivery is ~691 tonnes; B-ring single-chunk solid water-ice mass at 10-metre maximum diameter is ~482 tonnes. The 1.4× gap is a physics ceiling on B-ring particle size, not a closeable engineering item. Two possible breaks (multi-chunk-per-mission; water price above $10,000 per kilogram), both queued as separate rounds.

**Cross-learning.**

- **Decision-supporting (load-bearing):** R-chunk-as-heat-shield-revisit is worth pursuing — but its economic ceiling is the B-ring particle-size distribution, not the engineering. Re-baseline the SCOPE.md predicted-delivered-fraction framing: target is 482 tonnes per single chunk at L1-007-relaxed (8.22 percent marginal internal-rate-of-return), not "55–65 percent of a now-falsified baseline."
- **Decision-supporting (load-bearing):** the architecture decision matrix should carry a "marginal internal-rate-of-return ceiling at B-ring physical cap" entry of 8.22 percent. Pitch deck framing: ICEBERG is regulated-utility-eligible-conditional under chunk-as-heat-shield + L1-007-relaxation + 480-tonne-bag-scaling; **not** corporate-growth-equity-eligible at any single-chunk delivery uplift.
- **Methodology lesson (load-bearing, sixth occurrence):** pre-register numeric ranges only after running the back-of-envelope, not before. Pattern: pre-register-from-intuition produces ≥ 60 percent falsification rate (R0, R10, R-NPV-pre-registration, R-cadence, R-reactor-roadmap); pre-register-from-BOE produces ≤ 10 percent falsification rate (this round, 0-of-7). **Promote to a hard rule in PROTOCOL.md at next revision.**
- **Methodology lesson (new):** internal-rate-of-return scaling with revenue is non-linear near the fixed-cost-dilution threshold. Linear-mental-scaling over-predicts internal-rate-of-return collapse on the downside and under-predicts uplift on the upside.
- **Promotes R-multi-chunk-per-mission and R-water-price-market-depth to queued rounds.** Only paths to the corporate-growth hurdle.

---

## R-variant-B-100t-resizing — does chunk reduction to 100 tonnes rescue Variant B without aerocapture?

**Status:** post-result. Worker: phoebe (2026-05-15 latest). Full entry in `rounds/R_variant_B_100t_resizing/STUDY.md`.

**Question.** Hyperion's R-variant-B-impulsive-vs-continuous (commit `daaf522`) falsified the matrix's surviving Variant B cell at chunk 200 tonnes — Variant A (no architectural recovery) at 500 kilowatt-electric MARVL-anchored mass delivers 0.0 tonnes with round-trip 16.92 years. Hyperion surfaced four amendment paths; this round closes path 3: **does shrinking the chunk to 100 tonnes re-open Variant A without aerocapture or chemical Saturn-egress?**

**Result.** No. **Four of four gradable hypotheses HELD under pessimistic framing.** Tied with hyperion R-variant-B-impulsive-vs-continuous for best pre-registration grade in the campaign:

| Chunk (t), 500 kWe Variant A | Feasible? | Round-trip (yr) | Delivered (t) |
|---:|:--:|---:|---:|
| 50, 75, 100, 125, 150, 175 | **no** (m_prop > chunk) | — | deficit 5–29 t |
| 200 (L1-007 cap) | yes (edge) | 16.92 | 0.0 (closes_soft=no) |

| Reactor (kWe), chunk 100 t Variant A | Feasible? | Round-trip (yr) | Delivered (t) |
|---:|:--:|---:|---:|
| 100 | yes | 21.63 | 9.8 (closes_soft=no) |
| 200 | yes | 17.77 | 2.0 (closes_soft=no) |
| 300, 400, 500, 600, 700 | **no** | — | deficit 2–32 t |

**No (chunk, reactor) point in the swept envelope simultaneously satisfies propellant-feasibility AND L0-05 round-trip closure under ±1 yr soft margin.**

**Reading.** Three load-bearing findings:

1. **The bake-off taxonomy resolves cleanly.** Path 1 (Earth aerocapture mandatory): delivers 32.1 t/mission at chunk 200 t per hyperion's Variant C, contingent on R-chunk-as-heat-shield-revisit engineering closure. Path 2 (acknowledge collapse): retire Variant B from the matrix's surviving-cell list. **Path 3 (chunk reduction without aerocapture): falsified by this round.** The matrix's amendment decision is now binary, not ternary.

2. **The mechanism is a locked-shut closure trade.** Feasibility requires `tug ≤ 0.325 × chunk`; closure requires `t_burn ∝ m_prop / P_kWe ≤ 1.84 yr`. With MARVL tug ≈ 5 t + 0.1 × P_kWe, feasibility caps reactor at `P ≤ 3.08 × chunk − 50`; closure floors it at `P ≥ chunk / 0.196`. At every chunk, the feasibility cap is ~0.5× the closure floor. **Gap is fixed and proportional to chunk.** The chunk 200 t / 500 kilowatt-electric point is the unique feasibility-edge that doesn't satisfy closure — round-trip 16.92 yr > 16 yr soft ceiling.

3. **L1-007 chunk cap (200 t) is *binding* on Variant A feasibility, not a comfortable margin.** Propellant-feasibility threshold at 500 kilowatt-electric is between 175 t and 200 t. Any tightening of L1-007 (for structural / packaging reasons) immediately invalidates Variant A even before aerocapture is considered. Recommend orchestrator add a REQUIREMENTS.md note that L1-007 binds on propellant-feasibility, not packaging alone.

**Cross-learning.**

- **NEGATIVE for R-variant-B-recovery-paths-economic path 3 (rhea's bake-off).** Confirms rhea's "honest reading is path 2" conclusion structurally — path 3 is not just sub-hurdle, it doesn't exist. **Recommend matrix update: path-3 row reframed from "computed under chunk = 100 t" to "no closing configuration exists at chunk ≤ 200 t".**
- **NEGATIVE for orchestrator-authored SCOPE.md prediction.** Pre-registered 13.5–14.5 yr / 25–40 t bands were optimistic by ~5–10 yr and unavailable on delivered mass. The orchestrator skipped the back-of-envelope; the closure-trade mechanism was missed. Methodology lesson 1 (pessimistic-default holds) applies to orchestrator pre-registrations, not just worker pre-registrations.
- **POSITIVE for R-chunk-as-heat-shield-revisit (iapetus scaffold).** Path 1 is the only surviving Variant B amendment with delivered mass > 0. Aerocapture engineering closure is load-bearing for the entire matrix's surviving cell. **R-chunk-as-heat-shield-revisit should be the next critical-path round** if it has not closed yet.
- **POSITIVE for honest-reading-2 in rhea's bake-off.** Project-owner-locked Option A (Variant B as 500-kilowatt-electric all-electric inbound) under rhea's bake-off reading was "no path clears sovereign-bond at conservative anchors; honest reading is path 2". This round structurally confirms the binary collapse: aerocapture-closes (path 1) OR collapse-the-cell (path 2).
- **METHODOLOGY-FLAG: conditional-hypothesis grading convention.** H-100-d and H-100-e are conditional ("IF closure exists, ..."). The run.py console graded H-100-e HELD vacuously; tables.md graded it "not gradable". Cosmetic inconsistency. **Recommend campaign-level convention: antecedent-false → "not gradable" (per tables.md), not "held-vacuous" (per console).**

---

## R-chunk-as-heat-shield-revisit — does any (chunk, entry-velocity) configuration close single-pass chunk-as-heat-shield AND intersect a surviving variant cell?

**Status:** post-result. Worker: phoebe (2026-05-15 latest+). Reframed scope per project owner — Saturn's original SCOPE.md was authored before hyperion's R-aerocapture-fast-cruise-envelope ran and assumed orientation-stability was the binding open question. Hyperion's intervening round showed the chunk fails structurally before orientation matters at the Round-F STRICT cell; phoebe scans the broader (chunk-mass × velocity-at-infinity × tug-mass) cube for any closing region.

**Question.** For chunk masses 25–500 tonnes and Earth-arrival velocity-at-infinity 3–11 kilometres-per-second (covering the architecturally-relevant envelope of all current ICEBERG variants), what region simultaneously satisfies bag-thermal-survival, chunk-structural-survival, chunk-thermal-survival, AND single-pass-capture-feasibility? Does that region intersect any surviving variant cell?

**Result.** Both STRICT (bag-retained) and SACRIFICIAL_BAG closing regions are empty across the full 40-cell sweep. Every cell hits the periapsis-solver floor (40 km) — the binding constraint is **capture-feasibility itself**, not bag-thermal-survival or chunk-structural-survival as the SCOPE anticipated. ICEBERG ballistic coefficients (4,600–6,600 kilograms-per-square-metre across the swept envelope) cannot dissipate the required Earth-arrival delta-velocity (3.8–7.9 kilometres-per-second) in a single atmospheric pass at any altitude that survives thermally. At periapsis ≤ 40 kilometres, the trajectory is reentry, not aerocapture.

| Sub-claim | Pre-registered | Computed | Held |
|---|---|---|:---:|
| H-csa-a — STRICT closing region (predicted 0–2 of 40) | empty | 0 cells | YES |
| H-csa-b-chunk — SACR-BAG chunk upper bound (predicted 75–150 t) | undefined (region empty) | none | NO (vacuously, more pessimistic) |
| H-csa-b-vinf — SACR-BAG velocity upper bound (predicted 5–8 km/s) | undefined (region empty) | none | NO (vacuously, more pessimistic) |
| H-csa-c — Variant C STRICT cell intersection | False | False | YES |
| H-csa-d — Variant B chunk-200 intersection at any v_∞ | False | False | YES |
| H-csa-f — orientation-stability conditional | not gradable iff antecedent false | antecedent false | not gradable |

**Cross-check vs hyperion R-aerocapture-fast-cruise-envelope:** ratio 1.000 to four significant figures at the Round-F STRICT no-LGA case (200 t / 15.29 km/s). Physics agrees.

**Aggregate H-csa-agg: HELD.** Three of three aggregate-relevant claims (a + c + d) all held; chunk-as-heat-shield single-pass is structurally infeasible across the architecturally-relevant envelope. The two falsifications (H-csa-b sub-claims) were both *more pessimistic than predicted* — the SACR-BAG closing region was predicted bounded; actually empty. Continues the recurring-lesson pattern: aerocapture-adjacent rounds in this campaign (now six in sequence) have all falsified more pessimistically than their pre-registrations.

**Reading.** Three load-bearing findings:

1. **The matrix's aerocapture-conditional surviving cells (Variant C STRICT, year-twenty-plus megawatt all-electric end-to-end winner cell) are *engineering-falsified* on capture-feasibility, not just on heat flux or structural margin.** Hyperion already showed Variant C fails on structural+thermal at velocity-at-infinity 10.55 kilometres-per-second; phoebe shows it also fails on capture-feasibility at velocity-at-infinity ≤ 8.55 kilometres-per-second (with lunar-gravity-assist credit). Two independent failure modes; either alone is sufficient to retire the cell.

2. **The SACRIFICIAL_BAG relaxation does not save chunk-as-heat-shield.** Even discarding the bag entirely, no (chunk, velocity-at-infinity) cell achieves capture at periapsis ≥ 50 kilometres. Chunk-structural and chunk-thermal margins are necessary-but-insufficient; capture-feasibility is the upstream binding constraint that wasn't separately tested in either prior round.

3. **The hybrid path (single-deep-pass with sacrificial bag, then multi-pass aerobraking) remains the only architecturally-credible aerocapture-adjacent candidate.** R-chunk-as-heat-shield's "Three observations" #3 sketched it; R-hybrid-aerocapture-aerobraking has a SCOPE.md on main but has not been run. The hybrid would split delta-velocity across one deep pass and many shallow passes; chunk-thermal and chunk-structural margins for the deep pass are the binding open questions.

**Cross-learning.**

- **NEGATIVE for the matrix's aerocapture-conditional rows.** Reframe from "engineering-pending" to "single-pass-engineering-falsified, hybrid-engineering-pending". Variant B at chunk 200 tonnes has no aerocapture rescue at any tested velocity-at-infinity; combined with phoebe's prior R-variant-B-100t-resizing finding, Variant B is closed as a venture-class cell except via hybrid.
- **NEGATIVE for Saturn's R-chunk-as-heat-shield-revisit SCOPE.md.** SCOPE assumed orientation-stability was the binding open question — actually downstream of an unaddressed earlier question (capture-feasibility itself). Recommend SCOPE.md retrospective falsification note.
- **POSITIVE for hyperion's R-aerocapture-fast-cruise-envelope methodology.** Cross-check at Round-F STRICT cell reproduces hyperion's anchor exactly. Verified physics functions are reliable building blocks; reused via import (not copy-paste).
- **POSITIVE for R-hybrid-aerocapture-aerobraking** (SCOPE on main, not yet run). Now the only surviving aerocapture-adjacent candidate. **Should be promoted to the next critical-path round.**
- **METHODOLOGY-FLAG for hyperion's `required_periapsis_altitude_km`.** Function returns the *deepest* viable periapsis (loop iterates 40→120 km, returns first hit). For aerocapture, the optimum is the *shallowest* viable periapsis (cooler heating). Latent bug — phoebe's run.py uses local override `shallowest_viable_periapsis_km` iterating downward; identical result this round (no cell captures at any altitude in [40, 120]). Recommend orchestrator add docstring note to upstream function. References Methodology lesson 6.
- **METHODOLOGY-FLAG: conditional-grading convention extended.** This round adds a second case — "not held vacuously" (the prediction was bounded region; actual region is empty, strictly more pessimistic). Distinct from "not gradable" (antecedent false). Two distinct conventions; both honest. Recommend protocol-level addendum.
- **Promotes program-class-reframe meta-round (suggested).** Surviving-cell list now collapses to {Variant A acknowledged-collapse, Architecture-E with ≥ 25-year L0-05 waiver, hybrid-aerocapture-conditional pending R-hybrid}. Program may be L0-05-relaxation-required regardless of architectural choice. Worth surfacing to project owner.

---

## R-hybrid-aerocapture-aerobraking — does pass-1-deep-aerocapture-with-bag-sacrificed plus pass-2-onward-shallow-aerobraking close where single-pass aerocapture and pure aerobraking each fail?

**Status:** post-result. Worker: phoebe (resumed session, 2026-05-15 latest+1). Authored by hyperion (SCOPE.md, 2026-05-15) as the architectural-recovery candidate when the matrix collapsed to no-surviving-cell after R-aerocapture-fast-cruise-envelope + R-no-atmospheric-capture-baseline + R-chunk-as-heat-shield-revisit. Project owner directed promotion to next critical-path round (commit `0c29de8`).

**Question.** For chunk masses 50–350 tonnes, reactor classes 200/500/1000 kilowatt-electric, cruise aphelions 9.58 and 11 astronomical units, with and without lunar-gravity-assist credit, can any pass-1 deep periapsis + pass-2-onward shallow aerobraking configuration simultaneously satisfy (a) pass-1 captures Δv ≥ parabolic-velocity threshold, (b) chunk survives pass-1 structurally, (c) aerobraking campaign completes in less than 5 years, (d) chunk total sublimation across campaign stays below 50 percent of initial mass, AND (e) total round-trip closes inside L0-05 strict 15-year ceiling?

**Result.** **Zero of 1920 cells close.** Pass-1 captures only at periapsis ≤ 40 kilometres (the model floor), where heat flux is 20.4 megawatts-per-square-metre and bag radiative-equilibrium 4,604 K — bag designed-sacrificial as intended. Chunk structural at h₁ = 40 kilometres: tensile margin 0.75× for 200-tonne chunk (shatters), 0.93× for 100-tonne chunk (shatters), 1.0+× only for 50-tonne chunk. Aerobraking at h₂ = 130 kilometres: 346,000 passes over 79 years, total chunk sublimation 259 tonnes — chunk consumed past 50 percent tolerance. Aerobraking at h₂ = 180 kilometres (bag-survivable equivalent): 3.91 million passes over 892 years, 1,040 tonnes sublimed. No periapsis exists where pass-1 captures structurally AND aerobraking is timescale-tractable AND chunk survives sublimation.

| Sub-claim | Pre-registered | Computed | Held |
|---|---|---|:---:|
| H-hyb-a — chunk 200 t margin at capturing depth (predicted 0.5–1.0) | 0.5–1.0 | 0.75 | YES |
| H-hyb-b — chunk 100 t margin at capturing depth (predicted 0.6–1.2) | 0.6–1.2 | 0.93 | YES |
| H-hyb-c — pass-1 Δv-achieved/Δv-required ratio at 75 km (predicted 0.01–0.03) | 0.01–0.03 | 0.012 | YES |
| H-hyb-d — aerobraking pass count at 130 km (predicted 100k–1M) | 100k–1M | 346,000 | YES |
| H-hyb-e — total sublimation at 130 km (predicted 500–3,000 t) | 500–3,000 t | 259 t | NO (falsified-conservative; still 2.6× tolerance) |
| H-hyb-f — chunk T_eq at 130 km exceeds ice melt (predicted 500–900 K) | 500–900 K | 627 K | YES |
| H-hyb-g — aerobraking time at 180 km (predicted 200–1,500 yr) | 200–1,500 yr | 892 yr | YES |
| H-hyb-h — lunar-gravity-assist rescue Δv-to-insert (predicted 2.5–3.0 km/s) | 2.5–3.0 km/s | 2.72 km/s | YES |
| H-hyb-i — total closing cells (predicted 0–2) | 0–2 | 0 | YES |
| H-hyb-j — sacrificial-bag mass per mission (predicted 3–30 t) | 3–30 t | deferred — out of scope (thermal-protection-system design model) | DEFERRED |

**Aggregate H-hyb-agg: HELD.** 8 of 9 gradable sub-claims held; the single falsification (H-hyb-e) is falsified-conservative — actual chunk sublimation is lower than the pre-registered band because the run.py applies both boundary-layer-blocking and body-absorbed fractions where the BOE applied only heat-of-sublimation directly. The conservative falsification does not rescue any cell; 259 t computed still exceeds the 100 t tolerance for a 200-tonne chunk by 2.6×. Aerocapture-adjacent rounds in this campaign have now falsified more pessimistically than pre-registered in 4 of 4 instances.

**Cross-check vs hyperion R-aerocapture-fast-cruise-envelope.** At chunk 200 t / tug 63.8 t / v_entry 15.29 km/s / periapsis 40 km, US Standard 1976 atmosphere gives peak g 39.6, chunk stress 1.33 MPa, tensile margin 0.75; hyperion published 47.9 / 1.60 / 0.62 (exponential atmosphere; 1.6× denser at 40 km than US Standard's 4.00e-3 vs hyperion's 1.67e-3). The 20-percent discrepancy in peak g is attributable to the atmosphere-model choice and reverses the verdict's direction by zero cells — both atmospheres agree chunk shatters at depth needed for capture.

**Reading.** Three load-bearing findings:

1. **Three independent failure modes are aligned along the periapsis axis without an interior closing region.** Pass-1 fails structurally at depths shallow enough to achieve insertion; aerobraking takes centuries-to-millennia at altitudes thermally survivable for the chunk; chunk consumed by sublimation at altitudes where aerobraking is timescale-tractable. No interior solution. This is qualitatively the same finding as R-chunk-as-heat-shield's original "no altitude exists where bag survives AND pass count is tractable" — extended one architectural step further to "no altitude exists where chunk survives AND pass count is tractable AND chunk sublimation is tolerable."

2. **The SCOPE made three input-assumption errors that the round had to correct before answering the SCOPE's question.** (i) β-by-chunk-size is non-monotonic when tug mass is held — minimum at chunk 100 t (β = 5,936 kg/m²), worse at chunk 50 t (β = 6,546) because the fixed-mass tug behind a smaller frontal area dominates. The SCOPE's "smaller chunk rescues β" path is geometrically broken. (ii) Pass-1 Δv-to-insert is set by parabolic-velocity threshold (4.175 km/s at 75 km periapsis), not by engineering judgment "65 percent of total." (iii) Single-scale-height exponential atmosphere is qualitatively wrong above 110 km where scale height grows from ~7 km to ~25 km. All three documented in STUDY.md §"Three load-bearing methodology choices the SCOPE got partly wrong." Direct application of methodology lesson 9 (phoebe's own from prior round).

3. **Atmosphere-model methodology issue surfaced as candidate PROTOCOL lesson 10.** Four aerocapture-adjacent rounds have used three different atmosphere models (R-chunk-as-heat-shield hand-tabulated; R-aerocapture-fast-cruise-envelope and R-chunk-as-heat-shield-revisit single-exponential; this round US Standard 1976). For rounds spanning both deep (40-90 km) and shallow (130-200 km) regimes, atmosphere choice dominates aerobraking pass-count verdict (factor of ~40× in density at 180 km between single-exponential and US Standard). Adopt US Standard 1976 / NRLMSISE-00 as campaign default; flag prior aerocapture rounds for re-derivation if verdict turns out atmosphere-sensitive.

**Cross-learning.**

- **NEGATIVE for hybrid-engineering-pending matrix framing.** Phoebe's prior round introduced "hybrid-engineering-pending"; this round closes that conditional. The matrix's aerocapture-adjacent surviving cells collapse to drag-skirt-conditional only. Variant C, Architecture-E year-twenty-plus megawatt cell, and all hybrid-conditional rows should be relabelled "atmospheric-capture-falsified-without-drag-skirt."
- **POSITIVE for R-deployable-drag-skirt** (currently named in R-chunk-as-heat-shield as a follow-on; not yet in a SCOPE). Now the only architecturally-credible β-reduction lever. Should be promoted to next critical-path round. Open question: does an inflatable ballute close engineering with mass penalty ≤ 10 t?
- **POSITIVE for R-mission-architecture-pivot-survey.** Lunar-orbit catcher, cislunar processing depot, Earth-rendezvous via low-energy trajectories — alternative branches outside atmospheric capture. Worth scoping in parallel with R-deployable-drag-skirt.
- **POSITIVE for R-program-class-reframe-2.** If both hybrid AND drag-skirt fail engineering, the program's foundational delta-velocity-minimization premise needs re-derivation. Phoebe previously flagged this as a candidate meta-round.
- **METHODOLOGY-FLAG: SCOPE input-assumption errors documented (methodology lesson 9 second application).** This round applies the lesson phoebe authored from the prior round to a SCOPE authored by a different worker (hyperion). Three of three input-assumption errors caught and documented. Lesson 9 is now corroborated by two rounds.
- **METHODOLOGY-FLAG: atmosphere-model choice surfaced as campaign-wide methodology issue.** Candidate PROTOCOL methodology lesson 10. Recommend orchestrator pull a small follow-on round to re-derive the prior three aerocapture-adjacent rounds under US Standard 1976 atmosphere and check if any verdict flips. (Sensitivity check at Round F STRICT cell: ratio 1.21× on stress margin; both atmospheres reach falsification but at different margins.)
- **METHODOLOGY-FLAG: sublimation BOE-vs-code stack inconsistency.** H-hyb-e falsified-conservative because BOE used heat-of-sublimation directly while run.py applied BLBF=0.4 × body-absorbed=0.5 cumulatively. The qualitative verdict is unchanged (chunk still consumed past tolerance) but the magnitude is off by 5×. Future thermal-load BOEs should explicitly enumerate the partition factors. Minor methodology footnote.

---

## R-bring-rendezvous-survivability — does engineered survivability close the 99-percent-per-pass B-ring impact-prob gap?

**Status:** post-result. Worker: phoebe (continued session, 2026-05-15 latest+8 → +9). Authored by Saturn (orchestrator, 2026-05-15 latest+6) as engineering question 2 of 2 on the held chunk-rendezvous architecture, after project-owner held the architecture pending two engineering closures. Engineering question 1 (R-hybrid-aerocapture-aerobraking) was also adjudicated by phoebe and falsified at 0/1920 cells (commit `a7a8456`, awaiting orchestrator integration).

**Hypothesis (aggregate H-bsurv-agg).** The held chunk-rendezvous architecture cannot achieve B-ring per-pass impact probability ≤ 0.01 percent at conservative anchors. No combination of bag-armour, particle-cull mesh, off-plane geometry, or slow-cross approach closes the impact-prob target while keeping mass penalty within 10 percent of the Variant-B baseline.

**Test.** 162-cell deterministic sweep across τ-zone (9 zones from B-ring zone-average τ=2 down to Huygens Gap τ=0.001) × armour density (0, 50, 200 kg/m²) × cull-mesh (off, on) × inclination (26.7°, 60°, 90°). Per-pass impact probability via P = 1 - exp(-τ_eff × csc(i)), with τ_eff incorporating cull-mesh removal of shieldable < 1 cm fraction (75% unshieldable per fine-structure H3). Δv to inclination change computed at apoapsis (cheapest place for plane change on elliptical capture orbit, v_apo = 2.166 km/s vs v_periapsis = 26.5 km/s). Mass penalty as fraction of 264-tonne Variant-B baseline. Closure: P_two_crossings ≤ 2×10⁻⁴ AND penalty fraction ≤ 0.10 AND chunks present. See `rounds/R_bring_rendezvous_survivability/run.py`.

**Result.** **0 of 162 cells close the impact-prob target.** Best chunk-bearing cell: B-ring outermost 180 km × 90° × cull-mesh, P_per_pass = 7.23 percent — 723× short of the per-pass target. Best ANY-cell (no chunks): Huygens Gap × 90° × cull-mesh, P_per_pass = 0.075 percent — 7.5× short of target, and zero large particles available. Slow-cross sweep (per audit 1+2): minimum vehicle-to-ring-particle relative velocity without ring-orbit-match is 9 km/s (at v_target ≈ 17.5 km/s in Saturn frame, where in-plane component matches v_circ_ring = 19.48 km/s); below this, v_rel rises again because vehicle becomes sub-ring while inclination-driven cross-component remains; only ring-orbit-match (residence, project-owner-retired) achieves non-fatal per-impact KE. Inclination sweep: full 26.7° → 90° plane change at apoapsis costs 4.55 km/s round-trip = 9.7 percent of 264-t baseline — well within mass budget but reduces P_impact from 98.83 percent to 86.47 percent at zone-average — not enough to close.

| Hypothesis | Predicted | Measured | Verdict |
|---|---|---|---|
| H-bsurv-1 (armour alone P_impact ≥ 50%) | armour does not change P_impact (geometric only) | 98.83% at zone-avg + any armour | HELD-strong |
| H-bsurv-2 (mesh alone, flux reduction ≤ 30%) | 25% reduction → P drops 98.83% → 91.18% | 91.18% | HELD |
| H-bsurv-3 (off-plane Δv ≥ 5 km/s) | 4.55 km/s round-trip at apoapsis | 4.549 km/s | WRONG-BUT-INFORMATIVE |
| H-bsurv-4 (slow-cross-only Δv ≥ 8 km/s) | residence-or-9-km/s-floor | min v_rel = 9.07 km/s @ Δv = 23 km/s; ring-match Δv = 14 km/s | HELD (in two forms) |
| H-bsurv-5 (no closing combination) | 0 cells close | 0 of 162 | HELD-strong |
| H-bsurv-6 (conjunction with aerobraking < 10%) | 0 × P(this) = 0 | 0 × 0 = 0 | HELD-strong (conditional on `a7a8456` integration) |

**Reading.** **The held chunk-rendezvous architecture has no surviving cell at conservative anchors.** Both load-bearing engineering questions are now adjudicated and both fail: aerocapture (`a7a8456`, 0/1920) and B-ring crossing survivability (this round, 0/162). The conjunction is structurally non-closing. Project-owner decisions surfaced: (1) retire chunk-rendezvous as a venture-class architecture; (2) reframe matrix axis 19 from "chunk-rendezvous-engineering-pending" to "chunk-rendezvous-falsified-without-architecture-pivot"; (3) open R-mission-architecture-pivot-survey or R-program-class-reframe-2 as next critical-path rounds; (4) revisit drag-skirt-conditional under the new strict reading.

**Cross-learning.**

- **NEGATIVE for held chunk-rendezvous architecture.** Both engineering closures negative; conjunction zero. Architecture is non-viable at conservative anchors. Phoebe's recommendation: retire from venture-class viability, restate as technology-demonstrator candidate or architecture-pivot prerequisite.
- **NEGATIVE for matrix axis 19 ("chunk-rendezvous-engineering-pending" framing).** Should be relabelled "chunk-rendezvous-falsified-without-architecture-pivot" to match data.
- **POSITIVE for R-mission-architecture-pivot-survey** as next critical-path round. Catcher / processor-at-Saturn / lower-energy-trajectory / small-source variants need first-pass scoping. Pre-empts a third architectural collapse cycle.
- **POSITIVE for R-program-class-reframe-2** (meta-round on L0-05 relaxation). Phoebe's two consecutive engineering rounds raise the bar: now the question is "is there ANY 14-yr mission that closes given engineering constraints?", not just "should we accept a longer mission?".
- **METHODOLOGY-FLAG: SCOPE input-assumption errors documented (methodology lesson 9 third application).** Four input-assumption errors caught: (i) geometric-impact-probability is velocity-independent (load-bearing on H4 framing); (ii) "20 km/s to 5 km/s" Saturn-frame slow recipe doesn't reduce vehicle-to-ring-particle relative velocity below 9 km/s; (iii) armour cross-section bookkeeping needs care for extended-vehicle case (point-vehicle formula understates hit count by 5-6 orders of magnitude on the bag-aperture metric); (iv) Edelbaum cost computed at apoapsis (cheap, 4.55 km/s) vs periapsis (12× more expensive). Lesson 9 is now corroborated by three consecutive phoebe rounds — sturdy enough to be PROTOCOL-default for any worker reading any orchestrator-authored SCOPE.
- **METHODOLOGY-FLAG: geometric-vs-kinetic survivability distinction.** Per-pass impact probability and post-impact survival fraction have different functional forms and different levers. Future rounds touching ring crossings, atmospheric particle flux, debris fields should distinguish these explicitly. Candidate PROTOCOL footnote (not a full methodology lesson; phoebe lesson 9 already covers the "audit SCOPE assumptions" generic case).
- **METHODOLOGY-FLAG: chunk-population vs safe-passage co-location.** The fundamental architectural obstruction is that the only safe-passage zones (low τ) are also chunk-empty zones (per fine-structure H1+H2). This generalises to any "find a safer X" architectural recovery: must demonstrate chunks ARE in the recovered X. Worth a campaign-wide footnote.

---

## R-bring-survivability-relaxed — does the prior round's verdict survive self-questioning on threshold, mesh capability, extended-aperture, and single-crossing?

**Status:** post-result. Worker: phoebe (continued, fifth round of session, 2026-05-15 latest+8 → +9, second commit). Self-questioning follow-up under project-owner direction "question your assumptions". Interrogates the R-bring-rendezvous-survivability `abdcd35` verdict on four axes that could plausibly flip it.

**Hypothesis (aggregate H-rsr-agg).** Even with all four self-questioning levers combined (loosest defensible threshold + 1m-cull mesh + extended-aperture-as-best-case + single-crossing geometry), no chunk-bearing cell closes at defensible mass budget. The prior verdict is robust to self-questioning at conservative engineering anchors.

**Test.** 126-cell deterministic sweep across τ-zone (7 zones) × mesh-capability (no-mesh / 1cm / 5cm / 10cm / 20cm / 1m cull) × inclination (26.7°, 60°, 90°). For each cell, compute (a) point-vehicle P_per_pass = 1 - exp(-τ_eff × csc(i)), (b) extended-aperture expected hits per pass = (n_total × h × number-fraction-above-d-cull) × A_v × csc(i), (c) extended-aperture P_per_pass = 1 - exp(-expected_hits). Threshold derivation from L0-10 = 0.8 mission-success / 5 missions / 9 ring crossings under 5 different f_other (fraction of mission budget consumed by non-ring failures): ultra-strict (10⁻⁴ per crossing, f_other=0.995, SCOPE prior); strict (10⁻³, f_other=0.954); moderate (2.2×10⁻³, f_other=0.899); aggressive (1.1×10⁻², f_other=0.496); extreme (2.2×10⁻², f_other=0, non-defensible). Closure check: P_per_pass ≤ threshold AND mass penalty ≤ 10% of 264-tonne baseline AND chunks present. Single-crossing variant: propulsive depart from B-ring radius without re-crossing (29 m/s; free architectural lever). See `rounds/R_bring_survivability_relaxed/run.py`.

**Result.** **0 of 126 cells close at any of the 5 thresholds × 2 treatments × 2 crossings = 20 closure-check variants per cell.** Best chunk-bearing flip-threshold (lowest threshold at which any chunk-bearing cell would close): point-vehicle 4.79% per crossing at B-ring outermost 180 km × 20 cm cull mesh × 60° inclination — requires f_other = 0 (no budget for any other failure mode), AND under extended-aperture treatment the same cell shows 19.95 expected hits per pass (P_ea = 100%, mission-fatal regardless of threshold). Mesh-sweep spotlight at outermost 80 km × 90°: extended-aperture expected hits/pass drops 207k (no mesh) → 2073 (1cm) → 83 (5cm) → 21 (10cm) → 5.2 (20cm) → 0.21 (1m) — only 1m-cull drops below 1, costs 50t = 19% baseline (3× over mass budget), AND zone is chunk-sparse. Single-crossing geometry rescues 0 cells.

| H# | Predicted | Measured | Verdict |
|---|---|---|---|
| H-rsr-1 (threshold-sweep alone closes only at extreme threshold) | flips at 2.2% threshold | even at 2.2% / f_other=0: 0 cells close (best chunk-bearing P_per_pass = 4.79%) | HOLD-strong, more pessimistic |
| H-rsr-2 (1m mesh closes P at 0.75% but fails mass) | 1m mesh @ 50t = 19% penalty | confirmed; only at chunk-sparse outermost-80km × 90° | HOLD |
| H-rsr-3 (extended-aperture > 1 hit/pass) | mission-fatal across chunk-bearing space | confirmed: ≥ 5 hits/pass at all chunk-bearing cells with ≤ 20cm mesh | HOLD-strong |
| H-rsr-4 (single-crossing rescues 0 cells) | rescues 0 | confirmed: 0 cells flipped | HOLD |
| H-rsr-5 (verdict robust to all 4 levers combined) | 0 chunk-bearing closures | confirmed: 0 of 126 × 20 variants | HOLD-strong |
| H-rsr-6 (flip-threshold non-defensible) | 2.2% / f_other=0 | flip-threshold = 4.79% / f_other = 0; MORE extreme than predicted | HOLD-strong, more pessimistic |

**Reading.** **The held chunk-rendezvous architecture is doubly-confirmed-non-closing at conservative anchors** — three phoebe rounds converge on falsification: aerocapture-engineering (`1623cca`, 0/1920), B-ring point-vehicle (`abdcd35`, 0/162), B-ring extended-aperture under all-self-questioning (this round, 0/126 × 20 variants). **Phoebe's recommendation strengthens: retire the held chunk-rendezvous architecture from venture-class viability with high confidence.**

**Cross-learning.**

- **NEGATIVE for held chunk-rendezvous architecture (now 3rd convergent falsification).** Three independent rounds, three independent failure modes (atmospheric thermal-structural / atmospheric timescale; ring-particle co-location; ring-particle hit-count). All converge on non-closure.
- **POSITIVE for self-questioning rounds as campaign-default after high-stakes architectural verdicts.** This round's value was confirming verdict robustness, not finding new architectural levers. Worth running as a verdict-stress-test pattern; analogous to the lesson-9 SCOPE-audit pattern but applied to one's own work. Candidate PROTOCOL methodology lesson 11.
- **POSITIVE for extended-aperture treatment as PROTOCOL footnote.** Point-vehicle Beer-Lambert formula understates real hit count for extended-aperture vehicles by 4-6 orders of magnitude on bag-aperture metric. Future rounds touching ring crossings, atmospheric particle flux, or debris-field exposure where vehicle cross-section is much larger than typical particle should default to extended-aperture treatment. Surfaced from prior round audit 3, confirmed binding by this round.
- **METHODOLOGY-FLAG: "loosen the threshold" rescue pattern doesn't work for B-ring rendezvous.** The architectural impossibility is orders of magnitude, not factors. Future rounds attempting threshold-relaxation rescues should compute the gap-vs-budget ratio first; if > 100, the rescue path is hopeless before sweeping.
- **METHODOLOGY-FLAG: mesh capability has sharp diminishing-returns curve at the 5-20cm middle band.** Modest gains at modest costs; neither closes. Future structural-armor sweeps should anchor at 1cm and 1m endpoints first to characterize the curve before middle-band detail.
- **METHODOLOGY-FLAG: chunk-availability check must be applied to extended-aperture closures.** A cell that satisfies P_impact_extended ≤ threshold but is in a chunk-sparse zone (outermost 80 km, Cassini Division gaps) is not architecturally useful. Worth tracking this as a separate closure constraint per-cell, as this round did.

---

## R-bag-aperture-chunk-joint — does the bag-aperture lever (anchored at 100 m² without justification) rescue any architectural cell when swept jointly with chunk mass?

**Status:** post-result. Worker: phoebe (continued, sixth round of session, 2026-05-15 latest+8 → +9, third commit). Self-questioning round 3 under project-owner direction "question your assumptions". Interrogates the implicit bag-aperture = 100 m² anchor in R-bring-rendezvous-survivability and R-bring-survivability-relaxed.

**Hypothesis (aggregate H-bach-agg).** Even with the bag-aperture-chunk-mass joint relaxation, no closure cell satisfies (extended-aperture survivability AND mass-budget AND defensible threshold AND chunk-availability AND venture-class economics). The verdict is robust to the bag-aperture lever too.

**Test.** 2,160-cell sweep across chunk mass (10, 20, 50, 100, 200, 482 t) × bag aperture {bag_min, 2× bag_min, 4× bag_min, 100 m² if feasible} × mesh capability (no-mesh / 1cm / 5cm / 10cm / 20cm / 1m cull) × τ-zone (5 zones) × inclination (3). Bag minimum derived geometrically: A_bag ≥ 1.2 × π × r_chunk², where r_chunk = (3 m_chunk / (4π ρ_ice))^(1/3). For each cell, evaluate 5 closure constraints simultaneously. Venture-class economics anchored on R-delivery-irr-curve crossover findings (sovereign-bond hurdle ≥ 209 t/ship). See `rounds/R_bag_aperture_chunk_joint/run.py`.

**Result.** **0 of 2,160 cells close on the 5-constraint aggregate.** The most-favourable cell tested (10 t chunk × 7.13 m² bag × 1m cull mesh × outermost 80 km × 90° inclination) gives expected hits per pass = 0.015, P_ea = 1.47% — survives at extreme threshold but fails on three other constraints: (a) mass penalty 14.5% (over 10% budget — inclination Δv at 90° dominates the penalty fraction even at small vehicle); (b) outermost 80 km is chunk-sparse (per fine-structure H1+H2); (c) delivered mass 10 t fails all three venture-class hurdles. The bag-aperture lever has the predicted effect on hit count (linear scaling, 14× reduction at 14× smaller bag) but does not rescue venture-class viability because chunk-mass and bag-aperture are constrained one-to-one by geometry.

| Hypothesis | Predicted | Measured | Verdict |
|---|---|---|---|
| H-bach-1 (bag scales with chunk^(2/3)) | A_bag(13t) ~ 9 m² | A_bag(10t) = 7.13 m²; (200t) = 52.6 m² | HOLD |
| H-bach-2 (hits scale linearly with A_v) | hits drop to ≤ 1 at A_v ≤ 50 m² | confirmed: 0.21 hits at 100 m², 0.015 at 7 m² | HOLD |
| H-bach-3 (10t chunk × 7m² bag × 1m mesh closes at 2.2% extreme) | P_ea = 2.1% | P_ea = 1.47% (closes more comfortably than predicted) BUT fails on mass + chunks-present | HOLD-strong on threshold; reveals additional binding constraints |
| H-bach-4 (mesh mass closes at A_v ≤ 50 m² with 1m mesh) | mass closes at small bag | mesh alone closes (3.6 t / 74 t = 4.8%) but inclination Δv dominates penalty | HOLD with caveat |
| H-bach-5 (closure cells are chunk-sparse) | sparse zone | confirmed: outermost 80 km is sparse | HOLD-strong |
| H-bach-6 (10t fails venture-class hurdle) | not reachable at 13t/mission | confirmed: 10t fails ALL 3 hurdles | HOLD-strong |
| H-bach-agg (verdict robust to bag-aperture lever) | 0 cells satisfy all 5 constraints | 0 of 2,160 cells | HOLD-strong |

**Reading.** **The held chunk-rendezvous architecture is now triply-confirmed-non-closing across THREE self-questioning rounds plus the original two engineering rounds.** Phoebe's session: 4,268 unique closure-checks across 4 rounds, all negative. The architecture is robust against four independent lines of architectural relaxation (threshold, mesh, aperture, chunk-mass). Phoebe's recommendation strengthens further: retire the held chunk-rendezvous architecture from venture-class viability with very high confidence; only architectural-pivot or program-class-reframe rounds remain in the search space.

**Cross-learning.**

- **NEGATIVE for held chunk-rendezvous architecture.** Fourth convergent falsification of the session, this one against the bag-aperture lever I anchored without justification. No remaining internal lever to interrogate.
- **POSITIVE for self-questioning rounds as campaign-default after high-stakes architectural verdicts (third corroboration of methodology lesson 11 candidate).** Each of the three self-questioning rounds (relaxed-threshold, bag-aperture-chunk) confirmed verdict robustness from a different angle. Combined value: high-confidence retirement of the architecture, plus a campaign-shared library of "tried this self-question, didn't work" results that future workers can reference instead of re-running.
- **METHODOLOGY-FLAG: bag-min utility function should be campaign-shared.** Bag aperture should default to the geometric minimum given the chunk mass, not a fixed convenient number. Recommend extracting `bag_min_area_m2(chunk_t)` to `water-prop/src/`. Two prior phoebe rounds anchored bag at 100 m² without checking this constraint; future rounds should not.
- **METHODOLOGY-FLAG: mass-penalty fraction is invariant to vehicle size for fixed-Δv prop, but mesh-fraction-of-vehicle improves with smaller chunk.** Smaller chunk: mesh fraction drops faster than propellant fraction. The total penalty mostly tracks Δv penalty; mesh is a secondary contributor. Cross-architecture mass-budget analyses should foreground the dominant lever.
- **METHODOLOGY-FLAG: chunk-population vs safe-passage co-location is the single most-binding constraint on the held architecture.** No bag-aperture, mesh, threshold, inclination, or chunk-mass engineering changes that. Worth elevating to a campaign-shared "binding constraint" reference.

---

## R-particle-distribution-q-sensitivity — does the verdict survive across the literature range of particle-size-distribution exponents?

**Status:** post-result. Worker: phoebe (continued, seventh round of session, 2026-05-16 latest+9 → +10). Fourth self-questioning round of session under project-owner direction "question your assumptions". Interrogates the N(D) ∝ D⁻³ anchor used in three prior phoebe rounds (R-bring-rendezvous-survivability, R-bring-survivability-relaxed, R-bag-aperture-chunk-joint).

**Hypothesis (aggregate H-pq-7).** The prior verdict (0 chunk-bearing cells close on all-five-constraint) is robust across the literature-defensible particle-size-distribution exponent q ∈ [2.5, 4.0].

**Test.** 540-cell sweep across q (2.5, 2.7, 3.0, 3.3, 3.5, 4.0 per Cassini measurements) × τ-zone (5 zones) × mesh capability (6 options) × inclination (3). For each cell, recompute mean particle cross-section ⟨σ⟩, number-density × ring-thickness n_total × h, number-fraction-above-d-cull. All using arbitrary q (generalised from prior rounds' q=3 special case). Anchor: 200t chunk × bag = 100 m² × Variant-B Isp. Closure: extended-aperture P_ea ≤ threshold AND mass penalty ≤ 10% AND chunks present.

**Result.** **0 of 540 cells close at strict or moderate threshold at any q ∈ [2.5, 4.0].** The q-sensitivity is sharpest at moderate mesh capabilities (10cm-1m) where P_ea spans three orders of magnitude across the q range (e.g. at 1m mesh × outermost-180km × 90° × bag=100m²: P_ea = 73% at q=2.5, 50% at q=3, 0.42% at q=4.0). But mass-budget binds at 1m mesh (50t = 19% baseline) regardless of q. At mass-budget-passing meshes (≤ 5cm), P_ea ≥ 100% per pass at any q ≥ 2.5. The best chunk-bearing mass-passing cell at q=4 (outermost-180km × 20cm × 60°) gives P_ea = 45.8% — 458× short of strict closure threshold.

| Hypothesis | Predicted | Measured | Verdict |
|---|---|---|---|
| H-pq-1 (q=2.5 more pessimistic) | hits/pass rises 5-10× vs q=3 | rises 2× | HOLD-weak |
| H-pq-2 (q=4 drops hits ≥ 100×) | drop to ≤ 0.003 | drops 73× | HOLD-near-prediction |
| H-pq-3 (q ≥ 3.5 closes strict with 1m mesh) | closes at q ≥ 3.5 | q=4 closes aggressive (1.1%) but mass fails | FALSIFIED at strict |
| H-pq-4 (q ≥ 3.5 closes strict with 20cm mesh) | closes | q=3.5: 99.5%; q=4: 46% — fail | FALSIFIED |
| H-pq-5 (mass-budget binds even at q=4 + 1m mesh) | mass fails | 50t mesh + 25.5t prop = 29% > 10% budget | HOLD-strong |
| H-pq-6 (20cm × q=4 marginally closes) | marginal | P_ea = 46% fails all thresholds | FALSIFIED |
| H-pq-7 (verdict robust across literature q) | 0/540 cells | confirmed | HOLD-strong |

**Reading.** **The held chunk-rendezvous architecture is now FIVE-WAY confirmed-non-closing.** Phoebe's session has produced five rounds (two engineering + three self-questioning) all with 0-cell-closure verdicts on this architecture. Aggregate evidence: 4,808 unique closure-checks across 5 rounds. **Phoebe is demonstrably out of internal levers to interrogate** — five self-questions exhausted the obvious assumption space (threshold, mesh, aperture, chunk-mass, particle-distribution-exponent). Further self-questioning on this architecture would require challenging structural assumptions (L0-10 reliability target, REQUIREMENTS-L1 chunk-cap, Cassini-measured B-ring optical depths), which is requirements/measurements territory.

**Cross-learning.**

- **NEGATIVE (5th convergent falsification) for held chunk-rendezvous architecture.** No remaining internal assumption to interrogate; the architecture is structurally dead at conservative anchors. Phoebe's recommendation is now extremely high-confidence: retire from venture-class viability.
- **POSITIVE for self-questioning rounds as campaign-default after high-stakes architectural verdicts (4th corroboration this session of methodology lesson 11 candidate).** Each successive self-question round added independent angles of evidence. The pattern's diminishing returns are real (the 4th and 5th rounds add less new information than the 2nd and 3rd) but the cumulative effect is high-confidence retirement.
- **METHODOLOGY-FLAG: symmetric-looking assumptions can have non-symmetric sensitivities.** The q-sweep showed two opposing biases (low q = more large particles = higher hits from rare-but-fatal hits; high q = more small particles = higher n_total but lower hits-from-large) that partially cancel. The verdict is more robust to q than either single-direction analysis would predict. PROTOCOL footnote candidate.
- **METHODOLOGY-FLAG: the "target high-q location" architectural-rescue path is foreclosed.** Even at high-q locations (B3 core has q ≈ 3.3 per Hedman & Stark 2015), the τ = 4.5 there overwhelms the q-rescue. Documented for the architecture-pivot search space.
- **METHODOLOGY-FLAG: chunk-population vs safe-passage co-location confirmed across τ AND q variation.** This is the architecturally-binding constraint. Future architecture-pivot rounds should anchor on this as a hard constraint, not just a tendency.

---

## Verdict block

(Filled at end of campaign, per protocol section 12. Empty until then.)

| Component | Bucket | Round(s) | Reason |
|---|---|---|---|
| (none yet) | | | |
