# Project ICEBERG — Level 1 Requirements

**Status:** draft v0.4, 2026-05-15.
**Scope:** Level 1 system-level requirements derived from `REQUIREMENTS.md` (Level 0). Each L1 requirement names the system or subsystem responsible, has a verifiable metric, and traces upward to one or more L0 parents.
**Audience:** subsystem leads at concept-design level. The design and analysis for each subsystem flows downstream from these requirements. Variances from any L1 metric trace back to the L0 parent — if the parent absorbs the variance, the L1 metric is renegotiated; if not, the design is rejected.

---

## 1. Conventions

- **SHALL** = mandatory.
- **SHOULD** = strongly preferred; deviation requires written rationale.
- **MAY** = permitted.
- Verification methods: **T** = Test, **A** = Analysis, **D** = Demonstration, **I** = Inspection.
- Identifier format: `L1-NNN` (sequential within this document).
- Each requirement carries a "Traces to" field listing L0 parents.
- Each requirement carries an "Allocates to" field naming the responsible system.

## 2. System code legend

| Code | System | Owns |
|---|---|---|
| **PROP** | Propulsion | Reactor, electric thrusters, propellant feed, chemical kick stage interface |
| **THRM** | Thermal control | Radiators, multi-layer insulation, heat-pipe network, bag thermal environment |
| **STRC** | Structures and mechanisms | Tug bus, trawl-bag system, capture interface, deployable mechanisms |
| **GNC** | Guidance, navigation, control | Attitude control system, trajectory propagation, autonomy stack |
| **COMM** | Communications and data | Deep Space Network link, on-board storage, telemetry |
| **GS** | Ground segment | Mission control, ground stations, simulation team |
| **MISS** | Mission planning | Launch scheduling, Saturn arrival windowing, fleet management |
| **PROD** | Production | Vehicle manufacture rate, supply chain, sustaining engineering |
| **FIN** | Financial | Capital structure, cost models, customer contracts |
| **SAFE** | Safety and planetary protection | Re-entry, contamination control, regulatory compliance |
| **CUST** | Customer interface | Hand-off mechanism, propellant transfer, contract terms |

---

## 3. Propulsion (PROP)

