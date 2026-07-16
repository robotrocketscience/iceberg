# Risk Register — water-prop / Project ICEBERG

All known project, mission, propulsion, spacecraft, modeling, and sourcing risks. Ranked by likelihood × impact. **Mitigations are deferred** — next pass.

## Scoring

| Score | Likelihood | Probability |
|---|---|---|
| L1 | rare | <10% |
| L2 | unlikely | 10–30% |
| L3 | possible | 30–60% |
| L4 | likely | 60–85% |
| L5 | almost certain | >85% |

| Score | Impact | Consequence |
|---|---|---|
| I1 | minor | Re-plan; no architecture impact |
| I2 | moderate | One round / model needs rework |
| I3 | major | Architecture decision moves; rework partial |
| I4 | severe | Mission concept needs redesign |
| I5 | catastrophic | Program end / mission loss / total cargo loss |

**Risk score = L × I.** ≥15 = critical (red), 10–14 = high (orange), 5–9 = moderate (yellow), <5 = low (green). Probabilities and impact ratings are personal assessments, not vendor data; uncertainty in the rating itself is a meta-risk (E07).

## 5×5 Matrix

| Impact ↓ \ Likelihood → | L1 (rare) | L2 (unlikely) | L3 (possible) | L4 (likely) | L5 (almost certain) |
|---|---|---|---|---|---|
| **I5 (catastrophic)** | — | B07, B08 | **B02, B04** | — | — |
| **I4 (severe)** | — | — | A02, B03, B06, C06, D04 | **B01, C02** | — |
| **I3 (major)** | — | A03, C04, C05, C09 | A04, A05, B05, C07, D01, D02, D05, D06 | A01, C01, C03, C08, F03 | — |
| **I2 (moderate)** | — | — | E04, F01 | E01, E02, E03, E06, F02, E07 | — |
| **I1 (minor)** | — | D03 | — | — | — |

**Bold** = score ≥15 (critical). Empty cells (L5 column, L1 column, top-left) are the gaps in the current understanding — see "Honest gaps" at the bottom. **B01 was upgraded from L3-I4=12 to L4-I4=16 per checkpoint review** — the lunar gravity assist tour delivering 3 km/s is a load-bearing conops assumption that nothing currently retires.

## Sorted register

