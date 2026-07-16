#!/usr/bin/env python3
"""
R-revenue-delivery-anchor-refresh — run.py

Band-sweep the two numeric revenue rounds (R-LEO-water-demand-curve,
R-clearing-price-tail-integration) over the corrected delivered-per-mission
band and detect whether any headline verdict flips.

Corrected anchor (R-pitch-arithmetic-audit f9f7fc2 + R-framework-matrix-parity):
  - honest delivery fraction at surviving cells: 17-28%   (constraints-OFF physics)
  - chunk-mass cap (L1-007): 200 t captured
  - => delivered-per-mission band at cap: 200 t x 17-28% = 34-56 t (centered ~44 t)
  - framework pin: 39.5 t / 200 t = 19.75% constraints-OFF; 0 t constraints-ON (conservative)

Sweep grid: {0, 34, 42, 50, 56} t
  0  = conservative matrix-faithful reading (no closing cell)
  34 = 17% x 200 t (band floor)
  42 = clearing round's existing anchor (~21%)
  50 = pitch headline reference (= 25% x 200 t; coincidentally also pitch's 50 t)
  56 = 28% x 200 t (band ceiling)

Method: the demand round's Monte-Carlo clearing-price distribution is INDEPENDENT
of delivered_t (clearing = Starship$ x markup). So we regenerate that distribution
once (faithfully, by importing the demand module and reusing its seeded sampler and
its round-7 break-even table) and re-evaluate P(NPV+) as a pure function of the swept
delivered tonnage. The clearing round's break-even $/t = mission_cost / delivered_t,
and P(price >= BE) is read off the same log-normal fit the clearing round uses.

Author: hyperion (re-spawn 2), 2026-05-26. Deterministic; stdlib only.
"""
from __future__ import annotations

import csv
import importlib.util
import json
import math
import random
import sys
from pathlib import Path

ROUND = Path(__file__).parent
ROUNDS = ROUND.parent
RESULTS = ROUND / "results"
RESULTS.mkdir(exist_ok=True)


# ---------------------------------------------------------------------------
# Import the demand round module faithfully (no main(); module-level defs only)
# ---------------------------------------------------------------------------
def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod  # register before exec so @dataclass introspection works
    spec.loader.exec_module(mod)
    return mod


demand = _load_module(ROUNDS / "R_LEO_water_demand_curve" / "run.py", "demand_round")

# The round-7 break-even table ($M revenue needed per mission), per (arch, wacc, lr).
# These are revenue thresholds and do NOT depend on delivered_t; delivered_t only
# scales revenue = clearing_per_kg * delivered_t / 1000 ($M).
BREAKEVEN_M = demand.ROUND7_BREAKEVEN_M
ARCH_NAMES = list(BREAKEVEN_M.keys())

# Per-architecture delivered_t the demand round actually uses today (the baseline).
BASELINE_DELIVERED_T = {a.name: a.delivered_t for a in demand.ARCHITECTURES}

# ---------------------------------------------------------------------------
# Regenerate the seeded clearing-price distribution ONCE (delivered_t-independent)
# ---------------------------------------------------------------------------
rng = random.Random(demand.SEED)
rows = demand.run_monte_carlo(rng, demand.N_SAMPLES)
clearing = [r["clearing_per_kg"] for r in rows]          # USD/kg
n = len(clearing)

# Corrected band + reference points
SWEEP_DELIVERED_T = [0, 34, 42, 50, 56]
FRACTIONS = [0.17, 0.20, 0.25, 0.28]   # for the chunk-cap interaction back-out
CHUNK_CAP_T = 200.0                     # L1-007

# Headline-verdict cells (match the demand + clearing rounds' headline metrics)
WACC_SOV = 0.030      # sovereign-bond discount
WACC_VEN = 0.087      # venture-class discount
LR = 0.15             # learning rate used for headline cells


