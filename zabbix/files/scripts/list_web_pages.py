#!/usr/bin/python
import json
data = ['panel.bluehosting.host','panel.boxhosting.host','panel.hosty.host','panel.livehost.host','panel.opencloud.host','panel.rackeo.host','panel.sitiohost.host','panel.solucionhost.host','www.10mejoreshosting.cl','www.10mejoreshosting.pe','www.bluehosting.cl','www.bluehosting.com.co','www.bluehosting.pe','www.boxhosting.cl','www.boxhosting.pe','www.cotizarhosting.cl','www.hosty.cl','www.livehost.cl','www.livehost.pe','www.opencloud.cl','www.rackeo.cl','www.rackeo.com','www.rackeo.pe','www.sitiohost.cl','www.sitiohost.pe','www.solucionhost.cl','www.solucionhost.pe']

vec2json = json.dumps(data)

decoded = json.loads(vec2json)

a=0
print("{\"data\":[")
for p in decoded:
    if  a > 0:
               print(",")

    print("{ \"{#SITIO}\" : \""+ decoded[a]+"\" }")
    a += 1
print("]}")
