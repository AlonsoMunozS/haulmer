#!/usr/bin/python
import json
import argparse
import sys
import re

with open('/tmp/json_container.json') as f:
    data = json.load(f)

def discover():
    d = {}
    d["data"] = []
    for key in data.iterkeys():
        ps = {}
        ps["{#CONTAINERID}"] = key
        ps["{#CONTAINERNAME}"] = data[key]["cont_name"]
        d["data"].append(ps)
    print (json.dumps(d))

if __name__ == "__main__":
    if len(sys.argv) > 2:
        parser = argparse.ArgumentParser(prog="discover.py", description="discover and get stats from docker containers")
        parser.add_argument("container", help="container id")
        parser.add_argument("stat", help="container stat", choices=["cont_name","status","disk_usage","cpu_usage","memo_usage","tx_dropped","tx_errors","tx_packets","tx_bytes","rx_dropped","rx_errors","rx_packets","rx_bytes","memory_total","cpu_total"])
        args = parser.parse_args()
        m = re.match("(^[a-zA-Z0-9-_]+$)", args.container)
        if not m:
            print ("Invalid parameter for container id detected")
            debug("Invalid parameter for container id detected" + str(args.container))
            sys.exit(2)
        if args.stat == "cont_name":
            print data[args.container]["cont_name"]
        elif args.stat == "status":
            print data[args.container]["status"]
        elif args.stat == "memory_total":
            print data[args.container]["memory_total"]
        elif args.stat == "cpu_total":
            print data[args.container]["cpu_total"]
        elif args.stat == "memo_usage":
            print data[args.container]["stats"]["memo_usage"]
        elif args.stat == "disk_usage":
            print data[args.container]["stats"]["disk_usage"]
        elif args.stat == "cpu_usage":
            print data[args.container]["stats"]["cpu_usage"]
        elif args.stat == "tx_dropped":
            print data[args.container]["network"]["tx_dropped"]
        elif args.stat == "rx_packets":
            print data[args.container]["network"]["rx_packets"]
        elif args.stat == "rx_errors":
            print data[args.container]["network"]["rx_errors"]
        elif args.stat == "rx_bytes":
            print data[args.container]["network"]["rx_bytes"]
        elif args.stat == "tx_errors":
            print data[args.container]["network"]["tx_errors"]
        elif args.stat == "tx_bytes":
            print data[args.container]["network"]["tx_bytes"]
        elif args.stat == "rx_dropped":
            print data[args.container]["network"]["rx_dropped"]
        elif args.stat == "tx_packets":
            print data[args.container]["network"]["tx_packets"]

    else: discover()
