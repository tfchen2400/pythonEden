#!/usr/bin/env python3
# coding=utf-8
"""
    这是报告的封装类
"""
import time
import redis


class Report(object):
    __instance = None

    level = "info"

    file = "d:/report.txt"

    def __init__(self):
        try:
            self.pool = redis.ConnectionPool(host="192.168.60.95", port=6379, db=0, password="tfchen5211")
        except:
            self.pool = None

    def __new__(cls, *args, **kwargs):
        if (Report.__instance is None):
            Report.__instance = object.__new__(cls, *args, **kwargs)
        return Report.__instance

    def warn(self, str2, str1=""):
        if (self.level == "info" or self.level == "warn"):
            self.writeFile(str1, str2)
        pass

    def info(self, str2, str1=""):
        if (self.level == "info"):
            self.writeFile(str1, str2)
        pass

    def error(self, str2, str1=""):
        if (self.level == "info" or self.level == "warn" or self.level == "error"):
            self.writeFile(str1, str2)
        pass

    def writeFile(self, str1, str2):
        if self.pool == None:
            str1 = ""

        if (str1 != ""):
            r = redis.Redis(connection_pool=self.pool)
            str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\t' + self.level + '\t' + str2
            print(str)
            r.rpush(str1, str)
            pass
        else:
            f = open(self.file, 'a+', encoding='utf8')
            str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\t' + self.level + '\t' + str2
            print(str)
            f.writelines(str + '\n')
            f.close()

    # 获取list
    def getAllResult(self, uuid):
        r = redis.Redis(connection_pool=self.pool)
        res = r.lrange(uuid, 0, -1)

        res2 = [x.decode() for x in res]
        return res2


if __name__ == '__main__':
    report = Report()
    report.warn("haha")
    report.writeFile("report", "123")
    report.writeFile("report2", "234")
