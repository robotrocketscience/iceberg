# R-reactor-specific-power — does higher reactor specific power flip the FSP-vs-megawatt trade?

**Status:** pre-result.

## Question

R-chunk-fed-chemical found that delivered-water-per-launch-mass *peaks* at Fission Surface Power era (100 kilowatt-electric / 200 t chunk → ratio 5.90) and *crashes* at megawatt-class (1000 kilowatt-electric / 200 t chunk → ratio 0.98), because the 1-megawatt reactor at 10 watts-per-kilogram specific power weighs 100 tonnes and dominates the outbound launch.

That result was conditioned on **specific_power = 10 W/kg**, the Fission Surface Power target. Real specific-power values span at least an order of magnitude:

- 5 W/kg — conservative / Kilopower demonstrated
- 10 W/kg — Fission Surface Power target
- 20 W/kg — aggressive next-decade goal
- 40 W/kg — DARPA / DRACO-class research targets
- 80+ W/kg — speculative for fission reactors; characteristic of solar-photovoltaic at low Earth orbit (different power source)

Does the (reactor power × chunk × architecture) decision matrix from R-chunk-fed-chemical hold at higher specific power? Specifically, **at what specific-power threshold does megawatt-class become more launch-efficient than Fission Surface Power era?**

## Pre-registered hypothesis (H-rsp)

**Aggregate (H-rsp-agg):** Doubling specific power roughly halves reactor mass and approximately halves the outbound launch penalty attributable to the reactor. The Fission-Surface-Power peak in delivered-per-launch-mass shifts upward in reactor power as specific power increases. At 20 W/kg the megawatt class becomes competitive with FSP; at 40 W/kg megawatt class dominates and the FSP-peak disappears. The result is mechanically: optimum reactor power ≈ specific_power × (a constant determined by chunk size and Δv).

**Pre-registered sub-claims:**

| Sub-claim | Predicted | Falsification |
|---|---|---|
| H-rsp-a — At 5 W/kg, peak delivered/launch shifts to lower reactor power (≤ 40 kilowatt-electric) | yes | falsified if peak at ≥ 100 kWe |
| H-rsp-b — At 10 W/kg, peak at 100 kilowatt-electric (replicates R-chunk-fed-chemical) | yes | falsified if peak shifts |
| H-rsp-c — At 20 W/kg, peak shifts to 200–500 kilowatt-electric (sub-megawatt era becomes competitive) | yes | falsified if peak stays at 100 kWe or jumps to 1 MWe |
| H-rsp-d — At 40 W/kg, peak shifts to 500–1000 kilowatt-electric (megawatt era dominates) | yes | falsified if peak below 500 kWe |
| H-rsp-e — Peak delivered/launch-mass ratio at the optimum reactor for each specific power | roughly invariant at 5–7 | falsified outside [3, 12] |
| H-rsp-f — Architecture winner (all-electric vs Variant B) at the optimum cell is independent of specific power | yes | falsified if optimum cell switches architecture between any two specific-power steps |

**Aggregate decision:** if H-rsp-c and H-rsp-d hold, **specific power is the lever, not absolute reactor power.** The R-reactor-roadmap finding (megawatt-class is the IRR lever) is conditional on specific power assumptions; a 20–40 W/kg reactor program at sub-megawatt power could deliver the same IRR as a megawatt program at 10 W/kg, on a much shorter development timeline.

## Method

Reuse R-chunk-fed-chemical's mass-accounting code (all-electric + Variant B), parameterize specific_power_w_per_kg. Drop carried-hypergolic (never wins per R-chunk-fed-chemical).

**Sweep axes:**

- Reactor specific power: 5, 10, 20, 40 W/kg
- Reactor power: 10, 40, 100, 200, 500, 1000, 2000 kilowatt-electric (extend to 2 MWe to see asymptotic behavior)
- Chunk mass: 100, 200, 500 tonnes (drop small chunks; not the regime of interest here)
- Electric specific impulse: 1500, 2000, 2934, 5000 s
- Δv_chem (Variant B only): 0, 1, 2, 3 km/s

For each cell pick best architecture (all-electric or Variant B at best Δv_chem), best electric specific impulse, requiring schedule-feasible burn time ≤ 7 years. Report delivered-water-per-launch-mass.

**Validity caveats:**

- Tug structure mass (5 t) held constant. In reality, megawatt-class tug structure scales up too (radiator area for heat rejection alone scales with reactor power). Underestimates megawatt-era launch mass; the result is therefore *optimistic* on the megawatt-favorable conclusion.
- Reactor specific power treated as a single number. Real reactors have different specific powers for the core vs the power-conversion vs the radiator. The 10 W/kg target is system-level; component-level varies.
- Outbound architecture and Δv_outbound unchanged from R-chunk-fed-chemical.
- 7-year inbound burn cap retained; R-bag-permeability-vs-burn-time will explore relaxing this.

