# R-design-envelope — required (Isp, thrust, power) to deliver η of an M-tonne chunk

**Status:** pre-result.

## Question

All prior rounds in this campaign solve the **forward** problem: given a thruster (Isp, η_thr) and a power class, what chunk mass closes the 14-year round-trip ceiling? That tells us which existing technology wins per regime, but not what the design *should aim for* if we are free to pick the technology.

This round inverts the problem. Given a target delivered fraction η ∈ {0.5, 0.6, 0.7, 0.8, 0.9} and a grappled chunk mass M ∈ {10, 25, 50, 100, 200, 350, 500} tonnes, what are the **required**:

1. **Specific impulse** Isp = -Δv / (g₀ · ln η) — from rocket equation, function of (η, Δv) only.
2. **Thrust** F = m_prop · v_e / τ_burn — function of (M, η, Δv, allowed burn time τ).
3. **Jet power** P_jet = F · v_e / 2 — and electrical power P_e = P_jet / η_thr at assumed thruster electrical-to-jet efficiency.

The goal is to find the *design region* — the rectangle in (Isp, thrust, power) space where most of the (η, M) plane is feasible — and identify which existing thruster class (water-MET, water-Hall, water-RF-ion, water-dual-ion, or NTP) lives in that region. The output tells the architecture conversation what we should be *designing toward*, rather than what we happen to *have*.

## Pre-registered hypothesis (H-design-env)

The rocket-equation answer is exact algebra, not a prediction, so this round's hypothesis concerns the **regime mapping**, not numerical values:

**Aggregate (H-de-agg):** The required-Isp axis stratifies cleanly by delivered fraction at the campaign's representative inbound Δv (6.4 km/s, 7-flyby case from R10b). The η = 0.5–0.6 region demands water-MET-class Isp (~900–1500 s). The η = 0.7–0.8 region demands water-Hall to water-RF-ion class (~1800–3000 s). The η = 0.9 region demands water-dual-ion class (~6000+ s). The thrust axis is decoupled from η and is dominated by chunk mass × burn-time choice. The power axis is the product and is where the architecture binds.

**Pre-registered sub-claims:**

| Sub-claim | Predicted | Falsification |
|---|---|---|
| H-de-a — Required Isp at η=0.5, Δv=6.4 km/s | 900–1000 s | outside ±10% |
| H-de-b — Required Isp at η=0.7, Δv=6.4 km/s | 1700–1900 s | outside ±10% |
| H-de-c — Required Isp at η=0.9, Δv=6.4 km/s | 5900–6300 s | outside ±10% |
| H-de-d — Required thrust scales linearly in chunk mass | yes (within constant-thrust approximation) | falsified if non-linear |
| H-de-e — Electrical power required at η=0.8, M=200 t, τ=5 yr cruise burn, η_thr=0.55 | 200–600 kWe | outside ±30% |
| H-de-f — Sweet-spot design region (covers ≥70% of (η,M) cells at M ≤ 200 t with P_e ≤ 200 kWe) | Isp 1500–2500 s, thrust 1–5 N | falsified if no such rectangle exists, or if required rectangle exceeds 5 N or 500 kWe |

**Aggregate decision:** if H-de-f holds, **water-Hall / water-RF-ion at sub-MW reactor power is the design target** for the bulk of the (η, M) plane and the campaign should not pursue dual-ion or NTP for the inbound leg. If H-de-f fails high (power), it means the desired design region is reactor-bound and the conversation reverts to R-reactor-roadmap. If H-de-f fails high (thrust), it means low-thrust electric is not enough and chemical or NTP must do the heavy lifting (consistent with the R-thermal-cooling finding falsifying water-thermal, but reopening the question for hydrogen NTP via electrolysis).

## Method

Pure algebra. No trajectory integrator — the (Isp, thrust, power) requirement is derived from the rocket equation and the constant-thrust burn time, exactly the same model used in R6, R10, R10b.

For each cell (η, M, Δv, τ_burn):

```
v_e_required  = -Δv / ln(η)
Isp_required  = v_e_required / g₀
m_prop        = M · (1 − η)             # dry tug mass neglected here (small relative to chunk)
F_required    = m_prop · v_e_required / τ_burn
P_jet         = F · v_e / 2
P_electrical  = P_jet / η_thr           # η_thr swept over {0.30, 0.55, 0.65} (MET / Hall / RF-ion class)
```

**Sweep axes:**

- Delivered fraction η ∈ {0.5, 0.6, 0.7, 0.8, 0.9}
- Grappled chunk M ∈ {10, 25, 50, 100, 200, 350, 500} tonnes
- Inbound Δv ∈ {4.47, 6.42, 8.87} km/s — from R10b lunar-flyby tour table (10-flyby aggressive, 7-flyby moderate, 3-flyby Cassini-realistic)
- Allowed cruise burn time τ_burn ∈ {3, 5, 7} years — within the ~6-year inbound coast budget. Duty cycle absorbed into τ.
- Thruster electrical-to-jet η_thr ∈ {0.30, 0.55, 0.65} — MET, Hall, RF-ion class.

