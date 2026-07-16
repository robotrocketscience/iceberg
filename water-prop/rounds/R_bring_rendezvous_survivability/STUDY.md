# R-bring-rendezvous-survivability — STUDY

**Round:** R-bring-rendezvous-survivability
**Worker:** phoebe
**Date pre-registered:** 2026-05-15 (latest+8 → +9)
**SCOPE author:** Saturn (orchestrator), 2026-05-15 latest+6
**Methodology lessons applied:** 1 (pessimistic-prediction default), 7 (compute under most pessimistic credible anchor first), 8 (per-mission cashflow ≠ program NPV), 9 (anchor on prior aggregate-verdict primary text, not summaries)

---

## Question

Engineering question 2 of 2 on the held chunk-rendezvous architecture. For a chunk-rendezvous mission at periapsis 100,000 km (B-ring outer edge), arrival inclination 26.7° (Earth-Hohmann to Saturn equator), 200-tonne chunk × 64-tonne tug × bag — under what engineering combination, if any, does per-pass B-ring impact probability drop from titan's 98.85 percent to ≤ 0.01 percent (the conservative L0-10 per-crossing allocation)?

Held architecture has two load-bearing engineering questions: aerocapture (R-hybrid-aerocapture-aerobraking, phoebe `a7a8456` awaiting integration — falsified at 0/1920 cells) and B-ring crossing survivability (this round). If both fail, the chunk-rendezvous architecture has no surviving cell at conservative anchors.

---

## SCOPE audit (lesson 9 applied)

Per phoebe lesson 9 (anchor on PRIMARY text of prior rounds, not summary statements in SCOPE), I read `R_saturn_soi_periapsis_depth/STUDY.md` body 3 lines 131-204 and `R_bring_fine_structure_rendezvous/STUDY.md` body 3 lines 82-180 directly before drafting predictions. Four input-assumption issues in the SCOPE that are load-bearing on the round's framing:

### Audit 1 — geometric impact probability is velocity-independent (load-bearing on H4 framing)

The SCOPE's H4 (slow-cross-only) is implicitly framed as a probability-reduction lever — "slow vehicle from ~20 km/s to 5 km/s". This conflates two distinct quantities. Per-pass impact probability for a vehicle traversing a ring at angle `i` to ring plane is governed by:

    P_impact = 1 - exp(-τ × csc(i))   [titan SOI body 3, line 187 — reproduces 98.85% at τ=2, i=26.7°]

The formula has no velocity dependence. It is purely geometric: optical depth `τ` (Beer-Lambert through-ring opacity) and inclination `i` (path-length factor through the ring slab). Slowing the vehicle **does not** reduce per-pass impact probability — it reduces per-impact kinetic energy, which is a survival-given-impact lever, mechanistically identical to armour (H1).

**Implication for H4 framing.** H4 collapses to one of two cases: (a) survival-given-impact lever (degenerate with H1, evaluate jointly), or (b) propulsive-cost-only line (no impact-probability reduction at all, no closure achievable through this lever). The SCOPE's "slow-cross-only" should be evaluated as a residence-class-asymptote: any meaningful slow approach IS the residence architecture (project-owner-retired per axis 19, 14.7 km/s round-trip cost) until the slow-cross is matched to ring-orbit speed at which point relative velocity drops to ~10 m/s and impacts become non-fatal.

### Audit 2 — "20 km/s to 5 km/s" frame ambiguity (load-bearing on H4 magnitude)

The SCOPE's H4 narrative says "slow vehicle from ~20 km/s (B-ring outer orbital speed at 100,000 km radius) to 5 km/s". The ~20 km/s figure is the **ring-particle orbital speed in Saturn-inertial frame** at r = 100,000 km (v_circ = √(GM_S/r) = 19.48 km/s). The vehicle on capture orbit r_p = 100,000 km × r_a = r_titan = 1.222×10⁶ km is at v_p = 26.5 km/s at periapsis. **Vehicle-to-ring relative velocity is not 20 km/s.** Standard prograde equatorial case: |v_p - v_circ| = 7.0 km/s, matching HE-graze H-hgf-a (6.56 km/s at slightly different periapsis). For the architecturally-relevant 26.7° inclined arrival, in-plane component contributes 4.2 km/s, out-of-plane component contributes 11.9 km/s, total |Δv_rel| = 12.6 km/s.

