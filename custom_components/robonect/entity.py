"""Base Robonect entity."""
from __future__ import annotations

from datetime import datetime
import logging
from typing import Any

from homeassistant.components import mqtt
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_TYPE
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo, EntityDescription
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import slugify

from . import RobonectDataUpdateCoordinator
from .const import (
    CONF_BRAND,
    CONF_MQTT_ENABLED,
    CONF_MQTT_TOPIC,
    DOMAIN,
    EVENT_ROBONECT_RESPONSE,
    NAME,
    VERSION,
)

_LOGGER = logging.getLogger(__name__)


class RobonectEntity(RestoreEntity):
    """Base Robonect entity."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        description: EntityDescription,
    ) -> None:
        """Initialize Robonect entities."""
        self.hass = hass
        self.dev_reg = dr.async_get(hass)
        self.entry = entry
        self.entity_description = description
        self.base_topic = entry.data[CONF_MQTT_TOPIC]
        self.topic = f"{self.base_topic}/{self.entity_description.key}"
        self.slug = (
            slugify(self.topic.replace("/", "_"))
            if self.entity_description.name is None
            else slugify(self.entity_description.name)
        )
        if self.entity_description.translation_key:
            self._attr_translation_key = self.entity_description.translation_key
        else:
            self._attr_translation_key = slugify(
                self.entity_description.key.replace("/", "_")
            )
        self._attr_unique_id = (
            f"{entry.entry_id}-{self.entity_description.rest_category}-{self.slug}"
        )
        self.device_identifier = {(DOMAIN, self.base_topic)}

        self._attr_device_info = DeviceInfo(
            identifiers=self.device_identifier,
            name=self.base_topic.title(),
            manufacturer=NAME,
            configuration_url=f"http://{entry.data[CONF_HOST]}",
            entry_type=DeviceEntryType.SERVICE,
            model=f"{entry.data[CONF_BRAND]} {entry.data[CONF_TYPE]}",
            sw_version=VERSION,
        )
        self.last_synced = datetime.now()

    def not_supported(self, feature):
        """Log a warning for a not supported feature instead of raising a standard exception."""
        _LOGGER.warning(f"{feature} not supported")

    async def async_fire_event(self, response):
        """Fire a bus event."""
        device = self.dev_reg.async_get_device(self.device_identifier)
        self.hass.bus.async_fire(
            EVENT_ROBONECT_RESPONSE,
            {"device_id": device.id, "client_response": response},
        )

    async def async_send_command(
        self,
        command: str,
        params: dict[str, Any] | list[Any] | None = None,
        **kwargs: Any,
    ) -> None:
        """Send a command to a Robonect mower."""

        if not command:
            _LOGGER.error(f"No command defined for entity {self.entity_id}")
        if params is None:
            params = {}
        if self.coordinator:
            _LOGGER.debug(
                f"[REST async_send_command] command: {command}, params: {params}"
            )
            try:
                response = await self.coordinator.client.async_cmd(command, params)
            except Exception as exception:
                response = {"successful": False, "exception": exception.message}
            await self.async_fire_event(
                response | {"command": command, "params": params}
            )
        elif self.entry.data[CONF_MQTT_ENABLED] is True and "topic" in kwargs:
            _LOGGER.debug(
                f"[MQTT async_send_command] MQTT publish to topic: {self.entry.data[CONF_MQTT_TOPIC]}/{kwargs['topic']} with payload: {command}"
            )
            await mqtt.async_publish(
                self.hass,
                f"{self.entry.data[CONF_MQTT_TOPIC]}/{kwargs['topic']}",
                command,
                qos=0,
                retain=False,
            )

    def update_ha_state(self):
        """Update HA state."""
        self.last_synced = datetime.now()
        self.async_write_ha_state()


class RobonectCoordinatorEntity(
    CoordinatorEntity[RobonectDataUpdateCoordinator], RestoreEntity
):
    """Robonect Coordinator entity."""

    def __init__(
        self,
        coordinator: RobonectDataUpdateCoordinator,
        description: EntityDescription,
    ) -> None:
        """Initialize Robonect entities."""
        super().__init__(coordinator)
        self.entity_description = description

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if len(self.coordinator.data):
            self.update_ha_state()
            return
