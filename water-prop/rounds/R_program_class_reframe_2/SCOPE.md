# R-program-class-reframe-2 — does any 14-yr mission close given the new engineering constraints?

**Status:** scope, pre-study. Authored by Saturn (orchestrator), 2026-05-18 latest+8, immediately after the matrix amendment integrating phoebe rounds 3-6 (`b5c5d61`).

**Context.** Phoebe rounds 3-6 close both load-bearing engineering questions on the held chunk-rendezvous architecture (axis 19) and recommend retiring it as venture-class with very high confidence. The matrix's latest+7 framing — "technology-demonstrator is the only honest reading at flown-anchored specific power; regulated-utility-class requires both engineering closures AND a reactor program targeting ≥ 5 W/kg + ≥ 10-year flight life that does not exist" — is now even tighter because the engineering closures themselves are denied. Phoebe explicitly named this round (R-program-class-reframe-2) as the second of two next critical-path follow-ons, framing it as: **"does any 14-yr mission close given engineering constraints?"**

**This round is paired with R-mission-architecture-pivot-survey** but addresses a distinct question. The pivot-survey asks "which alternative architectures may restore a surviving cell?" This round asks "even if some pivot survives the survey at sketch level, does any concept-of-operations meet L0-05's 15-year ceiling under the engineering constraints phoebe found?" The two together close the loop on the program-class decision (matrix decision point #1).

---

## Distinction from prior reframe rounds

Two prior rounds in the campaign anchored on program-class:

- **rhea R-variant-B-recovery-paths-economic (`5fe5dd5`)** — surfaced the venture-class vs regulated-utility-vs-technology-demonstrator trichotomy. Pre-phoebe; assumed at least one engineering closure was reachable.
- **titan-2 R-HE-graze-feasibility (`b2e7a35`)** — closed the high-eccentric-graze multi-chunk-aggregation rescue path, eliminating venture-class. Pre-phoebe.

Both of these rounds left "regulated-utility-class with waivers" and "technology-demonstrator" as the surviving framings. Phoebe rounds 3-6 do not directly falsify those framings, but they collapse the engineering basis under which either can deliver any non-zero mass. The reframe-2 question is whether a 14-yr mission exists at all under the new engineering constraints — not whether the program is regulated-utility vs technology-demonstrator.

**Reframe-2 expressly does not assume any of the pivot-survey candidates is viable.** It runs three scenario tracks in parallel:

1. **Hold-and-restate.** Accept phoebe's retirement of the held chunk-rendezvous architecture. Test whether any one of the four pivot-survey candidates, even at sketch-level viability, meets L0-05 strict 15-yr under reactor-program priors.
2. **Reject-and-retry.** Reject one or both phoebe verdicts as too pessimistic. Test which residual within-chunk-rendezvous rescues (R-deployable-drag-skirt, R-bag-armour-multi-layer-deep, R-bring-fine-structure-deep, R-lower-inclination-arrival) could restore engineering closure AND whether the rescued architecture meets L0-05.
3. **Demonstrator-only.** Restate as technology-demonstrator class explicitly (REQUIREMENTS.md §7.5). What does a demonstrator-class mission deliver, what does it cost, what risk does it retire, and does it open any credible bridge to commercial-class?

The round produces a verdict per track plus a combined verdict on whether any 14-yr mission closes.

---

## Question this round answers

For each of three scenario tracks, **does at least one 14-yr mission concept-of-operations exist** that:

(a) meets L0-05 round-trip ≤ 15 yr,
(b) meets L0-04 mission-class delivered-mass floor (commercial-class undefined; demonstrator-class "any non-zero" per §7.5),
(c) survives engineering constraints surfaced through latest+8 (phoebe's three independent failure modes + B-ring rendezvous + KRUSTY-anchored specific power + 8-12-yr reactor burn lifetime),
(d) is credible under R-power-base-rate-style program-risk priors (locked aelfrice findings 2-4),
(e) closes L0-13 NPV-positive at appropriate cost-of-capital for the track (commercial / regulated-utility / demonstrator)?

Aggregate verdict: **how many of the three tracks produce ≥ 1 closing 14-yr mission?** If zero, the program-class commitment forces to "shelve until reactor-program landscape changes." If one or more, the project-owner has a substantive decision to make on track selection.

---

## Pre-registered hypotheses (numeric ranges + falsification bands)

| # | Hypothesis | Predicted range | Falsification band |
|---|---|---|---|
| H1 | **Hold-and-restate, catcher-at-Saturn.** The catcher-at-Saturn pivot (pivot-survey candidate #1) meets L0-05 strict 15-yr because the return-tug carries no inbound-cruise propellant for the harvest leg; cruise time is the matrix's pre-phoebe Variant-B 12.5-13.5 yr range. Per-mission delivered mass ≥ 100 t at the commercial floor. Probability ≥ 30% that the catcher-at-Saturn concept-of-operations meets L0-05 + L0-04 commercial floor + L0-13 NPV-positive at sov rate. | catcher-at-Saturn closes L0-05 strict at probability 0.20-0.40 | H1 falsified if either (a) round-trip > 15 yr under any cardinal cell (catcher closes at probability ≤ 10%), OR (b) catcher meets all L0s at probability ≥ 60% (sketch was already that strong, deep round is moot) |
| H2 | **Hold-and-restate, alternative-source Mimas.** Mimas-surface harvest avoids B-ring transit but per-mission delivered mass is constrained to ≤ 50 t by 500 kWe Variant-B power floor (lower than B-ring chunk-rendezvous would have been). Probability ≥ 40% that Mimas meets L0-05 strict + per-mission delivered ≥ 10 t at demonstrator-class floor; probability ≤ 10% that it meets commercial-class floor. | demonstrator-floor closure: probability 0.30-0.50; commercial-floor closure: probability ≤ 0.10 | H2 falsified if (a) Mimas closes commercial-floor at probability ≥ 30%, OR (b) demonstrator-floor closure probability ≤ 15% (Mimas is dead even for demonstrator) |
| H3 | **Reject-and-retry, deployable drag-skirt rescue.** R-deployable-drag-skirt is phoebe-named as the only architecturally-credible β-reduction lever for atmospheric capture. **If it closes** at β reduction factor ≥ 5× (β from ~5000 to ≤ 1000 kg/m²), AND aerocapture re-opens at the rescued β, AND specific-power assumption is held above 5 W/kg (rejected from KRUSTY anchor), then the held chunk-rendezvous architecture has a residual closing cell. Probability of the joint condition (drag-skirt closure × axis-06 rejected anchor × axis-12 rejected anchor) is < 5% under R-power-base-rate-style program-risk priors. | joint-condition probability 0.01-0.05 | H3 falsified if joint-condition probability ≥ 15% (the rejection-track has more credibility than phoebe's verdict implies) |
| H4 | **Demonstrator-only, single-mission technology-demonstrator.** A single demonstrator-class mission (1-10 t delivered, no commercial customer, ~10 yr round-trip) is engineering-feasible at 500 kWe Variant-B power floor with a Mimas-surface or B-ring-outermost-edge source. Cost is in the $5-15B range (per-mission marginal under sunk-architecture-development assumption). The demonstrator does NOT retire commercial-class risk on its own because the failure modes phoebe identified are population-density and geometry, not first-flight teething problems. Probability ≥ 80% that a demonstrator-class mission can be sized and budgeted; probability ≤ 20% that demonstrator-class outcomes meaningfully unlock a commercial-class bridge. | demonstrator sizeable: 0.75-0.90; commercial-class bridge: 0.10-0.25 | H4 falsified if (a) demonstrator un-sizeable (probability ≤ 50%) at < $20B per-mission, OR (b) demonstrator bridges to commercial at probability ≥ 50% (demonstrator already substantively retires commercial risk, which would be surprising) |
| H5 | **Aggregate across all three tracks.** At least one of the three tracks produces ≥ 1 closing 14-yr mission concept-of-operations. Specifically: hold-and-restate produces 0-1 closures (most likely catcher); reject-and-retry produces 0 closures (joint-condition probability is too low); demonstrator-only produces 1 closure (demonstrator-class is engineering-feasible at any source). Expected aggregate: **1-2 closing 14-yr mission concepts** across the three tracks. | aggregate closures: 1-2 | H5 falsified if aggregate ≥ 3 (too many surviving paths, suggests pre-registration is too permissive) OR = 0 (program-class forces to "shelve") |
| H6 | **Program-class decision implication.** If aggregate ≥ 1 closure, the program-class decision is between (a) commercial-class via catcher-at-Saturn or alternative-source pivot, (b) regulated-utility-class via the same pivots with waivers, (c) technology-demonstrator-only as a phased commitment with no commercial-class bridge. If aggregate = 0, the program-class decision is "shelve until reactor-program landscape changes" (matrix decision point #1 forced to a NULL option not previously enumerated). The round should explicitly add the NULL option to decision point #1 if H5 falsifies to zero closures. | decision-frame: 3 substantive options if aggregate ≥ 1; 1 NULL option if aggregate = 0 | falsified if either (a) round produces a 4th substantive option not in the enumeration, OR (b) demonstrator-only is shown to bridge to commercial after all (collapses the trichotomy) |

---

## Method sketch (worker drafts the actual code in `run.py`)

1. **Anchor data inputs from primary text.** Per methodology lesson 9, build inputs from:
   - **phoebe `1623cca` + `abdcd35` + `45869d4` + `8a31ba9`** for engineering-failure-mode definitions (cite specific cell verdicts).
   - **enceladus-r5 `62f7079` + `2d63291` + `12058b5` + `c685c52`** for specific-power × lifetime × aerocapture-credit constraint surface.
   - **titan R-inbound-dv-continuous-thrust + hyperion R-variant-B-impulsive-vs-continuous** for continuous-thrust accounting.
   - **rhea R-megawatt-marvl-radiator + R-architecture-D-L1007-relaxation** for mass and per-mission delivered.
   - **enceladus-r5 R-LEO-water-demand-curve `ed3dd58`** for clearing-price Monte Carlo.
   - **locked aelfrice findings 1-4** for reactor-program priors.

2. **For each scenario track**, define a closure-conjunction:

   - **Hold-and-restate (per pivot-survey candidate).** P(L0-05 met) × P(L0-04 met) × P(L0-13 met) × P(reactor-program available) × P(no axis-06 violation under the candidate's energy requirements). Compute under three priors: optimistic (Variant-B reference), nominal (R-power-base-rate posterior), conservative (locked aelfrice priors).

   - **Reject-and-retry.** P(drag-skirt closes) × P(reject axis-06 anchor justified) × P(reject axis-12 anchor justified) × all the above conjunction terms. Compute joint under three priors as above; flag the rejection-justification probability as load-bearing (phoebe rounds were not flagged as methodologically suspect; rejecting their verdicts is a strong claim).

   - **Demonstrator-only.** P(demonstrator sizeable at < $20B) × P(commercial-class bridge meaningful from demonstrator outcomes). Compute under cost-anchor uplift sensitivity (Starship vs SLS per decision point #4).

3. **Compute aggregate** as union probability that at least one track produces ≥ 1 closure: 1 − ∏ (1 − P_track).

4. **Decision-frame implication.** If P(aggregate) ≥ 0.5, the project-owner has a substantive program-class decision; report the option-by-option closure probabilities. If P(aggregate) < 0.2, the program-class decision should add a NULL option to decision point #1 ("shelve until reactor-program landscape changes") and the round flags this explicitly as a matrix amendment recommendation.

5. **Methodology audits before sweep:**
   - Audit 1: does L0-05 "15 years strict" cover SOI Δv (titan-2 0.8 km/s) + Saturn-side maneuvering + Earth aerocapture + LEO delivery hand-off, or just trans-Saturn-to-Saturn-arrival?
   - Audit 2: does the engineering-failure-mode list have implicit conjunctions (e.g. "B-ring impact-prob" already includes "chunk shatter" risk so they cannot multiply)?
   - Audit 3: does the demonstrator-class cost anchor distinguish between sunk-architecture-development cost and per-mission marginal cost?
   - Audit 4: are pivot-survey candidates already adjudicated by the time this round runs, or does this round have to assume sketch-level viability?

---

## Out-of-scope for this round (declared)

- **Detailed pivot-survey sketches.** Sketch-level viability of each candidate is R-mission-architecture-pivot-survey's job. This round uses the survey's GO/CONDITIONAL/NO-GO verdicts as inputs.
- **Deep R-deployable-drag-skirt physics.** Probability of closure is set externally as a prior; this round does not run the drag-skirt analysis.
- **Detailed program-NPV per pivot.** Per-mission and program-NPV is downstream; this round operates at L0-13 closure-probability level.
- **Project-owner-private decisions.** Capital-structure framing (L0-13 §8 deferred item) and reactor-program path (L0 §8 deferred item) are decision-frame outputs of this round, not pre-supplied inputs.

---

## Dependency on R-mission-architecture-pivot-survey

This round needs the pivot-survey's GO/CONDITIONAL/NO-GO verdicts per candidate to run track 1 (hold-and-restate) cleanly. Three options for sequencing:

1. **Run pivot-survey first; reframe-2 second** (sequential). Cleanest. Reframe-2 inherits the survey's candidate-by-candidate viability.
2. **Run reframe-2 with placeholder priors on pivot viability** (parallel). Reframe-2 uses 50% prior on each pivot's sketch-level viability and produces a sensitivity-analysis table on (P_pivot_viable × P_track_closes). Updated after the survey lands.
3. **Run reframe-2 demonstrator-only first; pivot-dependent later** (split). Demonstrator-only track is self-contained — it does not need the pivot survey. Run that first as an immediate value-delivery; defer hold-and-restate + reject-and-retry tracks until the pivot survey lands.

Project-owner direction sets sequencing. Default is option 1 (sequential) per the matrix's High-leverage open rounds ordering (pivot-survey is #1, reframe-2 is #2).

---

## Methodology lesson dependencies

- **Lesson 1** (pessimistic-prediction default). Apply to each probability anchor — engineer-pessimistic-insufficient pattern holds 13/13 times in the campaign.
- **Lesson 7** (compute under most pessimistic credible anchor first). Locked aelfrice priors are the most pessimistic credible; report results under those first, then sensitivity on more-optimistic priors.
- **Lesson 9** (anchor-from-PRIMARY-text). Every probability anchor in this round must cite a specific commit in the corroborating round, not a downstream summary.
- **Candidate lesson 11** (self-questioning rounds as campaign-default). After this round, if aggregate ≥ 0.5, the deep-track SCOPEs should be authored with built-in self-question on the load-bearing assumptions.

---

## Worker assignment

This SCOPE is a synthesis-and-decision round — Bayesian aggregation under explicit priors. Either a fresh worker or a continuation. Candidates with relevant heritage: rhea (program-class trichotomy origin, R-variant-B-recovery-paths-economic), enceladus-r5 (L0-09/L0-10/L0-13 coordinated decisions), hyperion (R-power-bayesian-update, three-prior bracket).

Expected effort: ~one session with deferred sweep on track 1 if pivot-survey is not yet done; ~two sessions if both pivot-survey and reframe-2 run together. Produces `STUDY.md` pre-registration, `run.py` Bayesian-aggregation logic, `results/per_track.md` per scenario track, `results/closure_verdict.md` aggregate + decision-frame implication.

---

## Matrix axes touched

- Axis 01 (Program class) — directly. Adds NULL option to decision point #1 if aggregate = 0.
- Axis 02 (Surviving cell) — indirectly via per-pivot closure probability.
- Axis 10 (Round-trip ceiling) — directly. The round's L0-05 closure-conjunction is a per-track per-pivot check.
- Axis 17 (Pitch / capital framing) — output. The track selection (commercial / regulated-utility / demonstrator) sets the pitch framing for the next pitch rewrite.
- Axis 16 (Concept-of-operations document) — output. The closing 14-yr mission concept-of-operations (if any) is the target for the titan-2 conops rebuild's next pass.