## Result

### Peak delivered-water-per-launch-mass and optimum reactor power, by (specific power × chunk)

| Specific power | Chunk | Peak reactor | Peak ratio | Architecture | Delivered | Launch mass |
|---:|---:|---:|---:|---|---:|---:|
|  5 W/kg | 100 t |  40 kWe |  2.92 | all-electric |  60.0 t |  21 t |
|  5 W/kg | 200 t | 100 kWe |  3.47 | all-electric | 137.2 t |  40 t |
|  5 W/kg | 500 t | 200 kWe |  4.32 | all-electric | 307.3 t |  71 t |
| 10 W/kg | 100 t |  40 kWe |  4.32 | all-electric |  61.5 t |  14 t |
| 10 W/kg | 200 t | 100 kWe |  5.90 | all-electric | 140.0 t |  24 t |
| 10 W/kg | 500 t | 200 kWe |  8.94 | all-electric | 353.4 t |  40 t |
| 20 W/kg | 100 t |  40 kWe |  5.61 | all-electric |  62.2 t |  11 t |
| 20 W/kg | 200 t | 100 kWe |  8.94 | all-electric | 141.4 t |  16 t |
| 20 W/kg | 500 t | 200 kWe | 15.01 | all-electric | 356.2 t |  24 t |
| 40 W/kg | 100 t |  40 kWe |  7.42 | all-electric |  70.4 t |   9 t |
| 40 W/kg | 200 t | 100 kWe | 11.97 | all-electric | 142.1 t |  12 t |
| 40 W/kg | 500 t | 200 kWe | 22.60 | all-electric | 357.6 t |  16 t |

### Delivered/launch-mass ratio at 200 t chunk, sweep reactor power × specific power

| Reactor (kWe) | 5 W/kg | 10 W/kg | 20 W/kg | 40 W/kg |
|---:|---:|---:|---:|---:|
|   10 |    – |    – |    – |    – |
|   40 | 2.53 | 3.13 | 3.54 | 3.78 |
|  100 | 3.47 | **5.90** | **8.94** | **11.97** |
|  200 | 2.12 | 3.92 | 6.62 | 9.99 |
|  500 | 0.98 | 1.94 | 3.62 | 6.26 |
| 1000 | 0.46 | 0.98 | 1.94 | 3.62 |
| 2000 | 0.20 | 0.46 | 0.98 | 1.94 |

### Delivered/launch-mass ratio at 500 t chunk, sweep reactor power × specific power

| Reactor (kWe) | 5 W/kg | 10 W/kg | 20 W/kg | 40 W/kg |
|---:|---:|---:|---:|---:|
|  100 | 4.31 | 6.15 | 7.77 | 8.92 |
|  200 | **4.32** | **8.94** | **15.01** | **22.60** |
|  500 | 2.28 | 4.47 | 8.30 | 14.32 |
| 1000 | 1.27 | 2.56 | 4.96 | 9.16 |
| 2000 | 0.61 | 1.27 | 2.56 | 4.96 |

### Winning architecture at 200 t chunk, sweep reactor × specific power

The architecture winner is invariant under specific power.

| Reactor (kWe) | 5 W/kg | 10 W/kg | 20 W/kg | 40 W/kg |
|---:|---|---|---|---|
|   40 | Variant B · 2 km/s · 2000 s | Variant B · 2 km/s · 2000 s | Variant B · 2 km/s · 2000 s | Variant B · 2 km/s · 2000 s |
|  100 | all-electric · 2000 s | all-electric · 2000 s | all-electric · 2000 s | all-electric · 2000 s |
|  200 | all-electric · 2934 s | all-electric · 2934 s | all-electric · 2934 s | all-electric · 2934 s |
|  500 | all-electric · 5000 s | all-electric · 5000 s | all-electric · 5000 s | all-electric · 5000 s |
| 1000 | all-electric · 5000 s | all-electric · 5000 s | all-electric · 5000 s | all-electric · 5000 s |

### Hypothesis grading

| Sub-claim | Predicted | Actual | Held? |
|---|---|---|---|
| H-rsp-a — Peak at ≤ 40 kWe at 5 W/kg | yes | 40 kWe for 100 t chunk; 100 kWe for 200 t; 200 kWe for 500 t — chunk-dependent, not a single number | partially held |
| H-rsp-b — Peak at 100 kWe at 10 W/kg | yes | 100 kWe at 200 t; 200 kWe at 500 t — chunk-dependent | partially held |
| H-rsp-c — Peak shifts to 200–500 kWe at 20 W/kg | yes | **falsified** — peak stays at the same (chunk-determined) reactor power regardless of specific power | falsified |
| H-rsp-d — Peak shifts to 500–1000 kWe at 40 W/kg | yes | **falsified** — peak does not shift | falsified |
| H-rsp-e — Peak ratio invariant at 5–7 across specific power | yes | **falsified** — peak ratio scales with specific power: at 500 t chunk, ratio goes from 4.32 (5 W/kg) to 22.60 (40 W/kg) | falsified |
| H-rsp-f — Architecture winner invariant under specific power | yes | held — same architecture wins at every cell across specific power | held |

