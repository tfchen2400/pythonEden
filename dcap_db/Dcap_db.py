#!/usr/bin/env python3
# coding=utf-8
"""
    这是Dcap_db的封装类
"""
import pymssql
import pyodbc

from dcap_db.Db_info import Db_info

__author__ = '陈腾飞(水言Dade)'

__version__ = 'v1.0.0'


class Dcap_db(object):
    dbinfo = ""

    sqls = ""

    methods = ""

    def __init__(self):
        pass

    def do_sqls(self):
        # self.do_sqls_pyodbc(2000)
        # self.do_sqls_pyodbc(2005)
        # self.do_sqls_pyodbc(2008)
        # self.do_sqls_pyodbc(2012)
        # self.do_sqls_pyodbc(2014)
        self.do_sqls_pymssql()
        pass

    def do_sqls_pymssql(self):
        print("do_sqls_pymssql")
        conn = pymssql.connect(host="192.168.60.99", port="5211", user="sa", password="Ctf12345", database="pubs", charset="utf8")
        cursor = conn.cursor()
        if not cursor:
            raise (NameError, "数据库连接失败")
        cursor.execute("SELECT * FROM pubs.dbo.authors WHERE 'pymssql'='pymssql'")
        for row in cursor.fetchall():
            print(row)
        cursor.close()
        conn.close()
        pass

    def do_sqls_pyodbc(self, type):
        print("do_sqls_pyodbc")
        # c    2000
        if (type == 2000):
            cnxn = pyodbc.connect(DRIVER='{SQL Server}', SERVER='192.168.60.99,5211', DATABASE='pubs', uid='sa', pwd='Ctf12345')
        # c10  2008
        elif (type == 2005):
            cnxn = pyodbc.connect(DRIVER='{SQL Native Client}', SERVER='192.168.60.99,5211', DATABASE='pubs', uid='sa', pwd='Ctf12345')
        # c10  2008
        elif (type == 2008):
            cnxn = pyodbc.connect(DRIVER='{SQL SERVER NATIVE CLIENT 10.0}', SERVER='192.168.60.99,5211', DATABASE='pubs', uid='sa', pwd='Ctf12345')
        # c11  2012
        elif (type == 2012):
            cnxn = pyodbc.connect(DRIVER='{ODBC Driver 11 for SQL Server}', SERVER='192.168.60.99,5211', DATABASE='pubs', uid='sa', pwd='Ctf12345')
        # c13 2014
        elif (type == 2014):
            cnxn = pyodbc.connect(DRIVER='{ODBC Driver 13 for SQL server}', SERVER='192.168.60.99,5211', DATABASE='pubs', uid='sa', pwd='Ctf12345')

        cursor = cnxn.cursor()
        if not cursor:
            raise (NameError, "数据库连接失败")
        cursor.execute("SELECT * FROM pubs.dbo.authors WHERE 'pyodbc'='pyodbc'")
        for row in cursor.fetchall():
            print(row)
        cursor.close()
        cnxn.close()
        pass


if __name__ == '__main__':
    dcap_db = Dcap_db()
    # db info
    db_info = Db_info()
    db_info.type = "msSql"
    db_info.charset = "utf8"
    db_info.database = "pubs"
    db_info.user = "sa"
    db_info.password = "Ctf12345"
    db_info.host = "192.168.60.99"
    db_info.port = "5211"

    dcap_db.dbinfo = db_info

    sqls = []
    sqls.append("SELECT * FROM pubs.dbo.authors")
    sqls.append("INSERT INTO pubs.dbo.authors VALUES ( '100-10-1000', 'tengfei', 'chen', '083 879-9240', 'fengtanload', 'hangzhou', 'ZJ', '31000', 1 )")
    sqls.append("UPDATE pubs.dbo.authors SET city = 'shanghai' WHERE city = 'hangzhou' AND au_id = '100-10-1000';")
    sqls.append("DELETE FROM pubs.dbo.authors WHERE au_id = '100-10-1000'")
    dcap_db.sqls = sqls

    methods = []
    methods.append("pymssql")
    methods.append("odbc2000")
    methods.append("odbc2005")
    methods.append("odbc2008")
    methods.append("odbc2012")
    methods.append("odbc2014")
    dcap_db.methods = methods


    print(sqls)
