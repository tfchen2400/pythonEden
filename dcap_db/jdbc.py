#!/usr/bin/env python3
# coding=utf-8
import os
import jpype

from dcap_db.Report import Report


def do_sql_java(jdbcType, jdbcStr, uname, pwd, sqls):
    report = Report()
    baseUrl = os.path.abspath('.')
    ext_classpath = ""
    if (jdbcType == "ojdbc14"):
        ext_classpath = os.path.join(baseUrl, "oraclelink", "OracleMain_ojdbc14.jar")
    elif (jdbcType == "classes12"):
        ext_classpath = os.path.join(baseUrl, "oraclelink", "OracleMain_classes12.jar")
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
    if not jpype.isJVMStarted():
        jpype.startJVM(jvmPath, jvmArg)
        system = jpype.java.lang.System
        oracle = jpype.JClass('snippet.OracleMain')
        oracleMain = oracle()
        for sql in sqls:
            res = oracleMain.runSql(jdbcStr, uname, pwd, sql)
            if res:
                report.info("runsql" + " success " + sql)
            else:
                report.info("runsql" + " error " + sql)
        jpype.shutdownJVM()
    pass


if __name__ == '__main__':
    sqls = []
    sqls.append("UPDATE authors SET CONTRACT = 0 WHERE AU_LNAME = 'White'")
    do_sql_java("sqljdbc4", "jdbc:sqlserver://192.168.60.109:1433;databaseName=pubs;", "sa", "Ctf12345", sqls)
