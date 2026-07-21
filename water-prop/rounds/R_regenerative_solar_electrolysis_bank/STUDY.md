# R-regenerative-solar-electrolysis-bank — STUDY

**Round:** R-regenerative-solar-electrolysis-bank. SCOPE pre-registered 2026-07-20 before `run.py` existed.
**Worker:** worktree-115637 session. Owner-directed follow-on to R-h2o2-closed-cycle-power-bridge.

## Hypotheses, tests, results

Computations in `run.py` (Kepler harvest integral, zero-boil-off ledger, mass rollup); numbers in `results/findings.json`; figures `regen_bank_mass.png`, `zbo_ledger.png`.

### H1 — harvest is cheap — **FALSIFIED on the power bound, mass held**

| metric | predicted | measured | held? |
| --- | --- | --- | --- |
| worst-corner array rating at 1 AU | ≤ 60 kW | **82.7 kW** | **FALSIFIED** |
| array + electrolyzer mass | ≤ 1.0 t | 0.77 t | (held) |

**Reading.** The SCOPE's 60 kW bound came from a hand-derived charge window of 1.25 years inside 3 astronomical units; the Kepler solve gives **0.62 years** — I doubled the transfer ellipse's period by hand in the pre-registration. Half the window, twice the array. The corrected picture is still cheap in mass (0.77 t) but the rating is real hardware: ~83 kW at 1 AU is four International-Space-Station roll-out-array wings. Feasible, not free.

### H2a — warm-tier cryo self-consumption — **HELD**

Cruise-integrated zero-boil-off electric demand at 10 W/t insulation is **2.15× the bank's entire chemical inventory**, at every grid point (the ratio is duty-independent — both sides scale with reactant mass). A conventionally insulated liquid-hydrogen bank eats itself before Saturn. This is the quantitative form of the campaign's old "multi-year H2 storage kills it" flag.

### H2b — cold-tier design closes, array carries the cooler — **HELD**

At 1.5 W/t (sunshield + deep blanket) with a 40 K precooled stage, bank self-drain is **zero at every grid point**: the charge array, already sized for electrolysis, out-supplies the cryocooler all the way to 9.5 astronomical units (worst corner: 426 W needed, 919 W available at arrival — still 613 W after applying the same 1.5× low-intensity derate used on the comparator, a check the SCOPE did not demand but the Revisit did). The array does double duty; the low-intensity penalty that ruins direct-solar hotel power is irrelevant to a load this small.

### H3 — mass ranking — **HELD**

Regenerative bank beats direct-Saturn solar at every duty point (2.25–6.5×); sits at or below the Kilopower band for discharges ≤ 100 GJ (0.87–2.6 t) and above it at the big corners (7.6 t at 15 kWe × 6 months).

### H4 — burst niche — **HELD**

Capture-ops bursts (50–100 kWe × 1–3 days): the bank costs 0.6–1.7 t against 4.8–28.8 t of batteries (7.7–16.6×) and 57–114 t of Saturn solar (65–91×). For burst power at Saturn, nothing else is close.

### H5 — closure, by citation — held as registered

Round 171's H4 stands: this round changes hotel and burst power, not propulsion energy; closure remains fission-gated or L0-05-relaxed.

## Revisit (mandatory)

One falsification, and once again it is the analyst, not the physics: a hand-doubled orbital period in the SCOPE's derived charge window. That is the fourth consecutive round where a pre-registered bound fell to worst-corner or derived-quantity arithmetic rather than to the concept under test. The convention now gets its final form: **derive every SCOPE bound from a scripted calculation, not by hand — if run.py will compute it, a ten-line pre-script must compute the bound.** Assumption checks done here beyond the SCOPE's ask: low-intensity derate applied to the charge array's Saturn-side role (survives, 613 W > 426 W); reversible-stack vs separate electrolyzer + fuel cell (separate units assumed, conservatively heavier); the cold-tier 1.5 W/t insulation figure is the round's largest unmodeled bet — it assumes sunshield architecture of James-Webb class discipline on a propellant tank, and a bench-to-flight number for it does not exist in the campaign's source base.

## Cross-learning

- **Adopt (scoped, upgraded from round 171):** the regenerative solar-electrolysis bank is the recommended non-fission Saturn-side power architecture: hotel loads at 0.9–2.6 t for duties up to ~100 GJ (inside the Kilopower band, with zero reactor dependence and flown-heritage components), and burst power at 10–90× over alternatives. The 83 kW-class 1-AU array doubles as outbound solar-augment per R_hybrid_solar_augmentation.
- **Kill within the concept:** warm-tier (conventional) hydrogen storage, permanently — 2.15× self-consumption is not a margin problem.
- **New bench item (joins the bag list):** sunshielded zero-boil-off hydrogen tankage at ≤ 1.5 W/t — the single unproven number the architecture now leans on.
- **For the orchestrator:** demonstrator Gates A/B power system recommendation upgrades from "fuel-cell bank" to "regenerative bank, launched-reactant mode" (no electrolyzer needed at demo scale); matrix axis candidate: Saturn-side power source now has three priced options (reactor / launched bank / regenerative bank).
- **Follow-on candidates:** scripted-bounds pre-check harness (methodology, cheap); thermal model of the sunshielded tank to put an anchor under 1.5 W/t; combined array/augment trajectory round (does the 83 kW array shorten the outbound spiral enough to pay for itself twice?).
