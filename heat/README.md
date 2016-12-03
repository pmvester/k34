# add these two lines to /etc/rc.local
```sleep 30 && /home/pi/git/k34/heat/water.sh >> /dev/null 2>&1 &
printf "k34 home automation heat water monitor started\n"```
