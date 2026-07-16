# R-bring-survivability-relaxed — closure verdict

**Round:** R-bring-survivability-relaxed
**Worker:** phoebe
**Date:** 2026-05-15 (latest+8 → +9, second commit of session)
**Pre-registration:** `STUDY.md`
**Sweep results:** `R_bring_survivability_relaxed.json`

---

## Headline

**The prior R-bring-rendezvous-survivability verdict (0 of 162 cells close) is robust to all four self-questioning levers combined.** Across 126 cells × 5 closure thresholds × 2 impact-treatment frameworks × 2 crossing-counts (= 2520 closure-checks), 0 chunk-bearing cells close under any defensible combination. The most permissive setting — extreme threshold (full L0-10 budget to B-ring, f_other = 0, non-defensible) × extended-aperture treatment × single-crossing — still produces 0 chunk-bearing closures. The lowest flip-threshold for any chunk-bearing cell is 4.8% per crossing, achieved at B-ring outermost 180 km × 20 cm cull mesh × 60° inclination — that flip-threshold requires f_other = 0 (no budget for any other failure mode) AND under extended-aperture treatment the same cell shows 20 expected hits per pass (P_ea = 100%, mission-fatal regardless of threshold).

**The verdict got SHARPER under self-questioning, not softer.** The extended-aperture treatment (audit 3 follow-up) reveals point-vehicle P_impact understates real risk by 4-6 orders of magnitude on the bag-aperture metric.

---

## Hypotheses adjudicated

