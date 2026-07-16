---
type: design-axes-index
last_revised: 2026-05-22
---

# ICEBERG Design Axes — index

Living document tracking the design axes the campaign is converging on. One file per axis under `design-axes/` at the project root. This index renders an at-a-glance current-state table (Dataview) plus a manual table fallback for non-Obsidian viewers.

> **Convention for HISTORY entries:** append-only. Each entry begins with `### YYYY-MM-DD — round-name or commit-hash — one-line summary`. Never silently rewrite a prior HISTORY entry. Supersessions go as a new entry that references the prior.

---

## At-a-glance current state — Dataview (Obsidian)

```dataview
TABLE
  status,
  confidence,
  last_revised
FROM "design-axes"
WHERE axis
SORT file.name ASC
```

If you're viewing this outside Obsidian or Dataview is not installed, the manual table below mirrors the same information; it's kept current by the orchestrator at each integration pass.

## At-a-glance current state — manual (fallback)

| # | Axis | Status | Confidence | File |
|---|---|---|---|---|
| 01 | Program class | 🟡 open | high | [[01-program-class]] |
| 02 | Surviving cell at conservative anchors | 🟡 open | high | [[02-surviving-cell]] |
| 03 | Inbound propulsion choice | ✅ closed | high | [[03-inbound-propulsion]] |
| 04 | Inbound delta-velocity accounting | ✅ closed | high | [[04-inbound-dv-accounting]] |
| 05 | Reactor power floor | 🟡 open | high | [[05-reactor-power-floor]] |
| 06 | Reactor specific power assumption | ✅ closed | high | [[06-reactor-specific-power]] |
| 07 | Radiator mass model | ✅ closed | high | [[07-radiator-mass-model]] |
| 08 | Saturn-side process power | 🟡 open | medium | [[08-saturn-side-process-power]] |
| 09 | Chunk-mass cap (L1-007) | 🟡 open | high | [[09-chunk-mass-cap]] |
| 10 | Round-trip ceiling (L0-05) | 🟡 open | high | [[10-round-trip-ceiling]] |
| 11 | Earth-arrival mode | 🔴 falsified | high | [[11-earth-arrival-mode]] |
| 12 | Saturn-side capture mode | 🔴 falsified | high | [[12-saturn-side-capture-mode]] |
| 13 | Outbound launch architecture | 🟡 open | medium | [[13-outbound-launch-architecture]] |
| 14 | Cruise trajectory | 🟡 open | low | [[14-cruise-trajectory]] |
| 15 | Per-mission reliability (L0-10) | ✅ closed | high | [[15-per-mission-reliability]] |
| 16 | Concept-of-operations document | 🟡 open | medium | [[16-conops-document]] |
| 17 | Pitch / capital framing | 🟡 open | high | [[17-pitch-capital-framing]] |
| 18 | Saturn-orbit-insertion delta-velocity | ✅ closed | high | [[18-saturn-soi-dv]] |
| 19 | Capture architecture (chunk vs ram-scoop) | 🔴 falsified | high | [[19-capture-architecture]] |
| 20 | Reactor lifetime | 🟡 open | high | [[20-reactor-lifetime]] |
| 21 | Architecture source comparator | 🟡 open | medium | [[21-architecture-source-comparator]] |

Legend: 🟡 open = decision outstanding; ✅ closed = decision made and stable; 🔴 falsified = a prior position has been falsified and no replacement decision is in place yet.

---

## Project-owner decision points outstanding (latest state)

These are the rows above marked open with confidence high. The five load-bearing decisions:

