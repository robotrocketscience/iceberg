# Project ICEBERG — Program-Level Risk Register

Top-level risks across the full Project ICEBERG program: mission architecture, spacecraft systems, business / capital, schedule, regulatory, external. **Propulsion-specific risks live in `water-prop/RISKS.md`** and are cross-referenced here by identifier.

This register is owned at the program level, not by any one engineering discipline. Updates happen at program-review cadence, not per-engineering-round.

## Scoring

Likelihood: L1 (<10%) → L5 (>85%). Impact: I1 (minor) → I5 (catastrophic, program-ending or total mission loss). Score = L × I. ≥15 critical, 10–14 high, 5–9 moderate, <5 low.

## 5×5 Matrix

| Impact ↓ \ Likelihood → | L1 | L2 | L3 | L4 | L5 |
|---|---|---|---|---|---|
| **I5** | — | M-TSI, M-AUTO | **M-BAG, M-AEROCAP-HYBRID** | **M-RNDZ-IMPACT** | — |
| **I4** | — | — | M-RNDZ, M-1SHIP | **M-LGA, B-FUND** | **A-REACTOR, A-REACTOR-SP, A-REACTOR-LIFE** |
| **I3** | — | — | B-COMP, B-STAFF, M-MASS, S-RAD, S-MMOD, S-THERM | — | — |
| **I2** | — | — | — | — | — |
| **I1** | — | S-DSN | — | — | — |

## Sorted register

