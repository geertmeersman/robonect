"""Robonect library using httpx."""

from __future__ import annotations

import asyncio
from datetime import datetime
import json
import logging
import urllib.parse

from homeassistant.helpers.httpx_client import create_async_httpx_client
import httpx

from .const import SAFE_COMMANDS
from .utils import transform_json_to_single_depth

_LOGGER = logging.getLogger(__name__)


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
        self._semaphore = asyncio.Semaphore(2)
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
        """No-op: HTTPX client is managed by Home Assistant; do not close here."""
        if self.client:
            self.client = None
            _LOGGER.debug("Skipping client close; HA manages the shared HTTPX client")

    async def async_cmd(
        self, command: str | None = None, params: dict | str | None = None
    ) -> dict | bool | None:
        """Send command to mower."""
        async with self._semaphore:
            return await self._async_cmd_impl(command, params)

    async def _async_cmd_impl(
        self, command: str | None = None, params: dict | str | None = None
    ) -> dict | bool | None:
        """Send command to mower, Internal implementation of async_cmd."""
        ext = None
        if command is None:
            return False
        if params is None:
            params = ""
        else:
            # copy to avoid mutating caller-provided dict
            params = dict(params)
            if command == "equipment":
                ext = params.pop("ext", None)
                if ext is None:
                    raise ValueError("equipment command requires 'ext' in params")
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
                if response.status_code == 200:
                    # Success — keep this scheme for future calls
                    self.scheme = [scheme]
                    break
                elif 300 <= response.status_code < 400:
                    # Redirects — try next scheme
                    _LOGGER.debug(
                        f"Redirect ({response.status_code}) from {url}, trying next scheme"
                    )
                    continue
                elif 400 <= response.status_code < 500:
                    # Client-side errors (auth, not found) — fail fast
                    _LOGGER.debug(f"Client error ({response.status_code}) from {url}")
                    self.scheme = [scheme]
                    break
                elif response.status_code >= 500:
                    # Server-side error — log and try next scheme (if any)
                    _LOGGER.warning(
                        f"Server error ({response.status_code}) from {url}, trying next scheme"
                    )
                    continue
            except httpx.TimeoutException as e:
                _LOGGER.warning(f"Timeout while connecting to {url}: {e!r}")
                last_exception = e
                last_url = url
                continue
            except httpx.RequestError as e:
                _LOGGER.warning(f"Request error from {url}: {e!r}")
                last_url = url
                last_exception = e
                continue

        if response is None:
            raise RobonectException(
                cmd=command,
                exception=last_exception,
                result=f"no response from {last_url}",
            ) from (last_exception or None)

        if response and response.status_code == 200:
            _LOGGER.debug(f"Successful response from {url}")
            if command == "reset_blades":
                return {"successful": True}
            result_text = response.text
            if command == "equipment":
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

        if self.transform_json:
            return transform_json_to_single_depth(result_json)

        return result_json

    async def async_cmds(self, commands=None, bypass_sleeping=False) -> dict:
        """Send multiple commands to the mower in limited parallel (safe for Robonect)."""
        result = await self.state()
        results = {"status": result} if result else {}

        allowed_cmds = [
            cmd
            for cmd in (commands or [])
            if not self.is_sleeping or bypass_sleeping or cmd in SAFE_COMMANDS
        ]

        if not allowed_cmds:
            return results

        async def limited_cmd(cmd):
            try:
                return await self.async_cmd(cmd)
            except Exception as e:
                _LOGGER.warning(f"Command {cmd} failed: {e}")
                return None

        tasks = [limited_cmd(cmd) for cmd in allowed_cmds]
        responses = await asyncio.gather(*tasks)

        for cmd, res in zip(allowed_cmds, responses):
            if res is not None:
                results[cmd] = res

        return results

    async def state(self) -> dict:
        """Send status command to mower."""
        result = await self.async_cmd("status")
        if result:
            status_val = None
            status_field = result.get("status")
            if isinstance(status_field, dict):
                status_val = status_field.get("status")
            elif isinstance(status_field, int):
                status_val = status_field
            else:
                # flattened forms from transform_json_to_single_depth, e.g. "status.status" or "status_status"
                status_val = result.get("status.status") or result.get("status_status")
            self.is_sleeping = status_val == 17

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

    async def async_reset_blades(self) -> dict:
        """Reset the mower blades."""
        return await self.async_cmd("reset_blades")
