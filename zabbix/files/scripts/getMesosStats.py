#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import urllib2
import json
import argparse

f = os.popen('ifconfig eth0 | awk \'/inet /{print substr($2,1)}\'')
ip_add=f.read()

tring = ip_add.replace('\r', '').replace('\n', '')

def get_metric(port,metric):
        port=port
        response = urllib2.urlopen('http://%s:%s/metrics/snapshot' % (tring,port))
        data = json.load(response)
        # print json.dumps(data, indent=4, sort_keys=True)
        try:
            print data[metric]
        except KeyError:
            print "ZBX_NOT_SUPPORTED"


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(
        description='Mesos metrics')
    arg_parser.add_argument(
        '-p', '--port', help="Specify mesos api port", required=True)
    arg_parser.add_argument(
        '-m', '--metric', help="Specify metric's name", required=True)

    arguments = arg_parser.parse_args()
    get_metric(arguments.port,arguments.metric)