| ID | Risk | L | I | Score | Category | Tested by round? | Notes |
|---|---|---|---|---|---|---|---|
| **C02** | **Water-ion thruster grid life inadequate for 7+ year operation under oxygen-ion and water-ion erosion** | 4 | 4 | **16** | propulsion | R3 (planned) | No publicly documented long-duration water-ion qualification data. Pale Blue and Koizumi work is short-duration. Xenon-ion heritage (NEXT thruster, 51,000 hr) is the upper bound. |
| **B02** | **Earth aerocapture fails at ICEBERG return** | 3 | 5 | **15** | mission | out of scope here | Technology readiness level 4–5; never flown at the relevant arrival velocity. Mars Sample Return has aerocapture studies; outer-planet return aerocapture is paper-only. |
| **B04** | **Bag thermal containment fails — cargo sublimates to space** | 3 | 5 | **15** | mission | out of scope here | Conops calls bag-capture efficiency the "primary architectural sensitivity for the entire concept." Multi-layer-insulation seam quality at multi-decade lifetime. |
| **B01** | **Lunar gravity assist tour doesn't deliver the assumed 3 km/s "free" ΔV** | 4 | 4 | **16** | mission | R2 (planned) | Conops assumes 3 km/s of Saturn-Earth gravity-assist absorption from a 2–3 flyby lunar tour. Real lunar gravity assists yield 1–5 km/s depending on lunar nodal cycle. Re-rated up per checkpoint review. |
| **A01** | Reactor program slippage (Kilopower or Fission Surface Power program cancelled or delayed past mission need) | 4 | 3 | 12 | program | R6 (planned) | Kilopower has been cancelled and revived multiple times. Fission Surface Power is Phase 1 paper study. United States has no fission flight heritage since 1965. |
| **A02** | Funding mismatch — venture-capital horizon vs sovereign-infrastructure horizon | 3 | 4 | 12 | program | not a simulation-testable risk | "Suez Canal, not Amazon" framing from prior memory. Capital structure issue, not engineering. |
| **B03** | Saturn rendezvous fails — target chunk wrong size or composition | 3 | 4 | 12 | mission | out of scope here | B-ring particle distribution favors meter-class; 14-tonne chunks are statistically findable but operationally fragile. |
| **B06** | Single-ship failure mode — no redundancy on a 13-year cruise | 3 | 4 | 12 | mission | out of scope here | Fleet architecture (ships 2 and 3 launched before ship 1 returns) partially mitigates. |
| **C01** | Microwave electrothermal thruster specific impulse lower than open-literature claim | 4 | 3 | 12 | propulsion | R0 (done) | **Partially confirmed by R0.** Realistic specific impulse 500–700 s, not the 1000 s previously assumed. |
| **C03** | Cathode poisoning by oxygen in the water plasma | 4 | 3 | 12 | propulsion | R3 (planned) | Barium-oxide-impregnated tungsten and lanthanum-hexaboride emitters both vulnerable to oxygen exposure. May force cathode-less radio-frequency designs. |
| **C06** | Propellant contamination from B-ring dust or regolith | 3 | 4 | 12 | propulsion | R7 (planned) | **Re-upgraded from L2 back to L3 per R3i discussion**: B-ring is >99% water ice (per R1), but the 0.1–0.5% non-icy fraction is mostly submicron silicate dust per Cassini Cosmic Dust Analyzer data. Dust fouling of ion thruster grids and electrolyzer membranes is fatal over a 7-year mission. Earlier L2 downgrade was wrong — "99% water" still means dust at the kilogram-per-tonne level. Filtration is now a hard requirement for any ion-based architecture. |
| **C08** | Total electrical-to-jet efficiency off by 2× | 4 | 3 | 12 | propulsion | R4 (planned) | Current numbers are guesses (0.4–0.5). Real values measured at the chosen operating point may differ enough to change architecture choice. |
| **D04** | Thermal management failure — radiator degradation over 13 years | 3 | 4 | 12 | spacecraft | out of scope here | Coating degradation, micrometeoroid and orbital debris strikes. |
| **F03** | No publicly available long-duration water-ion test data | 4 | 3 | 12 | sourcing | R1 (literature pull) | Drives the C02 uncertainty. Pulling Koizumi and Pale Blue full publication list may upgrade or downgrade C02. |
| **B07** | Trans-Saturn injection chemical kick-stage failure at Earth departure | 2 | 5 | 10 | mission | out of scope | Bought commercial; standard reliability. |
| **B08** | Spacecraft autonomy bug causes mission loss | 2 | 5 | 10 | mission | out of scope this campaign | Light-time at Saturn is 80–160 minutes one-way; full autonomy required. Massive software effort, not propulsion. |
| **A04** | Lunar in-situ-resource-utilization water beats ICEBERG to market | 3 | 3 | 9 | program | not propulsion-related | Sets price ceiling; doesn't kill ICEBERG but compresses margin. |
| **A05** | Staffing continuity over 13+ year program | 3 | 3 | 9 | program | not a simulation-testable risk | Cassini precedent: organizational continuity is possible but expensive. |
| **B05** | Mass margin insufficient | 3 | 3 | 9 | mission | R5 (planned) | Will only know after the architecture lock. |
| **C07** | Two-phase flow or clogging in chunk-fed feed system | 3 | 3 | 9 | propulsion | out of scope this campaign | Bag-side problem, not thruster-side; covered in the conops's bag engineering doc. |
| **D01** | Power-processing electronics radiation degradation | 3 | 3 | 9 | spacecraft | out of scope | Standard radiation-hardened practice; not architecturally driving. |
| **D02** | Reactor performance degradation over 13 years | 3 | 3 | 9 | spacecraft | out of scope | Reactor side, not thruster. Affects available power profile. |
| **D05** | Micrometeoroid or orbital debris impact damaging propellant feed or thruster | 3 | 3 | 9 | spacecraft | out of scope | Standard shielding; low-Earth-orbit and B-ring environments well-characterized. |
| **D06** | Avionics radiation tolerance at Saturn radiation belts | 3 | 3 | 9 | spacecraft | out of scope | Belt environments mapped by Cassini. |
| **E01** | Cantera h2o2 mechanism inadequate above ~9000 K (no ionization in mechanism) | 4 | 2 | 8 | modeling | R0b (retest R0 with extended mechanism) | R0 shows convergence failures at 10,000–12,000 K. May be invalidating sweep edges but probably not the operating point (7000 K). |
| **E02** | Plasma non-equilibrium (electron temperature different from gas temperature) not modeled | 4 | 2 | 8 | modeling | R0c (planned) | Real microwave electrothermal thrusters have electron temperature different from heavy-species temperature; affects ionization and dissociation fractions. |
| **E03** | Finite-rate kinetics in the nozzle not modeled (only bounded) | 4 | 2 | 8 | modeling | R0d (future) | Currently bracketed by equilibrium and frozen extremes. A finite-rate Cantera reactor-network model would give a real point estimate. |
| **E06** | Sensitivity to thrust duty-cycle assumption uncharacterized | 4 | 2 | 8 | modeling | R5 (planned) | 50% is a guess. Sensitivity sweep is cheap. |
| **F02** | Training-data references cited but not freshly verified | 4 | 2 | 8 | sourcing | R1 (planned, was R8) | Everything I've cited (Penn State Micci, Tethers HYDROS, Pale Blue, Sandia Aceves) — I haven't pulled the actual papers. Verification round was reordered to R1 per checkpoint. |
| **E07** | Risk ratings themselves are uncertain (meta-risk) | 4 | 2 | 8 | modeling | implicit in every round | The likelihood and impact scores are my best guess. Some risks I haven't thought of (unknown unknowns) are by definition not on this list. |
| **E08** | Reactor dry mass not in trade tables | 4 | 3 | 12 | modeling | R5 (planned) | **New finding from R1**: Kilopower specific power is 2.5–6.5 W/kg, so a 10 kWe reactor weighs 1.5–4 tons; a 40 kWe reactor weighs 6–16 tons; a 100 kWe sub-megawatt unit weighs 15–40 tons. Current power-vs-Isp tables in R1/R2 stage docs do not include this. Affects small-chunk (<50 t) trade decisively. |
| **A03** | Launch vehicle availability or cost | 2 | 3 | 6 | program | not a simulation-testable risk | Falcon Heavy, Vulcan, Starship class options exist. |
| **C04** | Microwave electrothermal thruster cavity erosion | 2 | 3 | 6 | propulsion | R9 (planned) | Magnetron and antenna under plasma exposure. Penn State data exists. |
| **C05** | Frozen-flow penalty larger than R0 lower bound | 2 | 3 | 6 | propulsion | R0 (done — bracketed) | Already bracketed: real value at least equal to frozen specific impulse. |
| **C09** | Thrust vector misalignment from asymmetric chunk-fed propellant flow | 2 | 3 | 6 | propulsion | out of scope this campaign | Bag-side propellant-management problem. |
| **E04** | Wall heat loss in microwave electrothermal thruster chamber not modeled | 3 | 2 | 6 | modeling | R0c (planned) | Adds 10–30% energy loss; affects microwave electrothermal thruster ceiling. Sensitivity test in R0c. |
| **F01** | Vendor data actually proprietary or not pullable | 3 | 2 | 6 | sourcing | R1 (planned) | Some commercial water-MET vendors' data is proprietary; Pale Blue's may be partial. |
| **D03** | Deep Space Network communications over 13 years | 2 | 1 | 2 | spacecraft | out of scope | Voyager and Cassini precedent. |

