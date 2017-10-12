#!/usr/bin/env python3
# coding=utf-8
import redis
import time
import threading


# 普通连接
def notrans():
    conn = redis.Redis(host="192.168.59.163", port=6379, db=0, password="")
    pipeline = conn.pipeline()
    pipeline.incr('notrans:')
    time.sleep(1)
    pipeline.incr('notrans:', -1)
    print(pipeline.execute()[0])


if 1:
    for i in range(3):
        threading.Thread(target=notrans).start()
    time.sleep(5)
