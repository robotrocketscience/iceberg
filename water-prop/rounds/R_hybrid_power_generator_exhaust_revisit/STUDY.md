# R-hybrid-power-generator-exhaust-revisit — STUDY

**Worker:** enceladus-r5, 2026-05-16. **Status:** complete. **Predecessor:** R-hybrid-chemical-power-augmentation (commit `98a9ded` on `iceberg-enceladus-r5`).

## Why this round exists

The predecessor round asserted that gas-generator exhaust is thrust-neutral and reduced the architecture to a single-stream Tsiolkovsky with a parasitic-mass dv tax (~97.6 percent of v_e wasted per kg hydrolox). **That assumption is structurally pessimistic and physically wrong** — the exhaust must go somewhere, and venting it through a vacuum-expansion nozzle along the thrust axis is strictly better than perpendicular venting. This round runs the correct two-stream rocket equation.

## Two-stream physics

Energy partition: 1 kg hydrolox × LHV 13.4 MJ/kg = η_gen × LHV (electrical, drives water-electric thrust) + (1 − η_gen) × LHV (thermal, expanded through gas-generator outlet nozzle).

- **Water stream:** `v_e_water = Isp × g0 = 19,613 m/s` at Isp 2000 s.
- **Hydrolox stream:** `v_e_hydrolox = sqrt(2 × (1 − η_gen) × LHV × η_nozzle)` = 3375 m/s at η_gen=0.5, 4773 m/s at η_gen=0.0 (η_nozzle=0.85).

Two-stream constant-rate-consumption Tsiolkovsky reduces to a mass-flow-weighted average exhaust velocity: `dv = v_e_effective × ln(m_0 / m_f)` with `v_e_effective = (M_water × v_e_w + M_hydrolox × v_e_h) / (M_water + M_hydrolox)`.

Per kg hydrolox impulse contribution (relative comparison at η_gen=0.5, η_thr=0.5, Isp 2000 s):
- Via electric route: `2 × η_thr × η_gen × LHV / v_e_w` = **479 N·s/kg**
- Via chemical exhaust: `v_e_hydrolox` = **3375 N·s/kg**

The chemical route is **~7× larger** than the electric route. The predecessor round entirely missed this.

## Other revised anchors (this round)

- **η_thruster** revised from 0.7 (Hall-class) → **0.5** (water-electric MET / arcjet class). Predecessor was optimistic.
- **bus_class** swept: "full" (15 t bus + 8 t bag = 23 t, predecessor anchor) and "demo" (5 t bus + 2 t bag = 7 t, demonstrator-class anchor). Predecessor used only full.
- **η_gen** sweep extended to include 0.0 (pure chemical, no electricity extracted) to bracket the limit.

## Pre-registered hypotheses and grades

| # | Hypothesis | Verdict | Notes |
|---|---|---|---|
| H1 | At P=10 kWe + chunk=50 + aero=10 + full bus, some M_h closes waiver | **FALSIFIED** | 0 of 28 cells all-pass. Hydrolox augmentation does not rescue the 10-kWe reactor-life cap. |
| H2 | At P=10 kWe + chunk=200 + η=0.5, no L0-05-strict all-pass closure | **HELD** | 0 of 28 cells close strict. Corroborates predecessor at higher rigor. |
| H3 | Optimal η_gen for delivered mass is interior (in (0, 0.5)) | **FALSIFIED** | All 4 tested (P, chunk, M_h) corners show optimum at η_gen=0.0 (pure chemical) — interior optimum hypothesis wrong; the chemical-thrust contribution always dominates the electric-route contribution at v_e_w=19,613 m/s. |
| H4 | Demonstrator-class (chunk≤10, demo bus, aero=10): some closure | **FALSIFIED** | 0 of 168 cells all-pass. Chunk 5-10 t is too small to push even demo-bus dry mass through 15 km/s propulsive dv at any v_e_eff. |
| H5 | At 200-t chunk + 10 kWe, hybrid still fails L0-05 strict | **HELD** | 0 of 84 cells all-pass strict. Corroborated. |
| H6 | Prior-round "M_h=0 strictly dominates" is FALSIFIED at two-stream physics | **FALSIFIED** | M_h=0 still dominates in delivered chunk mass at every tested (P, chunk, η_gen, aero) corner. The two-stream correction is quantitatively significant (~10× more dv per kg hydrolox) but qualitatively does not change the verdict. |

**Score: 2 HELD (H2, H5) + 4 FALSIFIED (H1, H3, H4, H6).** Four falsifications are *informative* — they reveal that the two-stream physics correction, while real, does not flip the architectural verdict. The architecture remains net-harmful with hydrolox augmentation.

## Headline architectural verdict

**The two-stream rocket-equation correction does not rescue the project-owner's hybrid-power proposal.** Hydrolox augmentation continues to be strictly net-harmful for delivered chunk mass at the dv ≈ 15 km/s propulsive envelope (25 km/s CT inbound − 10 km/s aerocapture credit). The reason is straightforward:

- Adding M_h drops v_e_eff (because v_e_h ≪ v_e_w by ~5×).
- Adding M_h also increases m_0 (parasitic burden) and m_dry (tank fraction 10 percent + generator mass).
- For the SAME dv requirement, the resulting mass ratio change must be larger, demanding more M_w.
- Net delivered chunk mass DECREASES monotonically in M_h at every tested corner.

