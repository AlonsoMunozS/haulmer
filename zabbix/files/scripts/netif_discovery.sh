#!/bin/bash

interfaces=$(netstat -i | column -t | awk '{ print $1 }' | grep "em[0-9]\|p[0-9]\|eth[0-9]\|ens[0-9]")
last_interface=$(netstat -i | column -t | awk '{ print $1 }' | grep "em[0-9]\|p[0-9]\|eth[0-9]\|ens[0-9]" | tail -n 1)

echo -e "{"
echo -e "\t\"data\":[\n";

for netif in $interfaces; do

  echo -en "\t\t{ \"{#PHYSNET}\":\"$netif\"\t}"

  if [ -z $(echo "$netif" | grep "$last_interface") ]; then
     echo -en ","
  fi

  echo ""

done

echo -e  "\n\t]"
echo -e  "}"
