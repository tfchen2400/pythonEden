#!/usr/bin/env python3
# coding=utf-8
"杭州美创抓周报的一个py"
__author__ = "陈腾飞(水言Dade)"
import requests
import re
import time
import os
import zipfile
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import shutil


def remove_file():
    htmlFileList = [x for x in os.listdir('.') if os.path.isfile(x) and (os.path.splitext(x)[1] == '.html')]
    for x in htmlFileList:
        targetFile = os.path.join(os.path.abspath('.'), 'oldWeekReport', x)
        shutil.copyfile(x, targetFile)
    fileList = [x for x in os.listdir('.') if
                os.path.isfile(x) and (os.path.splitext(x)[1] == '.html' or os.path.splitext(x)[1] == '.zip')]
    for x in fileList:
        os.remove(x)


def zip_file():
    timestr = time.strftime("%Y%m%d%H%M%S", time.localtime())
    filename = 'weekReport' + timestr + '.zip'  # 压缩后的文件名
    z = zipfile.ZipFile(filename, "w", zipfile.ZIP_DEFLATED)
    fileList = [x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1] == '.html']
    for x in fileList:
        z.write(x)
    cssDir = os.path.join(os.path.abspath('.'), 'css')
    cssFile = os.path.join(cssDir, 'table.css')
    start = cssDir.rfind(os.sep) + 1
    z.write(cssFile, cssFile[start:])
    z.close()


def login_web(people):
    timestr = time.strftime("%Y%m%d%H%M%S", time.localtime())
    f = open('weekReport' + timestr + '.html', 'a', encoding='utf8')

    url = 'http://wiki.mchz.com.cn/login.action'
    # print(url)

    s = requests.session()
    loginURL = "http://wiki.mchz.com.cn/dologin.action"

    data = {"os_username": "chentf", "os_password": "abc123456", "os_destination": '/dashboard.action', 'login': '登录'}

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'}

    login = s.post(loginURL, data=data, headers=headers)

    f.writelines("<!DOCTYPE HTML>")
    f.writelines("<html>")
    f.writelines("<head>")
    f.writelines("<link rel='stylesheet' href='css/table.css' /> ")
    f.writelines("</head>")
    f.writelines("<body>")
    for k, v in people:
        # print(people[key])
        f.writelines("---------------------------------------------------" + '</br>')
        f.writelines(v + '\n')
        afterURL = "http://wiki.mchz.com.cn/pages/viewpage.action?pageId=" + k
        response = s.get(afterURL, cookies=login.cookies, headers=headers)

        responseUTF8 = response.content.decode("UTF-8")
        # print(responseUTF8)

        html = responseUTF8

        everyTable = re.findall('<div class="table-wrap".*?</div>', html, re.S)

        # 只要第一个
        lastWeekReport = everyTable[0]
        # print("||||||||||||||||||||||||||")
        # print(lastWeekReport)
        f.writelines(lastWeekReport)
        # print("||||||||||||||||||||||||||")
        """
        # 取每行数据
        everyTr = re.findall('<tr>.*?</tr>', lastWeekReport, re.S)
        # print("---------------------------------------------------------------")
        # print(everyTr)

        for i, item in enumerate(everyTr):
            # print(i, item)
            evertTd = re.findall("<td.*?</td>", item, re.S)
            info = "";
            # print(evertTd)
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
                    # print(content)
            print(info)
            f.writelines(info + '\n')
            # print("---------------------")
        f.writelines("----------------------------------" + '\n')
        """
    f.writelines("</body>")
    f.writelines("</html>")


def send_email():
    # 第三方 SMTP 服务
    mail_host = "smtp.qq.com"  # 设置服务器
    mail_user = "tfchen5211@foxmail.com"  # 用户名
    mail_pass = "ptsptmkqzrxoiacf"  # 口令

    sender = 'tfchen5211@foxmail.com'
    receivers = ['1102414893@qq.com']
    receivers = ['zuoy@mchz.com.cn']

    timestr = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())

    # 创建一个带附件的实例
    message = MIMEMultipart()
    message['From'] = Header("tfchen5211@foxmail.com", 'utf-8')
    message['To'] = Header(receivers[0], 'utf-8')
    subject = 'Python' + timestr + '抓取的周报信息'
    message['Subject'] = Header(subject, 'utf-8')

    # 邮件正文内容
    message.attach(MIMEText('这是' + subject, 'plain', 'utf-8'))

    fileList = [x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1] == '.zip']
    # print (fileList[0])

    att1 = MIMEText(open(fileList[0], 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    att1["Content-Disposition"] = 'attachment; filename="' + timestr + '.rar"'
    message.attach(att1)

    smtpObj = smtplib.SMTP_SSL(mail_host, 465)
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())
    print("邮件发送成功")


def sort_by_value(d):
    items = d.items()
    backitems = [[v[1], v[0]] for v in items]
    backitems.sort()
    return [backitems[i][1] for i in range(0, len(backitems))]


def do_all():
    people = {"10847541": "卓勇", "1475258": "戚益益", "1474740": "陈晴", "9437272": "王舒豪", "1474730": "王兆伟", "3081804": "陈腾飞",
              "3080831": "方格", "2654685": "林华兴"}
    L = sorted(people.items(), key=lambda d: d[1], reverse=True)
    remove_file()
    login_web(L)
    zip_file()
    send_email()


if __name__ == '__main__':
    people = {"10847541": "卓勇", "1475258": "戚益益", "1474740": "陈晴", "9437272": "王舒豪", "1474730": "王兆伟", "3081804": "陈腾飞",
              "3080831": "方格", "2654685": "林华兴"}
    L = sorted(people.items(), key=lambda d: d[1], reverse=True)
    remove_file()
    login_web(L)
    zip_file()
    send_email()
