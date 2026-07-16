# R-A14-engineering-decomposition — replace the desk-study chunk-capture sub-step probabilities with engineering-anchored ones

**Worker:** hyperion. **Date:** 2026-05-22. **Status:** complete.
**Round type:** engineering decomposition + flight-heritage base-rate analysis + bag-material cruise-duration modeling + Bayesian conjunction.
**Bet audited:** #1 of the three engineering bets (active chunk capture at scale). Structurally parallel to R-kilopower-scale-up-credibility (`3529984`, bet #3, this session).

---

## Why this round

A14 chunk-capture efficiency is the single most load-bearing assumption in the mission_graph framework (locked belief `31a13abb`). The Saturn-worker bottoms-up decomposition — rendezvous 0.90 × deployment 0.95 × catch 0.80 × containment 0.70 × survive 0.95 = **0.455 joint** — was a desk-study placeholder, each sub-step an honest guess with no flight-heritage anchor. The matrix closure verdict pivots on whether the true joint is above or below the closure threshold:

- 200 t chunk × cap_eff × 27.7% downstream efficiency = delivered mass.
- **25 t floor (L0-04 provisional) → cap_eff ≥ 0.451.**
- **30 t floor (L0-09) → cap_eff ≥ 0.542.**

The placeholder 0.455 sits one part in a thousand above the 25 t threshold — too close to adjudicate with guesses. This round replaces the guesses with engineering-anchored probabilities + uncertainty brackets.

---

## Pre-registered hypotheses (frozen before the heritage fetch; authored in SCOPE by Saturn, graded here)

| # | Prediction | Measured (mid) | Grade |
|---|---|---|---|
| H1 | Rendezvous 92–97% (OSIRIS-REx + Hayabusa2 + Hayabusa proximity-ops 3/3, small Saturn de-rate) | 0.93 (bracket 0.88–0.97) | **HELD** |
| H2 | Deployment 92–97% (LOFTID + JWST sunshield deployable heritage) | 0.94 (0.90–0.97) | **HELD** |
| H3 | Catch splits by velocity: 85–95% at mm/s, 60–75% at m/s | mm/s 0.88; high-m/s 0.65; low-m/s 0.78 | **HELD** |
| H4 | Containment is weakest link: 75–85% at mm/s, 50–65% at m/s | mm/s 0.78; high-m/s 0.55 | **HELD** |
| H5 | Survive 75–90% (lower than desk 95%) | 0.88 (0.80–0.93), redundant cinch | **HELD** (driver is cinch fatigue, not sublimation) |
| H6 | Joint 50–65% at mm/s; 25–40% at m/s. Closure exists but conditional and sensitive. | mm/s mid **0.528**; low-m/s mid 0.41; high-m/s mid 0.28 | **HELD** |

**All six held.** Unlike the companion bet-#3 round (where H2/H3 falsified), the A14 pre-registration was accurate — Saturn's velocity-conditional framing was the right structure.

---

## Method

`run.py`, deterministic. Five sub-step probabilities, each a (low, mid, high) bracket anchored on the input documents:

- **Heritage base rates** (`inputs/heritage_base_rates.csv`): OSIRIS-REx (Bennu, success, 121.6 g returned), Hayabusa2 (Ryugu, success, ~5.4 g, two touchdowns), Hayabusa (Itokawa, proximity success / acquisition partial) → rendezvous. LOFTID (2022, inflatable deployed, 8 km/s reentry, recovered) + JWST sunshield (344 single-point failures, all survived) → deployment.
- **Catch-velocity envelope** (`inputs/catch_velocity_envelope.md`): the pitch's mm/s closing velocity is the co-orbital drift velocity at ~100 m station-keeping (≈8 mm/s in the B-ring) — physically achievable, but not yet demonstrated on a tumbling target at Saturn's 70–90-min light-time. Realistic autonomy pushes the operating point to ~0.3 m/s (low-m/s) or ~1 m/s (high-m/s). Catch is geometry (aperture crossing); containment is energy (∝ v²), so containment degrades faster with velocity and is the load-bearing weakest link.
- **Bag cruise-duration model** (`inputs/bag_cruise_duration_model.md`): survive = puncture × sublimation × cinch. Puncture ~0.98 (a bag tolerates pinholes; only gross tears matter; flux at 9 AU is low). **Sublimation ~0.995 — benign**: at the ~90–100 K passive cruise temperature, water-ice recession is sub-mm over 13 years (<1 molecule/cm²/hr below 70 K; no measurable loss at 100 K over days). **Cinch fatigue ~0.93 (redundant) is the actual driver** — a 13-year continuously-loaded, deeply thermal-cycled lockout mechanism, with no flight heritage; redundancy (k-of-n cinches) is the mitigation.

