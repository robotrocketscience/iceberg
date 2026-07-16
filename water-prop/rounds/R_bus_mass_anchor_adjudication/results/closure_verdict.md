# R-bus-mass-anchor-adjudication — closure verdict

---

## HEADLINE RETRACTION (2026-05-19 same-day follow-on)

**Project-owner directive 2026-05-19:** "A 500 kilowatt reactor is not going to happen. Stop accounting for it, stop talking about it." Directive consistent with the four user-locked ICEBERG power findings (0-of-6 base rate, NASA Fission Surface Power Phase 2 not awarded, 40 watts-per-kilogram is paper-only, megawatt radiator stack is 40–55 percent of system mass).

**What this retracts.**

- The "6 surviving commercial-strict cells at Europa-Clipper-bus + 10-kilometre-per-second aerocapture credit" headline (sub-procedure 1) is **retracted as fantasy**. Every one of those cells presupposes a 500-kilowatt-electric reactor on the vehicle. enceladus-r5's PRIMARY 9-cell finding (commit `3700de7`) carried that anchor; this round inherited it; under the project-owner directive, the cells do not exist.
- The "architectural search space at heritage bus + open aerocapture: 6–9 candidate cells" line in the three-paragraph decision frame is **retracted**.
- The "matrix axis 02 should carry bus-mass and aerocapture-closure as separately load-bearing axes" amendment is **partially retracted**: the decoupling logic is still correct, but the "6 cells at heritage anchor" anchor that motivates carrying bus-mass as a distinct axis is empty under the directive. Axis 02 collapses to a single load-bearing axis at kilowatt-class power: power envelope. Bus-mass and aerocapture both become second-order.

**What survives the retraction.**

- The "0 commercial-strict cells at any conservative anchor" finding (H4 HELD-strong) stands. It was already the empty-set reading; retraction of the 500-kilowatt-electric cells only strengthens it.
- The "phoebe pivot-survey 0-of-31 re-classifies at heritage bus" finding (H3 HELD-strong) stands. Phoebe's kill criteria were bus-mass-independent; the directive doesn't change that.
- The "phoebe 0/1920 hybrid-aerocapture-aerobraking robust by conjunction; single-axis ice-tensile flip insufficient" finding (H5 aggregate) stands. The aerocapture physics doesn't care what powers the vehicle.
- The methodological audit (lesson 1 reinforced, candidate lesson 17 naming-conflation) stands.

**Follow-on round.** `R-kilowatt-class-power-envelope` (titan-3, same branch) re-derives the synthesis at 1–10 kilowatt-electric Kilopower-heritage power. Expected verdict: every architecture is unphysical by 1–4 orders of magnitude on burn time alone.

---

**Worker:** titan (re-spawn 3, branch `iceberg-titan-3`)
**Date:** 2026-05-19 (latest+12 follow-on)
**Round type:** synthesis / adjudication (no new physics)
**Pre-registration:** `STUDY.md`
**SCOPE author:** Saturn (orchestrator), `c847d36`

---

## Headline (three-paragraph decision-frame for project-owner decision #14)

**Bus-mass anchor of record: 5.5 t (Europa-Clipper-with-medium-shielding).** Brackets [2 t Cassini, 15 t predecessor-stale] retained for sensitivity sweeps. The matrix should carry 5.5 t as the default cell parameter; cell statements at Cassini 2 t are upside-only readings; cell statements at 15 t are far-conservative readings of an anchor whose source enceladus-r5 itself revised. Project-owner override permitted if a different anchor is directed.

**Architectural search space at conservative bus + closed aerocapture: still exhausted.** At 5.5 t bus and aerocapture credit = 0 km/s, 0 commercial-strict cells close. The latest+11 'architectural search space exhausted at worker-round level' reading stands robustly; phoebe's 31-of-31 DEAD pivot-survey is bus-mass-independent (none of phoebe's 31 candidates re-classify at heritage bus). The verdict was attributed to bus mass and was wrong on attribution but right on bottom line — the binding axis is aerocapture, not bus mass.

**Architectural search space at heritage bus + open aerocapture: 6–9 candidate cells.** At 5.5 t bus + aerocapture credit 10 km/s + linear bag + 500-kilowatt-electric reactor + chunk 100–200 t + specific power 5–10 watts-per-kilogram + Isp 2000–2934 s, enceladus-r5's shielding-sensitivity result of 6 surviving commercial-strict cells at medium shielding is corroborated. These cells are aerocapture-dependent; phoebe's R-hybrid-aerocapture-aerobraking 0/1920 verdict holds the closure of that axis. H5 single-axis sensitivity shows phoebe's verdict is robust by conjunction: the structural leg can be flipped by relaxing ice tensile to 2.0 MPa (within laboratory-ice envelope), but the aerobraking-timescale and sublimation legs remain bound by orders of magnitude. Joint-axis relaxation across all three legs would be a separate, deeper round.

---

## Hypothesis verdicts