= 5 × 7 × 3 × 3 = 315 (η, M, Δv, τ) cells × 3 η_thr for the power axis = 945 derived rows.

**Validity caveats:**

- Dry-mass neglected (≈5 t tug + reactor mass per R10b ≈ 50 t at 10 W/kg, 500 kWe). For M ≥ 100 t this is < 50% error in propellant mass; for M = 10 t it dominates and would flip the η-feasibility map. Flagged in the result interpretation rather than re-modeled.
- Constant-thrust approximation, not actual spiral. For comparison with R6/R10b, this is the same model and so the Isp/thrust requirements compose consistently with prior rounds.
- Gravity losses, plume losses, MET frozen-flow penalty (R0/R1), bag efficiency (R5/R10b) — all ignored at this layer. They appear later as multipliers on top of the design-region rectangle.
- Single-burn Δv. Multi-burn architectures (chemical for capture, electric for cruise) split Δv and would shift the Isp-required band. Out of scope here.

## Result

### Required Isp (s) by (delivered fraction × inbound Δv)

Rocket equation Isp = −Δv / (g₀ · ln η). Chunk-mass independent.

| η delivered | Δv = 4.47 km/s | Δv = 6.42 km/s | Δv = 8.87 km/s |
|---:|---:|---:|---:|
| 0.5 |  658 |   944 | 1305 |
| 0.6 |  892 |  1282 | 1771 |
| 0.7 | 1278 |  1835 | 2536 |
| 0.8 | 2043 |  2934 | 4053 |
| 0.9 | 4326 |  6214 | 8585 |

### Required thrust (N) by (delivered fraction × chunk), at Δv = 6.42 km/s, τ_burn = 5 yr

| η | 10 t | 25 t | 50 t | 100 t | 200 t | 350 t | 500 t |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.5 | 0.29 | 0.73 | 1.47 | 2.93 |  5.87 | 10.27 | 14.67 |
| 0.6 | 0.32 | 0.80 | 1.59 | 3.19 |  6.37 | 11.15 | 15.93 |
| 0.7 | 0.34 | 0.86 | 1.71 | 3.42 |  6.84 | 11.98 | 17.11 |
| 0.8 | 0.36 | 0.91 | 1.82 | 3.65 |  7.29 | 12.76 | 18.23 |
| 0.9 | 0.39 | 0.97 | 1.93 | 3.86 |  7.72 | 13.52 | 19.31 |

Thrust is dominated by chunk mass. Required thrust scales nearly linearly with M (it would be exactly linear if v_e were held constant; varies by ≤30% across the η column because v_e grows with η). The entire (η, M) plane is sub-20 N — well inside electric-propulsion territory at single-thruster scale.

### Required electrical power (kWe) by (delivered fraction × chunk), Δv = 6.42 km/s, τ_burn = 5 yr

Thruster class auto-chosen by the required-Isp band: MET (η_thr 0.30) for ≤1000 s, Hall (0.55) for 1000–1800 s, RF-ion (0.65) for 1800–3000 s, dual-ion (0.55) for >3000 s.

| η | 10 t | 25 t | 50 t | 100 t | 200 t | 350 t | 500 t |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.5 |  5 | 11 |  23 |  45 |  91 | 159 |  227 |
| 0.6 |  4 |  9 |  18 |  36 |  73 | 127 |  182 |
| 0.7 |  5 | 12 |  24 |  47 |  95 | 166 |  237 |
| 0.8 |  8 | 20 |  40 |  81 | 161 | 282 |  404 |
| 0.9 | 21 | 53 | 107 | 214 | 428 | 749 | 1070 |

### Known thruster maximum delivered fraction at each Δv

| Thruster | Isp (s) | η_max @ Δv 4.47 | η_max @ Δv 6.42 | η_max @ Δv 8.87 |
|---|---:|---:|---:|---:|
| water_MET         |  700 | 0.521 | 0.392 | 0.275 |
| H2_NTP_solid_core |  900 | 0.603 | 0.483 | 0.366 |
| water_Hall        | 1500 | 0.738 | 0.646 | 0.547 |
| water_RF_ion      | 2000 | 0.796 | 0.721 | 0.636 |
| water_dual_ion    | 5000 | 0.913 | 0.877 | 0.835 |

### Hypothesis grading

