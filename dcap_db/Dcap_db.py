#!/usr/bin/env python3
# coding=utf-8
"""
    这是Dcap_db的封装类
"""
import logging
import logging.config
import pymssql
import pyodbc
from multiprocessing import Process

import cx_Oracle
import simplejson
from flask import json

from dcap_db import jdbc
from dcap_db.Db_info import Db_info
from dcap_db.Dcap_redis import Dcap_redis
from dcap_db.Report import Report
from dcap_db.req_restful import ReqRestful

__author__ = '陈腾飞(水言Dade)'

__version__ = 'v1.0.0'


class Dcap_db(object):
    dbinfo = ""

    sqls = ""

    methods = ""

    def __init__(self):
        self.logger = logging.getLogger('Dcap_db')
        self.report = Report()
        self.redis = Dcap_redis().getRedis()
        self.uuid = ""
        pass

    def do_sqls(self):
        if (self.dbinfo.type.upper() == "MSSQL"):
            for m in self.methods:
                self.logger.info("use method " + m + " #####################", self.uuid)
                self.report.info("@@@@ " + "use method start" + m + " @@@@", self.uuid)
                if m == "pymssql":
                    self.do_sqls_pymssql()
                elif m == "SQL server 2005":
                    self.do_sqls_pyodbc("SQL server 2005")
                elif m == "SQL server 2008":
                    self.do_sqls_pyodbc("SQL server 2008")
                elif m == "SQL server 2012":
                    self.do_sqls_pyodbc("SQL server 2012")
                elif m == "SQL server 2014":
                    self.do_sqls_pyodbc("SQL server 2014")
                elif m == "sqlcmd SQL server 2005":
                    self.do_sqls_pyodbc("sqlcmd SQL server 2005")
                elif m == "sqlcmd SQL server 2008":
                    self.do_sqls_pyodbc("sqlcmd SQL server 2008")
                elif m == "sqlcmd SQL server 2012":
                    self.do_sqls_pyodbc("sqlcmd SQL server 2012")
                elif m == "sqlcmd SQL server 2014":
                    self.do_sqls_pyodbc("sqlcmd SQL server 2014")
                elif m == "sqljdbc4":
                    jdbcStr = "jdbc:sqlserver://" + self.dbinfo.host + ":" + self.dbinfo.port + ";databaseName=" + self.dbinfo.database + ";"
                    user = self.dbinfo.user
                    pwd = self.dbinfo.password
                    p = Process(target=jdbc.do_sql_java, args=(m, jdbcStr, user, pwd, self.sqls, self.uuid, self.dbinfo,))
                    # print('Child process will start.')
                    p.start()
                    p.join()
                    # self.do_sql_java("ojdbc14")
                elif m == "jtds13":
                    jdbcStr = "jdbc:jtds:sqlserver://" + self.dbinfo.host + ":" + self.dbinfo.port + "/" + self.dbinfo.database
                    user = self.dbinfo.user
                    pwd = self.dbinfo.password
                    p = Process(target=jdbc.do_sql_java, args=(m, jdbcStr, user, pwd, self.sqls, self.uuid, self.dbinfo,))
                    # print('Child process will start.')
                    p.start()
                    p.join()
                    # self.do_sql_java("ojdbc14")
                self.report.info("@@@@ " + "use method end" + m + " @@@@", self.uuid)
        elif (self.dbinfo.type.upper() == "ORACLE"):
            for m in self.methods:
                self.logger.info("use method " + m + " #####################" + self.uuid)
                self.report.info("@@@@ " + "use method start" + m + " @@@@", self.uuid)
                jdbcStr = "jdbc:oracle:thin:@" + self.dbinfo.host + ":" + self.dbinfo.port + ":" + self.dbinfo.database
                user = self.dbinfo.user
                pwd = self.dbinfo.password
                if m == "cx_oracle":
                    self.do_sqls_cx_oracle()
                elif m == "ojdbc5":
                    p = Process(target=jdbc.do_sql_java, args=(m, jdbcStr, user, pwd, self.sqls, self.uuid, self.dbinfo,))
                    # print('Child process will start.')
                    p.start()
                    p.join()
                    # self.do_sql_java("ojdbc14")
                elif m == "ojdbc6":
                    p = Process(target=jdbc.do_sql_java, args=(m, jdbcStr, user, pwd, self.sqls, self.uuid, self.dbinfo,))
                    # print('Child process will start.')
                    p.start()
                    p.join()
                    # self.do_sql_java("ojdbc14")
                elif m == "ojdbc7":
                    p = Process(target=jdbc.do_sql_java, args=(m, jdbcStr, user, pwd, self.sqls, self.uuid, self.dbinfo,))
                    # print('Child process will start.')
                    p.start()
                    p.join()
                    # self.do_sql_java("ojdbc14")
                elif m == "ojdbc8":
                    p = Process(target=jdbc.do_sql_java, args=(m, jdbcStr, user, pwd, self.sqls, self.uuid, self.dbinfo,))
                    # print('Child process will start.')
                    p.start()
                    p.join()
                    # self.do_sql_java("ojdbc14")
                elif m == "classes12":
                    p = Process(target=jdbc.do_sql_java, args=(m, jdbcStr, user, pwd, self.sqls, self.uuid, self.dbinfo,))
                    # print('Child process will start.')
                    p.start()
                    p.join()
                    # self.do_sql_java("ojdbc14")
                elif m == "ojdbc14":
                    p = Process(target=jdbc.do_sql_java, args=(m, jdbcStr, user, pwd, self.sqls, self.uuid, self.dbinfo,))
                    # print('Child process will start.')
                    p.start()
                    p.join()
                    # self.do_sql_java("ojdbc14")
                elif m == "classes12":
                    p = Process(target=jdbc.do_sql_java, args=(m, jdbcStr, user, pwd, self.sqls, self.uuid, self.dbinfo,))
                    p.start()
                    p.join()
                elif m == "linux_X86_64_OCI_12":
                    self.do_sqls_linux_X86_64_OCI(12)
                elif m == "linux_X86_64_OCI_11":
                    self.do_sqls_linux_X86_64_OCI(11)
                elif m == "linux_X86_64_OCI_10":
                    self.do_sqls_linux_X86_64_OCI(10)

                self.report.info("@@@@ " + "use method end" + m + " @@@@", self.uuid)

    def do_sqls_linux_X86_64_OCI(self, version):
        urlport = ""
        if version == 10:
            urlport = 4999
        elif version == 11:
            urlport = 5000
        elif version == 12:
            urlport = 5001
        else:
            return

        for sql_info in self.sqls:
            sql_info_json = simplejson.loads(self.redis.hget(self.uuid + "sql", sql_info["uuid"]))

            clientsJa = sql_info_json.get("clients")
            if clientsJa == None:
                clientsJa = []

            pymssql_jo = {}
            pymssql_jo["client"] = "linux_X86_64_OCI_" + str(version)
            pymssql_jo["productDb"] = self.dbinfo.name

            req = ReqRestful()
            info = {}
            info["host"] = self.dbinfo.host
            info["port"] = self.dbinfo.port
            info["database"] = self.dbinfo.database
            info["user"] = self.dbinfo.user
            info["password"] = self.dbinfo.password
            # sql_info = {}
            # sql_info["sql"] = "select * from dept where dname = :dname"
            # par = {}
            # par["dname"] = "ACCOUNTING"
            # sql_info["par"] = par
            info["sql_info"] = sql_info

            s = json.dumps(info)
            test_data = {"info": s}
            req.data = test_data
            req.url = "http://192.168.210.120:" + str(urlport) + "/todo/api/v1.0/linkOracleOci"
            result = req.do_request()
            ret_dict = simplejson.loads(result)
            pymssql_jo["runsql"] = ret_dict["result"]
            pymssql_jo["errorInfo"] = ret_dict["message"]
            clientsJa.append(pymssql_jo)
            sql_info_json["clients"] = clientsJa
            self.redis.hset(self.uuid + "sql", sql_info["uuid"], simplejson.dumps(sql_info_json))

    def do_sqls_pymssql(self):
        # print("do_sqls_pymssql")
        conn = pymssql.connect(host=self.dbinfo.host, port=self.dbinfo.port, user=self.dbinfo.user, password=self.dbinfo.password, database=self.dbinfo.database,
                               charset=self.dbinfo.charset, autocommit=True)
        cursor = conn.cursor()
        if not cursor:
            raise (NameError, "数据库连接失败")
            self.report.error("数据库连接失败", self.uuid)
        for sql_info in self.sqls:
            # 获取sqlinfo的json
            # 变成dict
            sql_info_json = simplejson.loads(self.redis.hget(self.uuid + "sql", sql_info["uuid"]))

            clientsJa = sql_info_json.get("clients")
            if clientsJa == None:
                clientsJa = []

            pymssql_jo = {}
            pymssql_jo["client"] = "pymssql"
            pymssql_jo["productDb"] = self.dbinfo.name
            sql = sql_info["sql"]
            # print("runsql", sql)
            try:
                cursor.execute(sql)
                # print("runsql", "success", sql)
                pymssql_jo["runsql"] = "success"
                self.report.info("runsql" + " success " + sql, self.uuid)
            except Exception as e:
                print('Error:', e)
                self.report.error("runsql" + " error " + sql, self.uuid)
                pymssql_jo["runsql"] = "error"
                pymssql_jo["errorInfo"] = str(e)
            clientsJa.append(pymssql_jo)
            sql_info_json["clients"] = clientsJa
            self.redis.hset(self.uuid + "sql", sql_info["uuid"], simplejson.dumps(sql_info_json))
        cursor.close()
        conn.close()
        pass

    def do_sqls_pyodbc(self, type):
        # print("do_sqls_pyodbc")
        server = self.dbinfo.host + "," + self.dbinfo.port
        database = self.dbinfo.database
        uid = self.dbinfo.user
        pwd = self.dbinfo.password
        # c    2000
        # if (type == 2000):
        #     cnxn = pyodbc.connect(autocommit=True, DRIVER='{SQL Server}', SERVER=server, DATABASE=database, uid=uid, pwd=pwd, APP="SQL Server 2000")
        # c10  2005
        if (type == "SQL server 2005"):
            cnxn = pyodbc.connect(autocommit=True, DRIVER='{SQL Native Client}', SERVER=server, DATABASE=database, uid=uid, pwd=pwd, APP="SQL server 2005")
        # c10  2008
        elif (type == "SQL server 2008"):
            cnxn = pyodbc.connect(autocommit=True, DRIVER='{SQL SERVER NATIVE CLIENT 10.0}', SERVER=server, DATABASE=database, uid=uid, pwd=pwd,
                                  APP="SQL server 2008")
        # c11  2012
        elif (type == "SQL server 2012"):
            cnxn = pyodbc.connect(autocommit=True, DRIVER='{ODBC Driver 11 for SQL Server}', SERVER=server, DATABASE=database, uid=uid, pwd=pwd,
                                  APP="SQL server 2012")
        # c13 2014
        elif (type == "SQL server 2014"):
            cnxn = pyodbc.connect(autocommit=True, DRIVER='{ODBC Driver 13 for SQL server}', SERVER=server, DATABASE=database, uid=uid, pwd=pwd,
                                  APP="SQL server 2014")
        elif (type == "sqlcmd SQL server 2005"):
            cnxn = pyodbc.connect(autocommit=True, DRIVER='{SQL Native Client}', SERVER=server, DATABASE=database, uid=uid, pwd=pwd, APP="sqlcmd SQL server 2005")
        # c10  2008
        elif (type == "sqlcmd SQL server 2008"):
            cnxn = pyodbc.connect(autocommit=True, DRIVER='{SQL SERVER NATIVE CLIENT 10.0}', SERVER=server, DATABASE=database, uid=uid, pwd=pwd,
                                  APP="sqlcmd SQL server 2008")
        # c11  2012
        elif (type == "sqlcmd SQL server 2012"):
            cnxn = pyodbc.connect(autocommit=True, DRIVER='{ODBC Driver 11 for SQL Server}', SERVER=server, DATABASE=database, uid=uid, pwd=pwd,
                                  APP="sqlcmd SQL server 2012")
        # c13 2014
        elif (type == "sqlcmd SQL server 2014"):
            cnxn = pyodbc.connect(autocommit=True, DRIVER='{ODBC Driver 13 for SQL server}', SERVER=server, DATABASE=database, uid=uid, pwd=pwd,
                                  APP="sqlcmd SQL server 2014")

        cursor = cnxn.cursor()
        if not cursor:
            raise (NameError, "数据库连接失败")
            self.report.error("数据库连接失败", self.uuid)
        for sql_info in self.sqls:
            # print("runsql", sql)
            sql_info_json = simplejson.loads(self.redis.hget(self.uuid + "sql", sql_info["uuid"]))
            clientsJa = sql_info_json.get("clients")
            if clientsJa == None:
                clientsJa = []

            pymssql_jo = {}
            pymssql_jo["client"] = type
            pymssql_jo["productDb"] = self.dbinfo.name
            sql = sql_info["sql"]
            try:
                cursor.execute(sql)
                # print("runsql", "success", sql)
                self.report.info("runsql" + " success " + sql, self.uuid)
                pymssql_jo["runsql"] = "success"
            except Exception as e:
                print('Error:', e)
                self.report.error("runsql" + " error " + sql, self.uuid)
                pymssql_jo["runsql"] = "error"
                pymssql_jo["errorInfo"] = str(e)
            clientsJa.append(pymssql_jo)
            sql_info_json["clients"] = clientsJa
            self.redis.hset(self.uuid + "sql", sql_info["uuid"], simplejson.dumps(sql_info_json))
        cursor.close()
        cnxn.close()
        pass

    def do_sqls_cx_oracle(self):
        dsn = cx_Oracle.makedsn(self.dbinfo.host, self.dbinfo.port, self.dbinfo.database)
        conn = ""
        if "AS SYSDBA" in self.dbinfo.user.upper():
            user = self.dbinfo.user.upper().split()[0]
            conn = cx_Oracle.connect(user, self.dbinfo.password, dsn, mode=cx_Oracle.SYSDBA)
        else:
            conn = cx_Oracle.connect(self.dbinfo.user, self.dbinfo.password, dsn)
        cursor = cx_Oracle.Cursor(conn)
        if not cursor:
            raise (NameError, "数据库连接失败")
            self.report.error("数据库连接失败", self.uuid)
        sql = 'select * from common_user'
        for sql_info in self.sqls:
            sql_info_json = simplejson.loads(self.redis.hget(self.uuid + "sql", sql_info["uuid"]))
            clientsJa = sql_info_json.get("clients")
            if clientsJa == None:
                clientsJa = []

            pymssql_jo = {}
            pymssql_jo["client"] = "cx_oracle"

            sql = sql_info["sql"]
            par = sql_info["par"]
            try:
                cursor.execute(sql, par)
                conn.commit()
                self.report.info("runsql" + " success " + sql + " ----------par: " + str(par), self.uuid)
                pymssql_jo["runsql"] = "success"
            except Exception as e:
                print('Error:', e)
                self.report.error("runsql" + " error " + sql + " ----------par: " + str(par), self.uuid)
                pymssql_jo["runsql"] = "error"
                pymssql_jo["errorInfo"] = str(e)
            clientsJa.append(pymssql_jo)
            sql_info_json["clients"] = clientsJa
            self.redis.hset(self.uuid + "sql", sql_info["uuid"], simplejson.dumps(dict(sql_info_json)))
        cursor.close()
        conn.close()
        pass


