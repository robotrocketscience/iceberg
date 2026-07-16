# R-particle-distribution-q-sensitivity — closure verdict

**Round:** R-particle-distribution-q-sensitivity (4th self-question of session, 7th phoebe round overall)
**Worker:** phoebe
**Date:** 2026-05-16 (latest+9 → +10)
**Pre-registration:** `STUDY.md`
**Sweep results:** `R_particle_distribution_q_sensitivity.json`

---

## Headline

**The prior verdict (0 chunk-bearing cells close) is robust to the particle-size-distribution exponent across the literature range q ∈ [2.5, 4.0].** At q = 4 (most-favourable-to-architecture extreme of literature range, where most τ is in small/shieldable particles), the best chunk-bearing cell that satisfies mass-budget still gives P_ea = 45.8% per pass — 458× short of the strict closure threshold and 20× short of even the non-defensible extreme threshold. The q anchor I used in three prior rounds (q = 3, literature mean) was NOT load-bearing on the verdict.

---

## Hypothesis verdicts

| H# | Predicted | Measured | Verdict |
|---|---|---|---|
| H-pq-1 (q=2.5 verdict more pessimistic) | hits/pass at outermost-180km × 1m mesh × 90° rises 5-10× vs q=3 | hits = 1.31 (q=2.5) vs 0.68 (q=3) → ~2× rise (less than predicted); P_ea = 73% vs 50% | HOLD-weak (direction correct, magnitude over-predicted) |
| H-pq-2 (q=4 drops P_ea ≥ 100×) | hits drop from 0.31 to ≤ 0.003 | hits = 0.0042 at q=4 (drops 73×, slightly below predicted 100×) | HOLD-near-prediction |
| H-pq-3 (q ≥ 3.5 closes at strict with 1m mesh) | closes at q ≥ 3.5 with 1m mesh × outermost-180km × 90° | q=3.5: P_ea = 7.8% — 78× short of strict (10⁻³); q=4.0: P_ea = 0.42% — 4× short of strict; closes aggressive (1.1e-2) but mass fails | **FALSIFIED** at strict; partially holds at aggressive — but mass-budget fails anyway |
| H-pq-4 (q ≥ 3.5 closes at strict with 20cm mesh) | closes at q ≥ 3.5 with 20cm | q=3.5: P_ea = 99.5%; q=4.0: P_ea = 46% — both fail | **FALSIFIED** |
| H-pq-5 (mass-budget binds even at q=4 + 1m mesh) | mass-budget still fails | confirmed: 1m mesh = 50t + 25.5t prop = 75.5t = 29% (fails 10% budget) | HOLD-strong |
| H-pq-6 (20cm × q=4 marginally closes) | marginally closes survivability AND mass | survivability P_ea = 46% (fails strict by 460×, fails moderate by 200×, fails aggressive by 42×, fails extreme by 21×) | **FALSIFIED** |
| H-pq-7 (verdict robust across literature q) | 0 cells close at all-five-constraint at any q ∈ [2.5, 4.0] | confirmed: 0/540 cells close at strict or moderate threshold at any q | **HOLD-strong** |

---

## Aggregate verdict — H-pq-agg

**HELD-strong.** The verdict is robust to the q anchor across the full literature range [2.5, 4.0]. Two opposing direction-of-bias effects partially cancel:

- **At low q (heavier toward large particles):** mean particle cross-section ⟨σ⟩ grows (because the τ-contribution is dominated by larger particles), so n_total × h drops. But number-fraction-above-d-cull grows even faster (slow tail-off). Net: hit count rises modestly (~2× from q=3 to q=2.5).
- **At high q (heavier toward small particles):** ⟨σ⟩ drops (more τ in small particles); n_total × h rises by factor ~6 from q=3 to q=4. But number-fraction-above-d-cull drops by factor 10⁴ at d_cull=1m. Net: hit count drops, but by less than predicted.

At q=4 (literature extreme), the 1m-cull mesh case at outermost-180km × 90° gives P_ea = 0.42% per pass — closes the aggressive threshold (1.1%) but mass-budget fails (50t mesh + 25.5t Δv prop = 29% of 264t vehicle). At 20cm mesh (mass-passing at 60° inclination), P_ea = 46% — fails all thresholds.

**No combination of (q, mesh, inclination, zone) satisfies all-five-constraint closure at any q ∈ [2.5, 4.0]** for the 200-t chunk baseline.

---

## q-sensitivity reference table (outermost-180km × 90° × bag=100m²)

| q | ⟨σ⟩ [m²] | no mesh P_ea | 1cm mesh P_ea | 5cm mesh P_ea | 10cm mesh P_ea | 20cm mesh P_ea | 1m mesh P_ea |
|---|---|---|---|---|---|---|---|
| 2.5 | 2.3×10⁻⁴ | 100% | 100% | 100% | 100% | 100% | 73.1% |
| 2.7 | 6.6×10⁻⁵ | 100% | 100% | 100% | 100% | 100% | 69.2% |
| 3.0 | 1.4×10⁻⁵ | 100% | 100% | 100% | 100% | 100% | 49.6% |
| 3.3 | 5.6×10⁻⁶ | 100% | 100% | 100% | 100% | 100.0% | 19.9% |
| 3.5 | 3.9×10⁻⁶ | 100% | 100% | 100% | 100% | 98.9% | 7.8% |
| 4.0 | 2.4×10⁻⁶ | 100% | 100% | 100% | 98.6% | 41.2% | 0.42% |

