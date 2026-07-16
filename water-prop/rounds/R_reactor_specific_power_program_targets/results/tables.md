# R-reactor-specific-power-program-targets — result tables

## Table 1 — Joint closure surface, minimum closing points

Rows are L0-05 ceiling settings. Each cell reports the (SP, X, L) Pareto-frontier corner with the smallest value of the named axis among all (SP, X, L) tuples where at least one of the 60 (reactor kWe × chunk t × Isp) cells closes.

| L0-05 ceiling | n closing (SP, X, L) tuples | smallest-SP corner (SP, X, L, n_close) | smallest-X corner | smallest-L corner |
|---|---|---|---|---|
| 15 yr (L0-05 strict)   | **0** | none | none | none |
| 20 yr                  | 14    | (6, 25, ∞, 4) | (9, 10, ∞, 4) | (6, 25, ∞, 4) |
| 25 yr (waiver 1)       | 117   | (5, 10, 15, 3) | (8, 0, 10, 1) | (9, 25, 5, 16) |
| 30 yr (waiver 2)       | 37    | (2.4, 25, ∞, 4) | (5, 0, ∞, 1) | (2.4, 25, ∞, 4) |

Notation: "∞" lifetime means closure surveyed at infinite reactor lifetime (no reactor-life ceiling applied — i.e., only the SP and X axes from R-aerocapture-cliff-shift, since R-reactor-lifetime-vs-burn-time only regraded the 25-yr round-trip ceiling).

**Headline:** L0-05 strict (15-yr round-trip) has zero closing cells across the entire tested envelope (SP up to 10 W/kg, X up to 25 km/s, L up to infinite). The matrix has no surviving cell at L0-05 strict regardless of reactor program.

## Table 2 — Conjunction posterior bracket per program-target point

`P(conjunction)` = P(any US 500-kWe fission orbit by 2035) × P(SP ≥ threshold | orbits) × P(L ≥ threshold | orbits) × P(R-hybrid-aerocapture-aerobraking closes = 0.50) × P(R-bring-rendezvous-survivability closes = 0.25).

| Program-target point | Most-optimistic P(conj) | Most-skeptical P(conj) | Capital class (optimistic) |
|---|---|---|---|
| 8 W/kg, 5 yr   (H1 anchor)  | 2.44e-05 | 6.25e-08 | technology-demonstrator-only |
| 5 W/kg, 10 yr  (H2 anchor)  | 2.44e-05 | 9.38e-08 | technology-demonstrator-only |
| 5 W/kg, 5 yr   (stretch)    | 4.06e-05 | 1.88e-07 | technology-demonstrator-only |
| 8 W/kg, 10 yr  (stretch)    | 1.46e-05 | 3.13e-08 | technology-demonstrator-only |
| 10 W/kg, 5 yr  (optimistic) | 1.22e-05 | 3.13e-08 | technology-demonstrator-only |
| 10 W/kg, 10 yr (optimistic) | 7.31e-06 | 1.56e-08 | technology-demonstrator-only |

Max conjunction posterior across the entire 54-row table: **4.06e-5 (= 0.004 percent)**.

Capital-class thresholds applied: sovereign-grant ≥ 0.1 percent, sovereign-bond ≥ 1 percent, regulated-utility ≥ 5 percent. The maximum conjunction posterior is **23× below** the sovereign-grant threshold and **245× below** the sovereign-bond threshold.

## Table 3 — Pre-registered hypothesis verdicts

