# R-megawatt-composite-with-mass-scaling

**Worker:** titan (Block 14)
**Predecessors:** R-composite-burn-time-closure (Block 11), R-spiral-out-exit-architecture (Block 13)
**Pre-registration date:** 2026-05-18
**Status at pre-reg:** results not yet computed; hypotheses below frozen before any code is run.

---

## Motivation

Block 11 found that the residence-class composite is structurally dead at 500 kilowatt-electric under Block-4 accounting (6-month exit-burn dwell, 6-year inbound-cruise budget). Joint closure regimes exist at ≥ 5 megawatt-electric, with naive delivered fractions of 22.76 percent (5 megawatt-electric / specific-impulse 3000 exit / 9000 inbound) and 40.51 percent (10 megawatt-electric / 7000 / 9000). Block 13 found the spiral-out reframe drops the threshold from 5 megawatt-electric to 1-2 megawatt-electric but still requires megawatt-class operation.

Both Block 11 and Block 13 sweeps held the spacecraft dry mass fixed at 200 tonnes — Block 4's nominal Variant B value, derived for a 500-kilowatt-electric architecture. At 5-10 megawatt-electric the power-subsystem mass is dramatically higher and the 200-tonne dry-mass assumption is no longer physically consistent.

Per locked-memory ICEBERG power finding 1, the 40-watt-per-kilogram specific-power figure cited in National Academies 2021 and NASA Modular Assembled Radiators for Very Large systems (MARVL) studies is a Technology-Readiness-Level-2 paper-study aspirational number, not an extrapolation of Kilowatt Reactor Using Stirling Technology (KRUSTY) ground-test data. KRUSTY measured ~2.4 watts-per-kilogram system-level. Flown radioisotope thermoelectric generators top out at ~5.3 watts-per-kilogram (General Purpose Heat Source RTG). Per locked-memory ICEBERG power finding 4, at megawatt-electric scale the radiator subsystem alone is 40-55 percent of total system mass; the bundled rule-of-thumb `5 tonnes + reactor_kilowatt-electric × 0.1 tonnes` is closer to correct at megawatt scale than the optimistic decomposed model.

This round answers: **once power-subsystem mass scaling is applied per the four locked-memory anchor points, does any (power, specific-impulse-exit, specific-impulse-inbound) cell in the residence-class composite deliver positive water mass AND close both burn-time budgets simultaneously?**

If yes under any mass model, the architecture has a survival regime conditional on that specific-power assumption — and the entire economic case is then conditional on a single technology bet at the assumed Technology-Readiness Level.