**Implication for H4.** The "slow from 20 to 5 km/s" recipe is not what the SCOPE author intended. To reduce vehicle-to-ring-particle relative velocity to ≤ 100 m/s (HE-graze H-hgf-c soft-capture limit), the vehicle must match ring-orbital velocity in both magnitude and direction — the residence-class burn (~7.4 km/s one-way per HE-graze H-hgf-d). H4 in operational terms is degenerate with the project-owner-retired residence architecture.

### Audit 3 — armour H1 is well-framed, but the cross-section bookkeeping needs care

The SCOPE's H1 correctly states armour does not change the impact-prob bound, only post-impact survival fraction. This is the right framing. However, P_impact in titan SOI was computed for a POINT vehicle. For an extended-cross-section vehicle (bag aperture A_v ~ 100 m²), the appropriate generalisation depends on what counts as "impact":

- **"Bag-killing impact" definition.** P(at least one >1cm-particle hit) per pass. Then ⟨N_hits_>1cm⟩ ≈ τ_>1cm × csc(i) × (A_v / σ_typical_>1cm_particle). For τ_>1cm = 0.075 (B-ring outer 200 km, 75% of total τ per fine-structure H3), σ_typical_>1cm ~ π × (0.01 m)² = 3.1×10⁻⁴ m², A_v = 100 m²: ⟨N⟩ = 0.075 × 2.227 × (100 / 3.1×10⁻⁴) = 5.4×10⁴ hits per pass at 26.7°. Per-pass survival probability is essentially zero for any large-particle armour density.
- **"Catastrophic structural failure" definition.** A single >10cm or meter-class hit is bag-fatal even with armour. P(at least one ≥10cm hit) per pass, using fine-structure H3 q=3 power law: τ_>10cm = (1cm/10cm)² × τ_>1cm × correction-factor ≈ 0.0075 (a few percent of τ_>1cm). ⟨N_>10cm⟩ ≈ 0.0075 × 2.227 × (100 / π×(0.05)²) = 2,100 per pass at 26.7° in B-ring outer 200 km. Still far above closure threshold.

**Implication for round computation.** Use the point-vehicle formula for like-for-like comparison with titan SOI; explicitly note in the closure verdict that the bag-cross-section adjustment makes the result strictly worse, not better, by 5-6 orders of magnitude on the hit-count metric.

### Audit 4 — H3 Edelbaum cost computed at wrong orbital point (load-bearing on H3 magnitude)

The SCOPE's method 5 H3 says "Edelbaum-style continuous-thrust inclination change. Cost scales as 2 × v × sin(Δi/2)". For an elliptical orbit (capture orbit r_p = 100,000 km, r_a = r_titan = 1.222×10⁶ km), the cheapest place for an impulsive plane change is at apoapsis where vehicle velocity is lowest. v_apo = 2.166 km/s (vis-viva). Edelbaum impulsive-equivalent at apoapsis:

    Δv_plane(at apoapsis) = 2 × v_apo × sin(Δi/2)
    Δv_plane(at periapsis) = 2 × v_p × sin(Δi/2)   [13× more expensive]

For Δi = 63.3° (26.7° → 90° normal-to-ring-plane):
    at apoapsis: 2 × 2.166 × sin(31.65°) = 2.27 km/s
    at periapsis: 2 × 26.5 × sin(31.65°) = 27.8 km/s

The SCOPE's H3 prediction "≥ 5 km/s, falsifies if ≤ 1.5 km/s" implicitly anchors on the periapsis-burn cost (which is what continuous-thrust Edelbaum approximates around the orbit). At apoapsis the impulsive cost is ~2.3 km/s — already above the 1.5 km/s falsification floor but well below the 5 km/s prediction. **H3 will land "wrong-but-informative" — the propulsive cost is lower than predicted, but the impact-prob target is still not reached even at 90° inclination because the τ stays above 0.07 even at the most favourable B-ring location.**

---

## Pre-registered hypotheses (BOE central anchors first, then bands)

