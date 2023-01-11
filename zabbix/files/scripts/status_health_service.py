#!/usr/bin/python
import json
import sys
import requests

data = requests.get('http://localhost:61001/system/health/v1')

datae2 = data.json()
data_string = json.dumps(datae2)
decoded = json.loads(data_string)

ID= sys.argv[1]
#ID = "dcos-docker-gc.timer"
#print "hostname "+str(decoded["hostname"])
#print "ip "+str(decoded["ip"])

for p in decoded["units"]:
    if p["id"] == ID:
        print(p["health"])
