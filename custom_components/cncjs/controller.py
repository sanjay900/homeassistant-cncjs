import asyncio
from typing import Callable
import jwt
import socketio
from homeassistant.core import HomeAssistant
from socketio.exceptions import ConnectionError

from .const import ControllerType

class CNCjsController:
    def __init__(self, hass: HomeAssistant, name: str, user_id: str, user_name: str, secret: str, ip: str, port: int, serial: str, baudrate: int, controllerType: ControllerType) -> None:
        self.access_token = jwt.encode({'id': user_id, 'name': user_name}, secret, algorithm='HS256')
        self.ip = ip
        self.port = port
        self._hass = hass
        self.state = None
        self.connected = False
        self.event = asyncio.Event()
        self.sio = socketio.AsyncClient()
        self.error = None
        self.id = name
        self._callbacks = set()
        @self.sio.on('workflow:state')
        async def on_message(data):
            self.state = data
            self._publish_updates()

        @self.sio.on('sender:status')
        async def on_message(data):
            # {'sp': 1, 'hold': False, 'holdReason': None, 'name': '', 'context': {}, 'size': 0, 'total': 0, 'sent': 0, 'received': 0, 'startTime': 0, 'finishTime': 0, 'elapsedTime': 0, 'remainingTime': 0}
            self._publish_updates()

        @self.sio.event
        async def connect():
            self.connected = True
            self.event.set()
            await self.sio.emit("open", data=(serial,{'baudrate': baudrate, 'controllerType': controllerType.value}))

        @self.sio.event
        async def connect_error(data):
            self.error = "connection_error_auth"
            self.connected = False
            await self.sio.disconnect()
            self.event.set()

        @self.sio.event
        async def disconnect():
            self.connected = False
    def _publish_updates(self):
        for callback in self._callbacks:
            callback()
    async def disconnect(self):
        await self.sio.disconnect()

    async def connect(self):
        self.event.clear()
        try:
            await self.sio.connect(f"http://{self.ip}:{self.port}?token={self.access_token}")
            await self.event.wait()
        except ConnectionError as e:
            self.error = "connection_error"
            self.connected = False
        return self.connected

    def register_callback(self, callback: Callable[[], None]) -> None:
        """Register callback, called when Roller changes state."""
        self._callbacks.add(callback)

    def remove_callback(self, callback: Callable[[], None]) -> None:
        """Remove previously registered callback."""
        self._callbacks.discard(callback)