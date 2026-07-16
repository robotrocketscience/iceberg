# R-bring-survivability-relaxed — STUDY

**Round:** R-bring-survivability-relaxed (self-questioning follow-up to R-bring-rendezvous-survivability)
**Worker:** phoebe
**Date pre-registered:** 2026-05-15 (latest+8 → +9, second commit of this session)
**Methodology lessons applied:** 1, 7, 8, 9 (audit own prior verdict's input assumptions BEFORE re-running)

---

## Question

R-bring-rendezvous-survivability (commit `abdcd35`) returned 0 of 162 cells closing the per-pass impact-prob target ≤ 10⁻⁴. Under project-owner direction "question your assumptions", interrogate that verdict on four axes that could plausibly flip it:

1. **Closure threshold sensitivity.** The 10⁻⁴ per-crossing target was the SCOPE's "conservative" allocation across 9 ring-plane crossings + all-other-failure-modes within L0-10 = 0.8. If I instead allocate the FULL L0-10 mission-failure budget to the two B-ring crossings (acknowledging they ARE the dominant risk), per-crossing budget rises to ~10⁻² (1.1%) — 110× looser. Does closure open?

2. **Mesh capability sweep.** Prior round assumed cull-mesh stops only < 1cm particles, leaving 75% of τ unshielded (per fine-structure H3). What if engineering effort produces a 5cm-cull, 10cm-cull, or 20cm-cull mesh? Each captures more τ at a mass cost. Does any defensible combination close?

3. **Extended-aperture vs point-vehicle treatment** (audit 3 follow-up from prior round). The titan-anchored P_impact formula is for a point cross-section vehicle. For a 100 m² bag aperture, the EXPECTED hit count is much higher — possibly orders of magnitude. Does this make the verdict sharper or softer?

4. **Single-B-ring-crossing architecture.** Prior round assumed two crossings (inbound rendezvous + outbound). What if the architecture captures and propulsively departs without re-crossing the ring plane (e.g., spiral-out via electric propulsion)? Mission impact prob halves linearly. Does this rescue any cell?

---

## Self-audit of prior round's input assumptions

Per phoebe lesson 9 — apply audit to my OWN prior round, not just the SCOPE.

### Self-audit 1 — closure threshold derivation

The SCOPE method body 1 wrote: "L0-10 rolling-5-mission reliability is 0.8 per REQUIREMENTS.md v0.6. Allocating that across the 9 mission ring-plane crossings (per titan SOI Body 3 crossing inventory) plus all other failure modes gives a per-crossing impact-prob budget of order 10⁻⁴ to 10⁻³. Use 10⁻⁴ (0.01 percent) as the conservative target."

Re-derivation under more-careful budget allocation:
- L0-10 = 0.8 mission-success over 5 missions → per-mission success ≥ 0.8^(1/5) = 0.956 → per-mission failure ≤ 4.4 percent.
- Per-mission failure budget split: launch + cruise + Saturn-side + return + Earth aerocapture failure modes consume some fraction (call it f_other ∈ [0, 1]); the rest is allocated to the 9 ring-plane crossings.
- Per titan SOI body 3 line 184: 7 of the 9 crossings are F-G-gap or G-ring (P_impact ~ 2×10⁻⁵ each), contributing ~0.02 percent total — negligible against 4.4 percent budget.
- The 2 B-ring crossings get essentially the entire ring-related allocation. Per-crossing budget = (4.4% × (1 - f_other)) / 2.

| f_other (fraction of L0-10 budget consumed by non-ring failures) | Per-B-ring-crossing budget | Notes |
|---|---|---|
| 0.99 | 0.022% (2.2×10⁻⁴) | strict: only 1% of mission budget for ring crossings |
| 0.90 | 0.22% (2.2×10⁻³) | moderate |
| 0.50 | 1.1% (1.1×10⁻²) | aggressive: half the budget to B-ring |
| 0.0 | 2.2% (2.2×10⁻²) | extreme: ALL budget to B-ring |
| (SCOPE's 10⁻⁴) | 0.01% | implied f_other ≈ 0.995 — ultra-conservative |

The SCOPE's 10⁻⁴ assumes only ~0.5 percent of mission risk is allocable to a single B-ring crossing, implying 99.5 percent is consumed by other failure modes. That's defensible if other failure modes really are that risky, but it's an unstated assumption. The four thresholds above bracket the defensible range.

### Self-audit 2 — mesh capability anchor

Prior round assumed mesh cull-size = 1 cm fixed, mass = 5 kg/m². Under particle size distribution N(D) ∝ D⁻³ (fine-structure H3), τ contribution from particles > D scales as ln(D_max/D)/ln(D_max/D_min). For D_min = 1 mm, D_max = 10 m:

| Mesh cull size | Fraction of τ above cull (= unshielded by mesh) | τ removed (% of total) |
|---|---|---|
| no mesh | 1.000 | 0% |
| 1 cm | 0.750 | 25% |
| 5 cm | 0.575 | 42.5% |
| 10 cm | 0.500 | 50% |
| 20 cm | 0.425 | 57.5% |
| 1 m | 0.250 | 75% |
| 5 m | 0.075 | 92.5% |
| (10 m = max particle) | 0 | 100% |

Mesh mass scales with capability — heavier wire, more structural support, etc. Order-of-magnitude estimates:
- 1 cm cull: 5 kg/m² (fine wire mesh) → 0.5 t at 100 m²
- 5 cm cull: 25 kg/m² → 2.5 t
- 10 cm cull: 50 kg/m² → 5 t
- 20 cm cull: 100 kg/m² → 10 t
- 1 m cull: 500 kg/m² → 50 t (>10% baseline budget)
- 5 m cull: ~2500 kg/m² → 250 t (mesh exceeds chunk + tug; non-defensible)

Constraint: mesh cull-size cannot exceed target chunk diameter (~6 m for 200t water-ice sphere) — otherwise mesh blocks the chunk being captured. Realistic upper bound: 1 m mesh.

### Self-audit 3 — extended-aperture treatment

Per audit 3 of prior round, point-vehicle P_impact understates extended-vehicle hit count. For a vehicle of cross-section A_v sweeping ring at angle i:

    expected_hits_per_pass = (n_p × h_ring) × A_v × csc(i)

where (n_p × h_ring) is number-density × ring-thickness for particles in the relevant size range. Total τ = (n_total × h) × ⟨σ_particle⟩.

For B-ring particle distribution N(D) ∝ D⁻³ over [1mm, 10m]:
- ⟨D²⟩ = ∫ D² N(D) dD / ∫ N(D) dD ≈ 2 D_min² ln(D_max/D_min) = 2 × 10⁻⁶ × 9.21 = 1.84×10⁻⁵ m²
- ⟨σ⟩ = π/4 × ⟨D²⟩ = 1.45×10⁻⁵ m²
- (n_total × h) = τ / ⟨σ⟩

For zone-avg B-ring (τ=2): n_total × h = 1.38×10⁵ /m².

Number of particles > D per unit ring-area: n(>D) × h ≈ (n_total × h) × (D_min/D)² for D >> D_min.

Expected hits from particles > D for vehicle of A_v at inclination i:
    N_hits(>D) = (n_total × h) × (D_min/D)² × A_v × csc(i)

For zone-avg τ=2, D=1cm, A_v=100m², i=26.7°:
    N_hits(>1cm) = 1.38×10⁵ × (10⁻³/10⁻²)² × 100 × 2.227 = 1.38×10⁵ × 0.01 × 100 × 2.227 = 3.07×10⁵ hits per pass

That's 307,000 hits from > 1cm particles per pass at zone-avg τ=2 with a 100m² bag at Hohmann inclination — vastly mission-fatal.

For outermost 80 km (τ=0.03, scale 67×) × 90° inclination × 1cm cull (mesh stops < 1cm so bag sees only > 1cm hits):
    N_hits(>1cm) = (1.38×10⁵ / 67) × 0.01 × 100 × 1.0 = 2,060 hits per pass

For outermost 80 km × 90° × 5cm cull:
    N_hits(>5cm) = (1.38×10⁵ / 67) × (10⁻³/0.05)² × 100 × 1.0 = 82 hits per pass

For outermost 80 km × 90° × 20cm cull:
    N_hits(>20cm) = (1.38×10⁵ / 67) × (10⁻³/0.20)² × 100 × 1.0 = 5.1 hits per pass

For outermost 80 km × 90° × 1m cull:
    N_hits(>1m) = (1.38×10⁵ / 67) × (10⁻³/1.0)² × 100 × 1.0 = 0.21 hits per pass

The 1m-cull case finally drops EXPECTED hits below 1 per pass — but the mesh costs 50 t (~19% of vehicle baseline, exceeding mass budget) AND the mesh itself takes ALL the smaller-particle hits (300k+ per pass at zone-avg) — mesh structural integrity becomes the new binding constraint.

### Self-audit 4 — single-B-ring-crossing geometry

Prior round assumed inbound rendezvous + outbound = 2 B-ring crossings. Alternative: capture chunk via single B-ring crossing, then propulsively spiral OUT without re-crossing ring plane.

Constraint: vehicle starts on capture-orbit periapsis at 100,000 km (B-ring outer); to depart without re-crossing requires raising periapsis above B-ring outer edge (117,580 km) propulsively while at apoapsis (r_titan = 1,222,000 km). Δv to raise periapsis from 100,000 to 117,580 km at apoapsis (Hohmann-style):

    Δv ≈ v_apo × (Δa/a) where a_initial = 661,000 km, a_final = 669,790 km
    Δv ≈ 2.166 × (8,790/661,000) = 0.029 km/s = 29 m/s

Negligible cost. Single-crossing geometry is cheap and reduces mission impact prob from 1 - (1-P)² to P (linear instead of squared).

For P_per_pass = 2.23% (point-vehicle, prior round best chunk-bearing cell):
- 2 crossings: 1 - (1-0.0223)² = 4.41% mission impact
- 1 crossing: 2.23% mission impact

Doesn't change verdict at point-vehicle level, but is a free architectural lever for the threshold-sensitivity analysis.

---

## Pre-registered hypotheses (BOE central anchors)

| # | Hypothesis | BOE central prediction | Falsification band |
|---|---|---|---|
| H-rsr-1 | Threshold-sweep alone (no other lever changes from prior round): with 1cm cull-mesh × 90° inclination at outermost 80 km, point-vehicle P_per_pass = 2.23%. **Closes at threshold ≥ 2.23%** (i.e., f_other ≤ 0.0). **Falsifies prior verdict only at the most extreme threshold (full L0-10 budget to B-ring), not at any moderate allocation.** | closes at threshold ≥ 2.2% (point-vehicle) | falsified if closes at threshold ≤ 1% |
| H-rsr-2 | Mesh-capability sweep alone (1 cm → 5 cm → 10 cm → 20 cm → 1 m cull) at outermost 80 km × 90° × point-vehicle: each step roughly halves remaining τ_unshielded; 1m mesh gives τ_unshielded = 0.0075, P_per_pass = 0.75%. **Closes at threshold ≥ 0.75%** (mass penalty 19% — exceeds 10% budget). | mesh 1m: P=0.75%, mass 19% → fails mass | falsified if 5cm-mesh closes at < 5% mass penalty |
| H-rsr-3 | Extended-aperture treatment: at outermost 80 km × 90° × 1cm cull × 100 m² bag, expected hits from > 1cm particles per pass ≈ 2,000. **Mission-fatal under any threshold even at 1m cull** (5 hits/pass, each multi-MJ kinetic energy). | extended-aperture > 1 hit/pass at all 1m-cull and below | falsified if any (zone, mesh, inclination) gives < 0.001 expected hits per pass with chunks present |
| H-rsr-4 | Single-crossing architecture: free 2× reduction in mission impact prob; doesn't change per-pass; doesn't open any threshold cell that wasn't already close to closing. | rescues no cell that wasn't already at threshold edge | falsified if single-crossing rescues > 5 cells across the 4D sweep |
| H-rsr-5 (aggregate) | Even with all four self-questioning levers combined (loosest threshold + 1m-cull mesh + extended-aperture-as-best-case + single-crossing), no chunk-bearing cell closes at defensible mass budget. **The prior round's verdict is robust to self-questioning at conservative engineering anchors.** | 0 chunk-bearing cells close under any defensible combination | falsified if any chunk-bearing cell closes under defensible combination |
| H-rsr-6 | The threshold needed to flip the prior verdict (i.e., enable closure at 1cm-mesh × 90° × outermost 80 km, point-vehicle) is **2.2%** per crossing, which corresponds to f_other = 0 (ALL L0-10 budget to B-ring crossings). This is non-defensible because it leaves zero budget for launch / cruise / Saturn-side / return / Earth-aerocapture failure modes. | flip-threshold = 2.2%, requires non-defensible f_other = 0 | falsified if flip-threshold can be reached at f_other ≥ 0.5 (defensible budget split) |

---

## Method

### Body 1 — re-derive threshold-sensitivity table

Compute per-B-ring-crossing budget for f_other ∈ {0.0, 0.5, 0.9, 0.99} as in self-audit 1.

### Body 2 — point-vehicle vs extended-aperture sweep

For each (zone, mesh-cull, inclination) cell from the prior 162-cell grid + extended mesh sweep:
1. Point-vehicle P_per_pass (prior framework)
2. Extended-aperture expected hits (per self-audit 3 derivation)
3. Mass penalty including new mesh-mass model
4. Closure verdict under each of 4 thresholds × {point-vehicle, extended-aperture}

### Body 3 — single-vs-double-crossing variant

For the cells closest to closing under any threshold, recompute with single-crossing assumption. Tag any cell that flips from non-closing to closing under single-crossing.

### Body 4 — find the flip-threshold

For each (zone, mesh, inclination) combination, compute the minimum closure threshold required to declare "closes". Find the combination with the lowest flip-threshold. Adjudicate whether the implied f_other is defensible.

---

## Out of scope

- Re-deriving the L0-10 = 0.8 number itself (REQUIREMENTS.md v0.6).
- Project-owner-retired residence-class architecture (axis 19).
- Aerobraking integration status (assumes phoebe `1623cca` aerobraking falsification stands).

---

## Reading template (worker fills after run.py)

Standard 5-section. Aggregate verdict on H-rsr-agg: is the prior round's verdict robust to self-questioning?
