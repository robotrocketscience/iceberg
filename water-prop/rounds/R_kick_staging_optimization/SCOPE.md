# R-kick-staging-optimization — the 81 percent line item

**Status:** SCOPE pre-registered 2026-07-21, before `run.py`. Bounds from `scope_bounds.py` (committed alongside). Script-derived bounds labeled [S]; structural hypotheses labeled [W] per the R175 convention.
**Worker:** worktree-115637 session. R174's named follow-on; base case is R174's best corner (80 t chunk, 300 kW array, 58.8 t bank, 480 s gas).

## Question

R174 modeled the outbound kick as one stage with a flat 1.12 dry factor and found outbound propulsion ≥ 81 percent of launch mass. Two levers were left on the table: N-stage kick optimization, and splitting the 7.3 km/s injection between the kick and the already-flying array-lit thruster inside the sun window.

## Pre-registered hypotheses

**H1 [S] (staging gains).** Two stages cut kick wet mass **47–55 percent** versus single-stage across structural fractions 0.06–0.12 (scripted 52.4 percent at 0.08); a third stage adds only **15–20 percent** more. Falsified outside either band.

**H2 [S] (hybrid optimum).** The kick/lit-thruster split optimizes at kick delta-v **3.9–4.3 km/s** with lit water **44–48.2 t** — the harvest cap binds (scripted optimum 4.1 km/s, 46.9 t against a 48.2 t cap). Falsified outside the bands.

**H3 [W] (end-to-end improvement).** Best combined corner (staging × hybrid) brings outbound launch to **≤ 300 t** and the end-to-end ratio at the 80 t chunk from R174's 4.8× to **2.6–3.4×**. Falsified outside.

**H4 [W] (outbound still dominates).** Outbound share of launch mass falls below R174's 81 percent but stays **≥ 55 percent** at every swept corner. Falsified below.

## Deliverables

`scope_bounds.py`, `run.py` (n × structural-fraction × kick-split cross-sweep, figure `results/kick_optimization.png`), `results/findings.json`, `STUDY.md`.
