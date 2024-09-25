"""The Robonect component."""

from datetime import timedelta
import logging
from pathlib import Path
from typing import Any

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
from homeassistant.helpers.storage import STORAGE_DIR, Store
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
import pytz

from .const import (
    CONF_ATTRS_UNITS,
    CONF_BRAND,
    CONF_ENABLE,
    CONF_MQTT_ENABLED,
    CONF_MQTT_TOPIC,
    CONF_REST_ENABLED,
    CONF_SUGGESTED_BRAND,
    CONF_SUGGESTED_TYPE,
    CONF_WINTER_MODE,
    DEFAULT_MQTT_TOPIC,
    DOMAIN,
    EVENT_ROBONECT_RESPONSE,
    PLATFORMS,
    SENSOR_GROUPS,
    SERVICE_DIRECT,
    SERVICE_DIRECT_SCHEMA,
    SERVICE_JOB,
    SERVICE_JOB_AFTER_VALUES,
    SERVICE_JOB_CORRIDOR_VALUES,
    SERVICE_JOB_REMOTESTART_VALUES,
    SERVICE_JOB_SCHEMA,
    SERVICE_TIMER,
    SERVICE_TIMER_SCHEMA,
    WEEKDAYS_SHORT,
)
from .exceptions import RobonectException

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the Robonect integration."""

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {}

    for platform in PLATFORMS:
        hass.data[DOMAIN][entry.entry_id].setdefault(platform, set())

    # Cache the timezone during setup
    timezone = await hass.async_add_executor_job(pytz.timezone, hass.config.time_zone)
    hass.data[DOMAIN]["timezone"] = timezone

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
        if not entry.data.get(CONF_WINTER_MODE, True):
            try:
                await client.state()
            except Exception as exception:
                _LOGGER.warning(f"Exception: {exception}")

        storage_dir = Path(f"{hass.config.path(STORAGE_DIR)}/{DOMAIN}")
        if storage_dir.is_file():
            storage_dir.unlink()
        storage_dir.mkdir(exist_ok=True)
        store: Store = Store(hass, 1, f"{DOMAIN}/{entry.entry_id}")
        dev_reg = dr.async_get(hass)

        hass.data[DOMAIN][entry.entry_id]["coordinator"] = coordinator = (
            RobonectDataUpdateCoordinator(
                hass,
                entry=entry,
                client=client,
                dev_reg=dev_reg,
                store=store,
            )
        )
        await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    async def timer(service: ServiceCall) -> bool:
        """Modify a timer."""
        params = {}
        try:
            if CONF_ENABLE in service.data:
                params |= {CONF_ENABLE: 1 if service.data[CONF_ENABLE] is True else 0}
            params |= {"timer": service.data["timer"]}
            params |= {"start": service.data["start"][0:5]}
            params |= {"end": service.data["end"][0:5]}
            for weekday in WEEKDAYS_SHORT:
                if weekday in service.data["weekdays"]:
                    params |= {weekday: 1}
                else:
                    params |= {weekday: 0}
        except ValueError as error:
            raise RobonectException(error)
        await async_send_command(hass, entry, "timer", params)

    hass.services.async_register(
        DOMAIN, SERVICE_TIMER, timer, schema=SERVICE_TIMER_SCHEMA
    )

    async def direct(service: ServiceCall) -> bool:
        """Modify a direction."""
        params = {}
        try:
            params |= {"left": service.data["left"]}
            params |= {"right": service.data["right"]}
            params |= {"timeout": service.data["timeout"]}
        except ValueError as error:
            raise RobonectException(error)
        await async_send_command(hass, entry, "direct", params)

    hass.services.async_register(
        DOMAIN, SERVICE_DIRECT, direct, schema=SERVICE_DIRECT_SCHEMA
    )

    async def job(service: ServiceCall) -> bool:
        """Schedule a mowing job."""
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


async def async_remove_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle removal of pubsub subscriptions created during config flow."""
    storage = Path(f"{hass.config.path(STORAGE_DIR)}/{DOMAIN}/{entry.entry_id}")
    storage.unlink(True)
    storage_dir = Path(f"{hass.config.path(STORAGE_DIR)}/{DOMAIN}")
    if storage_dir.is_dir() and not any(storage_dir.iterdir()):
        storage_dir.rmdir()


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
        dev_reg: dr.DeviceRegistry,
        store: Store,
    ) -> None:
        """Initialize coordinator."""
        self._debug = _LOGGER.isEnabledFor(logging.DEBUG)
        self.entry = entry
        self.client = client
        self._device_registry = dev_reg
        self.store = store
        self._init = True
        self.hass = hass
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=entry.data[CONF_SCAN_INTERVAL]),
        )

    async def async_config_entry_first_refresh(self) -> None:
        """Refresh data for the first time when a config entry is setup."""
        self.data = await self.store.async_load() or {}
        await super().async_config_entry_first_refresh()

    async def get_data(self) -> dict | None:
        """Get the data from the Robonect client."""
        data = await self.client.async_cmds(
            self.entry.data[CONF_MONITORED_VARIABLES], self.data is None or self._init
        )
        if self._init:
            self._init = False
        for key, value in data.items():
            self.data[key] = value
        await self.store.async_save(self.data)

    async def _async_update_data(self) -> dict | None:
        """Update data."""
        if not self.entry.data.get(CONF_WINTER_MODE, True):
            if self._debug:
                cleanup = False
                if self.data is None:
                    cleanup = True
                await self.get_data()
                if cleanup:
                    await self.async_trigger_cleanup()
                if self.data:
                    _LOGGER.debug(f"Returned items: {self.data}")

            try:
                cleanup = False
                if self.data is None:
                    cleanup = True
                await self.get_data()
                if cleanup:
                    await self.async_trigger_cleanup()
            except Exception as exception:
                _LOGGER.warning(f"Exception {exception}")

        if len(self.data) > 0:
            return self.data
        return {}

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

    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    if not coordinator:
        _LOGGER.debug("[REST async_send_command] COORDINATOR NOK")

    _LOGGER.debug(f"[REST async_send_command] command: {command}, params: {params}")

    try:
        response = await coordinator.client.async_cmd(command, params)
    except Exception as exception:
        response = {"successful": False, "exception": f"{exception}"}
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

    if config_entry.version == 2:
        new = {**config_entry.data}

        entity_reg: er.EntityRegistry = er.async_get(hass)
        ha_entity_reg_list: list[er.RegistryEntry] = er.async_entries_for_config_entry(
            entity_reg, config_entry.entry_id
        )

        for entry in ha_entity_reg_list:
            entry_name = entry.name or entry.original_name
            if "sensor.automower_timer" in entry.entity_id:
                _LOGGER.info("Removing entity: %s", entry_name)
                entity_reg.async_remove(entry.entity_id)
        config_entry.version = 3
        hass.config_entries.async_update_entry(config_entry, data=new)

    if config_entry.version == 3:
        new = {**config_entry.data}

        new[CONF_WINTER_MODE] = False

        config_entry.version = 4
        hass.config_entries.async_update_entry(config_entry, data=new)

    _LOGGER.info("Migration to version %s successful", config_entry.version)

    return True
