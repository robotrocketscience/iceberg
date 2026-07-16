# R-reactor-specific-power-program-targets — STUDY.md

**Author:** rhea (worker session, iceberg-rhea-2 branch)
**Date:** 2026-05-15 (latest+8)
**Status:** pre-registration. Three deviations from Saturn-authored SCOPE documented below.

---

## SCOPE deviations (documented, anchored on input data)

Before writing this STUDY I read the four enceladus-r5 closure tables (`R_specific_power_cliff/results/specific_power_cliff.json`, `R_aerocapture_cliff_shift/results/*.json`, `R_reactor_lifetime_vs_burn_time/results/reactor_lifetime_regrade.json`, `R_arch_E_specific_power_flown_anchored/results/arch_E_specific_power_sweep.json`). Three things in the SCOPE do not survive contact with this data:

**Deviation 1 — H1 recast.** SCOPE H1 predicts the minimum-point at L0-05 **strict** (15-yr ceiling) is `(8 W/kg, 5 yr)`. The closure table shows `n_close_15yr = 0` at every specific-power level swept from 2.4 through 10 W/kg, and the lifetime regrade shows `close_15yr = 0` at every (sp, X, L) cell — no surviving point exists at L0-05 strict in the tested envelope. SCOPE method §1 explicitly forbids re-running propulsion physics, so the honest answer must be **either** (a) "no min-point exists in tested envelope" or (b) extrapolation to specific powers above 10 W/kg. I take (b) and pre-register a numeric extrapolation below.

**Deviation 2 — H2 ladder.** SCOPE H2 predicts the minimum-point at L0-05 ≥ 25-yr waiver, conditional on aerocapture credit X=10 km/s, is `(5 W/kg, 10 yr)`. The R-reactor-lifetime regrade shows that at `(sp=5 W/kg, X=10 km/s, L=10 yr)`: **0 cells close**. The actual min-point at X=10 km/s is `(6 W/kg, 10 yr)` or `(5 W/kg, 15 yr)`. H2's "aerocapture closes at all" prior (50%) also overstates because H2's min-point requires closure at ≥ 10 km/s credit specifically. I split H2 into a ladder of three (X, sp, L) min-points and condition each on a credit-specific aerocapture prior.

**Deviation 3 — H7 added.** SCOPE pre-registers no hypothesis on capital-class NPV post-cell-restoration. Methodology lesson 10 (rhea, captured this session) says per-mission cashflow ≠ program NPV. A reactor-program profile that restores a propulsion-physical cell may still leave the cell deep NPV-negative at every capital-class threshold — that would be a distinct falsification mode for H6's "technology-demonstrator-only" reading. H7 covers it.

Other SCOPE structure preserved: H3, H4, H5, H6 retained with min-point inputs updated per the deviation-1/-2 corrections. R-power-base-rate three-prior bracket (uniform 8.9%, Jeffreys 4.9%, skeptical 2.9% at 2035 horizon) carried verbatim from R-power-bayesian-update.

---

## Question

For the held chunk-rendezvous architecture (axis 19) at conservative anchors, and conditional on R-hybrid-aerocapture-aerobraking + R-bring-rendezvous-survivability both closing:

1. What is the minimum `(specific power × lifetime × aerocapture-credit)` point that puts at least one cell back in the matrix at L0-05 ≥ 25-yr waiver?
2. Does any such point exist at L0-05 strict (15-yr) in the tested envelope? If not, where would it sit under extrapolation?
3. Under R-power-base-rate three-prior priors (2.9–8.9% on US fission orbit by 2035), what is the joint posterior on (reactor delivers required sp × L) for each min-point?
4. Under conjunction with engineering-closure priors (aerocapture credit-laddered, B-ring 20–30%), what is the full conjunction posterior?
5. At the joint-weighted expected delivered mass per mission, which capital-class threshold (if any) does program NPV clear?

---

## Reading-anchor: joint constraint surface (extracted from R-reactor-lifetime regrade)

The min aerocapture credit X (km/s) for any cell to close L0-05 ≥ 25-yr waiver, by `(specific power × reactor lifetime ceiling)`:

