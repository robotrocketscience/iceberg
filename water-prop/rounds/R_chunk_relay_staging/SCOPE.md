# R-chunk-relay-staging — the dive shuttle vs the monolithic ship, at honest anchors

**Status:** SCOPE pre-registered 2026-07-21, before `run.py`. Bounds from `scope_bounds.py`, committed alongside.
**Worker:** worktree-115637 session. R179's named "surviving maybe": a shuttle transits the ±6.7 km/s well while the mothership waits on the staging ellipse (peri at ring, apo at Titan-crossing) and departs by the pump-up tour.
**Scope boundary:** Saturn-side only. Both architectures share Earth-arrival handling; the tour delivers the exact Hohmann v∞, so the relay's heliocentric legs are assumed at parity with the monolithic's spread-spiral (stated, not tested here).

## Anchors (all inherited, none new)

Well transit 6.70 km/s each way, flyby-irreducible (R179). MET 800 s, η 0.6. Reactor specific mass κ ∈ {**417 kg/kWe flown** (KRUSTY 2.4 W/kg system), **100 kg/kWe paper** (10 W/kg — the National-Academies-bounded ceiling per `R_arch_E_specific_power_flown_anchored`)}. Monolithic state-of-record: 30 kWe chunk-fed spiral spread over the 8-yr return transit (`mission_graph` phase 4), bus+bag 4 t, kick multiplier 5.84, chunk 40 t; calibration: paper-κ monolithic launch-per-delivered 1.02 vs the audit's 1.25 (consistent within 25 % — the audit's optimism is the known specific-power cliff). Schedule: residence budget **2.9 yr strict** (L0-05 15 yr − 12.1 transit) / **12.9 yr waiver** (25 yr), capture tour 1 yr. Relay masses: mothership bus 4 t (no reactor, no bag), shuttle bus+bag 2.5 t + κ·P_s. Sortie clock: the shuttle cannot spread its climb over the return transit — sorties burn residence.

## Pre-registered hypotheses (bounds scripted)

**H1 [S] (single-chunk relay strictly loses).** At N = 1 the relay is worse than the monolithic at **every** (κ, P_s) corner, by ≥ 10 % on launch-per-delivered (scripted worst edge −15 %, typical −80 to −400 %): extra mothership hardware, same well transit, and the sortie clocked against residence instead of the transit. Falsified if any N=1 cell beats the monolithic.

**H2 [S] (the multi-chunk win, and the slow-and-light optimum).** Under the 25-yr waiver, the relay beats N monolithic missions: best legal cells **launch-per-delivered 0.42–0.50 at paper κ** (scripted 0.46: 30 kWe, N=3, +55 %) and **1.30–1.50 at flown κ** (scripted 1.39: 30 kWe, N=2, +42 %). In both tiers the optimum sits at the **lowest swept power**: under a residence budget, reactor mass beats sortie speed — the winning shuttle is slow and light. Falsified if the per-tier optimum is not at minimum feasible power or falls outside bands.

**H3 [W] (the strict schedule kills it).** Under strict L0-05 no multi-chunk relay cell exists that beats the monolithic: the N=2 strict frontier sits at a bisected P_s ≥ ~200 kWe (paper κ) whose reactor mass drives launch-per-delivered above the monolithic's 1.02. **The relay's advantage exists only under the 25-yr waiver** — the same waiver architecture E needed. Falsified if a bisected strict-legal cell beats the monolithic.

**H4 [W] (harvest and exposure ledger).** At the winning waiver cells the relay *reduces* harvest per delivered chunk (scripted **2.9× vs the monolithic's 3.5×** chunk mass at paper κ — a 15–20 % relief on bet #1's capture-count exposure), while at flown-κ high-power corners it worsens (up to ~7×). The mothership crosses the ring plane **zero** times vs the monolithic's two per mission (per-pass impact context from `R_bring_survivability_relaxed`, cited not repriced). Falsified if winning-cell harvest ratio ≥ monolithic's.

## Sweep

κ {100, 417} × P_s {20–250, step 10} × N {1–5}; strict/waiver feasibility; bisection of the strict-N=2 power frontier; per-tier legal optima.

## Deliverables

`scope_bounds.py`, `run.py` (+ `results/relay_staging.png`), `results/findings.json`, `STUDY.md` with Revisit; matrix note: relay = a **fleet-era architecture** (waiver-gated, reactor-launched-once; shuttle-reuse across missions named as the follow-on with `R15_fleet_ramp` lineage), not a rescue for single-mission economics and not a reactor bypass — bet #3 rides on the shuttle.
