"""Config flow for My Integration."""

from __future__ import annotations

from typing import Any

import probatio
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_HOST
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import MyIntegrationClient, MyIntegrationConnectionError
from .const import DOMAIN, LOGGER

# Home Assistant uses probatio (the successor of voluptuous) for flow schemas.
STEP_USER_DATA_SCHEMA = probatio.Schema({probatio.Required(CONF_HOST): str})


class MyIntegrationConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for My Integration."""

    VERSION = 1
    MINOR_VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Ask for the host and test the connection before creating the entry."""
        errors: dict[str, str] = {}
        if user_input is not None:
            client = MyIntegrationClient(user_input[CONF_HOST], async_get_clientsession(self.hass))
            try:
                status = await client.async_get_status()
            except MyIntegrationConnectionError:
                errors["base"] = "cannot_connect"
            except Exception:  # noqa: BLE001 - the flow must never crash on unknown errors
                LOGGER.exception("Unexpected error while connecting")
                errors["base"] = "unknown"
            else:
                # One entry per physical device; a known device gets its new address.
                await self.async_set_unique_id(status.serial_number)
                self._abort_if_unique_id_configured(updates={CONF_HOST: user_input[CONF_HOST]})
                return self.async_create_entry(title=status.name, data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=self.add_suggested_values_to_schema(STEP_USER_DATA_SCHEMA, user_input),
            errors=errors,
        )
