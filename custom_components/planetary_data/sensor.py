import logging
import requests
from datetime import timedelta
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .api import fetch_k_index

_LOGGER = logging.getLogger(__name__)

DOMAIN = "planetary_data"

async def async_setup_entry(hass, config_entry, async_add_entities):
    coordinator = KIndexDataCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()

    async_add_entities([KIndexSensor(coordinator)], update_before_add=True)

class KIndexDataCoordinator(DataUpdateCoordinator):
    def __init__(self, hass):
        super().__init__(
            hass,
            _LOGGER,
            name="Planetary K-Index",
            update_interval=timedelta(minutes=10),
        )

    async def _async_update_data(self):
        try:
            return await self.hass.async_add_executor_job(fetch_k_index)
        except Exception as err:
            _LOGGER.exception("Failed to fetch K-index data")
            raise UpdateFailed(err)

class KIndexSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Planetary K-Index"
        self._attr_unique_id = "planetary_k_index"
        self._attr_state_class = "measurement"

    @property
    def native_value(self):
        return self.coordinator.data.get("estimated_kp")

    @property
    def extra_state_attributes(self):
        return {
            "time_tag": self.coordinator.data.get("time_tag"),
        }
