# R-composite-burn-time-closure

**Worker:** titan (Block 11)
**Owner:** project owner / orchestrator
**Pre-registration date:** 2026-05-16
**Predecessor:** R-exit-burn-power-audit (Block 10)

---

## Motivation

Block 10 found that Block 4's composite exit burn at 500 kilowatt-electric / Isp 7000 takes 8.92 years vs the 6-month residence dwell budget. Quick check on the inbound burn:

```
Inbound at 500 kilowatt-electric / Isp 5000 / 23.2 km/s / 345 t / efficiency 0.65:
  thrust 13.26 N, mass ratio 1.605, propellant 130 t, burn time 15.24 years.
```

The Hohmann Saturn-Earth cruise is ~6 years. **The inbound burn is also un-closed at the assumed 500 kilowatt-electric.** So Block 4's composite has TWO un-closed burn-time problems, not just one. Block 10 surfaced exit; this round audits the inbound and finds the joint (power, Isp_exit, Isp_inbound) closure regime — and the delivered fraction at that regime.

The question this round answers: **at what (power, Isp_exit, Isp_inbound) does the residence-class composite close both burns within their time budgets, AND what is the delivered fraction at that closure?** If no regime closes both burns AND delivers above Block 4 A1 baseline (3.9 percent), the architecture is structurally dead in burn-time terms — independent of any further analysis.

---

## Pre-registered hypotheses

