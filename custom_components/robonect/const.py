"""Constants used by Robonect."""
import json
import logging
from datetime import timedelta
from pathlib import Path
from typing import Final

from homeassistant.const import Platform

SHOW_DEBUG_AS_WARNING = False

_LOGGER = logging.getLogger(__name__)

PLATFORMS: Final = [Platform.SENSOR]

ATTRIBUTION: Final = "Data provided by Robonect"

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
COORDINATOR_UPDATE_INTERVAL = timedelta(minutes=2)
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
