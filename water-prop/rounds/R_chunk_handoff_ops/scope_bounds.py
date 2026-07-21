#!/usr/bin/env python3
"""Pre-script: R-chunk-handoff-ops bounds.

Decomposes the relay's two unprecedented in-space operations (R182 chunk
handoff; R184 reactor-module swap) in the campaign's engineering-
decomposition style (R_A14 lineage). All stage probabilities are
DESK-ANCHORED bands, not measurements — labeled [W]; the round's value is
the structure (retry-aware, failure-mode-split) and the bottleneck
ordering vs bet #1, not the absolute numbers.

Stage bands per chunk-handoff attempt (low/central/high), precedents:
  far rendezvous (Cassini-class nav)          0.985 / 0.99 / 0.995
  prox-ops, 44 t stack (ISS-VV class, 2x mass) 0.95 / 0.97 / 0.99
  berth bagged 40 t non-rigid load (novel;
    ISS arm 20 t rigid, MEV-1/2, OSAM)         0.88 / 0.92 / 0.95
  structural mate + load transfer               0.95 / 0.97 / 0.99
  separation                                    0.985 / 0.99 / 0.995
Failure split: benign (retryable) 90 %, damaging 10 % (swept 5-20 %).
Retry policy: up to 3 attempts. Reactor swap: rigid 6 t module — same
chain with berth band 0.92/0.95/0.97, one per mission.
"""
STAGES = {"rendezvous": (0.985, 0.99, 0.995), "proxops": (0.95, 0.97, 0.99),
          "berth_bag": (0.88, 0.92, 0.95), "mate": (0.95, 0.97, 0.99),
          "sep": (0.985, 0.99, 0.995)}
SWAP_BERTH = (0.92, 0.95, 0.97)


def chain(idx, berth=None):
    p = 1.0
    for k, v in STAGES.items():
        p *= (berth[idx] if (berth and k == "berth_bag") else v[idx])
    return p


def retry(p_att, f_dmg, tries=3):
    b = (1 - p_att) * (1 - f_dmg)
    d = (1 - p_att) * f_dmg
    succ = sum(p_att * b ** k for k in range(tries))
    dmg = sum(d * b ** k for k in range(tries))
    return succ, dmg


for i, tag in ((0, "low"), (1, "central"), (2, "high")):
    p = chain(i)
    s, d = retry(p, 0.10)
    print(f"handoff {tag}: per-attempt {p:.3f} -> eventual {s:.3f}, "
          f"damaging {d:.4f}")

p_c = chain(1)
s_c, d_c = retry(p_c, 0.10)
p_swap = chain(1, berth=SWAP_BERTH)
s_sw, d_sw = retry(p_swap, 0.10)
print(f"\nreactor swap central: per-attempt {p_swap:.3f} -> eventual "
      f"{s_sw:.3f}, damaging {d_sw:.4f}")

for n in (2, 4, 5):
    keep = s_c ** n * s_sw
    print(f"mission retention (N={n} handoffs + 1 swap): {keep:.3f}")

keep4 = s_c ** 4 * s_sw
print(f"\nrisk-adjusted steady lpd: 0.365 / {keep4:.3f} = {0.365/keep4:.3f}")
hw = (0.8 + 0.1 * 4 + 0.2) * 5.84 / 160
print(f"hardware penalty (arm 0.8 + fixtures 0.4 + swap i/f 0.2 t): "
      f"+{hw:.3f} lpd (~{hw/0.365:.0%})")
print("bet #1 capture-efficiency band for ordering: 0.46-0.85 per attempt")
