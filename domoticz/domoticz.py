import time
from datetime import datetime
from itertools import groupby

import requests
from endpoints import devices, command, uservariables, uservariable_type


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

    def __init__(self, host, port=8080):
        self.host = host
        self.port = port
        # self._cache_device_list()

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
        req = requests.get(self.base_url, devices.get('all'))
        self._device_list = req.json()['result']
        self.devices_last_update = datetime.strptime(req.json()['ServerTime'], '%Y-%m-%d %H:%M:%S')

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

    def get_all_variables(self):
        req = requests.get(self.base_url, uservariables['all'])
        return req.json()['result']

    def get_user_variable_type_id(self, name):
        if name.lower() == 'int' or name.lower() == 'integer':
            return uservariable_type['Integer']
        elif name.lower() == 'float':
            return uservariable_type['Float']
        elif name.lower() == 'str' or name.lower() == 'string':
            return uservariable_type['String']
        elif name.lower() == 'date':
            return uservariable_type['Date']
        elif name.lower() == 'time':
            return uservariable_type['Time']
        else:
            return None

    def get_variable_idx_by_name(self, name):
        var_idx = None
        if name is None:
            return None
        else:
            req = requests.get(self.base_url, uservariables['all'])
            vars = req.json()['result']
            selected = filter(lambda v: v['Name'].lower() == name.lower(), vars)
            if len(selected) > 0:
                var_idx = str(selected[0]['idx'])
            else:
                return None
        return var_idx

    def get_user_variable(self, name=None, idx=None):
        var_idx = None
        var_value = None
        if idx is not None:
            var_idx = idx
        if name is not None and var_idx is None:
            var_idx = self.get_variable_idx_by_name(name)
            if var_idx is None:
                return 'Variable `{}` not found'.format(name)
        if var_idx > 0:
            params = uservariables['byIdx'].copy()
            params['idx'] = var_idx
            req = requests.get(self.base_url, params)
            if 'result' not in req.json():
                return 'Variable `{}` not found'.format(var_idx)
            var_value = req.json()['result'][0]['Value']
            var_type = req.json()['result'][0]['Type']

            # Type cast to return proper value
            try:
                if int(var_type) == 0:
                    var_value = int(var_value)
                elif int(var_type) == 1:
                    var_value = float(var_value)
                elif int(var_type) == 2:
                    var_value = str(var_value)
                elif int(var_type) == 3:
                    var_value = datetime.strptime(var_value, '%Y-%m-%d').date()
                elif int(var_type) == 4:
                    var_value = time.strptime(var_value, '%H:%M')
            except:
                var_value = str(var_value)
        return var_value

    def create_or_update_user_variable(self, name, value, var_type=2):
        try:
            if int(var_type) == 3:
                if isinstance(value, datetime):
                    var_value = datetime.strftime(value, '%Y-%m-%d')
            elif int(var_type) == 4:
                if isinstance(value, time):
                    var_value = time.strftime(value, '%H:%M')
        finally:
            var_value = str(value)

        params = uservariables['save'].copy()
        params['vname'] = name
        params['vvalue'] = var_value
        params['vtype'] = str(var_type)
        req = requests.get(self.base_url, params)
        status = req.json()
        if status == 'Variable name already exists!':
            params['param'] = uservariables['update']['param']
            req = requests.get(self.base_url, params)
            status = req.json()
        return status

    def delete_user_variable(self, name=None, idx=None):
        var_idx = None
        if idx is not None:
            var_idx = idx
        if name is not None and var_idx is None:
            var_idx = self.get_variable_idx_by_name(name)

        params = uservariables['delete'].copy()
        params['idx'] = str(var_idx)
        req = requests.get(self.base_url, params)
        return req.json()['status']
