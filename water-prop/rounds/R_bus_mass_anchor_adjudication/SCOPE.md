# R-bus-mass-anchor-adjudication — establish the matrix's basis-of-record bus-mass anchor and decouple bus-mass closure from aerocapture closure

**Status:** scope, pre-study. Authored by Saturn (orchestrator), 2026-05-19 latest+12, immediately after the iceberg-enceladus-r5 + iceberg-rhea-2 + iceberg-titan-2 integration pass.

**Context.** Project-owner decision #14 (bus-mass anchor adjudication, new at latest+12). Three load-bearing facts:

1. **enceladus-r5 R-bus-mass-anchor-sweep (`3700de7`)** finds 9 commercial+strict cells exist for Architecture E (pure-electric end-to-end) at Cassini-anchor bus (m_bus = 2 t) + linear bag (5% × chunk) + 10 km/s aerocapture credit + 500-kilowatt-electric reactor + 200-tonne chunk. Even at flown-anchored specific power (5 W/kg KRUSTY-class), 1 cell closes commercial-strict.
2. **enceladus-r5 R-bus-mass-anchor-sweep shielding sensitivity (`95565cf`)** finds 7 of 9 cells still survive under realistic 500-kilowatt-electric radiation shadow shield (1-3 kg/kilowatt-electric) + power-conversion-unit (1.5 t) + cables/harness (0.5 t). At medium shield (3 kg/kilowatt-electric), 7/9 still pass. The 2 cells that fail are the marginal ones at flown-anchored specific power (5 W/kg) + low Isp (2000 s).
3. **phoebe R-hybrid-aerocapture-aerobraking (`1623cca`)** finds 0 of 1920 hybrid-aerocapture-aerobraking cells close under conservative anchors (US Standard 1976 atmosphere, ice tensile 1.0 MPa, ballistic-correction-factor 0.4, body-absorbed 0.5). Three independent failure modes: pass-1 chunk shatter at any depth dumping ≥ 4.18 km/s; aerobraking unphysical timescale (9 yr at 110 km to 1608 yr at 200 km); chunk consumed by sublimation (77-1486 t loss across 110-200 km).

**The apparent contradiction is a joint-condition.** enceladus-r5's surviving cells presuppose an aerocapture credit that phoebe's hybrid-aerocapture-aerobraking analysis says does not exist at conservative anchors. Both findings stand at their respective domains:

- Bus mass is NOT the architecturally-killing variable (enceladus-r5).
- Aerocapture IS the architecturally-killing variable (phoebe).

The matrix's prior "no engineering-closed cell" claim was wrong on its *attribution* (it blamed bus mass) but right on the bottom line (no cell closes when aerocapture is closed). The matrix's "architectural search space exhausted" claim was over-broad — what's exhausted is the architectural search at conservative bus + closed-aerocapture. The space at heritage bus + open-aerocapture has 9 candidate cells but they require a separate proof that aerocapture closes.

**This round does not run new physics.** It is a synthesis round that:

1. Adjudicates the matrix basis-of-record bus mass.
2. Decouples bus-mass closure from aerocapture closure as separate axes.
3. States the bus-mass-adjudicated reading of axis 02.
4. Identifies what would be required to also close the aerocapture-dependent question, so the project owner can decide whether to fund that work.

---

## Question this round answers

Three questions, one round:

