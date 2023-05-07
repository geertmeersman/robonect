"""Robonect API Client."""
from __future__ import annotations

from requests import (
    Session,
)

from .const import CONNECTION_RETRY
from .const import REQUEST_TIMEOUT
from .exceptions import BadCredentialsException
from .exceptions import RobonectException
from .exceptions import RobonectServiceException
from .models import RobonectItem
from .utils import format_entity_name
from .utils import log_debug
from .utils import wifi_signal_to_percentage


class RobonectClient:
    """Robonect client."""

    session: Session

    def __init__(
        self,
        session: Session | None = None,
        host: str | None = None,
        username: str | None = None,
        password: str | None = None,
    ) -> None:
        """Initialize RobonectClient."""
        self.session = session if session else Session()
        self.host = host
        self.api_endpoint = "http://" + host
        self.username = username
        self.password = password
        self.request_error = {}

    def request(
        self,
        url,
        caller="Not set",
        data=None,
        expected="200",
        log=False,
        retrying=False,
        connection_retry_left=CONNECTION_RETRY,
    ) -> dict:
        """Send a request to Robonect."""
        if data is None:
            log_debug(f"{caller} Calling GET {url}")
            response = self.session.get(
                url, auth=(self.username, self.password), timeout=REQUEST_TIMEOUT
            )
        else:
            log_debug(f"{caller} Calling POST {url} with {data}")
            response = self.session.post(
                url, data, auth=(self.username, self.password), timeout=REQUEST_TIMEOUT
            )

        log_debug(
            f"{caller} http status code = {response.status_code} (expecting {expected})"
        )
        if log:
            log_debug(f"{caller} response:\n{response.text}")
        if expected is not None and response.status_code != expected:
            if response.status_code == 404:
                self.request_error = response.json()
                return False
            if response.status_code == 401:
                raise BadCredentialsException(response.text)
            if (
                response.status_code != 403
                and response.status_code != 500
                and connection_retry_left > 0
                and not retrying
            ):
                raise RobonectServiceException(
                    f"[{caller}] Expecting HTTP {expected} | response HTTP {response.status_code}, response: {response.text}, Url: {response.url}"
                )
            log_debug(
                f"[RobonectClient|request] Received a HTTP {response.status_code}, nothing to worry about! We give it another try :-)"
            )
            self.login()
            response = self.request(
                url, caller, data, expected, log, True, connection_retry_left - 1
            )
        j = response.json()
        if j.get("successful"):
            return j
        raise RobonectServiceException(
            f"[{caller}] Response: {response.text}, Url: {response.url}"
        )

    def command(self, cmd=None):
        """Get command."""
        if cmd is None:
            return False
        response = self.request(
            f"{self.api_endpoint}/json?cmd={cmd}",
            f"[RobonectClient|{cmd}]",
            None,
            200,
        )
        return response

    def login(self) -> dict:
        """Start a new Robonect session with a user & password."""

        log_debug("[RobonectClient|login|start]")
        """Login process"""
        if self.username is None or self.password is None:
            raise BadCredentialsException()
        return self.command("name")

    def fetch_data(self):
        """Fetch Robonect data."""
        data = {}
        name = self.command("name")
        if not name:
            raise RobonectException()
        id = name.get("id")
        device_key = format_entity_name(f"Robonect {id}")
        device_name = f"Robonect {name.get('name')}"
        device_model = "Robonect"
        key = format_entity_name(f"{id} id")
        data[key] = RobonectItem(
            name=name.get("name"),
            key=key,
            type="mower",
            device_key=device_key,
            device_name=device_name,
            device_model=device_model,
            state=id,
            extra_attributes=name,
        )
        for battery in self.command("battery").get("batteries"):
            key = format_entity_name(f"{id} battery {battery.get('id')} status")
            data[key] = RobonectItem(
                name=f"Battery {battery.get('id')+1} Status",
                key=key,
                type="battery_percentage",
                device_key=device_key,
                device_name=device_name,
                device_model=device_model,
                state=battery.get("charge"),
            )
            key = format_entity_name(f"{id} battery {battery.get('id')} voltage")
            data[key] = RobonectItem(
                name=f"Battery {battery.get('id')+1} Voltage",
                key=key,
                type="battery_voltage",
                device_key=device_key,
                device_name=device_name,
                device_model=device_model,
                state=battery.get("voltage") / 1000,
            )
            key = format_entity_name(f"{id} battery {battery.get('id')} capacity")
            data[key] = RobonectItem(
                name=f"Battery {battery.get('id')+1} Capacity",
                key=key,
                type="battery_capacity",
                device_key=device_key,
                device_name=device_name,
                device_model=device_model,
                state=battery.get("capacity").get("remaining"),
            )
            key = format_entity_name(f"{id} battery {battery.get('id')} charge current")
            data[key] = RobonectItem(
                name=f"Battery {battery.get('id')+1} Charge current",
                key=key,
                type="battery_charge_current",
                device_key=device_key,
                device_name=device_name,
                device_model=device_model,
                state=battery.get("current"),
            )
            key = format_entity_name(f"{id} battery {battery.get('id')} temperature")
            data[key] = RobonectItem(
                name=f"Battery {battery.get('id')+1} Temperature",
                key=key,
                type="battery_temperature",
                device_key=device_key,
                device_name=device_name,
                device_model=device_model,
                state=battery.get("temperature") / 10,
            )
        wlan = self.command("wlan")
        key = format_entity_name(f"{id} wlan ap")
        data[key] = RobonectItem(
            name="WLAN AP",
            key=key,
            type="wlan_ap",
            device_key=device_key,
            device_name=device_name,
            device_model=device_model,
            state=wlan.get("ap").get("ssid"),
            extra_attributes=wlan.get("ap"),
        )
        key = format_entity_name(f"{id} wlan station")
        data[key] = RobonectItem(
            name=f"WLAN {wlan.get('station').get('ssid')}",
            key=key,
            type="wlan_station",
            device_key=device_key,
            device_name=device_name,
            device_model=device_model,
            state=wifi_signal_to_percentage(wlan.get("station").get("signal")),
            extra_attributes=wlan.get("station"),
        )
        return data