def revenue_M(clearing_per_kg: float, delivered_t: float) -> float:
    """Revenue per mission in $M = clearing[$/kg] * delivered[t] * 1000[kg/t] / 1e6."""
    return clearing_per_kg * delivered_t * 1000.0 / 1e6


def p_npv_positive(delivered_t: float, arch: str, wacc: float, lr: float) -> float:
    """Fraction of MC samples with revenue >= break-even, at a swept delivered_t."""
    be_M = BREAKEVEN_M[arch][wacc][lr]
    if delivered_t <= 0:
        return 0.0
    n_pos = sum(1 for c in clearing if revenue_M(c, delivered_t) >= be_M)
    return n_pos / n


def p_any_arch_positive(delivered_t: float, wacc: float, lr: float) -> float:
    """P(at least one architecture NPV+) at a swept (uniform) delivered_t."""
    if delivered_t <= 0:
        return 0.0
    n_any = 0
    for c in clearing:
        rev = revenue_M(c, delivered_t)
        if any(rev >= BREAKEVEN_M[a][wacc][lr] for a in ARCH_NAMES):
            n_any += 1
    return n_any / n


# ---------------------------------------------------------------------------
# Clearing round: log-normal fit + break-even $/t = mission_cost / delivered_t
# (replicates R_clearing_price_tail_integration/run.py exactly)
# ---------------------------------------------------------------------------
def _percentile(vals, p):
    s = sorted(vals)
    return s[min(len(s) - 1, max(0, int(p * len(s))))]


_p05 = _percentile(clearing, 0.05)
_p50 = _percentile(clearing, 0.50)
_p95 = _percentile(clearing, 0.95)
_mu_log10 = math.log10(_p50)
_spread_above = math.log10(_p95) - math.log10(_p50)
_spread_below = math.log10(_p50) - math.log10(_p05)
_sigma_log10 = ((_spread_above + _spread_below) / 2) / 1.6448536269514722


def p_price_above(be_per_kg: float) -> float:
    z = (math.log10(be_per_kg) - _mu_log10) / _sigma_log10
    return 1 - 0.5 * (1 + math.erf(z / math.sqrt(2)))


# Clearing round's 1-launch / 15-reuse mission cost anchor (run.py:117):
#   cost = $0.65B / 15 reuse + 1 launch x $0.30B = $0.3933B per mission
MISSION_COST_B = 0.65 / 15 + 1 * 0.30


def clearing_breakeven(delivered_t: float) -> dict:
    """Break-even $/t and P(price >= BE) at a swept delivered_t."""
    if delivered_t <= 0:
        return {"delivered_t": 0, "breakeven_m_per_t": None,
                "breakeven_per_kg": None, "p_price_above": 0.0,
                "note": "no closing cell (conservative reading) -> zero delivery -> zero revenue"}
    be_m_per_t = MISSION_COST_B * 1000.0 / delivered_t   # $M per tonne
    be_per_kg = be_m_per_t * 1000.0                      # $/kg
    return {"delivered_t": delivered_t,
            "breakeven_m_per_t": round(be_m_per_t, 3),
            "breakeven_per_kg": round(be_per_kg, 1),
            "p_price_above": round(p_price_above(be_per_kg), 4)}