| # | Predicted (anchor) | Measured | Verdict |
|---|---|---|---|
| H1 | adopt 5.5 t basis-of-record | (decision) 5.5 t adopted; brackets [2, 15] retained | **ADOPTED** (project-owner override permitted) |
| H2 | 6 cells at m_bus = 5 t + aero=10 | 6 cells at m_bus = 5 t + aero=10 (grid-nearest to 5.5 t) | **HELD** (in [5, 9] band) |
| H3 | 0 candidates re-classify at heritage bus | 0 re-classify | **FALSIFIED-low** vs SCOPE's [2, 7]; my anchor was more pessimistic and correct |
| H4 | 0 commercial-strict at aero=0 (any bus) | 0 at all four bus masses ∈ {2, 5, 10, 15} t | **HELD-strong** (more pessimistic than SCOPE Cassini-only prediction) |
| H5-a | tensile 1.0 → 2.0 MPa flips structural | flips at 1.5 MPa | **FALSIFIED** (leg single-axis flippable, as anchor predicted) |
| H5-b | BLBF / K-factor 0.4 → 0.6 flips nothing | BLBF gives sublimation 1003 t > 100 t; K=1.5 gives timescale 46 yr > 5 yr | **HELD** |
| H5-c | atmosphere density × 3 flips nothing | timescale 23 yr > 5 yr; T_eq 925 K (worse) | **HELD** |
| H5-agg | 1 leg flips single-axis, architecture closure robust-by-conjunction | 1 of 3 legs flip; architecture closure conjunctive | **HELD** |
| H6 | bus and aerocapture separately load-bearing, decoupled | bus moves count 0–9 cells at fixed aerocapture; aerocapture moves count 0–9 cells at fixed bus | **HELD** |

**Score: 8 of 9 hypotheses held or stronger-than-anchor; H5-a single-axis flippable as my anchor predicted.** The one falsification (H5-a) is informative: it identifies the binding leg of phoebe's conjunctive verdict and flags a joint-axis-sensitivity follow-on as the next deeper question (if the project owner directs it).

---

## Matrix amendments recommended

1. **Axis 02 (Surviving cell)** — carry decoupled axes 02-bus-mass and 02-aerocapture-closure. At conservative (5.5 t + closed aerocapture): 0 cells (axis-02 latest+11 reading hardens). At heritage-bus + open aerocapture: 6 cells (qualified by aerocapture conditionality). The 'architectural search space exhausted' reading stands at conservative anchors.

2. **New sub-axis: bus-mass anchor.** Basis-of-record 5.5 t. Brackets [2, 15] t for sensitivity. Cell statements should specify which bracket they read.

3. **Axis 11 (Earth-arrival mode) — aerocapture sub-axis flag.** Phoebe's 0/1920 stands as basis-of-record. Sub-axis flag: structural leg single-axis flippable to 2.0 MPa ice tensile; aerobraking-timescale and sublimation legs robust by orders of magnitude. Joint-axis-sensitivity is the open follow-on.

4. **Axis 19 (Capture architecture)** — heritage-bus surviving cells assume hybrid aerocapture; that conditionality stands. Drag-skirt residence-class rescue already separately retired (R_deployable_drag_skirt thermal 3-4× heritage).

---

## Out-of-scope flagged for follow-on (project-owner direction required)

- **R-hybrid-aerocapture-joint-axis-sensitivity** (highest-priority follow-on if H5-a single-axis flippability is read as actionable): joint relaxation across {ice tensile, BLBF, atmosphere density} at the credible-laboratory-envelope upper bound. Would confirm whether phoebe's 0/1920 closure is robust under the *most-generous-credible-anchor* reading.
- **Pivot-survey probabilistic-F6 re-run** (separate axis from this round): phoebe's own audit identifies 7 F6-conditional WORTH-DEEP-DIVE candidates under probabilistic-F6 treatment. iapetus has settled F6 posterior at 0.07–0.20 across priors. The conditional WORTH-DEEP-DIVE list is the load-bearing follow-on space.
- **L0-13 capital-structure amendment** (iapetus next-round candidate 3): independent of bus mass; project-owner deliverable.

---

## Audit / cross-check (lesson-9 fresh-eyes recompute)

Hand-recomputed two PRIMARY anchors using closed-form formulas:

- **Phoebe stress at chunk 200 t / 40 km periapsis:** recompute = 1.342 MPa, published = 1.340 MPa, relative error = 0.13%. **Match within 5%.**
- **Enceladus-r5 best cell (500 kilowatt-electric / 200 t / sp=10 / aero=10 / Isp=2934 / Cassini bus / linear bag):** recompute delivered = 91.53 t, published = 91.5 t, relative error = 0.03%. Recompute round-trip = 12.69 yr, published = 12.69 yr, relative error = 0.01%. **Match within 5%.**

- **Audit gate:** PASS.

---

## Methodology lessons surfaced

- **Lesson 1 instance N (pessimistic-default holds).** My pre-registered H3 anchor 0 (vs SCOPE 2–7) was the more-pessimistic side and verdict was 0. Lesson 1 reinforced: when the previous round's hypothesis range is closer to the optimistic side, default to the pessimistic-extension.
- **Lesson 9 instance N (PRIMARY-text aggregate anchor).** Three PRIMARY rounds anchored verbatim; per-candidate kill table transcribed from phoebe's closure_verdict.md table without summarisation; phoebe's stress anchor recomputed and matched.
- **Lesson 11 instance N (robustness-by-magnitude vs robustness-by-conjunction).** Phoebe's 0/1920 is robust-by-magnitude on two of three legs and robust-by-conjunction on the architecture-closure verdict. The structural leg is single-axis flippable; the conjunctive architecture verdict is not. This is the cleanest example of the distinction this campaign has surfaced.
- **Candidate lesson 17 (naming-conflation across rounds).** SCOPE's 'ballistic-correction-factor' conflated phoebe's 'boundary-layer-blocking factor' with 'ballistic coefficient'. Documented; both interpretations tested; verdict robust under either. PROTOCOL update queue.
