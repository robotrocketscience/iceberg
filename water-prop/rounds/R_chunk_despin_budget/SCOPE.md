# R-chunk-despin-budget — propellant and time cost of de-spinning a captured chunk

**Status:** SCOPE pre-registered 2026-07-20, before `run.py` was written or executed.
**Worker:** worktree-115637 session, project-owner-directed round.
**Predecessors:** R-chunk-capture-monte-carlo Tier 0.5 spin prior (`tier_0_5_spin_prior.md`); A14 capture-efficiency decomposition (R_A14_engineering_decomposition); ICEBERG-bag-engineering.md (cinch + laminate treatment); SATURN-SHIP-SPEC.md (12× water-vapor cold-gas RCS at envelope corners, 50 kg reserve).

## Question

The project owner flags de-spin as a potentially major unpriced fuel cost: after capturing a multi-tonne spinning ice chunk, the stack must be de-spun before the inbound burn, and that propellant comes out of delivered water. Quantify the de-spin budget — propellant, time, and closure impact — against the campaign's own spin priors, and against pessimistic tails well beyond them.

## Boundary

- IN: rigid-body de-spin of the captured chunk / rigidized stack; ship-applied reaction-control torque; passive fabric-friction damping inside the cinched bag; angular-momentum bookkeeping of the capture itself (stack spin-up); delivered-mass and closure-rate impact at the 25 t floor.
- OUT: capture success probability under spin (that is A14's axis — the Monte Carlo already carries spin-rate sensitivity); attitude control DURING the multi-year inbound burn (center-of-mass offset, wobble, thrust-vector alignment) — if the Revisit flags it, it becomes a follow-on round, not scope creep here.

## Pre-registered hypotheses (numeric, falsifiable, written before the run)

**H1 (central prior — de-spin propellant is negligible).** At the Tier 0.5 size-conditioned spin prior (log-normal, median 0.005 rpm size-marginal), de-spin propellant for a 10–200 t chunk using the ship's water cold-gas RCS (Isp 70 s, effective torque arm 3 m, geometry efficiency 0.7) has a 95th-percentile below **1 kg**. Falsified if p95 ≥ 1 kg for any chunk mass in the grid.

**H2 (stress tail — still sub-0.5% of floor).** Sweeping spin deterministically up to 1 rpm — two orders of magnitude above the decameter prior median, above the CIRS slow-rotator bound, covering collision-recent spin-up — de-spin propellant for a 200 t porous chunk (500 kg/m³) stays below **125 kg** on cold-gas RCS and below **15 kg** on the 800 s main thruster. Falsified if either bound is exceeded at 1 rpm.

**H3 (passive fabric damping beats active de-spin).** With cinch contact pressure ≥ 10 Pa over the bag-chunk contact area, ice-on-fabric friction coefficient 0.1, residual chunk spin inside the cinched bag self-damps (chunk and stack reach common rotation) in under **one hour** for all cases up to the 1 rpm stress tail. Falsified if damping time exceeds 1 hour anywhere in that envelope. (Consequence if held: active de-spin of the chunk relative to the bag is unnecessary; only the combined stack's angular momentum must be removed by RCS, which is the same L — H1/H2 already price it.)

**H4 (stack spin-up is attitude-absorbable).** Capturing a chunk at the prior-median spin transfers its angular momentum to the combined stack; the resulting stack rotation rate is below **0.1 deg/s** at prior median for all chunk masses (comparable to normal deadband rates), and below **5 deg/s** at the 1 rpm stress tail. Falsified if exceeded.

**H5 (closure impact is nil).** Charging the p95 de-spin propellant against delivered mass across the audit-sweep grid (48 cells, capture-multiplier × chunk-mass × vehicle-mass × Isp) changes the closure count at the 25 t floor by **zero cells**. Falsified if any cell flips.

If H1–H5 all hold, the honest reading is a **drop (negative result)**: de-spin is not a fuel problem at ring-chunk spin rates; the spin risk lives in capture success (A14) and possibly in thrust-phase attitude control (Revisit will adjudicate whether that becomes a follow-on).

## Method

Closed-form rigid-body budget, Monte Carlo over the Tier 0.5 prior (n=20,000 per chunk-mass point), plus deterministic stress sweep:

- Chunk: sphere, mass grid {10, 25, 40, 80, 200} t, density {900 solid, 500 porous} kg/m³; I = (2/5) m r²; tumbling (non-principal-axis) penalty factor 1.5 on required angular impulse.
- Spin: Tier 0.5 log-normals (size-conditioned: 1–10 m class for ≤ 40 t, 10–100 m class above) + deterministic sweep 0.001–1 rpm.
- De-spin propellant: m_p = L·k_tumble / (d_eff · g0 · Isp · η), d_eff = 3 m (envelope-corner couple), η = 0.7, Isp {70 cold-gas water, 800 MET}.
- Fabric damping: τ_f = μ · p_c · A_contact · r̄, damping time t = L_rel/τ_f; μ = 0.1, p_c ∈ {1, 10, 100} Pa, A_contact = half-sphere area, r̄ = (2/3) r.
- Stack spin-up: ω_stack = L_chunk / (I_chunk + I_ship + m_red·l²) with ship 50 t, offset l = 5 m.
- Closure: reprocess `runs/audit_capture_efficiency/20260522T175555Z/cells.jsonl`, subtract p95 de-spin propellant from best-delivery per cell, recount 25 t closures.

## Deliverables

1. `run.py` — all computations, deterministic seed, writes `results/`.
2. `results/despin_budget.png` — propellant vs spin rate, chunk-mass family, both Isp, prior band shaded.
3. `results/despin_time_fabric.png` — passive damping time vs spin.
4. `results/despin_findings.json` — headline numbers per hypothesis.
5. `STUDY.md` — hypothesis/test/result/reading/**revisit**/cross-learning per protocol.
6. Handoff note for the orchestrator; design-axes amendment is orchestrator-owned, not this round's.
