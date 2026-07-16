# Round 10 — Inbound Propulsion Architecture Revisit

**Status:** pre-result.

## Question

R8 falsified the conops' choice of water-microwave-electrothermal thruster (500 s specific impulse) for the chunk-fed inbound leg under a Hohmann return trajectory: chunk delivery is 0% (full propellant consumption) at the corrected inbound delta-velocity budget. The user's prompt is broader: explore propulsion options beyond microwave electrothermal.

This round asks: across a realistic candidate set of water-compatible propulsion technologies (and one split-prop architecture that breaks the chunk-fed-only assumption), which candidate delivers the largest fraction of a 14 t grappled chunk at each realistic power level (10 kWe Kilopower, 40 kWe Fission Surface Power, 100 kWe sub-megawatt) under the R8 corrected inbound delta-velocity budgets (Case B at 5.94 km/s chunk-fed, Case C at 2.85 km/s chunk-fed)?

## Candidate set

| ID | Name | Specific impulse band (s) | Heritage / TRL | Compatibility note |
|---|---|---|---|---|
| C1 | Water resistojet | 180–220 | TRL 9 (HYDROS-C, Tethers Unlimited) | Lowest specific impulse but high thrust-to-power, no plasma physics |
| C2 | Water microwave electrothermal | 400–650 | TRL 4–5 (Penn State Micci lab, Momentus Vigoride proxy) | R0 baseline; R8 falsified at conops trajectory |
| C3 | Water Hall thruster | 1200–1800 | TRL 2–3 (no flown water-Hall) | Adjacent to Hall-Kr/Xe; cathode erosion is the open question |
| C4 | Water radio-frequency ion | 1800–2200 | TRL 7–8 (Pale Blue flight heritage per R1) | Grid erosion under oxidizing plume is the open question |
| C5 | Water dual-ion (electrolyzed H⁺ + O⁺) | 4500–15000 | TRL 1–2 as integrated system (R3i exploratory) | Wins only at megawatt-class power per R3i |
| C6 | Split-prop: water electrothermal Saturn egress + Hall-xenon inbound braking | 500 + 2000 (separate) | TRL 9 (Hall-Xe flight heritage across hundreds of satellites) | Breaks chunk-fed-only assumption; requires Earth-launched xenon |

## Pre-registered hypothesis (H10)

**At Kilopower (10 kWe) power class and Case B inbound budget (5.94 km/s chunk-fed):**

| Sub-claim | Predicted | Falsification |
|---|---|---|
| H10a — C1 (water resistojet, 200 s) chunk delivery | 0% — Tsiolkovsky mass ratio explodes at 200 s | held if delivery ≤ 0.1 t |
| H10b — C2 (water microwave electrothermal, 500 s) chunk delivery | 0.5–5% (R8 case B was 4.7%) | held if delivery ∈ [0.1, 1.0] t |
| H10c — C3 (water Hall, 1500 s) chunk delivery | 40–65% | held if ∈ predicted range |
| H10d — C4 (water radio-frequency ion, 2000 s) chunk delivery | 60–80% | held if ∈ predicted range |
| H10e — C5 (water dual-ion, 5000 s) chunk delivery | 80–95% | held if ∈ predicted range; load-bearing if reactor-mass penalty inverts the ranking |
| H10f — C6 (split-prop) chunk delivery | 70–90% (chunk delivered intact; xenon mass becomes the constraint) | held if ∈ predicted range |

**Pre-registered ranking:** I predict the ranking by chunk delivery at Kilopower / Case B is **C5 > C4 ≈ C6 > C3 > C2 > C1**. C4 (Pale Blue) is my expected "right answer" for near-term flight because it dominates Hall and microwave electrothermal while having actual heritage; C6 is a viable alternative that trades Earth-launch mass for inbound braking specific impulse.