**Q1.** What single bus-mass anchor should the matrix carry as basis-of-record? Cassini (~2 t bus, no shielding), Europa-Clipper-with-shielding (~5.5 t per enceladus-r5's own honest caveat), or a higher full-vehicle anchor?

**Q2.** Of the matrix axes' prior verdicts, which were genuinely bus-mass-anchored and need updating, versus which were aerocapture-anchored and stand under conservative aerocapture?

**Q3.** If aerocapture closure is the binding constraint (not bus mass), what is the deepest possible aerocapture analysis still open? Phoebe's R-hybrid-aerocapture-aerobraking used US Standard 1976 atmosphere, ice tensile 1.0 MPa, ballistic-correction-factor 0.4, body-absorbed 0.5. Are any of these conservatism choices over-tight? Is there a self-consistent set of more-generous-but-still-defensible anchors that flips the 0/1920 verdict?

---

## Pre-registered hypotheses (numeric ranges + falsification bands)

| # | Hypothesis | Predicted | Falsification band |
|---|---|---|---|
| **H1** | **Europa-Clipper-with-shielding (~5.5 t) is the right basis-of-record bus mass.** Cassini's 2-t anchor under-counts because it ignores radiation shadow shield + power-conversion-unit + cables that a 500-kilowatt-electric ICEBERG vehicle requires. Full-vehicle 15-23 t anchor over-counts because it conflates per-mission consumables with structural dry mass. 5.5 t is the median of enceladus-r5's own shielding-sensitivity result. | Adopt 5.5 t as basis-of-record; carry 2 t and 15 t as upper and lower brackets in sensitivity sweeps. | H1 falsified if (a) project owner directs a different anchor, OR (b) the shielding sensitivity is shown to be over-tight (e.g., 500-kilowatt-electric reactor can be designed to use bus structure as shadow geometry, dropping the explicit shield mass) and Cassini 2 t becomes defensible. |
| **H2** | **The "no engineering-closed cell" verdict (axis 02 prior) was bus-mass-anchored and is overturned.** At Europa-Clipper-with-shielding bus + 10 km/s aerocapture credit + 500-kilowatt-electric / 200-tonne chunk / 8-10 W/kg specific power, **at least 5 commercial+strict cells exist** (per enceladus-r5's shielding sensitivity 7/9 minus marginal sp=5 cells). | 5-9 surviving cells under Europa-Clipper-with-shielding anchor. | H2 falsified if (a) the shielding overhead is even more conservative than enceladus-r5 modelled and 0 cells survive at Europa-Clipper-anchor; OR (b) some other matrix axis (reactor lifetime, Saturn-side process power, B-ring rendezvous survivability) kills the cells that survive the bus-mass + aerocapture test. |
| **H3** | **The "architectural search space exhausted at worker level" verdict (latest+11 axis 02 claim, derived from phoebe pivot-survey 31/31 DEAD) is bus-mass-anchored on phoebe's choice of conservative bus.** Re-running phoebe's pivot-survey at Europa-Clipper-with-shielding bus would yield 2-7 candidates re-classifying from DEAD-ON-ARRIVAL to WORTH-DEEP-DIVE. | 2-7 candidates re-classify at heritage bus. | H3 falsified if phoebe's pivot-survey's kill criteria are not bus-mass-anchored (e.g., F2 B-ring crossing is geometric and doesn't care about bus mass; F6 reactor program is independent). If only 0-1 candidates re-classify, the "architectural search space exhausted" claim is robust to bus-mass anchor. |
| **H4** | **enceladus-r5's 9-cells finding is aerocapture-conditional.** Removing the 10 km/s aerocapture credit (aero=0) and re-running the 1920-cell sweep at Cassini bus yields 0 commercial+strict cells. | 0 cells at aero=0 / Cassini. | H4 falsified if any cell at aero=0 closes commercial+strict. Would imply bus-mass alone is the binding lever (a stronger claim than enceladus-r5 made). |
| **H5** | **phoebe's R-hybrid-aerocapture-aerobraking 0/1920 verdict is robust to the three most conservative anchors phoebe used.** Specifically: relaxing the ice tensile from 1.0 MPa to 2.0 MPa (still within laboratory-ice envelope) does NOT flip the pass-1 chunk-shatter failure mode. Relaxing ballistic-correction-factor from 0.4 to 0.6 does NOT flip the aerobraking timescale failure mode. Switching atmosphere model from US Standard 1976 to a real Earth-equator-thermosphere model (which has 2-3× density at 130 km) does NOT flip the sublimation failure mode. | 0/1920 holds under each single-axis relaxation. | H5 falsified if any single-axis relaxation flips the verdict. Would put the burden on phoebe (or a re-run) to demonstrate which anchor was actually load-bearing. |
| **H6** | **Aggregate verdict: bus mass and aerocapture are separately load-bearing axes; the matrix should carry both explicitly.** Bus-mass anchor: Europa-Clipper-with-shielding (~5.5 t) basis-of-record. Aerocapture anchor: phoebe's conservative-anchor 0/1920 stands as basis-of-record; an "aerocapture sensitivity" sub-axis flags H5 as the open question. Under both conservative anchors: 0 surviving cells (matrix axis 02 stands). Under heritage bus + open aerocapture: 5-9 surviving cells (a non-empty cell set, but requires aerocapture rescue). | H1-H5 all held; H6 follows mechanically. | H6 falsified if the bus-mass and aerocapture findings are not actually decoupled (e.g., shielding mass scales with aerocapture peak-q in a way that destroys the heritage-bus cells under heat-shield assumptions). |

---

## Method sketch (worker drafts `run.py` and `STUDY.md`)

1. **Read PRIMARY round verdicts** per methodology lesson 9: enceladus-r5 R-bus-mass-anchor-sweep STUDY.md + shielding_sensitivity.txt; phoebe R-hybrid-aerocapture-aerobraking STUDY.md + closure_verdict.md; phoebe R-mission-architecture-pivot-survey STUDY.md + closure_verdict.md. Document what anchors each round used; identify whether the bus mass appears in the round's parameter set or is an implicit downstream assumption.

2. **Re-run enceladus-r5's bus-mass-anchor sweep at aero=0** (Q1 cross-axis). 1920-cell sweep, identical to enceladus-r5's, but with `aerocapture_credit = 0 km/s` only. Count cells passing L0-05 strict AND L0-09 commercial floor. Pre-register 0 cells (H4).

3. **Re-classify phoebe's 31 pivot-survey candidates at heritage bus** (Q1 cross-axis). For each of phoebe's 31 candidates, walk through the 8 kill criteria and identify which criteria are bus-mass-anchored. For criteria that are bus-mass-anchored, re-test at Europa-Clipper-with-shielding (5.5 t). Aggregate count of re-classifications.

4. **Single-axis sensitivity sweeps on phoebe's R-hybrid-aerocapture-aerobraking** (H5). Re-derive the pass-1 chunk-shatter failure mode at ice tensile ∈ {1.0, 1.5, 2.0} MPa. Re-derive the aerobraking timescale at ballistic-correction-factor ∈ {0.4, 0.5, 0.6}. Re-derive the sublimation failure mode at atmosphere density {US Std 1976, US Std 1976 × 2, US Std 1976 × 3}. For each, count which periapsis-altitude × chunk-mass cells now close.

5. **Aggregate verdict.** Synthesize Q1 (Europa-Clipper-with-shielding = 5.5 t basis-of-record), Q2 (decoupled axes 02-bus-mass and 02-aerocapture-closure), Q3 (sensitivity-on-phoebe's-aerocapture-anchors as residual open question). Recommend matrix amendments.

---

## Out-of-scope for this round (declared)

- **New physics on Architecture E surviving cells.** This round does not validate or invalidate enceladus-r5's surviving cells; it determines whether the bus-mass attribution is the right framing.
- **New physics on aerocapture closure.** Single-axis sensitivity (H5) is in-scope; a full re-run of R-hybrid-aerocapture-aerobraking under relaxed anchors is out-of-scope (would be a separate SCOPE if H5 surfaces a flippable anchor).
- **L0-24 reactor-program-availability gate.** Independent of bus mass; iapetus chain settled this.
- **Pricing anchor.** Independent of bus mass; R-pricing-anchor-revisit covers it.

---

## Methodology lesson dependencies

- **Lesson 1** (pessimistic-prediction default). H1 picks 5.5 t (median) not 2 t (optimistic); H5 retains conservative anchors as basis-of-record and only sensitivity-sweeps one axis at a time.
- **Lesson 7** (compute under most pessimistic credible anchor first). Adopt 5.5 t + closed aerocapture as the matrix's pessimistic-anchor reading; heritage-bus + open-aerocapture is the upside-only reading.
- **Lesson 9** (anchor-from-PRIMARY-text). The two PRIMARY rounds are enceladus-r5 R-bus-mass-anchor-sweep and phoebe R-hybrid-aerocapture-aerobraking. Cite both verbatim in the round's STUDY.md.
- **Lesson 11** (robustness-by-magnitude vs robustness-by-cancellation). H5 explicitly tests whether phoebe's 0/1920 is robust-by-magnitude (relaxing any single anchor still gives 0) or robust-by-cancellation (the three failure modes balance such that relaxing one makes another binding).
- **Lesson 13** (robust-to-single-axis vs robust-to-joint-axis). H5 is single-axis only. A joint-axis relaxation of all three anchors at once is out-of-scope here; flagged as follow-on if H5 surfaces a flippable single axis.
- **Candidate lesson 14** (conditional-axis stripping discipline). enceladus-r5's 9-cells finding inherits the 10 km/s aerocapture credit as a charitable conditional axis. H4 tests the without-stripping reading.

---

## Worker assignment

This SCOPE is a synthesis round — broad and rule-based; very little new code. Either a fresh worker (any moon) or enceladus-r5 on resume (would naturally extend their own bus-mass-anchor work).

Expected effort: ~1 session. Produces `STUDY.md` pre-registration, `run.py` for the three sub-sweeps (aero=0 re-run, phoebe-pivot-survey re-classification, single-axis aerocapture sensitivity), `results/closure_verdict.md` aggregate.

---

## Matrix axes touched

- **Axis 02 (Surviving cell)** — directly. The latest+12 retraction of "architectural search space exhausted" is hardened or softened per this round's findings.
- **Axis 11 (Earth-arrival mode)** — H5 may surface single-axis relaxations of phoebe's R-hybrid-aerocapture-aerobraking that flip the verdict.
- **Axis 19 (Capture architecture)** — heritage-bus surviving cells assume hybrid aerocapture; this round establishes whether that conditionality is hardened or open.
- **New sub-axis: bus-mass anchor.** This round produces a basis-of-record bus mass that the matrix can carry as a top-line parameter.

---

## What "done" looks like

Three-paragraph decision-frame for project-owner decision #14:

- **Bus-mass anchor of record:** Europa-Clipper-with-shielding ~5.5 t (or another value if H1 is falsified).
- **Architectural search space at conservative bus + closed aerocapture:** still exhausted (latest+11 reading stands).
- **Architectural search space at heritage bus + open aerocapture:** 5-9 candidate cells; binding question shifts from bus mass to aerocapture closure; H5 verdict identifies whether phoebe's aerocapture closure is robust-by-magnitude or has a single-axis flippable anchor.

If H5 surfaces a flippable single axis, the next critical-path round is a re-run of R-hybrid-aerocapture-aerobraking under the relaxed anchor. If H5 confirms phoebe's verdict is robust, the matrix axis 02 reading stabilises as "anchor-conditional surviving cells; no realisation path absent aerocapture rescue."
