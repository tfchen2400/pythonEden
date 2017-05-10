#!/usr/bin/env python3
# coding=utf-8
"""
    这是dcap_solr的封装类
"""
import pymysql
import time
__author__ = '陈腾飞(水言Dade)'

__version__ = 'v1.0.0'


class Dcap_solr(object):
    # solr地址
    solr_url = ''

    # mysql地址
    mysql_url = ''

    # sqls
    sqls = ''

    def __init__(self):
        pass

    def get_solr_url(self):
        return self.solr_url

    def set_solr_url(self, solr_url):
        self.solr_url = solr_url

    def get_mysql_url(self):
        return self.mysql_url

    def set_mysql_url(self, mysql_url):
        self.mysql_url = mysql_url

    def get_sqls(self):
        return self.sqls

    def set_sqls(self, sqls):
        self.sqls = sqls

    # 查找 登录和访问的core名
    def find_solr_cores(self):
        conn = pymysql.connect(host='192.168.60.99', port=3306, user='asset', passwd='hzmc321#', db='capaa')
        cursor = conn.cursor()
        cursor.execute('SET NAMES UTF8')
        cursor.execute("SELECT * FROM mc$asset_type")
        for row in cursor.fetchall():
            print(row)
        cursor.close()
        conn.close()
        print("find_solr_cores")
        pass

    def find_sqls_in_solr(self):
        print("find_sqls_in_solr")
        pass


if __name__ == '__main__':
    dcap_solr = Dcap_solr()
    print(dcap_solr.get_solr_url())

    dcap_solr.set_solr_url("http://192.168.60.99:8983/solr")
    print(dcap_solr.get_solr_url())

    dcap_solr.set_mysql_url("192.168.60.99")
    print(dcap_solr.get_mysql_url())

    dcap_solr.find_solr_cores()
