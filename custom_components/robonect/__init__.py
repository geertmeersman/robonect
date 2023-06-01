"""The Robonect component."""
from datetime import timedelta
import logging
from typing import Any

from aiohttp import ClientConnectorError, ClientError, ClientResponseError
from aiorobonect import RobonectClient
from homeassistant.components import mqtt
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_HOST,
    CONF_MONITORED_VARIABLES,
    CONF_PASSWORD,
    CONF_SCAN_INTERVAL,
    CONF_TYPE,
    CONF_USERNAME,
)
from homeassistant.core import HomeAssistant, ServiceCall, callback
from homeassistant.helpers import device_registry as dr, entity_registry as er
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    CONF_ATTRS_UNITS,
    CONF_BRAND,
    CONF_MQTT_ENABLED,
    CONF_MQTT_TOPIC,
    CONF_REST_ENABLED,
    CONF_SUGGESTED_BRAND,
    CONF_SUGGESTED_TYPE,
    DEFAULT_MQTT_TOPIC,
    DOMAIN,
    EVENT_ROBONECT_RESPONSE,
    PLATFORMS,
    SENSOR_GROUPS,
    SERVICE_JOB,
    SERVICE_JOB_AFTER_VALUES,
    SERVICE_JOB_CORRIDOR_VALUES,
    SERVICE_JOB_REMOTESTART_VALUES,
    SERVICE_JOB_SCHEMA,
)
from .exceptions import RobonectException, RobonectServiceException

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, hass_config: ConfigType) -> bool:
    """Set up the Robonect component."""
    hass.data[DOMAIN] = {
        "device_tracker": set(),
        "binary_sensor": set(),
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

    async def job(service: ServiceCall) -> bool:
        """Set the Robonect mower to sleep."""
        params = {"mode": "job"}
        if "start" in service.data:
            params |= {"start": service.data["start"][0:5]}
        if "end" in service.data:
            params |= {"end": service.data["end"][0:5]}
        if "duration" in service.data:
            params |= {"duration": service.data["duration"]}
        if "after" in service.data:
            try:
                index = SERVICE_JOB_AFTER_VALUES.index(service.data["after"])
            except ValueError as error:
                raise RobonectException(error)
            params |= {"after": index}
        if "remotestart" in service.data:
            try:
                index = SERVICE_JOB_REMOTESTART_VALUES.index(
                    service.data["remotestart"]
                )
            except ValueError as error:
                raise RobonectException(error)
            params |= {"remotestart": index}
        if "corridor" in service.data:
            try:
                if service.data["corridor"] == "Normal":
                    pass
                index = SERVICE_JOB_CORRIDOR_VALUES.index(service.data["corridor"]) - 1
            except ValueError as error:
                raise RobonectException(error)
            params |= {"corridor": index}

        await async_send_command(hass, entry, "mode", params)

    hass.services.async_register(DOMAIN, SERVICE_JOB, job, schema=SERVICE_JOB_SCHEMA)

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
        self._debug = _LOGGER.isEnabledFor(logging.DEBUG)
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
        if self._debug:
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

        entities_removed: bool = False
        allowed = self.entry.data[CONF_MONITORED_VARIABLES] + ["NONE"]
        for entry in ha_entity_reg_list:
            if entry.original_name is None:
                continue
            entry_name = entry.name or entry.original_name
            if (
                len(entry.unique_id.split("-")) == 1
                or entry.unique_id.split("-")[1] not in allowed
            ):
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


async def async_fire_event(
    hass: HomeAssistant,
    entry: ConfigEntry,
    response: dict,
):
    """Fire a bus event."""
    dev_reg = dr.async_get(hass)

    device = dev_reg.async_get_device({(DOMAIN, entry.data[CONF_MQTT_TOPIC])})
    hass.bus.async_fire(
        EVENT_ROBONECT_RESPONSE,
        {"device_id": device.id, "client_response": response},
    )


async def async_send_command(
    hass: HomeAssistant,
    entry: ConfigEntry,
    command: str,
    params: dict[str, Any] | list[Any] | None = None,
    **kwargs: Any,
) -> None:
    """Send a command to a Robonect mower."""

    coordinator = hass.data[DOMAIN][entry.entry_id]
    if not coordinator:
        _LOGGER.debug("[REST async_send_command] COORDINATOR NOK")

    _LOGGER.debug(f"[REST async_send_command] command: {command}, params: {params}")

    try:
        response = await coordinator.client.async_cmd(command, params)
    except Exception as exception:
        response = {"successful": False, "exception": exception.message}
    await async_fire_event(
        hass, entry, response | {"command": command, "params": params}
    )

    return


async def async_migrate_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Migrate old entry."""
    _LOGGER.info("Migrating from version %s", config_entry.version)

    if config_entry.version == 1:
        new = {**config_entry.data}
        # TODO: modify Config Entry data
        if CONF_MONITORED_VARIABLES not in new:
            new[CONF_MONITORED_VARIABLES] = SENSOR_GROUPS
            new[CONF_MQTT_ENABLED] = False
            new[CONF_MQTT_TOPIC] = DEFAULT_MQTT_TOPIC
            new[CONF_TYPE] = CONF_SUGGESTED_TYPE
            new[CONF_BRAND] = CONF_SUGGESTED_BRAND
            new[CONF_REST_ENABLED] = True
            new[CONF_SCAN_INTERVAL] = new["update_interval"]
            del new["update_interval"]
            del new["tracking"]

        new[CONF_ATTRS_UNITS] = True

        config_entry.version = 2
        hass.config_entries.async_update_entry(config_entry, data=new)

    _LOGGER.info("Migration to version %s successful", config_entry.version)

    return True
