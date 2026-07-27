# R-vehicle-mass-fidelity-refinement — FINDINGS

**Worker:** rhea-5 (`iceberg-rhea-5`), executing the titan-7-scoped round at project-owner
direction 2026-06-12. Pre-registration: STUDY.md (this directory), written before any
sweep ran. Artifacts: `run.py`, `total_order_h3.py`, `wet_vs_dry_audit.md`,
`results/fidelity_sweep.json`, `results/total_order_h3.json` (results not committed).
**Baseline regression check:** f = 0.80 / aerocapture=True reproduces titan-6 exactly —
0 arrivals, 0 closures at every floor. The harness is measuring the same thing.

## Headline

**The titan-6 "0 closures" verdict is propellant-fraction-conditional, and H5 — the
load-bearing hypothesis — is FALSIFIED as stated.** At launch propellant fraction
f ≈ 0.18–0.22 (vs the frozen 0.80), the chemical-kick + Mars/Jupiter-gravity-assist
family closes 10 of 150 cells at the 30-tonne delivered floor (6.7 % > the 5 % H5 gate),
delivering 44.6–45.3 t at a 17.3-year round trip (L0-05 waiver). **But the rescue runs
entirely through the capture-efficiency anchor the Monte-Carlo round already falsified:**
at the harpoon Tier-1 empirical median (multiplier 0.43), the 20 t and 30 t floors are
dead at every f, and only the 10 t floor closes (10 cells, best delivered 18.6 t).
Mass fidelity and capture fidelity are coupled; neither refinement program alone settles
the matrix. Per the SCOPE's reading-if-falsified: **the titan-6 matrix-amendment cascade
should pause** pending the conjunction reading below.

## Verdicts

| Hypothesis | Verdict | Pre-registered prediction | What actually happened |
|---|---|---|---|
| H1 (propellant-fraction refinement opens closures) | **HELD, stronger than predicted** | 5–25 cells gain `arrived_at_depot` at best-f, via electric outbound | 50 of 150 cells arrive at best-f (45 at f = 0.20 alone); via the **chemical-kick ballistic family, not electric** |
| H1-corollary (chemical-TSI-class f stays dead) | **HELD** | f = 0.92 opens nothing | f ≥ 0.28 opens nothing; 0.92 zero |
| H3 (capture mass is largest dry-mass uncertainty) | **FALSIFIED as stated** (numeric gate passes) | capture 0.15–0.35, narrowly largest | capture 0.21–0.32 — above the 0.15 gate but **third behind thermal protection (0.33–0.50) and tankage (0.33 at f = 0.80)**; tankage collapses to <0.04 at f = 0.20 (regime-dependent) |
| H4 (path-conditional thermal protection changes closure ≥ 5 % of cells) | **FALSIFIED at the bracket level** | aerocapture=False adds ≥ 8 cells | True/False closure cell-sets are **identical** at every floor and every f (50∩50, 10∩10, zero exclusive cells) |
| H5 (load-bearing: nothing produces > 5 % closure at 25 t) | **FALSIFIED as stated; HELD under empirical capture** | HELD (≤ 7 cells at 20 t, ≤ 3 at 30 t) | At anchor capture: 20 cells at 20 t, 10 at 30 t → > 5 % at L0-04 = 25 t. At multiplier 0.43: **0 cells at 20 t and 30 t** |
| H6 (more wet-vs-dry-ambiguous anchors exist) | **HELD** | 2–5 ambiguous anchors | ≥ 5 unqualified anchor sites beyond the known 12× case (`wet_vs_dry_audit.md`) |
| H2 (Wertz anchor review) | **NO VERDICT** | — | Deferred (STUDY deviation D-C: reference text not available this session) |

## The closure window and the closing architecture

Closure exists only in a narrow window f ∈ [0.15, 0.25], peaking at 0.18–0.22, with hard
edges both sides (f = 0.12: 10 arrivals, 0 floors; f = 0.28: nothing). The window is the
intersection of two physical constraints, not an artifact: below it the vehicle carries
too little propellant for the direct-chemical Saturn capture; above it the launch wet
mass plus kick stage exceeds the four-Falcon-Heavy manifest dry envelope.

The closing path (all 10 closing cells, which are {30, 55 kWe} × {200 t chunk} × all
thrust values — thrust is inert as expected):

> multi-Falcon-4 launch → autonomous assembly → Falcon-Heavy + Helios kick →
> Mars + Jupiter gravity assist → direct chemical Saturn capture → single-pass trawl →
> chunk-fed spiral departure → ballistic inbound → Earth hybrid aerocapture/aerobraking →
> low-Earth-orbit depot. Delivered 44.6–45.3 t, round trip 17.3 yr (waiver, not strict).

Delivered 45.3 t at a 200 t chunk = 22.6 % retention — independently consistent with
hyperion's corrected 17–28 % delivery band (R-revenue-delivery-anchor-refresh), a
cross-validation neither round engineered.

## Prediction-error analysis (the part that matters)

