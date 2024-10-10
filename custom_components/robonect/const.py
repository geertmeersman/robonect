"""Constants used by Robonect."""

import json
from pathlib import Path
from typing import Final

from homeassistant.const import CONF_ENTITY_ID, Platform
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.selector import (
    BooleanSelector,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)
import voluptuous as vol


# Custom validator for degrees (allowing positive and negative integers)
def validate_degrees(value):
    """Validate degree value."""
    return vol.Coerce(int)(value)


PLATFORMS: Final = [
    Platform.BINARY_SENSOR,
    Platform.SENSOR,
    Platform.BUTTON,
    Platform.DEVICE_TRACKER,
    Platform.SWITCH,
    Platform.LAWN_MOWER,
]

ATTR_STATE_UNITS = {
    "battery": {
        "charge": "%",
        "voltage": {"lambda": "lambda a : math.ceil(a / 10)/100", "unit": "V"},
        "current": "mA",
        "temperature": {"lambda": "lambda a : a / 10", "unit": "°C"},
        "full": "mAh",
        "remaining": "mAh",
    },
    "motor": {
        "power": "%",
        "speed": {"lambda": "lambda a : round(a , 1)", "unit": "cm/s"},
        "current": "mA",
        "average": "RPM",
    },
    "status": {
        "distance": "m",
        "duration": "min",
        "battery": "%",
        "hours": "h",
        "quality": "%",
        "days": "d",
        "signal": "dBm",
        "temperature": "°C",
        "humidity": "%",
    },
}

EVENT_ROBONECT_RESPONSE = "robonect_response"

ATTR_SATELLITES = "satellites"

CONF_MQTT_ENABLED = "mqtt_enabled"
CONF_MQTT_TOPIC = "mqtt_topic"
CONF_REST_ENABLED = "rest_enabled"
CONF_ATTRS_UNITS = "attributes_units"
DEFAULT_MQTT_TOPIC = "automower"
CONF_SUGGESTED_TYPE = "Automower 310"
CONF_SUGGESTED_HOST = "10.0.0.99"
CONF_SUGGESTED_BRAND = "Husqvarna"
CONF_BRAND = "brand"
CONF_ENABLE = "enable"
CONF_WINTER_MODE = "winter_mode"

ATTRIBUTION_REST: Final = "Data provided by Robonect REST"
ATTRIBUTION_MQTT: Final = "Data provided by Robonect MQTT"

SERVICE_START = "start"
SERVICE_STOP = "stop"
SERVICE_REBOOT = "reboot"
SERVICE_SHUTDOWN = "shutdown"
SERVICE_SLEEP = "sleep"
SERVICE_TIMER = "timer"
SERVICE_JOB = "job"
SERVICE_DIRECT = "direct"
SERVICE_EQUIPMENT = "ext"
CONF_ENTRY_ID = "entry_id"

ROBONECT_BRANDS = ["Husqvarna", "Gardena", "Flymo", "McCulloch"]
SERVICE_JOB_AFTER_VALUES = ["Auto", "Home", "End of day"]
SERVICE_JOB_REMOTESTART_VALUES = [
    "Normal",
    "From charging station",
    "Remote start 1",
    "Remote start 2",
    "Remote start 3",
    "Remote start 4",
    "Remote start 5",
]
SERVICE_JOB_CORRIDOR_VALUES = [
    "Normal",
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
]
SERVICE_MODE_VALUES = ["man", "auto", "eod", "home"]
SERVICE_JOB_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ENTITY_ID): cv.string,
        vol.Optional("start"): cv.string,
        vol.Optional("end"): cv.string,
        vol.Optional("duration"): cv.positive_int,
        vol.Optional("after", default="Auto"): vol.In(SERVICE_JOB_AFTER_VALUES),
        vol.Optional("remotestart", default="Normal"): vol.In(
            SERVICE_JOB_REMOTESTART_VALUES
        ),
        vol.Optional("corridor", default="Normal"): vol.In(SERVICE_JOB_CORRIDOR_VALUES),
    }
)
WEEKDAYS_SHORT = ["mo", "tu", "we", "th", "fr", "sa", "su"]
SERVICE_TIMER_IDS = [str(id) for id in list(range(1, 15))]
SERVICE_TIMER_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ENTITY_ID): cv.string,
        vol.Required("timer"): vol.In(SERVICE_TIMER_IDS),
        vol.Required(CONF_ENABLE): bool,
        vol.Required("start"): cv.string,
        vol.Required("end"): cv.string,
        vol.Required("weekdays"): SelectSelector(
            SelectSelectorConfig(
                options=WEEKDAYS_SHORT,
                multiple=True,
                custom_value=False,
                mode=SelectSelectorMode.LIST,
                translation_key="weekdays",
            )
        ),
    }
)

