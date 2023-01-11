#!/bin/env python
# -*- coding: utf-8 -*-
#
# usage: ipvsadm.py acctiveconn tcp 172.18.0.12:80 172.17.0.22:80
import sys
import re
def findData(type):
    totalStr = None
    connsStr = None
    result = None
    for line in file("/proc/net/ip_vs_stats"):
        line=line.strip()
        if totalStr and connsStr:
            break
        if line.startswith("Total"):
            totalStr = True
            continue
        if totalStr is True and line.startswith("Conns"):
            connsStr= True
            continue

    values = re.split('\s+', line)
    #print values
    result = dict()
    result['cps'] = values[0]
    result['inpps'] = values[1]
    result['outpps'] = values[2]
    result['inbps'] = values[3]
    result['outbps'] = values[4]
    return str(int(result[type], 16))

if __name__ == "__main__":
    if sys.argv[1] not in ('cps', 'inbps', 'inpps', 'outbps', 'outpps') :
        print 'type error'
        sys.exit(1)
    print findData(sys.argv[1])