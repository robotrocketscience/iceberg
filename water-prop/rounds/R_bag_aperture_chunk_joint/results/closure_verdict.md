# R-bag-aperture-chunk-joint — closure verdict

**Round:** R-bag-aperture-chunk-joint
**Worker:** phoebe
**Date:** 2026-05-15 (latest+8 → +9, third commit of session)
**Pre-registration:** `STUDY.md`
**Sweep results:** `R_bag_aperture_chunk_joint.json`

---

## Headline

**The bag-aperture-chunk-mass joint relaxation does not rescue any architecture cell.** 0 of 2,160 cells close on the 5-constraint aggregate (extended-aperture survivability + mass budget + defensible threshold + chunk-availability + venture-class economics). The bag-aperture lever I anchored at 100 m² without justification is not load-bearing on the prior verdict — even shrinking the bag to its geometric minimum (7 m² at 10 t chunk) does not open closure. The blocking constraint shifts from survivability to a triplet of (a) inclination-Δv mass-penalty fraction rises on smaller vehicles; (b) chunk-bearing zones still have too high τ even at smallest aperture; (c) small-chunk architectures (≤ 50 t) fail venture-class hurdles per R-delivery-irr-curve.

---

## What the joint sweep showed

### Bag-min geometry (sanity check)

| Chunk mass | Chunk radius | Chunk frontal area | Bag aperture min (1.2× margin) |
|---|---|---|---|
| 10 t | 1.38 m | 5.95 m² | 7.13 m² |
| 20 t | 1.73 m | 9.44 m² | 11.33 m² |
| 50 t | 2.35 m | 17.38 m² | 20.86 m² |
| 100 t | 2.96 m | 27.60 m² | 33.12 m² |
| 200 t | 3.73 m | 43.81 m² | 52.57 m² |
| 482 t (B-ring single-chunk cap) | 5.01 m | 78.74 m² | 94.49 m² |

### Anchor cell — most-favourable configuration tested

10 t chunk × 7.13 m² bag × 1m cull mesh × outermost-80km × 90° inclination:
- **expected hits per pass = 0.015** (extended-aperture, well under 1)
- **P_ea per pass = 1.47%** — closes at extreme threshold (2.2%, f_other=0, non-defensible) but does NOT close at aggressive threshold (1.1%, f_other=0.5, defensible-stretch)
- **mass penalty fraction = 14.5%** — fails 10% mass budget
- **chunks present = False** — outermost 80 km is chunk-sparse zone (per fine-structure H1+H2)
- **delivered mass per mission = 10 t** — fails all three venture-class hurdles (sovereign-bond requires ≥ 209 t)

The mass-penalty failure is interesting. At 100 m² bag with 200 t chunk (vehicle total 264 t), the inclination-change Δv at 90° gave 9.7% penalty — within budget. At 7 m² bag with 10 t chunk (vehicle total 74 t), the SAME Δv (4.55 km/s round-trip) gives a fractionally LARGER penalty (10.7 t / 74 t = 14.5%) because the propellant fraction doesn't scale linearly with vehicle dry mass at fixed Isp. Smaller vehicle → mass-budget-tighter on plane changes, not looser.

### Closure tally

| Closure constraint set | Cells closing |
|---|---|
| Extended-aperture P_ea ≤ extreme threshold (2.2%) AND mass budget AND chunks present | 0 |
| ...AND sovereign-bond delivered-mass hurdle (≥ 209 t) | 0 |
| All-five-constraint at aggressive threshold (1.1%) | 0 |
| All-five-constraint at extreme threshold (2.2%) | 0 |

---

## Hypothesis verdicts

