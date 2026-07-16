# Studies — paper-study index

Each study is a self-contained, reproducible analysis answering one specific question. Layout:

```
studies/
└── SNN_short_name/
    ├── STUDY.md      # question, method, validity caveats, findings, decisions
    ├── run.py        # CLI runner, imports from src/waterprop/
    └── results/      # output figures and tables
```

To reproduce a study:
```
uv run python studies/SNN_short_name/run.py
```

## Index

| ID  | Question                                              | Round    | Status      |
|-----|-------------------------------------------------------|----------|-------------|
| S01 | Water-MET frozen-flow Isp ceiling                     | R2.1     | Complete    |
| S02 | Trajectory Isp sweep — power required per Isp band    | R2 / R4  | Planned     |
| S03 | Water-ion grid life under oxidizing plume             | R2.2     | Planned     |
| S04 | H₂ storage thermal model at 9 AU                      | R2.4     | Planned     |
| S05 | Electrolysis escape-route quantitative trade          | R2.3     | Planned     |

## Adding a new study

1. Pick the next `SNN` number.
2. Create `studies/SNN_short_name/`.
3. Write `STUDY.md` first — question, method, validity caveats. Forces you to state the question before coding.
4. Add models to `src/waterprop/<module>/` if reusable; otherwise keep study-specific helpers in `run.py`.
5. Add a regression test in `tests/` if the model is non-trivial.
6. Update the index table above and reference the study from the round writeup in `docs/`.
