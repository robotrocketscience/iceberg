# Trade study — ICEBERG end-of-mission concept of operations

**Date:** 2026-05-15
**Author:** Titan parallel session
**Scope:** End-of-cruise leg only, from Saturn departure through delivery of clean water to a low Earth orbit customer. Does not revisit cruise architecture, source-end harvesting, or vehicle class trades upstream.
**Status:** Recommendation pending review.

## Trigger

The prior baseline end-of-mission concept (direct aerocapture into low Earth orbit) has two structural problems that were not addressed in the existing concept-of-operations document:

1. **Planetary protection.** Saturn ring-source material has plausible Enceladus-derived content via the E-ring pathway. The Committee on Space Research (COSPAR) classification for return of such material to Earth is restricted Earth return — the same category as Mars sample return — which requires containment from acquisition through receipt at a controlled facility. Aerocapture violates containment by definition: the ablation losses inject unsurveyed extraterrestrial material directly into Earth's atmosphere.
2. **Engineering feasibility.** Megaton-scale aerocapture has no demonstrated technique. The largest aerocapture target in any flight or near-flight plan is in the few-ton class. Scaling six orders of magnitude past demonstrated capability is not a real baseline.

This memo compares the prior baseline against a proposed alternative and recommends a replacement baseline.

## Alternatives

### Alternative A — Direct aerocapture (prior baseline)

Inbound from Saturn, aerocapture the carrier vehicle into low Earth orbit. Deliver the ice cargo into Earth's atmosphere via repeated aerobraking passes or aerocaptured processing. Sterilization and characterization happen post-arrival at Earth, or are deferred entirely.

### Alternative B — Cislunar quarantine and ferry (proposed)

Inbound from Saturn, capture into the Earth-Moon system via a combined Earth-Moon weak-stability-boundary trajectory. No atmospheric entry by the cargo. Process the ice at a fully automated depot in lunar orbit: melt, filter, sterilize, characterize, tank. Ferry sterilized water in sealed tanks from the lunar-orbit depot to low Earth orbit via a reusable water-Microwave-Electrothermal-Thruster tug class.

The depot is uncrewed by design. Crew at the depot would defeat the quarantine (returning crew is the contamination vector), would eat the mass and schedule budget the architecture buys, and is not a competence the program can assume.

## Criteria

Seven criteria, ranked by my read of how decisive each is. Higher rank means more decisive.

1. Planetary protection compliance (regulatory and treaty risk)
2. Mass of clean water delivered to low Earth orbit per cycle
3. Technology readiness at the riskiest subsystem
4. Failure mode severity (total loss versus degraded throughput)
5. Capital cost
6. Schedule to first delivery
7. Operational complexity beyond first delivery

## Scoring

### 1. Planetary protection

**Alternative A.** Restricted Earth return is incompatible with aerocapture. Architecture cannot pass a formal planetary protection review. **Fatal blocker.**

**Alternative B.** Cargo never enters Earth's atmosphere. Sterilization, characterization, and residue containment happen at the lunar-orbit depot. Only certified water in sealed tanks reaches low Earth orbit. Defensible by design under restricted return rules. **Passes review.**

This criterion alone is decisive. The remaining criteria score the magnitude of the win for risk-discounting purposes downstream.

### 2. Mass of clean water delivered to low Earth orbit per cycle

Let cargo mass at Saturn departure equal X kilograms.

**Alternative A.** Megaton-class aerocapture is undefined; the realistic engineering path is aerocapture of a small carrier followed by repeated aerobraking passes for the cargo. Each pass ablates the surface. Order-of-magnitude estimate for total cargo loss across the capture sequence: 30 to 60 percent. Useable water at low Earth orbit: roughly 0.4 X to 0.7 X. The ablated mass is the planetary protection violation from criterion 1.

