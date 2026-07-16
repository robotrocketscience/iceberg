# R-particle-distribution-q-sensitivity — STUDY

**Round:** R-particle-distribution-q-sensitivity (fourth self-questioning round of session)
**Worker:** phoebe
**Date pre-registered:** 2026-05-16 (latest+9 → +10)
**Methodology lessons applied:** 1, 7, 9 (audit my own implicit anchor — particle-size-distribution exponent q = 3)

---

## Question

The three prior phoebe rounds on the held chunk-rendezvous architecture (R-bring-rendezvous-survivability, R-bring-survivability-relaxed, R-bag-aperture-chunk-joint) all assumed B-ring particle size distribution N(D) ∝ D⁻³ as the literature anchor (per fine-structure H3 derivation). This came from the Tiscareno et al. 2013 review value q ≈ 3. But the literature actually puts q in the range **[2.5, 4.0]** depending on which observational technique (radio occultation vs ultraviolet occultation vs imaging) and which radial location in B-ring:

- Cuzzi et al. 2010 (Cassini radio occultation): q ≈ 3.0 in B-ring central; q ≈ 2.7 in B-ring outer; q ≈ 2.9 in Cassini Division.
- Tiscareno et al. 2013 (Cassini ISS imaging of ring features): q ≈ 3.0 mean across B-ring features.
- Hedman & Stark 2015 (Cassini visible-infrared spectrometer): q ≈ 3.3 in B3 core.
- Cuzzi et al. 2018 review chapter: q range across B-ring locations is 2.5-4.0, with mean ~3.0 and uncertainty ~0.5 at each location.

Why this matters: my prior three rounds' verdicts depend on the fraction of τ contributed by particles above each mesh-cull diameter. At q=3, 75 percent of τ is above 1 cm. At q=4, only ~10 percent is above 1 cm (much more shieldable). At q=2.5, 97.8 percent is above 1 cm (much less shieldable).

**Self-question:** does the verdict (0 chunk-bearing cells close) survive across the literature-defensible q ∈ [2.5, 4.0]?

---

## Self-audit of q anchor

Per phoebe lesson 9 — re-audit my own anchor.

### Audit: how much of the prior verdict's pessimism comes from q = 3?

For mesh cull diameter d_cull, fraction of τ above d_cull is:
- q = 2 (constant area-per-bin): fτ(>d_cull) = (D_max - d_cull) / (D_max - D_min)
- q = 3: fτ(>d_cull) = ln(D_max / d_cull) / ln(D_max / D_min)
- q = 4: fτ(>d_cull) = (d_cull⁻¹ - D_max⁻¹) / (D_min⁻¹ - D_max⁻¹) ≈ D_min / d_cull for d_cull >> D_min
- Generic q ≠ 1, 2, 3: ∫_d D^(2-q) dD / ∫_{D_min} D^(2-q) dD

For D_min = 1 mm, D_max = 10 m:

| Mesh cull | q = 2.5 | q = 3.0 | q = 3.5 | q = 4.0 |
|---|---|---|---|---|
| 1 cm | 0.968 | 0.750 | 0.317 | 0.100 |
| 5 cm | 0.927 | 0.575 | 0.142 | 0.020 |
| 10 cm | 0.900 | 0.500 | 0.100 | 0.010 |
| 20 cm | 0.860 | 0.425 | 0.071 | 0.005 |
| 1 m | 0.683 | 0.250 | 0.0316 | 0.001 |

So q-sweep matters most at moderate cull sizes (1cm-20cm). At q=4, even 1cm mesh removes 90 percent of τ (vs 25 percent at q=3); at q=2.5, even 1m mesh removes only 32 percent of τ.

### Why this is worth testing

Two opposing directions of bias possible:
1. **If true q is closer to 2.5 than 3** (i.e., heavier tail toward large particles): verdict gets MORE pessimistic; impossible architecture is even more impossible. Robustness check confirms verdict.
2. **If true q is closer to 4 than 3** (i.e., heavier tail toward small particles): verdict gets SOFTER; cull-mesh effectiveness rises 7.5×. Could potentially flip the verdict.

Real B-ring has q distributed across this range by radial location. Architectural choice could target high-q regions (where most particles are sub-cm).

---

## Pre-registered hypotheses (BOE central anchors)

### BOE: extended-aperture P_ea at outermost-180km × 90° × 1m mesh × bag=100m² as function of q

Using:
- τ_total = 0.10 (outermost 180 km, thin chunks)
- n_total × h = τ / ⟨σ⟩, where ⟨σ⟩ depends on q
- n(>1m) × h scales with both n_total and number-fraction-above-1m