1. **Program class** ([[01-program-class]]) — technology-demonstrator vs regulated-utility-with-waivers vs continue exploring rescue paths.
2. **Round-trip ceiling** ([[10-round-trip-ceiling]]) — hold L0-05 strict at 15 years (no surviving cell) or admit waiver to ≥ 25 years (Architecture E closes at 50 t/mission).
3. **Chunk-mass cap** ([[09-chunk-mass-cap]]) — hold L1-007 at 200 tonnes (binding economic constraint) or admit relaxation. With multi-chunk falsified, relaxation requires single-chunk > 200 t (exceeds tested architectures).
4. **Outbound launch architecture** ([[13-outbound-launch-architecture]]) — Starship vs Space Launch System assumption per the project-owner conops note 2026-05-15. Affects per-mission launch mass and economics across the matrix.
5. **Reactor program path** ([[05-reactor-power-floor]]) — **AMENDED 2026-05-19 latest+13** under project-owner directive retiring 500 kilowatt-electric power class. Prior L0-24 framing (Fission-Surface-Power Phase 2 + 500 kilowatt-electric scope) is moot. New decision: accept 30 kilowatt-electric Kilopower-extrapolation as flyable (softens the locked-memory "Kilopower-class single-kilowatt at best" envelope; enables titan-3 R-chunk-size-pareto closure cell at 40-80 tonne chunks), OR hold the strict single-kilowatt envelope and accept campaign termination at flyable power, OR require a KRUSTY-scale-up-credibility audit round before treating 30 kilowatt-electric closure as real. Demonstrator-class missions exempt per §7.5; the open question is what reactor class the demonstrator targets.
6. **Pricing anchor** (latest+9 addition; touches [[17-pitch-capital-framing]]) — project-owner-triggered challenge to the $1,400/kg pitch headline. Audit (`water-prop/rounds/R_pricing_anchor_revisit/AUDIT.md`) shows no load-bearing financial round uses $1,400/kg; most anchor at $2,000-10,000/kg already. Pricing-anchor correction is real (pitch headline is too low) but does NOT flip the program-class verdict — reactor-program-availability per L0-24 is the binding constraint. R-pricing-anchor-revisit H7 is the deciding round; pitch rewrite blocked on it.
7. **Pitch staged-options reframe** (latest+11 addition; touches [[01-program-class]], [[17-pitch-capital-framing]]) — project-owner-decision-point-#13: accept iapetus R7 four-tranche staged-options structure ($80M + $260M + $310M + $460M, max committed $1.15B, expected loss $80M under conservative anchors) as the pitch's capital-framing of record? Drop-in text in `water-prop/rounds/R_staged_options_with_technology_gates/STUDY.md` §"Reading".

## Sole high-leverage open round

**R-no-atmospheric-capture-baseline** — named by R-chunk-as-heat-shield itself as the load-bearing next-step. No worker has run it. Touches [[02-surviving-cell]], [[10-round-trip-ceiling]], [[11-earth-arrival-mode]].

---

## Relationship to the architecture decision matrix

`water-prop/docs/ARCHITECTURE-DECISION-MATRIX.md` is the architectural-cell synthesis document. Its top section ("Current decision state — design axes") is intentionally redundant with this index — the matrix is the architecture story, this index is the per-axis decision tracker. When they disagree, this index is canonical for design-axis state; the matrix is canonical for architectural-cell viability synthesis.

Audit trail of how the current decision state was arrived at lives in the matrix HISTORY section (PAUSE / UPDATE / FALSIFICATION blocks plus the source-rounds tables). Per-axis HISTORY blocks in the axis files reference back to the matrix HISTORY for the broader narrative.

## Living-document conventions (recap)

- **Per-axis files** in `design-axes/NN-slug.md`. One file per axis. Filename is stable across the campaign; rename only with a HISTORY entry noting the rename.
- **YAML frontmatter** carries structured state (`axis`, `status`, `confidence`, `last_revised`, `related`). Dataview queries off this.
- **Current** block: 3-5 sentences. Stable enough that the orchestrator surgically edits in place, never wholesale rewrites.
- **Open question** block: what's outstanding. Closed axes say "Closed."
- **Last touched by** block: the round(s) and commit(s) that produced the current state. Orchestrator updates on each amendment.
- **HISTORY** block at bottom: append-only entries. Supersessions are new entries that reference the prior; never rewrite or delete a prior entry. ADR pattern.
- **Amendments are surgical.** The orchestrator finds-and-replaces inside a block; never rewrites the whole file. This is what keeps user annotations safe.
