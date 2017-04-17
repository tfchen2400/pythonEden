#!/usr/bin/env python3
# coding=utf-8
"杭州美创抓周报的一个py"
__author__ = "陈腾飞(水言Dade)"
import requests
import re
import time


def login_web(people):
    timestr = time.strftime("%Y%m%d%H%M%S", time.localtime())
    f = open('weekReport' + timestr + '.txt', 'a', encoding='utf8')

    url = 'http://wiki.mchz.com.cn/login.action'
    # print(url)

    s = requests.session()
    loginURL = "http://wiki.mchz.com.cn/dologin.action"

    data = {"os_username": "chentf", "os_password": "abc123456", "os_destination": '/dashboard.action', 'login': '登录'}

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'}

    login = s.post(loginURL, data=data, headers=headers)

    for key in people:
        f.writelines(people[key] + '\n')
        afterURL = "http://wiki.mchz.com.cn/pages/viewpage.action?pageId="+key
        response = s.get(afterURL, cookies=login.cookies, headers=headers)

        responseUTF8 = response.content.decode("UTF-8")
        # print(responseUTF8)

        html = responseUTF8

        everyTable = re.findall('<div class="table-wrap".*?</div>', html, re.S)

        # 只要第一个
        lastWeekReport = everyTable[0]
        # print(lastWeekReport)

        # 取每行数据
        everyTr = re.findall('<tr>.*?</tr>', lastWeekReport, re.S)
        # print("---------------------------------------------------------------")
        # print(everyTr)

        for i, item in enumerate(everyTr):
            # print(i, item)
            evertTd = re.findall("<td.*?</td>", item, re.S)
            info = "";
            #print(evertTd)
            for j, td in enumerate(evertTd):
                # print(j, td)
                content = re.search('<strong>(.*?)</strong>', td, re.S)
                # 计划
                if (content):
                    content = content.group(1)
                    info = content
                    # print(content)
                else:
                    content = re.search('confluenceTd">(.*?)</td>', td, re.S)
                    content = content.group(1)
                    info = info + content + '\t'
                    #print(content)
            print(info)
            f.writelines(info + '\n')
            # print("---------------------")
        f.writelines("----------------------------------" + '\n')


if __name__ == '__main__':
    people = {"3081804": "陈腾飞", "2130626": "王薪水", "1475258": "戚益益"}
    for key in people:
        print(people[key])
    login_web(people)
