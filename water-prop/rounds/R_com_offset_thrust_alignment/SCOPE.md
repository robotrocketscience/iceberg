# R-com-offset-thrust-alignment — attitude cost of pushing an offset, shifting center of mass

**Status:** SCOPE pre-registered 2026-07-20, before `run.py` was written or executed.
**Worker:** worktree-115637 session. Follow-on demanded by R-chunk-despin-budget's Revisit.
**Predecessors:** R-chunk-despin-budget (de-spin refuted as a fuel item; surfaced this question); ICEBERG-bag-engineering.md (harvest-port geometry); SATURN-SHIP-SPEC.md (no thrust-vector-control requirement currently).

## Question

The inbound burn pushes a stack whose cargo is an irregular ice chunk inside a fabric bag: the stack center of mass sits off the thrust line by an offset ε, and *walks* over the burn as sublimation draws the cargo down. Holding attitude against that offset costs propellant. How much, under which control strategy, and what requirement does it impose on the vehicle?

Per the R-chunk-despin-budget methodology lesson, every numeric bound below is set against the **worst corner of the declared grid**, not the central case.

## Pre-registered hypotheses

**H1 (RCS-fought offset is architecturally dead).** Fighting the offset torque with corner reaction-control thrusters (arm 3 m, Isp 70 s, η 0.7) over the full inbound chunk-fed burn (delta-v 4.2 km/s) costs more than **5 tonnes** of propellant at every grid point with chunk ≥ 25 t and ε ≥ 0.5 m, and more than **50 tonnes** at the worst corner (200 t chunk, ε = 1.0 m, 10 kWe). Falsified if any such point is under its bound.

**H2 (steer-through-center-of-mass is cheap).** Steering the thrust vector through the stack center of mass (main-engine gimbal or thruster-array differential throttle) needs at most **atan(1.0/5) ≈ 11.4°** of steer authority at the worst declared offset and engine lever (ε = 1.0 m, l = 5 m), and the associated cosine tax is under **2 percent** of inbound propellant at every grid point. Falsified if either is exceeded.

**H3 (the walk makes ε = 0.5 m the operating point, not the tail).** With a fully one-sided sublimation draw (harvest port on one hemisphere, no draw rotation), removing the inbound propellant fraction of the cargo walks the cargo center of mass by more than **0.5 m** for every chunk ≥ 40 t (porous or solid). Falsified if any such chunk walks less. Consequence if held: absent an actively symmetrized draw, ε ≥ 0.5 m is the *expected operating condition*, and H1's verdict applies to the baseline design, not a corner case.

**H4 (closure discriminates the strategies).** On the audit sweep (48 cells, 5 closing at the 25 t floor): charging each closing cell the steer-through cosine tax (computed at ε = 1.0 m, l = 5 m) flips **0** cells; charging the RCS-fought cost flips **all 5**. Falsified by any deviation in either count.

## Method

Closed form, deterministic, no Monte Carlo needed:

- Thrust T = 2·η_thr·P/(g0·Isp), η_thr = 0.6, Isp = 800 s, P ∈ {10, 30, 100} kWe.
- Stack: ship dry 20 t + chunk m_c ∈ {25, 40, 80, 200} t; inbound propellant from the rocket equation at 4.2 km/s drawn from cargo; burn time from thrust and log-mean stack mass.
- Offset torque τ = T·ε, ε ∈ {0.1, 0.5, 1.0} m; RCS-fought angular impulse = τ·t_burn → propellant at arm 3 m, Isp 70, η 0.7.
- Steer-through: angle atan(ε/l), l ∈ {5, 10} m; cosine tax = inbound propellant × (1/cos θ − 1).
- Center-of-mass walk: sphere radius from {500, 900} kg/m³; remove fraction f (inbound propellant / cargo) from one hemisphere centered at 3r/8; walk = f·(3/8)·r/(1−f).
- Closure reprocess as in R-chunk-despin-budget (leaf_state.payload_kg — the corrected field).

## Deliverables

1. `run.py`, `results/com_offset_costs.png` (RCS-fought vs steer-through, log scale), `results/com_walk.png`, `results/findings.json`.
2. `STUDY.md` with Revisit.
3. Proposed L1 requirement text for the orchestrator: thrust-vector authority ≥ the walk envelope, or an actively symmetrized harvest draw — surfaced via handoff, not edited into shared docs by this round.
