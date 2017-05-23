#!/usr/bin/env python3
# coding=utf-8
"""
    这是dcap_solr的封装类
"""
import pymysql
import json
from solrpy import core

from dcap_db.Report import Report

__author__ = '陈腾飞(水言Dade)'

__version__ = 'v1.0.0'


class Dcap_solr(object):
    # solr地址
    solr_url = ''

    # mysql地址
    mysql_url = ''

    # sqls
    sqls = ''

    # time 2017-04-26T22:05:30Z
    time = ''

    # login core
    logon_core = []

    # access core
    access_core = []

    def __init__(self):
        self.report = Report()
        pass

    # 查找 登录和访问的core名
    def find_solr_cores(self):
        conn = pymysql.connect(host='192.168.60.99', port=3306, user='asset', passwd='hzmc321#', db='capaa')
        cursor = conn.cursor()
        cursor.execute('SET NAMES UTF8')
        cursor.execute("SELECT * FROM mc$core_info")
        for row in cursor.fetchall():
            # 访问
            if (row[2] == '0'):
                self.logon_core.append(row[1])
            elif (row[2] == '1'):
                self.access_core.append(row[1])
        cursor.close()
        conn.close()
        # print("find_solr_cores")
        pass

    def complete_sql(self, access_result):
        sqlids = []
        for result in access_result:
            # 获取hashids
            sqlids.append(result['sqlid'])

        sqlids = list(set(sqlids))

        # 去sql库中查找
        solr_sql_url = self.solr_url + '/6'

        s = core.SolrConnection(solr_sql_url)
        q = ""
        for sqlid in sqlids:
            if len(q) == 0:
                q = q + "id:" + sqlid
            else:
                q = q + " OR id:" + sqlid
        response = s.query(q=q, rows=50)

        sql_result = response.results

        # 翻译合起来
        for access in access_result:
            for sql in sql_result:
                if sql['id'] == access['sqlid']:
                    access['sql_solr'] = sql['sqltext']
                    # 替换组装真正的sql
                    sql_real = sql['sqltext']
                    combined_info = access['combined_info'].split('|')
                    myvar_str = combined_info[21]
                    # 可变参数
                    myvars = myvar_str.split(',')
                    # 组装回去
                    for myvar in myvars:
                        sql_real = sql_real.replace('?', myvar.strip(), 1)
                    access['sql_real'] = sql_real
        return access_result

    def find_sqls_in_solr(self):
        self.find_solr_cores()
        # 向访问库搜索 JOIN SQL库搜索
        for sql in self.sqls:
            flag = False
            bingo_str = ""
            sql = sql.upper()
            # 变成sql_solr
            sql_solr = sql
            # 截断
            if sql.startswith("SELECT"):
                # print("select-----------")
                if sql_solr.find("WHERE") != -1:
                    sql_solr = sql_solr[:sql_solr.find("WHERE")]
            elif sql.startswith("INSERT"):
                # print("insert-----------")
                if sql_solr.find("VALUES") != -1:
                    sql_solr = sql_solr[:sql_solr.find("VALUES")]
            elif sql.startswith("UPDATE"):
                if sql_solr.find("SET") != -1:
                    sql_solr = sql_solr[:sql_solr.find("SET")]
            elif sql.startswith("DELETE"):
                if sql_solr.find("WHERE") != -1:
                    sql_solr = sql_solr[:sql_solr.find("WHERE")]
            # print(sql_solr)
            # 查找访问库
            solr_access_url = self.solr_url + '/' + self.access_core[0]
            # print(solr_access_url)
            s = core.SolrConnection(solr_access_url)
            fq = '{!join from=id to=sqlid fromIndex=6 toIndex=' + self.access_core[0] + '}( combined_all:(' + sql_solr + ') )'
            q = "*:*"
            if len(self.time) > 0:
                q = "optime:[ " + self.time + " TO * ]"
            response = s.query(q=q, fq=fq, rows=10)

            access_result = response.results
            access_result = self.complete_sql(access_result)

            for result in access_result:
                if sql.upper() == result["sql_real"]:
                    flag = True
                    bingo_str = "find sql success " + sql.upper() + " in solr core " + self.access_core[0] + " id : " + result["id"]  # + "other info : " + str(result)
                    # print("bingo------bingo------bingo------bingo------bingo------bingo------bingo------")
                    break

            while (True):
                if flag == True:
                    break
                response = response.next_batch()
                if len(response.results) == 0:
                    break
                access_result = response.results
                access_result = self.complete_sql(access_result)
                for result in access_result:
                    # print(result["sql_real"])
                    # print(result['id'])
                    print(result)
                    if sql.upper() == result["sql_real"]:
                        flag = True
                        bingo_str = "find sql success " + sql.upper() + " in solr core " + self.access_core[0] + " id : " + result["id"]  # + "other info : " + str(result)
                        # print("bingo------bingo------bingo------bingo------bingo------bingo------bingo------")
            if flag:
                self.report.info(bingo_str, self.uuid)
            else:
                self.report.error("find sql error " + sql.upper() + " in solr core", self.uuid)
        # 向SQL库搜索
        # print("find_sqls_in_solr")
        pass


if __name__ == '__main__':
    dcap_solr = Dcap_solr()

    dcap_solr.solr_url = "http://192.168.60.99:8983/solr"

    dcap_solr.mysql_url = "192.168.60.99"

    dcap_solr.time = "2017-05-11T17:33:19Z"

    sql = "SELECT * FROM pubs.dbo.authors"

    if sql.find("WHERE") != -1:
        print("yes------------")
    else:
        print("no find-----------")
    sqls = []
    sqls.append("SELECT * FROM pubs.dbo.authors")
    sqls.append("INSERT INTO pubs.dbo.authors VALUES ( '100-10-1000', 'tengfei', 'chen', '083 879-9240', 'fengtanload', 'hangzhou', 'ZJ', '31000', 1 )")
    sqls.append("UPDATE pubs.dbo.authors SET city = 'shanghai' WHERE city = 'hangzhou' AND au_id = '100-10-1000'")
    sqls.append("DELETE FROM pubs.dbo.authors WHERE au_id = '100-10-1000'")
    dcap_solr.sqls = sqls

    dcap_solr.find_sqls_in_solr()
