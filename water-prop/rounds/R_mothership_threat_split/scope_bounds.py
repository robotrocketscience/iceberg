#!/usr/bin/env python3
"""Pre-script: R-mothership-threat-split bounds.

R185 modeled every damaging handoff failure as "chunk lost, mission
continues," and flagged the gap: "mothership-threatening subsets
unmodeled." This round splits the damaging fraction into chunk-only vs
mothership-threatening, prices the catastrophic tail, and surfaces a
retry tension R185's fixed 3-attempt policy hid.

The mothership is the single asset that carries the reactor, all N
chunks aboard, and the return capability. Its loss is total mission
loss, not a chunk write-off. R185 (correctly for its scope) folded that
event into "chunk loss," slightly UNDER-counting consequence.

Stage-weighted threat (the physical refinement over a flat phi_ms):
damaging failures are distributed across the five handoff stages in
proportion to each stage's failure probability; each stage carries a
DIFFERENT conditional probability that its damaging failure threatens
the mothership (a berth-contact RUD of a 40 t bag is far more
mothership-threatening than a far-rendezvous abort). Because the
riskiest stage (berth_bag: highest failure prob) is ALSO the highest-
threat stage, the correlation pushes phi_ms above a naive flat guess.

Conditional mothership-threat given a damaging failure at each stage
(desk anchors, swept in run.py):
  rendezvous  0.00   (far; abort clean)
  proxops     0.05   (approaching, abort-capable)
  berth_bag   0.35   (40 t non-rigid load in contact — the driver)
  mate        0.25   (structural load-path failure at the dock)
  sep         0.15   (recontact risk)
Swap (rigid 6 t module) threat set lower per stage (0.6x); one per
mission.

The retry tension: each retry of a berth is another close approach =
another roll against the mothership. R185 found retries load-bearing
for chunk retention; here they also ACCUMULATE mothership exposure.
Mission EV = retention x P(mothership survives) has an interior optimum
in try-count once phi_ms and f_dmg are high enough.
"""
STAGES = {"rendezvous": (0.985, 0.99, 0.995), "proxops": (0.95, 0.97, 0.99),
          "berth_bag": (0.88, 0.92, 0.95), "mate": (0.95, 0.97, 0.99),
          "sep": (0.985, 0.99, 0.995)}
THREAT = {"rendezvous": 0.00, "proxops": 0.05, "berth_bag": 0.35,
          "mate": 0.25, "sep": 0.15}
SWAP_BERTH = (0.92, 0.95, 0.97)
SWAP_THREAT_SCALE = 0.6
OPS_LPD = 0.453           # R185 ops-honest steady state
MONO_LPD = 1.02
DELAY = 10.4


def chain(idx, berth=None):
    p = 1.0
    for k, v in STAGES.items():
        p *= (berth[idx] if (berth and k == "berth_bag") else v[idx])
    return p


def phi_ms(idx, threat=THREAT):
    """Stage-weighted fraction of damaging failures that threaten the
    mothership, at band idx."""
    num = den = 0.0
    for k, v in STAGES.items():
        fail = 1.0 - v[idx]
        num += fail * threat[k]
        den += fail
    return num / den


def retry(p_att, f_dmg, tries):
    b = (1.0 - p_att) * (1.0 - f_dmg)
    d = (1.0 - p_att) * f_dmg
    succ = sum(p_att * b ** k for k in range(tries))
    dmg = sum(d * b ** k for k in range(tries))
    return succ, dmg


# --- H1: phi_ms from stage decomposition ---
print("== H1: mothership-threat fraction of damaging failures ==")
for idx, tag in ((0, "low"), (1, "central"), (2, "high")):
    print(f"  {tag}: phi_ms = {phi_ms(idx):.2f} "
          f"(berth_bag drives it: fail {1-STAGES['berth_bag'][idx]:.2f} "
          f"x threat {THREAT['berth_bag']:.2f})")

# --- H2: central consequence ---
print("\n== H2: central mission-total-loss and its economics ==")
idx = 1
phic = phi_ms(idx)
p_hf = chain(idx)
_, dmg_hf = retry(p_hf, 0.10, 3)
p_sw = chain(idx, SWAP_BERTH)
_, dmg_sw = retry(p_sw, 0.10, 3)
phi_sw = phi_ms(idx, {k: v * SWAP_THREAT_SCALE for k, v in THREAT.items()})
m_hf = dmg_hf * phic
m_sw = dmg_sw * phi_sw
p_survive = (1 - m_hf) ** 4 * (1 - m_sw)
p_loss = 1 - p_survive
risk_lpd = OPS_LPD / p_survive
print(f"  dmg/handoff {dmg_hf:.4f} x phi_ms {phic:.2f} = mothership-loss/"
      f"handoff {m_hf:.4f}")
print(f"  N=4 + swap: P(survive) {p_survive:.3f}, P(total loss) "
      f"{p_loss*100:.1f}%")
print(f"  risk-adjusted lpd {OPS_LPD:.3f} -> {risk_lpd:.3f} "
      f"(a tail-risk line, small at central)")

# --- H3: the tail ---
print("\n== H3: the catastrophic tail (stress corner) ==")
idxh = 0                       # low band = worst stage probs
phih = phi_ms(idxh, {k: v * 1.3 for k, v in THREAT.items()})  # +30% threat
phih = min(phih, 0.40)
p_hf_s = chain(idxh)
_, dmg_s = retry(p_hf_s, 0.20, 3)
m_s = dmg_s * phih
p_surv_s = (1 - m_s) ** 5 * (1 - m_sw)
print(f"  f_dmg 20%, phi_ms {phih:.2f}, N=5: dmg/handoff {dmg_s:.4f} -> "
      f"mothership-loss/handoff {m_s:.4f}")
print(f"  P(total loss) {(1-p_surv_s)*100:.1f}% — a program-defining "
      f"single-point catastrophic risk")
print(f"  risk-adjusted lpd -> {OPS_LPD/p_surv_s:.3f}")

# --- H4: the retry tension does NOT bind (opposite of the naive worry) ---
print("\n== H4: is the retry policy mothership-safe? ==")
for corner, (ci, fd, ph) in (("central", (1, 0.10, phic)),
                             ("stress", (idxh, 0.20, phih))):
    p_att = chain(ci)
    best_t, best_ev = 0, -1.0
    for tries in (1, 2, 3, 4, 5, 6):
        succ, dmg = retry(p_att, fd, tries)
        ev = succ ** 4 * (1 - dmg * ph) ** 4        # catastrophic-weighted EV
        if ev > best_ev:
            best_ev, best_t = ev, tries
    # marginal ratio of the 3rd retry: retention gain vs ms-exposure gain
    s2, d2 = retry(p_att, fd, 2)
    s3, d3 = retry(p_att, fd, 3)
    ratio = (s3 - s2) / max((d3 - d2) * ph, 1e-9)
    print(f"  {corner}: EV-optimal tries = {best_t} (>=3 => safe); "
          f"3rd-retry retention:ms-exposure = {ratio:.0f}:1")

print("\n== the tail is N-driven, not retry-driven ==")
for n in (1, 2, 3, 4, 5, 6):
    surv = (1 - m_hf) ** n * (1 - m_sw)
    print(f"  N={n}: P(total loss) central {(1-surv)*100:.1f}%")

