# Round — Concept-of-operations: single-chunk vs ram-scoop reframe

**Status:** pre-result.

**Round directory:** `water-prop/rounds/R_conops_chunk_vs_ram_scoop/`.

**Owning session:** titan (re-spawn), branch `iceberg-titan-2`.

**Date:** 2026-05-15.

**Pre-requisite rounds:**
- R-HE-graze-feasibility (commit `b2e7a35` / merged at `266e877`): falsified high-eccentric Saturn-graze chunk capture as soft-capture mode. Relative velocity at periapsis 6.56 kilometres per second; aspirational bag tolerance 64 metres per second. 102× over.
- R-saturn-soi-periapsis-depth (commit `1b1b889`): B-ring crossings at zone-averaged optical depth τ ≈ 2 yield 99% impact probability per crossing at 26.7° inclination. Naive passage is mission-fatal.
- R-bring-fine-structure-rendezvous (commit `201e2c2`): no B-ring sub-feature exists with τ ≤ 0.01 for naive passage. Residence-class architecture (circularise at ~100,000 kilometres, sweep ring material at relative velocity ~10 metres per second) accretes 5,000–230,000 kilograms per second per 100 square metres of bag opening. Cost: ~14.7 kilometres per second Saturn-side round-trip delta-velocity (~30% propellant penalty at megawatt-electric specific impulse 5000 seconds).

---

## Question

The single-chunk abstraction ("harpoon-a-chunk", "iceberg", "single 482-tonne particle") propagates through every load-bearing shared document in the project. The ram-scoop architecture invalidates that abstraction at the operational layer. The mass and composition delivered are the same; the operational picture, structural design, capture-event timeline, mission-success accounting, and language stack are different.

This round answers four questions:

1. **Surface mapping**: where in the shared documents does the single-chunk abstraction appear, and what gets reframed vs what survives intact?
2. **Semantic delta**: what are the substantive (non-cosmetic) differences between single-chunk and ram-scoop concept-of-operations? Identify any place where a sentence's *truth value* changes — not just its wording.
3. **Number-level propagation**: which numbers in the matrix and requirements documents are made wrong by the reframe (e.g., capture-event durations, bag-mouth dimensions, structural-load specifications, mission-success conditional probabilities)?
4. **Integration recommendation**: what is the minimum-edit reframe that preserves the campaign's analytical conclusions while making the documents consistent with the ram-scoop architecture?

The round produces a synthesis brief Saturn (orchestrator) can use to drive the consequent rewrites.

## Pre-registered hypotheses

| ID | Hypothesis | Predicted | Falsification |
|---|---|---|---|
| H1 | The single-chunk language is **pervasive** across all seven shared documents. Total instances of "chunk" and "iceberg" terminology exceeds 300, with the heaviest concentration in concept-of-operations and pitch. | ≥ 300 instances across the seven shared docs | falsified if < 200 instances OR if heavily concentrated in only 1–2 docs |
| H2 | At least 80% of single-chunk references are **cosmetic** — they describe the deliverable (482 tonnes of water ice in low-Earth orbit) rather than the operational mechanism. These can be left as-is or trivially reworded. | ≥ 80% cosmetic | falsified if < 60% cosmetic; that would mean the chunk abstraction is operationally load-bearing in the docs rather than just rhetorically pervasive |
| H3 | A small subset of references — predicted ≤ 30 — encode **operationally load-bearing assumptions** that are now wrong: capture-event duration (modelled as seconds-to-minutes of "rendezvous" rather than seconds of "sweep"), structural loads (point-loaded harpoon vs distributed ram drag), mission-success conditional probabilities (chunk-mass uncertainty becomes irrelevant; ring-material-density variability replaces it), bag-mouth geometry (closed pouch vs open scoop), residence-time-in-Saturn-orbit duration (single rendezvous opportunity vs sustained orbital match). | ≤ 30 load-bearing operational references | falsified if > 50 such references — indicates the reframe is more invasive than a documentation patch |
| H4 | The matrix's delivered-fraction numbers **are not changed** by the reframe. Delivered fraction is mass-out / mass-launched; ram-scoop changes the mass-into-bag mechanism but not the mass-out / mass-launched ratio (the propellant is sized to return the same payload). | matrix delivered-fraction rows unchanged | falsified if any matrix row's delivered-fraction shifts by > 1 percentage point |
| H5 | The Saturn-side round-trip delta-velocity, however, **does** shift in the matrix. Current matrix lines book ~1–5 kilometres per second for Saturn capture; residence-class architecture needs ~14.7 kilometres per second round-trip. At megawatt-electric specific impulse 5000 seconds, this is a ~30% propellant penalty per mission, which propagates into the matrix's mass-out / mass-launched ratio via Tsiolkovsky. | matrix Saturn-side delta-velocity row needs upward revision of ~10–13 kilometres per second; mass-out / mass-launched penalty ~30% | falsified if matrix's current Saturn-capture delta-velocity already books ≥ 10 kilometres per second, OR if propellant penalty under recomputation is < 15% or > 50% |
| H6 | The pitch document's economic conclusions — regulated-utility-class, sovereign + strategic-corporate + infrastructure-fund capital partners — are **unaffected** by the reframe. Economics is set by mass-out / mass-launched ratio × mass-out unit price × cadence, and only the first changes (slightly worse per H5), within the already-wide regulated-utility envelope. | pitch's regulated-utility conclusion unchanged; demand-side, pricing, and partner-profile sections do not need rewriting | falsified if H5's propellant penalty drops marginal internal-rate-of-return by > 2 percentage points (which would push some economic cases below regulated-utility threshold) |
| H7 | The bag-engineering document needs **the most substantive rewrite** of any shared document. It currently specifies a soft-capture closed-pouch architecture optimised for one large chunk at ≤ 64 metres per second relative velocity. Ram-scoop wants an open scoop sustaining ~1 meganewton of accretion drag during a seconds-long sweep, plus tolerance for ~30 occasional metre-class particle impacts at 10 metres per second. | bag-engineering doc needs full rewrite of structural sections; cosmetic-only for material-selection sections | falsified if bag-engineering doc already implicitly supports an open-scoop geometry (which would mean less rewrite than predicted) |

