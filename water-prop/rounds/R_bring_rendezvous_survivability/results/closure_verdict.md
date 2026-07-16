# R-bring-rendezvous-survivability — closure verdict

**Round:** R-bring-rendezvous-survivability
**Worker:** phoebe
**Date:** 2026-05-15 (latest+8 → +9)
**Pre-registration:** `STUDY.md`
**Sweep results:** `R_bring_rendezvous_survivability.json`

---

## Headline

**Engineered survivability does not close the B-ring rendezvous impact-prob target at any cell.** Across 162 swept cells (9 τ-zones × 3 armour densities × 2 mesh states × 3 inclinations), 0 cells satisfy per-pass impact probability ≤ 0.01%. The lowest P_impact achievable in any zone with chunks present is **7.23% per pass** (B-ring outermost 180 km × 90° inclination × cull-mesh), 723× short of the per-crossing target. The lowest P_impact anywhere is 0.075% per pass at the Huygens Gap, but the Huygens Gap contains no large particles (per fine-structure H1+H2 verdict). The architecture is doubly load-bearing on this round AND R-hybrid-aerocapture-aerobraking; with the latter falsified at 0/1920 cells (phoebe `a7a8456` awaiting integration), the conjunction is structurally non-closing.

---

## Hypotheses adjudicated

| H# | Pre-registered prediction | BOE central prediction | Measured | Verdict |
|---|---|---|---|---|
| H-bsurv-1 | Bag-armour alone, P_impact ≥ 50% | armour does not change P_impact (geometric); stays at zone-baseline | armour-only at zone-avg τ=2, i=26.7°: P_impact = 98.83% (unchanged across 0–200 kg/m²) | **HOLD-strong** |
| H-bsurv-2 | Cull-mesh alone, flux reduction ≤ 30% (P_impact ≥ 65%) | mesh removes shieldable 25%; at zone-avg τ=2, i=26.7°: P_impact drops 98.83% → 91.16% | mesh-only zone-avg i=26.7°: P_impact = 91.18% (≥ 65% threshold met) | **HOLD** |
| H-bsurv-3 | Off-plane Δv to 90° ≥ 5 km/s (round-trip framing implied) | 4.55 km/s round-trip at apoapsis (BOE under predicted band but above 1.5 km/s falsification floor) | round-trip at apoapsis: 4.55 km/s; 9.7% propellant uplift on 264-t baseline | **WRONG-BUT-INFORMATIVE** (cost lower than predicted; mass penalty manageable; impact-prob target still not reached) |
| H-bsurv-4 | Slow-cross-only Δv ≥ 8 km/s round-trip | per audit 1+2: lever does not change P_impact; minimum vehicle-to-particle v_rel without ring-match is 9 km/s (at v_target ≈ 17.5 km/s in Saturn frame, where in-plane component matches ring); at 15 km/s and below, v_rel rises again | minimum v_rel = 9.07 km/s at v_target = 15 km/s; Δv to slow ≥ 13 km/s round-trip; ring-orbit-match (residence) requires 14.0 km/s round-trip and v_rel = 0.01 km/s | **HOLD** (in two independent forms) |
| H-bsurv-5 | No combination of (armour × mesh × inclination × slow-cross) closes both P_impact ≤ 0.01% AND mass-penalty ≤ 10% Variant-B | maximum-stack at outermost 180 km + mesh + 90° + armour: P_per_pass ≈ 7.2%, 720× short | 0 of 162 cells close P_impact target. Best with chunks present: B-ring outermost 180 km × 90° × mesh: P_per_pass = 7.23% (penalty fraction 9.91% — at the edge of mass budget but useless given P_impact failure) | **HOLD-strong** |
| H-bsurv-6 | Conjunction prob (this round closes AND aerobraking closes) < 10% under base-rate priors | aerobraking 0/1920 cells per phoebe `a7a8456` → conjunction = 0 | this round 0/162 closes; conjunction = 0 × 0 = 0 | **HOLD-strong (conditional on aerobraking integration)** |

---

## Aggregate verdict — H-bsurv-agg

