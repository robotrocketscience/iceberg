# R-chunk-capture-monte-carlo — replace the 0.85 capture-efficiency anchor with a defensible posterior

**Status:** scope, pre-study. Authored by Saturn (orchestrator), 2026-05-26. Predecessor: `/aelf:wonder` pass on chunk-capture Monte Carlo, 2026-05-26 (three phantom beliefs persisted).

## Premise

A14 chunk-capture efficiency is the single most load-bearing assumption in the mission_graph framework. The desk-study anchor 0.85 has no engineering decomposition and no flight precedent. Bottoms-up product (rendezvous 0.90 × deployment 0.95 × catch 0.80 × containment 0.70 × survive 0.95) gives ~0.46 joint success. The matrix verdict at L0-04 = 25 tonnes requires the real number to be at least 0.75 × anchor (i.e., catch success ≥ 0.64). Below 50 percent the matrix collapses.

The project owner has asked to attack this with a Monte Carlo simulation. The wondering pass (2026-05-26) returned three phantom beliefs the next /aelf:reason will pick up; the most important is that **published precedent for capture-mechanism Monte Carlo is uniformly a hybrid stack — rigid-body / contact-dynamics inner core, Gaussian / empirical outer loop. No naked scalar anchor is defensible in this literature.**

This round designs and runs that Monte Carlo. It is pre-registered with falsifiers per the campaign methodology (lesson 11, phoebe rounds 3-6).

## Architecture-of-record decision — RESOLVED 2026-05-26

Project-owner decision 2026-05-26: **run three architectures in parallel.** The round produces three posteriors (one per decomposition tree) and a three-way comparison memo. The deliverable formally resolves design-axis 19 (currently falsified-no-replacement) and feeds matrix decision points #1 and #2.

The third architecture (everting-sleeve active enclosure) was raised by the project owner during scoping: the everting-sleeve mechanism from earlier cooperative-satellite-capture work (beliefs `ae7031e288c1ce59`, `839a793587c9f84c`, `606187f2f970cc2f`, `3ac3f0245c2e5044`) is a credible third pattern that has not been evaluated against ring-chunk targets. Properties of interest: actively encloses the target (vs harpoon's impact-based capture and ram-scoop's passive drift), geometric plume avoidance (target ends up forward of the thruster), and decel via fabric stretch rather than impulsive contact. The mechanism is unstudied for ICEBERG; this round produces the first defensible posterior.

The three decomposition trees:

| Stage | Single-chunk-harpoon | Ram-scoop residence-class | Everting-sleeve active enclosure |
|---|---|---|---|
| 1 | Rendezvous with one targeted chunk | Radial-offset station-keeping in B-ring | Rendezvous with one targeted chunk |
| 2 | Deploy harpoon / net / claw | Open aperture / fill rate | **Eversion kinematics — sleeve everts cleanly forward** |
| 3 | Catch the chunk | Inelastic deceleration of incoming particles | Envelopment — sleeve geometry captures the chunk |
| 4 | Contain the chunk | Cinch / outlier rejection | Cinch — drawstring closes behind the chunk |
| 5 | Survive grab loads | Inbound permeability (bag retention over coast) | Decel + carry — fabric stretch + transit retention |

**Scale and engineering-risk note (everting-sleeve column):** a 200-tonne ice chunk at ~900 kg/m³ is ~222 m³ — a characteristic length scale of ~7.5 m if roughly spherical, larger if irregular. The sleeve has to be larger than the chunk in both diameter and length (eversion extension distance), so we are talking a deployable fabric structure tens of metres on a side. Largest deployable / inflatable structures flown to date are ~4 m (Bigelow Expandable Activity Module) and ~14 m (Echo balloons, non-everting). **Eversion at this scale has zero flight heritage.** The eversion-kinematics stage carries failure modes the other architectures do not have at the same scale:
- Sleeve jams mid-eversion (snags, asymmetric folding, friction against deployment ring)
- Eversion direction stalls or reverses
- Fabric tears under inflation pressure during eversion
- Asymmetric eversion shifts vehicle centre of mass and induces attitude excursion
- Eversion completes but misaligned with target (chunk drifts during deployment)
- Drawstring cinch fails (knot tangle, actuator stall, fabric bunching)
This is why the decomposition above gets eversion as its own stage (slot 2), distinct from envelopment (slot 3). Treating eversion as part of "deployment" the way the harpoon architecture does would hide the failure mode.