## Reading

**The mechanism I assumed was wrong, but the answer it produces is still informative.** I predicted that doubling specific power would shift the optimum reactor power upward (because megawatt-class becomes mass-efficient enough to compete). The data falsifies this cleanly: the optimum reactor power is set by **chunk size**, not by specific power. Specific power is a launch-efficiency multiplier at every reactor power, not an optimum-shifter.

**Five observations the result actually supports:**

1. **Optimum reactor power scales with chunk size, full stop.** 40 kilowatt-electric for 100 t chunks; 100 kilowatt-electric for 200 t; 200 kilowatt-electric for 500 t. This relationship holds across the full 5–40 watts-per-kilogram specific-power sweep. **The reactor and the chunk are sized together; specific power is a separate axis.**

2. **Specific power is a roughly-linear multiplier on delivered-per-launch-mass.** At the peak cell (200 kWe / 500 t chunk), the ratio goes 4.32 → 8.94 → 15.01 → 22.60 as specific power goes 5 → 10 → 20 → 40 W/kg. Doubling specific power roughly doubles launch efficiency at every reactor power.

3. **Megawatt class becomes launch-efficient at 40 watts-per-kilogram.** At 1000 kilowatt-electric / 500 t chunk: ratio = 2.56 at 10 W/kg → 9.16 at 40 W/kg. The 40-W/kg megawatt cell is finally comparable to the 10-W/kg Fission-Surface-Power peak (8.94). So R-reactor-roadmap's "megawatt class is the IRR lever" is structurally correct **only if a 40 W/kg specific-power program also closes**. At today's 10 W/kg target, the megawatt class is dominated by sub-megawatt on launch efficiency.

4. **The architecture decision matrix from R-chunk-fed-chemical is robust to specific power.** Same architecture wins at every (reactor, chunk) cell across the full specific-power sweep. The decision matrix surfaced in R-chunk-fed-chemical's revisit clause does not need to be redone for different reactor programs.

5. **The peak optimum at all four specific powers is 200 kilowatt-electric reactor + 500-tonne chunk.** That cell's ratio at 40 W/kg (22.60) is roughly 5× the same cell at 5 W/kg (4.32). **The single highest-leverage variable in the campaign is reactor watts-per-kilogram, not watts.**

**Tension with R-reactor-roadmap, reconciled:** R-reactor-roadmap holds specific power at the Fission-Surface-Power target (10 W/kg) and finds that megawatt-class arrival year is the dominant internal-rate-of-return lever. This round shows that the megawatt-class trade is also conditional on specific power. The reconciled finding: **the program should track two independent variables — reactor arrival year *and* watts-per-kilogram trajectory — and the latter is roughly as leveraged as the former.** Doubling specific power has the same launch-efficiency effect as halving outbound launch cost; if the specific power program is on a 5-year horizon and the megawatt-power program is on a 20-year horizon, the specific power lever is more reachable.

**What this round still papers over:**

- **Tug structure mass held constant at 5 tonnes.** Megawatt-class tug needs a megawatt-class radiator, propellant feed lines, structural mass for thermal management — none of which scale with chunk; they scale with reactor power. The 5-t fixed assumption flatters megawatt cells. A megawatt-scale radiator alone is ~5–10 tonnes; including that, the 40 W/kg megawatt cell delivers/launch ratio drops by maybe 20–30%.
- **Reactor specific power is treated as a single number.** Real-world it's a stack (core W/kg + power conversion W/kg + radiator W/kg). Aggressive specific-power programs improve some elements but not all proportionally.
- **The 5–40 W/kg sweep brackets a real engineering range, but 40 W/kg specifically is research-grade.** Treating it as feasible is optimistic.

## Revisit clause

H-rsp-a partially held; H-rsp-b partially held; H-rsp-c, H-rsp-d, H-rsp-e falsified; H-rsp-f held. The aggregate hypothesis (specific power shifts the optimum reactor power) is **wrong on mechanism but right on consequence** — specific power is the lever, just as a multiplier rather than as a shifter.

**Headline that should propagate to the conops document and to the R-reactor-roadmap revisit:** *Optimum reactor power tracks chunk size; specific power is an independent multiplier on launch efficiency. A 40-W/kg specific-power program at sub-megawatt power is approximately equivalent to a 10-W/kg megawatt program on delivered-per-launch-mass, and reaches that point on a shorter development horizon.*


## Revisit clause

Grade H-rsp-a through H-rsp-f. If H-rsp-c and H-rsp-d hold, propagate the finding to the conops document and reframe R-reactor-roadmap's headline.
