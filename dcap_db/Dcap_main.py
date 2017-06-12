#!/usr/bin/env python3
# coding=utf-8
"""
    对外的接口类
"""
import time
import uuid

import simplejson

from dcap_db.Db_info import Db_info
from dcap_db.Dcap_db import Dcap_db
from dcap_db.Dcap_redis import Dcap_redis
from dcap_db.Report import Report
from solrpy import core

from dcap_solr.Dcap_solr import Dcap_solr

__author__ = '陈腾飞(水言Dade)'

__version__ = 'v1.0.0'

import json


class Dcap_main(object):
    def __init__(self):
        self.report = Report()
        self.redis = Dcap_redis().getRedis()
        pass

    def exec_all(self, data):
        self.report.info("---- " + "exec all start ----")
        dataDict = json.loads(data)
        serversJa = dataDict["servers"]
        # servers
        serversObjs = []
        for jo in serversJa:
            db_info = Db_info()
            db_info.__dict__ = jo
            serversObjs.append(db_info)
        # client
        clients = dataDict["clients"]

        # sqls
        sqls = dataDict["sqls"]

        # level
        level = dataDict["level"]

        # managerip
        managerhost = dataDict["managerhost"]

        self.uuid = dataDict.get("uuid")
        # 如果没有uuid 就生成一个uuid
        if (self.uuid == None):
            self.uuid = time.strftime("%Y%m%d%H%M%S", time.localtime())
            # self.uuid = str(uuid.uuid1())

        # 生成一个返回的hashmap
        self.redis.hset(self.uuid, 'uuid', self.uuid)
        self.redis.hset(self.uuid, 'reqInfo', str(data))

        # 每个sql生成一个uuid
        sqls = map(self.generate_sql_uuid, sqls)
        sqls = list(sqls)
        # 每一句
        self.report.level = level

        # 以server为单位
        for db_info in serversObjs:
            for client in clients:
                timeStr = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
                time.sleep(1)
                self.report.info("#### " + "server " + db_info.host + " start ####", self.uuid)
                # 运行sql
                self.report.info("$$$$ " + "run sql mode start $$$$", self.uuid)
                dcap_db = Dcap_db()
                dcap_db.uuid = self.uuid

                dcap_db.sqls = sqls
                clients_now = []
                clients_now.append(client)
                dcap_db.methods = clients_now
                dcap_db.dbinfo = db_info
                dcap_db.do_sqls()
                self.report.info("$$$$ " + "run sql mode end $$$$", self.uuid)


                # self.report.info("$$$$ " + "solr search mode start $$$$", self.uuid)
                # dcap_solr = Dcap_solr()
                # dcap_solr.uuid = self.uuid

                # dcap_solr.time = timeStr
                # # dcap_solr.time = "2017-05-11T17:33:19Z"
                # dcap_solr.solr_url = "http://" + managerhost + ":8983/solr"
                # dcap_solr.mysql_url = managerhost
                # dcap_solr.sqls = sqls
                # #休息一段时间等待数据进入solr
                # secend = 1 * 3
                # self.report.info("**** thread sleep %d s for data into solr start ****" % secend, self.uuid)
                # time.sleep(secend)
                # self.report.info("**** thread sleep %d s for data into solr end ****" % secend, self.uuid)
                # dcap_solr.find_sqls_in_solr()
                # self.report.info("$$$$ " + "solr search mode end $$$$", self.uuid)
                # self.report.info("#### " + "server " + db_info.host + " end ####", self.uuid)
        self.report.info("---- " + "exec all end ----")

        # 获取uuid
        result_true = self.redis.hgetall(self.uuid)
        result = self.redis.hgetall(self.uuid + "sql")
        resultTemp = []
        for k, v in result.items():
            tv = simplejson.loads(v)
            # print(simplejson.dumps(tv))
            resultTemp.append(tv)
            result_true["result"] = resultTemp
        return simplejson.dumps(result_true)

    def generate_sql_uuid(self, x):
        x["uuid"] = str(uuid.uuid1())
        self.redis.hset(self.uuid + "sql", x["uuid"], json.dumps(x))
        return x