if __name__ == '__main__':
    logging.config.fileConfig("../logging.conf")

    # dcap_db = Dcap_db()
    # # db info
    # db_info = Db_info()
    # db_info.type = "msSql"
    # db_info.charset = "utf8"
    # db_info.database = "pubs"
    # db_info.user = "sa"
    # db_info.password = "Ctf12345"
    # db_info.host = "192.168.60.99"
    # db_info.port = "5211"
    #
    # dcap_db.dbinfo = db_info
    #
    # sqls = []
    # sqls.append("SELECT * FROM pubs.dbo.authors")
    # sqls.append("INSERT INTO pubs.dbo.authors VALUES ( '100-10-1000', 'tengfei', 'chen', '083 879-9240', 'fengtanload', 'hangzhou', 'ZJ', '31000', 1 )")
    # sqls.append("UPDATE pubs.dbo.authors SET city = 'shanghai' WHERE city = 'hangzhou' AND au_id = '100-10-1000'")
    # sqls.append("DELETE FROM pubs.dbo.authors WHERE au_id = '100-10-1000'")
    # dcap_db.sqls = sqls
    #
    # methods = []
    # # methods.append("pymssql")
    # # methods.append("odbc2000")
    # # methods.append("odbc2005")
    # # methods.append("odbc2008")
    # # methods.append("odbc2012")
    # # methods.append("odbc2014")
    # # methods.append("sqljdbc4")
    # methods.append("jtds13")
    # dcap_db.methods = methods
    #
    # print(dcap_db.dbinfo.host + "," + dcap_db.dbinfo.port)
    # # dcap_db.do_sqls_pymssql()
    # dcap_db.do_sqls()
    # print(sqls)


    dcap_db = Dcap_db()
    # db info
    db_info = Db_info()
    # db_info.type = "oracle"
    # db_info.database = "wangzw"
    # db_info.user = "scott"
    # db_info.password = "scott"
    # db_info.host = "192.168.60.95"
    # db_info.port = "1521"

    db_info.type = "oracle"
    db_info.database = "orcl"
    db_info.user = "scott"
    db_info.password = "scott"
    db_info.host = "192.168.200.179"
    db_info.port = "1521"

    dcap_db.dbinfo = db_info

    sqls = []
    # sql_info = {}
    # sql_info["sql"] = "select * from dept"
    # sql_info["par"] = {}
    # sqls.append(sql_info)
    #
    # sql_info = {}
    # sql_info["sql"] = "select * from dept where dname = :dname"
    # par = {}
    # par["dname"] = "ACCOUNTING"
    # sql_info["par"] = par
    #
    # sqls.append(sql_info)

    # sqls.append("select * from dept where dname = 'ACCOUNTING'")
    # sqls.append("INSERT INTO dept VALUES (11, 'chentf', 'hz')")
    # sqls.append("UPDATE dept SET dname = 'CHENTF_UPDATE' WHERE DEPTNO = 11")
    # sqls.append("DELETE dept WHERE DEPTNO = 11")


    # sql_info = {}
    # sql_info["sql"] = "INSERT INTO dept VALUES (:id, :dname, :city)"
    # par = {}
    # par["id"] = 11
    # par["dname"] = "chentf"
    # par["city"] = "hz"
    # sql_info["par"] = par
    # sqls.append(sql_info)
    #
    # sql_info = {}
    # sql_info["sql"] = "UPDATE dept SET dname = :dname WHERE DEPTNO = :id"
    # par = {}
    # par["id"] = 11
    # par["dname"] = "CHENTF_UPDATE"
    # sql_info["par"] = par
    # sqls.append(sql_info)

    sql_info = {}
    sql_info["sql"] = "DELETE dept WHERE DEPTNO = 11"
    par = {}
    sql_info["par"] = par
    sql_info["uuid"] = "123"
    sqls.append(sql_info)

    dcap_db.sqls = sqls
    dcap_db.uuid = "chentf"

    methods = []
    methods.append("cx_oracle")
    # methods.append("ojdbc14")
    # methods.append("classes12")
    # methods.append("ojdbc5")
    # methods.append("ojdbc6")
    # methods.append("ojdbc7")
    # methods.append("ojdbc8")

    dcap_db.methods = methods

    dcap_db.do_sqls()
