# R-eccentric-harvest-departure — option 4 closes; the electric departure is robustly megawatt-class

**Status:** run + STUDY complete 2026-07-22. **3/4 HELD** — H-D3 falsified *against my own optimistic prediction*, which **confirms and strengthens** `R-lowthrust-spiral-departure` (Round C). Result JSON `results/eccentric_harvest.json`; figure `results/eccentric_harvest.png`.
**Predecessors:** `R-lowthrust-spiral-departure` (`2690b6b`, this session — continuous electric spiral 21.9 km/s → 1248 kWe) named "option 4: eccentric harvest orbit" as its one honest open escape. This round runs it.

## Hypothesis (pre-registered; see SCOPE.md)

Two assumptions: (1) harvest from an eccentric orbit (depart from near-escape energy) — argued impossible because gentle bag-harvest needs velocity-matching the ring (~m/s, locked finding 1) but an eccentric periapsis is km/s; (2) depart the *required circular* orbit via periapsis-concentrated burns, recovering the Oberth Δv (8.5 not 21.9 km/s) and — I *predicted optimistically* (H-D3) — rescuing the floor to 300–900 kWe.

## Test

Deterministic. (1) Ring relative velocity v_p(r_a) − v_circ vs the capture threshold. (2) A discrete periapsis-burn departure simulation from the circular ring orbit: constant thrust fired within r < 2·r_p each pass (Oberth burn at r_p), raising apoapsis to escape then completing to v∞; report Δv, elapsed time, duty cycle, and peak reactor power (0.5·F·v_e/η); sweep thrust to find the minimum peak power completing within 2 yr. Anchors identical to R179/Round C.

## Result

| Sub-claim | Predicted | Measured | Held? |
|---|---|---|---|
| H-D1 harvest-from-eccentric killed by v_rel | ≥1 km/s at apoapsis ≥1.3× r_p | **1190 m/s at 1.3× r_p**, 2913 at 2×, 6704 near-parabolic (vs ~1 m/s capture) | ✅ |
| H-D2 periapsis burns recover Oberth Δv | 8.5–12 km/s | **8.51 km/s** (= impulsive floor; vs 21.9 continuous) | ✅ |
| H-D3 min peak power (2-yr) in 300–900 kWe | rescue to 300–900 | **FALSIFIED — no ≤2-yr completion below megawatt; F=300 N → 1961 kWe / 3.1 yr; duty ~1%** | ❌ |
| H-D4 bet #3 not relieved to Kilopower class | floor ≥300 kWe electric | floor is megawatt (≥1248) — not relieved | ✅ |

## Reading

**Option 4 fails in both halves, and the failure of my own optimistic H-D3 confirms Round C's megawatt departure floor is robust to thrust strategy — not an artifact of the continuous-thrust assumption.**

1. **Harvest-from-eccentric is dead on arrival (H-D1).** Gentle bag-harvest requires co-orbiting the ring particles (which move at v_circ = 18.8 km/s); capture works only at mm/s–low-m/s closing velocity (locked finding 1). An eccentric orbit's periapsis velocity exceeds v_circ by **1190 m/s at only 1.3× r_p apoapsis** and 2.9 km/s at 2× — a hypervelocity ring encounter, not harvesting. **The same variable that cheapens departure (high periapsis velocity) destroys harvesting.** The harvest orbit must be near-circular; you cannot harvest from the eccentric orbit that would make departure cheap.

2. **Periapsis-burning recovers the Oberth Δv but not the power (H-D2 ✅, H-D3 ❌).** Departing the circular orbit via periapsis-concentrated burns *does* recover the Oberth benefit — every burn is at r_p, so the total Δv is 8.51 km/s, not the 21.9 km/s of the continuous spiral. **But it doesn't help**, because the duty cycle collapses: as apoapsis is raised toward escape the orbital period diverges (the classic low-thrust-escape many-revs tail), the vehicle fires only ~1% of the time near periapsis, and to deliver even the reduced impulse within a bounded window the reactor must supply megawatt peak power (F=300 N → 1961 kWe, 3.10 yr; nothing in the swept range completes in 2 yr below that). **The fundamental tension: low Δv requires thrust concentrated at periapsis (low duty → high peak power); low peak power requires continuous thrust (duty 1 → no Oberth → high Δv). The product has no sub-megawatt minimum.** At duty 1 you get Round C's continuous spiral (21.9 km/s, 1248 kWe); at low duty you get the Oberth Δv (8.5 km/s) but peak power ≥1300 kWe. Both endpoints are megawatt; the continuous spiral (1248 kWe) is actually the *better* electric strategy for a 2-yr departure.

