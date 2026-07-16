# R-water-electrothermal-flight-scale-audit — bet #2: continuous water-electrothermal at flight scale on Saturn-water purity

**Worker:** hyperion. **Date:** 2026-05-22. **Status:** complete.
**Round type:** flight-gap audit + cross-round reconciliation + reliability conjunction. Worker-authored SCOPE (no orchestrator SCOPE existed).
**Bet audited:** #2 of three (continuous water-electrothermal at flight scale). Completes the bet #1 (R-A14) / #2 (this) / #3 (R-kilopower) audit set, all this session.

---

## Why this round

Locked finding 5 names three engineering bets; #2 was the only one without a dedicated audit. The Saturn-worker A1 finding (locked `650938e3`) rated water-electrothermal 800 s PLAUSIBLE-PROVISIONAL with three flight gaps (ground→flight, pulse→continuous, clean→Saturn-water) but did not quantify them. This round quantifies the gaps, reconciles two cross-round tensions, and classifies how bet #2 fails relative to bets #1 and #3.

---

## Pre-registered hypotheses (frozen before computation; graded here)

| # | Prediction | Measured | Grade |
|---|---|---|---|
| H1 | Continuous-flight water-MET Isp on Saturn water is 500–700 s, below the 800 s ground/pulse anchor | R0-anchored bracket 500 / 575 / 700 s | **HELD** |
| H2 | At realistic continuous MET Isp, matrix closure <2% | 0.0% (low/mid) – 0.5% (high); 800 s ground anchor would give 4% | **HELD** |
| H3 | RF-ion continuous-months flight-readiness conjunction 0.3–0.6 absent a demonstrator | 0.25 / **0.48** / 0.73 | **HELD** (mid 0.48 in band; low 0.25 well above the <0.15 falsifier) |
| H4 | Cumulative-operating-time flight gap ≥100× | 144× (6 mo) to 1461× (5 yr) | **HELD** |
| H5 | Bet #2 fails differently from #1/#3: physics works (Vigoride proved it in pulses) but the matrix-closing Isp belongs to the contamination-SENSITIVE RF-ion architecture whose continuous-months-on-Saturn-water operation is flight-unproven | reading-level | **HELD** |

All five held.

---

## Method

`run.py`, deterministic. (1) MET continuous-flight effective Isp (anchored on R0 frozen-flow, **not** the 800 s ground/pulse anchor) mapped to matrix closure via the locked A1 closure sensitivity (0% @600 s, 0.5% @700 s, 4% @800 s, 12% @900 s, 30 t floor; piecewise-linear). (2) RF-ion (2000 s) continuous-months flight-readiness as a three-factor conjunction anchored on R11 (bag silicate rejection) and R-MET-cathode-escape-hatch (cathode/grid life). (3) Flight-gap cumulative-operating-time ratio vs the closest flown precedent. Heritage in `inputs/flight_heritage.csv`.

---

## Results

### MET branch (contamination-tolerant, no electrodes/grids in plume)

| Isp regime | Isp (s) | Matrix closure (30 t floor) |
|---|---:|---:|
| ground / clean / ~50 s-pulse anchor (A1) | 800 | 4.0% |
| continuous-flight low | 500 | 0.0% |
| continuous-flight mid | 575 | 0.0% |
| continuous-flight high | 700 | 0.5% |

The contamination-tolerant architecture (water-MET) **does not reach matrix-closing Isp at realistic continuous-flight conditions.** Even the optimistic 700 s continuous-flight high gives 0.5% closure; the campaign's R0-realistic 500–575 s gives 0%. The 800 s figure that yields 4% is a ground/clean/short-pulse number, not a continuous-flight-on-Saturn-water number.

### RF-ion branch (Isp-sufficient at 2000 s, contamination-SENSITIVE)

RF-ion at 2000 s **closes the matrix on Isp** (it is what the titan-3 / mission_graph closure cells actually run). The bet is its **continuous-months flight-readiness on Saturn water**, a conjunction of three reliability factors:

| Factor | low | mid | high | anchor |
|---|---:|---:|---:|---|
| bag silicate rejection holds over burn | 0.65 | 0.80 | 0.90 | R11 (negligible nominal wear; 18 mo to grid failure under bag-thermal failure) |
| cathode/grid life ≥ multi-year burn | 0.65 | 0.80 | 0.92 | R-MET-cathode-escape-hatch (Wang-pessimistic 3000 hr; Dawn ≤1%/swap; grid >7 yr nominal) |
| no continuous-operation anomaly over months | 0.60 | 0.75 | 0.88 | Vigoride pulse-only flight heritage; V-3 difficulties |
| **joint flight-readiness** | **0.25** | **0.48** | **0.73** | |

### Flight gap (cumulative operating time)

Closest flown precedent ≈ 30 hr (Vigoride-5 35 pulse firings of varying durations; AQUARIUS deep-space resistojet). ICEBERG inbound continuous burn: **144×** (a conservative 6-month continuous) to **1461×** (a representative 5-year mission burn). The flight gap is 2–3 orders of magnitude in cumulative thrust-on time.

---

## Reading (load-bearing, per H5)

**Bet #2 fails differently from bets #1 and #3 — and the failure is an architecture trap, not a physics wall.**

Water electrothermal propulsion *works in space*: Vigoride-5 raised its orbit >3 km with a water MET in 2023, and AQUARIUS ran a water resistojet in deep space. The physics is flight-proven — **in pulses, on distilled water, at sub-100-to-few-hundred-second Isp.** That is the regime that has flown. ICEBERG needs a different regime in three independent ways, and the three are not separable from the architecture choice:

