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
            if res :
                report.info("runsql" + " success " + sql)
            else:
                report.info("runsql" + " success " + sql)
        jpype.shutdownJVM()
    pass
