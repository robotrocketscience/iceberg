# R-cadence — Multi-ship-per-window cadence sensitivity on IRR

**Status:** pre-result.

## Question

R-NPV established that ICEBERG IRR is 3.6%–7.0% — sovereign-bond territory, not commercial-equity territory. R-NPV's cross-learning explicitly promoted this round: *"the single largest IRR lever is revenue cadence; 2x cadence → IRR rises ~1.5pp; 3x → ~3pp."*

That was an estimate. Question it. **Does multi-ship-per-window cadence actually raise IRR, or does it just scale absolute NPV?** First-principles concern: if we 2x cost AND 2x revenue with the same time profile, NPV doubles but IRR is unchanged. The only IRR-relevant change is the **ratio of fixed (NRE) costs to variable cashflow**, plus any **schedule compression** (faster total-fleet build = nearer-term revenue).

This round explores two distinct cadence interpretations:

1. **"Doubled cadence, larger fleet"** — N ships per launch event, total fleet over 45-year horizon scales with N. Same time profile per ship. NPV scales, but IRR may not.
2. **"Compressed schedule, constant fleet"** — same ~37 total ships, but launched at N ships per window, so fleet build completes by year 25 instead of year 41. Late-fleet revenue arrives 10–15 years earlier. IRR should rise meaningfully.

## Pre-registered hypothesis (H-cad)

**Aggregate (H-cad-agg):** Cadence is a meaningful but bounded IRR lever. Doubling the launch cadence under interpretation (1) raises IRR by less than 1pp (only the fixed NRE drag dilutes); under interpretation (2), schedule compression raises IRR by 1.5–3pp. **Even at 3x cadence with schedule compression, IRR remains under 10%** — ICEBERG does not cross the corporate-growth-equity hurdle. The R-NPV finding ("sovereign-class instrument") is not rescued by cadence alone.

**Pre-registered sub-claims** (best-case audited cell: $10k/kg + $2B sovereign yr 11 + commercial_mid; with perpetuity terminal value, growth 0%):

| Sub-claim | Predicted | Falsification threshold |
|---|---|---|
| H-cad-a — IRR at N=1 (baseline reproduction of R-NPV) | 6.97% ± 0.05% | outside ±0.2% |
| H-cad-b — IRR at N=2, larger-fleet flavor | 7.0–8.0% | outside ±0.5pp |
| H-cad-c — IRR at N=3, larger-fleet flavor | 7.0–8.5% | outside ±0.5pp |
| H-cad-d — IRR at N=2, compressed-schedule flavor | 8.5–10.0% | outside ±0.7pp |
| H-cad-e — IRR at N=3, compressed-schedule flavor | 9.5–11.5% | outside ±0.7pp |
| H-cad-f — IRR at N=5, compressed-schedule flavor | 10.5–13.0% | outside ±1.0pp |
| H-cad-g — Cells with positive NPV at 10% commercial discount, N=3 compressed, full sweep | 0–5 of 90 | held if 0–5; falsified if >5 |
| H-cad-h — Cells with positive NPV at 10%, N=5 compressed, full sweep | 5–25 of 90 | outside range |

**Aggregate decision rule:** if H-cad-g and H-cad-h both hold, the cadence lever is sub-critical for commercial-equity classification. If H-cad-h falsifies high (more cells positive than predicted), schedule-compressed N=5 cadence promotes ICEBERG to "regulated-utility-eligible," and the binding constraint shifts from financial structure to industrial-base constraint (reactor production rate, launch cadence).

## Method

Reuse the R-NPV / R15-rerun cashflow model. Modify `build_fleet_schedule()` to generate two cadence variants:

**Larger-fleet variant.** N ships per launch event, same window spacing (~1.08 years between events). Total fleet over horizon scales with N: 37 → 74 → 111 ships at N=1 → 2 → 3.

**Compressed-schedule variant.** Total fleet pinned to ~37 ships (the R-NPV baseline total). N ships per launch event but fewer events: e.g. N=2 means 19 events instead of 37; N=3 means 13 events; etc. All events front-loaded into years 0–18.

Per-ship cost, per-ship revenue, per-ship reactor era unchanged. Ground-ops scaled with fleet (linear, not optimistic-economies-of-scale).

