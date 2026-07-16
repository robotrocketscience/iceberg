# R&D Campaign Protocol — water-prop

Adapted from the aelfrice project's internal experiment conventions (CONVENTIONS.md). That protocol was forged for retrieval/ML experiments over a synthetic belief-graph corpus. The shape (numbered rounds, pre-registered numeric hypotheses, mandatory Revisit, drops as first-class outputs, pivots explicit and named) transfers cleanly. The domain specifics (deterministic seeded harness, sub-10s wall clock, real-corpus survey, public-safe spec to `aelfrice/docs/specs/`) don't and are replaced below.

Read the upstream CONVENTIONS.md for the full theory. This doc records only what's adapted, with reasons.

---

## The inner loop (unchanged)

Same 5-section round template:

```
### R<N> — <one-line title>

**Hypothesis (H<N>):** <falsifiable prediction with numeric ranges, written
BEFORE the run>

**Test:** <what we did; reference to rounds/R<N>/run.py>

**Result:**
| metric | predicted | measured | held? |
| --- | --- | --- | --- |

**Reading.** <interpretation>

**Revisit.** <did the prediction hold? if wrong, why? mandatory>

**Cross-learning.** <forward/backward references to other rounds; "positive
for R<M>: adopt X"; "negative for R<K>: drop Y"; "methodology issue flagged
for R<L>">
```

The Revisit clause remains the load-bearing piece. Pre-registration without Revisit is decoration.

Three-bucket taxonomy unchanged: **adopt** / **drop (honest negative)** / **defer** (with retest spec or out-of-scope-after-pivot note).

Pivots and bug-catch protocol unchanged.

---

## Deviation 1: Vocabulary

- **Round** (R0, R1, R1b for retests) — protocol unit; one hypothesis, one test, one result. Same as CONVENTIONS.
- **Study** — abandoned. The upstream aelfrice experiment protocol uses `run_R<N>_<slug>.py` script + per-round result JSON. I'd been using `studies/S01_*`; renaming to `rounds/R<N>_*` to align. The S01 → R0 rename is a one-time renumbering, not a retroactive protocol claim — S01 was run *before* this protocol was adopted; documenting as such in its STUDY.md.
- **Stage** (new term) — coarse phase of the campaign, owning multiple rounds. `docs/R1-landscape.md` and `docs/R2-deepdive.md` are *stage writeups*, not rounds in the protocol sense. They came before the protocol was adopted and are kept as pre-protocol scoping work. Going forward, stage = "round writeup index"; rounds nest under stages.

## Deviation 2: Deterministic harness

CONVENTIONS §16 demands `seed=0`, deterministic, sub-10s wall clock, byte-for-byte reproducible from JSON. Designed for ML metrics over synthetic corpora.

