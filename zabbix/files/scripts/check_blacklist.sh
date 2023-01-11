#!/bin/bash
if [[ $# -ne 2 ]]; then
        echo "Usage: ./${0##*/} <hostname> <blacklist service>"
        exit 1
fi
######################
######################
######################
#######AGREGAR  IVMSIP IVMSIP24 #####
######################
######################
######################
# Retrieves A record for hostname ($1)
HOSTLOOKUP="$1"
# Converts resolved IP into reverse IP
REVIP=`/bin/sed -r 's/([0-9]+)\.([0-9]+)\.([0-9]+)\.([0-9]+)/\4.\3.\2.\1/' <<< ${HOSTLOOKUP##*[[:space:]]}`
# Performs the actual lookup against blacklists
CHECK=`/usr/bin/host -W 2 -t a $REVIP.$2`
if echo $CHECK | grep -q "has address" >> /dev/null;then
        ((listed++))
        echo $listed
else
        echo "0"
fi
exit 0
