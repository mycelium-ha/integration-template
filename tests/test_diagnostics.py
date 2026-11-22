"""Tests for diagnostics."""

from __future__ import annotations

import json

from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.my_integration.diagnostics import async_get_config_entry_diagnostics

from .conftest import MOCK_HOST, MOCK_STATUS


async def test_diagnostics_redact_identifiers(
    hass: HomeAssistant, init_integration: MockConfigEntry
) -> None:
    """Diagnostics contain the data but no host, serial number or device name."""
    result = await async_get_config_entry_diagnostics(hass, init_integration)

    assert result["last_update_success"] is True
    assert result["data"]["value"] == MOCK_STATUS.value
    dumped = json.dumps(result, default=str)
    for secret in (MOCK_HOST, MOCK_STATUS.serial_number, MOCK_STATUS.name):
        assert secret not in dumped
