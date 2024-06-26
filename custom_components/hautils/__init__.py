"""The Home Assistant Utilities integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

# from .coordinator import HAUtilsDataUpdateCoordinator
from .services import HAUtilsServiceManager

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = []

# type HAUtilsConfigEntry = ConfigEntry[HAUtilsDataUpdateCoordinator]
type HAUtilsConfigEntry = ConfigEntry


async def async_setup_entry(
    hass: HomeAssistant,
    entry: HAUtilsConfigEntry,
) -> bool:
    """Set up Home Assistant Utilities from a config entry."""
    # # Create the data update coordinator
    # coordinator = HAUtilsDataUpdateCoordinator(
    #     hass,
    #     _LOGGER,
    #     entry=entry,
    # )

    # # Store the coordinator in runtime data
    # entry.runtime_data = coordinator

    # # Fetch initial data so we have data when entities subscribe
    # await coordinator.async_config_entry_first_refresh()

    # Set up platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Set up services
    services = HAUtilsServiceManager(hass)
    await services.async_setup()
    entry.async_on_unload(services.async_on_unload)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload Azure DevOps config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