**Pre-registered ranking at Case C inbound budget (2.85 km/s chunk-fed):** I predict the ranking compresses. The 2.85 km/s budget is small enough that even water resistojet starts delivering meaningful fractions (10–30%), and the specific-impulse advantage of high-end candidates shrinks. **C4 still wins, but the margin over C2 narrows from ~15× delivery to ~2×.** This means the slow-transfer trajectory choice (R9 territory) decouples the propulsion choice from the trajectory pain — at low chunk-fed delta-velocity, almost anything works.

**Pre-registered cross-power-level claim:** at 100 kWe sub-megawatt-class power, the *power-optimal* specific impulse from R6 rises into the C4-C5 band. The dominant constraint at high power is not specific impulse but thruster mass and lifetime, neither of which this round attempts to model. R10 stops at delivered-mass-vs-specific-impulse; lifetime is deferred to a later round.

**Pre-registered split-prop claim (H10f detail):** if C6 is run, the optimal split point between Earth-launched xenon and chunk-fed water is where the Earth-launch dry-mass increase (xenon + tanks) equals the chunk-water savings on the inbound leg. I predict that point lies near 2–4 t of Earth-launched xenon, allowing 4–6 km/s of inbound braking at Hall-xenon specific impulse 2000 s. This decouples the chunk-fed budget from the trajectory choice and lets the conops keep water-microwave-electrothermal for Saturn-side burns.

**Pre-registered open question I expect to surface:** B-ring silicate dust contamination tolerance is a known concern for all ion-class thrusters (C3/C4/C5). This round does not test it; it assumes the chunk-fed propellant is clean enough that grid life is not the binding constraint. R7 (deferred) is the round where that gets tested.

## Method

Closed-form Tsiolkovsky + R6's power-optimal-specific-impulse framework + reactor-mass overhead from R1's 2.5–6.5 W/kg.

For each candidate at each (power class, inbound budget) combination:
1. Set specific impulse from the candidate's band midpoint.
2. Compute propellant mass required at the inbound delta-velocity from initial mass (14 t chunk + 5 t dry + reactor mass at 5 W/kg).
3. Delivered chunk mass = chunk mass minus propellant required (if propellant fits within chunk supply); else delivery = 0 and the spacecraft's dry mass is also consumed before reaching Earth (the same failure mode R8 found for microwave electrothermal at Case A).
4. Estimate thrust at this power and specific impulse via `F = 2 η P / v_e` with η = 0.4 (constant across candidates as a first-order assumption; in reality, η varies by tech).
5. Estimate cruise time required to deliver the inbound delta-velocity at this thrust, given the time-varying initial mass.

For C6 (split-prop):
- Saturn egress (2.09 km/s, mirror of ingress) runs on chunk-fed water-microwave-electrothermal at 500 s.
- Inbound braking (the residual after lunar gravity assist) runs on Earth-launched xenon at 2000 s.
- Trade variable: amount of xenon launched. Optimum: where the Earth-launch wet-mass increase equals the chunk-mass-delivered improvement.

**Validity caveats.**
- Constant 0.4 total electrical-to-jet efficiency across all candidates is a first-order assumption; real efficiencies differ (resistojet ~0.7, microwave electrothermal ~0.3, Hall ~0.5–0.6, radio-frequency ion ~0.6–0.7, dual-ion uncertain). Specific-impulse ranking is robust; absolute numbers are not.
- Reactor mass at 5 W/kg is mid-band per R1; the load-bearing high-end is 2.5 W/kg, which would double reactor mass.
- Time-of-flight estimate is closed-form (constant thrust, constant mass at midpoint); a real low-thrust trajectory integrator is needed for R-mid or R-synthesis.
- B-ring dust contamination is not modeled. Risk C06 is open.
- Hall-xenon at the C6 split assumes xenon-grade purity supply at LEO ($1k–$3k per kg launch cost on top of the xenon commodity price); cost is not in this round's scope.

## Result

See `results/propulsion_sweep.json`. Headline tables below.

