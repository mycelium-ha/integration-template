"""Tests for the sensor platform."""

from __future__ import annotations

from dataclasses import replace
from unittest.mock import MagicMock

from homeassistant.const import STATE_UNAVAILABLE
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.my_integration.api import MyIntegrationConnectionError
from custom_components.my_integration.const import DOMAIN

from .conftest import MOCK_STATUS


def _entity_id(hass: HomeAssistant) -> str:
    entity_id = er.async_get(hass).async_get_entity_id(
        "sensor", DOMAIN, f"{MOCK_STATUS.serial_number}_value"
    )
    assert entity_id is not None
    return entity_id


async def test_sensor_state_and_device(
    hass: HomeAssistant, init_integration: MockConfigEntry
) -> None:
    """The sensor reports the device value and belongs to the device."""
    entity_id = _entity_id(hass)
    state = hass.states.get(entity_id)
    assert state is not None
    assert state.state == "21.5"
    assert state.attributes["friendly_name"] == "My Device Value"

    device = dr.async_get(hass).async_get_device_by_identifier(
        (DOMAIN, MOCK_STATUS.serial_number), init_integration.entry_id
    )
    assert device is not None
    assert device.serial_number == MOCK_STATUS.serial_number


async def test_sensor_updates_and_becomes_unavailable(
    hass: HomeAssistant, init_integration: MockConfigEntry, mock_client: MagicMock
) -> None:
    """New data updates the state; a failed poll makes the sensor unavailable."""
    entity_id = _entity_id(hass)
    coordinator = init_integration.runtime_data

    mock_client.async_get_status.return_value = replace(MOCK_STATUS, value=22.0)
    await coordinator.async_refresh()
    await hass.async_block_till_done()
    state = hass.states.get(entity_id)
    assert state is not None
    assert state.state == "22.0"

    mock_client.async_get_status.side_effect = MyIntegrationConnectionError
    await coordinator.async_refresh()
    await hass.async_block_till_done()
    state = hass.states.get(entity_id)
    assert state is not None
    assert state.state == STATE_UNAVAILABLE
