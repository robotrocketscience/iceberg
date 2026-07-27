# bag_dynamics_6dof — coupled slosh + ACS Basilisk sim

R191's named 6-DOF follow-on: verify coupled attitude stability of a mothership
berthing a non-rigid 40 t bag (20 t sloshing) under reaction-wheel ACS.

## Run (on archon — the powerful box)

```bash
# from repo root, sync the sim up
rsync -az water-prop/sims/bag_dynamics_6dof/run_sim.py jso@archon:~/iceberg-sims/bag_dynamics_6dof/
# run the full grid (both seed modes, 64 cells, ~few min)
ssh jso@archon 'bash -lc "cd ~/iceberg-sims/bag_dynamics_6dof && ~/venvs/iceberg-basilisk-sims/bin/python run_sim.py"'
# pull the results back
rsync -az jso@archon:~/iceberg-sims/bag_dynamics_6dof/results/bag_6dof_findings.json water-prop/sims/bag_dynamics_6dof/results/
# render the figure locally (matplotlib only, no Basilisk)
python3 water-prop/sims/bag_dynamics_6dof/plot.py
```

Basilisk 2.10.2, venv `~/venvs/iceberg-basilisk-sims` on archon. Deterministic.
Note: archon's login shell is fish; wrap Python invocations in `bash -lc "..."`.
`unitTestSupport` pulls in pytest (absent) — avoid importing it.

## Outputs
- `results/bag_6dof_findings.json` — per-cell metrics + summary (both seed modes)
- `results/bag_6dof.png` — 3-panel figure
- `STUDY.md` — hypotheses (R191 H4), results, reading

## Headline
The berth *capture* injects ~5000 N·m·s of net angular momentum (20 t slosh ×
5 cm/s × 5 m arm) — ~17× the 3-wheel storage capacity. Reaction wheels store
momentum but cannot remove it, so every realistic-berth cell saturates and
tumbles; **momentum-dumping thrusters are mandatory**. R191's RW-viable corner
survives only for an idealized mean-zero slosh on the heavy monolithic host.