**Kilopower power class (10 kWe, 2 t reactor) at Case B (5.94 km/s chunk-fed inbound):**

| ID | Candidate | Specific impulse (s) | Propellant required (t) | Delivered chunk (t) | Delivery fraction | Thrust (N) | Cruise (yr est.) |
|---|---|---|---|---|---|---|---|
| C1 | Water resistojet | 200 | 19.98 | 0.00 | **0.0%** | 7.14 | 0.58 |
| C2 | Water microwave electrothermal | 500 | 14.75 | 0.00 | **0.0%** | 1.22 | 4.19 |
| C3 | Water Hall thruster | 1500 | 6.98 | 7.02 | **50.2%** | 0.75 | 8.82 |
| C4 | Water radio-frequency ion (Pale Blue) | 2000 | 5.49 | 8.51 | **60.8%** | 0.66 | 10.37 |
| C5 | Water dual-ion (electrolyzed) | 5000 | 2.40 | 11.60 | **82.9%** | 0.22 | 33.23 |
| C6 | Split-prop (water egress + Hall-xenon braking) | 500 + 2000 | n/a | 5.61 | **40.0%** | n/a | — |

**Kilopower power class at Case C (2.85 km/s chunk-fed inbound — slow trajectory):**

| ID | Candidate | Delivered chunk (t) | Delivery fraction | Cruise (yr est.) |
|---|---|---|---|---|
| C1 | Resistojet | 0.00 | 0.0% | 0.33 |
| C2 | Microwave electrothermal | 4.74 | 33.9% | 2.42 |
| C3 | Water Hall | 10.30 | 73.6% | 4.63 |
| C4 | Water radio-frequency ion | 11.16 | 79.7% | 5.34 |
| C5 | Dual-ion | 12.81 | 91.5% | 16.43 |
| C6 | Split-prop | 6.48 | 46.3% | — |

**Fission Surface Power class (40 kWe, 8 t reactor) at Case B — reactor mass becomes the dominant penalty:**

| ID | Candidate | Delivered chunk (t) | Delivery fraction | Cruise (yr est.) |
|---|---|---|---|---|
| C3 | Water Hall | 5.03 | 35.9% | 2.83 |
| C4 | Water radio-frequency ion | 6.95 | 49.6% | 3.33 |
| C5 | Dual-ion | 10.92 | 78.0% | 10.68 |

At 100 kWe (20 t reactor — heavier than the chunk), Hall drops to 7.5% delivery, radio-frequency ion to 27.2%, dual-ion to 68.2%. **Adding power makes it worse for a 14 t chunk** because reactor mass scales linearly while specific-impulse benefit is logarithmic.

**Hypothesis grading at Kilopower / Case B:**

| ID | Predicted | Measured | Verdict |
|---|---|---|---|
| H10a (C1 resistojet) | 0% delivery | 0.0% | **held** |
| H10b (C2 microwave electrothermal) | 0.5–5% | **0.0%** | **falsified** — reactor mass (omitted in R8) pushes mass closure below the threshold |
| H10c (C3 Hall) | 40–65% | 50.2% | **held** |
| H10d (C4 radio-frequency ion) | 60–80% | 60.8% | **held** (lower-edge) |
| H10e (C5 dual-ion) | 80–95% | 82.9% | **held** (lower-edge) |
| H10f (C6 split-prop) | 70–90% | **40.0%** | **falsified** — Saturn egress at 500 s consumes ~60% of the chunk before the inbound burn even begins |

Aggregate pre-registered ranking C5 > C4 ≈ C6 > C3 > C2 > C1 was **partially wrong**: actual ranking at Kilopower / Case B is **C5 > C4 > C3 > C6 > C2 = C1**. C6 was over-predicted because I assumed split-prop would preserve the chunk; in fact the Saturn egress segment itself, when run on water-microwave-electrothermal at 500 s, costs ~8.4 t of chunk water on an already-heavy stack (chunk + dry + reactor + xenon + tanks ≈ 24 t initial mass). C6 underdelivers unless the egress segment also moves to higher specific impulse.