The five all-pass-waiver cells in this 5040-cell sweep are **all at 50 kWe + 50-t chunk + 10 km/s aerocapture + demo bus** — most with M_h=0 (pure-reactor demonstrator). The cells with non-zero M_h deliver less than their M_h=0 sibling.

## Two new load-bearing findings (NOT in predecessor)

### Finding 1 — bus + bag dry mass is the binding constraint

The predecessor's 23-t "full bus + bag" anchor (15 t Cassini-class bus + 8 t bag) closes **zero** cells in this sweep. The 7-t "demo bus" anchor (5 t bus + 2 t bag) closes 5. Cassini's actual bus dry mass was ~2.15 t; Europa Clipper's was ~5.9 t. **Even the 7-t demo anchor may be over-conservative.** A rigorous bus-mass anchor sweep is the natural next round.

### Finding 2 — dv-regime hardcoding is also load-bearing

This sweep uses CT inbound dv = 25 km/s uniformly. That is appropriate for water-electric-dominated thrust (low T/W) but inappropriate for chemical-dominated thrust (high T/W → impulsive). At η_gen=0 with high M_h, the architecture IS effectively chemical inbound, for which the matrix's impulsive dv = 6.42 km/s is the right number. **Applying CT dv to chemical-dominated cells over-penalises them by approximately 4×.** This is the same dv-regime asymmetry that R-matrix-dv-regime-consistency (R15) flagged for the broader matrix.

Resolving Finding 2 would require: (a) per-cell dv selection based on instantaneous T/W ratio over the burn (hard); or (b) sweep over dv ∈ {6.42, 15, 25} km/s as a sensitivity (easier). At dv_required = 0 with aerocapture 10 km/s (i.e., 6.42 − 10 < 0, full aerocapture), the chemical case trivially closes — but phoebe's R-chunk-as-heat-shield-revisit has already established that full inbound aerocapture is structurally infeasible.

## What this implies for the architecture matrix

1. **Predecessor's "FALSIFIED-STRUCTURAL" verdict for hybrid power-augmentation stands** — the two-stream correction does not rescue it. Matrix should still carry the row as falsified, but the **mechanism citation should switch** from "parasitic-mass dv tax" (predecessor) to "two-stream effective-v_e degradation under CT dv requirement" (this round). The earlier citation is internally consistent with the predecessor's pessimal-exhaust assumption but is not the operative mechanism in the corrected physics.

2. **A new architecture line opens:** sub-megawatt pure-reactor + demonstrator-class bus + aerocapture. 50 kWe + 50-t chunk + 10 km/s aero + 7-t bus delivers 13.92 t at RT 15.80 yr (waiver-class). This is consistent with R-architecture-E demonstrator scope but at a tighter mass budget than R-architecture-E used. **R-architecture-E should be revisited with the lighter bus anchor.**

3. **dv-regime selection across hybrid architectures needs a uniform protocol.** Matrix has now flagged this three times: R15 (Variant B vs Arch E inbound dv asymmetry), R16 (Variant B chemical-inbound 837-t hydrolox requirement at impulsive), and this round (chemical-thrust-dominated cells over-penalised by CT-only modelling). Suggested protocol: select dv per-cell based on dominant thrust source.

## Methodology / recurring-lesson tracker

- **Recurring lesson 10 filed (NEW).** Pre-registering a hypothesis that says "prior-round verdict is FALSIFIED" is risky if the prior verdict's *direction* was correct but its *magnitude* was wrong. H6 fell because the predecessor's qualitative answer ("hydrolox net-harmful") was right; only its quantitative justification was incomplete. Future protocol: distinguish "rejecting prior verdict" from "tightening prior verdict's mechanism" at pre-registration time.
- **No R7 strikes filed.** Two-stream rocket-equation derivation matched closed-form analytic prediction (per-kg-hydrolox impulse 3375 N·s vs 479 N·s for chemical vs electric route) within 1% at the η_gen=0.5 / Isp 2000 s anchor.

## Files of record

```
water-prop/rounds/R_hybrid_power_generator_exhaust_revisit/STUDY.md           (this file)
water-prop/rounds/R_hybrid_power_generator_exhaust_revisit/run.py
water-prop/rounds/R_hybrid_power_generator_exhaust_revisit/results/tables.md
water-prop/rounds/R_hybrid_power_generator_exhaust_revisit/results/results.json
```

## Threads spawned

- **R-bus-mass-anchor-sweep** — bus + bag dry mass appears load-bearing for ICEBERG demonstrator-class cells. Predecessor's 23-t anchor was high vs Cassini's 2.15 t / Europa Clipper's 5.9 t. Sweep m_dry across [2, 25] t and quantify how many cells open at each anchor.
- **R-dv-regime-per-cell** — chemical-thrust-dominated cells are over-penalised by CT-only dv modelling. Implement per-cell dv selection or sensitivity sweep over dv ∈ {6.42, 15, 25} km/s.
- **R-architecture-E-light-bus-revisit** — re-run architecture-E with bus + bag at 7 t (demonstrator-class anchor) rather than 23 t (full bus). May open additional sub-megawatt cells.