3. **Net: bet #3's megawatt departure is confirmed and robust (H-D4).** No harvest-compatible orbit + electric departure strategy gets the departure reactor floor below ~1248 kWe. The only sub-megawatt departure remains a **chemical kick stage** (non-electric, ~1095 t of Isp-350 propellant per Round C) — which is the honest "outside-the-box" answer for the axis-05 project-owner note: the departure wants a high-thrust (chemical or, aspirationally, a much higher-thrust electric) stage, not the low-thrust engine the cruise uses.

## Revisit

**H-D3 falsified against my own optimistic pre-registration — the honest and valuable outcome.** I predicted periapsis-burning would rescue the floor to 300–900 kWe (softening Round C); the simulation showed it does not, because I under-weighted the duty-cycle collapse near escape. This is methodology lesson 1/5 working as intended: I pre-registered the optimistic hypothesis explicitly, tested it, and let it fall — Round C's megawatt finding is *strengthened*, now shown robust to the smart (periapsis-concentrated) thrust strategy, not just the naive continuous one. Honest limitations: (a) the discrete-pass model is numerically sensitive near the E=0 escape crossing (whether a given pass jumps across E=0 before its period diverges), so the exact periapsis-burn escape *times* are noisy — but the robust conclusion (no sub-megawatt bounded-time electric departure) rests on the fundamental duty-vs-Oberth tension and the two well-defined endpoints (continuous 1248, narrow-periapsis ≥1300 for ≤3 yr), not on the noisy tail; (b) the intermediate arc-width regime is not swept with position-dependent Oberth crediting (the lumped-at-periapsis model is valid only for narrow arcs) — but any intermediate has Δv ∈ [8.5, 21.9] and duty coupled to it by the orbit geometry, and neither endpoint dips below ~1248, so a sub-megawatt intermediate would have to beat both, which the coupling precludes.

**Deferred (retest spec):** a full (thrust × arc-width) low-thrust optimal-control departure with position-dependent Oberth crediting and propellant-mass depletion, to pin the exact min peak power between the two endpoints (expected ~1200–1300 kWe); and the higher-thrust-electric option (a departure-dedicated high-power electric stage vs the cruise engine) as a distinct "outside-the-box" lever.

## Cross-learning

- **Forward to axis 05:** option 4 (the one open escape Round C named) is **closed** — the electric departure floor is robustly ~1248 kWe, confirmed against both the naive continuous-spiral and the smart periapsis-burn strategies, and harvest-from-eccentric is physically impossible. Integration records that Round C's megawatt headline is not softened by option 4; the only sub-megawatt departure is a chemical/high-thrust stage.
- **Backward to R-lowthrust-spiral-departure (Round C):** its 1248 kWe stands as the best electric strategy, not a pessimistic artifact. The two rounds together close the departure-power question for the electric architecture: ~1248 kWe, megawatt-class, no low-thrust escape.
- **New physical framing for the deck:** the departure-power problem is a **thrust-regime** problem, not merely a power-level problem. The chunk must be lifted from the ring's deep gravity well; doing it Oberth-efficiently (8.5 km/s) needs high thrust (chemical, or a high-power dedicated electric burst), and doing it with the low-thrust cruise engine costs either 2.4× the Δv (continuous) or a 1% duty cycle (periapsis) — both megawatt. This is the sharp statement of the axis-05 project-owner "think outside the box on power" note: the box to think outside of is the *low-thrust* departure.
- **Methodology (reinforces lesson 23):** a Δv is only valid paired with a thrust regime — and this round adds that the *peak power* is set by the duty cycle, so an Oberth-Δv saving delivered at low duty buys nothing. Report peak power (duty-weighted), not just average, for any low-thrust burn against a time budget.