| ID | Requirement | Metric | Traces to | Allocates to | Verification |
|---|---|---|---|---|---|
| L1-001 | The propulsion system SHALL achieve Saturn capture into a closed orbit at or within the B-ring radius. | Saturn capture delta-v ≤ 3.0 km/s, periapsis altitude inside Saturn's main rings (≤ 92,000 km from Saturn center), achieved within 30 days of Saturn approach. | L0-01 | PROP | A, T |
| L1-002 | The propulsion system SHALL provide the inbound delta-v required to return chunk-bearing vehicle to a customer-specified low or medium Earth orbit, within the L0-05 round-trip envelope. | Inbound integrated delta-velocity ≤ **25 km/s** under continuous-thrust electric, conditional on high-elliptical Saturn-side departure orbit (~1 million km) and lunar gravity assist credit at Earth approach. Above 25 km/s, round-trip exceeds L0-05 ceiling. For the surviving 500-kWe chemical-kick architecture, the impulsive 6.42 km/s budget remains binding. R-inbound-dv-continuous-thrust (titan, commit `58581fb`); R-outbound-dv-continuous-thrust (rhea). | L0-02, L0-05 | PROP | A, T |
| L1-003 | The reactor SHALL provide the electrical power required for the chosen architecture cell over the mission-elapsed lifetime. | Time-averaged available power ≥ **500 kilowatt-electric** for the surviving year-zero-through-fifteen chemical-kick + electric-inbound cell (revised upward from 100-kWe Kilopower-class per R-megawatt-marvl-radiator). Beginning-of-life to end-of-life degradation ≤ 20%. **Reactor lifetime under multi-year continuous inbound burn not yet derived; follow-on round R-reactor-lifetime-under-continuous-thrust-inbound recommended.** Per R-power-wonder findings 2 and 3, reactor-class delivery by 2032–2035 is contingent on a NASA Fission Surface Power Phase-2 award that has not yet happened, plus a 5× scope expansion past Phase 2's 100-kWe target. | L0-04, L0-05 | PROP | T, A |
| L1-004 | Electric thrusters SHALL be tolerant of bag-feed water with realistic Saturn-ring silicate contamination, downstream of an inline filtration stage. | Thruster grid life ≥ 7 years at design propellant flow, with Option B filter (≤ 200 kg, 100-nanometre mesh) in place. Pre-Gate-B chamber test required. | L0-03 | PROP | T, D |
| L1-005 | The propulsion system SHALL provide attitude control authority sufficient for radial-offset stationkeeping during bag-fill operations. | Reaction control system delta-v reserve ≥ 30 m/s per fill cycle (per R-bag-engineering §5). | L0-01 | PROP, GNC | A, T |
| L1-006 | The vehicle SHALL be refuelable from in-space water inventory once a depot or prior-mission delivery is available. | Refuel interface compatible with low-Earth-orbit cryogenic-water depot specification; refuel duration ≤ 14 days per cycle. | L0-18 | PROP, CUST | A, D |
| L1-047 | The flight reactor SHALL provide system-level specific power ≥ 8 W/kg without aerocapture credit, OR ≥ 5 W/kg conditional on successful hybrid-aerocapture-aerobraking closure (R-hybrid-aerocapture-aerobraking). | System-level specific power at end-of-life ≥ floor per the binding architecture cell. Floor anchored on R-arch-E-specific-power-flown-anchored (`62f7079`: closure cliff between 7-8 W/kg) and R-aerocapture-cliff-shift (`12058b5`: inbound aerocapture rescues 5-8 W/kg band, cannot rescue KRUSTY 2.4 W/kg). KRUSTY 2018 flown anchor of 2.4 W/kg is 2-3× below floor. Verified by qualified ground demonstration or flown precursor at the design power class. | L0-04, L0-05, L0-24 | PROP | T, A |
| L1-048 | The flight reactor SHALL demonstrate cumulative full-power burn lifetime ≥ 10 years before commitment to commercial-class launch. | Cumulative reactor full-power burn time ≥ 10 years (Kilopower design target; per R-reactor-lifetime-vs-burn-time `c685c52`, viable Architecture-E cells require 8-12 years). KRUSTY 2018 flight-heritage of 28 hours is 3-4 orders of magnitude short. Verified by qualified ground accelerated-life test plus on-orbit demonstrator if applicable. Demonstrator-class missions per REQUIREMENTS §7.5 are NOT subject to this floor; the floor applies only at commercial-class commitment per L0-24. | L0-04, L0-05, L0-24 | PROP | T |

## 4. Structures and mechanisms (STRC)

