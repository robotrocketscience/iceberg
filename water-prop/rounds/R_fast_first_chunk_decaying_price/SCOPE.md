# R-fast-first-chunk-decaying-price — the project-owner fleet hypothesis, re-tested under R188's decaying clearing price

**Status:** SCOPE pre-registered 2026-07-21, before `run.py`. Bounds from `scope_bounds.py`, committed alongside.
**Worker:** worktree-115637 session. Re-opens the project-owner USER-NOTES hypothesis (`design-axes/02-surviving-cell.md` lines 18-20) that `R_heterogeneous_cadence` (rhea, 2026-05-15) tested and falsified — but under a **static** clearing price, which that round's own SCOPE flagged as a deferral: *"Does not model time-evolution of clearing price."* R188 `R_clearing_price_time_path` has since anchored that decay. This round folds it in.

## The hypothesis under (re-)test

Project owner: *"mission 1 is return a chunk, any size chunk, as fast as possible, using water as the propellant … but then subsequent vehicles can take longer round trips, which would eventually get us into the green right?"*

`R_heterogeneous_cadence` found this **loses** NPV in three senses under a static price: chunk-shrinking mission 1 is a strictly dominated decision (the delivered-mass loss, 8× at chunk-25, is not recovered by the earlier-arrival discount gain); the real winner is stage-gating the *same* full fleet on mission-1 success (Regime R, +$2.7B). The one thing that round could not see: a **decaying** clearing price makes early delivery worth *more* — the fast mission 1 sells into a higher price than the later full mission. This round asks: **does R188's decay revive the front-loading case, or does it survive falsification?**

## Isolation of variables (the control)

This round changes **exactly one input** vs `R_heterogeneous_cadence`: the clearing price is now time-decaying per R188, `price(t) = P0 · exp(−rate·t)`. Vehicle parametric, cadence (2/yr), Wright's law (LR 15%), NRE, WACC grid, and schedule engine are held at het_cadence's values, so any verdict change is attributable to the decay alone. **The 500-kWe Variant B vehicle is retired (no-large-fission); absolute NPV levels are not the claim — the schedule-shape delta under decay is.** The matrix already settles absolute viability; this round isolates the mechanism the USER-NOTES proposed.

## Derived identity (verified: reproduces het_cadence cell α = −$112.7M exactly)

In Regime D single-flight, missions 2..N are identical between the het schedule (chunk_1<200) and the homogeneous baseline (chunk_1=200) — same slots, ships, build costs. So the whole Regime-D Δ-NPV is the mission-1 delivery term:

    Δ_NPV(c) = P0 · [ deliv(c)·D(rt(c)) − 80·D(14.5) ],   D(t)=exp(−rate·t)/(1+wacc)^t
    deliv(c)=0.40·c ;  rt(c)=11.5 + 3.0·(c/200)

## Pre-registered hypotheses (bounds scripted)

**H1 [XC] (decay off reproduces het).** At rate=0, P0=$2.5M/t, WACC 3%, Regime D: Δ-NPV(chunk_1=25) = **−$112.7M** (het cell α; XC band [−130, −95]); Δ-NPV(chunk_1=200)=0.0 exactly; monotonic penalty in chunk_1 (−112.7 / −95.5 / −62.2 / −30.4 / 0.0 across {25,50,100,150,200}). Falsified if the engine does not reproduce het's signs and cell-α magnitude within band.

**H2 [S] (decay on: still loses, penalty collapses).** With decay at every anchored rate (cons 9.2 / central 12.8 / median 17.7 / bull 32.4 %/yr), the chunk-25 shrink **still loses** in Regime D (Δ-NPV < 0 at all rates). At the central rate the penalty **collapses** to **[−$40, −$8]M** across the P0 band (from −$135 to −$180M static — an **85-89% narrowing**), because the fast mission-1 delivers into a higher price. The break-even decay rate is **~76%/yr** (SCOPE band [65, 90]%/yr) — far above the bull 32.4% — so the hypothesis is **robust-falsified**: no anchored decay flips it. Falsified if any anchored-rate Δ-NPV(chunk_1<200) goes ≥ 0 in Regime D, or if the flip rate lands below 50%/yr.

**H3 [S] (time dominates mass under decay).** The combined effective discount (decay + wacc-log) is **~15.8%/yr**; pulling the full 80 t mission-1 delivery one year earlier is worth **[$4, $10]M/mission** — and applied across the ~28-delivery fleet it dwarfs the entire single-mission chunk-shrink move (net −$23M at central). **The lever is delivery *time*, not chunk *size*; chunk-shrinking is a strictly dominated micro-optimization.** Falsified if the 1-yr-compression per-mission gain leaves band or is smaller than the chunk-shrink benefit.

**H4 [W] (Regime R stage-gating shrinks but stays positive).** het's static Regime-R advantage (stage-gate the same fleet on mission-1 success) was **+$2,733M** at chunk_1=200. Under decay, deferring missions 2..N still defers capex (good) but now decays the deferred revenue harder, so the advantage **shrinks**. Pre-registered to stay **positive**, in **[+$300M, +$2,000M]** at central decay. Falsified if it goes negative or exceeds the static +$2.7B.

## Sweep (run.py)

Closed-form Regime-D Δ-NPV over chunk_1 {25,50,100,150,200} × rate {0, 0.092, 0.128, 0.177, 0.324} × P0 {2.5,3.0,3.5,4.0} × WACC {0.03, 0.087}; flip-rate solve per chunk; full-schedule Regime-D and Regime-R NPV (reusing het_cadence's engine with the time-varying price) for the H4 advantage; 1-yr-compression sensitivity for H3. Deterministic. Grids span the pre-script's.

## What this round does NOT do

- Does not re-litigate absolute viability (matrix-settled) or the 500-kWe retirement — it isolates the schedule-shape mechanism under decay.
- Does not re-run het_cadence's Monte Carlo over the static demand distribution (superseded by the deterministic decay path; MC is a possible follow-on).
- Does not change vehicle physics, chunk-mass cap, or any requirement.
- Does not model a price *floor* (deep-space niche, R188 H4) — LEO-accessible decay only.

## Deliverables

`scope_bounds.py`, `run.py` (+ `results/fast_first_decay.png`), `results/findings.json`, `STUDY.md` with Revisit + bug-catch. Orchestrator notes: the USER-NOTES hypothesis is **re-confirmed falsified even under the most favorable (decaying) price** — front-loading narrows but does not flip the penalty; the decay *sharpens* het_cadence's "the lever is timing, not chunk size" reading; design-axes 02 / 10 gain the decay-robustness result.
