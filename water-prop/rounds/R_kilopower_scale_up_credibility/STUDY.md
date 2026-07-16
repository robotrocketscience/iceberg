# R-kilopower-scale-up-credibility — is 30 kilowatt-electric defensibly Kilopower-extrapolation, or does it re-import the retired 500 kilowatt-electric fantasy under a softer name?

**Worker:** hyperion. **Date:** 2026-05-22. **Status:** complete.
**Round type:** credibility audit (Bayesian conjunction synthesis + mass-budget feedback). NOT a closed-form physics sweep.
**Anchors:** titan-3 R-chunk-size-pareto (`1997a51`) closure cell; hyperion R-power-bayesian-update three-prior bracket; enceladus-r5 R-arch-E-specific-power-flown-anchored (`62f7079`) and R-reactor-lifetime-vs-burn-time (`c685c52`); four user-locked R-power-wonder findings.

---

## Question (from SCOPE)

titan-3's R-chunk-size-pareto found a non-empty L0-05-strict + L0-09-floor closure cell at 40–80 tonne chunks + **30 kilowatt-electric** reactor power + a 10-flyby lunar-gravity-assist Earth-arrival. 30 kilowatt-electric is **3× outside** titan-3's own 1–10 kilowatt-electric "flyable Kilopower-extrapolation" envelope and outside the locked-memory directive ("Kilopower-class single-kilowatt fission at best"). **The matrix does not carry titan-3's closure cell as state-of-record until this round either survives or kills the 30 kilowatt-electric assumption.** Three candidate paths from KRUSTY's flown anchor (1 kilowatt-electric, 28-hour ground test, 2.4 watts-per-kilogram system-level, 2018) to titan-3's design point:

- **Path A** — single 30-kilowatt-electric reactor (closest heritage: Fission Surface Power Phase-1 40-kilowatt-electric design).
- **Path B** — 30× parallel 1-kilowatt-electric Kilopower modules.
- **Path C** — intermediate (N × k = 30).

---

## Pre-registered hypotheses (authored by Saturn / orchestrator in SCOPE; graded here)

| # | Hypothesis (abbreviated) | Predicted | Grade |
|---|---|---|---|
| H1 | Path A is NOT Kilopower-extrapolation; it is Fission-Surface-Power-Phase-1-class. | Path A requires Phase-2 award. | **HELD** |
| H2 | Path B (30× parallel modules) pays a severe specific-power penalty; effective system specific power **< 1 W/kg**. | < 1 W/kg | **FALSIFIED** (parallel modules preserve per-unit 2.4 W/kg; central estimate 1.8–2.4 W/kg) |
| H3 | Path B mass penalty **falsifies** titan-3's closure cell (reactor mass > chunk budget). | cell collapses | **FALSIFIED** on the mass axis (cell closes strict down to 1.1–1.6 W/kg; survives waiver to 0.4 W/kg) |
| H4 | Joint posterior of any United States/allied program delivering ≥30 kilowatt-electric AND ≥5-year lifetime AND ≥5 W/kg inside 2032–2035 is **≤ 1%**. | ≤ 1% (falsify if > 5%) | **HELD** (0.05–1.5%; only the most-charitable-prior single-core path reaches 1.5%, still ≪ 5%) |
| H5 | The honest decision-#14 answer is **(b)** hold the directive or **(c)** require this audit; **(a)** soften-to-admit-30-kilowatt-electric-as-Kilopower is structurally indefensible. | (b)/(c), not (a) | **HELD** |
| H6 | The closure cell is fantasy-conditioned in the same sense as the prior 500-kilowatt-electric cells, just with a softer power-class name; the matrix should **not** carry it as state-of-record. | cell NOT load-bearing | **HELD — but via a different failure mode than H2/H3 predicted** |

**Aggregate verdict pre-registered by SCOPE:** if H6 holds, the campaign returns to the iapetus tech-demonstrator-only framing; decision #15 becomes the only live ICEBERG architectural question. **H6 holds. The aggregate verdict stands — but the *reason* is programmatic + lifetime, not mass.**

