# Sub-procedure 2 — phoebe pivot-survey re-classification at heritage bus

Source: phoebe R-mission-architecture-pivot-survey closure_verdict.md per-candidate kill table.
Method: identify bus-mass-anchored kill criteria (F1 inbound Δv, F3 round-trip) versus bus-mass-independent (F2, F4, F5, F6, F7, F8). A candidate could re-classify under heritage bus ONLY if every kill criterion is bus-anchored AND the kill margin is within ~13% of dry mass (the recovery from 15 t → 5.5 t bus reduction).

## Per-candidate audit (31 candidates)

| ID | Name | All kills | Bus-anchored | Bus-independent | At heritage bus |
|---|---|---|---|---|---|
| A | Held chunk-rendezvous | F1,F2,F6 | F1 | F2,F6 | STILL_DEAD |
| A' | Chunk-rendezvous + drag-skirt | F1,F2,F6,F8 | F1 | F2,F6,F8 | STILL_DEAD |
| A'' | Outer-ring chunk-rendezvous | F1,F6 | F1 | F6 | STILL_DEAD |
| H | Aerocapture-conditional chunk-rendezvous | F2,F6 | — | F2,F6 | STILL_DEAD |
| B | Ram-scoop residence-class | F6 | — | F6 | STILL_DEAD |
| B' | Outer-ring residence-class | F6 | — | F6 | STILL_DEAD |
| P1 | Lunar-orbit catcher | F1,F2,F6 | F1 | F2,F6 | STILL_DEAD |
| P3 | Tether-rendezvous | F1,F2,F6 | F1 | F2,F6 | STILL_DEAD |
| P4 | Push-the-rock | F1,F2,F6 | F1 | F2,F6 | STILL_DEAD |
| S1 | Enceladus plume | F6 | — | F6 | STILL_DEAD |
| S2 | Mimas surface mining | F6 | — | F6 | STILL_DEAD |
| S3 | Iapetus surface mining | F1,F3,F6 | F1,F3 | F6 | STILL_DEAD |
| S4 | Hyperion surface mining | F6 | — | F6 | STILL_DEAD |
| S5 | Tethys surface mining | F6 | — | F6 | STILL_DEAD |
| S6 | Phoebe surface mining | F1,F3,F6 | F1,F3 | F6 | STILL_DEAD |
| S7 | Trojan / Hilda | F1,F3,F6 | F1,F3 | F6 | STILL_DEAD |
| T1 | Slow cruise | F2,F3 | F3 | F2 | STILL_DEAD |
| T2 | Pre-staging at moon | F2,F6 | — | F2,F6 | STILL_DEAD |
| F1d | Return propellant (Arch D) | F5,F6,F8 | — | F5,F6,F8 | STILL_DEAD |
| F2d | Bulk ring material | F6 | — | F6 | STILL_DEAD |
| F3d | Many small chunks | F1,F2,F3,F6,F8 | F1,F3 | F2,F6,F8 | STILL_DEAD |
| F4d | Deliver to L4/L5/GEO | F1,F2,F6,F8 | F1 | F2,F6,F8 | STILL_DEAD |
| C2c | Precursor mission | F2 | — | F2 | STILL_DEAD |
| C3c | Shared launch | F1,F2,F6 | F1 | F2,F6 | STILL_DEAD |
| C4c | Data-resource mode | F2 | — | F2 | STILL_DEAD |
| M2m | One-way ships | F2 | — | F2 | STILL_DEAD |
| M3m | Tug-and-go fleet | F6,F8 | — | F6,F8 | STILL_DEAD |
| L1r | Drop 14-yr cap | F2,F6 | — | F2,F6 | STILL_DEAD |
| L2r | Drop chunk-as-propellant-tank lever | F6 | — | F6 | STILL_DEAD |
| L3r | Drop 100% Earth-delivery | F2 | — | F2 | STILL_DEAD |
| L4r | Drop Earth-orbit target | F2,F6,F8 | — | F2,F6,F8 | STILL_DEAD |

**Total re-classifications at heritage bus: 0 of 31.**

**H3 verdict.** Predicted [0, 1] (SCOPE predicted [2, 7]; my pre-registered anchor was 0). Observed 0. **FALSIFIED-low** — phoebe's kill criteria are essentially all bus-mass-independent. The two bus-anchored criteria (F1, F3) appear as kills only in candidates that also have F2 or F6 as kills, so the bus-mass reduction does not save them. F1 kill margins are 4–6× (continuous-thrust 24.7–40.2 km/s vs impulsive-equivalent 6.42 km/s threshold), far beyond any 13%-of-dry-mass recovery. F3 kill margins are typically cruise-physics-driven (R9_slow_trajectory_tof anchors 24 yr round-trip vs 14 yr cap), also not bus-mass-recoverable.

**Audit-trail caveat.** Per phoebe's own closure_verdict.md §'F6 over-determination problem', the *binarised* F6 reading produces 31/31 DEAD; the *probabilistic* F6 reading produces 7 F6-conditional WORTH-DEEP-DIVE. This round inherits the binarised reading because the SCOPE-question is about bus-mass attribution, not F6-treatment. The probabilistic F6 reading remains the load-bearing programme-level question (iapetus settlement).
