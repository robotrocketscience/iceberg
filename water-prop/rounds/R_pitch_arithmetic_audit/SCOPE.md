# R-pitch-arithmetic-audit — Tsiolkovsky-check every quantitative claim in ICEBERG-pitch.md against the framework's executors

**Status:** scope, pre-study. Authored by Saturn (orchestrator), 2026-05-22 latest+15 → 16, walking `SATURN-PUNCH-LIST-20260521.md` items S-3 + M-3 + cross-references to the five pitch corrections in punch-list section 1.

---

## Why this round

`ICEBERG-pitch.md` carries quantitative claims that have not survived first-principles checks. Saturn-worker's wonder + reason passes (commit `030cb5e`) identified five of them (punch-list P-1 through P-5). The pitch is the external-facing artifact and the highest-risk surface for the campaign — every claim there has the load-bearing job of getting an outside reader to take ICEBERG seriously. **A pitch claim that fails a Tsiolkovsky check is a deal-killer when the reader is sophisticated enough to spot it.**

Two prior rounds bracket this question but don't close it:

- **R-pricing-anchor-revisit** (worktree-105823 SCOPE, integrated to main via cherry-pick `61206bd`; still in Open SCOPEs queue) — audits the $1,400/kilogram pitch headline against per-round financial-model anchors. AUDIT.md confirms pitch headline is below what financial rounds already use. **Does not audit other quantitative claims.**
- **Saturn-worker assumption-audit** (commit `030cb5e`) — produced five locked beliefs and the punch list, but did not run a systematic per-claim audit of the pitch.

This round is the systematic audit. **It Tsiolkovsky-checks every load-bearing quantitative claim in `ICEBERG-pitch.md` against the mission_graph framework's executors and against first-principles physics, and produces a per-claim verdict table that drives the pitch rewrite.**

**Round type:** primarily AST-pass over the pitch markdown (identify quantitative claims), followed by per-claim Tsiolkovsky / framework-executor / first-principles checks, then a per-claim verdict table.

**Dependency note:** `R-framework-matrix-parity` (companion SCOPE in this same authoring pass) is upstream — once the framework is matrix-replay-trustworthy, the executors in this round can produce framework-derived ground truth for any claim that touches delivered mass, round-trip time, per-mission cost, or annual throughput. This round can begin before R-framework-matrix-parity completes (the pitch-claim identification is independent), but per-claim verdicts on framework-anchored numbers should wait.

---

## The five known-suspect claims (from punch-list section 1)

These are the claims saturn-worker flagged in the punch list. The round MUST audit them; it may surface others.

| # | Claim | Saturn-worker recommendation | Severity |
|---|---|---|---|
| P-1 | 75 percent chunk-tow delivery ratio. 100-tonne chunk delivers 75 tonnes; 1000-tonne chunk delivers 747 tonnes (belief `1488270c`). | Tsiolkovsky at stated inputs (Isp 800 seconds, delta-velocity 6.7 kilometres-per-second) gives 42.5 percent delivery, not 75 percent. Either delta-velocity is lower than cited (~2.2 kilometres-per-second; requires aerocapture to absorb entire return-leg Δv) or Isp is higher (water-microwave-electrothermal literature sits 400-800 seconds; high end feasible but not generous). Find every occurrence; correct or footnote derivation. | Highest. Drives revenue model. |
| P-2 | "Lunar surface to low-Earth orbit is ~6 km/s of delta-velocity out of a gravity well, every tonne, forever." | Correct value with aerobraking is ~4.6 km/s (1.87 ascent + 5.93 LLO-to-LEO minus 3.2 aerobraking savings per Wikipedia delta-v-budget table). The lunar-versus-ICEBERG case should NOT be argued on per-tonne Δv (loses when aerobraking is admitted); argue on source concentration (18× best-case lunar, ~100× average lunar). Re-anchor or drop. | High. Public-facing comparator. |
| P-3 | 3.2 km/s Saturn-ring departure number. ICEBERG-internal; not literature-sourced. | Local Saturn escape at B-ring radius is ~27 km/s. Realistic low-thrust spiral + Titan-assist departure is 5-9 km/s. The 3.2 figure looks like a leak from the aerobraking-savings line in the lunar accounting. Derive from low-thrust + assist mechanics, replace with sourced value, or flag as internal target needing derivation. | Medium. Internal anchor. |
| P-4 | 97 percent Saturn propellant fraction (belief `1488270c`). | First-principles reproduction from Edelbaum heliocentric Earth-to-Saturn ~20 km/s one-way, ~40 km/s round-trip; at water-microwave-electrothermal Isp 800 s (exhaust velocity 7.85 km/s), propellant fraction = 1 - exp(-40/7.85) = 99.4 percent. The 97 percent corresponds to ~32 km/s, plausible if Jupiter gravity assist trims the heliocentric leg. Publish the delta-velocity-budget breakdown or update the figure. | Medium. Qualitative claim ("Saturn doesn't close on water-electrothermal alone") survives; the specific number is wrong by ~2 percentage points. |
| P-5 | Dual-revenue mission: bulk water as logistics revenue plus consortium-funded science allocation off the same towed chunk (belief `8176e23b`). | Gap-filler found NO precedent in NASA / European Space Agency / Japan Aerospace Exploration Agency records for a sample-allocation prebuy. Existing partnerships are hardware-contribution consortia (Cassini-Huygens, BepiColombo, Hera-plus-Ramses, Mars Moons Exploration). Closest analogue: NASA-JAXA Hayabusa2 / OSIRIS-REx bilateral sample-exchange (540 milligrams traded). Find precedent or acknowledge in pitch that this is a new deal class. | Highest. Pitch business model depends on it. |

