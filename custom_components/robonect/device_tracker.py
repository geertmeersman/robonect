"""Robonect device tracking."""
from dataclasses import dataclass
from datetime import datetime
import logging

from homeassistant.components import mqtt
from homeassistant.components.device_tracker import SourceType, TrackerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_BATTERY_LEVEL, ATTR_LATITUDE, ATTR_LONGITUDE
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import EntityDescription
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity

from . import RobonectDataUpdateCoordinator
from .const import (
    ATTR_SATELLITES,
    ATTRIBUTION_MQTT,
    ATTRIBUTION_REST,
    CONF_MQTT_ENABLED,
    CONF_MQTT_TOPIC,
    CONF_REST_ENABLED,
    DOMAIN,
)
from .entity import RobonectCoordinatorEntity, RobonectEntity
from .utils import convert_coordinate_degree_to_float, filter_out_units

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up an Robonect device_tracker entry."""

    # Make sure MQTT integration is enabled and the client is available
    if entry.data[CONF_MQTT_ENABLED] is True:
        if not await mqtt.async_wait_for_mqtt_client(hass):
            _LOGGER.error("MQTT integration is not available")
            return

    @callback
    def async_mqtt_event_received(msg: mqtt.ReceiveMessage) -> None:
        """Receive set latitude."""
        if (
            entry.data[CONF_MQTT_TOPIC]
            in hass.data[DOMAIN][entry.entry_id]["device_tracker"]
        ):
            return

        hass.data[DOMAIN][entry.entry_id]["device_tracker"].add(
            entry.data[CONF_MQTT_TOPIC]
        )

        async_add_entities([RobonectMqttGPSEntity(hass, entry)])

    if entry.data[CONF_MQTT_ENABLED] is True:
        await mqtt.async_subscribe(
            hass,
            f"{entry.data[CONF_MQTT_TOPIC]}/gps/latitude",
            async_mqtt_event_received,
            0,
        )
    elif entry.data[CONF_REST_ENABLED] is True:
        _LOGGER.debug("Creating REST device tracker")
        coordinator: RobonectDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id][
            "coordinator"
        ]
        if (
            coordinator.data is not None
            and "gps" in coordinator.data
            and coordinator.data.get("gps").get("succesful")
        ):
            async_add_entities(
                [
                    RobonectRestGPSEntity(
                        hass,
                        entry,
                        coordinator,
                    )
                ]
            )


@dataclass
class DeviceTrackerEntityDescription(EntityDescription):
    """Device tracker entity description for Robonect."""

    category: str | None = None


class RobonectGPSEntity(RobonectEntity, TrackerEntity, RestoreEntity):
    """Represent a tracked device."""

    _attr_has_entity_name = True

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
    ):
        """Set up GPS entity."""
        self.coordinator = None
        self.entity_description = DeviceTrackerEntityDescription(
            key="gps",
            icon="mdi:robot-mower",
            category="NONE",
        )
        self.entry = entry
        super().__init__(hass, entry, self.entity_description)
        self._attr_translation_key = "gps"
        self.entity_id = f"device_tracker.{self.slug}"
        self._longitude = None
        self._latitude = None
        self._satellites = None
        self._battery = None
        self._attributes = None

    @property
    def battery_level(self) -> int | None:
        """Return the battery level of the device.

        Percentage from 0-100.
        """
        return self._battery

    @property
    def latitude(self) -> float | None:
        """Return latitude value of the device."""
        return self._latitude

    @property
    def longitude(self) -> float | None:
        """Return longitude value of the device."""
        return self._longitude

    @property
    def source_type(self) -> SourceType:
        """Return the source type of the device."""
        return SourceType.GPS

    def update_rest_gps_state(self):
        """Update state based on REST GPS State."""
        if self.coordinator is None:
            return False
        if len(self.coordinator.data) and "gps" in self.coordinator.data:
            gps_state = self.coordinator.data.get("gps")
            # gps_state = {"gps": {"satellites": 12, "latitude": "51.12052635932699", "longitude": "4.223141069768272"}, "successful": True}
            status = self.coordinator.data.get("status")
            if "gps" in gps_state:
                gps_state = gps_state.get("gps")
                self._latitude = float(gps_state.get(ATTR_LATITUDE))
                self._longitude = float(gps_state.get(ATTR_LONGITUDE))
                self._attributes = {
                    "last_synced": self.last_synced,
                    "category": self.category,
                    ATTR_SATELLITES: gps_state.get(ATTR_SATELLITES),
                }
            else:
                _LOGGER.debug(f"RobonectRestGPSEntity update NOK {gps_state}")
                self._location = (None, None)
                self._accuracy = None
                self._attributes = {
                    ATTR_SATELLITES: None,
                }
            self._battery = int(status.get("status").get("battery"))
            self.update_ha_state()
            return True
        return False

    async def async_added_to_hass(self) -> None:
        """Subscribe to MQTT events."""
        await super().async_added_to_hass()

        @callback
        def latitude_received(message):
            """Handle new latitude topic."""
            self._latitude = convert_coordinate_degree_to_float(message.payload)
            self.update_ha_state()

        @callback
        def longitude_received(message):
            """Handle new longitude topic."""
            self._longitude = convert_coordinate_degree_to_float(message.payload)
            self.update_ha_state()

        @callback
        def battery_received(message):
            """Handle battery topic."""
            self._battery = int(filter_out_units(message.payload))
            self.update_ha_state()

        @callback
        def satellites_received(message):
            """Handle satellites topic."""
            self._attributes |= {"satellites": message.payload}
            self.update_ha_state()

        if self.entry.data[CONF_MQTT_ENABLED] is True:
            await mqtt.async_subscribe(
                self.hass,
                f"{self.entry.data[CONF_MQTT_TOPIC]}/gps/latitude",
                latitude_received,
                1,
            )
            await mqtt.async_subscribe(
                self.hass,
                f"{self.entry.data[CONF_MQTT_TOPIC]}/gps/longitude",
                longitude_received,
                1,
            )
            await mqtt.async_subscribe(
                self.hass,
                f"{self.entry.data[CONF_MQTT_TOPIC]}/gps/satellites",
                satellites_received,
                1,
            )
            await mqtt.async_subscribe(
                self.hass,
                f"{self.entry.data[CONF_MQTT_TOPIC]}/mower/battery/charge",
                battery_received,
                1,
            )

        # Don't restore if status is fetched from coordinator data
        if self.entry.data[CONF_MQTT_ENABLED] is False and self.update_rest_gps_state():
            return

        if (state := await self.async_get_last_state()) is None:
            self._location = (None, None)
            self._accuracy = None
            self._attributes = {
                ATTR_SATELLITES: None,
            }
            self._battery = None
            return

        attr = state.attributes
        self._latitude = attr.get(ATTR_LATITUDE)
        self._longitude = attr.get(ATTR_LONGITUDE)
        self._attributes = {
            ATTR_SATELLITES: attr.get(ATTR_SATELLITES),
        }
        self._battery = attr.get(ATTR_BATTERY_LEVEL)


class RobonectMqttGPSEntity(RobonectGPSEntity):
    """Represent an MQTT tracked device."""

    _attr_attribution = ATTRIBUTION_MQTT

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(hass, entry)


class RobonectRestGPSEntity(RobonectCoordinatorEntity, RobonectGPSEntity):
    """Represent a REST tracked device."""

    _attr_attribution = ATTRIBUTION_REST

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        coordinator: RobonectDataUpdateCoordinator,
    ) -> None:
        """Initialize the sensor."""
        RobonectGPSEntity.__init__(self, hass, entry)
        super().__init__(coordinator, self.entity_description)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.last_synced = datetime.now()
        self.update_rest_gps_state()
        return
