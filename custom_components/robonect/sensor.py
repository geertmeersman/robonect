"""Robonect sensor platform."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.components.sensor import SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ELECTRIC_CURRENT_MILLIAMPERE
from homeassistant.const import ELECTRIC_POTENTIAL_VOLT
from homeassistant.const import PERCENTAGE
from homeassistant.const import TEMP_CELSIUS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityDescription
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from . import RobonectDataUpdateCoordinator
from .const import DOMAIN
from .entity import RobonectEntity
from .models import RobonectItem
from .utils import log_debug


@dataclass
class RobonectSensorDescription(SensorEntityDescription):
    """Class to describe a Robonect sensor."""

    value_fn: Callable[[Any], StateType] | None = None


SENSOR_DESCRIPTIONS: list[SensorEntityDescription] = [
    RobonectSensorDescription(key="mower", icon="mdi:robot-mower"),
    RobonectSensorDescription(
        key="battery_percentage",
        icon="mdi:percent",
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
    ),
    RobonectSensorDescription(
        key="battery_voltage",
        icon="mdi:flash",
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
    ),
    RobonectSensorDescription(
        key="battery_capacity",
        icon="mdi:battery",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="mAh",
    ),
    RobonectSensorDescription(
        key="battery_charge_current",
        icon="mdi:current-ac",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=ELECTRIC_CURRENT_MILLIAMPERE,
    ),
    RobonectSensorDescription(
        key="battery_temperature",
        icon="mdi:temperature-celsius",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=TEMP_CELSIUS,
    ),
    RobonectSensorDescription(
        key="wlan_ap",
        icon="mdi:router-wireless",
    ),
    RobonectSensorDescription(
        key="wlan_station",
        icon="mdi:wifi",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
    ),
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Robonect sensors."""
    log_debug("[sensor|async_setup_entry|async_add_entities|start]")
    coordinator: RobonectDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    entities: list[RobonectSensor] = []

    SUPPORTED_KEYS = {
        description.key: description for description in SENSOR_DESCRIPTIONS
    }

    # log_debug(f"[sensor|async_setup_entry|async_add_entities|SUPPORTED_KEYS] {SUPPORTED_KEYS}")

    if coordinator.data is not None:
        for item in coordinator.data:
            item = coordinator.data[item]
            if description := SUPPORTED_KEYS.get(item.type):
                if item.native_unit_of_measurement is not None:
                    native_unit_of_measurement = item.native_unit_of_measurement
                else:
                    native_unit_of_measurement = description.native_unit_of_measurement
                sensor_description = RobonectSensorDescription(
                    key=str(item.key),
                    name=item.name,
                    value_fn=description.value_fn,
                    native_unit_of_measurement=native_unit_of_measurement,
                    icon=description.icon,
                )

                log_debug(f"[sensor|async_setup_entry|adding] {item.name}")
                entities.append(
                    RobonectSensor(
                        coordinator=coordinator,
                        description=sensor_description,
                        item=item,
                    )
                )
            else:
                log_debug(
                    f"[sensor|async_setup_entry|no support type found] {item.name}, type: {item.type}, keys: {SUPPORTED_KEYS.get(item.type)}",
                    True,
                )

        async_add_entities(entities)


class RobonectSensor(RobonectEntity, SensorEntity):
    """Representation of a Robonect sensor."""

    entity_description: RobonectSensorDescription

    def __init__(
        self,
        coordinator: RobonectDataUpdateCoordinator,
        description: EntityDescription,
        item: RobonectItem,
    ) -> None:
        """Set entity ID."""
        super().__init__(coordinator, description, item)
        self.entity_id = f"sensor.{DOMAIN}_{self.item.key}"

    @property
    def native_value(self) -> str:
        """Return the status of the sensor."""
        state = self.item.state

        if self.entity_description.value_fn:
            return self.entity_description.value_fn(state)

        return state

    @property
    def extra_state_attributes(self):
        """Return attributes for sensor."""
        if not self.coordinator.data:
            return {}
        attributes = {
            "last_synced": self.last_synced,
        }
        if len(self.item.extra_attributes) > 0:
            for attr in self.item.extra_attributes:
                attributes[attr] = self.item.extra_attributes[attr]
        return attributes