if __name__ == '__main__':
    data = {}
    db_info = Db_info()
    db_info.type = "oracle"
    db_info.database = "ORCLCDB"
    db_info.user = "sys as sysdba"
    db_info.password = "hzmc321#"
    db_info.host = "192.168.60.95"
    db_info.port = "1521"
    db_info.name = "chentfdb"
    # db_info2 = Db_info()
    # db_info2.type = "msSql"
    # db_info2.charset = "utf8"
    # db_info2.database = "pubs"
    # db_info2.user = "sa"
    # db_info2.password = "Ctf12345"
    # db_info2.host = "192.168.60.109"
    # db_info2.port = "1433"
    # db_info2.name = "chentfdb"

    # 生产库
    servers = []
    servers.append(db_info.__dict__)
    # servers.append(db_info2.__dict__)

    clients = []
    # clients.append("pymssql")
    # clients.append("SQL server 2005")
    # clients.append("SQL server 2008")
    # clients.append("SQL server 2012")
    # clients.append("SQL server 2014")
    # clients.append("sqlcmd SQL server 2005")
    # clients.append("sqlcmd SQL server 2008")
    # clients.append("sqlcmd SQL server 2012")
    # clients.append("sqlcmd SQL server 2014")
    # clients.append("sqljdbc4")
    # clients.append("jtds13")

    # clients.append("cx_oracle")
    clients.append("linux_X86_64_OCI_12")
    clients.append("linux_X86_64_OCI_11")
    clients.append("linux_X86_64_OCI_10")

    sqls = []
    # sql_info = {}
    # sql_info["sql"] = "SELECT * FROM pubs.dbo.authors"
    # sql_info["par"] = {}
    # sqls.append(sql_info)
    #
    # sql_info = {}
    # sql_info["sql"] = "INSERT INTO pubs.dbo.authors VALUES ( '100-10-1000', 'tengfei', 'chen', '083 879-9240', 'fengtanload', 'hangzhou', 'ZJ', '31000', 1 )"
    # sql_info["par"] = {}
    # sqls.append(sql_info)
    #
    # sql_info = {}
    # sql_info["sql"] = "UPDATE pubs.dbo.authors SET city = 'shanghai' WHERE city = 'hangzhou' AND au_id = '100-10-1000'"
    # sql_info["par"] = {}
    # sqls.append(sql_info)
    #
    # sql_info = {}
    # sql_info["sql"] = "DELETE FROM pubs.dbo.authors WHERE au_id = '100-10-1000'"
    # sql_info["par"] = {}
    # sqls.append(sql_info)
    #
    # sql_info = {}
    # sql_info["sql"] = "create login dba with password='dba',default_database=sales"
    # sql_info["par"] = {}
    # sqls.append(sql_info)

    sql_info = {}
    sql_info["sql"] = "DELETE dept WHERE DEPTNO = 11"
    par = {}
    sql_info["par"] = par
    sql_info["uuid"] = "123"
    sqls.append(sql_info)

    sql_info = {}
    sql_info["sql"] = "select 1 from dual"
    par = {}
    sql_info["par"] = par
    sql_info["uuid"] = "123"
    sqls.append(sql_info)

    data["servers"] = servers
    data["clients"] = clients
    data["sqls"] = sqls
    data["level"] = "info"
    data["target"] = "sqlWhite"
    data["condition"] = "condition123"
    data["managerhost"] = "192.168.60.99"

    jsonStr = json.dumps(data)
    print(jsonStr)
    f = open('./jsonStr.txt', 'w')
    json.dump(jsonStr, f)
    f.close()

    f = open('./jsonStr.txt', 'r')
    jsonStrFile = json.load(f)
    print(jsonStrFile)

    dcap_main = Dcap_main()
    res = dcap_main.exec_all(jsonStrFile)
    print(res)
    # print(data)
