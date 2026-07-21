# R-rtg-keepalive — STUDY

**Round:** R-rtg-keepalive. SCOPE pre-registered 2026-07-21 with scripted bounds (`scope_bounds.py`), before `run.py` existed.
**Worker:** worktree-115637 session. Owner-directed follow-on to the closed-loop-generator / RTG conversation.

## Results vs registered hypotheses

### H1 — the unpriced liability — **HELD**

Pricing bus baseload + cold-tier ZBO cryocooler input (13.3 We per tonne of banked gas, straight from R172's TIERS) at the canonical corner: bank **79.8 → 91.3 t**, keep-alive gas **11.0 t = 4.2×** the legacy 2.6 t hotel line (9.8 t of it on the outbound cruise), launch mass **+82 t**. R174–R176's small-array corners were all quietly optimistic by roughly this much. The regression anchor held exactly (keep-alive off reproduces R174's 79.8 t).

### H2 — array self-coverage at the optimum — **HELD**

Every 300 kW corner with unshadowed ops shows **0.0 t** shortfall gas; even the worst shadowed-ops 300 kW stress cell (80 t chunk, 600 We bus, 2 yr ops at 50 % availability) needs only 0.86 t. The R176 best-corner launch mass shifts **0.0 %**. The arrays the non-fission variant already carries cover its dark keep-alive at Saturn — **the 3.57× headline stands untouched, and this session's conversational claim that RTG keep-alive is "genuinely promising" is wrong at the economic optimum.** The RTG's entire constituency is the small-array corners.

### H3 — the RTG niche, sized — **FALSIFIED (registration mismatch + real structure)**

N\* = 4 (in band), PuO2 19.2 kg (inside the Cassini envelope) — but net saving **148 t** vs the registered 55–90, and **no interior optimum**: launch falls ~**19 t per MMRTG** monotonically through N=10. Cause: the pre-script's N-scan never implemented the trickle credit that the SCOPE's own model paragraph registered — an R174-class mismatch, this time in mechanism rather than parameter. With trickle live, each unit's spare watts regenerate ~0.96 t of inbound gas from chunk water, compounding through the chain (×2.7) and the 2-stage kick (×5.84×1.2) to 18.9 t of launch — closed-form check matches the sweep steps exactly. The true optimum sits at the trickle cap (residual-demand saturation, ~N≈11, ~53 kg PuO2 — past the Cassini envelope), so the practical suite is bounded by plutonium procurement, not by physics.

### H4 — both conversational claims adjudicated — **HELD**

Trickle at N\* is **3.65 t** (band 3–6): the session's "≤ 2 t, negligible" claim is **formally falsified**, as the pre-script predicted. The bulk reductio confirms the other half: charging the canonical bank by RTG alone needs **48 MMRTGs** (~230 kg PuO2) — RTG-as-electrolysis-plant stays dead; RTG-as-trickle-regenerator is real money at small-array corners.

## Bug-catch (protocol §bug-catch)

1. Pre-script/model mismatch (drove the H3 falsification, above): the scripted N-scan omitted the registered trickle mechanism. Lesson recorded: **the pre-script must implement every mechanism the SCOPE's model paragraph registers, not only its parameters.**
2. The draft figure annotated an "interior optimum" that the data had already falsified; caught on render review before shipping.

## Revisit (mandatory)

Thin spots carried honestly: trickle credit assumes residual burns land after regeneration accrues (burn-scheduling unmodeled); regenerated-gas ZBO inventory unmodeled (second-order); keep-alive product water vented — recovering it would shrink the liability with no RTG at all and deserves its own look; MMRTG waste heat (~2 kWt/unit) unmodeled, would offset heater and cryocooler load in the RTG's favor; economics are full-kick 2-stage (R176's hybrid split not re-ported — relative deltas approximately carry; the best corner is untouched either way); and the PuO2 ledger prices launch mass only — 19.2 kg is ~4 Perseverance loads against ~0.5 kg/yr current US production, a procurement bet of the same species as bet #3, unpriced here and flagged.

## Cross-learning

- **Corrects R174/R175/R176 at small-array corners:** their banks/ratios omit an 11 t-class keep-alive line (+~10 % launch at canonical). Big-array corners — including the standing 3.57× — are unaffected; matrix amendment should say exactly that.
- **The honest RTG statement for the matrix:** *an MMRTG suite is worthless where the non-fission variant already wins (300 kW arrays self-cover), and worth ~19 t of launch per unit at power-poor corners — as a trickle regenerator more than a keep-alive source — up to a plutonium-procurement wall at ~50 kg PuO2.*
- **Convention amended (third consecutive pre-script lesson):** scripted bounds must implement registered mechanisms, not just registered parameters.
- **Follow-on candidates:** keep-alive product-water recovery loop (attacks H1's liability at zero PuO2); array-spare chunk-fed regeneration at mid-array corners (the kWe-scale big brother of trickle); trickle-timing fidelity vs mid-course burn schedule; Pu-238 procurement base-rate round (locked-findings style) before any RTG suite is baselined.