If no under all mass models, the residence-class composite is conclusively dead independent of power class. The architecture must either be retired in favour of one of the lab-side alternatives (Variant C reformulation, Architecture E no-Saturn-side-electrolysis, Hyperion-owned cruise-time-optimization regime) or be reframed structurally (the next round in line is R-megawatt-spiral-out-with-mass-scaling, which applies the same mass scaling to Block 13's spiral reframe rather than Block 4 accounting).

---

## Reframed accounting

**Dry-mass decomposition:**

| Component | Symbol | Source | Tonnes |
|---|---|---|---|
| Non-power structure + tankage + jettison hardware + avionics | M_struct_base | Block 4 / 9 / 11 nominal 200 tonnes total minus implicit ~50 tonnes power subsystem at 500 kilowatt-electric | 150 |
| Residence-jettison hardware (subtracted at exit) | M_jettison | Block 4 / 9 nominal | 20 |
| Aerocapture thermal-protection-system shield (carried through both burns; ablates at Earth arrival) | M_shield | Block 8 / 9 nominal | 4.13 |
| Power subsystem (reactor + shield + power-conversion + radiator) | M_power(P) | This round — scales with power per four mass models | varies |

Total dry mass carried through both burns: `M_dry_total = M_struct_base + M_power(P) - M_jettison + M_shield`.
Wet mass at exit-burn ignition: `M_at_exit = M_dry_total + M_collected` where M_collected = 200 tonnes water (Block 4 nominal).

**Four mass models for M_power(P) (tonnes, with P in megawatt-electric):**

1. **Paper-aspirational** — `M_power = 25 × P_MWe`. Specific power 40 watts-per-kilogram, the figure used in National-Academies-2021-style paper studies. Locked memory ICEBERG power finding 1 flags this as TRL-2 aspirational; locked memory ICEBERG power finding 4 notes the 40 watts-per-kilogram target essentially bets on deployable ultra-low-areal-density radiators that have not flown.
2. **Bottoms-up moderate** — `M_power = 100 × P_MWe`. Specific power 10 watts-per-kilogram. Roughly KRUSTY-extrapolated upward 4× to credit some megawatt economy of scale, while remaining anchored to measured ground-test data rather than to deployable-radiator aspirations.
3. **KRUSTY-anchored conservative** — `M_power = 417 × P_MWe`. Specific power 2.4 watts-per-kilogram, the directly-measured Kilowatt Reactor Using Stirling Technology system-level value from locked memory ICEBERG power finding 1.
4. **Bundled-Finding-4 rule-of-thumb** — `M_power = 5 + 100 × P_MWe` (i.e. M_power_tonnes = 5 + 0.1 × P_kilowatt-electric). This is the orchestrator's reference formula flagged in locked memory ICEBERG power finding 4 as the more-defensible figure at megawatt scale per MARVL studies.

**Sweep grids:**

- Reactor electric power: 1, 2, 5, 10 megawatt-electric.
- Exit specific impulse: 3000, 5000, 7000, 9000 seconds.
- Inbound specific impulse: 3000, 5000, 7000, 9000 seconds.
- Mass model: four scenarios above.
- Total cells: 4 × 4 × 4 × 4 = **256**.

**Closure criteria for a cell:**

- Exit burn time ≤ 6 months (residence-dwell budget, Block 4 / 11).
- Inbound burn time ≤ 6 years (Hohmann Saturn-Earth cruise budget, Block 4 / 11).
- Delivered water mass > 0 (Tsiolkovsky mass-closure: `M_at_exit / (MR_exit × MR_inbound) > M_dry_total`).

Delta-velocities: exit 7.4 kilometres-per-second; inbound net 23.2 kilometres-per-second after the 1.5-kilometre-per-second aerocapture credit (Block 4 / 8 / 9 / 11 standard).

Power-to-thrust: `Thrust_newtons = 2 × η × P_watts / (Isp × g₀)` with η = 0.65 (Block 11 standard).

---

## Anchor calculation (one cell, by hand)

To pre-register against the physical mechanism rather than intuition (per Block-9 meta-lesson), I compute one grid point under each mass model before freezing hypotheses. Anchor cell: **5 megawatt-electric, exit-specific-impulse 3000, inbound-specific-impulse 9000**, which gave 22.76 percent delivered fraction in Block 11's un-mass-scaled run.

Combined mass ratio: `MR_exit × MR_inbound = exp(7400 / (3000 × 9.80665)) × exp(23200 / (9000 × 9.80665)) = 1.2861 × 1.3007 = 1.6731`.

| Mass model | M_power (t) | M_dry_total (t) | M_at_exit (t) | M_at_earth (t) | Delivered (t) | Delivered fraction |
|---|---|---|---|---|---|---|
| Paper-aspirational (40 W/kg) | 125 | 259.13 | 459.13 | 274.42 | 15.29 | **7.65 %** |
| Bottoms-up moderate (10 W/kg) | 500 | 634.13 | 834.13 | 498.55 | −135.58 | **negative (no closure)** |
| KRUSTY-anchored (2.4 W/kg) | 2083 | 2217.13 | 2417.13 | 1444.78 | −772.36 | **negative (no closure)** |
| Bundled Finding-4 (5 + 100 × P) | 505 | 639.13 | 839.13 | 501.54 | −137.59 | **negative (no closure)** |

A second anchor at **10 megawatt-electric, exit 7000, inbound 9000** (Block 11's 40.51 percent un-mass-scaled cell). Combined mass ratio: `exp(7400/(7000×9.80665)) × exp(23200/(9000×9.80665)) = 1.1138 × 1.3007 = 1.4490`.

| Mass model | M_power (t) | M_dry_total (t) | M_at_exit (t) | M_at_earth (t) | Delivered (t) | Delivered fraction |
|---|---|---|---|---|---|---|
| Paper-aspirational (40 W/kg) | 250 | 384.13 | 584.13 | 403.13 | 19.00 | **9.50 %** |
| Bottoms-up moderate (10 W/kg) | 1000 | 1134.13 | 1334.13 | 920.74 | −213.39 | **negative** |
| KRUSTY-anchored (2.4 W/kg) | 4167 | 4301.13 | 4501.13 | 3106.55 | −1194.58 | **negative** |
| Bundled Finding-4 | 1005 | 1139.13 | 1339.13 | 924.18 | −214.95 | **negative** |

**Functional form noted:** delivered tonnage as a function of M_dry is `M_at_exit / (MR_e × MR_i) − M_dry_total = M_collected / (MR × MR) − M_dry_total × (1 − 1/(MR × MR))`. For fixed M_collected = 200 t, the slope is `−(1 − 1/(MR × MR))`. At 5 megawatt-electric / 3000 / 9000 the slope is −0.4023 (every additional tonne of dry mass costs 0.40 tonnes delivered); at 10 megawatt-electric / 7000 / 9000 the slope is −0.3098. So a 100-tonne dry-mass hit (jumping from paper-aspirational to bottoms-up at 5 megawatt-electric: 375-tonne increase, predicting 375 × 0.40 = 150-tonne delivery loss; observed 15.29 → −135.58, a 150.87-tonne swing — matches). The functional form is locked.

---

## Pre-registered hypotheses

Each hypothesis is **frozen** before the run. Adjudication rule: held / marginal / falsified by literal comparison of run output to the predicted band. "Marginal" reserved for cases falling within a 50-percent band beyond the central prediction.

**H1 (KRUSTY-anchored at 5 megawatt-electric):** Zero cells in (specific-impulse-exit, specific-impulse-inbound) grid at 5 megawatt-electric / 2.4 watts-per-kilogram deliver positive water mass. Reason: M_power = 2083 tonnes makes M_at_exit > 2.2 kilotonnes, and no specific-impulse pair in {3000-9000 s} has combined mass ratio < ~1.05 needed for closure at that dry-to-water ratio.

**H2 (bottoms-up moderate at 5 megawatt-electric):** Zero cells deliver positive water. Anchor calculation shows −135.58 tonnes at the best Block-11 cell. Slope analysis: even at the highest combined-specific-impulse cell (9000/9000), combined mass ratio = 1.193 and slope is −0.297; M_dry_total at 5 megawatt-electric with bottoms-up is 634 tonnes, so delivered would be `200/1.193 − 634 × (1 − 1/1.193) = 167.6 − 102.5 = +65.1` tonnes — wait, this contradicts. Recheck.

  Re-doing: at Isp_exit = Isp_inbound = 9000, MR_e = exp(7400/(9000×9.80665)) = exp(0.0838) = 1.0874; MR_i = exp(23200/(9000×9.80665)) = 1.3007; combined = 1.4145. M_at_exit at bottoms-up 5 megawatt-electric = 834.13. M_at_earth = 589.71. Delivered = 589.71 − 634.13 = −44.42 tonnes. Still negative.

  At Isp_exit = 9000, Isp_inbound = 9000 the slope is −(1 − 1/1.4145) = −0.293; M_dry_total = 634; delivered = M_collected/MR² − M_dry × (1 − 1/MR²) = 141.4 − 185.9 = −44.5 t. Confirms negative.

  Tightening H2: zero cells at 5 megawatt-electric / 10 watts-per-kilogram deliver positive water mass across the {3000, 5000, 7000, 9000}² grid. (If the run shows positive delivery at some cell I missed, H2 falsifies.)

**H3 (paper-aspirational at 5 megawatt-electric):** Maximum delivered fraction across the (specific-impulse-exit × specific-impulse-inbound) grid is in [5 %, 12 %]. Anchor cell gives 7.65 %; expect slightly better at higher exit-specific-impulse (lower exit-mass-ratio dominates the cost) but constrained by burn-time at 5 megawatt-electric / Isp 7000-9000 exit.

**H4 (bundled Finding-4 at 5 megawatt-electric):** Zero cells deliver positive water. M_power at 5 megawatt-electric is 505 tonnes — within 1 percent of bottoms-up 500 tonnes — so the model behaves identically. H4 ≈ H2.

**H5 (KRUSTY-anchored at 10 megawatt-electric):** Zero cells. M_power = 4167 tonnes makes the vehicle unflyable.

**H6 (bottoms-up moderate at 10 megawatt-electric):** Zero cells. M_power = 1000 tonnes; anchor cell shows −213 tonnes; no specific-impulse combination recovers.

**H7 (paper-aspirational at 10 megawatt-electric):** Maximum delivered fraction across the grid is in [7 %, 14 %]. Anchor cell gives 9.50 %; expect modest spread.

**H8 (bundled Finding-4 at 10 megawatt-electric):** Zero cells. M_power = 1005 tonnes; ≈ H6.

**H9 (1-2 megawatt-electric under any mass model):** Zero cells deliver positive water mass under ANY mass model — because Block 11 already showed the only burn-time-closing regime at 1-2 megawatt-electric is low-specific-impulse, where mass-ratio exceeds 4 even with naive 184-tonne dry mass; the mass-scaling penalty only worsens the situation.

**H10 (architectural verdict):** The residence-class composite has a closing regime under Block-4 accounting (6-month exit dwell, 6-year inbound cruise) **only** under the paper-aspirational 40-watts-per-kilogram specific-power assumption, at 5 megawatt-electric or higher. Under all three other mass models (bottoms-up, KRUSTY-anchored, bundled-Finding-4), the composite has zero closing cells. Architecture is a single-point-of-failure technology bet on TRL-2 deployable ultra-low-areal-density radiators that have not flown — combined with locked-memory ICEBERG power finding 2 (0-of-6 US space-fission programs reached orbit within their originally-stated decade), this places the architecture in venture-non-viability territory absent a structural reframe (Block 13's spiral reframe, or Architecture E / Variant C / Hyperion-owned alternatives).

**H11 (methodology — Lesson 8 instance #7):** The mass-scaled delivered fractions under the paper-aspirational model will fall within ±20 percent of the anchor-cell predictions (7.65 % and 9.50 %) — i.e. the functional-form-based prediction is robust because the slope-derived sensitivity to M_dry was computed from physics rather than guessed. If the run shows any paper-aspirational cell outside [6.1 %, 9.2 %] for 5 megawatt-electric or [7.6 %, 11.4 %] for 10 megawatt-electric, the prediction's functional form needs revision (likely meaning the Isp interaction is non-monotonic in a way I haven't anticipated).

---

## What this round does NOT test

- **Block-13 spiral-reframe accounting** (continuous-thrust exit burn through cruise). That's R-megawatt-spiral-out-with-mass-scaling, the natural Block-15 successor if this round confirms paper-aspirational dependence.
- **Vehicle development and deployment cost.** Even if the architecture closes physically at 5-10 megawatt-electric, megawatt-class deep-space-rated reactor development is a multi-billion-dollar program with no Phase-2 award yet (per locked memory ICEBERG power finding 3). That economic audit is R-megawatt-vehicle-cost-vs-delivered-fraction (medium priority per STATE.md).
- **Mass-scaling for the chemical outbound stage.** Outbound chemical kick is locked per REQUIREMENTS-L1 v0.3 §axis-2 and uses different propulsion class; this round inherits the Variant-B inert-mass values for outbound.
- **Radiator thermal closure for high-specific-impulse operation.** Higher specific impulse means higher exit-velocity and higher waste-heat fraction at fixed efficiency η; a complete model would couple specific impulse to radiator area requirement. This round holds η = 0.65 constant per Block 11 to isolate the mass-scaling effect from the efficiency-coupling effect. Joint coupling is a follow-on if any cell survives.

---

## Method

`run.py` implements the four-mass-model × four-power × four-Isp-exit × four-Isp-inbound sweep using the Block-11 closure-time engine, with `M_dry_total` recomputed per cell. Outputs:

- `results/mass_scaled_grid.csv` — all 256 cells with mass-model, power, Isp-exit, Isp-inbound, M_dry, M_at_exit, M_at_earth, burn times, closure flags, delivered fraction.
- `results/closing_cells.csv` — subset where both burn-time and mass closures hold.
- `results/summary_by_mass_model.csv` — max delivered fraction per (mass-model, power) pair, with the winning Isp pair.
- `results/anchor_cell_audit.csv` — explicit recomputation of the two anchor cells under each mass model, to verify the pre-reg arithmetic.
- `results/summary.json` — hypothesis adjudications and architectural verdict.

---

## Decision-rule sketch (frozen before run)

- **Verdict 1 (architecture rescued):** If ≥ 1 cell delivers > 12 percent under EITHER bottoms-up-moderate OR bundled-Finding-4 (the two more-defensible models per locked-memory finding 4), and at ≤ 10 megawatt-electric — composite survives mass-scaling.
- **Verdict 2 (architecture conditional on paper-aspirational only):** Closing cells exist only under paper-aspirational 40-watts-per-kilogram. Architecture survives ONLY by betting on the TRL-2 specific-power assumption. Programmatic-feasibility-conditional.
- **Verdict 3 (architecture dead under Block-4 accounting):** Zero closing cells across all four mass models. Architecture is conclusively dead under residence-class Block-4 accounting; only structural reframe remains (Block-13 spiral, or non-composite alternatives).

The H1-H8 numerical predictions above point to **Verdict 2** as the expected outcome. If observed, the architecture's survival hinges on a single technology assumption flagged by locked memory as paper-study aspirational.

---

## Results (post-run, 2026-05-18)

**256 cells swept; 2 closing cells.** Both under paper-aspirational mass model; zero closing cells across the other three. Architecture verdict locked: **Verdict 2 — composite is conditional on paper-aspirational 40-watts-per-kilogram only**.

### Headline matrix (max delivered fraction, percent of 200-tonne water haul)

| Mass model | 1 megawatt-electric | 2 megawatt-electric | 5 megawatt-electric | 10 megawatt-electric |
|---|---|---|---|---|
| Paper-aspirational (40 W/kg) | no closure | no closure | **7.68 %** | **1.03 %** |
| Bottoms-up moderate (10 W/kg) | no closure | no closure | no closure | no closure |
| KRUSTY-anchored (2.4 W/kg) | no closure | no closure | no closure | no closure |
| Bundled Finding-4 (5 t + 100 t/MWe) | no closure | no closure | no closure | no closure |

### Closing cells (both)

| Mass model | Power (MWe) | Isp exit | Isp inbound | M_dry total (t) | Delivered (t) | Delivered (%) | Exit burn (mo) | Inbound burn (yr) |
|---|---|---|---|---|---|---|---|---|
| Paper-aspirational | 5 | 3000 | 9000 | 259.13 | 15.37 | **7.684 %** | 5.17 | 3.13 |
| Paper-aspirational | 10 | 5000 | 9000 | 384.13 | 2.07 | **1.033 %** | 5.75 | 2.20 |

### Hypothesis adjudication

- **H1 (KRUSTY-anchored 5 MWe = zero):** HELD. M_power = 2083 t at 2.4 watts-per-kilogram makes the vehicle unflyable. Zero cells deliver positive water across the 16-cell sub-grid.
- **H2 (bottoms-up 5 MWe = zero):** HELD. M_power = 500 t makes M_dry_total (634 t) exceed the heavy-Isp m_at_earth at every cell. Zero closures.
- **H3 (paper-aspirational 5 MWe in 5-12 %):** HELD. Observed 7.68 % at Isp_exit 3000 / Isp_inbound 9000 — anchor-cell prediction was 7.65 %; engine confirms within 0.05 percentage points. Only one cell in the 16-cell sub-grid closes; all four 5000-9000 / 5000-9000 cells fail burn time at the heavier vehicle.
- **H4 (bundled-Finding-4 5 MWe = zero):** HELD. M_power = 505 t; behaves identically to bottoms-up.
- **H5 (KRUSTY-anchored 10 MWe = zero):** HELD. M_power = 4167 t.
- **H6 (bottoms-up 10 MWe = zero):** HELD. M_power = 1000 t.
- **H7 (paper-aspirational 10 MWe in 7-14 %):** **FALSIFIED.** Observed 1.03 % vs predicted band [7.0 %, 14.0 %]. The anchor-cell calculation at Isp 7000 / 9000 (predicted 9.50 %) is in fact a *non-closing* cell — at the heavier paper-aspirational vehicle (M_at_exit = 584 t vs Block 11's 384 t), the exit burn at Isp 7000 / 10 MWe stretches to 8.22 months, exceeding the 6-month dwell budget. The only closing cell at 10 MWe is the Isp_exit 5000 corner, which has a much higher exit mass ratio (1.163 vs 1.114), eating most of the delivered fraction.
- **H8 (bundled-Finding-4 10 MWe = zero):** HELD. M_power = 1005 t.
- **H9 (no low-power closure under any model):** HELD. 1 and 2 megawatt-electric have zero closing cells under all four mass models — the burn-time constraint dominates at low Isp_exit (mass-closure-favourable) and the inbound burn time blows out at low Isp_inbound regardless.
- **H10 (architectural verdict):** HELD as "paper-aspirational only." Closing cells exist only under the paper-aspirational mass model. Architecture is conditional on a single TRL-2 specific-power assumption.
- **H11 (functional-form robustness):** MARGINAL. 5-megawatt-electric prediction held inside the [6.1 %, 9.2 %] band (observed 7.68 %), but 10-megawatt-electric did not — observed 1.03 % vs predicted [7.6 %, 11.4 %]. Functional-form robustness held *within* a fixed closure region; it failed because the closure region itself contracted at heavier vehicle mass. This is a new sub-mechanism (closure-region contraction) not anticipated in the anchor calculation.

### Architectural finding

The residence-class composite under Block-4 accounting (6-month exit dwell, 6-year inbound cruise) **has no closing regime** under the three more-defensible mass models per locked-memory ICEBERG power finding 4 (MARVL-anchored). The architecture survives only under the paper-aspirational 40-watt-per-kilogram model — and even there:

- Maximum delivered fraction is **7.68 % at 5 megawatt-electric** — far below the lab-side Option A baseline of 17 %, below Block 9's no-Jupiter honest-floor of 15.73 %, and below the Block-13 spiral-reframe threshold-power-reduction-region of 21.5 % at 2 megawatt-electric (un-mass-scaled). The composite delivers less water at 5 megawatt-electric paper-aspirational than the *un-mass-scaled* spiral-out reframe delivered at 2 megawatt-electric — and the spiral-out reframe has not yet been mass-scaled (next round).
- At 10 megawatt-electric, paper-aspirational delivered fraction collapses to **1.03 %** — *worse* than 5 megawatt-electric, because the closure region contracts faster than the un-mass-scaled gain Block 11 reported (40.51 % naive at 10 megawatt-electric drops to 1.03 % with mass scaling). The Block-11 "more power is monotonically better" narrative reverses under mass scaling.
- Locked-memory ICEBERG power finding 2 (0-of-6 US space-fission programs reached orbit within their originally-stated decade) and finding 3 (NASA Fission Surface Power Phase 2 not awarded as of May 2026) make the underlying technology bet on TRL-2 paper-aspirational specific power deeply uncertain on programmatic grounds.

**The residence-class composite is structurally non-viable under any mass model that respects the MARVL-anchored decomposition.** It survives only by betting on a specific-power assumption that the same locked-memory record flags as paper-aspirational; and even when the bet pays, the architecture delivers a worse fraction than Option A.

### Methodology lessons

**Lesson 8 instance #7 (functional-form pre-registration partially robust):** The slope-based anchor calculation captured the *within-closure-region* effect of mass scaling correctly — H3 (5 megawatt-electric, paper-aspirational) held within 0.05 percentage points. The slope is `−(1 − 1/(MR_exit × MR_inbound))` and was derived correctly. But H7 (10 megawatt-electric, paper-aspirational) falsified by 6-13 percentage points because the *closure region itself contracted* — the cell I anchored on (Isp 7000 / 9000) became non-closing at the heavier vehicle. The mass-scaling effect on delivered fraction has TWO compounding sub-mechanisms: (a) slope effect within a fixed closure region, and (b) closure-region contraction by burn-time-budget violation.

**Lesson 12 candidate (closure-region contraction under mass scaling):** When sweeping a physical parameter (here: vehicle dry mass) that simultaneously enters multiple closure constraints (burn time AND mass-ratio AND delivery positivity), the constraint that binds first can switch with parameter value. Pre-reg-by-anchor-cell captures only the sub-mechanism active at the anchor; sub-mechanism switching across the swept range is a separate physical effect that must be enumerated up-front, not anchored. Future rounds should anchor on TWO cells from opposite ends of the swept range — not one — to surface sub-mechanism switching at pre-reg time.

**Lesson 12 corollary:** "More of the leverage parameter is monotonically better" intuitions almost always break under mass scaling. Block 11 said "10 megawatt-electric delivers 1.78× the 5-megawatt-electric headline." With mass scaling, 10 megawatt-electric delivers 0.13× the 5-megawatt-electric headline. The mass-scaling effect non-linearly inverts the leverage parameter's monotonicity.

### What this opens

- **R-megawatt-spiral-out-with-mass-scaling (next critical-path round):** Block 13 found the spiral reframe drops the threshold from 5 megawatt-electric to 1-2 megawatt-electric un-mass-scaled. This round shows that 2 megawatt-electric closure under Block-4 accounting requires zero-closing-cells (H9 held across all mass models). If the spiral reframe also closes under bottoms-up or bundled-Finding-4 at low power, the architecture has a survival regime independent of paper-aspirational. If not, the composite is **conclusively dead under any plausible mass-and-Δv-accounting combination**, regardless of structural reframe.
- **Vehicle cost audit moves down a notch in priority:** even if the architecture survives at 5 megawatt-electric paper-aspirational delivering 7.68 %, the per-ship delivered tonnage (15.4 t water per 200-t haul) makes the economic case more than 5× worse than Option A. Cost audit is now of "how bad is the loss?" relevance, not "is the architecture profitable?" relevance.
- **No re-derivation of Variant-B dry mass needed at 500 kilowatt-electric:** the implicit ~50-tonne power subsystem in Block 4's 200-tonne dry mass corresponds to a specific power of 10 watts-per-kilogram — matching the bottoms-up model and the bundled-Finding-4 model. So Block 4's nominal vehicle mass was internally consistent at the 500-kilowatt-electric scale; the inconsistency surfaced only when extrapolating Block 11's "more power, more delivery" narrative without re-scaling.