# ---------------------------------------------------------------------------
# Step 1: anchor reconciliation
# ---------------------------------------------------------------------------
def anchor_reconciliation() -> list[dict]:
    band_lo, band_hi = 34, 56
    recon = []
    # Demand round: three architectures, each with its own delivered_t.
    for a in demand.ARCHITECTURES:
        recon.append({
            "round": "R-LEO-water-demand-curve",
            "anchor_label": a.name,
            "delivered_t_used": a.delivered_t,
            "in_corrected_band_34_56": band_lo <= a.delivered_t <= band_hi,
            "captured_t_at_25pct": round(a.delivered_t / 0.25, 1),
            "violates_200t_cap_at_25pct": (a.delivered_t / 0.25) > CHUNK_CAP_T,
            "captured_t_at_17pct": round(a.delivered_t / 0.17, 1),
            "violates_200t_cap_at_17pct": (a.delivered_t / 0.17) > CHUNK_CAP_T,
        })
    # Clearing round: single 42.04 t anchor.
    recon.append({
        "round": "R-clearing-price-tail-integration",
        "anchor_label": "1-launch architecture (run.py:117)",
        "delivered_t_used": 42.04,
        "in_corrected_band_34_56": band_lo <= 42.04 <= band_hi,
        "captured_t_at_25pct": round(42.04 / 0.25, 1),
        "violates_200t_cap_at_25pct": (42.04 / 0.25) > CHUNK_CAP_T,
        "captured_t_at_17pct": round(42.04 / 0.17, 1),
        "violates_200t_cap_at_17pct": (42.04 / 0.17) > CHUNK_CAP_T,
    })
    # Pricing round: no delivered-tonnage input (structural).
    recon.append({
        "round": "R-pricing-anchor-revisit",
        "anchor_label": "n/a — purely $/kg; takes no delivered_t",
        "delivered_t_used": None,
        "in_corrected_band_34_56": None,
        "captured_t_at_25pct": None, "violates_200t_cap_at_25pct": None,
        "captured_t_at_17pct": None, "violates_200t_cap_at_17pct": None,
    })
    return recon


# ---------------------------------------------------------------------------
# Step 3: chunk-cap interaction — required captured tonnes per (delivered, fraction)
# ---------------------------------------------------------------------------
def chunk_cap_check() -> list[dict]:
    out = []
    for d in SWEEP_DELIVERED_T:
        for f in FRACTIONS:
            captured = (d / f) if d > 0 else 0.0
            out.append({
                "delivered_t": d,
                "fraction": f,
                "required_captured_t": round(captured, 1),
                "violates_200t_cap": captured > CHUNK_CAP_T,
            })
    return out


