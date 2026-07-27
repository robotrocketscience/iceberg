---
axis: "Inbound propulsion choice"
status: closed
confidence: high
last_revised: 2026-07-26 (latest+29)
related:
  - "[[inbound-dv-accounting]]"
  - "[[outbound-launch-architecture]]"
---

# Inbound propulsion choice

## Current

All-electric end-to-end. Chemical-trim at Earth capture is falsified as a Variant-B saver (chemical exhaust velocity 4.41 km/s is 4.45x lower than electric 19.62 km/s; smaller chemical burn eats more propellant than the larger electric burn it replaces).

**2026-05-22 latest+18 — bet #2 audit + demonstrator-mission concept ammend electric-thruster choice with an architecture-trap finding:** the matrix's closure cells run at Isp 2000 s (RF-ion class), which closes the matrix on Isp but is **contamination-SENSITIVE on Saturn-ring water** (hyperion R-water-electrothermal-flight-scale-audit `cd8d753`). Microwave-Electrothermal-Thruster (the contamination-tolerant thruster a Kilopower-class small vehicle would naturally fly) at realistic continuous flight 500-700 s gives 0-0.5 percent matrix closure (the 800-s ground/pulse A1 anchor is above the campaign's own R0 continuous ceiling and yields only 4 percent). The two requirements pull against each other; continuous-months flight-readiness on Saturn-ring water at matrix-closing Isp is a conjunction 0.48 mid (0.25-0.73 range), un-flown. Flight gap 144-1461× cumulative operating time versus closest flown precedent. **Demonstrator implication (R-demonstrator-mission-concept `61afe0c`):** the demonstrator must fly the commercial water RF-ion (2000 s) + bag sublimation-distillation filtration stack on dirty chunk water, NOT the power-appropriate MET (~543 s) a small low-power vehicle would naturally fly. MET would prove water-electrothermal in deep space but would not retire the contamination-sensitive RF-ion-continuous bet the commercial matrix actually rests on. Status remains closed on the chemical-vs-electric question; the electric-thruster sub-choice (RF-ion vs MET) is now load-bearing on the demonstrator's bet-#2 retirement.

**2026-07-22 latest+27 — the RF-ion contamination-sensitivity is localized to one derived quantity + one design choice (R-bag-silicate-rejection-derivation `744d9ee`, 5/5 HELD):** the 0.48-conjunction's biggest driver ("bag silicate rejection holds") is not an intrinsic ~10⁻⁴ — it is derived carryover f_pass = massfrac(silicate PSD below the free-molecular cutoff d_max = ρ_gas(T)·L/ρ_grain), which is ~0 at cold bag operation (200 K, d_max 0.6 nm) but 2.6–88 % warm (273 K, d_max 1.6 µm). **Derived design rule: run the bag cold (≤ ~220 K)** — feasible (2.3 m² feeds 0.5 g/s) — to suppress gas entrainment. But an electrostatic nano-tail leak (~3×10⁻² at a Hsu-class inclusion PSD) persists even cold and consumes 373 % of the RF-ion grid via R11's own erosion mapping. So R11's "silicate not a grid-life-limiter" is conditional on the assumed 10⁻⁴ (= cold bag + small nano-tail). The bet reduces to one unmeasured input — **the sub-100-nm silicate inclusion PSD of ring ice** — nameable as a cheap pre-Gate-B measurement that *predicts* the grid outcome the months-continuous run only *exhibits*. Axis stays closed on chemical-vs-electric; this sharpens the bet-#2 demonstrator retirement (cold-bag design + nano-tail PSD measurement).

## Open question

Closed.

## Last touched by

