# R-harvest-draw-symmetrization — can geometry retire the center-of-mass walk?

**Status:** SCOPE pre-registered 2026-07-20, before `run.py` was written or executed.
**Worker:** worktree-115637 session. Third round in the spin/attitude arc; directly attacks R-com-offset-thrust-alignment's one-sided-draw assumption.
**Predecessors:** R-com-offset-thrust-alignment (walk 1.2–1.7 m under one-sided draw; ±1.7 m / 12° thrust-vector requirement proposed); ICEBERG-bag-engineering.md (sun-wall sublimation → cold-wall frost → harvest-port cycle).

## Question

Round 169 treated a one-sided harvest draw as the default and derived a heavy requirement: 12° of thrust-vector authority tracking a ±1.7 m center-of-mass walk. But the draw geometry is a design choice. Does a harvest port on the thrust axis, plus a slow roll about that axis (Apollo-style passive thermal control), symmetrize the draw and the sun-driven ablation well enough to hold the transverse offset inside the cheap-gimbal regime (ε < 0.2 m, where 3° suffices)?

Bounds set at the worst corner of the declared grid, per standing convention.

## Pre-registered hypotheses

**H1 (polar port kills the draw walk — with a buildable tolerance).** Modeling the draw as a column removed parallel to the thrust axis at transverse offset δ from it (walk = f·δ/(1−f), f = inbound draw fraction), a port placed within **δ ≤ 0.3 m** of the thrust axis holds transverse draw-walk **< 0.25 m** for every chunk in {25, 40, 80, 200} t, both densities {500, 900} kg/m³. Falsified if any case reaches 0.25 m. (The tolerance is absolute, not proportional to chunk size — that is what makes it buildable.)

**H2 (without roll, sun geometry recreates the side draw).** If at least 60 percent of net mass removal comes from the sun-facing hemisphere of an inertially-fixed stack (removal split s ≥ 0.6; walk = f·(2s−1)·(3/8)·r/(1−f)), the transverse walk exceeds **0.5 m** — the kill regime — for every chunk ≥ 40 t at porous density. Falsified if any such case stays under 0.5 m. Consequence if held: the polar port alone is insufficient; the sun-side ablation channel must also be symmetrized.

**H3 (a lazy barbecue roll symmetrizes the sun channel).** Rolling the stack about the thrust axis at ≥ 1 revolution per day bounds the residual sun-driven transverse walk below **0.05 m** for all cases: successive half-revolutions cancel, and the residual is bounded by one revolution's worth of ablated mass at the hemisphere centroid, ε ≤ (ṁ·P_roll/m)·(3/8)·r·(2s−1)/(1−f) evaluated cumulatively as one-rev worth of uncancelled moment. Falsified if the bound exceeds 0.05 m anywhere on the grid (thrust from 10–100 kWe sets ṁ).

**H4 (the roll is gyroscopically free).** Precessing the rolling stack's axial angular momentum through the slow thrust-vector slews that track the (now axial) center-of-mass motion — bounded by a full 3° slew per day, generous — costs **< 1 kg** of reaction-control propellant over the whole inbound burn at every grid point. Falsified if ≥ 1 kg anywhere.

If H1, H3, H4 hold and H2 holds (showing roll is *necessary*, not decorative), the round supersedes half of round 169's requirement: the compliant design becomes **polar port (±0.3 m) + roll ≥ 1 rev/day + 3° thrust-vector trim**, and the ±1.7 m / 12° tracking requirement is demoted to the no-roll fallback.

## Method

Closed form, deterministic. Grid: chunk {25, 40, 80, 200} t × density {500, 900} kg/m³ × power {10, 30, 100} kWe (sets ṁ = T/v_e via T = 2·0.6·P/v_e, Isp 800 s); f from the 4.2 km/s rocket equation with 20 t ship dry mass, capped at the cargo. Roll: 1 rev/day; stack axial inertia = chunk (2/5)mr² + ship 0.4·m_ship·2.5². Slew tracking: 3°/day at worst; precession torque τ = Ω × L_roll; propellant at arm 3 m, Isp 70 s, η 0.7. Sun-split s swept {0.6, 0.8, 1.0}.

## Deliverables

1. `run.py`, `results/walk_strategies.png` (one-sided vs polar-port vs polar+roll, per chunk), `results/findings.json`.
2. `STUDY.md` with Revisit and a proposed requirement rewrite for the orchestrator.
