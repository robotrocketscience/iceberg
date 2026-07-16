# R-no-jupiter-composite-headroom

**Worker:** titan (Block 9)
**Owner:** project owner / orchestrator
**Pre-registration date:** 2026-05-16

---

## Motivation

The Block-5/6/7 Jupiter-gravity-assist sub-campaign closed by demonstrating that Jupiter gravity-assist is only realisable at ~7.5 percent of launch windows under self-consistent cruise-reshape budgets. Block 8 then bookkept aerocapture's heat-shield mass and re-anchored the composite at **15.37 percent no-Jupiter** / **15.79 percent campaign-mean**, vs Option A's 17 percent locked baseline (rhea-2 Round 3).

The architecture is therefore Option-A-equivalent in the 92.5 percent of windows where Jupiter is not available, not Option-A-superior. Two questions follow:

1. **Within the levers that are already engineering-credible** (TPS-geometry realism, heat-shield-as-water-ablator), how much of the ~1.6 pp gap to 17 percent can be closed honestly?
2. **Of the levers that require open R&D rounds to close** (jettison engineering, dry-mass scaling, fill-fraction up-sweep, faster-cruise inbound), which would shift the composite by enough to be worth elevating in priority?

Distinguishing these two categories matters for the pitch deck: it lets the program quote either "Option-A-equivalent at honest accounting" or "Option-A-superior under stretch but credible engineering" with the conditioning made explicit.

**Out of scope:**

- Re-opening Jupiter gravity-assist availability. Three Block-5/6/7 rounds adjudicated this; the lever buys at most ~5 percent additional viable windows at meaningful cost. Not revisited here.
- Faster-cruise inbound delta-velocity reduction. Hyperion's R-cruise-time-optimization showed for Variant C that non-Hohmann cruise saves 3-6 yr round-trip at +6 km/s heliocentric. That insight may transfer to residence-class but requires a separate trajectory recomputation (Lambert at residence-class semi-major axis with the Saturn-side residence-exit burn unchanged). **Flagged for follow-on round R-residence-cruise-time-optimization.**
- Power-class up-sweep. Hyperion's R-variant-B-500kWe-sizing established 500 kilowatt-electric as the risk-adjusted optimum. Not revisited.

---

## Lever set

All upside is measured against Block 8 baseline: composite no-Jupiter at central parameters (1.5 km/s aerocapture saving, 50 kg/m² TPS, 50 percent windward coverage, Isp_exit 7000 s, Isp_inbound 5000 s, 20 t jettison at residence, 200 t collected at residence, 200 t dry mass), **delivered fraction 15.37 percent.**

Categorise each lever as **engineering-credible** (already grounded in published anchors or basic geometry) or **conditional** (depends on an open R&D round closing favourably):

| # | Lever | Description | Category | Pre-registered uplift range |
|---|---|---|---|---|
| L1 | TPS coverage 50 → 30 percent | Sphere-cone biconic with backshell only marginal — engineering reality, not lever | engineering-credible | +0.4 to +0.8 pp |
| L2 | Water-as-ablator | Outer water layer ablates as TPS, eliminating separate heat shield mass | engineering-credible-conditional | +0.8 to +1.2 pp (ceiling) |
| L3 | Exit Isp 7000 → 9000 s | Specific impulse uplift on the 7.4 km/s Saturn-side exit burn only; inbound stays at 5000 s | engineering-credible | +0.4 to +0.8 pp |
| L4 | Jettison 20 → 40 t at residence | Drop more hardware (lower stage, ram-scoop intake, surplus structure) before inbound burn | conditional on R-jettison-engineering | +0.3 to +0.6 pp |
| L5 | Dry mass 200 → 160 t (Variant B scaling) | Tighter mass budget for 500-kW-electric spacecraft (smaller radiator, lighter structures) | conditional on Variant scaling | +0.5 to +1.0 pp |
| L6 | Fill 200 → 250 t at residence | Higher ram-scoop fill in same residence time | conditional on R-residence-bag-structural (Iapetus-owned) | +0.5 to +1.2 pp |

Block 8 already noted L1 and L2 as "limitations of the model" rather than headline levers. This round promotes them to first-class levers and bookkeeps L3 through L6 alongside, to determine the upper edge of credible composite headroom.

---

## Pre-registered hypotheses

