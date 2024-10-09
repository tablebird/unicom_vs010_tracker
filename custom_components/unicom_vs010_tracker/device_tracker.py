from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD, CONF_ALIAS

from homeassistant.components.device_tracker import (
    DeviceScanner,
    DOMAIN
)
from homeassistant.core import HomeAssistant
from .vs010 import Router
from .const import ONLY_WIRELESS
from homeassistant.helpers.typing import ConfigType
import logging

_LOGGER = logging.getLogger(__name__)

def get_scanner(hass: HomeAssistant, config: ConfigType) -> DeviceScanner :
    scanner = UnicomDeviceScanner(config[DOMAIN])
    return scanner if scanner.success_init else None

class UnicomDeviceScanner(DeviceScanner):

    last_results = []
    only_wireless = True

    def __init__(self, config):
        url = config[CONF_HOST]
        username = config[CONF_USERNAME]
        password = config[CONF_PASSWORD]
        if ONLY_WIRELESS in config:
            self.only_wireless = config[ONLY_WIRELESS]

        self.router = Router(url, username, password)
        if CONF_ALIAS in config:
            mac_alias =  config[CONF_ALIAS]
            self.router.set_mac_alias(mac_alias)
        self.success_init = self.router.valid()

    def scan_devices(self):
        self._update_devices()
        return [device.mac for device in self.last_results]
    
    def _update_devices(self):
        self.last_results = []
        devices = self.router.get_devices(only_online=True, only_wireless=self.only_wireless)
        for device in devices:
            self.last_results.append(device)

    def get_device_name(self, device: str) -> str:
        name = next(
            (result.name for result in self.last_results if result.mac == device),
            None
            )
        return name


    def get_extra_attributes(self, device: str) -> dict:
        device = next(
            (result for result in self.last_results if result.mac == device), None
        )
        return device.asdict()