1. **Right verdict, wrong mechanism (H1).** I predicted the electric-outbound channel
   (specific impulse 3000 s needs only f ≈ 0.25, so low f should unlock it). The actual
   channel is chemical-kick ballistic. The error: I reasoned from the Phase-1 electric
   power gate and ignored that the kick family's recorded failure mode — "kick wet mass
   exceeds dry envelope of launch manifest," 180 records in the assembly audit — is the
   single most directly f-sensitive precondition in the graph: dropping f converts wet
   manifest mass into dry envelope one-for-one. The electric family still never closes
   (Saturn-departure power and coast-window gates kill it regardless of f). Lesson for
   pre-registration: when predicting which family a relaxation unlocks, rank families by
   the f-sensitivity of their *recorded killer*, not by which family the relaxed
   parameter superficially "belongs to."
2. **Delivered mass scales almost linearly with capture efficiency, not super-linearly
   (conditioning sweep).** I registered "delivered drops faster than linear because
   propulsion water consumption is fixed per vehicle." Measured: 45.3 → 33.1 → 18.6 →
   9.3 t at multipliers 1.0 / 0.75 / 0.43 / 0.25 — barely sub-linear. The error: the
   chunk-fed departure pushes mostly *chunk*, so water consumption scales with captured
   mass, not with the fixed vehicle. Consequence: floor-survival thresholds sit close to
   the naive linear estimate (30 t floor dies between multiplier 0.75 and 0.60; naive
   linear says 0.66).
3. **Thermal-protection mass moves dry mass but not closure (H4).** A 22 t dry-mass swing
   at the 200 t chunk crosses no cell threshold anywhere on the grid — the binding
   constraints are the kick envelope and capture water, and the 6 × 5 power × chunk grid
   is coarse. Caveat recorded: the True/False bracket conflates path-inconsistent
   combinations (False + aerocapture-arrival path = aerocapture without thermal
   protection). A true per-path dispatch remains correct bookkeeping for titan-7 proper,
   but the SCOPE's closure-count claim for it is dead at this grid resolution.
4. **Sensitivity rankings are regime-dependent (H3).** Tankage is co-largest (0.325) at
   f = 0.80 because it couples through f/(1−f) = 4; at f = 0.20 the coupling is 0.25 and
   tankage vanishes from the ranking (< 0.04) while thermal protection rises to 0.504.
   A total-order sensitivity ranking quoted without its conditioning regime is not a finding. (Cousin of
   PROTOCOL lesson 18.)

## What this means for the matrix (amendment specification — orchestrator owns the edits)

1. **Pause the titan-6 amendment cascade** (SCOPE reading-if-falsified). The honest
   state-of-record statement is now: *"Closed-loop closure at L0-04 = 25 t is 0 % at the
   frozen 0.80 propellant fraction; ~7–13 % in the f ≈ 0.2 window under the desk-study
   0.85 capture anchor; 0 % in that same window under the empirical harpoon Tier-1
   capture median. The commercial-class verdict therefore now rests entirely on capture
   efficiency — consistent with locked audit finding 1 (A14 is the single most
   load-bearing assumption)."*
2. **The relaxation envelope (decision #16) has its first non-empty cell set:** at
   empirical capture, floor 10 t × ceiling 25 yr closes 10 cells (best 18.6 t delivered,
   17.3 yr round trip, 30–55 kWe, 200 t chunk, kick-ballistic family). The
   demonstrator-class pivot gains a concrete reduced-floor mission shape.
3. **Hyperion-3's contact-fidelity round is now the gating round for the whole matrix**
   (it sharpens the capture posterior that everything above conditions on), ahead of
   further mass-fidelity work.
4. **Titan-7 proper still owes:** per-phase Tsiolkovsky derivation (this round's best-f
   union is its upper bound; any derivation landing inside [0.15, 0.25] inherits these
   results), the H2 Wertz review, and the thermal-protection dispatch (bookkeeping
   honesty, not closure-count).
5. **L0-05 note:** every closing path is waiver-class (17.3 yr > 15 yr strict). Strict
   round-trip closure remains zero everywhere.

## Methodology-lesson candidates (for PROTOCOL ratification)

- **Lesson 23 candidate:** "A swept constant that interacts with a manifest or envelope
  cap (here: propellant fraction × launch manifest) must be swept to its physical limits
  before a zero-closure verdict is recorded — optimum may sit far from convention."
- **Lesson 24 candidate:** "Quote sensitivity rankings with their conditioning regime;
  re-run the ranking at the closure-relevant operating point before using it to
  prioritize refinement work."

---

## CORRECTION NOTICE — 2026-06-12, same worker (rhea-5), appended per append-only convention

**The headline of this round is RETRACTED.** R-closing-path-self-consistency (same
branch, same day) showed the f ≈ 0.2 closure window was manufactured by v0-era
kick-stage manifest semantics in `phase1_leo_to_saturn.py`: the kick was carved out of
the closed-loop vehicle's own derived hardware mass, leaving a 9.2 t ghost vehicle (vs
93.2 t derived dry) to fly the mission. Under the corrected self-consistent kick model,
closure is 0 of 150 cells at every propellant fraction and every capture multiplier —
**H5 is HELD, not falsified; titan-6's collapse verdict stands, strengthened (now
f-independent).** Surviving contributions of this round: the f-window mechanism
analysis, the H3/H4/H6 verdicts, the regime-dependent-sensitivity lesson, and the
per-phase-derivation recommendation. Void: the closure counts, the 45.3 t delivered
figure, and the matrix amendment specification (superseded by
R_closing_path_self_consistency/FINDINGS.md).
