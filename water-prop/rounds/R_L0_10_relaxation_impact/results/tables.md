# R-L0-10-relaxation-impact — results tables

## 1. L0-10 rolling-5-block minimum p

L0-10 says success rate >= threshold across any rolling block of 5 launches. P(rolling-5-block clears) >= 0.95 requires minimum per-mission p as:

| L0-10 threshold | Minimum per-mission p | P(block clears) at min p |
|---|---|---|
| 0.75 | 0.93 | 0.9575 |
| 0.8 | 0.93 | 0.9575 |
| 0.85 | 0.99 | 0.9510 |
| 0.9 | 0.99 | 0.9510 |

**Reading:** at L0-10's nominal threshold 0.90, the rolling-5-block clauses requires per-mission p ≥ 0.99 for >= 0.95 confidence the block passes. Relaxed thresholds 0.80 and 0.75 share the same min p because both round up to 4-of-5 needed.

## 2. Three L0-09 charitable readings × cadence × p

**Reading (a) — slot-met fraction at 1 / yr contracted cadence.**
**Reading (b) — P(rolling 12-month window has >= 1 delivery), Poisson.**
**Reading (c) — steady-state queue depth (14-yr round-trip).**

### Reading (a) — slot-met fraction (>= 0.95 to clear)

| cadence \ p | 0.50 | 0.70 | 0.80 | 0.90 | 0.95 | 0.99 |
|---|---|---|---|---|---|---|
| 1.0 | 0.50   | 0.70   | 0.80   | 0.90   | 0.95 ✓ | 0.99 ✓ |
| 1.5 | 0.75   | 1.00 ✓ | 1.00 ✓ | 1.00 ✓ | 1.00 ✓ | 1.00 ✓ |
| 2.0 | 1.00 ✓ | 1.00 ✓ | 1.00 ✓ | 1.00 ✓ | 1.00 ✓ | 1.00 ✓ |
| 3.0 | 1.00 ✓ | 1.00 ✓ | 1.00 ✓ | 1.00 ✓ | 1.00 ✓ | 1.00 ✓ |
| 4.0 | 1.00 ✓ | 1.00 ✓ | 1.00 ✓ | 1.00 ✓ | 1.00 ✓ | 1.00 ✓ |
| 6.0 | 1.00 ✓ | 1.00 ✓ | 1.00 ✓ | 1.00 ✓ | 1.00 ✓ | 1.00 ✓ |
| 12.0 | 1.00 ✓ | 1.00 ✓ | 1.00 ✓ | 1.00 ✓ | 1.00 ✓ | 1.00 ✓ |

### Reading (b) — P(window has delivery) (>= 0.95 to clear)

| cadence \ p | 0.50 | 0.70 | 0.80 | 0.90 | 0.95 | 0.99 |
|---|---|---|---|---|---|---|
| 1.0 | 0.393   | 0.503   | 0.551   | 0.593   | 0.613   | 0.628   |
| 1.5 | 0.528   | 0.650   | 0.699   | 0.741   | 0.759   | 0.773   |
| 2.0 | 0.632   | 0.753   | 0.798   | 0.835   | 0.850   | 0.862   |
| 3.0 | 0.777   | 0.878   | 0.909   | 0.933   | 0.942   | 0.949   |
| 4.0 | 0.865   | 0.939   | 0.959 ✓ | 0.973 ✓ | 0.978 ✓ | 0.981 ✓ |
| 6.0 | 0.950 ✓ | 0.985 ✓ | 0.992 ✓ | 0.995 ✓ | 0.997 ✓ | 0.997 ✓ |
| 12.0 | 0.998 ✓ | 1.000 ✓ | 1.000 ✓ | 1.000 ✓ | 1.000 ✓ | 1.000 ✓ |

### Reading (c) — queue depth (>= 1.0 to clear; usually trivial)

| cadence \ p | 0.50 | 0.70 | 0.80 | 0.90 |
|---|---|---|---|---|
| 1.0 | 7.0 ✓ | 9.8 ✓ | 11.2 ✓ | 12.6 ✓ |
| 1.5 | 10.5 ✓ | 14.7 ✓ | 16.8 ✓ | 18.9 ✓ |
| 2.0 | 14.0 ✓ | 19.6 ✓ | 22.4 ✓ | 25.2 ✓ |
| 3.0 | 21.0 ✓ | 29.4 ✓ | 33.6 ✓ | 37.8 ✓ |
| 4.0 | 28.0 ✓ | 39.2 ✓ | 44.8 ✓ | 50.4 ✓ |
| 6.0 | 42.0 ✓ | 58.8 ✓ | 67.2 ✓ | 75.6 ✓ |
| 12.0 | 84.0 ✓ | 117.6 ✓ | 134.4 ✓ | 151.2 ✓ |

## 3. Coordinated revision: minimum p that clears all readings at a relaxed target

If L0-09 is *also* relaxed to the same target as L0-10 (matched coordinated revision), what minimum per-mission p satisfies (a) slot-met, (b) window-has-delivery at the relaxed threshold, AND (c) L0-10 rolling-5-block at >= 0.95 confidence?

| Relaxed L0-09 = L0-10 target | Launch cadence (per yr) | Minimum p required | Feasible? |
|---|---|---|---|
| 0.75 | 1.0 | — | no |
| 0.75 | 2.0 | 0.93 | yes |
| 0.75 | 4.0 | 0.93 | yes |
| 0.80 | 1.0 | — | no |
| 0.80 | 2.0 | 0.93 | yes |
| 0.80 | 4.0 | 0.93 | yes |
| 0.85 | 1.0 | — | no |
| 0.85 | 2.0 | 0.99 | yes |
| 0.85 | 4.0 | 0.99 | yes |
| 0.90 | 1.0 | — | no |
| 0.90 | 2.0 | — | no |
| 0.90 | 4.0 | 0.99 | yes |

## 4. Headline cross-check

At L0-07's launch-cadence floor of 1 / yr and per-mission p = 0.80 (the user's Option B/C target):

- Reading (a) slot-met fraction: 0.800 (clears 0.80 target ? **yes**; clears 0.95 ? **NO**)
- Reading (b) window-has-delivery: 0.551 (clears 0.80 ? **NO**; clears 0.95 ? **NO**)
- Reading (c) queue depth: 11.2 (clears 1.0 ? yes)
- L0-10 block-5 at threshold 0.80: 0.737 (clears 0.95 ? **NO**)

At L0-07 cadence and p = 0.80, reading (a) of L0-09 fails — only 80 % of yearly slots met, well below 0.95 — but it does clear a *relaxed* L0-09 target at 0.80. Reading (b) fails badly (0.551 << 0.95). Reading (c) is trivially satisfied. L0-10 block-5 at threshold 0.80 also fails (0.737 << 0.95), meaning the per-mission p that clears the rolling-5 form of L0-10 = 0.80 is much higher than 0.80 itself.