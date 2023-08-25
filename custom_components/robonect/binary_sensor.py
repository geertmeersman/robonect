"""Binary sensor platform for Robonect."""
from __future__ import annotations

import copy
import logging

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_MONITORED_VARIABLES,
    STATE_OFF,
    STATE_ON,
    STATE_UNAVAILABLE,
)
from homeassistant.core import HomeAssistant, State, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import RobonectDataUpdateCoordinator
from .const import ATTRIBUTION_REST, CONF_ATTRS_UNITS, CONF_REST_ENABLED, DOMAIN
from .definitions import BINARY_SENSORS, RobonectSensorEntityDescription
from .entity import RobonectCoordinatorEntity, RobonectEntity
from .utils import adapt_attributes, get_json_dict_path

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Robonect binary sensors from config entry."""

    if entry.data[CONF_REST_ENABLED] is True:
        _LOGGER.debug("Creating REST binary sensors")
        coordinator: RobonectDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
        entities: list[RobonectRestBinarySensor] = []
        if coordinator.data is not None:
            for description in BINARY_SENSORS:
                if not description.rest:
                    path = description.key
                else:
                    if description.rest == "$.none":
                        continue
                    if (
                        description.rest_category
                        not in entry.data[CONF_MONITORED_VARIABLES]
                    ):
                        continue
                    path = description.rest
                _LOGGER.debug(f"[sensor|async_setup_entry|adding] {path}")
                if description.array:
                    array = get_json_dict_path(
                        coordinator.data, description.rest_attrs.replace(".0", "")
                    )
                    for idx, item in enumerate(array):
                        _LOGGER.debug(f"Item in array: {item}")
                        desc = copy.copy(description)
                        desc.rest_attrs = description.rest_attrs.replace(
                            ".0", f".{idx}"
                        )
                        desc.key = description.key.replace(".0", f".{idx}")
                        entities.append(
                            RobonectRestBinarySensor(
                                hass,
                                entry,
                                coordinator=coordinator,
                                description=desc,
                            )
                        )
                else:
                    entities.append(
                        RobonectRestBinarySensor(
                            hass,
                            entry,
                            coordinator=coordinator,
                            description=description,
                        )
                    )
        async_add_entities(entities)


class RobonectBinarySensor(RobonectEntity, BinarySensorEntity):
    """Representation of a Robonect binary sensor."""

    entity_description: RobonectSensorEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        description: RobonectSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(hass, entry, description)
        self.entity_id = f"sensor.{self.slug}"
        self._state = None
        self._attributes = {}


class RobonectRestBinarySensor(RobonectCoordinatorEntity, RobonectBinarySensor):
    """Representation of a Robonect binary sensor that is updated via REST API."""

    _attr_attribution = ATTRIBUTION_REST

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        coordinator: RobonectDataUpdateCoordinator,
        description: RobonectSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, description)
        RobonectBinarySensor.__init__(self, hass, entry, description)
        self.category = self.entity_description.rest.split(".")[1]
        self.entity_description = description

    def handle_last_state(self, last_state: State | None) -> None:
        """Handle the last state."""
        if last_state is not None and last_state.state is not None:
            if last_state.state == STATE_ON:
                self._attr_is_on = True
            elif last_state.state == STATE_OFF:
                self._attr_is_on = False
            elif last_state.state == STATE_UNAVAILABLE:
                self._attr_available = False

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.set_extra_attributes()
        self.set_is_on()
        super()._handle_coordinator_update()

    def set_is_on(self):
        """Set the status of the from the coordinatorsensor."""
        if len(self.coordinator.data) and self.category in self.coordinator.data:
            state = get_json_dict_path(
                self.coordinator.data, self.entity_description.rest
            )
            if self.entity_description.rest == "$.health.health.alarm":
                for alarm in state:
                    if state[alarm]:
                        self._attr_is_on = True
                        return
                self._attr_is_on = False
                return
            if state is True:
                self._attr_is_on = True
            else:
                self._attr_is_on = False
        self._attr_is_on = False
        return

    def set_extra_attributes(self):
        """Set the attributes for the sensor from coordinator."""
        if len(self.coordinator.data) and self.category in self.coordinator.data:
            attributes = {
                "last_synced": self.last_synced,
                "category": self.category,
            }
            if self.entity_description.rest_attrs:
                attrs = get_json_dict_path(
                    self.coordinator.data, self.entity_description.rest_attrs
                )
                if attrs:
                    adapt_attributes(
                        attrs, self.category, self.entry.data[CONF_ATTRS_UNITS]
                    )
                    if not isinstance(attrs, list):
                        attributes.update(attrs)
            self._attr_extra_state_attributes = attributes

    @property
    def extra_state_attributes(self):
        """Return attributes for sensor."""
        self.set_extra_attributes()
        return self._attr_extra_state_attributes
