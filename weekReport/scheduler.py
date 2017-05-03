#!/usr/bin/env python3
# coding=utf-8
from apscheduler.schedulers.background import BackgroundScheduler
from weekReport import weekReportHzmc
import time

scheduler = BackgroundScheduler()
print('start to sleep')

scheduler.add_job(weekReportHzmc.do_all, 'cron', day_of_week='mon-sun', hour='*', minute='0-59', second='*/30')
scheduler.start()
while True:
    time.sleep(1*60*60)  # 其他任务是独立的线程执行
