# R-bag-aperture-chunk-joint — STUDY

**Round:** R-bag-aperture-chunk-joint (third self-questioning round of session)
**Worker:** phoebe
**Date pre-registered:** 2026-05-15 (latest+8 → +9, third commit of session)
**Methodology lessons applied:** 1, 7, 9 (audit my own assumption — bag aperture = 100 m² was anchored without justification)

---

## Question

I anchored bag aperture at 100 m² in R-bring-rendezvous-survivability and R-bring-survivability-relaxed without explicit justification. Bag aperture is a CHOSEN architectural parameter, not a fundamental constraint. A smaller bag means:

- Linearly fewer hits per pass (extended-aperture treatment scales with A_v).
- Linearly lower mesh mass at any given mesh capability (mesh kg/m² × A_v).
- Constraint: bag aperture ≥ chunk frontal area + capture margin (~20%).

The constraint chains bag aperture to chunk mass: smaller bag requires smaller chunk. Phoebe's R-variant-B-100t-resizing (`b5d37a9`) showed no (chunk, reactor) point in the swept envelope simultaneously satisfies propellant-feasibility AND L0-05 closure for chunks ≤ 200 t — but that was sweeping chunks 100-200 t, not chunks ≤ 50 t.

**Joint question:** does shrinking bag aperture AND chunk mass simultaneously open any combination that satisfies (a) B-ring crossing survivability under extended-aperture treatment AND (b) propellant-feasibility AND (c) defensible threshold AND (d) chunk-availability in zone?

If yes, I owe the project owner a retraction of the prior verdict's "doubly-load-bearing → architecturally non-closing" framing. If no (predicted), I confirm the prior verdict is robust against the bag-aperture lever too.

---

## Self-audit of bag-aperture anchor

R-bring-rendezvous-survivability anchored A_v = 100 m² implicitly because:
- 200 t chunk at water-ice density 917 kg/m³ has spherical-equivalent diameter 7.5 m, frontal area 43.9 m².
- Bag must be ≥ chunk frontal area + capture margin → ≥ 53 m² for 200 t chunk.
- 100 m² provides ~2× capture margin, reasonable for envelope/skirt structure.

But the bag-aperture-chunk-mass relationship is one-to-one for any chunk size:

    A_bag_min(m_chunk) = 1.2 × π × (3 m_chunk / (4π ρ_ice))^(2/3)

| Chunk mass | r_chunk | A_chunk_frontal | A_bag_min (1.2× margin) |
|---|---|---|---|
| 10 t | 1.37 m | 5.92 m² | 7.1 m² |
| 20 t | 1.73 m | 9.42 m² | 11.3 m² |
| 50 t | 2.34 m | 17.2 m² | 20.6 m² |
| 100 t | 2.95 m | 27.4 m² | 32.9 m² |
| 200 t | 3.71 m | 43.3 m² | 52.0 m² |
| 482 t (B-ring single-chunk cap) | 4.99 m | 78.4 m² | 94.0 m² |

So smaller chunks enable smaller bags. At 10 t chunk, 7 m² bag — 14× smaller than the 100 m² anchor.

**The question this round answers:** does any (chunk-mass, bag-aperture) combination at the bag-min boundary, combined with mesh capability + inclination + zone, yield a closure cell? And does that closure cell satisfy R-variant-B-100t-resizing's propellant feasibility?

---

## Pre-registered hypotheses (BOE central anchors)

### BOE: extended-aperture hits per pass at outermost 80 km × 90° × 1m cull, bag aperture sweep

n_total × h at outermost 80 km (τ = 0.03) = 0.03 / 1.45×10⁻⁵ = 2,070 /m²
n(>1m) × h = (0.001/1)² × 2,070 = 2.07×10⁻³ /m²
hits/pass = 2.07×10⁻³ × A_v × csc(90°) = 2.07×10⁻³ × A_v

| Bag aperture | hits/pass at 1m mesh | P_ea per pass |
|---|---|---|
| 100 m² | 0.207 | 18.7% |
| 50 m² | 0.104 | 9.9% |
| 30 m² | 0.062 | 6.0% |
| 20 m² | 0.041 | 4.1% |
| 10 m² | 0.021 | 2.1% |
| 7 m² | 0.014 | 1.4% |

**Sweet spot: bag ≤ 10 m² (chunk ≤ ~13 t) gets P_ea ≤ 2.2% at outermost 80 km × 90° × 1m mesh.** Closes at extreme threshold (2.2%, non-defensible). Chunk-availability: outermost 80 km is sparse.

### BOE: mesh mass with smaller bag

