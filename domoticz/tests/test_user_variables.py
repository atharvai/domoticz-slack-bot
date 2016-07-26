import json
import unittest
import requests_mock
from domoticz import domoticz
from datetime import date
import time

@requests_mock.Mocker()
class TestUserVariables(unittest.TestCase):
    var_integer = {
        'Name': 'var_integer',
        'Value': '1',
        'Type': '0',
        'idx': '1'
    }
    var_float = {
        'Name': 'var_float',
        'Value': '3.142',
        'Type': '1',
        'idx': '2'
    }
    var_str = {
        'Name': 'var_string',
        'Value': 'dummyval',
        'Type': '2',
        'idx': '3'
    }
    var_date = {
        'Name': 'var_date',
        'Value': '2016-01-01',
        'Type': '3',
        'idx': '4'
    }
    var_time = {
        'Name': 'var_time',
        'Value': '16:00',
        'Type': '4',
        'idx': '5'
    }
    var_new = {
        'Name': 'var_new',
        'Value': 'newvalue',
        'Type': '2',
        'idx': '6'
    }
    all_vars = [var_integer, var_float, var_str, var_date, var_time]

    def test_get_all_variables_returns_five_vars(self, m):
        domo = domoticz.Domoticz('mydomoticz')
        m.get('http://mydomoticz:8080/json.htm?type=command&param=getuservariables', text='{{"status":"OK", "result":{data}}}'.format(data=json.dumps(self.all_vars)))
        actual_vars = domo.get_all_variables()
        self.assertEqual(5, len(actual_vars))
        self.assertListEqual(actual_vars, self.all_vars)

    def test_get_variable_by_idx_returns_one(self, m):
        domo = domoticz.Domoticz('mydomoticz')
        m.get('http://mydomoticz:8080/json.htm?type=command&param=getuservariable&idx=1', text='{{"status":"OK", "result":{data}}}'.format(data=json.dumps([self.var_integer])))
        var = domo.get_user_variable(idx=1)
        self.assertTrue(isinstance(var, int))
        self.assertEqual(var, 1)

    def test_get_variable_by_name_returns_dummyval(self, m):
        domo = domoticz.Domoticz('mydomoticz')
        m.get('http://mydomoticz:8080/json.htm?type=command&param=getuservariables', text='{{"status":"OK", "result":{data}}}'.format(data=json.dumps(self.all_vars)))
        m.get('http://mydomoticz:8080/json.htm?type=command&param=getuservariable&idx=3', text='{{"status":"OK", "result":{data}}}'.format(data=json.dumps([self.var_str])))
        var = domo.get_user_variable(name='var_string')
        self.assertTrue(isinstance(var, str))
        self.assertEqual(var, 'dummyval')

    def test_get_variable_float_returns_float(self, m):
        domo = domoticz.Domoticz('mydomoticz')
        m.get('http://mydomoticz:8080/json.htm?type=command&param=getuservariable&idx=2', text='{{"status":"OK", "result":{data}}}'.format(data=json.dumps([self.var_float])))
        var = domo.get_user_variable(idx=2)
        self.assertTrue(isinstance(var, float))
        self.assertEqual(var, 3.142)

    def test_get_variable_date_returns_date(self, m):
        domo = domoticz.Domoticz('mydomoticz')
        m.get('http://mydomoticz:8080/json.htm?type=command&param=getuservariable&idx=4', text='{{"status":"OK", "result":{data}}}'.format(data=json.dumps([self.var_date])))
        var = domo.get_user_variable(idx=4)
        self.assertTrue(isinstance(var, date))
        self.assertEqual(var, date(2016,1,1))

    def test_get_variable_time_returns_time(self, m):
        domo = domoticz.Domoticz('mydomoticz')
        m.get('http://mydomoticz:8080/json.htm?type=command&param=getuservariable&idx=5', text='{{"status":"OK", "result":{data}}}'.format(data=json.dumps([self.var_time])))
        var = domo.get_user_variable(idx=5)
        self.assertTrue(isinstance(var, time.struct_time))
        self.assertEqual(var, time.strptime('16:00', '%H:%M'))

    def test_create_or_update_user_variable_returns_new_ok(self, m):
        domo = domoticz.Domoticz('mydomoticz')
        m.get('http://mydomoticz:8080/json.htm?type=command&param=getuservariables', text='{{"status":"OK", "result":{data}}}'.format(data=json.dumps(self.all_vars)))
        m.get('http://mydomoticz:8080/json.htm?type=command&param=saveuservariable&vname=var_new&vtype=2&vvalue=newvalue', text='{"status":"OK"}')
        result = domo.create_or_update_user_variable('var_new','newvalue')
        m.get('http://mydomoticz:8080/json.htm?type=command&param=getuservariable&idx=6', text='{{"status":"OK", "result":{data}}}'.format(data=json.dumps([self.var_new])))
        var = domo.get_user_variable(idx=6)
        self.assertTrue(isinstance(var, str))
        self.assertEqual(var, 'newvalue')

    def test_create_or_update_user_variable_returns_updates_value(self, m):
        domo = domoticz.Domoticz('mydomoticz')
        m.get('http://mydomoticz:8080/json.htm?type=command&param=getuservariables', text='{{"status":"OK", "result":{data}}}'.format(data=json.dumps(self.all_vars)))
        m.get('http://mydomoticz:8080/json.htm?type=command&param=saveuservariable&vname=var_str&vtype=2&vvalue=newvalue', text='{"status":"OK"}')
        m.get('http://mydomoticz:8080/json.htm?type=command&param=updateuservariable&vname=var_str&vtype=2&vvalue=newvalue', text='{"status":"OK"}')
        result = domo.create_or_update_user_variable('var_str','newvalue')
        var_string = self.var_str.copy()
        var_string['Value'] = 'newvalue'
        m.get('http://mydomoticz:8080/json.htm?type=command&param=getuservariable&idx=3', text='{{"status":"OK", "result":{data}}}'.format(data=json.dumps([var_string])))
        var = domo.get_user_variable(idx=3)
        self.assertTrue(isinstance(var, str))
        self.assertEqual(var, 'newvalue')

    def test_create_or_update_user_variable_returns_updates_value(self, m):
        domo = domoticz.Domoticz('mydomoticz')
        m.get('http://mydomoticz:8080/json.htm?type=command&param=getuservariables', text='{{"status":"OK", "result":{data}}}'.format(data=json.dumps(self.all_vars)))
        m.get('http://mydomoticz:8080/json.htm?type=command&param=saveuservariable&vname=var_str&vtype=2&vvalue=newvalue', text='{"status":"OK"}')
        m.get('http://mydomoticz:8080/json.htm?type=command&param=updateuservariable&vname=var_str&vtype=2&vvalue=newvalue', text='{"status":"OK"}')
        result = domo.create_or_update_user_variable('var_str','newvalue')
        var_string = self.var_str.copy()
        var_string['Value'] = 'newvalue'
        m.get('http://mydomoticz:8080/json.htm?type=command&param=getuservariable&idx=3', text='{{"status":"OK", "result":{data}}}'.format(data=json.dumps([var_string])))
        var = domo.get_user_variable(idx=3)
        self.assertTrue(isinstance(var, str))
        self.assertEqual(var, 'newvalue')

    def test_delete_user_variable_returns_ok(self, m):
        domo = domoticz.Domoticz('mydomoticz')
        m.get('http://mydomoticz:8080/json.htm?type=command&param=getuservariables', text='{{"status":"OK", "result":{data}}}'.format(data=json.dumps(self.all_vars[1:])))
        m.get('http://mydomoticz:8080/json.htm?type=command&param=deleteuservariable&idx=1', text='{"status":"OK"}')
        result = domo.delete_user_variable(idx=1)
        self.assertEqual(result, 'OK')
        allvars = domo.get_all_variables()
        self.assertEqual(len(allvars), 4)