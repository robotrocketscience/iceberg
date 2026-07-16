# R-chunk-as-heat-shield-revisit — does chunk-as-Earth-aerocapture-heat-shield rescue the year-twenty-plus megawatt all-electric end-to-end architecture under titan's corrected inbound delta-velocity?

**Status:** scope, pre-study. Authored by Saturn (orchestrator session) on
2026-05-15 in response to titan's R-inbound-dv-continuous-thrust finding
(commit `58581fb`).

**Trigger and standing:** titan demonstrated that continuous-thrust electric
inbound integrated delta-velocity is 24.7–40.2 kilometres-per-second, of which
**17.97 kilometres-per-second sits in the Earth-side phase** (heliocentric
decelerate 10.30 + low-Earth-orbit Edelbaum spiral 7.67, no Oberth bonus).
Earth aerocapture eliminates both: ballistic arrival at velocity-at-infinity
~10.3 kilometres-per-second, hyperbolic atmospheric pass to Earth elliptical,
aerobraking down. If chunk-as-heat-shield closes the engineering, the
Earth-side 17.97 kilometres-per-second collapses to ~0.3–1.0
kilometres-per-second (post-capture trim) and the year-twenty-plus megawatt
all-electric end-to-end winner cell's delivered-fraction returns from 20% to
something like 50–70%.

This is **not** a re-run of R-chunk-as-heat-shield. That round established
chunk-as-heat-shield is thermodynamically viable for single-pass aerocapture
at ICEBERG's 4,000-kilograms-per-square-metre ballistic coefficient (0.5%
chunk ablation; chunk survives 99.5% intact). The binding open question was
**chunk geometric stability through a 200-second hypersonic pulse**. This
revisit addresses that question at the engineering level R-chunk-as-heat-shield
declined to enter, and re-derives the architecture rescue under titan's
corrected inbound delta-velocity budget.

---

## What changed since R-chunk-as-heat-shield closed

| Element | Then (R-chunk-as-heat-shield closing state) | Now (post titan) |
|---|---|---|
| Inbound delta-velocity budget (Earth side) | 0.3–1.0 km/s post-aerocapture vs ~7 km/s propulsive low-Earth-orbit-spiral alternative | 0.3–1.0 km/s post-aerocapture vs **17.97 km/s** propulsive-only alternative under continuous-thrust electric |
| Architecture rescue magnitude | Marginal delivered-mass improvement (~11–31%) | Architecture-saving: year-twenty-plus winner cell needs this rescue or accepts 20% delivered fraction |
| Alternative rescue paths | R-deployable-drag-skirt and chunk-as-heat-shield in parallel | R-deployable-drag-skirt was killed (thermal envelope fails at 12.6 km/s entry, commit `34a473b`). **Chunk-as-heat-shield is the last surviving aerocapture rescue.** |
| Earth-approach velocity-at-infinity | Assumed lunar-gravity-assist 6 km/s | Direct Hohmann return: 10.3 km/s; lunar-gravity-assist credit 2 km/s leaves ~8 km/s. Entry velocity ~12.5–14 km/s, higher than the R-chunk-as-heat-shield 12.6 km/s assumption |
| Binding open question | "Can the chunk be oriented chunk-forward through a 200-second hypersonic pulse without tumbling?" | Same. Now load-bearing for an entire architectural era. |

---

## Question this round answers

For a 100-tonne-class chunk-bearing ICEBERG vehicle returning from Saturn on
a Hohmann-equivalent trajectory under continuous-thrust electric propulsion:

1. **Can the chunk be reliably oriented chunk-forward (ice face into the
   relative wind) and stabilised against passive tumbling through a 200-second
   single-pass aerocapture pulse, given the chunk's irregular shape
   (assumed prolate spheroid or rubble-pile) and the entry velocity range of
   12.5–14 kilometres-per-second?**

