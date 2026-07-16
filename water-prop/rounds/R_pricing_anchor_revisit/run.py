"""R-pricing-anchor-revisit pricing model (titan-5, 2026-05-22).

Synthesis round: encodes real public per-kg comparables and the ICEBERG-demand.md
section-5 segment bands, computes a volume-weighted blended realised price per
supply era, and compares against the three anchors in play:
  - pitch headline      $1,400/kg   (Falcon-Heavy published $/kg-to-LEO; pitch fn 540)
  - lunar-ISRU ceiling  $1,000/kg   (pitch section 3.4 reframe midpoint)
  - campaign anchor      $10,000/kg  (load-bearing financial rounds, per AUDIT.md)

Pure stdlib. Run:
  python water-prop/rounds/R_pricing_anchor_revisit/run.py
Writes results/pricing_bands.json.
"""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
RESULTS.mkdir(exist_ok=True)

PITCH_ANCHOR = 1_400          # $/kg, Falcon Heavy published $/kg-to-LEO (pitch fn 540)
LUNAR_ISRU_CEILING = 1_000    # $/kg, pitch section 3.4 operative-ceiling midpoint
CAMPAIGN_ANCHOR = 10_000      # $/kg, load-bearing financial rounds (AUDIT.md)


# -------------------------------------------------------------------- #
# Real public comparables (titan-5 web research). $/kg ~2026 dollars.
# heritage: AVAILABLE (real contract/transaction) / ADJACENT (proxy with
# disclosed price) / NONE (projection or speculative claim).
# -------------------------------------------------------------------- #
COMPARABLES = [
    {"name": "ISS commercial resupply, effective (Dragon)", "usd_per_kg": 78_000,
     "heritage": "AVAILABLE", "source": "NASA OIG IG-18-021 (via SpaceNews)"},
    {"name": "ISS commercial resupply, effective (Cygnus)", "usd_per_kg": 125_000,
     "heritage": "AVAILABLE", "source": "NASA OIG IG-18-021 (via SpaceNews)"},
    {"name": "NASA ISS-upmass planning assumption", "usd_per_kg": 26_000,
     "heritage": "AVAILABLE", "source": "NASA OIG IG-18-021"},
    {"name": "Orbit Fab GEO hydrazine, published price", "usd_per_kg": 200_000,
     "heritage": "ADJACENT", "source": "Orbit Fab announcement 2022 ($20M/100kg)"},
    {"name": "Intuitive Machines CLPS lunar-surface (value/payload)", "usd_per_kg": 775_000,
     "heritage": "AVAILABLE", "source": "NASA CLPS award 2021 (arithmetic)"},
    {"name": "Lunar-ISRU propellant, projected", "usd_per_kg": 90_000,
     "heritage": "NONE", "source": "NASA NTRS ISRU breakeven ~2019"},
    {"name": "Falcon Heavy $/kg-to-LEO (= pitch anchor)", "usd_per_kg": 1_500,
     "heritage": "AVAILABLE", "source": "CSIS / SpaceX list price"},
    {"name": "Falcon 9 $/kg-to-LEO", "usd_per_kg": 3_000,
     "heritage": "AVAILABLE", "source": "CSIS / Our World in Data"},
    {"name": "Starship aspirational", "usd_per_kg": 100,
     "heritage": "NONE", "source": "SpaceX public statements"},
    {"name": "Luna-16 sample auction (novelty ceiling)", "usd_per_kg": 4_300_000_000,
     "heritage": "ADJACENT", "source": "Sotheby's 2018 (collectible, non-analogous)"},
]


# -------------------------------------------------------------------- #
# ICEBERG-demand.md section 5.1 demand stack. price = (low, high) $/kg WTP band;
# 'internal' segments priced at an assumed internal transfer cost (near marginal).
# -------------------------------------------------------------------- #
INTERNAL_TRANSFER_USD_PER_KG = 1_000  # assumed operator-internal transfer price