| sp (W/kg) | L=5 yr | L=8 yr | L=10 yr | L=15 yr | L=∞ |
|---:|---:|---:|---:|---:|---:|
| 2.4 (KRUSTY) | — | — | — | — | — |
| 5.0 | — | — | 15 | 10 | 10 |
| 6.0 | — | 20 | 10 | 5 | 5 |
| 7.0 | — | 15 | 5 | 5 | 5 |
| 8.0 | — | 10 | 0 | 0 | 0 |
| 9.0 | 25 | 5 | 0 | 0 | 0 |
| 10.0 | 20 | 0 | 0 | 0 | 0 |

`—` = no aerocapture credit in tested range [0, 25 km/s] closes any cell.

**Headline reads from the surface:**

- KRUSTY 2.4 W/kg never closes regardless of lifetime or aerocapture credit.
- L=5 yr (Brayton-flight-rated minimum) rules out anything below 9 W/kg even with aerocapture.
- L=10 yr (Kilopower design target) is the cheapest credible flight-life that lets ≤ 8 W/kg cells close at X=0.
- The "no-aerocapture" column (X=0) requires sp ≥ 8 W/kg AND L ≥ 10 yr — this is the floor at conservative engineering anchors.
- L0-05 strict (15-yr) is empty across the entire tested grid (sp ∈ [2.4, 10], X ∈ [0, 25], L ∈ [5, ∞]).

---

## Pre-registration BOE

### H1 (recast) — L0-05 strict (15-yr) closure-cliff extrapolation

R-specific-power-cliff `best_at_25yr` cells show round-trip dropping with sp at fixed chunk=200 t, Isp=2934 s, reactor=500 kWe:

| sp (W/kg) | best round-trip (yr) |
|---:|---:|
| 8 | 24.91 |
| 9 | 24.19 |
| 10 | 23.60 |

The decrement is ~0.65 yr per (W/kg). Components at sp=10: outbound burn 4.37 yr + inbound burn 6.06 yr + cruise 12.17 yr + ops 1.0 yr = 23.6 yr. **Burn time scales ~1/sp** (constant-thrust under constant thrust-mass ratio scaling); cruise time is sp-independent at fixed trajectory.

Setting cruise + ops = 13.17 yr as the sp-independent floor (would require faster-cruise trajectory to relax — out of scope for this round): total burn budget at L0-05 strict = 15 − 13.17 = **1.83 yr**. At sp=10 W/kg the burn is 10.43 yr. Burn time scaling sp_target / 10 = 10.43 / 1.83 → sp_target ≈ **57 W/kg**.

This is 24× KRUSTY-anchored 2.4 W/kg and 1.4× the TRL-2 paper-aspiration 40 W/kg. Pre-registered min-point at L0-05 strict (Hohmann cruise): **sp ≥ 57 W/kg** with L ≥ ~10 yr.

| H | claim | predicted range | falsification band |
|---|---|---|---|
| H1 | At L0-05 strict (15-yr) with Hohmann cruise, the minimum specific power to close any cell in the chunk × reactor × Isp envelope is **sp ≥ 50 W/kg** (extrapolated). Lifetime requirement is at least 10 yr to clear cumulative burn time. No point in tested envelope closes. | min sp at strict-15 = 50–65 W/kg | H1 falsified if a credible argument puts the min-point ≤ 30 W/kg under Hohmann cruise, OR if fast-cruise relaxation brings the floor below 20 W/kg |

### H2 (ladder) — L0-05 ≥ 25-yr waiver min-points

From the constraint surface above, the cheapest min-points at three aerocapture-credit rungs:

| H | claim | predicted point | falsification |
|---|---|---|---|
| H2a | At X=0 km/s aerocapture (no closure), min-point is `(sp=8 W/kg, L=10 yr)`. | (8, 10) | falsified if (≤ 7 W/kg, ≤ 10 yr) or (≤ 8, ≤ 8) close |
| H2b | At X=5 km/s aerocapture, min-point is `(sp=7 W/kg, L=10 yr)` or `(sp=6 W/kg, L=15 yr)`. Both are dominated solutions: H2b min on sp-axis = 6. | min sp = 6 at X=5 (with L=15) | falsified if ≤ 5 W/kg closes at X=5 |
| H2c | At X=10 km/s aerocapture, min-point is `(sp=6 W/kg, L=10 yr)` or `(sp=5 W/kg, L=15 yr)`. H2c min on sp-axis = 5. | min sp = 5 at X=10 (with L=15) | falsified if ≤ 4 W/kg closes at X=10 |