| ID | Requirement | Metric | Traces to | Allocates to | Verification |
|---|---|---|---|---|---|
| L1-007 | The trawl-bag system SHALL accumulate at least the chunk-class mass within the Saturn-side operations window. | Per-mission accumulated chunk mass ≥ commercial-class floor (L0-04), capped at ≤ 200 tonnes per mission for L0-05 compliance under continuous-thrust electric inbound (titan); within 30 days of bag deployment, at design closing rate ≤ 10 cm/s. **Saturn-side operations location:** B-ring under the surviving 500-kWe chemical-kick architecture; high-elliptical (~1 million km) if a year-twenty-plus all-electric cell is revived via R-chunk-as-heat-shield-revisit. Bag-fill concept-of-operations is currently calibrated to B-ring; high-elliptical relocation is a load-bearing open question for any year-twenty-plus revival. **Economic-lever note (R-delivery-irr-curve, worktree-110450):** the 200-tonne cap is the binding economic constraint at MARVL-anchored mass; sovereign-bond hurdle (~4 percent marginal internal-rate-of-return) requires 209 tonnes-per-ship; regulated-utility hurdle (~8 percent) requires 461 tonnes-per-ship. Relaxing L1-007 toward the B-ring single-chunk physical cap (482 tonnes-per-ship) requires re-deriving L1-002 inbound delta-velocity ceiling against an extended continuous-thrust profile. Aerocapture closure (R-chunk-as-heat-shield-revisit) is necessary-but-not-sufficient for return-seeking-capital framing — L1-007 relaxation is also required. | L0-01, L0-04, L0-13 | STRC | T, A |
| L1-008 | The bag-laminate SHALL retain water-vapour containment over the 14-year mission elapsed time. | Total water-mass loss to permeability ≤ 5% of chunk mass over the inbound 7-year coast. Bench-test-grade verified before flight unit qualification. | L0-03, L0-17 | STRC | T |
| L1-009 | The bag-aperture mesh SHALL reject particles larger than the design cull diameter. | Aperture mesh maximum-particle-pass ≤ 1 m diameter. Verified by lidar reject system at 1-km approach. | L0-03 | STRC, GNC | T |
| L1-010 | The bag system SHALL include an inline filtration stage compatible with Option B (mechanical mesh) sufficiency conditional. | Filter mass ≤ 200 kg, captures particulate > 100 nanometres. Pre-Gate-B test required against Cassini-Cosmic-Dust-Analyser B-ring particle-size distribution. | L0-03 | STRC, PROP | T |
| L1-011 | The vehicle SHALL retain bag integrity through low-Earth-orbit insertion sequence (Earth approach + propulsive trim, no aerocapture). | Bag puncture probability per mission ≤ 5%. End-state bag pressure ≥ 90% of beginning-of-mission pressure. | L0-10 | STRC | A, T |
| L1-012 | The bag system SHALL be scalable across the chunk-mass classes required by the surviving and conditional architecture cells. | Bag-aperture geometry and feed-port interface unchanged across 50 to 200 tonne chunk classes (binding for the surviving 500-kWe chemical-kick cell per L0-05 under continuous-thrust electric inbound). Scalability to 1,000-tonne chunk mass retired as a hard requirement: under R-inbound-dv-continuous-thrust (titan), chunk masses ≥ 500 tonnes burst the round-trip past L0-05's 15-year ceiling. The 1,000-tonne scaling claim now applies only to a hypothetical aerocapture-revived year-twenty-plus cell (R-chunk-as-heat-shield-revisit). Verified by interface-control-document review. | L0-20 | STRC | A, I |
| L1-013 | The vehicle outer mold line SHALL be compatible with at least two qualified heavy-lift launch vehicles. | Vehicle envelope fits within the smaller of {Starship payload bay, New Glenn fairing, Vulcan Heavy fairing}. Mass and structural-loads compatibility verified. | L0-21 | STRC, MISS | A, I |

## 5. Thermal control (THRM)

| ID | Requirement | Metric | Traces to | Allocates to | Verification |
|---|---|---|---|---|---|
| L1-014 | Thermal control SHALL maintain bag wall temperature within the design envelope for water-vapour containment. | Bag-wall temperature 200–280 Kelvin sustained over the inbound coast. Sun-facing wall ≤ 280 K (sublimation control). Anti-sun wall ≥ 100 K (cryopump). | L0-01, L0-03, L0-17 | THRM, STRC | A, T |
| L1-015 | The reactor radiator SHALL reject waste heat sized to the chosen reactor class, with margin for end-of-life degradation. | Radiator heat-rejection capacity ≥ 1.25 × beginning-of-life waste-heat load. Radiator mass per **MARVL-anchored decomposed model** (R-megawatt-marvl-radiator, rhea): at megawatt scale the radiator subsystem is 40–55% of system mass per National Academies 2021 / NASA Modular Assembled Radiators for Very Large systems studies. R-radiator-mass-penalty's earlier decomposed-mid figure (~1.2 t at 1 MWe) is **superseded** as optimistic-wrong; the correct anchor is the bundled formula closer to ~50 t radiator mass at 1 MWe. | L0-04, L0-05 | THRM, PROP | A |
| L1-016 | Thermal control SHALL prevent ice-pinning at the bag harvest port over operational duty cycles. | Harvest port active-heat range supports re-sublimation at ≥ 1 kg/s flow rate, at ≤ 5 kilowatts auxiliary heat. | L0-03 | THRM, STRC | T |

## 6. Guidance, navigation, control (GNC)