Per phoebe methodology lessons 1, 7, 9 — central BOE anchor computed FIRST in the audit above, falsification bands wrapped around each. SCOPE H1-H6 carry over with reframings noted under audit 1 and 4.

### BOE central anchors

| Lever | Predicted measured value | Method |
|---|---|---|
| **Baseline P_impact at titan-anchored geometry** (B-ring zone-average τ=2.0, i=26.7°) | **98.8% per pass** | 1 - exp(-2.0 × csc(26.7°)) = 1 - exp(-4.454) — reproduces titan SOI body 3 line 186 |
| **Best-location P_impact (outermost 80 km B-ring, τ=0.03)** at i=26.7° | **6.5% per pass** | 1 - exp(-0.03 × 2.227) — fine-structure H3 anchor |
| **Best-location-best-inclination P_impact (outermost 80 km, i=90°)** | **3.0% per pass** | 1 - exp(-0.03 × 1.0) |
| **Cull-mesh-augmented P_impact (outermost 80 km, mesh removes shieldable 25%, leaving τ_unshieldable = 0.0225, i=90°)** | **2.2% per pass** | 1 - exp(-0.0225 × 1.0) |
| **Maximum-stack P_impact (outermost 80 km + mesh + 90° + armour for survival-given-impact, τ_eff = 0.0225, i=90°)** | **2.2% per pass** | armour does not enter probability bound |
| **L0-10 per-crossing target** | **0.01% per pass** (10⁻⁴) | from L0-10 0.8 / 5 missions / ~9 crossings × all-other-failures, conservative allocation |
| **Closure gap at maximum-stack** | **220× short of target per pass** | 2.2% / 0.01% |
| **Inclination-change Δv at apoapsis (26.7° → 90°)** | **2.27 km/s one-way, 4.55 km/s round-trip** | 2 × v_apo × sin(31.65°) |
| **Mass penalty for armour @ 50 kg/m² × 100 m² aperture** | **5,000 kg = 5 t** | linear |
| **Mass penalty for cull mesh @ 5 kg/m² × 100 m²** | **500 kg = 0.5 t** | linear |
| **Mass penalty for inclination-change Δv (Variant B Isp=5000s, ve=49 km/s)** | **9.6% propellant uplift** | exp(4.55/49) = 1.096 |
| **Mass penalty for inclination-change Δv (chemical-trim Isp=450s, ve=4.41 km/s)** | **177% propellant uplift** | exp(4.55/4.41) = 2.78 |

### Pre-registered hypothesis verdicts (per SCOPE H1-H6)

| # | Pre-registered (per SCOPE) | BOE central prediction (this STUDY) | Falsification band | Predicted verdict |
|---|---|---|---|---|
| H1 | Bag-armour alone, per-pass impact-prob ≥ 50% | armour does not change impact bound; armour-only stays at 86.5% per pass at zone-avg τ=2 with i=90° | falsified if armour drops P_impact to ≤ 5% | **HOLD-strong** |
| H2 | Cull-mesh alone, flux reduction ≤ 30% (P_impact ≥ 65%) | mesh removes ~25% (shieldable < 1cm fraction); at zone-avg τ=2, i=26.7°, reduces P_impact from 98.8% to ~91% | falsified if mesh drops P_impact to ≤ 10% | **HOLD** |
| H3 | Off-plane Δv to 90° ≥ 5 km/s | 2.27 km/s one-way at apoapsis; 4.55 km/s round-trip; falls UNDER predicted 5 km/s, but ABOVE 1.5 km/s falsification floor | falsified if Δv ≤ 1.5 km/s | **WRONG-BUT-INFORMATIVE** (cost lower than predicted, impact-prob target still not reached) |
| H4 | Slow-cross-only Δv ≥ 8 km/s round-trip | per audit 1+2: H4 collapses to (a) residence-class-asymptote (~14.7 km/s round-trip per fine-structure H5, project-owner-retired) OR (b) propulsive-cost-only-no-probability-reduction. Either way the lever does not close P_impact. | falsified if slow-cross-only ≤ 3 km/s round-trip AND reduces P_impact | **HOLD** (under both audit-1 and audit-2 reframings) |
| H5 | Combined survivability (armour + mesh + inclination + slow-cross) cannot satisfy P_impact ≤ 0.01% AND mass-penalty ≤ 10% Variant-B mass | maximum-stack P_impact = 2.2% per pass at outermost 80 km × 90° × mesh; 220× short of target. NO closing combination at conservative anchors — at any τ-zone with chunks present (B3 core, dense ringlets, B-ring inner), P_impact stays ≥ 50% per pass | falsified if any combination closes both | **HOLD-strong** |
| H6 | Conjunction prob (this round closes AND aerobraking closes) < 10% under base-rate priors | aerobraking already 0/1920 cells per phoebe `a7a8456` awaiting integration → conjunction = 0 × P(this) = 0 | falsified if either round closes | **HOLD-strong (conditional on aerobraking integration)** |

