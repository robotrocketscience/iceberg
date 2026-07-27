# R-ephemeris-departure-anchor — real JPL-ephemeris Saturn→Earth departure v∞ (first ephemeris round)

**Status:** SCOPE pre-registered 2026-07-22 (latest+25 arc), before `run.py` was written or executed. The input ephemeris (JPL Horizons state vectors) was fetched first as external ground-truth data; no transfer/porkchop was computed before this pre-registration.
**Worker:** worktree-115637 session. Project-owner-directed: cross-apply `~/projects/trajectory-bot`'s real-ephemeris trajectory toolkit to ICEBERG.
**Predecessors:** `R-hohmann-vinf-reconciliation` (`62fff0f`) — hand-derived min-energy Hohmann v∞ = 5.44 km/s; campaign 6.21 = faster-transfer. `R_departure_anchor_reconciliation` (R179) / `R_titan_tour_ephemeris` (R186, `623d779`) — departure floor 8.4-8.5 km/s; Titan pump-up lever revoked via a Tisserand/bound-chain cap ~3.3 km/s. `design-axes/04` — Methodology lesson 20: "vis-viva-default anchoring when no primary-text source."
**Toolkit source:** `~/projects/trajectory-bot` — `ephemeris.py`/`horizons_backend.py` (Horizons pipeline), `scripts/lambert.py` (universal-variable Lambert), `scripts/tisserand_3d.py` (Titan@Saturn constants v_P=5.57, μ=8978.14, R=2574.7).

## Why this round is a new fidelity tier

Every prior ICEBERG Saturn-departure anchor is **hand-derived vis-viva** (5.44 / 6.21 / 7.7 / 8.4-8.5 km/s), carrying the flagged methodology weakness that no primary-source or ephemeris check backs the numbers. This is the **first ICEBERG round to use real JPL Horizons ephemeris** — Saturn (699) + Earth (399) heliocentric ecliptic state vectors, 2035-2056, fetched via trajectory-bot's astroquery pipeline — with a vendored pure-numpy universal-variable Lambert solver (Curtis Alg 5.2, no JAX). It re-anchors the departure v∞ on a real launch-window porkchop and independently reproduces R186's Titan cap from trajectory-bot's Titan@Saturn constants.

## Question

(1) Does a real-ephemeris Saturn→Earth Lambert porkchop confirm the hand-derived 5.44 km/s min-energy departure v∞ (retiring the vis-viva-default weakness), and is 6.21 a realizable faster-transfer value? (2) Does trajectory-bot's Titan@Saturn constant set reproduce R186's ~3.3 km/s Titan pump cap — and is that revocation as unconditional as R186's magnitude-bound implied? (3) Does the real anchor move the 155-175 kWe reactor floor?

## Boundary

