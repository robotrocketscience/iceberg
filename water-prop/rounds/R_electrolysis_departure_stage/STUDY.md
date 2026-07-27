# R-electrolysis-departure-stage — a reactor-charged H₂/O₂ departure stage is the leading lever: megawatt → few-hundred-kWe, but not Kilopower

**Status:** run + STUDY complete 2026-07-22. **4/4 HELD.** Result JSON `results/electrolysis_departure.json`; figure `results/electrolysis_departure.png`.
**Predecessors:** `R-lowthrust-spiral-departure` (`2690b6b`) + `R-eccentric-harvest-departure` (`c17d088`) — the electric low-thrust departure is robustly ~1248 kWe (megawatt); the only sub-megawatt departure is a high-thrust burn. This round evaluates the water-compatible high-thrust option, the "outside the box" lever the project owner asked to pursue.

## Hypothesis (pre-registered; see SCOPE.md)

Decouple departure from the cruise engine: the reactor electrolyzes harvested water into H₂/O₂ over the Saturn dwell (steady average power, storing energy chemically), then a high-thrust H₂/O₂ engine does the Oberth-efficient impulsive 8.5 km/s departure. Predicted a genuine partial win — roughly halving both reactor power and departure water propellant — that does not reach Kilopower class and adds a cryo-H₂ storage problem.

## Test

Deterministic. Three-way departure trade (reactor power, harvested-water propellant, added dry mass, delivery efficiency, risk): electric low-thrust spiral (Round C baseline), reactor-charged H₂/O₂ chemical impulsive (Isp 380/420/450 s; electrolysis 20 MJ/kg over dwell 1/2/3 yr; added mass = plant + cryo tanks + engine), and reactor-thermal steam (Isp 190 s, no cryo). Plus the Kilopower-window check and the just-in-time-electrolysis power spike (the cryo-avoidance alternative). Anchors as R179/Round C.

## Result

| Architecture | Δv | Isp | water prop | reactor | delivery-eff | added dry |
|---|---|---|---|---|---|---|
| Electric low-thrust spiral | 21.9 km/s | 800 s | **1531 t** | **1248 kWe** (peak) | 6.1 % | 0 |
| **H₂/O₂ (electrolysis)** | 8.51 km/s | 420 s | **690 t** | **146–437 kWe** (avg, 3–1 yr dwell) | 12.7 % | ~37 t |
| Reactor-thermal steam | 8.51 km/s | 190 s | 9545 t | — | 1.0 % | (prohibitive) |

| Sub-claim | Predicted | Measured | Held? |
|---|---|---|---|
| H-F1 chemical uses less water than electric | 586–882 t < 1531 t | **690 t (Isp 420) < 1531 t**; delivery-eff 6.1 %→12.7 % | ✅ |
| H-F2 reactor few-hundred kWe, not Kilopower | 250–600 kWe; Kilopower needs >15 yr | **146–437 kWe** (dwell 3–1 yr); Kilopower-window **15 yr** | ✅ |
| H-F3 added dry mass + forced cryo-H₂ | ≥ several t; boiloff first-order | **37 t** (34.5 t cryo tanks + 2.2 t plant + 0.5 t engine); **77 t H₂ at 20 K**; just-in-time electrolysis spikes to 887–5325 kWe → cryo forced | ✅ |
| H-F4 not relieved to Kilopower | reactor ≥ 40 kWe | 146 kWe at a generous 3-yr dwell | ✅ |

## Reading

**The reactor-charged H₂/O₂ departure stage is the leading departure-architecture candidate and the honest answer to the project-owner "think outside the box on power" note — it is a real, quantified partial win, not a silver bullet.**

1. **It relieves the reactor power by 3–9×** (1248 → 146–437 kWe, dwell-dependent) by converting the reactor's job from *deliver peak power during a low-thrust departure burn* to *deliver average power for electrolysis over the Saturn dwell*, storing the energy chemically in H₂/O₂. The high-thrust chemical burn then spends that stored energy impulsively at the ring, capturing the Oberth effect the low-thrust engine could not.

2. **It also roughly halves the departure water propellant** (1531 → 690 t) and **doubles the departure-leg delivery efficiency** (6.1 → 12.7 %), because the Oberth Δv (8.5 km/s) beats the electric spiral's 21.9 km/s by more than Isp 800 beats Isp 420. This is the counterintuitive win: a *lower-Isp* propellant delivers *more* payload here because it can burn impulsively deep in the well. (Reactor-thermal steam is rejected: Isp 190 s makes propellant prohibitive at 9545 t.)

3. **But it does not relieve bet #3 to Kilopower class.** Electrolysis is fundamentally hundreds of kWe: a Kilopower-class (30 kWe) electrolysis of the ~690 t departure propellant would take a **15-year dwell**. The reactor is still 146–437 kWe — 5–15× the flyable Kilopower envelope — so bet #3's power problem is *softened from megawatt to few-hundred-kWe*, not solved.

