"""Robonect vacuum platform."""
from __future__ import annotations

from dataclasses import dataclass
import logging
from typing import Any

from homeassistant.components import mqtt
from homeassistant.components.vacuum import StateVacuumEntity, VacuumEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_BATTERY_LEVEL
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import EntityDescription
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.icon import icon_for_battery_level
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.util import slugify

from . import RobonectDataUpdateCoordinator
from .const import (
    ATTRIBUTION_MQTT,
    ATTRIBUTION_REST,
    CONF_MQTT_ENABLED,
    CONF_MQTT_TOPIC,
    CONF_REST_ENABLED,
    DOMAIN,
)
from .entity import RobonectCoordinatorEntity, RobonectEntity
from .utils import filter_out_units, get_json_dict_path, unix_to_datetime

_LOGGER = logging.getLogger(__name__)

MQTT_ATTRIBUTES = [
    "status_plain",
    "status_duration",
    "distance",
    "statistic_hours",
    "timer_next_unix",
    "blades_quality",
    "mode",
]


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up an Robonect vacuum entry."""

    # Make sure MQTT integration is enabled and the client is available
    if entry.data[CONF_MQTT_ENABLED] is True:
        if not await mqtt.async_wait_for_mqtt_client(hass):
            _LOGGER.error("MQTT integration is not available")
            return

    @callback
    def async_mqtt_event_received(msg: mqtt.ReceiveMessage) -> None:
        """Receive set latitude."""
        if entry.data[CONF_MQTT_TOPIC] in hass.data[DOMAIN][entry.entry_id]["vacuum"]:
            return

        _LOGGER.debug("async_mqtt_event_received | Adding MQTT Vacuum")
        hass.data[DOMAIN][entry.entry_id]["vacuum"].add(entry.data[CONF_MQTT_TOPIC])

        async_add_entities([RobonectMqttVacuumEntity(hass, entry)])

    if entry.data[CONF_MQTT_ENABLED] is True:
        _LOGGER.debug("Creating MQTT Vacuum")
        await mqtt.async_subscribe(
            hass, f"{entry.data[CONF_MQTT_TOPIC]}/mqtt", async_mqtt_event_received, 0
        )
    elif entry.data[CONF_REST_ENABLED] is True:
        _LOGGER.debug("Creating REST Vacuum")
        coordinator: RobonectDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id][
            "coordinator"
        ]
        if coordinator.data is not None and "status" in coordinator.data:
            async_add_entities(
                [
                    RobonectRestVacuumEntity(
                        hass,
                        entry,
                        coordinator,
                    )
                ]
            )


@dataclass
class VacuumEntityDescription(EntityDescription):
    """Vacuum entity description for Robonect."""

    category: str | None = None


class RobonectVacuumEntity(RobonectEntity, StateVacuumEntity, RestoreEntity):
    """Representation of a Robonect vacuum."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:robot-mower"
    _attr_supported_features = (
        VacuumEntityFeature.BATTERY
        | VacuumEntityFeature.RETURN_HOME
        | VacuumEntityFeature.STOP
        | VacuumEntityFeature.START
        | VacuumEntityFeature.STATE
        | VacuumEntityFeature.STATUS
        | VacuumEntityFeature.TURN_OFF
        | VacuumEntityFeature.SEND_COMMAND
    )

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
    ):
        """Set up Vacuum entity."""
        self.coordinator = None
        self.entity_description = VacuumEntityDescription(
            key="automower",
            icon="mdi:robot-mower",
            category="NONE",
        )
        self.entry = entry
        super().__init__(hass, entry, self.entity_description)
        self._attr_translation_key = "automower"
        self.entity_id = f"vacuum.{self.base_topic}_robonect"
        self._battery = None
        self._attributes = {}
        self._attr_state = None
        self._attr_status = None

    @property
    def extra_state_attributes(self) -> dict:
        """Return the specific state attributes of this mower."""
        if self._attr_status:
            return {
                "substatus": self._attr_status,
            } | self._attributes
        return self._attributes | {"last_synced": self.last_synced}

    @property
    def battery_level(self) -> int | None:
        """Return the battery level of the device.

        Percentage from 0-100.
        """
        return self._battery

    @property
    def battery_icon(self) -> str:
        """Return the battery icon for the Robonect mower."""
        charging = bool(self.state == "Charging")

        return icon_for_battery_level(
            battery_level=self.battery_level, charging=charging
        )

    async def async_turn_off(self) -> None:
        """Start."""
        await self.async_send_command("service", {"shutdown": 1})

    async def async_start(self) -> None:
        """Start."""
        await self.async_send_command("start", {}, topic="control")

    async def async_stop(self) -> None:
        """Stop."""
        await self.async_send_command("stop", {}, topic="control")

    async def async_return_to_base(self) -> None:
        """Return home."""
        if self.entry.data[CONF_MQTT_ENABLED] is True:
            await self.async_send_command("home", {}, topic="control/mode")
        else:
            await self.async_send_command("mode", {"mode": "home"})

    # Not supported services
    def clean_spot(self, **kwargs: Any) -> None:
        """Perform a spot clean-up."""
        self.not_supported("clean_spot")

    def locate(self, **kwargs: Any) -> None:
        """Locate the Robonect mower."""
        self.not_supported("locate")

    def set_fan_speed(self, fan_speed: str, **kwargs: Any) -> None:
        """Set fan speed."""
        self.not_supported("set_fan_speed")

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the vacuum on and start cleaning."""
        self.not_supported("turn_on")

    async def async_start_pause(self, **kwargs: Any) -> None:
        """Start, pause or resume the cleaning task."""
        self.not_supported("start_pause")

    def pause(self) -> None:
        """Pause the cleaning task."""
        self.not_supported("pause")

    def update_rest_state(self):
        """Update state based on REST State."""
        if self.coordinator is None:
            return False
        if len(self.coordinator.data) and "status" in self.coordinator.data:
            status = self.coordinator.data.get("status")
            self._attr_state = status.get("status").get("status")
            self._battery = int(status.get("status").get("battery"))
            attr_states = {
                "status_duration": "$.status.status.duration",
                "distance": "$.status.status.distance",
                "statistic_hours": "$.status.status.hours",
                "timer_next_unix": "$.status.timer.next.unix",
                "blades_quality": "$.status.blades.quality",
                "mode": "$.status.status.mode",
            }
            self._attributes = {}
            for key, value in attr_states.items():
                state = get_json_dict_path(self.coordinator.data, value)
                if state is not None:
                    if key == "timer_next_unix":
                        state = unix_to_datetime(state, self.coordinator.hass)
                    elif key == "status_duration":
                        state = round(state / 60)
                    self._attributes |= {key: state}
            self.update_ha_state()
            return True
        return False

    async def async_added_to_hass(self) -> None:
        """Subscribe to MQTT events."""

        @callback
        def battery_received(message):
            """Handle battery topic."""
            self._battery = int(filter_out_units(message.payload))
            self.update_ha_state()

        @callback
        def state_received(message):
            """Handle state topic."""
            self._attr_state = message.payload
            self.update_ha_state()

        @callback
        def substatus_received(message):
            """Handle substatus topic."""
            self._attr_status = message.payload
            self.update_ha_state()

        @callback
        def topic_received(message):
            """Handle topic."""
            slug = slugify(
                message.topic.replace(
                    f"{self.entry.data[CONF_MQTT_TOPIC]}/mower/", ""
                ).replace("/", "_")
            )
            if slug in MQTT_ATTRIBUTES:
                payload = message.payload
                if slug == "timer_next_unix":
                    payload = unix_to_datetime(message.payload, self.hass)
                self._attributes |= {slug: payload}

        if self.entry.data[CONF_MQTT_ENABLED] is True:
            await mqtt.async_subscribe(
                self.hass,
                f"{self.entry.data[CONF_MQTT_TOPIC]}/mower/battery/charge",
                battery_received,
                1,
            )
            await mqtt.async_subscribe(
                self.hass,
                f"{self.entry.data[CONF_MQTT_TOPIC]}/mower/status",
                state_received,
                1,
            )
            await mqtt.async_subscribe(
                self.hass,
                f"{self.entry.data[CONF_MQTT_TOPIC]}/mower/substatus",
                substatus_received,
                1,
            )
            await mqtt.async_subscribe(
                self.hass,
                f"{self.entry.data[CONF_MQTT_TOPIC]}/mower/#",
                topic_received,
                1,
            )
        # Don't restore if status is fetched from coordinator data
        if self.entry.data[CONF_MQTT_ENABLED] is False and self.update_rest_state():
            await super().async_added_to_hass()
            return

        if (state := await self.async_get_last_state()) is None:
            self._attr_state = None
            self._battery = None
            self._attributes = {}
            await super().async_added_to_hass()
            return

        attr = state.attributes
        self._attributes = attr
        self._battery = attr.get(ATTR_BATTERY_LEVEL)
        await super().async_added_to_hass()


class RobonectMqttVacuumEntity(RobonectVacuumEntity):
    """Represent an MQTT tracked device."""

    _attr_attribution = ATTRIBUTION_MQTT

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(hass, entry)


class RobonectRestVacuumEntity(RobonectCoordinatorEntity, RobonectVacuumEntity):
    """Represent a REST tracked device."""

    _attr_attribution = ATTRIBUTION_REST

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        coordinator: RobonectDataUpdateCoordinator,
    ) -> None:
        """Initialize the sensor."""
        RobonectVacuumEntity.__init__(self, hass, entry)
        super().__init__(coordinator, self.entity_description)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""

        self.update_rest_state()
        return
