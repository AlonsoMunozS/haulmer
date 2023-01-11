#!/root/haulmer_hosting_apps/python_env_assp_mail_scripts/bin/python
# -*- coding: UTF-8 -*-
# By Eliseo Basualto

import os
from datetime import datetime
import sys
#import argparse

#variables globales
eximstats_db = "/var/cpanel/eximstats_db.sqlite3"
exim_mainlog = "/var/log/exim_mainlog"
exim_rejectlog = "/var/log/exim_rejectlog"
now = datetime.now()
today = now.strftime('%Y-%m-%d')


def get_send_email_today():
    total_send = os.popen("cat /var/log/exim_mainlog |grep '"+today+"' |grep 'A\=dovecot_login' |awk '{print $3}' |wc -l").read()
    return total_send

def get_email_queue():
    email_queue = os.popen("exim -bpc").read()
    return email_queue

def detalle_send_email():
    detalle_total_send = os.popen("cat /var/log/exim_mainlog |grep '"+today+"' |grep 'A\=dovecot_login' |awk -F'A=dovecot_login:' {'print $2'} |cut -f1 -d' ' |sort |uniq -c |sort -n |awk {'print $1, ' correos enviados por ' , $2'}')").read()
    return detalle_total_send

#test para zabbix
def message_arrival():
	count = os.popen("grep \" <= \" /var/log/exim_mainlog |grep '"+today+"' |awk '{print $3}'|sort |uniq |wc -l").read()
	return count

def message_fakereject():
	count = os.popen("grep \" (= \" /var/log/exim_mainlog |grep '"+today+"' |awk '{print $3}' |sort |uniq |wc -l").read()
	return count

def normal_message_delivery():
	count = os.popen("grep \" => \" /var/log/exim_mainlog |grep '"+today+"' |awk '{print $3}' |sort |uniq |wc -l").read()
	return count

def additional_address_in_same_delivery():
	count = os.popen("grep \" -> \" /var/log/exim_mainlog |grep '"+today+"' |awk '{print $3}' |sort |uniq |wc -l").read()
	return count

def cutthrough_message_delivery():
	count = os.popen("grep \" >> \" /var/log/exim_mainlog |grep '"+today+"' |awk '{print $3}' |sort |uniq |wc -l").read()
	return count

def delivery_suppressed():
	count = os.popen("grep '"+today+"' /var/log/exim_mainlog |awk '{print $3, $4}' |sort |uniq |grep \"*>\" |wc -l").read()
	return count

def delivery_failed():
	count = os.popen('grep "'+today+'" /var/log/exim_mainlog |awk \'{print $3, $4}\' |sort |uniq |grep "^*\*" |wc -l').read()
	return count

def delivery_deferred():
	count = os.popen("grep \" == \" /var/log/exim_mainlog |grep '"+today+"' |awk '{print $3, $4}' |sort |uniq |wc -l").read()
	return count

# -- debug --
#conexiones activas por IP
#conexiones activas por imap
#conexiones activas por pop

#estadisticas de fallidos

def main():
	sys.argv

	if sys.argv[1] == "arrival":
		print(message_arrival())
	elif sys.argv[1] == "fakereject":
		print(message_fakereject())
	elif sys.argv[1] == "delivery":
		print(normal_message_delivery())
	elif sys.argv[1] == "additional_address":
		print(additional_address_in_same_delivery())
	elif sys.argv[1] == "cutthrough":
		print(cutthrough_message_delivery)
	elif sys.argv[1] == "suppressed":
		print(delivery_suppressed())
	elif sys.argv[1] == "failed":
		print(delivery_failed())
	elif sys.argv[1] == "deferred":
		print(delivery_deferred())



if __name__ == '__main__':
        main()