### H3 — joint posterior at H2a min-point `(8 W/kg, 10 yr)`, no aerocapture credit

Conditional probabilities `P(reactor delivers ≥ θ | flies)` are pre-registered from known program anchors. KRUSTY 2.4 W/kg / 28 hr is the sole flown heritage; FSP Phase-1 paper-target ~6 W/kg / 10 yr is the next anchor up; Duffy directive August 2025 100 kWe scope is 5× FSP Phase-1 nominal but not contracted.

Pre-registered conditionals (educated; ranged in run.py sensitivity):

| Threshold | P(delivers ≥ θ specific power \| flies by 2035) | P(delivers ≥ θ lifetime \| flies) |
|---|---:|---:|
| 5 W/kg | 0.70 | n/a |
| 6 W/kg | 0.60 (≈ FSP design target) | n/a |
| 8 W/kg | 0.25 | n/a |
| 10 W/kg | 0.10 | n/a |
| 5 yr | n/a | 0.70 |
| 10 yr | n/a | 0.30 (Kilopower design, no flight heritage) |
| 15 yr | n/a | 0.05 |

Treating sp-conditional and lifetime-conditional as independent (caveat: not strictly true; flagged in validity).

**H3 prediction (uniform prior):** P(any US fission orbit by 2035) × P(≥ 8 W/kg | flies) × P(≥ 10 yr | flies) = 0.089 × 0.25 × 0.30 = **0.67%**. Three-prior bracket: skeptical 0.22% (0.029 × 0.25 × 0.30) — uniform 0.67% — three-prior midpoint ≈ 0.40%.

| H | claim | predicted range | falsification |
|---|---|---|---|
| H3 | Joint posterior at H2a min-point `(8 W/kg, 10 yr, X=0)` is in `[0.2%, 1.0%]` across three-prior bracket; uniform-prior point estimate ≤ 1.0%. | [0.2%, 1.0%] | falsified if uniform > 3.0%, OR if the bracket collapses to a single number > 0.5% under any defensible prior |

### H4 — joint posterior at H2c min-point `(6 W/kg, 10 yr)` conditional on aerocapture credit X ≥ 10 km/s

**H4 prediction (uniform prior):** 0.089 × 0.60 × 0.30 = **1.60%**. Bracket: skeptical 0.029 × 0.60 × 0.30 = **0.52%**.

| H | claim | predicted range | falsification |
|---|---|---|---|
| H4 | Joint posterior at H2c min-point `(6 W/kg, 10 yr)`, conditional on aerocapture credit ≥ 10 km/s closing, is in `[0.5%, 1.7%]` across bracket; uniform-prior point ≈ 1.6%. | [0.5%, 1.7%] | falsified if uniform > 4%, OR if conditional independence of sp / lifetime / fly-by-2035 turns out to be load-bearing wrong |

### H5 — full conjunction posterior with engineering closures (credit-laddered priors)