**Alternative B.** Weak-stability-boundary capture: effectively zero mass loss (no atmosphere). Depot processing: roughly 5 percent loss to residue, filtration cartridges, and sterilization waste. Ferry transport at water-Microwave-Electrothermal-Thruster specific impulse of about 700 seconds across a round-trip delta-V of approximately 4 kilometers per second: the ferry consumes about 44 percent of each tank-leg's mass as its own propellant. Net useable clean water at low Earth orbit per Saturn cycle: about 0.53 X.

**Verdict.** Comparable net mass, roughly half the Saturn-departure cargo in both cases. But Alternative A's half is unsterilized, uncharacterized, and arrives via uncontrolled atmospheric injection of the other half. Alternative B's half is clean, certified, in sealed tanks. The two are not interchangeable.

### 3. Technology readiness

**Alternative A.** Megaton-scale aerocapture: technology readiness level 1, possibly 2. Six orders of magnitude past demonstrated capability.

**Alternative B.**
- Weak-stability-boundary capture: technology readiness level 9 at spacecraft scale, demonstrated by the Hiten mission and used operationally by the Gravity Recovery and Interior Laboratory mission. Not demonstrated at kilometer-scale cargo, but the trajectory mathematics is mass-independent.
- Automated water processing in deep space: technology readiness level 3 to 5. Components (filtration, distillation, mass spectrometry, robotic handling) are individually flight-heritage. Integrated system not demonstrated.
- Reusable water-electric ferry tug: technology readiness level 5 to 7. Adjacent to existing in-space transportation product lines.

**Verdict.** Alternative B uses higher-readiness building blocks at every layer.

### 4. Failure mode severity

**Alternative A.** Aerocapture corridor miss is total loss of payload; the entry corridor is narrow and the spacecraft does not get a second pass. Heat shield failure is total loss. Higher-than-modeled ablation is degraded throughput. Planetary protection review failure is program death at any point in the mission lifecycle, with the possible additional cost of an international treaty incident.

**Alternative B.** Capture miss results in an Earth flyby and a retry on the next phasing window — recoverable, the spacecraft is still alive. Depot subsystem failure degrades throughput but does not destroy the depot. Ferry failure loses one ferry and one tank of cargo, not the depot or the cruise vehicle. The depot itself is the highest-value asset and it is not in any failure path that the cargo or the ferries can trigger.

**Verdict.** Alternative B's worst case is a delayed delivery. Alternative A's worst case is total program loss. An order of magnitude difference in tail risk.

### 5. Capital cost

**Alternative A.** Megaton-scale aeroshell development cost is speculative. Plausibly several hundred million dollars, possibly more, with no comparable precedent. No depot, no ferry fleet, no other capital infrastructure.

**Alternative B.** No aeroshell. Depot infrastructure: rough estimate 500 million to 1 billion dollars first-of-kind. Reusable ferry tug, first of class: 100 to 300 million dollars. Subsequent ferry units: 30 to 100 million dollars each.

**Verdict.** Alternative B's total capital is higher than Alternative A's nominal. Alternative A's nominal is fictional because the architecture does not survive review.

### 6. Schedule to first delivery

**Alternative A.** Nominal schedule is shorter (no depot, no ferry fleet to develop). Real schedule includes a planetary protection review that adds two to four years to critical path before any launch is authorized, and the review may never clear.

**Alternative B.** Depot and ferry tug developments can run in parallel with cruise vehicle development. The combined weak-stability-boundary capture sequence adds approximately 6 to 12 months at the back end versus aerocapture. First delivery latency is probably 1 to 2 years longer than Alternative A's optimistic nominal.

**Verdict.** Alternative B's real schedule is shorter than Alternative A's review-inclusive schedule. Alternative A's paper schedule is fictional.

### 7. Operational complexity beyond first delivery

**Alternative A.** Each Saturn cycle requires another aerocapture, another atmospheric injection event, another planetary protection escalation. Operations do not amortize.

**Alternative B.** Depot and ferry fleet amortize across all subsequent Saturn cycles. Marginal cost per delivered tank drops with operating tempo. Regulatory question is settled once at deployment and stays settled for the operating life of the depot.

**Verdict.** Alternative B has dramatically better long-run economics. The depot is also reusable for any other source-end mission (asteroid water, lunar water resold to higher orbits, comet-fragment processing) without architectural change.

