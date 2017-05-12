#!/usr/bin/env python3
# coding=utf-8
"""
    这是Dcap_db的封装类
"""
import pymssql
import pyodbc
import logging
import logging.config

from dcap_db.Db_info import Db_info
from dcap_db.Report import Report

__author__ = '陈腾飞(水言Dade)'

__version__ = 'v1.0.0'


class Dcap_db(object):
    dbinfo = ""

    sqls = ""

    methods = ""

    def __init__(self):
        self.logger = logging.getLogger('Dcap_db')
        self.report = Report()
        pass

    def do_sqls(self):
        for m in self.methods:
            self.logger.info("use method " + m + " #####################")
            self.report.info("@@@@ " + "use method start" + m + " @@@@")
            if m == "pymssql":
                self.do_sqls_pymssql()
            elif m == "odbc2000":
                self.do_sqls_pyodbc(2000)
            elif m == "odbc2005":
                self.do_sqls_pyodbc(2005)
            elif m == "odbc2008":
                self.do_sqls_pyodbc(2008)
            elif m == "odbc2012":
                self.do_sqls_pyodbc(2012)
            elif m == "odbc2014":
                self.do_sqls_pyodbc(2014)
            self.report.info("@@@@ " + "use method end" + m + " @@@@")

    def do_sqls_pymssql(self):
        #print("do_sqls_pymssql")
        conn = pymssql.connect(host=self.dbinfo.host, port=self.dbinfo.port, user=self.dbinfo.user, password=self.dbinfo.password, database=self.dbinfo.database,
                               charset=self.dbinfo.charset, autocommit=True)
        cursor = conn.cursor()
        if not cursor:
            raise (NameError, "数据库连接失败")
            self.report.error("数据库连接失败")
        for sql in self.sqls:
            #print("runsql", sql)
            try:
                cursor.execute(sql)
                #print("runsql", "success", sql)
                self.report.info("runsql" + " success " + sql)
            except Exception as e:
                print('Error:', e)
                self.report.error("runsql" + " error " + sql)

        cursor.close()
        conn.close()
        pass

    def do_sqls_pyodbc(self, type):
        #print("do_sqls_pyodbc")
        server = self.dbinfo.host + "," + self.dbinfo.port
        database = self.dbinfo.database
        uid = self.dbinfo.user
        pwd = self.dbinfo.password
        # c    2000
        if (type == 2000):
            cnxn = pyodbc.connect(autocommit=True, DRIVER='{SQL Server}', SERVER=server, DATABASE=database, uid=uid, pwd=pwd)
        # c10  2008
        elif (type == 2005):
            cnxn = pyodbc.connect(autocommit=True, DRIVER='{SQL Native Client}', SERVER=server, DATABASE=database, uid=uid, pwd=pwd)
        # c10  2008
        elif (type == 2008):
            cnxn = pyodbc.connect(autocommit=True, DRIVER='{SQL SERVER NATIVE CLIENT 10.0}', SERVER=server, DATABASE=database, uid=uid, pwd=pwd)
        # c11  2012
        elif (type == 2012):
            cnxn = pyodbc.connect(autocommit=True, DRIVER='{ODBC Driver 11 for SQL Server}', SERVER=server, DATABASE=database, uid=uid, pwd=pwd)
        # c13 2014
        elif (type == 2014):
            cnxn = pyodbc.connect(autocommit=True, DRIVER='{ODBC Driver 13 for SQL server}', SERVER=server, DATABASE=database, uid=uid, pwd=pwd)

        cursor = cnxn.cursor()
        if not cursor:
            raise (NameError, "数据库连接失败")
            self.report.error("数据库连接失败")
        for sql in self.sqls:
            #print("runsql", sql)
            try:
                cursor.execute(sql)
                #print("runsql", "success", sql)
                self.report.info("runsql" + " success " + sql)
            except Exception as e:
                print('Error:', e)
                self.report.error("runsql" + " error " + sql)
        cursor.close()
        cnxn.close()
        pass


if __name__ == '__main__':
    logging.config.fileConfig("../logging.conf")

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
    sqls.append("UPDATE pubs.dbo.authors SET city = 'shanghai' WHERE city = 'hangzhou' AND au_id = '100-10-1000'")
    sqls.append("DELETE FROM pubs.dbo.authors WHERE au_id = '100-10-1000'")
    dcap_db.sqls = sqls

    methods = []
    #methods.append("pymssql")
    methods.append("odbc2000")
    methods.append("odbc2005")
    methods.append("odbc2008")
    methods.append("odbc2012")
    methods.append("odbc2014")
    dcap_db.methods = methods

    print(dcap_db.dbinfo.host + "," + dcap_db.dbinfo.port)
    # dcap_db.do_sqls_pymssql()
    dcap_db.do_sqls()
    print(sqls)
