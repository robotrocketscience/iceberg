# R-inbound-dark-leg-energy — STUDY

**Round:** R-inbound-dark-leg-energy. SCOPE pre-registered 2026-07-20; **first round with scripted bounds** (`scope_bounds.py`, committed before `run.py`).
**Worker:** worktree-115637 session. Owner-directed: the generator belongs on the return trip.

## Hypotheses, tests, results

### H1 — lit-window braking capability — **HELD**

1,575 m/s of thruster braking inside 3.5 astronomical units on direct array power (13.3 t of chunk water through the thruster; band 1.34–1.81 km/s). The array flown for outbound charging (round 172) pays a second time on the return.

### H2 — departure by banked gas — **HELD**

26.4 t of banked H2/O2 executes the 1.5 km/s Saturn-departure burn at 450 s; its 533 GJ charge fits inside the 645 GJ the 83 kW array harvests during the outbound sun-window. The darkest maneuver of the mission runs on sunlight collected four years earlier.

### H3 — full non-fission inbound closes at 40–55 t penalty — **FALSIFIED, in the variant's favor**

| metric | predicted | measured | held? |
| --- | --- | --- | --- |
| closes in sweep box | yes | yes (blue region: array ≥ ~115 kW) | — |
| cheapest closing penalty | 40–55 t | **36.8 t** (30 t bank + 150 kW array + thrust-to-4-AU) | **FALSIFIED** (below band) |

**Reading.** The first falsification of this arc that is not analyst arithmetic: the scripted pre-bound assumed gas-heavy closure (bank ≈ 40 t), but the sweep found that array mass at 120 W/kg out-trades banked gas per unit of braking — buy panels, not tanks. The registered belief about the *shape* of the solution was wrong; pre-registration surfaced it instead of letting the narrative absorb it.

### H4 — what the reactor is worth — **HELD**

Launch-mass-per-delivered-tonne of the cheapest non-fission variant: **1.74×** the reactor baseline. **Bet #3 reframes from a wall to a price:** without any fission, the inbound closes; the reactor's value is buying back ~43 percent of the launch stack, not the mission's existence.

## Revisit (mandatory)

The scripted-bounds convention worked on its first outing — H1 and H2 landed inside their scripted bands, and H3's miss was a genuine model-versus-belief discrepancy (the pre-script priced two points; the sweep explored the trade). Honest thinness to carry forward: (1) the lit-leg model spends harvested energy at a fixed arrival-stack mass rather than integrating the coupled trajectory — a full mission-graph encoding will move the 1,575 m/s figure by tens of percent, not orders; (2) the cryocooler chain carries mass but no sunshield structure mass; (3) **outbound power is excluded by the registered H5 boundary** — the non-fission variant still owes an outbound story (chemical kick + the same array as solar augment is the campaign's existing answer, unpriced in combination); (4) the 105 percent margin is thin for a 13-year mission. The 1.74× ratio is therefore a floor, not a estimate.

## Cross-learning

- **Adopt:** the owner's return-trip instinct, formalized: bank-on-the-way-out, spend-on-the-way-home. New named architecture variant for the matrix: **"solar-bank inbound"** — 150 kW-class array (double-duty: outbound electrolysis + augment, inbound direct drive), ~30 t H2/O2 bank (departure burn + mid-cruise residual), lunar-gravity-assist arrival. Fully non-fission inbound at 36.8 t penalty, 1.74× launch economics.
- **Supersedes in part:** R_non_fission_baseline's "fission-dependent, period" framing — the dependency is now quantified as a 1.74× economic multiplier on the inbound side, pending the outbound round.
- **For the orchestrator:** matrix Saturn-side-power axis gains the priced variant; mission-graph framework wants `solar_bank_inbound` phase options encoded so the canonical sweep can test it at full fidelity.
- **Follow-on (the load-bearing one): R-non-fission-round-trip** — combine chemical-kick outbound + solar-augment + this inbound; price the full stack against the reactor baseline end-to-end. If the round-trip ratio stays under ~2×, the campaign's three bets become two and a half.
