"""Client for the device API.

Replace this module with the API of your device or service. Once the client grows
beyond a few calls, move it into its own library on PyPI and list it in
`manifest.json` `requirements` (Quality Scale: dependency-transparency).
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass

import aiohttp

REQUEST_TIMEOUT = 10


class MyIntegrationError(Exception):
    """Base error of the device API."""


class MyIntegrationConnectionError(MyIntegrationError):
    """The device could not be reached."""


@dataclass(frozen=True, slots=True)
class DeviceStatus:
    """State reported by the device."""

    serial_number: str
    name: str
    value: float


class MyIntegrationClient:
    """Minimal async client; uses the shared Home Assistant aiohttp session."""

    def __init__(self, host: str, session: aiohttp.ClientSession) -> None:
        """Initialize the client."""
        self._host = host
        self._session = session

    async def async_get_status(self) -> DeviceStatus:
        """Fetch the current device status."""
        url = f"http://{self._host}/api/status"
        try:
            async with asyncio.timeout(REQUEST_TIMEOUT), self._session.get(url) as response:
                response.raise_for_status()
                payload = await response.json()
        except (TimeoutError, aiohttp.ClientError) as err:
            raise MyIntegrationConnectionError(f"Cannot reach {self._host}") from err

        try:
            return DeviceStatus(
                serial_number=str(payload["serial_number"]),
                name=str(payload["name"]),
                value=float(payload["value"]),
            )
        except (KeyError, TypeError, ValueError) as err:
            raise MyIntegrationError(f"Unexpected response from {self._host}") from err
