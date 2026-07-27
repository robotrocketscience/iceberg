---
axis: "Outbound launch architecture"
status: open
confidence: medium
last_revised: 2026-07-26 (latest+29)
related:
  - "[[program-class]]"
  - "[[chunk-mass-cap]]"
  - "[[15-per-mission-reliability]]"
  - "[[20-reactor-lifetime]]"
---

# Outbound launch architecture

## Current

Chemical kick stage at Earth departure (Trans-Saturn-Injection burn); jettisoned post-burn. Starship economics lifts marginal-IRR by ~2 percentage points but does not change the structural picture (10 percent corporate-growth hurdle unreachable at 200-tonne L1-007 cap even at zero-dollar launch cost).

**2026-07-21 latest+25 — the relay/fleet architecture was opened and closed; the monolithic single-vehicle reactor baseline is restored as the outbound state-of-record (R182-R187 `R_relay_ledger_reconciliation` `aed61c4`; R184 `R_shuttle_reuse_fleet` `7b9adf6`).** A dive-shuttle relay — a mothership parked on a Saturn staging ellipse while reusable shuttles cycle chunks up from the B-ring — was priced across four honesty passes (lifetime → NPV → ops → departure). Every pass converged on the utility hurdle, and R187 (propagating R186's revoked Titan-departure lever through the ledger) flipped the verdict to **"real, dead at honest departure"**: best advantage-ratio d\* = 7.0 percent sits below the 8 percent utility hurdle at every relay option and shuttle count N. The relay survives only as a component library and as the rationale for a demonstrator handoff-rehearsal (REQUIREMENTS §7.5). R184 adds the fleet-launch-mass framing — the reactor is ~60 percent of a fleet's recurring launch mass, so the outbound launch-architecture choice is dominated by reactor mass, not chunk mass, and every year of reactor life is directly monetisable in launch-mass terms (see [[20-reactor-lifetime]]). A **unified chunk-water ledger convention** was adopted (delivered = Earth-handoff mass; propellant debits harvest; hardware debits launch; residence debits work). This does **not** resolve the open Starship-vs-Space-Launch-System question below — that remains the load-bearing project-owner decision on this axis.

## Open question

Project-owner direction (conops note 2026-05-15): 'do not count on Starship, I think Space Launch System is more likely.' Re-derive launch-mass multiplier under Space Launch System pricing. Round queued; no SCOPE.md yet.

## Last touched by

- titan-2 R-launch-cost-sensitivity — `8c29cdd`
- project-owner conops note 2026-05-15
- worktree-115637 R-relay-ledger-reconciliation — `aed61c4` (latest+25; relay/fleet closed NPV-dead, monolithic baseline restored, unified ledger convention)
- worktree-115637 R-shuttle-reuse-fleet — `7b9adf6` (latest+25; reactor ~60% of fleet recurring launch mass)

- 2026-07-26 latest+29: launcher axis parameterized (launcher_cap_multiplier); closure needs x1.2–x5 (Arm A) / x8–x16 (Arm B / electrolysis corridor) effective lift; Starship-refill is the only mover (late-2026 demo); SLS Block 1B/2 cancelled.

## HISTORY

### 2026-05-15 — Initial scaffold from `ARCHITECTURE-DECISION-MATRIX.md` current-decision-state table

Status: open. Confidence: medium.

Current state and open question captured from the matrix's top section as of commit `9704700`. Full audit trail of how this axis arrived at its current state is in the matrix HISTORY section (`water-prop/docs/ARCHITECTURE-DECISION-MATRIX.md`).

---

<!-- Append-only HISTORY entries go below this line. Each entry: ### YYYY-MM-DD — round-name or commit-hash — one-line summary -->

### 2026-07-21 latest+25 — worktree-115637 R-relay-ledger-reconciliation (`aed61c4`) + R-shuttle-reuse-fleet (`7b9adf6`) — relay/fleet architecture opened and closed NPV-dead; monolithic reactor baseline restored as outbound state-of-record

The R182-R187 arc priced a dive-shuttle relay (mothership on a Saturn staging ellipse; reusable shuttles cycle chunks up from the B-ring) across four successive honesty passes — reactor lifetime, then NPV, then ops, then departure. Each pass converged on the utility hurdle. R187 propagated R186's revoked Titan-departure lever (see [[04-inbound-dv-accounting]]) through a unified chunk-water ledger and flipped the verdict to "real, dead at honest departure": best advantage-ratio d\* = 7.0 percent < 8 percent utility hurdle at every relay option and shuttle count N. The relay is retired as a commercial architecture and retained only as (a) a component library and (b) the rationale for a demonstrator handoff-rehearsal objective (REQUIREMENTS §7.5, added this pass). R184 reframed the fleet economics around reactor mass: the reactor is ~60 percent of a fleet's recurring launch mass, so outbound launch-architecture is reactor-mass-dominated, not chunk-mass-dominated. Unified ledger convention adopted campaign-wide (delivered = Earth-handoff mass; propellant debits harvest; hardware debits launch; residence debits work). Status held at open / medium — the Starship-vs-Space-Launch-System project-owner decision is untouched by this arc.

### 2026-07-26 — R-closure-boundary-inversion + R-saturn-water-v2-electrolysis-departure (worktree-172651, latest+29) — launcher requirement quantified: no launcher value closes alone (x16 alone = 0); jointly, Arm A needs x1.2–x5 effective capacity (Starship-refill class 120–500 t), Arm B / electrolysis corridor x8–x16 (800–1,600 t assembled or refilled) at f = 0.80 — largely an artifact of the frozen propellant fraction (per-phase accounting would cut it; un-run fidelity item). Record corrections: encoded 6xFH capacity is 300 t (FINDINGS' 382 t was a wrong per-launch cap); New Glenn / SLS remain un-encoded and immaterial (SLS Block 1B/2 cancelled 2026-02/03; Starship V3 + refill demo late 2026 is the only lever that moves).
