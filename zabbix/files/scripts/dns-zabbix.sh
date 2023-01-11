#!/bin/sh
if test -z "$1"; then
    echo "You need to supply a DNS server and IP to check"
    exit 0;
fi

DNS_SERVER=$1
IP_HOST=$(ip -f inet a show eth1| grep inet| awk '{ print $2}' | cut -d/ -f1)

MYTIME=$(dig @$DNS_SERVER -x $IP_HOST | grep "Query time:"| egrep -o '[0-9]+')
if [ $? -eq 0 ]; then
    echo $MYTIME
else
    echo -1
fi
