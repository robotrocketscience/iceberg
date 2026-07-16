"""Pull JPL Horizons state vectors for the six tour-relevant Saturnian moons
across the 2032-2050 demonstrator window.

Purpose (R-saturn-moon-ga-ephemeris):
  - verify orbital radii / velocities against the IAU/JPL standard constants in STUDY.md
  - confirm gravity-assist leverage is epoch-invariant (H7)
  - sample inter-moon phasing (true longitudes at common epochs) for sequencing feasibility

Output: results/horizons_moon_states.json

Saturn-centred ecliptic state vectors (VEC_TABLE=2). Center = Saturn body center 500@699.
"""
from __future__ import annotations

import json
import math
import re
import sys
import time
from pathlib import Path

import requests

HORIZONS = "https://ssd.jpl.nasa.gov/api/horizons.api"

# Horizons body IDs for the Saturnian moons (NAIFs 6xx)
MOONS = {
    "Mimas": "601",
    "Enceladus": "602",
    "Tethys": "603",
    "Dione": "604",
    "Rhea": "605",
    "Titan": "606",
}

# Sample epochs spanning the 2032-2050 demonstrator window.
EPOCHS = [
    "2032-01-01",
    "2036-01-01",
    "2040-01-01",
    "2044-01-01",
    "2048-01-01",
    "2050-01-01",
]


def pull_state(body_id: str, start: str) -> dict:
    """One-step VECTORS query; returns Saturn-centred ecliptic state vector (km, km/s)."""
    # stop = start + 1 day so Horizons accepts the interval; we read only the first row.
    yyyy, mm, dd = (int(x) for x in start.split("-"))
    stop = f"{yyyy}-{mm:02d}-{dd+1:02d}" if dd < 28 else f"{yyyy}-{mm:02d}-{dd}"
    params = {
        "format": "text",
        "COMMAND": f"'{body_id}'",
        "OBJ_DATA": "'NO'",
        "MAKE_EPHEM": "'YES'",
        "EPHEM_TYPE": "'VECTORS'",
        "CENTER": "'500@699'",  # Saturn body center
        "REF_PLANE": "'ECLIPTIC'",
        "START_TIME": f"'{start}'",
        "STOP_TIME": f"'{stop}'",
        "STEP_SIZE": "'1 d'",
        "VEC_TABLE": "'2'",      # position + velocity
        "OUT_UNITS": "'KM-S'",
    }
    r = requests.get(HORIZONS, params=params, timeout=60)
    r.raise_for_status()
    text = r.text
    m = re.search(r"\$\$SOE(.*?)\$\$EOE", text, re.DOTALL)
    if not m:
        raise RuntimeError(f"no SOE/EOE block for body {body_id} at {start}:\n{text[:500]}")
    block = m.group(1)
    # VEC_TABLE=2 layout: lines 'X = ... Y = ... Z = ...' then 'VX= ... VY= ... VZ= ...'
    def grab(label):
        mm = re.search(rf"{label}\s*=\s*([-+0-9.Ee]+)", block)
        if not mm:
            raise RuntimeError(f"missing {label} in block:\n{block[:400]}")
        return float(mm.group(1))

    x, y, z = grab("X"), grab("Y"), grab("Z")
    vx, vy, vz = grab("VX"), grab("VY"), grab("VZ")
    r_km = math.sqrt(x * x + y * y + z * z)
    v_kms = math.sqrt(vx * vx + vy * vy + vz * vz)
    lon_deg = math.degrees(math.atan2(y, x)) % 360.0
    return {
        "pos_km": [x, y, z],
        "vel_kms": [vx, vy, vz],
        "r_km": r_km,
        "v_kms": v_kms,
        "true_lon_deg": lon_deg,
    }


def main() -> int:
    out = {"center": "Saturn body center (500@699)", "frame": "ecliptic",
           "units": "KM-S", "epochs": EPOCHS, "moons": {}}
    for name, bid in MOONS.items():
        out["moons"][name] = {}
        for epoch in EPOCHS:
            for attempt in range(3):
                try:
                    out["moons"][name][epoch] = pull_state(bid, epoch)
                    print(f"  {name:10s} {epoch}: r={out['moons'][name][epoch]['r_km']:.0f} km  "
                          f"v={out['moons'][name][epoch]['v_kms']:.4f} km/s  "
                          f"lon={out['moons'][name][epoch]['true_lon_deg']:.1f} deg")
                    break
                except Exception as e:  # transient API hiccup → retry
                    print(f"  retry {name} {epoch} ({attempt}): {e}", file=sys.stderr)
                    time.sleep(2)
            else:
                raise SystemExit(f"failed to pull {name} {epoch} after retries")
            time.sleep(0.4)  # be polite to the API

    results = Path(__file__).parent / "results"
    results.mkdir(exist_ok=True)
    (results / "horizons_moon_states.json").write_text(json.dumps(out, indent=2))
    print(f"\nwrote {results/'horizons_moon_states.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
