"""Robonect utils."""
from __future__ import annotations

import logging
import re

from jsonpath import jsonpath

from .const import SHOW_DEBUG_AS_WARNING

_LOGGER = logging.getLogger(__name__)


def log_debug(input, force=False) -> None:
    """Log to logger as debug or force as warning."""
    if SHOW_DEBUG_AS_WARNING is True or force is True:
        _LOGGER.warning(input)
    else:
        _LOGGER.debug(input)


def str_to_float(input) -> float:
    """Transform float to string."""
    return float(input.replace(",", "."))


def float_to_timestring(float_time, unit_type) -> str:
    """Transform float to timestring."""
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
        result += f" {hours:02.0f}" + "u"
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
    # log_debug(f"[get_json_dict_path] Path: {path}, Dict: {dictionary}")
    json_dict = jsonpath(dictionary, path)
    if isinstance(json_dict, list):
        json_dict = json_dict[0]
    return json_dict


def wifi_signal_to_percentage(signal_strength):
    # Define the maximum and minimum WiFi signal strengths
    max_signal_strength = -30  # dBm
    min_signal_strength = -100  # dBm

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
