# Demonstrator-retirement analysis (Step 6)

Which demonstrator-mission profile retires which A14 sub-step, and what the joint posterior becomes once a demonstrator confirms a sub-step (lifting it from its anchored estimate to a demonstrator-confirmed ~0.92–0.95).

| Sub-step | Anchored mid (mm/s, redundant) | Earth-orbit demonstrator | Saturn small-chunk mission-1 | 13-yr cruise (first full mission) |
|---|---:|:--|:--|:--|
| 1 rendezvous | 0.93 | partial (proximity ops, but not Saturn light-time) | **RETIRES** (real Saturn target, real autonomy) | — |
| 2 deployment | 0.94 | **RETIRES** (deploy the bag mechanism in orbit) | confirms again | — |
| 3 catch (mm/s) | 0.88 | **RETIRES** (deployable target mass, controlled mm/s closing) | confirms at real chunk | — |
| 4 containment (mm/s) | 0.78 | **RETIRES** (catch + hold a target mass) — the weakest link, cheapest to retire | confirms at real friable ice chunk | — |
| 5 survive (13 yr) | 0.88 | no (duration) | partial (short-duration survive only) | **RETIRES** (only the full cruise retires it) |

## Reading

- **The Earth-orbit demonstrator retires the three load-bearing-and-cheapest sub-steps** (deployment, catch, containment) using deployable target masses at controlled mm/s closing velocity. These are exactly the sub-steps with the most uncertainty (containment 0.78) and the only direct test of the closing-velocity regime the whole joint pivots on. **An Earth-orbit catch-and-contain demonstrator is the single highest-leverage A14 retirement action.**
- **The Saturn small-chunk mission-1 retires rendezvous** (real Saturn light-time autonomy on a real non-cooperative target) and partially confirms short-duration survive.
- **The 13-year cruise survive does not retire until the first full mission returns.** No demonstrator shortcuts it; it ratchets as missions complete. This is the irreducible un-retirable residual — and it is cinch-fatigue-dominated, so the mitigation is design-side (redundant cinches), not demonstrator-side.

## Demonstrator-conditional joint

With Earth-orbit (deployment, catch, containment confirmed at mm/s) + Saturn small-chunk (rendezvous confirmed), and 13-yr survive held un-retired at the redundant-cinch mid value:

    joint = 0.95 (rendezvous) x 0.95 (deployment) x 0.95 (catch) x 0.92 (containment) x 0.88 (survive)
          = 0.694

**0.69 clears both the 25 t floor (0.451) and the 30 t floor (0.542) at the matrix-canonical 200 t chunk.** This is somewhat above the orchestrator thread-walk's ~0.58 estimate — the difference is that this analysis credits the Saturn small-chunk demonstrator with retiring rendezvous to ~0.95; under a more conservative crediting (rendezvous left at 0.93) the demonstrator-conditional joint is ~0.68, still comfortably above threshold. The qualitative conclusion is robust: **once both demonstrators succeed, A14 is no longer the binding constraint.**