1m cull mesh @ 500 kg/m² × A_bag:
- 100 m²: 50 t (19% of 264-t baseline)
- 10 m²: 5 t (1.9% of baseline) — within budget!

So the small-bag/small-chunk combination **does** satisfy mass-penalty AND P_impact at the extreme threshold AND with 1m mesh.

But the architectural cost: chunk 13 t means delivered mass per mission is ~13 t (gross) instead of 200 t. **Per R-delivery-irr-curve and R-variant-B-100t-resizing, delivered mass < 100 t/mission falls below all venture-class hurdle rates.** The architecture survives the B-ring crossing but doesn't pay for the launch.

### Pre-registered hypotheses

| # | Hypothesis | BOE central prediction | Falsification |
|---|---|---|---|
| H-bach-1 | Bag aperture scales with chunk mass^(2/3) per geometry constraint A_bag ≥ 1.2 π r_chunk² | A_bag(13t) = ~9 m²; A_bag(200t) = ~52 m² | falsified if bag ≥ chunk-min relationship breaks |
| H-bach-2 | At outermost 80 km × 90° × 1m cull mesh, expected hits per pass scales linearly with A_v: 0.21 hits/pass at 100 m²; ≤ 0.022 hits/pass at 10 m² | hits drop to ≤ 1 at A_v ≤ 50 m² | falsified if A_v scaling deviates from linear by > 20% |
| H-bach-3 | At outermost 80 km × 90° × 1m mesh × A_v = 10 m², P_ea per pass = 2.1%, marginally closes at extreme threshold (2.2%, f_other=0) | closes at threshold = 2.1% | falsified if doesn't close even at f_other=0 OR closes at f_other > 0.3 (defensible) |
| H-bach-4 | Mesh mass at 1m cull × A_v = 10 m² is 5 t = 1.9% of vehicle baseline (264 t) | mass penalty closes at A_v ≤ 50 m² with 1m mesh | falsified if mass exceeds 10% at any A_v ≤ 50 m² |
| H-bach-5 | The closure cell (chunk = 13 t, bag = 10 m², 1m mesh, outermost 80 km, 90°) is at chunk-SPARSE zone — so even if survival closes, the bag scoops nothing | sparse zone has chunk-thin contents; per fine-structure H1+H2 essentially no large particles in outermost 80 km | falsified if chunk-availability data shows >1 large particle per 1000 m³ in outermost 80 km |
| H-bach-6 | Even if survivability closes for chunk = 13 t, the architecture fails on per-R-delivery-irr-curve sovereign-bond hurdle (209 t/ship needed); 13 t is 16× short | venture-class IRR not reachable at 13 t/mission | falsified if delivered mass per mission ≥ 209 t at small-chunk architecture |
| H-bach-agg | Even with the bag-aperture-chunk-mass joint relaxation, no closure cell satisfies (survivability AND mass-budget AND propellant-feasibility AND chunk-availability AND venture-class economics) — verdict robust to this lever too | 0 cells satisfy all 5 constraints simultaneously | falsified if any cell satisfies all 5 |

---

## Method

For each (chunk_mass, A_v_bag, mesh_capability, zone, inclination):
1. Verify A_v ≥ A_bag_min(chunk_mass).
2. Compute extended-aperture hits/pass and P_ea.
3. Compute mass penalty (mesh + inclination Δv).
4. Tag closure under each of 5 thresholds.
5. Tag chunk-availability in zone.
6. Tag economic viability per R-delivery-irr-curve hurdles (209 t/ship for 4% sovereign-bond, 461 t for 8% regulated-utility).
7. Aggregate: ALL constraints simultaneously satisfied.

Sweep:
- chunk_mass ∈ {10, 20, 50, 100, 200, 482} t
- A_v_bag ∈ {bag_min, 2×bag_min, 4×bag_min, 100} m²
- mesh ∈ {none, 1cm, 5cm, 10cm, 20cm, 1m}
- zone ∈ {B-ring zone-avg, outer-580km, Huygens-ringlet, outermost-180km, outermost-80km}
- inclination ∈ {26.7°, 60°, 90°}

= 6 × 4 × 6 × 5 × 3 = 2160 cells

---

## Out of scope

- Re-deriving R-variant-B-100t-resizing's propellant-feasibility (anchor on its result).
- Re-deriving R-delivery-irr-curve's hurdle-rate findings (anchor on 209/461/691 t hurdles).
- Bag aperture below A_bag_min (geometrically infeasible).

---

## Reading template

Standard 5-section. Aggregate verdict: does the bag-aperture-chunk-mass joint lever rescue ANY architectural cell, or does the venture-class economic constraint close it even when survivability opens?
