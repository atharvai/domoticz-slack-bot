import requests
from endpoints import devices

class Domoticz:
    host = ''
    port = 8080
    endpoint = 'json.htm?'

    @property
    def base_url(self):
        return 'http://{host}:{port}/{endpoint}'.format(host=self.host,
                                                        port=self.port,
                                                        endpoint=self.endpoint,
                                                        )

    device_list = []
    devices_last_update = ''

    def __init__(self, host, port = 8080):
        self.host = host
        self.port = port
        self._cache_device_list()

    def _cache_device_list(self):
        req = requests.get(self.base_url,devices.get('all'))
        self.device_list = req.json()['result']
        self.devices_last_update = req.json()['ServerTime']

    def get_device_data(self, idx=None, name=None):
        selected_dev = self.select_device(idx, name)
        if selected_dev is None:
            return
        return selected_dev

    def select_device(self, idx=None, name=None):
        if (idx is None and name is None):
            raise Exception('Please provide either idx or name. Providing both will use idx value.')
        selected_dev = {}
        if idx is not None:
            result = filter(lambda d: d['idx'] == str(idx), self.device_list)
            if len(result) >= 1:
                selected_dev = result[0]
        if name is not None:
            result = filter(lambda d: d['Name'] == str(name), self.device_list)
            if len(result) >= 1:
                selected_dev = result[0]
        return selected_dev

    def get_device_status_many(self, device_type):
        if device_type is not None:
            req = requests.get(self.base_url, devices['temp'])
            return req.json()['result']