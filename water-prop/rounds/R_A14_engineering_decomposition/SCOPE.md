# R-A14-engineering-decomposition — replace the desk-study chunk-capture sub-step probabilities with engineering-anchored ones

**Status:** scope, pre-study. Authored by Saturn (orchestrator), 2026-05-22 latest+16, during project-owner-directed thread-walk ("question our assumptions and test our hypotheses").

---

## Why this round

The Saturn-worker assumption audit (`030cb5e`, 2026-05-21) identified A14 chunk-capture efficiency as the single most load-bearing assumption in the mission_graph framework (locked belief `31a13abb`). The bottoms-up decomposition Saturn-worker used was rendezvous 90 percent × deployment 95 percent × catch 80 percent × containment 70 percent × structural survival 95 percent = ~46 percent joint success. That decomposition is itself a desk-study placeholder — each sub-step probability was an honest guess, not anchored against flight heritage or engineering test data.

Orchestrator analysis during the 2026-05-22 thread-walk surfaced two structural concerns with the placeholder decomposition:

1. **The 46 percent joint sits 5 percentage points below the ~45 percent threshold needed to deliver 25 tonnes from a 200-tonne chunk** (given the framework's ~27.7 percent downstream efficiency from chunk-fed-spiral + Earth-arrival). The matrix closure verdict pivots on whether the true joint is above or below ~45 percent. Placeholder probabilities cannot adjudicate that.
2. **The two weakest sub-steps (containment 70 percent + survive 95 percent over 13 years) are the load-bearing ones, but their placeholder numbers are not defensible.** Containment 70 percent assumes a higher catch velocity than the architecture (mm/s closing per pitch text) actually uses. Survive 95 percent over 13 years does not model bag-material cruise-duration tax explicitly.

This round replaces the placeholder probabilities with engineering-anchored ones derived from flight heritage + cruise-duration physics. Output is a per-sub-step probability with explicit uncertainty bracket + joint posterior with sensitivity table.

**Round type:** engineering decomposition + flight-heritage base-rate analysis + bag-material cruise-duration modeling. Primary research load: pull flight heritage data for OSIRIS-REx + Hayabusa2 proximity ops, LOFTID + James Webb Space Telescope sunshield deployment, micrometeoroid puncture statistics for soft-fabric bag materials at ~9 AU heliocentric distance.

---

## The five sub-steps to anchor

| # | Sub-step | Saturn-worker placeholder | Engineering-heritage anchor target |
|---|---|---:|---|
| 1 | Rendezvous with the target chunk at Saturn | 90 percent | OSIRIS-REx (Bennu, 2018-2023, successful) + Hayabusa2 (Ryugu, 2018-2019, successful) + Hayabusa (Itokawa, 2005, partial) base rate. Modulate for Saturn-system specifics (longer light-time autonomy, ring-particle proper motion). |
| 2 | Deployment of the trawl bag mechanism | 95 percent | LOFTID (Low-Earth Demonstration of Inflatable Decelerator Technology, 2022, successful) + James Webb Space Telescope sunshield (2022, successful, 344 single-point failures, all survived). Modulate for bag-specific mechanism complexity. |
| 3 | Catch (chunk enters the bag) | 80 percent | Novel; no direct heritage. Anchor on closing-velocity sensitivity (mm/s per pitch text vs higher-velocity asteroid sample acquisition). Document the catch envelope explicitly. |
| 4 | Containment (chunk stays in the bag after catch) | 70 percent | Bag tear / cinch failure / chunk fragmentation modes. Anchor on bag-material tensile strength + chunk-mass impact-energy + cinch mechanism reliability under deployment-fatigue. Decompose containment into sub-failure modes with per-mode probability. |
| 5 | Structural survival of the bagged chunk over the 13-year cruise | 95 percent | Micrometeoroid puncture rate at ~9 AU (much lower than Earth-vicinity but non-zero) + sublimation rate of water ice at bag-internal-temperature × cruise duration + cinch integrity over thermal-cycling × 13 years. Decompose survive into puncture / sublimation / cinch sub-failure modes. |

---

## Pre-registered hypotheses (worker's honest predictions)

| # | Hypothesis | Predicted range | Falsification band |
|---|---|---|---|
| H1 | Rendezvous probability (sub-step 1) at engineering-heritage anchor is 92-97 percent. OSIRIS-REx + Hayabusa2 base rate is ~100 percent for proximity (2 of 2 successful at Bennu / Ryugu); Saturn-system-specific autonomy de-rate is small (~2-5 percentage points) for a target with characterized orbit. | 92-97 percent. | H1 falsified if anchored rendezvous probability < 88 percent or > 99 percent. |
| H2 | Deployment probability (sub-step 2) at engineering-heritage anchor is 92-97 percent. LOFTID + James Webb Space Telescope sunshield base rate is 2 of 2 successful for deployable space hardware in the relevant complexity class. Bag mechanism is more complex than LOFTID and less than the sunshield. | 92-97 percent. | H2 falsified if anchored deployment probability < 85 percent or > 99 percent. |
| H3 | Catch probability (sub-step 3) at engineering-heritage anchor splits sharply by closing-velocity regime. At mm/s (pitch-text-quoted) closing velocity, catch probability is 85-95 percent (low-energy collision; bag aperture margins large relative to chunk cross-section). At m/s closing velocity (more realistic for autonomous proximity ops on a rotating particle), catch probability drops to 60-75 percent. The round produces a closing-velocity-sensitivity table, not a single point estimate. | 60-95 percent across the closing-velocity envelope. | H3 falsified if catch probability is below 50 percent or above 98 percent at any closing-velocity-feasible operating point. |
| H4 | Containment probability (sub-step 4) is the weakest engineering link. Bag-tear + cinch-failure + chunk-fragmentation joint probability at mm/s closing velocity is 75-85 percent; at m/s closing velocity drops to 50-65 percent (chunk fragments transfer momentum to bag in ways the soft-fabric / aerogel layer may not absorb cleanly). | 50-85 percent across the closing-velocity envelope. | H4 falsified if containment probability is above 92 percent at any closing-velocity-feasible operating point, OR is below 40 percent at any operating point. |
| H5 | Structural survival over 13-year cruise (sub-step 5) is 75-90 percent — lower than the desk-study 95 percent. Micrometeoroid puncture at ~9 AU is ~0.5-2 percent over 13 years for a representative bag area + material. Sublimation rate at bag-internal-temperature is ~1-5 percent of chunk mass over 13 years (Saturn-ring ice at ~70 K internally, but bag thermal regulation is uncertain). Cinch-mechanism thermal-cycling fatigue over 13 years is a non-trivial reliability driver (5-15 percent failure probability for a single cinch; redundant cinches improve substantially). | 75-90 percent. | H5 falsified if anchored cruise-survival probability is above 95 percent or below 65 percent under defensible bag-design anchors. |
| H6 (load-bearing reading) | Joint posterior probability at the matrix-canonical chunk-size (200 tonnes, mm/s closing velocity) is 50-65 percent — above the ~45 percent closure threshold but well below the 0.85 desk-study anchor. **Closure exists but is conditional and sensitive.** At m/s closing velocity (worst credible), joint drops to 25-40 percent — below threshold. The architectural reading is that closing the matrix at 200-tonne chunks requires demonstrator-confirmed mm/s-closing-velocity catch with high cinch reliability and bag-material cruise-duration survive. | 50-65 percent at mm/s; 25-40 percent at m/s. | H6 falsified if joint posterior at mm/s is below 40 percent (closure does not exist even with best-credible engineering) OR above 75 percent (closure exists without conditioning on the demonstrator). |

---

## Method (worker drafts the actual implementation)

**Step 1 — Heritage base-rate fetch.**

- OSIRIS-REx (Bennu): mission timeline, proximity-ops success rate, sample-acquisition Touch-and-Go (TAG) outcome (returned 121.6 grams 2023). Reference: NASA / Lockheed Martin OSIRIS-REx post-mission reports.
- Hayabusa2 (Ryugu): mission timeline, proximity-ops, sample-acquisition Small Carry-on Impactor (SCI) + two TAG sequences (returned 5.4 grams 2020). Reference: JAXA Hayabusa2 mission reports.
- Hayabusa (Itokawa, 2005): proximity ops successful; sample acquisition partial. Reference: JAXA Hayabusa post-mission report.
- LOFTID (Low-Earth Demonstration of Inflatable Decelerator Technology, 2022): single-test deployment success. Reference: NASA LOFTID post-flight report.
- James Webb Space Telescope (sunshield deployment, 2022): 344 single-point failures, all survived. Reference: NASA / Northrop Grumman post-deployment reports.

**Step 2 — Catch-velocity sensitivity analysis.** Reproduce the pitch's mm/s closing-velocity claim from the trawl mechanism + radial-drift orbital geometry. Identify what the realistic closing-velocity envelope is given autonomous-proximity-ops uncertainty on a rotating ring particle. Produce a closing-velocity sensitivity table for sub-steps 3 (catch) and 4 (containment).

**Step 3 — Bag-material cruise-duration model.** For a representative bag material (Vectran-aerogel composite per pitch text; sensitivity sweep across Vectran-only, Vectran-aerogel, Kevlar-aerogel, etc.):

- Micrometeoroid puncture rate at ~9 AU heliocentric × 13-year cruise × representative bag area (~200 m^2 for a 200-tonne chunk geometric envelope). Reference: existing micrometeoroid environment models (NASA Meteoroid Engineering Model, ESA MASTER).
- Sublimation rate at bag-internal-temperature (~70 K for passively-thermal-regulated bag at 9 AU; warmer if active thermal control is needed). Reference: water-ice sublimation physical-chemistry literature.
- Cinch-mechanism thermal-cycling fatigue over 13 years. Reference: deployable-mechanism reliability literature; single-cinch vs redundant-cinch comparison.

**Step 4 — Per-sub-step probability + uncertainty bracket.** For each of the five sub-steps, produce a point estimate AND an uncertainty bracket (low / mid / high), anchored on Step 1-3 outputs. Document the engineering reasoning per sub-step. The brackets matter as much as the point estimates — the joint posterior is what the matrix consumes.

**Step 5 — Joint posterior + sensitivity table.** Compute joint posterior at each of (mm/s, low-m/s, high-m/s) closing velocity × (low, mid, high) cinch-reliability × (low, mid, high) bag-material-survival. Produce a sensitivity table the matrix can consume. Identify which joint cells close at L0-04 = 25 tonnes vs which collapse.

**Step 6 — Demonstrator-mission retirement analysis.** For each of the five sub-steps, document what demonstrator-mission profile retires the uncertainty:
- Earth-orbit demonstrator: retires deployment + catch + containment cheaply (3 of 5 sub-steps).
- Saturn small-chunk demonstrator (mission 1): retires rendezvous + short-duration survive (2 of 5 sub-steps).
- 13-year cruise survival: does not retire until first full mission flies; ratchets credibility as missions return.

**Step 7 — Iapetus staged-options re-gating.** Compute the demonstrator-conditional joint posterior assuming Earth-orbit + Saturn-small-chunk demonstrators succeed. The expected outcome is ~58 percent joint (per orchestrator thread-walk analysis), above the ~45 percent closure threshold. Document this as the natural tranche-1 gate for the iapetus staged-options framing — replacing the Fission Surface Power Phase 2 award gate that is moot per matrix decision #14 resolution toward audit-required.

---

## Out of scope

- Reactor-program-credibility audit. That is R-kilopower-scale-up-credibility (separate SCOPE, gates matrix decision #14).
- L0-04 numerical floor derivation. That is a separate financial-model question (matrix decision pending project-owner; A14 is upstream of it but not the same decision).
- Demonstrator-mission specification. R-demonstrator-mission-concept (separate SCOPE) handles what mission profile retires the three engineering bets. This round produces an input (the A14 retirement-by-demonstrator analysis) that R-demonstrator-mission-concept consumes.
- Re-running the framework's chunk-fed-spiral or Earth-arrival downstream efficiency. The ~27.7 percent downstream efficiency anchor stands; this round audits A14 only.

---

## Inputs to acquire (reading order)

1. `water-prop/rounds/R_assumption_audit_2026_05_21/FINDINGS.md` — Saturn-worker placeholder decomposition.
2. Locked beliefs `31a13abb` (A14 load-bearing) + `c646b3c6` (chunk water fraction).
3. NASA OSIRIS-REx mission documents (Lockheed Martin post-mission reports, sample-return mass).
4. JAXA Hayabusa + Hayabusa2 mission documents.
5. NASA LOFTID post-flight report (2022).
6. NASA / Northrop Grumman James Webb Space Telescope sunshield deployment report.
7. NASA Meteoroid Engineering Model + ESA MASTER micrometeoroid environment models.
8. Water-ice sublimation literature (peer-reviewed thermal-physical-chemistry, planetary science).
9. Deployable-mechanism reliability literature (especially cinch / lockout mechanisms).
10. `water-prop/sims/mission_graph/missions/sweeps/audit_capture_efficiency.py` — the existing parametric sweep saturn-worker ran; use it as the framework substrate for plug-in of the new probabilities.

---

## Deliverables (in commit order)

1. `STUDY.md` — pre-registered hypotheses H1-H6 frozen before the heritage fetch.
2. `inputs/heritage_base_rates.csv` — Step 1 output (mission × sub-step × success outcome).
3. `inputs/catch_velocity_envelope.md` — Step 2 output (closing-velocity geometry derivation + sensitivity table).
4. `inputs/bag_cruise_duration_model.md` — Step 3 output (puncture / sublimation / cinch fatigue per material).
5. `results/per_substep_probabilities.csv` — Step 4 output (5 sub-steps × low / mid / high uncertainty brackets).
6. `results/joint_posterior_sensitivity.csv` — Step 5 output (joint × closing velocity × cinch reliability × bag survival).
7. `results/demonstrator_retirement_analysis.md` — Step 6 output (per-demonstrator-profile sub-step retirement).
8. `results/iapetus_staged_options_re_gating.md` — Step 7 output (demonstrator-conditional joint posterior + matrix decision #13 input).
9. `READING.md` — load-bearing reading per H6; recommended replacement for the desk-study 46 percent joint in mission_graph; recommended matrix amendment for decision #13.
10. Handoff doc to orchestrator (`~/.claude/handoffs/iceberg-<worker>-<date>-A14-engineering-decomposition.md`).

---

## Suggested worker

Any moon. Best fit: comfortable with both space-systems engineering (deployable mechanisms, micrometeoroid environment, bag-material thermal modeling) AND Bayesian probability composition. Phoebe would be a good fit (already audited engineering survivability for B-ring rendezvous in R-bring-rendezvous-survivability). Enceladus-r5 would be a good fit (already audited reactor-lifetime burn-time and bus-mass anchors with similar rigor).

---

## Cross-references

- Locked belief `31a13abb` (A14 single-most-load-bearing) — the assumption this round anchors.
- Locked belief `5535179f` (matrix reduces to three engineering bets) — A14 is bet #1 of three.
- `water-prop/rounds/R_assumption_audit_2026_05_21/FINDINGS.md` — Saturn-worker placeholder decomposition.
- `water-prop/sims/mission_graph/missions/sweeps/audit_capture_efficiency.py` — existing parametric sweep substrate.
- `design-axes/19-capture-architecture.md` — Current section + 2026-05-22 latest+16 HISTORY entry frame this round's deliverable.
- Matrix decision #13 (pitch staged-options reframe) + decision #14 (reactor power class) — both informed by this round's Step 7 demonstrator-retirement analysis.
- R-demonstrator-mission-concept SCOPE — consumes this round's output as the A14-bet retirement specification.
- R-kilopower-scale-up-credibility SCOPE — companion audit on bet #3 (reactor program); structurally parallel to this round which audits bet #1 (chunk capture).