### Aggregate H-bsurv-agg

The held chunk-rendezvous architecture cannot achieve B-ring per-pass impact probability ≤ 0.01% at conservative anchors. The closest closure achievable through any combination of bag-armour, cull-mesh, off-plane geometry, and slow-cross is 2.2% per pass at the chunk-sparse outermost 80 km of B-ring with maximal inclination, mesh, and armour. This is 220× short of the per-crossing target. **Survivability is dominated by a chunk-population vs safe-passage co-location problem (fine-structure H1 restated): the only B-ring locations with low enough τ for survivable crossings are the chunk-sparse outermost edge and the Cassini-Division gaps that contain no large particles.** The architecture is doubly load-bearing on this round AND R-hybrid-aerocapture-aerobraking; with the latter falsified at 0/1920 cells (phoebe `a7a8456` awaiting integration), the conjunction is structurally non-closing.

**Aggregate grading rule:** if H5 holds AND H6 holds (both expected per BOE), the held chunk-rendezvous architecture has no surviving cell at conservative anchors; project-owner decision required (retire, restate as technology-demonstrator, or open R-mission-architecture-pivot-survey).

---

## Method

### Body 1 — reproduce titan baseline

Verify titan SOI body 3 line 186: P_impact at zone-avg B-ring τ=2.0, i=26.7° = 98.85%. This anchors the round on titan's framework before sweeping levers.

### Body 2 — single-lever sweeps

For each lever L ∈ {armour, cull-mesh, inclination, slow-cross}, sweep L individually across the SCOPE-defined grid:

- **Armour**: sweep mass density ρ_a ∈ {0, 10, 50, 200} kg/m² × bag aperture A_v ∈ {50, 100, 200} m². Compute mass penalty (kg) and survival-fraction-given-impact (Whipple-shield rule of thumb: σ-ballistic-limit-particle ∝ ρ_a^(1/3) at hypervelocity, see method body 4).
- **Cull-mesh**: binary {none, 1cm-cull-mesh}. With mesh, vehicle bag sees only τ_unshieldable = 0.75 × τ_total (per fine-structure H3). Mesh mass = 5 kg/m² × A_v.
- **Inclination**: sweep i ∈ {26.7°, 45°, 60°, 75°, 90°}. Compute Δv at apoapsis (2 × v_apo × sin(Δi/2)) and at periapsis (2 × v_p × sin(Δi/2)). Mass penalty via mass-ratio for Variant B (Isp=5000s) and chemical (Isp=450s).
- **Slow-cross**: Per audit 1, this lever does not change P_impact. Two interpretations evaluated: (a) slow vehicle's tangential velocity in Saturn frame to {5, 10, 15} km/s, compute resulting v_rel-to-ring-particle and round-trip Δv; (b) slow vehicle to ring-orbit-match (residence-class), compute Δv. Per-impact KE calculated for each.

### Body 3 — combined sweep (4D grid)

Grid: armour ∈ {0, 50, 200} kg/m² × cull-mesh ∈ {none, 1cm} × inclination ∈ {26.7°, 60°, 90°} × τ-zone ∈ {2.0 zone-avg, 0.10 outer-200km, 0.03 outermost-80km, 0.001 Huygens-gap}.