2. **At titan's corrected entry velocity (12.5–14 km/s vs R-chunk-as-heat-shield's
   12.6 km/s), does the chunk surface ablation stay below ~1% chunk mass loss
   (Sutton-Graves stagnation-point + boundary-layer-blocked sublimative
   ablation), or does the higher velocity push ablation into the
   "delivered-fraction-degrading" regime (≥ 5% per pass)?**

3. **Does the bag-retraction mechanism close as a single-mission engineering
   item, or is sacrificial-bag (consumable per mission) the only path?** This
   gates whether the 14-year round-trip mission economics tolerate
   bag-per-mission cost vs reusable-bag with a retraction mechanism.

4. **If chunk-as-heat-shield closes, what delivered chunk fraction does it
   restore in the year-twenty-plus megawatt all-electric end-to-end winner
   cell, vs titan's 20% baseline?**

The four questions sequence: (1) is the binding engineering question, (2) and
(3) refine the cost of closing it, (4) is the architecture-payoff if it
closes.

---

## Pre-registered prediction (sketch — full hypothesis grading in STUDY.md when round runs)

**Aggregate:** chunk-as-heat-shield closes as a single-engineering-programme
item. Active attitude control (cold-gas reaction-control-system on the tug,
firing during the 200-second pulse) is required and sufficient. Sacrificial
bag is the path of least resistance for the first three commercial missions;
retractable-bag mechanism is a follow-on R&D programme worth pursuing for
year-twenty-plus operations only. Chunk ablation at 12.5–14
kilometres-per-second entry stays ≤ 2% per pass — higher than R-chunk-as-heat-shield's
0.5% (Sutton-Graves heat flux scales as v³, so 14/12.6 → 1.36× more total
heat load) but still in the "delivered-fraction-tolerable" regime. Restored
delivered fraction in the year-twenty-plus winner cell: 55–65% (vs titan's
20% baseline; not quite the matrix's original 70% because some ablation and
some post-capture trim cost persists).

**Falsification bands and sub-claims to refine in STUDY.md:**

- Chunk attitude stability under cold-gas-only reaction-control during pulse:
  hypothesis says closed; falsified if the chunk inertia-ratio + atmospheric
  torque cross-section demands reaction-control-system propellant > 1 tonne
  per pulse (mass-budget breaker).
- Chunk ablation at 14 km/s entry: 1–3% per pass. Falsified if > 5%.
- Restored delivered fraction at megawatt-class year-twenty-plus: 50–70%.
  Falsified if < 35% (no architecture rescue) or > 75% (suspect modelling).
- Sacrificial-bag economic tolerance: bag-per-mission cost ≤ 5% of mission
  revenue. Falsified if > 20%.

---

## Method sketch

Approximate methodology — detailed in STUDY.md when the round runs.

1. **Chunk geometric-stability analysis.** Treat chunk as a prolate spheroid
   with ratio drawn from B-ring observation literature (aspect ratio
   1.5–3.0). Compute aerodynamic centre vs centre-of-mass under hypersonic
   newtonian-impact flow at 12.5–14 kilometres-per-second. Estimate restoring
   torque vs perturbation torque ratio. If passively unstable (centre-of-mass
   behind aerodynamic centre), size reaction-control-system propellant for
   active stabilisation over a 200-second pulse with bandwidth-matched
   correction frequency (~10 hertz).

2. **Chunk ablation at corrected entry velocity.** Sutton-Graves stagnation
   heating at v ∈ {12.5, 13, 14} kilometres-per-second, with 90-kilometre
   periapsis, 100-tonne vehicle, ~25 square-metre windward area (R-chunk-as-heat-shield
   geometry). Boundary-layer-blocked sublimation at ~25 megajoules-per-kilogram
   effective. Compare per-pass mass loss to chunk mass.

