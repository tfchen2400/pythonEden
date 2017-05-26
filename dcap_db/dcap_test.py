import logging

from dcap_db.Db_info import Db_info
from dcap_db.Dcap_db import Dcap_db
from dcap_db.Dcap_main import Dcap_main

if __name__ == '__main__':
    logging.config.fileConfig("../logging.conf")

    # dcap_db = Dcap_db()
    # # db info
    # db_info = Db_info()
    # db_info.type = "msSql"
    # db_info.charset = "utf8"
    # db_info.database = "pubs"
    # db_info.user = "sa"
    # db_info.password = "Ctf12345"
    # db_info.host = "192.168.60.99"
    # db_info.port = "5211"
    #
    # dcap_db.dbinfo = db_info
    #
    # sqls = []
    # sqls.append("SELECT * FROM pubs.dbo.authors")
    # sqls.append("INSERT INTO pubs.dbo.authors VALUES ( '100-10-1000', 'tengfei', 'chen', '083 879-9240', 'fengtanload', 'hangzhou', 'ZJ', '31000', 1 )")
    # sqls.append("UPDATE pubs.dbo.authors SET city = 'shanghai' WHERE city = 'hangzhou' AND au_id = '100-10-1000'")
    # sqls.append("DELETE FROM pubs.dbo.authors WHERE au_id = '100-10-1000'")
    # dcap_db.sqls = sqls
    #
    # methods = []
    # # methods.append("pymssql")
    # # methods.append("odbc2000")
    # # methods.append("odbc2005")
    # # methods.append("odbc2008")
    # # methods.append("odbc2012")
    # # methods.append("odbc2014")
    # # methods.append("sqljdbc4")
    # methods.append("jtds13")
    # dcap_db.methods = methods
    #
    # print(dcap_db.dbinfo.host + "," + dcap_db.dbinfo.port)
    # # dcap_db.do_sqls_pymssql()
    # dcap_db.do_sqls()
    # print(sqls)


    dcap_db = Dcap_db()
    # db info
    db_info = Db_info()
    # db_info.type = "oracle"
    # db_info.database = "wangzw"
    # db_info.user = "scott"
    # db_info.password = "scott"
    # db_info.host = "192.168.60.95"
    # db_info.port = "1521"

    db_info.type = "oracle"
    db_info.database = "orcl"
    db_info.user = "scott"
    db_info.password = "scott"
    db_info.host = "192.168.200.179"
    db_info.port = "1521"

    dcap_db.dbinfo = db_info

    sqls = []
    # sql_info = {}
    # sql_info["sql"] = "select * from dept"
    # sql_info["par"] = {}
    # sqls.append(sql_info)
    #
    # sql_info = {}
    # sql_info["sql"] = "select * from dept where dname = :dname"
    # par = {}
    # par["dname"] = "ACCOUNTING"
    # sql_info["par"] = par
    #
    # sqls.append(sql_info)

    # sqls.append("select * from dept where dname = 'ACCOUNTING'")
    # sqls.append("INSERT INTO dept VALUES (11, 'chentf', 'hz')")
    # sqls.append("UPDATE dept SET dname = 'CHENTF_UPDATE' WHERE DEPTNO = 11")
    # sqls.append("DELETE dept WHERE DEPTNO = 11")


    # sql_info = {}
    # sql_info["sql"] = "INSERT INTO dept VALUES (:id, :dname, :city)"
    # par = {}
    # par["id"] = 11
    # par["dname"] = "chentf"
    # par["city"] = "hz"
    # sql_info["par"] = par
    # sqls.append(sql_info)
    #
    # sql_info = {}
    # sql_info["sql"] = "UPDATE dept SET dname = :dname WHERE DEPTNO = :id"
    # par = {}
    # par["id"] = 11
    # par["dname"] = "CHENTF_UPDATE"
    # sql_info["par"] = par
    # sqls.append(sql_info)

    sql_info = {}
    sql_info["sql"] = "DELETE dept WHERE DEPTNO = 11"
    par = {}
    sql_info["par"] = par
    sql_info["uuid"] = "123"
    sqls.append(sql_info)

    dcap_main = Dcap_main()
    dcap_main.uuid = "chentf"
    sqls = map(dcap_main.generate_sql_uuid, sqls)
    sqls = list(sqls)

    dcap_db.sqls = sqls
    dcap_db.uuid = "chentf"

    methods = []
    methods.append("cx_oracle")
    # methods.append("ojdbc14")
    # methods.append("classes12")
    # methods.append("ojdbc5")
    # methods.append("ojdbc6")
    # methods.append("ojdbc7")
    # methods.append("ojdbc8")

    dcap_db.methods = methods

    dcap_db.do_sqls()
