import os
import json

import simplejson

from dcap_db.Dcap_redis import Dcap_redis

print(os.path.abspath('.'))
baseUrl = os.path.abspath('.')
url = os.path.join(baseUrl, "oraclelink", "2")
print(url)

par = {}
par["id"] = 11
par["dname"] = "chentf"
par["city"] = "hz"

print(json.dumps(par))

str = Dcap_redis().getRedis().hget("1sql", "89635550-41e8-11e7-b982-00e04c10d44e")
sql_info_json = simplejson.loads(str)

print(sql_info_json)


