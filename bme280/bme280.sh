#!/bin/sh

# add the following entry to /etc/rc.local
# sudo -u pi /home/pi/git/k34/bme280/bme280.sh >> /home/pi/git/k34/bme280/bme280.log 2>&1 &

python /home/pi/git/k34/bme280/bme280.py
