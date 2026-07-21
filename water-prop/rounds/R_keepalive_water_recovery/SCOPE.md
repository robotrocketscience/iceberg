# R-keepalive-water-recovery — adjudicating R177's own follow-on: does recovering keep-alive product water buy anything?

**Status:** SCOPE pre-registered 2026-07-21, before `run.py`. Bounds from `scope_bounds.py`, committed alongside.
**Worker:** worktree-115637 session. This round questions a suggestion **this session made**: R177's STUDY named product-water recovery a "zero-PuO2 attack on the H1 liability." The pre-script indicates the suggestion dies on a structural theorem; the round registers that expectation and the sweep tries to break it.

## The structural claim

In the chain model, spare power and keep-alive shortfall are pointwise mutually exclusive (spare > 0 ⟺ shortfall = 0), so recovery can never re-split product water with energy that coexists with the draw — it can only time-shift feedstock. Feedstock is scarce only outbound (no chunk aboard), and with monotone-declining outbound array power against a constant load there is a **single crossing radius: the spare window closes at exactly the point the draw opens**. The re-split credit is identically zero. What is left to price: the crossing structure across corners, the retention penalty (venting adjudicated as optimal rather than merely conservative), and the dead condenser hardware.

## Pre-registered hypotheses (bounds scripted)

**H1 [S] (mutual-exclusion theorem, numerically verified).** The pointwise product spare × shortfall is **exactly zero** at every trajectory grid point of every swept corner. Falsified by any nonzero overlap.

**H2 [S] (crossing structure).** Wherever a draw exists, the spare window closes at the same radius the draw opens (single crossing): canonical crossing **6.5–6.8 AU** with draw **9.3–10.3 t** (scripted 6.63 / 9.83); stress corner (600 We, 100 kW) **5.9–6.2 AU / 14–16 t**; at 300 kW no draw exists anywhere — nothing to recover. Re-split credit **identically 0** at every corner. Falsified if any corner shows a credit > 0.1 t.

**H3 [W] (the kill, and venting adjudicated optimal).** Recovery's net effect is ≤ 0 at every corner: credit 0, condenser allowance (50–100 kg) −0.3 to −0.7 t of launch, and *retaining* the product water instead of venting costs **110–140 t of launch at the canonical corner** (scripted 124: 9.8 t hauled through 3.85 km/s of burns compounds to 13.6 t of gas). **The R177 follow-on suggestion is falsified; the R174–R178 venting convention was optimal, not merely conservative.** Falsified if any corner nets positive.

**H4 [W] (no quantitative rescue).** The abort-feedstock argument also fails at R179's honest anchors: a light-ship abort return needs ~69 t of gas (20 t × (e^(7.0/4.71)−1)) against a ~10 t recovered inventory — recovery cannot make abort-return gas either. Surviving roles are qualitative only (radiation shielding, trim ballast) — named, not claimed, unpriced. Falsified if the abort arithmetic closes within 2× on recovered inventory.

## Sweep

array {100, 150, 200, 250, 300} kW × P_ka {150, 300, 450, 600} We × bank {40, 70, 91, 120} t: crossing radius, draw, overlap integral, retention penalty per cell.

## Deliverables

`scope_bounds.py`, `run.py` (+ `results/recovery_adjudication.png`), `results/findings.json`, `STUDY.md` with Revisit; matrix note: convention elevated — *vent keep-alive product water; recovery is structurally dead in-mission* — plus the transient-interleaving caveat (eclipses/attitude events create brief spare/draw interleaving a smooth model cannot see; second-order, flagged).
