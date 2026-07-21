# R-rtg-keepalive — pricing the dark keep-alive load, and the RTG suite that retires it

**Status:** SCOPE pre-registered 2026-07-21, before `run.py` was written or executed. All bounds derive from `scope_bounds.py`, committed alongside and reviewed to run.py standard (R176 convention).
**Worker:** worktree-115637 session. Owner-directed: "run the rtg keepalive round, question your assumptions, test your hypotheses."
**Predecessors:** R171 (fuel-cell bank, hotel duty grid), R172 (cold-tier ZBO spec: 1.5 W/t-LH2 leak, 80 We input + 50 kg per W lifted → **13.3 We and 8.3 kg per tonne of banked gas**), R174 (round-trip chain), R176 (2-stage kick, best corner 3.57×).

## Assumptions this round questions — including two of this session's own

1. **R174's chain charged zero gas for cruise keep-alive.** Its only power line was the 2.6 t active-ops hotel entry; bus baseload and ZBO cryocooler input across ~11 dark cruise years were never priced. The pre-script shows this was not free.
2. **The conversational claim that RTG keep-alive is "genuinely promising"** (this session, 2026-07-21) assumed the dark legs are powerless. R172's own arrays are not dead at Saturn: 100 kW-rated → 733 We, 300 kW → 2.2 kWe (1/r², LILT ×1.5). At big-array corners the liability may be self-covered and the RTG useless where the economics are best.
3. **The conversational claim that RTG trickle electrolysis is "≤ 2 t, negligible"** — the pre-script says 4.2 t at the N* suite. Registered here so the correction is on the record either way.
4. **Made explicit:** the bank is launched pre-charged (ground electrolysis). R174 never checked en-route charge feasibility; its canonical bank (79.8 t, 1.61 TJ chemical) exceeds the outbound ≤3 AU harvest window (~0.8 TJ at 100 kW), so launched-charged is the only self-consistent reading. Recorded as a chain clarification, not a change.

## Model (all parameters from predecessors; no new tunables)

R174 chain + phased keep-alive: load(t) = P_ka + 13.33 We/t × bank(t), array avail = rating/r²(t)/1.5 beyond 3 AU (f_ops availability factor at the ring station), MMRTG = 110 We BOL, 45 kg, 4.8 kg PuO2, 1.9 %/yr exponential decay (NASA MMRTG fact-sheet values; flown MSL 2011, Mars 2020). Shortfall burned from the bank at η_fc 0.55 (product water vented — conservative); RTG spare watts beyond 4 AU inbound + Saturn ops trickle-electrolyze chunk water at η 0.66, credited against the residual demand and **debited from delivered mass** (the 3–4 AU inbound overlap with the lit-thrust integral is excluded to avoid double-counting array energy). Keep-alive product-water recovery and RTG waste heat (~2 kWt/unit offsetting heater share of P_ka) are unmodeled benefits — both favor the concept; stated, not claimed. Economics: 2-stage kick (ε 0.08, 480 s, R176), ratio vs the 50 t/40 t reactor baseline. Regression anchor: keep-alive off reproduces R174's canonical 79.8 t bank (pre-script: exact).

**Sweep:** chunk {40, 80} t × array {100, 200, 300} kW × relief {nominal, moon-tour} × bank Isp {450, 480} s × P_ka {150, 300, 600} We × T_ops {1.0, 2.0} yr × f_ops {1.0, 0.5} × suite N {0, 2, 4, 5, 6, 8} MMRTG.

## Pre-registered hypotheses (bounds scripted; sweep may beat them only by finding structure the script lacks)

**H1 [W] (the unpriced liability).** At the canonical corner (40 t, 100 kW, nominal, 450 s, P_ka 300 We, T_ops 1.5 yr, f_ops 1.0, N=0), pricing keep-alive grows the bank to **85–98 t** (scripted 91.3), keep-alive gas **3–5.5×** the legacy 2.6 t hotel line (scripted 4.2×), launch mass **+60 to +100 t** (scripted +81). Falsified outside any band.

**H2 [W] (array self-coverage at the optimum).** At every 300 kW corner with f_ops = 1.0, keep-alive shortfall gas ≤ **1.5 t** (scripted: 0.0 at the R176 best corner) and the R176 3.57× headline shifts ≤ **2 %**. The RTG buys nothing where the economics already won. Falsified by any such corner above 1.5 t.

**H3 [S] (the RTG niche, sized).** At the canonical corner, the minimum suite covering ≥ 90 % of shortfall energy is **N\* = 4–6 MMRTG** (scripted 5; 24 kg PuO2 ≤ Cassini's 32.7 kg), net launch saving **55–90 t** (scripted 71, net of hauled RTG mass), and launch-vs-N has an **interior optimum** (units beyond full coverage cost mass; scripted minimum at N≈6–7). Falsified if N\*·4.8 kg > 32.7 kg, saving falls outside the band, or launch decreases monotonically through N=8.

**H4 [S] (both conversational claims, adjudicated).** Trickle regeneration at the N\* suite is **3–6 t** of gas (scripted 4.2) — falsifying this session's "≤ 2 t, negligible" claim in advance — while RTG-only bulk charging of the canonical bank requires **≥ 40 MMRTGs** (scripted 48, ~230 kg PuO2), confirming the bulk-scale death. Falsified if trickle < 3 t or > 6 t at N\*, or the reductio lands under 40 units.

## Deliverables

`scope_bounds.py`, `run.py` (sweep + `results/rtg_keepalive.png`), `results/findings.json`, `STUDY.md` with Revisit; matrix notes for the orchestrator (R174–R176 ratios inherit the H1 correction at small-array corners; Saturn-side-power axis gains the RTG-keepalive option with its PuO2 price).
