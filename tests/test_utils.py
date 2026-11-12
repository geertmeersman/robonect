"""Tests for Robonect utils."""

import pytest

from custom_components.robonect.utils import (
    convert_coordinate_degree_to_float,
    filter_out_units,
    float_to_timestring,
    format_entity_name,
    has_non_numeric_characters,
    hex2weekdays,
    parse_duration_seconds_to_minutes,
    sensor_name,
    sizeof_fmt,
    str_to_float,
    wifi_signal_to_percentage,
)

# ---------------------------------------------------------------------------
# parse_duration_seconds_to_minutes
# ---------------------------------------------------------------------------


def test_parse_duration_int():
    """Parse integer seconds to minutes string."""
    assert parse_duration_seconds_to_minutes(120) == "2 min"


def test_parse_duration_string():
    """Parse string with seconds to minutes string."""
    assert parse_duration_seconds_to_minutes("300 sec") == "5 min"


def test_parse_duration_zero():
    """Parse zero seconds returns 0 min."""
    assert parse_duration_seconds_to_minutes(0) == "0 min"


def test_parse_duration_invalid_string():
    """Parse string without number returns unknown duration."""
    assert parse_duration_seconds_to_minutes("no number here") == "unknown duration"


# ---------------------------------------------------------------------------
# str_to_float
# ---------------------------------------------------------------------------


def test_str_to_float_dot():
    """Convert dot-decimal string to float."""
    assert str_to_float("3.14") == 3.14


def test_str_to_float_comma():
    """Convert comma-decimal string to float."""
    assert str_to_float("3,14") == 3.14


# ---------------------------------------------------------------------------
# float_to_timestring
# ---------------------------------------------------------------------------


def test_float_to_timestring_hours():
    """Convert 3600 raw input to 1 hour string."""
    assert float_to_timestring(3600.0) == "01h"


def test_float_to_timestring_minutes():
    """Convert 90 minutes to 1h 30min string."""
    assert float_to_timestring(90, "minutes") == "01h 30 min"


def test_float_to_timestring_zero():
    """Convert zero to 0 sec string."""
    assert float_to_timestring(0) == "0 sec"


def test_float_to_timestring_seconds_unit():
    """Convert 1 with seconds unit to 1 hour (1 * 60 * 60 = 3600 seconds)."""
    assert float_to_timestring(1, "seconds") == "01h"


def test_float_to_timestring_minutes_unit():
    """Convert 90 minutes to 1h 30min."""
    assert float_to_timestring(90, "minutes") == "01h 30 min"


# ---------------------------------------------------------------------------
# format_entity_name
# ---------------------------------------------------------------------------


def test_format_entity_name_spaces():
    """Format entity name with spaces to underscored lowercase."""
    assert format_entity_name("My Sensor") == "my_sensor"


def test_format_entity_name_special_chars():
    """Format entity name strips special characters."""
    assert format_entity_name("sensor/value!") == "sensorvalue"


def test_format_entity_name_already_clean():
    """Format entity name that is already clean stays unchanged."""
    assert format_entity_name("battery") == "battery"


# ---------------------------------------------------------------------------
# sensor_name
# ---------------------------------------------------------------------------


def test_sensor_name_underscores():
    """Sensor name converts underscores to title case."""
    assert sensor_name("battery_charge") == "Battery Charge"


def test_sensor_name_already_title():
    """Sensor name that is already title case stays unchanged."""
    assert sensor_name("Battery") == "Battery"


# ---------------------------------------------------------------------------
# sizeof_fmt
# ---------------------------------------------------------------------------


def test_sizeof_fmt_bytes():
    """Format bytes value."""
    assert sizeof_fmt(512) == "512.0b"


def test_sizeof_fmt_kilobytes():
    """Format kilobytes value."""
    assert sizeof_fmt(1024) == "1.0Kb"


def test_sizeof_fmt_megabytes():
    """Format megabytes value."""
    assert sizeof_fmt(1024 * 1024) == "1.0Mb"


# ---------------------------------------------------------------------------
# wifi_signal_to_percentage
# ---------------------------------------------------------------------------


def test_wifi_signal_strong():
    """Strong signal at -60 dBm returns 100%."""
    assert wifi_signal_to_percentage(-60) == 100.0


def test_wifi_signal_weak():
    """Weak signal at -90 dBm returns 0%."""
    assert wifi_signal_to_percentage(-90) == 0.0


def test_wifi_signal_mid():
    """Mid signal returns value between 0 and 100."""
    result = wifi_signal_to_percentage(-75)
    assert 0 < result < 100


def test_wifi_signal_above_max_clamped():
    """Signal above max is clamped to 100%."""
    assert wifi_signal_to_percentage(-50) == 100.0


def test_wifi_signal_below_min_clamped():
    """Signal below min is clamped to 0%."""
    assert wifi_signal_to_percentage(-100) == 0.0


# ---------------------------------------------------------------------------
# filter_out_units
# ---------------------------------------------------------------------------


def test_filter_out_units_with_unit():
    """Filter out unit suffix from numeric string."""
    assert filter_out_units("42.5 km") == "42.5"


def test_filter_out_units_no_unit():
    """Non-numeric string is returned as-is."""
    assert filter_out_units("hello world") == "hello world"


def test_filter_out_units_plain_number():
    """Plain number string is returned as-is."""
    assert filter_out_units("100") == "100"


# ---------------------------------------------------------------------------
# has_non_numeric_characters
# ---------------------------------------------------------------------------


def test_has_non_numeric_true():
    """String with unit returns True."""
    assert has_non_numeric_characters("12.3 km", ".") is True


def test_has_non_numeric_false():
    """Pure numeric string returns False."""
    assert has_non_numeric_characters("12.3", ".") is False


# ---------------------------------------------------------------------------
# convert_coordinate_degree_to_float
# ---------------------------------------------------------------------------


def test_coordinate_plain_float():
    """Plain float string is returned as float."""
    assert convert_coordinate_degree_to_float("51.5") == pytest.approx(51.5)


def test_coordinate_degrees_north():
    """North coordinate in degrees is converted to positive float."""
    result = convert_coordinate_degree_to_float("51°30.0N")
    assert result == pytest.approx(51.5)


def test_coordinate_degrees_south():
    """South coordinate in degrees is converted to negative float."""
    result = convert_coordinate_degree_to_float("51°30.0S")
    assert result == pytest.approx(-51.5)


# ---------------------------------------------------------------------------
# hex2weekdays
# ---------------------------------------------------------------------------


def test_hex2weekdays_all_days():
    """0x7F activates all 7 days."""
    result = hex2weekdays("7F")
    assert all(result.values())


def test_hex2weekdays_no_days():
    """0x00 activates no days."""
    result = hex2weekdays("00")
    assert not any(result.values())


def test_hex2weekdays_returns_dict():
    """hex2weekdays returns a dict."""
    result = hex2weekdays("7F")
    assert isinstance(result, dict)
