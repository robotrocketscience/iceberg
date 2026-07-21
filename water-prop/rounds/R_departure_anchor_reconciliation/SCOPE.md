# R-departure-anchor-reconciliation — the desk arc's 1.5 km/s departure line vs the campaign's own audited anchors, with the Titan pump-up priced honestly

**Status:** SCOPE pre-registered 2026-07-21, before `run.py` was written or executed. Bounds from `scope_bounds.py`, committed alongside. One pre-freeze correction documented: v1 of the pre-script priced only a two-burn Oberth escape (10.5 km/s) and missed the cheaper single-burn direct escape from co-orbital (8.51) — the Oberth detour does not pay from a deep circular orbit. Caught on review; bounds frozen after the fix.
**Worker:** worktree-115637 session. Trigger: the owner's trajectory-bot question ("multiple gravity assists to pump up the delta v for the return trip") forced a check of what the departure line actually anchors on. **This round adjudicates this session's own arc: R173–R178 all carry the line under test.**

## The assumption under adjudication

R173 registered a chronological dark-side ledger — capture 1.0, ops 0.5, **departure 1.5**, inbound budget 4.2 km/s — inherited from the conops itemization that **R8 had already flagged as under-itemized in May** ("1.6 km/s for everything else"). Meanwhile the campaign's own anchors, all predating the arc:

- `R_dv_anchor_audit` (methodology lesson 20 origin): Saturn departure from B-ring parking = **7.7 km/s** impulsive Oberth, derived from vis-viva after catching a prior informal 5.5 anchor.
- `mission_graph` phase 4 (state of record, paid by the reactor baseline the arc used as its denominator): `CHEMICAL_TEI_DV_KM_S = 7.7`, `CHUNK_FED_DV_KM_S = 9.0` at 800 s.
- `R_HE_graze_feasibility`: grazing capture dead at 5–10 km/s relative velocity — **co-orbital B-ring capture is binding**, so the chunk-laden ship departs from deep in the well.
- `R_bring_fine_structure_rendezvous` / axis 19: residence-class ~7.4 km/s each way, owner-retired at 14.7 round trip.

The arc measured a variant priced on the conops ledger against a baseline priced on the honest ledger. If no surviving architecture legitimizes 1.5 km/s, every non-fission round-trip ratio from this week (1.74× → 4.8× → 3.57× → 3.28×) is falsified as a headline, and the arc survives only as components.

## Pre-registered hypotheses (bounds scripted)

**H1 [S] (anchors regressed).** Vis-viva reproduces the audit's Oberth burn at **7.5–7.8 km/s** (scripted 7.63); the true minimum impulsive escape from co-orbital B-ring is **8.3–8.7 km/s** (scripted 8.51 single-burn; bi-elliptic-via-Titan 8.62 — within 0.2, no free lunch); the residence-class text value (7.4) is **not** reproduced (reconstructed 10.6) — recorded as an anchor discrepancy on a retired architecture, both readings ≥ 5× the desk line. Falsified if any swept moonless impulsive sequence beats 8.0 km/s.

**H2 [W] (what Titan can and cannot do).** The Cassini-reverse pump-up tour makes the 6.21 km/s hyperbolic excess ~free (+300 m/s trims, +1–2 yr), but the apo-raise out of the well is propulsive and flyby-irreducible: Titan-assisted departure floor **6.8–7.3 km/s** (scripted 7.00), an **15–20 %** saving — the well, not the v∞, is the cost. Symmetrically, capture-side circularization at the ring is **6.5–6.9 km/s** (scripted 6.70; the co-orbital circular state at 1.8 R_S is Tisserand-unreachable from outer-moon flybys). Honest in-system round trip with maximal Titan assist: **13.3–14.1 km/s** (scripted 13.71) — corroborating retired axis-19's 14.7 within 10 %. Falsified if any swept flyby-augmented sequence departs for < 6.0 km/s propulsive.

**H3 [W] (the arc adjudicated).** At honest anchors the non-fission variant has no priced departure: staged-gas (2-stage, ε 0.08, 480 s) inflates the R178 best corner from 3.28× to **≥ 35×** (scripted 39.2 Titan-assisted / 59.1 direct — hundreds of tonnes of gas *at Saturn*, thousands launched); chunk-fed MET at the variant's 2.2 kWe takes **> 100 years** (scripted 106–159). **The R173–R178 non-fission round-trip headline is falsified.** The arc's mechanisms survive on legs that remain real — keep-alive pricing, banks, regeneration, the allocation law, RTG marginals, demonstrator gates A/B — as components of a reactor mission's resilience, which is where R174's H4 tried to land before this session re-inflated it. Falsified (i.e., the arc's headline survives) only if some non-fission departure option prices under 10×.

**H4 [S] (bet #3 re-derived from departure physics).** A 2-year chunk-fed departure burn on a 100 t final mass needs **100–190 kWe** (scripted 175 direct, 117 Titan-assisted) — independently reproducing the audit's reactor power class from the departure leg alone. The Titan pump-up survives as a **reactor-mission lever**: −33 % reactor power, or −33 % departure propellant (144 vs 215 t) at fixed power. Falsified outside bands.

## Sweep (run.py)

Impulsive sequence search: {single-burn, two-burn Oberth (periapsis depth 60–80×10³ km), bi-elliptic via r ∈ {Titan, 2×Titan, 3×10⁹ m}, Titan-raise+tour} × v∞ {5.4, 6.21, 7.0 km/s}; repricing table at canonical + best corners × departure options {desk 1.5 (reference), Titan-gas 7.0, direct-gas 8.51, chunk-fed at P ∈ {2.2, 50, 110, 175, 300} kWe with burn-time vs a 2-yr window}; power-requirement curve.

## Deliverables

`scope_bounds.py`, `run.py` (+ `results/departure_anchor.png`), `results/findings.json`, `STUDY.md` with Revisit; matrix notes for the orchestrator: the arc correction (per R174-precedent, corrections live forward — no retro-editing of prior STUDYs), the Titan-tour adoption into the reactor architecture, the anchor-discrepancy flag on the retired residence number, and the public-repo write-up caveat (rounds 173–178 pages need a correction pointer).