3. **Bag-retraction feasibility, qualitative.** Survey existing mechanism
   heritage (deployable booms, retractable solar arrays, James-Webb sunshield
   deployment-and-stowage). Identify the closest engineering analog. Mark
   technology-readiness level and identify next test article. This is not a
   quantitative result, it is an engineering-judgement output.

4. **Sacrificial-bag economic check.** Bag mass ~1–3 tonnes; bag cost
   $5–20 million per unit (synthetic-fabric envelopes at this scale, scaled
   from comparable hardware). Compare to mission revenue (set by the financial
   model — current value ~$80 million per 50-tonne delivery).

5. **Architecture re-derivation.** With Earth-side delta-velocity collapsed
   from 17.97 to 1.0 kilometres-per-second, recompute the year-twenty-plus
   megawatt all-electric end-to-end mass ratio and delivered fraction. Cross-
   check with titan's run.py at the new boundary condition (or re-derive
   independently for the Earth-side phase only).

6. **Sweep axes:**
   - Chunk aspect ratio: 1.5, 2.0, 2.5, 3.0
   - Entry velocity at periapsis: 12.5, 13.0, 14.0 kilometres-per-second
   - Bag mode: retractable vs sacrificial
   - Reaction-control-system thrust authority: 1, 5, 10 newtons (cold-gas
     range)

7. **Deterministic run.py per project convention.** No randomness; results
   reproducible from inputs.

---

## Cross-references (read before authoring STUDY.md)

- `water-prop/rounds/R_chunk_as_heat_shield/STUDY.md` — the closing round.
  Critically: §"Revisit clause" names this exact round as a next-round
  candidate.
- `water-prop/rounds/R_chunk_as_heat_shield/results/` — heat flux and
  ablation tables at 12.6 kilometres-per-second.
- `water-prop/rounds/R_deployable_drag_skirt/STUDY.md` — the rescue path
  that was killed. Confirms drag-skirt thermal envelope fails at
  ~12.6 kilometres-per-second entry, so the higher entry velocity at this
  revisit (12.5–14) is harder still for skirt-class rescues. **Chunk-as-heat-shield
  is the only surviving aerocapture path.**
- `water-prop/rounds/R_inbound_dv_continuous_thrust/STUDY.md` — titan's
  round. The Earth-side decomposition (17.97 kilometres-per-second) and the
  pre-registered "three resolution paths" frame this scope.
- `water-prop/docs/ARCHITECTURE-DECISION-MATRIX.md` "Aerocapture conditional
  architecture" section — the pre-existing matrix conditional that this round
  re-opens.
- `ICEBERG-bag-engineering.md` — bag mechanical and capture-efficiency
  reference.

---

## Out-of-scope (deferred to follow-on rounds)

- Detailed thermal protection of the **tug** (electric stage + reactor) during
  the aerocapture pulse. The chunk shields the tug if chunk-forward
  orientation is achieved; if not, the tug sees full stagnation conditions.
  R-tug-thermal-survival is the follow-on.
- Hybrid aerocapture-then-aerobraking trajectory optimization. R-chunk-as-heat-shield
  named this as a next-round candidate. If chunk-as-heat-shield closes single-pass
  cleanly, the hybrid is a fall-back; if not, hybrid is the next move.
- Long-duration bag-laminate fatigue under repeat-mission reuse (only
  relevant if retractable-bag closes).
- COSPAR planetary-protection category determination for returning Saturn
  ring material to low Earth orbit via an atmospheric pass. Backward-contamination
  risk is non-zero and is a regulatory item not addressed here.

---

## Worker handoff convention

This round is sizeable (six sweep axes, ~6–10 hours of analyst time including
STUDY.md draft, run.py, results, and grading). Worker (project-owner-assigned
NAME) reads this SCOPE.md, drafts the STUDY.md against the project's
pre-registration template, writes run.py, runs it, grades hypotheses, and
hands off to the orchestrator for matrix integration. Worker assignment is
the project owner's call; the orchestrator does not pick names.