Joint posterior computed across the full grid: closing velocity {mm/s, low-m/s, high-m/s} × cinch {single, redundant} × bracket {low, mid, high}. Each joint mapped to capture efficiency, multiplier of the 0.85 desk anchor, and closure against the 25 t / 30 t thresholds. Demonstrator-retirement (Step 6) and iapetus re-gating (Step 7) in separate result docs.

---

## Results

### Joint posterior sensitivity (selected; full table in `results/joint_posterior_sensitivity.csv`)

| velocity | cinch | bracket | joint | ×0.85 | closes 25 t? | closes 30 t? |
|---|---|---|---:|---:|:--:|:--:|
| mm/s | redundant | low | 0.399 | 0.47 | no | no |
| **mm/s** | **redundant** | **mid** | **0.528** | **0.62** | **YES** | no |
| mm/s | redundant | high | 0.684 | 0.80 | YES | YES |
| low-m/s | redundant | mid | 0.408 | 0.48 | **no** | no |
| high-m/s | redundant | mid | 0.275 | 0.32 | no | no |

- **Placeholder joint 0.455** vs **engineering mm/s-mid 0.528** — the desk study was *pessimistic* at mm/s by ~7 points, but the placeholder did not name the velocity regime it implicitly assumed.
- **The closure is razor-thin and regime-gated.** At mm/s, the mid joint (0.528) clears the 25 t floor (0.451) but not the 30 t floor (0.542). One regime step down — to realistic low-m/s autonomy — drops the mid joint to 0.408 and **fails the 25 t floor**. Closure exists only in the mm/s regime at mid-or-better brackets.
- **Cinch redundancy is a small but real lever** (mm/s mid: 0.510 single → 0.528 redundant). It matters more at the low brackets where it can be the difference at the threshold.

### Demonstrator-conditional joint

