"""Constants for the My Integration integration."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import Final

DOMAIN: Final = "my_integration"
LOGGER: Final = logging.getLogger(__package__)

MANUFACTURER: Final = "My Manufacturer"
DEFAULT_SCAN_INTERVAL: Final = timedelta(minutes=1)
