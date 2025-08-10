"""Robonect library using httpx."""

from __future__ import annotations

from datetime import datetime
import json
import logging
import urllib.parse

from homeassistant.helpers.httpx_client import create_async_httpx_client
import httpx

from .const import SAFE_COMMANDS
from .utils import transform_json_to_single_depth

_LOGGER = logging.getLogger(__name__)


def encode_dict_values_to_utf8(dictionary):
    """Encode dict values to utf8."""
    encoded_dict = {}
    for key, value in dictionary.items():
        if isinstance(value, dict):
            encoded_dict[key] = encode_dict_values_to_utf8(value)
        elif isinstance(value, str):
            encoded_dict[key] = value.encode("utf-8")
        else:
            encoded_dict[key] = value
    return encoded_dict


def validate_json(json_str):
    """Validate json string."""
    if isinstance(json_str, dict):
        return True
    try:
        return json.loads(json_str)
    except ValueError as error:
        print(error)
        return False


class RobonectException(Exception):
    """Raised when an update has failed."""

    def __init__(self, cmd, exception, result):
        """Init the Robonect Exception."""
        self.message = f"Aiorobonect call for cmd {cmd} failed: {result}\n{exception}"
        super().__init__(self.message)


class RobonectClient:
    """Class to communicate with the Robonect API."""

    def __init__(self, hass, host, username, password, transform_json=False) -> None:
        """Initialize the Communication API to get data."""
        self.auth = None
        self.hass = hass
        self.host = host
        self.scheme = None
        self.username = username
        self.password = password
        self.client = None
        self.is_sleeping = None
        self.transform_json = transform_json
        if username is not None and password is not None:
            self.auth = (username, password)

    async def client_start(self):
        """Start a new, isolated httpx client."""
        if not self.client:
            self.client = create_async_httpx_client(
                self.hass, timeout=httpx.Timeout(20.0, read=20.0)
            )
            if self.auth:
                self.client.auth = self.auth

    async def client_close(self):
        """Properly close and cleanup the httpx client."""
        if self.client:
            # await self.client.aclose() commented as this closes the HA httpx client
            # Don't close the client as it's a shared Home Assistant HTTPX client
            # that's managed by Home Assistant itself
            self.client = None

    async def async_cmd(self, command=None, params={}) -> list[dict]:
        """Send command to mower."""
        ext = None
        if command is None:
            return False
        if params is None:
            params = ""
        else:
            if command == "equipment":
                ext = params.pop("ext")
            params = urllib.parse.urlencode(params)

        if command == "job":
            _LOGGER.debug(f"Job params: {params}")
            return

        result_json = None

        def create_url(scheme):
            if command == "reset_blades":
                return f"{scheme}://{self.host}/?btexe="
            if command == "equipment":
                return f"{scheme}://{self.host}/{ext}?{params}"
            return f"{scheme}://{self.host}/json?cmd={command}&{params}"

        if self.scheme is None:
            self.scheme = ["http", "https"]

        if command == "direct":
            status = await self.async_stop()
            if status.get("successful") is False and status.get("error_code") != 7:
                _LOGGER.warning(
                    f"Mower not stopped before `direct` command: {status.get('error_code')}"
                )
                return

        response = None
        last_exception = None
        last_url = None  # Track the last attempted URL

        await self.client_start()

        for scheme in self.scheme:
            url = create_url(scheme)
            _LOGGER.debug(f"Attempting to call {url}")
            try:
                response = await self.client.get(url)
                _LOGGER.debug(f"Received status code {response.status_code} from {url}")
                if response.status_code == 200 or response.status_code >= 400:
                    self.scheme = [scheme]  # Set scheme for future calls
                    break  # Exit the loop on usable response
                elif 300 <= response.status_code < 400:
                    _LOGGER.debug(
                        f"Redirect ({response.status_code}) from {url}, trying next scheme"
                    )
                    continue
            except httpx.TimeoutException as e:
                _LOGGER.warning(f"Timeout while connecting to {url}")
                last_exception = e
                last_url = url
                continue
            except httpx.RequestError as e:
                _LOGGER.warning(f"Request error from {url}")
                last_url = url
                last_exception = e
                continue

        if response is None:
            raise Exception(
                f"Failed to get a response from the mower at {last_url}. "
                f"Last error: `{str(last_exception) or type(last_exception).__name__}`"
            )

        if response and response.status_code == 200:
            _LOGGER.debug(f"Successful response from {url}")
            if command == "reset_blades":
                await self.client_close()
                return {"successful": True}
            result_text = response.text
            if command == "equipment":
                await self.client_close()
                if "The changes were successfully applied" in result_text:
                    return {"successful": True}
                else:
                    return {"successful": False}
            _LOGGER.debug(f"Rest API call result for {command}: {result_text}")
            try:
                result_json = json.loads(result_text)
            except (json.JSONDecodeError, ValueError) as e:
                _LOGGER.debug(f"Invalid JSON for {command} ({e}): {result_text}")
                return False
            if command == "wire":
                # Extract the lowest quality value from the sensors list
                sensors = result_json.get("sensors", [])
                if sensors:
                    min_quality = min(
                        sensor.get("quality", float("inf")) for sensor in sensors
                    )
                    result_json["lowest_quality"] = min_quality
                else:
                    result_json["lowest_quality"] = None
            result_json["sync_time"] = datetime.now()
        elif response and response.status_code >= 400:
            response.raise_for_status()
        await self.client_close()

        if self.transform_json:
            return transform_json_to_single_depth(result_json)

        return result_json

    async def async_cmds(self, commands=None, bypass_sleeping=False) -> dict:
        """Send command to mower."""
        await self.client_start()
        result = await self.state()
        if result:
            result = {"status": result}
            for cmd in commands:
                if not self.is_sleeping or bypass_sleeping or cmd in SAFE_COMMANDS:
                    json_res = await self.async_cmd(cmd)
                    if json_res:
                        result.update({cmd: json_res})
            await self.client_close()
        return result

    async def state(self) -> dict:
        """Send status command to mower."""
        await self.client_start()
        result = await self.async_cmd("status")
        if result:
            self.is_sleeping = result.get("status").get("status") == 17
            await self.client_close()
        return result

    async def async_start(self) -> bool:
        """Start the mower."""
        result = await self.async_cmd("start")
        return result

    async def async_stop(self) -> bool:
        """Stop the mower."""
        result = await self.async_cmd("stop")
        return result

    async def async_reboot(self) -> bool:
        """Reboot Robonect."""
        result = await self.async_cmd("service", {"service": "reboot"})
        return result

    async def async_shutdown(self) -> bool:
        """Shutdown Robonect."""
        result = await self.async_cmd("service", {"service": "shutdown"})
        return result

    async def async_sleep(self) -> bool:
        """Make Robonect sleep."""
        result = await self.async_cmd("service", {"service": "sleep"})
        return result

    def is_asleep(self) -> bool:
        """Return if the mower is sleeping."""
        return self.is_sleeping

    async def async_reset_blades(self) -> bool:
        """Reset the mower blades."""
        result = await self.async_cmd("reset_blades")
        return {"successful": result}
