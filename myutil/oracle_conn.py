import cx_Oracle
import time

print("cx_Oracle.version:", cx_Oracle.clientversion())
dsn = cx_Oracle.makedsn("192.168.60.95", 1521, "wangzw")
#conn = cx_Oracle.connect("scott", "scott", dsn, clientinfo="hahah", module="mycxoracle")
conn = cx_Oracle.connect("scott", "scott", dsn)
cursor = cx_Oracle.Cursor(conn)
print("======")
sql = "select * from dept where dname = :dname"
par = {}
par["dname"] = "ACCOUNTING"
print(par)
cursor.execute(sql, par)

for i in cursor:
    print(i)
cursor.close()
conn.close()
