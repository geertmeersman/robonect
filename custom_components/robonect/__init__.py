"""The Robonect component."""
import logging
from datetime import timedelta

from aiohttp import ClientConnectorError
from aiohttp import ClientError
from aiohttp import ClientResponseError
from aiorobonect import RobonectClient
from homeassistant.components import mqtt
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.const import CONF_MONITORED_VARIABLES
from homeassistant.const import CONF_PASSWORD
from homeassistant.const import CONF_SCAN_INTERVAL
from homeassistant.const import CONF_USERNAME
from homeassistant.core import callback
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.update_coordinator import UpdateFailed

from .const import CONF_MQTT_ENABLED
from .const import CONF_REST_ENABLED
from .const import DOMAIN
from .const import PLATFORMS
from .exceptions import RobonectException
from .exceptions import RobonectServiceException

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, hass_config: ConfigType) -> bool:
    """Set up the Robonect component."""
    hass.data[DOMAIN] = {
        "device_tracker": set(),
        "vacuum": set(),
        "sensor": set(),
    }
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the Robonect integration."""

    if entry.data[CONF_MQTT_ENABLED] is True:
        if not await mqtt.async_wait_for_mqtt_client(hass):
            _LOGGER.error("MQTT integration is not available")
            return False

    if entry.data[CONF_REST_ENABLED] is True:
        client = RobonectClient(
            host=entry.data[CONF_HOST],
            username=entry.data[CONF_USERNAME],
            password=entry.data[CONF_PASSWORD],
        )

        try:
            await hass.async_add_executor_job(client.state)
        except ClientConnectorError as exception:
            raise RobonectServiceException(f"Bad response {exception.message}")
        except ClientResponseError as exception:
            raise RobonectServiceException(f"Bad response {exception.message}")
        except ClientError as exception:
            raise RobonectServiceException(f"Request failed {exception.message}")
        except TimeoutError:
            raise RobonectServiceException("Request timed out")
        except Exception as exception:
            raise exception.message

        hass.data[DOMAIN][entry.entry_id] = coordinator = RobonectDataUpdateCoordinator(
            hass,
            entry=entry,
            client=client,
        )
        await coordinator.async_config_entry_first_refresh()
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class RobonectDataUpdateCoordinator(DataUpdateCoordinator):
    """Data update coordinator for Robonect."""

    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        client: RobonectClient,
    ) -> None:
        """Initialize coordinator."""
        self.entry = entry
        self.client = client
        self.hass = hass
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=entry.data[CONF_SCAN_INTERVAL]),
        )

    async def _async_update_data(self) -> dict | None:
        """Update data."""
        try:
            cleanup = False
            if self.data is None:
                cleanup = True
            items = await self.client.async_cmds(
                self.entry.data[CONF_MONITORED_VARIABLES], self.data is None
            )
            if cleanup:
                await self.async_trigger_cleanup()
            if items:
                return items
            return []
        except ClientConnectorError as exception:
            raise UpdateFailed(f"ConnectionError {exception}") from exception
        except ClientError as exception:
            raise UpdateFailed(f"Request failed {exception.message}")
        except TimeoutError:
            raise UpdateFailed("Request timed out")
        except ConnectionError as exception:
            raise UpdateFailed(f"ConnectionError {exception}") from exception
        except RobonectServiceException as exception:
            raise UpdateFailed(f"RobonectServiceException {exception}") from exception
        except RobonectException as exception:
            raise UpdateFailed(f"RobonectException {exception}") from exception
        except ClientResponseError as exception:
            raise UpdateFailed(f"RobonectException {exception}") from exception
        except Exception as exception:
            raise UpdateFailed(f"Exception {exception}") from exception

    async def async_trigger_cleanup(self) -> None:
        """Trigger entity cleanup."""
        entity_reg: er.EntityRegistry = er.async_get(self.hass)
        ha_entity_reg_list: list[er.RegistryEntry] = er.async_entries_for_config_entry(
            entity_reg, self.entry.entry_id
        )

        """
        for e in self.hass.states.async_entity_ids(DOMAIN):
            _LOGGER.critical(e)
        for state in self.hass.states.async_all():
            _LOGGER.critical(f"state: {state}")
        """
        entities_removed: bool = False
        allowed = self.entry.data[CONF_MONITORED_VARIABLES] + ["NONE"]
        for entry in ha_entity_reg_list:
            if entry.original_name is None:
                continue
            entry_name = entry.name or entry.original_name
            if entry.unique_id.split("-")[1] not in allowed:
                _LOGGER.info("Removing entity: %s", entry_name)
                entity_reg.async_remove(entry.entity_id)
                entities_removed = True
        if entities_removed:
            self._async_remove_empty_devices(entity_reg)

    @callback
    def _async_remove_empty_devices(self, entity_reg: er.EntityRegistry) -> None:
        """Remove devices with no entities."""

        device_reg = dr.async_get(self.hass)
        device_list = dr.async_entries_for_config_entry(device_reg, self.entry.entry_id)
        for device_entry in device_list:
            if not er.async_entries_for_device(
                entity_reg,
                device_entry.id,
                include_disabled_entities=True,
            ):
                _LOGGER.info("Removing device: %s", device_entry.name)
                device_reg.async_remove_device(device_entry.id)
