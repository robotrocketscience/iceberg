# READING — R-shared-physics-audit

**Round:** R-shared-physics-audit
**Worker:** mimas (commits `7cada59` → audit-script `feat(scripts)`)
**Branch:** iceberg-mimas
**Status:** complete; load-bearing reading H6 held.

---

## Hypotheses adjudicated

| # | Predicted (SCOPE) | Mimas point | Observed | Verdict |
|---|---|---|---:|---|
| H1 | 3 ≤ N ≤ 12 | 5–7 | **3** | held (low edge) |
| H2 | 4 ≤ Tier-A ≤ 10 | 2–4 | **0** | **falsified low** |
| H3 | ≥ 1 Tier-A verdict-flip | 0 (SCOPE-null) | **0** | SCOPE-falsified; mimas-held |
| H4 | All 3 known catches assertion-catchable | partial (1 in-scope) | 1 of 1 in-scope catchable under Mechanism B (named-helper-pair) | held with refined mechanism |
| H5 | ≤ 200 lines, ≤ 30 s | held with margin | **178 lines, 1.63 s** | held |
| H6 (load-bearing) | cleanup parallel, not architecturally rescuing | held | 0 live-decision flips; closure cell anchored on clean rounds | **held** |

Detailed adjudication per hypothesis: `results/H1.md` through `results/H6.md`.

---

## Headline

**3 of 136 rounds contaminated by the function-convention bug class; 0 are Tier-A; the audit confirms reactive triage caught the live cases and produces a canonical helper-pair + enforcement gate so the bug class cannot recur. The "every test is contaminated" framing is overstated by ~45×.**

---

## Reading

### For the project owner

The challenge — "every test is contaminated and needs to be re-run with this new reality" — was right that the bug class exists and wrong about its magnitude.

- **Magnitude:** 3 contaminated rounds out of 136 (2.2%). Reactive triage already caught all three. Two have been superseded by clean reruns (`R_electric_outbound` by `R_electric_outbound_rerun`; the megawatt cell by 500-kilowatt-electric retirement at latest+13); one (`R_redundancy_budget_cost`) has its load-bearing finding (per-vehicle redundancy cost) in a branch the bug does not touch.
- **Live-decision impact:** zero. The titan-3 40-80 tonne / 30 kilowatt-electric closure cell — the single still-live closure — is anchored on clean rounds. No contaminated round flips a live verdict.
- **Binding constraints unchanged:** decision points #5 (pricing anchor), #14 (reactor power class), #15 (L0-04 strict deliver-to-Earth-orbit). These are project-owner adjudication items. The audit does not move them.

### Therefore

Function-convention cleanup proceeds in parallel with the anchor decisions. It does not gate them. The audit's contribution is structural — diagnosis reframe, canonical helper-pair, enforcement gate — not architectural rescue.

