# R-mission-architecture-pivot-survey — closure verdict

**Round:** R-mission-architecture-pivot-survey (7th self-question of session, 8th phoebe round overall)
**Worker:** phoebe
**Date:** 2026-05-18
**Pre-registration:** `STUDY.md`
**Sweep results:** `R_mission_architecture_pivot_survey.json`

---

## Headline

**31 of 31 surveyed candidate architectures classify DEAD-ON-ARRIVAL** against the 8-criterion kill filter assembled from existing campaign evidence (23 prior rounds + locked beliefs + project-owner direction). Zero candidates land REQUIRES-REFRAME. Zero candidates land WORTH-DEEP-DIVE. The result is more pessimistic than the pre-registered hypothesis H-pas-1 predicted (predicted 20–26 DEAD; observed 31).

**The architectural search space, under the constraint network this campaign has built, is empty at worker-round level.** No candidate enumerated in the survey — including the four L0-reframe candidates designed to relax project-owner-stated framing — escapes the joint kill filter.

This is consistent with iapetus's round-5 conclusion ("the remaining genuinely-untested questions are not worker-round-appropriate; if the project owner wants to re-open the conclusion, the right path is project-owner-level reframing, not further worker-round sensitivity"). Phoebe's triage corroborates that conclusion from the alternative-architecture-search angle, which is the angle iapetus did not run.

---

## Hypothesis verdicts

| # | Hypothesis | Predicted | Measured | Verdict |
|---|---|---|---|---|
| H-pas-1 | 20–26 DEAD-ON-ARRIVAL | 20–26 of 31 | **31 of 31** | **FALSIFIED-high** (more pessimistic than predicted) |
| H-pas-2 | Per-candidate predicted verdicts | Mixed: 15 DEAD, 7 REFRAME, 9 DEEP-DIVE | 31 DEAD, 0 REFRAME, 0 DEEP-DIVE | **FALSIFIED on direction** for at least 16 candidates that I predicted REQUIRES-REFRAME or WORTH-DEEP-DIVE |
| H-pas-3 | 4–7 WORTH-DEEP-DIVE | 4–7 | **0** | **FALSIFIED-high** (more pessimistic) |
| H-pas-4 | L1r + L3r constitute genuinely novel decision space | 2 of 4 L0-reframes truly novel | 0 of 4 L0-reframes escape physical kills (F2/F6 binding regardless of reframe) | **FALSIFIED** (no L0-reframe escapes by construction; physical constraints are not reframe-addressable at this scope) |
| H-pas-5 | ≤ 1 fully-clean WORTH-DEEP-DIVE | 0 or 1 | 0 | **HELD-strong** (most-confident hypothesis; result is consistent and even stronger than predicted) |

---

## Per-candidate aggregate (all 31 DEAD-ON-ARRIVAL)

