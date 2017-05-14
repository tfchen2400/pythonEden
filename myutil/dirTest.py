import os

print(os.path.abspath('.'))
baseUrl = os.path.abspath('.')
url = os.path.join(baseUrl, "oraclelink", "2")
print(url)