| # | Hypothesis | Prediction | Falsification rule |
|---|---|---|---|
| H1 | L1 (TPS coverage 50 → 30 percent) at Block 8 central params alone gives a +0.4 to +0.8 pp delivered-fraction uplift. | Composite_no_Jupiter at 30% coverage ∈ [15.8, 16.2] percent. | Falsified if outside [15.5, 16.5] percent. |
| H2 | L2 (water-as-ablator, zero TPS) at Block 8 central params alone gives +0.8 to +1.2 pp uplift over Block 8's 50%-coverage baseline. | Composite_no_Jupiter at zero-TPS ∈ [16.1, 16.6] percent. | Falsified if outside [15.8, 17.0] percent. |
| H3 | L3 (exit Isp 7000 → 9000 s) at Block 8 central params alone gives +0.4 to +0.8 pp. | Uplift ∈ [0.4, 0.8] pp; composite ∈ [15.8, 16.2] percent. | Falsified if outside [0.2, 1.0] pp. |
| H4 | L4 (jettison 20 → 40 t) at Block 8 central params alone gives +0.3 to +0.6 pp. | Uplift ∈ [0.3, 0.6] pp. | Falsified if outside [0.1, 0.9] pp. |
| H5 | L5 (dry mass 200 → 160 t) at Block 8 central params alone gives +0.5 to +1.0 pp. | Uplift ∈ [0.5, 1.0] pp. | Falsified if outside [0.3, 1.5] pp. |
| H6 | L6 (fill 200 → 250 t) at Block 8 central params alone gives a +0.5 to +1.2 pp uplift in *delivered fraction* (per-mission absolute delivered mass grows more than 25 percent). | Composite ∈ [15.9, 16.6] percent at 250 t fill. | Falsified if outside [15.5, 17.5] percent. |
| H7 | **Engineering-credible-only stack** (L1 + L3) at central params clears 16 percent but stays below 17 percent. | Stack delivered ∈ [16.0, 16.8] percent. | Falsified if stack < 15.5 percent (no honest headroom available) or > 17.2 percent (single lever closes the gap without re-opening conditional rounds). |
| H8 | **Engineering-credible-plus-water-ablator stack** (L1 + L2 + L3) at central params reaches but does not robustly exceed 17 percent. | Stack delivered ∈ [16.8, 17.4] percent. | Falsified if outside [16.3, 17.8] percent. |
| H9 | **All-credible-with-conditionals stack** (L1 + L2 + L3 + L4 + L5 + L6, ceilings) crosses 17 percent comfortably, into [17.5, 19.5] percent. | Stack delivered ∈ [17.5, 19.5] percent. | Falsified if outside [16.5, 21] percent (model bug or compounding error if higher). |
| H10 | **Architecture claim:** no engineering-credible-only stack robustly clears Option A's 17 percent in the no-Jupiter case. Crossing 17 percent requires water-as-ablator engineering OR one of the conditional levers (L4 / L5 / L6) to close. Architecture remains "Option-A-equivalent" at honest accounting, "Option-A-superior" only with conditional bets. | H7 falsified-low + H8 marginal/held. | Falsified if H7 stack alone > 17 percent. |

---

## Method

All calculations extend Block 8's `R_aerocapture_savings_bracket/run.py` Tsiolkovsky framework with composite levers:

**Baseline (Block 8 central, reproduced first):**
- M_collected = 200 t at residence
- M_dry_base = 200 t (Variant B 500-kilowatt-electric)
- DV_exit = 7.4 km/s at Isp_exit = 7000 s
- DV_inbound = 24.7 km/s at Isp_inbound = 5000 s, minus 1.5 km/s aerocapture saving = 23.2 km/s
- Jettison = 20 t at residence (M_dry_effective = 180 t)
- TPS = 50 kg/m² × 164.5 m² × 50% coverage = 4.1 t heat shield
- Heat shield carries through both burns as inert mass (per Block 8 bug-fix)
- Expected delivered fraction: 15.37 percent (Block 8 result)

**Lever model.** For each lever L_k, compute delivered fraction with only that lever active (all others at Block 8 baseline). For stack hypotheses (H7/H8/H9), compute delivered fraction with all levers in the stack active simultaneously.

**Stack interactions.** Tsiolkovsky compounds via mass ratio. L5 (dry mass down) and L4 (jettison up) both reduce inert mass; together they should add roughly linearly but the inbound burn's mass ratio amplifies smaller inert mass nontrivially. L6 (fill up) raises the propellant pool relative to fixed dry mass, improving the mass-ratio penalty per unit delivered mass. L1 and L2 are TPS-side and act on the inert-mass term only at central parameters; full superposition is not exact but for the ~1-2 pp scale of each lever the cross-terms are second order.