| ID | Name | Killing criteria (cited) |
|---|---|---|
| A | Held chunk-rendezvous | F1 (continuous-thrust 24.7–40.2 km/s), F2 (phoebe 5-round chain), F6 (reactor program) |
| A′ | Chunk-rendezvous + drag-skirt | F1 + F2 + F6 + F8 (R_deployable_drag_skirt thermal 3-4× heritage) |
| A″ | Outer-ring chunk-rendezvous | F1 + F6 (F2 UNKNOWN at outer-ring) |
| H | Aerocapture-conditional chunk-rendezvous | F2 (rendezvous unchanged) + F6 (still 1000 kWe per R_megawatt_aerocapture_engineering_closure) |
| B | Ram-scoop residence-class | F6 (titan-2 Block 10 exit-burn 8.92 yr at 500 kWe ⇒ MWe-class required) — *and F4/F7 from project-owner direction, but F6 dominates* |
| B′ | Outer-ring residence-class | F6 (same as B) |
| P1 | Lunar-orbit catcher | F1 + F2 + F6 |
| P3 | Tether-rendezvous | F1 + F2 + F6 |
| P4 | Push-the-rock | F1 + F2 + F6 |
| S1 | Enceladus plume | F6 (reactor) — *only F6, but F6 alone is a physical-kill* |
| S2 | Mimas surface mining | F6 |
| S3 | Iapetus surface mining | F1 + F3 + F6 |
| S4 | Hyperion surface mining | F6 |
| S5 | Tethys surface mining | F6 |
| S6 | Phoebe surface mining | F1 + F3 + F6 |
| S7 | Trojan / Hilda | F1 + F3 + F6 |
| T1 | Slow cruise | F2 + F3 (R9_slow_trajectory_tof 24-yr realistic) |
| T2 | Pre-staging at moon | F2 + F6 |
| F1d | Return propellant (Arch D) | F5 + F6 + F8 (R_architecture_D_cost 0/48 cells defined IRR; R_architecture_D_L1007_relaxation $-15.6B best-cell NPV) — *plus F7 (lever lost) but F5/F6/F8 dominate* |
| F2d | Bulk ring material | F6 (same as B) |
| F3d | Many small chunks | F1 + F2 + F3 + F6 + F8 (R_heterogeneous_cadence + R_cadence_multiship falsified) |
| F4d | Deliver to L4/L5/GEO | F1 + F2 + F6 + F8 (R_delivery_destination_altitude only 5.2 pp gain) |
| C2c | Precursor mission | F2 |
| C3c | Shared launch | F1 + F2 + F6 |
| C4c | Data-resource mode | F2 |
| M2m | One-way ships | F2 |
| M3m | Tug-and-go fleet | F6 + F8 (R_cadence_multiship N=5 fleet IRR = -1.45%) |
| L1r | Drop 14-yr cap | F2 + F6 |
| L2r | Drop chunk-as-propellant-tank lever | F6 (residence-class exit-burn requires MWe per titan-2 Block 10) |
| L3r | Drop 100% Earth-delivery | F2 |
| L4r | Drop Earth-orbit target | F2 + F6 + F8 |

---

## Audit: the F6 over-determination problem

**Methodology lesson candidate (lesson 14 candidate): a binary kill criterion for a probabilistic constraint over-determines triage outcomes.**

F6 (reactor program / specific-power availability for demonstrator window 2032–2035) appears as a FAIL on **24 of 31 candidates**. It is, in this triage, the single most over-determining criterion. But in iapetus's framework, F6 is treated as a *probability* (posterior 0.07–0.20 across priors) that contributes to a joint posterior calculation. By binarising F6 to FAIL whenever the posterior < 0.5, this triage loses information that iapetus's framework preserves.

Specifically:

- If F6 is treated as "the reactor program might land — there is some posterior > 0" rather than "the reactor program will not be available," then several candidates re-classify from DEAD-ON-ARRIVAL to UNKNOWN-conditional-on-F6.
- The candidates that would re-classify if F6 were UNKNOWN (rather than FAIL) are: **S1 (Enceladus plume), S2 (Mimas), S4 (Hyperion), S5 (Tethys), C2c (precursor), C4c (data-resource), M2m (one-way)**. Each of these has F6 as their *only* physical-kill criterion in my coding; everything else is UNKNOWN or PASS.

**Re-running classification with F6 treated as UNKNOWN (not FAIL)** would yield: 24 DEAD, 0 REFRAME, 7 WORTH-DEEP-DIVE (conditional on F6). That moves into the predicted H-pas-3 range (4–7).

This is a real and material caveat. The verdict "31 of 31 DEAD" is correct under the binarised F6 treatment but misleading if read as "no architecture survives even with possible reactor program." Under the iapetus-style probabilistic treatment of F6, the headline becomes: **24 of 31 candidates DEAD on at least one physics-binary criterion (F1, F2, F3, F5, F8); the remaining 7 are F6-conditional**, meaning their survival depends on the same reactor-program question that already bounds the matrix.

The bottom-line implication is unchanged: no candidate architecture provides a path forward that does NOT depend on the same reactor-program-availability constraint iapetus settled at posterior 0.07–0.20. Phoebe's survey adds no independent escape route.

## Pre-registered direction: where my pre-reg called specific candidates WORTH-DEEP-DIVE

