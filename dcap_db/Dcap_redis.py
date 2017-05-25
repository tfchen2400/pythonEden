#!/usr/bin/env python3
# coding=utf-8
"""
    redis操作
"""
import redis


class Dcap_redis(object):
    __instance = None

    def __init__(self):
        try:
            self.pool = redis.ConnectionPool(host="192.168.60.95", port=6379, db=0, password="tfchen5211")
        except Exception as e:
            print('Error:', e)
            self.pool = None

    def getRedis(self):
        return redis.Redis(connection_pool=self.pool)