| H# | Predicted | Measured | Verdict |
|---|---|---|---|
| H-rsr-1 (threshold-sweep alone, point-vehicle, closes at threshold ≥ 2.2% only) | flips only at extreme threshold | even at extreme threshold (2.2%, f_other=0): 0 chunk-bearing cells close (best chunk-bearing P_per_pass = 4.79% at B-ring outermost 180 km × 20cm mesh × 60°) | **HOLD-strong, more pessimistic than predicted** |
| H-rsr-2 (mesh capability sweep, 1m-cull mass 50t exceeds 10% budget) | 1m mesh closes P_impact at 0.75% but fails mass | confirmed: 1m mesh @ 50t = 19% penalty AND P_per_pass(pv)=0.75% only at chunk-sparse outermost 80km × 90° | **HOLD** |
| H-rsr-3 (extended-aperture > 1 hit/pass at all 1m-cull and below) | mission-fatal across the chunk-bearing parameter space | extended-aperture expected hits/pass at outermost 80 km × 90°: 207k (no mesh) → 2073 (1cm) → 83 (5cm) → 21 (10cm) → 5.2 (20cm) → 0.21 (1m); only the 1m-mesh case drops below 1, and it's chunk-sparse and mass-prohibitive | **HOLD-strong** |
| H-rsr-4 (single-crossing rescues no cell that wasn't already at threshold edge) | rescues 0 cells | confirmed: 0 cells flipped from non-closing to closing under single-crossing at any threshold | **HOLD** |
| H-rsr-5 (aggregate: prior verdict robust to all four levers combined) | 0 chunk-bearing cells close under any defensible combination | confirmed: 0 of 126 cells close at all 5 thresholds × 2 treatments × 2 crossings | **HOLD-strong** |
| H-rsr-6 (flip-threshold non-defensible) | 2.2% / f_other=0, non-defensible | best chunk-bearing flip-threshold = 4.79% (more extreme than my prediction); requires f_other = 0 | **HOLD-strong, MORE EXTREME than predicted (4.79% vs predicted 2.2%)** |

---

## Aggregate verdict — H-rsr-agg

**HELD-strong.** The prior R-bring-rendezvous-survivability verdict is robust to self-questioning under conservative engineering anchors. None of the four interrogation axes flip the verdict:

1. **Threshold sensitivity:** even allocating the entire L0-10 mission-failure budget to the two B-ring crossings (4.4% per mission, 2.2% per crossing — non-defensible because it leaves zero budget for other failure modes) does not flip any chunk-bearing cell to closure under either treatment.

2. **Mesh capability:** scaling mesh from 1cm cull to 1m cull reduces τ_unshielded by 75% but at mass cost ~50t (19% of vehicle baseline, exceeding the 10% mass budget). And even the 1m-cull case at outermost 80 km × 90° gives extended-aperture P_per_pass = 18.7% — still 8.5× short of the extreme threshold.

3. **Extended-aperture treatment:** vastly sharpens the verdict. At chunk-bearing zones (B-ring outer 580km, Huygens Ringlet, B-ring outermost 180km), even 20cm-cull mesh leaves expected hits-per-pass ≥ 5. Mission-fatal regardless of threshold or per-impact armor.

4. **Single-crossing geometry:** free architectural lever (cheap propulsive depart at 29 m/s) but doesn't rescue any cell whose double-crossing P was non-closing.

---

## Threshold-sensitivity table (self-audit 1 BOE)

L0-10 = 0.8 mission-success over 5 missions → per-mission failure budget ≤ 4.37 percent. Budget allocated across two B-ring crossings + all other failure modes. f_other = fraction of budget consumed by non-ring failures.

| Threshold label | Per-crossing | f_other (implied) | Defensibility |
|---|---|---|---|
| ultra-strict (SCOPE prior) | 1.0×10⁻⁴ | 0.995 | comfortable: ≥ 70% budget for other failures |
| strict | 1.0×10⁻³ | 0.954 | comfortable |
| moderate | 2.2×10⁻³ | 0.899 | comfortable |
| aggressive (50% budget to B-ring) | 1.1×10⁻² | 0.496 | stretched |
| extreme (full budget to B-ring) | 2.2×10⁻² | 0.000 | **non-defensible** (no budget for other failures) |

---

## Closure stats by threshold × treatment × crossings (126 cells)

| Threshold | point-vehicle 2× | point-vehicle 1× | extended-aperture 2× | extended-aperture 1× |
|---|---|---|---|---|
| ultra-strict (10⁻⁴) | 0 | 0 | 0 | 0 |
| strict (10⁻³) | 0 | 0 | 0 | 0 |
| moderate (2.2×10⁻³) | 0 | 0 | 0 | 0 |
| aggressive (1.1×10⁻²) | 0 | 0 | 0 | 0 |
| extreme (2.2×10⁻²) | 0 | 0 | 0 | 0 |

---

## Spotlight: outermost 80 km × 90° inclination (chunk-sparse), full mesh sweep

| Mesh | mesh mass | total penalty fraction | P_per_pass (point-vehicle) | expected hits/pass (extended-aperture) | P_per_pass (extended-aperture) |
|---|---|---|---|---|---|
| no mesh | 0 t | 9.7% | 2.96% | 207,360 | 100% |
| 1 cm cull | 0.5 t | 9.9% | 2.22% | 2,074 | 100% |
| 5 cm cull | 2.5 t | 10.7% | 1.71% | 83 | 100% |
| 10 cm cull | 5.0 t | 11.6% | 1.49% | 21 | 100% |
| 20 cm cull | 10.0 t | 13.5% | 1.27% | 5.2 | 99.44% |
| 1 m cull | 50.0 t | **28.7%** | 0.75% | **0.21** | **18.7%** |

The 1m-cull mesh is the ONLY configuration that drops extended-aperture P_per_pass below 99 percent — and it requires 50 tonnes of mesh (19 percent of vehicle baseline; total penalty 28.7%, ~3× over 10% budget). And this is at the chunk-SPARSE outermost 80 km zone — there are essentially no large chunks to harvest there (per fine-structure H1 verdict).

---

## What this means for the prior verdict

**Sharper, not softer.** The point-vehicle P_impact = 1 - exp(-τ × csc(i)) framework that titan SOI used (and that I anchored on in the prior round) is appropriate for "1 unit of cross-section". A 100 m² bag aperture sweeps a ring volume that contains ⟨n_total × h⟩ × 100 m² particle-areal-density of particle-cross-sections — millions of intercept events at zone-average τ. Most of those are sub-mm dust hits (bag-survivable with armor), but the > 1cm large-particle hit count is itself in the thousands per pass at chunk-bearing zones, and even with engineering-aggressive 20cm-cull mesh the > 20cm hit count stays in single digits per pass at chunk-bearing zones.

**The extended-aperture treatment is not "more pessimistic" — it's the correct way to count hits for an extended vehicle.** The point-vehicle formula was always a unit-conversion convenience; it captures "is at least one absorbing event possible" but not "how many large-particle hits will the bag take per pass". For ICEBERG's 100 m² aperture at chunk-bearing B-ring zones, the answer is: many. Always many.

**No new architectural lever surfaced.** All four interrogation axes are now eliminated from the architectural-recovery search space. The held chunk-rendezvous architecture's death is robust to:
- threshold-relaxation (full L0-10 budget allocation),
- mesh-capability scaling (up to chunk-diameter limit at 1m),
- extended-aperture treatment (worse, not better),
- single-crossing geometry (free architectural lever, doesn't help).

---

## Reading

**The held chunk-rendezvous architecture is doubly-confirmed-non-closing at conservative anchors.** Phoebe's three-round arc on the held architecture — R-hybrid-aerocapture-aerobraking (`1623cca`), R-bring-rendezvous-survivability (`abdcd35`), and now R-bring-survivability-relaxed (this round) — produces a converged falsification:

- aerocapture-engineering: 0 of 1920 cells (three independent failure modes)
- B-ring crossing point-vehicle: 0 of 162 cells (chunk-population vs safe-passage co-location)
- B-ring crossing extended-aperture under all-self-questioning: 0 of 126 cells × 20 closure-check variants

**Project-owner decisions reinforced (no new decisions added):**

The same six decisions surfaced by R-bring-rendezvous-survivability remain on the table. This round adds confidence that the verdict is robust — the architectural collapse is not an artefact of conservative threshold or simplified extended-vehicle treatment. **Phoebe's recommendation strengthens to: retire the held chunk-rendezvous architecture from venture-class viability with high confidence; open R-mission-architecture-pivot-survey and R-program-class-reframe-2 as the next critical-path rounds.**

---

## Cross-learning

1. **Self-questioning rounds are valuable as verdict-robustness checks.** This round's purpose was not to find a new architectural lever — it was to interrogate phoebe's own prior verdict against four plausible "I might be wrong" axes. The result (verdict unchanged, sharper) increases confidence in the architectural decision. Worth doing as a campaign-default after any high-stakes architectural verdict; analogous to the lesson-9 SCOPE-audit pattern but applied to one's own work.

2. **Point-vehicle vs extended-aperture is a load-bearing modeling choice.** The point-vehicle Beer-Lambert formula understates real hit counts for extended-aperture vehicles by 4-6 orders of magnitude. This generalises to any future round with ring crossings, atmospheric particle flux, or debris-field exposure where the vehicle has cross-section much larger than a typical particle. PROTOCOL footnote candidate.

3. **The "loosen the threshold" rescue path doesn't work for B-ring rendezvous.** Even allocating the entire L0-10 budget to one failure-mode category fails to rescue chunk-bearing closure — the architectural impossibility is too large to fit inside any reasonable per-mission risk allocation. This argues against future rounds attempting "what if we relax L0-10 to 0.7?" style rescues; the gap is orders of magnitude, not factors.

4. **Mesh capability scaling has a sharp diminishing-returns curve.** Going from 1cm to 1m mesh reduces τ_unshielded by 67% and reduces extended-aperture hits by ~10⁴ — but at 100× mass cost. The 5cm/10cm/20cm middle band is poorly served: modest gains, modest costs, neither closes the case. Useful campaign reference.

---

## Next-round candidates

- **R-mission-architecture-pivot-survey** (priority: critical-path) — same as named in prior round. The case for pivot is now stronger after self-questioning.
- **R-program-class-reframe-2** (priority: critical-path) — same as named in prior round.
- **R-extended-aperture-correction-prior-rounds** (priority: low) — sweep prior aerocapture-adjacent rounds (R-aerocapture-fast-cruise-envelope, R-chunk-as-heat-shield-revisit) to check whether their atmosphere-vehicle interaction assumed point-vehicle drag/heating that should also be re-derived under extended-aperture treatment. Likely no verdict change (those rounds use vehicle-cross-section properly), but worth a one-page audit.
