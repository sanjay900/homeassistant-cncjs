
"""The CNCjs sensor integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from . import controller
from .const import CONF_USER_ID, DOMAIN, CONF_CONTROLLER_TYPE, CONF_SERIAL_PORT, CONF_BAUDRATE, ControllerType
from homeassistant.const import (
    CONF_IP_ADDRESS,
    CONF_ACCESS_TOKEN,
    CONF_NAME,
    CONF_USERNAME,
    CONF_PORT,
)

# List of platforms to support. There should be a matching .py file for each,
# eg <cover.py> and <sensor.py>
PLATFORMS: list[str] = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up CNCjs from a config entry."""
    # Store an instance of the "connecting" class that does the work of speaking
    # with your actual devices.
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = controller.CNCjsController(hass, entry.data[CONF_USER_ID], entry.data[CONF_USERNAME], entry.data[CONF_ACCESS_TOKEN], entry.data[CONF_IP_ADDRESS], entry.data[CONF_PORT], entry.data[CONF_SERIAL_PORT], entry.data[CONF_BAUDRATE], ControllerType(entry.data[CONF_CONTROLLER_TYPE]))

    # This creates each HA object for each platform your device requires.
    # It's done by calling the `async_setup_entry` function in each platform module.
    hass.config_entries.async_setup_platforms(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # This is called when an entry/configured device is to be removed. The class
    # needs to unload itself, and remove callbacks. See the classes for further
    # details
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
