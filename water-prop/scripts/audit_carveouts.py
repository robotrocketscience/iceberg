"""Known carve-outs for audit-call-conventions.py.

Each entry: (path_suffix, line) → reason. Lines blessed here are skipped by the
strict gate. Carve-outs are for INTENTIONAL bug-pattern reproductions (e.g. a
round's `unit_sanity_check` deliberately demonstrating the historical bug) and
manually-verified false positives where the heuristic name-pattern misclassifies
a semantically-correct variable.

Add a new entry only after manual inspection. Do not weaken the heuristic
itself; carve-out specific lines and document the why.

Source-of-truth audit: water-prop/rounds/R_shared_physics_audit/READING.md.
"""

CARVEOUTS = {
    # R_electric_outbound_rerun deliberately reproduces the hyperion bug pattern as
    # a unit-sanity-check + reproducibility cross-check. Documented in the source.
    ("R_electric_outbound_rerun/run.py", 195): "intentional bug reproduction in unit_sanity_check",
    ("R_electric_outbound_rerun/run.py", 225): "intentional bug reproduction under use_bugged_outbound=True",
    ("R_electric_outbound_rerun/run.py", 234): "intentional bug reproduction under use_bugged_outbound=True",
    # R_redundancy_budget_cost passes m_after_kick (= m_initial_inbound / exp(...)),
    # which is wet-at-start of the NEXT (electric) burn. The variable name trips
    # the dry-hint regex but the semantic is correct.
    ("R_redundancy_budget_cost/run.py", 222): "m_after_kick is wet-at-start of the subsequent electric burn",
}
