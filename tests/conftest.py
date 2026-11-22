"""Shared fixtures for the My Integration tests (real Home Assistant core)."""

from __future__ import annotations

from collections.abc import Generator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.my_integration.api import DeviceStatus
from custom_components.my_integration.const import DOMAIN

MOCK_HOST = "192.0.2.10"
MOCK_STATUS = DeviceStatus(serial_number="ABC123", name="My Device", value=21.5)


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations: None) -> None:
    """Load custom_components/my_integration in every test."""


@pytest.fixture
def mock_config_entry() -> MockConfigEntry:
    """Return a config entry for the mocked device."""
    return MockConfigEntry(
        domain=DOMAIN,
        title=MOCK_STATUS.name,
        data={CONF_HOST: MOCK_HOST},
        unique_id=MOCK_STATUS.serial_number,
    )


@pytest.fixture
def mock_client() -> Generator[MagicMock]:
    """Replace the API client in the integration and the config flow."""
    with (
        patch(
            "custom_components.my_integration.MyIntegrationClient", autospec=True
        ) as client_class,
        patch("custom_components.my_integration.config_flow.MyIntegrationClient", new=client_class),
    ):
        client = client_class.return_value
        client.async_get_status.return_value = MOCK_STATUS
        yield client


@pytest.fixture
def mock_setup_entry() -> Generator[AsyncMock]:
    """Prevent the integration from being set up during config flow tests."""
    with patch(
        "custom_components.my_integration.async_setup_entry", return_value=True
    ) as mock_setup:
        yield mock_setup


@pytest.fixture
async def init_integration(
    hass: HomeAssistant, mock_config_entry: MockConfigEntry, mock_client: MagicMock
) -> MockConfigEntry:
    """Set up the integration with the mocked client and return the entry."""
    mock_config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    return mock_config_entry
