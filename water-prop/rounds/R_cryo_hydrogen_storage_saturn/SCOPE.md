# R-cryo-hydrogen-storage-saturn — does the 77 t LH₂ departure propellant survive a multi-year Saturn dwell?

**Status:** SCOPE pre-registered 2026-07-22, before `run.py`. `scope_bounds.py` computes the tank geometry and per-source heat-leak brackets.
**Worker:** worktree-115637 session. Project-owner-directed ("test your hypotheses, question your assumptions, use the scientific method in all its rigor"). Tests the single most load-bearing unmodeled cost of `R-electrolysis-departure-stage` (`49f4bb1`).
**Predecessor under test:** `R-electrolysis-departure-stage` — the reactor-charged H₂/O₂ departure stage softens the departure from megawatt to few-hundred-kWe, but rests on storing **77 t of liquid H₂ at 20 K over the 1–3 yr Saturn dwell**. That round treated the boiloff as a "first-order risk," not modeled. This round models it.

## The assumption under test

That 77 t of LH₂ can be stored for the dwell with acceptable boiloff and acceptable added power/mass. Three heat sources compete, two of which are potential **showstoppers** that would collapse the Round F mitigation back to the megawatt electric departure:

1. **MLI radiation** from the ~90 K Saturn environment (hypothesis: small — T⁴ scaling makes Saturn ~50–60× more benign than near-Earth storage).
2. **Ortho-para conversion self-heating** — freshly electrolyzed H₂ is ~75 % ortho; converting to para releases ~527 kJ/kg, *exceeding* the 446 kJ/kg latent heat, so an uncatalyzed inventory self-boils-off completely (showstopper unless catalyzed at liquefaction).
3. **Reactor proximity** — the 150–440 kWe reactor's ~700 K radiators would boil the tank off through radiation unless shadow-shielded and boom-separated (showstopper unless separated).

## Boundary

- **IN:** LH₂ tank geometry (77 t, para density, sphere); per-source heat leak — MLI radiation at warm-boundary {50, 90, 150} K × effective emittance {5e-4, 1e-3, 2e-3}; ortho-para self-heating (uncatalyzed full conversion vs catalyzed ~0); reactor radiation vs view-factor (unshielded 0.1 → shadow-shielded 1e-3) at radiator temp {500, 700, 900} K; structural strut conduction; total boiloff fraction over dwell {1,2,3} yr; the zero-boiloff cryocooler input power (Carnot × real-fraction at 20 K rejecting to 90 K) and its adder to the reactor load.
- **OUT:** the O₂ tank (near its 90 K boiling point at Saturn ambient — a minor cooling problem, noted not modeled); tank structural mass (Round F's ~34.5 t tankage estimate); the electrolysis plant; cryocooler mass/reliability (power adder modeled, hardware deferred); active-cooling control law.

## Pre-registered hypotheses (numeric, falsifiable, before run.py)

**H-G1 [S] — MLI radiative boiloff at Saturn is small.** With good MLI (ε* ~ 1e-3) and a ~90 K warm boundary, the 77 t / ~510 m² tank's radiative boiloff over a 2-yr dwell is **< 5 %** of the H₂ (the T⁴ scaling makes Saturn ~50–60× better than a 250 K near-Earth boundary). **Falsified** if MLI-only 2-yr boiloff > 10 % at the nominal (90 K, ε*=1e-3).

**H-G2 [S] — ortho-para self-heating is a showstopper if uncatalyzed, ~zero if catalyzed.** Full ortho→para conversion of 77 t releases ~527 kJ/kg > the 446 kJ/kg latent heat, so an uncatalyzed inventory over the dwell self-heats at **> 100 kW** and boils off **> 100 %** of the H₂. Catalytic para-conversion at liquefaction reduces storage self-heating to ~0. **Falsified** if uncatalyzed self-heat < 100 kW over a 2-yr dwell (not a showstopper) or if catalysis leaves > 10 % residual.

**H-G3 [S] — reactor proximity is a showstopper if unshielded, benign if shadow-shielded + separated.** An unshielded view (VF ~0.1) of ~700 K reactor radiators delivers **> 100 W** to the tank (> 10 %/yr boiloff); a shadow shield + boom separation (VF ≤ 1e-3) brings it to **≤ 10 W**. **Falsified** if the shielded (VF 1e-3, 700 K) reactor heat > 30 W (not mitigable to benign).

**H-G4 [S] — with both hard requirements met, storage is tractable.** With para-catalysis + reactor separation, total realistic heat leak (MLI + struts + shielded-reactor) is **10–40 W** → 2-yr boiloff **1–8 %**, OR a **zero-boiloff cryocooler drawing < 2 kW** (negligible vs the 150–440 kWe electrolysis) eliminates it. **Falsified** if total heat > 100 W or the zero-boiloff cryocooler > 10 kW.

**H-G5 [W] — Round F's cryo-H₂ cost is real but manageable; the lever survives.** No modeled configuration with the two hard requirements met loses > 10 % of the H₂ or adds > 10 kW of cryocooler power. **Falsified** if some realistic (met-requirements) configuration boils off > 20 % or needs > 10 kW.

**Honest expected reading (pre-registered):** H-G1/G2/G3/G4 hold. Cryo-H₂ storage at Saturn is **tractable** — the cold environment is a genuine advantage that makes radiative boiloff tiny, and a small cryocooler achieves zero-boiloff — **contingent on two hard design requirements**: ortho-para catalytic conversion at liquefaction (else ~527 kJ/kg self-heating destroys the inventory) and reactor thermal separation via shadow shield + boom (else the hot reactor boils it off). Both are standard-practice, not showstoppers. Net: this **validates and strengthens** the Round F H₂/O₂ departure lever — the scariest cost (cryo-H₂ boiloff) is manageable because Saturn is cold — rather than killing it. The honest risk that remains is the two hard requirements being *engineering commitments*, not free.

## Method

Deterministic. `run.py`: (1) tank geometry from 77 t / para density. (2) MLI radiation q = ε*·σ·(T_h⁴−T_c⁴)·A over the warm-boundary × emittance grid. (3) Ortho-para self-heat = m·Δh_op·(converted fraction)/dwell, uncatalyzed vs catalyzed. (4) Reactor radiation = VF·ε·σ·A·T_rad⁴ over VF × T_rad grid. (5) Strut conduction k·A/L·ΔT for representative composite struts. (6) Total boiloff = Σq·dwell / L_v; zero-boiloff cryocooler input = Σq / (Carnot_COP × real_fraction). **Anchors (cited in code):** LH₂ para density 70.8 kg/m³; L_v(H₂,20 K) 446 kJ/kg; Δh ortho→para 527 kJ/kg; σ 5.67e-8; MLI ε* 5e-4–2e-3; cryocooler real-fraction 0.15–0.25 of Carnot at 20 K→90 K; H₂ mass 77 t (Round F, Isp 420).
