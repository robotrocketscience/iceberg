# R-roundtrip-closure-departure-stage — the H₂/O₂ stage helps 7×, but chunk-return-to-Earth is intrinsically ~20–25:1 harvest-hungry

**Status:** run + STUDY complete 2026-07-22. **3/4 HELD** (H-H1 falsified on its absolute-threshold clause, in the pessimistic direction; its qualitative-improvement clause held strongly). Result JSON `results/roundtrip.json`; figure `results/roundtrip.png`.
**Predecessors:** `R-electrolysis-departure-stage` (`49f4bb1`) + `R-cryo-hydrogen-storage-saturn` (`3b7dd67`) characterized the H₂/O₂ departure stage in isolation. This round tests it at the round-trip mass-cascade level.

## Hypothesis (pre-registered; see SCOPE.md)

That the isolated-analysis H₂/O₂ win carries over to the round trip once the stage mass, the reactor mass, and the propellant are all carried and accelerated. Predicted: H₂/O₂ much better harvest ratio (wins on departure propellant *and* reactor mass 350 vs 1248 kWe), but the reactor specific-power (mass) wall still binds — viable only at aspirational specific power.

## Test

Deterministic backward mass cascade for delivered chunk D ∈ {20,30,50} t × reactor specific power {2.4, 10, 40} W/kg × architecture {H₂/O₂, all-electric}. Reactor mass = P/sp; departure propellant (fixed-point with propellant tanks) to accelerate (D + vehicle dry + reactor + tanks) through Δv_dep (8.5 km/s H₂/O₂ impulsive vs 21.9 km/s electric spiral, Isp 420 vs 800); Earth-capture propellant = H₂/O₂ impulsive 7.3 km/s on the released chunk (aerocapture closed, axis 11); harvest = departure + Earth-capture propellant; metric = harvest ratio (harvest/D) and delivery efficiency.

## Result (D = 30 t)

| specific power | H₂/O₂ reactor | H₂/O₂ harvest | delivery | electric reactor | electric harvest |
|---|---|---|---|---|---|
| 2.4 W/kg (flown KRUSTY) | 146 t | **72.8:1** | 1.4 % | 520 t | 538:1 |
| 10 W/kg | 35 t | 34.1:1 | 2.9 % | 125 t | 165:1 |
| 40 W/kg (aspirational) | 9 t | **24.9:1** | 4.0 % | 31 t | 77:1 |

| Sub-claim | Pre-registered | Measured | Verdict |
|---|---|---|---|
| H-H1 H₂/O₂ ≤ 50:1 & electric > 150:1, ≥3× | 50 / 150 / 3× | **72.8:1 / 538:1 / 7.4×** | ⚠️ threshold falsified (72.8 > 50); improvement held (7.4×) |
| H-H2 reactor mass dominant (≥100/≥400 t) | ≥100 / ≥400 t | **146 / 520 t** vs 30 t chunk | ✅ HELD |
| H-H3 H₂/O₂ closes poor-but-positive; electric non-closing | 20–80:1 / >150:1 | **72.8:1 (1.4%) / 538:1** | ✅ HELD |
| H-H4 not viable (<10:1) at flown; mass wall binds | ≥10:1 at 2.4 | **72.8:1 at 2.4; 24.9:1 even at 40** | ✅ HELD (stronger — never viable) |

## Reading

**The H₂/O₂ departure stage is worth adopting — it is a 7.4× system-level improvement, the difference between an effectively non-closing all-electric round-trip (538:1) and a positive-but-inefficient one (73:1). But the round trip is *intrinsically* propellant-hungry: even with a near-massless aspirational reactor, chunk-return-to-Earth harvests ~25 tonnes of water per tonne delivered, because it pays large Δv at *both* ends of a deep-well round-trip. Two distinct walls, and the departure lever only moves one.**

1. **The isolated win carries over — and is large (H-H1 improvement, H-H3).** All-electric is effectively non-closing (538:1 harvest ratio at flown specific power — you would harvest 538 t of water to deliver 1 t), because it pays the 21.9 km/s electric-spiral departure *and* carries a 520 t megawatt reactor that must itself be accelerated through that spiral. H₂/O₂ cuts both: the 8.5 km/s impulsive departure and the 146 t reactor give 73:1. The 7.4× improvement is the honest system-level value of the departure lever.

2. **But it does not reach viability — the intrinsic two-end Δv floor is ~20–25:1 (H-H4, stronger than predicted).** Even at aspirational 40 W/kg specific power (reactor shrinks to 9 t), the harvest ratio is 24.9:1 (4 % delivery efficiency) — because the Δv is paid twice: 8.5 km/s to climb out of Saturn's well at departure *and* 7.3 km/s to capture the chunk at Earth (aerocapture being closed), each through a rocket equation at Isp 420. The minimum harvest ratio anywhere on the grid is 21:1. **Chunk-return-to-Earth is a ~20–25:1 harvest-ratio proposition in the best conceivable case, and 73:1 at flown reactor tech.** My pre-registered H-H1 threshold (H₂/O₂ ≤ 50:1) was too optimistic; the true floor is higher, because I under-counted the Earth-capture leg and the reactor mass in the single-leg bracket.

