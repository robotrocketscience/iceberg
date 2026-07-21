# R-shuttle-reuse-fleet — what fleet reuse actually amortizes when reactor life is the currency

**Status:** SCOPE pre-registered 2026-07-21, before `run.py`. Bounds from `scope_bounds.py`, committed alongside.
**Worker:** worktree-115637 session. Adjudicates R182's fleet-multiplier implication against the reactor-lifetime anchor (`R_reactor_lifetime_vs_burn_time`: Kilopower design life **10 full-power-years, a program target, not a measurement**), and corrects R182's own optimum in passing.

## Model

Full-power-years (fpy) is the currency: one sortie at 60 kWe = 2.08 fpy. Reactors serve sorties until life L is exhausted; replacement modules (κ·P_s) ride subsequent motherships; the reusable part is the shuttle bus+bag (2.5 t). Discrete swap model (one reactor per mission, conservative) and long-horizon pooled model (fractional reactors/mission) both computed. Kick 5.84, chunk 40 t, paper κ primary, waiver schedule, synodic-window cadence (1.02 yr) feasible by inspection.

## Pre-registered hypotheses (bounds scripted)

**H1 [S] (R182's optima bust the lifetime target).** Both R182 winning cells exceed 10 fpy in a single mission (paper 60 kWe/N=5 → 10.4; flown 50 kWe/N=3 → 11.4). Lifetime-capped headlines: **paper N=4, lpd 0.44–0.48** (scripted 0.46, was 0.36); **flown N=2, lpd 1.9–2.1** (2.00, was 1.33 — still beats the flown monolithic's 2.41). Falsified outside bands.

**H2 [S] (steady-state swap, and the dream's price).** Discrete steady-state launch-per-delivered **0.35–0.38** (scripted 0.365); the reactor module is **55–65 %** of recurring launch; fleet-average at K=3 **0.38–0.41**. The naive reactor-immortal figure (0.14–0.15) is registered as a falsified-in-advance comparator: it assumes a reactor that never dies. Falsified outside bands.

**H3 [W] (the reactor is the propellant).** Long-horizon pooled steady lpd vs design life: **0.32–0.34 / 0.26–0.28 / 0.23–0.25** at L = {10, 15, 20} fpy; reaching the naive dream requires **L ≥ 40 fpy — four times an unmeasured target**. Consequence: bet #3's demonstrator objective gains a lifetime clause — full-power-years, not criticality, is what must be demonstrated. Falsified outside bands.

**H4 [S] (NPV restoration, cross-cite R183).** The steady-state advantage vs the monolithic (**2.7–2.9×**, scripted 2.79) restores the waiver's break-even rate to **10.2–10.6 %** (scripted 10.4) — putting the waiver+fleet+paper-κ package back above the 8 % utility hurdle with ~2.4 points of margin, versus the single-mission lifetime-capped tier's zero margin. Falsified outside bands.

## Sweep

P_s {40–100, step 10} × L {10, 15, 20, 40} × K {1–5}; discrete + pooled models; d\* per steady advantage.

## Deliverables

`scope_bounds.py`, `run.py` (+ `results/fleet_reuse.png`), `results/findings.json`, `STUDY.md` with Revisit; matrix notes: R182 headline correction (0.36 → 0.46 single-mission at the lifetime target), the fleet-swap statement, the bet-#3 lifetime clause.
