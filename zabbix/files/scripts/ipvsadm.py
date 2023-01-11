#!/bin/env python
# -*- coding: utf-8 -*-
#
# usage: ipvsadm.py acctiveconn tcp 172.18.0.12:80 172.17.0.22:80
import sys

def parserArgs(args):
    p = dict()
    if args[1] not in ('Conns', 'InPkts', 'OutPkts', 'InBytes', 'OutBytes') :
        print 'type error'
        sys.exit(1)
    p['type'] = args[1]
    p['proto'] = args[2].upper()
    vip = args[3].split(':')
    p['vip'] = vip[0]
    p['vipPort'] = vip[1]
    rip = args[4].split(':')
    p['rip'] = rip[0]
    p['ripPort'] = rip[1]
    #print p
    return p

def findData(args):
    vip = "%s  %s:%s" % (args['proto'], args['vip'], args['vipPort'])
    rip = "-> %s:%s" % (args['rip'], args['ripPort'])
    vipStr = None
    result = None
    for line in file("/tmp/ipvs_out"):
        line=line.strip()
        if line.startswith(vip):
            vipStr = True
            continue
        if vipStr is True and line.startswith(rip):
            break
    #  -> AC110016:0050      Masq    1      10         157
    import re
    values = re.split('\s+', line)
    #print values
    # ['', '->', 'AC110016:0050', 'Masq', '1', '0', '0', '']
    result = dict()
    result['Conns'] = values[2]
    result['InPkts'] = values[3]
    result['OutPkts'] = values[4]
    result['InBytes'] = values[5]
    result['OutBytes'] = values[6]

    return result[args['type']]

if __name__ == "__main__":
    args = parserArgs(sys.argv)
    print findData(args)

