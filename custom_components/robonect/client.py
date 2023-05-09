"""Robonect API Client."""
from __future__ import annotations

from requests import (
    Session,
)

from .const import CONNECTION_RETRY
from .const import REQUEST_TIMEOUT
from .const import SERVICE_JOB_AFTER_VALUES
from .const import SERVICE_JOB_CORRIDOR_VALUES
from .const import SERVICE_JOB_REMOTESTART_VALUES
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

    def command(self, cmd=None, params=""):
        """Get command."""
        if cmd is None:
            return False
        response = self.request(
            f"{self.api_endpoint}/json?cmd={cmd}&{params}",
            f"[RobonectClient|{cmd}]",
            None,
            200,
        )
        return response

    def start(self) -> bool:
        """Start the mower."""
        return self.command("start")

    def stop(self) -> bool:
        """Stop the mower."""
        return self.command("stop")

    def reboot(self) -> bool:
        """Reboot Robonect."""
        return self.command("service", params="service=reboot")

    def shutdown(self) -> bool:
        """Shutdown robonect."""
        return self.command("service", params="service=shutdown")

    def sleep(self) -> bool:
        """Make Robonect sleep."""
        return self.command("service", params="service=sleep")

    def sleeping(self) -> int:
        """Return raw status code"""
        status = self.command("status")
        return status.get("status").get("status") == 17

    def job(
        self,
        start: str,
        end: str,
        duration: int,
        after: str,
        remotestart: str,
        corridor: str,
    ) -> bool:
        """Place a mowing job."""
        params = ["mode=job"]
        if start is not None:
            params.append(f"start={start}")
        if end is not None:
            params.append(f"end={end}")
        if duration is not None:
            params.append(f"duration={duration}")
        if after is not None:
            try:
                index = SERVICE_JOB_AFTER_VALUES.index(after)
            except ValueError as error:
                raise RobonectException(error)
            params.append(f"after={index}")
        if remotestart is not None:
            try:
                index = SERVICE_JOB_REMOTESTART_VALUES.index(remotestart)
            except ValueError as error:
                raise RobonectException(error)
            params.append(f"remotestart={index}")
        if corridor is not None:
            try:
                if corridor == "Normal":
                    pass
                index = SERVICE_JOB_CORRIDOR_VALUES.index(corridor) - 1
            except ValueError as error:
                raise RobonectException(error)
            params.append(f"corridor={index}")
        self.command("mode", params="&".join(params))
        return True

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
        status = self.command("status")
        if not status:
            raise RobonectException()
        id = status.get("id")
        device_key = format_entity_name(f"Robonect {id}")
        device_name = f"Robonect {status.get('name')}"
        device_model = "Robonect"
        key = format_entity_name(f"{id} id")
        data[key] = RobonectItem(
            name=status.get("name"),
            key=key,
            type="mower",
            device_key=device_key,
            device_name=device_name,
            device_model=device_model,
            state=id,
        )
        status = self.command("status")
        key = format_entity_name(f"{id} status")
        data[key] = RobonectItem(
            name="Status",
            key=key,
            type="status",
            device_key=device_key,
            device_name=device_name,
            device_model=device_model,
            state=f"raw_{status.get('status').get('status')}",
            extra_attributes=status.get("status"),
        )
        key = format_entity_name(f"{id} mode")
        data[key] = RobonectItem(
            name="Mode",
            key=key,
            type="mode",
            device_key=device_key,
            device_name=device_name,
            device_model=device_model,
            state=f"raw_{status.get('status').get('mode')}",
            extra_attributes=status.get("status"),
        )
        key = format_entity_name(f"{id} distance")
        data[key] = RobonectItem(
            name="Distance from home",
            key=key,
            type="distance",
            device_key=device_key,
            device_name=device_name,
            device_model=device_model,
            state=status.get("status").get("distance"),
        )
        key = format_entity_name(f"{id} stopped")
        data[key] = RobonectItem(
            name="Stopped",
            key=key,
            type="stopped",
            device_key=device_key,
            device_name=device_name,
            device_model=device_model,
            state=status.get("status").get("stopped"),
        )
        key = format_entity_name(f"{id} hours")
        data[key] = RobonectItem(
            name="Operation hours",
            key=key,
            type="hours",
            device_key=device_key,
            device_name=device_name,
            device_model=device_model,
            state=status.get("status").get("hours"),
        )
        key = format_entity_name(f"{id} duration")
        data[key] = RobonectItem(
            name="Status duration",
            key=key,
            type="seconds",
            device_key=device_key,
            device_name=device_name,
            device_model=device_model,
            state=status.get("status").get("duration"),
        )
        key = format_entity_name(f"{id} timer next start")
        if "next" in status.get("timer"):
            next_start = f"{status.get('timer').get('next').get('date')} {status.get('timer').get('next').get('time')}"
        else:
            next_start = ""
        data[key] = RobonectItem(
            name="Next start",
            key=key,
            type="timestamp",
            device_key=device_key,
            device_name=device_name,
            device_model=device_model,
            state=next_start,
        )
        key = format_entity_name(f"{id} timer status")
        data[key] = RobonectItem(
            name="Timer status",
            key=key,
            type="timer_status",
            device_key=device_key,
            device_name=device_name,
            device_model=device_model,
            state=f"raw_{status.get('timer').get('status')}",
        )
        key = format_entity_name(f"{id} blades quality")
        data[key] = RobonectItem(
            name="Blades quality",
            key=key,
            type="blades_quality",
            device_key=device_key,
            device_name=device_name,
            device_model=device_model,
            state=status.get("blades").get("quality"),
        )
        key = format_entity_name(f"{id} blades hours")
        data[key] = RobonectItem(
            name="Blades hours",
            key=key,
            type="hours",
            device_key=device_key,
            device_name=device_name,
            device_model=device_model,
            state=status.get("blades").get("hours"),
        )
        key = format_entity_name(f"{id} blades days")
        data[key] = RobonectItem(
            name="Blades days",
            key=key,
            type="days",
            device_key=device_key,
            device_name=device_name,
            device_model=device_model,
            state=status.get("blades").get("days"),
        )
        key = format_entity_name(f"{id} health temperature")
        data[key] = RobonectItem(
            name="Temperature",
            key=key,
            type="temperature",
            device_key=device_key,
            device_name=device_name,
            device_model=device_model,
            state=status.get("health").get("temperature"),
        )
        key = format_entity_name(f"{id} health humidity")
        data[key] = RobonectItem(
            name="Humidity",
            key=key,
            type="humidity",
            device_key=device_key,
            device_name=device_name,
            device_model=device_model,
            state=status.get("health").get("humidity"),
        )
        key = format_entity_name(f"{id} clock")
        data[key] = RobonectItem(
            name="Clock",
            key=key,
            type="timestamp",
            device_key=device_key,
            device_name=device_name,
            device_model=device_model,
            state=f"{status.get('clock').get('date')} {status.get('clock').get('time')}",
        )
        if status.get("status").get("status") != 17:
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
                key = format_entity_name(
                    f"{id} battery {battery.get('id')} charge current"
                )
                data[key] = RobonectItem(
                    name=f"Battery {battery.get('id')+1} Charge current",
                    key=key,
                    type="battery_charge_current",
                    device_key=device_key,
                    device_name=device_name,
                    device_model=device_model,
                    state=battery.get("current"),
                )
                key = format_entity_name(
                    f"{id} battery {battery.get('id')} temperature"
                )
                data[key] = RobonectItem(
                    name=f"Battery {battery.get('id')+1} Temperature",
                    key=key,
                    type="temperature",
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
            version = self.command("version")
            key = format_entity_name(f"{id} version mower")
            data[key] = RobonectItem(
                name="Hardware",
                key=key,
                type="date",
                device_key=device_key,
                device_name=device_name,
                device_model=device_model,
                state=version.get("mower").get("hardware").get("production"),
                extra_attributes=version.get("mower"),
            )
            key = format_entity_name(f"{id} version mower")
            data[key] = RobonectItem(
                name="Hardware Production",
                key=key,
                type="date",
                device_key=device_key,
                device_name=device_name,
                device_model=device_model,
                state=version.get("mower").get("hardware").get("production"),
                extra_attributes=version.get("mower"),
            )
            key = format_entity_name(f"{id} version serial")
            data[key] = RobonectItem(
                name="Hardware Serial",
                key=key,
                type="version",
                device_key=device_key,
                device_name=device_name,
                device_model=device_model,
                state=version.get("serial"),
            )
            key = format_entity_name(f"{id} version bootloader")
            data[key] = RobonectItem(
                name="Bootloader version",
                key=key,
                type="version",
                device_key=device_key,
                device_name=device_name,
                device_model=device_model,
                state=version.get("bootloader").get("version"),
                extra_attributes=version.get("bootloader"),
            )
            key = format_entity_name(f"{id} version wlan")
            data[key] = RobonectItem(
                name="Wlan version",
                key=key,
                type="version",
                device_key=device_key,
                device_name=device_name,
                device_model=device_model,
                state=version.get("wlan").get("at-version"),
                extra_attributes=version.get("bootloader"),
            )
            key = format_entity_name(f"{id} version application")
            data[key] = RobonectItem(
                name="Application version",
                key=key,
                type="version",
                device_key=device_key,
                device_name=device_name,
                device_model=device_model,
                state=version.get("application").get("version"),
                extra_attributes=version.get("application"),
            )
            key = format_entity_name(f"{id} version application")
            data[key] = RobonectItem(
                name="Application version",
                key=key,
                type="version",
                device_key=device_key,
                device_name=device_name,
                device_model=device_model,
                state=version.get("application").get("version"),
                extra_attributes=version.get("application"),
            )
            # timer = self.command("timer")
            hour = self.command("hour")
            key = format_entity_name(f"{id} mowing time")
            data[key] = RobonectItem(
                name="Mowing time",
                key=key,
                type="hours",
                device_key=device_key,
                device_name=device_name,
                device_model=device_model,
                state=hour.get("general").get("mow"),
            )
            key = format_entity_name(f"{id} search time")
            data[key] = RobonectItem(
                name="Search time",
                key=key,
                type="hours",
                device_key=device_key,
                device_name=device_name,
                device_model=device_model,
                state=hour.get("general").get("search"),
            )
            key = format_entity_name(f"{id} charging time")
            data[key] = RobonectItem(
                name="Charging time",
                key=key,
                type="hours",
                device_key=device_key,
                device_name=device_name,
                device_model=device_model,
                state=hour.get("general").get("charge"),
            )
            key = format_entity_name(f"{id} Full charges")
            data[key] = RobonectItem(
                name="Full charges",
                key=key,
                type="counter",
                device_key=device_key,
                device_name=device_name,
                device_model=device_model,
                state=hour.get("general").get("charges"),
            )
            error = self.command("error")
            key = format_entity_name(f"{id} faults")
            data[key] = RobonectItem(
                name="Faults",
                key=key,
                type="counter",
                device_key=device_key,
                device_name=device_name,
                device_model=device_model,
                state=hour.get("general").get("errors"),
                extra_attributes=error,
            )
            key = format_entity_name(f"{id} data since")
            data[key] = RobonectItem(
                name="Data since",
                key=key,
                type="timestamp",
                device_key=device_key,
                device_name=device_name,
                device_model=device_model,
                state=hour.get("general").get("since"),
            )
            key = format_entity_name(f"{id} last error")
            data[key] = RobonectItem(
                name="Last error",
                key=key,
                type="error",
                device_key=device_key,
                device_name=device_name,
                device_model=device_model,
                state=error.get("errors")[1].get("error_message"),
                extra_attributes=error.get("errors")[1]
                | {"Fault-Memory": error.get("errors")},
            )
        return data
