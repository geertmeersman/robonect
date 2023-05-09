"""Robonect integration."""
from __future__ import annotations

from datetime import timedelta

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
from .const import CONF_TRACKING
from .const import CONF_UPDATE_INTERVAL
from .const import DOMAIN
from .const import PLATFORMS
from .const import SERVICE_JOB
from .const import SERVICE_JOB_SCHEMA
from .const import SERVICE_MODE_SCHEMA
from .const import SERVICE_REBOOT
from .const import SERVICE_SHUTDOWN
from .const import SERVICE_SLEEP
from .const import SERVICE_START
from .const import SERVICE_STOP
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
        tracking=entry.data[CONF_TRACKING],
        update_interval=entry.data[CONF_UPDATE_INTERVAL],
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

    async def start(call) -> bool:
        """Start the Robonect mower."""
        return await hass.async_add_executor_job(client.start)

    hass.services.async_register(DOMAIN, SERVICE_START, start)

    async def stop(call) -> bool:
        """Stop the Robonect mower."""
        return await hass.async_add_executor_job(client.stop)

    hass.services.async_register(DOMAIN, SERVICE_STOP, stop)

    async def reboot(call) -> bool:
        """Reboot the Robonect mower."""
        return await hass.async_add_executor_job(client.reboot)

    hass.services.async_register(DOMAIN, SERVICE_REBOOT, reboot)

    async def shutdown(call) -> bool:
        """Shut the Robonect mower down."""
        return await hass.async_add_executor_job(client.shutdown)

    hass.services.async_register(DOMAIN, SERVICE_SHUTDOWN, shutdown)

    async def sleep(call) -> bool:
        """Set the Robonect mower to sleep."""
        return await hass.async_add_executor_job(client.sleep)

    hass.services.async_register(DOMAIN, SERVICE_SLEEP, sleep)

    async def job(call) -> bool:
        """Place a mowing job."""
        await hass.async_add_executor_job(
            lambda: client.job(
                start=call.data.get("start"),
                end=call.data.get("end"),
                duration=call.data.get("duration"),
                after=call.data.get("after"),
                remotestart=call.data.get("remotestart"),
                corridor=call.data.get("corridor"),
            )
        )

    hass.services.async_register(DOMAIN, SERVICE_JOB, job, schema=SERVICE_JOB_SCHEMA)

    async def mode(call) -> bool:
        """Set the Robonect mower mode."""
        await hass.async_add_executor_job(
            lambda: client.mode(mode=call.data.get("mode"))
        )

    hass.services.async_register(DOMAIN, SERVICE_JOB, mode, schema=SERVICE_MODE_SCHEMA)

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
        self._config_entry_id = config_entry_id
        self._device_registry = dev_reg
        self.client = client
        self.hass = hass
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=self.client.update_interval),
        )

    async def _async_update_data(self) -> dict | None:
        """Update data."""
        try:
            items = await self.hass.async_add_executor_job(self.client.fetch_data)
            sleeping = await self.hass.async_add_executor_job(self.client.sleeping)
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
            if not sleeping:
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
                # log_debug(f"[init|RobonectDataUpdateCoordinator|_async_update_data|async_reload] {product.product_name}", True)
                self.hass.async_create_task(
                    self.hass.config_entries.async_reload(self._config_entry_id)
                )
                return None
            return items
        return []
