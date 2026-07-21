# R-mothership-threat-split — STUDY

**Round:** R-mothership-threat-split. SCOPE pre-registered 2026-07-21. All four hypotheses **HELD** — including H4, which holds in the *opposite* direction from the intuition that motivated it.

## Results vs registered hypotheses — all four HELD

### H1 — φ_ms from stage decomposition — **HELD**

The stage-weighted mothership-threat fraction of damaging failures is **0.24 central** (band 0.17–0.31 across the threat-anchor sweep), and it is **berth_bag-driven**: that stage's failure-probability × threat-conditional (0.08 × 0.35) contributes more than the other four stages combined. The refinement over a flat φ_ms matters precisely because the riskiest stage is also the highest-threat one — the correlation is adverse.

### H2 — central consequence is a small economics line — **HELD**

At the central corner (N=4, 3-try, f_dmg 10 %, φ_ms 0.24): mothership-loss per handoff 0.42 %, **mission-total-loss 1.9 %**, risk-adjusted lpd 0.453 → **0.462**. On economics alone the mothership tail barely moves the needle — R185's folding it into "chunk loss" was numerically forgivable at central anchors.

### H3 — the tail is program-defining — **HELD**

At the stress corner (low stage band, f_dmg 20 %, φ_ms 0.31, N=5): **mission-total-loss 8.5 %**, risk-adjusted lpd 0.495. The point is not the 0.04 lpd delta — it is that a **~1-in-12 chance of losing a reactor-bearing mothership with all N chunks and the return capability aboard** is a program-ending event no economics line captures. This is the true consequence R185 deferred, and it lives in the same desk-anchor uncertainty band as bet #1.

### H4 — the retry policy is mothership-safe (the naive tension does NOT bind) — **HELD**

The hypothesis that motivated this round — *each berth retry is another close approach, so retries should expose the mothership and cap the try-count* — was **falsified by the pre-script before SCOPE froze**, and H4 was re-registered to what the mechanism actually does (R177/R182 lineage). Incremental per-retry mothership exposure decays geometrically (∝ bᵏ, each retry conditioned on the prior having *benignly* failed), so it is dominated by the retention gain at **233:1 (central), 55:1 (stress)** — both far above the 50:1 floor. EV-optimal try-count is **6 at every corner** (≥ 3). The catastrophic tail is an **N-and-φ_ms phenomenon, monotone-increasing in N** (central 0.6 % → 2.7 % over N=1→6), not a retry-count one. R185's always-retry policy is vindicated even with the mothership as the asset at risk: you protect the asset by limiting **how many chunks you berth**, not by berthing each one more timidly.

## Bug-catch (protocol §bug-catch)

The H4 pre-freeze correction is documented above and in SCOPE — it is a re-registration, not a run-time bug. No run-time bug; all four bands reproduced the pre-script.

## Revisit (mandatory)

All threat-conditionals are desk anchors with no flight precedent for a bagged 40 t non-rigid berthing — the campaign's 85 %→46 % lesson applies to *these* numbers too; the bands are the claim. The model treats a mothership-threatening event as instantaneous total loss; a partial-damage / degraded-return spectrum (reactor survives, one chunk lost, mission limps) is unmodeled and would soften the tail. Correlated failures (a berth RUD that also damages the next chunk in queue) are not modeled — they would worsen it. The swap threat-scale (0.6×) is a guess. The retry-safety result assumes each attempt's mothership risk is independent and identical; a "damage accumulates across attempts" model (each failed berth degrades the bag or the dock) could reintroduce a binding tension and is the one way H4 could flip — named as the sharpest follow-on.

## Cross-learning

- **For the demonstrator (matrix):** the LEO handoff-rehearsal gate (R185) gains a **specific measurement objective — bound the berth-contact mothership-threat conditional**, because that single number drives both the retention floor (R185) and the catastrophic tail (this round). The mothership enters the risk register as a **named single-point of failure**, tail probability 2–9 % across the honest band.
- **R185 retry policy confirmed mothership-safe** — the tension does not bind; the lever for tail risk is **N (chunks per mission)**, which puts the fleet-economics push toward high N (R182/R184: amortize the reactor) into direct tension with catastrophic-loss exposure. That N-tradeoff (economic optimum vs risk-aware optimum) is the quantitative follow-on.
- **Follow-ons:** the risk-aware optimal-N round (economic vs catastrophic-loss optimum, needs R184's N-dependent lpd); a damage-accumulation retry model (the one path to flip H4); a partial-damage consequence spectrum.
