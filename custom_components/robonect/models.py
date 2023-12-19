"""Models used by Robonect."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TypedDict


class RobonectConfigEntryData(TypedDict):
    """Config entry for the Robonect integration."""

    mqtt_enabled: bool | None
    mqtt_topic: str | None
    host: str | None
    username: str | None
    password: str | None
    type: str | None
    brand: str | None
    rest_enabled: bool | None
    monitored_variables: dict | None
    scan_interval: int | None
    attributes_units: bool | True
    winter_mode: bool | True


@dataclass
class RobonectEnvironment:
    """Class to describe a Robonect environment."""

    api_endpoint: str


@dataclass
class RobonectTimer:
    """Robonect timer model."""

    enable: bool | False
    weekdays: str | None
    weekdays_dict: dict | None
    start: str | None
    end: str | None


@dataclass
class RobonectItem:
    """Robonect item model."""

    platform: str = ""
    name: str = ""
    key: str = ""
    type: str = ""
    state: str = ""
    device_key: str = ""
    device_name: str = ""
    device_model: str = ""
    serial: str = ""
    firmware: str = ""
    status: dict = field(default_factory=dict)
    data: dict = field(default_factory=dict)
    extra_attributes: dict = field(default_factory=dict)
    native_unit_of_measurement: str = None


@dataclass
class RobonectSensorItem(RobonectItem):
    """Robonect sensor model."""

    platform: str = "sensor"


@dataclass
class RobonectVacuumItem(RobonectItem):
    """Robonect Vacuum model."""

    platform: str = "vacuum"