1. **The contamination-tolerant architecture (MET) cannot reach matrix-closing Isp.** At realistic continuous-flight Isp (R0's 500–650 s), MET delivers 0–0.5% matrix closure. MET tolerates Saturn-water silicates (no electrodes/grids in the plume) but tops out ~150 s *below* the 800 s anchor that already only gives 4%. **The locked A1 800 s anchor is a ground/clean/pulse figure above the campaign's own continuous frozen-flow ceiling (R0); it should not be carried as a continuous-flight number.**

2. **The Isp-sufficient architecture (RF-ion, 2000 s) is the contamination-SENSITIVE one.** It closes the matrix on Isp — but its continuous-months operation on Saturn water depends on the bag's sublimation-distillation silicate rejection holding for the entire multi-year burn (R11: negligible wear *under nominal bag operation*; 18 months to grid failure if bag thermal control fails) **and** on cathode/grid life covering the burn. The joint continuous-months flight-readiness is **0.48 (mid), 0.25–0.73 (range)** — not a physics impossibility, but an un-flown reliability conjunction.

3. **The flight gap is 2–3 orders of magnitude in cumulative operating time** (144–1461×). No pulse-mode demonstration retires a months-continuous reliability question.

**So bet #2 is not "fantasy-conditioned" like the 500-kWe reactor (bet #3 mass), nor "razor-thin and velocity-gated" like chunk capture (bet #1).** It is an **architecture trap**: the contamination-tolerant thruster doesn't reach the needed Isp, and the Isp-sufficient thruster is contamination-sensitive and flight-unproven for continuous-months operation on dirty water. The matrix's propulsion cell silently assumes the RF-ion 2000 s case *and* that its continuous-months-on-Saturn-water reliability holds — a ~0.48 conjunction it does not price.

**The matrix should carry the propulsion cell as demonstrator-conditional on a continuous-months water-RF-ion (or MET) run on chunk-purity water in deep space** — exactly the experiment the Saturn-worker A1 finding already named as the single highest-leverage demonstrator objective. This round quantifies *why*: it is the only thing that retires both the duration gap (144–1461×) and the bag-rejection-holds-for-months factor (the largest single driver of the 0.48 conjunction).

---

## Revisit (mandatory)

All five hypotheses held. Like R-A14 (and unlike R-kilopower), the pre-registration was accurate — because, as in R-A14, the hypotheses pre-registered the **conditioning structure** (MET-vs-RF-ion architecture branch; the three reliability factors) rather than a single point estimate. This is the third data point for the candidate methodology lesson (*pre-register the conditioning structure, not just the point estimate*): the two rounds that conditioned on the right structural variable (R-A14 on closing velocity, this round on thruster architecture) graded clean; the round that imported a single-regime analogy (R-kilopower H2/H3) falsified.

**Cross-round tension resolved, and it is a finding for the project owner:** the locked A1 belief's 800 s anchor (a) exceeds the campaign's own R0 continuous frozen-flow ceiling (~700–750 s), and (b) is not the Isp the closure cells run on (they use 2000 s RF-ion). The "bet #2 = water-electrothermal at 800 s" framing in locked finding 5 is therefore partly mis-specified: the live bet is RF-ion-continuous-on-Saturn-water reliability, with MET as a contamination-tolerant fallback that does not reach matrix-closing Isp. (Both are user-locked beliefs; surfaced for project-owner update, not silently rewritten.)

**Where I could be wrong.** (1) The 30 hr flown-precedent anchor is a conservative estimate of Vigoride-5 + AQUARIUS cumulative thrust-on; if Vigoride-5's 35 firings were long-duration, the gap narrows — but stays ≥100×. (2) The three RF-ion reliability factors are engineering judgments anchored on adjacent campaign rounds, not measured continuous-months data — which is precisely the point (no such data exists; that is the bet). (3) I treated the factors as independent; a common-cause failure (bag thermal control loss → both silicate flooding *and* anomaly) would correlate them and lower the joint below 0.48.

---

## Cross-learning

- **Completes the three-engineering-bets audit set** (locked `5535179f`): bet #1 (R-A14, `fd6fab0`) razor-thin/velocity-gated; bet #2 (this) architecture-trap, demonstrator-conditional; bet #3 (R-kilopower, `3529984`) mass-robust but programmatically near-zero. Each fails in a different way, as locked finding 5 predicted — this round confirms and characterizes the third failure mode.
- **Reconciles locked A1 (`650938e3`) with R0 frozen-flow:** the 800 s anchor is ground/clean/pulse; continuous-flight is 500–700 s. Recommend the framework carry continuous-flight MET Isp at R0's 500–650 s, not 800 s.
- **Surfaces the matrix propulsion-cell mis-specification:** closure cells run 2000 s RF-ion, not 800 s MET; the matrix should price the RF-ion continuous-months-on-Saturn-water flight-readiness conjunction (~0.48) rather than treat 2000 s as free.
- **Feeds R-demonstrator-mission-concept:** the continuous-months water-thruster-on-chunk-water run is the bet-#2 retirement and the highest-leverage demonstrator objective (Saturn-worker A1 + this round). Pair with the Earth-orbit catch-and-contain demonstrator (bet #1, R-A14) for the tranche-1 gate; the reactor (bet #3) stays off the critical path.

---

## Files

- `SCOPE.md` (worker-authored), `run.py`, `inputs/flight_heritage.csv`, `results/summary.json`, `READING.md`.
