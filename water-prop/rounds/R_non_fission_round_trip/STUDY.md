# R-non-fission-round-trip — STUDY

**Round:** R-non-fission-round-trip. SCOPE pre-registered 2026-07-20 with scripted bounds (`scope_bounds.py`).
**Worker:** worktree-115637 session. The end-to-end test R173 demanded of itself.

## Results vs registered hypotheses

### H1 — full-chain bank 86–105 t — **FALSIFIED (registration mismatch)**

Measured 79.8 t at the sweep's canonical corner. The scripted bound used the 83 kW array; the sweep's floor is 100 kW, whose extra lit braking shrinks the bank below the band. The substantive claim survives: the full chain is **2.7× R173's inbound-only bank** — capture and ring operations, both dark, and the haul-the-gas-through-every-burn compounding are real.

### H2 — no corner under 6× — **FALSIFIED, by real structure**

Best corner: **4.8×** the reactor baseline (80 t chunk, 300 kW array, moon-tour relief on capture/ops, 480 s gas, chemical-kick outbound; 58.8 t bank, 483 t to orbit). Big chunks amortize the fixed bank and array; the scripted two-point estimate (15.6–20×) missed that. Nothing approaches R173's 1.74×.

### H3 — outbound dominates — **HELD**

Outbound propulsion is ≥ **81 percent** of launch mass at every swept corner. The wall was never the Saturn side; it is pushing several hundred tonnes of departure stack out of Earth's gravity well without a reactor-driven spiral.

### H4 — the honest reversal — **FALSIFIED as compounded, corrected in substance**

The registered statement ("reverts fully to fission-dependent") was too strong, like the 6× floor: the corrected verdict is that **a non-fission round trip exists at best ≈ 4.8× the reactor's launch economics** — a factor sitting squarely between R173's boundary-limited 1.74× and the pre-script's naive 15.6×. Bet #3's final form after four rounds of this arc: **the reactor buys back roughly 80 percent of the launch bill; its absence is survivable physics but brutal economics.**

## Two bug-catches (protocol §bug-catch)

1. First sweep scaled R173's lit delta-v linearly with array power and ignored stack mass, inflating lit braking ~4× at heavy corners and manufacturing a false 1.4× cell. Caught by hand-check of the winning corner before any claim shipped.
2. The bank-sizing iterator's `max(rem, 0)` clamp silently reported convergence at its seed whenever the lit leg zeroed the residual requirement — a 40 t "bank" that owed 54 t. Caught because the printed bank equalled the initializer exactly. Lesson recorded: **a solver output equal to its seed is a red flag, always.**

## Revisit (mandatory)

Both registered numeric bounds fell — one to a registration/sweep mismatch (canonical must be pinned to identical parameters in pre-script and sweep; convention amended), one because the pre-script priced two points where the sweep explored amortization. That is the second consecutive round where the sweep found genuine structure below the scripted floor — the pre-script convention is working as a falsifiable-belief generator, exactly as intended. Thin spots carried forward honestly: kick staging modeled as a 1.12 factor with no stage dry-mass optimization; spiral-mode trip time unpriced against L0-05 (the 15.7 km/s lit-spiral both busts economics *and* would bust schedule); the moon-tour relief numbers inherit R_saturn_capture_moon_gravity_assist's single-tour anchors; reactor baseline held fixed at the audit's 50 t / 40 t.

## Cross-learning

- **Corrects R173's headline (self-demanded):** "1.74×" was the inbound floor, not the mission price. The matrix should carry: non-fission round-trip variant closes at ≈ 4.8× launch economics, outbound-dominated.
- **The three bets stand, re-weighted:** bet #3 is now a quantified economic bet (≈ 4.8× vs 1×), no longer an existence bet. Demonstrator gates A/B remain fission-free regardless (R171/172 adoption).
- **For the orchestrator:** matrix Saturn-side-power axis and the R173 amendment note both need this round cited together; mission-graph encoding of `solar_bank_inbound` remains worthwhile for full-fidelity confirmation of the 4.8× figure.
- **Follow-on candidates:** kick-stage staging optimization (the 81 percent line item deserves its own round); L0-05 schedule audit of the spiral mode; refueling-depot variants (LEO water depot cuts the kick's mass ratio — the program's own product as its own propellant).
