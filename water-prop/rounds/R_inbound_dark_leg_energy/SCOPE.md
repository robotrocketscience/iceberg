# R-inbound-dark-leg-energy — can the return leg run without fission?

**Status:** SCOPE pre-registered 2026-07-20, before `run.py` was written or executed. **All numeric bounds below derive from `scope_bounds.py` (committed alongside this SCOPE) — the scripted-bounds convention adopted in R172's Revisit, applied for the first time.**
**Worker:** worktree-115637 session. Owner-directed: "the generator should work on the return trip — that's where the power is most needed."
**Predecessors:** R_h2o2_closed_cycle_power_bridge (chemical energy cannot feed electric propulsion per kg of *launched* reactant); R_regenerative_solar_electrolysis_bank (solar-charged bank closes for hotel/burst; 83 kW-class array aboard); R_non_fission_baseline (Architecture A busts L0-05 by 1–4 yr on the Saturn-side power gap).

## Framing

The owner's instinct — return-leg power is the mission's real power problem — is correct: the inbound burn spends the payload. The correction carried in from round 171: chunk water is reaction mass, not energy (water is combustion product; electrolyzing it costs more than burning it back returns). The variant under test time-shifts *solar* energy into the dark leg: bank H2/O2 during the outbound sun-window, **burn it directly** (450 s) for the Saturn-departure burn, run the thruster **directly on the array** once the return trajectory re-enters sunlight, and take the lunar-gravity-assist arrival for free. Direct burn of the banked gas — never fuel-cell-fed electric propulsion — per round 171's H1 dominance result.

## Pre-registered hypotheses (bounds from `scope_bounds.py` output, ±15 percent where banded)

Canonical case: 40 t chunk, 20 t dry ship, inbound budget 4.2 km/s (departure 1.5, cruise braking 2.0, trim 0.5, reaction control 0.2), lunar-gravity-assist arrival credited separately as in the conops.

**H1 (lit-window capability).** Thrusting on direct array power inside 3.5 astronomical units of the return leg (scripted window 0.78 yr, 684 GJ at the 83 kW array) yields **1.34–1.81 km/s** of braking delta-v on the 60 t arrival stack (scripted center 1.575 km/s). Falsified outside the band.

**H2 (departure by banked gas fits the existing bank chain).** The 1.5 km/s Saturn-departure burn at 450 s on the departure stack requires **22.4–30.4 t** of banked gas (scripted center 26.4 t), whose charge energy (scripted 533 GJ) fits within the outbound sun-window harvest of the round-172 array (scripted 645 GJ; array-needed 69 kW ≤ 83 kW aboard). Falsified if the gas mass leaves the band or the charge exceeds the harvest.

**H3 (the full inbound closes non-fission, at a price).** Sweeping bank size ≤ 55 t, array 60–150 kW, lit-thrust radius 3–4 AU: at least one corner covers the full 4.2 km/s budget with margin ≥ 5 percent, and the **minimum launch-mass penalty of any closing corner is 40–55 t** (gas water + 20 percent tankage + cold-tier cryocooler chain; scripted partial-closure floor 31.9 t plus ~14 t residual gas). Falsified if nothing closes in the box, or if a closing corner beats 40 t.

**H4 (what the reactor is actually worth).** Launch-mass-per-delivered-tonne of the cheapest closing non-fission variant is **≥ 1.6×** the reactor baseline's. Falsified below 1.6×. (Consequence if held: bet #3 reframes from "no fission, no mission" to "fission buys back roughly half the launch stack" — a price, not a wall.)

**H5 (boundary, by citation).** Outbound-leg power accounting (chemical kick + solar augment vs reactor spiral) is NOT retested here; the sweep charges the variant only for inbound-side hardware and gas. Full-round-trip non-fission accounting is the named follow-on.

## Deliverables

1. `scope_bounds.py` (pre-script, committed with this SCOPE), `run.py` (full sweep), `results/dark_leg_closure.png`, `results/findings.json`.
2. `STUDY.md` with Revisit; matrix-axis note for the orchestrator (Saturn-side power axis gains a priced non-fission inbound variant).
