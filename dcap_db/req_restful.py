#!/usr/bin/env python3
# coding=utf-8
"""
    restful
"""
import urllib
from urllib import parse

from flask import json


class ReqRestful(object):
    def __init__(self):
        pass

    def do_request(self):
        test_data_urlencode = parse.urlencode(self.data)
        req = urllib.request.urlopen(self.url + "?" + test_data_urlencode)
        str = req.read().decode('utf-8')
       #print(str)
        return str


if __name__ == '__main__':
    req = ReqRestful()
    info = {}
    info["host"] = "192.168.60.95"
    info["port"] = "1521"
    info["database"] = "ORCLCDB"
    info["user"] = "SYS AS SYSDBA"
    info["password"] = "hzmc321#"
    sql_info = {}
    sql_info["sql"] = "select * from dept where dname = :dname"
    par = {}
    par["dname"] = "ACCOUNTING"
    sql_info["par"] = par
    info["sql_info"] = sql_info

    str = json.dumps(info)

    test_data = {"info": str}
    req.data = test_data
    req.url = 'http://192.168.210.120:5000/todo/api/v1.0/linkOracleOci'
    req.do_request()
