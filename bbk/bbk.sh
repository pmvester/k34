#!/bin/sh

r=$(/home/pi/git/k34/bbk/bbk_cli_linux_armhf-1.0 --quiet)
l=$(echo $r | cut -d ' ' -f 1)
d=$(echo $r | cut -d ' ' -f 2)
u=$(echo $r | cut -d ' ' -f 3)
i=$(echo $r | cut -d ' ' -f 4)
t=$(($(date +%s) * 1000))
json="{\"latency\": $l, \"download\": $d, \"upload\": $u, \"id\": \"$i\", \"timestamp\": $t}"
mosquitto_pub -h k34.mine.nu -t "k34/bbk" -m "$json"
echo $json
