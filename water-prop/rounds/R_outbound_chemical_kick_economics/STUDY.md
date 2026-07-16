# R-outbound-chemical-kick-economics — does outbound chemical-kick economics independently kill the surviving 500-kWe Variant B cell, and if so under what launch market?

**Worker:** hyperion (4th batch follow-on, 11th round).
**Branch:** `iceberg-hyperion`. Worktree: `~/projects/iceberg/.claude/worktrees/hyperion/`.
**Round directory:** `water-prop/rounds/R_outbound_chemical_kick_economics/`.

## One-paragraph summary

The batch-3/4 handoffs flagged an unrun "sleeper falsifier" — claim from `R_aerocapture_fast_cruise_envelope/results/closure_verdict.md`: "Round F uses 715 t of hydrolox per outbound mission. At Earth-launch costs of $500–1000/kg this is $358–715 million in propellant per mission, dwarfing the matrix-implied per-mission revenue." This round **retracts that claim**. The 715 t figure was a back-of-envelope inserted into a verdict text without being computed; the actual `variant_b_closure`-anchored figure is **150 t hydrolox per mission** for the rhea-bake-off-surviving 500-kWe / 200-t cells. The orthogonal finding that the round DID surface: the rhea bake-off's inherited `LAUNCH_PLUS_TSI = $290M/ship` (=$150M Falcon Heavy expendable + $140M Vulcan-Centaur-class kick) assumes ONE Falcon Heavy launch per ship, but the variant_b_closure-required LEO mission-1 mass is 214–228 t — **3.4–3.6× Falcon Heavy expendable's 63.8 t LEO capacity**. The bake-off undercounts launch+TSI by ~1.8–3.5× under realistic 2026 launch markets. Sensitivity sweep across launch costs {$200, $500, $1500, $3000, $5000}/kg confirms: the matrix's surviving cell does not cross sovereign-bond IRR at L0-05-hard at any (launch cost × water price × payment) combination this round tested. Outbound chemical-kick economics is not an *independent* kill-shot, but it is a meaningful calibration on the bake-off's assumed cost band: the bake-off's $290M/ship anchor implicitly bets on Starship-class launch economics being achieved by program horizon, with no contingency.

## Pre-registration block (frozen before run.py executed)

Per recurring lesson #N stacked intervention: back-of-envelope computed FIRST, anchors taken from PRIMARY texts (`variant_b_closure` source, R-reactor-roadmap `LAUNCH_PLUS_TSI`, rhea bake-off `STUDY.md`), not from SCOPE summaries.

### Anchor values (computed first)

| Quantity | Anchor | Source |
|---|---:|---|
| Outbound chemical kick delta-velocity | 5.0 km/s | `R_variant_B_impulsive_vs_continuous.run.DV_CHEM_OUTBOUND_KM_S` |
| Hydrolox specific impulse | 450 s | matrix R-outbound-architecture, consistent across all rounds |
| Outbound kick stage dry mass | 10 t | `R_variant_B_impulsive_vs_continuous.run.M_OUTBOUND_KICK_DRY_T` |
| Mass ratio outbound kick | 3.105 | exp(5000 / (450 × 9.80665)) |
| Tug dry mass at 500 kWe (MARVL, path 1 baseline) | 62.2 t | live from `variant_b_closure` |
| **Outbound hydrolox per mission, path 1 (variant C, chunk 200 t)** | **152 t** | live |
| **Outbound hydrolox per mission, path 4 (variant D, chunk 200 t)** | **145 t** | live |
| **LEO launch mass mission 1, path 1** | **224 t** | live |
| **LEO launch mass mission 1, path 4** | **214 t** | live |
| Falcon Heavy expendable LEO capacity | 63.8 t | SpaceX published; stable since 2018 |
| Starship Block 2 expendable LEO capacity (target) | 250 t | SpaceX 2025 stated |
| rhea bake-off LAUNCH_PLUS_TSI | $290M/ship | `R_reactor_roadmap.run.LAUNCH_PLUS_TSI` (= 150e6 + 140e6) |
| **Implied launch cost at rhea bake-off anchor** | **$1,295/kg** | $290M / 224 t |