---

## Method

Two deterministic computations in `run.py` (no Monte Carlo; the programmatic bracket reuses an already-run posterior as a fixed input):

**Step 4 — mass-budget feedback.** titan-3's `m_dry` and `evaluate` closure formulas are copied **verbatim** (cited, not re-derived, per SCOPE out-of-scope guard #2). The only change: sweep effective system specific power as a free variable (0.2 → 12.0 W/kg) at titan-3's two closing chunk sizes (50, 60 t) at P = 30 kilowatt-electric, and report the lowest specific power that still satisfies (i) the L0-09 30-tonne floor, (ii) L0-05 strict 15-year round-trip, (iii) L0-05 waiver 25-year round-trip. The sweep is monotone (higher specific power → lighter reactor → easier closure), so the lowest-passing value is the collapse threshold.

**Step 3 — programmatic conjunction.** Take the heritage P(any United States fission reactor reaches orbit by 2035) three-prior bracket from R-power-bayesian-update — **uniform 8.9%, Jeffreys 4.9%, skeptical 2.9%** — as the unconditional prior. Multiply by three path-specific conditional credibility weights, **set deliberately at the charitable (high) end** so the result is an *upper bound* (inverted lesson-7 discipline: rather than the most-pessimistic input, use the most-*generous* input and show even that is sub-threshold):

