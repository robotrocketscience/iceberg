# R-relay-ledger-reconciliation — the chunk-water ledger unified, and R186 propagated through the relay arc

**Status:** SCOPE pre-registered 2026-07-21, before `run.py`. Bounds from `scope_bounds.py`, committed alongside.
**Worker:** worktree-115637 session. Two debts fall due together: R178's flagged ledger reconciliation (R173/R174 never debited lit-leg propellant from delivered), and **R186's revocation of the free pump-up departure — which the relay arc (R182–R185) had built into the mothership's ledger as a 0.0 km/s departure line** (4 t bus, no reactor, no departure propellant, "departs by the pump-up tour"). The staging ellipse is the Hohmann raise orbit; its contour's honest exit ceiling is 3.16 km/s against the required 6.21.

## Unified chunk-water ledger convention (registered)

**Delivered = mass at Earth handoff. Every gram of propellant debits harvest. Every tank, stage, or reactor launched debits launch mass. Every hour of Saturn-side work debits residence.** The monolithic baseline already conforms (it pays the 9.0 km/s chunk-fed spiral out of extra harvest: 3.53× harvest per delivered, lpd 1.02 unchanged). The relay as shipped does not.

## Pre-registered hypotheses (bounds scripted)

**H1 [S] (the omitted line, priced).** The mothership's honest departure from the staging ellipse is **1.6–1.8 km/s** impulsive-equivalent (scripted 1.68: S4-from-ellipse peri burn at v₀ 5.37 + one outbound kick + 50 m/s targeting) or **3.2–3.5 km/s** as a no-Oberth spiral (scripted 3.35: free pump to the contour ceiling 3.16, linear residual, 300 m/s trims). R182 carried 0.0. Falsified if any in-scope mechanism prices it under 1.0 km/s.

**H2 [S] (the knife-edge resolves downward).** Three honest options propagated through the ladder (0.365 → 0.453 → departure-honest): in-situ gas kick (+79 t harvest, +40 t launch for stage hardware, +1.7 yr electrolysis residence → lpd 0.70, d\* 3.7 %); mothership MET at paper κ (+88 t harvest, +8 t amortized reactor launch → **lpd 0.49–0.53**, scripted 0.505, advantage 1.9–2.1×, **d\* 6.4–7.5 %**, scripted 7.0); mothership MET at flown κ (lpd 0.68, d\* 4.0 %). **Every honest option lands below the 8 % utility hurdle** — the relay arc's three-pass knife-edge (10.4 → 8.0 → 8.12 %) resolves downward on the fourth pass; the relay loses its NPV case. Falsified if any priced option holds d\* ≥ 8 %.

**H3 [W] (harvest ledger unified).** Honest relay harvest per delivered tonne **3.2–3.4×** (scripted 3.27) vs the monolithic's 3.53×: R182-H4's capture-exposure relief collapses from 23 % to **5–10 %** (scripted 7 %). Bet #1's exposure is architecture-invariant to first order. Falsified if honest relief ≥ 15 %.

**H4 [W] (the R173/R174 footnote).** The desk arc's canonical 300 kW lit leg (r ≤ 4 AU, 0.95 yr) carried **45–55 t** of EP propellant (scripted 50 t = 3.21 km/s of its 4.2 km/s inbound budget) that was never debited from delivered — up to **60–66 %** of the 80 t chunk at full utilization. Recorded as a convention footnote only; the arc's headline is already falsified (R179). Falsified if the recomputed propellant leaves band.

## Sweep (run.py)

Departure options {gas-impulsive, MET paper, MET flown} × N ∈ {2–5} × the R185 retention/hardware chain; d\* per cell vs hurdles {8, 10 %}; harvest-ledger table (mono / relay-shipped / relay-honest); lit-leg footnote at array power {100, 300 kW} × chunk {40, 80 t}. Grids span the pre-script's.

## Deliverables

`scope_bounds.py`, `run.py` (+ `results/relay_ledger.png`), `results/findings.json`, `STUDY.md` with Revisit; orchestrator notes: the relay-arc verdict flips (matrix + design-axes: "real, better, marginal" → **"real, dead at honest departure under every priced option"**), the unified ledger convention for all future rounds, and the R186→R182 propagation as the session's second one-round-later self-correction.
