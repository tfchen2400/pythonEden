#!/usr/bin/env python3
# coding=utf-8
from my_redis.RedisHelper import RedisHelper

obj = RedisHelper()
obj.publish('hello123')  # 发布
