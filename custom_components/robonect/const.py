"""Constants used by Robonect."""
import json
import logging
from pathlib import Path
from typing import Final

import voluptuous as vol
from homeassistant.const import Platform
from homeassistant.helpers import config_validation as cv

SHOW_DEBUG_AS_WARNING = False
BYPASS_SLEEP = True

_LOGGER = logging.getLogger(__name__)

CONF_TRACKING = "tracking"
CONF_UPDATE_INTERVAL = "update_interval"

PLATFORMS: Final = [Platform.SENSOR]

ATTRIBUTION: Final = "Data provided by Robonect"

SERVICE_START = "start"
SERVICE_STOP = "stop"
SERVICE_REBOOT = "reboot"
SERVICE_SHUTDOWN = "shutdown"
SERVICE_SLEEP = "sleep"
SERVICE_JOB = "job"

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
SERVICE_MODE_SCHEMA = vol.Schema(
    {
        vol.Required("mode", default="auto"): vol.In(SERVICE_MODE_VALUES),
    }
)
SENSOR_GROUPS = ["battery", "wlan", "version", "timer", "hour", "error"]

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
DEFAULT_UPDATE_INTERVAL = 2
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
STARTUP = """
-------------------------------------------------------------------
{name}
Version: {version}
This is a custom component
If you have any issues with this you need to open an issue here:
{issueurl}
-------------------------------------------------------------------
""".format(
    name=NAME, version=VERSION, issueurl=ISSUEURL
)
