import requests
import base64
import logging
from typing import List

from bs4 import BeautifulSoup

_LOGGER = logging.getLogger(__name__)

class DeviceInfo:

    def __init__(self, name: str, connection_type: str,
                  connection_status: str, online_time: str, mac: str, ip: str) -> None:
        self.name = name
        self.connection_type = connection_type
        self.connection_status = connection_status
        self.online_time = online_time
        self.mac = mac
        self.ip = ip

    def asdict(self)-> dict:
        return {
            'name': self.name,
            'connection_type': self.connection_type,
            'connection_status': self.connection_status,
            'online_time': self.online_time,
            'mac': self.mac,
            'ip': self.ip
        }

class Router:
    _headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    _mac_alias = {

    }

    _devices = []

    def __init__(self, host: str, userName: str, password: str) -> None:
        self._data = {
            'luci_username': userName,
            'luci_password': base64.b64encode(password.encode())
        }
        self._authUrl = 'http://' + host + "/api"

    def set_mac_alias(self, mac_alias):
        self._mac_alias = mac_alias

    def valid(self):
        result = requests.post(self._authUrl, data = self._data, headers=self._headers, allow_redirects=False)
        return result.status_code == 302

    def get_devices(self, only_wireless: bool = False, only_online: bool = False) -> List[DeviceInfo]:
        self._devices = []
        with requests.Session() as s:
            result = s.post(self._authUrl, data = self._data, headers = self._headers)
        if result.status_code != 200:
            _LOGGER.error(f"request router not success statusCode: {result.status_code} text: {result.text}")
            return []
        # Step 2: 获取响应的 HTML 内容
        html_content = result.text

        # Step 3: 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        # 查找所有表格行（tr），表格中的设备信息是 <tr> 标签内的
        rows = soup.find_all('tr')
        # 遍历每一行，提取设备信息
        devices = []
        for row in rows:
            columns = row.find_all('td')
            if len(columns) >= 6:  # 确保有足够的列数据
                connection_type = columns[1].get_text(strip=True)
                connection_status = columns[2].get_text(strip=True)
                if only_online is True and connection_status != '在线':
                    continue
                if only_wireless is True and (connection_status != '在线' or connection_type not in ['2.4G', '5G']):
                    continue
                name = columns[0].get_text(strip=True)
                online_time = columns[3].get_text(strip=True)
                mac = columns[4].get_text(strip=True)

                if self._mac_alias is not None and mac in self._mac_alias:
                    name = self._mac_alias[mac]
                elif name == 'unkown' or name == '未知':
                    name = mac
                ip = columns[5].get_text(strip=True)
                
                # 将设备信息添加到设备列表中
                devices.append(DeviceInfo(name,
                                          connection_type,
                                          connection_status,
                                          online_time, mac, ip))
        self._devices = devices
        return devices
    
    def get_device(self, mac: str) -> DeviceInfo:
        for device in self._devices:
            if device.mac == mac:
                return device
        return None