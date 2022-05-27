#!/bin/sh

# add the following entry to /etc/rc.local
# sudo -u pi /home/pi/git/k34/bme280/bme280-app.sh >> /home/pi/git/k34/bme280/bme280-app.log 2>&1 &

python3 /home/pi/git/k34/bme280/bme280-app.py