## Method

### Body 1 — Inventory pass

For each of the seven shared documents, classify every "chunk" / "iceberg" / "harpoon" / "rendezvous" / "soft-capture" instance into one of four bins:

- **(C) Cosmetic**: describes the deliverable, not the mechanism. Example: "ICEBERG returns 482 tonnes of water ice per mission". Stays as-is.
- **(R) Rewordable**: describes the mechanism using single-chunk language but the underlying meaning survives a substitution. Example: "rendezvous with B-ring chunk" → "rendezvous with B-ring material". Trivial edit.
- **(S) Semantically wrong**: states something that becomes false under ram-scoop. Example: "capture event duration: minutes to hours of station-keeping with the chunk" — false; ram-scoop sweep is seconds, no station-keeping with a coherent body. Substantive rewrite required.
- **(N) Numerically wrong**: a number that becomes invalid. Example: "Saturn-side delta-velocity budget: 3 kilometres per second" — wrong by an order of magnitude. Number change required.

Sample-pull a representative section from each document; do not exhaustively rewrite all ~360 instances. Tabulate bin counts by document.

### Body 2 — Semantic-delta map

For each (S) bin instance found in Body 1, write a one-line "before / after" pair documenting the truth-value change. Aim for a master list of ≤ 30 such pairs.

### Body 3 — Number-level audit

Identify the matrix rows and requirements lines whose numbers are made wrong by the reframe. Recompute under ram-scoop assumptions:

- Saturn-side delta-velocity (matrix line, current ~1–5 kilometres per second → revised ~14.7 kilometres per second).
- Per-mission propellant mass (recomputed via Tsiolkovsky at specific impulse 5000 seconds and dry mass ~200 tonnes).
- Mass-out / mass-launched ratio (recomputed under new propellant load).
- Capture-event duration (modelled as seconds in concept-of-operations; was minutes-to-hours).
- Bag structural specifications (drag force ~1 meganewton, vs prior point-load harpoon spec).
- Mission-success accounting: failure modes shift. The chunk-mass-uncertainty failure mode (will-we-find-a-482-tonne-chunk?) is retired; new failure modes (will-the-bag-survive-1-meganewton-of-drag?, will-the-spacecraft-survive-30-large-impacts?) take its place. These are different probability distributions and propagate into L0-09 / L0-10 mission-success budgets differently.

### Body 4 — Integration recommendation

Produce a single-page integration brief for Saturn covering:

- Document-by-document edit-scope estimate (lines changed, sections rewritten, sections retired).
- Numerical updates to the matrix and requirements (specific row-by-row).
- Recommended sequencing (which doc gets edited first; what triggers the next).
- Open follow-on rounds that the reframe creates (e.g., R-residence-bag-structural is now critical-path; chunk-mass-uncertainty rounds become irrelevant; R-bring-particle-composition rises in priority).
- Pitch-language guidance: how to talk about the architecture publicly. "Ram-scoop" / "ring-material scoop" / "B-ring accretion bag" — pick a phrase and stick to it.

### Validity caveats

