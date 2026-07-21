# R-leo-depot-bootstrap — does "the product as its own propellant" compound or drain?

**Status:** SCOPE pre-registered 2026-07-20, before `run.py`. Bounds from `scope_bounds.py`, committed alongside.
**Worker:** worktree-115637 session. Questions the follow-on R174 itself proposed — the poetic one.
**Predecessors:** R174 (outbound ≥ 81 percent of launch mass; named this round); R173 (solar-bank inbound).

## Question

A LEO water depot filled by returning missions could fuel the next mission's outbound — launch only hardware, ride on delivered water. The bootstrap compounds only if a mission consumes less depot water than it delivers: the **water interest rate** (tonnes consumed per tonne delivered) must be < 1. The pre-script says it is 4.3–18.9. This round registers that as falsifiable and prices the salvage.

## Pre-registered hypotheses (from `scope_bounds.py`)

**H1 (the rate).** Depot-fueled non-fission outbound interest rate ∈ **[4.3, 18.9]** across modes (lit spiral at 800 s; depot-electrolyzed H2/O2 kick at 450/480 s) and cases (canonical 40 t with the 79.8 t bank; big 80 t with the 58.8 t bank). Falsified outside the band.

**H2 (break-even is unreachable).** Rate = 1 requires outbound delta-v ≤ **4,867 m/s** (best case: 80 t chunk at 800 s) — every real outbound mode costs ≥ 7,300 m/s impulsive-equivalent. Falsified if any mode reaches its break-even.

**H3 (fleet ledger diverges).** Simulating a fleet drawing outbound water from the depot: net depot level after each mission changes by delivered − consumed < 0 at every mode/case, so an N-mission campaign drains **≥ 3.3 t of depot water per delivered tonne** net at the best corner. Falsified if any corner nets positive.

**H4 (the salvage).** Depot water spent only on low-delta-v service (≤ 1 km/s of LEO-departure ops and arrival trim at 800 s) has rate **0.15–0.18** — accretive, adopt-scoped. Falsified outside the band.

## Deliverables

`scope_bounds.py`, `run.py` (fleet ledger + figure `results/depot_ledger.png`), `results/findings.json`, `STUDY.md`.
