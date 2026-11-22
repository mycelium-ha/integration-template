"""The My Integration integration."""

from __future__ import annotations

from homeassistant.const import CONF_HOST, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import MyIntegrationClient
from .coordinator import MyIntegrationConfigEntry, MyIntegrationCoordinator

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: MyIntegrationConfigEntry) -> bool:
    """Set up My Integration from a config entry."""
    client = MyIntegrationClient(entry.data[CONF_HOST], async_get_clientsession(hass))
    coordinator = MyIntegrationCoordinator(hass, entry, client)
    # Raises ConfigEntryNotReady if the device cannot be reached (test-before-setup).
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: MyIntegrationConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