**No project-owner action required from this audit.** The next critical-path rounds are R-kilopower-scale-up-credibility (decision point #14) and R-pricing-anchor-revisit H7 (decision point #5), both already in the Open SCOPEs queue.

---

## Cross-learning

### Methodology lesson 6 ("shared-physics function input conventions need assertions") needs amendment

The lesson as authored (after hyperion's catch) assumed the convention-bearing function lives in `waterprop/`. It does not — `constant_thrust_burn` was defined locally in 6 rounds with one convention-inverted variant (`R_non_fission_baseline` documents `m_initial_t` as post-burn final mass; the other 5 documents wet-at-start). The contagion pattern is **copy-pasted-physics with per-round drift**, not shared-library-function-with-many-callers.

Proposed PROTOCOL amendment (candidate lesson 17 or 21, awaiting orchestrator ratification):

> **Methodology lesson 17 candidate — round-local redefinition of physics-helper functions invites convention drift.** When a round defines a helper function locally (rather than importing from `waterprop/`), the convention lives only in that round's docstring and the next round to copy-paste the helper may invert the convention silently. The R-shared-physics-audit found that 6 rounds redefined `constant_thrust_burn` with one convention-inverted variant out of the six. The fix is twofold: (a) lift any helper that appears in ≥ 2 rounds into `waterprop/`, pinning the convention by function name (e.g., `burn_from_wet` / `burn_from_dry_end`); (b) flag any new local redefinition of a name in the shared library via `audit-call-conventions.py`. Lesson 6 was the right diagnosis but the wrong enforcement scope.

### Mechanism B (named-helper-pair) is the actual assertion mechanism

Lesson 6 said "add `assert` statements at function entry." The audit's H4 verdict refines this: a value assertion cannot disambiguate wet-at-start from dry-at-end at the function entry, because `m_dry` and `m_prop` are not available inside the function. The actual mechanism is **separate functions with the convention pinned in the name** (`burn_from_wet` vs `burn_from_dry_end`). The caller commits to the convention via the import. Runtime assertions (`m_initial_t > 0`, `dv > 0`, `power > 0`) are sanity checks, not convention checks.

This pattern was already invented by rhea in `R_electric_outbound_rerun` (the hyperion-bug fix round). The audit lifts it from one round's local code into the shared library at `water-prop/src/waterprop/propulsion/burns.py`.

### The reactive triage already worked

The campaign has 14 rounds with `_audit` / `_revisit` / `_rerun` / `_consistency` suffixes — about 10% of the tree. The reactive pattern caught every Tier-A bug before this audit could surface a new one. The systematic audit is therefore confirmatory + preventive, not novel-finding. Reactive triage is doing its job; the new enforcement gate (`audit-call-conventions.py`) just prevents the bug class from re-entering after migration.

---

## Next-round candidates

### Tier-A re-runs — none

No Tier-A rounds identified. The 3 contaminated rounds are all Tier-B (superseded, closed-by-directive, or incidental-to-load-bearing-finding). See `results/H2.md` per-round tier rationale.

### Migration plan for the 11 rounds carrying deprecated `constant_thrust_burn` / locally-redefined `burn_from_wet` / `burn_from_dry_end`

The enforcement script flags 18 violations across 11 rounds. **Migration is NOT in scope for this round** (out-of-scope guard per ASSIGNMENT.md: "do not run any Tier-A re-runs yourself"). The migration is a follow-on activity, ordered by load-bearing-ness:

| Round | Lines to migrate | Notes |
|---|---|---|
| R_electric_outbound_rerun | 134, 155 | The reference implementation. Migration is symbolic — its local `burn_from_wet` / `burn_from_dry_end` are byte-equivalent to the canonical pair. Suggest: remove local defs, import canonical, verify results bit-equal. |
| R_outbound_dv_continuous_thrust | 152, 170 | Same pattern as the rerun. |
| R_arch_E_specific_power_flown_anchored | 74, 84 | Same pattern. |
| R_architecture_E_no_saturn_side_electrolysis | 78, 88 | Same pattern. |
| R_megawatt_marvl_radiator | 157, 167 | Same pattern. |
| R_megawatt_relaxed_specific_power | 53, 63 | Same pattern. |
| R_electric_outbound | 137 | Round superseded; do not migrate — leave deprecated local def as historical record. Carve-out in `audit_carveouts.py` if the round is kept in the tree. |
| R_megawatt_architecture_viability | 62 | Round's headline retired by directive; migration optional. |
| R_redundancy_budget_cost | 162 | Round's load-bearing finding (per-vehicle cost) stands; migration optional. |
| R_all_electric_thruster_sweep | 87 | Active round; migrate to `burn_from_wet`. |
| R_inbound_dv_continuous_thrust | 160 | Active round; migrate to `burn_from_wet`. |
| R_non_fission_baseline | 89 | **Convention-inverted variant** — migrate to `burn_from_dry_end`. Verify per-call-site argument is dry mass not wet (manual; the round documents the convention but a future reader could misread).  |

Suggested batching: one PR per "active" round (4-5 PRs total), each replacing the local definition with the canonical import and asserting results bit-equality against the round's checked-in CSV. Once migration completes, enable the gate in CI / pre-commit.

### Follow-on round candidates (out of this audit's scope)

1. **R-matrix-anchor-audit** — the enceladus-r5 bug class (matrix-stated Variant B numbers not reproducing from first principles). Out of scope for the function-convention audit but flagged in SCOPE §"Reading template" as a per-cell follow-on. Highest-leverage starting points: year-zero-through-fifteen Kilopower Variant B cell, year-twenty-plus megawatt cell (now closed-by-directive, lower priority). Audit method: per-cell re-derivation, NOT call-graph walking. Worker fit: light on Python, heavy on physics + spreadsheet recompute.

2. **PROTOCOL methodology-lesson amendment** — orchestrator (Saturn) integrates the lesson-17-candidate text into `water-prop/PROTOCOL.md` as part of the next integration pass. Not a research round; orchestrator pen-stroke.

3. **Round-local convention-inversion audit** — extend the AST walker in this round's `run.py` to flag any pair of rounds that defines the same helper-name with different formulas. The `R_non_fission_baseline` variant is the only one currently inverted from the consensus; a future inversion would be silently inserted. The current `audit-call-conventions.py` flags redefinition, not inversion.

---

## Deliverables manifest

- `STUDY.md` — pre-registration (`fc7ed1e`).
- `run.py` — AST walker + call-graph builder + tiering (`f1dd8ff`).
- `contamination_matrix.csv` — round × callee × verdict × tier (`f1dd8ff`).
- `results/library_functions.json` — library catalogue (`f1dd8ff`).
- `results/round_local_defs.json` — round-local redefinitions (`f1dd8ff`).
- `results/call_sites.json` — every flagged-function call site with raw args (`f1dd8ff`).
- `results/summary.json` — aggregate counts (`f1dd8ff`).
- `results/H1.md` through `results/H6.md` — per-hypothesis verdict files (`c62e2c3`).
- `water-prop/src/waterprop/propulsion/burns.py` — canonical helper-pair (`f84f587`).
- `water-prop/src/waterprop/propulsion/__init__.py` — exports (`f84f587`).
- `water-prop/src/waterprop/propulsion/nep_optimum.py` — assertion-on-entry for shared library convention-bearing functions (`f84f587`).
- `water-prop/scripts/audit-call-conventions.py` — enforcement gate (next commit).
- `water-prop/scripts/audit_carveouts.py` — blessed-line data module (next commit).

Branch: `iceberg-mimas`. Worktree: `~/projects/iceberg/.claude/worktrees/mimas/`.
