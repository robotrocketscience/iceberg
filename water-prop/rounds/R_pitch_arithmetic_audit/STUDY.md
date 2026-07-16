# R-pitch-arithmetic-audit — STUDY

**Round type:** systematic claim-extraction + per-claim Tsiolkovsky / first-principles audit of `ICEBERG-pitch.md`.
**Worker:** hyperion (`worktree-121226`).
**Date:** 2026-05-22.
**SCOPE:** `water-prop/rounds/R_pitch_arithmetic_audit/SCOPE.md` (authored by Saturn orchestrator, latest+15→16).
**Commit prefix:** `exp:` (PROTOCOL deviation 5).

---

## Pre-registration integrity note (read first)

The six hypotheses below were **frozen in the SCOPE by Saturn (orchestrator) on 2026-05-22 before this worker ran.** I adopt them verbatim as the round's pre-registration and add my own point predictions in the "hyperion prediction" column.

**One material fact that reframes every hypothesis:** the SCOPE and the punch-list (`SATURN-PUNCH-LIST-20260521.md` §1) describe five suspect claims **as they stood on 2026-05-21**. The `ICEBERG-pitch.md` on disk has since been **partially revised** (it carries reader-notes through latest+9). Before doing any check I grepped the current text for each suspect literal. Result:

| Punch-list claim | Literal in current pitch? | Current state |
|---|---|---|
| P-1: 75% / 747 t delivery ratio | **No** — `75`/`747` absent | §2 now states **~54% @ Isp 700 s** (66% @1000, 70% @1200) |
| P-2: 6 km/s lunar tax | **No** — replaced | §3.4 reason 1 already shows **~4.6 km/s** with the `1.87 + 5.93 − 3.2` breakdown |
| P-3: 3.2 km/s Saturn-ring departure | **No** as a departure claim | `3.2` survives only as the *aerobraking-savings* term in the lunar line; §2 Saturn departure now **~1.5 km/s** |
| P-4: 97% Saturn propellant fraction | **No** — `97` absent | not a current pitch claim |
| P-5: consortium science-allocation prebuy | **Partially** | §6 lists it as a revenue stream, but §4 + §7 already label it **speculative / not in the table / not load-bearing** |

This means the audit is **less "catch the five errors"** and **more "did the corrections introduce new defensibility problems?"** They did — see H2/H4. The pre-registered hypotheses are scored against this reframed reality, and any hypothesis whose premise was already overtaken by a prior revision is scored as such (not silently passed).

---

## Pre-registered hypotheses (frozen in SCOPE; hyperion predictions added)

| # | Hypothesis (SCOPE, verbatim intent) | Pre-registered range | hyperion prediction (frozen pre-write) |
|---|---|---|---|
| H1 | Systematic audit surfaces 8–15 additional quantitative claims beyond the five known-suspect; 2–5 of them fail. Known-suspect have higher prior fail rate than background. | 8–15 additional; 2–5 fail | I expect ~40–60 quantitative claims total, ~10–18 load-bearing/supporting beyond the five; **1–3 additional fails** (the pitch is heavily reader-noted and self-hedged, so background fail rate is low). H1 likely **HOLDS on claim count, marginal on fail count.** |
| H2 | P-1 (delivery ratio) fails framework-replay; framework-derived delivery at surviving cells is 30–45%, not the pitch number. Anchored on a Tsiolkovsky that double-counts aerocapture savings. | 30–45% framework-derived | The framework hasn't landed (R-framework-matrix-parity unrun), so the *framework-replay* verdict is **BLOCKED**. But first-principles + the campaign's continuous-thrust finding already put delivered fraction at **17–28%** at surviving cells (titan-2 Block-4 21.8%, Option A 17%), **below the pre-registered 30–45% band**. I predict H2 **HOLDS in direction (54% fails) but the band is too generous** — true delivered fraction is lower than 30–45%. |
| H3 | P-2 replaces cleanly with source-concentration framing (18× best / 100× avg). More defensible. | replacement more defensible | Already implemented in the on-disk pitch (§3.4 reason 1 uses 4.6 km/s; reason 2 uses 98% vs single-digit %). **HOLDS, already-done.** Ore-grade ratio ~16–98× is internally consistent; not wrong by >2×. |
| H4 | P-3 (3.2 km/s ring departure) is indefensible; closest defensible is 5.5 (titan-2) or 7.7 km/s (titan-3 vis-viva); retract with derivation. | 5.5–7.7 km/s | The literal 3.2 ring-departure claim is **already gone**; §2 now says **1.5 km/s** Saturn departure — which is **even less defensible** (B-ring circular escape alone is 7.5 km/s impulsive). H4 **HOLDS and sharpens**: the replacement number is the new failure. |
| H5 | P-4 (97% propellant fraction) survives qualitatively at 99.4% first-principles; specific 97% needs Jupiter-GA budget or update to 99%. | qualitative survives; number → 99% or explicit GA | The 97% literal is **not in the current pitch.** P-4 is **moot for the pitch text** (lives in belief `1488270c`). H5 is **not testable against the current artifact**; I report it as "claim absent." |
| H6 (load-bearing) | P-5 (science-allocation prebuy) has no precedent; must be acknowledged as new deal class. Strongest path is option (c): reframe dual-revenue around hardware-contribution consortium (Cassini-Huygens, BepiColombo). | reframed; new-deal-class acknowledged | The current pitch **already does most of option (a)**: science stream is labeled speculative, excluded from the revenue table, and explicitly not load-bearing. Residual issue: §6's revenue-stream table still bills it equally ("First-and-only access") which is inconsistent with §4/§7's hedge. H6 **HOLDS but understates how far the pitch already moved**; recommended edit is small (reconcile §6 with §4/§7 + add the hardware-consortium precedent framing). |

