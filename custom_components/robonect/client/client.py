"""Robonect library using httpx."""

from __future__ import annotations

from datetime import datetime
import json
import logging
import urllib.parse

from homeassistant.helpers.httpx_client import get_async_client
import httpx

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
        """Start the httpx client."""
        if not self.client:
            self.client = get_async_client(self.hass)
            self.client.auth = self.auth

    async def client_close(self):
        """Close the httpx client."""
        if self.client:
            # await self.client.aclose()
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

        await self.client_start()

        for scheme in self.scheme:
            url = create_url(scheme)
            _LOGGER.debug(f"Calling {url}")
            try:
                response = await self.client.get(url)
                if response.status_code == 200 or response.status_code >= 400:
                    self.scheme = [scheme]  # Set scheme for future calls
                    break  # Exit the loop on successful or error response
                elif 300 <= response.status_code < 400:
                    _LOGGER.debug(
                        f"Received redirect status code {response.status_code}, continuing to next scheme"
                    )
                    continue  # Continue loop on redirect (3xx)
            except httpx.RequestError as e:
                _LOGGER.debug(
                    f"Failed to connect using {scheme}://{self.host}, error: {e}"
                )
                last_exception = e
                continue  # Continue to the next scheme on connection error

        if response is None:
            raise last_exception or Exception(
                "Failed to get a response from the mower."
            )
        if response and response.status_code == 200:
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
            except json.JSONDecodeError as e:
                _LOGGER.debug(
                    f"The returned JSON for {command} is invalid ({e}): {result_text}"
                )
                return False
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
            if not self.is_sleeping or bypass_sleeping:
                for cmd in commands:
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

    def is_sleeping(self) -> int:
        """Return if the mower is sleeping."""
        return self.is_sleeping

    async def async_reset_blades(self) -> bool:
        """Reset the mower blades."""
        result = await self.async_cmd("reset_blades")
        return {"successful": result}