- **IN:** real Horizons Saturn+Earth heliocentric states; Lambert porkchop over departure epoch × time-of-flight; minimum and 6.21-locus departure v∞; Titan single-flyby turn (δmax) and Saturn-centric pump cap from real Titan constants, with its v∞_T sensitivity; Oberth-quadrature propagation to the reactor floor (R179 model, reproduced).
- **OUT:** the Saturn-centric Oberth escape burn detail (R179 owns it); a full Saturn-system multi-moon tour optimizer (trajectory-bot's tour SEARCH is heliocentric-only — re-hosting it in a Saturn frame is net-new work, a named follow-on); low-thrust spiral (separate named follow-on, needs an Isp model trajectory-bot lacks); aerocapture (trajectory-bot has none).

## Pre-registered hypotheses (numeric, falsifiable, written before the porkchop)

**H1 [S] — The real-ephemeris minimum Saturn→Earth departure v∞ brackets the hand-derived 5.44 km/s.** Circular-coplanar Hohmann at Saturn's real distance range (9.07-10.02 AU, from the fetched ephemeris) gives 5.40-5.48 km/s. **SCOPE:** real-ephemeris porkchop minimum v∞ ∈ [5.0, 6.0] km/s (2.5° inclination + phasing raise it slightly above coplanar). **Falsified** if the ephemeris minimum < 4.8 or > 6.3 (hand anchor materially wrong).

**H2 [S] — The campaign's 6.21 km/s is a realizable faster-than-minimum departure v∞, not below the achievable minimum.** **SCOPE:** 6.21 ≥ the porkchop minimum and lies within its range. **Falsified** if 6.21 < the ephemeris minimum (would make 6.21 unphysically low).

**H3 [S] — Titan pump cap is v∞_T-dependent: it reproduces R186's ~3.3 km/s at the natural capture-orbit v∞_T≈3, but the revocation is *conditional* on v∞_T.** With trajectory-bot's Titan constants, the max Saturn-centric departure excess = √((v_Titan+v∞_T)² − 2μ_S/r_Titan). **SCOPE:** (a) reproduce R186 — 3.38 km/s at v∞_T=3; (b) the v∞_T threshold to reach the 5.44 km/s requirement ∈ [3.8, 4.2] km/s. **Finding (honest):** R186's revocation holds at nominal capture-orbit v∞_T (~3) but is conditional on v∞_T ≲ 3.5 — a patient high-v∞_T Titan tour (slow near-apoapsis crossing) is a candidate re-open that R186's magnitude bound did not quantify. This does **not** change the reactor floor (the departure burn supplies v∞ if Titan does not) but re-opens a design question. **Falsified** if the cap at v∞_T=3 is not ~3.3 km/s (would break the R186 reproduction).

**H4 [W] — The real anchor barely moves the reactor floor.** Oberth quadrature (R179 model) at the deep B-ring well suppresses the v∞ spread. **SCOPE:** floor at the real-ephemeris minimum v∞ stays in [150, 180] kWe (hand 5.44 → 154 kWe; 6.21 → 159 kWe). **Falsified** if outside 150-180 kWe.

**Honest expected reading:** H1/H2/H4 hold (the hand anchor is validated by real ephemeris; the reactor floor is Oberth-robust) — the main deliverable is **retiring the vis-viva-default methodology weakness** with a real-ephemeris backing. H3 is the interesting one: it corroborates R186's number at nominal parameters but surfaces that the Titan revocation is conditional on the arrival-orbit v∞_T — a genuine open question the bound-only R186 did not address, and a candidate follow-on (a Saturn-frame Titan-tour optimizer, which trajectory-bot's heliocentric tour search would need re-hosting to run).

## Method

Deterministic. Input ephemeris in `inputs/ephem_saturn_earth.json` (Horizons, heliocentric ecliptic, km/km·s⁻¹). `run.py`:

- **Lambert porkchop:** vendored pure-numpy universal-variable Lambert (Curtis Alg 5.2; validated against Curtis Ex 5.2 in-script). For departure epoch t_dep (Saturn state) × time-of-flight ToF ∈ [4, 9] yr (Earth state at t_dep+ToF), solve Lambert(r_Sat, r_Earth, ToF, μ_Sun); departure v∞ = |v_transfer(t_dep) − v_Saturn(t_dep)|. Skip near-Δθ=π ill-posed geometries (the known Lambert singularity — bracket the minimum with the well-posed grid).
- **Compare:** porkchop minimum & the 6.21-locus vs hand 5.44 / 6.21.
- **Titan cap:** δmax = 2·arcsin(1/(1+r_p·v∞_T²/μ_Titan)); Saturn-centric excess = √((v_Titan+v∞_T)² − 2μ_S/r_Titan) over v∞_T ∈ [2,4], peri alt {500,1000,2000} km; find the v∞_T reaching 5.44.
- **Reactor floor:** dv = √(v∞²+2μ_S/R_ring) − v_circ; P = ½·v_e²·m_f(exp(dv/v_e)−1)/η/(2 yr) (R179 model, reproduced) at the real minimum v∞ and 6.21.

**Anchors:** μ_Sun=1.32712440018e11 km³/s², AU=1.495978707e8 km, μ_Saturn=3.793e7 km³/s² (R179); Titan v_P=5.57, μ=8978.14, R=2574.7 (trajectory-bot tisserand_3d); reactor model VE=800×9.80665, R_ring=1.07e8 m, η=0.6 (R179). Ephemeris provenance recorded in the input JSON.
