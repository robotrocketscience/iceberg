---
axis: "Program class"
status: open
confidence: high
last_revised: 2026-05-18
related:
  - "[[surviving-cell]]"
  - "[[round-trip-ceiling]]"
  - "[[chunk-mass-cap]]"
  - "[[pitch-capital-framing]]"
---

# Program class

## Current

Technology-demonstrator OR regulated-utility-class infrastructure. **NOT venture.** Venture-class framing is structurally unreachable across the entire explored architecture space.

## Open question

Project-owner commitment: technology-demonstrator (path 2 of the bake-off — accept no commercial cell at conservative anchors) vs regulated-utility-class with requirement waivers (Architecture E under L0-05 ≥ 25-year waiver).

## Last touched by

- rhea R-variant-B-recovery-paths-economic — `5fe5dd5`
- titan-2 R-HE-graze-feasibility — `b2e7a35`

## HISTORY

### 2026-05-15 — Initial scaffold from `ARCHITECTURE-DECISION-MATRIX.md` current-decision-state table

Status: open. Confidence: high.

Current state and open question captured from the matrix's top section as of commit `9704700`. Full audit trail of how this axis arrived at its current state is in the matrix HISTORY section (`water-prop/docs/ARCHITECTURE-DECISION-MATRIX.md`).

---

<!-- Append-only HISTORY entries go below this line. Each entry: ### YYYY-MM-DD — round-name or commit-hash — one-line summary -->

### 2026-05-18 latest+11 — iapetus rounds 6-7-8 (`ccea189` + `7ffc1e6` + `ad18654`) — program-class reframed as four-tranche staged-options structure

Iapetus rounds 6 (pitch-EV-reconciliation), 7 (staged-options-with-technology-gates), and 8 (T1-sensitivity-and-breakeven) collectively reframe the program-class as a four-tranche staged-options structure with kill criteria at each gate. Under this structure: max committed loss $1.15B across worst-case path; expected loss $80M under conservative reactor-program priors (12.5× option-value gain vs prior terminal-bet $1B framing) because tranche 1 ($80M, gated on Fission Surface Power Phase 2 award by year 2) kills the program with probability > 99.95% before downstream spend if FSP-2 is not awarded.

Defensible capital structure: research-grant tranche 1 + venture-sleeve-options tranches 2-3 ($570M combined) + commercial-revenue tranche 4 ($460M Saturn ship). NOT venture-equity; NOT sovereign-bond.

Breakeven T1-probability at pitch headline value $24B is 0.25; public-evidence high estimate of T1 is 0.023 (10.9× gap, plausibly closeable through 2-3 corroborating private signals on FSP-2 negotiation status). At $12B floor, program is structurally unviable even at T1 = 1.0. At $200B induced-demand upside, public evidence alone closes the gap.

Methodology surprise: T3 (B-ring rendezvous survivability) is the highest-leverage technology gate after T1, not T2 (hybrid aerocapture). T3 starts at baseline prior 0.20.

Axis status held at open (project-owner decision point #13 outstanding); confidence high. Drop-in pitch revision text in `water-prop/rounds/R_staged_options_with_technology_gates/STUDY.md` §"Reading".