Sweep:
- N ∈ {1, 2, 3, 5}
- Cadence flavor ∈ {larger_fleet, compressed_schedule}
- Discount rates as in R-NPV
- Best-case cell ($10k/kg + $2B sov yr 11 + commercial_mid) for primary IRR comparison
- Full price × sov × cost sweep at 10% commercial discount for H-cad-g/h

**Validity caveats:**
- Reactor production at N=3+ requires a sustained 3+ reactors/year cadence — TRL and industrial-base risk not modeled here. Treated as exogenous.
- Launch vehicle availability at N=3+ requires multiple vehicle classes per window — physically possible (SpaceX manifests support this) but contractually non-trivial.
- Per-window grappling traffic at Saturn: B-ring chunk inventory is essentially unlimited at the per-mission scale; no traffic cap modeled.
- Ground-ops scale linearly. Real economies-of-scale would shift IRR slightly upward.
- Per-ship NRE assumed amortized over the first ship only; no per-ship-class re-NRE for upgraded reactor eras. Optimistic.

## Result

### IRR vs cadence (best-case audited cell)

| Flavor | N ships per event | Total fleet | IRR (no TV) | IRR (with perpetuity TV) | NPV at 8% with TV ($B) | Undisc. break-even |
|---|---:|---:|---:|---:|---:|---:|
| larger_fleet | 1 | 37 | 3.63% | 6.97% | −1.62 | year 40 |
| larger_fleet | 2 | 74 | 3.70% | 7.05% | −2.92 | year 40 |
| larger_fleet | 3 | 111 | 3.72% | 7.07% | −4.22 | year 40 |
| larger_fleet | 5 | 185 | 3.74% | 7.09% | −6.83 | year 40 |
| compressed_schedule | 1 | 37 | 3.63% | 6.97% | −1.62 | year 40 |
| **compressed_schedule** | **2** | **37** | **5.26%** | **7.52%** | **−1.36** | **year 36** |
| compressed_schedule | 3 | 37 | 2.66% | 2.66% | −7.71 | year 34 |
| compressed_schedule | 5 | 37 | −1.45% | −1.45% | −10.87 | never |

### Positive-NPV cell counts under high-cadence compressed schedule

| Variant | Cells NPV+TV > 0 at 8% | Cells NPV+TV > 0 at 10% |
|---|---:|---:|
| N=3 compressed | 0 / 90 | 0 / 90 |
| N=5 compressed | 0 / 90 | 0 / 90 |

### Hypothesis grading

| Sub-claim | Predicted | Measured | Verdict |
|---|---|---|---|
| H-cad-a — IRR at N=1 (baseline) | 6.97% ± 0.05% | 6.97% | **held** |
| H-cad-b — IRR at N=2, larger_fleet | 7.0–8.0% | 7.05% | **held at lower edge** |
| H-cad-c — IRR at N=3, larger_fleet | 7.0–8.5% | 7.07% | **held at lower edge** |
| H-cad-d — IRR at N=2, compressed | 8.5–10.0% | 7.52% | **falsified low** |
| H-cad-e — IRR at N=3, compressed | 9.5–11.5% | 2.66% | **load-bearing falsified — wrong direction** |
| H-cad-f — IRR at N=5, compressed | 10.5–13.0% | −1.45% | **load-bearing falsified — wrong direction** |
| H-cad-g — N=3 compressed, cells positive at 10% | 0–5 of 90 | 0 / 90 | **held** |
| H-cad-h — N=5 compressed, cells positive at 10% | 5–25 of 90 | 0 / 90 | **falsified-conservative** |

**Aggregate H-cad-agg held** (cadence is not the lever that promotes ICEBERG to commercial-equity class) — but for an entirely different reason than predicted. Cadence is not just bounded; it is **anti-optimal at high values under realistic reactor-roadmap assumptions**. The pre-registered hypothesis treated cadence and reactor era as orthogonal axes; they are not.

## Reading

**The load-bearing finding is one I did not pre-register and explicitly got wrong:** compressing the launch schedule removes access to the late-era megawatt-class reactor. In the R15-rerun cashflow model, ships 25–37 launch in years 25–41 and use the megawatt reactor (588 tonnes delivered each). When the schedule is compressed to N=3 ships per event, all 37 ships launch in years 0–12 — exclusively in the Kilopower (7 t each) and Fission Surface Power (42 t each) reactor eras. The fleet's total deliverable mass collapses from ≈ 7,300 t (1×K + 5×FSP + 3×stretch + 5×sub-MW + 23×MW under R15-rerun) to ≈ 1,500 t under N=3 compressed (1×K + 5×FSP + 31×stretch). Per-ship capex scarcely changes, but per-ship revenue collapses by 2–4×. Capex outruns revenue regardless of how fast you launch.