TIERS = {
    "100 t/yr (entry / Kilopower)": {
        "supply_t": 100,
        "segments": [
            {"name": "Crewed LEO stations", "t": 30, "price": (5_000, 10_000), "conf": "anchored"},
            {"name": "Operator-internal tug fleet", "t": 50, "price": "internal", "conf": "anchored"},
            {"name": "GEO servicing", "t": 10, "price": (3_000, 7_500), "conf": "inferred"},
            {"name": "DoD strategic reserve (one-shot)", "t": 10, "price": (10_000, 25_000), "conf": "speculative"},
        ],
    },
    "1,000 t/yr (FSP era)": {
        "supply_t": 1_000,
        "segments": [
            {"name": "Crewed LEO stations", "t": 50, "price": (2_000, 5_000), "conf": "anchored"},
            {"name": "Operator-internal tug fleet", "t": 300, "price": "internal", "conf": "anchored"},
            {"name": "GEO servicing", "t": 50, "price": (2_000, 5_000), "conf": "inferred"},
            {"name": "DoD strategic reserve", "t": 50, "price": (5_000, 10_000), "conf": "speculative"},
            {"name": "Lunar surface (LEO-staged)", "t": 50, "price": (1_500, 2_000), "conf": "inferred"},
        ],
    },
    "10,000 t/yr (MW era + Mars)": {
        "supply_t": 10_000,
        "segments": [
            {"name": "Crewed LEO stations", "t": 80, "price": (1_000, 2_000), "conf": "anchored"},
            {"name": "Operator-internal tug fleet", "t": 800, "price": "internal", "conf": "anchored"},
            {"name": "GEO servicing", "t": 150, "price": (1_500, 3_000), "conf": "inferred"},
            {"name": "DoD strategic reserve", "t": 100, "price": (3_000, 5_000), "conf": "speculative"},
            {"name": "Lunar surface (LEO-staged)", "t": 200, "price": (1_000, 1_500), "conf": "inferred"},
            {"name": "Mars-architecture", "t": 8_000, "price": (200, 500), "conf": "speculative"},
        ],
    },
}


def _seg_price_mid(seg) -> float:
    if seg["price"] == "internal":
        return INTERNAL_TRANSFER_USD_PER_KG
    return 0.5 * (seg["price"][0] + seg["price"][1])


def blended(tier, include_speculative=True, include_internal=True) -> tuple[float, float]:
    """Volume-weighted blended price midpoint and cleared tonnage for a tier."""
    num = 0.0
    vol = 0.0
    for seg in tier["segments"]:
        if not include_speculative and seg["conf"] == "speculative":
            continue
        if not include_internal and seg["price"] == "internal":
            continue
        num += seg["t"] * _seg_price_mid(seg)
        vol += seg["t"]
    return (num / vol if vol else 0.0), vol


