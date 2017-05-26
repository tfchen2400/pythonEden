import cx_Oracle
import time

print("cx_Oracle.version:", cx_Oracle.clientversion())
dsn = cx_Oracle.makedsn("192.168.200.180", 1578, "orcl")
#conn = cx_Oracle.connect("scott", "scott", dsn, clientinfo="hahah", module="mycxoracle")
conn = cx_Oracle.connect("sys as sysdba", "oracle", dsn)
cursor = cx_Oracle.Cursor(conn)
print("======")
sql = "select * from dept where dname = :dname;select 1 from dual"
par = {}
par["dname"] = "ACCOUNTING"
print(par)
cursor.execute(sql, par)

for i in cursor:
    print(i)
cursor.close()
conn.close()