---

## Method (as executed)

1. **Extraction.** Read `ICEBERG-pitch.md` end-to-end (556 lines). Built `claims_inventory.csv`: every quantitative claim with line number, verbatim text, type, anchor/source, triage rank, verdict, recommended edit.
2. **Triage.** load-bearing / supporting / descriptive. Audited load-bearing + supporting only.
3. **Per-claim check.** Tsiolkovsky at first principles (Δv, Isp, delivered fraction); orbital mechanics for Saturn-side Δv; cross-check against in-repo campaign anchors (titan-3 `42120cf` vis-viva; titan-2 `1b1b889` SOI; pitch line-35 continuous-thrust 24.7/29.56 vs 6.42 impulsive; locked beliefs). Framework-replay checks deferred (R-framework-matrix-parity unrun) and marked BLOCKED.
4. **Edits.** correct-in-place / footnote / replace-framing / drop / blocked.
5. **Diff.** `PROPOSED-PITCH-DIFF.md` — not applied; orchestrator applies after project-owner ratifies.
6. **Reading.** `READING.md` — H6 verdict + pitch-rewrite sequence.

## Verification calculations (reproducible)

```
g0 = 9.80665 m/s²;  ve(Isp) = Isp·g0;  delivered = exp(−Δv/ve)
Saturn GM = 3.7931e16 m³/s²;  B-ring r = 117,000 km

Pitch §2 face value (impulsive inbound 4.2 km/s):
  Isp 700 s  → 54.2%   Isp 1000 s → 65.2%   Isp 1200 s → 70.0%   ✓ reproduces pitch
B-ring orbital mechanics:
  v_circ = 18.0 km/s   v_esc = 25.5 km/s   escape Δv (impulsive) = 7.5 km/s
  → pitch's 1.5 km/s Saturn departure is 5× too low; pitch's own §1 says v_orbit ~17 km/s
Fix Saturn departure to defensible 5.5 / 7.7 km/s (impulsive, Isp 700 s):
  inbound delivered → 30.3% / 22.0%
Continuous-thrust accounting (campaign anchor: 24.7 km/s inbound, pitch line 35):
  Isp 700 s → 2.7%   Isp 1000 s → 8.1%   Isp 2000 s → 28.4%
Lunar check: 1.87 + 5.93 − 3.2 = 4.60 km/s  ✓ arithmetic correct
```

**Load-bearing reading (preview; full in READING.md):** the pitch's central "the math closes at ~54% delivery" claim (§2) is impulsive-accounted on an indefensible 1.5 km/s Saturn-departure input. It is the *same root error* as the retired 75% (P-1): impulsive frame + low Saturn-side anchor. The honest delivered fraction at surviving cells is **17–28%**, not 54%. Exact framework number is BLOCKED on R-framework-matrix-parity; the directional FAIL is confirmed now from first principles.
