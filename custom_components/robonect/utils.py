"""Robonect utils."""

from __future__ import annotations

import datetime
import logging
import math
import re

from jsonpath import jsonpath
import pytz

from .const import ATTR_STATE_UNITS, DOMAIN, WEEKDAYS_HEX

_LOGGER = logging.getLogger(__name__)

_cached_timezone = None


def parse_duration_seconds_to_minutes(payload: str | int) -> str:
    """Parse a duration in seconds to minutes appending it with min."""

    if isinstance(payload, int):
        seconds = payload
    else:
        # assume string, extract number with regex
        match = re.search(r"(\d+)", payload)
        if match:
            seconds = int(match.group(1))
        else:
            return "unknown duration"

    minutes = round(seconds / 60)
    return f"{minutes} min"


def get_cached_timezone(hass):
    """Get the cached timezone."""
    global _cached_timezone
    if _cached_timezone is None:
        _cached_timezone = pytz.timezone(hass.config.time_zone)
    return _cached_timezone


def str_to_float(input, entity=None) -> float:
    """Transform float to string."""
    return float(input.replace(",", "."))


def raw_prefix(value, entity=None):
    """Prefix raw."""
    return f"raw_{value}"


def float_minutes_to_timestring(float_time, entity=None):
    """Transform float minutes to timestring."""
    return float_to_timestring(float_time, "minutes")


def float_to_timestring(float_time, unit_type="") -> str:
    """Transform float to timestring."""
    if isinstance(float_time, str):
        float_time = str_to_float(float_time)
    if unit_type.lower() == "seconds":
        float_time = float_time * 60 * 60
    elif unit_type.lower() == "minutes":
        float_time = float_time * 60
    # log_debug(f"[float_to_timestring] Float Time {float_time}")
    hours, seconds = divmod(float_time, 3600)  # split to hours and seconds
    minutes, seconds = divmod(seconds, 60)  # split the seconds to minutes and seconds
    result = ""
    if hours:
        result += f" {hours:02.0f}" + "h"
    if minutes:
        result += f" {minutes:02.0f}" + " min"
    if seconds:
        result += f" {seconds:02.0f}" + " sec"
    if len(result) == 0:
        result = "0 sec"
    return result.strip()


def format_entity_name(string: str) -> str:
    """Format entity name."""
    string = string.strip()
    string = re.sub(r"\s+", "_", string)
    string = re.sub(r"\W+", "", string).lower()
    return string


def sensor_name(string: str) -> str:
    """Format sensor name."""
    string = string.strip().replace("_", " ").title()
    return string


def sizeof_fmt(num, suffix="b"):
    """Convert unit to human readable."""
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


def get_json_dict_path(dictionary, path):
    """Fetch info based on jsonpath from dict."""
    json_dict = jsonpath(dictionary, path)
    if json_dict is False:
        return None
    if isinstance(json_dict, list):
        json_dict = json_dict[0]
    return json_dict


def wifi_signal_to_percentage(signal_strength, entity=None):
    """Convert wifi signal in dBm to percentage."""
    # Define the maximum and minimum WiFi signal strengths
    signal_strength = int(signal_strength)
    max_signal_strength = -60  # dBm
    min_signal_strength = -90  # dBm

    # Input validation
    if not isinstance(signal_strength, int | float):
        return 0

    # Convert the input signal strength to a percentage
    percentage = (
        (signal_strength - min_signal_strength)
        / (max_signal_strength - min_signal_strength)
        * 100
    )

    # Ensure that the percentage is within the range of 0 to 100
    percentage = max(0, min(percentage, 100))

    # Return the percentage
    return round(percentage, 1)


def unix_to_datetime(epoch_timestamp, hass=None):
    """Convert unix epoch to datetime."""

    if epoch_timestamp is None or int(epoch_timestamp) == 0 or hass is None:
        return None
    # Convert epoch timestamp to datetime object in UTC
    datetime_utc = datetime.datetime.fromtimestamp(int(epoch_timestamp), pytz.UTC)
    _LOGGER.debug(f"unix_to_date: UTC {datetime_utc}")
    # remove timezone info, das Robonect doesn't have any
    datetime_none = datetime_utc.replace(tzinfo=None)
    # Convert UTC datetime to the desired timezone
    timezone = hass.data[DOMAIN].get("timezone")
    if timezone is None:
        timezone = pytz.UTC  # Fallback in case timezone isn't cached properly

    datetime_with_timezone = timezone.localize(datetime_none, is_dst=None)
    _LOGGER.debug(f"unix_to_date: LOCAL {datetime_with_timezone}")
    return datetime_with_timezone


def filter_out_units(s):
    """Split string by whitespace and return the first part.

    If the string contains whitespace, returns only the first part before the space if it is numeric.

    Otherwise, returns the string as is.
    """

    parts = s.strip().split()
    if parts and parts[0].replace(".", "", 1).replace("-", "", 1).isdigit():
        return parts[0]
    return s


def convert_coordinate_degree_to_float(coordinate_str):
    """Convert coordinate value in degrees to a float."""
    if "°" not in coordinate_str:
        return float(coordinate_str)

    direction = coordinate_str[-1]
    coordinate_str = coordinate_str[:-2]
    degrees, minutes = coordinate_str.split("°")
    decimal_degrees = float(degrees) * 60 + float(minutes)

    if direction in ["S", "W"]:
        decimal_degrees = -decimal_degrees

    return decimal_degrees / 60


def adapt_attributes(attr_dict, category, add_units=False):
    """Add attribute state units."""
    if not isinstance(attr_dict, dict):
        return
    for key, value in attr_dict.items():
        if isinstance(value, dict):
            adapt_attributes(value, category, add_units)
        else:
            if category in ATTR_STATE_UNITS and key in ATTR_STATE_UNITS.get(category):
                unit = ATTR_STATE_UNITS.get(category).get(key)
                if isinstance(value, str) and has_non_numeric_characters(value, "."):
                    _LOGGER.debug(f"Ignoring attribute update for {category} - {value}")
                else:
                    if isinstance(unit, dict):
                        lambda_func = eval(unit.get("lambda"))
                        if add_units:
                            if isinstance(value, str):
                                value = str_to_float(filter_out_units(value))
                            attr_dict.update(
                                {key: f"{lambda_func(value)} {unit.get('unit')}"}
                            )
                        else:
                            attr_dict.update({key: lambda_func(value)})
                    elif add_units:
                        attr_dict.update({key: f"{value} {unit}"})


def has_non_numeric_characters(string, decimal_separator):
    """Check for non numeric characters."""
    pattern = r"[^0-9" + re.escape(decimal_separator) + "]"
    matches = re.search(pattern, string)
    return bool(matches)


def dummy_math(input):
    """Set Dummy math function."""
    return math.floor(input)


def hex2weekdays(hex_value):
    """Convert hex value to active weekdays."""
    binary_value = bin(int(hex_value, 16))[
        2:
    ]  # Convert hex to binary and remove '0b' prefix
    active_days = {}
    for bit, day in WEEKDAYS_HEX.items():
        if int(binary_value, 2) & bit:
            active_days.update({day: True})
        else:
            active_days.update({day: False})
    return active_days
