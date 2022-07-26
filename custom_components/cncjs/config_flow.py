"""Config flow to configure the igrill integration."""
from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries, exceptions
from homeassistant.config_entries import ConfigEntry, ConfigFlow
from homeassistant.const import (
    CONF_IP_ADDRESS,
    CONF_ACCESS_TOKEN,
    CONF_NAME,
    CONF_USERNAME,
    CONF_PORT,
)
from homeassistant.data_entry_flow import FlowResult

from .controller import CNCjsController

from .const import CONF_USER_ID, DOMAIN, CONF_CONTROLLER_TYPE, CONF_SERIAL_PORT, CONF_BAUDRATE, ControllerType

class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""

class CNCjsFlowHandler(ConfigFlow, domain=DOMAIN):
    """Config flow for cncjs."""

    VERSION = 1

    entry: ConfigEntry | None = None

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initialized by the user."""
        errors = {}

        if user_input is not None:
            user_id = user_input[CONF_USER_ID] if CONF_USER_ID in user_input else ""
            cncjs = CNCjsController(None, user_input[CONF_NAME], user_id, user_input[CONF_USERNAME], user_input[CONF_ACCESS_TOKEN], user_input[CONF_IP_ADDRESS], user_input[CONF_PORT], user_input[CONF_SERIAL_PORT], user_input[CONF_BAUDRATE], user_input[CONF_CONTROLLER_TYPE])
            if not await cncjs.connect():
                errors["base"] = cncjs.error
            else:
                await cncjs.disconnect()
                return self.async_create_entry(
                    title=user_input[CONF_NAME],
                    data={
                        CONF_CONTROLLER_TYPE: user_input[CONF_CONTROLLER_TYPE].value,
                        CONF_NAME: user_input[CONF_NAME],
                        CONF_IP_ADDRESS: user_input[CONF_IP_ADDRESS],
                        CONF_ACCESS_TOKEN: user_input[CONF_ACCESS_TOKEN],
                        CONF_PORT: user_input[CONF_PORT],
                        CONF_USER_ID: user_id,
                        CONF_USERNAME: user_input[CONF_USERNAME],
                        CONF_SERIAL_PORT: user_input[CONF_SERIAL_PORT],
                        CONF_BAUDRATE: user_input[CONF_BAUDRATE],
                    },
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_NAME): str,
                    vol.Required(CONF_IP_ADDRESS): str,
                    vol.Required(CONF_PORT, default=8000): int,
                    vol.Optional(CONF_USER_ID): str,
                    vol.Required(CONF_USERNAME, default="cncjs-pendant"): str,
                    vol.Required(CONF_ACCESS_TOKEN): str,
                    vol.Required(CONF_SERIAL_PORT): str,
                    vol.Required(CONF_BAUDRATE, default=115200): int,
                    vol.Required(CONF_CONTROLLER_TYPE): vol.Coerce(ControllerType),
                }
            ),
            errors=errors,
        )
