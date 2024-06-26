"""Services for Home Assistant Utilities integration."""

from collections.abc import Callable, Coroutine
from dataclasses import dataclass, field
from typing import Any, cast

import voluptuous as vol

from homeassistant.core import (
    EntityServiceResponse,
    HomeAssistant,
    ServiceCall,
    ServiceResponse,
    SupportsResponse,
    callback,
)
from homeassistant.helpers.entity_platform import EntityPlatform

from .const import DOMAIN, LOGGER

SCHEMA_LIST_INTEGRATIONS = vol.Schema({})


@dataclass
class HAUtilsService:
    """Class to represent a Home Assistant Utilities service."""

    name: str
    service_func: Callable[
        [ServiceCall],
        Coroutine[Any, Any, ServiceResponse | EntityServiceResponse]
        | ServiceResponse
        | EntityServiceResponse
        | None,
    ]
    supports_response: SupportsResponse = SupportsResponse.NONE


@dataclass
class HAUtilsServiceManager:
    """Class to manage Home Assistant Utilities services."""

    hass: HomeAssistant

    _services: set[HAUtilsService] = field(default_factory=set)

    def __post_init__(self) -> None:
        """Post initialization."""
        LOGGER.debug("Home Assistant Utilities service manager initialized")

    async def async_setup(self) -> None:
        """Set up the Home Assistant Utilities services."""
        LOGGER.debug("Setting up Home Assistant Utilities services")

        # Register the services
        services = [
            HAUtilsService(
                name="list_integrations_core",
                service_func=self.list_integrations_core,
                supports_response=SupportsResponse.ONLY,
            ),
            HAUtilsService(
                name="list_integrations_custom",
                service_func=self.list_integrations_custom,
                supports_response=SupportsResponse.ONLY,
            ),
        ]

        for service in services:
            LOGGER.debug(
                "Registering service: %s.%s",
                DOMAIN,
                service.name,
            )
            self.hass.services.async_register(
                domain=DOMAIN,
                service=service.name,
                service_func=service.service_func,
                schema=None,
                supports_response=service.supports_response,
            )

    @callback
    def async_on_unload(self) -> None:
        """Tear down the Home Assistant Utilities services."""
        LOGGER.debug("Tearing down Home Assistant Utilities services")
        for service in self._services:
            LOGGER.debug(
                "Unregistering service: %s.%s",
                DOMAIN,
                service.name,
            )
            self.hass.services.async_remove(
                domain=DOMAIN,
                service=service.name,
            )

    def list_integrations_core(
        self,
        _: ServiceCall,
    ) -> ServiceResponse:
        """List the integrations in Home Assistant."""
        LOGGER.debug("Listing integrations in Home Assistant")
        entity_platforms: dict[str, EntityPlatform] = self.hass.data["entity_platform"]
        integrations: list[str] = [platform for platform, _ in entity_platforms.items()]
        return cast(
            ServiceResponse,
            {
                "count": len(integrations),
                "integrations": integrations,
            },
        )

    def list_integrations_custom(
        self,
        _: ServiceCall,
    ) -> ServiceResponse:
        """List the integrations in Home Assistant."""
        LOGGER.debug("Listing integrations in Home Assistant")
        entity_platforms: dict[str, EntityPlatform] = self.hass.data[
            "custom_components"
        ]
        integrations: list[str] = [platform for platform, _ in entity_platforms.items()]
        return cast(
            ServiceResponse,
            {
                "count": len(integrations),
                "integrations": integrations,
            },
        )