## Honest gaps in this register

1. **No L1 row populated.** Either I genuinely have no "rare" risks identified, or I'm systematically over-rating likelihood. Audit candidate.
2. **No L5 column populated.** I haven't flagged any risk as ">85% likely." Probably correct (most risks are open questions, not foregone conclusions), but worth checking that I'm not avoiding strong claims.
3. **Unknown unknowns.** By definition not enumerable. The mid-cycle audit (PROTOCOL §6) is the protocol mechanism for surfacing these — explicitly ask "what did I not put on this list?" at round midpoint.
4. **Risks I marked "out of scope this campaign" still need to be tracked at program level.** Aerocapture, bag thermal, autonomy, MMOD, comms — these are large risks for ICEBERG overall but not testable by this campaign. They belong on RRS's program risk register, not just here.
5. **No cross-coupling captured.** Some risks compound: if A01 (reactor slips) hits, the architecture forced to lower-power = lower Isp = changes C02 priority. The matrix doesn't show couplings.

## Where the rounds attack

Round queue reordered per checkpoint review: citation verification moved to R1 because most current numbers are training-data references; everything downstream depends on them.

| Highest-scored testable risks | Round(s) that retire them |
|---|---|
| C02 (water-ion grid life, score 16) | R3 — literature pull, sputter-yield model, cluster-redundancy sizing |
| B01 (lunar gravity assist ΔV uncertain, score 16, upgraded) | R2 — trajectory integration with explicit gravity-assist accounting |
| C01 (microwave electrothermal thruster specific impulse ceiling, score 12) | R0 — **partially done.** Remaining: finite-rate kinetics in R0d |
| C08 (efficiency off by 2×, score 12) | R4 — sensitivity sweep on assumed efficiencies |
| C03 (cathode poisoning, score 12) | R3 (combined with C02) |
| F03 (no long-duration water-ion data, score 12) | R1 — citation verification and literature pull |
| C06 (B-ring dust contamination, score 12) | R7 — contamination tolerance model |
| A01 (reactor program slippage, score 12) | R6 — power-as-free-variable trade with specific-impulse band per power class |
| F02 (training-data references not verified, score 8) | R1 — citation verification (same round as F03) |

