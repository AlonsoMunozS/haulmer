#!/bin/bash
echo '{ "data" : ['

IP=`/bin/cat /etc/mailips |/bin/grep '*: '| /bin/awk '{print $2}'`
if [ -z "$IP" ];then
	IP=`hostname --ip-address`
fi

echo -n "{ \"{#IP}\" : \"${IP}\" }"

echo " ] }"
