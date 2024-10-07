"""Robonect library utils."""


def transform_json_to_single_depth(json_data, prefix=""):
    """Transform a json so only 1 depth level."""
    result = []
    for key, value in json_data.items():
        if isinstance(value, dict):
            result.extend(transform_json_to_single_depth(value, f"{key}_"))
        else:
            result.append({f"{prefix}{key}": value})
    return result