| ID | Requirement | Metric | Traces to | Allocates to | Verification |
|---|---|---|---|---|---|
| L1-017 | The guidance, navigation, and control system SHALL provide trajectory propagation accuracy sufficient for trans-Saturn-injection and Saturn-capture targeting. | Trans-Saturn-injection burn dispersion ≤ 0.1% in delta-v magnitude, ≤ 0.1° in direction. Saturn-capture targeting ≤ 100 km dispersion at periapsis. | L0-01, L0-05 | GNC | A, T |
| L1-018 | The attitude-control system SHALL hold vehicle attitude within the design envelope during chunk-fill stationkeeping. | Attitude error ≤ 1° (3-sigma) during fill operations. Roll rate ≤ 0.01°/s. | L0-01 | GNC | T |
| L1-019 | The vehicle SHALL achieve final-orbit insertion within the customer-specified envelope. | Altitude dispersion ≤ 10 km, inclination dispersion ≤ 0.1°, ephemeris accuracy ≤ 1 km cross-track at delivery hand-off. | L0-02 | GNC | T |
| L1-020 | The autonomy stack SHALL handle routine mission events without ground intervention. | ≥ 95% of nominal events autonomous (≥ 99% at large round-trip light-time). Pre-loaded contingency procedures cover ≥ 80% of known fault modes. | L0-10, L0-22 | GNC | T, D |
| L1-021 | Failure-mode response SHALL prevent derelict vehicles from threatening operational orbits or Earth atmosphere. | Lost-comms safe-mode places vehicle in a disposal orbit (heliocentric or graveyard) within 30 days, irrespective of mission phase. | L0-15, L0-17 | GNC, SAFE | A, T |
| L1-022 | The reject system SHALL detect and avoid oversized ring particles approaching the bag aperture. | Forward-facing lidar detects ≥ 1 m particles at ≥ 1 km range, with rotational-dodge maneuver budget ≤ 1 m/s per reject event. | L0-01, L0-03 | GNC, STRC | T |

## 7. Communications and data (COMM)

| ID | Requirement | Metric | Traces to | Allocates to | Verification |
|---|---|---|---|---|---|
| L1-023 | The vehicle SHALL maintain command and telemetry link via Deep Space Network throughout the mission. | Downlink ≥ 1 kilobit per second during cruise; ≥ 10 kilobits per second during critical events; uplink ≥ 1 kilobit per second always. Link margin ≥ 3 decibels at Saturn distance. | L0-22 | COMM | A, T |
| L1-024 | On-board data storage SHALL retain mission-critical telemetry through communication gaps. | Storage capacity ≥ 30 days of telemetry at full sample rate. Critical-event recorder retains 1 hour at 10× normal sample rate. | L0-22 | COMM | T |
| L1-025 | The vehicle SHALL execute pre-loaded autonomy if the communication gap exceeds the design threshold. | Loss-of-signal threshold for autonomy fall-back: 24 hours during nominal phases; 1 hour during capture / departure / delivery. | L0-10, L0-22 | COMM, GNC | T |

## 8. Ground segment (GS)

| ID | Requirement | Metric | Traces to | Allocates to | Verification |
|---|---|---|---|---|---|
| L1-026 | The ground segment SHALL maintain dual-string Deep Space Network coverage at all critical mission events. | At least two qualified ground stations under contract with overlap windows during capture, departure, and delivery events. Backup acquisition time ≤ 1 hour. | L0-22, L0-23 | GS | I, D |
| L1-027 | The ground segment SHALL provide simulation-team capability to replay every vehicle event prior to issuing go/no-go authorisations. | Simulation toolchain (Basilisk + SPICE + custom mission stack) reproduces vehicle state within 0.1% of telemetered values, within 30 minutes of telemetry receipt. | L0-10 | GS, MISS | T, D |
| L1-028 | Ground operations SHALL maintain a contingency library covering all named critical events. | Documented response procedure for each of the 11 critical-event classes (capture, customer release, bag deploy, chunk cinch, Saturn departure, lunar gravity assist, low-Earth-orbit insertion, customer hand-off, refuel approach, safe-mode recovery, end-of-life disposal). | L0-10 | GS | I |

## 9. Mission planning (MISS)