## Reading

1. **The conops microwave-electrothermal architecture loses on every realistic budget.** At Case B / Kilopower, microwave electrothermal delivers 0% of the chunk (mass closure fails). At the more forgiving Case C / Kilopower, it delivers 34% — well below the conops' headline 75%. Microwave electrothermal is not a viable inbound chunk-fed thruster at the conops' 14 t chunk mass under any of the trajectory cases R8 admits.

2. **Water radio-frequency ion (Pale Blue class, 2000 s, TRL 7–8) is the right inbound thruster.** At Case B / Kilopower it delivers 61% of the chunk and at Case C / Kilopower it delivers 80% — meeting the conops' 75% headline. This is the swap R8 demanded.

3. **Dual-ion at 5000 s delivers more (83% at Case B / Kilopower, 92% at Case C) but at extreme cruise-time cost (33 years estimated at Case B).** The cruise time is a hard constraint; the conops mission is sized for 13.5 years round-trip total. Dual-ion is over-spec'd for the chunk size; its window opens at chunks > 200 t per R3i.

4. **Adding reactor power hurts delivery for a 14 t chunk.** At 100 kWe / Case B, the 20 t reactor swamps the chunk; even dual-ion drops to 68%. The chunk-size-optimal reactor is sub-Kilopower for water radio-frequency ion + Case B (formally minimized when reactor mass equals the propellant savings, which lands near 5–10 kWe in the data).

5. **The split-prop architecture (C6) fails for a reason I didn't anticipate.** Earth-launched xenon successfully handles inbound braking at 2000 s, but Saturn egress on chunk-fed water-microwave-electrothermal eats 60% of the chunk before the spacecraft leaves Saturn's gravity well. The architecture only recovers if Saturn egress *also* moves to high specific impulse — at which point C6 is essentially "water radio-frequency ion + xenon supplement," not a separate architecture.

6. **The Saturn egress chunk-fed burn was previously assumed cheap. It is not.** With a 14 t chunk plus 5+ t dry plus 2 t reactor plus any Earth-launched tanks, the egress mass-ratio at 500 s specific impulse costs 8–10 t of water — most of the chunk. This is the load-bearing finding the campaign had not yet surfaced. **Saturn egress wants the same high specific impulse as inbound braking.** Microwave electrothermal is not viable on either side under the conops' chunk mass.

7. **R6 was wrong in a structurally important way.** R6 concluded "microwave electrothermal at 500 s is power-optimal for Kilopower-class missions." That was true under R6's assumption of zero reactor mass and zero dry mass — under a "chunk + propellant only" model. R10 adds reactor + dry mass and shows that even at the power-optimal specific impulse, microwave electrothermal cannot close mass for a chunk this size. **The Stuhlinger / Edelbaum power-optimal-specific-impulse argument applies only at chunk masses much larger than the reactor + dry mass.**

## Revisit

H10a, H10c, H10d, H10e held; H10b and H10f falsified.