**HELD-strong.** The held chunk-rendezvous architecture cannot achieve B-ring per-pass impact probability ≤ 0.01% at conservative anchors. No combination of bag-armour, particle-cull mesh, off-plane geometry, or slow-cross approach closes the impact-prob target. The fundamental obstruction is the **chunk-population vs safe-passage co-location problem** (fine-structure H1+H2 restated as a survivability constraint): the only B-ring locations with low enough τ for survivable crossings are the chunk-sparse outermost edge and the Cassini-Division gaps that contain no large particles. Where chunks live (B-ring τ ≥ 0.30), per-pass impact probability stays ≥ 20% even at 90° inclination with cull-mesh.

---

## Closure stats from the 162-cell combined sweep

| Closure metric | Count | Notes |
|---|---|---|
| Total cells | 162 | 9 τ-zones × 3 armour × 2 mesh × 3 inclinations |
| Cells closing P_impact ≤ 2×10⁻⁴ (two-crossing target) | **0** | |
| Cells closing P_impact AND chunks present | **0** | tighter constraint, same answer |
| Cells closing all three (P_impact + mass + chunks) | **0** | |
| Lowest P_impact ANY cell (zone, lever stack) | 0.075% per pass | Huygens Gap × 90° × mesh — chunk count = none |
| Lowest P_impact CHUNK-PRESENT cell | **7.23% per pass** | B-ring outermost 180 km × 90° × mesh; 723× target |
| Lowest in chunk-rich zone (τ ≥ 0.30 with chunks) | **20.1% per pass** | Huygens Ringlet × 90° × mesh |

---

## Slow-cross findings (audit 2 confirmed by data)

The SCOPE's H4 framing assumed slowing the vehicle in the Saturn frame would monotonically reduce vehicle-to-ring-particle relative velocity. The data shows a non-monotonic minimum:

| Vehicle v_target (Saturn frame) | v_rel to ring particle | Δv round-trip from capture orbit | Per-impact KE for 1cm particle |
|---|---|---|---|
| 26.48 km/s (no slow, capture orbit) | 12.61 km/s | 0.0 km/s | 119 kJ |
| 20.00 km/s | **9.13 km/s** | 13.0 km/s | 63 kJ |
| 15.00 km/s | 9.07 km/s | 23.0 km/s | 62 kJ |
| 10.00 km/s | 11.46 km/s | 33.0 km/s | 98 kJ |
| 5.00 km/s | 15.18 km/s | 43.0 km/s | 173 kJ |
| 19.48 km/s = ring-match (residence) | **0.010 km/s** | 14.0 km/s | 0.0001 kJ |