- rhea R-chemical-trim-vs-all-electric-earth-arrival — `47b69bc`
- hyperion R-water-electrothermal-flight-scale-audit — `cd8d753` (bet #2 architecture trap: RF-ion 2000 s closes Isp but is contamination-sensitive; MET 500-700 s tolerates Saturn-water silicates but does not close on Isp)
- hyperion R-demonstrator-mission-concept — `61afe0c` (demonstrator must fly commercial RF-ion + bag filtration, not power-appropriate MET)
- worktree-115637 R-bag-silicate-rejection-derivation — `744d9ee` (bag rejection factor is derived + PSD-gated, not intrinsic 10⁻⁴; cold-bag design rule; nano-tail PSD is the named pre-Gate-B measurement)

- 2026-07-26 latest+29: boundary inversion pins the return-leg Isp requirement (window 2,000–4,000 s Arm A; 3,000 s Arm B) — water-MET 500–800 s confirmed as architecture trap for the return leg.

## HISTORY

### 2026-05-15 — Initial scaffold from `ARCHITECTURE-DECISION-MATRIX.md` current-decision-state table

Status: closed. Confidence: high.

Current state and open question captured from the matrix's top section as of commit `9704700`. Full audit trail of how this axis arrived at its current state is in the matrix HISTORY section (`water-prop/docs/ARCHITECTURE-DECISION-MATRIX.md`).

---

<!-- Append-only HISTORY entries go below this line. Each entry: ### YYYY-MM-DD — round-name or commit-hash — one-line summary -->

### 2026-05-22 latest+18 — hyperion R-water-electrothermal-flight-scale-audit (`cd8d753`) + R-demonstrator-mission-concept (`61afe0c`) — electric-thruster sub-choice (RF-ion vs MET) becomes load-bearing on bet #2 retirement

Audit finds bet #2 (continuous water-electrothermal at flight scale on Saturn-water purity) fails as an architecture trap, not a physics wall. Contamination-tolerant MET at realistic continuous flight 500-700 s gives 0-0.5 percent matrix closure (the 800-s ground/pulse A1 anchor is above the campaign's own R0 continuous ceiling and yields only 4 percent). Isp-sufficient RF-ion at 2000 s closes the matrix on Isp but is contamination-SENSITIVE; continuous-months flight-readiness on Saturn-ring water is a conjunction (bag silicate-rejection holds) × (cathode/grid life ≥ burn) × (no anomaly) = 0.48 mid (0.25-0.73 range), un-flown. Flight gap 144-1461× cumulative operating time versus closest flown precedent (Momentus Vigoride-5 water-MET 2023 orbit-raising; AQUARIUS 91-s water resistojet in deep space).

R-demonstrator-mission-concept synthesises: demonstrator must fly commercial water RF-ion (2000 s) + bag sublimation-distillation filtration stack on dirty chunk water, NOT power-appropriate MET (~543 s) a small low-power vehicle would naturally fly. MET would prove water-electrothermal in deep space but would not retire the contamination-sensitive RF-ion-continuous bet the commercial matrix actually rests on. This is the most-consequential design decision the demonstrator faces; the SCOPE pre-audit assumed MET and was corrected by the bet-#2 audit landing.

Status remains closed on chemical-vs-electric. Sub-choice (RF-ion vs MET) is load-bearing on the demonstrator's bet-#2 retirement path. Locked beliefs `650938e3` (A1 800-s anchor) and `5535179f` (bet #2 framing) surfaced for project-owner update.

### 2026-07-22 latest+27 — worktree-115637 R-bag-silicate-rejection-derivation (`744d9ee`, 5/5 HELD) — the RF-ion contamination-sensitivity reduces to one derived quantity + one design choice

R11 and R_silicate_contamination both *assumed* the bag silicate rejection factor (10⁻³–10⁻⁶, central 10⁻⁴) from vacuum-distillation literature; neither derived it. This round derives it from sublimation-distillation entrainment physics: the free-molecular carryover cutoff **d_max = ρ_gas(T)·L/ρ_grain** swings 0.60 nm (200 K) → 221 nm (250 K) → 1.60 µm (273 K) as ρ_gas ∝ P_sat rises ~3700× over 73 K, so derived carryover f_pass = massfrac(silicate PSD below d_max) is ~0 cold but 2.6–88 % warm (even under a plain q=3.5 power-law — ~25 % of silicate mass sits below 100 nm for r_max = 1 µm). **The assumed 10⁻⁴ is a cold-bag + small-sub-micron-mass corner, not intrinsic.** Derived design rule: run the bag cold (≤ ~220 K, feasible — 2.3 m² feeds 0.5 g/s at 200 K) to suppress gas entrainment. But an electrostatic nano-tail leak (lofting the sub-100-nm tail, residual even cold) gives f_pass ~3×10⁻² at a Hsu-class inclusion PSD, which through R11's own silicate→grid-wear mapping consumes 373 % of the RF-ion grid over the burn — the grid dies even with a perfectly cold bag. So R11's "silicate is not a nominal grid-life-limiter" is conditional on the assumed 10⁻⁴ (cold operation AND small nano-tail). **The bet-#2 grid-erosion story reduces to one unmeasured input: the sub-100-nm silicate inclusion PSD of ring ice** (Hsu 2011 Nature 471 / Hsu 2018 Science 362 detected nanometre SiO₂ in ring-fall/stream particles; the inclusion PSD *within* main-ring ice is not directly measured). Demonstrator implication: a cheap in-situ / sample-return nano-tail PSD measurement *predicts* the grid outcome the months-continuous thruster run only *exhibits* — a sharper, earlier bet-#2 retirement, paired with cold-bag operation as the standing mitigation. 5/5 held because the pre-registration bands were derived from the scope_bounds pre-script (lesson 18/20), not round-number guesses. Status stays closed; this localizes the RF-ion contamination-sensitivity for the demonstrator. Does not change the matrix propulsion-cell status (bet #2 remains an architecture trap).

### 2026-07-26 — R-closure-boundary-inversion + R-saturn-water-v2-electrolysis-departure (worktree-172651, latest+29) — return-leg Isp requirement pinned by inversion: closure window 2,000–4,000 s (Arm A; non-monotone axis — burn time grows with exhaust velocity at fixed power) and 3,000 s (Arm B), landing exactly on the RF-ion-class regime; no water-compatible hardware >900 s exists (water-Hall 2,039 s single lab point). Alternative: skip high-Isp electric entirely via electrolysis-fed nuclear-thermal >=750–900 s impulsive departure (v2 round).
