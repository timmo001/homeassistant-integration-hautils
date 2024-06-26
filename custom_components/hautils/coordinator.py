"""Coordinator for Home Assistant Utilities integration."""

# from asyncio import Task
# from datetime import timedelta
# import logging
# from typing import Any

# from homeassistant.config_entries import ConfigEntry
# from homeassistant.core import HomeAssistant
# from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

# from .const import DOMAIN
# from .data import HAUtilsData


# class HAUtilsDataUpdateCoordinator(DataUpdateCoordinator[HAUtilsData]):
#     """Class to manage fetching Home Assistant Utilities data from single endpoint."""

#     def __init__(
#         self,
#         hass: HomeAssistant,
#         LOGGER: logging.Logger,
#         *,
#         entry: ConfigEntry,
#     ) -> None:
#         """Initialize global Home Assistant Utilities data updater."""
#         self._entry_data: dict[str, Any] = entry.data.copy()
#         self._listener_task: Task | None = None
#         self.title = entry.title

#         super().__init__(
#             hass,
#             LOGGER,
#             name=DOMAIN,
#             update_interval=timedelta(seconds=30),
#         )

#     async def _async_update_data(self) -> HAUtilsData:
#         """Update Home Assistant Utilities data from WebSocket."""

#         return HAUtilsData()