Wondering surfaced this as a structural problem: the locked 0.85 anchor and 0.46 decomposition were both written for single-chunk-harpoon framing; titan-2 R-conops-chunk-vs-ram-scoop pivoted to ram-scoop framing without re-running the decomposition; the everting-sleeve was never evaluated for chunk targets. Running all three in parallel produces the artifact that retires the ambiguity and gives a defensible answer on the everting transfer hypothesis.

Cost impact: Tier 1 (Morris) + Tier 2 (Polynomial Chaos Expansion) work transfers across architectures (uncertainty axes overlap heavily, ~70 percent). Real duplication is Tier 3 — three ~1200-run binomial posteriors at the operating point, one per architecture. Total wall time: ~36 hours MacBook, or one cloud-VM evening. Cross-architecture sensitivity-index comparison is a bonus deliverable.

## Pre-registered hypotheses

(Architecture-of-record locked to three parallel decomposition trees per the section above. Hypotheses below apply across all three unless noted.)

H1: **The defensible posterior on single-pass capture efficiency is a distribution conditioned on target spin-rate**, not a scalar. Falsified if spin-rate sensitivity (total-order sensitivity index) is below 0.10 across the operating envelope.

H2: **The dominant sensitivity axis is target angular velocity (spin rate).** Falsified if any of the other seven axes (chunk mass, surface friction, approach velocity, sensor noise, contact geometry, catcher compliance, controller delay) shows higher total-order sensitivity index.

H3: **A defensible posterior at ±0.02 half-width 95 percent confidence on the binomial capture probability requires approximately 1200 contact-fidelity runs at the operating point**, plus screening runs. Falsified if the half-width target requires more than 5000 runs (would imply the binomial framing is wrong and the outcome is not effectively Bernoulli).

H4: **The contact-engine choice (MuJoCo vs Drake) does not move the posterior by more than 0.05.** Falsified if cross-engine A/B at 200 runs each shows posterior means separated by more than 0.05. If falsified, the contact-engine choice itself becomes a project-owner decision point.

H5: **The five-stage product decomposition over-estimates joint success relative to the contact-fidelity Monte Carlo by at least 0.05 (i.e., the closed-form is optimistic).** Reasoning: closed-form products treat stages as independent, but failure modes co-vary (high spin both raises catch failure and raises containment failure). Falsified if the closed-form is within 0.02 of the contact-fidelity result.

H6 (load-bearing reading): **At least one of the three architectures produces a posterior median single-pass capture probability >= 0.64 × anchor reference.** This is the threshold the matrix verdict at L0-04 = 25 t requires. Falsified if all three architectures' posterior medians fall below 0.64 — in which case the L0-04 25-tonne floor is structurally unviable at current architecture and the matrix's open SCOPEs cascade. Sub-question for the comparison memo: which of the three architectures has the highest posterior median, and is the difference statistically separable given the binomial credible intervals?

H7 (everting-sleeve transfer): **The everting-sleeve mechanism from the satellite-capture study transfers to ring-chunk capture without a posterior penalty greater than 0.10 vs the better of the other two architectures.** Reasoning: the tug application captures cooperative satellites with known geometry, mass, and rigidity; ring chunks are uncooperative, irregular, frictionally poor (ice), and may tumble. Falsified if everting-sleeve posterior median is more than 0.10 below the best other architecture — in which case the sleeve mechanism is satellite-specific and not chunk-capture-transferable.

H8 (eversion-kinematics dominance): **For the everting-sleeve architecture, the eversion-kinematics stage (slot 2 in the decomposition) is the dominant single-stage failure mode — i.e., it contributes more to total joint-failure probability than any of the other four stages.** Reasoning: eversion at the required scale (tens of metres of fabric structure) has zero flight heritage; the other four stages have at least some analog precedent (rendezvous, envelopment, cinch, decel). Falsified if variance-based sensitivity decomposition over the five-stage product shows another stage with a larger single-stage failure-rate share — in which case the engineering-risk priority for the everting architecture shifts to that other stage. Sub-question: does eversion-kinematics failure-rate scale sub-linearly, linearly, or super-linearly with chunk size? Sub-linear would favour the everting architecture at large chunks; super-linear would retire it.

