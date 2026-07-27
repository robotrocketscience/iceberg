# R-delivery-point-harvest-ratio — the depot prize is "don't climb out of Saturn's well," not "deliver closer to Earth"

**Status:** run + STUDY complete 2026-07-22. **2/3 HELD** (H-I3 falsified on its ≤3:1 threshold; conclusion holds strongly). Result JSON `results/delivery_point.json`; figure `results/delivery_point.png`.
**Predecessor:** `R-roundtrip-closure-departure-stage` (`c01a90e`) — chunk-return-to-LEO is ~73:1 harvest ratio; framed as a "two-end deep-well Δv." This round maps the harvest ratio across delivery points to locate the depot prize and decompose the penalty.

## Hypothesis (pre-registered; see SCOPE.md)

Predicted the harvest ratio drops steeply toward the source, that Earth-vicinity delivery stays > 25:1 (the Saturn-departure leg being the other half of the penalty), and that a Saturn-orbit depot collapses the ratio to ~1:1 — so the pivot's win is "don't return to Earth's vicinity," not "deliver to a higher Earth orbit."

## Test

Deterministic. The Round H mass cascade (reactor mass = P/sp; H₂/O₂ Isp 420; departure/transport propellant accelerating D + dry + reactor + tanks; Earth-capture propellant on the released chunk) applied across four delivery points with their Δv from the B-ring harvest orbit: Saturn ring/orbit depot (2.0 km/s raise), heliocentric-at-Saturn (8.5 departure), Earth cislunar/high-ellipse (8.5 + 4.07 capture), LEO (8.5 + 7.29 capture), at flown (2.4) and aspirational (40) W/kg.

## Result (D = 30 t)

| delivery point | harvest ratio 2.4 W/kg | 40 W/kg | capture share of penalty |
|---|---|---|---|
| **Saturn ring/orbit depot** | **4.2:1** | **1.2:1** | 0 % |
| heliocentric-at-Saturn | 67.6:1 | 19.7:1 | 0 % |
| Earth cislunar / high-ellipse | 69.4:1 | 21.5:1 | 3 % |
| LEO | 72.8:1 | 24.9:1 | 7 % |

| Sub-claim | Pre-registered | Measured | Verdict |
|---|---|---|---|
| H-I1 monotonic drop; Saturn-depot < 5:1 | monotone; < 5 | monotone; 4.2:1 | ✅ HELD |
| H-I2 Earth-vicinity > 25:1; LEO→cislunar only ~halves | > 25; ~2× | > 25; **only 1.05×** | ✅ HELD (stronger) |
| H-I3 Saturn-depot ≤ 3:1 at any specific power | ≤ 3:1 | **4.2:1 at flown** (1.2 at aspirational) | ❌ threshold falsified; conclusion holds |

## Reading

**The harvest penalty of chunk-return is almost entirely the Saturn-*departure* leg — climbing the vehicle-plus-reactor out of Saturn's deep gravity well — not the Earth-capture leg. So the delivery point in Earth's vicinity barely matters (LEO → cislunar buys 1.05×), and even a heliocentric depot at Saturn's distance is still 67.6:1. The only architecture that escapes the penalty is a Saturn-*orbit* depot that never climbs out of the well (4.2:1 at flown, 1.2:1 at aspirational). The depot prize is precisely located: "don't leave Saturn orbit," not "deliver closer to Earth."**

1. **The departure leg is ~90 % of the penalty (H-I2, stronger than predicted).** Earth capture is only 7 % of the LEO harvest ratio (73 → 67.6 when you drop it entirely). The reason is mass asymmetry: the departure burn must accelerate the *whole vehicle including the 146 t reactor* out of Saturn's well through 8.5 km/s (propellant ~6.9× the ~180 t burnout mass = ~1240 t), while Earth capture only decelerates the released 30 t chunk through 7.3 km/s (~156 t). The reactor mass rides the departure burn, so the departure dominates. **Moving the delivery point anywhere in Earth's vicinity (LEO → cislunar → high ellipse) changes the harvest ratio by ≤ 5 %.** This refines Round H's "two-end Δv" framing: the departure end is the overwhelming driver; the Earth end is a rounding error.

