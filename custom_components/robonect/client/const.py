"""Constants used by the Robonect client."""

COMMANDS = [
    "battery",  # wakes up robonect
    "clock",  # ok when sleeping
    "door",  # ok when sleeping
    "error",  # wakes up robonect
    "ext",  # ok when sleeping
    "gps",  # ok when sleeping
    "health",  # ok when sleeping
    "hour",  # wakes up robonect
    "motor",  # wakes up robonect
    "portal",  # ok when sleeping
    "push",  # ok when sleeping
    "remote",  # wakes up robonect
    "report",  # wakes up robonect
    "status",  # ok when sleeping
    "timer",  # ok when sleeping
    "version",  # wakes up robonect
    "weather",  # ok when sleeping
    "wlan",  # ok when sleeping
    "wire",  # wakes up robonect
]

SAFE_COMMANDS = [
    "clock",  # ok when sleeping
    "door",  # ok when sleeping
    "ext",  # ok when sleeping
    "health",  # ok when sleeping
    "status",  # ok when sleeping
    "timer",  # ok when sleeping
    "weather",  # ok when sleeping
    "wlan",  # ok when sleeping
]