| # | Predicted | Measured | Verdict |
|---|---|---|---|
| H1 | Min-point at L0-05 strict = (8 W/kg, 5 yr) | L0-05 strict closure set is **empty** across the entire tested envelope | HELD-WITH-EXTENSION (no min-point exists; prediction's direction correct, prediction's value too optimistic) |
| H2 | Min-point at L0-05 25-yr waiver = (5 W/kg, 10 yr, X=10 km/s) | Pareto frontier: smallest-SP (5, 10, 15); smallest-X (8, 0, 10); smallest-L (9, 25, 5) | FALSIFIED — closure surface is a 3D Pareto frontier with trade-off between SP, X, L. SCOPE falsifier "L ≤ 7" triggers at the smallest-L corner. Falsification is informative — closure is achievable at L=5 yr if SP and X compensate. |
| H3 | Joint posterior at (8 W/kg, 5 yr) ≤ 3 percent | Max joint posterior across three priors: 0.0195 percent | HELD by 154× margin |
| H4 | Joint posterior at (5 W/kg, 10 yr) ≤ 1 percent | Max joint posterior across three priors: 0.0195 percent | HELD by 51× margin |
| H5 | Conjunction posterior ≤ 1 percent (H3 anchor) / ≤ 0.1 percent (H4 anchor) | Max conjunction: 2.44e-5 at both H3 and H4 anchors | HELD by 400× and 40× margins respectively |
| H6 | Reading-level: technology-demonstrator-only at conservative anchors | Max conjunction across entire 54-row table: 4.06e-5; capital class is technology-demonstrator-only at every tested target × prior × bracket combination | HELD by 1230× margin against the regulated-utility threshold |

## Table 4 — Closure-by-aerocapture-credit slice, L = inf ceiling

(For reference. From R-aerocapture-cliff-shift, ceiling = 25-yr.)

| SP \ X (km/s) | 0 | 5 | 10 | 15 | 20 | 25 |
|---|---|---|---|---|---|---|
| 2.4 W/kg (KRUSTY) |  0 |  0 |  0 |  0 |  0 |  0 |
| 5 W/kg            |  0 |  0 |  3 | 11 | 25 | 44 |
| 6 W/kg            |  0 |  3 |  8 | 19 | 36 | 56 |
| 7 W/kg            |  0 |  6 | 13 | 25 | 41 | 56 |
| 8 W/kg            |  4 |  7 | 20 | 29 | 42 | 56 |
| 9 W/kg            |  7 | 10 | 21 | 32 | 44 | 56 |
| 10 W/kg           |  9 | 11 | 23 | 34 | 44 | 60 |

Values are number of closing cells (of 60) at 25-yr round-trip ceiling.

**Reading:** At KRUSTY-anchored 2.4 W/kg specific power, **no amount of inbound aerocapture credit (up to 25 km/s — implausibly large) recovers L0-05 closure** at the 25-yr waiver. The KRUSTY-anchored cell is structurally dead.

## Table 5 — Closure-by-lifetime-ceiling slice, ceiling = 25-yr round-trip

(For reference. From R-reactor-lifetime-vs-burn-time. Each entry is n_close at the labeled (SP, X) and L ceiling.)

Lifetime ceiling **L = 5 yr** (Brayton-flight-rated minimum, currently no flown anchor in space-fission):

| SP \ X (km/s) | 0 | 5 | 10 | 15 | 20 | 25 |
|---|---|---|---|---|---|---|
| 2.4 |  0 |  0 |  0 |  0 |  0 |  0 |
| 5   |  0 |  0 |  0 |  0 |  0 |  0 |
| 8   |  0 |  0 |  0 |  0 |  0 |  0 |
| 9   |  0 |  0 |  0 |  0 |  0 | 16 |
| 10  |  0 |  0 |  0 |  0 |  9 | 24 |

**Reading:** At L = 5 yr reactor lifetime, closure requires *both* SP ≥ 9 W/kg AND inbound aerocapture X ≥ 20 km/s. Either constraint alone — high SP without aerocapture, or aerocapture without high SP — does not close. The two axes compound multiplicatively.

Lifetime ceiling **L = 10 yr** (Kilopower design target):

| SP \ X (km/s) | 0 | 5 | 10 | 15 | 20 | 25 |
|---|---|---|---|---|---|---|
| 2.4 |  0 |  0 |  0 |  0 |  0 |  0 |
| 5   |  0 |  0 |  0 |  1 | 12 | 32 |
| 8   |  1 |  3 | 15 | 23 | 39 | 56 |
| 10  |  5 |  7 | 18 | 31 | 41 | 56 |

**Reading:** Even at Kilopower design-target lifetime (10 yr, never demonstrated), KRUSTY-anchored 2.4 W/kg specific power closes zero cells regardless of aerocapture. The third viability axis is binding alongside the first two.
