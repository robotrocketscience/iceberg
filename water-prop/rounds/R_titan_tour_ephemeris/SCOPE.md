# R-titan-tour-ephemeris — the pump-up tour R179 adopted, checked against the bound-chain constraint it never faced

**Status:** SCOPE pre-registered 2026-07-21, before `run.py` was written or executed. Bounds from `scope_bounds.py`, committed alongside. Two pre-freeze fixes documented: (a) an H3 row initially carried hand-typed dv constants (8.25 / 10.0) that the script derives elsewhere — replaced with derived values per the R184 red-flag rule; (b) the Iapetus print echoed a mangled expression — fixed to print the computed exit v∞.
**Worker:** worktree-115637 session. This is the ephemeris check **R179's own Revisit demanded before baselining** the Titan pump-up departure lever. Constants and conventions from the phoebe round (`R_saturn_moon_ga_ephemeris`, Horizons-verified: Titan GM 8978.14 km³/s², a 1,221,870 km, e 0.0288, P 15.945 d; flyby altitude 1000 km nominal / 1500 sensitivity; tour spacing 2×T_Titan per flyby).

## The claim under adjudication

R179 H2/H4 (HELD as registered, adopted into the reactor architecture): *"the Cassini-reverse pump-up tour buys the entire 6.21 km/s hyperbolic excess for ~300 m/s of trims plus 1–2 years — Titan-assisted departure floor 7.0 km/s (−17%), −33% reactor power (117 vs 175 kWe)."* R179's `scope_bounds.py` literally annotates the raise with "v_inf pumped free" — the pump was **assumed, never computed**.

The constraint it never faced: **a flyby conserves v∞ relative to Titan (Tisserand), and every orbit between flybys must remain bound to re-encounter Titan.** So a pure flyby chain's departure excess is capped by a single final kick from a barely-bound orbit — `v∞,S(exit) = √(v_sc(α_esc−δ)² − v_esc²)`, maximized over the contour v∞,T. Pump-down tours (capture side) are immune to this constraint because their "free" direction descends *into* the bound region; the departure mirror does not exist. R179 priced the two sides as symmetric. They are not.

## Model

Patched conics throughout. Exit-ceiling curve over v∞,T ∈ [2.35, 9.0] km/s × Titan radius {perikrone, mean, apokrone} × flyby altitude {1000, 1500 km}. Repair-strategy families, all required to reach the state-of-record v∞ = 6.21 km/s from co-orbital B-ring (r = 1.07×10⁸ m), tour strategies charged R179's 300 m/s trim allowance, single-flyby strategies 50 m/s targeting:
S0 direct (R179 anchors: single 8.51, far-bi-elliptic 8.45) · S2 raise(r_a) + free pump + exit kick + post-escape linear residual · S3 raise + pump + **powered final flyby** (burn at Titan periapsis, exit alignment limited by the powered hyperbola's turn) · S4 **peri burn to hyperbolic + one outbound kick** (radial crossing geometry) · S5 raise + pump to the contour's barely-bound member + residual burn at that member's own periapsis (the Tisserand-continuum check: this must and does converge to the single-burn cost as r_a → ∞). Sweep grids: r_a/r_T ∈ [1.001, 20] (log), v∞,S0 ∈ [0, 6.21]. Schedule: pump-rotation flyby count at phoebe's 2×T convention; declination crank vs epoch (obliquity 26.73°, equinox 2025.37, Saturn year 29.457 yr); Iapetus post-Titan trim.

## Pre-registered hypotheses (bounds scripted)

**H1 [S] (the ceiling).** The pure-flyby exit ceiling is **3.0–3.4 km/s** across every swept corner (scripted 3.28 central, 3.05 worst, 3.33 best) — **≤ 55 % of the required 6.21**. R179's "v∞ pumped free" mechanism is impossible from any raise orbit, at any flyby count. Falsified (R179 vindicated) if any corner reaches 6.21.

**H2 [S] (the honest floor).** Minimum over all repair strategies: **8.30–8.45 km/s** (scripted 8.38, achieved by S4 — a 5.37 km/s-excess peri burn plus a single outbound kick; the tour is not even the best repair). Saving vs direct 8.45: **0.05–0.15 km/s (≤ 2 %)**, not 1.45 km/s (17 %). **R179's Titan-assisted floor band 6.8–7.3 is falsified; the adopted lever is revoked.** Falsified (this round) if any swept strategy beats 8.0 km/s.

**H3 [S] (the −33 % power lever dies).** 2-yr chunk-fed burn on 100 t final mass at honest anchors: impulsive-gas-hybrid best **150–160 kWe** (scripted 155, −11 %); pure low-thrust Titan-assisted **210–235 kWe** (scripted 224, +28 % — for a pure low-thrust ship the Titan detour *hurts*, because the exit kick's 2.9 km/s shortfall is bought back without Oberth leverage). The 117 kWe branch of bet #3 is revoked; the requirement band collapses from 117–175 to **≈ 155–175 kWe**. Falsified if any priced variant beats 130 kWe.

**H4 [W] (what survives).** Capture-side ring circularization **6.70 km/s stands** (it is the Hohmann-tangential bound, flyby-irreducible — R179's number was right for the reason R179 gave). Honest max-assist in-system round trip **14.95–15.25** (scripted 15.09) — *above* R179's registered 13.3–14.1 band and within 3 % of retired axis-19's 14.7 (the desk-retired figure looks better every honesty pass). Exit-sequence schedule: 4–8 flybys, 0.3–0.7 yr (2×T convention) + 0–2 declination-crank flybys epoch-dependent (≈ free at the 2032.7 solstice, worst ≈ 1.3 flybys at the 2040.1 equinox); Iapetus adds ≈ +0.2 km/s of exit excess (a trim, not a bridge). Falsified if the round trip leaves band or the crank exceeds 3 flybys anywhere in 2030–2045.

## Sweep (run.py)

Exit-ceiling curve (400-pt v∞,T grid × 3 Titan radii × 2 altitudes); strategy-total curves vs r_a/r_T and vs v∞,S0 (400-pt, same grids as pre-script); declination curve 2026–2050; findings.json; two-panel figure (ceiling curve vs requirement; honest strategy ladder vs R179's claim).

## Deliverables

`scope_bounds.py`, `run.py` (+ `results/titan_tour_ephemeris.png`), `results/findings.json`, `STUDY.md` with Revisit; orchestrator notes: R179 lever revocation (matrix + design-axes + bet #3 clause), the departure/capture asymmetry statement, cross-refs to `R_saturn_moon_ga_ephemeris` (capture side untouched) and `R_jupiter_ga_saturn_exit_flexibility` (the surviving exit-geometry lever, already priced not-material for chunk delivery).