| # | Hypothesis | Prediction | Falsification rule |
|---|---|---|---|
| H1 | At 500 kilowatt-electric, no (Isp_exit, Isp_inbound) combination closes both burns within their time budgets (exit ≤ 6 months, inbound ≤ 6 years) AND delivers > Block 4 A1 baseline (3.9 percent). | No closure regime at 500 kilowatt-electric. | Falsified if any combination closes both burns AND delivers > 6 percent. |
| H2 | At 500 kilowatt-electric, the (Isp_exit, Isp_inbound) combination that closes both burns within time budgets is Isp_exit ≤ 1000 s AND Isp_inbound ≤ 2000 s — i.e. chemical-equivalent for exit and Variant-B-equivalent for inbound. At this regime, delivered fraction is < 8 percent (below Block 4 A1+A5 baseline). | Closure regime at Isp_exit ≤ 1000 s / Isp_inbound ≤ 2000 s; delivered fraction in [3, 8] percent. | Falsified if closure regime is at Isp_exit > 2000 s or Isp_inbound > 3000 s, OR if delivered fraction > 10 percent. |
| H3 | Minimum power that closes both burns at delivered-fraction-optimal Isp (Isp_exit 7000 / Isp_inbound 5000) is 5-15 megawatt-electric. | Min power for joint closure at optimal Isp ∈ [5, 15] megawatt-electric. | Falsified if outside [2, 25] megawatt-electric. |
| H4 | At 1 megawatt-electric (mid-tier between Variant B's 500 kilowatt-electric and the megawatt-class regime), there is a (Isp_exit, Isp_inbound) combination that closes both burns. Delivered fraction at this regime is 8-14 percent. | 1 megawatt-electric closure regime exists; delivered fraction ∈ [8, 14] percent. | Falsified if no closure at 1 megawatt-electric OR if delivered fraction outside [5, 18] percent. |
| H5 | **Architecture verdict.** The residence-class composite architecture has a structural power-class-vs-delivered-fraction trade: at 500 kilowatt-electric, no high-delivered-fraction regime closes burn time; closure requires either (a) megawatt-class power (locked-memory-Bayesian-unlikely), (b) very low Isp (delivered fraction collapses), or (c) architectural reframe (spiral-out during cruise, separate round). Block 4 / Block 5 / Block 8 / Block 9 delivered-fraction headlines are all conditional on Path (a) or Path (c). | Joint outcomes: H1 held, H3 held, H4 marginal. | If H1 falsifies (500 kilowatt-electric has a closure regime above baseline), architecture is saved at the assumed power class. |

---

## Method

**Variables.**
- exit_power, inbound_power (megawatt-electric): assumed equal (single reactor); sweep [0.5, 1, 2, 5, 10] MWe.
- exit_isp, inbound_isp (s): independent sweep [1000, 2000, 3000, 5000, 7000, 9000].
- efficiency: 0.65 canonical (sensitivity at 0.30 reported).
- mass_at_exit = 380 t (200 collected + 180 dry-effective after 20 t jettison).
- mass_after_exit = 380 / MR_exit (depends on Isp_exit and dv_exit = 7.4 km/s).
- dv_exit = 7.4 km/s (Block 4); dv_inbound_net = 23.2 km/s (24.7 minus 1.5 aerocapture).
- residence_dwell_budget = 6 months; cruise_budget = 6 years (Hohmann Saturn-Earth).

**Closure rule.** For each (power, Isp_exit, Isp_inbound) cell, compute:
- exit_burn_time and exit_closure_flag (≤ 6 months)
- inbound_burn_time and inbound_closure_flag (≤ 6 years)
- delivered_fraction (Tsiolkovsky with both burns, including shield mass at 4.13 t)

A cell *closes* if both flags are true. Among closing cells, find max delivered fraction.

**Outputs.**
- `results/closure_grid.csv` — (power, Isp_exit, Isp_inbound) × (exit_time, inbound_time, closes?, delivered).
- `results/closing_cells.csv` — only the rows where both burns close.
- `results/max_delivered_per_power.csv` — at each power class, max delivered fraction among closing cells.
- `results/summary.json` — hypothesis adjudication and architecture verdict.

---

## Limitations

- **Equal exit and inbound power.** Real spacecraft has a single reactor sized for both burns. Real exit burn could conceivably use a separate higher-power supplemental source (chemical augmenter, fission battery). This round assumes a single power class for both burns; a follow-on can audit augmenter architectures.
- **Constant power throughout each burn.** Real power supply has a startup/shutdown curve and possible thermal-management throttling. Ignored.
- **Fixed cruise time of 6 years.** Hyperion's R-cruise-time-optimization showed faster cruise (4 yr) is round-trip-optimal for Variant C. The residence-class composite would benefit from re-derivation under non-Hohmann cruise — but only if cruise time is the binding constraint. At 500 kilowatt-electric, both exit (8.9 yr) and inbound (15.2 yr) burns exceed any plausible cruise time, so cruise reshape isn't the resolution.
- **No spiral-out resolution.** Path (d) from Block 10 — exit burn spans cruise leg — is not modeled here; flagged for separate round R-spiral-out-exit-architecture.
- **Single-reactor mass assumption.** Block 4's 200 t dry mass assumes Variant B 500-kilowatt-electric reactor. Scaling to 1-10 megawatt-electric increases dry mass substantially (per locked memory: radiator alone is 40-55 percent of megawatt-class system mass per MARVL). This round holds dry mass constant at 200 t for simplicity, knowing that the megawatt-class closure rows are optimistic by an unknown factor on delivered fraction. A proper megawatt-class composite re-derivation is a follow-on round.

---

## Decision rule

- **H1 held + H5 held** → composite as-Block-4-framed has no burn-time-closing regime at 500 kilowatt-electric. Architecture's headline delivered fraction is conditional on Path (a) or Path (d).
- **H1 falsified** → some (Isp_exit, Isp_inbound) combination saves the composite at 500 kilowatt-electric. Block 9's verdict survives; pitch can still quote the honest-floor number.
- **H4 held** → 1 megawatt-electric regime exists and delivers 8-14 percent. This is the "moderate-mid-tier" answer; pitch can quote conditional-on-1-MWe rather than requiring full megawatt-class.
- **H3 held + H4 falsified-low** → closure requires full megawatt-class (5-15 MWe). Architecture inherits Fission Surface Power Phase 2 dependency (locked memory: not awarded).

---

## Results (2026-05-16)

### Headline numbers

| Power class | Joint closure regime exists? | Max delivered fraction (naive, no mass-scaling) | Best Isp combination |
|---|---|---|---|
| **500 kilowatt-electric** (Block 4 assumed) | **NO** | 0 (architecture broken) | n/a |
| 1 megawatt-electric | yes, but only at Isp_exit=Isp_inbound=1000 s | 0.00% (mass closure fails) | 1000 / 1000 |
| 2 megawatt-electric | yes, only Isp 1000 / 1000 | 0.00% (mass closure fails) | 1000 / 1000 |
| 5 megawatt-electric | yes, at multiple Isp combinations | **22.76%** | 3000 / 9000 |
| 10 megawatt-electric | yes, at delivered-fraction-optimal Isp | **40.51%** | 7000 / 9000 |

The 500-kilowatt-electric verdict is the headline: **Block 4's composite is structurally broken at the assumed power class. There is no Isp combination at 500 kilowatt-electric that closes both burns AND delivers any positive water mass.** The architecture cannot operate at the Variant-B-equivalent power class.

### Why 500 kilowatt-electric is fully broken

At 500 kilowatt-electric, every (Isp_exit, Isp_inbound) cell falls into one of two regimes:

- **High-Isp regime (Isp ≥ 2000 s):** Tsiolkovsky-favourable for delivered fraction but burn time is too long (exit > 6 months, inbound > 6 years). Doesn't close.
- **Low-Isp regime (Isp ≤ 1500 s):** Burn time is short enough to close, but mass ratio is high enough that propellant consumption exceeds the (collected + dry) wet mass. Delivered fraction goes negative.

There is no intermediate Isp at 500 kilowatt-electric where both burns close AND delivered fraction is positive. The architecture is structurally dead at this power class.

### Closure at megawatt-class is delivered-fraction-favourable — but unrealistic without mass-scaling

The grid surfaces a striking pattern: at 10 megawatt-electric with Isp_exit 7000 / Isp_inbound 9000, naive delivered fraction is **40.51 percent** — much higher than Block 4's 21.8 percent or Block 9's 15.73 percent honest floor. The reason: at higher power, burn time fits even at delivered-fraction-optimal high Isp (especially the inbound, where Isp 9000 gives mass ratio 1.30 instead of Block 4's 1.60).

**However: this naive number does not account for the megawatt-class spacecraft dry-mass scaling.** Block 9's analysis held dry mass at 200 t (Variant B 500-kilowatt-electric). At 5-10 megawatt-electric, the spacecraft dry mass is substantially higher: per locked-memory ICEBERG power findings 1-4:
- Radiators alone are 40-55 percent of megawatt-class system mass (MARVL anchor).
- Reactor + shield is 25-35 percent at 1 megawatt-electric.
- 40-watts-per-kilogram specific-power target is TRL-2.

A naive scaling: 200 t at 500 kilowatt-electric ≈ 400 watts-per-kilogram (50% of payload mass is propulsion). At 40 watts-per-kilogram (locked-memory optimistic), 10 megawatt-electric requires 250 t for power system alone, plus structures + jettison + tankage. A megawatt-class composite likely has 500-1000 t dry mass, not 200 t.

If dry mass scales to 500 t at 10 megawatt-electric (mid estimate), the composite delivered fraction at Isp_exit 7000 / Isp_inbound 9000 / 200 t collected / 500 t dry:
- mr_e = 1.114; m_post_exit = (200 + 500) / 1.114 = 628.4 t
- mr_i = 1.301; m_at_earth = 628.4 / 1.301 = 483.0 t
- m_delivered = 483.0 − 500 = **−17 t (architecture fails to close on dry-mass terms)**.

At dry mass 400 t (more aggressive scaling): m_at_earth = 538.6, m_delivered = 138.6, delivered fraction = 69%. But that's only if 400 t is feasible at 10 megawatt-electric, which locked memory says it isn't.

**The real megawatt-class composite delivered fraction is unknown without an explicit reactor + radiator + structures mass scaling per locked-memory ICEBERG power findings.** Naive 40.51 percent is an upper bound; the realistic number is probably 0-20 percent depending on mass-scaling pessimism.

### Hypothesis adjudication

| Hyp | Prediction | Observed | Status |
|---|---|---|---|
| H1 (no closure above baseline at 500 kilowatt-electric) | no closure > 3.9% | no closure at all | **held (strongly)** |
| H2 (low-Isp closure at 500 kilowatt-electric, df < 8%) | low-Isp closure exists, df ≤ 8% | low-Isp does NOT close at 500 kilowatt-electric (worse than predicted) | falsified-direction (no low-Isp closure) |
| H3 (min power for optimal-Isp closure 5-15 MWe) | [5, 15] MWe | 10 MWe at Isp 7000/5000 | **held** |
| H4 (1 MWe closure at 8-14%) | [8, 14]% | 0% (low-Isp only) | **falsified** |
| H5 (composite conditional on megawatt or reframe) | held | held | **held** |

H2's "falsified-direction" is itself important: even chemical-equivalent Isp doesn't save the architecture at 500 kilowatt-electric. Mass closure fails in addition to burn-time closure. The architecture is *more* broken at 500 kilowatt-electric than I pre-registered.

### What this means for the Titan campaign

**Block 4's composite architecture has TWO load-bearing closure conditions that were flagged but never numerically audited:**

1. **Exit burn fits 6-month residence dwell** — falsified by Block 10 (8.92 yr at 500 kilowatt-electric).
2. **Inbound burn fits ~6-year cruise** — falsified by this round (15.24 yr at 500 kilowatt-electric / Isp 5000).

**Combined:** the residence-class composite at Block 4's assumed 500 kilowatt-electric has NO valid operating point. The architecture is structurally dead at this power class.

The remaining resolution paths from Block 10 narrow further:

| Path | Status after Block 11 |
|---|---|
| (a) Megawatt-class residence power | Requires ≥ 5 MWe. Naive delivered fraction 22-40 percent, BUT realistic delivered fraction at megawatt-class dry-mass scaling per locked memory is likely 0-20 percent. Architecture inherits Fission Surface Power Phase 2 dependency that locked memory says has 0-of-6 base rate. **Plausible only with explicit megawatt-class mass-scaling round.** |
| (b) Extend residence + cruise to ~15 years | Mission duration would be 30+ years; far beyond L0-05 ceiling. **Retired.** |
| (c) Revert Isp to chemical-equivalent | Mass closure fails at 500 kilowatt-electric. **Retired by this round.** |
| (d) Spiral-out exit during cruise | Not modeled. Most-likely-to-save path. **Critical-path follow-on.** |

The Block 4 / 5 / 6 / 7 / 8 / 9 delivered-fraction headlines (21.8%, 15.97%, 15.79%, 15.73%) are all conditional on Path (a) closing favourably with proper mass scaling, OR Path (d) closing favourably with a different architecture.

### Methodology lesson 8, instance #5

Pre-registered H4 (1 MWe closure at 8-14 percent delivered) was wrong because I didn't compute the (mass-closure, burn-time-closure) joint constraint. At 1 megawatt-electric, low-Isp closure exists for burn time but mass closure fails; high-Isp closure exists for mass but burn time exceeds budget. Pre-reg should have computed *both* constraints together before naming a delivered-fraction range.

Same root cause as Lesson 8 from Block 9 and Block 10: predict against the physics, not against intuition. Adding instance count.

### Follow-on rounds (re-priorities)

1. **R-spiral-out-exit-architecture** (critical-path, was Block 10 follow-on, now elevated). If Path (d) closes, the architecture is rescued. If not, the composite is structurally dead at any plausible power class.
2. **R-megawatt-composite-with-mass-scaling** (new, critical-path). Re-derive delivered fraction at 5-10 megawatt-electric with proper reactor + radiator + structures mass scaling per locked-memory ICEBERG power findings. Likely outcome: realistic delivered fraction 0-20 percent at megawatt-class, not the naive 40 percent.
3. **R-megawatt-vehicle-cost-vs-delivered-fraction** (new). Even if megawatt-class architecture closes, vehicle development + deployment cost is dramatically higher than Variant B 500-kilowatt-electric. Economic case may collapse even at favourable delivered fraction. Cross-references locked-memory finding 2 (0-of-6 fission base rate) for Bayesian-prior risk-adjustment.

### Files

- `STUDY.md` — this document.
- `run.py` — joint burn-time + delivered-fraction calculator across (power, Isp_exit, Isp_inbound).
- `results/closure_grid.csv` — full 180-cell grid.
- `results/closing_cells.csv` — 59 closing cells.
- `results/max_delivered_per_power.csv` — best delivered fraction per power class among closing cells.
- `results/summary.json` — hypothesis adjudication.
