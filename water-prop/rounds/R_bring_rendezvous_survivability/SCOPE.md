# R-bring-rendezvous-survivability — does engineered survivability through B-ring crossings close the 99-percent-per-pass impact-prob gap?

**Status:** scope, pre-study. Authored by Saturn (orchestrator), 2026-05-15 latest+6, immediately after project-owner decision on decision point #6 (chunk-rendezvous architecture held).

**Context.** Titan-2 R-saturn-soi-periapsis-depth H5 (`1b1b889`) computed B-ring rendezvous crossing impact probability under zone-averaged optical-depth τ ≈ 2 at the chunk-rendezvous orbit geometry (~26.7° inclination, periapsis ~100,000 km radius). Result: **98.85 percent per pass; 99.99 percent mission-failure for the 9 ring-plane crossings a chunk capture requires** (1 SOI in, 1 SOI out, 1 B-ring inbound rendezvous, 1 B-ring outbound, plus 5 other low-τ-zone crossings). The titan round assumed a *passive-target* spacecraft (no armouring, no particle-cull, no off-plane approach). The titan round surfaced three operational responses:

1. **Target B-ring sub-features (τ ≤ 0.01 zones).** **Foreclosed** by titan-2 R-bring-fine-structure-rendezvous (`201e2c2`) H1-H3: B-ring proper has no τ ≤ 0.01 sub-feature; the lowest is τ = 0.03 at the outermost 80 km; Huygens + Laplace gaps are safe-passage but contain no large particles (chunk-population radii and safe-passage radii are NOT co-located).
2. **Match B-ring orbital speed (residence-class ram-scoop).** **Foreclosed** by project-owner decision 2026-05-15 latest+6 (matrix decision point #6): adds 14.7 km/s of Saturn-side Δv, contradicting ICEBERG's foundational delta-velocity-minimization premise. Retired as program direction.
3. **Engineered survivability through crossings.** **NOT yet investigated.** This SCOPE.

The held chunk-rendezvous architecture requires this question to close. Aerocapture closure (R-hybrid-aerocapture-aerobraking, hyperion SCOPE) is necessary but not sufficient — even if aerocapture closes, a 99-percent-per-pass B-ring impact prob makes any chunk capture mission-fatal. **Both must close for the held architecture to have a surviving cell at conservative anchors.**

This is the **second of two load-bearing open engineering questions** on the held architecture per `ARCHITECTURE-DECISION-MATRIX.md` latest+6.

---

## What the titan SOI round actually said about the rendezvous (PRIMARY-text quotes)

Per methodology lesson 7 (compute under most pessimistic credible anchor first), anchor on titan's primary results, not on downstream summaries.

`water-prop/rounds/R_saturn_soi_periapsis_depth/STUDY.md:140` (B-ring zonal optical depth):

> | B-ring | 92,000–117,580 km | τ = 2.0 | P_impact(0° incl) = 100% | P_impact(26.7° incl) = 99% | mission-fatal |

Lines 186–189 (mission-integrated risk):

> | B-ring inbound rendezvous | 1 crossing | 100,000 km | B-ring zone | per-crossing P_impact = 0.988 | contribution = 98.85% |
> | B-ring outbound (post-capture) | 1 crossing | 100,000 km | B-ring zone | per-crossing P_impact = 0.988 | contribution = 98.85% |
> | TOTAL mission impact-failure probability | 9 crossings | — | — | — | **99.99%** |

Lines 195–197 (architectural framing the titan worker explicitly named as out-of-scope):

> H5 holds quantitatively: the SOI ring crossings contribute 0.002% of mission risk. But the headline result is uglier: the naive zone-averaged optical-depth model predicts ~100% mission failure from B-ring rendezvous crossings alone. **The B-ring chunk-rendezvous geometry itself is a hostile-environment problem, not just a velocity-match problem.**

The titan round adjudicated the velocity-match problem (R-HE-graze-feasibility falsification) and the geometric impact problem (this finding). It DID NOT adjudicate the engineering-mitigation-of-impact-prob problem. That's this round.

Line 219 (titan's explicit follow-on-round flag):

> **Open: B-ring rendezvous architecture.** Cannot survive naive zone-averaged ring optical depth. Must target sub-features or run a residence-class architecture inside ring. **New round.**

This SCOPE responds to that flag, with the constraint that the two named responses are now both foreclosed.

---

## Question this round answers

For a chunk-rendezvous mission at periapsis 100,000 km (B-ring outer), arrival inclination 26.7° (Earth-Hohmann to Saturn equator), 200-t chunk × 64-t tug × bag — under what engineering combination, if any, does per-pass B-ring impact probability drop from 98.85 percent to ≤ 0.01 percent (the L0-10 0.8 rolling-5-mission reliability target's per-crossing allocation)?

**Levers to sweep:**

1. **Bag-armouring.** Particle-armour outer layer (multi-layer Whipple-shield-class? Vectran + aerogel multilayer? Self-healing elastomer?) as a forward-facing shield during the B-ring crossing window. Mass penalty scales with armour thickness × bag aperture area; cost penalty scales similarly. Does it reduce the impact-prob bound (which is geometric, P ≈ τ × csc(i) at this inclination) or does it just convert impacts from "vehicle-destroying" to "vehicle-degrading"? The latter is what closes the round; the former does not.
2. **Particle-cull mesh.** Forward-mounted aperture-sized mesh that intercepts particles above some size threshold before they hit the bag or tug. Already in the conops as an HE-graze cull mechanism; titan-2's H1 in R-bring-fine-structure-rendezvous confirmed B-ring large-particle content is ~75 percent unshieldable (particles > 1 cm). Mesh probably retires particles < 1 cm; does that change the impact-prob picture given that most flux is from > 1 cm particles?
3. **Off-plane approach geometry.** Approach the B-ring outer at the maximum inclination achievable post-SOI. Higher inclination reduces in-plane path length, reduces per-pass impact prob as csc(i) → 1 as i → 90°. Constraint: argument-of-periapsis must lock at trans-Saturn-injection to place ring-plane crossings outside main rings (axis 18 / titan H4); off-plane approach trades against the trans-Saturn-injection burn cost. What's the propulsive penalty for crossing-at-90°-inclination, and does it stay inside the matrix's outbound mass budget?
4. **Slow-cross-only.** Brief retrograde burn before the B-ring rendezvous to reduce ring-particle relative velocity from orbital (~20 km/s) to slow (e.g. ~3 km/s) for the rendezvous-and-capture window only, then accelerate out. Distinct from the residence-class reframe (which circularises into B-ring orbit and stays); this slows for minutes-to-hours and re-accelerates. Propellant penalty is the round-trip of the velocity change. Cheaper than residence (~10 m/s ram-scoop) but not free.

Each lever has a mass/cost penalty that must fit inside the matrix's Variant-B / chunk-rendezvous mass budget. The round must price each lever and find the combination (if any) that closes the impact-prob target without collapsing the mass-ratio.

---

## Pre-registered hypotheses (numeric ranges + falsification bands)

| # | Hypothesis | Predicted range | Falsification band |
|---|---|---|---|
| H1 | Bag-armouring alone reduces per-pass impact prob from 98.85% to a value > 10%. The flux is dominated by > 1 cm particles (titan-2 R-bring-fine-structure-rendezvous H3: ~75% of τ is from > 1 cm) which are unshieldable at any reasonable mass budget; armour does not change the impact-prob bound, only the post-impact survival fraction. | bag-armour-only per-pass impact-prob ≥ 50% | H1 falsified if armour alone drops per-pass impact-prob to ≤ 5% |
| H2 | Particle-cull mesh sized to retire particles below ~1 cm reduces flux by a small fraction (titan-2 R-bring-fine-structure-rendezvous H3 says ~75% of τ is from > 1 cm; mesh retires the remaining ~25% from < 1 cm but not the bulk). | mesh-only flux reduction ≤ 30% (per-pass impact-prob ≥ 65%) | H2 falsified if cull-mesh reduces per-pass impact-prob to ≤ 10% |
| H3 | Off-plane approach geometry at 90° inclination relative to ring-plane is propulsively prohibitive. To rotate the orbit normal by ~63° (from 26.7° Hohmann arrival inclination to 90° relative to ring plane) costs Δv ≥ 5 km/s at SOI radius. | inclination-change propulsive cost ≥ 5 km/s | H3 falsified if 90°-relative-inclination achievable at Δv ≤ 1.5 km/s |
| H4 | Slow-cross-only approach (brief retrograde burn before rendezvous window, re-accelerate after) costs Δv on the order of 8-12 km/s round-trip (slow from 20 km/s to 5 km/s and re-accelerate). | slow-cross-only Δv ≥ 8 km/s | H4 falsified if slow-cross-only Δv ≤ 3 km/s round-trip |
| H5 | Combined engineered survivability (bag-armour + cull-mesh + reduced inclination + slow-cross-only) cannot simultaneously satisfy per-pass impact-prob ≤ 0.01% AND mass-penalty ≤ 10 percent of Variant-B mass budget. There is no closing combination at conservative anchors. | no closing combination exists | H5 falsified if any combination of the four levers closes both constraints simultaneously |
| H6 | Reading-level conclusion (load-bearing): the held chunk-rendezvous architecture is doubly-load-bearing on two engineering closures (this round + R-hybrid-aerocapture-aerobraking), and the conjunction probability of both closing is < 10% under R-power-base-rate-style program-risk priors. If H5 holds, the program needs a project-owner decision: accept the doubly-load-bearing engineering bet, or restate as technology-demonstrator (rhea-bake-off path 2). | both rounds closing: < 10% under base-rate priors | H6 falsified if either (a) H5 falsified (this round closes), OR (b) prior-posterior analysis gives > 30% for both closing |

---

## Method sketch (worker drafts the actual code in `run.py`)

1. **Set the impact-prob target.** L0-10 rolling-5-mission reliability is 0.8 per `REQUIREMENTS.md` v0.6. Allocating that across the 9 mission ring-plane crossings (per titan SOI Body 3 crossing inventory) plus all other failure modes gives a per-crossing impact-prob budget of order 10⁻⁴ to 10⁻³. Use 10⁻⁴ (0.01 percent) as the conservative target.

2. **Compute baseline per-pass impact-prob** at the titan-anchored geometry (periapsis 100,000 km, 26.7° inclination, B-ring τ = 2). Should reproduce titan's 98.85% within rounding.

3. **Sweep H1-H4 individually**, then combined:
   - **H1 (armour).** Mass-and-cost model for multi-layer Whipple-class armour at the bag aperture area. Mass per m² × bag-aperture-area gives total mass penalty. Per-pass impact-prob bound is set by geometric flux × τ — armour does not reduce flux, only post-impact survival. Compute the survival-fraction-after-impact for armour mass density 10, 50, 200 kg/m².
   - **H2 (cull mesh).** Mass-and-cost model for cull-mesh forward of bag. Reduces flux by (1 - fraction-of-particles-below-cull-size). Use titan-2 R-bring-fine-structure-rendezvous H3: ~75% of τ is from particles > 1 cm; mesh sized to cull ≤ 1 cm reduces flux by ≤ 25%. Compute per-pass impact-prob under flux × 0.25.
   - **H3 (off-plane).** Propulsive cost to rotate the orbital plane via Edelbaum-style continuous-thrust inclination change. Cost scales as 2 × v × sin(Δi / 2). Compute for inclination changes 26.7° → 45°, 60°, 75°, 90°.
   - **H4 (slow-cross).** Propulsive cost to slow vehicle from ~20 km/s (B-ring outer orbital speed at 100,000 km radius) to 5 km/s, then re-accelerate, with each leg as a Hohmann-like impulsive burn. Account for chunk-fed propulsion (mass-ratio improves on the re-acceleration leg because chunk is now aboard). Compute round-trip Δv.

4. **Combined sweep.** For each combination (armour level × cull mesh × inclination × slow-cross-magnitude), compute (a) per-pass impact-prob, (b) total mission impact-prob across 2 B-ring crossings, (c) mass penalty as fraction of Variant-B mass budget, (d) program-NPV under per-mission-cashflow vs program-level NPV (per methodology lesson 8, both checks required). Pre-register a 4D grid: armour ∈ {0, 50, 200} kg/m², cull-mesh ∈ {none, 1cm-cull}, inclination ∈ {26.7°, 60°, 90°}, slow-cross ∈ {none, slow-to-5km/s}.

5. **Reading-level conclusion.** Either: (a) at least one combination closes impact-prob ≤ 0.01% with mass-penalty ≤ 10% of budget (H5 falsified, architecture survives); (b) no combination closes both (H5 held, decision returns to project owner with explicit "doubly-load-bearing on aerobraking AND this; conjunction prob < 10%" framing).

---

## Reading template (5-section round template, worker fills in after run)

- **Hypotheses adjudicated.** Verdict per H1..H6 (held / falsified / held-with-margin / falsified-at-magnitude). Predicted vs measured numeric range for each.
- **Headline.** One-line summary of whether engineered survivability closes the impact-prob target inside the mass budget.
- **Reading.** Reading-level decision the project-owner needs: does the held architecture survive at conservative anchors, or does it need restating?
- **Cross-learning.** What this round teaches about engineered-survivability-in-hostile-particle-environments more generally; relationship to R-chunk-as-heat-shield (different hostile environment, similar engineering-survivability question).
- **Next-round candidates.** Follow-on questions surfaced by the result. If H5 falsified, the closing combination needs full engineering-development-cost estimate. If H5 held, decision-frame returns to project owner.

---

## Worker assignment notes

- **Round priority:** **critical-path**. Held architecture cannot have a surviving cell until this AND R-hybrid-aerocapture-aerobraking both close. Either can be assigned first; running them in parallel is fine (different physics, different worker skills useful).
- **Worker fit:** any moon (Iapetus, Mimas, Dione, fresh name). Touches particle-flux physics + propulsive Δv + mass-budget accounting. R-chunk-as-heat-shield was hyperion-flavoured (atmospheric heat transfer); this is closer to ring-particle-flux physics, which titan-2 has been doing — but titan-2 has nine rounds shipped already and may want a different topic.
- **Inputs the worker needs:** `water-prop/rounds/R_saturn_soi_periapsis_depth/STUDY.md` (anchor on H5 Body 2-3 derivation); `water-prop/rounds/R_bring_fine_structure_rendezvous/STUDY.md` (anchor on H1-H3 verdicts for particle-size distribution); `water-prop/rounds/R_HE_graze_feasibility/STUDY.md` (anchor on velocity-match falsification at 6.6 km/s relative velocity); current matrix Capture architecture (axis 19) decision; methodology lessons 7 (pessimistic anchor first) and 8 (program-level NPV check).
- **Out-of-scope for this round:** any consideration of returning to residence-class ram-scoop architecture (project-owner-retired per axis 19); any "what if τ < 2 at the rendezvous radius" optimism (R-bring-fine-structure-rendezvous H1 confirmed B-ring proper has no τ ≤ 0.01 sub-feature, lowest is τ = 0.03).
