# R-staged-commitment-gates-frame-B-interaction — SCOPE

**Author:** rhea (worker session, iceberg-rhea-2 branch).
**Date:** 2026-05-15 (latest+8, fifth round this sitting; queued from R-clearing-price-tail-integration-decision-frame and R-heterogeneous-cadence).

## Goal

Quantify how Frame B P(NPV>0) — "conditional on technical closure, integrated over R-LEO-water-demand-curve clearing-price distribution" — shifts when the program is structured under staged-commitment accounting (R-heterogeneous-cadence Regime R, full-chunk 200 t demonstrator + gated fleet build-out at P_demonstrator_success = 0.90) instead of upfront-fleet-capital accounting.

This is the financing-mechanism question for the anchor investor's pitch posture: ICEBERG as a capital sleeve gated by demonstrator flights, with kill criteria at each gate (per the locked anchor-investor framing). The matrix and pitch currently cite Frame B = 29% at sovereign-bond 3% LR=0 (round 11 anchor); the demand-curve MC actually reports 42.8% at sovereign-bond 3% LR=15. This round asks where staged commitment lands.

## What this round does

1. Re-runs the R-LEO-water-demand-curve clearing-price MC (10,000 samples; same log-normal Starship × markup parameters) over E_500kWe_200t configuration under two accounting regimes:
   - Regime D (upfront fleet capital, the demand-curve baseline).
   - Regime R (staged: mission 1 ship + ground systems committed at year 0; fleet capex deferred to year RT_1 + 0.5 and probability-gated by P_demonstrator = 0.90).
2. Sweeps WACC ∈ {0%, 3% sovereign-bond, 8.7% corporate-growth} × LR ∈ {0%, 15%}.
3. Sweeps launch count ∈ {1, 2, 3} per round 12's specific-power × m_LEO mapping (1-launch requires sp ≥ 11 W/kg; 2/3-launch closes at sp ≥ 8 W/kg; the conjunction posterior multiplier differs per round 9 H2a uniform-prior).
4. Computes Frame A (full-chain expected NPV including conjunction multiplier) and Frame B (conditional on technical closure) per cell.
5. Reports the demonstrator-NRE fraction of total program capex under staged commitment — the "option price" the gate-1 investor pays.

## What this round does NOT do

- Does NOT re-derive trajectory or propulsion physics. Inherits H2a min-point closure-cell parameters (chunk 200 t, RT 14.5 yr, delivered 80 t per R-fleet-ramp-NPV baseline; flagged parameter ambiguity vs Option A's 17% delivered, see R-heterogeneous-cadence STUDY §"Caveat for methodology lesson #8").
- Does NOT model heterogeneous launch counts within a program (demonstrator and fleet use the same launch count).
- Does NOT model heterogeneous chunk sizes (R-heterogeneous-cadence proved chunk-shrinking is a strictly dominated decision; mission 1 chunk stays at 200 t).
- Does NOT model multi-gate (only the mission-1 gate is gated; missions 2..N are committed together post-gate). R-multi-gate-staged-commitment is a separate Priority-2 queued round.
- Does NOT model salvage value on demonstrator failure (R-heterogeneous-cadence Priority-2 thread, deferred).
- Does NOT vary P_demonstrator_success outside the 0.90 baseline; per R-heterogeneous-cadence H-7, lower P_success INCREASES the staged-commitment improvement (option-value-of-abandoning), so 0.90 is the conservative anchor.

## Why now

Round 11 established three decision frames and identified Frame B as the load-bearing framing for venture-class capital evaluating ICEBERG conditional on technical closure. Round 12 found 2-launch is Frame A optimum. Neither round composed the Frame B math with the staged-commitment structure from R-heterogeneous-cadence — that's load-bearing for the pitch's "demonstrator-then-gate" framing in axis 17.

The anchor-investor belief (locked, `76fd04cdba8b2c3b`) describes ICEBERG as gated demonstrator flights with kill criteria at each gate. The matrix's pitch posture should reflect Frame B under staged commitment, not Frame B under upfront commitment. This round produces the number.