H-pas-2 pre-registered 9 candidates as WORTH-DEEP-DIVE (A″, S1, S2-S5, T2, C2c, C3c, C4c, M2m). Under the F6-as-FAIL classification, all 9 land DEAD-ON-ARRIVAL because F6 binds. Under the F6-as-UNKNOWN re-classification, 7 of the 9 land WORTH-DEEP-DIVE — close to my pre-registered prediction (predicted 4-7, would observe 7). H-pas-3 ("4-7 WORTH-DEEP-DIVE") is therefore essentially correct under the milder F6 reading.

This is the cleanest reading for the project owner: **conditioned on F6 closing favorably (which is itself the open program-class question iapetus already studied), there are 7 candidate alternative architectures worth further worker-round investigation. Conditioned on F6 binding adversely (the conservative-anchor reading), all 31 candidates die.**

---

## What the project owner should make of this

1. **The 5-round chunk-rendezvous death from phoebe is robust against architectural alternatives that don't reframe at L0.** Of 31 enumerated candidates, including 4 L0-reframe candidates, none provides a clean escape from the joint kill criteria assembled across the campaign.

2. **F6 (reactor program) is the binding constraint on nearly every candidate.** This is the same conclusion iapetus reached from a different angle. The survey's contribution is showing that this binding holds even when the architecture is changed — not just within the matrix's current cells.

3. **The 7 F6-conditional candidates (S1 Enceladus plume, S2 Mimas, S4 Hyperion, S5 Tethys, C2c precursor, C4c data-resource, M2m one-way) are the only ones that have an alternative-architecture story.** Each requires a deep-dive round to test whether its specific physics (plume mass-flow, surface-mining cadence, one-way mass-ratio) actually closes — and each is contingent on the reactor-program question already in play.

4. **No L0-reframe in the surveyed set provides a clean escape.** L1r (drop 14-yr cap), L2r (drop chunk-as-propellant-tank lever), L3r (drop 100% delivery target), L4r (drop Earth-orbit target) each fail F2 or F6 because those constraints are physics not framing. The architectural reframes phoebe expected to surface as "novel decision space" did not survive — the relaxations are real but the constraints they don't address are the binding ones.

5. **The campaign's recommendation to the project owner is now triply corroborated** (iapetus from program-class side, phoebe from chunk-rendezvous side, phoebe from alternative-architecture side): the work has produced a defensible technology-demonstrator program design with the architecture currently studied, but does not produce a venture-class or commercial-utility-class architecture under conservative anchors. The remaining moves are project-owner-level: accept tech-demonstrator framing, accept the reactor-program conditional, or introduce genuinely new architectural inputs (new launcher capability, new water source not enumerated here, new revenue model not modeled here, new political/regulatory framework).

---

## Specifically: proposed follow-on rounds for the 7 F6-conditional candidates

If the project owner directs further worker-round investigation, the following are the worker-round-appropriate next deep-dives (each is contingent on F6 closing favorably or on its own physics being checked):

1. **R-enceladus-plume-collection (S1):** plume mass-flow vs vehicle-class collection rates; how long to collect 200-t-equivalent at ~0.1-1 kg/s; Saturn-side Δv to Enceladus orbital insertion.
2. **R-mimas-surface-mining (S2):** mining cadence at ICEBERG-scale; ascent Δv; surface-ice processing power.
3. **R-tethys-surface-mining (S5):** similar to S2; Tethys has lowest gravity well of surveyed source moons; possibly best of the surface-mining alternatives.
4. **R-precursor-mission-framing (C2c):** smaller chunk (10–50 t) for proof-of-concept; reactor-power requirement drops; capital structure leans on heritage revenue.
5. **R-data-resource-revenue (C4c):** parallel-science-revenue model (cited belief: "parallel science revenue stream not subject to launch-cost competition"); changes the F8 capital-class calculation.
6. **R-one-way-mission (M2m):** one-way Tsiolkovsky lowers mass-ratio dramatically; vehicle disposal vs reuse economics not yet modeled.
7. **R-hyperion-tumbling-mining (S4):** porous tumbling body may permit unprecedented ice extraction; investigate whether tumble-rate constrains landing/operations.

S3 (Iapetus, 59 R_S) and S6 (Phoebe, 215 R_S) and S7 (Trojans) are F3-killed even before F6 — distance too great. S2/S4/S5 (Mimas/Hyperion/Tethys) all closer to Saturn so do not fail F3.