For physics simulation:
- **Deterministic given input parameters**: yes. No random seeds unless a round explicitly does Monte Carlo (and then the seed is in the round's run.py + result CSV).
- **Sub-10s wall clock**: relaxed. Cantera sweeps run ~30s; future trajectory integration may run minutes; FEA-style models will run longer. Each round's `STUDY.md` documents *expected runtime* and *what the slow step is*.
- **Reproducible from result file**: yes. Result CSVs / JSONs in `rounds/R<N>_*/results/` capture full inputs alongside outputs. Re-running `run.py` produces identical numbers.

## Deviation 3: Real-corpus prereq survey → flight-heritage survey

CONVENTIONS §11 asks whether the production belief corpus has the inputs the mechanism needs.

Our equivalent: **does the candidate propulsion tech have flight heritage, vendor data, or laboratory measurements we can pull?** If a round concludes "water-ion at 2000 s Isp works," before the campaign verdict the relevant flight-heritage row must say one of:
- **HERITAGE-AVAILABLE**: at least one publicly disclosed flight or qualified ground demo at adjacent operating conditions, with citation. (Treat ground demos as adjacent only if T/P/duration are within 2× of the campaign operating point.)
- **HERITAGE-ADJACENT**: heritage exists for a similar tech (e.g., Xe-ion for water-ion), with explicit derate factors documented.
- **HERITAGE-NONE**: no publicly available data within 2× of the operating point. Tech is research-grade; downstream rounds must include redundancy or risk register entries.

The flight-heritage survey lives in `docs/HERITAGE.md` and is updated each round that touches a new tech. The verdict block must reference it.

## Deviation 4: Public-safe spec → engineering decisions

CONVENTIONS §14 hands off to `~/projects/aelfrice/docs/specs/`. For RRS, decisions land in `docs/decisions/D<NN>_<name>.md` (one file per decision, dated, references the rounds that backed it). These are internal RRS documents, not public-facing — but they should be self-contained enough to onboard a new engineer cold.

## Deviation 5: Commit prefix

CONVENTIONS §13 uses `experiment:`. Per project-level `CLAUDE.md`, the allowed prefix is `exp:`. Round commits use `exp: R<N> <one-line summary>`. Non-round work (scaffolding, protocol updates) uses the appropriate prefix from `CLAUDE.md` (`feat:`, `docs:`, `refactor:`, etc.).

## Deviation 6: Layered model code

CONVENTIONS imagines `harness.py` shared across rounds plus per-round `run_R<N>.py`. We have a more modular layout (`src/waterprop/` as installable package). The mapping:
- `src/waterprop/<module>/` = the shared physics layer (CONVENTIONS' `harness.py`, decomposed).
- `rounds/R<N>_*/run.py` = the per-round CLI.
- `rounds/R<N>_*/results/` = the per-round outputs.
- `rounds/R<N>_*/STUDY.md` = the per-round narrative (the entry that gets copied into RUNNING_DOC.md and then advanced through the 4 states).
- `tests/` = sanity tests on the shared layer.

## Deviation 7: Aggregate prediction → mission-level prediction

CONVENTIONS §4 asks for an aggregate prediction (what the campaign as a whole concludes). For us, the aggregate prediction is *what propulsion architecture the campaign recommends for ICEBERG's inbound leg*, with quantitative confidence. Pre-registered in `HYPOTHESES.md` before R0 runs.

---

## What stays unchanged

- Round template (§3 in CONVENTIONS).
- Pre-registration with numeric ranges (§4).
- Mid-cycle audit (§6).
- Three buckets — adopt/drop/defer (§7).
- Pivots explicit and named, deferred rounds runnable (§8).
- Bug catches documented in the round where they land, prior claims explicitly corrected (§9).
- Final synthesis round composing all surviving components and measuring cumulative effect (§10).
- Verdict block at end of RUNNING_DOC (§12).

---

## Files (this campaign)

```
water-prop/
├── PROTOCOL.md             (this file)
├── HYPOTHESES.md           pre-registered predictions, revisited as rounds resolve
├── RUNNING_DOC.md          phase question + per-round narrative, ends with Verdict
├── ASSUMPTIONS.md          questioned assumptions, mapped to rounds that test them
├── src/waterprop/          shared physics (per-module __init__.py exports)
├── rounds/
│   ├── README.md           round index
│   └── R<N>_<slug>/
│       ├── STUDY.md        per-round entry (hypothesis/test/result/reading/revisit/cross-learning)
│       ├── run.py          deterministic round CLI
│       └── results/        figures, CSVs, JSON summary
├── tests/                  sanity tests on src/waterprop/
└── docs/
    ├── R1-landscape.md     (pre-protocol scoping; treated as Stage 1 background)
    ├── R2-deepdive.md      (pre-protocol scoping; treated as Stage 2 background)
    ├── HERITAGE.md         flight-heritage survey, updated per round
    └── decisions/          D<NN>_<name>.md — engineering decisions with round attribution
```

---

## Methodology lessons accumulated this campaign

Pre-registration and cross-round lessons surfaced by completed rounds,
captured here so future workers in this campaign can apply them without
re-deriving the lesson. Each lesson names the round that surfaced it.

### Methodology lesson 1 — pessimistic-prediction default holds (afternoon 2026-05-15)

From R-radiator-mass-penalty, R-silicate-contamination, R-electric-outbound.
Three of four afternoon rounds produced *less pessimistic* findings than the
pre-registered hypothesis. When pre-registering, ask "where could this be 2×
wrong in either direction?" and widen the falsification band on the side you
did not think of. A lumped figure that survived multiple rounds without
challenge is more likely conservative-with-margin than optimistic-with-cheating.

### Methodology lesson 2 — sub-spirals compound across legs (titan)

From R-inbound-dv-continuous-thrust. The outbound leg pays one Edelbaum
capture spiral (Earth side); the inbound leg pays two (Earth and Saturn).
When pre-registering an aggregate impulsive-to-continuous-thrust
delta-velocity ratio, count the spirals per leg explicitly rather than
assuming symmetry. A doubled-from-impulsive rule of thumb collapses when one
leg has twice the spiral count of the other.

### Methodology lesson 3 — at a time-ceiling, low specific impulse wins (titan)

From R-inbound-dv-continuous-thrust. At an L0-style round-trip time ceiling,
the electric specific impulse optimum sits at the *lower* band of the
available range, not the upper. Higher specific impulse reduces thrust, which
raises burn time, which under L0-05 is the binding variable. This inverts
the conventional ion-propulsion design intuition for time-constrained
architectures. Pre-register specific impulse sweeps in both directions when
the round is time-bounded.

### Methodology lesson 4 — anchor heritage predictions on population mean, not mode (enceladus)

From R-mission-success-probability. When pre-registering a reliability or
per-mission-success-probability prediction, anchor on the population-mean of
the heritage dataset rather than its mode. The HERITAGE-NONE rows
(subsystems with no flight heritage — fission reactor, bag-harvest) drag the
mean below the mode, and the program is going to be built out of the rows
that do not yet exist. The mode anchors you on a subset that excludes the
load-bearing risk.

### Methodology lesson 5 — two-bucket bias check (enceladus)

From R-mission-success-probability. This campaign's physics rounds
(R-radiator, R-silicate, R-electric-outbound, R-inbound-dv-continuous-thrust)
have been pessimistically pre-registered; corrections came back
less-pessimistic-than-predicted. The first reliability round was
optimistically pre-registered; correction came back
more-pessimistic-than-predicted. Worth a per-domain prior check at
pre-registration: which way does my domain bias me, and have I corrected for
it?

### Methodology lesson 6 — shared-physics function input conventions need assertions (hyperion)

From R-bag-capture-efficiency-revisit. The bug at
`R_electric_outbound/run.py:223` was that `constant_thrust_burn` documents
its `m_initial_t` parameter as wet-mass-at-start-of-burn, but the call site
passed dry-mass-at-end-of-burn. The bug survived multiple rounds because no
prior reader cross-checked the convention against the caller. When authoring
or reviewing a physics function with a mass-interpretation convention, add
either an explicit precondition assertion or a docstring example showing the
correct call. Future shared-physics functions in `src/waterprop/` should
follow this pattern.

### Methodology lesson 7 — compute under the most pessimistic credible anchor first (titan-2)

From titan-2's seven-round session (R-conops-skeleton through
R-HE-graze-feasibility). Multiple rounds in that session produced
headline findings under one anchor that were retracted under a more
conservative anchor a round later. R-multi-chunk-per-mission's
"venture-class at N=5" headline rested on a silent high-eccentric-Saturn-graze
departure assumption; R-multi-chunk-departure-orbit then surfaced that the
B-ring-direct anchor needed N=23; R-HE-graze-feasibility then physically
falsified the HE-graze case entirely.

The lesson: when pre-registering an economic-leverage round, compute the
product of central estimates under the most pessimistic credible anchor
first, then range upward only if that case closes. Where an inherited
number is ambiguous (e.g. a departure-orbit-dependent delta-velocity),
run both endpoints rather than picking one. A headline that survives the
pessimistic anchor is durable; a headline derived under the optimistic
anchor will be retracted by the next round that tightens the anchor.

This compounds with lesson 1 (pessimistic-prediction default): the
*prediction* should be pessimistic; the *computation* should also use the
pessimistic anchor. Both directions of the bias check matter.

### Methodology lesson 8 — per-mission cashflow is not program NPV (rhea)

From rhea R-architecture-D-cost (round 6) and R-architecture-D-L1007-relaxation
(round 7). Round 6's "Architecture D is structurally money-losing at zero
discount rate" headline was derived from per-mission gross cashflow at the
L1-007 200-t cap. Round 7 falsified the per-mission piece at chunk ≥ 413 t
(D-solar-thermal turns positive on a per-mission basis at relaxed chunk)
but confirmed the headline holds at program-NPV level: best D case at chunk
482 t is NPV(0) = -$14.1B because the fleet-of-ships capital amortisation
swamps the per-mission gains.

The lesson: when pre-registering a marginal-IRR or "structurally money-losing"
claim, the back-of-envelope must include program-level NPV, not just
per-mission cashflow. Per-mission positive does not imply program NPV
positive once fleet capital, R&D, and operations are amortised across the
mission set. Sub-claims of the form "Architecture X economically closes"
need a program-level check, not a per-mission check.

Enceladus-r5 R-fleet-ramp-NPV surfaced the dual of this: a per-mission
calculation can also UNDERSTATE program-level NPV when the fleet-ramp
timing is not modeled (round-6 NPV was 64 percent magnitude overstated as
a negative number, i.e. the program was closer to break-even than the
per-mission calc implied). Either direction of error is in play.

### Methodology lesson 9 — anchor SCOPE.md on the prior round's aggregate verdict, not on a cherry-picked sub-finding (phoebe)

From phoebe R-chunk-as-heat-shield-revisit (commit `9b3d29e`). The prior
`R_chunk_as_heat_shield_revisit/SCOPE.md` (authored by Saturn / orchestrator)
took the "chunk thermodynamically viable" sub-finding from the original
R-chunk-as-heat-shield round while omitting that the round's *aggregate*
verdict was FALSIFIED (multi-pass aerobraking unworkable; ballistic
coefficient too high). The downstream worker (phoebe) re-anchored on the
primary-text aggregate and surfaced the structural infeasibility that the
SCOPE had elided.

The lesson: when an orchestrator (or any author) writes a SCOPE.md or
proposes a follow-on round, anchor on the prior round's *aggregate*
verdict and *primary-text* claims, not on a downstream summary or a single
favourable sub-finding. A SCOPE that picks the convenient sub-claim out
of a round whose aggregate verdict is falsified inherits that falsification
and produces an investigation that is downstream of an unaddressed earlier
question.

Practical: when writing a SCOPE for `R-X-revisit` or `R-X-followon`, the
SCOPE should explicitly quote the prior round's Reading section and
aggregate verdict (held / falsified / mixed) in its Context section. If
the aggregate was falsified, the SCOPE must justify why the revisit is
not already foreclosed. If the SCOPE skips this step, a downstream worker
will reasonably re-anchor and the SCOPE-driven framing will be retired
(as happened with R-chunk-as-heat-shield-revisit).

This compounds with lesson 7 (compute under the most pessimistic credible
anchor first) — both lessons point at the same failure mode: optimistic
anchoring at the SCOPE / round-design step propagates through into rounds
that have to be retracted when a more careful worker re-anchors on
primary text or pessimistic conditions.

### Methodology lesson 10 — multi-burn stacks compound dry-mass and delta-velocity sensitivity more than single-burn intuition predicts (titan-2)

From titan-2 Block-4 R-residence-exit-maneuver (commit `513fe06`). The
composite-architecture round pre-registered that 20 t of jettisoned residence
hardware would yield a modest delivered-fraction uplift, dominated by the
larger lever of Earth aerocapture savings. The measured uplift was
substantially larger because the jettison happens *before* the high-Isp exit
burn — every kilogram dropped saves not just its own mass but the propellant
mass to accelerate it through the exit Δv, the inbound coast propellant to
decelerate it for aerocapture, and the carried-mass tax across the multi-burn
stack. Single-burn intuition (Tsiolkovsky on one Δv leg) understates the
sensitivity by a factor that grows with the number of post-jettison Δv legs.

The lesson: when pre-registering a mass-jettison or staged-vehicle hypothesis
under a multi-burn architecture, decompose the sensitivity by jettison-point
along the burn sequence. A jettison early in the stack propagates through
every downstream Tsiolkovsky exponent; a jettison late in the stack pays
back only on the remaining legs. The composite-architecture central uplift
of 21.8% (vs Option A's 17%) comes mostly from this propagation, not from
the individual lever-by-lever credits.

### Methodology lesson 11 — robustness-by-magnitude vs robustness-by-cancellation (iapetus)

From iapetus R-global-vs-US-base-rate (commit `d05f9a8`) and
R-engineering-closure-sensitivity (commit `9a556b3`). Two ways a conjunction
posterior can be "robust" to assumption changes: (i) the absolute floor is
low enough that no assumption combination clears the decision threshold —
robustness-by-magnitude; (ii) competing parameters move in opposite directions
and cancel, leaving the central estimate stable — robustness-by-cancellation.
The two have very different implications. (i) is durable: the threshold
crossing genuinely never occurs. (ii) is fragile: a single asymmetric shock
breaks the cancellation and the central estimate moves materially.

The H6 (program-class-decision) conclusion is robust by magnitude: even
under all conditional priors set to 1.0, the absolute ceiling is 2.7%, below
the venture threshold of 10%. The chain therefore stops there — additional
sensitivity rounds have diminishing returns. By contrast, a
robustness-by-cancellation finding would warrant continued probing of the
cancellation structure to make sure no asymmetric channel has been missed.

The lesson: when reporting "robust to assumption variation," classify which
kind of robustness. Robustness-by-magnitude lets you stop the sensitivity
campaign; robustness-by-cancellation requires probing the cancellation
mechanism before stopping.

### Methodology lesson 12 — forward-looking conditionals are not historical conditionals (iapetus)

From iapetus R-global-vs-US-base-rate (commit `d05f9a8`). The historical
base rate of orbited space-fission programs is dominated by US Cold-War
and post-Cold-War programs (SNAP-10A, SP-100, Timberwind, Prometheus,
DRACO, Kilopower, Fission Surface Power). The scope distribution of those
programs is heavily weighted to <100 kWe (~67% historical mass below 100
kWe). The prospective scope distribution — what reactor programs are
currently funded or proposed worldwide — is weighted differently (~40%
historical-mode, with the remainder shifted higher per Chinese megawatt
ambitions and DRACO-class targets).

The lesson: for orbit-in-window questions (probability of program of
scope X reaching orbit by date Y), use prospective scope distributions
not historical ones. The two differ by ~10× at the conjunction posterior
level. The historical conditional is the right anchor for "what fraction
of attempted programs in scope X have orbited"; the prospective conditional
is the right anchor for "what fraction of currently-planned programs in
scope X will orbit." A pre-registration that conflates the two will report
an answer 5-10× off in magnitude.

This compounds with lesson 4 (anchor heritage predictions on population
mean, not mode): both lessons say "be explicit about which population is
the anchor."

### Methodology lesson 13 — robust-to-single-axis is not robust-to-joint-axis (iapetus)

From iapetus R-conditional-prior-sensitivity (commit `af8eb91`). When a
sensitivity round produces a robust conclusion, distinguish "robust to
single-axis lift" from "robust to joint-axis lift" from "robust to
maximum-everywhere lift". The three are not interchangeable.

Round 4 of the iapetus chain (R-engineering-closure-sensitivity) swept
engineering-closure priors with conditional priors held fixed at
conservative anchors. The resulting "2.7% absolute ceiling with all
conditional priors set to 1.0" was REPORTED as the pathological maximum.
Round 5 then swept conditional priors with engineering priors at
baseline, and surfaced that the true pathological maximum requires
*both* dimensions at 1.0 simultaneously, with the joint conjunction
reaching the orbit-posterior ceiling itself (14.51%). The round-4 number
was a specific 1-of-2-dimension corner, not the pathological maximum.

The lesson: when reporting "the absolute ceiling under all priors at 1.0",
verify that the sweep covers *every* prior dimension simultaneously, not
just the dimension the round focused on. If a multi-dimensional joint
maximum is not actually computed, report only the conditional or single-
dimension maximum, and flag that the joint maximum is not yet in hand.

This is the asymmetric companion to lesson 7 (compute under most
pessimistic credible anchor first): lesson 7 is about cross-anchor
robustness on the input side; this lesson is about cross-prior robustness
on the conclusion side. Both warn against over-broad robustness claims
derived from incomplete sweeps.

### Methodology lesson 14 — conditional-axis stripping discipline (phoebe, candidate; awaiting project-owner ratification)

From phoebe R-hybrid-chemical-power-augmentation (commit `a969aa6`). When a
SCOPE inherits axes from upstream-falsified architectures, the round can
report charitable joint-passing cells that vanish under audit-conditional
stripping. Phoebe's sweep produced 54 raw joint-demonstrator-passing cells
under charitable flags, all of which collapsed to 0 after stripping three
audit-conditional axes (aerocapture credit conditional on separately-
falsified R-hybrid-aerocapture-aerobraking; reactor lifetime ≤ Kilopower
10-yr design target; launch envelope ≤ 1× Starship 150-t single-flight).
The raw 54 cells were not real findings — they were rescue-from-falsified-
upstream artifacts.

The lesson: when a SCOPE inherits axes from an upstream-falsified
architecture, report results with and without those axes side-by-side.
Audit-condition each inherited axis explicitly. Charitable cells that
disappear under audit-stripping are not findings; they are rescue-from-
falsified-upstream artifacts.

### Methodology lesson 15 — binary kill criteria for probabilistic constraints over-determine triage outcomes (phoebe, candidate; awaiting project-owner ratification)

From phoebe R-mission-architecture-pivot-survey (commit `bb570d7`). When a
triage round applies binary PASS / FAIL kill criteria to a constraint that
is genuinely probabilistic in upstream analysis (e.g., reactor-program
availability per iapetus's chain, where posterior is 0.07-0.20), the
binary conversion over-determines the triage outcome. Phoebe's pivot-survey
classified 24 of 31 candidates DEAD-ON-ARRIVAL because F6 (reactor program)
was binarised to FAIL whenever its posterior was below 0.5. Re-running the
triage with F6 as UNKNOWN (rather than FAIL) yielded 24 DEAD + 7
F6-conditional WORTH-DEEP-DIVE — the latter set being the actually-
load-bearing decision space.

The lesson: when a triage round applies kill criteria to constraints
that are probabilistic in upstream analysis, use a probability-weighted
aggregator (e.g., expected kill-probability product) rather than a binary
PASS/FAIL conversion. Report both binarised and probability-weighted
results side-by-side when reporting aggregate-DEAD counts.

### Methodology lesson 16 — distinguish dominant-kill-gate from highest-leverage gate (iapetus, candidate; awaiting project-owner ratification)

From iapetus R-staged-options-with-technology-gates (commit `7ffc1e6`) and
R-T1-sensitivity-and-breakeven (commit `ad18654`). In a multi-gate decision
tree, two distinct gate-priority rankings emerge: (i) **dominant-kill gate**
— the gate with the highest p_kill, which dominates expected loss; (ii)
**highest-leverage gate** — the gate where a unit lift in pass-probability
buys the largest EV gain. The two need not coincide and often do not.

In iapetus's staged-options model: T1 (Fission-Surface-Power Phase-2 award)
is the dominant-kill gate with p_kill > 99.95% under conservative anchors,
making it the gate that determines E[loss]. But T3 (B-ring rendezvous
survivability) is the highest-leverage gate post-T1, because its baseline
prior is only 0.20 (vs T2's 0.50), so a unit lift in T3's prior buys more
EV than a unit lift in T2's prior. **Investing in T3 closure rounds before
T2 closure rounds is the correct sequencing under highest-leverage prioritisation**
— a methodological surprise relative to the prior "fix the highest-failure-
probability thing first" intuition.

The lesson: in a multi-gate decision tree, report both the dominant-kill
gate (drives E[loss]) and the highest-leverage gate (drives optimal
sequencing). The two are different optimisation criteria and produce
different priority orderings. The pitch / capital-allocation framing
should cite both.

> **Number 17 reserved** for mimas's pending candidate (round-local
> redefinition of physics-helper functions invites convention drift; see
> mimas R-shared-physics-audit handoff), not yet integrated as of
> 2026-05-22. Numbered 18 below to avoid a collision when both are merged;
> orchestrator to reconcile if mimas's is dropped (a gap at 17 is harmless).

### Methodology lesson 18 — pre-register the conditioning structure, not just the point estimate (hyperion, RATIFIED 2026-05-22 by project owner)

When a quantity under test depends on an operating or structural variable —
closing velocity, thruster architecture, reactor power class — pre-register a
hypothesis that **brackets each regime** of that variable, not a single point
estimate. A single-point pre-registration silently bakes in an unstated regime
assumption and is fragile to it; a regime-conditional pre-registration surfaces
the dependence and is the robust form. The brackets are not decoration: when a
later round changes the operating point, a regime-conditional pre-registration
still holds (you predicted each regime), whereas a point pre-registration is
falsified by the regime shift even when the underlying physics was understood.

Evidence — one session, three rounds, 2026-05-22:

- **R-A14-engineering-decomposition** (`fd6fab0`) pre-registered catch and
  containment *conditional on closing velocity* (millimetre-per-second vs
  metre-per-second) and survive *conditional on cinch redundancy*. All six
  hypotheses held; the round's load-bearing finding was precisely that the
  joint pivots on the conditioning variable (closing velocity), which the
  bracketed pre-registration surfaced.
- **R-water-electrothermal-flight-scale-audit** (`cd8d753`) pre-registered
  *conditional on thruster architecture* (microwave-electrothermal vs
  radio-frequency-ion). All five hypotheses held; the finding was an
  architecture trap that only a branch-conditional structure could express.
- **R-kilopower-scale-up-credibility** (`3529984`) pre-registered single-regime
  point predictions (H2/H3) by importing the 500-kilowatt-electric
  mass-blowout failure mode into the 30-kilowatt-electric regime *without
  re-checking that reactor mass at fixed specific power scales linearly with
  power* (17× smaller here). **Both H2 and H3 falsified** — the only two
  falsified hypotheses across the three rounds, and both on the axis where the
  pre-registration omitted the conditioning variable.

**Corollary (input-side failure mode):** do not import a failure mode across
regimes without re-checking that its mechanism scales into the new parameter
regime. The kilopower H2/H3 falsification was caused by assuming the
500-kilowatt-electric specific-power collapse recurs at 30-kilowatt-electric;
it does not, because reactor mass at fixed specific power scales with power.

This compounds with lesson 7 (compute under the most pessimistic credible
anchor first — input-side *cross-anchor* robustness) and lesson 13
(robust-to-single-axis is not robust-to-joint-axis — conclusion-side
*cross-prior* robustness). Lesson 18 is the **pre-registration-side**
discipline: make the regime-dependence explicit in the hypothesis itself.

### Methodology lesson 19 — scope-mismatch is a clean falsification root cause; do not conflate it with a bug (titan-4, candidate; awaiting project-owner ratification)

When a hypothesis predicts that one model reproduces another within tolerance
(e.g., "framework reproduces titan-3's surviving cells within ±20 percent"),
and the round produces a large disagreement, the natural disposition is
binary: either *the test-of-record is wrong* or *the model being compared is
wrong*. There is a third disposition that the binary reading misses:
**the two models are predicting different things at the architecture-parametrisation
level**, and the disagreement is identifiable as scope, not bug.

Treat scope-mismatch as a first-class falsification root cause distinct from
bug. The discipline:

1. **When a tolerance hypothesis fails by margin much larger than the
   tolerance,** do not stop at "falsified" — diagnose whether the disagreement
   has an *identifiable, clean* root cause in differing model scope (i.e.,
   the two models charge for different cost categories, or one models the
   round-trip and the other models a leg, or one carries a constraint the
   other omits). If yes, the falsification is **"falsified-in-framing"** and
   the test-of-record is preserved as valid for its own scope.

2. **Document the scope difference explicitly** in the READING so downstream
   readers cannot conflate scope-mismatch with model-bug. The two have very
   different downstream consequences: a bug demands fixing the bug; a
   scope-mismatch demands a parallel reading of each model's verdict in its
   own scope.

3. **The more-complete model becomes the new test-of-record, but the less-complete
   model is preserved as valid for its own scope.** Do NOT delete the prior
   model's results from the matrix HISTORY; annotate them as scope-limited
   and keep the cells as data inputs.

Evidence — titan-4 R-framework-matrix-parity (`0eb11a7`, 2026-05-22 latest+18):

The round pre-registered H4 ("titan-3's 4 cells reproduce within ±20 percent
of titan-3's stated tonnage"). H4 fell by ~half — framework constraints-OFF
delivers 19.4 tonnes from a 50-tonne chunk versus titan-3's 35.6 tonnes. The
binary-disposition reading would be either "framework is wrong" or
"titan-3 is wrong." The actual disposition was neither: titan-3 modeled the
inbound leg only (vehicle already at Saturn; chunk as sole propellant; no
Earth-launched propellant; no powerplant mass throughout; no reactor-lifetime
constraint) while the framework models the full round-trip carrying the
powerplant the whole way. The scope mismatch is identifiable as clean and the
framework verdict is the more-complete reading. titan-3's cells are preserved
as valid inbound-leg analysis (axis 02 + axis 09 carry them with the
"inbound-only accounting" annotation).

**Without the scope-mismatch-as-root-cause discipline,** the natural reading
would have been either "scrap the framework" or "scrap titan-3" — both wrong.
With the discipline, the framework becomes the canonical full-round-trip
sweep substrate and titan-3's leg-level analysis is preserved.

This compounds with lesson 9 (anchor SCOPE.md on the prior round's aggregate
verdict, not on a cherry-picked sub-finding) and lesson 18 (pre-register the
conditioning structure). Lesson 19 is the **post-round disposition** discipline
for tolerance-hypothesis failures: do not stop at falsified; diagnose for
scope versus bug.

### Methodology lesson 20 — before correcting an anchor, confirm the axis is load-bearing; and when correcting, re-derive from inputs (titan-5 + hyperion, candidate; awaiting project-owner ratification)

Two related disciplines surfaced jointly in the latest+20 integration pass; both pair with lesson 7 (compute under the most pessimistic credible anchor first) and lesson 18 (pre-register the conditioning structure) and are best read as the
**input-side and output-side discipline** for anchor correction.

**Part A — confirm the axis is load-bearing before correcting an anchor.** Lesson 7 protects against optimism on engineering axes by computing under the most pessimistic credible input. On a pricing axis (or any axis with natural-monopoly / mission-essential willingness-to-pay structure), the "pessimistic" anchor (flat earth-launch-displacement price floor) can be *too* pessimistic; it ignores supplier market power in captive, no-substitute segments. The discipline that saves the verdict is not the pessimistic anchor — it is **checking which axis is binding**. If pricing is not the binding axis (a reactor-program-availability gate is), then correcting the pricing anchor up or down cannot rescue or kill the verdict, and the round risks producing a number with no decision implications.

Test before correcting: state the axis, state the verdict-class outcome under the current anchor, state what the verdict would look like under a corrected anchor at each extreme of the credible band. If the verdict-class is the same at both extremes, the axis is non-binding and the correction is bookkeeping; if the verdict-class flips, the axis is binding and the correction matters. R-pricing-anchor-revisit's H7 was precisely this test for the pricing axis (verdict class did not flip across $1,400-10,000/kg); R-pricing's inverse-risk follow-on confirmed the same axis is also not propping up the verdict from the optimistic side.

**Part B — correcting a flagged number without re-deriving from inputs preserves the error class.** When a pre-registered audit flags a derived quantity (e.g., a 75-percent delivery fraction), the natural correction is to back-solve a more conservative-looking output (e.g., edit the output to 54 percent). This fixes the symptom (a too-high number) but preserves the disease (the input-frame error that produced the original). A reader sophisticated enough to recompute from the displayed inputs will catch the same error class with a different magnitude.

The fix is to re-derive from inputs, not edit the output. R-pitch-arithmetic-audit found the pitch §2 delivery-fraction edit (75 → 54 percent) halved the symptom but kept the disease: the 54-percent figure still computed off an indefensible Saturn-departure anchor (1.5 km/s) and impulsive accounting on continuous-thrust legs. The fix that worked was applied this pass via `PROPOSED-PITCH-DIFF.md` D-1 through D-4: change the Saturn-departure input (D-1), let the delivery-fraction output cascade (D-2), and label the impulsive-vs-continuous frame explicitly (footnote `[^contthrust]`).

**Combined corollary.** Anchor corrections must be doubly disciplined: confirm the axis the anchor sits on is load-bearing for the verdict (Part A) AND, when applying the correction, re-derive from inputs rather than back-solve the output (Part B). Lesson 7 + lesson 13 (robust-to-single-axis is not robust-to-joint-axis) + lesson 18 (pre-register the conditioning structure) + lesson 20 (axis-load-bearing-first + re-derive-from-inputs) compose the campaign's full anchor-discipline stack.

Evidence — two rounds, both 2026-05-22 latest+20:

- **R-pricing-anchor-revisit (titan-5 `1023a45`)** — H7 held (pricing is not the binding axis); H6 falsified (correcting the pricing anchor does NOT flip the program-class verdict). The project-owner challenge ("$1,400/kg is too low") was correct in direction but not in load-bearing-ness. Methodology-lesson candidate explicit in READING.md.
- **R-pitch-arithmetic-audit (hyperion `f9f7fc2`)** — found the prior 75-percent → 54-percent pitch edit halved the symptom but kept the disease (same impulsive-on-continuous-thrust error class, just at lower magnitude). `PROPOSED-PITCH-DIFF.md` D-1 corrects the input; D-2/D-3/D-4 cascade from the input fix; D-5 reconciles a separate framing inconsistency. Methodology-lesson candidate explicit in READING.md.

The two candidates compose: Part A explains *whether* to correct (and warns when correction is bookkeeping); Part B explains *how* to correct without preserving the error class.

### Methodology lesson 21 — vehicle dry mass is a derived quantity, not a sweep axis (saturn orchestrator, 2026-05-26, candidate; awaiting project-owner ratification)

From R-smaller-vehicle-demonstrator-envelope (commit `20117ac`) and the project-owner observation that surfaced mid-execution. The mission_graph framework's treatment of `vehicle_mass_kg` as a sweep axis — a free input the cell assumes and walks forward from — makes every per-cell vehicle-mass answer non-self-consistent. The phases themselves have internal dry-mass demands (capture mechanism, reactor + shield, radiator, thermal protection, structural backbone, communications floor) that should *determine* vehicle dry mass, not be assumed against it.

The bug surfaces visibly when the sweep is extended to small vehicle masses (10-20 t): the framework reports these as closing the 30-tonne delivered-floor at 200-tonne chunk, despite the capture mechanism alone demanding ~15 t and the reactor + radiators + TPS + structure + comms demanding another ~25-30 t. The "10 t vehicle closes" finding is a methodology artifact, not a physics result.

The lesson: in any campaign-style sweep over architecture-defining choices, the sweep axes must not include quantities that are determined by the phases themselves. Vehicle dry mass is a derived quantity computed iteratively from per-phase mass demands; treat it as an output of the mission graph walk, not an input. Sweep axes are the *exogenous* choices (chunk mass, capture architecture, reactor class, specific impulse, trajectory choices, launch class). Cells that fail to converge to a self-consistent vehicle mass are NOT closures — they are mutually inconsistent design choices and must be flagged as such.

This is the structural-sweep-design companion to lesson 20's anchor-discipline stack: lesson 20 catches anchor correction errors (correcting non-load-bearing anchors, back-solving outputs instead of re-deriving inputs); this lesson catches sweep-design errors that hide internal consistency failures.

**Action item carried by R-vehicle-mass-closure-refactor SCOPE** (titan-6 currently executing; STUDY.md pre-registered with H1-H5).
