# R-per-phase-propellant-fidelity — FINDINGS

**Worker:** worktree-172651, 2026-07-26 latest+29d. Pre-registration: `STUDY.md`.
Artifacts: `run.py`, `results/min_multiplier_vs_f.json`.

## Headline

**My latest+29c claim — "the corridor's ×16 launch requirement is largely a
frozen-propellant-fraction artifact" — is RETRACTED.** The minimal-f scan shows
the corridor family is chemical-schedule-bound, not convention-bound:

- **150 kWe / 500 t cell:** minimum launcher multiplier **8.75 at every feasible
  f**; f_optimal = 0.80 — the frozen convention was already optimal. Zero
  artifact. (The ×16 record figure was probe-grid coarseness {8,16,32}, not
  physics: bisection puts the true requirement at ×8.75 ≈ 875-t-class effective
  lift.)
- **200 kWe / 1,000 t cell:** ×15.29 at f = 0.80 → **×11.41 at f_optimal =
  0.75** — a 1.34× cut, real but modest.
- **Electric family (chunk-fed at the resolved 22.5 km/s, Isp 3,000 s,
  60 W/kg, 200 kWe / 500 t):** closes at NO f at any multiplier ≤ 32 — the
  family is dead independently of the propellant convention, so the artifact
  claim is unmeasurable there (the f = 0.36 "artifact" arithmetic that seeded
  the claim belonged to paths the resolved departure anchor has since killed).

## Verdicts

| # | Hypothesis | Verdict | Measured |
|---|---|---|---|
| H-P1 | Optimal-f cuts corridor ×16 → ≤×8 (150 kWe/500 t) | **FALSIFIED (as pre-registered)** | no cut at all; f_opt = 0.80; true minimum ×8.75 at every f |
| H-P2 | f_optimal ∈ 0.70–0.85 for the corridor family | **HELD** | 0.80 / 0.75 |
| H-P3 | Optimal-f cuts the electric family ≥2× | **FALSIFIED (family dead)** | no closure at any f ≤ 0.85, multiplier ≤ 32 |
| H-P4 | Delivered mass moves ≤10% with f | **HELD** | delivery set by the departure mass ratio |

## Corrected corridor launch requirements (supersede the ×16 figure)

| Cell | Min effective lift | at f |
|---|---|---|
| 150 kWe / 500 t → 32 t delivered | **×8.75 (≈875 t)** | 0.80 |
| 200 kWe / 1,000 t → 89 t delivered | **×11.4 (≈1,140 t)** | 0.75 |

In Starship-refill terms (100–150 t/flight to LEO): 6–11 flights of raw lift
per mission, before tanker flights for the departure kick — a cost line, not a
physics wall, but 2–3× the latest+29 "×5 Starship-refill era" scenario.

## What this retracts / amends

1. Retract "×16 is largely a frozen-f artifact" (latest+29c, twice in the
   record). The corridor is chemically propellant-hungry by construction
   (Helios kick residual + periapsis capture + arrival trim ≈ 93% tank
   utilization); per-phase accounting was already effectively priced in.
2. Amend the corridor requirement downward ×16 → ×8.75–×11.4 (a REAL
   improvement, from bisection granularity + mild f-tuning — just not for the
   claimed reason).
3. The full R-vehicle-mass-fidelity-refinement (Wertz subsystem anchors,
   path-conditional TPS) remains open; this round discharges only its
   propellant-fraction limb for the corridor family.