Engineering closure priors split per credit-rung (deviation from SCOPE's flat-50% aerocapture prior):

| Engineering claim | Pre-registered prior |
|---|---:|
| P(R-hybrid-aerocapture-aerobraking closes at any credit > 0) | 0.50 |
| P(closes at ≥ 5 km/s \| closes at all) | 0.70 → marginal 0.35 |
| P(closes at ≥ 10 km/s \| closes at all) | 0.40 → marginal 0.20 |
| P(closes at ≥ 15 km/s \| closes at all) | 0.15 → marginal 0.08 |
| P(R-bring-rendezvous-survivability closes at meaningful operating cadence) | 0.25 |

(Aerocapture-credit ladder anchored on hyperion's R-aerocapture-fast-cruise-envelope finding that Variant C engineering closure was falsified at fast-cruise framing — the "closes at large credit" tail is thinner than the SCOPE's flat 50%.)

**H5 conjunction at H2a min-point `(8, 10, X=0)`:** reactor posterior × B-ring = 0.0067 × 0.25 = **0.17%** (uniform). No aerocapture multiplier needed because H2a doesn't require closure.

**H5 conjunction at H2c min-point `(6, 10, X=10)`:** reactor posterior × P(aerocapture ≥ 10) × B-ring = 0.016 × 0.20 × 0.25 = **0.080%** (uniform). Skeptical: 0.005 × 0.20 × 0.25 = **0.026%**.

| H | claim | predicted range | falsification |
|---|---|---|---|
| H5 | Full conjunction posterior at the best surviving min-point (H2a `(8, 10, X=0)` or H2c `(6, 10, X=10)`) is in `[0.02%, 0.20%]` across three-prior bracket × credit-ladder. **The architecture is not financeable on this conjunction posterior under any return-seeking-capital structure** — sovereign-grant class only. | best-case uniform ≤ 0.20% | falsified if any defensible prior combination puts the conjunction > 1.0%, OR if either engineering prior has empirically-anchored update lifting it (e.g. hyperion's R-hybrid-aerocapture-aerobraking returns with prior > 70%) |

### H6 — reading-level conclusion (load-bearing)

| H | claim | falsification |
|---|---|---|
| H6 | Program-class decision at conservative anchors is **technology-demonstrator-only.** Restoring regulated-utility-class framing requires (a) reactor program targets that no current US program funds (≥ 6 W/kg AND ≥ 10 yr, ideally ≥ 8 W/kg) AND (b) two engineering closures that have not run. Until at least one of those constraints relaxes, technology-demonstrator is the honest pitch posture. | H6 falsified if any (H1-H5) combination produces joint posterior > 10% for a return-seeking-capital-class cell |

### H7 (new) — capital-class NPV at conjunction-weighted expected mass

R-specific-power-cliff `best_at_25yr` at sp=8 W/kg, chunk=200 t, Isp=2934 s, reactor=500 kWe: delivered mass = 42.0 t/mission, round-trip 24.9 yr.

At H5 conjunction posterior 0.17% (uniform-prior, H2a min-point), the **programmatic-risk-adjusted expected delivered mass = 0.17% × 42.0 t = 0.071 t/mission ≈ 71 kg**.

At H5 conjunction posterior 0.080% (uniform-prior, H2c min-point with aerocapture credit), best cell at sp=6 W/kg = 28.9 t/mission (R-specific-power-cliff `best_at_30yr` table, but 25-yr-conditional only at higher X — anchor on the closest 25-yr-conditional cell, ~25 t). Expected = 0.080% × 25 t ≈ 20 kg/mission.

Per R-LEO-water-demand-curve BEST_CELL clearing price ≈ $2.5M/tonne:
- Per-mission gross revenue at H2a expected mass: 0.071 t × $2.5M = **$0.18M** programmatic-risk-adjusted.
- Per-mission gross revenue at H2c expected mass: **$0.05M**.

Per-mission CapEx (rhea R-architecture-D-cost, low ship CapEx anchor): $1–3B. NRE: $5–10B program-level.

Even at zero discount, program revenue over 25 missions at $0.18M each = $4.5M against $1–3B/mission CapEx + $5–10B NRE → **NPV(0) deeply negative across all three priors and all min-points**.

| H | claim | predicted range | falsification |
|---|---|---|---|
| H7 | Programmatic-risk-adjusted program NPV at every (H2 min-point × three-prior × engineering-conjunction) combination is structurally negative at every capital-class threshold including sovereign-grant (which doesn't require positive NPV but does require sustained mission cadence). Sovereign-grant is the only class that can underwrite this; bond / regulated-utility / corp-growth / venture all structurally unreachable. | sovereign-grant only | H7 falsified if any combination of (sp lift to ≥ 10 W/kg) × (clearing-price lift) × (mission-cadence lift) produces NPV(0) > 0 at sovereign-bond hurdle (~3% discount) at uniform-prior reactor posterior |

---

## Method (run.py)

1. **Load** the four enceladus-r5 closure JSONs.
2. **Reconstruct the (sp × L × X) closure-count grid** at L0-05 ≥ 25-yr ceiling from the R-reactor-lifetime regrade.
3. **Identify min-points** at each (waiver-ceiling, aerocapture-credit-rung) combination — three for H2a/b/c and the extrapolation for H1.
4. **Apply R-power-base-rate three-prior bracket** (uniform 8.9%, Jeffreys 4.9%, skeptical 2.9%) × conditional-on-flies-by-2035 priors for sp + lifetime.
5. **Compute conjunction posteriors** with credit-laddered aerocapture priors + B-ring 25%.
6. **Compute capital-class NPV** at conjunction-weighted expected mass, anchored on R-specific-power-cliff `best_at_25yr` per-mission delivered mass × $2.5M/tonne × 25 missions over 25 years − ship CapEx − NRE.
7. **Synthesis table** — rows: each (sp, L, X) min-point; columns: closure-yes/no, three-prior reactor-flies, conditionals, conjunction, expected mass, expected revenue, NPV(0), capital-class threshold met.
8. **Grade hypotheses** H1–H7 against pre-registered ranges.

Output: `results/synthesis_table.csv`, `results/synthesis.json`, `results/findings.md`.

---

## Validity caveats

1. **Conditional-independence assumption.** P(sp ≥ θ) × P(lifetime ≥ θ) × P(flies by 2035) treats the three factors as independent. In reality they are positively correlated: a well-funded reactor program will tend to deliver on more than one axis simultaneously. The model therefore **under-estimates the joint** at the optimistic tail (a successful program is likely to deliver both targets) and **over-estimates the joint** at the pessimistic tail (a half-funded program likely delivers neither). Sensitivity range: a ±30% adjustment on each conditional from this baseline preserves the H5 ordering but moves point estimates ~40%.

2. **Conditional probabilities are best-guess, not measured.** Anchors on KRUSTY (2.4 W/kg flown), FSP Phase-1 paper-target (~6 W/kg), Duffy directive (100 kWe scope). The P(≥ 8 W/kg | flies) = 0.25 is the most load-bearing single number in H3-H5. If real value is 0.10, posteriors drop ~2.5×; if 0.50, rise 2×. Run.py will sweep.

3. **Aerocapture-credit ladder priors are educated.** Hyperion has SCOPE only. The credit-rung priors (0.35 / 0.20 / 0.08 at ≥ 5 / 10 / 15 km/s | closes-at-all) are derived from R-aerocapture-cliff-shift's finding that the credit range is bounded by outbound burn binding at the low-sp limit — i.e. high-credit closure is harder physics, not just less-likely-engineering. Worth a sensitivity ladder.

4. **No non-US programs.** China (CASC paper-target megawatt-class fission by 2040), Russia (Project Zeus, NEP 1 MWe, suspended), India (BHARAT-class concepts). Out-of-scope per SCOPE; ICEBERG campaign is US-anchored. A non-US program in the demonstrator window would lift posteriors but adds geopolitical-procurement uncertainty.

5. **Cruise time held constant at Hohmann.** Hyperion R-cruise-time-optimization found fast-cruise wins 3–6 yr for Variant C; that finding is unintegrated for Architecture E and the cliff envelope. H1's extrapolation assumes Hohmann; a faster-cruise relaxation would lower the strict-15-yr sp floor from ~57 W/kg toward maybe 30–35. H1 falsification band brackets this.

6. **L0-05 ≥ 25-yr waiver is a project-owner decision, not a derivation.** Matrix decision point #2 (round-trip ceiling) is open. This round answers conditionally on the waiver. If the waiver is denied and L0-05 holds strict, H1's "no min-point in tested envelope" is the answer — sp must rise to ~57 W/kg or cruise must drop.

7. **R-architecture-D-cost and R-architecture-D-L1007-relaxation (this worker's prior rounds)** found Architecture D structurally NPV-negative at zero discount. H7's "sovereign-grant only" conclusion mirrors that finding — convergence is not surprising but is not independent evidence either.

---

## Reading template (filled after run)

Five sections per protocol: Hypotheses adjudicated, Headline, Reading, Cross-learning, Next-round candidates.
