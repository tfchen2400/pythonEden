#!/usr/bin/env python3
# coding=utf-8
import json

from dcap_db.Db_info import Db_info
from dcap_db.Dcap_main import Dcap_main

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
# servers.append(db_info.__dict__)
servers.append(db_info2.__dict__)

clients = []
# clients.append("pymssql")
# clients.append("SQL server 2005")
# clients.append("SQL server 2008")
# clients.append("SQL server 2012")
# clients.append("SQL server 2014")
clients.append("sqlcmd SQL server 2005")
clients.append("sqlcmd SQL server 2008")
clients.append("sqlcmd SQL server 2012")
clients.append("sqlcmd SQL server 2014")
# clients.append("sqljdbc4")
# clients.append("jtds13")

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
dcap_main.exec_all(jsonStrFile)
