# R-spent-reactor-disposal — where the activated core goes, and what that constrains

**Status:** SCOPE pre-registered 2026-07-21, before `run.py`. Bounds from `scope_bounds.py`, committed alongside. A lean round: two computed Δv numbers, an inventory bound, and the planetary-protection constraint set. **Introduces external data** (KRUSTY fuel mass, Cassini disposal precedent, COSPAR framing) — cited below.
**Worker:** worktree-115637 session. R185's Revisit named it: *"reactor-swap dose/criticality handling near a crewless but instrumented mothership unexamined"*; the broader gap is end-of-life disposal of a fission core in a system containing an ocean world.

## The two disposal problems

1. **Monolithic (state-of-record post-R187):** the reactor powers the 8-yr return-transit chunk-fed spiral (mission_graph phase 4), so it **returns with the mothership** and is disposed near Earth/delivery — the planetary-protection concern moves to **cislunar** (an activated reactor arriving in the delivery zone).
2. **Fleet / relay (R184 reactor-swap; NPV-dead post-R187 but architecturally live):** each swap leaves a **spent core at Saturn**, which must be disposed into Saturn's atmosphere — the **Cassini precedent**.

## External anchors (cited)

- **KRUSTY core:** 32.2 kg fuel, **27.7 kg U-235**, 93 wt% enriched U-8Mo ([KRUSTY Reactor Design, *Nuclear Technology*](https://www.tandfonline.com/doi/full/10.1080/00295450.2020.1725382)). A bare HEU fast core is **critical-mass-bound**, so fuel scales weakly with kWe.
- **Cassini disposal:** deliberately flown into Saturn 2017-09-15 to deny even a **~1-in-10⁶ chance** of striking Enceladus or Titan ([NASA/JPL](https://www.jpl.nasa.gov/edu/resources/teachable-moment/a-moment-you-wont-want-to-miss-cassinis-mission-finale-at-saturn/); [SwRI](https://www.swri.org/newsroom/technology-today/cassinis-grand-finale); [NASA Science](https://science.nasa.gov/mission/cassini/grand-finale/overview/)). Enceladus's global subsurface ocean and Titan's organics are the protected targets.

## Pre-registered hypotheses (bounds scripted)

**H1 [S] (disposal Δv, and the R186 asymmetry).** Controlled deorbit of a co-orbital B-ring reactor into Saturn's atmosphere is **2.6–3.0 km/s** (scripted 2.78 — lower periapsis to atmosphere-grazing, apoapsis at the ring). From a Titan-crossing staging orbit the periapsis-lowering is **0.4–0.6 km/s** (scripted 0.518), **inside a single Titan flyby's capacity 1.1–1.3 km/s** (scripted 1.229) → **disposal is free via one flyby, the Cassini method**. Registered asymmetry vs R186: **Titan can LOWER periapsis (disposal, free) but cannot RAISE v∞ (departure, capped ~3.3) — the well helps going down, not up.** Falsified if the flyby cannot cover the periapsis-lowering, or the co-orbital deorbit lands outside 2.6–3.0.

**H2 [S] (inventory and deorbit mass).** U-235 per Kilopower unit **27.7 kg** (critical-mass bound); operational burnup over ~3 fpy at ~500 kWth is **0.4–0.8 kg** (scripted 0.58) — the fuel is barely touched; the hazard is the fission-product inventory + activation, not fuel depletion. Deorbiting a spent core **parked co-orbital** (not on a Titan orbit) costs **43 % of reactor mass** in MET propellant: **6–8 t (paper κ, 16 t reactor) / 26–30 t (flown κ, 65 t reactor)** (scripted 6.6 / 27.5). Falsified outside bands.

**H3 [W] (planetary protection).** Enceladus (subsurface ocean, active plumes) and Titan (organics, subsurface water) make the Saturn system COSPAR-governed; the Cassini precedent sets the bar (controlled high-probability Saturn atmospheric disposal, refusing even ~10⁻⁶ moon-strike risk). Anything left at Saturn must be disposed into the atmosphere. The **monolithic's returning reactor shifts the concern to cislunar** — an activated core in the delivery zone, a distinct and arguably harder political/regulatory constraint. Held if the framing is precedent-anchored and the two-architecture split is correct.

**H4 [W] (cheap and precedented, but constraining).** Disposal is **not a binding bet** — cheap (≤ 2.8 km/s, free via Titan) and precedented (Cassini). But it imposes three design constraints: **(a)** the reactor must be **separable and independently disposable** (cannot depend on a mothership that may not return); **(b)** the fleet must **reserve one Titan disposal flyby per spent core** (park spent cores on a Titan-crossing orbit, not co-orbital, to keep disposal free); **(c)** the monolithic delivers an **activated reactor to cislunar** — an **unpriced** delivery-zone PP/safety constraint, the sharp one. Falsified if disposal Δv proves material vs the departure budget, or if the separability/cislunar constraints turn out free.

## Sweep (run.py)

Disposal Δv ladder (co-orbital deorbit, staging-ellipse periapsis-lower, single-flyby capacity, departure reference) vs periapsis target ∈ [R_1bar, ring]; deorbit propellant vs reactor mass over κ ∈ [100, 417] × P ∈ [30, 175] kWe; the architecture disposal-destination table. Grids span the pre-script's.

## Deliverables

`scope_bounds.py`, `run.py` (+ `results/reactor_disposal.png`), `results/findings.json`, `STUDY.md` with Revisit; orchestrator notes: disposal enters the risk register as a **solved-in-principle line with three design constraints**, not a bet; the **cislunar activated-reactor constraint (c) is flagged as unpriced** and named for a follow-on; the R186 departure/disposal Titan-asymmetry is recorded.
