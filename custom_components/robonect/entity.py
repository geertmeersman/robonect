"""Base Robonect entity."""
from __future__ import annotations

from datetime import datetime

from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity import EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import RobonectDataUpdateCoordinator
from .const import ATTRIBUTION
from .const import DOMAIN
from .const import NAME
from .const import VERSION
from .const import WEBSITE
from .models import RobonectItem
from .utils import log_debug
from .utils import sensor_name


class RobonectEntity(CoordinatorEntity[RobonectDataUpdateCoordinator]):
    """Base Robonect entity."""

    _attr_attribution = ATTRIBUTION

    def __init__(
        self,
        coordinator: RobonectDataUpdateCoordinator,
        description: EntityDescription,
        item: RobonectItem,
    ) -> None:
        """Initialize Robonect entities."""
        super().__init__(coordinator)
        self.entity_description = description
        self._item = item
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, str(self.item.device_key))},
            name=f"{NAME} {self.item.device_name}",
            manufacturer=NAME,
            configuration_url=WEBSITE,
            entry_type=DeviceEntryType.SERVICE,
            model=self.item.device_model,
            sw_version=VERSION,
        )
        """
        extra attributes!
        """
        self._attr_unique_id = f"{DOMAIN}_{self.item.key}"
        self._key = self.item.key
        self.client = coordinator.client
        self.last_synced = datetime.now()
        self._attr_name = sensor_name(self.item.name)
        self._item = item
        log_debug(f"[RobonectEntity|init] {self._key}")

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if len(self.coordinator.data):
            for item in self.coordinator.data:
                item = self.coordinator.data[item]
                if self._key == item.key:
                    self.last_synced = datetime.now()
                    self._item = item
                    self.async_write_ha_state()
                    return
        log_debug(
            f"[RobonectEntity|_handle_coordinator_update] {self._attr_unique_id}: async_write_ha_state ignored since API fetch failed or not found",
        )

    @property
    def item(self) -> RobonectItem:
        """Return the product for this entity."""
        return self._item

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        # Force available to True as when the mower is sleeping, the "non status" entities will not be fetched and otherwise they will become unavailable
        return True

    async def async_update(self) -> None:
        """Update the entity.  Only used by the generic entity update service."""
        return