3. **Two distinct walls, and the departure lever moves only one (H-H2).** Bet #3 has a *power* half (peak kWe — the departure lever softens this, megawatt → few-hundred-kWe) and a *specific-power / mass* half (reactor mass — the departure lever does **not** touch this). At flown KRUSTY specific power (2.4 W/kg) the reactor is 146 t of dead mass that quadruples the harvest ratio (25:1 → 73:1). This is exactly titan-4's mass-floor kill (latest+18) reappearing at the round-trip level, and it is orthogonal to the departure-power softening.

4. **The strong strategic implication: the deep-well Earth-return Δv is the dominant cost, so architectures that avoid it win by construction.** A Saturn-system water depot (deliver water *at* Saturn — axis 02 waiver) or process-at-Saturn (return higher-value lower-mass products) pays neither the 8.5 km/s departure nor the 7.3 km/s Earth capture on the bulk water. This round quantifies the prize: avoiding the Earth-return round-trip removes a ~20–73× harvest-ratio multiplier. The departure lever makes chunk-return-to-Earth *closeable*; the depot pivot makes it *unnecessary*.

## Revisit

H-H2/H3/H4 held; H-H1's improvement clause held (7.4×) but its absolute-threshold clause was falsified (72.8:1 > my ≤50:1) — the fourth pre-registered-threshold miss of the session, again in the pessimistic direction, from under-counting a leg (Earth capture) and the reactor mass in the pre-script bracket. Consistent with methodology lesson 1 inverted: my optimism keeps landing on the *absolute* numbers while the *directional/comparative* predictions hold. The load-bearing conclusion (departure lever helps 7×; round-trip intrinsically ~20–73:1; specific-power wall binds) is robust to the threshold miss. Honest limitations: (a) Earth capture is modeled as a 7.3 km/s impulsive burn to LEO — delivering to a **high Earth orbit / cislunar** instead (~4 km/s to barely capture) would materially lower the ratio and is a real un-modeled lever (deferred); (b) the inbound leg is a Hohmann coast (no cruise propellant) — a faster inbound would add propellant; (c) the reactor is carried to Earth in the cascade rather than reused/disposed at Saturn — reuse would amortize its mass over multiple missions (a fleet effect, not modeled); (d) outbound + Saturn capture are Earth-launched (not in the harvest ratio); (e) specific power 2.4 W/kg is the KRUSTY measured value (power finding 1) and 40 W/kg is TRL-2 aspirational — the true flyable value is the open bet-#3 question.

**Deferred (retest spec):** the high-Earth-orbit / cislunar delivery target (~4 km/s capture) as a harvest-ratio lever; reactor reuse across a mission fleet (amortize the dead mass); a direct comparison against a Saturn-system-depot architecture (which pays neither deep-well Δv) to quantify the pivot's advantage; and folding this cascade into the `mission_graph` framework for cross-check against its full-round-trip closure.

## Cross-learning

- **Forward to axis 02 (surviving cell) + axis 05 (reactor-power-floor) + axis 10 (round-trip ceiling):** the H₂/O₂ departure stage is a genuine, adoptable system-level improvement (7.4×) that makes the electric-only non-closing round-trip closeable, but chunk-return-to-Earth remains intrinsically ~20–25:1 harvest-ratio (4 % delivery) even at aspirational reactor tech, and ~73:1 at flown tech — the reactor specific-power (mass) wall (bet #3's mass half, titan-4's kill) is untouched by the departure lever. Integration records this as: the departure thread (Rounds C→H) softens bet #3's *power* half and improves round-trip closure several-fold, but does not remove bet #3's *mass* half, and it *strengthens the quantitative case for the Saturn-depot / process-at-Saturn pivot* (axis 02 open question) by pricing the Earth-return Δv at a 20–73× harvest-ratio multiplier.
- **Backward across the departure thread (C, E, F, G, H):** C/E established the electric departure is robustly megawatt; F/G found the H₂/O₂ mitigation (few-hundred-kWe, survivable cryo); H shows the mitigation helps the round-trip 7× but the round-trip is still gated by reactor mass and the intrinsic two-end Δv. The thread's net: a real lever on bet #3's power half, a real system-level improvement, and a sharpened case that the *mass* half and the *deep-well Δv* are the residual binding constraints — pointing at the depot pivot.
- **Reinforces locked finding 5 (three engineering bets):** this round is a clean quantitative illustration that bet #3 is two walls (power + mass), that the departure architecture only addresses power, and that the Earth-return Δv is a first-order cost that the depot pivot avoids by construction.