Two regimes:
- **Slowing without ring-match.** v_rel bottoms at ~9 km/s (when vehicle's in-plane prograde component aligns with ring orbital speed). Below v ≈ 17.5 km/s, v_rel rises again because vehicle becomes sub-ring; out-of-plane component still contributes 11.9 km/s minimum (the inclination-driven cross-track component). Per-impact KE for 1cm particle stays in 60–170 kJ range — vastly above Whipple ballistic limit (~10 kJ for cm-scale at 6.6 km/s on 50 kg/m² armour).
- **Ring-orbit-match (residence).** v_rel collapses to dispersion-class 10 m/s, per-impact KE drops to 0.0001 kJ (non-fatal). But this IS the project-owner-retired residence-class architecture (axis 19, fine-structure H5: 14.7 km/s round-trip Saturn-side Δv).

The audit-1 conclusion holds either way: P_impact is geometric and unchanged by slowing. Slowing only lowers per-impact KE (a survival-given-impact lever), and the only slow-cross that achieves non-fatal per-impact KE is residence-match itself.

---

## Inclination-change findings (audit 4 confirmed by data)

Computing Edelbaum impulsive-equivalent at apoapsis (the cheapest place for an elliptical-orbit plane change) gives Δv_round_trip across the inclination sweep:

| Target inclination | Δv round-trip (apoapsis burn) | Propellant @ Variant-B Isp 5000 s | % of 264-t baseline | P_impact at zone-avg τ=2 | P_impact at outermost 180 km | P_impact at outermost 80 km |
|---|---|---|---|---|---|---|
| 26.7° (Hohmann, no plane change) | 0 km/s | 0 t | 0% | 98.83% | 19.95% | 6.46% |
| 45° | 1.38 km/s | 7.5 t | 2.9% | 94.09% | 13.19% | 4.15% |
| 60° | 2.48 km/s | 13.7 t | 5.2% | 90.07% | 10.91% | 3.40% |
| 75° | 3.55 km/s | 19.8 t | 7.5% | 87.39% | 9.83% | 3.06% |
| 90° (max csc(i) reduction) | 4.55 km/s | 25.7 t | 9.7% | 86.47% | 9.52% | 2.96% |

The propulsive cost is well-bounded (< 10% of baseline mass for full 90° flip), so audit 4's prediction holds: H3's "≥ 5 km/s" prediction is wrong (actual ~4.5 km/s round-trip), but the more important finding is that inclination cannot rescue the round — at 90° with B-ring outermost 180 km × mesh, P_per_pass = 7.2%, two-crossing P = 13.9%, still 720× the target.

---

## Reading

**The held chunk-rendezvous architecture has no surviving cell at conservative anchors when both load-bearing engineering rounds are integrated.**

Phoebe's two consecutive rounds adjudicate the two engineering questions on the held architecture:

1. **R-hybrid-aerocapture-aerobraking (commit `a7a8456`, awaiting orchestrator integration):** atmospheric capture falsified at 0 of 1920 cells. Three independent failure modes (chunk shatter, aerobraking timescale unphysical at thermally-survivable altitudes, sublimation consuming chunk at timescale-tractable altitudes).

2. **R-bring-rendezvous-survivability (this round):** B-ring crossing survivability falsified at 0 of 162 cells. Fundamental obstruction is the chunk-population vs safe-passage co-location problem — the only safe-passage zones are the chunk-sparse outermost B-ring edge and the chunk-empty Cassini-Division gaps.

Both are necessary. Both fail. The conjunction is structurally non-closing.

**Project-owner decisions surfaced:**

1. **Should the held chunk-rendezvous architecture be retired entirely?** Both load-bearing engineering questions now answered negatively. Phoebe recommends yes; the architecture-decision-matrix's chunk-rendezvous row should be marked falsified at conservative anchors, with the fallback being either (a) restate as technology-demonstrator (rhea-bake-off path 2), (b) re-open R-mission-architecture-pivot-survey (catcher / processor / lower-energy trajectory), or (c) accept residence-class architecture's 14.7 km/s Saturn-side Δv penalty (project-owner-retired path resurrected under L0-05 waiver).

2. **Is the matrix's "chunk-rendezvous-engineering-pending" framing now retired?** Phoebe recommends yes; both engineering questions are now answered. Reframe to "chunk-rendezvous-falsified-without-architecture-pivot".

3. **Should the project-owner decisions phoebe surfaced from R-hybrid-aerocapture-aerobraking (decisions 1–4 in `STATE.md`) be addressed before opening any new architectural rounds?** Phoebe recommends yes; the matrix needs reconciliation with the now-completed engineering-survivability adjudication before new architectural search begins.

4. **Should the cull-mesh-and-armour mass models from this round be promoted to a campaign-shared utility?** Single-bumper Whipple ballistic-limit (Christiansen 2003) and 5-kg/m² mesh anchors will likely recur in any architecture that involves close-approach to ring or moon-surface debris. Recommend extracting to `water-prop/src/`.

---

## Cross-learning

1. **Geometric-impact-probability framework is velocity-transparent — write this into PROTOCOL or shared utility.** Phoebe's audit 1 caught a SCOPE input-assumption error (slow-cross framed as a probability-reduction lever) that's likely to recur. Any future round that touches "ring crossings", "atmospheric particle flux", "debris field" should distinguish (a) per-pass intercept probability (geometric) from (b) per-impact survival fraction (kinetic). The two have different levers and different functional forms.

2. **Chunk-population vs safe-passage co-location is the binding constraint, not just the per-pass probability.** Fine-structure H1+H2 already named this; this round operationalises it as a survivability hard-constraint. Any architectural recovery via "find a safer crossing zone" must demonstrate chunks ARE in the zone — the dust gaps and outer edges are empty by the same physics that makes them safe.

3. **Phoebe's two-round arc on the held architecture both used the same methodology pattern (lesson 9 SCOPE audit → BOE central anchor → range-band wrap → run, then 5-section reading).** Two consecutive rounds on different physics (aerocapture-thermal-structural and ring-particle-flux) both produced 0-cell-closure verdicts. The pattern is robust enough to be a campaign default. Worth a PROTOCOL footnote.

4. **The Whipple-shield ballistic limit at 6.6 km/s relative velocity is severely undersized for B-ring particle distribution.** Even 200 kg/m² multi-layer Whipple shields stop only ~1 cm particles at hypervelocity; per fine-structure H3, 75% of B-ring τ is in particles > 1 cm. The Whipple-shield-only architecture is mismatched to the threat. Real ICEBERG would need either residence-velocity (no hypervelocity at all) or armour mass-densities so high they consume the entire mass budget — neither closes.

---

## Next-round candidates

If the project owner accepts both engineering rounds as falsifying the held chunk-rendezvous architecture:

- **R-mission-architecture-pivot-survey** (priority: critical-path) — what alternative architectures remain after chunk-rendezvous and ram-scoop-residence are both retired? Catcher (chunk delivered to a Saturn-orbit catcher then transferred), processor-at-Saturn (electrolyse on-station before Earth return), lower-energy-trajectory (ballistic-capture, gravity-assist tour of inner moons), small-source (Mimas-instead-of-B-ring, Phoebe-instead-of-Saturn) — each needs first-pass architecture and Δv accounting.
- **R-program-class-reframe-2** (priority: critical-path) — meta-round on L0-05 relaxation (≥ 25-yr round-trip waiver opens Architecture E without Saturn-side electrolysis, per enceladus-r5 R-architecture-E-no-saturn-side-electrolysis). Phoebe's two engineering rounds raise the bar: now the question is not just "can we accept a longer mission", but "is there a 14-yr mission at all that closes given engineering constraints"?
- **R-deployable-drag-skirt** (priority: high) — reverted from phoebe `a7a8456`'s recommendation list. Was named as the only architecturally-credible β-reduction lever for atmospheric capture. With both engineering rounds now closed-negative, drag-skirt is also reframed as a technology-demonstrator candidate, not a Variant-B-rescue path.

If the project owner rejects either engineering round as too pessimistic:

- **R-bag-armour-multi-layer-deep** — re-do this round's H1 with deeper Whipple-shield modelling (multi-bumper, mesh-bumper-mesh, fluid-filled honeycomb, self-healing elastomer). Plausibly survival-fraction-given-impact rises but the underlying P_impact is unchanged; round would need to argue some hits are non-fatal even at large-particle scale.
- **R-bring-fine-structure-deep** — re-anchor on Cassini UVIS deep occultation profiles to look for chunk-bearing sub-features the radial-zone-average measurements miss. Fine-structure H1 already did this at km-scale resolution; deeper would need 100-m-resolution data.
- **R-lower-inclination-arrival** — inverse direction: instead of going to 90° (which doesn't help enough), what if arrival inclination drops below 26.7° via heliocentric trajectory shaping? csc(i) approaches infinity as i→0, so this DOESN'T help — but a worker should formally close it.

---

## Notes for orchestrator integration

- Worker session: phoebe (continued, 4th round shipped on `iceberg-phoebe`).
- Phoebe is now 2 ahead of `origin/main` (commits `a7a8456` R-hybrid-aerocapture-aerobraking + this round). Both await orchestrator integration.
- This round's verdict is **conditional on the aerobraking-round result also being accepted**. If orchestrator rejects `a7a8456` for any reason, H6 of this round needs to be re-evaluated.
- Methodology lessons reinforced (no new lessons surfaced — all four audit issues caught match phoebe lesson 9's pattern; all five BOE central anchors landed within the run.py output range; audit 4's "wrong-but-informative" prediction landed exactly).
- Suggested matrix amendment: in axis 19 (Capture architecture), mark "chunk-rendezvous via B-ring atmospheric or particle-flux engineering" as falsified at conservative anchors.