For each cell compute:
1. Per-pass P_impact = 1 - exp(-τ_eff × csc(i)) where τ_eff = (mesh_factor) × τ_zone with mesh_factor = 0.75 if mesh else 1.0.
2. Mission P_impact = 1 - (1-P_per_pass)² (two B-ring crossings: inbound rendezvous + outbound).
3. Mass penalty as fraction of Variant-B mass budget (anchor 100 t bag/tug/payload baseline).
4. Closure verdict: passes if mission P_impact ≤ 1 - (1 - 10⁻⁴)² ≈ 2×10⁻⁴ AND mass-penalty fraction ≤ 0.10.

Also tag chunk-availability for each τ-zone (per fine-structure H1: zone-avg ≥ 0.3 in chunk-rich regions; outermost 80 km has τ=0.03 but is chunk-sparse; Huygens Gap τ=0.001 has no large particles).

### Body 4 — armour ballistic limit (Whipple-shield rule of thumb)

Single-layer aluminum bumper Whipple-shield ballistic-limit equation (Christiansen 2003, NASA-TM-2003-211930, eq. 4):

    d_crit = 5.24 × (ρ_a × t_b)^(1/3) × (v_n × ρ_p^(-1/2))^(-2/3)    [cm]

For multi-layer Whipple (typical micrometeoroid shielding), the ballistic limit roughly scales with (areal mass)^(1/3). For ρ_a = 50 kg/m², ballistic-limit-particle diameter at v_n = 6.6 km/s (HE-graze residual relative velocity) ≈ 0.5-1 cm depending on bumper config. Particles > ballistic-limit penetrate.

Simplified survivability metric: P(survive given impact) = fraction of unshieldable τ that the armour does NOT block. For mesh + armour stack, both shieldable (< 1 cm) and partially-shieldable (1-5 cm at 50 kg/m² armour) are blocked; meter-class chunks always penetrate.

### Body 5 — chunk-availability tagging

Per fine-structure H1 verdict:
- B3 core (107,000 km, τ=4.5): chunk-rich (highest density); P_impact at i=26.7° = 100%.
- B-ring outer 580 km (117,000 km, τ=0.4): chunk-rich at edge of dense region; P_impact at i=26.7° = 59%.
- B-ring outermost 180 km (117,400 km, τ=0.10): chunk-thin (drift from inner B-ring); P_impact at i=26.7° = 20%.
- B-ring outermost 80 km (117,500 km, τ=0.03): chunk-sparse (very few large particles); P_impact at i=26.7° = 6.5%.
- Cassini-Division gaps (Huygens 117,680 km, τ=0.001): NO LARGE PARTICLES per fine-structure H2; P_impact = 0.22% at i=26.7°.

Closure must satisfy BOTH: P_impact at zone ≤ 0.01% per pass AND chunks available at zone.

### Body 6 — reading-level decision

Tabulate H1-H6 verdicts. If H5 holds (no closing combination), decision returns to project owner under H6's conjunction framing. Surface follow-on rounds candidate list.

---

## Out of scope

Per SCOPE worker-assignment notes:
- Returning to residence-class ram-scoop architecture (project-owner-retired per axis 19).
- Optimism about τ < 2 at the rendezvous radius (fine-structure H1 confirmed B-ring proper has no τ ≤ 0.01 sub-feature).

Phoebe-added out-of-scope:
- Reframing the rendezvous radius from 100,000 km (B-ring outer) to a different ring or a Saturn moon — that's a different architecture (R-mission-architecture-pivot-survey territory).
- Re-deriving the L0-10 per-crossing allocation; use the SCOPE's 10⁻⁴ as conservative target.
- Aerobraking integration: phoebe `a7a8456` carries that result, integration awaits orchestrator. This round assumes the aerobraking finding stands but flags H6 as conditional.

---

## Reading template (worker fills after run.py)

- **Hypotheses adjudicated.** Verdict per H1..H6 (held / falsified / held-with-margin / falsified-at-magnitude / wrong-but-informative). Predicted vs measured numeric range for each.
- **Headline.** One-line summary on whether engineered survivability closes the impact-prob target inside the mass budget.
- **Reading.** Reading-level decision the project-owner needs.
- **Cross-learning.** Relationship to R-chunk-as-heat-shield-revisit, R-hybrid-aerocapture-aerobraking; what this round teaches about engineered-survivability-in-hostile-particle-environments more generally.
- **Next-round candidates.** Follow-on questions surfaced by the result.
