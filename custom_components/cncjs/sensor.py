"""Support for displaying collected data over SNMP."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.sensor import Entity

from .const import (
    DOMAIN
)
import socketio

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    cnc = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([
        CNCjsStateSensor(
            cnc=cnc
        )
    ])


class CNCjsStateSensor(Entity):
    def __init__(self, cnc):
        self.cnc = cnc
        self.state = "unknown"
    _attr_name = "Workflow State"
    @property
    def state(self):
        """Return the state of the sensor."""
        return self.cnc.state
