"""Robonect integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.const import CONF_PASSWORD
from homeassistant.const import CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.update_coordinator import UpdateFailed
from requests.exceptions import ConnectionError

from .client import RobonectClient
from .const import _LOGGER
from .const import COORDINATOR_UPDATE_INTERVAL
from .const import DOMAIN
from .const import PLATFORMS
from .exceptions import RobonectException
from .exceptions import RobonectServiceException
from .models import RobonectItem
from .utils import log_debug


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Robonect from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    client = RobonectClient(
        host=entry.data[CONF_HOST],
        username=entry.data[CONF_USERNAME],
        password=entry.data[CONF_PASSWORD],
    )

    dev_reg = dr.async_get(hass)
    hass.data[DOMAIN][entry.entry_id] = coordinator = RobonectDataUpdateCoordinator(
        hass,
        config_entry_id=entry.entry_id,
        dev_reg=dev_reg,
        client=client,
    )

    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class RobonectDataUpdateCoordinator(DataUpdateCoordinator):
    """Data update coordinator for Robonect."""

    data: list[RobonectItem]
    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry_id: str,
        dev_reg: dr.DeviceRegistry,
        client: RobonectClient,
    ) -> None:
        """Initialize coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=COORDINATOR_UPDATE_INTERVAL,
        )
        self._config_entry_id = config_entry_id
        self._device_registry = dev_reg
        self.client = client
        self.hass = hass

    async def _async_update_data(self) -> dict | None:
        """Update data."""
        try:
            items = await self.hass.async_add_executor_job(self.client.fetch_data)
        except ConnectionError as exception:
            raise UpdateFailed(f"ConnectionError {exception}") from exception
        except RobonectServiceException as exception:
            raise UpdateFailed(f"RobonectServiceException {exception}") from exception
        except RobonectException as exception:
            raise UpdateFailed(f"RobonectException {exception}") from exception
        except Exception as exception:
            raise UpdateFailed(f"Exception {exception}") from exception

        items: list[RobonectItem] = items

        current_items = {
            list(device.identifiers)[0][1]
            for device in dr.async_entries_for_config_entry(
                self._device_registry, self._config_entry_id
            )
        }

        if len(items) > 0:
            fetched_items = {str(items[item].device_key) for item in items}
            log_debug(
                f"[init|RobonectDataUpdateCoordinator|_async_update_data|fetched_items] {fetched_items}"
            )
            if stale_items := current_items - fetched_items:
                for device_key in stale_items:
                    if device := self._device_registry.async_get_device(
                        {(DOMAIN, device_key)}
                    ):
                        log_debug(
                            f"[init|RobonectDataUpdateCoordinator|_async_update_data|async_remove_device] {device_key}",
                            True,
                        )
                        self._device_registry.async_remove_device(device.id)

            # If there are new items, we should reload the config entry so we can
            # create new devices and entities.
            if self.data and fetched_items - {
                str(self.data[item].device_key) for item in self.data
            }:
                # log_debug(f"[init|RobonectDataUpdateCoordinator|_async_update_data|async_reload] {product.product_name}")
                self.hass.async_create_task(
                    self.hass.config_entries.async_reload(self._config_entry_id)
                )
                return None
            return items
        return []