EQUIPMENT_SHORT = ["ext0", "ext1", "ext2", "ext3"]
EQUIPMENT_CHANNEL = [
    {"value": "0", "label": "[IN] Analog"},
    {"value": "4", "label": "[IN] Floating"},
    {"value": "40", "label": "[IN] PullDown"},
    {"value": "72", "label": "[IN] PullUp"},
    {"value": "20", "label": "[OUT] OpenDrain"},
    {"value": "16", "label": "[OUT] PushPull"},
]

EQUIPMENT_MODE = [
    {"value": "0", "label": "Off"},
    {"value": "1", "label": "On"},
    {"value": "2", "label": "Night (19-7 o'clock)"},
    {"value": "3", "label": "Drive"},
    {"value": "4", "label": "Night drive (19-7 o'clock)"},
    {"value": "5", "label": "Searching/Way home"},
    {"value": "6", "label": "Park position"},
    {"value": "7", "label": "Brake light"},
    {"value": "8", "label": "Left Turn Signal"},
    {"value": "9", "label": "Right Turn Signal"},
    {"value": "10", "label": "API"},
]

SERVICE_EQUIPMENT_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ENTITY_ID): cv.entity_id,  # Validate entity ID
        vol.Required("ext"): SelectSelector(
            SelectSelectorConfig(
                options=EQUIPMENT_SHORT,
                multiple=False,
                custom_value=False,
                mode=SelectSelectorMode.LIST,
                translation_key="equipment",
            )
        ),
        vol.Required("gpioout"): SelectSelector(
            SelectSelectorConfig(
                options=EQUIPMENT_CHANNEL,
                multiple=False,
                custom_value=False,
                mode=SelectSelectorMode.LIST,
                translation_key="equipment_channel",
            )
        ),
        vol.Required("gpiomode"): SelectSelector(
            SelectSelectorConfig(
                options=EQUIPMENT_MODE,
                multiple=False,
                custom_value=False,
                mode=SelectSelectorMode.LIST,
                translation_key="equipment_mode",
            )
        ),
        vol.Required("gpioerr"): BooleanSelector(),  # Checkbox for gpioerr
        vol.Required("gpioinv"): BooleanSelector(),  # Checkbox for gpioinv
    }
)

SERVICE_DIRECT_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ENTITY_ID): cv.entity_id,  # Validate entity ID
        vol.Required(
            "left"
        ): validate_degrees,  # Validate left as an integer (positive or negative)
        vol.Required(
            "right"
        ): validate_degrees,  # Validate right as an integer (positive or negative)
        vol.Required("timeout"): vol.All(
            cv.positive_int, vol.Range(max=5000)
        ),  # Validate timeout as a positive integer with a max of 5000
    }
)

SERVICE_MODE_SCHEMA = vol.Schema(
    {
        vol.Required("mode", default="auto"): vol.In(SERVICE_MODE_VALUES),
    }
)
SENSOR_GROUPS = [
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

STATUS_MAPPING_LAWN_MOWER = {
    0: "detecting_status",
    1: "paused",  # "stopped",
    2: "mowing",
    3: "returning",  # "searching for charging station",
    4: "charging",
    5: "returning",  # "searching",
    7: "error",
    8: "lost_cable_signal",
    16: "off",
    17: "docked",
    18: "waiting_for_garage_door",
    98: "offline_cannot_bind",
    99: "unknown",
}

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
DEFAULT_SCAN_INTERVAL = 2
CONNECTION_RETRY = 5
REQUEST_TIMEOUT = 20
WEBSITE = "https://www.robonect-shop.de"

manifestfile = Path(__file__).parent / "manifest.json"
with open(manifestfile) as json_file:
    manifest_data = json.load(json_file)

DOMAIN = manifest_data.get("domain")
NAME = manifest_data.get("name")
VERSION = manifest_data.get("version")
ISSUEURL = manifest_data.get("issue_tracker")
STARTUP = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom component
If you have any issues with this you need to open an issue here:
{ISSUEURL}
-------------------------------------------------------------------
"""
TRACKER_UPDATE = f"{DOMAIN}_tracker_update"
WEEKDAYS_HEX = {
    0x1: "mo",
    0x2: "tu",
    0x4: "we",
    0x8: "th",
    0x10: "fr",
    0x20: "sa",
    0x40: "su",
}
