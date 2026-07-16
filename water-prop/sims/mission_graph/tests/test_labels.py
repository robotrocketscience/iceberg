"""Label determinism, canonicalization, and distinctness."""

from mission_graph.framework import (
    canonicalize_params,
    node_label,
    params_hash,
    path_label,
)


def test_canonicalize_sorts_keys():
    a = {"b": 1.0, "a": 2.0, "c": 3.0}
    b = {"c": 3.0, "a": 2.0, "b": 1.0}
    assert canonicalize_params(a) == canonicalize_params(b)


def test_canonicalize_coerces_int_to_float():
    a = {"isp": 340}
    b = {"isp": 340.0}
    assert canonicalize_params(a) == canonicalize_params(b)


def test_canonicalize_rounds_to_precision():
    a = {"x": 1.234567891}
    b = {"x": 1.234567892}
    # default precision is 6 sig digits — these differ at the 9th digit
    assert canonicalize_params(a) == canonicalize_params(b)


def test_canonicalize_distinguishes_meaningful_differences():
    a = {"x": 1.234567}
    b = {"x": 1.234568}
    # these differ at the 6th decimal, within precision
    assert canonicalize_params(a) != canonicalize_params(b)


def test_canonicalize_preserves_bool():
    a = canonicalize_params({"flag": True})
    b = canonicalize_params({"flag": False})
    assert a != b


def test_params_hash_is_deterministic():
    p = {"isp": 340.0, "dv": 7.3}
    assert params_hash(p) == params_hash(p)


def test_params_hash_is_short_hex():
    h = params_hash({"x": 1.0})
    assert len(h) == 6
    assert all(c in "0123456789abcdef" for c in h)


def test_params_hash_distinguishes_distinct_inputs():
    h1 = params_hash({"x": 1.0})
    h2 = params_hash({"x": 2.0})
    assert h1 != h2


def test_params_hash_collides_for_equivalent_inputs():
    h1 = params_hash({"x": 340, "y": 7.3})
    h2 = params_hash({"y": 7.3, "x": 340.0})
    assert h1 == h2


def test_node_label_format():
    lbl = node_label("P1_LEO_to_Saturn", "hohmann", {"isp": 340.0})
    assert lbl.startswith("P1_LEO_to_Saturn.hohmann.")
    parts = lbl.split(".")
    assert len(parts[-1]) == 6


def test_node_label_is_stable():
    a = node_label("P", "opt", {"isp": 340.0})
    b = node_label("P", "opt", {"isp": 340.0})
    assert a == b


def test_path_label_joins_with_arrow():
    nodes = ["P0.a.aaaaaa", "P1.b.bbbbbb"]
    assert path_label(nodes) == "P0.a.aaaaaa -> P1.b.bbbbbb"


def test_path_label_handles_single_node():
    assert path_label(["P0.a.aaaaaa"]) == "P0.a.aaaaaa"


def test_path_label_handles_empty():
    assert path_label([]) == ""
