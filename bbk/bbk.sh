#!/bin/sh

r=$(/home/pi/git/k34/bbk/bbk_cli_linux_armhf-1.0 --quiet)
t=$(($(date +%s) * 1000))

l=$(echo $r | awk '{print $1}')
d=$(echo $r | awk '{print $2}')
u=$(echo $r | awk '{print $3}')
i=$(echo $r | awk '{print $4}')

ip=$(/sbin/ifconfig eth0 | grep 'inet ' | awk '{print $2}')
ea=$(/sbin/ifconfig eth0 | grep 'ether ' | awk '{print $2}')

json="{\"latency\": $l, \"download\": $d, \"upload\": $u, \"id\": \"$i\", \"timestamp\": $t, \"ip\": \"$ip\", \"mac\": \"$ea\"}"
mosquitto_pub -h k34.mine.nu -t "k34/bbk" -m "$json"
echo $json
