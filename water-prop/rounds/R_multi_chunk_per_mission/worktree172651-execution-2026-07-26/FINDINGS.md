# R-multi-chunk-per-mission (execution 2) — FINDINGS

**Worker:** worktree-172651, 2026-07-26 latest+29d. Pre-registration:
`STUDY.md`; prior-execution adjudication `../README.md`. Artifacts: `run.py`,
`results/multi_chunk_results.json`, `results/ledger_walk_overhead_cell.txt`
(lesson-25 walk).

## Headline

**Multi-chunk harvesting survives every physics gate cheaply — the corridor
keeps its 30-t closure with overheads charged (31.7 t at N = 2; 87.8 t at
N = 3, 18.7 yr incl. ops) — and converts capture-mechanism reliability from a
margin item into THE mission driver.** At the optimized harpoon operating point
(0.961/capture) joint success is 0.92 / 0.89 / 0.82 for N = 2/3/5 — the N ≤ 3
corridor clears L0-10's 0.80 floor with margin; at the un-optimized prior mean
(0.549) even N = 2 collapses to 0.30. The two demonstrator-track bench items
(porous-ice penetration; cinch/mechanism reliability) are now load-bearing for
the only closing corridor, exactly as the owner's decision-6 caveat
anticipated.

## Verdicts

| # | Hypothesis | Verdict | Measured |
|---|---|---|---|
| H-M1 | Re-rendezvous ≤ 6 months and ≤ 50 m/s per chunk at 10–1,000 km spacing | **REFINED-HELD (band, not blanket)** | pure-drift strategy: 10 km → 2 m/s but 3.4 yr worst-case phasing; 100 km → 19.5 m/s, 125 d ✓; 1,000 km → 12 d but 195 m/s (≈29 t chemical on a 500-t stack — not negligible). Feasible band ≈ 30–300 km spacing; the binding open input is the NUMBER DENSITY of ≥100-t chunks (ties to the un-measured ring PSD — same gap as the bet-#2 silicate tail) |
| H-M2 | Joint reliability ≥ 0.80 at N ≤ 3 optimized; fails at N ≥ 2 on prior-mean | **HELD (both halves)** | 0.961^N: 0.92/0.89/0.82; 0.549^N: 0.30/0.17/0.05 |
| H-M3 | Containment is per-chunk; N smaller chunks beat one big one | **HELD** | Round-J ceiling gain N^(1/6): 1.12×/1.20×/1.31× at N = 2/3/5 |
| H-M4 | Despin sub-1% of budget for slow rotators | **HELD (strongly)** | 1.2 kg propellant per 400-t chunk at 0.05 rpm; 6.5 kg at the 0.28-rpm fast corner — despin is a non-issue at Tier 1; the fast-rotator GNC/structural handling (not Δv) stays the named corner |
| H-M5 | Corridor survives 350 kg/chunk + 0.25 yr/chunk overheads | **HELD** | 32.2 → 31.7 t (N = 2, 21.1 yr); 88.8 → 87.8 t (N = 3, 18.7 yr); ledger walk clean (1,507 t launch → 87.8 t delivered) |
| H-M6 | 1,000–2,000 t aggregate reaches the 209-t sovereign-hurdle delivery class | **FALSIFIED (fully — worse than the predicted half)** | ×16 ceiling: 87.8 t; even ×32 / 500 kWe / 2,000 t gives 169.8 t < 209 t. NO hurdle-class delivery exists anywhere in the mapped corridor; the titan-2 execution's venture-class claim is confirmed dead under closed-loop physics |

## What multi-chunk changes in the corridor requirement stack

- Capture side: N = 2–3 captures of ~250–400 t each (inside the 482-t cap),
  30–300 km spacing assumed available — **chunk number density is the new
  named measurement gap**.
- Reliability side: per-capture ≥ 0.95 is now a hard corridor requirement
  (titan-2's structural contingency, re-derived under closed-loop physics).
- Mass/time side: negligible (≤ 1.05 t dry, ≤ 0.5 yr).
- Economics side: H-M6 kills delivery-class hurdles — handed to
  R-corridor-financial-model.
