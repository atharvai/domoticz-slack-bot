import json
import unittest

import requests_mock
from domoticz import domoticz


@requests_mock.Mocker()
class TestDevice(unittest.TestCase):
    device_data = {'result': [{'Type': 'Light', 'idx': '1', 'Name': 'Device1'},
                              {'Type': 'Light', 'idx': '2', 'Name': 'Device2'},
                              ],
                   'ServerTime': '2016-07-13 01:01:01'}
    device_data_1 = {'result': [{'Type': 'Light', 'idx': '1', 'Name': 'Device1'},
                                ],
                     'ServerTime': '2016-07-13 01:01:01'}
    sunrise_data = {'Sunrise': '04:00', 'Sunset': '20:00', 'ServerTime': '2016-07-13 01:01:01',
                    'title': 'getSunRiseSet',
                    'status': 'OK'}

    def test_base_url_returns_full_endpoint(self, m):
        domo = domoticz.Domoticz('mydomoticz')
        self.assertEqual(domo.base_url, 'http://mydomoticz:8080/json.htm?', 'Generated base URL is incorrect')

    # def test_cache_device_list(self, m):
    #     m.get('http://mydomoticz:8080/json.htm?type-devices&filter=all&used=true&order=Name', text='{"result":[{"Type":"Light"}],"ServerTime":"2016-07-13 01:01:01"}')
    #     domo = domoticz.Domoticz('mydomoticz')
    #     domo._cache_device_list()
    #     self.assertEqual(len(domo.device_list), 1, 'device list is not as expected with 1 device')

    def test_device_id_map_returns_dict(self, m):
        m.get('http://mydomoticz:8080/json.htm?type-devices&filter=all&used=true&order=Name',
              text=json.dumps(self.device_data))
        domo = domoticz.Domoticz('mydomoticz')

    def test_select_device_idx_returns_device1(self, m):
        m.get('http://mydomoticz:8080/json.htm?type-devices&filter=all&used=true&order=Name',
              text=json.dumps(self.device_data))
        domo = domoticz.Domoticz('mydomoticz')
        device = domo.select_device(idx=1)
        self.assertEqual(device[0], self.device_data['result'][0]['idx'], 'Device1 not returned')

    def test_select_device_name_returns_device2(self, m):
        m.get('http://mydomoticz:8080/json.htm?type-devices&filter=all&used=true&order=Name',
              text=json.dumps(self.device_data))
        domo = domoticz.Domoticz('mydomoticz')
        device = domo.select_device(name='Device2')
        self.assertEqual(len(device), 1)
        self.assertEqual(device[0], self.device_data['result'][1]['idx'])

    def test_get_device_data_returns_device1(self, m):
        m.get('http://mydomoticz:8080/json.htm?type-devices&filter=all&used=true&order=Name',
              text=json.dumps(self.device_data))
        m.get('http://mydomoticz:8080/json.htm?rid=1&type=devices', text=json.dumps(self.device_data_1))
        domo = domoticz.Domoticz('mydomoticz')
        dev = domo.get_device_data(idx=1)
        self.assertEqual(len(dev), 1)
        self.assertDictEqual(dev[0], self.device_data['result'][0], 'Incorrect device returned')

    def test_get_device_status_returns_both_devices(self, m):
        m.get('http://mydomoticz:8080/json.htm?filter=light&used=true&type=devices&order=Name',
              text=json.dumps(self.device_data))
        domo = domoticz.Domoticz('mydomoticz')
        dev = domo.get_device_status_many('light')
        self.assertEqual(len(dev), 2)
        self.assertListEqual(dev, self.device_data['result'])

    def test_get_sunriseset_returns_sunriseset(self, m):
        m.get('http://mydomoticz:8080/json.htm?type=command&param=getSunRiseSet', text=json.dumps(self.sunrise_data))
        domo = domoticz.Domoticz('mydomoticz')
        sriseset = domo.get_sunriseset()
        self.assertDictEqual(sriseset, self.sunrise_data, 'Incorrect SunRiseSet data')