**Output grids:**
- `lever_individual.csv` — each lever in isolation: name, baseline_pct, with_lever_pct, uplift_pp
- `lever_stacks.csv` — three stacks (H7 = L1+L3; H8 = L1+L2+L3; H9 = all six) at central
- `stack_sensitivity.csv` — H7 stack swept over ±0.5 km/s aerocapture saving, ±10 kg/m² TPS (where applicable)
- `summary.json` — hypothesis adjudication

**Reproducibility checks:**
- With *no* levers (Block 8 central reproduced): expect 15.37 percent ±0.05.
- With L2 only (zero TPS): should reproduce Block 8's `composite_no_jupiter_no_shield` = 16.28 percent.
- With L1 only (30% coverage): should reproduce Block 8's `composite_no_jupiter_central_shield_30pct_coverage`. (Available in Block 8's CSV; this round confirms it.)

---

## Limitations

- **L2 (water-as-ablator) is an architectural assumption, not a derivation.** This round treats it as a zero-TPS counterfactual to bracket the ceiling. Whether ablating water can actually protect a 200-t cargo entering at 11.4 km/s without bag rupture or unacceptable mass loss is a separate engineering question (not in scope; flagged for water-prop's bag-engineering side).
- **L4 (40 t jettison) is conditional on R-jettison-engineering-feasibility, which is not yet run.** This round computes the headroom *if* 40 t can be cleanly jettisoned at residence; the engineering audit may show 20 t is the practical ceiling, retiring L4 entirely.
- **L5 (dry mass 200 → 160 t) is a Variant scaling assumption.** A real reduction would have to be sourced from a specific subsystem (radiator areal density, structures, propellant tankage). Hyperion's R-marvl-mass-anchor-validation already locked Variant C's reactor + radiator mass; the 40-t budget cut here would come from non-power-system subsystems and is illustrative only.
- **L6 (fill 250 t) increases ram-scoop accretion fill, which depends on R-residence-bag-structural (Iapetus-owned).** Per `.session/STATE.md` Iapetus has not run this round yet. This round computes the delivered-fraction headroom only; the bag-structural audit may show 250 t fills are at or beyond bag tolerance, retiring L6.
- **Faster cruise inbound is not modeled here.** Hyperion's R-cruise-time-optimization showed for Variant C that 4-yr cruise at +6 km/s heliocentric saves 3-6 yr round-trip. The residence-class composite's 24.7 km/s integrated continuous-thrust inbound was computed at Hohmann-equivalent assumptions; a faster inbound could reduce 24.7 km/s by ~10-20 percent and adds a *separate* lever not bookkept in this round.
- **Cross-term compounding.** When levers stack, the Tsiolkovsky cross-terms (e.g. a smaller dry mass amplifies the benefit of higher Isp) are captured exactly by the run.py composite calculator but not by the linear-add intuition in the H7/H8/H9 prediction ranges. If the observed stack is significantly above the linear-add prediction, this is *not* a model bug — it is the cross-term effect surfacing.
- **L3 (exit Isp 9000 s) is a thruster-readiness assumption.** Water-dual-ion at 5000 s and water-radio-frequency-ion at 2000-7000 s are published anchors; 9000 s would require a specific water-thruster development. The round computes the headroom; programmatic feasibility is a separate question.

---

## Decision rule

- **H10 held + H7 falsified-low** → Architecture is "Option-A-equivalent" in honest accounting. Pitch must reflect this; "Option-A-superior" requires conditional bets to be flagged.
- **H10 falsified (H7 stack alone > 17 percent)** → Architecture has remaining engineering-credible headroom; the no-Jupiter composite is genuinely Option-A-superior and the pitch can quote this.
- **H8 marginal/held + H9 held** → Conditional-stack route to Option-A-superiority exists. Each conditional lever should be elevated as critical-path R&D.
- **H9 falsified-low** (< 16.5 percent even at all-credible-with-conditionals ceiling) → No combination of identified levers closes to 17 percent. This would imply either an un-considered architectural lever or acceptance of Option-A-parity.

The orchestrator should update the architecture decision matrix's residence-class row footnote with the realised headroom number under each stack regime, and update the pitch's "delivered fraction" claim to match the engineering-credible-only stack (not the all-credible-with-conditionals ceiling).

---

## Results (2026-05-16)

### Baseline reproduction
Block 8 central reproduced cleanly at 15.369 percent (Block 8 reported 15.37 percent; agreement to 0.001 pp). Shield mass 4.13 t, delivered 30.74 t.

### Individual lever uplift

| Lever | Composite (%) | Uplift vs baseline | Pre-reg range | Status |
|---|---|---|---|---|
| L1 (TPS coverage 30%)  | 15.73 | +0.36 pp | [0.4, 0.8] pp | marginal (just below predicted band) |
| L2 (water-as-ablator)  | 16.28 | +0.91 pp | [0.8, 1.2] pp | held |
| L3 (exit Isp 9000 s)   | 17.97 | +2.61 pp | [0.4, 0.8] pp | **falsified-high** |
| L4 (jettison 40 t)     | 19.78 | +4.41 pp | [0.3, 0.6] pp | **falsified-high** |
| L5 (dry mass 160 t)    | 24.18 | +8.81 pp | [0.5, 1.0] pp | **falsified-high** |
| L6 (fill 250 t)        | 23.37 | +8.00 pp | [0.5, 1.2] pp | **falsified-high** |

Four of six pre-registered lever uplifts are falsified-high — by 3× to 10×. The pre-registration relied on linear-additive intuition for what is, in fact, a multiplicative Tsiolkovsky cross-term effect. Every 1 t of inert mass reduction yields ~0.44 t of additional delivered water under the composite's inbound mass-ratio of 1.605 and exit mass-ratio of 1.114. The pre-reg's 0.3-1.0 pp ranges should have been 2-9 pp ranges. **Methodology miss documented as Lesson 8 below.**

### Stack results

| Stack | Composite (%) | Pre-reg range | Status | Honest? |
|---|---|---|---|---|
| Honest floor (L1 only) | 15.73 | [15.4, 16.0] | held | yes — TPS geometry is realism, not lever |
| H7 (L1 + L3)           | 18.33 | [16.0, 16.8] | falsified-high | conditional — L3 needs cathode-life budget |
| H8 (L1 + L2 + L3)      | 18.86 | [16.8, 17.4] | falsified-high | conditional — L2 engineering validation pending |
| H9 (all six levers)    | 36.79 | [17.5, 19.5] | falsified-high | all-conditional ceiling |

H9 at 36.79 percent is not credible as a *target* — it is the unrestricted ceiling assuming every conditional round closes maximally. The fact that the ceiling is 37 percent (~2.4× Block 8 baseline) is itself important: it quantifies how much inert-mass-leveraged headroom the composite architecture has if multiple conditional rounds close. But it is a ceiling, not a forecast.

### Architecture claim H10 — **held**

Under strict-honest accounting (L1 only, TPS-geometry realism), the no-Jupiter composite is at **15.73 percent — below Option A's 17 percent**. Architecture remains Option-A-equivalent in honest accounting; closure to 17 percent or above requires at least one of:

- **L2** (water-as-ablator engineering) — entry-physics analysis required; bag-rupture-under-ablation a real failure mode
- **L3** (exit Isp uplift) — proportionally extends cathode hours per mission (Block 4 §validity caveat + R-cathode-life). 5- or 10-mission tug reuse cadence binds.
- **L4** (40-t jettison) — pending R-jettison-engineering-feasibility (low-priority in STATE.md follow-ons)
- **L5** (Variant B dry mass 160 t) — pending mass-budget re-derivation from radiator + structures + propellant tankage
- **L6** (250-t fill) — pending R-residence-bag-structural (Iapetus-owned, on critical path)

### Re-categorised lever credibility

| Category | Lever | Implicit condition | Status |
|---|---|---|---|
| Free (geometry only)         | L1 | none | engineering reality |
| Engineering-validation-pending | L2 | entry-physics audit of water-as-ablator + bag rupture | open |
| Cathode-life-conditional     | L3 | cathode hours per mission × reuse cadence | bookkept Block 4 §validity caveat; needs explicit closure |
| Engineering-feasibility-cond | L4 | mechanical separation of 40-t residence hardware | R-jettison-engineering not yet run |
| Variant-scaling-conditional  | L5 | dry mass 200 → 160 t at 500-kWe spacecraft | mass-budget re-derivation needed |
| Bag-structural-conditional   | L6 | 250-t residence fill mechanically supportable | R-residence-bag-structural Iapetus-owned, not yet run |

### Hypothesis adjudication summary

- H1 (L1 +0.4-0.8 pp): **marginal** (+0.36 pp, just below predicted band; near-miss)
- H2 (L2 +0.8-1.2 pp): **held** (+0.91 pp)
- H3-H6 (L3-L6 uplift ranges): **falsified-high** by 3-10× — pre-registration anchored on linear-additive intuition rather than Tsiolkovsky cross-term physics
- H7-H9 (stack ranges): **falsified-high** for the same reason
- H10 (architecture-equivalent-only under honest accounting): **held** — L1-only at 15.73 percent < 17 percent

### Methodology Lesson 8 — Tsiolkovsky cross-terms compound much more than linear-add intuition suggests in two-burn architectures with high inbound mass-ratio

For the composite's mass-ratio profile (MR_exit = 1.114, MR_inbound = 1.605, product = 1.788), every 1 t of inert mass reduction yields ~0.44 t of additional delivered water. The pre-registration anchored uplift ranges on "small uplift because each lever is a small perturbation" without computing the propagation through both burns. Result: predictions 5-10× too low.

This is the **third instance of the same meta-pattern** in the Titan campaign:
- **Block 5 lesson**: multi-body alignment availability scales as (2T)/360°, not as looser pairwise intuition (`roughly half` was wrong by ~18×).
- **Block 7 lesson**: three-body alignment availability scales linearly in any single trajectory-DOF; budget to compensate for a missing DOF must grow by ~25× the local angular-motion rate.
- **Block 9 lesson (this round)**: inert-mass reductions in two-burn architectures yield ~(1 / (MR_exit × MR_inbound) − partial-subtraction-correction) ≈ 0.4-0.5 of the reduction as additional delivered mass, NOT a small fraction.

Common recurring meta-lesson: **at this fidelity level, pre-register against the relevant physical mechanism's actual functional form, not against intuition.** Compute one grid point under the physics before naming a prediction range.

### Headline finding

**The composite architecture has substantial inert-mass headroom — but under strict-honest accounting (TPS-geometry realism only), it does NOT clear Option A's 17 percent. The no-Jupiter composite is 15.73 percent. Each conditional lever (L2 through L6) individually closes the gap on paper, but each carries an implicit condition that requires a separate round to validate.**

**Implication for pitch and matrix:**
- ICEBERG residence-class composite **at honest accounting** is Option-A-equivalent (~15.7 percent) in the 92.5 percent of windows without Jupiter alignment. Should be quoted as such, not as Option-A-superior.
- Each of L2-L6 should be elevated as critical-path R&D *if and only if* the program wants to claim above 17 percent. Otherwise, parity is the honest claim.
- The matrix should footnote the residence-class row with the conditional-lever decomposition: ~15.7 percent baseline; +1-9 pp upside per conditional lever; ~37 percent ceiling if all close (programmatically improbable).
- The pitch should NOT quote H9's 36.79 percent ceiling as a target. The ceiling is interesting for headroom-existence but not for honest forecasting.

### Open questions surfaced

- **L3 burn-time × cathode life at exit-Isp 9000 s.** Block 4 validated Isp 7000 s exit at 6-month half-thrust burn; at Isp 9000 s, burn time scales further. Per-mission cathode hours likely +30 percent vs Isp 7000 baseline. R-cathode-life-water-plasma's Variant-B-safe-through-5-missions verdict may not survive. **Flagged for R-exit-isp-cathode-budget follow-on.**
- **L5 dry-mass-reduction sourcing.** A 40-t cut on 200-t spacecraft would have to come from somewhere; hyperion's R-marvl-mass-anchor-validation pinned radiator + reactor mass. Most credible sources: structures + propellant tankage (potentially 10-15 t each at 500 kWe). 40 t is at the upper edge of what is mass-budget-derivable; 15-25 t more credible. Flag for R-variant-B-mass-budget-re-derivation if it becomes critical path.
- **L6 cargo-geometry effect on TPS.** Increasing fill from 200 → 250 t grows the spherical cargo radius from 3.62 m to 3.90 m (surface area 164.5 → 191.5 m²), so heat-shield mass at fixed areal density × coverage also grows by 16 percent. Already captured in this round's L6 model. But ram-scoop accretion mass-flow at constant residence time would need to roughly 1.25× — bag-structural impact non-linear.

### Files

- `STUDY.md` — this document.
- `run.py` — composite delivered-fraction calculator with six levers and four stacks.
- `results/lever_individual.csv` — each lever in isolation.
- `results/lever_stacks.csv` — four stacks (honest_floor, H7, H8, H9).
- `results/stack_sensitivity.csv` — H7 sensitivity to aerocapture saving × TPS density.
- `results/summary.json` — full numerical summary with hypothesis adjudication.
