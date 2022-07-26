from __future__ import annotations

from datetime import timedelta
from enum import Enum

import logging
from typing import Final
CONF_CONTROLLER_TYPE = "controllertype"
CONF_BAUDRATE = "baudrate"
CONF_SERIAL_PORT = "serialport"
CONF_USER_ID = "user_id"

SERVICE_CNCJS: Final = "cncjs"
SCAN_INTERVAL = timedelta(seconds=10)
LOGGER = logging.getLogger(__package__)
DOMAIN = "cncjs"

class ControllerType(Enum):
    Marlin = "Marlin"
    Grbl = "Grbl"
    Smoothie = "Smoothie"
    TinyG = "TinyG"