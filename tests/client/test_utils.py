"""Tests for client utils."""

from custom_components.robonect.client.utils import transform_json_to_single_depth


def test_flat_dict():
    """Flat dict returns list of single-key dicts."""
    result = transform_json_to_single_depth({"a": 1, "b": 2})
    assert {"a": 1} in result
    assert {"b": 2} in result


def test_nested_dict():
    """Nested dict is flattened with prefix."""
    result = transform_json_to_single_depth({"status": {"code": 4, "mode": 1}})
    assert {"status_code": 4} in result
    assert {"status_mode": 1} in result


def test_deeply_nested_dict():
    """Deeply nested dict: prefix is only applied one level deep (by design)."""
    result = transform_json_to_single_depth({"a": {"b": {"c": 42}}})
    assert {"b_c": 42} in result


def test_mixed_dict():
    """Mix of flat and nested keys."""
    result = transform_json_to_single_depth({"x": 1, "y": {"z": 2}})
    assert {"x": 1} in result
    assert {"y_z": 2} in result


def test_empty_dict():
    """Empty dict returns empty list."""
    result = transform_json_to_single_depth({})
    assert result == []
