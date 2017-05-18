#!/user/bin/env python3
# coding=utf-8
from my_redis.RedisHelper import RedisHelper

obj = RedisHelper()
redis_sub = obj.subscribe()  # 调用订阅方法

while True:
    msg = redis_sub.parse_response()
    print(msg)
