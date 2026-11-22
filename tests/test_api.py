"""Tests for the API client."""

from __future__ import annotations

import aiohttp
import pytest
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from pytest_homeassistant_custom_component.test_util.aiohttp import AiohttpClientMocker

from custom_components.my_integration.api import (
    MyIntegrationClient,
    MyIntegrationConnectionError,
    MyIntegrationError,
)

from .conftest import MOCK_HOST, MOCK_STATUS

URL = f"http://{MOCK_HOST}/api/status"


async def test_get_status(hass: HomeAssistant, aioclient_mock: AiohttpClientMocker) -> None:
    """A valid response is parsed into DeviceStatus."""
    aioclient_mock.get(URL, json={"serial_number": "ABC123", "name": "My Device", "value": "21.5"})
    client = MyIntegrationClient(MOCK_HOST, async_get_clientsession(hass))
    assert await client.async_get_status() == MOCK_STATUS


@pytest.mark.parametrize(
    "mock_kwargs",
    [
        {"exc": aiohttp.ClientError()},
        {"exc": TimeoutError()},
        {"status": 500},
    ],
)
async def test_connection_errors(
    hass: HomeAssistant, aioclient_mock: AiohttpClientMocker, mock_kwargs: dict[str, object]
) -> None:
    """Network errors, timeouts and HTTP errors raise MyIntegrationConnectionError."""
    aioclient_mock.get(URL, **mock_kwargs)
    client = MyIntegrationClient(MOCK_HOST, async_get_clientsession(hass))
    with pytest.raises(MyIntegrationConnectionError):
        await client.async_get_status()


async def test_unexpected_payload(hass: HomeAssistant, aioclient_mock: AiohttpClientMocker) -> None:
    """A response without the expected fields raises MyIntegrationError."""
    aioclient_mock.get(URL, json={"name": "My Device"})
    client = MyIntegrationClient(MOCK_HOST, async_get_clientsession(hass))
    with pytest.raises(MyIntegrationError) as err:
        await client.async_get_status()
    assert not isinstance(err.value, MyIntegrationConnectionError)