---

## The question this round answers

**For every load-bearing quantitative claim in `ICEBERG-pitch.md` (the five known-suspect ones above, plus any others surfaced by systematic audit), what is the per-claim verdict — survives / fails / needs footnote / needs derivation — and what is the recommended pitch edit?**

The round's deliverable is a **per-claim verdict table** keyed by pitch line number, with three columns: (a) the claim as written in the pitch; (b) the first-principles or framework-derived check result; (c) the recommended edit (correct in place / add footnote / replace framing / drop).

The round's secondary deliverable is a **proposed pitch diff** as a separate `PROPOSED-PITCH-DIFF.md` artifact (not applied to `ICEBERG-pitch.md` directly; orchestrator applies the diff in a follow-on pass after project-owner ratifies the per-claim verdicts).

---

## Pre-registered hypotheses (worker's honest predictions)

| # | Hypothesis | Predicted range | Falsification band |
|---|---|---|---|
| H1 | The systematic audit surfaces 8-15 additional quantitative claims beyond the five known-suspect ones, of which 2-5 fail their first-principles check. The five known-suspect claims have higher prior failure rate (saturn-worker already smelled them) than the unflagged background. | 8-15 additional claims; 2-5 additional fails. | H1 falsified if systematic audit surfaces <3 additional claims or >25; if 0 or >8 additional fails. |
| H2 | P-1 (75 percent chunk-tow delivery ratio) fails the framework-replay test once R-framework-matrix-parity lands. The framework-derived per-mission delivery ratio at the surviving cells is 30-45 percent, not 75 percent. The pitch claim was anchored on a Tsiolkovsky calculation that double-counted aerocapture savings. | Framework-derived delivery ratio at the surviving cells: 30-45 percent. | H2 falsified if framework-derived delivery ratio at any surviving cell is ≥ 65 percent. |
| H3 | P-2 (6 kilometres-per-second lunar tax framing) replaces cleanly with source-concentration framing (18× best-case / 100× average lunar ore-grade ratio). The replacement is more defensible, makes a stronger argument, and is consistent with axis 04 latest+15 amendment and axis 21 new comparator. | Replacement framing is more defensible; reader takes ICEBERG more seriously after the edit. | H3 falsified if the source-concentration framing has its own quantitative issues (e.g., the ore-grade ratio is wrong by > 2x). |
| H4 | P-3 (3.2 kilometres-per-second Saturn-ring departure) cannot be derived from low-thrust + Titan-assist mechanics under any defensible anchor. The closest defensible number is 5.5 kilometres-per-second (titan-2 R-saturn-soi-periapsis-depth `1b1b889`: SOI Δv ~0.8 km/s + Titan-gravity-assist tour ~4 km/s + heliocentric departure trim) or 7.7 kilometres-per-second (titan-3 R-delta-velocity-anchor-audit `42120cf`: vis-viva-corrected Saturn-departure). The 3.2 number should be retracted with derivation. | Saturn-ring departure Δv: 5.5-7.7 km/s under defensible anchors; 3.2 km/s indefensible. | H4 falsified if a defensible anchor produces 3.2 km/s Saturn-ring departure. |
| H5 | P-4 (97 percent Saturn propellant fraction) survives at 99.4 percent first-principles (Saturn doesn't close on water-electrothermal alone), but the specific 97 percent number is anchored on an implicit Jupiter-gravity-assist trim that the pitch text does not state. Either publish the Jupiter-gravity-assist Δv budget breakdown (which then forces the pitch to commit to the gravity-assist architecture) or update the number to 99 percent (no implicit gravity assist). | Qualitative claim survives; numerical fix to 99 percent OR explicit Jupiter-gravity-assist commitment. | H5 falsified if both options have non-trivial pitch-cost (rare). |
| H6 (load-bearing reading) | P-5 (consortium-funded science-allocation prebuy) has no precedent and must be acknowledged as a new deal class. The pitch's dual-revenue business model is therefore an architectural bet, not a derisked revenue stream. The pitch needs to either (a) downgrade dual-revenue to "potential" not "anchor"; (b) introduce R-science-allocation-prebuy-precedent-survey as a follow-on round; or (c) reframe dual-revenue around hardware-contribution consortium (which DOES have precedent — Cassini-Huygens, BepiColombo) rather than science-allocation prebuy. Option (c) is the strongest pitch-defensible path. | Reading-level: dual-revenue is reframed around hardware-contribution consortium; science-allocation prebuy is acknowledged as new-deal-class with downstream survey round. | H6 falsified if a precedent for science-allocation prebuy is found in the systematic audit. |

---

## Method (worker drafts the actual implementation)

**Step 1 — Pitch claim extraction.** Read `ICEBERG-pitch.md` end-to-end. Build a structured table of every quantitative claim: (a) line number, (b) claim text verbatim, (c) claim type (Δv, Isp, mass, cost, time, percentage, ratio, $/kg, IRR, etc.), (d) anchor source (citation if present; flag as "unsourced" if not). Expect 30-80 quantitative claims total. Output: `claims_inventory.csv`.

**Step 2 — Triage by load-bearing rank.** For each claim, classify as (a) load-bearing (claim drives an argument in the pitch — e.g., 75 percent delivery ratio drives revenue model), (b) supporting (claim provides texture but the pitch argument survives without it), or (c) descriptive (claim is factual color, not load-bearing). Audit only (a) and (b). Output: triage column added to `claims_inventory.csv`.

**Step 3 — Per-claim Tsiolkovsky / framework check.** For each load-bearing or supporting claim:
- If claim type is Δv, Isp, mass, or delivered-fraction — Tsiolkovsky-check at first principles AND framework-replay-check (once R-framework-matrix-parity lands).
- If claim type is cost, time, IRR, $/kg — framework-derived check AND cross-check against the per-round financial-model anchors (per R-pricing-anchor-revisit AUDIT.md).
- If claim type is percentage or ratio — derive from first principles + cite source.
- If claim is unsourced — flag for sourcing or removal.

Output: per-claim verdict column added to `claims_inventory.csv`.

**Step 4 — Pitch-edit recommendations.** For each FAIL verdict, draft the recommended pitch edit: (a) correct in place (number is wrong, replacement number is derivable); (b) add footnote (number is right but derivation needs to be visible to reader); (c) replace framing (the framing is wrong; replacement framing exists — e.g., P-2 source-concentration); (d) drop (number is indefensible and adds no argument the pitch can't make without it); (e) blocked (number depends on a round that hasn't run yet; defer pitch edit until the round lands). Output: per-claim recommended-edit column.

**Step 5 — Compose proposed pitch diff.** Produce `PROPOSED-PITCH-DIFF.md` as a side-by-side diff of `ICEBERG-pitch.md` showing current text and proposed text for each FAIL claim. The diff is NOT applied to `ICEBERG-pitch.md` during this round; orchestrator applies after project-owner ratifies.

**Step 6 — Reading.** Produce `READING.md` with the load-bearing reading per H6 and a project-owner-facing summary: how many claims fail, which ones are pitch-killers, which ones are derisked, recommended sequence for the pitch rewrite.

---

## Out of scope

- Actually applying the pitch diff to `ICEBERG-pitch.md`. This is project-owner-ratification work (orchestrator applies after the round closes and the project owner has reviewed the per-claim verdicts).
- Re-running revenue rounds (R-LEO-water-demand-curve, R-pricing-anchor-revisit, R-clearing-price-tail-integration-decision-frame) against a corrected 75 percent chunk-tow delivery anchor. That refresh is its own SCOPE (matrix-item M-3 → follow-on round to be authored after R-framework-matrix-parity completes).
- Authoring R-science-allocation-prebuy-precedent-survey. If P-5 reframe goes toward option (b), that round becomes a SCOPE in a future authoring pass.
- Resolving project-owner decision points #13, #14, #15. The pitch-arithmetic-audit is upstream of pitch rewrite; pitch rewrite is upstream of decisions #13. Decisions #14 + #15 are orthogonal.

---

## Inputs to acquire (reading order)

1. `ICEBERG-pitch.md` — the artifact being audited.
2. `SATURN-PUNCH-LIST-20260521.md` — section 1 with the five known-suspect claims.
3. Saturn-worker assumption-audit `water-prop/rounds/R_assumption_audit_2026_05_21/FINDINGS.md` — locked beliefs anchored against.
4. `water-prop/rounds/R_pricing_anchor_revisit/AUDIT.md` — per-round financial-model anchors for cross-check on cost / $/kg claims.
5. `water-prop/sims/mission_graph/` — framework substrate for per-claim Tsiolkovsky / replay checks (read after R-framework-matrix-parity lands its constraint encoding).
6. titan-3 R-delta-velocity-anchor-audit `42120cf` — vis-viva-corrected delta-velocity anchors.
7. titan-2 R-saturn-soi-periapsis-depth `1b1b889` — Saturn-orbit-insertion Δv anchor for P-3 cross-check.
8. Wikipedia delta-v-budget table — source for P-2 lunar aerobraking calculation.

---

## Deliverables (in commit order)

1. `STUDY.md` — pre-registered hypotheses H1-H6 frozen before the systematic audit.
2. `claims_inventory.csv` — structured table of all quantitative claims in the pitch (Step 1-2).
3. Per-claim verdict additions to `claims_inventory.csv` (Step 3).
4. `PROPOSED-PITCH-DIFF.md` — side-by-side diff for all FAIL claims (Step 5).
5. `RESULTS.md` — sweep summary; counts of survive / fail / blocked claims; cross-reference table to punch-list items P-1 through P-5.
6. `READING.md` — load-bearing reading (H6 verdict); project-owner-facing pitch-rewrite recommendation.
7. Handoff doc to orchestrator (`~/.claude/handoffs/iceberg-<worker>-<date>-pitch-arithmetic-audit.md`).

---

## Suggested worker

Any moon. Best fit: comfortable with Tsiolkovsky at first principles AND with reading-as-an-outside-reader-would the pitch document. Hyperion would be a good fit (already audited pitch-adjacent claims in R-outbound-chemical-kick-economics retraction). Iapetus would be a good fit (already produced drop-in pitch text for the staged-options reframe).

**Workflow flag:** this round is partially blocked by R-framework-matrix-parity. The pitch-claim identification (Steps 1-2) is independent and can start immediately; per-claim verdicts on framework-anchored numbers (Step 3 sub-bullet "framework-replay-check") should wait for R-framework-matrix-parity to land its constraint encoding. The Tsiolkovsky-only checks (Δv, Isp, first-principles ratio) can complete before R-framework-matrix-parity ships.

---

## Cross-references

- Matrix `water-prop/docs/ARCHITECTURE-DECISION-MATRIX.md` — High-leverage open rounds section flag for `R-pitch-arithmetic-audit` (punch-list S-3).
- `SATURN-PUNCH-LIST-20260521.md` section 1 (P-1 through P-5) + S-3.
- R-framework-matrix-parity (companion SCOPE this authoring pass) — upstream dependency for framework-anchored verdicts.
- R-pricing-anchor-revisit (Open SCOPE, worktree-105823 cherry-pick `61206bd`) — companion audit on pricing-anchor-specific claims.
- Saturn-worker assumption-audit FINDINGS.md (commit `030cb5e`) — locked beliefs anchored against for P-1, P-3, P-4, P-5.
- Wonder-pass beliefs `1488270c` (75 percent delivery ratio source), `8be3ec81` (lunar Δv accounting source), `8176e23b` (dual-revenue model source).
