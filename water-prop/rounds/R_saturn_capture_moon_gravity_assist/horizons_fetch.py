"""Fetch Saturnian moon state vectors from JPL Horizons.

Stdlib-only (urllib + json). Results cached to results/horizons/.
Re-run with --refresh to bypass the cache.
"""

from __future__ import annotations

import argparse
import json
import shutil
import ssl
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

HORIZONS_API = "https://ssd.jpl.nasa.gov/api/horizons.api"

MOONS = {
    "Mimas":     "601",
    "Enceladus": "602",
    "Tethys":    "603",
    "Dione":     "604",
    "Rhea":      "605",
    "Titan":     "606",
    "Hyperion":  "607",
    "Iapetus":   "608",
    "Phoebe":    "609",
}

CACHE_DIR = Path(__file__).parent / "results" / "horizons"


def fetch_vectors(target_id: str, epoch: str = "2045-01-01") -> dict:
    """Return one row of (x,y,z,vx,vy,vz) at the requested epoch in km, km/s.

    Reference frame: ICRF/J2000, center = Saturn system barycenter (500@6).
    """
    params = {
        "format":     "json",
        "COMMAND":    f"'{target_id}'",
        "OBJ_DATA":   "'NO'",
        "MAKE_EPHEM": "'YES'",
        "EPHEM_TYPE": "'VECTORS'",
        "CENTER":     "'500@6'",
        "START_TIME": f"'{epoch}'",
        "STOP_TIME":  f"'{epoch} 00:01'",
        "STEP_SIZE":  "'1m'",
        "REF_PLANE":  "'FRAME'",
        "OUT_UNITS":  "'KM-S'",
        "VEC_TABLE":  "'2'",
        "CSV_FORMAT": "'YES'",
    }
    query = urllib.parse.urlencode(params)
    url = f"{HORIZONS_API}?{query}"
    # macOS Python ships without the system CA chain; corporate proxies often
    # break the bundled certifi chain too. curl uses the system trust store,
    # which is what works reliably in this environment.
    if shutil.which("curl") is not None:
        proc = subprocess.run(
            ["curl", "-sS", "--fail", url],
            capture_output=True, text=True, timeout=60,
        )
        if proc.returncode != 0:
            raise RuntimeError(f"curl failed for {target_id}: {proc.stderr.strip()}")
        raw = proc.stdout
    else:
        with urllib.request.urlopen(url, timeout=60, context=ssl.create_default_context()) as r:
            raw = r.read().decode()
    payload = json.loads(raw)
    text = payload.get("result", "")
    soe = text.find("$$SOE")
    eoe = text.find("$$EOE")
    if soe < 0 or eoe < 0:
        raise RuntimeError(f"Horizons did not return a vector table for {target_id}:\n{text[:500]}")
    block = text[soe + 5:eoe].strip()
    first_row = [c.strip() for c in block.splitlines()[0].split(",")]
    jd_tdb = float(first_row[0])
    x, y, z = (float(first_row[2]), float(first_row[3]), float(first_row[4]))
    vx, vy, vz = (float(first_row[5]), float(first_row[6]), float(first_row[7]))
    r_km = (x*x + y*y + z*z) ** 0.5
    v_km_s = (vx*vx + vy*vy + vz*vz) ** 0.5
    return {
        "target_id": target_id,
        "epoch_utc": epoch,
        "jd_tdb": jd_tdb,
        "x_km": x, "y_km": y, "z_km": z,
        "vx_kms": vx, "vy_kms": vy, "vz_kms": vz,
        "r_km": r_km,
        "v_kms": v_km_s,
    }


def fetch_all(epoch: str = "2045-01-01", refresh: bool = False) -> dict:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    out = {}
    for name, body_id in MOONS.items():
        cache_path = CACHE_DIR / f"{name.lower()}_{epoch.replace('-', '')}.json"
        if cache_path.exists() and not refresh:
            out[name] = json.loads(cache_path.read_text())
            continue
        print(f"  pulling {name} (Horizons id {body_id}) at {epoch} ...", flush=True)
        try:
            data = fetch_vectors(body_id, epoch=epoch)
        except Exception as exc:  # network failure, server-side complaint, etc.
            print(f"    FAILED: {exc}", file=sys.stderr)
            continue
        cache_path.write_text(json.dumps(data, indent=2))
        out[name] = data
    return out


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--epoch", default="2045-01-01")
    p.add_argument("--refresh", action="store_true")
    args = p.parse_args()
    data = fetch_all(epoch=args.epoch, refresh=args.refresh)
    print(f"\nFetched {len(data)} moons at {args.epoch}:")
    print(f"  {'moon':<10s} {'r [km]':>14s} {'v [km/s]':>10s}")
    for name, d in data.items():
        print(f"  {name:<10s} {d['r_km']:>14,.0f} {d['v_kms']:>10.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
