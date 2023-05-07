"""Models used by Robonect."""
from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import TypedDict


class RobonectConfigEntryData(TypedDict):
    """Config entry for the Robonect integration."""

    username: str | None
    password: str | None


@dataclass
class RobonectEnvironment:
    """Class to describe a Robonect environment."""

    api_endpoint: str


@dataclass
class RobonectItem:
    """Robonect item model."""

    name: str = ""
    key: str = ""
    type: str = ""
    state: str = ""
    device_key: str = ""
    device_name: str = ""
    device_model: str = ""
    data: dict = field(default_factory=dict)
    extra_attributes: dict = field(default_factory=dict)
    native_unit_of_measurement: str = None
