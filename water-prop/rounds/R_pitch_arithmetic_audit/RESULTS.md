# R-pitch-arithmetic-audit — RESULTS

**Worker:** hyperion · **Date:** 2026-05-22 · **Artifact audited:** `ICEBERG-pitch.md` (556 lines, reader-notes through latest+9).

## Headline

The pitch's central arithmetic claim — **"the math closes at ~54% chunk delivery on a ~13 km/s round-trip" (§2)** — **FAILS.** It reproduces correctly at face value but rests on two indefensible inputs: an impulsive ΔV frame for low-thrust electric legs (campaign finding: continuous-thrust is 3.8–6.3× higher) and a **1.5 km/s Saturn departure** that is physically impossible from the circular B-ring orbit the pitch itself describes (escape alone is 7.5 km/s). The honest delivered fraction at surviving cells is **17–28%, not 54%** — the *same root error* as the punch-list's already-retired 75% (P-1): impulsive accounting + low Saturn-side anchor.

**The good news for the pitch:** the five punch-list literals are mostly already gone (the pitch was revised since 2026-05-21). The bad news: one correction (75% → 54%) preserved the error class, and another (3.2 → 1.5 km/s departure) made the Saturn-departure number *worse*.

## Tally (35 quantitative claims; load-bearing + supporting audited)

| Verdict | Count | Claim IDs |
|---|---|---|
| SURVIVE | 21 | C01, C04–C09, C14, C16, C18, C19, C21, C23, C25, C27, C29, C30, C31, C32, C34, C35 |
| FAIL (hard, arithmetic/physics) | 4 | **C10** (impulsive frame), **C12** (1.5 km/s departure), **C13** (54% delivery), **C22** (1.5 km/s in lunar comparison) |
| FAIL-framing | 1 | **C33** (P-5 science-stream over-billed vs §4/§7 hedge) |
| FAIL-dependent / already-reader-noted | 5 | C03, C17, C20, C26, C28 (downstream of C13 + reactor-class; matrix already flags) |
| FOOTNOTE / MARGINAL / UNSOURCED | 3 | C02, C11, C24 |
| BLOCKED on R-framework-matrix-parity | 1 | C15 (power-per-chunk sizing) |

The four hard fails **collapse to one root cause**: the §2 ΔV budget. C10/C12/C13/C22 are the same error seen four times.

## Cross-reference to punch-list P-1 … P-5

| Punch-list | Status in current pitch | This round's verdict |
|---|---|---|
| **P-1** 75% delivery ratio | Literal gone; replaced by 54% (§2) | **FAIL persists in new form (C13).** Root error (impulsive + low anchor) survived the 75→54 edit. True value 17–28%. |
| **P-2** 6 km/s lunar tax | Already fixed → 4.6 km/s with `1.87+5.93−3.2` breakdown (§3.4) | **RESOLVED (C21).** Arithmetic correct; source-concentration framing (98% vs single-digit %) present. H3 holds. |
| **P-3** 3.2 km/s ring departure | Literal gone as a departure claim; §2 now 1.5 km/s | **FAIL, sharpened (C12).** 1.5 km/s is *less* defensible than 3.2; should be 5.5–7.7 km/s (titan-2 / titan-3 vis-viva). |
| **P-4** 97% propellant fraction | Not present in current pitch text | **MOOT for the artifact (H5 untestable).** Lives in belief `1488270c`; no pitch edit needed. |
| **P-5** consortium science prebuy | Heavily hedged in §4/§7; over-billed in §6 | **FAIL-framing, minor (C33).** Pitch already does most of option (a); reconcile §6 with the §4/§7 hedge and recast as hardware-contribution consortium (option c). |

## Hypothesis scoring

| # | Verdict | Note |
|---|---|---|
| H1 | **HOLDS (count), MARGINAL (fails)** | 35 claims total (≈30 beyond the five); hard fails beyond P-1/P-3/P-5 = effectively the ΔV-table cluster, which is 1 root error. Background fail rate low, as predicted — the pitch self-hedges heavily. |
| H2 | **HOLDS in direction; band too generous; framework-replay BLOCKED** | 54% fails; true 17–28% is *below* the pre-registered 30–45%. Exact framework number deferred to R-framework-matrix-parity. |
| H3 | **HOLDS (already implemented)** | Source-concentration framing in place; ore-grade ratio 16–98× internally consistent. |
| H4 | **HOLDS and sharpens** | Replacement 1.5 km/s is the new failure; defensible band 5.5–7.7 km/s confirmed. |
| H5 | **NOT TESTABLE (claim absent)** | 97% not in current pitch. |
| H6 (load-bearing) | **HOLDS, understates prior movement** | Dual-revenue already not load-bearing in the pitch; residual is a §6↔§4/§7 reconciliation + hardware-consortium precedent framing. No precedent for science-allocation prebuy found. |

## What this round does NOT close (out of scope / blocked)

- **Exact framework-derived delivered fraction** (C13, C15) — blocked on R-framework-matrix-parity. Directional FAIL is confirmed now.
- **Revenue-round re-run** against a corrected ~17–28% delivery anchor (C20, C26) — separate SCOPE (punch-list M-3), to be authored after R-framework-matrix-parity.
- **Program-value / capital-class** reconciliation (C26, C28) — iapetus staged-options + L0-24 territory, not arithmetic.
- **Applying the diff** — see `PROPOSED-PITCH-DIFF.md`; orchestrator applies after project-owner ratifies.
