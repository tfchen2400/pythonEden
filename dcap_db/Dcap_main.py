#!/usr/bin/env python3
# coding=utf-8
"""
    对外的接口类
"""
import time

from dcap_db.Db_info import Db_info
from dcap_db.Dcap_db import Dcap_db
from dcap_db.Report import Report
from solrpy import core

from dcap_solr.Dcap_solr import Dcap_solr

__author__ = '陈腾飞(水言Dade)'

__version__ = 'v1.0.0'

import json


class Dcap_main(object):
    def __init__(self):
        self.report = Report()
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

        report = Report()

        report.level = level

        # 以server为单位
        for db_info in serversObjs:
            for client in clients:
                timeStr = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
                time.sleep(1)
                self.report.info("#### " + "server " + db_info.host + " start ####")
                # 运行sql
                self.report.info("$$$$ " + "run sql mode start $$$$")
                dcap_db = Dcap_db()
                dcap_db.sqls = sqls
                clients_now = []
                clients_now.append(client)
                dcap_db.methods = clients_now
                dcap_db.dbinfo = db_info
                dcap_db.do_sqls()
                self.report.info("$$$$ " + "run sql mode end $$$$")
                self.report.info("$$$$ " + "solr search mode start $$$$")
                dcap_solr = Dcap_solr()

                dcap_solr.time = timeStr
                #dcap_solr.time = "2017-05-11T17:33:19Z"
                dcap_solr.solr_url = "http://" + managerhost + ":8983/solr"
                dcap_solr.mysql_url = managerhost
                dcap_solr.sqls = sqls
                # 休息一段时间等待数据进入solr
                secend = 60 * 3
                self.report.info("**** thread sleep %d s for data into solr start ****" % secend)
                time.sleep(secend)
                self.report.info("**** thread sleep %d s for data into solr end ****" % secend)
                dcap_solr.find_sqls_in_solr()
                self.report.info("$$$$ " + "solr search mode end $$$$")
                self.report.info("#### " + "server " + db_info.host + " end ####")
        self.report.info("---- " + "exec all end ----")


if __name__ == '__main__':
    data = {}
    # db info
    db_info = Db_info()
    db_info.type = "msSql"
    db_info.charset = "utf8"
    db_info.database = "pubs"
    db_info.user = "sa"
    db_info.password = "Ctf12345"
    db_info.host = "192.168.60.99"
    db_info.port = "5211"

    db_info2 = Db_info()
    db_info2.type = "msSql"
    db_info2.charset = "utf8"
    db_info2.database = "pubs"
    db_info2.user = "sa"
    db_info2.password = "Ctf12345"
    db_info2.host = "192.168.60.109"
    db_info2.port = "1433"

    # 生产库
    servers = []
    servers.append(db_info.__dict__)
    #servers.append(db_info2.__dict__)

    clients = []
    #clients.append("pymssql")
    clients.append("odbc2000")
    clients.append("odbc2005")
    clients.append("odbc2008")
    clients.append("odbc2012")
    clients.append("odbc2014")

    sqls = []
    sqls.append("SELECT * FROM pubs.dbo.authors")
    sqls.append("INSERT INTO pubs.dbo.authors VALUES ( '100-10-1000', 'tengfei', 'chen', '083 879-9240', 'fengtanload', 'hangzhou', 'ZJ', '31000', 1 )")
    sqls.append("UPDATE pubs.dbo.authors SET city = 'shanghai' WHERE city = 'hangzhou' AND au_id = '100-10-1000'")
    sqls.append("DELETE FROM pubs.dbo.authors WHERE au_id = '100-10-1000'")

    data["servers"] = servers
    data["clients"] = clients
    data["sqls"] = sqls
    data["level"] = "info"
    data["target"] = "sqlWhite"
    data["condition"] = "condition123"
    data["managerhost"] = "192.168.60.99"
    jsonStr = json.dumps(data)
    # print(jsonStr)

    dcap_main = Dcap_main()
    dcap_main.exec_all(jsonStr)

    # print(data)
