# R-solar-thermal-hybrid-power — STUDY (pre-registration; closed-loop reframe)

**Worker:** hyperion (re-spawn 2). **Date:** 2026-05-26. **Status:** pre-registration frozen; model pending.
**Round type:** focused architecture-physics check answering the SCOPE's decision gate ("is hybrid worth the framework structural change?") BEFORE committing the invasive `VehicleState`/executor refactor.

**Question (SCOPE):** does a hybrid reactor + solar-array architecture (e.g. 10 kWe reactor + 20 kWe LEO-equivalent solar) move ICEBERG closure thresholds enough to justify making `power_available_kwe` a location-dependent derived quantity across `VehicleState` + every phase executor + the sweep axes?

## The reframe the SCOPE could not have

The SCOPE (2026-05-21) predates titan-6's closed-loop refactor. The Saturn closed-loop closure inventory is now **0/150**, bound by the **powerplant mass-floor** (vehicle lighter than its own reactor) and reactor lifetime — both *static* / *cumulative* constraints, not inbound-thrust-authority constraints. The hybrid's benefit (the project owner's real insight) is **dial-up thrust on the inbound approach** as the spacecraft nears the sun. So the load-bearing question becomes: **is the binding constraint inbound-thrust-limited?** If not, the hybrid does not move closure, and the invasive refactor is not justified for the closure verdict (it may still have conops/fidelity value).

## Physics the verdict turns on (stated up front)

Power → thrust via F = 2P/vₑ (framework convention). For a fixed inbound Δv and Isp, **propellant is fixed by Tsiolkovsky and is independent of power**; more power buys **shorter burn time** (higher thrust), not less propellant. So the hybrid's dial-up can only help:
- **round-trip time** (L0-05 ≤ 15 yr) — by shortening burn time, and
- **cumulative reactor burn hours** (reactor-lifetime constraint),

and ONLY on the fraction of the inbound Δv spent close enough to the sun for the solar array to contribute. The bulk of the inbound Δv (Saturn-departure spiral, outer cruise braking) is spent at 5–9.5 AU where a 20-kWe-at-1-AU array delivers 0.2–0.8 kW — negligible against a 10-kWe reactor. The dial-up only bites on the final Earth-capture spiral near 1 AU, a small Δv fraction. **It does nothing for the mass-floor kill (a static mass constraint).**

## Pre-registered hypotheses

| # | Hypothesis | Predicted | Falsification |
|---|---|---|---|
| H1 | Solar contribution is negligible (<10% of reactor power) for the majority of the inbound Δv: at ≥2.7 AU (Saturn, Jupiter, belt) a 20-kWe-at-1-AU array gives ≤2.7 kW vs a 10-kWe reactor. | solar < 10% of total power for the Δv spent beyond ~2 AU | Falsified if solar ≥ 25% of total power across the majority of inbound Δv. |
| H2 | Total inbound burn-time / cumulative-reactor-hours reduction from the hybrid vs reactor-only is **modest (<25%)**, because only the near-Earth Δv fraction is sped up. | inbound burn-time reduction < 25% | Falsified if hybrid cuts inbound burn time ≥ 40%. |
| H3 | The hybrid does NOT change the closed-loop closure verdict: Saturn is 0/150 on the **mass-floor + reactor-lifetime** axes, which the inbound power profile does not relieve (mass floor static; lifetime helped only marginally per H2). | closure surface unchanged (still 0 at conservative anchors) | Falsified if modeling hybrid power flips ≥1 cell to closing at conservative anchors. |
| H4 | The hybrid's real value is **inner-system / NEA** (where solar dominates anyway, per this session's NEA round) and **conops thrust-authority on final approach**, not Saturn closure. | hybrid value is inner-system + conops, not Saturn closure | Falsified if the hybrid is shown to be load-bearing specifically for Saturn closure. |
| **H5 (load-bearing / decision gate)** | The invasive location-aware-power refactor (VehicleState two-field split + per-executor recompute + new sweep axes) is **NOT justified by the closure verdict** under the closed-loop framework. A documented location-aware power *function* (cheap, local to the inbound burn-time accounting) suffices to capture the dial-up effect for conops/round-trip without re-plumbing every executor. | refactor not justified for closure; lightweight power(r) function suffices | Falsified if the closure surface moves enough that per-executor power gating changes feasibility. |

### Honest prior
I expect H1–H5 to hold and the round to recommend: **do NOT do the full invasive refactor for closure's sake.** Model the dial-up as a local power(r) function in the inbound burn-time accounting (for round-trip / reactor-hours fidelity and conops), and record that the hybrid's genuine architectural home is the inner-system / NEA arm where solar already dominates. Same recurring lesson: check whether the proposed change touches the binding axis before paying for it.

## Anchors
- Inbound continuous-thrust Δv ≈ 27.56 km/s (R-all-electric-thruster-sweep high-elliptical Saturn departure + lunar-GA mid-case); Isp 2000 s (RF-ion, bet-2 audit).
- F = 2P/vₑ; burn_s = m_prop·vₑ/F = m_prop·vₑ²/(2P) (framework `electric_burn_hours`).
- Solar 1/r²; 20 kWe at 1 AU. Reactor 10 kWe constant. Distances per SCOPE worked example (Saturn 9.5, Jupiter 5.2, belt 2.7, Mars 1.5, Earth 1.0 AU).
- Closed-loop Saturn = 0/150 (titan-6); mass-floor + reactor-lifetime binding.

## Deliverables
STUDY.md → run.py (location-aware power + segmented inbound burn-time model) + results → RESULTS.md (H1–H5 + refactor recommendation) → READING.md → handoff. Focused model, not the full framework refactor (which is the decision this round informs).
