#!/usr/bin/env python3
# coding=utf-8
import os
import platform

import jpype
import json

import simplejson

from dcap_db.Dcap_redis import Dcap_redis
from dcap_db.Report import Report


def do_sql_java(jdbcType, jdbcStr, uname, pwd, sqls, uuid, dbinfo):
    report = Report()
    # baseUrl = os.path.abspath('.')
    baseUrl = findPath("tag")
    baseUrl = os.path.split(baseUrl)[0]
    baseUrl = os.path.join(baseUrl, "dcap_db")
    ext_classpath = ""
    if (jdbcType == "ojdbc14"):
        ext_classpath = os.path.join(baseUrl, "oraclelink", "OracleMain_ojdbc14.jar")
    elif (jdbcType == "ojdbc5"):
        ext_classpath = os.path.join(baseUrl, "oraclelink", "OracleMain_ojdbc5.jar")
    elif (jdbcType == "ojdbc6"):
        ext_classpath = os.path.join(baseUrl, "oraclelink", "OracleMain_ojdbc6.jar")
    elif (jdbcType == "ojdbc7"):
        ext_classpath = os.path.join(baseUrl, "oraclelink", "OracleMain_ojdbc7.jar")
    elif (jdbcType == "ojdbc8"):
        ext_classpath = os.path.join(baseUrl, "oraclelink", "OracleMain_ojdbc8.jar")
    elif (jdbcType == "sqljdbc4"):
        ext_classpath = os.path.join(baseUrl, "oraclelink", "SQL_sqljdbc4.jar")
    elif (jdbcType == "jtds13"):
        ext_classpath = os.path.join(baseUrl, "oraclelink", "SQL_jtds13.jar")
    jvmPath = jpype.getDefaultJVMPath()
    # ext_classpath = "E:\Lib\OracleMain_ojdbc14.jar"
    # ext_classpath = "E:\Lib\OraceJdbc.jar"
    jvmArg = '-Djava.class.path=' + ext_classpath
    redis = Dcap_redis().getRedis()
    if not jpype.isJVMStarted():
        jpype.startJVM(jvmPath, jvmArg)
        system = jpype.java.lang.System
        oracle = jpype.JClass('snippet.OracleMain')
        oracleMain = oracle()
        for sql_info in sqls:
            sql_info_json = simplejson.loads(redis.hget(uuid + "sql", sql_info["uuid"]))

            clientsJa = sql_info_json.get("clients")
            if clientsJa == None:
                clientsJa = []

            pymssql_jo = {}
            pymssql_jo["client"] = jdbcType
            pymssql_jo["productDb"] = dbinfo.name
            sql = sql_info["sql"]
            par_str = json.dumps(sql_info["par"])
            res = oracleMain.runSql(jdbcStr, uname, pwd, sql, par_str, jdbcType)
            if res:
                report.info("runsql" + " success " + sql, uuid)
                pymssql_jo["runsql"] = "success"
            else:
                report.info("runsql" + " error " + sql, uuid)
                pymssql_jo["runsql"] = "error"
            clientsJa.append(pymssql_jo)
            sql_info_json["clients"] = clientsJa
            redis.hset(uuid + "sql", sql_info["uuid"], simplejson.dumps(sql_info_json))
        jpype.shutdownJVM()
    pass


def getSeparator():
    if 'Windows' in platform.system():
        separator = '\\'
    else:
        separator = '/'
    return separator


def findPath(file):
    o_path = os.getcwd()
    separator = getSeparator()
    str = o_path
    str = str.split(separator)
    while len(str) > 0:
        spath = separator.join(str) + separator + file
        leng = len(str)
        if os.path.exists(spath):
            return spath
        str.remove(str[leng - 1])


if __name__ == '__main__':
    sqls = []
    sql_info = {}
    sql_info["sql"] = "SELECT * FROM pubs.dbo.authors"
    sql_info["par"] = {}
    sqls.append(sql_info)

    sql_info = {}
    sql_info["sql"] = "INSERT INTO pubs.dbo.authors VALUES ( '100-10-1000', 'tengfei', 'chen', '083 879-9240', 'fengtanload', 'hangzhou', 'ZJ', '31000', 1 )"
    sql_info["par"] = {}
    sqls.append(sql_info)

    sql_info = {}
    sql_info["sql"] = "UPDATE pubs.dbo.authors SET city = 'shanghai' WHERE city = 'hangzhou' AND au_id = '100-10-1000'"
    sql_info["par"] = {}
    sqls.append(sql_info)

    sql_info = {}
    sql_info["sql"] = "DELETE FROM pubs.dbo.authors WHERE au_id = '100-10-1000'"
    sql_info["par"] = {}
    sqls.append(sql_info)

    sqls.append("UPDATE authors SET CONTRACT = 0 WHERE AU_LNAME = 'White'")
    # do_sql_java("sqljdbc4", "jdbc:sqlserver://192.168.60.109:1433;databaseName=pubs;", "sa", "Ctf12345", sqls)


    # sqls = []
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
    #
    # sql_info = {}
    # sql_info["sql"] = "DELETE dept WHERE DEPTNO = 11"
    # par = {}
    # sql_info["par"] = par
    # sqls.append(sql_info)
    #
    do_sql_java("ojdbc6", "jdbc:oracle:thin:@192.168.60.95:1521:wangzw", "scott", "scott", sqls, "")

    print(findPath('tag'))
