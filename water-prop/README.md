# water-prop

Water propulsion R&D for **Project ICEBERG** (Robot Rocket Science). Greenfield analysis of water-based electric propulsion options — resistojet, MET, ion, Hall, electrolyze→H₂-electric — for a Saturn-class water-haul mission.

## Layout

```
water-prop/
├── pyproject.toml              # uv-managed, deps: cantera, numpy, matplotlib, scipy
├── src/waterprop/              # reusable physics models (installable as `waterprop`)
│   ├── constants.py            # G0, AU, GM_*, unit conversions
│   ├── thermo/                 # Cantera-backed nozzle expansion
│   ├── trajectory/             # (future) poliastro low-thrust
│   ├── lifetime/               # (future) sputter / erosion models
│   └── storage/                # (future) H2 tank thermal
├── studies/                    # paper studies — one dir per question
│   ├── README.md               # study index
│   └── SNN_short_name/
│       ├── STUDY.md            # question, method, findings, decisions
│       ├── run.py              # runner; imports from waterprop
│       └── results/            # figures, CSVs
├── tests/                      # sanity tests on physics models
└── docs/                       # round-by-round writeups
    ├── R1-landscape.md
    └── R2-deepdive.md
```

## Running studies

```bash
uv sync                                                    # one-time, installs waterprop in editable mode
uv run python studies/S01_met_frozen_flow/run.py           # reproduce S01
uv run pytest tests/                                       # run sanity tests
```

## Conventions

- **Physics models** under `src/waterprop/` are pure functions: no I/O, no plotting, no `print`. Tested.
- **Study runners** under `studies/SNN_*/` own CLI, sweeps, plotting, and output paths. They import models from `waterprop`.
- **STUDY.md** in each study captures *question → method → validity caveats → findings → decisions → open follow-ups*. The round writeup (`docs/RN-*.md`) synthesizes across studies; it doesn't repeat methodology.
- **Atomic commits**: one logical change per commit; conventional-commits prefix (`feat:`, `exp:`, `docs:`, etc.) — see top-level `CLAUDE.md`.
- **No large data files in git** — `.gitignore` excludes `.npz`, `.h5`, `.parquet`. PNG figures are kept for the paper trail.

## Project context

- ICEBERG mission profile: 50 t Saturnian B-ring water chunk hauled to LEO in ~13.5 yr round trip. See `../ICEBERG-conops.md`, `../ICEBERG-pitch.md`.
- This R&D is **greenfield** — RRS is not bound to any external company's propulsion stack. Pale Blue, Tethers Unlimited, Penn State MET work are referenced as open-literature data points only.