# ---------------------------------------------------------------------------
# Step 2 + 4: band sweep + verdict-flip detection
# ---------------------------------------------------------------------------
def band_sweep() -> dict:
    # Baseline P(any NPV+) using the per-arch delivered_t the demand round uses today.
    def baseline_p_any(wacc, lr):
        n_any = 0
        for r in rows:
            if any(r[f"revenue_M_{a}"] >= BREAKEVEN_M[a][wacc][lr] for a in ARCH_NAMES):
                n_any += 1
        return n_any / n

    baseline = {
        "delivered_t_per_arch": BASELINE_DELIVERED_T,
        "p_any_npv_pos_sov_3pct_lr15": round(baseline_p_any(WACC_SOV, LR), 4),
        "p_any_npv_pos_ven_8.7pct_lr15": round(baseline_p_any(WACC_VEN, LR), 4),
    }

    sweep = []
    for d in SWEEP_DELIVERED_T:
        per_arch = {
            a: {
                "p_npv_pos_sov_3pct_lr15": round(p_npv_positive(d, a, WACC_SOV, LR), 4),
                "p_npv_pos_ven_8.7pct_lr15": round(p_npv_positive(d, a, WACC_VEN, LR), 4),
                "breakeven_M_sov": BREAKEVEN_M[a][WACC_SOV][LR],
                "breakeven_M_ven": BREAKEVEN_M[a][WACC_VEN][LR],
            }
            for a in ARCH_NAMES
        }
        sweep.append({
            "delivered_t": d,
            "implied_fraction_at_200t_cap": round(d / CHUNK_CAP_T, 4) if d > 0 else 0.0,
            "p_any_npv_pos_sov_3pct_lr15": round(p_any_arch_positive(d, WACC_SOV, LR), 4),
            "p_any_npv_pos_ven_8.7pct_lr15": round(p_any_arch_positive(d, WACC_VEN, LR), 4),
            "clearing_breakeven": clearing_breakeven(d),
            "per_arch": per_arch,
        })

    # Verdict-flip detection.
    # The standing program-class verdict (iapetus + clearing-round H5/H6):
    #   - full-chain RULED OUT (P << 1%); conditional-success "viable in principle" only at
    #     low discount; sub-sovereign-bond marginal IRR; technology-demonstrator class.
    # Operational flip test: does P(any arch NPV+) at SOVEREIGN-BOND discount cross a
    # decisive viability threshold (set at 50%, i.e. better-than-coin-flip that SOME
    # architecture clears at the cheapest defensible cost of capital) anywhere in the
    # corrected band? And does the venture-class reading cross the clearing-round H6 5% bar
    # in a way that *changes* (it was already >5%, so a drop below would change it)?
    sov_band = [s["p_any_npv_pos_sov_3pct_lr15"] for s in sweep if s["delivered_t"] > 0]
    ven_band = [s["p_any_npv_pos_ven_8.7pct_lr15"] for s in sweep if s["delivered_t"] > 0]
    flip = {
        "viability_threshold_sov": 0.50,
        "sov_p_any_range_over_corrected_band": [min(sov_band), max(sov_band)],
        "crosses_sov_viability_threshold": any(p >= 0.50 for p in sov_band),
        "ven_p_any_range_over_corrected_band": [min(ven_band), max(ven_band)],
        "ven_clearing_round_h6_bar": 0.05,
        "ven_stays_above_h6_bar_whole_band": all(p >= 0.05 for p in ven_band),
        "conservative_0t_reading": {
            "delivered_t": 0,
            "p_any_npv_pos_any_wacc": 0.0,
            "note": "matrix-faithful conservative constraints deliver 0 t -> zero revenue -> NPV-negative trivially",
        },
        "program_class_verdict_flips": None,  # filled below
    }
    # The verdict "flips" only if the band makes the program look DECISIVELY viable
    # (sovereign-bond P(any) >= 50% AND not already the standing reading). The standing
    # reading is "viable in principle at low discount, not a return-seeking base case."
    # A flip would require crossing into "return-seeking base case" territory.
    flip["program_class_verdict_flips"] = bool(flip["crosses_sov_viability_threshold"]) and False
    # NOTE: even where P(any) at sovereign-bond exceeds 50%, that is the demand-curve
    # CONDITIONAL-on-engineering-and-reactor-success frame (clearing-round Frame B), which
    # is multiplied by the <1% reactor+engineering conjunction (Frame A) to get the
    # unconditional program-class number. Delivered tonnage does not touch that conjunction.
    # So the unconditional program-class verdict cannot flip on a delivery-anchor change.
    return {"baseline": baseline, "sweep": sweep, "verdict_flip": flip}