- This is a synthesis round, not a physics round. No new computation beyond Tsiolkovsky for the propellant-load update and matrix consistency checks. The physics is settled by the three pre-requisite rounds.
- The bin classification (C / R / S / N) is somewhat subjective at the boundary between R and S. Borderline cases go to S (conservative — over-flags rather than under-flags rewrite scope).
- Workers do not edit shared documents per `PARALLEL-SESSIONS.md`. The output is a brief for Saturn (orchestrator) to act on, not a set of patches.
- The reframe assumes R-bring-fine-structure-rendezvous's residence-class architecture closes structurally. If R-residence-bag-structural (queued, not yet run) falsifies the ram-scoop, this brief becomes a worked example of the alternative architecture and the campaign reverts to the prior chunk picture (or a third architecture, if one emerges). The brief should be written to be reversible.

## Results

Full inventory and number-level audit in `results/inventory.md`. Headline verdicts:

| ID | Prediction | Verdict |
|---|---|---|
| H1 | ≥ 300 instances of chunk/iceberg language | **held** — 360 instances across seven shared documents |
| H2 | ≥ 80% cosmetic | **partially held** — 55% pure cosmetic, 78% cosmetic + trivially rewordable |
| H3 | ≤ 30 load-bearing operational references | **partially held** — ~36 instances, within 20% of prediction; concentrated in `ICEBERG-bag-engineering.md` and `ICEBERG-conops.md` |
| H4 | Matrix delivered-fraction unchanged | **falsified — load-bearing** — under continuous-thrust accounting and chunk-fed exit-Δv, delivered fraction drops from 17% (Option A) to ~3.5% for the 500-kilowatt-electric surviving cell |
| H5 | Saturn-side Δv shifts +10–13 km/s; ~30% propellant penalty at megawatt specific impulse 5000 s | **held with caveat** — penalty is multiplicatively worse under continuous-thrust accounting because the 7.4 km/s exit burn is chunk-fed and stacks with the existing 24.7 km/s inbound continuous-thrust delta-velocity |
| H6 | Pitch's regulated-utility conclusion unchanged | **at risk — conditional** — if R-residence-exit-maneuver does not find a workable exit-Δv path, the cell fails closure entirely and the pitch needs more than posture-revision |
| H7 | Bag-engineering needs most substantive rewrite | **held** — 40% S-bin share, highest of any document. §0.1, §3, §5.4 all sized for single-chunk soft-capture; ram-scoop wants open-mouth scoop sustaining ~1 meganewton drag over a 5-second sweep |