## Fidelity stack

Per wondering finding: hybrid is the only defensible stack. Three tiers:

**Tier 0 — closed-form sanity check.** The existing audit_capture_efficiency sweep at 25 percent / 50 percent / 75 percent / 100 percent multiplier of anchor. Already done. Output is the 4.3 / 19.7 / 33.1 / 47.1 tonne delivery cliff.

**Tier 0.5 — spin-rate prior refinement from Cassini data.** Per the discussion logged 2026-05-26: the published space-robotics literature reports target spin rate as the dominant sensitivity, and the H2 hypothesis bets on the same for ICEBERG. But the *current* spin-rate prior in the table below is a log-uniform [0.01, 1.0] revolutions per minute bracket anchored against **asteroid** spin distributions, not ring-chunk-specific observation. Ring chunks live in a different environment — tidal forces from Saturn, frequent low-velocity collisions with neighboring particles, gravitational stirring from shepherding moons (Pan, Daphnis, Mimas, etc.). The spin distribution could plausibly be much slower (collisional damping) or much faster (recent collision spinup) than the asteroid analog. Tightening this prior by an order of magnitude can change which architecture wins: slow-spin prior favors harpoon (matches easily), fast-spin prior favors everting sleeve (compliance absorbs angular momentum).

Sub-tasks for Tier 0.5:
1. Survey Cassini infrared / thermal-emission data for ring-particle rotation signatures (Spilker et al. CIRS papers; Morishima et al. 2010-2017 thermal modeling; Tiscareno et al. on "propeller" features — propeller hosts have known rotation states).
2. Survey N-body ring-dynamics literature for predicted collisional spin-damping timescales at B-ring densities (Cuzzi, Schmidt, Salo, Spahn group output).
3. If observational data exists for chunks at the meter-to-decameter target scale: build an empirical posterior. If it does not exist: build a theoretical prior from collision-frequency × momentum-transfer arguments, with explicit "no direct observation" disclosure.
4. Output: revised spin-rate prior table — point estimate, 90 percent credible interval, anchor citation per architecture-relevant chunk-size band.

Budget: this is a literature-review and BOE-arithmetic sub-task, 2-4 hours of effort, no Monte Carlo. Output is a markdown memo `tier_0_5_spin_prior.md` in this round's directory plus the revised priors table that Tier 1 inherits.

**Tier 1 — screening Monte Carlo (Morris elementary effects).** Eight candidate uncertainty axes (chunk mass, spin rate, surface friction, approach velocity, sensor noise, contact geometry, catcher compliance, controller delay). Morris design at r=10 trajectories: approximately 90 runs total. Per-run cost on contact-engine model: 1-5 wall-seconds on one CPU core. **Total: under one hour on MacBook Pro.** Output: ranking of the eight axes by elementary-effect mean and standard deviation. Drops axes whose elementary effects are negligible.

**Tier 2 — refinement Monte Carlo (Polynomial Chaos Expansion on surviving axes).** Build a PCE surrogate from approximately 500 carefully chosen runs over the surviving 4-5 axes. Output: total-order sensitivity indices analytically. Per-run cost identical to Tier 1; total approximately 30-60 minutes MacBook.

**Tier 3 — defensible posterior (direct contact-fidelity).** At the operating point identified by Tier 1+2, run 1200 contact-fidelity Bernoulli trials for ±0.02 half-width 95 percent confidence on the binomial capture probability. Per-run cost as above; total approximately 1-2 hours MacBook for a single operating point, or overnight if multiple operating points are needed (e.g., one per architecture-of-record).

**Budget headroom.** If H4 surfaces an engine-choice problem, double the Tier 3 budget for cross-engine A/B. If the contact transient turns out to be more expensive than 5 seconds per run, escalate to a 32-core cloud VM — published precedent is a few dollars per defensible posterior.

## Tooling

**Inner core (contact + friction):** MuJoCo as primary candidate (Apache-2, DeepMind, fastest, widest published precedent in space-robotics Monte Carlo per wondering finding). Drake as cross-check (rigorous Newton solver on complementarity; slower but stronger correctness story) — used only if H4 cross-engine test is warranted.

