# R-k2-bus-architecture-study — RESULTS

**Worker:** hyperion (re-spawn 2). **Date:** 2026-05-26. Research/strategy round; no code (per SCOPE). Facts in `COMPARISON.md`, all cited.

## Headline

**K2 Space has flown (Feb 2026) a mass-produced, $3B-backed solar-electric bus at ~10–20 W/kg — the productized form of exactly the light-powerplant path that lets the near-Earth-asteroid architecture close the closed-loop mass loop. K2 is the buyable chassis for the ICEBERG inner-system / NEA successor and for the demonstrator, but it is fundamentally dead at Saturn (solar at 9 AU yields ~1% of its 1-AU rating), and it is NOT a framework-physics change — so no new sweep axis is warranted.**

## Hypothesis verdicts

| # | Verdict | Basis |
|---|---|---|
| H1 | **HELD** | Mega ~10–20 W/kg system (20 kW / ~2 t wet to ~1 t dry-bus) — 4–8× KRUSTY fission (2.4), ~2–4× flown RTG (5.3); first *flown* hardware in that band. |
| H2 | **HELD** | K2 is solar-only; at 9 AU a 20-kW (1 AU) array → ~0.2 kW. The solar-at-Saturn gap is **fundamental physics, not a contracting gap**. K2 serves inner-system / NEA; cannot serve Saturn without ceasing to be "a K2 bus." |
| H3 | **HELD** | A 40-kWe K2-derived power-bus (~2–3 t at 10–20 W/kg system) sits far inside the NEA closed-loop dry-mass budget (~45 t) and is ~15× lighter than Saturn's fission stack. K2-anchored flown numbers **corroborate** the NEA mass-loop closure. |
| H4 | **HELD** | Procure favors the demonstrator (flown, mass-produced, $60M-class units vs clean-sheet NRE). The binding risk is **deep-space heritage** (K2 has LEO/MEO/GEO/cislunar only; ICEBERG cruise is 7+ yr), not cost. |
| **H5 (load-bearing)** | **HELD** | K2 vs clean-sheet is a cost/heritage/supply-chain distinction that does **not** change any framework-computed closure output (mass, power, delivered water). **No `vehicle_bus_architecture` enum axis is warranted.** The only framework-relevant toggle is `power_source ∈ {solar, fission}`, which the NEA round already introduced de facto at the mass-demand layer. |

**5/5 held.**

## Framework-parameter recommendation (SCOPE deliverable 2)

**Do NOT add a `vehicle_bus_architecture` sweep axis.** Rationale:
- The framework computes physics (closed-loop dry mass, power, delivered water). K2-vs-clean-sheet changes *cost, schedule, heritage, supply-chain* — none of which the closure predicates evaluate. Adding a vendor axis would multiply the sweep without changing any closure verdict (a leaky abstraction in the opposite direction: encoding business facts as physics axes).
- The one genuinely physics-relevant distinction — solar vs fission powerplant — is already captured: `saturn_mass_demands.py` (fission) vs `nea_mass_demands.py` (solar), via the closed-loop demand-function seam. Recommend the orchestrator document this as the canonical `power_source` distinction and note K2 as the real-world solar-bus anchor for the `nea_mass_demands` solar specific-power inputs (replace the array-only 150 W/kg with a K2-anchored whole-bus 10–20 W/kg as a conservative-fidelity option in the fidelity-refinement round).
- K2 belongs in **three non-framework places**: the demonstrator cost/heritage narrative, the NEA-successor conops, and the pitch (a flown, funded existence-proof that the inner-system solar-electric chassis is buyable today).

## Procure-vs-build decision criterion (SCOPE sub-question 5)

For a **demonstrator** (non-nuclear, inner-system, ≤100 kWe): **procure a K2 Giga (or Mega-derived) bus** — it is flown, mass-produced, and cheap relative to clean-sheet NRE; one Giga (100 kW) covers the 40–100 kWe need with no on-orbit assembly. The go/no-go gate is **deep-space qualification of the K2 line for a 7-yr cruise**, which is a heritage-extension contract conversation with K2, not an ICEBERG build decision. For **Saturn commercial-class**: K2 is irrelevant (solar dead; the binding constraint is the fission reactor program, L0-24).
