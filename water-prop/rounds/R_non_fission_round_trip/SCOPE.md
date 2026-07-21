# R-non-fission-round-trip — end-to-end pricing of the solar-bank mission

**Status:** SCOPE pre-registered 2026-07-20, before `run.py` was written or executed. All bounds derive from `scope_bounds.py`, committed alongside.
**Worker:** worktree-115637 session. The load-bearing follow-on named by R-inbound-dark-leg-energy; owner-directed continuation.
**Predecessors:** R173 (inbound closes at 36.8 t penalty, 1.74× — **with outbound and Saturn-side dark maneuvers excluded by its registered boundary**); R171/172 (bank chain); R_non_fission_baseline.

## What the pre-script already shows

Chaining the *full* mission exposes what R173's boundary hid: capture (1.0 km/s) and ring operations (0.5 km/s) are dark and gas-fed too; every kilogram of bank must be hauled through every earlier burn at 450 s; and the outbound leg has no free option. Scripted chain at the canonical 40 t chunk: **bank 95.5 t** (capture 27.3 + ops 10.9 + hotel 2.6 + departure 36.2 + residual 18.5), penalty 115.4 t, outbound mode (a) chemical kick 575 t of kick propellant on the 136 t stack, mode (b) lit solar spiral 871 t of water. **Launch-per-delivered ratio: 15.6× (a) / 20.1× (b)** against the reactor baseline — an order of magnitude past R173's inbound-only 1.74×.

## Pre-registered hypotheses (bounds from `scope_bounds.py`; sweep may beat them only by finding structure the script lacks)

**H1 (chain compounding).** The full-chain bank at the canonical case is **86–105 t** (scripted 95.5), i.e. ≥ 3.2× R173's inbound-only 30 t. Falsified outside the band.

**H2 (no corner survives).** Sweeping chunk mass {25–200 t}, array {100–300 kW}, dark-side relief via moon-tour credits (capture 1.0 → 0.6 km/s, ops 0.5 → 0.3), bank engine Isp {450, 480}, both outbound modes: **no corner achieves launch-per-delivered below 6×** the reactor baseline. Falsified if any corner beats 6×.

**H3 (where the mass goes).** In every swept corner, outbound propulsion (kick or spiral propellant) is the largest single launch-mass line, ≥ 55 percent of total. Falsified below 55 percent anywhere.

**H4 (the honest reversal).** Consequence hypothesis: R173's "bet #3 reframes to a 1.74× price" claim, extended end-to-end, is **falsified by this round** — the correct statement reverts to R_non_fission_baseline's: no non-fission round trip at credible launch economics; the priced non-fission assets (R171 hotel bank, R172 regenerative bank, R173 lit-leg braking) survive as *components* of a reactor mission's resilience, not as a reactor replacement. This hypothesis is held if H1–H3 hold.

## Deliverables

`scope_bounds.py`, `run.py` (sweep + one figure `results/round_trip_ratio.png`), `results/findings.json`, `STUDY.md` with Revisit; matrix note for the orchestrator correcting the R173 headline.