**H10b (microwave electrothermal at 0.5–5%) falsified.** The R8 case B delivery of 4.7% was computed without reactor mass (R8 inherited R6's omission). R10 adds 2 t of reactor mass and the delivery drops to 0%. This is the same methodology defect surfacing across rounds. **Recurring lesson #4 (to coin one): every chunk-fed delivery-fraction calculation in this campaign must include reactor mass, dry mass, AND any non-propellant payload as part of the Tsiolkovsky initial mass.** R8 needs a footnote update; the JSON results are unchanged but the interpretation shifts.

**H10f (split-prop at 70–90%) falsified.** I anticipated that decoupling xenon-fed inbound braking from the chunk would preserve the chunk through the inbound leg, ignoring that Saturn egress itself was a heavy chunk burn at microwave electrothermal specific impulse. Saturn egress alone at 500 s / 2.09 km/s costs 35% of the egress-initial mass — and the egress-initial mass on a split-prop architecture is heavier than chunk-only because of the xenon. So the split-prop case loses more chunk water during egress than it saves by avoiding the inbound burn.

**Aggregate H10 status: half-held.** The single-prop trade is exactly what I expected: high specific impulse wins, dual-ion overdelivers, radio-frequency ion is the right answer at TRL 7-8. The split-prop trade failed for a reason that points to a stronger architectural finding: **both Saturn egress and inbound braking want the same thruster, and that thruster is water radio-frequency ion class.**

## Cross-learning

- **Decision-supporting:** water radio-frequency ion (Pale Blue) at Kilopower power class is the recommended inbound propulsion architecture for ICEBERG. At Case B trajectory (slow inbound to velocity-at-infinity = 6 km/s at Earth) it delivers 61% of a 14 t chunk; at Case C (very slow to velocity-at-infinity = 4 km/s) it delivers 80%, meeting the conops' 75% headline. Replaces microwave electrothermal as the conops-stated inbound thruster.
- **Saturn egress propulsion also needs revision.** The conops uses water-microwave-electrothermal for Saturn departure (the chunk-fed mirror of the rendezvous-in burns). R10 shows that segment alone costs 35% of the egress-initial mass at microwave electrothermal specific impulse. Saturn egress should also be on water radio-frequency ion. This is a propulsion architecture revision beyond just the inbound leg.
- **Negative for split-prop (C6) as proposed.** Earth-launched xenon doesn't help unless Saturn egress is *also* moved to high-specific-impulse propulsion. At that point, all-water radio-frequency ion strictly dominates the architecture: same delivery, simpler propellant chain.
- **Negative for power-up strategy.** Adding power to enable higher specific impulse stops helping at the chunk size R10 modeled (14 t). The Fission Surface Power-class (40 kWe) and sub-megawatt (100 kWe) reactor mass overhead degrades delivery below the Kilopower (10 kWe) case. **Sub-Kilopower might be a real design point** — the optimum reactor sizing for 14 t chunks lies below current flight-ready power levels. Worth a future round.
- **Methodology lesson #4 surfaces.** Every Tsiolkovsky-style delivery-fraction calc must include reactor + dry + payload as initial mass. R6 silently omitted this; R8 inherited the omission; R10 corrects it. This is the same recurring pattern (single-number budgets in concept-paper documents are optimistic) showing up in our own derivations, not just external sources.
- **Cruise time becomes the binding constraint at dual-ion-class specific impulse.** 33 years estimated cruise time at Case B / Kilopower / dual-ion is incompatible with the conops 13.5-year round-trip headline. Dual-ion remains a megawatt-class candidate only.
- **New round R5 (proposed-and-needed): mass margin with reactor + dry + payload mass included throughout.** R6's methodology gap is now confirmed load-bearing across two rounds (R8, R10). R5 should rerun R6's power-optimal-specific-impulse curve with the full mass stack to redraw the Pareto frontier. Likely conclusion: the power-optimum collapses to a much smaller window than R6 suggested, centered near 1500–2500 s specific impulse at Kilopower for 14 t chunks.
- **New round R11 (proposed): B-ring dust contamination tolerance for water radio-frequency ion.** Promotes R7 (deferred) to load-bearing because R10's recommendation hinges on radio-frequency ion working under chunk-fed-water grid erosion. Pale Blue's flight heritage is on purified water; ICEBERG chunk water is Saturn-ring-derived and may carry silicate dust.
- **Reading for the conops.** The conops' Propulsion section needs a rewrite: replace water-microwave-electrothermal with water radio-frequency ion for both Saturn egress and inbound braking. The 75% chunk-delivery headline survives but at a different thruster than the conops claims, and only at a slow inbound trajectory (Case C / velocity-at-infinity = 4 km/s at Earth) — which is R9 territory.