| ID | Requirement | Metric | Traces to | Allocates to | Verification |
|---|---|---|---|---|---|
| L1-029 | Mission planning SHALL produce trajectory solutions closing the L0-05 round-trip ceiling for the selected architecture cell. | Per-mission trajectory total elapsed time ≤ 15 years, including margin. Solutions exist for the Kilopower Variant B chunk-fed chemical and megawatt all-electric cells. | L0-05, L0-06 | MISS | A |
| L1-030 | Mission planning SHALL stagger Saturn-arrival windows so that inbound delivery cadence meets L0-07. | Saturn-arrival windows scheduled to produce ≥ 1 delivery per calendar year at steady state. Earth-Saturn synodic windows characterised through year 40. | L0-07, L0-08 | MISS | A |
| L1-031 | Mission planning SHALL maintain in-cruise inventory of at least 3 vehicles after year 12. | Vehicle build / launch / Saturn-arrival schedule maintains ≥ 3 vehicles in transit at all times after year 12. Verified by Gantt-chart inspection. | L0-08 | MISS, PROD | A, I |
| L1-032 | Mission planning SHALL accommodate scaling to 4 missions per year cadence within 10 years of commercial-class steady state. | Synodic windowing supports 4 Saturn-arrivals in any single calendar year without violating other constraints. | L0-19 | MISS | A |
| L1-046 | Mission planning SHALL NOT schedule any commercial-class mission launch until a flight-qualified reactor program meeting L1-047 (specific power) and L1-048 (lifetime) is documented on contract with a delivery date inside the launch window. | Documented procurement record on file at Gate D close, naming a flight reactor program (Fission-Surface-Power Phase 2 or equivalent), with contracted delivery date inside the program's launch window AND technology-readiness-level ≥ 7 milestones tracked in the program's published schedule. Demonstrator-class missions per REQUIREMENTS §7.5 are NOT subject to this gate. Verified by procurement-record review and independent technical-readiness assessment. | L0-24 | MISS, PROD, PROP | I, A |

## 10. Production (PROD)

| ID | Requirement | Metric | Traces to | Allocates to | Verification |
|---|---|---|---|---|---|
| L1-033 | Vehicle manufacture rate SHALL support the L0-07 cadence at steady state. | Build-line throughput ≥ 1 vehicle per year sustained from year 8 onward. Stretch to 4 vehicles per year within 10 years of commercial steady state. | L0-07, L0-19 | PROD | A, D |
| L1-034 | Spare-vehicle availability SHALL support the L0-09 service-availability requirement. | At least one launch-ready spare vehicle within 13 months of any per-mission failure detection. | L0-09 | PROD, MISS | A |
| L1-035 | Per-mission marginal manufacturing cost SHALL be consistent with L0-12 cost-competitiveness. | Vehicle-build cost ≤ $200 million in 2026-dollars at steady-state cadence (≥ 5 vehicles per year amortisation). | L0-12, L0-13 | PROD, FIN | A |

## 11. Financial (FIN)

| ID | Requirement | Metric | Traces to | Allocates to | Verification |
|---|---|---|---|---|---|
| L1-036 | The capital structure SHALL support program net-present-value positivity at infrastructure-class weighted-average cost of capital. | Project internal-rate-of-return ≥ 8.7% (matching the R-financing-capital-stack blended weighted-average cost of capital). **Status (v0.3):** under R-reactor-roadmap (worktree-110450) MARVL-anchored cashflow audit, marginal internal-rate-of-return at L1-007's 200-tonne cap is 1.45 percent — sub-sovereign-bond, well below the 8.7 percent target. L1-036 is currently NOT met by the surviving architecture. Closure paths: (a) aerocapture (R-chunk-as-heat-shield-revisit) + L1-007 relaxation toward 461 t/ship to reach regulated-utility hurdle; (b) accept that this requirement cannot be met and re-classify capital structure as government-grant / strategic-customer-co-funded (would require L0-13 amendment at the project-owner level). | L0-13 | FIN | A |
| L1-037 | The capital structure SHALL withstand any single mission-loss event without triggering program termination. | Reserve capital ≥ 1.5 × per-mission cost. Mission-loss insurance line available at ≤ 6% per cycle (per R-cadence-multiship finding). | L0-11 | FIN | A |
| L1-038 | Customer contracts SHALL price delivered water below the customer's next-best-alternative supply cost. | Per-kilogram delivery price ≤ 0.5 × (Earth-launched water displacement cost) at the customer interface, at steady state. | L0-12 | FIN, CUST | A |

## 12. Safety and planetary protection (SAFE)