**Outer loop (orbit + GNC):** Basilisk's existing `mission_graph` framework, extended with a `capture_event` callable that hands off to MuJoCo at first contact and resumes after grapple-established. Basilisk's MJScene module exists for this bridge but is flagged [BETA]; if MJScene is unreliable, fall back to manual state hand-off at the contact instant.

**Sampling library:** SALib (Python, Apache-2) for Morris + variance-based sensitivity + PCE design. Already pip-installable; no Basilisk-venv collision risk.

**Pre-registration + papermill pinning:** match the campaign methodology — STUDY.md with H1..H6 written before any runs, papermill-pinned notebook for each tier, FINDINGS.md as the canonical output document with a variance-log entry against the matrix.

## Uncertainty axes — initial priors

Inputs need prior distributions before Tier 1 runs. Initial cuts (refined during the round):

| Axis | Prior | Rationale / source |
|---|---|---|
| Chunk mass | Power-law over [1, 200] tonnes; index q ≈ 3 | Cuzzi 2010 / Tiscareno 2010 B-ring size distribution (belief 1985a336) |
| Spin rate | **PROVISIONAL** — Log-uniform [0.01, 1.0] revolutions / minute, asteroid analog | Replaced by Tier 0.5 output before Tier 1 begins. H2 (spin-rate dominance) cannot be honestly tested against a prior anchored on the wrong population; the ring-environment-specific prior is load-bearing on the round's interpretability. |
| Surface friction | Uniform [0.05, 0.40] | Ice-on-Kevlar / ice-on-aerogel published range |
| Approach velocity | Normal, mean 1 cm/s, sd 3 mm/s (radial-offset / Hill-frame analysis per belief 1d248028) | Earlier 360× drift-velocity error retired |
| Sensor noise | Normal, sd from published rendezvous-radar bracket | Per Chen 2024 |
| Contact geometry | Discrete cases (edge / face / vertex) with weights | Per published grasp-stability work |
| Catcher compliance | Uniform over plausible bag stiffness | Wide prior — second-order per literature |
| Controller delay | Uniform [10, 100] ms | Per published GNC anchor |
| **Eversion-completion rate** (everting-sleeve only) | Bernoulli prior, uniform over [0.5, 0.95] | No flight precedent at 200-tonne-class deployable scale; prior is intentionally wide and pessimistic-leaning. Single biggest contributor to H8 — wide prior makes H8 falsification more demanding. |
| **Eversion-asymmetry-induced misalignment angle** (everting-sleeve only) | Normal, sd 5 degrees, truncated at 30 degrees | Asymmetric eversion shifts centre of mass; couples to attitude excursion. Wider sd if vehicle reaction-wheel authority is low. |

Priors are intentionally wide for Tier 1. Tier 2 + 3 tightens them on the surviving axes.

## Deliverables of THIS round

1. This SCOPE.md (you are reading it).
2. STUDY.md with H1..H8 pre-registered, falsifiers explicit, priors locked.
3. `tier_0_5_spin_prior.md` — Cassini-anchored ring-chunk spin-rate prior. Literature survey + theoretical bracket + revised prior table. **Blocks Tier 1.**
4. `simulator.py` — MuJoCo capture-event model with Basilisk hand-off. Three architecture variants share the orbital/GNC outer loop; differ in contact + deployment models.
5. `tier1_morris.ipynb` — papermill-pinned, ~90 runs per architecture (~270 total), axis ranking.
6. `tier2_pce.ipynb` — papermill-pinned, ~500 runs per architecture (~1500 total), total-order sensitivity indices on survivors.
7. `tier3_posterior.ipynb` — papermill-pinned, ~1200 runs per architecture (~3600 total), defensible binomial posterior with credible interval per architecture.
8. `comparison_memo.md` — three-way head-to-head: posterior medians + credible intervals, sensitivity-index cross-architecture comparison, recommendation on architecture-of-record for the matrix.
9. FINDINGS.md — verdict on H1..H8, variance-log entry, recommendations for the matrix amendment.
10. If H6 falsifies (all three architectures below 0.64): matrix-amendment specification that cascades through L0-04 / decision points #1, #2, #3 / open SCOPEs queue.
11. If H7 falsifies (everting-sleeve does not transfer): cross-project memo flags that the sleeve application is satellite-specific.

## Out of scope

