#!/usr/bin/env python3
# coding=utf-8
import pymssql

conn = pymssql.connect(host="192.168.60.109", port=1433, user="sa", password="Ctf12345", database="pubs",
                       charset="utf8", autocommit=True)
cursor = conn.cursor()
if not cursor:
    raise (NameError, "数据库连接失败")
    self.report.error("数据库连接失败")
    sql = "SELECT * FROM pubs.dbo.authors"
    # print("runsql", sql)
    try:
        cursor.execute(sql)
        # print("runsql", "success", sql)
        self.report.info("runsql" + " success " + sql)
    except Exception as e:
        print('Error:', e)
        self.report.error("runsql" + " error " + sql)
cursor.close()
conn.close()
