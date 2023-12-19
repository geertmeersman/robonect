"""Config flow to configure Robonect."""
from __future__ import annotations

from abc import ABC
from collections.abc import Awaitable
import logging
from typing import Any

import aiohttp
from aiorobonect import RobonectClient
from homeassistant.components import mqtt
from homeassistant.config_entries import ConfigEntry, ConfigFlow, OptionsFlow
from homeassistant.const import (
    CONF_HOST,
    CONF_MONITORED_VARIABLES,
    CONF_PASSWORD,
    CONF_SCAN_INTERVAL,
    CONF_TYPE,
    CONF_USERNAME,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowHandler, FlowResult
from homeassistant.helpers.config_entry_flow import DiscoveryFlowHandler
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.selector import (
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
    TextSelector,
    TextSelectorConfig,
    TextSelectorType,
)
from homeassistant.helpers.typing import UNDEFINED
import voluptuous as vol

from .const import (
    CONF_ATTRS_UNITS,
    CONF_BRAND,
    CONF_MQTT_ENABLED,
    CONF_MQTT_TOPIC,
    CONF_REST_ENABLED,
    CONF_SUGGESTED_BRAND,
    CONF_SUGGESTED_HOST,
    CONF_SUGGESTED_TYPE,
    CONF_WINTER_MODE,
    DEFAULT_MQTT_TOPIC,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    NAME,
    ROBONECT_BRANDS,
    SENSOR_GROUPS,
)
from .exceptions import BadCredentialsException, RobonectServiceException
from .models import RobonectConfigEntryData

_LOGGER = logging.getLogger(__name__)

DEFAULT_ENTRY_DATA = RobonectConfigEntryData(
    mqtt_enabled=True,
    mqtt_topic=DEFAULT_MQTT_TOPIC,
    host=CONF_SUGGESTED_HOST,
    type=CONF_SUGGESTED_TYPE,
    brand=CONF_SUGGESTED_BRAND,
    rest_enabled=True,
    username=None,
    password=None,
    monitoried_variables=SENSOR_GROUPS,
    scan_interval=DEFAULT_SCAN_INTERVAL,
    attributes_units=True,
    winter_mode=False,
)


async def _async_has_devices(_: HomeAssistant) -> bool:
    """MQTT is set as dependency, so that should be sufficient."""
    return True


class RobonectFlowHandler(DiscoveryFlowHandler[Awaitable[bool]], domain=DOMAIN):
    """Handle Robonect MQTT DiscoveryFlow. The MQTT step is inherited from the parent class."""

    def __init__(self) -> None:
        """Set up the config flow."""
        super().__init__(DOMAIN, "Robonect", _async_has_devices)

    async def async_step_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Confirm setup."""
        if user_input is None:
            return self.async_show_form(
                step_id="confirm",
            )

        return await super().async_step_confirm(user_input)


class RobonectCommonFlow(ABC, FlowHandler):
    """Base class for Robonect flows."""

    def __init__(self, initial_data: RobonectConfigEntryData) -> None:
        """Initialize RobonectCommonFlow."""
        self.initial_data = initial_data
        self.new_entry_data = RobonectConfigEntryData()
        self.new_title: str | None = None
        self._config_id = None

    def new_data(self):
        """Construct new data."""
        return DEFAULT_ENTRY_DATA | self.initial_data | self.new_entry_data

    async def async_validate_input(self, user_input: dict[str, Any]) -> None:
        """Validate user credentials."""

        client = RobonectClient(
            host=user_input[CONF_HOST],
            username=user_input[CONF_USERNAME],
            password=user_input[CONF_PASSWORD],
        )
        state = await client.state()
        return state

    async def async_step_connection_methods(
        self, user_input: dict | None = None
    ) -> FlowResult:
        """Handle connection configuration."""
        errors: dict = {}

        if user_input is None:
            self.new_entry_data = self.new_data()

        if not await mqtt.async_wait_for_mqtt_client(self.hass):
            self.new_entry_data |= RobonectConfigEntryData(
                mqtt_enabled=False,
            )

        if user_input is not None:
            user_input = self.new_data() | user_input
            self.new_entry_data |= user_input
            if user_input[
                CONF_MQTT_ENABLED
            ] and not await mqtt.async_wait_for_mqtt_client(self.hass):
                errors["base"] = "mqtt_disabled"
                self.new_entry_data |= RobonectConfigEntryData(
                    mqtt_enabled=False,
                )
            else:
                self._config_id = f"{DOMAIN}_" + user_input[CONF_MQTT_TOPIC]
                if (
                    self.hass.config_entries.async_get_entry(self._config_id)
                    is not None
                ):
                    errors["CONF_MQTT_TOPIC"] = "topic_used"
                else:
                    return await self.async_step_connection_rest()

        fields = {
            vol.Required(CONF_MQTT_ENABLED): bool,
            vol.Required(CONF_MQTT_TOPIC): str,
            vol.Required(CONF_REST_ENABLED): bool,
            vol.Required(CONF_BRAND): SelectSelector(
                SelectSelectorConfig(
                    options=ROBONECT_BRANDS,
                    multiple=False,
                    custom_value=False,
                    mode=SelectSelectorMode.DROPDOWN,
                ),
            ),
            vol.Required(CONF_TYPE): TextSelector(
                TextSelectorConfig(type=TextSelectorType.TEXT, autocomplete=CONF_TYPE)
            ),
        }
        return self.async_show_form(
            step_id="connection_methods",
            data_schema=self.add_suggested_values_to_schema(
                vol.Schema(fields), self.new_entry_data
            ),
            description_placeholders={
                "name": NAME,
            },
            errors=errors,
        )

    async def async_step_connection_rest(
        self, user_input: dict | None = None
    ) -> FlowResult:
        """Handle connection configuration."""
        errors: dict = {}
        placeholders = {
            "name": NAME,
        }
        if user_input is not None:
            user_input = self.new_data() | user_input
            self.new_entry_data |= user_input
            if user_input[CONF_REST_ENABLED]:
                test = await self.test_connection(user_input)
                if not test["errors"]:
                    self.new_title = test["status"].get("name")
                    await self.async_set_unique_id(self._config_id)
                    self._abort_if_unique_id_configured()
                    _LOGGER.debug(f"New account {self.new_title} added")
                    return self.finish_flow()
                if test["exception"]:
                    placeholders |= {"exception": test["exception"]}
            else:
                await self.async_set_unique_id(self._config_id)
                self._abort_if_unique_id_configured()
                _LOGGER.debug(f"New account {self.new_title} added")
                return self.finish_flow()
            errors = test["errors"]
        else:
            self.new_entry_data = self.new_data()

        fields = {
            vol.Required(CONF_HOST): TextSelector(
                TextSelectorConfig(type=TextSelectorType.TEXT, autocomplete="host")
            ),
            vol.Required(CONF_USERNAME): TextSelector(
                TextSelectorConfig(type=TextSelectorType.TEXT, autocomplete="username")
            ),
            vol.Required(CONF_PASSWORD): TextSelector(
                TextSelectorConfig(
                    type=TextSelectorType.PASSWORD, autocomplete="password"
                )
            ),
            vol.Required(
                CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL
            ): NumberSelector(
                NumberSelectorConfig(min=1, max=60, step=1, mode=NumberSelectorMode.BOX)
            ),
            vol.Required(
                CONF_MONITORED_VARIABLES, default=SENSOR_GROUPS
            ): SelectSelector(
                SelectSelectorConfig(
                    options=SENSOR_GROUPS,
                    multiple=True,
                    custom_value=False,
                    mode=SelectSelectorMode.DROPDOWN,
                    translation_key=CONF_MONITORED_VARIABLES,
                )
            ),
            vol.Required(CONF_ATTRS_UNITS): bool,
        }
        return self.async_show_form(
            step_id="connection_rest",
            data_schema=self.add_suggested_values_to_schema(
                vol.Schema(fields), self.new_entry_data
            ),
            description_placeholders=placeholders,
            errors=errors,
        )

    async def test_connection(self, user_input: dict | None = None) -> dict:
        """Test the connection to Robonect."""
        errors: dict = {}
        status: dict = {}
        exception: dict = {}

        if user_input is not None:
            user_input = self.new_data() | user_input
            try:
                status = await self.async_validate_input(user_input)
                if not status.get("successful") or status.get("successful") is not True:
                    raise RobonectServiceException
            except AssertionError as exception:
                errors["base"] = "cannot_connect"
                _LOGGER.debug(f"[async_step_password|login] AssertionError {exception}")
            except aiohttp.ClientConnectorError:
                errors["base"] = "cannot_connect"
            except ConnectionError:
                errors["base"] = "cannot_connect"
            except RobonectServiceException:
                errors["base"] = "service_error"
            except BadCredentialsException:
                errors["base"] = "invalid_auth"
            except Exception as e:
                if isinstance(e, aiohttp.ClientResponseError):
                    errors["base"] = "invalid_auth"
                else:
                    errors["base"] = "unknown"
                exception = e.message
        return {"status": status, "errors": errors, "exception": exception}

    async def async_step_username_password(
        self, user_input: dict | None = None
    ) -> FlowResult:
        """Configure password."""
        errors: dict = {}

        if user_input is not None:
            user_input = self.new_data() | user_input
            test = await self.test_connection(user_input)
            if not test["errors"]:
                self.new_entry_data |= RobonectConfigEntryData(
                    password=user_input[CONF_PASSWORD],
                )
                return self.finish_flow()

        fields = {
            vol.Required(CONF_USERNAME): cv.string,
            vol.Required(CONF_PASSWORD): cv.string,
        }
        return self.async_show_form(
            step_id="username_password",
            data_schema=self.add_suggested_values_to_schema(
                vol.Schema(fields),
                self.initial_data
                | RobonectConfigEntryData(
                    password=None,
                ),
            ),
            errors=errors,
        )

    async def async_step_connection_options(
        self, user_input: dict | None = None
    ) -> FlowResult:
        """Configure password."""
        errors: dict = {}

        if user_input is not None:
            user_input = self.new_data() | user_input
            self.new_entry_data |= user_input
            if user_input[
                CONF_MQTT_ENABLED
            ] and not await mqtt.async_wait_for_mqtt_client(self.hass):
                errors["base"] = "mqtt_disabled"
                self.new_entry_data |= RobonectConfigEntryData(
                    mqtt_enabled=False,
                )
            else:
                return self.finish_flow()

        fields = {
            vol.Required(CONF_MQTT_ENABLED): bool,
            vol.Required(CONF_REST_ENABLED): bool,
        }

        return self.async_show_form(
            step_id="connection_options",
            data_schema=self.add_suggested_values_to_schema(
                vol.Schema(fields),
                self.initial_data,
            ),
            description_placeholders={
                "name": NAME,
            },
            errors=errors,
        )

    async def async_step_winter_mode(
        self, user_input: dict | None = None
    ) -> FlowResult:
        """Configure winter mode."""
        errors: dict = {}

        if user_input is not None:
            self.new_entry_data |= user_input
            return self.finish_flow()

        fields = {
            vol.Required(CONF_WINTER_MODE): bool,
        }

        return self.async_show_form(
            step_id="winter_mode",
            data_schema=self.add_suggested_values_to_schema(
                vol.Schema(fields),
                self.initial_data,
            ),
            description_placeholders={
                "name": NAME,
            },
            errors=errors,
        )

    async def async_step_brand_type(self, user_input: dict | None = None) -> FlowResult:
        """Configure brand and type."""
        errors: dict = {}

        if user_input is not None:
            self.new_entry_data |= user_input
            return self.finish_flow()

        fields = {
            vol.Required(CONF_BRAND): SelectSelector(
                SelectSelectorConfig(
                    options=ROBONECT_BRANDS,
                    multiple=False,
                    custom_value=False,
                    mode=SelectSelectorMode.DROPDOWN,
                ),
            ),
            vol.Required(CONF_TYPE): TextSelector(
                TextSelectorConfig(type=TextSelectorType.TEXT, autocomplete=CONF_TYPE)
            ),
        }

        return self.async_show_form(
            step_id="brand_type",
            data_schema=self.add_suggested_values_to_schema(
                vol.Schema(fields),
                self.initial_data,
            ),
            description_placeholders={
                "name": NAME,
            },
            errors=errors,
        )

    async def async_step_host(self, user_input: dict | None = None) -> FlowResult:
        """Configure host."""
        errors: dict = {}

        if user_input is not None:
            user_input = self.new_data() | user_input
            test = await self.test_connection(user_input)
            if not test["errors"]:
                self.new_entry_data |= RobonectConfigEntryData(
                    host=user_input[CONF_HOST],
                )
                return self.finish_flow()

        fields = {
            vol.Required(CONF_HOST): cv.string,
        }
        return self.async_show_form(
            step_id="host",
            data_schema=self.add_suggested_values_to_schema(
                vol.Schema(fields),
                self.initial_data,
            ),
            errors=errors,
        )

    async def async_step_scan_interval(
        self, user_input: dict | None = None
    ) -> FlowResult:
        """Configure update interval."""
        errors: dict = {}

        if user_input is not None:
            self.new_entry_data |= user_input
            return self.finish_flow()

        fields = {
            vol.Required(CONF_SCAN_INTERVAL): NumberSelector(
                NumberSelectorConfig(min=1, max=60, step=1, mode=NumberSelectorMode.BOX)
            ),
        }
        return self.async_show_form(
            step_id="scan_interval",
            data_schema=self.add_suggested_values_to_schema(
                vol.Schema(fields),
                self.initial_data,
            ),
            errors=errors,
        )

    async def async_step_monitored_variables(
        self, user_input: dict | None = None
    ) -> FlowResult:
        """Configure monitored variables."""
        errors: dict = {}

        if user_input is not None:
            self.new_entry_data |= user_input
            return self.finish_flow()

        fields = {
            vol.Required(CONF_MONITORED_VARIABLES): SelectSelector(
                SelectSelectorConfig(
                    options=SENSOR_GROUPS,
                    multiple=True,
                    custom_value=False,
                    mode=SelectSelectorMode.DROPDOWN,
                    translation_key=CONF_MONITORED_VARIABLES,
                )
            ),
            vol.Required(CONF_ATTRS_UNITS): bool,
        }
        return self.async_show_form(
            step_id="monitored_variables",
            data_schema=self.add_suggested_values_to_schema(
                vol.Schema(fields),
                self.initial_data,
            ),
            errors=errors,
        )


class RobonectOptionsFlow(RobonectCommonFlow, OptionsFlow):
    """Handle Robonect options."""

    general_settings: dict

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize Robonect options flow."""
        self.config_entry = config_entry
        super().__init__(initial_data=config_entry.data)  # type: ignore[arg-type]

    @callback
    def finish_flow(self) -> FlowResult:
        """Update the ConfigEntry and finish the flow."""
        new_data = DEFAULT_ENTRY_DATA | self.initial_data | self.new_entry_data
        self.hass.config_entries.async_update_entry(
            self.config_entry,
            data=new_data,
            title=self.new_title or UNDEFINED,
        )
        self.hass.async_create_task(
            self.hass.config_entries.async_reload(self.config_entry.entry_id)
        )
        return self.async_create_entry(title="", data={})

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage Robonect options."""
        return self.async_show_menu(
            step_id="init",
            menu_options=[
                "connection_options",
                "brand_type",
                "host",
                "username_password",
                "scan_interval",
                "monitored_variables",
                "winter_mode",
            ],
        )


class RobonectConfigFlow(RobonectCommonFlow, ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Robonect."""

    VERSION = 4

    def __init__(self) -> None:
        """Initialize Robonect Config Flow."""
        super().__init__(initial_data=DEFAULT_ENTRY_DATA)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> RobonectOptionsFlow:
        """Get the options flow for this handler."""
        return RobonectOptionsFlow(config_entry)

    @callback
    def finish_flow(self) -> FlowResult:
        """Create the ConfigEntry."""
        title = self.new_title or NAME
        return self.async_create_entry(
            title=title,
            data=DEFAULT_ENTRY_DATA | self.new_entry_data,
        )

    async def async_step_user(self, user_input: dict | None = None) -> FlowResult:
        """Handle a flow initialized by the user."""
        return await self.async_step_connection_methods()

        #    async def async_step_mqtt(self, user_input: dict | None = None) -> FlowResult:
        """Handle a flow initialized by the autodiscovery."""
