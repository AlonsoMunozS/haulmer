#!/bin/bash

END_FLG=0

echo '{ "data" : ['

for IP in `/bin/cat /etc/ips_list_check_zabbix`
do
	if [ ${END_FLG} != 0 ] ; then
		echo ", "
	fi
	echo -n "{ \"{#IP}\" : \"${IP}\" }"
	END_FLG=1
done
echo " ] }"