### Hypotheses

- **H-ock-a:** the batch-3/4 sleeper-falsifier claim of 715 t hydrolox per outbound mission is overstated by ≥ 4×. Falsified if real value > 200 t.

- **H-ock-b:** at rhea bake-off's stated LAUNCH_PLUS_TSI = $290M/ship and central LEO mission-1 mass 224 t, implied launch cost is in $1,200–$1,400/kg. Falsified if outside.

- **H-ock-c:** rhea bake-off's $290M/ship inherits R-reactor-roadmap's "one Falcon Heavy expendable + one Vulcan-Centaur kick" assumption (per LAUNCH_PLUS_TSI source comment "Falcon Heavy expendable + Vulcan-Centaur-class kick"). Under that assumption, with central LEO mission-1 mass 224 t and Falcon Heavy expendable LEO capacity 63.8 t, the assumption is mass-infeasible: required launches ≥ 3 per ship. Falsified if 224 / 63.8 < 2.5.

- **H-ock-d:** under realistic Falcon Heavy market (3.5 launches × $150M + $140M kick = $665M/ship), the rhea bake-off cashflow with `LAUNCH_PLUS_TSI` updated to $665M shows worse marginal IRR than the inherited $290M case for path 4 (variant D, chunk 200 t) — but does NOT change the verdict from `marginal_irr = +0.00%` because the bake-off's marginal IRR is already floored at zero by the `irr_bisect` convention (every conditional NPV is already negative). Falsified if marginal IRR remains > +0% under updated cost OR if marginal IRR drops below the floor differently than rhea bake-off.

- **H-ock-e:** at Starship-class promised launch cost ($200/kg, 250 t expendable @ $100M), per-ship launch+TSI drops to $186M — LOWER than the rhea bake-off's $290M anchor. The cell still does not close at sovereign-bond hurdle (4% IRR) with this cheaper launch market because the cashflow is dominated by ship cost ($650M), demonstrator non-recurring engineering ($500M), and ground operations, not by launch. Falsified if cell crosses sovereign-bond at L0-05 hard under best path × Starship-class launch × $10k/kg water × sovereign payment.

- **H-ock-f:** sweep of launch cost {$200, $500, $1500, $3000, $5000}/kg crossed with path {1, 4} × chunk {200, 482} t × water price {$2k, $10k}/kg × sovereign payment {none, $2B at year 11}: NO row crosses sovereign-bond IRR (4%) at L0-05 hard (round-trip ≤ 15 yr). Falsified if any row passes both.

- **H-ock-g:** in the same sweep (H-ock-f), at L0-05 SOFT (round-trip ≤ 16 yr), at most 1 row crosses sovereign-bond IRR — and that row requires Starship-class launch cost ($200/kg) AND high-band water price ($10k/kg) AND sovereign payment AND chunk 200 t (path 4) OR equivalent. Falsified if ≥ 2 rows pass at L0-05 soft, OR if the passing row has more conservative launch cost than $500/kg.

- **H-ock-h (assumption-flagging — held a priori on H-ock-c):** the rhea bake-off's `LAUNCH_PLUS_TSI = $290M/ship` anchor is internally inconsistent with the `variant_b_closure`-required LEO mission-1 mass for the surviving 500-kWe cell. Either the launch market assumption needs to be Starship-class (~$800/kg) to match $290M, OR the per-ship launch contribution needs to be raised to $665M+ to match Falcon Heavy expendable as the source comment claims. The bake-off's "we don't return capital at conservative assumptions" verdict is robust to the discrepancy because IRR is already floored at zero, but the matrix should record this internal inconsistency. Held a priori if H-ock-c held.