| ID | Requirement | Metric | Traces to | Allocates to | Verification |
|---|---|---|---|---|---|
| L1-039 | The program SHALL not cause an Earth-atmosphere re-entry casualty event. | Probability of casualty per mission ≤ 1 × 10⁻⁴ (per US Federal Aviation Administration 14 CFR 450.101). All re-entries pre-approved per Inter-Agency Space Debris Coordination Committee guidelines. | L0-15, L0-17 | SAFE, GNC | A, I |
| L1-040 | Saturn-system operations SHALL comply with the Committee on Space Research planetary-protection category applicable at mission-design-freeze date. | Documented planetary-protection-officer sign-off before each Saturn-bound mission departure. Bioburden control to applicable category. | L0-16 | SAFE | I |
| L1-041 | No deliberate venting of water vapour, propellant, or chemical waste SHALL occur in any operating customer orbit. | No-vent zone: altitude ≤ 600 kilometres; conjunction zone within 50 kilometres of any operational satellite. Verified by operations log. | L0-17 | SAFE | I |
| L1-042 | The launch vehicle SHALL be selected from at least two qualified providers per critical launch event. | Active contract or maintained qualification with at least two heavy-lift providers at any time. Loss of primary results in mission slip ≤ 12 months. | L0-21 | SAFE, MISS, PROD | I |

## 13. Customer interface (CUST)

| ID | Requirement | Metric | Traces to | Allocates to | Verification |
|---|---|---|---|---|---|
| L1-043 | The customer hand-off interface SHALL transfer water to the customer-side depot or vehicle without plume impingement on customer hardware. | Plume cone clearance ≥ 5° from customer wetted surfaces. Transfer rate ≥ 1 kilogram per second. Liability framework defined per customer contract. | L0-02, L0-03 | CUST, GNC | T, D |
| L1-044 | Delivered water purity SHALL meet customer specification at the hand-off interface. | Purity ≥ 99% H₂O by mass. Trace metals ≤ 1 part per million; trace organics ≤ 100 parts per million. Sampled and certified per delivery. | L0-03 | CUST, STRC | T |
| L1-045 | The customer hand-off interface SHALL be compatible with industry-standard cryogenic-water transfer mechanisms in use at delivery hand-off date. | Interface complies with the prevailing standard for in-space cryogenic-water transfer at the time of delivery, with adapter availability for legacy customer hardware. | L0-02, L0-20 | CUST | I |

---

## 14. Open items not yet captured

Items the orchestrator owes but has not yet drafted:

- **Test-program requirements.** L1 reqs assume test programs exist (Gate-A through Gate-D) but do not specify test campaign content, instrumentation, or environments.
- **Margin requirements.** Mass margin, power margin, delta-v margin should be allocated explicitly. Currently embedded in individual L1 metrics but not normalised.
- **Operations-team requirements.** Headcount, skill mix, training cadence, shift coverage during critical events.
- **Insurance and liability requirements.** Per-mission insurance line, third-party liability cap, customer-acceptance contract framework.
- **Reactor-program-path requirement — RESOLVED 2026-05-15 latest+9.** The v0.4 deferral to `R-reactor-specific-power-program-targets` is now resolved: iapetus's four-round chain ran (synthesis + three robustness rounds), establishing max conjunction posterior on flight-reactor-availability inside 2032-2035 of 0.0055%-0.77%, 2.7% absolute ceiling. Promoted to REQUIREMENTS v0.8 L0-24; L1-046 (procurement gate), L1-047 (specific-power floor), L1-048 (lifetime floor) added this revision per L0-24 traceability requirement. Closes the open-item.
- **Reliability and redundancy requirement (new, post-evening).** Per enceladus's R-mission-success-probability + R-redundancy-budget-cost, a per-mission L0-10 = 0.90 target requires 2-of-3 redundancy on 7 of 8 critical subsystems at $565M–$710M per-vehicle overlay. L1 currently has no reliability requirement allocated to subsystem level. Redundancy budget should propagate as L1 mass, cost, and round-trip-time allocations.
- **L0-09 service-availability charitable reading (new, post-evening).** Per enceladus's R-L0-10-relaxation-impact, L0-09 as literally written is structurally infeasible. The charitable reading the project owner picks ("delivery-cadence-met", "rolling-window service availability", "queue-never-empty") binds as tightly as L0-10 and shapes L0-07 launch-cadence floor. Pending REQUIREMENTS.md amendment.

These propagate to v0.2.

## 15. Traceability summary

Every L0 requirement has at least one L1 child. Selected traceability:

