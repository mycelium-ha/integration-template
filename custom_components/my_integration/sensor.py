"""Sensor platform for My Integration."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.typing import StateType

from .api import DeviceStatus
from .coordinator import MyIntegrationConfigEntry, MyIntegrationCoordinator
from .entity import MyIntegrationEntity

# The coordinator does all I/O, so entities never update in parallel.
PARALLEL_UPDATES = 0


@dataclass(frozen=True, kw_only=True)
class MyIntegrationSensorEntityDescription(SensorEntityDescription):
    """Describes a My Integration sensor."""

    value_fn: Callable[[DeviceStatus], StateType]


SENSORS: tuple[MyIntegrationSensorEntityDescription, ...] = (
    MyIntegrationSensorEntityDescription(
        key="value",
        translation_key="value",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda status: status.value,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: MyIntegrationConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up sensors from a config entry."""
    coordinator = entry.runtime_data
    async_add_entities(MyIntegrationSensor(coordinator, description) for description in SENSORS)


class MyIntegrationSensor(MyIntegrationEntity, SensorEntity):
    """A sensor backed by the coordinator data."""

    entity_description: MyIntegrationSensorEntityDescription

    def __init__(
        self,
        coordinator: MyIntegrationCoordinator,
        description: MyIntegrationSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.data.serial_number}_{description.key}"

    @property
    def native_value(self) -> StateType:
        """Return the sensor value."""
        return self.entity_description.value_fn(self.coordinator.data)