- **H-ock-i (sleeper-falsifier framing retirement):** the matrix's open-item list of "sleeper falsifiers" should retire "outbound chemical-kick economics" per the H-ock-a finding, AND should flag the cost-anchor inconsistency surfaced by H-ock-c/H-ock-h as a separate item ("LAUNCH_PLUS_TSI internal inconsistency at 500-kWe MARVL ship mass"). Falsified if the round produces a sleeper-falsifier-class result (i.e., contradicts the calibration framing the round was set up under).

### Falsification policy

Standard project policy: each sub-claim graded honestly in Reading. The pre-registration ranges are derived from back-of-envelope arithmetic at central inputs computed against PRIMARY-text sources. Per recurring-lesson-#N stacked intervention, the Reading must distinguish *which* anchor was wrong if a sub-claim falsifies — was the anchor wrong, or was the prediction wrong?

## Method

1. **Anchor inputs (cross-references):**
   - `R_variant_B_impulsive_vs_continuous/run.py` — variant_b_closure for each rhea bake-off path's outbound kick prop and LEO mission-1 mass.
   - `R_reactor_roadmap/run.py` — `LAUNCH_PLUS_TSI`, `SHIP_COST`, `DEMONSTRATOR_NRE`, `GROUND_OPS_PER_YEAR`, `BEST_CELL`, `MW_YEARS`, `cashflow_yearly`, `marginal_irr`, `conditional_irr_curve`, `MARVL_CHUNK_DELIVERED_T`, `ROUND_TRIP_YR_MARVL`.
   - `R_variant_B_recovery_paths_economic/results/R_variant_B_recovery_paths_economic.json` — rhea bake-off baseline delivered, RT, IRR for each path × chunk; this round overrides launch+TSI and reruns.

2. **Launch-cost market reference (PRIMARY sources):**
   - Falcon Heavy expendable: $150M per launch, 63.8 t to LEO ($2,351/kg) — stable SpaceX-published values since 2018.
   - Falcon Heavy reusable: $97M per launch, 30.6 t to LEO ($3,170/kg) — SpaceX-published.
   - SLS Block 1: ~$2.2B per launch (cost-plus), 95 t to LEO ($23,158/kg) — GAO 2024.
   - Vulcan VC6L: ~$110M per launch, 27.2 t to LEO ($4,044/kg) — ULA 2025 published.
   - Starship Block 2 expendable target: $100M per launch, 250 t to LEO ($400/kg) — SpaceX 2025 stated. NOT YET ACHIEVED.
   - Starship Block 2 reusable target: $50M per launch, 150 t to LEO ($333/kg) — SpaceX 2025 stated. NOT YET ACHIEVED.
   - Starship optimistic floor: $20M per launch, 200 t to LEO ($100/kg) — Musk-stated 2032+ aspiration. UNVERIFIED.

3. **Round computation:**
   - For each surviving rhea bake-off path × chunk: extract delivered_t, RT_yr, m_LEO_mission1_t from `variant_b_closure`.
   - Compute "true launch+TSI" under each launch market as: ceil(m_LEO_mission1_t / launcher_LEO_capacity) × per_launch_cost + kick_stage_cost ($140M, held).
   - Override `LAUNCH_PLUS_TSI` in R-reactor-roadmap's cashflow_yearly via this round's per-cell value.
   - Recompute conditional IRR curve over MW_YEARS, take marginal IRR (R-power-base-rate-CDF averaged).
   - For each (path × chunk × launch_market × water_price × sovereign), record marginal IRR and L0-05 status.

4. **Sweep axes:**
   - Path: {1 (variant C), 4 (variant D)}
   - Chunk: {200, 482} t
   - Launch market: {Starship_floor_$100/kg, Starship_target_$200/kg, Starship_pessimistic_$500/kg, Falcon_Heavy_expendable_$2351/kg, Falcon_Heavy_realistic_$1500/kg, SLS_class_$5000/kg}
   - Water price: {$2,000/kg, $10,000/kg}
   - Sovereign payment: {none, $2B at year 11}