With an Earth-orbit catch-and-contain demonstrator (retires deployment + catch + containment at mm/s) and a Saturn small-chunk mission-1 (retires rendezvous), 13-yr survive held un-retired: **joint = 0.694**, clears both the 25 t and 30 t floors. (Above the orchestrator thread-walk's ~0.58; the qualitative conclusion — A14 is no longer binding once both demonstrators succeed — is robust to conservative re-crediting.)

---

## Reading (load-bearing, per H6)

**Closure at the matrix-canonical 200 t chunk EXISTS but is conditional and razor-thin.** The engineering-anchored joint at the pitch-nominal mm/s closing velocity (0.528 mid) clears the 25 t commercial floor — but only at mm/s, only at mid-or-better brackets, and it does *not* clear the 30 t L0-09 floor. The moment the closing-velocity operating point rises to the realistic low-m/s autonomy regime, the 25 t floor fails. **The entire A14 closure pivots on one demonstrable fact: can the system achieve mm/s catch-and-contain on a non-cooperative tumbling target?**

This relocates the A14 question from "is 0.85 right?" (it is not — the honest mm/s mid is 0.53, a 0.62 multiplier of the desk anchor) to **"is the operating point mm/s or low-m/s?"** That is exactly what an Earth-orbit catch-and-contain demonstrator retires, cheaply, before any Saturn commitment. The decomposition's value is not the point estimate; it is identifying that **containment-at-velocity is the load-bearing sub-step and a ground-cheap demonstrator collapses its uncertainty.**

Two corrections to the desk study worth carrying forward:
1. **Containment (0.70 → 0.78 at mm/s, 0.55 at high-m/s) is velocity-conditional**, not a fixed number. The desk 0.70 was pessimistic at mm/s and optimistic at high-m/s.
2. **Survive (0.95 → 0.88) is cinch-fatigue-dominated, not mass-loss-dominated.** The desk study implicitly feared sublimation; at cold passive cruise that is negligible. The real residual is a 13-year thermal-cycled cinch, mitigated by redundancy, un-retirable by any demonstrator.

**Recommended replacement for the mission_graph framework:** replace the single 0.85 anchor with a velocity-conditional capture efficiency: 0.53 (mm/s, un-demonstrated), 0.41 (low-m/s), 0.69 (mm/s, demonstrator-confirmed). The matrix should carry the 200 t closure cell as **demonstrator-conditional**, not as a standing 0.85.

---

## Revisit (mandatory)

**All six hypotheses held — the SCOPE pre-registration was accurate**, in contrast to the companion R-kilopower round where two hypotheses falsified. Why the difference? The A14 SCOPE pre-registered a *velocity-conditional structure* (catch/containment split by closing velocity) rather than single point estimates, and that structure was correct — the conditioning variable (closing velocity) really is what the joint pivots on. The kilopower SCOPE, by contrast, imported a failure-mode analogy across power classes that did not scale. **Lesson: pre-registering the right conditioning structure matters more than pre-registering the right point estimate.** A velocity-conditional hypothesis that brackets each regime is robust; a single-point hypothesis that omits the conditioning variable is fragile.

**Where I could be wrong.** (1) The mm/s vs low-m/s operating point is an autonomy-engineering judgment, not measured — the whole closure hinges on it, which is precisely why the demonstrator is the right next step rather than more desk analysis. (2) The cinch single-mechanism failure band (5–15% over 13 yr) has no flight heritage; it is anchored on general deployable-mechanism reliability and could be argued either way — redundancy makes the joint robust to it. (3) Sub-step independence is assumed (joint = product); a common-cause failure (e.g., a contamination event that degrades both catch and containment) would correlate them and lower the joint. (4) The demonstrator-conditional 0.69 caps confirmed sub-steps at 0.92–0.95; a believer in perfect demonstrator retirement would go higher, a skeptic lower — but it clears the threshold across that range.

**Methodology-lesson candidate (hyperion, awaiting project-owner ratification):** *pre-register the conditioning structure, not just the point estimate.* When a quantity is suspected to depend on an operating variable (here, closing velocity), the hypothesis should bracket each regime of that variable rather than guess a single number. A single-point pre-registration silently bakes in an unstated regime assumption (the desk 0.70 containment baked in an unnamed velocity), and is fragile to it; a regime-conditional pre-registration surfaces the dependence and is the robust form. Compounds with the kilopower round's candidate lesson (do not import a failure mode across regimes without re-checking scaling) — both are about making the regime-dependence explicit.

---

## Cross-learning

- **Replaces the desk-study A14 decomposition** (Saturn-worker `030cb5e`, locked belief `31a13abb`): the honest joint is velocity-conditional — 0.53 (mm/s, un-demonstrated) / 0.41 (low-m/s) / 0.69 (demonstrator-confirmed), not a standing 0.85 or 0.46. The matrix's 200 t closure cell is **demonstrator-conditional**.
- **Feeds iapetus staged-options re-gating** (`results/iapetus_staged_options_re_gating.md`): bet #1 (chunk capture) retires via an internal, ICEBERG-controllable demonstrator, not an external award. Combined with R-kilopower-scale-up-credibility (bet #3 reactor moves off the critical path), the tranche-1 gate should be re-cast from "FSP-2 award" to "Earth-orbit catch-and-contain + continuous water-electrothermal demonstrators." Matrix decision #13 input.
- **Surfaces bet #2 (continuous water-electrothermal at flight scale) as the highest-leverage un-audited bet.** Both bet #1 (this round) and bet #3 (R-kilopower) now have dedicated audits; bet #2 has only the Saturn-worker A1 PLAUSIBLE-PROVISIONAL finding. It is the hardest part of the proposed tranche-1 demonstrator and lacks its own round.
- **Highest-leverage demonstrator action identified:** an Earth-orbit catch-and-contain test with deployable target masses retires the three weakest/cheapest sub-steps (deployment, catch, containment) and directly tests the mm/s-vs-low-m/s closing-velocity question the whole joint pivots on. Feeds the R-demonstrator-mission-concept SCOPE.

---

## Files

- `run.py` — sub-step brackets + joint sensitivity grid + demonstrator-conditional + closure thresholds. Deterministic.
- `inputs/heritage_base_rates.csv`, `inputs/catch_velocity_envelope.md`, `inputs/bag_cruise_duration_model.md` — Steps 1–3.
- `results/per_substep_probabilities.csv`, `results/joint_posterior_sensitivity.csv`, `results/summary.json` — Steps 4–5.
- `results/demonstrator_retirement_analysis.md`, `results/iapetus_staged_options_re_gating.md` — Steps 6–7.
- `READING.md` — load-bearing reading + recommended framework/matrix amendments.
