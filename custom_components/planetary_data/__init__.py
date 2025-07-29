from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .api import fetch_k_index

DOMAIN = "planetary_data"
PLATFORMS = ["sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    # Optional: try fetching data early to test connection
    try:
        await hass.async_add_executor_job(fetch_k_index)
    except Exception as err:
        raise ConfigEntryNotReady(f"Initial data fetch failed: {err}")

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass, entry):
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    return unload_ok