## Sensitivity check

The recommendation is dominated by criterion 1 (planetary protection). What would change the answer?

- **If planetary protection turns out not to apply** — for example if the cargo is judged unambiguously non-Enceladus-derived after better characterization of E-ring sourcing. Then Alternative A loses its fatal blocker. Alternative B still wins on criteria 3, 4, and 7. The trade narrows but Alternative B still leads.
- **If a working megaton-scale aeroshell technology emerges in the demonstrator window.** Lifts Alternative A on criterion 3. Alternative B still wins on criteria 1, 4, and 7.
- **If capital is severely constrained.** Alternative B's depot-and-ferry infrastructure becomes harder to fund. But Alternative A's only viable path also requires new technology development (the unsolved megaton aeroshell), so the capital comparison is not one-sided. Neither option is cheap.
- **If first-delivery schedule is the dominant program constraint** (for example if a customer commitment requires delivery by a specific date). Alternative A's paper schedule looks better but its real schedule is worse. Alternative B still wins on real schedule.

No reasonable sensitivity flips the answer.

## Recommendation

**Adopt Alternative B as the baseline end-of-mission concept of operations.** Drop Alternative A from the architecture matrix. Retain it as a documented historical baseline for traceability but do not carry it forward as an active option.

## Implications for the rest of the project

Adopting Alternative B forces revisions in adjacent sections of the project documents:

1. **Architecture matrix.** The end-of-mission row currently anchored on aerocapture is replaced by a row anchored on cislunar quarantine. Numerical assumptions in the matrix that depended on direct low-Earth-orbit delivery need to be reviewed.
2. **Requirements documents (REQUIREMENTS.md, REQUIREMENTS-L1.md).** Add depot system requirements. Add ferry tug requirements. Adjust cruise vehicle arrival requirements (no longer needs aeroshell; does need weak-stability-boundary trajectory targeting).
3. **Risks document (RISKS.md).** Remove or downgrade aerocapture-related risks. Add depot subsystem risks, ferry fleet risks, weak-stability-boundary capture timing risks.
4. **Demand model (ICEBERG-demand.md).** Ferry capacity becomes a new throughput constraint between Saturn cycles and delivery to customers. Need to size the ferry fleet against demand model.
5. **Pitch (ICEBERG-pitch.md).** The cislunar depot is a new piece of physical infrastructure that the pitch did not previously describe. It is also reusable for any other source-end mission, which is a strategic asset worth highlighting.

## Open items the trade exposes

1. **Pick the depot orbit.** Near-Rectilinear Halo Orbit, Earth-Moon Lagrange point 1, Distant Retrograde Orbit, or a specific lunar orbit. Each has different stationkeeping cost, communications geometry, and ferry round-trip delta-V. Trade is small but real.
2. **Quantify ferry propellant fraction more precisely.** The 44 percent figure assumes 700-second specific impulse and 4 kilometers-per-second round trip. Both are open variables. Worth a one-page follow-up analysis.
3. **Define the depot biosignature-detection protocol.** What happens if in-line characterization instruments detect a candidate biosignature in a batch? Default policy: sterilize anyway, store characterization data, telemeter, refer to a follow-on dedicated sample-return mission. Worth making the policy explicit.
4. **Confirm the Committee on Space Research classification.** This trade assumes restricted Earth return applies. Worth getting a formal opinion from a planetary protection officer before the next document revision. If the classification turns out to be unrestricted, criterion 1 weakens and the trade narrows.
5. **Pick the trajectory-optimization toolchain.** Jet Propulsion Laboratory's Mission Analysis Low-Thrust Optimizer and the General Mission Analysis Tool both handle the combined Earth-Moon flyby class. Either works. Pick one before the next trajectory iteration.
6. **Decide whether the ferry fleet uses cargo water as propellant.** The water-Microwave-Electrothermal-Thruster can. Doing so couples ferry economics to cargo throughput. Alternative is a separate ferry propellant supply chain.
