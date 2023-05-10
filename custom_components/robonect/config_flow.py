"""Config flow to configure the Robonect integration."""
from abc import ABC
from abc import abstractmethod
from typing import Any

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.config_entries import ConfigFlow
from homeassistant.config_entries import OptionsFlow
from homeassistant.const import CONF_HOST
from homeassistant.const import CONF_PASSWORD
from homeassistant.const import CONF_USERNAME
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowHandler
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.selector import NumberSelector
from homeassistant.helpers.selector import NumberSelectorConfig
from homeassistant.helpers.selector import NumberSelectorMode
from homeassistant.helpers.selector import SelectSelector
from homeassistant.helpers.selector import SelectSelectorConfig
from homeassistant.helpers.selector import SelectSelectorMode
from homeassistant.helpers.selector import TextSelector
from homeassistant.helpers.selector import TextSelectorConfig
from homeassistant.helpers.selector import TextSelectorType
from homeassistant.helpers.typing import UNDEFINED

from .client import RobonectClient
from .const import CONF_TRACKING
from .const import CONF_UPDATE_INTERVAL
from .const import DEFAULT_UPDATE_INTERVAL
from .const import DOMAIN
from .const import NAME
from .const import SENSOR_GROUPS
from .exceptions import BadCredentialsException
from .exceptions import RobonectServiceException
from .models import RobonectConfigEntryData
from .utils import log_debug

DEFAULT_ENTRY_DATA = RobonectConfigEntryData(
    host=None,
    username=None,
    password=None,
    tracking=[],
    update_interval=DEFAULT_UPDATE_INTERVAL,
)


class RobonectCommonFlow(ABC, FlowHandler):
    """Base class for Robonect flows."""

    def __init__(self, initial_data: RobonectConfigEntryData) -> None:
        """Initialize RobonectCommonFlow."""
        self.initial_data = initial_data
        self.new_entry_data = RobonectConfigEntryData()
        self.new_title: str | None = None

    @abstractmethod
    def finish_flow(self) -> FlowResult:
        """Finish the flow."""

    def new_data(self):
        """Construct new data."""
        return DEFAULT_ENTRY_DATA | self.initial_data | self.new_entry_data

    async def async_validate_input(self, user_input: dict[str, Any]) -> None:
        """Validate user credentials."""

        client = RobonectClient(
            host=user_input[CONF_HOST],
            username=user_input[CONF_USERNAME],
            password=user_input[CONF_PASSWORD],
            tracking=user_input[CONF_TRACKING],
            update_interval=user_input[CONF_UPDATE_INTERVAL],
        )

        return await self.hass.async_add_executor_job(client.login)

    async def async_step_connection_init(
        self, user_input: dict | None = None
    ) -> FlowResult:
        """Handle connection configuration."""
        errors: dict = {}

        if user_input is not None:
            user_input = self.new_data() | user_input
            test = await self.test_connection(user_input)
            log_debug(test)
            if not test["errors"]:
                self.new_title = test["profile"].get("name")
                self.new_entry_data |= user_input
                await self.async_set_unique_id(f"{DOMAIN}_" + test["profile"].get("id"))
                self._abort_if_unique_id_configured()
                log_debug(f"New account {self.new_title} added")
                return self.finish_flow()
            errors = test["errors"]
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
                CONF_UPDATE_INTERVAL, default=DEFAULT_UPDATE_INTERVAL
            ): NumberSelector(
                NumberSelectorConfig(min=1, max=60, step=1, mode=NumberSelectorMode.BOX)
            ),
            vol.Required(CONF_TRACKING, default=SENSOR_GROUPS): SelectSelector(
                SelectSelectorConfig(
                    options=SENSOR_GROUPS,
                    multiple=True,
                    custom_value=False,
                    mode=SelectSelectorMode.DROPDOWN,
                    translation_key=CONF_TRACKING,
                )
            ),
        }
        return self.async_show_form(
            step_id="connection_init",
            data_schema=vol.Schema(fields),
            errors=errors,
        )

    async def test_connection(self, user_input: dict | None = None) -> dict:
        """Test the connection to Robonect."""
        errors: dict = {}
        profile: dict = {}

        if user_input is not None:
            user_input = self.new_data() | user_input
            try:
                profile = await self.async_validate_input(user_input)
            except AssertionError as exception:
                errors["base"] = "cannot_connect"
                log_debug(f"[async_step_password|login] AssertionError {exception}")
            except ConnectionError:
                errors["base"] = "cannot_connect"
            except RobonectServiceException:
                errors["base"] = "service_error"
            except BadCredentialsException:
                errors["base"] = "invalid_auth"
            except Exception as exception:
                errors["base"] = "unknown"
                log_debug(exception)
        return {"profile": profile, "errors": errors}

    async def async_step_password(self, user_input: dict | None = None) -> FlowResult:
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
            vol.Required(CONF_PASSWORD): cv.string,
        }
        return self.async_show_form(
            step_id="password",
            data_schema=self.add_suggested_values_to_schema(
                vol.Schema(fields),
                self.initial_data
                | RobonectConfigEntryData(
                    password=None,
                ),
            ),
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

    async def async_step_update_interval(
        self, user_input: dict | None = None
    ) -> FlowResult:
        """Configure update interval."""
        errors: dict = {}

        if user_input is not None:
            self.new_entry_data |= user_input
            return self.finish_flow()

        fields = {
            vol.Required(CONF_UPDATE_INTERVAL): NumberSelector(
                NumberSelectorConfig(min=1, max=60, step=1, mode=NumberSelectorMode.BOX)
            ),
        }
        return self.async_show_form(
            step_id="update_interval",
            data_schema=self.add_suggested_values_to_schema(
                vol.Schema(fields),
                self.initial_data,
            ),
            errors=errors,
        )

    async def async_step_sensors(self, user_input: dict | None = None) -> FlowResult:
        """Configure sensors."""
        errors: dict = {}

        if user_input is not None:
            self.new_entry_data |= user_input
            return self.finish_flow()

        fields = {
            vol.Required(CONF_TRACKING): SelectSelector(
                SelectSelectorConfig(
                    options=SENSOR_GROUPS,
                    multiple=True,
                    custom_value=False,
                    mode=SelectSelectorMode.DROPDOWN,
                    translation_key=CONF_TRACKING,
                )
            ),
        }
        return self.async_show_form(
            step_id="sensors",
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
            step_id="options_init",
            menu_options=[
                "host",
                "password",
                "update_interval",
                "sensors",
            ],
        )


class RobonectConfigFlow(RobonectCommonFlow, ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Robonect."""

    VERSION = 1

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
        return await self.async_step_connection_init()
