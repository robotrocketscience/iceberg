# Project ICEBERG

Project ICEBERG is a mission-concept study of harvesting multi-tonne water-ice chunks from Saturn's B ring and delivering them to Earth orbit as propellant feedstock. The chunk is also the return-leg propellant tank: the tug consumes its own cargo on the way home, feeding a water microwave-electrothermal thruster through a sublimation-capture trawl bag.

The physics of a commercial Saturn water round trip does not close on any technology in flight today. The one corridor that closes it on paper takes three unproven technology bets at once, and the financial model, built after fourteen months as an open dependency, comes back negative everywhere on that corridor. This is a paper study with no hardware and no booked flight, run as a 215-round adversarial analysis campaign. This repository documents the verdict and the campaign that produced it.

![Mission flight plan: ten phases, one bought chemical burn; every other maneuver is water-electrothermal or a free lunar gravity assist](plots/01a_flightplan.png)

The architecture, the method, the graveyard of killed claims, and the hardening of the verdict are written up at [robotrocketscience.com/projects/iceberg](https://www.robotrocketscience.com/projects/iceberg/).

## Campaign verdict (2026-07)

The early campaign swept architectures with the vehicle's dry mass as a free parameter and found thousands of conditionally-closing paths. The current mission-graph code closes the loop: vehicle mass is derived from what the vehicle carries, a conserved mass ledger is walked through every burn and jettison, and the power available in each phase must match the powerplant on board. Under that bookkeeping, the record-technology sweep enumerates 1,744 end-to-end mission paths and **zero of them complete the round trip**. The result holds for every flyable power class, at any delivery floor from 0.5 to 25 tonnes and any mission ceiling out to 35 years. Relaxing the ground rules does not help ([R_l0_relaxation_envelope](water-prop/rounds/R_l0_relaxation_envelope/)). No single performance parameter fixes it at any value, whether specific impulse, reactor power, dry-mass fraction, launcher capacity, or capture scale ([R_closure_boundary_inversion](water-prop/rounds/R_closure_boundary_inversion/)). Closure requires at least three levers moving at once.

Two corridors looked like they might close. The electric-return family died under direct integration. It had been priced at a 9.0 km/s Saturn departure, but a low-thrust spiral cannot buy the Oberth discount an impulsive burn gets, and the honest cost at flyable electric thrust is 22.5–24.2 km/s ([R_departure_anchor_resolution](water-prop/rounds/R_departure_anchor_resolution/)).

![Delta-v to leave Saturn versus thrust acceleration: the spiral cost falls from 24 km/s at low thrust toward the 8.6 km/s impulsive value only near 1 m/s2, far beyond flyable electric thrust](plots/18_departure_anchor.png)

The surviving corridor electrolyzes part of the harvested water into hydrogen and oxygen and burns it through a nuclear-thermal-class engine at 750–900 seconds of specific impulse ([R_saturn_water_v2_electrolysis_departure](water-prop/rounds/R_saturn_water_v2_electrolysis_departure/)). It needs:

- 500–1,000 tonnes of harvested ice per mission, which is two to three chunk captures ([R_multi_chunk_per_mission](water-prop/rounds/R_multi_chunk_per_mission/))
- a 150–200 kilowatt-electric reactor
- roughly 875–1,140 tonnes of launch mass in low Earth orbit ([R_per_phase_propellant_fidelity](water-prop/rounds/R_per_phase_propellant_fidelity/))
- a 25-year mission waiver

It delivers 32 to 88 tonnes of water. The corridor is an existence proof of what closure would take and is not a design: every element of it is at low technology readiness. Once the plan has more than one chunk, per-capture reliability of 95 percent or better becomes the binding requirement.

![The surviving corridor: two cells, 31.7 tonnes delivered for 875 tonnes of lift and 87.8 tonnes for 1,141 tonnes of lift; the electric family closes nowhere and the 209-tonne sovereign delivery class is unreachable](plots/19_corridor_map.png)

![Joint capture success probability versus chunks per mission: at 96.1 percent per capture the three-chunk mission holds 0.89; at the un-optimized 54.9 percent prior it collapses to 0.30 by two chunks](plots/21_capture_reliability.png)

The financial model settles the question the engineering left open ([R_corridor_financial_model](water-prop/rounds/R_corridor_financial_model/)). At the cheapest conceivable inputs (mature Starship launch at $100 per kilogram, a $0.5 billion marginal vehicle, an undiscounted dollar), the corridor's breakeven is $15,513 per delivered kilogram, 3.1 times the top defensible bulk price band. At a sovereign 3 percent discount rate it is $26,176. Delivered-water prices track falling launch costs down at roughly 13 percent per year. By the 19-to-21-year delivery date, every price band has decayed one to two orders of magnitude below breakeven, in a market whose anchored demand is 40–60 tonnes per year.

![Breakeven price versus decaying market price bands over the mission timeline: every band crosses far below the 15,513 dollar breakeven line years before the delivery window](plots/20_breakeven_race.png)

These lines of work survive the negative verdict:

- The demonstrator-track bench program: porous-ice penetration, capture-cinch mechanism reliability, and a new item, measuring the number density of hundred-tonne-class chunks in the ring, which no instrument has done.
- Sovereign or science-program framings that are valued on non-commercial grounds.
- A near-Earth-asteroid successor study that closes its mass loop on solar power where Saturn cannot ([R_near_earth_asteroid_mission_tree](water-prop/rounds/R_near_earth_asteroid_mission_tree/)).

## Engineering bets

The mid-campaign verdict reduced closure to three engineering bets. All of them still stand, and the surviving corridor stacks them:

1. Active chunk capture at scale. Nobody has actively captured a multi-tonne ring particle, and the multi-chunk corridor requires it two or three times per mission at 95 percent-plus reliability each.
2. Continuous water-fed propulsion on ring-sourced water. Lab thrusters reach the 700–900-second band in pulses on clean water. The corridor moves the burden to an electrolysis plant and nuclear-thermal burn, which trades one unflown propulsion mode for another.
3. A flight fission reactor on program schedule. The United States has flown one, in 1965, and cancelled six programs since. The corridor needs 150–200 kilowatts electric.

The financial rounds added what is effectively a fourth, economic bet and settled it in the negative: the market the mission would sell into decays faster than the mission can fly.

## Repository contents

| Path | Contents |
|---|---|
| [`ICEBERG-conops.md`](ICEBERG-conops.md) | Working concept of operations. Full math, costed mission breakdown, trawl-bag engineering treatment, economics, risk. |
| [`ICEBERG-pitch.md`](ICEBERG-pitch.md) | Executive-summary discussion draft, kept with its audit scars and current-status addendum. |
| [`ICEBERG-demand.md`](ICEBERG-demand.md) | Bottoms-up demand build per buyer, alternative-cost stacks, willingness-to-pay curves, lunar-resource crossover model. |
| [`ICEBERG-bag-engineering.md`](ICEBERG-bag-engineering.md) | Trawl-bag companion: particle cull sizing, permeability aging, stationkeeping delta-v during fill. |
| [`saturn-water-isru-sketch.md`](saturn-water-isru-sketch.md) | The original back-of-envelope sketch the architecture evolved from. |
| [`REQUIREMENTS.md`](REQUIREMENTS.md) / [`REQUIREMENTS-L1.md`](REQUIREMENTS-L1.md) | Level-0 and Level-1 requirements with a variance log. |
| [`RISKS.md`](RISKS.md) | Risk register. |
| [`TRADE-end-of-mission-conops.md`](TRADE-end-of-mission-conops.md) | End-of-mission disposal trade study. |
| [`design-axes/`](design-axes/) | 22 architecture-decision-record files, one per design axis, with append-only history. |
| [`water-prop/`](water-prop/) | The analysis campaign: 215 rounds under `rounds/`, each with a pre-registered study document and a runnable `run.py`; reusable physics models under `src/waterprop/`; the closed-loop mission-graph code under `sims/mission_graph/` (179 tests). |
| [`plots/`](plots/), `*.py` at root | Concept-of-operations plots and the scripts that generate them. The corridor-era figures regenerate from [`water-prop/scripts/plot_corridor_figures.py`](water-prop/scripts/plot_corridor_figures.py). |

## Reproduce the analysis

The campaign code is Python, managed with [uv](https://docs.astral.sh/uv/).

```bash
cd water-prop
uv sync
uv run pytest tests/          # physics-model sanity tests
PYTHONPATH=src:sims uv run pytest sims/mission_graph/tests/   # closed-loop framework tests
uv run python rounds/R_closure_boundary_inversion/boundary_sweep.py   # or any other round
```

The root-level scripts (`saturn_isru_boe.py`, `saturn_rendezvous_sim.py`, `generate_conops_plots.py`) need numpy, scipy, and matplotlib, and regenerate the plots in `plots/`.

A few rounds' large sweep outputs (multi-megabyte JSON) are excluded from the repository. Each regenerates from its round's `run.py`.

## Method

The campaign runs on a pre-registered protocol ([`water-prop/PROTOCOL.md`](water-prop/PROTOCOL.md)). Each round states its hypotheses and falsification criteria in a SCOPE or STUDY document before the run, results land unedited, and retractions are recorded instead of erased.

The final stretch turns the protocol on the campaign itself. One round uses data to retract one of the orchestrating agent's own headline claims ([R_per_phase_propellant_fidelity](water-prop/rounds/R_per_phase_propellant_fidelity/)). Another traces a closure revival to a simulation bug and reverses it ([R_closing_path_self_consistency](water-prop/rounds/R_closing_path_self_consistency/)). A standing rule requires any newly claimed closure surface to ship a hand-checkable mass-ledger walk before it may be cited.

AI research agents (Claude) carried out the work in parallel orchestrated sessions. Human direction set the questions, locked ground-truth findings, and killed assumptions that failed audit. Round documents attribute work to session codenames (titan, rhea, phoebe, and other Saturn moons).

## Excluded material

Some round documents cite internal working files: a session log, a planning registry, a business-planning thread (`startup/`), and orchestration protocols. Those files stay in the private working repository, which remains active. The citations are left intact instead of rewritten so the paper trail stays honest. This repository is a curated snapshot with fresh history.

MIT licensed.
