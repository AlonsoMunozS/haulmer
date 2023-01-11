#! /bin/sh

DEBUG=0
if [ $DEBUG -gt 0 ]
then
    exec 2>>/tmp/my_ssl_script.log
    set -x
fi

f=$1
host=$2
port=443
server=$2

case $f in
d)
end_ssl_date=`openssl s_client -servername $server -host $host -port $port -prexit </dev/null 2>/dev/null | openssl x509 -noout -dates | grep notAfter | cut -d'=' -f2`
ssl_sec=`date -d "$end_ssl_date" +'%s'`
now=`date '+%s'`
echo "($ssl_sec - $now) / 24 / 3600" | bc
;;

i)
issue_dn=`openssl s_client -servername $server -host $host -port $port -prexit </dev/null 2>/dev/null  | openssl x509 -noout -issuer| sed -n 's/.*CN=*//p'`
echo $issue_dn
;;

*)
echo "usage: $0 [-i|-d] hostname port"
echo "    -i Show Issuer"
echo "    -d Show days remaining"
;;
esac
