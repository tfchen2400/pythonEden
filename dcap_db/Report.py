#!/usr/bin/env python3
# coding=utf-8
"""
    这是报告的封装类
"""
import time


class Report(object):
    __instance = None

    level = "info"

    file = "d:/report.txt"

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if (Report.__instance is None):
            Report.__instance = object.__new__(cls, *args, **kwargs)
        return Report.__instance

    def warn(self, str2, str1="root"):
        if (self.level == "info" or self.level == "warn"):
            self.writeFile(str1, str2)
        pass

    def info(self, str2, str1="root"):
        if (self.level == "info"):
            self.writeFile(str1, str2)
        pass

    def error(self, str2, str1="root"):
        if (self.level == "info" or self.level == "warn" or self.level == "error"):
            self.writeFile(str1, str2)
        pass

    def writeFile(self, str1, str2):
        f = open(self.file, 'a+', encoding='utf8')
        str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\t' + self.level + '\t' + str1 + '\t' + str2;
        print(str)
        f.writelines(str + '\n')
        f.close()


if __name__ == '__main__':
    report = Report()
    report.warn("haha")
    report.writeFile("report", "123")
    report.writeFile("report2", "234")