- `p_power` = P(orbited reactor is ≥30 kilowatt-electric | orbit) = **0.60** for all paths. Per iapetus methodology lesson 12, the *prospective* scope distribution of currently-funded programs favours <100 kilowatt-electric; 30 kilowatt-electric sits just below the Fission Surface Power Phase-1 40-kilowatt-electric scope, so a generous 0.60.
- `p_life` = P(sustains the cell's ~6–8-year cumulative full-power burn | orbit) = **0.40**. KRUSTY's longest run was **28 hours**; the Kilopower 10-year life is a design *target*, never demonstrated (enceladus-r5 `c685c52`). The titan-3 cell's own inbound burn alone is ~6 years at 2.0–2.4 W/kg.
- `p_arch` = P(the *specific path architecture* is the one that flies | a ≥30-kilowatt-electric reactor orbits): Path A **0.70** (single large core is the funded direction); Path B **0.07** (no funded program pursues a parallel-module power plant); Path C **0.20** (interpolated).

Joint posterior = p_orbit × p_power × p_life × p_arch.

---

## Results

### Step 4 — mass-budget feedback (titan-3 cell, P = 30 kilowatt-electric)

| chunk | at KRUSTY 2.4 W/kg | reactor mass | delivered | round-trip | strict? | lowest sp: floor | lowest sp: strict | lowest sp: waiver |
|---|---|---|---|---|---|---|---|---|
| 50 t | closes | 12.5 t | 35.6 t | 13.81 yr | yes | 0.8 W/kg | **1.1 W/kg** | 0.8 W/kg |
| 60 t | closes | 12.5 t | 43.4 t | 14.46 yr | yes | 0.4 W/kg | **1.6 W/kg** | 0.4 W/kg |

**Reading of Step 4.** The cell's binding constraint at low specific power is the **L0-05 strict round-trip** (heavier reactor → larger initial mass → more inbound propellant → longer burn → longer round-trip), not the delivered-mass floor (the chunk dominates delivered mass, so the floor survives to ~0.4–0.8 W/kg). The strict cell collapses only below **1.1–1.6 W/kg**.

**Where does Path B actually sit?** KRUSTY's 2.4 W/kg system-level figure is measured **at 1 kilowatt-electric** and already includes that unit's convertor, controls, and structure. Thirty replicated 1-kilowatt-electric modules preserve the per-unit mass-to-power ratio (this is the entire point of a parallel-module plant: replicate a proven unit, no core-physics scaling). The only degradation is integration overhead — power management and distribution to combine 30 sources, common structure, and shared/clustered shielding. Realistic penalty: 10–40%, giving an **effective system specific power of ~1.8–2.4 W/kg**. That is **above the 1.1–1.6 W/kg strict-collapse threshold.** H2's "<1 W/kg" prediction is therefore too pessimistic, and H3's "cell collapses on mass" does not hold at the central estimate.

This is the surprise of the round, and it **diverges from the SCOPE author's pre-registration**. The 30-kilowatt-electric cell is fundamentally unlike the retired 500-kilowatt-electric cells: those died on specific power (at 500 kilowatt-electric and 2.4 W/kg the reactor alone is ~208 tonnes — enceladus-r5 `62f7079` found 0/60 cells close). At 30 kilowatt-electric the reactor is only **12.5 tonnes** at the same flown-anchored specific power, and a 50–60-tonne chunk absorbs it. **The 30-kilowatt-electric cell is robust on the mass / specific-power axis. It is not a mass-fantasy.**

*Caveat flagged for project owner:* if module-isolation requirements (single-point-failure separation, independent shadow shields per module, thermal stand-off) force the effective specific power below 1.6 W/kg, strict closure collapses to waiver-only (25-year round-trip), and below 0.4 W/kg the floor itself fails. The 1.8–2.4 W/kg central estimate assumes clustered shielding and shared structure. This is the one mass-side sensitivity worth a dedicated engineering check before treating the cell as mass-robust.

### Step 3 — programmatic joint posterior, P(path delivers ≥30 kilowatt-electric, ≥5-yr life, in 2032–2035 window)

| Path | Kilopower-extrapolation? | uniform | Jeffreys | skeptical |
|---|---|---:|---:|---:|
| A — single 30-kilowatt-electric core | **no** (Fission-Surface-Power-class) | 1.50% | 0.82% | 0.49% |
| B — 30× parallel 1-kilowatt-electric modules | **yes** | 0.15% | 0.08% | 0.05% |
| C — intermediate N×k=30 | project-owner-call | 0.43% | 0.24% | 0.14% |

**Reading of Step 3.** The two findings split cleanly across the paths:

1. **The only path with a delivery posterior above 1% (Path A, single core, 1.5% at the most charitable prior) is NOT Kilopower-extrapolation.** It is a single 30-kilowatt-electric reactor whose nearest design heritage is the Fission Surface Power Phase-1 40-kilowatt-electric concept — a program whose **Phase 2 has not been awarded as of May 2026** (locked finding 3). Calling Path A "Kilopower-extrapolation" is precisely the fantasy-conditioned move the project-owner directive retired: it borrows the credibility of a *flown* 1-kilowatt-electric reactor to dress up an *unfunded* 30–40-kilowatt-electric program. **H1 holds.**

2. **The only genuinely-Kilopower path (Path B, parallel modules) has a delivery posterior of 0.05–0.15%** — one to three parts in two thousand. Path B is technically defensible as Kilopower-extrapolation (it literally replicates the flown unit) and, per Step 4, is even mass-robust. But no funded program is building a parallel-module fission power plant; its programmatic credibility is dominated by `p_arch = 0.07`. **H4 holds** (≤1% for B and C; A's 1.5% is below the 5% falsification band). **H5 holds:** decision-#14 option (a) is indefensible — there is no path that is *both* genuinely-Kilopower *and* above ~0.15% delivery probability.

---

## Synthesis table for the project owner (decision #14)

| Path | Technical credibility | Mass-budget verdict (Step 4) | Programmatic posterior (Step 3, uniform→skeptical) | Lifetime credibility | Kilopower-extrapolation under locked directive? | Overall |
|---|---|---|---|---|---|---|
| **A** single 30 kWe core | Fission-Surface-Power-Phase-1 design heritage; no flight heritage; needs Phase-2 award | cell **closes** (single core ≥2.4 W/kg, scale benefit) | **1.5% → 0.5%** | 28-hr flown vs ~6–8-yr need; 3–4 orders short | **NO** — this is FSP-class, not Kilopower | sub-threshold; mislabelled if called "Kilopower" |
| **B** 30× parallel 1 kWe | replicates flown KRUSTY unit; no core scaling; PMAD/structure integration risk | cell **closes** at ~1.8–2.4 W/kg central (collapses to waiver-only if module isolation forces <1.6 W/kg) | **0.15% → 0.05%** | same 28-hr-vs-years gap, per module | **YES** (engineering sense) but nobody is funding it | mass-robust, programmatically near-zero |
| **C** intermediate (e.g. 3×10 kWe) | between A and B | cell closes | **0.43% → 0.14%** | same | **partial / owner-call** | sub-threshold |

**Reading-level recommendation: decision #14 → option (c)→(b).** This audit (option c) was the right gate. Its result: **hold the locked-memory directive (option b).** Option (a) — soften the directive to admit 30 kilowatt-electric as "Kilopower-extrapolation" — is structurally indefensible, because the audit splits the question in two and neither half supports it:

- The path that *carries the Kilopower name honestly* (B, parallel modules) delivers at **0.05–0.15%**.
- The path with a *deliverable-looking posterior* (A, 1.5% at best) is **Fission-Surface-Power-class, not Kilopower** — and is itself gated on a Phase-2 award that has not happened (locked finding 3) and a 0-of-6 base rate (locked finding 2).

**The matrix should NOT carry titan-3's closure cell as state-of-record (H6 holds).** But the precise reason matters for how the matrix annotates it, and it is *not* the reason the SCOPE author anticipated:

> The 30-kilowatt-electric cell is **mass-robust** — it closes at KRUSTY-measured 2.4 W/kg because the reactor is only 12.5 tonnes and a 50–60-tonne chunk absorbs it. Unlike the 500-kilowatt-electric cells (which died on a 208-tonne reactor), this cell is **fantasy-conditioned on the programmatic and lifetime axes, not the mass axis.** It is a real piece of physics gated on a reactor program with a ≤1.5% chance of delivering in window and a 3–4-order-of-magnitude lifetime gap (28 measured hours vs ~6–8 required years). The "softer-sounding power class name" (H6) is real, but the softening happens by mislabelling an FSP-class single core as "Kilopower," not by hiding a mass blowout.

---

## Revisit (mandatory)

**Pre-registration accuracy: 4 of 6 held; 2 falsified — both on the same axis, both in the *less-pessimistic* direction.** H2 and H3 (the parallel-module mass-penalty pair) were pre-registered pessimistically (severe penalty, cell collapses) and came back less-pessimistic: parallel modules preserve per-unit specific power, so the cell is mass-robust. This is the **third campaign instance of methodology lesson 1** (pessimistic-prediction default; lumped/inherited figures more often conservative-than-cheating) and lesson 5's two-bucket bias check: the SCOPE author reasoned by analogy from the 500-kilowatt-electric mass blowout, but the analogy fails because reactor mass at fixed specific power scales with *power*, and 30 kilowatt-electric is 17× smaller than 500. The pre-registration imported the failure mode of a different power class.

**Why the falsifications do not change the aggregate verdict.** H6 (the load-bearing reading) held regardless, because the cell's lethal axis was always programmatic + lifetime, and those are independent of the mass result. This is **methodology lesson 11 (robustness-by-magnitude)**: the decision-#14 conclusion is robust because the programmatic posterior floor (0.05–1.5%) is far below any plausible go-threshold, *not* because competing factors cancel. Killing H2/H3 (mass) does not lift the programmatic posterior, so the verdict is durable. The mass-robustness finding is a refinement of *how* the cell fails, not *whether* it fails.

**Where I could be wrong.** (1) If module-isolation engineering forces Path B below 1.6 W/kg effective, strict closure collapses to waiver-only — I flagged this but did not compute a module-shield mass model (out of scope; candidate for a dedicated round). (2) The `p_arch = 0.07` for Path B is a judgment, not a measured base rate; a project-owner who believes a parallel-module plant is more fundable would lift it — but even `p_arch = 0.5` only moves Path B to ~1.1%/0.4%/0.25%, still sub-threshold. (3) The conditional factors are multiplied, not convolved, understating the uncertainty band (same caveat as R-power-bayesian-update); the point estimates are upper-bound-charitable, so the true posteriors are lower.

---

## Cross-learning

- **Negative for titan-3 R-chunk-size-pareto (`1997a51`):** the 30-kilowatt-electric closure cell is **not load-bearing** as a program bet. It survives physics (mass-robust at flown-anchored specific power) but fails programmatic credibility (≤1.5% delivery by 2035) and lifetime credibility (28 hr vs ~6–8 yr). titan-3's three flagged tensions are resolved: tension (1) [30 kWe outside Kilopower envelope] is **confirmed lethal via the programmatic axis** — the deliverable-looking path is FSP-class, not Kilopower.
- **Positive for iapetus tech-demonstrator-only framing:** with the titan-3 closure cell retired as state-of-record, iapetus's R7 staged-options / tech-demonstrator framing is reinforced as the honest reading. Decision #15 (L0-04 strict deliver-to-Earth-orbit) becomes the live ICEBERG architectural question.
- **Reconciles with enceladus-r5 R-arch-E-specific-power-flown-anchored (`62f7079`):** that round found 0/60 cells close at 2.4 W/kg under Architecture E (500–1000 kilowatt-electric, 200-tonne chunk). This round finds titan-3's cell *does* close at 2.4 W/kg. **No contradiction:** the reactor-mass calculation is identical; the cells differ by 17× in power (30 vs 500 kilowatt-electric), so the reactor is 12.5 t here vs 208 t there. The mass axis is fatal at 500 kilowatt-electric and benign at 30 kilowatt-electric. The *programmatic* axis is fatal at both.
- **Methodology lesson candidate (hyperion, awaiting project-owner ratification):** *do not import a failure mode across power classes without re-checking the scaling.* The SCOPE pre-registered H2/H3 by analogy to the 500-kilowatt-electric mass blowout; the analogy failed because reactor mass at fixed specific power scales linearly with power, and the two cases differ 17×. When a SCOPE inherits a "this will collapse on axis X" intuition from a prior round, verify the axis-X mechanism actually scales into the new parameter regime before pre-registering it. (Compounds with lesson 9: anchor on the prior round's *mechanism*, not its *verdict label*.)

---

## Validity caveats

1. **Primary-source fetch was not independently re-run.** The four external findings the SCOPE requires (KRUSTY 2.4 W/kg / 28-hr; Fission Surface Power Phase-1 status; 0-of-6 base rate; National Academies 2021) are **user-locked beliefs** from R-power-wonder, each with primary-source attribution, and the SCOPE explicitly instructs anchoring against them rather than litigating them. I treated the locked beliefs + the already-run R-power-bayesian-update posterior as the evidence chain. I did not pull fresh primary documents; if any locked finding is stale (e.g., a Fission Surface Power Phase-2 award lands after May 2026), Path A's `p_arch` and the whole programmatic table move upward — but Path A is FSP-class, not Kilopower, so even a Phase-2 award would resolve decision #14 toward "ICEBERG depends on FSP," not toward "30 kWe is Kilopower-extrapolation."
2. **The conditional factors are judgments, not fitted base rates.** They are documented in `run.py` and set charitably (upper-bound). The qualitative conclusion (all paths sub-threshold; the Kilopower-honest path is near-zero) is robust to plausible variation; the exact percentages are not load-bearing.
3. **Module-shield mass model not built.** Path B's effective specific power could fall below the 1.6 W/kg strict-collapse threshold if modules require individual shielding/separation. Central estimate (clustered shielding) keeps it mass-robust; the sensitivity is flagged, not closed.

---

## Files

- `run.py` — Step 4 mass-budget sweep (titan-3 formula verbatim) + Step 3 programmatic conjunction. Deterministic; re-run reproduces `results/summary.json` byte-for-byte.
- `results/summary.json` — full sweep, anchor cells, collapse thresholds, per-path joint posteriors under all three priors.
- `SCOPE.md` — orchestrator-authored scope (Saturn, 2026-05-19).
