"""Base entity for My Integration."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER
from .coordinator import MyIntegrationCoordinator


class MyIntegrationEntity(CoordinatorEntity[MyIntegrationCoordinator]):
    """Common device info and naming for all entities."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: MyIntegrationCoordinator) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        status = coordinator.data
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, status.serial_number)},
            manufacturer=MANUFACTURER,
            name=status.name,
            serial_number=status.serial_number,
        )