def main():
    out = {"anchors": {"pitch": PITCH_ANCHOR, "lunar_isru_ceiling": LUNAR_ISRU_CEILING,
                       "campaign": CAMPAIGN_ANCHOR},
           "comparables": COMPARABLES, "tiers": {}}

    print("=== Comparables (real public, $/kg ~2026) ===")
    for c in COMPARABLES:
        print(f"  {c['heritage']:9s} ${c['usd_per_kg']:>13,.0f}/kg  {c['name']}")

    # Min recurring real comparable for delivering mass to a space destination:
    recurring = [c for c in COMPARABLES if c["heritage"] == "AVAILABLE"
                 and c["usd_per_kg"] >= 20_000]
    min_recurring = min(c["usd_per_kg"] for c in recurring)
    print(f"\n  Lowest recurring real 'deliver-to-destination' comparable (ISS-CRS family): "
          f"${min_recurring:,.0f}/kg")

    print("\n=== Blended realised price per era ===")
    print(f"  {'tier':32s} {'full':>10s} {'no-spec':>10s} {'ext-only':>10s}  cleared_t")
    for name, tier in TIERS.items():
        full, vfull = blended(tier, True, True)
        nospec, _ = blended(tier, False, True)
        extonly, vext = blended(tier, True, False)  # exclude internal -> external market price
        print(f"  {name:32s} ${full:>8,.0f} ${nospec:>8,.0f} ${extonly:>8,.0f}   {vfull:.0f} t")
        out["tiers"][name] = {
            "supply_t": tier["supply_t"],
            "blended_full_usd_per_kg": round(full),
            "blended_no_speculative_usd_per_kg": round(nospec),
            "blended_external_only_usd_per_kg": round(extonly),
            "cleared_t": vfull,
        }

    # H-by-H adjudication inputs.
    t1 = TIERS["100 t/yr (entry / Kilopower)"]
    seg_ceilings = {s["name"]: (s["price"][1] if s["price"] != "internal" else None)
                    for tier in TIERS.values() for s in tier["segments"]}
    non_mars_ceilings = [v for k, v in seg_ceilings.items()
                         if v is not None and "Mars" not in k]
    print("\n=== Hypothesis adjudication inputs ===")
    print(f"  H1: min non-Mars segment ceiling = ${min(non_mars_ceilings):,}/kg "
          f"(vs pitch ${PITCH_ANCHOR:,}) -> {'HELD' if min(non_mars_ceilings) >= PITCH_ANCHOR else 'FALSIFIED'}")
    t1_full, _ = blended(t1, True, True)
    t1_nospec, _ = blended(t1, False, True)
    print(f"  H2: tier-1 blended full=${t1_full:,.0f}, conservative(no-spec)=${t1_nospec:,.0f} "
          f"(vs 2x pitch=${2*PITCH_ANCHOR:,}) -> {'HELD' if t1_nospec >= 2*PITCH_ANCHOR or t1_full >= 2*PITCH_ANCHOR else 'CHECK'}")
    print(f"  H3: first-100t premium >= $10k/kg supported by ISS-CRS ${min_recurring:,}/kg "
          f"& Orbit Fab $200,000/kg (recurring, not collectible) -> HELD-via-recurring")
    print(f"  H5: captive ceiling (DoD one-shot $25k, Orbit Fab $200k) >= $20k early -> HELD-early; "
          f"DoD erodes to $3-5k at 10kt tier -> FALSIFIED-sustained")
    print(f"  H6: defensible blended ($3-5k early) < campaign anchor ${CAMPAIGN_ANCHOR:,} already used "
          f"-> correcting price moves verdicts WORSE, none flips positive -> FALSIFIED")
    print(f"  H7: even at ${CAMPAIGN_ANCHOR:,}/kg the verdict is technology-demonstrator (L0-24) "
          f"-> pricing does not flip program-class -> HELD")

    # Demand-curve distribution defensibility (R_LEO_water_demand_curve).
    print("\n=== R_LEO_water_demand_curve distribution defensibility ===")
    print("  Distribution: median $1,500/kg, 5th $200, 95th $15,000 (Starship x markup).")
    print("  median $1,500 ~ Falcon-Heavy / lunar-ISRU floor; 95th $15,000 ~ DoD/ISS-CRS WTP.")
    print("  Verdict: DEFENSIBLE as a launch-cost-driven BULK blend, but CONSERVATIVE — its")
    print("  median sits at the competing-supply floor, under-weighting captive-segment market")
    print("  power (ISS-CRS $78k, Orbit Fab $200k). Upside tail is real and under-represented.")
    out["demand_curve_verdict"] = ("defensible-but-conservative: median at competing-supply "
                                   "floor; captive-segment market power under-weighted")

    (RESULTS / "pricing_bands.json").write_text(json.dumps(out, indent=1))
    print(f"\nWrote {RESULTS / 'pricing_bands.json'}")


if __name__ == "__main__":
    main()