**The load-bearing finding:** R-bring-fine-structure-rendezvous computed the residence-class Saturn-side delta-velocity at ~14.7 km/s round-trip *under impulsive-equivalent accounting*. Under continuous-thrust electric accounting (consistent with how Option A's 17% delivered fraction was derived), the chunk-fed exit segment from B-ring residence orbit must be added to the existing inbound continuous-thrust delta-velocity:

- Chunk-fed Δv = 7.4 (residence-out continuous-thrust) + 24.7 (interplanetary inbound continuous-thrust) = **32.1 km/s**.
- At megawatt-electric specific impulse 5000 s, mass ratio = 1.93.
- At 200-tonne dry + 200-tonne collected ring material, delivered fraction = **3.5%**.
- **A 5× drop from Option A's 17%; an 18× drop from the matrix's original 64%.**

Chemical-kick exit at the 7.4 km/s residence-out leg does not close (mass ratio 5.34 at specific impulse 450 s requires 326 t propellant on a 400 t wet mass). Spiral-out exit under low-thrust electric without chunk-feeding requires ~20 years just to clear B-ring optical depth — L0-05 fail. Specific-impulse uplift to ~7000 s recovers delivered fraction to ~20% but is beyond near-term thrust envelope at megawatt scale.

## Reading

Three findings.

1. **R-bring-fine-structure-rendezvous opened the architecture-rescue door, but the exit-Δv problem may slam it shut again under the correct accounting regime.** The ram-scoop is operationally feasible per the prior round's accretion-rate calculation (5,000–230,000 kg/s of bulk ring material at 100 m² × 10 m/s), but the propellant cost of *exiting* the residence orbit at chunk-fed specific impulse and continuous-thrust accounting consumes ~half the collected mass. The architecture's claim of "free chunk capture" is wrong at the order-of-magnitude level once exit-Δv is accounted honestly.

2. **The document-rewrite scope is medium, not large.** 78% of single-chunk references are cosmetic or trivially rewordable. The genuinely-load-bearing rewrites (~36 instances) cluster in bag-engineering and concept-of-operations. The pitch and demand documents are largely insulated — they describe deliverables and pricing, not mechanism.

3. **The methodology lesson from titan's prior session — "compute the product of central estimates under the most pessimistic credible anchor first" — is reaffirmed.** R-bring-fine-structure-rendezvous applied impulsive-equivalent accounting to the residence-class delta-velocity, while the rest of the campaign has shifted to continuous-thrust accounting. Mixing accounting regimes obscured the cell-closure problem; applying the conservative anchor (continuous-thrust) consistently surfaces it.

## Cross-learning

1. **Recommended integration path for Saturn: Path A — defer doc-rewrite pending R-residence-exit-maneuver.** Rewriting ~108 lines across seven docs to reflect an architecture that may not close is wasted effort. R-residence-exit-maneuver should run before any Path B/C action.

2. **R-residence-exit-maneuver is a new critical-path round.** It addresses: under what specific-impulse / thrust / propellant-source combination does the residence-class exit Δv close? Is there a hybrid (chemical chunk-feed for the exit kick + electric for interplanetary inbound) that recovers delivered fraction to ≥ 10%? Are there alternative residence-class architectures (e.g., partial-eccentric residence; resonance-pumping exit through Mimas / Enceladus gravity assists; ring-edge graze at lower τ) that reduce exit-Δv below 7.4 km/s? This round should run before bag-structural; if exit-Δv doesn't close, bag-structural is moot.

3. **R-residence-bag-structural is still critical-path but second priority now.** If exit-Δv kills the architecture, bag-structural never happens. If exit-Δv closes, bag-structural is the next falsification gate.

4. **The HE-graze multi-chunk row in the matrix is double-falsified.** Once by R-HE-graze-feasibility (commit `266e877`); now again by the ram-scoop pivot, which makes the multi-chunk concept itself architecturally obsolete (you don't "capture multiple chunks"; you do one residence-class sweep that aggregates a continuous mass of ring material). The matrix's "Multi-chunk per mission" row should be retired in the next orchestrator integration pass regardless of which architecture survives.

5. **The "chunk-as-heat-shield" rescue path in the matrix is at risk under ram-scoop.** A coherent ice block can plausibly act as ablative thermal mass during Earth aerocapture. A fabric-bagged slurry of cm-to-metre ring particles is a fundamentally different thermal-protection problem. If R-residence-exit-maneuver closes the architecture and ram-scoop becomes the operational picture, R-chunk-as-heat-shield-revisit needs to re-validate under a slurry payload, not a coherent block.

## Open threads for follow-on rounds (orchestrator-routed, not Titan-owned)

| Round | Priority | Notes |
|---|---|---|
| **R-residence-exit-maneuver** | **critical-path (new)** | Under what propulsion configuration does the residence-class exit Δv close? Chemical kick (doesn't close at face value), electric chunk-fed (3.5% delivered, sub-sovereign-bond), hybrid (TBD), or alternative exit architecture (resonance-pumping, ring-edge graze)? This is the architecture-survival round. Should run before any doc-rewrite. |
| **R-residence-bag-structural** | **critical-path (queued by R-bring-fine-structure-rendezvous)** | ~1 MN of accretion drag + ~30 occasional metre-class chunk impacts during a 5-second sweep — does the bag survive? Mooted if R-residence-exit-maneuver doesn't close. |
| R-residence-tour-design | moderate | The 7.4 km/s spiral from r_a = Titan radius to circular at 100,000 km — does the megawatt-electric thrust profile / specific impulse / mission duration close? |
| R-bring-particle-composition | low | Cassini RPX says > 99% water ice by mass; trace silicates ~1%, organics < 0.1%. Confirm for downstream electrolysis. |
| R-chunk-as-heat-shield-revisit-under-slurry | low (conditional) | Run only if R-residence-exit-maneuver closes. Coherent-ice heat-shield analysis does not transfer to fabric-bagged slurry. |
| R-saturn-side-residence-radiation | low | Months-long dwell at 100,000 km circular orbit incurs more radiation dose than Cassini's eccentric tour. Spacecraft electronics survival. |

**Doc-rewrite scope (for Path B/C, if R-residence-exit-maneuver clears the architecture):**

| Document | Estimated rewrite effort | Notes |
|---|---|---|
| ICEBERG-bag-engineering.md | full §0.1, §3, §5.4, §8 rewrite (~6 hours of focused work) | Highest-load-bearing; §6 (η_c convention) survives; §4 (permeability) survives |
| ICEBERG-conops.md | Phase 5–6 rewrite (~3 hours); cosmetic touch-up elsewhere (~1 hour) | Phase 7+ (inbound cruise, aerocapture, delivery) unchanged |
| ARCHITECTURE-DECISION-MATRIX.md | Saturn-side Δv row update, ram-scoop cell addition, multi-chunk row retirement, chunk-as-heat-shield row re-conditioning (~2 hours) | |
| REQUIREMENTS-L1.md | L1-001, L1-007, L1-018, L1-028 rewrites (~1 hour) | |
| ICEBERG-pitch.md | optional posture-revision (~1 hour) | Mostly cosmetic; can be deferred |
| ICEBERG-demand.md | no rewrite needed | Mechanism-independent |
| REQUIREMENTS.md | no rewrite needed | Level-0 deliverable-framed |

Total Path C effort: ~13 hours of focused Saturn work. **Not worth committing until R-residence-exit-maneuver clears the architecture.**
