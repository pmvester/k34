#!/bin/sh

did="k34Bbk"
dtype="K34Bbk"
orgId="m0cbg7"
token="1221080932"
topic="k34bbk"

r=$(/home/pi/git/k34/bbk/bbk_cli_linux_armhf-1.0 --quiet)
t=$(($(date +%s) * 1000))

l=$(echo $r | awk '{print $1}')
d=$(echo $r | awk '{print $2}')
u=$(echo $r | awk '{print $3}')
i=$(echo $r | awk '{print $4}')

ip=$(/sbin/ifconfig eth0 | grep 'inet ' | awk '{print $2}')
ea=$(/sbin/ifconfig eth0 | grep 'ether ' | awk '{print $2}')

json="{\"latency\": $l, \"download\": $d, \"upload\": $u, \"id\": \"$i\", \"timestamp\": $t, \"ip\": \"$ip\", \"mac\": \"$ea\"}"

hs=$orgId.messaging.internetofthings.ibmcloud.com
is="d:$orgId:$dtype:$did" 
ts="iot-2/evt/$topic/fmt/json" 

mosquitto_pub -h $hs -t $ts -m "$json" -i $is -P "$token" -u "use-token-auth" -q 1 

echo $json
