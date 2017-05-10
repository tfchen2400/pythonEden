#!/usr/bin/env python3
# coding=utf-8

"dbinfo 存放数据库连接信息"
class Db_info(object):

    type = ""

    host = ""

    port = ""

    user = ""

    password = ""

    database = ""

    charset = ""

    def __init__(self):
        pass
if __name__ == '__main__':
    db_info = Db_info()