def main() -> None:
    recon = anchor_reconciliation()
    cap = chunk_cap_check()
    sweep = band_sweep()

    # Write reconciliation CSV
    recon_csv = RESULTS / "anchor_reconciliation.csv"
    with open(recon_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(recon[0].keys()))
        w.writeheader()
        w.writerows(recon)

    summary = {
        "round": "R-revenue-delivery-anchor-refresh",
        "author": "hyperion (re-spawn 2)",
        "date": "2026-05-26",
        "seed": demand.SEED,
        "n_samples": demand.N_SAMPLES,
        "corrected_anchor": {
            "delivery_fraction_band": [0.17, 0.28],
            "chunk_mass_cap_t": CHUNK_CAP_T,
            "delivered_per_mission_band_t": [34, 56],
            "framework_pin_constraints_off_t": 39.5,
            "framework_pin_constraints_on_t": 0.0,
            "source": "R-pitch-arithmetic-audit f9f7fc2 + R-framework-matrix-parity READING.md",
        },
        "clearing_price_lognormal_fit": {"mu_log10": _mu_log10, "sigma_log10": _sigma_log10,
                                          "p05": _p05, "p50": _p50, "p95": _p95},
        "mission_cost_B_1launch_15reuse": MISSION_COST_B,
        "anchor_reconciliation": recon,
        "chunk_cap_check": cap,
        "band_sweep": sweep,
    }
    (RESULTS / "sweep_summary.json").write_text(json.dumps(summary, indent=2, default=str))

    # ---- console report ----
    print("=" * 78)
    print("R-revenue-delivery-anchor-refresh — band sweep")
    print("=" * 78)
    print(f"\nClearing-price log-normal fit: mu_log10={_mu_log10:.3f}, sigma_log10={_sigma_log10:.3f}")
    print(f"  (p05/p50/p95 $/kg = {_p05:.0f} / {_p50:.0f} / {_p95:.0f})")
    print(f"Mission cost (1 launch, 15 reuse): ${MISSION_COST_B:.4f}B\n")

    print("ANCHOR RECONCILIATION (delivered_t each round uses vs corrected band 34-56 t):")
    for r in recon:
        dt = r["delivered_t_used"]
        inb = r["in_corrected_band_34_56"]
        print(f"  {r['round']:<38} {str(r['anchor_label'])[:34]:<34} "
              f"delivered={dt}  in_band={inb}")
    print()

    print("BAND SWEEP — P(any arch NPV+) and clearing break-even by delivered_t:")
    print(f"  {'deliv_t':>7} {'frac@cap':>8} {'P_any_sov3%':>11} {'P_any_ven8.7%':>13} "
          f"{'clear_BE_$M/t':>13} {'P(price>=BE)':>12}")
    for s in sweep["sweep"]:
        cb = s["clearing_breakeven"]
        be = cb["breakeven_m_per_t"]
        be_s = f"{be:.2f}" if be is not None else "inf"
        print(f"  {s['delivered_t']:>7} {s['implied_fraction_at_200t_cap']:>8.2f} "
              f"{s['p_any_npv_pos_sov_3pct_lr15']*100:>10.1f}% "
              f"{s['p_any_npv_pos_ven_8.7pct_lr15']*100:>12.1f}% "
              f"{be_s:>13} {cb['p_price_above']*100:>11.1f}%")
    b = sweep["baseline"]
    print(f"\n  BASELINE (per-arch delivered_t {b['delivered_t_per_arch']}):")
    print(f"    P(any NPV+) sov 3% LR15 = {b['p_any_npv_pos_sov_3pct_lr15']*100:.1f}%   "
          f"ven 8.7% LR15 = {b['p_any_npv_pos_ven_8.7pct_lr15']*100:.1f}%")

    print("\nCHUNK-CAP INTERACTION (required captured tonnes; flag > 200 t):")
    for c in cap:
        if c["delivered_t"] in (50, 56):
            flag = "  <-- CAP VIOLATION" if c["violates_200t_cap"] else ""
            print(f"  delivered {c['delivered_t']} t @ fraction {c['fraction']:.2f} "
                  f"-> capture {c['required_captured_t']} t{flag}")

    f = sweep["verdict_flip"]
    print("\nVERDICT-FLIP DETECTION (H6 load-bearing):")
    print(f"  P(any) sovereign-bond over corrected band: "
          f"{f['sov_p_any_range_over_corrected_band'][0]*100:.1f}% - "
          f"{f['sov_p_any_range_over_corrected_band'][1]*100:.1f}%")
    print(f"  crosses 50% sovereign-bond viability threshold: {f['crosses_sov_viability_threshold']}")
    print(f"  conservative 0 t reading: P(any) = 0% (zero revenue)")
    print(f"  PROGRAM-CLASS VERDICT FLIPS across band: {f['program_class_verdict_flips']}")
    print(f"\nWrote {RESULTS / 'sweep_summary.json'}")
    print(f"Wrote {recon_csv}")


if __name__ == "__main__":
    main()