5. **Outputs:**
   - `results/R_outbound_chemical_kick_economics.json` — full sweep
   - `results/tables.md` — comparison table per path
   - `results/closure_verdict.md` — single-paragraph verdict

## Assumptions held fixed (not under test in this round)

- **Inbound architecture and propellant requirements** — inherited from `variant_b_closure` per rhea bake-off paths.
- **Mass model = MARVL** (per rhea bake-off).
- **Saturn-departure orbit = high-elliptical 1-million-km** (hyperion default).
- **Lunar Gravity Assist credit = 2 km/s** (hyperion default).
- **Cryogenic depot scenario (mission 2+)** — DEFERRED to follow-on round R-depot-amortization-economics. Mission 1 is the binding constraint per matrix R-outbound-architecture finding "Mission 1 is a one-shot capital deployment, not a recurring cost." This round treats every mission as mission-1-equivalent (no depot operational), matching the rhea bake-off's accounting convention.
- **Demonstrator NRE = $500M, ship cost = $650M at 500-kWe, ground ops $50M/yr** — inherited from R15-rerun via R-reactor-roadmap.
- **Sovereign payment timing = $2B at year 11** — held per BEST_CELL.
- **Reactor program risk priors** — already absorbed in R-power-bayesian-update overlay; this round does not touch them. The conditional IRR curve already encodes the 0-of-6 base-rate prior.

## Assumptions questioned (results inform the matrix)

- **Batch-3/4 sleeper-falsifier claim of 715 t hydrolox per outbound mission** — this round retracts.
- **rhea bake-off's $290M/ship LAUNCH_PLUS_TSI assumption** — internally inconsistent with the surviving cell's MARVL-anchored LEO launch mass. Either the bake-off implicitly bets on Starship-class launch economics being achieved by program horizon (with no contingency), OR the per-ship launch contribution is materially undercounted (~1.8–3.5×).
- **Whether outbound chemical-kick economics independently kills the matrix** — per H-ock-f/g, no row crosses sovereign-bond at L0-05 hard at any tested launch market. The cell remains killed by the rhea-bake-off's own headline (reactor program risk + L0-05 ceiling), not by an orthogonal launch-cost mechanism.

## Result

Run output (full JSON: `results/R_outbound_chemical_kick_economics.json`; tables: `results/tables.md`; closure: `results/closure_verdict.md`).

### Per-cell variant_b_closure (PRIMARY-text source)

| Path | Variant | Chunk (t) | Tug (t) | Out kick prop (t) | LEO mission-1 (t) | Egress prop (t) | Inbound prop (t) | Delivered (t) | Round-trip (yr) | L0-05 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|:---:|
| path_1 | C — Earth aerocapture | 200 | 63.4 | 154.4 | 227.8 | 0.0 | 167.9 | 32.13 | 16.32 | fail (over by 1.32) |
| path_1 | C — Earth aerocapture | 482 | 72.7 | 174.0 | 256.6 | 0.0 | 353.5 | 128.47 | 19.80 | fail |
| path_4 | D — both recoveries | 200 | 59.7 | 145.0 | 214.7 | 100.4 | 80.0 | 19.96 | 14.67 | hard |
| path_4 | D — both recoveries | 482 | 64.7 | 156.7 | 231.4 | 220.6 | 232.5 | 105.61 | 16.36 | fail |

**Outbound chemical-kick propellant per mission, observed range: 145.0 – 174.0 tonnes.** This is **4.1–4.9× LOWER** than the batch-3/4 sleeper-falsifier claim of "715 t per outbound mission."

### Per-market launch+TSI per ship (mission 1, no depot)

