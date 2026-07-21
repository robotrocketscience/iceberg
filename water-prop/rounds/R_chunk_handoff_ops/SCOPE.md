# R-chunk-handoff-ops — the relay's two unprecedented operations, decomposed

**Status:** SCOPE pre-registered 2026-07-21, before `run.py`. Bounds from `scope_bounds.py`, committed alongside.
**Worker:** worktree-115637 session. Prices R182's chunk handoff and R184's reactor-module swap in the campaign's engineering-decomposition style (`R_A14` lineage). **All stage probabilities are desk-anchored bands, not measurements** — the deliverable is the retry-aware structure, the failure-mode split, and the bottleneck ordering, per the campaign's own lesson that desk anchors inflate (85 % → 46 % on bet #1).

## Model

Five-stage chain per handoff (rendezvous 0.985–0.995, prox-ops at 44 t 0.95–0.99, **berth of a bagged non-rigid 40 t load 0.88–0.95** — the novel stage; nearest precedents ISS arm berthing of 20 t rigid modules, MEV-1/2 dockings, OSAM —, mate 0.95–0.99, separation 0.985–0.995); failures split benign/retryable (90 %) vs damaging (10 %, swept 5–20 %); up to 3 attempts. Reactor swap: same chain, rigid 6 t module, berth 0.92–0.97, one per mission. Economics composed onto R184's steady state (0.365): risk-adjusted lpd = 0.365 / retention; hardware (arm 0.8 t + fixtures 0.4 + swap interface 0.2) rides the kick.

## Pre-registered hypotheses (bounds scripted)

**H1 [W] (per-handoff numbers).** Per-attempt success **0.77–0.92** (central 0.848); with retry, eventual success **0.96–0.99** (0.980) and damaging loss **0.8–2.9 %** (1.75 %) per handoff. Falsified outside bands.

**H2 [S] (mission retention and risk-adjusted economics).** N=4 handoffs + 1 swap retain **0.89–0.93** of mission water throughput (scripted 0.908); risk-adjusted steady lpd **0.39–0.42** (0.402). Falsified outside bands.

**H3 [S] (hardware is not free).** Handoff/swap hardware adds **+0.045–0.060 lpd** (scripted +0.051, ~14 %) — enough that "handoff is only a reliability line" (this session's framing when R182 shipped) is **wrong**: it is also an economics line. Ops-honest steady state ≈ **0.44–0.47** (scripted 0.453). Falsified outside bands.

**H4 [W] (ordering, and the knife-edge theorem).** (a) Handoff retention (≥ 0.89) sits far above bet #1's capture-efficiency band (0.46–0.85): **the relay adds no new dominant bottleneck**; capture remains binding. (b) Composition: the ops-honest advantage over the monolithic (1.02/0.453 ≈ **2.25×**) puts the waiver break-even at **8.0–8.5 %** — the third consecutive honesty pass (lifetime → NPV → ops) to land the relay's viability **exactly at the utility hurdle**. Registered consequence: the relay is not robustly superior; it is hurdle-marginal under every honest accounting, and the demonstrator needs a **LEO handoff-rehearsal gate** before the architecture is credited. Held if H1–H3 hold and the composed d\* lands in band.

## Sweep

retry {1, 2, 3} × damaging fraction {5, 10, 20 %} × N {2–5} × band {low, central, high}; composed economics per cell.

## Deliverables

`scope_bounds.py`, `run.py` (+ `results/handoff_ops.png`), `results/findings.json`, `STUDY.md` with Revisit; matrix notes: the ops-honest relay ladder entry (~0.45), the knife-edge statement, the LEO rehearsal gate, and the desk-anchor caveat in bold.
