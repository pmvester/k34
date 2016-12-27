#!/usr/bin/env python2.7
import MySQLdb as mdb
import RPi.GPIO as GPIO
import sys
import time
import paho.mqtt.publish as publish

from apscheduler.scheduler import Scheduler
from datetime import datetime
from datetime import timedelta

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)

# global counter holding number of pulses for a given time interval
pulses = 0

db = mdb.connect('localhost', 'logger', '13142k34', 'housedb')
cursor = db.cursor()

# callback function counting pulses
def my_callback(channel):
    global pulses
    pulses += 1

def publishData( power ):
    try:
        publish.single("k34/power", "{\"power\": %d, \"timestamp\": %d}" % (power, int(time.time())*1000), hostname="k34.mine.nu")
    except:
        pass

def logData():
    global pulses

    # sampling interval is 60 s so multiply by 60 to
    # convert from Wh to Ws i.e. J.
    sql = "INSERT INTO Data (power) VALUES (%d)" % (pulses * 60)
    try:
        cursor.execute(sql)
        db.commit()
        publishData( pulses * 60 )
        pulses = 0
    except:
        db.rollback()

try:
    GPIO.add_event_detect(23, GPIO.FALLING, callback=my_callback)

    sched = Scheduler()
    sched.start()

    sched.add_cron_job(logData, minute='*/1')

    while(True):
        time.sleep(3600.0)
except KeyboardInterrupt:
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit
