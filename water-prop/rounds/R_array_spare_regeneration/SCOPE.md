# R-array-spare-regeneration — every spare watt priced: electrolysis vs dark-leg EP, and who gets the joule

**Status:** SCOPE pre-registered 2026-07-21, before `run.py` was written or executed. All bounds derive from `scope_bounds.py`, committed alongside, reviewed to run.py standard. The pre-script went through two documented corrections during that review before bounds were frozen: (1) dark-leg EP propellant was double-counted (added to the departure stack *and* debited from delivered — it is chunk water already aboard; debit only), and (2) the first allocation implementation let EP consume demand before electrolysis, contradicting the rule it was meant to encode. Both fixed pre-registration; both recorded here because they changed the scripted bounds materially.
**Worker:** worktree-115637 session. Owner-directed: "run the array-spare regeneration round," plus the mid-round message: *"whats wrong with running the electric propulsion on the 2.2kw from the solar panels for the return trip? … 2.2kw is nothing to scoff at."*
**Predecessors:** R173 (the lit leg — the owner's EP-on-solar concept has been load-bearing inside 4 AU since that round; the 4 AU cutoff was registered, never derived), R177 (trickle mechanism, RTG watts only; keep-alive chain), Variant B lineage (`R_chunk_fed_chemical`, `R_architecture_E_no_saturn_side_electrolysis`: *dedicated* Saturn-side process power died on credibility cascade — this round's mechanism reuses the electrolyzer, cryostorage, and array the solar-bank variant carries anyway, at spare-watt scale, so that cascade does not re-apply at its old magnitude; ops-credibility of chunk-water feed handling still flagged).

## Mechanisms priced (all spare watts = array above keep-alive loads; RTG optional axis)

- **(a) Ops regeneration:** electrolyze chunk water at the ring station; credit against departure gas (pre-departure sink; cap = departure gas).
- **(b) Inbound regeneration** beyond 4 AU: credit against residual + inbound keep-alive demand only (you cannot regenerate departure gas after departing); 3–4 AU stays with the lit-thrust integral (no double count).
- **(c) Dark-leg EP (the owner's proposal):** spare watts beyond 4 AU drive the MET directly, gated to thrust only while return dv is still owed; propellant is chunk water already aboard (delivered debit, no added stack mass).

**Mass ledger:** regenerated gas and EP propellant are chunk water — debited from delivered mass; departure stack mass unchanged (chunk mass moves into already-launched empty tanks). Outbound: no feedstock, no credit (keep-alive product water vented per R177). **Modes:** `off` / `rtg` (R177 regression) / `regen` (a+b) / `ep` (c only, the proposal isolated) / `mix` (a + φ-split of residual dv between EP and regeneration, φ scanned).

**The allocation physics this round adjudicates.** Per spare joule, electrolysis→480 s burn delivers 2.34e-4 N·s vs the MET's 1.53e-4 (burned gas brings its own chemical energy) — but per metre-per-second retired, EP debits only 480/800 = 0.6× the chunk mass. Launch-mass recovery favors electrolysis; the campaign's ratio metric (launch per delivered) can favor EP. This session produced the claim "electrolysis dominates 1.53:1" **hours before this SCOPE**; the pre-script already indicates the ratio metric falsifies it at the canonical corner. Registered so the adjudication is on the record.

## Pre-registered hypotheses (bounds scripted)

**H1 [S] (regression and continuity).** `off` reproduces R177's canonical exactly (91.3 t / 767 t); `rtg` reproduces R177's N=4 within 1.5 % (scripted 70.7/622 vs 70.2/619 — the ops-credit cap refinement, documented). RTG marginal value at the canonical corner *after* array regeneration is live: **17–22 t per MMRTG** (scripted 19.6) — R177's ~19 t/unit survives. Falsified outside bands.

**H2 [S] (the best corner moves).** Ops regeneration at the R176 best corner, T_ops 1.5 yr: launch **547 → 495–509 t** (scripted 503, −44), ratio **5.15–5.35** (5.24) on this round's full-kick basis — hybrid-translated headline ≈ **3.2–3.4×** (secondary, stated not sworn). The ops-extension trade is ~linear: **26–36 t launch per added ops year** through T_ops 3.0 (scripted 30–33), schedule 13.4 yr ≤ L0-05's 15. Falsified outside bands.

**H3 [W] (power-poor corners transformed).** Array-spare regeneration recovers **190–230 t** of launch at the canonical corner (scripted 211; 767 → 555 with zero plutonium) and **130–165 t** at the 200 kW/80 t middle corner (scripted 147). R177's anti-correlation reading ("value concentrates in ops-serving-departure") survives only at 300 kW; at 100–200 kW the inbound spare is the dominant recovery. Falsified outside bands.

**H4 [S] (the owner's EP proposal, adjudicated three ways).** (a) At the best corner, gated EP-only changes launch by **0 ± 2 t** (no residual demand — nothing to buy). (b) At the canonical corner, EP-only *beats* full-electrolysis on the ratio metric (scripted **13.55 vs 13.78**, gap 0.1–0.4) while losing on launch (629 vs 555) — falsifying this session's "electrolysis dominates" claim on the metric that matters. (c) The composite `mix` mode is best-or-tied on ratio at all three probe corners (scripted: MID 5.72 vs {5.82 ep, 5.97 regen}; ties at CANON/BEST within 0.02). Falsified if any leg fails.

## Sweep

chunk {40, 80} t × array {100, 200, 300} kW × relief {nominal, moon-tour} × Isp {450, 480} × P_ka {150, 300, 600} We × T_ops {1.0, 1.5, 2.0, 3.0} yr × f_ops {1.0, 0.5} × N {0, 4} × modes {off, regen, ep, mix φ∈{0.25, 0.5, 0.75}} — best-ratio mix per corner.

## Deliverables

`scope_bounds.py`, `run.py` (+ `results/spare_watt_allocation.png`), `results/findings.json`, `STUDY.md` with Revisit; matrix notes: best-corner economics improve (H2), the RTG option's post-regen marginal value (H1), the two-regime allocation law (H4). Named exclusions: burst-duty-cycle optimization (owner interest, own round — R172 H4 is the current anchor); trickle-timing fidelity; tank-capacity headroom within the inbound phase (flagged, unmodeled).
