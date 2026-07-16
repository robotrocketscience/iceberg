# Public-release runbook — iceberg

How this repository was prepared for publication, what was verified, and what
remains to do at and after the visibility flip. Same pattern as
trajectory-bot's runbook.

## Done (verifiable)

- **Fresh-history snapshot (2026-07-15).** The private working repository's
  history is not publishable (private material remains reachable in old
  commits and in commit messages that reference it). This repository was
  therefore initialized from a curated snapshot of the private repo's `main`
  at `43a037a`, tracked files only, with fresh history. There is no object
  continuity with the private repository.
- **Excluded at snapshot:** `startup/` (business planning), `SESSION-LOG.md`,
  `.planning/`, `PARALLEL-SESSIONS.md`, `CLAUDE.md`,
  `SATURN-PUNCH-LIST-20260521.md`, `ICEBERG-pitch.pdf` (stale pre-scrub
  render), `water-prop/docs/HANDOFF-2026-05-15*.md` (session handoffs), and
  five results JSON files over 500 KB (regenerable from their rounds'
  `run.py`).
- **Scrubbed at snapshot:** references to non-public business relationships
  neutralized; USER-NOTES annotation blocks stripped from all `design-axes/`
  files; five stale plot renders regenerated from the current generator
  script; one hardcoded local output path fixed in `saturn_rendezvous_sim.py`.
- **Verification before first commit:** case-insensitive word-boundary grep
  for the scrubbed markers returns zero hits; `gitleaks` clean; personal-name
  / email / hostname / local-path sweeps clean; `uv run pytest` green in
  `water-prop/`.
- **CI:** `ci.yml` (pytest on Python 3.13 via uv) and `secrets-scan.yml`
  (gitleaks over full history + private-pattern scan keyed to the
  `PII_PATTERNS_SECRET` org secret, no-op for forks).

## At/after the visibility flip

1. Apply branch protection via `gh api` once the repo is public (free-tier
   org repos only get rulesets when public): required status checks
   `tests`, `gitleaks`; linear history; block force-push and deletion.
2. Enable secret scanning + push protection + Dependabot alerts.
3. Confirm the `PII_PATTERNS_SECRET` org secret is visible to this repo.
4. Verify a green Actions run on `main`.
5. Website cross-link once the write-up page is live at
   robotrocketscience.com/projects/iceberg/.

## Claims discipline (for the README and the website write-up)

- The study's verdict is conditional, and every stated closure number carries
  its anchor: capture-efficiency multiplier, specific-impulse floor, reactor
  availability. Do not quote a closure rate without its floor and anchors.
- Megawatt-class rows are upside-only by standing project directive; never
  headline them.
- No hardware exists; no flight heritage is claimed. Momentus Vigoride is the
  closest flown precedent for water propulsion and belongs to Momentus, not
  to this project.
- The paper trail is honest by construction: retractions stay in the record.
  Quote them when they qualify a claim.
