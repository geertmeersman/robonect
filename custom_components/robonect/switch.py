"""Switch platform for Robonect."""
import copy
import logging
from typing import Any

from homeassistant.components import mqtt
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_MONITORED_VARIABLES
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity

from . import RobonectDataUpdateCoordinator
from .const import (
    ATTRIBUTION_MQTT,
    ATTRIBUTION_REST,
    CONF_ATTRS_UNITS,
    CONF_MQTT_ENABLED,
    CONF_MQTT_TOPIC,
    CONF_REST_ENABLED,
    DOMAIN,
)
from .definitions import SWITCHES, RobonectSwitchEntityDescription
from .entity import RobonectCoordinatorEntity, RobonectEntity
from .models import RobonectTimer
from .utils import adapt_attributes, get_json_dict_path, hex2weekdays

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up an Robonect device_tracker entry."""

    timer_topic = entry.data[CONF_MQTT_TOPIC] + "/mower/timer/"
    # Make sure MQTT integration is enabled and the client is available
    if entry.data[CONF_MQTT_ENABLED] is True:
        if not await mqtt.async_wait_for_mqtt_client(hass):
            _LOGGER.error("MQTT integration is not available")
            return

    if entry.data[CONF_REST_ENABLED] is False:
        _LOGGER.info("Ignoring the Timer switches as REST is not enabled")
        return

    coordinator: RobonectDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id][
        "coordinator"
    ]

    @callback
    def async_mqtt_event_received(msg: mqtt.ReceiveMessage) -> None:
        """Receive set latitude."""
        if entry.data[CONF_MQTT_TOPIC] in hass.data[DOMAIN][entry.entry_id]["switch"]:
            return
        topic = msg.topic.replace(timer_topic, "").split("/")
        if topic and topic[0].startswith("ch"):
            if isinstance(hass.data[DOMAIN][entry.entry_id]["switch"], set):
                hass.data[DOMAIN][entry.entry_id]["switch"] = {}
            if topic[0] not in hass.data[DOMAIN][entry.entry_id]["switch"]:
                hass.data[DOMAIN][entry.entry_id]["switch"].update(
                    {topic[0]: RobonectTimer(False, "", "", "", "")}
                )
                async_add_entities(
                    [
                        RobonectTimerSwitchEntity(
                            hass, entry, coordinator, None, topic[0].replace("ch", "")
                        )
                    ]
                )

        # hass.data[DOMAIN][entry.entry_id]["device_tracker"].add(entry.data[CONF_MQTT_TOPIC])

        # async_add_entities([RobonectMqttGPSEntity(hass, entry)])

    if entry.data[CONF_MQTT_ENABLED] is True:
        await mqtt.async_subscribe(
            hass,
            f"{timer_topic}#",
            async_mqtt_event_received,
            0,
        )
    elif entry.data[CONF_REST_ENABLED] is True:
        _LOGGER.debug("Creating REST sensors")
        entities: list[RobonectRestSwitch] = []
        if coordinator.data is not None:
            for description in SWITCHES:
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
                    if description.category not in entry.data[CONF_MONITORED_VARIABLES]:
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
                        desc.key = description.key.replace("/0", f"/{idx+1}")
                        entities.append(
                            RobonectRestSwitch(
                                hass,
                                entry,
                                coordinator=coordinator,
                                description=desc,
                                timer_id=idx,
                            )
                        )
                else:
                    entities.append(
                        RobonectRestSwitch(
                            hass,
                            entry,
                            coordinator=coordinator,
                            description=description,
                            timer_id=1,
                        )
                    )
        async_add_entities(entities)


class RobonectTimerSwitchEntity(RobonectEntity, SwitchEntity, RestoreEntity):
    """Represent a timer switch."""

    _attr_has_entity_name = True
    _attr_attribution = ATTRIBUTION_MQTT

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        coordinator: RobonectDataUpdateCoordinator,
        description: RobonectSwitchEntityDescription,
        timer_id: str,
    ):
        """Set up Switch entity."""
        self.coordinator = coordinator
        if description is None:
            self.entity_description = RobonectSwitchEntityDescription(
                key=f"timer {int(timer_id)+1}",
                category="timer",
                translation_key=f"timer_{int(timer_id)+1}",
                rest="$.timer.timer.0.enabled",
                icon="mdi:calendar-clock",
                entity_category=EntityCategory.DIAGNOSTIC,
            )
        else:
            self.entity_description = description
        self.entry = entry
        self.timer_id = timer_id
        super().__init__(hass, entry, self.entity_description)
        self.category = self.entity_description.category
        self.entity_id = f"switch.{self.slug}"
        self._attributes = None
        self._is_on = False
        self._weekdays = None
        self._weekdays_str = None
        self._start = None
        self._end = None

    @property
    def is_on(self) -> bool:
        """Return true if switch is on."""
        return self._is_on

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        if self.is_on is True:
            return
        await self.async_send_command(
            "timer", {"timer": int(self.timer_id) + 1, "enable": 1, "save": 1}
        )
        await self.coordinator.async_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        if self.is_on is False:
            return
        await self.async_send_command(
            "timer", {"timer": int(self.timer_id) + 1, "enable": 0, "save": 1}
        )
        await self.coordinator.async_refresh()

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes of the device."""
        return {
            "last_synced": self.last_synced,
            "category": self.category,
            "id": int(self.timer_id) + 1,
            "enabled": self._is_on,
            "start": self._start,
            "end": self._end,
            "weekdays": self._weekdays_str,
        }

    async def async_added_to_hass(self) -> None:
        """Subscribe to MQTT events."""
        await super().async_added_to_hass()
        timer_topic = (
            f"{self.entry.data[CONF_MQTT_TOPIC]}/mower/timer/ch{self.timer_id}"
        )

        if state := await self.async_get_last_state():
            self._state = state.state
            self._attributes = state.attributes
        else:
            _LOGGER.debug(f"Last state is none for {self._attr_unique_id}")

        @callback
        def timer_received(msg):
            """Handle new weekdays topic."""
            topic = msg.topic.replace(timer_topic + "/", "")
            if topic == "enable":
                self._is_on = True if msg.payload == "true" else False
            elif topic == "weekdays":
                self._weekdays = msg.payload
                self._weekdays_str = hex2weekdays(msg.payload)
            elif topic == "start":
                self._start = msg.payload
            elif topic == "end":
                self._end = msg.payload
            self.update_ha_state()

        if self.entry.data[CONF_MQTT_ENABLED] is True:
            await mqtt.async_subscribe(
                self.hass,
                f"{self.entry.data[CONF_MQTT_TOPIC]}/mower/timer/ch{self.timer_id}/#",
                timer_received,
                1,
            )


class RobonectRestSwitch(RobonectCoordinatorEntity, RobonectTimerSwitchEntity):
    """Representation of a Robonect REST switch."""

    _attr_attribution = ATTRIBUTION_REST

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        coordinator: RobonectDataUpdateCoordinator,
        description: RobonectSwitchEntityDescription,
        timer_id: str,
    ) -> None:
        """Initialize the sensor."""
        self.coordinator = coordinator
        super().__init__(coordinator, description)
        RobonectTimerSwitchEntity.__init__(
            self, hass, entry, coordinator, description, timer_id
        )
        self.set_state()

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
            self._is_on = state

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
                attrs = copy.copy(attrs)
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
