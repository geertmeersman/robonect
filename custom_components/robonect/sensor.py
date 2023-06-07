"""Support for Robonect through MQTT."""
from __future__ import annotations

import copy
import logging

from homeassistant.components import mqtt
from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_MONITORED_VARIABLES,
    STATE_UNAVAILABLE,
    STATE_UNKNOWN,
)
from homeassistant.core import Event, HomeAssistant, callback
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import slugify

from . import RobonectDataUpdateCoordinator
from .const import (
    ATTRIBUTION_MQTT,
    ATTRIBUTION_REST,
    CONF_ATTRS_UNITS,
    CONF_MQTT_ENABLED,
    CONF_MQTT_TOPIC,
    CONF_REST_ENABLED,
    DOMAIN,
    EVENT_ROBONECT_RESPONSE,
)
from .definitions import SENSORS, RobonectSensorEntityDescription
from .entity import RobonectCoordinatorEntity, RobonectEntity
from .utils import (
    adapt_attributes,
    filter_out_units,
    get_json_dict_path,
    unix_to_datetime,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Robonect sensors from config entry."""

    # Make sure MQTT integration is enabled and the client is available
    if entry.data[CONF_MQTT_ENABLED] is True:
        if not await mqtt.async_wait_for_mqtt_client(hass):
            _LOGGER.error("MQTT integration is not available")
            return

    added_entities = []

    @callback
    def async_mqtt_event_received(msg: mqtt.ReceiveMessage) -> None:
        """Process events as sensors."""
        slug = slugify(msg.topic.replace("/", "_"))
        entity_id = f"sensor.{slug}"
        if slug in hass.data[DOMAIN]["sensor"]:
            return
        hass.data[DOMAIN]["sensor"].add(slug)

        if entity_id not in added_entities:
            description_key = msg.topic.replace(f"{entry.data[CONF_MQTT_TOPIC]}/", "")
            if description_key[0] != ".":
                _LOGGER.debug(
                    f"[async_mqtt_event_received] Adding entity {entity_id} (MQTT Topic {msg.topic})"
                )
                async_add_entities([RobonectMqttSensor(hass, entry, description_key)])
                added_entities.append(entity_id)

    if entry.data[CONF_MQTT_ENABLED] is True:
        _LOGGER.debug(f"MQTT Subscribing to {entry.data[CONF_MQTT_TOPIC]}/#")
        await mqtt.async_subscribe(
            hass, f"{entry.data[CONF_MQTT_TOPIC]}/#", async_mqtt_event_received, 0
        )

    if entry.data[CONF_REST_ENABLED] is True:
        _LOGGER.debug("Creating REST sensors")
        coordinator: RobonectDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
        entities: list[RobonectRestSensor] = []
        entities.append(
            RobonectServiceSensor(
                hass,
                entry,
                description=RobonectSensorEntityDescription(
                    key=".service/call/result",
                    rest="$.service.call.result",
                    icon="mdi:book-information-variant",
                    entity_category=EntityCategory.DIAGNOSTIC,
                    rest_category="NONE",
                ),
            )
        )
        if coordinator.data is not None:
            for description in SENSORS:
                if not description.rest:
                    path = description.key
                else:
                    if entry.data[CONF_MQTT_ENABLED] and description.key[0] != ".":
                        _LOGGER.debug(
                            f"[sensor|async_setup_entry|skipping since MQTT] {description.key}"
                        )
                        continue
                    if description.rest == "$.none":
                        continue
                    if (
                        description.rest_category
                        not in entry.data[CONF_MONITORED_VARIABLES]
                    ):
                        continue
                    path = description.rest
                _LOGGER.debug(f"[async_setup_entry|REST|adding] {path}")
                if description.array:
                    array = get_json_dict_path(
                        coordinator.data, description.rest_attrs.replace(".0", "")
                    )
                    for idx, item in enumerate(array):
                        _LOGGER.debug(
                            f"[async_setup_entry|REST|adding] Item in array: {item}"
                        )
                        desc = copy.copy(description)
                        desc.rest = description.rest.replace(".0", f".{idx}")
                        desc.rest_attrs = description.rest_attrs.replace(
                            ".0", f".{idx}"
                        )
                        desc.key = description.key.replace("/0", f"/{idx}")
                        entities.append(
                            RobonectRestSensor(
                                hass,
                                entry,
                                coordinator=coordinator,
                                description=desc,
                            )
                        )
                else:
                    entities.append(
                        RobonectRestSensor(
                            hass,
                            entry,
                            coordinator=coordinator,
                            description=description,
                        )
                    )
        async_add_entities(entities)


class RobonectSensor(RobonectEntity, SensorEntity):
    """Representation of a Robonect sensor."""

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

    async def async_added_to_hass(self) -> None:
        """Subscribe to MQTT events."""

        @callback
        def message_received(message):
            """Handle new MQTT messages."""
            if message.payload == "":
                self._state = None
            else:
                if self.entity_description.native_unit_of_measurement:
                    state = filter_out_units(message.payload)
                else:
                    state = message.payload
                if self.entity_description.state is not None:
                    self._state = self.entity_description.state(state, self.hass)
                    self._attributes = {"Raw state": message.payload}
                else:
                    self._state = state
            self.update_ha_state()

        if state := await self.async_get_last_state():
            if state.state in [STATE_UNAVAILABLE, STATE_UNKNOWN]:
                _LOGGER.debug(f"Restoring state for: {self.entity_id} => {state.state}")
            if (
                state.state is not STATE_UNAVAILABLE
                and state.as_dict().get("attributes").get("device_class")
                == SensorDeviceClass.TIMESTAMP
            ):
                if state.state is STATE_UNKNOWN:
                    self._state = None
                else:
                    self._state = unix_to_datetime(
                        state.as_dict().get("attributes").get("unix"), self.hass
                    )
            else:
                if state.state is STATE_UNAVAILABLE:
                    self._state = None
                else:
                    self._state = state.state
            self._attributes = state.attributes
        else:
            _LOGGER.debug(f"Last state is none for {self._attr_unique_id}")

        if self.entry.data[CONF_MQTT_ENABLED] is True:
            await mqtt.async_subscribe(self.hass, self.topic, message_received, 1)

        await super().async_added_to_hass()

        return


class RobonectMqttSensor(RobonectSensor):
    """Representation of a Robonect sensor that is updated via MQTT."""

    _attr_attribution = ATTRIBUTION_MQTT

    def __init__(
        self, hass: HomeAssistant, entry: ConfigEntry, description_key: str
    ) -> None:
        """Initialize the sensor."""
        self._description_key = description_key
        self.entity_description = self.get_mqtt_description()
        self._attr_entity_registry_enabled_default = self.get_mqtt_description(True)
        super().__init__(hass, entry, self.entity_description)

    def get_mqtt_description(
        self, return_bool=False
    ) -> RobonectSensorEntityDescription:
        """Return the RobonectSensorEntityDescription for the description_key."""
        for description in SENSORS:
            if description.key == self._description_key:
                if return_bool:
                    return True
                return description
        if return_bool:
            return False
        return RobonectSensorEntityDescription(
            key=self._description_key,
            icon="mdi:help",
            entity_category=EntityCategory.DIAGNOSTIC,
        )

    @property
    def native_value(self):
        """Return the status of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return attributes for sensor."""
        self._attributes |= {
            "last_synced": self.last_synced,
        }
        return self._attributes


class RobonectRestSensor(RobonectCoordinatorEntity, RobonectSensor):
    """Representation of a Robonect sensor that is updated via REST API."""

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
        RobonectSensor.__init__(self, hass, entry, description)
        self.category = self.entity_description.rest.split(".")[1]
        self.entity_description = description

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.set_extra_attributes()
        self.set_state()
        super()._handle_coordinator_update()

    def set_state(self):
        """Set the status of the sensor from the coordinatorsensor."""
        if len(self.coordinator.data) and self.category in self.coordinator.data:
            state = get_json_dict_path(
                self.coordinator.data, self.entity_description.rest
            )
            if self.entity_description.rest == "$.health.health.alarm":
                for alarm in state:
                    if state[alarm]:
                        return True
                return False
            if state is not None:
                state = copy.copy(state)
                if isinstance(state, str):
                    state = filter_out_units(state)
                if self.entity_description.device_class == SensorDeviceClass.TIMESTAMP:
                    state = unix_to_datetime(state, self.coordinator.hass)
                elif self.entity_description.device_class == SensorDeviceClass.VOLTAGE:
                    state = round(state / 1000, 1)
                elif self.entity_description.rest == "$.status.status.duration":
                    state = state / 60
                self._state = state

    @property
    def native_value(self):
        """Return the status of the sensor."""
        return self._state

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


class RobonectServiceSensor(RobonectSensor):
    """Representation of a Robonect sensor that is updated via REST API."""

    _attr_attribution = ATTRIBUTION_REST

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        description: RobonectSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(hass, entry, description)
        self.category = self.entity_description.rest.split(".")[1]
        self.entity_description = description
        self._attributes = {}
        self._state = "SUCCESS"
        hass.bus.async_listen(EVENT_ROBONECT_RESPONSE, self.update_busevent)

    def update_busevent(self, event: Event):
        """Update sensor on bus event."""
        client_response = event.data.get("client_response")
        self._attributes = client_response
        self._state = client_response.get("successful")
        self.update_ha_state()
        _LOGGER.debug(f"Event client_response: {client_response}")

    @property
    def native_value(self):
        """Return the status of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return attributes for sensor."""
        return self._attributes | {"timestamp": self.last_synced}