Pattern: q dependence is strongest at moderate mesh capabilities (10cm-1m). At 1m mesh, P_ea spans 73% (q=2.5) to 0.42% (q=4) — three orders of magnitude. But mass-budget for 1m mesh fails regardless of q. At mass-budget-passing meshes (≤ 5cm), P_ea ≥ 100% at all q ≥ 2.5.

---

## Best chunk-bearing cell per q (closes_mass AND chunks_present, lowest P_ea)

| q | Zone | Mesh | Inclination | P_ea per pass | Penalty fraction |
|---|---|---|---|---|---|
| 2.5 | outermost-180km | 20cm | 60° | 100% | 9.0% |
| 2.7 | outermost-180km | 20cm | 60° | 100% | 9.0% |
| 3.0 | outermost-180km | 20cm | 60° | 100% | 9.0% |
| 3.3 | outermost-180km | 20cm | 60° | 100.0% | 9.0% |
| 3.5 | outermost-180km | 20cm | 60° | 99.5% | 9.0% |
| 4.0 | outermost-180km | 20cm | 60° | **45.8%** | 9.0% |

At every q, the best chunk-bearing cell that passes mass-budget is outermost-180km × 20cm mesh × 60°. The "best" cell barely changes — but its P_ea is 100% at q ≤ 3.5 and drops to 46% at q=4. Even the q=4 case is 20× short of the extreme threshold (2.2%).

---

## What this means

**The verdict is robust to ALL FOUR self-questioning axes I have now tested:** (a) closure threshold, (b) mesh capability, (c) bag-aperture-chunk-mass joint, (d) particle-distribution exponent q across the literature range. Four convergent self-questions on the verdict. Combined with the original two engineering rounds, the held chunk-rendezvous architecture has been falsified five times over from independent angles.

**Methodology note:** the only direction that softens the verdict is q → 4 (heavier toward small particles). Literature mean is q ≈ 3 with site-to-site variation ±0.5. To have a defensible q ≥ 3.5 anchor, the architecture would need to specifically target B-ring locations where Cassini measurements show high q — which Hedman & Stark 2015 found in B3 core (q ≈ 3.3 ± 0.2). But B3 core has τ = 4.5 — even at q = 4 with 1m mesh, P_ea would still be near 100% there due to overwhelming τ. The "target high-q location" strategy doesn't rescue the architecture either.

---

## Reading

**The held chunk-rendezvous architecture is now FIVE-WAY confirmed-non-closing.** Phoebe's session arc:

1. R-hybrid-aerocapture-aerobraking (`1623cca`): atmospheric capture engineering — 0/1920
2. R-bring-rendezvous-survivability (`abdcd35`): B-ring crossing point-vehicle — 0/162
3. R-bring-survivability-relaxed (`45869d4`): self-Q on threshold/mesh/extended-aperture/crossing — 0/126 × 20 variants
4. R-bag-aperture-chunk-joint (`8a31ba9`): self-Q on bag-aperture × chunk-mass × economics — 0/2160
5. R-particle-distribution-q-sensitivity (this round): self-Q on particle-size exponent across literature range — 0/540

**Project-owner-decisions surfaced (unchanged from prior session):** retire held chunk-rendezvous as venture-class architecture; reframe matrix axis 19; promote R-mission-architecture-pivot-survey + R-program-class-reframe-2 as critical-path; add three PROTOCOL footnotes (geometric-vs-kinetic survivability; chunk-population vs safe-passage co-location; extended-aperture vs point-vehicle treatment); add one campaign utility (`bag_min_area_m2(chunk_t)`).

**Phoebe is now demonstrably out of internal levers to interrogate.** Five self-questioning rounds have exhausted the obvious assumption space (threshold, mesh, aperture, chunk-mass, particle-distribution-exponent). The verdict is robust against all. Further self-questioning on this architecture would require challenging structural assumptions (e.g., L0-10 reliability target itself, REQUIREMENTS-L1 chunk-cap, B-ring optical-depth measurements from Cassini), which is requirements/measurements territory not engineering territory.

---

## Cross-learning

1. **Convergent self-questioning produces high-confidence verdicts.** Four self-question rounds, each interrogating a different anchor, each from a different angle, all confirming. The combined evidence is dramatically stronger than any single round. **PROTOCOL methodology lesson 11 candidate (4th corroboration this session)** continues to mount.

2. **Two opposing biases partially cancel in the q-sweep.** Lower q (heavier toward large): higher hit count from large particles, but lower n_total. Higher q (heavier toward small): more shieldable, but higher n_total. The two effects partially cancel — verdict is more robust to q than I'd have predicted from either effect alone. This is an instance of "interrogate symmetric-looking assumptions because the sensitivity may surprise you" — worth a PROTOCOL footnote.

3. **The "target high-q location" architectural rescue path is foreclosed.** If a future worker proposes "let's target B3 core where q is higher", the τ = 4.5 there overwhelms the q rescue. Documented for the architecture-pivot search space.

4. **The chunk-population vs safe-passage co-location problem is now confirmed across BOTH τ-zone variation AND q variation.** This is the architecturally-binding constraint. Future architecture-pivot rounds should anchor on this finding as a hard constraint.

---

## Next-round candidates (unchanged from prior recommendation)

- **R-mission-architecture-pivot-survey** (priority: critical-path)
- **R-program-class-reframe-2** (priority: critical-path)

Phoebe has now exhausted the internal-assumption interrogation layer. The next session — whether phoebe or another worker — should pivot to genuinely new architectural-search territory.