| Level 0 | Level 1 children |
|---|---|
| L0-01 | L1-001, L1-002 (partial), L1-005, L1-007, L1-009, L1-014, L1-017, L1-018, L1-022 |
| L0-02 | L1-002, L1-019, L1-043, L1-045 |
| L0-03 | L1-004, L1-008, L1-009, L1-010, L1-014, L1-016, L1-043, L1-044 |
| L0-04 | L1-003, L1-007, L1-015 |
| L0-05 | L1-002, L1-003, L1-015, L1-017, L1-029 |
| L0-06 | L1-029 |
| L0-07 | L1-030, L1-033 |
| L0-08 | L1-030, L1-031 |
| L0-09 | L1-034 |
| L0-10 | L1-011, L1-020, L1-025, L1-027, L1-028 |
| L0-11 | L1-037 |
| L0-12 | L1-035, L1-038 |
| L0-13 | L1-007 (added v0.3), L1-035, L1-036 |
| L0-15 | L1-021, L1-039 |
| L0-16 | L1-040 |
| L0-17 | L1-008, L1-014, L1-021, L1-039, L1-041 |
| L0-18 | L1-006 |
| L0-19 | L1-032, L1-033 |
| L0-20 | L1-012, L1-045 |
| L0-21 | L1-013, L1-042 |
| L0-22 | L1-020, L1-023, L1-024, L1-025, L1-026 |
| L0-23 | L1-026 |
| L0-24 | L1-046, L1-047, L1-048 (added v0.5) |

(Some L0 requirements remain weakly populated. Notably L0-06 and L0-09 have only one L1 child each — both deserve more decomposition in v0.2.)

## 16. Revision history

| Version | Date | Notes |
|---|---|---|
| v0.1 | 2026-05-15 | Initial draft. Forty-five L1 requirements across eleven systems. Built from Level 0 v0.3. Traceability map at section 15. Test-program, margin allocation, ops, and insurance reqs deferred to v0.2. |
| v0.2 | 2026-05-15 (evening) | Post-four-worker integration. L1-002 inbound delta-velocity revised upward (≤ 25 km/s under continuous-thrust electric per titan; chemical-kick 6.42 km/s preserved). L1-003 reactor-power floor revised upward (500 kWe, not Kilopower-class, per rhea R-megawatt-marvl-radiator); reactor-program-path note added per R-power-wonder findings 2 and 3. L1-007 chunk-mass cap added (≤ 200 t for L0-05 compliance per titan); Saturn-side operations location qualified. L1-012 1,000-tonne scaling claim retired (only applies under hypothetical aerocapture-revived year-twenty-plus cell). L1-015 radiator anchor switched from R-radiator-mass-penalty decomposed-mid (now superseded) to MARVL-anchored decomposed model per R-power-wonder finding 4. Three new open-item categories added (reactor-program-path, reliability/redundancy, L0-09 charitable reading). |
| v0.3 | 2026-05-15 (late evening) | Post-three-handoff integration (worktree-110450, enceladus-r5, rhea-2). L1-007 economic-lever note added: 200-tonne cap is the binding economic constraint at MARVL-anchored mass per R-delivery-irr-curve. Sovereign-bond hurdle requires 209 t/ship; regulated-utility 461 t/ship. L1-007 now traces to L0-13 (net-present-value) in addition to L0-01 and L0-04. Aerocapture closure (R-chunk-as-heat-shield-revisit) is necessary-but-not-sufficient for return-seeking-capital framing — L1-007 relaxation also required. No other L1 metrics changed in this version. |
| v0.4 | 2026-05-15 (latest+8) | No L1 metric change. §14 reactor-program-path open-item updated to record project-owner deferral to `R-reactor-specific-power-program-targets`. Cross-reference added to coupling with L0-13 capital-structure-framing deferral. Both pending Level-0 / Level-1 program-path decisions now gate on the same unrun round. |
| v0.5 | 2026-05-15 (latest+9) | iapetus four-round chain resolves the v0.4 deferral. Three L1 requirements added per REQUIREMENTS v0.8 L0-24: L1-046 (procurement gate; mission planning SHALL NOT schedule commercial-class launch until a flight-qualified reactor program is on contract; MISS, PROD, PROP); L1-047 (reactor specific-power floor ≥ 8 W/kg or ≥ 5 W/kg under aerocapture-credit; PROP); L1-048 (reactor lifetime floor ≥ 10 years cumulative full-power burn; PROP). Traceability map updated with L0-24 row. §14 reactor-program-path open-item closed. Demonstrator-class missions per REQUIREMENTS §7.5 explicitly exempt from L1-046/047/048 per L0-24. |