**Round queue, in order:**
1. R0 — microwave electrothermal thruster frozen-flow ceiling **(done)**
2. R1 — citation verification (retires F02, F03, F01 partially)
3. R2 — lunar gravity assist trajectory analysis (retires B01)
4. R3 — water-ion grid life and cluster redundancy (retires C02, C03)
5. R4 — efficiency sensitivity sweep (retires C08)
6. R5 — duty cycle and mass margin sensitivity (retires E06, B05)
7. R6 — power vs specific impulse trade across reactor classes (retires A01)
8. R7 — B-ring dust contamination tolerance (retires C06)
9. R0b — extended-mechanism retest of R0 (retires E01)
10. R0c — wall-loss and plasma non-equilibrium in chamber (retires E02, E04)
11. R0d — finite-rate kinetics nozzle expansion (retires E03)
12. R-mid — mid-cycle audit (per protocol §6)
13. R-final — synthesis round with cumulative architecture trade (per protocol §10)

**Next pass:** mitigation strategies for each ≥10 risk, with explicit retire / transfer / accept disposition.

---

## Methodology note

This register was built bottom-up (enumerate every risk I could think of in 30 minutes) rather than top-down (work through a standard FMEA template). Bottom-up surfaces domain-specific risks fast but is prone to omitting categories that don't come to mind. An FMEA pass would be the audit-round complement; flagging as a possible R-audit-1 task.
