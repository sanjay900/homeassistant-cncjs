"""Support for displaying collected data over SNMP."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.sensor import SensorEntity

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


class CNCjsStateSensor(SensorEntity):
    should_poll = False
    def __init__(self, cnc):
        self.cnc = cnc
        self._attr_unique_id = f"{self.cnc.id}_state"
        self._attr_name = f"{self.cnc.name} Workflow State"
    @property
    def state(self):
        """Return the state of the sensor."""
        return self.cnc.state
    async def async_added_to_hass(self) -> None:
        """Run when this Entity has been added to HA."""
        self.cnc.register_callback(self.async_write_ha_state)

    async def async_will_remove_from_hass(self) -> None:
        """Entity being removed from hass."""
        # The opposite of async_added_to_hass. Remove any registered call backs here.
        self.cnc.remove_callback(self.async_write_ha_state)
    @property
    def available(self) -> bool:
        return self.cnc.connected
