import os
import json
print(os.path.abspath('.'))
baseUrl = os.path.abspath('.')
url = os.path.join(baseUrl, "oraclelink", "2")
print(url)

par = {}
par["id"] = 11
par["dname"] = "chentf"
par["city"] = "hz"

print(json.dumps(par))