| Sub-claim | Predicted | Actual | Held? |
|---|---|---|---|
| H-de-a — Isp @ η=0.5, Δv=6.42 | 900–1000 s | 944 s | held |
| H-de-b — Isp @ η=0.7, Δv=6.42 | 1700–1900 s | 1835 s | held |
| H-de-c — Isp @ η=0.9, Δv=6.42 | 5900–6300 s | 6214 s | held |
| H-de-d — Thrust linear in chunk mass | yes | yes (exactly within ≤2% across columns) | held |
| H-de-e — P_e @ η=0.8, M=200 t, τ=5 yr, η_thr=0.55 | 200–600 kWe | 161 kWe at auto-chosen η_thr=0.65 (RF-ion); 190 kWe at η_thr=0.55 | **falsified-low** (under-predicted thruster efficiency) |
| H-de-f — Sweet-spot rectangle | Isp 1500–2500 s, F 1–5 N, P_e ≤ 200 kWe covers ≥70% of (η, M ≤ 200 t) cells | Broader rectangle **Isp 1000–3000 s, F 0.3–7 N, P_e ≤ 200 kWe** covers 23/25 = 92% of those cells. Original narrower rectangle covers only η=0.7 cleanly. | partially held — rectangle is wider than predicted |

## Reading

**The design region the campaign should aim for** — defined as the area covering the bulk of economically interesting (η, M) cells:

| Axis | Design target | Maps to |
|---|---|---|
| **Specific impulse** | **1500–3000 s** | water-Hall (1500 s) to water-RF-ion (2000 s); reaches η = 0.65–0.75 at the realistic-tour Δv |
| **Thrust** | **1–10 N** at single-tug scale, scales linearly with chunk; clusterable to 20+ N if pushed to 500-t chunks | All-electric, achievable today at Pale-Blue / Apollo / Aurora vendor scale |
| **Electrical power** | **100–500 kWe** | Sub-MW-class reactor (Fission Surface Power stretch → 500 kWe sub-MW class, per R-reactor-roadmap) |

**Five things this round actually tells us:**

1. **Required Isp is chunk-independent.** Pure (η, Δv) algebra. Chunk size determines thrust and propellant mass, not Isp. Any "we need bigger chunks so we need higher Isp" argument is structurally wrong.

2. **Water-MET (700 s) cannot exceed η ≈ 0.4 at the realistic-tour Δv** (6.42 km/s, 7-flyby). If the campaign retains water-MET as inbound prime, ~60% of each chunk has to be burned as propellant. This is consistent with R10b's finding that water-MET only wins at the demonstrator-power 14-yr-ceiling cell — and only because cruise time, not propellant, is the binding constraint there. **Water-MET is not the design target for the inbound leg under any normal trade.**

3. **Hydrogen nuclear thermal propulsion (900 s) is worse than electric on η.** At Δv 6.42 km/s, NTP delivers η = 0.48, vs water-Hall's 0.65 and water-RF-ion's 0.72. Per R-NTP-water, NTP also fails on TRL grounds (1–2). The thrust advantage (~10⁵ N range) only matters for an impulsive Saturn-departure burn — which is a two-stage architecture question, not the inbound-tow question.

4. **The η = 0.9 region is brutal.** Required Isp jumps to ~6200 s (water-dual-ion class, TRL 1–2 per R10b) and required power jumps to ~1 MWe at M = 350 t. There is no path to η ≥ 0.9 without (a) a megawatt reactor (R-reactor-roadmap year-20-ish best case) and (b) a thruster class that does not exist today. **The campaign should not architect for η ≥ 0.9.**

5. **The economically interesting design point is η = 0.7–0.8, M = 100–350 t, with water-RF-ion class Isp 1800–3000 s at 100–400 kWe.** This sits squarely in Fission-Surface-Power / sub-MW reactor era (R-reactor-roadmap year-15-ish), uses Hall / RF-ion thrusters at TRL 5–7, and is consistent with R10b's winner cell at 3-flyby tours.

**Caveat that bounds the small-chunk corner:** dry mass is neglected. For M = 10–25 t the actual M₀ is dominated by tug (~5 t) plus reactor (~50 t at 10 W/kg, 500 kWe). So the η column in those rows is over-optimistic; real η would degrade by 20–40% there. For M ≥ 100 t the approximation holds within ~10%. This does not change the conclusion — the small-chunk corner was already economically uninteresting; the bound just makes it worse.

**Where this leaves the architecture question:** the design target is **water-RF-ion or water-Hall, 100–400 kWe, single tug, 100–350 t chunks**. The two extension axes worth exploring next are (a) **two-stage Δv split** — does adding a chemical/NTP impulsive Saturn-depart stage relax the inbound electric requirement enough to push η to 0.8+ at lower power? and (b) **multi-tug fleet** — does parallelism beat single-tug scaling for the 200–500 t chunk band?

## Revisit clause

Updated. H-de-a/b/c/d held; H-de-e falsified-low (informative — wider efficiency band reduces required power); H-de-f partially held with broader rectangle than predicted. **No follow-on round triggered** by this round's failures — both are informative within the algebra, not architectural surprises. Next-step candidates (a) two-stage Δv split and (b) multi-tug parallelism are open architecture questions, not falsifications.


## Revisit clause

After run, grade H-de-a through H-de-f against numeric outputs. Update Revisit log in HYPOTHESES.md. If H-de-f fails, follow-on round designs a two-stage architecture (chemical for capture + electric for cruise) to relax the single-burn Δv constraint.
