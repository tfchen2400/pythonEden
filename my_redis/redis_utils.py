#!/usr/bin/env python3
# coding=utf-8
import json
import pickle
import redis

# 普通连接
r = redis.Redis(host="192.168.59.162", port=6379, db=0, password="tfchen5211")
r.set("wein", "tiancai2")
var_wenn = r.get("wein")
var_wenn = str(var_wenn, "utf-8")
print(var_wenn)
print(str(r.get("chentf"), "utf-8"))

pass

r = redis.Redis(host="192.168.60.95", port=6379, db=0, password="tfchen5211")
r.set("wein", "tiancai2")
var_wenn = r.get("wein")
var_wenn = str(var_wenn, "utf-8")
print(var_wenn)
print(str(r.get("chentf"), "utf-8"))

# 连接池
pool = redis.ConnectionPool(host="192.168.60.95", port=6379, db=0, password="tfchen5211")
r = redis.Redis(connection_pool=pool)
r.set('name', 'zhangsan')  # 添加
print(r.get('name'))  # 获取

# 管道
pipe = r.pipeline(transaction=True)

r.set('name', 'zhangsan')
r.set('name', 'lisi')

pipe.execute()

# 批量插入
r.mset({"hzh": 'superman11', "zy": 'dist111'})

# 批量获取
li = ["chentf", "wein"]
print(r.mget(li))

# hash操作
r.hset("citys", "hz", "hangzhou")
r.hset("citys", "sh", "shanghai")

dic = {"bj": "beijin", "sc": "sichuan"}
r.hmset("citys", dic)

# list
r.lpush("list_chentf", 2)
r.lpush("list_chentf", 3, 4, 5)

d = dict(name='Bob', age=20, score=88)
print(d)
print(pickle.dumps(d))
r.set("dict", pickle.dumps(d))

redis_dict = r.get("dict")
print(pickle.loads(redis_dict))

#
print("----------------------------------")
r.lpush("list_chentf", 2)
res = r.lrange("c9f2e894-3f66-11e7-af2f-00e04c10d44e", 0, -1)
print(res)
res2 = [x.decode('utf8') for x in res]

print(res2)