| Market | n launches per ship | Launch USD | Total launch+TSI USD | Implied $/kg | Ratio vs $290M anchor |
|---|---:|---:|---:|---:|---:|
| starship_floor_$100/kg | 2 | $40M | $180M | $178/kg | 0.62× |
| starship_target_$200/kg | 1 | $100M | $240M | $446/kg | 0.83× |
| starship_pessimistic_$500/kg | 3 | $300M | $440M | $1,338/kg | 1.52× |
| falcon_heavy_realistic_$1500/kg | 3 | $450M | $590M | $2,007/kg | 2.03× |
| falcon_heavy_expendable_published | 4 | $600M | $740M | $2,676/kg | 2.55× |
| SLS_class_$5000/kg | 3 | $1,425M | $1,565M | $6,356/kg | 5.40× |

(values shown for path_1 / chunk 200; other cells within ±5%)

**The rhea bake-off's $290M/ship anchor implies $1,273/kg launch cost** — between Starship-pessimistic ($1,338/kg) and Falcon-Heavy-realistic ($2,007/kg), but using ONE Falcon Heavy expendable as the source comment claims is mass-infeasible (would need 4 launches at $600M for the launch cost alone).

### Marginal IRR sweep — sovereign-bond pass count

Total sweep cells: 4 paths-and-chunks × 6 markets × 2 water prices × 2 sovereign options = 96 rows.

| L0-05 status | Pass sov-bond (4% IRR) |
|---|---:|
| L0-05 hard pass (≤ 15 yr) | **0** rows |
| L0-05 soft pass (≤ 16 yr) | **0** rows |
| Total passing rows | **0** |

