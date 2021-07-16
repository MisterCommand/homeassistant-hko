from homeassistant.components.weather import WeatherEntity
from homeassistant.const import TEMP_CELSIUS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import HKOUpdateCoordinator
from .const import (API_CONDITION, API_CURRENT, API_FORECAST, API_HUMIDITY,
                    API_TEMPERATURE, ATTRIBUTION, CONF_NAME, COORDINATOR,
                    DEFAULT_NAME, DOMAIN, MANUFACTURER)


async def async_setup_entry(hass, config_entry, async_add_entities) -> None:
    """Set up HKO weather entity based on a config entry."""
    domain = hass.data[DOMAIN][config_entry.entry_id]
    name = config_entry.data[CONF_NAME]
    unique_id = f"{config_entry.unique_id}"
    coordinator = domain[COORDINATOR]
    async_add_entities([HKOEntity(name, unique_id, coordinator)])

class HKOEntity(WeatherEntity):
    """Define a HKO entity."""

    def __init__(self, name: str, unique_id:str, coordinator: HKOUpdateCoordinator) -> None:
        self.coordinator = coordinator
        self._name = name
        self._unique_id = unique_id

    @property
    def name(self) -> str:
        """Return the name."""
        return self._name

    @property
    def attribution(self) -> str:
        """Return the attribution."""
        return ATTRIBUTION

    @property
    def unique_id(self) -> str:
        """Return a unique_id for this entity."""
        return self._unique_id
    
    @property
    def device_info(self):
        """Return the device info."""
        return {
            "identifiers": {(DOMAIN, self._unique_id)},
            "name": DEFAULT_NAME,
            "manufacturer": MANUFACTURER,
            "entry_type": "service",
        }

    @property
    def condition(self) -> str:
        """Return the current condition."""
        return self.coordinator.data[API_FORECAST][0][API_CONDITION]

    @property
    def temperature(self) -> int:
        """Return the temperature."""
        return self.coordinator.data[API_CURRENT][API_TEMPERATURE]

    @property
    def temperature_unit(self) -> str:
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    @property
    def humidity(self) -> int:
        """Return the humidity."""
        return self.coordinator.data[API_CURRENT][API_HUMIDITY]

    @property
    def forecast(self) -> list:
        """Return the forecast array."""
        return self.coordinator.data[API_FORECAST]