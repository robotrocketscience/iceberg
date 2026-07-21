# R-array-spare-regeneration — STUDY

**Round:** R-array-spare-regeneration. SCOPE pre-registered 2026-07-21 with scripted bounds (`scope_bounds.py`), before `run.py` existed. Two pre-freeze corrections documented in the SCOPE itself.
**Worker:** worktree-115637 session. Owner-directed, including the mid-round EP question this round adjudicates.

## Results vs registered hypotheses — all four HELD

### H1 — regression and continuity — **HELD**

`off` reproduces R177's canonical exactly (91.3 t / 767 t); `rtg` mode lands within 0.5 % of R177's N=4 (622 vs 619 — the documented ops-credit cap refinement). RTG marginal value at the canonical corner *with array regeneration live* is **19.5 t per MMRTG** — R177's ~19 t/unit survives, now decomposed as keep-alive coverage + ops credit rather than inbound trickle.

### H2 — the best corner moves — **HELD**

Ops-phase regeneration (electrolyzing chunk water at the ring station to feed the departure burn) cuts the standing best corner from **547 to 503 t (−8 %)**, ratio 5.47 → 5.24 on this round's full-kick basis — hybrid-translated headline ≈ **3.28×** (secondary estimate pending a hybrid-basis port). The ops-extension trade is real and linear: **30–33 t of launch per added ops year**, schedule-bounded (13.4 yr at T_ops 3.0 vs L0-05's 15), not cap-bounded. Ring-ops duration is now a first-class economic lever.

### H3 — power-poor corners transformed — **HELD**

Array-spare regeneration recovers **212 t** of launch at the canonical corner (767 → 555) and **147 t** at 200 kW/80 t — with **zero plutonium**. R177's "value concentrates at ops" reading survives only at 300 kW; at 100–200 kW the inbound spare dominates. The non-fission variant's arrays were carrying an unused asset the whole campaign.

### H4 — the owner's EP proposal, adjudicated — **HELD (and it wins where it matters)**

(a) At the best corner, gated dark-leg EP changes nothing (0.0 t — no residual demand; the inside-4-AU lit leg already closed the return). (b) At the canonical corner, **EP-only beats full-electrolysis on the campaign's ratio metric (13.55 vs 13.78)** while losing on launch mass (629 vs 555 t) — the session's own "electrolysis dominates 1.53:1" claim, made hours before this SCOPE, is **falsified on the metric that matters**. The two-regime allocation law stands: electrolysis wins impulse-per-joule (1.53×), EP wins chunk-mass-per-m/s (exhaust 7848 vs 4709 m/s = 1.67×), and the ratio metric weights the latter. (c) The composite is best-or-tied at every probe (mid corner: 5.79 in the sweep grid, 5.72 at the fine φ scan, vs 5.82 EP / 5.97 regen).

## Bug-catch (protocol §bug-catch)

Both catches were pre-registration, during pre-script review, and are documented in the SCOPE (EP propellant double-count; allocation-order violation letting EP eat demand first). One render-review catch post-run: panel-B annotation collided with the schedule label; fixed before shipping (second consecutive round — render review is earning its place as a mandatory step).

## Revisit (mandatory)

Thin spots carried honestly: regeneration/burn scheduling unmodeled (credits assume demand lands after accrual); tank-capacity headroom within the inbound phase unchecked; electrolyzer feed purity from chunk water is bet-#2-adjacent and unpriced; the sweep's mix grid is coarse (φ ∈ {0.25, 0.5, 0.75}; fine scan only at the three probes — the mid-corner optimum sits at φ=1.0, outside the sweep grid, caught by the registered fine-scan); economics are full-kick 2-stage, so the 3.28× headline is a translation, not a hybrid-basis measurement. **Ledger inconsistency flagged for the orchestrator:** R173/R174 never carried lit-leg propellant mass through the departure burn nor debited it from delivered (harvest-margin convention); this round debits everything it introduces. A reconciliation pass (or the named trajectory-scheduled lit-thrust round) should unify the chunk-water ledger.

## Cross-learning

- **New standing best-corner candidate: ≈ 3.28×** (from 3.57×), via ops regeneration alone — needs orchestrator ratification and a hybrid-basis confirmation before the matrix headline moves.
- **The allocation law for the matrix:** spare joules → electrolysis when energy is scarce relative to gas demand; → dark-leg EP when energy is abundant (it spends 1.67× less chunk per m/s); ops-phase spare always serves the departure burn first. The owner's EP instinct was right in the regime the campaign's metric actually rewards.
- **R177's RTG statement survives intact** (19.5 t/unit at power-poor corners, worthless at 300 kW), now correctly benchmarked against a regeneration-enabled baseline.
- **Follow-on candidates:** burst-duty-cycle optimization (owner interest; R172 H4 anchor); chunk-water ledger reconciliation + trajectory-scheduled lit thrust; keep-alive product-water recovery; hybrid-basis port of rounds 177–178 economics.
