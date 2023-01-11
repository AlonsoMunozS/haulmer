#!/usr/bin/python
import json
import requests

data = requests.get('http://localhost:61001/system/health/v1')

datae2 = data.json()
data_string = json.dumps(datae2)
decoded = json.loads(data_string)

#print "hostname "+str(decoded["hostname"])
#print "ip "+str(decoded["ip"])
a = 0
print("{\"data\":[")
for p in decoded["units"]:
    if  a > 0:
                print(",")


    print("{ \"{#ID}\" : \""+p["id"]+"\" }")
    a += 1
print("]}")