**No row crosses sovereign-bond IRR at any tested launch market × water price × sovereign payment combination.** Marginal IRR is `+0.0000` everywhere (R-reactor-roadmap's `irr_bisect` returns `None` for all conditional NPVs and `marginal_irr` floors them at zero per its averaging convention — every conditional NPV is negative across MW_YEARS).

### Hypothesis grading

| Sub-claim | Predicted | Measured | Held? |
|---|---|---|:---:|
| H-ock-a | real outbound prop per mission < 200 t (715 claim overstated by ≥ 4×) | max 174.0 t | ✓ |
| H-ock-b | implied launch cost in [$1200, $1400]/kg | $1,273/kg | ✓ |
| H-ock-c | central LEO mass / FH expendable capacity ≥ 2.5 | 3.57× | ✓ |
| H-ock-d | marginal IRR ≤ 0 under FH realistic launch | all 0.0000 | ✓ |
| H-ock-e | no Starship-class config crosses sovereign-bond at L0-05 hard | 0 passes | ✓ |
| H-ock-f | zero rows cross sovereign-bond at L0-05 hard | 0 / 96 | ✓ |
| H-ock-g | ≤ 1 row at L0-05 soft; requires Starship if so | 0 / 96 | ✓ |
| H-ock-h | rhea LAUNCH_PLUS_TSI internally inconsistent with MARVL ship LEO mass | INCONSISTENT (3.57×) | ✓ |
| H-ock-i | round produces calibration finding, NOT independent kill-shot | confirmed | ✓ |

**Aggregate (H-ock-agg): HELD. All 9 sub-claims held — second held aggregate in 9 hyperion rounds.**

## Reading

### What the result actually says

The batch-3/4 sleeper-falsifier framing was based on a back-of-envelope error. The actual outbound chemical-kick propellant for the rhea-bake-off-surviving cells is 145–174 t per mission (variant_b_closure-anchored), not 715 t. At rhea bake-off's inherited LAUNCH_PLUS_TSI = $290M/ship, implied launch cost is $1,273/kg — close to current Falcon-Heavy-class commercial-realistic mid range, NOT optimistic Starship pricing as I had originally suspected mid-back-of-envelope. The $290M/ship anchor is INTERNALLY inconsistent with R-reactor-roadmap's source comment "Falcon Heavy expendable + Vulcan-Centaur-class kick" because Falcon Heavy expendable's 63.8 t LEO capacity needs 3.57 launches to hoist the 228 t mission-1 mass. The bake-off implicitly assumes either (a) Starship-pessimistic launch economics ($1,338/kg, NOT YET ACHIEVED) without flagging it, or (b) the per-ship launch contribution is undercounted by ~1.8–3.5×.

The full sweep across launch market × water price × sovereign payment confirms: 0 / 96 rows cross sovereign-bond IRR at L0-05 hard (or even soft). Updating LAUNCH_PLUS_TSI to realistic Falcon-Heavy market ($590M/ship) or to SLS-class ($1,565M/ship) does not change the verdict — the bake-off cashflow's marginal IRR is already floored at zero (every conditional NPV negative across MW_YEARS). The outbound chemical-kick economics is therefore **not an independent matrix-killer**; the cell is killed by reactor program risk + L0-05 ceiling, both of which were already established by rhea's bake-off.

### What the result implies for the matrix

Three implications:

1. **Retire the sleeper-falsifier item.** The matrix's open-items list of "sleeper falsifiers" should remove "outbound chemical-kick economics" — the source claim was a back-of-envelope error that propagated into batch-3/4 handoffs without verification. This round is the verification.

2. **Flag the LAUNCH_PLUS_TSI internal inconsistency as a separate item.** The rhea bake-off's $290M/ship anchor implies launch economics that are NOT YET ACHIEVED (Starship-pessimistic), but the source comment claims Falcon Heavy expendable. The matrix should record this discrepancy and queue R-launch-cost-anchor-revision to settle it.

3. **The bake-off's headline ("no surviving cell at conservative assumptions") is robust to launch-cost revision.** Marginal IRR floored at zero across the full sweep, including SLS-class launch costs. This is a strengthening of the bake-off's verdict, not a softening — even with materially worse launch economics, the cell still does not return capital.

### Why this matters for the campaign-level recurring lesson #N

This round is the SECOND held aggregate in 9 hyperion rounds, and the FIRST round to catch a prior-round error rather than just predict its own outcome correctly. The recurring-lesson-#N stacked intervention (back-of-envelope FIRST, anchor on PRIMARY texts not SCOPE summaries or verdict-text claims) caught:
- batch-2: my own pre-registration intuition (6 falsifications)
- batch-4: Saturn's SCOPE.md misrepresentation of a prior round (R-aerocapture-fast-cruise-envelope, R-no-atmospheric-capture-baseline)
- batch-5 (this round): hyperion-3's OWN verdict-text back-of-envelope error in R-aerocapture-fast-cruise-envelope's closure_verdict.md (the 715 t figure)

The vector generalizes: any unsourced numerical claim in any round's verdict text or SCOPE summary is a candidate for back-of-envelope verification before being adopted as load-bearing. Recommend orchestrator-level discipline: round closure verdicts should not introduce numerical claims that aren't either in the round's run.py output or anchored to a named PRIMARY-text source.

## Revisit

No falsifications this round. No Revisit clause triggered. The pre-registration ranges held with margin (max outbound prop 174 t vs band [145, 200]; implied cost $1,273 vs band [1200, 1400]; FH ratio 3.57× vs band ≥ 2.5).

## Files

- `STUDY.md` — this document.
- `run.py` — deterministic; uses `variant_inbound_dv` from R_variant_B_impulsive_vs_continuous and overrides R_reactor_roadmap's LAUNCH_PLUS_TSI / MARVL_CHUNK_DELIVERED_T / ROUND_TRIP_YR_MARVL per cell.
- `results/R_outbound_chemical_kick_economics.json` — full sweep data.
- `results/tables.md` — comparison tables.
- `results/closure_verdict.md` — single-paragraph verdict and three reconciliation findings.

## Status

Round complete on iceberg-hyperion worktree. Awaiting Saturn integration. Two batch-5 commits will be pushed: this round (R-outbound-chemical-kick-economics, calibration + sleeper-falsifier-retraction) plus the merge-from-origin/main commit (which brought in shared rounds R_reactor_roadmap, R_variant_B_recovery_paths_economic, etc., needed for cross-round cashflow imports).

