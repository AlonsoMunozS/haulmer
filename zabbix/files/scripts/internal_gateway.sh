#! bin/sh
net=$(facter network_eth1)
mask=$(facter netmask_eth1)
broadcast=$(ipcalc -b $net $mask)
parse_broad=$(echo $broadcast | awk -F '=' '{ print $2 }')
gateway=$(echo $parse_broad | awk -F'.' -v OFS="." '$4=$4-1')
echo $gateway
