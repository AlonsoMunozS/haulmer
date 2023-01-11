#!/usr/bin/python
#
# Copyright (c) 2015, Cristian Greco <cristian@regolo.cc>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   1. Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#
#   2. Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
#
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#   AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#   IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#   ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
#   LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#   CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
#   SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
#   INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
#   CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#   ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#   POSSIBILITY OF SUCH DAMAGE.
import sys
import ast
import os

__version__ = '1.0.0'
__author__ = 'cristian@regolo.cc'

PLUGIN_NAME = 'softirqs'
COLLECTD_VALUE_TYPE = 'derive'

class SoftIrqs(object):

    def __init__(self):
        self.list = []
        self.blacklist = False
        self.verbose = False

    def config_callback(self, conf):
        """
        Configuration callback.
        """
        for node in conf.children:
            if node.key == 'Softirq':
                self.list.append(node.values[0])
            elif node.key == 'IgnoreSelected':
                self.blacklist = bool(node.values[0])
            elif node.key == 'Verbose':
                self.verbose = bool(node.values[0])
            else:
                self.error('Unknown config key: %s' % node.key)

    def read_callback(self):
        """
        Read callback that parses data and call dispatch.
        """
        self.log('Read callback invoked')
        data = self.fetch_data()
        self.dispatch_values(data)

    @staticmethod
    def fetch_data():
        """
        Parse softirqs data from /proc filesystem.
        :returns: a dictionary of softirqs names and values
        :rtype: dictionary
        """
        data = {}
        with open('/proc/softirqs') as f:
            # get cpu count from the first line
            cpus = len(f.readline().split())

            for l in f.readlines():
                fields = l.split()
                fields_num = len(fields)

                if (fields_num) < 2:
                    continue

                # first column is softirq name and colon
                name = fields[0][:-1]

                # sum all per-cpu values
                all_values = map(int, fields[1:])
                value = sum(all_values)

                data[name] = value
        return data

    def dispatch_values(self, data):
        """
        Dispatch value to collectd.
        :param data: the dictionary of names and values to dispatch
        :type data: dictionary
        """
        for name, value in data.items():
            if self.match(name):
                self.log('%s:%s' % (name, value))
                val = collectd.Values()
                val.plugin = PLUGIN_NAME
                val.type = COLLECTD_VALUE_TYPE
                val.type_instance = name
                val.values = [value,]
                val.dispatch()

    def match(self, softirq):
        """
        Check whether a softirq should be collected.
        :param softirq: the name of the softirq to check
        :type softirq: string
        :returns: True if the softirq should be collected, False otherwise
        :rtype: boolean
        """
        if not self.list:
            return True
        if self.blacklist:
            return True if softirq not in self.list else False
        else:
            return True if softirq in self.list else False

    def log(self, msg):
        if self.verbose:
            collectd.info('%s: %s' % (PLUGIN_NAME, msg))

    def error(self, msg):
        collectd.error('%s: [error] %s' % (PLUGIN_NAME, msg))

def get_current_data():
    return SoftIrqs.fetch_data()

def get_latest_data(log):
    if not os.path.exists(log):
        return False
    with open(log, 'r') as f:
        latest_data = ast.literal_eval(f.read()) #load latest data

    if not latest_data:
        return False
    else:
        return latest_data

def log_data(log, data):
    file_latest = open(log,"w")
    file_latest.write(str(data))
    file_latest.close()

if __name__ == '__main__':
    log = "/tmp/latest_irq.log"
    data = SoftIrqs.fetch_data() #load current data
    latest_data = get_latest_data(log) #load latest check data 
    if not latest_data: #if not exist latest data, write current data to log
        log_data(log, data)
        latest_data = get_latest_data(log) #load latest check data 

    keys =  data.keys()
    if len(sys.argv) > 1:
        action = sys.argv[1]
        if action == "list": #Lista todos los items de softirq, current data
            out_data = ""
            for i, val in enumerate(keys):
                out_data+="\n"
                out_data+="""{"{#SOFTIRQ}": "%s"}""" % val
                out_data+=","
            print """{"data": [%s\n]}""" % out_data.strip(",")

        elif action in keys: #Obtiene el valor por la KEY dada
            ## print "latest: %s %s" % (action, latest_data[action])
            ## print "current: %s %s" % (action, data[action])
            print (data[action] - latest_data[action]) #get diff 
    else:
        print data

    log_data(log, data) #log data to log file
else:
    import collectd
    s = SoftIrqs()
    collectd.register_config(s.config_callback)
    collectd.register_read(s.read_callback)