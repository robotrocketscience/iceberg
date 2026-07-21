# R-waiver-value-consolidation — what the 25-year waiver is actually worth, discounted

**Status:** SCOPE pre-registered 2026-07-21, before `run.py`. Bounds from `scope_bounds.py`, committed alongside.
**Worker:** worktree-115637 session. Adjudicates R182's own closing claim ("the L0-05 waiver is the campaign's most valuable programmatic lever") on the NPV side — the third round this week to put one of this session's claims on trial.

## Model

NPV per launched tonne; the relay's launch-mass advantage (R182: **2.83×** paper-κ, **1.81×** flown-κ; **2.22×** for the lifetime-capped N=4 variant that R-shuttle-reuse-fleet will establish) is bought with a **10.4-yr delivery delay** (23.5 vs 13.1 yr). Value ratio = advantage / (1+d_eff)^10.4 with d_eff compounding the discount rate (campaign hurdles 8 % utility / 10 % growth, `R_NPV` lineage) and a water-price decay path (no campaign time-path anchor exists — swept {0, 3, 7 %/yr} as open scenario, stated). **Fairness lemma:** per-launched-tonne NPV is cadence-invariant for the monolithic fleet (K serial missions scale linearly), so the two-point comparison is fleet-fair.

## Pre-registered hypotheses (bounds scripted)

**H1 [S] (break-even rates).** The waiver's break-even total effective rate: **10.2–10.8 %** at paper-κ (scripted 10.5), **5.6–6.2 %** at flown-κ (5.9), **7.7–8.3 %** for the lifetime-capped 2.22× advantage (8.0). Falsified outside bands.

**H2 [W] (at the campaign's own hurdles).** With zero decay: paper-κ relay **wins at the 8 % utility hurdle by 22–32 %** (scripted 1.27) and is a **wash at the 10 % growth hurdle** (1.00–1.10); flown-κ **loses at both** (0.81 at 8 %). Falsified outside bands.

**H3 [S] (decay kills fast).** Any price decay ≥ 3 %/yr at the 8 % hurdle sinks even paper-κ (scripted 0.94); the entire WIN region is {d_eff ≤ ~10.5 %} — one octant, not a robust regime. Falsified if the 8 %+3 % cell exceeds 1.0.

**H4 [W] (the conditioned lever).** Consequence hypothesis: R182's "most valuable programmatic lever" survives **only jointly with the specific-power bet** — the waiver is worth exercising iff reactor specific power reaches paper values (≥ ~10 W/kg) AND the program prices capital at the utility hurdle with a stable water price. Elsewhere the strict-schedule monolithic is NPV-preferred despite its 2.8× launch-mass penalty. The matrix must carry waiver and specific-power as coupled, not independent, levers. Held if H1–H3 hold.

## Sweep

d {4–14 %, step 0.5} × decay {0–8 %, step 0.5} × advantage tier {paper 2.83, lifetime-capped 2.22, flown 1.81}; d* solve per tier; WIN/WASH/LOSE partition.

## Deliverables

`scope_bounds.py`, `run.py` (+ `results/waiver_value.png`), `results/findings.json`, `STUDY.md` with Revisit; matrix note: the waiver/specific-power coupling, and the delay sensitivity (the advantage decays at ~9.6 %/yr of delay — every year shaved off Saturn residence is worth ~10 % of NPV ratio, which prices the sortie-tempo trades of R182 in financial units).