The N=2 compressed case is the sweet spot — schedule still extends to year ~18, ships pick up some FSP and some sub-megawatt-class reactors, IRR rises from 6.97% → 7.52%. That is the **maximum achievable IRR improvement from cadence alone** under the R15-rerun reactor roadmap: **+0.55 percentage points**, not the +1.5–3 pp R-NPV's cross-learning estimated.

Larger-fleet flavor (scale fleet with N, same time profile) raises IRR by 0.10 pp at N=5. Confirms the first-principles concern that scaling cost AND revenue with the same shape barely moves IRR — the only relief is dilution of fixed NRE drag, which is small ($500M against $20–80B fleet capex).

**The strategic implication is sharper than R-NPV's read.** The IRR-improving lever is not cadence per se — it is **reactor-roadmap acceleration**. If the megawatt-class reactor arrived at year 8 instead of year 20, more ships across the entire fleet would deliver megawatt-era chunk masses. Reactor-roadmap timing is exogenous to ICEBERG (it depends on STMD / DOE / DOD funding posture toward Kilopower → Fission Surface Power → MMR-class), but it is the single highest-leverage external dependency for ICEBERG's IRR.

This makes the **A-REACTOR risk in the program register a much sharper financial concern than its current L4-I3 = 12 score implies**. A-REACTOR is not just a schedule risk; it is the dominant determinant of the project's discount-rate-bearing financial profile.

## Revisit

- **The pre-registered hypothesis was wrong about the mechanism.** I treated cadence and reactor era as orthogonal levers and predicted compressed-schedule cadence would monotonically improve IRR by 1.5–3 pp. Reality: at N≥3 compressed, IRR collapses below baseline. Wrong direction, large magnitude. The mechanism I missed: schedule compression denies late-launching ships access to later-era reactors.
- **The R-NPV cross-learning estimate ("2x cadence → IRR rises ~1.5pp") was wrong by 3×.** Actual maximum lift is ~0.55pp (N=2 compressed). R-NPV's STUDY.md should be updated to flag this, and the verdict-block claim "cadence promotes ICEBERG to regulated-utility-eligible" was premature speculation that R-cadence falsifies.
- **A new and better-targeted round is needed: R-reactor-roadmap.** What does the IRR curve look like if megawatt-class reactor arrival is exogenously varied from year 8 to year 30? At what arrival year does IRR cross 8%? 10%? Pre-register: I expect megawatt-at-year-8 to push IRR to 9–10% under N=1 schedule, possibly higher under N=2 compressed.
- **Methodology lesson:** in any future cashflow round, reactor-era assignments must be a free axis, not coupled to schedule via a launch-year function. R15-rerun's `reactor_era_for_launch_year()` is convenient but conceals a load-bearing assumption.

## Cross-learning

- **Decision-supporting (negative):** cadence is not the IRR lever R-NPV's cross-learning suggested. Drop "2x ships per launch window would raise IRR ~1.5pp" from any future deck or pitch. Maximum achievable IRR lift from cadence alone is +0.55pp at N=2 compressed; higher cadences are anti-optimal under the current reactor roadmap.
- **Decision-supporting (positive):** the dominant exogenous IRR lever is reactor-roadmap timing. Promote A-REACTOR risk from L4-I3 = 12 to L4-I4 = 16 in the program register; it is a financial-existence concern, not just a schedule concern.
- **Promotes R-reactor-roadmap as next round.** If reactor arrival year is the dominant lever, parameterize it explicitly. Pre-register IRR vs MW-reactor-arrival-year curve.
- **R-cadence = R15c (queued).** The R15-rerun cross-learning naming "R15c queued" is satisfied by this round; close that thread.
- **Methodology lesson #6:** "X is the largest lever" claims based on first-principles intuition are no substitute for actually running the sweep. R-NPV's cross-learning made a confident prediction that this round falsified by 3× and in the wrong direction at N≥3. Pre-register and run before promoting a lever.
- **Risk register update.** Promote A-REACTOR to L4-I4 = 16. ICEBERG IRR is dominated by reactor-roadmap timing more than by any propulsion or business lever the company directly controls.

