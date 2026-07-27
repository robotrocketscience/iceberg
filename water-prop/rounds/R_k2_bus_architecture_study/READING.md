# R-k2-bus-architecture-study — READING (5-section template)

**Worker:** hyperion (re-spawn 2) · **Date:** 2026-05-26

## Hypotheses adjudicated

H1 **held** (Mega ~10–20 W/kg, flown) · H2 **held** (solar-at-Saturn gap is physics, not contracting) · H3 **held** (K2-anchored numbers corroborate NEA mass-loop closure) · H4 **held** (procure favors demonstrator; heritage is the binding gap) · **H5 (load-bearing) held** (no `vehicle_bus_architecture` axis; the physics-relevant distinction is `power_source ∈ {solar, fission}`, already captured).

## Headline

**K2 Space is the existence-proof for the inner-system half of the ICEBERG comparator.** This session's NEA round found that solar-electric power at ~1 AU closes the closed-loop mass loop where Saturn fission (0/150) cannot — that solar is the light-powerplant path. K2 has now *flown* (Gravitas, Feb 2026) a mass-produced, $3B-backed bus that is precisely that path productized: 20 kW at ~10–20 W/kg, multi-orbit, stackable to 200 kW/launch, with a 100 kW Giga announced. **K2 is the buyable chassis for the NEA / inner-system successor architecture and for a non-nuclear demonstrator — and it is fundamentally useless at Saturn.** That asymmetry is not a K2 limitation to engineer around; it is the same solar-vs-fission, 1-AU-vs-9-AU split that defines the whole Saturn-vs-NEA dual.

## Reading (for the project owner)

1. **Use K2 in the pitch and the demonstrator plan, not in the framework.** It is a flown, funded, mass-produced answer to "where does the inner-system ICEBERG vehicle come from?" — procure, don't build, for the demonstrator. But it changes no closure physics; resist the temptation to add a bus-vendor sweep axis (H5).
2. **K2 sharpens the Saturn-vs-NEA dual into a sourcing statement.** NEA-successor: the vehicle is buyable today (K2-class solar bus); the gate is target water fraction (per the NEA round) and 7-yr deep-space qualification of the K2 line. Saturn: no vendor solves it; the gate remains the fission reactor program (L0-24). The two architectures differ not just in failure mode but in *whether the vehicle can be bought off a production line* — and only the NEA one can.
3. **One fidelity hand-off:** the NEA mass model used an array-only 150 W/kg solar specific power. K2's flown whole-bus 10–20 W/kg is a stricter, real-hardware anchor. Recommend the fidelity-refinement round (titan-6 D5 successor, now SCOPE'd) swap in a K2-anchored whole-bus solar number as a conservative option; it does not break NEA closure (~2–3 t power-bus ≪ 45 t dry), but it makes the NEA vehicle numbers defensible against flown hardware rather than a component-level array figure.

## Cross-learning

- **Corroborates R-near-earth-asteroid-mission-tree (this session):** K2's flown 10–20 W/kg solar bus is independent real-world confirmation that the inner-system solar-electric vehicle is light and buildable today — strengthens the NEA mass-loop closure (H3) with flown hardware rather than a paper array figure.
- **Negative for any K2-at-Saturn hope:** the solar-at-Saturn gap is fundamental (1% flux at 9 AU). No K2 product or contract closes it; only a grafted reactor would, at which point it is not a K2 bus and inherits the fission mass-floor kill (titan-6, 0/150).
- **For the fidelity-refinement round (titan-6 D5 successor):** adopt K2 whole-bus specific power as the conservative solar anchor in `nea_mass_demands.py`.
- **Methodology note:** the SCOPE asked "should we add a `vehicle_bus_architecture` axis?" The honest answer is no — a vendor/procurement distinction is not a physics axis. Encoding business facts as sweep axes is the mirror of the campaign's existing lesson about keeping the framework physics-faithful; flagged as a small guard.

## Revisit

Prediction held (5/5). The reframe the round added beyond the SCOPE: K2 is not just "inspiration for demonstrator-era vehicles" (SCOPE framing) — it is the *sourcing answer for one specific arm of the Saturn-vs-NEA dual*, and the dual is now expressible as "can you buy the vehicle off a line?" (NEA: yes; Saturn: no). That is the most decision-useful framing for a pitch conversation.

---

## Conops sketch (SCOPE deliverable 3) — "a K2-style ICEBERG demonstrator"

**One-paragraph pitch slide:**

> The ICEBERG demonstrator does not need a clean-sheet spacecraft. K2 Space flew a 20-kW, mass-produced, multi-orbit bus in February 2026 and has a 100-kW Giga announced — at ~10–20 W/kg, 4–8× the specific power of any flight reactor. A demonstrator-class ICEBERG vehicle is a single K2-class Giga bus (100 kW solar-electric, ~3 t), procured rather than built, flying a commercial radio-frequency-ion thruster and a bag/harpoon capture experiment to a low-delta-velocity near-Earth asteroid (e.g. 2008 EV5, 6.29 km/s) — the *inner-system* arm where solar power is abundant. It retires the two demonstrator bets (capture at scale; continuous electric propulsion on extracted water) on a flown, fundable chassis, at ~1 AU, with no reactor on the critical path. Saturn-class commercial delivery remains gated on the fission reactor program (L0-24) and is explicitly a *later, separate* bet — the demonstrator buys down inner-system risk on hardware you can order today.

**What it is NOT:** a Saturn vehicle (solar dies at 9 AU), a megawatt stack (fantasy-conditioned), or a framework change.
