import requests
from endpoints import devices, command
from datetime import datetime, timedelta
from itertools import groupby

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

    _device_list = []
    device_list_by_type = {}
    devices_last_update = ''

    def __init__(self, host, port = 8080):
        self.host = host
        self.port = port
        #self._cache_device_list()

    @property
    def device_list(self):
        if self._device_list == [] or ((datetime.utcnow() - self.devices_last_update).seconds >= 300):
            self._cache_device_list()
        return self._device_list

    @property
    def device_id_map(self):
        return dict(map(lambda d: (d['Name'], d['idx']), self._device_list))

    def _cache_device_list(self):
        # TODO: make this a live API call every time or use job queue system
        req = requests.get(self.base_url,devices.get('all'))
        self._device_list = req.json()['result']
        self.devices_last_update = datetime.strptime(req.json()['ServerTime'],'%Y-%m-%d %H:%M:%S')

        grouped = groupby(self._device_list, lambda d: d['Type'])
        new_list = {}
        for k, v in grouped:
            if k in new_list:
                new_list[k] = new_list[k] + list(v)
            else:
                new_list[k] = list(v)
        self.device_list_by_type = new_list

    def get_device_data(self, idx=None, name=None):
        selected_dev = self.select_device(idx, name)
        if selected_dev is None or len(selected_dev) == 0:
            return
        return selected_dev

    def select_device(self, idx=None, name=None, count=1):
        if idx is None and name is None:
            raise Exception('Please provide either idx or name. Providing both will use idx value.')
        selected_dev = []
        if idx is not None:
            result = filter(lambda d: d['idx'] == str(idx), self.device_list)
            if len(result) >= 1:
                selected_dev = result[:count]
        if name is not None:
            result = filter(lambda d: d['Name'] == str(name), self.device_list)
            if len(result) >= 1:
                selected_dev = result[:count]
        return selected_dev

    def get_device_status_many(self, device_type):
        if device_type is not None:
            req = requests.get(self.base_url, devices[device_type])
            return req.json()['result']


    def get_sunriseset(self):
        req = requests.get(self.base_url, command['sunriseset'])
        return req.json()