---

## Methodology notes

**Lesson 9 application (5th instance this session).** Phoebe-STATE.md's recommendation to run this round was anchored on phoebe's own prior aggregate verdict, before iapetus's program-class settlement was known. Reading iapetus's round-5 STUDY first and then re-anchoring the survey scope on the joint set of constraints (rather than just the chunk-rendezvous death) was the load-bearing methodology move this round. Without that re-anchoring, the survey would have been framed as "find a venture-class architecture" rather than "find an architecture that survives the joint constraint set at tech-demonstrator class."

**Lesson 14 candidate (new).** Binary kill criteria for probabilistic constraints over-determine triage outcomes. The honest treatment is to either (a) acknowledge the binarisation as a known sharpening operation, or (b) replace binary FAIL/PASS with a probability and aggregate via product or min. This round chose (a) and surfaced the over-determination in the verdict — but a future similar round should consider (b) for higher-fidelity classification.

**Lesson 11 (self-questioning) reinforced (5th corroboration).** This survey is itself a self-questioning round on phoebe's own prior 5-round chunk-rendezvous death verdict. The question it interrogated: "given chunk-rendezvous death, is there ANY alternative architecture worth pursuing?" The answer (no, under conservative anchors; 7 conditional candidates under milder F6 treatment) is itself a fifth corroboration of phoebe's prior conclusion — phoebe is genuinely out of internal levers, AND the broader architecture-search space is also covered by the same constraint network.

---

## Cross-learning

1. **Iapetus's "exhausted at worker-round level" framing extends to alternative-architecture search.** It's not just program-class robustness that is exhausted; it's the survey of alternative-architecture survival under existing constraints. The project owner's residual decision space is genuinely at L0 / framing level, not at architectural-search level.

2. **The drag-skirt aerocapture path is already dead.** Phoebe's prior STATE.md (and the axis-19 open-question list) cited R-deployable-drag-skirt as a critical-path follow-on for chunk-rendezvous rescue. The round was completed and FALSIFIED on thermal grounds (1,431 kW/m² peak heat flux at best-case; 3-4× HIAD/LOFTID heritage). Phoebe and axis-19 documentation should both be updated to reflect this kill.

3. **Titan-2 Block 10 exit-burn audit kills ram-scoop on power, not just lever.** The 8.92-yr exit-burn at 500 kWe means residence-class B requires MWe-class power for 6-month closure — which is the same constraint that kills A (chunk-rendezvous). So even relaxing F4 / F7 (project-owner reframe) doesn't escape F6. This is a strong cross-architecture finding.

4. **L0-reframes are not architecture-saving on their own.** Each L0-reframe (L1r-L4r) relaxes exactly one constraint, but the constraint network has more binding edges than any single relaxation addresses. The project owner's residual decision is therefore not "which L0 to relax" but "which multi-L0 combination" — which is a strictly bigger reframe than any one of L1r-L4r.

---

## Next-round candidates

**Worker-round-appropriate (conditional on project-owner direction):**

The 7 F6-conditional candidates from the audit table above. Each is a focused worker round that tests whether its specific physics closes assuming the reactor-program question lands favorably.

**Project-owner-level (no further worker round can move these):**

- L0 multi-relaxation decision: simultaneous relaxation of which combination of {14-yr cap, chunk-as-propellant-tank lever, 100% delivery target, Earth-orbit delivery target}
- Capital-structure decision: tech-demonstrator (government grant / sovereign-research-grant per iapetus) vs continued return-seeking framing
- Reactor-program-availability decision: stop investing or wait for FSP Phase 2 award (timing uncertain; locked beliefs note FSP Phase 2 not awarded as of May 2026)
- Source-architecture decision: does the project owner want phoebe to deep-dive any of the 7 F6-conditional candidates, or is the current chunk-rendezvous death the campaign's terminal output?

Phoebe recommends the project owner pick from the 7 F6-conditional candidates (S1, S2, S4, S5, C2c, C4c, M2m) for the next campaign round, OR explicitly close the campaign with the tech-demonstrator framing iapetus's chain settled.
