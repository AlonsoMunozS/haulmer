#!/bin/bash

END_FLG=0

echo '{ "data" : ['

for IP in `route -n|grep "vtep1024"|grep -v "0.0.0.0"|awk '{print $2} '|sort|uniq`
do
  	if [ ${END_FLG} != 0 ] ; then
                echo ", "
        fi
	echo -n "{ \"{#IP}\" : \"${IP}\" }"
        END_FLG=1
done
echo " ] }"