For q=3: ⟨σ⟩ = π/4 × 2 × D_min² × ln(D_max/D_min) = 1.45e-5 m². n_total × h = 6,897 /m². n(>1m)/n_total = (D_min/1)² = 10⁻⁶. hits = 6,897 × 10⁻⁶ × 100 = 0.69 hits/pass at 26.7°; at 90° = 0.31 hits/pass. P_ea = 26%.

For q=4: ⟨D²⟩ = 3 × D_min² (different normalisation). n_total × h ~ proportional. n(>1m)/n_total = (D_min/1)³ = 10⁻⁹. hits scale down much harder.

Detailed computation needed (in run.py).

### Pre-registered hypotheses

| # | Hypothesis | BOE central prediction | Falsification |
|---|---|---|---|
| H-pq-1 | At q = 2.5 (heavier toward large particles), verdict is MORE pessimistic than q = 3 baseline | hits/pass at chunk-bearing × 1m mesh × 90° rises by 5-10× vs q=3 | falsified if hits drop or rise > 100× |
| H-pq-2 | At q = 4.0 (heavier toward small particles), 1m mesh removes ≥ 99% of τ; P_ea at outermost-180km × 90° × 1m mesh drops by ≥ 100× vs q=3 | hits/pass drops from 0.31 (q=3) to ≤ 0.003 | falsified if doesn't drop by ≥ 100× |
| H-pq-3 | At q ≥ 3.5, the chunk-bearing cell (outermost-180km × 90° × 1m mesh) closes at strict threshold (10⁻³) | closes at q ≥ 3.5 with 1m mesh | falsified if doesn't close at any q ≤ 4.0 with 1m mesh |
| H-pq-4 | At q ≥ 3.5, the chunk-bearing cell (outermost-180km × 90° × 20cm mesh) closes at strict threshold | closes at q ≥ 3.5 with 20cm mesh (more defensible mass-wise) | falsified if doesn't close at q ≤ 4.0 with 20cm mesh |
| H-pq-5 | Even at q = 4.0 with 1m mesh closing P_ea, the mass-penalty constraint still fails (50t mesh too heavy) — so verdict is still NEGATIVE on all-five-constraint closure | mass-budget still binds at q = 4 | falsified if all-five-constraint closes at any q ∈ [2.5, 4.0] |
| H-pq-6 | The "20 cm mesh × q=4" combination is the most plausible architecturally-credible closure: P_ea ≤ 10⁻³, mass-penalty ≤ 10%, chunks present. If this combination closes, the architecture is **conditionally** rescued under "high-q anchor" assumption — but credibility requires showing real B-ring is at q ≥ 3.5 at the rendezvous radius. | (20 cm × q=4) at outermost-180km × 90° gives marginal closure | falsified if doesn't close even at q=4 with 20cm mesh |
| H-pq-7 (aggregate) | Verdict (0 chunk-bearing cells close on all-five-constraint) is robust across q ∈ [2.5, 4.0] for defensible mass-budget configurations (mesh ≤ 20cm). At q=4 + 1m mesh, survivability MAY close but mass-budget still binds; that's not a defensible rescue. | verdict holds across literature q range for defensible mass | falsified if any chunk-bearing cell closes on all-five-constraint AT defensible q ∈ [2.7, 3.3] (the published mean ± 1σ) |

---

## Method

For each q ∈ {2.5, 2.7, 3.0, 3.3, 3.5, 4.0}:
1. Recompute ⟨σ⟩, n_total × h, n(>D)/n_total for each (zone, mesh) pair.
2. Recompute extended-aperture P_ea per pass.
3. Tag closure under each of 5 thresholds + mass budget + chunks present + venture-class hurdle (anchor on R-bag-aperture-chunk-joint's 200t chunk × bag=100m² setup for like-for-like comparison).
4. Tabulate: at what q does each (zone, mesh, inclination) combination flip from non-closing to closing?

Sweep: q × zone (5 chunk-bearing or chunk-near zones) × mesh (6 options) × inclination (3) = 6 × 5 × 6 × 3 = 540 cells. Sub-second wall clock.

---

## Out of scope

- Re-deriving q empirically (anchored on literature range).
- Spatial variation of q within B-ring (treat as global parameter for this sweep).
- Particle-density variation with size (assume constant ρ = 2500 kg/m³).
- Anything outside the architectural-survivability question.

---

## Reading template

Standard 5-section. Aggregate verdict: across literature q ∈ [2.5, 4.0], does any chunk-bearing cell close on all-five-constraint under defensible mass budget?
