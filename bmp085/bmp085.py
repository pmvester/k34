import Adafruit_BMP.BMP085 as BMP085
import apscheduler
import sys
import time
import paho.mqtt.publish as publish

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from datetime import timedelta

sensor = BMP085.BMP085()

def publishData():
    json = '{"pressure": %f, "temperature": %f, "time": %d}' % (sensor.read_pressure(), sensor.read_temperature(), int(time.time())*1000)
    try:
        publish.single("k34/bmp085", json, hostname="k34.mine.nu")
    except:
        pass

try:
    sched = BackgroundScheduler()
    sched.start()

    sched.add_job(publishData, 'cron', minute='*/1')

    while(True):
        time.sleep(3600.0)
except KeyboardInterrupt:
    pass
