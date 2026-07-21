# R-mothership-threat-split — decomposing R185's damaging-failure fraction into chunk-loss vs mission-loss

**Status:** SCOPE pre-registered 2026-07-21, before `run.py`. Bounds from `scope_bounds.py`, committed alongside. One pre-freeze correction documented below (an initial H4 intuition was falsified by the pre-script and the hypothesis re-registered to what the mechanism actually does — R177/R182 lineage).
**Worker:** worktree-115637 session. R185's Revisit named the gap: *"damaging-failure consequences are simplified (chunk loss, mission continues; mothership-threatening subsets unmodeled)."* This round models that subset. The mothership carries the reactor, all N chunks aboard, and the return capability; its loss is **total mission loss**, which R185 (correctly for its scope) folded into "chunk loss," slightly under-counting consequence.

## Model

Stage-weighted mothership threat (the refinement over a flat φ_ms): damaging failures distribute across the five handoff stages in proportion to each stage's failure probability, and each stage carries a distinct conditional probability that *its* damaging failure threatens the mothership. Conditional-threat desk anchors (swept ±30 % in `run.py`): rendezvous 0.00 (far; clean abort), prox-ops 0.05, **berth_bag 0.35 (40 t non-rigid load in contact — the driver)**, mate 0.25 (load-path failure at the dock), sep 0.15 (recontact). Because the highest-failure-probability stage (berth_bag) is *also* the highest-threat stage, the correlation lifts φ_ms above a naive flat guess. Swap (rigid 6 t module) threat scaled 0.6×, one per mission. Economics compose onto R185's ops-honest 0.453: risk-adjusted lpd = 0.453 / P(mothership survives).

## Pre-registered hypotheses (bounds scripted)

**H1 [S] (φ_ms from stage decomposition).** The stage-weighted mothership-threat fraction of damaging failures is **0.17–0.31** (scripted central 0.24, high-threat corner 0.31), **berth_bag-driven** (its failure-prob × threat 0.08 × 0.35 dominates the sum). Nearly band-invariant in the stage probs (it is a ratio); the spread comes from the threat-anchor sweep. Falsified outside 0.15–0.35.

**H2 [S] (central consequence is a small economics line).** At the central corner (N=4, 3-try, f_dmg 10 %, φ_ms 0.24) the mothership-loss probability per handoff is 0.42 %, mission-total-loss **1.5–2.5 %** (scripted 1.9 %), inflating risk-adjusted lpd from 0.453 to **0.46–0.47** (scripted 0.462). On economics alone the tail is minor. Falsified outside bands.

**H3 [S] (the tail is program-defining).** At the stress corner (low stage band, f_dmg 20 %, φ_ms 0.31, N=5) mission-total-loss reaches **7–12 %** (scripted 8.5 %) — a **single-point catastrophic risk that forfeits the reactor and all chunks**, risk-adjusted lpd **0.49–0.52** (scripted 0.495). The consequence is not the lpd delta; it is that a ~1-in-12 chance of losing a reactor-bearing mothership is a program-ending event no economics line captures. Falsified outside bands.

**H4 [W] (the retry policy is mothership-safe — the naive tension does NOT bind).** *Pre-freeze correction:* the intuitive worry (each berth retry is another close approach, so retries should expose the mothership and cap the try-count) is **falsified by the pre-script**. Incremental per-retry mothership exposure decays geometrically (∝ bᵏ, conditioned on prior benign failure), so it is dominated by the retention gain at **≥ 50:1** (scripted 233:1 central, 55:1 stress); EV-optimal try-count is **≥ 3 at every corner** (scripted 6). The catastrophic tail is an **N-and-φ_ms phenomenon, monotone-increasing in N** (scripted central 0.6 % → 2.7 % over N=1→6), not a retry-count one. R185's always-retry policy is vindicated even with the mothership as the asset at risk. Falsified if any swept corner shows EV-optimal tries < 3 or a 3rd-retry ratio < 50:1.

## Sweep (run.py)

φ_ms vs threat-anchor scale ∈ [0.7, 1.3]; mission-total-loss surface over N ∈ {1–6} × f_dmg ∈ {5, 10, 20 %} × band {low, central, high}; retry-count EV curves at central and stress corners; risk-adjusted lpd and d\* per cell. Grids span the pre-script's.

## Deliverables

`scope_bounds.py`, `run.py` (+ `results/mothership_threat.png`), `results/findings.json`, `STUDY.md` with Revisit; orchestrator notes: the demonstrator's LEO handoff-rehearsal gate (R185) gains a **specific objective — bound the berth-contact mothership-threat conditional, since it drives both the retention floor and the catastrophic tail**; the mothership is a named single-point-of-failure in the risk register; R185's retry policy confirmed mothership-safe (the tension does not bind).