4. **And it introduces a forced cryo-H₂ storage problem.** The H₂/O₂ propellant is 11 % H₂ by mass — **77 t of liquid H₂ at 20 K** stored over the multi-year dwell. Saturn's ~90 K ambient helps the O₂ (near its 90 K boiling point) but not the H₂. You cannot dodge it by electrolyzing just before departure: a 30–180-day just-in-time window spikes the reactor to **887–5325 kWe** (worse than the electric spiral), so the low average power *requires* long H₂ storage. Cryocooling/boiloff management of 77 t of H₂ for 1–3 years is a first-order new subsystem risk. The ~34.5 t of cryo tankage is jettisonable post-departure (it burdens the departure burn but not the inbound cruise; a second-order effect that raises the 690 t propellant modestly — still far under the electric 1531 t).

**Bottom line for the deck:** the departure-power problem has a real mitigation — a reactor-charged H₂/O₂ stage — that turns a ~1250 kWe peak-power wall into a ~150–440 kWe average-power problem plus a cryo-H₂ storage problem, while *improving* delivery efficiency. It is the strongest "outside the box" lever found, and it reframes bet #3's departure leg from *impossible megawatt reactor* to *demanding-but-more-tractable few-hundred-kWe reactor + cryogenic energy storage*. It does not make the reactor flyable-Kilopower.

## Revisit

Held cleanly and as predicted (pessimistic pre-registration per lesson 1: I predicted a partial win with real costs, and the costs materialized — 37 t added mass, forced cryo-H₂, not-Kilopower). The one genuinely surprising sub-result is that the lower-Isp chemical option uses *less* propellant and delivers *more* payload than the higher-Isp electric — a direct consequence of Oberth (lesson 23: a Δv is only valid paired with a thrust regime; here the thrust regime *chooses* the Δv, and the impulsive 8.5 dominates the continuous 21.9 despite half the Isp). Honest limitations: (a) electrolysis specific energy (20 MJ/kg, ~70 % efficient) and H₂/O₂ Isp (420 s) are literature mid-values, not vendor-anchored — the reactor power scales linearly with the former and the propellant with the latter (both swept); (b) the cryo-H₂ boiloff is treated as a first-order risk + the just-in-time power-spike bound, not a full thermal/cryocooler model; (c) the jettisonable tank mass raises the departure propellant ~1.3× (still < electric); (d) the dwell duration couples to the (unmodeled) harvest rate — a slower harvest lowers the electrolysis power for free but lengthens the mission.

**Deferred (retest spec):** vendor-anchor the electrolysis efficiency and H₂/O₂ Isp (heritage tier T1/T2 per PROTOCOL Deviation 8); a cryo-H₂ boiloff/cryocooler thermal model over the dwell at Saturn's ~90 K; the harvest-rate ↔ dwell ↔ electrolysis-power coupling; and a staging analysis of the jettisonable tank mass. Also worth: a **reactor-charged battery + high-thrust electric burst** comparison (likely loses to electrolysis on energy-storage density, but bounds the design space).

## Cross-learning

- **Forward to axis 05 (reactor-power-floor) + axis 03 (inbound-propulsion):** this round provides the *mitigation* the axis-05 project-owner USER-NOTE asked for. Integration records the reactor-charged H₂/O₂ departure stage as the **leading departure-architecture candidate**: it softens the departure reactor from ~1248 kWe (electric spiral, robust per Round C/E) to ~150–440 kWe (electrolysis over the dwell) and doubles departure delivery efficiency, at the cost of a cryo-H₂ storage subsystem and ~37 t added (mostly jettisonable) mass — but does not reach Kilopower class. This is a genuine softening of bet #3's departure leg, the first this session, and it changes the departure framing from "impossible" to "demanding + cryogenic energy storage."
- **Backward to R-lowthrust-spiral-departure / R-eccentric-harvest-departure:** those closed the *electric* departure at megawatt; this opens the *decoupled high-thrust* departure at few-hundred-kWe. Together they define the departure-power design space: electric = 1248 kWe (megawatt, no cryo); H₂/O₂ = 150–440 kWe (few-hundred, cryo-H₂); chemical-from-Earth = 175 kWe but defeats the free-water premise. The H₂/O₂ route dominates the electric on both power and propellant.
- **Reframes an ICEBERG fundamental:** either way, the departure propellant (690–1531 t) dwarfs the delivered payload (~100 t) — Saturn's deep well makes chunk-return-to-Earth intrinsically propellant-hungry (single-digit-to-teens % departure-leg efficiency). The H₂/O₂ stage is the best available answer but does not change that the well is the dominant cost. Consistent with the three-bets reading (locked finding 5): the departure/power leg is bet #3, and this round finds a real lever on it without removing the bet.