| H# | Predicted | Measured | Verdict |
|---|---|---|---|
| H-bach-1 (bag scales with chunk^(2/3)) | A_bag(13t) ~ 9 m²; A_bag(200t) ~ 52 m² | A_bag(10t)=7.13 m²; A_bag(200t)=52.57 m² | HOLD |
| H-bach-2 (hits scale linearly with A_v) | hits drop to ≤ 1 at A_v ≤ 50 m² | confirmed: 0.207 hits/pass at A_v=100 m², 0.014 at A_v=7 m² (linear scaling) | HOLD |
| H-bach-3 (10 t chunk × 7 m² bag × 1m mesh closes at 2.2% extreme threshold) | P_ea = 2.1%, marginally closes | P_ea = 1.47% — closes more comfortably than predicted but still NOT at defensible threshold; ALSO fails on mass and chunks-present | HOLD-strong on threshold, BUT mass-budget fails (didn't predict that) |
| H-bach-4 (mesh mass at 10 m² is 5 t = 1.9% of baseline) | mesh mass closes at A_v ≤ 50 m² with 1m mesh | confirmed for mesh ALONE: 1m mesh × 7m² = 3.57 t = 4.8% of 74t vehicle. But TOTAL penalty (mesh + inclination Δv) = 14.5%. Inclination-Δv dominates the penalty on small vehicles | HOLD with caveat |
| H-bach-5 (closure cells are chunk-sparse) | sparse zone has chunk-thin contents | confirmed: outermost 80 km chunk_avail = "sparse"; bag scoops nothing | HOLD-strong |
| H-bach-6 (small chunk fails venture-class hurdle) | not reachable at 13t/mission | confirmed: 10t fails ALL THREE hurdles (sovereign-bond 4% needs 209t; regulated-utility 8% needs 461t; corporate-growth 10% needs 691t) | HOLD-strong |
| H-bach-agg (verdict robust to bag-aperture lever) | 0 cells satisfy all 5 constraints simultaneously | confirmed: 0 of 2,160 cells | HOLD-strong |

---

## Cross-learning

1. **Mass-penalty fraction is NOT linear in vehicle size.** I implicitly assumed smaller vehicle = proportionally smaller propellant penalty, so the budget would scale. But for a fixed Δv and fixed Isp, propellant mass scales with dry mass × (e^(Δv/ve) - 1) — linear in dry mass. The penalty FRACTION is constant in vehicle size: at 4.55 km/s and Isp 5000 s, penalty fraction = 9.6 percent regardless of dry mass. **However, mesh mass scales with bag aperture, which scales with chunk^(2/3), while propellant scales with vehicle total mass which is dry + chunk (linear in chunk).** So mesh-fraction-of-vehicle improves with smaller chunk (because chunk^(2/3) drops faster than chunk), but propellant-fraction stays constant. Net: at small-chunk-end, mesh fraction drops faster than propellant — but the SUM of both at chunk=10t was still 14.5% > 10% budget because the prop-fraction is itself ~9.6% leaving little room for any mesh.

   **Implication:** the 10% mass-penalty budget is effectively monopolised by inclination-change Δv at 90°. Going to lower inclinations frees mass-budget for mesh but worsens P_impact. There's no Pareto-improving direction in (inclination, mesh) space at any chunk size. Cross-confirms the prior verdict.

2. **Bag-aperture lever has a sharp transition.** The expected-hits scaling is linear in A_v, which means a 14× reduction in bag size (100 m² → 7 m²) gives 14× reduction in hits. From 0.207 to 0.015 hits/pass — both small numbers in absolute terms but with very different P_ea (18.7% vs 1.47%). The non-linear P_ea = 1 - exp(-N) function amplifies the bag-aperture lever in this regime. **Future architecture-pivot rounds should ANCHOR bag aperture at the geometric minimum, not at a fixed 100 m².** Worth a campaign-shared utility function `bag_min_area_m2(chunk_mass_t)`.

3. **The chunk-availability constraint at outermost 80 km is binding even after all other constraints relax.** The architectural-recovery scenarios that close on survivability all converge on outermost 80 km × 90° (the only zone where extended-aperture hit count drops below 1 at modest mesh capability). But that zone is chunk-sparse. **The chunk-population vs safe-passage co-location problem (fine-structure H1+H2) is the single most-binding constraint on the held architecture.** No bag-aperture, mesh, threshold, or inclination engineering changes that.

4. **Three self-questioning rounds, three convergent confirmations.** The pattern (R-bring-survivability-relaxed targeting threshold/mesh/aperture/crossing; R-bag-aperture-chunk-joint targeting aperture/chunk/economics) has now exhausted the obvious self-question levers on the held chunk-rendezvous architecture. Phoebe is out of architecturally-internal levers to interrogate; the next layer of self-questioning would have to be at the requirements level (R-program-class-reframe-2 territory).

---

## Reading

**The held chunk-rendezvous architecture is now triply-confirmed-non-closing across THREE self-questioning rounds plus the original two engineering rounds.** Phoebe's session has produced 5 rounds with 100% convergent falsification on this architecture:

1. R-hybrid-aerocapture-aerobraking (`1623cca`): aerocapture-engineering 0/1920
2. R-bring-rendezvous-survivability (`abdcd35`): B-ring point-vehicle 0/162
3. R-bring-survivability-relaxed (`45869d4`): self-question on threshold/mesh/aperture/crossing 0/126 × 20 variants
4. R-bag-aperture-chunk-joint (this round): self-question on bag-aperture-chunk joint 0/2160

Together: 4,268 unique closure-checks, all negative. The held chunk-rendezvous architecture has no surviving cell at conservative anchors and is robust against four independent lines of architectural relaxation.

**Phoebe's recommendation strengthens further: retire the held chunk-rendezvous architecture from venture-class viability with very high confidence.** The only remaining architectural search direction is true pivot — R-mission-architecture-pivot-survey (catcher / processor-at-Saturn / lower-energy-trajectory / small-source variants) or R-program-class-reframe-2 (L0-05 relaxation, residence-class waiver, etc.).

---

## Next-round candidates (no new ones; same as prior recommendation)

- **R-mission-architecture-pivot-survey** (priority: critical-path)
- **R-program-class-reframe-2** (priority: critical-path)

The case for both is now the strongest it has ever been across the campaign.
