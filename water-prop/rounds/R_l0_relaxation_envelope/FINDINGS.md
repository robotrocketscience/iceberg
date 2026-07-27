# R-l0-relaxation-envelope — FINDINGS (proper round)

**Worker:** worktree-172651 (project-owner-directed "run the open rounds"), 2026-07-24
latest+28. Pre-registration: `STUDY.md` (this directory, written before the run, with
priors disclosed). Harness: `sweep_combined.py`; results:
`results/closure_rate_envelope.json`. Deterministic. Predecessors: `SCOPE.md` (Saturn,
latest+25), `TIER1-SANITY-FINDINGS.md` (Tier-1 sanity sweep, preserved verbatim),
`audit_assembly_preconditions.md` (rhea-5: walker enumeration honest, NO BUG).
Runs under the corrected kick physics (post `d379198`).

## Headline

**H1 FALSIFIED — and therefore the entire relaxation envelope is empty. Under the
corrected closed-loop framework, not one of 1,744 walked paths even completes the phase
graph, let alone arrives at the Earth-orbit depot: 0 feasible leaves, 0 arrivals, best
delivered payload 0.0 t.** Closure is 0/150 cells at every pre-registered floor (down to
**0.5 t**) × every ceiling (out to **35 years**) × every power class (including the
non-nuclear 1–11 kilowatt-electric rows with L0-24 vacated), at both the f = 0.80
baseline and the f = 0.20 guard-rail (4,440 paths). Per the SCOPE's pre-committed
reading: **"ICEBERG is not deliverable as currently conceived."** There is no
combination of spirit-preserving L0 relaxations that restores commercial closure,
because the walls sit upstream of every L0 the question would relax.

## Verdicts

| # | Hypothesis | Verdict | Measured |
|---|---|---|---|
| H1 | ≥ 1 cell arrives at LEO depot, payload > 0 | **FALSIFIED** (as predicted from priors) | 0 arrivals / 1,744 paths (f = 0.80); 0 / 4,440 (f = 0.20) |
| H2 | Floor → 5 t opens > 5 % closure | **FALSIFIED** (vacuous) | 0/150 at every floor 0.5–25 t |
| H3 | Ceiling → 25 yr alone opens > 5 % | **FALSIFIED** (vacuous) | 0/150 at every ceiling 15–35 yr |
| H4 | Non-nuclear (1–11 kWe) closes at 10 t / 25 yr | **FALSIFIED** (vacuous) | 0/75 non-nuclear cells |
| H5 | Combined relaxation > 20 % closure | **FALSIFIED** (vacuous) | 0.0 % |
| H6 | Cost-competitiveness at relaxed L0s | **DEFERRED** | financial model not operative (per SCOPE) |

## The load-bearing output: the failure taxonomy (where the 1,744 paths die)

At f = 0.80 (baseline), grouped by phase and reason class:

| Count | Phase | Failure mode |
|---|---|---|
| 660 | P0 Earth-to-LEO | launch wet mass exceeds every cap tested — 6× Falcon Heavy raw (360), Falcon Heavy expended (150), Starship (150) |
| 180 | P1 LEO-to-Saturn | kick stack exceeds the most-permissive launch manifest |
| 316 | P1 LEO-to-Saturn | chemical/TSI propellant shortfalls + electric power gates |
| 180 | P0b assembly | honest enumeration stubs (per rhea-5 audit — not a bug) |
| 208 | P4 Saturn departure | TEI propellant (136) + water-MET/electric power floors (72) |
| 200 | (remainder) | electric-thrust power gates, misc preconditions |

At f = 0.20 (guard-rail) the wall MOVES but does not open: launch-cap failures fall
(propellant no longer dominates wet mass) and the same paths die downstream of
propellant shortfalls at P1 (2,390 counts) — the two regimes of the fidelity round's
retracted "window", both now honestly fatal. This is the corrected-physics picture of
why the f-window was a bug artifact: below the window there is no propellant, above it
there is no launcher, and with self-consistent kick physics the window between them
contains nothing.

**Reading:** the binding walls are (1) the launch-mass wall — the self-consistent
closed-loop vehicle cannot be lifted by any current or near-term launch option, and
(2) behind it, the Saturn-departure propellant/power wall. Both are upstream of L0-04,
L0-05, L0-07, L0-12, and L0-24. Relaxing delivered-mass floors, round-trip ceilings,
cadence, cost-competitiveness, or the reactor-contract condition cannot touch either
wall. The only levers that could are architectural (smaller derived vehicle, different
departure scheme — the 115637 departure-thread H₂/O₂ stage territory) or a different
mission concept entirely (the depot pivot, the near-Earth-asteroid successor).

## Matrix amendment specification

- Decision #16 (parametric L0-04 floor sweep as decision-#15 softener): **the
  framework side of the sweep is now complete and returns the empty set at every
  floor.** The softener has no engineering content left; only the financial-model
  question (H6, deferred) remains, and it now has nothing to price on the Saturn
  round-trip tree.
- Decision #15 option (c) — hold L0-04 strict, accept termination at flyable power —
  is corroborated a further time, now against maximum spirit-preserving relaxation.
- The demonstrator-class promotion (REQUIREMENTS §7.5) is the only remaining
  programmatic path for the Saturn concept; commercial-class closure questions on the
  current architecture should be treated as answered-negative, not open.
- Axis 02 (surviving cell): no surviving cell at ANY spirit-preserving relaxation;
  recommend `status: falsified` for the commercial-class question at current
  architecture (project-owner call).

## Follow-ons (named, not started)

- Encode the 115637 departure-thread H₂/O₂ electrolysis stage as a `saturn_water_v2`
  phase-4 option and re-run this envelope — the only named architectural lever that
  attacks the P4 wall (it does not touch the P0 launch-mass wall, which binds first).
- The launch-mass wall re-derives at smaller chunk masses than the current 10-t grid
  floor; a demonstrator-scale grid (0.5–5 t chunks) is demonstrator-class territory,
  not commercial-class, and belongs to the §7.5 track.
