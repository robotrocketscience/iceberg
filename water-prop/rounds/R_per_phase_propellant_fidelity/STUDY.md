# R-per-phase-propellant-fidelity — STUDY (pre-registration)

**Worker:** worktree-172651, 2026-07-26 latest+29d (owner: "do them all … question
your assumptions"). This is the long-gated per-phase-Tsiolkovsky successor to
R-vehicle-mass-fidelity-refinement H1, executed framework-natively: because all
chemical burns draw from one launch-loaded tank, "per-phase accounting" is
equivalent to **the minimal propellant fraction f at which a given path family
remains feasible** — so the round scans f per path family instead of rebuilding
the mass model.

## The assumption under interrogation (my own)

Latest+29c states, twice, that the corridor's ×16 launch requirement is "largely
an artifact of the frozen 0.80 fraction." The corridor's own ledger walk
contradicts this from the record: the closing path consumed 1,119 of its 1,198 t
of chemical propellant (kick residual + periapsis capture + arrival trim) —
utilization 93%, implying f_optimal ≈ 0.78, not 0.36. **Pre-registered
prediction: the frozen-f-artifact claim is FALSE for the chemical-kick corridor
family** (launch-requirement cut < 1.5×) **and true only for all-electric
outbound families** (which the resolved 22.5 km/s departure anchor has already
demoted below the 30-t floor).

## Hypotheses

| # | Hypothesis | Gate | Prediction |
|---|---|---|---|
| H-P1 | Optimal-f cuts the corridor's minimum launcher multiplier from ×16 to ≤×8 at the 32.6-t cell (150 kWe / 500 t) | min multiplier > 8 at every f falsifies | **FALSIFIED expected** — cut < 1.5× (my latest+29c claim dies here) |
| H-P2 | f_optimal for the corridor family lies in 0.70–0.85 | outside falsifies | chemical schedule dominates |
| H-P3 | For the retired electric family (chunk-fed at 22.5 km/s), optimal-f DOES cut the multiplier ≥2× vs f = 0.80 | cut < 2× falsifies | the artifact claim survives only here |
| H-P4 | Optimal-f raises corridor delivered mass ≤ 10% (propellant savings mostly go to launch margin, not payload) | > 10% falsifies | delivery is set by the departure mass ratio, not launch propellant |

## Method

Grid: f ∈ {0.30…0.85 step 0.05} × launcher multiplier bisection, saturn_water_v2
at the corridor posture (harpoon, no-TPS, 33 W/kg, stage Isp 900 s, non-aero
paths only), cells (150 kWe / 500 t) and (200 kWe / 1,000 t); same for v1
arm-B-resolved (chunk_fed_dv 22.5) electric family. Deliverable: min multiplier
(f) tables + f_optimal per family. Lesson-25: ledger walk at the new optimum if
it differs from the recorded corridor cell.
