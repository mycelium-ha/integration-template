"""Data update coordinator for My Integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import DeviceStatus, MyIntegrationClient, MyIntegrationError
from .const import DEFAULT_SCAN_INTERVAL, DOMAIN, LOGGER

type MyIntegrationConfigEntry = ConfigEntry[MyIntegrationCoordinator]


class MyIntegrationCoordinator(DataUpdateCoordinator[DeviceStatus]):
    """Poll the device once per interval and share the result with all entities."""

    config_entry: MyIntegrationConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: MyIntegrationConfigEntry,
        client: MyIntegrationClient,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            LOGGER,
            config_entry=config_entry,
            name=DOMAIN,
            update_interval=DEFAULT_SCAN_INTERVAL,
        )
        self.client = client

    async def _async_update_data(self) -> DeviceStatus:
        """Fetch the latest status from the device."""
        try:
            return await self.client.async_get_status()
        except MyIntegrationError as err:
            raise UpdateFailed(
                translation_domain=DOMAIN,
                translation_key="update_failed",
                translation_placeholders={"error": str(err)},
            ) from err
