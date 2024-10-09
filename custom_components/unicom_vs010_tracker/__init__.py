from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: ConfigEntry):
    # 注册设备追踪组件
    hass.helpers.discovery.load_platform('device_tracker', 'unicom_vs010_tracker', {}, config)
    return True