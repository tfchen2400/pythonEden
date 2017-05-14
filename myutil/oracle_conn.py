import cx_Oracle

print("cx_Oracle.version:", cx_Oracle.clientversion())
dsn = cx_Oracle.makedsn("192.168.60.95", 1521, "wangzw")
conn = cx_Oracle.connect("tfchen", "tfchen", dsn)
cursor = cx_Oracle.Cursor(conn)
print("======")
sql = 'select * from common_user'
cursor.execute(sql)
for i in cursor:
    print(i)

cursor.close()
conn.close()