2. **Even "don't return to Earth" is not enough — you must not leave Saturn orbit (H-I1, H-I3).** A heliocentric-at-Saturn depot (Saturn escape, no Earth transit) is still 67.6:1, because you still pay the 8.5 km/s to escape Saturn's well. Only the Saturn ring/orbit depot — where the harvested ice never climbs out of the well — collapses the ratio to 4.2:1 (flown) or 1.2:1 (aspirational). And that 4.2:1 is *conservative*: it charges the reactor mass to the 2 km/s depot-raise, but a Saturn-orbit depot **reuses the harvest reactor in situ** across many chunks rather than sending it with each chunk, so the amortized depot ratio approaches ~1:1 (harvest and stockpile in place). My pre-registered ≤ 3:1 threshold was falsified only because I charged the full reactor mass to the depot-raise at flown specific power; the physical conclusion (Saturn-orbit depot is ~15–60× better than any Earth-vicinity delivery) is unambiguous.

3. **The strategic verdict for the pivot.** ICEBERG's deep-well penalty is fundamentally a *Saturn-escape* cost, not an Earth-return cost. Chunk-return to *anywhere* in Earth's vicinity is ~67–73:1 harvest ratio at flown reactor tech (and even at aspirational specific power, ~20–25:1). The source-concentration advantage (99.7 % pure ice) does nothing to touch this — the penalty is Δv to escape Saturn, not ore grade. **The only physics escape is a Saturn-orbit water depot**, which collapses the ratio to ~1:1. That reframes the axis-02 open question sharply: the pivot's viability is *entirely* a demand question — **is there a customer for water in Saturn orbit?** (in-situ propellant for other Saturn/outer-planet missions, aggregation for later bulk transport, etc.). If yes, ICEBERG is a Saturn-local utility with ~1:1 efficiency; if no, chunk-return-to-Earth is a ~70:1 proposition regardless of delivery point. The physics has done its job; the load-bearing unknown is now demand, not Δv.

## Revisit

H-I1/H-I2 held (H-I2 more strongly than predicted — the departure leg is ~90 %, not ~50 %, of the penalty, because it carries the reactor mass); H-I3's ≤ 3:1 threshold was falsified (4.2:1 at flown specific power) — the fifth pre-registered-threshold miss of the session, again from an optimistic absolute-number guess while the comparative/directional prediction held. The pattern is now unmistakable and worth a methodology note: my *directional* pre-registrations (X beats Y, Z dominates) hold reliably, but my *absolute-threshold* pre-registrations keep landing optimistic by a modest factor — I should pre-register absolute thresholds with wider bands or as inequalities anchored on a computed bracket rather than a round number. Honest limitations: (a) the Saturn-orbit-depot 4.2:1 charges the reactor to the depot-raise; the in-situ-reuse case (~1:1) is the more realistic depot number but was not the pre-registered configuration; (b) delivery-point Δv values are impulsive vis-viva (the H₂/O₂ stage is high-thrust, so impulsive is correct here); (c) the Saturn-orbit depot's *station-keeping*, radiation, and ring-environment survival over a stockpiling campaign are unmodeled; (d) demand at each delivery point is explicitly out of scope.

**Deferred (retest spec):** the in-situ-reactor-reuse Saturn-depot cascade (~1:1, the realistic depot number); and — the now-load-bearing follow-on — a **demand-side round for a Saturn-orbit water depot** (R-saturn-system-water-depot-demand: who needs propellant/water in the Saturn system or outer solar system on ICEBERG's timeline, and at what price), which is a market/mission-model question, not physics, and is the honest gate on the entire pivot.

## Cross-learning

- **Forward to axis 02 (surviving cell) + axis 21 (architecture-source-comparator):** the depot pivot's physics is now sharply located — the prize is a **Saturn-orbit depot** (~1–4:1 harvest ratio), not any Earth-vicinity delivery (~67–73:1 flown, ~20–25:1 aspirational, essentially independent of the Earth orbit chosen). The Saturn-escape Δv, not the Earth return or ore grade, is the dominant cost. Integration records this and flips the axis-02 pivot question from "where to deliver" (answered: Saturn orbit) to "is there Saturn-orbit demand" (the load-bearing unknown, a SCOPE for R-saturn-system-water-depot-demand).
- **Backward to R-roundtrip-closure-departure-stage (Round H):** its "two-end deep-well Δv" is refined — the *departure* end is ~90 % of the penalty (it carries the reactor mass), so Round H's Earth-capture term (7.3 km/s) is a minor contributor and the harvest ratio is nearly independent of the Earth delivery orbit.
- **Reinforces locked finding 5 and the source-concentration reading (axis 04 latest+15):** the campaign's "argue on source concentration, not per-tonne Δv" framing is correct *for the extraction* comparison but does not rescue *the transport* — the Saturn-escape Δv makes Earth-vicinity delivery ~70:1 regardless of ore grade. Source concentration wins the mining argument; the deep well loses the transport argument; only a Saturn-local market reconciles them.
