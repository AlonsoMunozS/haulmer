#!/bin/bash
ms=$(ping -c 1 $1 | tail -1| awk '{print $4}' | cut -d '/' -f 2)
if [ ! -z "$ms" ]
then
    	echo "$ms"
else
    	echo "-1"
fi
exit 0