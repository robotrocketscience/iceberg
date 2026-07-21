# R-shuttle-reuse-fleet — STUDY

**Round:** R-shuttle-reuse-fleet. SCOPE pre-registered 2026-07-21. All four hypotheses HELD after one run-time bug-catch.

## Results vs registered hypotheses — all HELD

### H1 — R182's optima bust the lifetime target — **HELD**

Both R182 winning cells exceed the 10 full-power-year design target inside a single mission (10.4 and 11.4 fpy). Lifetime-capped corrections: **paper-κ N=4, 0.46 t/t** (was 0.36); **flown-κ N=2, 2.00** (was 1.33 — still beats the monolithic's 2.41). R182's headline is hereby corrected forward.

### H2 — steady-state swap, and what the dream costs — **HELD**

With replacement reactor modules riding each mothership: steady-state **0.365 t/t**, the reactor being **60 % of recurring launch**; fleet-average at K=3 is 0.395. The naive reactor-immortal figure (0.146) is confirmed as fantasy accounting — it assumes a component with unlimited full-power-years.

### H3 — the reactor is the propellant — **HELD**

Pooled steady-state lpd: **0.33 / 0.27 / 0.24** at L = {10, 15, 20} fpy; the dream needs **L ≥ 40 fpy, four times an unmeasured program target**. Bet #3's demonstrator objective gains a formal lifetime clause: what must be demonstrated is full-power-years, not criticality.

### H4 — NPV restoration — **HELD**

Steady-state advantage over the monolithic: **2.79×**, restoring the waiver's break-even rate to **10.4 %** — the fleet-swap mechanism is what lifts the waiver+relay package back above the 8 % utility hurdle (R183's lifetime-capped tier sat exactly on it). The three rounds compose: relay (R182) needs the waiver, the waiver (R183) needs the fleet, the fleet (this round) needs reactor modules as consumables.

## Bug-catch (protocol §bug-catch)

The first run's swap-mission formula subtracted the shuttle bus from the recurring launch (a mangled edit over a leftover placeholder line), understating swap mass 43.8 vs 58.4 t and "falsifying" H2/H4 spuriously. Caught by comparison against the pre-script's registered model before any claim shipped; dead line removed. Lesson: **a run.py line ending in a hand-typed constant that the pre-script derives is a red flag** — same family as R174's seed-equals-output rule.

## Revisit (mandatory)

Life pooling across missions assumes reactor restart tolerance and cross-mission scheduling (unpriced); reactor-module swap in the staging orbit is a second new in-space operation (same family as R185's chunk handoff — the ops round should cover both); shuttle bus wear/refurb over multi-decade service unmodeled; flown-κ fleet numbers computed but not headline (they track the same structure at worse absolutes); disposal/end-of-life of spent reactor modules at Saturn unaddressed (planetary-protection flag for the orchestrator).

## Cross-learning

- **Matrix statements:** R182 single-mission headline corrected to **0.46** at the lifetime target; fleet steady-state **0.365** (discrete) / 0.33 (pooled); *the recurring cost of the relay fleet is reactor modules — bet #3 is not a one-time gate but the fleet's fuel line.*
- **Bet #3 demonstrator clause:** full-power-year accumulation is the qualifying metric.
- **Follow-ons:** ops round covering chunk handoff + reactor swap jointly (next); spent-module disposal; flown-κ fleet table for the matrix appendix.