- Detailed catcher mechanism design (mass, packing, deployment kinematics). This round models a generic catcher with parameterized compliance; detailed design is a follow-on engineering round.
- Ring-traffic survival (B-ring impact probability per pass). Already studied to falsification in phoebe rounds 3-6; this round assumes those constraints and operates within the surviving operating envelope.
- Multi-chunk-per-mission economics. Already falsified by rhea R-heterogeneous-cadence; this round is single-mission-single-capture per fill (or single residence-class-fill for ram-scoop framing).
- Reactor / power-class gating. Out per wondering scope; bet 3 has its own SCOPE'd round.
- Water-electrothermal flight-gap modeling. Out per wondering scope; bet 2 has its own program.

## Predecessor work

- **Locked beliefs:** `31a13abb` (A14 capture efficiency anchor), `c646b3c6` (A4 water content), `650938e3` (A1 plausible-provisional), `c9562697` (L0-04 = 25 t), `5535179f` (three engineering bets).
- **Phantom beliefs from 2026-05-26 wondering** (3 inserted): domain research (published precedent), internal gap analysis (architecture-of-record question), coverage extension (Morris / PCE / variance-based-sensitivity methodology).
- **`R_assumption_audit_2026_05_21/FINDINGS.md`** — established the 0.85 vs 0.46 cliff and the matrix sensitivity at L0-04 = 25 t.
- **`R_assumption_audit_2026_05_21/audit_capture_efficiency_sweep`** — Tier 0 sanity sweep, already complete.
- **`R_conops_chunk_vs_ram_scoop` (titan-2)** — surfaced the ram-scoop reframe; the architecture-of-record question depends on it.
- **phoebe rounds 3-6** — B-ring rendezvous survivability is already falsified; this round assumes the surviving operating envelope.
- **`R_bag_aperture_chunk_joint`, `R_bring_fine_structure_rendezvous`, `R_HE_graze_feasibility`** — bracket the surviving envelope.
- **Phantom beliefs cite:** Chen 2024 (J. Spacecraft & Rockets, tether-net concurrent design optimization); Basilisk MJScene MuJoCo docs; NASA NTRS 20180008686 (Sample Return Systems); Lidec 2023 contact-models comparison (arXiv 2304.06372); Sudret PCE work.

## Project-owner decisions required before run

1. ~~**Architecture-of-record:** single-chunk-harpoon, ram-scoop residence-class, or both (parallel runs).~~ **RESOLVED 2026-05-26: three parallel architectures — single-chunk-harpoon, ram-scoop residence-class, and everting-sleeve active enclosure.**
2. **Ratify or adjust the eight-axis list.** Drop any axes the project owner believes are clearly second-order. Note: contact-geometry priors and catcher-compliance priors will differ across the three architectures (rigid harpoon vs flexible bag vs everting fabric); the round handles this with per-architecture prior tables.
3. **Approve the Tier 3 budget.** Default is ~1200 runs per architecture at one operating point — three architectures × 1200 = ~3600 runs total. If multiple operating points (e.g., demonstrator vs commercial chunk-mass envelope), multiply. Total wall time at default: ~36 hours MacBook, or one cloud-VM evening.
4. **Direction on H6 falsification cascade.** If all three architectures' posterior medians fall below 0.64, what is the next move — retire L0-04, search for a fourth architecture, or terminate the chunk-capture path entirely? Pre-decided guidance saves a round.
5. **Direction on H7 falsification.** If the everting-sleeve transfer falsifies (posterior > 0.10 below the better of the other two), the satellite-capture sleeve work does not generalize to ICEBERG and the mechanism should be retired from ICEBERG planning. Pre-decided guidance on documentation / cross-project memo saves rework.

## Priority

**HIGH.** A14 is the single most load-bearing assumption. The matrix decision state for points #1 (program class), #2 (round-trip ceiling), #3 (chunk-mass cap) all depend on whether L0-04 = 25 t survives the capture-efficiency posterior. Pair-blocked with R-kilopower-scale-up-credibility (bet 3) but otherwise independent of all other queued SCOPEs.

## Suggested worker

Any moon worker comfortable with both physics simulation and Bayesian sensitivity analysis. The round has a hard architecture decision blocker (project owner) before runs start, but the technical work after that is mechanical: write the priors, run Morris, run PCE, run the binomial posterior, write the verdict.