| ID | Risk | L | I | Score | Category | Status |
|---|---|---|---|---|---|---|
| **M-LGA** | **Lunar gravity assist tour delivers <3 km/s — entire mission energy budget rebalances** | 4 | 4 | **16** | mission | Under analysis in water-prop R2 (trajectory round) |
| **M-AEROCAP-HYBRID** | **Earth aerocapture is necessary for any surviving cell, AND single-pass aerocapture is now closed — only the hybrid (single-deep-pass with sacrificial bag + multi-pass shallow aerobraking) remains as candidate, and it has not been engineering-validated.** | 3 | 5 | **15** | mission | **Reframed 2026-05-15 latest+7 from M-AEROCAP-RETIRED.** Hyperion R-no-atmospheric-capture-baseline (`1ce7c89`) showed zero of 288 cells close without aerocapture — aerocapture is necessary, not preferred. Phoebe R-chunk-as-heat-shield-revisit (`9b3d29e`) closed single-pass aerocapture across the full envelope (zero of 40 cells achieve capture at periapsis ≥ 50 km; ballistic coefficient binds). R-hybrid-aerocapture-aerobraking (hyperion SCOPE `6ef36eb`) is the sole architecturally-credible aerocapture-adjacent candidate. **Has not been run.** Even if it closes, KRUSTY-anchored specific power still kills the cell (R-aerocapture-cliff-shift). |
| **M-RNDZ-IMPACT** | **B-ring rendezvous crossings give ~99 percent per-pass impact probability under zone-averaged optical-depth ~ 2** — chunk-rendezvous architecture is structurally exposed to particle-flux on every chunk capture | 4 | 5 | **20** | mission | **NEW 2026-05-15 latest+5.** Surfaced by titan-2 R-saturn-soi-periapsis-depth (`1b1b889`) H5. The B-ring chunk-rendezvous geometry itself is a hostile-environment problem orthogonal to the velocity-match problem (R-HE-graze-feasibility falsification). Two of three operational responses titan surfaced are foreclosed (target B-ring sub-features falsified by titan-2 R-bring-fine-structure-rendezvous H1; residence-class ram-scoop retired by project-owner direction 2026-05-15 latest+6). Sole open response is engineered survivability through crossings — R-bring-rendezvous-survivability (SCOPE authored latest+6 at `water-prop/rounds/R_bring_rendezvous_survivability/SCOPE.md`). Has not been run. |
| **M-BAG** | **Bag thermal containment fails — cargo sublimates to space** | 3 | 5 | **15** | mission | Primary architectural sensitivity per conops. Bag engineering doc owns the analysis. |
| **A-REACTOR** | Nuclear reactor program (Kilopower / Fission Surface Power / megawatt-class) slippage or cancellation — scope to ≥ 500 kWe not in any funded program | 5 | 4 | **20** | external / partnership | **Amended 2026-05-15 latest+9: now formally encoded as REQUIREMENTS L0-24 + L1-046/047/048.** The iapetus four-round chain (`eab4b13`, `b03b3e2`, `d05f9a8`, `9a556b3`) quantified the joint posterior: max conjunction posterior on flight-reactor-availability inside 2032-2035 is 0.0055%-0.77% depending on assumption combination; 2.7% absolute ceiling under all conditional priors set to 1.0. The risk is now a hard L0 precondition on commercial-class commitment (demonstrator-class missions are exempt). Scoring unchanged (5×4=20) — the risk magnitude is correct as scored; the change is structural: the risk is now an explicit Gate-D-close gate rather than a forecasting concern. **Prior latest+7 commentary preserved:** Re-scored latest+7 (likelihood 4→5). Same risk core as prior — US has no fission flight heritage since 1965, FSP Phase 2 not yet awarded as of May 2026, FY2026 budget request zeroed nuclear-electric-propulsion and nuclear-thermal-propulsion technology lines, DARPA DRACO cancelled May 2025. Likelihood raised because the program is now joined by two new conditional risks (A-REACTOR-SP, A-REACTOR-LIFE) — even if a reactor program funds at the ≥ 500 kWe scope, it must also clear specific-power and lifetime gates that no current US program targets. See water-prop A01. |
| **A-REACTOR-SP** | **Reactor specific power must be ≥ 5 W/kg (with aerocapture credit) or ≥ 8 W/kg (without) for any surviving cell.** Closure cliff between 7-8 W/kg; KRUSTY 2018 flown anchor is 2.4 W/kg | 4 | 4 | **16** | external / partnership / technology | **Amended 2026-05-15 latest+9: now formally encoded as REQUIREMENTS L1-047** (specific-power floor allocated to PROP, traces to L0-24). The risk is no longer a forecasting concern; it is a verifiable Gate-D-close precondition on commercial-class launch. **Prior latest+7 commentary preserved:** Surfaced by enceladus-r5 R-specific-power-cliff (`2d63291`) + R-aerocapture-cliff-shift (`12058b5`). Round-6's "two mass models" were mathematically equivalent (R-arch-E-specific-power-flown-anchored `62f7079`: 60 of 60 cells match) — the campaign's prior "10 W/kg conservative anchor" was the optimistic edge of the closure cliff, not the floor. Inbound aerocapture (R-hybrid-aerocapture-aerobraking) rescues the 5-8 W/kg band but cannot rescue KRUSTY 2.4 W/kg (outbound burn becomes binding). 40 W/kg paper-aspiration target is TRL-2 per R-power-wonder. No funded US reactor program targets ≥ 5 W/kg at megawatt-class scope. |
| **A-REACTOR-LIFE** | **Cumulative reactor full-power burn lifetime must be ≥ 5-10 years.** KRUSTY 2018 ground-test heritage is 28 hours — 3-4 orders of magnitude short | 4 | 4 | **16** | external / partnership / technology | **Amended 2026-05-15 latest+9: now formally encoded as REQUIREMENTS L1-048** (lifetime floor ≥ 10 years cumulative full-power burn, allocated to PROP, traces to L0-24). The risk is no longer a forecasting concern; it is a verifiable Gate-D-close precondition on commercial-class launch. **Prior latest+7 commentary preserved:** Surfaced by enceladus-r5 R-reactor-lifetime-vs-burn-time (`c685c52`). Every viable Architecture-E cell needs 70,000-105,000 hours of cumulative reactor full-power burn time. Survival: at L=5 yr (Brayton flight-rated minimum) only 9-10 W/kg cells at X≥20 km/s survive; L=10 yr (Kilopower design target) ~80 percent survive; L=15 yr non-binding. KRUSTY heritage of 28 hours puts the flown anchor at L=0.003 yr — zero cells survive at flown anchor. Orthogonal axis to A-REACTOR-SP: the two compound (KRUSTY misses both). |
| **M-RNDZ** | Saturn rendezvous fails (target chunk wrong size, wrong composition, wrong orbit) | 3 | 4 | 12 | mission | B-ring particle distribution favors meter-class; tens-of-tonne chunks statistically findable but operationally fragile. |
| **M-1SHIP** | Single-ship failure mode on a 13-year cruise (no in-flight redundancy) | 3 | 4 | 12 | mission | Fleet architecture (ships 2 and 3 launched before ship 1 returns) mitigates at program scale but not per-flight. |
| **B-FUND** | Capital-horizon mismatch — at flown anchors no commercial cell exists, only technology-demonstrator framing is honest | 4 | 4 | **16** | business | **Amended 2026-05-15 latest+9: formal capital-structure framing is now encoded in REQUIREMENTS L0-13 parenthetical** (government-grant / sovereign-research-grant as operative compliance pathway; return-seeking capital ruled out across every assumption combination tested per iapetus four-round chain). Pricing-anchor question opened mid-pass under R-pricing-anchor-revisit; pricing-anchor audit (`water-prop/rounds/R_pricing_anchor_revisit/AUDIT.md`) showed the pitch headline $1,400/kg is BELOW what financial rounds already use ($2,000-10,000/kg), so pricing correction does not flip the verdict — reactor-program-availability remains the binding constraint. Scoring unchanged. **Prior latest+7 commentary preserved:** at flown-anchored specific power and conservative reactor-lifetime, **no surviving cell exists at any anchor or waiver tested**. The "restoration via aerocapture closure + L1-007 relaxation" path is closed by R-aerocapture-cliff-shift (`12058b5`): even aerocapture closing perfectly cannot rescue KRUSTY-anchored cells because outbound binds. The chunk-shrinking heterogeneous-cadence alternative (project-owner USER-NOTES axis 02 hypothesis) was falsified by rhea R-heterogeneous-cadence (`2e85d4f`): chunk-shrinking loses NPV in every regime tested. **Honest capital structure at flown anchors is government-grant / technology-demonstrator, not return-seeking.** Staged-commitment via go/no-go gates A-C HOLDS as a structure (decoupled from chunk-size variation per rhea R-heterogeneous-cadence). |
| **B-COMP** | Lunar in-situ-resource-utilization water beats ICEBERG to market on price | 3 | 3 | 9 | business / competitive | Sets price ceiling. Compresses margin, doesn't kill thesis. |
| **B-STAFF** | Organizational continuity over 13+ year mission lifetime | 3 | 3 | 9 | business / programmatic | Cassini precedent: possible but expensive. |
| **M-MASS** | Spacecraft mass budget overruns | 3 | 3 | 9 | mission | Locked downstream of propulsion architecture decision. |
| **S-RAD** | Avionics radiation tolerance at Saturn radiation belts and over 13-year mission | 3 | 3 | 9 | spacecraft | Belt environments mapped by Cassini. Standard radiation-hardened parts. |
| **S-MMOD** | Micrometeoroid or orbital debris damage over the mission | 3 | 3 | 9 | spacecraft | Standard shielding practice. |
| **S-THERM** | Thermal management failure — radiator degradation over 13 years | 3 | 4 | 12 | spacecraft | Coating degradation and impact strikes. |
| **M-TSI** | Trans-Saturn injection chemical kick-stage failure at Earth departure | 2 | 5 | 10 | mission | Bought commercial; standard reliability. |
| **M-AUTO** | Spacecraft autonomy failure — round-trip light-time at Saturn is 80–160 minutes; full autonomy required, software complexity is large | 2 | 5 | 10 | spacecraft / software | Substantial software-engineering risk, not propulsion. Owned by avionics team if/when one exists. |
| **S-DSN** | Deep Space Network communications availability over 13 years | 2 | 1 | 2 | spacecraft / external | Voyager and Cassini precedent — solvable. |

## Cross-reference to propulsion register

| Program risk here | Propulsion register entry |
|---|---|
| M-LGA | water-prop/RISKS.md B01 (testable in water-prop R2 trajectory round) |
| A-REACTOR | water-prop/RISKS.md A01 (informs water-prop R6 power-trade round) |

Other propulsion risks (microwave electrothermal thruster ceiling, water-ion grid life, efficiency sensitivities, mechanism validity, etc.) are not surfaced at the program level until they cross a threshold that affects mission architecture. The propulsion register's R-final synthesis round is where elevation happens.

## What's not on this list

- Regulatory / export control / launch licensing.
- Insurance / cargo loss financial coverage.
- Treaty (Outer Space Treaty, Article II) implications of extracting Saturnian material.
- Public reception / political risk to sovereign customers.
- Cargo-side risks beyond bag containment (ice composition, structural integrity, etc.).

These belong on this register eventually but I haven't reasoned about them yet. Flagged for the next program review.

## Methodology note

This register was built bottom-up by extracting from existing ICEBERG documentation (`ICEBERG-conops.md`, `ICEBERG-pitch.md`, `ICEBERG-bag-engineering.md`, prior memory) plus the propulsion register. Top-down failure-modes-and-effects analysis is the audit complement and has not been done.
