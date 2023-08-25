"""Constants used by Robonect."""
import json
from pathlib import Path
from typing import Final

from homeassistant.const import CONF_ENTITY_ID, Platform
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.selector import (
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)
import voluptuous as vol

PLATFORMS: Final = [
    Platform.BINARY_SENSOR,
    Platform.SENSOR,
    Platform.BUTTON,
    Platform.DEVICE_TRACKER,
    Platform.VACUUM,
    Platform.SWITCH,
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

ATTRIBUTION_REST: Final = "Data provided by Robonect REST"
ATTRIBUTION_MQTT: Final = "Data provided by Robonect MQTT"

SERVICE_START = "start"
SERVICE_STOP = "stop"
SERVICE_REBOOT = "reboot"
SERVICE_SHUTDOWN = "shutdown"
SERVICE_SLEEP = "sleep"
SERVICE_TIMER = "timer"
SERVICE_JOB = "job"

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

SERVICE_MODE_SCHEMA = vol.Schema(
    {
        vol.Required("mode", default="auto"): vol.In(SERVICE_MODE_VALUES),
    }
)
SENSOR_GROUPS = [
    "battery",
    "clock",
    "door",
    "error",
    "ext",
    "gps",
    "health",
    "hour",
    "motor",
    "portal",
    "push",
    "remote",
    "status",
    "timer",
    "version",
    "weather",
    "wlan",
    "wire",
]

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
