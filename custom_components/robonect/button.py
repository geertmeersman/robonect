"""Button platform for Robonect."""

from __future__ import annotations

from dataclasses import dataclass
import logging

from homeassistant.components import mqtt
from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.entity_platform import AddEntitiesCallback
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
from .entity import RobonectEntity

_LOGGER = logging.getLogger(__name__)


@dataclass
class RobonectButtonEntityDescription(ButtonEntityDescription):
    """Sensor entity description for Robonect."""

    category: str | None = None
    cmd: str | None = None
    params: dict | None = None
    topic: str | None = None
    key: str | None = None
    icon: str | None = None


BUTTON_TYPES = (
    RobonectButtonEntityDescription(
        key="error_reset",
        icon="mdi:backup-restore",
        cmd="error",
        params={"reset": 1},
        category="NONE",
    ),
    RobonectButtonEntityDescription(
        key="home",
        icon="mdi:home-import-outline",
        topic="control/mode",
        cmd="mode",
        params={"mode": "home"},
        category="NONE",
    ),
    RobonectButtonEntityDescription(
        key="eod",
        icon="mdi:weather-sunset-down",
        topic="control/mode",
        cmd="mode",
        params={"mode": "eod"},
        category="NONE",
    ),
    RobonectButtonEntityDescription(
        key="stop",
        icon="mdi:stop",
        topic="control",
        cmd="stop",
        category="NONE",
    ),
    RobonectButtonEntityDescription(
        key="reboot",
        icon="mdi:restart",
        cmd="service",
        params={"reboot": 1},
        category="NONE",
    ),
    RobonectButtonEntityDescription(
        key="shutdown",
        icon="mdi:power",
        cmd="service",
        params={"shutdown": 1},
        category="NONE",
    ),
    RobonectButtonEntityDescription(
        key="sleep",
        icon="mdi:sleep",
        cmd="service",
        params={"sleep": 1},
        category="NONE",
    ),
    RobonectButtonEntityDescription(
        key="start",
        icon="mdi:play",
        topic="control",
        cmd="start",
        category="NONE",
    ),
    RobonectButtonEntityDescription(
        key="auto",
        icon="mdi:refresh-auto",
        topic="control/mode",
        cmd="mode",
        params={"mode": "auto"},
        category="NONE",
    ),
    RobonectButtonEntityDescription(
        key="man",
        icon="mdi:hand-clap",
        topic="control/mode",
        cmd="mode",
        params={"mode": "man"},
        category="NONE",
    ),
)


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

    entity_reg: er.EntityRegistry = er.async_get(hass)

    entities = []
    if entry.data[CONF_REST_ENABLED] is True:
        coordinator: RobonectDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id][
            "coordinator"
        ]
    for description in BUTTON_TYPES:
        added = False
        if entry.data[CONF_MQTT_ENABLED] is True and description.topic is not None:
            entities.append(RobonectMqttButton(hass, entry, description))
            added = True
        if entry.data[CONF_REST_ENABLED] is True:
            coordinator: RobonectDataUpdateCoordinator = hass.data[DOMAIN][
                entry.entry_id
            ]["coordinator"]
            if (
                entry.data[CONF_MQTT_ENABLED] is True and description.topic is None
            ) or entry.data[CONF_MQTT_ENABLED] is False:
                added = True
                entities.append(
                    RobonectRestButton(hass, entry, coordinator, description)
                )
        if not added:
            topic = f"{entry.data[CONF_MQTT_TOPIC]}/{description.key}"
            slug = slugify(topic.replace("/", "_"))
            if entity_reg.async_get_entity_id(
                "button", DOMAIN, f"{entry.entry_id}-{description.category}-{slug}"
            ):
                entity_reg.async_remove(f"button.{slug}")
    async_add_entities(entities)


class RobonectButton(RobonectEntity, ButtonEntity):
    """Representation of a Robonect button."""

    entity_description: ButtonEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        description: ButtonEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        self.entity_description = description
        super().__init__(hass, entry, self.entity_description)
        self.entity_id = f"button.{self.slug}"


class RobonectMqttButton(RobonectButton):
    """Representation of a Robonect MQTT button."""

    _attr_attribution = ATTRIBUTION_MQTT

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        description: ButtonEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        self.coordinator = None
        super().__init__(hass, entry, description)

    async def async_press(self) -> None:
        """Press the button."""
        _LOGGER.debug(f"MQTT button pressed {self.entity_id}")
        if not self.entity_description.cmd:
            _LOGGER.error(f"No command defined for button {self.entity_id}")
        await self.async_send_command(
            self.entity_description.key, {}, topic=self.entity_description.topic
        )


class RobonectRestButton(RobonectButton):
    """Representation of a Robonect REST button."""

    _attr_attribution = ATTRIBUTION_REST

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        coordinator: RobonectDataUpdateCoordinator,
        description: ButtonEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        self.coordinator = coordinator
        super().__init__(hass, entry, description)

    async def async_press(self) -> None:
        """Press the button."""
        _LOGGER.debug(
            f"REST BUTTON PRESSED: {self.entity_description.cmd} {self.entity_id} {self.entity_description.params}",
            True,
        )
        await self.async_send_command(
            self.entity_description.cmd, self.entity_description.params
        )
        await self.coordinator.async_refresh()
        return
